from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
from pathlib import Path

from mind01.cli import main as cli_main
from mind01.patches import PatchStore
from mind01.receipts import ReceiptError, ReceiptStore, sha256_file
from mind01.tools import ToolError, ToolRegistry


def run_receipt_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-receipts-"))
    try:
        (tmp / "src").mkdir()
        tools = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            mode="write-approved",
        )
        store = ReceiptStore(tmp)

        write_result = tools.call(
            "write_file",
            {"path": "src/new.py", "content": "x = 1\n"},
        ).text
        write_receipt = latest_receipt(store)
        assert "receipt" in write_result
        assert write_receipt["operation_type"] == "write_file"
        assert write_receipt["approval_yes_status"] is True
        assert write_receipt["before_exists"] is False
        assert write_receipt["before_sha256"] is None
        assert write_receipt["before_size_bytes"] is None
        assert write_receipt["after_sha256"] == sha256_file(tmp / "src" / "new.py")
        assert write_receipt["after_size_bytes"] == len("x = 1\n")
        assert write_receipt["relative_file_path"] == "src/new.py"
        assert write_receipt["success"] is True
        assert write_receipt["backup_path"] is None

        edit_result = tools.call(
            "edit_file",
            {"path": "src/new.py", "old": "x = 1", "new": "x = 2"},
        ).text
        edit_receipt = latest_receipt(store)
        assert "receipt" in edit_result
        assert edit_receipt["operation_type"] == "edit_file"
        assert edit_receipt["before_exists"] is True
        assert edit_receipt["before_sha256"]
        assert edit_receipt["after_sha256"] == sha256_file(tmp / "src" / "new.py")
        assert edit_receipt["before_size_bytes"] == len("x = 1\n")
        assert edit_receipt["after_size_bytes"] == len("x = 2\n")
        assert edit_receipt["backup_path"]
        assert (tmp / edit_receipt["backup_path"]).exists()

        patches = PatchStore(tmp)
        proposal = patches.propose_edit("src/new.py", "x = 2", "x = 3", "receipt test")
        applied = patches.apply(
            proposal.id,
            mode="write-approved",
            allow_write=False,
            approved=True,
            source="test:patch apply",
        )
        patch_receipt = latest_receipt(store)
        assert "Receipt" in applied
        assert patch_receipt["operation_type"] == "patch_apply"
        assert patch_receipt["tool_name"] == "test:patch apply"
        assert patch_receipt["after_sha256"] == sha256_file(tmp / "src" / "new.py")
        assert patch_receipt["backup_path"]
        assert (tmp / patch_receipt["backup_path"]).exists()

        try:
            tools.call("write_file", {"path": ".mind01/receipts/bad.txt", "content": "x"})
            raise AssertionError("runtime receipt path write was not blocked")
        except ToolError as exc:
            assert "Runtime path access is blocked" in str(exc)

        list_output = run_cli_capture(["receipts", "--workspace", str(tmp), "list"])
        assert patch_receipt["receipt_id"] in list_output
        show_output = run_cli_capture(
            ["receipts", "--workspace", str(tmp), "show", patch_receipt["receipt_id"]]
        )
        shown = json.loads(show_output)
        assert shown["receipt_id"] == patch_receipt["receipt_id"]

        original_write_receipt = ReceiptStore.write_receipt

        def fail_write_receipt(self, receipt):  # type: ignore[no-untyped-def]
            raise ReceiptError("forced receipt failure")

        ReceiptStore.write_receipt = fail_write_receipt
        try:
            try:
                tools.call("write_file", {"path": "src/fails.py", "content": "boom\n"})
                raise AssertionError("write reported success despite receipt failure")
            except ToolError as exc:
                assert "forced receipt failure" in str(exc)
        finally:
            ReceiptStore.write_receipt = original_write_receipt
    finally:
        shutil.rmtree(tmp)


def latest_receipt(store: ReceiptStore) -> dict:
    receipts = store.list(limit=1)
    assert receipts
    return receipts[0]


def run_cli_capture(argv: list[str]) -> str:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
        code = cli_main(argv)
    assert code == 0
    return stdout.getvalue()


def test_receipt_regressions() -> None:
    run_receipt_tests()
