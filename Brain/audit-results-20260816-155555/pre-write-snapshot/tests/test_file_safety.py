from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

from mind01.cli import main as cli_main
from mind01.file_safety import MAX_TEXT_FILE_BYTES
from mind01.tools import ToolError, ToolRegistry


def run_file_safety_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-file-safety-"))
    outside = Path(tempfile.mkdtemp(prefix="mind01-outside-"))
    try:
        (tmp / "src").mkdir()
        (tmp / "src" / "demo.py").write_text("token = 'abc'\nprint(token)\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True)

        assert "token" in tools.call("read_file", {"path": "src/demo.py"}).text
        assert "src/demo.py:2" in tools.call("search_code", {"query": "print"}).text

        traversal = "../" + outside.name + "/escape.txt"
        (outside / "escape.txt").write_text("outside", encoding="utf-8")
        try:
            tools.call("read_file", {"path": traversal})
            raise AssertionError("path traversal was not blocked")
        except ToolError as exc:
            assert "escapes workspace" in str(exc)

        (outside / "outside.py").write_text("print('outside')\n", encoding="utf-8")
        (tmp / "src" / "linked.py").symlink_to(outside / "outside.py")
        try:
            tools.call("read_file", {"path": "src/linked.py"})
            raise AssertionError("symlink escape was not blocked")
        except ToolError as exc:
            assert "escapes workspace" in str(exc)

        (tmp / "src" / "binary.bin").write_bytes(b"\x00\x01\x02")
        try:
            tools.call("read_file", {"path": "src/binary.bin"})
            raise AssertionError("binary read was not blocked")
        except ToolError as exc:
            assert "Binary file reads are blocked" in str(exc)

        (tmp / "src" / "large.txt").write_text("a" * (MAX_TEXT_FILE_BYTES + 1), encoding="utf-8")
        try:
            tools.call("read_file", {"path": "src/large.txt"})
            raise AssertionError("oversized read was not blocked")
        except ToolError as exc:
            assert "too large" in str(exc)

        (tmp / ".mind01").mkdir(exist_ok=True)
        (tmp / ".mind01" / "private.sqlite3").write_text("not really sqlite", encoding="utf-8")
        try:
            tools.call("read_file", {"path": ".mind01/private.sqlite3"})
            raise AssertionError("runtime DB read was not blocked")
        except ToolError as exc:
            assert "Runtime file access is blocked" in str(exc)

        write_tools = ToolRegistry(tmp, yes=True, allow_write=True, mode="write-approved")
        try:
            write_tools.call("write_file", {"path": traversal, "content": "x"})
            raise AssertionError("write outside workspace was not blocked")
        except ToolError as exc:
            assert "escapes workspace" in str(exc)
        try:
            write_tools.call("edit_file", {"path": "src/linked.py", "old": "outside", "new": "inside"})
            raise AssertionError("edit outside workspace was not blocked")
        except ToolError as exc:
            assert "escapes workspace" in str(exc)

        propose = ToolRegistry(tmp, yes=True, mode="propose")
        try:
            propose.call("propose_write_file", {"path": ".mind01/patches.json", "content": "{}"})
            raise AssertionError("runtime patch proposal was not blocked")
        except ToolError as exc:
            assert "Runtime file access is blocked" in str(exc)

        assert run_cli_quietly(["index-code", "--workspace", str(tmp)]) == 2
        assert run_cli_quietly(["index-code", "--workspace", str(tmp), "--mode", "propose"]) == 0
        assert run_cli_quietly(["remember", "k", "v", "--workspace", str(tmp)]) == 2
        assert run_cli_quietly(
            ["remember", "k", "v", "--workspace", str(tmp), "--mode", "write-approved"]
        ) == 0
    finally:
        shutil.rmtree(tmp)
        shutil.rmtree(outside)


def run_cli_quietly(argv: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return cli_main(argv)


def test_file_safety_regressions() -> None:
    run_file_safety_tests()
