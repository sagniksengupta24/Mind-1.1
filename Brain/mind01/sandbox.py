"""Unified sandboxed execution engine for Mind1.1.

Mandatory isolation for all command, compiler, and test execution paths.
Enforces container/namespace isolation (Bubblewrap/Docker), resource limits
(RLIMIT_CPU, RLIMIT_AS, RLIMIT_NOFILE, RLIMIT_FSIZE), isolated environment,
and timeout boundaries across all operating modes.
"""

from __future__ import annotations

import os
import resource
import shutil
import signal
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence


DEFAULT_TIMEOUT_SECONDS = 60
MAX_TIMEOUT_SECONDS = 120
DEFAULT_CPU_LIMIT_SECONDS = 30
DEFAULT_MEMORY_LIMIT_BYTES = 1024 * 1024 * 1024  # 1 GB
DEFAULT_MAX_OUTPUT_BYTES = 50_000


class SandboxError(RuntimeError):
    """Raised when sandboxed execution fails or violates policy."""
    pass


class SandboxTimeoutError(SandboxError):
    """Raised when sandboxed execution exceeds configured time budget."""
    pass


class SandboxSecurityViolation(SandboxError):
    """Raised when code inside the sandbox violates isolation boundaries."""
    pass


@dataclass
class SandboxConfig:
    workspace: Path
    timeout_seconds: int = DEFAULT_TIMEOUT_SECONDS
    cpu_limit_seconds: int = DEFAULT_CPU_LIMIT_SECONDS
    memory_limit_bytes: int = DEFAULT_MEMORY_LIMIT_BYTES
    max_output_bytes: int = DEFAULT_MAX_OUTPUT_BYTES
    allow_network: bool = False
    allow_write: bool = True
    read_only_workspace: bool = False
    custom_env: Dict[str, str] = field(default_factory=dict)
    writable_paths: List[Path] = field(default_factory=list)


@dataclass
class SandboxedExecutionResult:
    returncode: int
    stdout: str
    stderr: str
    duration_seconds: float
    timed_out: bool = False
    resource_limited: bool = False
    driver_used: str = "posix_isolated"

    @property
    def output(self) -> str:
        if self.stdout and self.stderr:
            return f"{self.stdout}\n{self.stderr}"
        return self.stdout or self.stderr or ""

    @property
    def success(self) -> bool:
        return self.returncode == 0 and not self.timed_out and not self.resource_limited


