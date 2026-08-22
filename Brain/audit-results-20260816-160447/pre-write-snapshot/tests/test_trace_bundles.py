"""Workstream 5 — task-bundle trace recording tests.

Bundles are consent-gated records appended to the SAME hash-chained TraceStore
as every other trace event (no parallel logging system).  They sanitize prompt
content and tool payloads, and they must never break the agent loop.
"""

from __future__ import annotations

import json
from pathlib import Path

from mind01.config import AgentConfig
from mind01.modes import AgentMode
from mind01.traces import TraceStore, verify_trace_chain


def _config(workspace: Path, trace_bundles: bool) -> AgentConfig:
    return AgentConfig.build(
        workspace=str(workspace),
        model="qwen2.5-coder:7b",
        ollama_url="http://127.0.0.1:11434",
        max_steps=4,
        yes=False,
        dry_run=False,
        allow_write=True,
        allow_shell=True,
        mode=AgentMode.WRITE_APPROVED.value,
        trace_bundles=trace_bundles,
    )


def test_task_bundle_recorded_when_enabled(tmp_path: Path) -> None:
    store = TraceStore(tmp_path)
    bundle = {
        "consent": True,
        "consent_source": "test",
        "session_id": "sess-1",
        "model_name": "qwen2.5-coder:7b",
        "mode": "write-approved",
        "prompt": "Create hardware/and_gate.v with an AND gate module.",
        "action_sequence": [
            {
                "tool": "write_file",
                "args": {"path": "hardware/and_gate.v", "content": "module and_gate(a,b,y); endmodule"},
            }
        ],
        "verification": [{"check": "iverilog-syntax", "status": "unavailable"}],
        "completion_status": "verified",
        "steps": 3,
        "latency_ms": 1200,
        "workspace_name": tmp_path.name,
    }
    item = store.record_task_bundle(bundle)
    assert item["event_type"] == "task_bundle"
    assert item["consent"] is True
    # Prompt content must be stored as a summary record (hash + bounded
    # redacted preview), not as a raw content field.
    assert isinstance(item["prompt"], dict)
    assert "sha256" in item["prompt"]
    assert "preview" in item["prompt"]
    assert item["prompt"]["size"] > 0
    # Tool file content must be summarized, not stored raw.
    action = item["action_sequence"][0]
    assert isinstance(action["args"]["content"], dict)
    assert "sha256" in action["args"]["content"]
    assert "size" in action["args"]["content"]
    assert "preview" in action["args"]["content"]
    # The bundle participates in the hash chain.
    status = verify_trace_chain(tmp_path)
    assert status["status"] == "valid", status


def test_task_bundle_skipped_without_consent(tmp_path: Path) -> None:
    store = TraceStore(tmp_path)
    result = store.record_task_bundle({"consent": False, "prompt": "secret stuff"})
    assert result.get("consent_required") is True
    status = verify_trace_chain(tmp_path)
    assert status["status"] == "empty" or status["verified_count"] == 0


def test_agent_records_bundle_only_when_configured(tmp_path: Path) -> None:
    from unittest.mock import patch

    from mind01.agent import Agent

    final = json.dumps(
        {
            "schema_version": "1.0",
            "response_type": "final",
            "status": "unverified",
            "summary": "Noted.",
            "evidence_refs": [],
        }
    )
    for enabled in (True, False):
        workspace = tmp_path / f"ws-{enabled}"
        workspace.mkdir()
        agent = Agent(_config(workspace, trace_bundles=enabled))
        with patch("mind01.agent.OllamaClient.chat", return_value=final):
            response = agent.ask("Say hello")
        assert response.text == "Noted."
        status = verify_trace_chain(workspace)
        bundles = [
            item
            for item in _read_all(workspace)
            if item.get("event_type") == "task_bundle"
        ]
        if enabled:
            assert bundles, "expected a task bundle when trace_bundles enabled"
            assert status["status"] == "valid"
        else:
            assert not bundles, "no bundle should be recorded when disabled"


def _read_all(workspace: Path) -> list[dict]:
    events: list[dict] = []
    for path in sorted((workspace / ".mind01" / "traces").glob("*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                events.append(json.loads(line))
    return events
