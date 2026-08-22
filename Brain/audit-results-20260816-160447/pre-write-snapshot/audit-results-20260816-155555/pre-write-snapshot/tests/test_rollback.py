from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

from mind01.cli import main as cli_main
from mind01.receipts import ReceiptStore, sha256_file
from mind01.tools import ToolRegistry


def run_rollback_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-rollback-"))
    try:
        (tmp / "src").mkdir()
        target = tmp / "src" / "app.py"
        target.write_text("value = 1\n", encoding="utf-8")
        tools = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            mode="write-approved",
        )
        store = ReceiptStore(tmp)

        tools.call(
            "edit_file",
            {"path": "src/app.py", "old": "value = 1", "new": "value = 2"},
        )
        edit_receipt = latest_receipt(store)
        assert target.read_text(encoding="utf-8") == "value = 2\n"
        rollback_output = run_cli_capture(
            [
                "rollback",
                "--workspace",
                str(tmp),
                "--mode",
                "write-approved",
                "--yes",
                edit_receipt["receipt_id"],
            ]
        )
        rollback_receipt = latest_receipt(store)
        assert "Rolled back src/app.py" in rollback_output
        assert target.read_text(encoding="utf-8") == "value = 1\n"
        assert rollback_receipt["operation_type"] == "rollback"
        assert rollback_receipt["original_receipt_id"] == edit_receipt["receipt_id"]
        assert rollback_receipt["before_sha256"] == edit_receipt["after_sha256"]
        assert rollback_receipt["after_sha256"] == sha256_file(target)
        assert rollback_receipt["backup_path"]
        assert (tmp / rollback_receipt["backup_path"]).exists()

        tools.call("write_file", {"path": "src/new.py", "content": "created = True\n"})
        write_receipt = latest_receipt(store)
        assert (tmp / "src" / "new.py").exists()
        run_cli_capture(
            [
                "rollback",
                "--workspace",
                str(tmp),
                "--mode",
                "unsafe",
                "--yes",
                write_receipt["receipt_id"],
            ]
        )
        new_file_rollback = latest_receipt(store)
        assert not (tmp / "src" / "new.py").exists()
        assert new_file_rollback["operation_type"] == "rollback"
        assert new_file_rollback["after_exists"] is False
        assert new_file_rollback["after_sha256"] is None
        assert new_file_rollback["after_size_bytes"] is None

        tools.call(
            "edit_file",
            {"path": "src/app.py", "old": "value = 1", "new": "value = 3"},
        )
        stale_receipt = latest_receipt(store)
        target.write_text("unexpected = True\n", encoding="utf-8")
        failed_code, _stdout, stderr = run_cli_capture_code(
            [
                "rollback",
                "--workspace",
                str(tmp),
                "--mode",
                "write-approved",
                "--yes",
                stale_receipt["receipt_id"],
            ]
        )
        assert failed_code == 2
        assert "Current file hash differs" in stderr
        assert target.read_text(encoding="utf-8") == "unexpected = True\n"

        forced_output = run_cli_capture(
            [
                "rollback",
                "--workspace",
                str(tmp),
                "--mode",
                "write-approved",
                "--yes",
                "--force",
                stale_receipt["receipt_id"],
            ]
        )
        assert "Rolled back src/app.py" in forced_output
        assert target.read_text(encoding="utf-8") == "value = 1\n"

        tools.call(
            "edit_file",
            {"path": "src/app.py", "old": "value = 1", "new": "value = 4"},
        )
        policy_receipt = latest_receipt(store)
        read_only_code, _stdout, read_only_stderr = run_cli_capture_code(
            ["rollback", "--workspace", str(tmp), policy_receipt["receipt_id"]]
        )
        assert read_only_code == 2
        assert "read-only" in read_only_stderr
        no_yes_code, _stdout, no_yes_stderr = run_cli_capture_code(
            [
                "rollback",
                "--workspace",
                str(tmp),
                "--mode",
                "write-approved",
                policy_receipt["receipt_id"],
            ]
        )
        assert no_yes_code == 2
        assert "requires `--yes`" in no_yes_stderr
    finally:
        shutil.rmtree(tmp)


def latest_receipt(store: ReceiptStore) -> dict:
    receipts = store.list(limit=1)
    assert receipts
    return receipts[0]


def run_cli_capture(argv: list[str]) -> str:
    code, stdout, stderr = run_cli_capture_code(argv)
    assert code == 0, stderr
    return stdout


def run_cli_capture_code(argv: list[str]) -> tuple[int, str, str]:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = cli_main(argv)
    return code, stdout.getvalue(), stderr.getvalue()


def test_rollback_regressions() -> None:
    run_rollback_tests()