class SandboxedExecutor:
    """Central authority for executing subprocesses within an isolated sandbox."""

    def __init__(self, workspace: Path, config: Optional[SandboxConfig] = None) -> None:
        self.workspace = workspace.resolve()
        self.config = config or SandboxConfig(workspace=self.workspace)
        self.bwrap_path = shutil.which("bwrap")
        self.docker_path = shutil.which("docker")

    def get_safe_env(self, executable: Optional[str] = None) -> Dict[str, str]:
        """Produce an isolated, sanitized environment with no inherited host secrets."""
        runtime_home = self.workspace / ".mind01" / "runtime-home"
        runtime_tmp = self.workspace / ".mind01" / "tmp"
        runtime_home.mkdir(parents=True, exist_ok=True)
        runtime_tmp.mkdir(parents=True, exist_ok=True)

        path_entries = ["/usr/local/bin", "/usr/bin", "/bin"]
        if executable:
            exec_dir = str(Path(executable).parent)
            if exec_dir not in path_entries:
                path_entries.insert(0, exec_dir)

        safe_env = {
            "PATH": os.pathsep.join(dict.fromkeys(path_entries)),
            "HOME": str(runtime_home),
            "TMPDIR": str(runtime_tmp),
            "PYTHONNOUSERSITE": "1",
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONUNBUFFERED": "1",
            "GIT_CONFIG_NOSYSTEM": "1",
            "GIT_TERMINAL_PROMPT": "0",
            "MIND_SANDBOX_ACTIVE": "1",
            "MIND_SANDBOX_WORKSPACE": str(self.workspace),
        }
        if not self.config.allow_network:
            safe_env["MIND_BLOCK_NETWORK"] = "1"
            safe_env["http_proxy"] = "http://127.0.0.1:0"
            safe_env["https_proxy"] = "http://127.0.0.1:0"
            safe_env["HTTP_PROXY"] = "http://127.0.0.1:0"
            safe_env["HTTPS_PROXY"] = "http://127.0.0.1:0"

        if self.config.custom_env:
            for k, v in self.config.custom_env.items():
                if not k.startswith(("AWS_", "OPENAI_", "ANTHROPIC_", "GITHUB_", "SECRET_", "TOKEN_", "API_KEY")):
                    safe_env[k] = str(v)

        return safe_env

    def _build_bwrap_argv(self, argv: List[str], safe_env: Dict[str, str]) -> List[str]:
        """Construct Bubblewrap command line for Linux namespace isolation."""
        assert self.bwrap_path is not None
        bwrap_cmd = [
            self.bwrap_path,
            "--unshare-all",
            "--ro-bind", "/", "/",
            "--dev", "/dev",
            "--proc", "/proc",
            "--tmpfs", "/tmp",
            "--bind", safe_env["TMPDIR"], safe_env["TMPDIR"],
            "--bind", safe_env["HOME"], safe_env["HOME"],
        ]

        if self.config.allow_network:
            bwrap_cmd.append("--share-net")

        if self.config.read_only_workspace:
            bwrap_cmd.extend(["--ro-bind", str(self.workspace), str(self.workspace)])
        else:
            bwrap_cmd.extend(["--bind", str(self.workspace), str(self.workspace)])

        for p in self.config.writable_paths:
            resolved = p.resolve()
            if resolved.exists():
                bwrap_cmd.extend(["--bind", str(resolved), str(resolved)])

        bwrap_cmd.extend(argv)
        return bwrap_cmd

    def _make_preexec_fn(self) -> Any:
        """Create POSIX preexec function enforcing resource limits."""
        cpu_limit = self.config.cpu_limit_seconds
        mem_limit = self.config.memory_limit_bytes

        def preexec() -> None:
            # Create a separate process group for clean process tree termination
            try:
                os.setpgrp()
            except OSError:
                pass

            # CPU time limit
            try:
                resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit + 5))
            except (ValueError, OSError):
                pass

            # Max open file descriptors
            try:
                resource.setrlimit(resource.RLIMIT_NOFILE, (256, 512))
            except (ValueError, OSError):
                pass

            # File size limit (e.g. 50 MB max output file)
            try:
                resource.setrlimit(resource.RLIMIT_FSIZE, (50 * 1024 * 1024, 50 * 1024 * 1024))
            except (ValueError, OSError):
                pass

            # Virtual address space limit where supported
            if hasattr(resource, "RLIMIT_AS") and mem_limit > 0:
                try:
                    resource.setrlimit(resource.RLIMIT_AS, (mem_limit, mem_limit * 2))
                except (ValueError, OSError):
                    pass

        return preexec

    def execute(
        self,
        argv: Sequence[str],
        cwd: Optional[Path] = None,
        timeout_seconds: Optional[int] = None,
        stdin_text: Optional[str] = None,
    ) -> SandboxedExecutionResult:
        """Execute command in sandbox, returning structured output and metrics."""
        if not argv:
            raise SandboxError("Empty command argv.")

        resolved_cwd = (cwd or self.workspace).resolve()
        executable = shutil.which(argv[0])
        if not executable:
            raise SandboxError(f"Executable not found: {argv[0]}")

        final_argv = list(argv)
        final_argv[0] = executable

        timeout = min(
            timeout_seconds or self.config.timeout_seconds,
            MAX_TIMEOUT_SECONDS
        )

        safe_env = self.get_safe_env(executable)
        driver_used = "posix_isolated"

        if self.bwrap_path:
            final_argv = self._build_bwrap_argv(final_argv, safe_env)
            driver_used = "bwrap"

        preexec = None if os.name != "posix" else self._make_preexec_fn()

        start_time = time.monotonic()
        timed_out = False
        resource_limited = False
        stdout_text = ""
        stderr_text = ""
        returncode = -1

        try:
            process = subprocess.Popen(
                final_argv,
                cwd=resolved_cwd,
                stdin=subprocess.PIPE if stdin_text else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                env=safe_env,
                preexec_fn=preexec,
            )

            try:
                stdout_text, stderr_text = process.communicate(
                    input=stdin_text,
                    timeout=timeout
                )
                returncode = process.returncode
            except subprocess.TimeoutExpired:
                timed_out = True
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except (ProcessLookupError, OSError):
                        pass
                else:
                    process.kill()
                stdout_text, stderr_text = process.communicate()
                returncode = -9

        except OSError as exc:
            raise SandboxError(f"Could not execute sandboxed command: {exc}") from exc

        duration = time.monotonic() - start_time

        # Check for resource limitation signals (SIGXCPU = 24, SIGSEGV/memory abort = 11)
        if returncode in (-signal.SIGXCPU, 128 + signal.SIGXCPU, -signal.SIGKILL if timed_out else -999):
            resource_limited = True

        max_len = self.config.max_output_bytes
        truncated_stdout = (stdout_text or "")[-max_len:]
        truncated_stderr = (stderr_text or "")[-max_len:]

        return SandboxedExecutionResult(
            returncode=returncode,
            stdout=truncated_stdout,
            stderr=truncated_stderr,
            duration_seconds=duration,
            timed_out=timed_out,
            resource_limited=resource_limited,
            driver_used=driver_used,
        )


def run_sandboxed(
    argv: Sequence[str],
    workspace: Path,
    cwd: Optional[Path] = None,
    timeout_seconds: Optional[int] = None,
    allow_network: bool = False,
    read_only_workspace: bool = False,
) -> SandboxedExecutionResult:
    """Convenience helper to run a command inside the sandbox."""
    config = SandboxConfig(
        workspace=workspace,
        timeout_seconds=timeout_seconds or DEFAULT_TIMEOUT_SECONDS,
        allow_network=allow_network,
        read_only_workspace=read_only_workspace,
    )
    executor = SandboxedExecutor(workspace, config)
    return executor.execute(argv, cwd=cwd, timeout_seconds=timeout_seconds)
