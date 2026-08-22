from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Dict

from .verify_tools import ToolError, ToolResult, approve, require_arg


ALLOWED_COMMANDS = {"python", "python3", "pytest", "ruff", "mypy", "git"}
DISALLOWED_EXECUTABLES = {
    "rm",
    "sudo",
    "curl",
    "wget",
    "ssh",
    "scp",
    "chmod",
    "chown",
    "dd",
    "mkfs",
    "kill",
    "perl",
    "ruby",
    "node",
}
ALLOWED_GIT_SUBCOMMANDS = {
    "branch",
    "diff",
    "grep",
    "log",
    "ls-files",
    "rev-parse",
    "show",
    "status",
}
BLOCKED_SHELL_TOKENS = {"|", "||", "&&", ";", ">", ">>", "<", "<<", "`"}
BLOCKED_SHELL_CHARS = {"|", "&", ";", ">", "<", "`", "$", "\n", "\r"}
BLOCKED_PYTHON_ARGS = {"-c"}
DEFAULT_TIMEOUT_SECONDS = 60
MAX_TIMEOUT_SECONDS = 120
DEFAULT_OUTPUT_LIMIT = 20000
MAX_OUTPUT_LIMIT = 20000


from ..sandbox import SandboxConfig, SandboxedExecutor, SandboxError, SandboxTimeoutError


def run_command(registry: Any, args: Dict[str, Any]) -> ToolResult:
    command = require_arg(args, "command")
    if not registry.allow_shell:
        raise ToolError(
            "Command execution is disabled. Re-run with `--allow-shell` "
            "to enable allowlisted commands."
        )
    argv = parse_allowed_command(command)
    approve(registry, f"Run command in {registry.workspace}: {command}")
    timeout_seconds = bounded_int(
        args.get("timeout_seconds", DEFAULT_TIMEOUT_SECONDS),
        minimum=1,
        maximum=MAX_TIMEOUT_SECONDS,
        name="timeout_seconds",
    )
    output_limit = bounded_int(
        args.get("output_limit", DEFAULT_OUTPUT_LIMIT),
        minimum=1,
        maximum=MAX_OUTPUT_LIMIT,
        name="output_limit",
    )
    try:
        executable = shutil.which(argv[0])
        if not executable:
            raise ToolError(f"Allowlisted executable was not found: {argv[0]}")
        validate_workspace_command_paths(argv[1:], registry.workspace)

        is_unsafe = getattr(registry.mode, "value", str(registry.mode)) == "unsafe"
        bwrap_path = shutil.which("bwrap")
        if is_unsafe and not bwrap_path:
            raise ToolError("bwrap is required for OS-level sandboxing in unsafe mode, but it is not installed. Failing closed.")

        sandbox_config = SandboxConfig(
            workspace=registry.workspace,
            timeout_seconds=timeout_seconds,
            max_output_bytes=output_limit,
            allow_network=False,
            read_only_workspace=is_unsafe,
        )
        executor = SandboxedExecutor(registry.workspace, sandbox_config)
        res = executor.execute(argv, cwd=registry.workspace, timeout_seconds=timeout_seconds)
        if res.timed_out:
            raise ToolError(f"Command timed out after {timeout_seconds} seconds.\n{res.output}")
        output = (res.output or "")[-output_limit:]
        return ToolResult(f"exit_code={res.returncode}\n{output}")
    except SandboxError as exc:
        raise ToolError(f"Sandbox execution failure: {exc}") from exc
    except OSError as exc:
        raise ToolError(f"Could not execute allowlisted command: {exc}") from exc


def parse_allowed_command(command: str) -> list[str]:
    lowered = command.lower()
    if any(char in command for char in BLOCKED_SHELL_CHARS):
        raise ToolError("Shell operators and command substitution are not allowed in commands.")
    blocked_phrases = [
        "rm -rf /",
        "rm -fr /",
        "mkfs",
        "dd if=",
        "diskutil erase",
        "git reset --hard",
        "git clean -fd",
        "git clean -xdf",
        ":(){",
        "chmod -r 777",
        "chown -r",
        "$(",
        "python -c",
        "python3 -c",
        "node -e",
        "perl -e",
        "ruby -e",
    ]
    for phrase in blocked_phrases:
        if phrase in lowered:
            raise ToolError(f"Blocked dangerous command pattern: {phrase}")

    try:
        parts = shlex.split(command)
    except ValueError as exc:
        raise ToolError(f"Could not parse command safely: {exc}") from exc
    if not parts:
        raise ToolError("Empty command.")

    if any(token in BLOCKED_SHELL_TOKENS for token in parts) or any(
        char in part for part in parts for char in BLOCKED_SHELL_CHARS
    ):
        raise ToolError("Shell operators are not allowed in commands.")

    executable = Path(parts[0]).name
    if executable in DISALLOWED_EXECUTABLES:
        raise ToolError(f"Command `{executable}` is blocked.")
    if executable not in ALLOWED_COMMANDS:
        raise ToolError(
            f"Command `{executable}` is not allowlisted. Allowed commands: "
            f"{', '.join(sorted(ALLOWED_COMMANDS))}."
        )

    if executable in {"python", "python3"} and any(
        arg in BLOCKED_PYTHON_ARGS for arg in parts[1:]
    ):
        raise ToolError("Inline Python execution with `-c` is not allowed.")

    if executable == "git":
        if len(parts) < 2 or parts[1] not in ALLOWED_GIT_SUBCOMMANDS:
            raise ToolError(
                "Only read-only git subcommands are allowed: "
                f"{', '.join(sorted(ALLOWED_GIT_SUBCOMMANDS))}."
            )

    if executable == "rm" and any(flag in parts for flag in ["-rf", "-fr", "-r"]):
        raise ToolError("Blocked recursive remove command.")
    return parts


def validate_workspace_command_paths(arguments: list[str], workspace: Path) -> None:
    for argument in arguments:
        if not argument or argument.startswith("-"):
            continue
        candidate_text = argument.split("=", 1)[-1] if "=" in argument else argument
        candidate = Path(candidate_text).expanduser()
        if candidate.is_absolute():
            resolved = candidate.resolve()
            if workspace != resolved and workspace not in resolved.parents:
                raise ToolError(f"Command argument escapes workspace: {argument}")
        if ".." in candidate.parts:
            resolved = (workspace / candidate).resolve()
            if workspace != resolved and workspace not in resolved.parents:
                raise ToolError(f"Command argument escapes workspace: {argument}")


def validate_command_is_allowed(command: str) -> None:
    parse_allowed_command(command)


def bounded_int(value: Any, minimum: int, maximum: int, name: str) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError) as exc:
        raise ToolError(f"`{name}` must be an integer.") from exc
    if number < minimum or number > maximum:
        raise ToolError(f"`{name}` must be between {minimum} and {maximum}.")
    return number
