"""Integration test: agent loop handles pre-validation rejections correctly.

Proves that when the model proposes a mutation with invalid syntax,
the pre-validation gate rejects it, the agent observes the error,
and the model gets a chance to self-repair without any dirty state.
"""
from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from mind01.agent import Agent
from mind01.config import AgentConfig
from mind01.modes import AgentMode


def test_agent_repairs_after_syntax_rejection(tmp_path: Path) -> None:
    """Agent sends write_file with bad Python → pre-validation rejects →
    agent observes error → model gets repair chance → second attempt
    has valid Python → success."""
    target = tmp_path / "module.py"
    target.write_text("# initial\n", encoding="utf-8")

    config = AgentConfig.build(
        str(tmp_path),
        "model",
        "http://127.0.0.1:11434",
        max_steps=5,
        yes=True,
        dry_run=False,
        allow_write=True,
        mode=AgentMode.WRITE_APPROVED,
    )
    agent = Agent(config)

    # Canned LLM responses:
    # 1. Inspect first (read_file on existing file)
    # 2. Write bad Python → pre-validation rejects
    # 3. Write good Python → succeeds
    # 4. Final response
    replies = [
        # Step 1: read_file to satisfy inspection requirement
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "read_file",
            "arguments": {"path": "module.py"},
        }),
        # Step 2: write_file with invalid Python
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "write_file",
            "arguments": {
                "path": "module.py",
                "content": "def broken(\n",
            },
        }),
        # Step 3: write_file with valid Python (after seeing pre-validation error)
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "write_file",
            "arguments": {
                "path": "module.py",
                "content": "def hello():\n    return 1\n",
            },
        }),
        # Step 4: final response
        json.dumps({
            "schema_version": "1.0",
            "response_type": "final",
            "status": "verified",
            "summary": "Created module.py with hello function.",
            "evidence_refs": [],
        }),
    ]

    with patch.object(agent.llm, "chat", side_effect=replies):
        response = agent.ask("Modify module.py to add a hello function")

    # Verify the pre-validation rejection observation was received by the agent
    assert agent.last_state is not None
    assert any("Pre-validation failed" in obs for obs in agent.last_state.observations), (
        f"Expected Pre-validation failed in observations, got: {agent.last_state.observations}"
    )

    # Verify the file was ultimately written correctly
    assert target.exists()
    content = target.read_text(encoding="utf-8")
    assert "def hello" in content

    # Verify no dirty state was created (the bad write never reached the filesystem)
    dirty_dir = tmp_path / ".mind01" / "mutations" / "dirty"
    if dirty_dir.exists():
        dirty_files = list(dirty_dir.glob("*.json"))
        assert len(dirty_files) == 0, f"Unexpected dirty state files: {dirty_files}"


def test_agent_edit_nonexistent_gets_helpful_error(tmp_path: Path) -> None:
    """Agent tries edit_file on a non-existent file → pre-validation rejects
    with a helpful message suggesting write_file."""
    (tmp_path / "README.md").write_text("project info\n", encoding="utf-8")

    config = AgentConfig.build(
        str(tmp_path),
        "model",
        "http://127.0.0.1:11434",
        max_steps=5,
        yes=True,
        dry_run=False,
        allow_write=True,
        mode=AgentMode.WRITE_APPROVED,
    )
    agent = Agent(config)

    replies = [
        # Step 1: read_file for inspection on existing README.md
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "read_file",
            "arguments": {"path": "README.md"},
        }),
        # Step 2: edit_file on non-existent file
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "edit_file",
            "arguments": {
                "path": "nonexistent.py",
                "old": "old_code",
                "new": "new_code",
            },
        }),
        # Step 3: use write_file instead (correct approach)
        json.dumps({
            "schema_version": "1.0",
            "response_type": "tool_call",
            "tool": "write_file",
            "arguments": {
                "path": "nonexistent.py",
                "content": "new_code\n",
            },
        }),
        # Step 4: final
        json.dumps({
            "schema_version": "1.0",
            "response_type": "final",
            "status": "verified",
            "summary": "Created file.",
            "evidence_refs": [],
        }),
    ]

    with patch.object(agent.llm, "chat", side_effect=replies):
        response = agent.ask("Modify nonexistent.py to fix bad code")

    # The pre-validation error should mention TARGET_NOT_FOUND in the observations
    assert agent.last_state is not None
    assert any("TARGET_NOT_FOUND" in obs for obs in agent.last_state.observations), (
        f"Expected TARGET_NOT_FOUND in observations, got: {agent.last_state.observations}"
    )
