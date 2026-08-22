from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
from pathlib import Path

import mind01.mutations as mutations
from mind01.cli import main as cli_main
from mind01.patches import PatchError, PatchStore
from mind01.receipts import ReceiptError, ReceiptStore, sha256_file
from mind01.tools import ToolError, ToolRegistry


def run_mutation_transaction_tests() -> None:
    test_write_and_edit_transaction_success()
    test_failure_before_replace_leaves_original_unchanged()
    test_receipt_failure_after_replace_restores_and_has_no_success_receipt()
    test_restore_failure_creates_dirty_record()
    test_rollback_transaction_and_hash_policy()
    test_patch_apply_validation_and_restore()
    test_dirty_cli_commands()


def test_write_and_edit_transaction_success() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-success-"))
    try:
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")
        tools.call("write_file", {"path": "src/new.py", "content": "x = 1\n"})
        store = ReceiptStore(tmp)
        write_receipt = store.list(limit=1)[0]
        target = tmp / "src" / "new.py"
        assert target.read_text(encoding="utf-8") == "x = 1\n"
        assert write_receipt["operation_type"] == "write_file"
        assert write_receipt["success"] is True
        assert write_receipt["after_sha256"] == sha256_file(target)

        tools.call("edit_file", {"path": "src/new.py", "old": "x = 1", "new": "x = 2"})
        edit_receipt = store.list(limit=1)[0]
        assert target.read_text(encoding="utf-8") == "x = 2\n"
        assert edit_receipt["operation_type"] == "edit_file"
        assert edit_receipt["backup_path"]
        assert (tmp / edit_receipt["backup_path"]).exists()
    finally:
        shutil.rmtree(tmp)


def test_failure_before_replace_leaves_original_unchanged() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-before-"))
    original_write_temp = mutations.write_temp_file
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")

        def fail_before_replace(path, content):  # type: ignore[no-untyped-def]
            raise mutations.MutationError("forced pre-replace failure")

        mutations.write_temp_file = fail_before_replace
        try:
            tools.call("edit_file", {"path": "src/app.py", "old": "1", "new": "2"})
            raise AssertionError("edit_file succeeded despite pre-replace failure")
        except ToolError as exc:
            assert "before replace" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 1\n"
        assert ReceiptStore(tmp).list(limit=1) == []
    finally:
        mutations.write_temp_file = original_write_temp
        shutil.rmtree(tmp)


def test_receipt_failure_after_replace_restores_and_has_no_success_receipt() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-restore-"))
    original_write_receipt = ReceiptStore.write_receipt
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")

        def fail_write_receipt(self, receipt):  # type: ignore[no-untyped-def]
            raise ReceiptError("forced receipt failure")

        ReceiptStore.write_receipt = fail_write_receipt
        try:
            tools.call("edit_file", {"path": "src/app.py", "old": "1", "new": "2"})
            raise AssertionError("edit_file succeeded despite receipt failure")
        except ToolError as exc:
            assert "original state restored" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 1\n"
        assert ReceiptStore(tmp).list(limit=1) == []
    finally:
        ReceiptStore.write_receipt = original_write_receipt
        shutil.rmtree(tmp)


def test_restore_failure_creates_dirty_record() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-dirty-"))
    original_write_receipt = ReceiptStore.write_receipt
    original_restore = mutations.restore_previous_state
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")

        def fail_write_receipt(self, receipt):  # type: ignore[no-untyped-def]
            raise ReceiptError("forced receipt failure")

        def fail_restore(workspace, target, before, backup_path):  # type: ignore[no-untyped-def]
            raise mutations.MutationError("forced restore failure")

        ReceiptStore.write_receipt = fail_write_receipt
        mutations.restore_previous_state = fail_restore
        try:
            tools.call("edit_file", {"path": "src/app.py", "old": "1", "new": "2"})
            raise AssertionError("edit_file succeeded despite dirty state")
        except ToolError as exc:
            assert "dirty state recorded" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 2\n"
        dirty = mutations.DirtyStateStore(tmp).list(limit=1)
        assert len(dirty) == 1
        assert dirty[0]["operation"] == "edit_file"
        assert dirty[0]["target_relative_path"] == "src/app.py"
        assert dirty[0]["before_sha256"]
        assert dirty[0]["intended_after_sha256"]
        assert dirty[0]["current_sha256"]
    finally:
        ReceiptStore.write_receipt = original_write_receipt
        mutations.restore_previous_state = original_restore
        shutil.rmtree(tmp)


