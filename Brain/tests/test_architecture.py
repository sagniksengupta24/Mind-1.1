from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from mind01.planning import Planner
from mind01.policy import PolicyViolation, ServerPolicy
from mind01.routing import HierarchicalRouter
from mind01.skills import SkillRegistry
from mind01.state import AgentState, AgentPhase
from mind01.verification import VerificationEngine
from mind01.modes import AgentMode


def test_router_planner_and_skill_registry() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-routing-"))
    try:
        router = HierarchicalRouter()
        security = router.route("Review API token auth and SSRF risks in api.py", tmp)
        assert security.specialist == "security_review"
        assert security.planning_required
        assert "security regression tests" in security.verification_strategy

        verilog = router.route("Fix counter.sv and verify it with iverilog", tmp)
        assert verilog.specialist == "verilog_verification"

        general = router.route("Explain what an agent is", tmp)
        assert general.specialist == "general_reasoning"

        repository = router.route("Explain the Agent class in agent.py", tmp)
        assert repository.planning_required
        assert not repository.mutation_required
        assert "write_file" not in repository.permitted_tools

        mutation = router.route("Modify agent.py to add a bounded retry", tmp)
        assert mutation.mutation_required
        assert "write_file" in mutation.permitted_tools

        plan = Planner().build("Review API auth", security)
        assert plan.risk_level == "high"
        assert any(step.id == "inspect" for step in plan.steps)
        assert any(step.id == "verify" for step in plan.steps)

        skills = SkillRegistry()
        assert "api_security_review" in {skill.name for skill in skills.select("security_review")}
        assert "safe_code_edit" in skills.names()
    finally:
        shutil.rmtree(tmp)


def test_agent_state_loop_counters() -> None:
    state = AgentState("objective", "read-only", max_steps=4)
    assert state.phase == AgentPhase.RECEIVE
    state.transition(AgentPhase.CLASSIFY)
    assert state.phase == AgentPhase.CLASSIFY
    assert state.record_action("x") == 1
    assert state.record_action("x") == 2
    assert state.record_error("bad") == 1


def test_server_policy_caps_privileges_and_endpoint() -> None:
    policy = ServerPolicy(maximum_mode=AgentMode.PROPOSE, max_steps=8)
    assert policy.resolve_mode("read-only") == AgentMode.READ_ONLY
    assert policy.resolve_mode("propose") == AgentMode.PROPOSE
    try:
        policy.resolve_mode("unsafe")
        raise AssertionError("mode escalation was not rejected")
    except PolicyViolation:
        pass
    try:
        policy.resolve_steps(99)
        raise AssertionError("step escalation was not rejected")
    except PolicyViolation:
        pass
    assert policy.validate_ollama_url("http://127.0.0.1:11434") == "http://127.0.0.1:11434"
    try:
        policy.validate_ollama_url("http://169.254.169.254/latest")
        raise AssertionError("SSRF endpoint was not rejected")
    except PolicyViolation:
        pass


def test_verification_engine_reports_real_evidence() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-verification-"))
    try:
        (tmp / "good.py").write_text("x = 1\n", encoding="utf-8")
        results = VerificationEngine(tmp).verify_paths(["good.py"])
        assert any(item.check == "python-compile" and item.status == "passed" for item in results)

        (tmp / "bad.json").write_text("{bad", encoding="utf-8")
        results = VerificationEngine(tmp).verify_paths(["bad.json"])
        assert any(item.check == "json-parse" and item.status == "failed" and item.blocking for item in results)
    finally:
        shutil.rmtree(tmp)


def test_agent_config_rejects_unbounded_execution() -> None:
    from mind01.config import AgentConfig

    try:
        AgentConfig.build(".", "model", "http://127.0.0.1:11434", 0, False, True)
        raise AssertionError("zero steps were accepted")
    except ValueError as exc:
        assert "between 1 and 64" in str(exc)

    try:
        AgentConfig.build(
            ".", "model", "http://127.0.0.1:11434", 4, False, True,
            request_timeout_seconds=0,
        )
        raise AssertionError("zero timeout was accepted")
    except ValueError as exc:
        assert "request_timeout_seconds" in str(exc)
