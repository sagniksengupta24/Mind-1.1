from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from mind01.patches import PatchError, PatchStore
from mind01.receipts import ReceiptError, ReceiptStore
from mind01.tools import ToolError, ToolRegistry
from mind01.traces import TraceError, TraceStore


def run_integration_audit_tests() -> None:
    test_required_trace_blocks_write_file()
    test_required_trace_blocks_shell()
    test_required_trace_blocks_patch_apply()
    test_required_trace_blocks_rollback()


def test_required_trace_blocks_write_file() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-audit-write-"))
    original_append = TraceStore.append
    try:
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")
        TraceStore.append = failing_append  # type: ignore[method-assign]
        try:
            tools.call("write_file", {"path": "src/new.py", "content": "x = 1\n"})
            raise AssertionError("write_file proceeded without required trace")
        except ToolError as exc:
            assert "Required trace event" in str(exc)
        assert not (tmp / "src" / "new.py").exists()
    finally:
        TraceStore.append = original_append  # type: ignore[method-assign]
        shutil.rmtree(tmp)


def test_required_trace_blocks_shell() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-audit-shell-"))
    original_append = TraceStore.append
    try:
        tools = ToolRegistry(tmp, yes=True, allow_shell=True, mode="write-approved")
        TraceStore.append = failing_append  # type: ignore[method-assign]
        try:
            tools.call("run_command", {"command": "python3 --version"})
            raise AssertionError("run_command proceeded without required trace")
        except ToolError as exc:
            assert "Required trace event" in str(exc)
    finally:
        TraceStore.append = original_append  # type: ignore[method-assign]
        shutil.rmtree(tmp)


def test_required_trace_blocks_patch_apply() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-audit-patch-"))
    original_append = TraceStore.append
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        patches = PatchStore(tmp)
        proposal = patches.propose_edit("src/app.py", "value = 1", "value = 2")
        TraceStore.append = failing_append  # type: ignore[method-assign]
        try:
            patches.apply(
                proposal.id,
                mode="write-approved",
                approved=True,
                source="test:patch apply",
            )
            raise AssertionError("patch apply proceeded without required trace")
        except PatchError as exc:
            assert "Required patch apply trace" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 1\n"
    finally:
        TraceStore.append = original_append  # type: ignore[method-assign]
        shutil.rmtree(tmp)


def test_required_trace_blocks_rollback() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-audit-rollback-"))
    original_append = TraceStore.append
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")
        tools.call("edit_file", {"path": "src/app.py", "old": "value = 1", "new": "value = 2"})
        receipt = ReceiptStore(tmp).list(limit=1)[0]
        assert target.read_text(encoding="utf-8") == "value = 2\n"
        TraceStore.append = failing_append  # type: ignore[method-assign]
        try:
            ReceiptStore(tmp).rollback(
                receipt["receipt_id"],
                mode="write-approved",
                approved=True,
                source="test:rollback",
            )
            raise AssertionError("rollback proceeded without required trace")
        except ReceiptError as exc:
            assert "Required rollback trace" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 2\n"
    finally:
        TraceStore.append = original_append  # type: ignore[method-assign]
        shutil.rmtree(tmp)


def failing_append(self, event):  # type: ignore[no-untyped-def]
    raise TraceError("forced trace failure")