def test_rollback_transaction_and_hash_policy() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-rollback-"))
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")
        tools.call("edit_file", {"path": "src/app.py", "old": "1", "new": "2"})
        edit_receipt = ReceiptStore(tmp).list(limit=1)[0]
        target.write_text("unexpected = True\n", encoding="utf-8")
        try:
            ReceiptStore(tmp).rollback(
                edit_receipt["receipt_id"],
                mode="write-approved",
                approved=True,
            )
            raise AssertionError("rollback ignored hash mismatch")
        except ReceiptError as exc:
            assert "differs from receipt" in str(exc)
        assert target.read_text(encoding="utf-8") == "unexpected = True\n"

        rollback_receipt = ReceiptStore(tmp).rollback(
            edit_receipt["receipt_id"],
            mode="write-approved",
            approved=True,
            force=True,
        )
        assert rollback_receipt["operation_type"] == "rollback"
        assert rollback_receipt["success"] is True
        assert target.read_text(encoding="utf-8") == "value = 1\n"
    finally:
        shutil.rmtree(tmp)


def test_patch_apply_validation_and_restore() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-patch-"))
    original_write_receipt = ReceiptStore.write_receipt
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        patches = PatchStore(tmp)
        proposal = patches.propose_edit("src/app.py", "value = 1", "value = 2")

        def fail_write_receipt(self, receipt):  # type: ignore[no-untyped-def]
            raise ReceiptError("forced receipt failure")

        ReceiptStore.write_receipt = fail_write_receipt
        try:
            patches.apply(proposal.id, mode="write-approved", approved=True)
            raise AssertionError("patch apply succeeded despite receipt failure")
        except PatchError as exc:
            assert "original state restored" in str(exc)
        assert target.read_text(encoding="utf-8") == "value = 1\n"

        (tmp / ".mind01" / "patches.json").write_text(
            json.dumps(
                [
                    {
                        "id": 99,
                        "kind": "write",
                        "path": "../escape.py",
                        "content": "bad\n",
                        "reason": "bad",
                        "created_at": 1,
                    }
                ]
            ),
            encoding="utf-8",
        )
        try:
            patches.apply(99, mode="write-approved", approved=True)
            raise AssertionError("patch apply accepted escaping path")
        except PatchError as exc:
            assert "escapes workspace" in str(exc)
    finally:
        ReceiptStore.write_receipt = original_write_receipt
        shutil.rmtree(tmp)


def test_dirty_cli_commands() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-mutation-cli-"))
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 2\n", encoding="utf-8")
        dirty = mutations.DirtyStateStore(tmp).create(
            operation="test",
            target=target,
            before=mutations.FileState(True, "before", 1),
            intended_after=mutations.FileState(True, "after", 2),
            current=mutations.FileState(True, "current", 3),
            backup_path=".mind01/receipts/backups/example.bak",
            error="forced",
            recovery_status="test",
        )
        listed = run_cli_capture(["mutations", "--workspace", str(tmp), "dirty-list"])
        assert dirty["dirty_id"] in listed
        shown = run_cli_capture(
            ["mutations", "--workspace", str(tmp), "dirty-show", dirty["dirty_id"]]
        )
        assert json.loads(shown)["dirty_id"] == dirty["dirty_id"]
    finally:
        shutil.rmtree(tmp)


def run_cli_capture(argv: list[str]) -> str:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = cli_main(argv)
    assert code == 0, stderr.getvalue()
    return stdout.getvalue()
