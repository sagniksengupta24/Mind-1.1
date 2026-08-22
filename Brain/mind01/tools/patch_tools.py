from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import Any, Dict

from ..file_safety import FileSafetyError, ensure_text_file_safe, ensure_write_target_safe
from ..patches import PatchError, PatchProposal
from ..sandbox import SandboxConfig, SandboxedExecutor, SandboxError
from .shell_tools import parse_allowed_command
from .verify_tools import ToolError, ToolResult, require_arg


def propose_write_file(registry: Any, args: Dict[str, Any]) -> ToolResult:
    path = require_arg(args, "path")
    content = require_arg(args, "content")
    reason = str(args.get("reason", ""))
    try:
        proposal = registry.patches.propose_write(path, content, reason)
    except PatchError as exc:
        raise ToolError(str(exc)) from exc
    return ToolResult(
        f"Proposed patch {proposal.id}. Review with `show_patch` or "
        f"`python3 -m mind01.cli patch show {proposal.id}`."
    )


def propose_edit_file(registry: Any, args: Dict[str, Any]) -> ToolResult:
    path = require_arg(args, "path")
    old = require_arg(args, "old")
    new = require_arg(args, "new")
    reason = str(args.get("reason", ""))
    try:
        proposal = registry.patches.propose_edit(path, old, new, reason)
        preview = registry.patches.show(proposal.id)
    except PatchError as exc:
        raise ToolError(str(exc)) from exc
    return ToolResult(f"Proposed patch {proposal.id}.\n{preview[:12000]}")


def list_patches(registry: Any, args: Dict[str, Any]) -> ToolResult:
    return ToolResult(registry.patches.render_list())


def show_patch(registry: Any, args: Dict[str, Any]) -> ToolResult:
    patch_id = int(require_arg(args, "id"))
    try:
        return ToolResult(registry.patches.show(patch_id))
    except PatchError as exc:
        raise ToolError(str(exc)) from exc


def test_patch(registry: Any, args: Dict[str, Any]) -> ToolResult:
    if not registry.allow_shell:
        raise ToolError(
            "Patch testing is disabled. Re-run with `--allow-shell` "
            "to enable allowlisted test commands."
        )
    patch_id = int(require_arg(args, "id"))
    command = str(args.get("command", "python3 -B tests/smoke_test.py"))
    argv = parse_allowed_command(command)
    try:
        proposal = registry.patches.get(patch_id)
    except PatchError as exc:
        raise ToolError(str(exc)) from exc

    with tempfile.TemporaryDirectory(prefix="mind01-patch-test-") as tmp:
        tmp_workspace = Path(tmp) / "workspace"
        shutil.copytree(
            registry.workspace,
            tmp_workspace,
            ignore=shutil.ignore_patterns(".git", ".mind01", ".pycache", "__pycache__"),
        )
        apply_patch_proposal(tmp_workspace, proposal)
        config = SandboxConfig(
            workspace=tmp_workspace,
            timeout_seconds=120,
            max_output_bytes=20000,
            allow_network=False,
        )
        executor = SandboxedExecutor(tmp_workspace, config)
        res = executor.execute(argv, cwd=tmp_workspace, timeout_seconds=120)
    output = (res.output or "")[-20000:]
    status = "PASS" if res.returncode == 0 and not res.timed_out else "FAIL"
    return ToolResult(
        f"{status} patch {patch_id} with `{command}`\n"
        f"exit_code={res.returncode}\n{output}"
    )


def apply_patch_proposal(workspace: Path, proposal: PatchProposal) -> None:
    try:
        target = ensure_write_target_safe(workspace, proposal.path)
    except FileSafetyError as exc:
        raise ToolError(str(exc)) from exc
    if proposal.kind == "write":
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(proposal.content or "", encoding="utf-8")
        return
    if proposal.kind == "edit":
        if proposal.old is None or proposal.new is None:
            raise ToolError("Edit proposal is missing old/new text.")
        try:
            ensure_text_file_safe(workspace, target, proposal.path)
        except FileSafetyError as exc:
            raise ToolError(str(exc)) from exc
        current = target.read_text(encoding="utf-8")
        if proposal.old not in current:
            raise ToolError("Old text is not present in current file.")
        target.write_text(current.replace(proposal.old, proposal.new, 1), encoding="utf-8")
        return
    raise ToolError(f"Unknown proposal kind: {proposal.kind}")
