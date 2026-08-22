from __future__ import annotations

import contextlib
import io
import json
import shutil
import tempfile
from pathlib import Path

from mind01.agent import Agent
from mind01.cli import main as cli_main
from mind01.config import AgentConfig
from mind01.tools import ToolError, ToolRegistry
from mind01.traces import TraceStore


def run_trace_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-traces-"))
    try:
        (tmp / "src").mkdir()
        (tmp / "src" / "demo.py").write_text("print('hello')\n", encoding="utf-8")
        tools = ToolRegistry(tmp, yes=True)

        result = tools.call("read_file", {"path": "src/demo.py"})
        assert "hello" in result.text
        events = read_events(tmp)
        read_event = events[-1]
        assert read_event["event_type"] == "tool_call"
        assert read_event["tool_name"] == "read_file"
        assert read_event["policy_decision"] == "allowed"
        assert read_event["tool_result_summary"]["size"] > 0

        try:
            tools.call("write_file", {"path": "src/blocked.py", "content": "x = 1\n"})
            raise AssertionError("read-only write was not blocked")
        except ToolError:
            pass
        blocked_event = read_events(tmp)[-1]
        assert blocked_event["tool_name"] == "write_file"
        assert blocked_event["policy_decision"] == "blocked"
        assert "read-only" in blocked_event["error"]

        write_tools = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            mode="write-approved",
        )
        write_tools.call(
            "write_file",
            {"path": "src/secret.py", "content": "token=abc123\nvalue = 1\n"},
        )
        write_event = read_events(tmp)[-1]
        assert write_event["tool_name"] == "write_file"
        assert write_event["receipt_id"]
        serialized = json.dumps(write_event, sort_keys=True)
        assert "abc123" not in serialized
        assert "[REDACTED]" in serialized

        config = AgentConfig.build(
            workspace=str(tmp),
            model="qwen2.5-coder:7b",
            ollama_url="http://127.0.0.1:11434",
            max_steps=1,
            yes=True,
            dry_run=True,
        )
        response = Agent(config).ask("hello token=abc123")
        assert "Dry run ready" in response.text
        agent_events = read_events(tmp)
        assert any(item["event_type"] == "agent_prompt" for item in agent_events)
        agent_serialized = "\n".join(json.dumps(item, sort_keys=True) for item in agent_events)
        assert "abc123" not in agent_serialized

        store = TraceStore(tmp)
        listed = store.list()
        assert listed
        file_name = listed[0]["file"]
        show_file = run_cli_capture(["traces", "--workspace", str(tmp), "show", file_name])
        assert "\n" in show_file
        for line in show_file.splitlines():
            if line.strip():
                json.loads(line)
        event_id = write_event["event_id"]
        show_event = run_cli_capture(["traces", "--workspace", str(tmp), "show", event_id])
        shown = json.loads(show_event)
        assert shown["event_id"] == event_id
        list_output = run_cli_capture(["traces", "--workspace", str(tmp), "list"])
        assert file_name in list_output
    finally:
        shutil.rmtree(tmp)


def read_events(workspace: Path) -> list[dict]:
    root = workspace / ".mind01" / "traces"
    events = []
    for path in sorted(root.glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    assert events
    return events


def run_cli_capture(argv: list[str]) -> str:
    stdout = io.StringIO()
    with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(io.StringIO()):
        code = cli_main(argv)
    assert code == 0
    return stdout.getvalue()


def test_trace_regressions() -> None:
    run_trace_tests()
