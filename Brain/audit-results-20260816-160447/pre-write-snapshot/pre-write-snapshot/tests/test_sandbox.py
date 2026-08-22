"""Workstream 1 — sandboxed execution tests.

Covers:
- `unsafe` mode fails closed when bwrap is not available;
- out-of-workspace / path-traversal writes are blocked (write_file and
  run_command argument paths);
- commands in `unsafe` mode run under a read-only root bind with only the
  explicit scratch (HOME/TMPDIR) writable;
- the workspace itself is read-only inside the sandbox unless it is an
  approved scratch path.
"""

from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from mind01.modes import AgentMode
from mind01.tools.registry import ToolRegistry
from mind01.tools.verify_tools import ToolError

pytestmark = pytest.mark.skipif(
    shutil.which("bwrap") is None,
    reason="bwrap is required for sandboxed-execution tests",
)

SCRATCH_PROBE = """\
import os
from pathlib import Path

# 1) attempt to write into the read-only workspace root
try:
    Path("sandbox_escape_ws.txt").write_text("pwned")
    print("WS_WRITE_OK")
except OSError as exc:
    print(f"WS_WRITE_BLOCKED: {exc}")

# 2) attempt to write to a read-only host path (outside the workspace)
try:
    Path("/etc/mind_sandbox_escape_abs.txt").write_text("pwned")
    print("ABS_WRITE_OK")
except OSError as exc:
    print(f"ABS_WRITE_BLOCKED: {exc}")

# 2b) /tmp is a private tmpfs inside the sandbox: the write must not escape
#     to the host, even though it succeeds inside the sandbox.
Path("/tmp/mind_sandbox_escape_abs.txt").write_text("pwned")
print("TMP_ISOLATED_OK")

# 3) scratch path must remain writable
scratch = os.environ.get("TMPDIR", "")
if scratch and Path(scratch).exists():
    Path(scratch, "probe.txt").write_text("ok")
    print("SCRATCH_WRITE_OK")
else:
    print("SCRATCH_MISSING")
"""


def _unsafe_registry(workspace: Path) -> ToolRegistry:
    return ToolRegistry(
        workspace,
        yes=True,
        allow_write=True,
        allow_shell=True,
        mode=AgentMode.UNSAFE,
    )


def test_unsafe_mode_fails_closed_without_bwrap(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    real_which = shutil.which

    def fake_which(name: str) -> str | None:
        if name == "bwrap":
            return None
        return real_which(name)

    monkeypatch.setattr(shutil, "which", fake_which)
    registry = _unsafe_registry(tmp_path)
    with pytest.raises(ToolError, match="Failing closed"):
        registry.call("run_command", {"command": "python3 --version"})


def test_out_of_workspace_write_file_blocked(tmp_path: Path) -> None:
    registry = _unsafe_registry(tmp_path)
    with pytest.raises(ToolError):
        registry.call(
            "write_file",
            {"path": "/tmp/mind_pwned.txt", "content": "pwned"},
        )
    assert not (Path("/tmp") / "mind_pwned.txt").exists()


def test_path_traversal_write_file_blocked(tmp_path: Path) -> None:
    registry = _unsafe_registry(tmp_path)
    with pytest.raises(ToolError):
        registry.call(
            "write_file",
            {"path": "../mind_escape.txt", "content": "pwned"},
        )
    assert not (tmp_path.parent / "mind_escape.txt").exists()


def test_command_argument_path_traversal_blocked(tmp_path: Path) -> None:
    registry = _unsafe_registry(tmp_path)
    with pytest.raises(ToolError, match="escapes workspace"):
        registry.call(
            "run_command",
            {"command": f"python3 {tmp_path.parent / 'outside.py'}"},
        )


def test_unsafe_command_runs_in_read_only_sandbox(tmp_path: Path) -> None:
    probe = tmp_path / "sandbox_probe.py"
    probe.write_text(SCRATCH_PROBE, encoding="utf-8")
    registry = _unsafe_registry(tmp_path)
    result = registry.call("run_command", {"command": "python3 sandbox_probe.py"})
    output = result.text
    assert "WS_WRITE_BLOCKED" in output, f"workspace must be read-only inside sandbox:\n{output}"
    assert "ABS_WRITE_BLOCKED" in output, f"host absolute writes must be blocked:\n{output}"
    assert "TMP_ISOLATED_OK" in output, f"private tmpfs must accept isolated writes:\n{output}"
    assert "SCRATCH_WRITE_OK" in output, f"scratch path must stay writable:\n{output}"
    assert not (tmp_path / "sandbox_escape_ws.txt").exists()
    assert not (Path("/tmp") / "mind_sandbox_escape_abs.txt").exists(), (
        "write into sandbox /tmp leaked to the host"
    )


def test_write_approved_command_not_sandboxed_but_paths_still_safe(tmp_path: Path) -> None:
    """write-approved mode never enters the sandbox but still blocks escape paths."""
    registry = ToolRegistry(
        tmp_path,
        yes=True,
        allow_write=True,
        allow_shell=True,
        mode=AgentMode.WRITE_APPROVED,
    )
    with pytest.raises(ToolError, match="escapes workspace"):
        registry.call(
            "run_command",
            {"command": f"python3 {tmp_path.parent / 'outside.py'}"},
        )
