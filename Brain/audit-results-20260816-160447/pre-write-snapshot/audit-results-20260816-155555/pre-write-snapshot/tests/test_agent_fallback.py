from __future__ import annotations

import shutil
import tempfile
import json
from pathlib import Path
from unittest.mock import patch

from mind01.agent import (
    Agent,
    build_deterministic_domain_repair_answer,
    build_preflight_deterministic_answer,
    get_final_quality_issue,
)
from mind01.config import AgentConfig
from mind01.modes import AgentMode
from mind01.prompts import SYSTEM_PROMPT


def _config(tmp: Path, mode: AgentMode = AgentMode.READ_ONLY, max_steps: int = 4) -> AgentConfig:
    return AgentConfig.build(
        workspace=str(tmp),
        model="qwen2.5-coder:7b",
        ollama_url="http://127.0.0.1:11434",
        max_steps=max_steps,
        yes=True,
        dry_run=False,
        allow_write=mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE},
        mode=mode,
    )


def test_system_prompt_has_strict_examples() -> None:
    assert "canonical JSON" in SYSTEM_PROMPT
    assert "Never emit XML" in SYSTEM_PROMPT
    assert "Markdown fences" in SYSTEM_PROMPT


def test_canonical_final_and_route_state() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-fallback-"))
    try:
        agent = Agent(_config(tmp))
        output = json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"Hello from the agent.","evidence_refs":[]})
        with patch.object(agent.llm, "chat", return_value=output):
            response = agent.ask("Say hello")
        assert response.text == "Hello from the agent."
        assert response.specialist == "general_reasoning"
        assert agent.last_state is not None and agent.last_state.completed
    finally:
        shutil.rmtree(tmp)


def test_malformed_action_is_repaired_without_executing_loose_json() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-parser-repair-"))
    try:
        agent = Agent(_config(tmp))
        replies = [
            '{"tool":"run_command","args":{"command":"rm -rf /"}}',
            json.dumps({"schema_version":"1.0","response_type":"final","status":"policy_denied","summary":"Rejected malformed action safely.","evidence_refs":[]}),
        ]
        with patch.object(agent.llm, "chat", side_effect=replies) as chat, patch.object(
            agent.tools, "call", side_effect=AssertionError("loose JSON must never execute")
        ):
            response = agent.ask("Explain why that command is unsafe")
        assert response.text == "Rejected malformed action safely."
        assert chat.call_count == 2
        assert any("parser_failure=SCHEMA_VERSION_MISMATCH" in item for item in response.trace)
        assert any("Error code: SCHEMA_VERSION_MISMATCH" in item["content"] for item in agent.messages)
    finally:
        shutil.rmtree(tmp)


def test_repository_answer_requires_real_tool_grounding() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-grounding-"))
    try:
        (tmp / "api.py").write_text("def health():\n    return {'ok': True}\n", encoding="utf-8")
        agent = Agent(_config(tmp))
        replies = [
            json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"The route probably returns ok.","evidence_refs":[]}),
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"read_file","arguments":{"path":"api.py"}}),
            json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"api.py defines health(), which returns {'ok': True}.","evidence_refs":[]}),
        ]
        with patch.object(agent.llm, "chat", side_effect=replies):
            response = agent.ask("Inspect api.py and explain the health function")
        assert "returns {'ok': True}" in response.text
        assert any("FINAL_ANSWER_WHEN_ACTION_REQUIRED" in item for item in response.trace)
        assert any("tool read_file -> ok" in item for item in response.trace)
        assert response.specialist == "repository_understanding"
    finally:
        shutil.rmtree(tmp)


def test_generation_only_task_cannot_mutate_workspace() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-generation-guard-"))
    try:
        agent = Agent(_config(tmp, AgentMode.PROPOSE))
        replies = [
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"propose_write_file","arguments":{"path":"demo.py","content":"x=1","reason":"demo"}}),
            json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"Here is the requested example: `x = 1`.","evidence_refs":[]}),
        ]
        with patch.object(agent.llm, "chat", side_effect=replies), patch.object(
            agent.tools, "call", side_effect=AssertionError("mutation must be blocked")
        ):
            response = agent.ask("Generate a tiny Python example without saving it")
        assert "x = 1" in response.text
        assert any("UNKNOWN_TOOL" in item for item in response.trace)
    finally:
        shutil.rmtree(tmp)


def test_benchmark_specific_canned_repair_was_removed() -> None:
    assert build_preflight_deterministic_answer("Explain recursion with a railway analogy") is None
    assert build_deterministic_domain_repair_answer("Write a BCD counter", "parser_error") is None
    assert get_final_quality_issue("Please provide a valid command or request.", "Explain recursion") == "generic non-answer"


def test_route_policy_blocks_unrelated_mutation_tool() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-route-policy-"))
    try:
        (tmp / "agent.py").write_text("class Agent:\n    pass\n", encoding="utf-8")
        agent = Agent(_config(tmp, AgentMode.WRITE_APPROVED, max_steps=4))
        replies = [
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"write_file","arguments":{"path":"agent.py","content":"bad"}}),
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"read_file","arguments":{"path":"agent.py"}}),
            json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"agent.py defines an empty Agent class.","evidence_refs":[]}),
        ]
        original_call = agent.tools.call

        def guarded_call(name, args):  # type: ignore[no-untyped-def]
            assert name != "write_file", "route policy should block the unrelated mutation"
            return original_call(name, args)

        with patch.object(agent.llm, "chat", side_effect=replies), patch.object(
            agent.tools, "call", side_effect=guarded_call
        ):
            response = agent.ask("Explain the Agent class in agent.py")
        assert "empty Agent class" in response.text
        assert any("UNSAFE_ACTION" in item for item in response.trace)
    finally:
        shutil.rmtree(tmp)


def test_successful_mutation_attaches_verification_evidence() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-verification-summary-"))
    try:
        (tmp / "good.py").write_text("x = 0\n", encoding="utf-8")
        agent = Agent(_config(tmp, AgentMode.WRITE_APPROVED, max_steps=4))
        replies = [
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"read_file","arguments":{"path":"good.py"}}),
            json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"write_file","arguments":{"path":"good.py","content":"x = 1\n"}}),
            json.dumps({"schema_version":"1.0","response_type":"final","status":"verified","summary":"Updated good.py.","evidence_refs":["verification-001"]}),
        ]
        with patch.object(agent.llm, "chat", side_effect=replies):
            response = agent.ask("Modify good.py so x equals 1")
        assert "PASSED verification-001 python-executable-structure" in response.text
        assert "PASSED verification-002 python-compile" in response.text
        assert "Result status: relevant deterministic checks passed." in response.text
        assert any(item["status"] == "passed" for item in response.verification)
    finally:
        shutil.rmtree(tmp)


def run_agent_fallback_tests() -> None:
    test_system_prompt_has_strict_examples()
    test_canonical_final_and_route_state()
    test_malformed_action_is_repaired_without_executing_loose_json()
    test_repository_answer_requires_real_tool_grounding()
    test_generation_only_task_cannot_mutate_workspace()
    test_benchmark_specific_canned_repair_was_removed()
    test_route_policy_blocks_unrelated_mutation_tool()
    test_successful_mutation_attaches_verification_evidence()
