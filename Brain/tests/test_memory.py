from __future__ import annotations

import contextlib
import io
import shutil
import tempfile
from pathlib import Path

from mind01.cli import main as cli_main
from mind01.memory import MemoryStore
from mind01.tools import ToolError, ToolRegistry


def run_memory_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-memory-"))
    try:
        store = MemoryStore(tmp)
        store.remember(
            "startup",
            "Mind1.1 focuses on code, Indian languages, and reasoning.",
            "Project,AI,project",
            source="test",
            importance=2,
        )
        store.remember(
            "reasoning",
            "Reasoning workflows need ranked memory retrieval.",
            "project,reasoning",
            source="test",
            importance=9,
        )
        store.remember(
            "low",
            "Reasoning note with lower importance.",
            "project,reasoning",
            source="test",
            importance=1,
        )
        ranked = store.recall("reasoning", tags="reasoning", limit=3)
        assert ranked
        assert ranked[0].key == "reasoning"
        assert ranked[0].importance == 9
        assert ranked[0].score > ranked[-1].score

        tagged = store.list(tags="ai")
        assert len(tagged) == 1
        assert tagged[0].tags == "project,ai"
        assert tagged[0].source == "test"
        assert tagged[0].updated_at >= tagged[0].created_at

        store.remember("secret", "token=abc123 password=hunter2", "security", importance=5)
        secret = store.recall("secret token", tags="security", limit=1)[0]
        assert "abc123" not in secret.value
        assert "hunter2" not in secret.value
        assert "[REDACTED]" in secret.value

        store.update(1, "Updated startup memory for semiconductor code.", tags="project,vlsi", importance=8)
        updated = store.recall("semiconductor", tags="vlsi", limit=1)
        assert updated
        assert updated[0].id == 1
        assert updated[0].importance == 8

        read_only = ToolRegistry(tmp, yes=True)
        try:
            read_only.call("remember", {"key": "blocked", "value": "nope"})
            raise AssertionError("read-only memory mutation was not blocked")
        except ToolError as exc:
            assert "read-only" in str(exc) or "not allowed" in str(exc)

        write_tools = ToolRegistry(tmp, yes=True, mode="write-approved")
        write_tools.call(
            "remember",
            {
                "key": "tool",
                "value": "Tool memories support tags.",
                "tags": "tool,test",
                "importance": 6,
            },
        )
        tool_recall = write_tools.call(
            "recall",
            {"query": "tags", "tags": "tool", "limit": 2},
        ).text
        assert "Tool memories support tags" in tool_recall
        assert "importance=6" in tool_recall

        blocked_code = run_cli_code(["memory", "--workspace", str(tmp), "add", "cli", "blocked"])
        assert blocked_code == 2
        add_output = run_cli_capture(
            [
                "memory",
                "--workspace",
                str(tmp),
                "add",
                "cli",
                "CLI memory with tags",
                "--tags",
                "cli,test",
                "--importance",
                "7",
                "--mode",
                "write-approved",
            ]
        )
        assert "Remembered `cli`" in add_output
        search_output = run_cli_capture(
            [
                "memory",
                "--workspace",
                str(tmp),
                "search",
                "CLI",
                "--tags",
                "cli",
            ]
        )
        assert "CLI memory with tags" in search_output
    finally:
        shutil.rmtree(tmp)


def run_cli_capture(argv: list[str]) -> str:
    stdout = io.StringIO()
    stderr = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
        code = cli_main(argv)
    assert code == 0, stderr.getvalue()
    return stdout.getvalue()


def run_cli_code(argv: list[str]) -> int:
    with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
        return cli_main(argv)


def test_memory_regressions() -> None:
    run_memory_tests()
