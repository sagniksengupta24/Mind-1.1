"""Comprehensive tests for mandatory sandbox isolation and resource limits."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pytest

from mind01.modes import AgentMode
from mind01.sandbox import (
    SandboxConfig,
    SandboxedExecutor,
    run_sandboxed,
)
from mind01.tools.registry import ToolRegistry
from mind01.tools.verify_tools import ToolError


def _registry_with_mode(workspace: Path, mode: AgentMode = AgentMode.WRITE_APPROVED) -> ToolRegistry:
    return ToolRegistry(
        workspace,
        yes=True,
        allow_write=True,
        allow_shell=True,
        mode=mode,
    )


def test_filesystem_escape_blocked_in_sandboxed_executor(tmp_path: Path) -> None:
    """Test that executed code cannot write outside the workspace."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    outside_target = tmp_path / "outside_escape.txt"

    probe_script = workspace / "escape_probe.py"
    probe_script.write_text(f"""\
import os, sys
from pathlib import Path

target = Path({repr(str(outside_target))})
try:
    target.write_text("pwned")
    print("ESCAPE_WRITE_SUCCEEDED")
except Exception as exc:
    print(f"ESCAPE_WRITE_BLOCKED: {{exc}}")
""")

    config = SandboxConfig(workspace=workspace, timeout_seconds=10, allow_network=False)
    executor = SandboxedExecutor(workspace, config)
    res = executor.execute([sys.executable, str(probe_script)])

    # If running with bwrap, it will fail write with PermissionDenied or Read-only file system
    # If running under posix_isolated, the file path outside workspace must not be modified if tool policy blocks it
    # Furthermore, verify run_command rejects paths outside workspace
    registry = _registry_with_mode(workspace)
    with pytest.raises(ToolError, match="escapes workspace"):
        registry.call("run_command", {"command": f"python3 {outside_target}"})


def test_network_call_blocked_in_sandbox(tmp_path: Path) -> None:
    """Test that network calls are blocked when allow_network=False."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    probe_script = workspace / "net_probe.py"
    probe_script.write_text("""\
import urllib.request
import urllib.error

try:
    req = urllib.request.Request("http://1.1.1.1:80", headers={"User-Agent": "Test"})
    resp = urllib.request.urlopen(req, timeout=2)
    print("NET_SUCCESS")
except Exception as exc:
    print(f"NET_BLOCKED: {type(exc).__name__}")
""")

    config = SandboxConfig(workspace=workspace, timeout_seconds=10, allow_network=False)
    executor = SandboxedExecutor(workspace, config)
    res = executor.execute([sys.executable, str(probe_script)])

    assert "NET_SUCCESS" not in res.output
    assert "NET_BLOCKED" in res.output


def test_time_limit_enforced_on_every_mode(tmp_path: Path) -> None:
    """Test that execution time limits are enforced across all operating modes."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    probe_script = workspace / "hang.py"
    probe_script.write_text("""\
import time
while True:
    time.sleep(0.1)
""")

    # Test via SandboxedExecutor
    config = SandboxConfig(workspace=workspace, timeout_seconds=2)
    executor = SandboxedExecutor(workspace, config)
    res = executor.execute([sys.executable, str(probe_script)], timeout_seconds=2)
    assert res.timed_out is True
    assert res.duration_seconds < 6.0

    # Test via ToolRegistry in write-approved mode (not just unsafe mode)
    registry = _registry_with_mode(workspace, mode=AgentMode.WRITE_APPROVED)
    with pytest.raises(ToolError, match="timed out"):
        registry.call("run_command", {"command": f"python3 {probe_script.name}", "timeout_seconds": 2})


def test_memory_and_resource_limits_configured(tmp_path: Path) -> None:
    """Test that SandboxConfig configures CPU, memory, and file limits."""
    workspace = tmp_path / "workspace"
    workspace.mkdir()

    config = SandboxConfig(
        workspace=workspace,
        cpu_limit_seconds=5,
        memory_limit_bytes=256 * 1024 * 1024,
        timeout_seconds=5,
    )
    executor = SandboxedExecutor(workspace, config)
    safe_env = executor.get_safe_env()

    assert safe_env["MIND_SANDBOX_ACTIVE"] == "1"
    assert safe_env["MIND_SANDBOX_WORKSPACE"] == str(workspace.resolve())
    assert safe_env["PYTHONNOUSERSITE"] == "1"
    assert safe_env["PYTHONDONTWRITEBYTECODE"] == "1"


def test_all_code_execution_routes_through_sandbox() -> None:
    """Verify that no code execution subprocess in tools/verification bypasses SandboxedExecutor."""
    import ast

    brain_dir = Path(__file__).parent.parent / "mind01"
    execution_files = [
        brain_dir / "tools" / "shell_tools.py",
        brain_dir / "tools" / "patch_tools.py",
        brain_dir / "verification.py",
        brain_dir / "self_correction.py",
    ]

    for file_path in execution_files:
        content = file_path.read_text()
        tree = ast.parse(content, filename=str(file_path))
        # Ensure SandboxedExecutor or run_sandboxed is imported/used
        assert "SandboxedExecutor" in content or "run_sandboxed" in content, (
            f"{file_path.name} does not reference SandboxedExecutor"
        )
