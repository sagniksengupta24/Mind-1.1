from __future__ import annotations

import json
from pathlib import Path

import pytest

from mind01.agent import Agent
from mind01.config import AgentConfig
from mind01.intent import ExpectedOutputMode, TaskClass
from mind01.routing import ReasonCode, Specialist, ToolFamily
from mind01.semantic_router_v2 import (
    FAMILY_LIFECYCLE,
    FAMILY_TOOLS,
    TASK_SPECIALIST_FAMILIES,
    TASK_SPECIALISTS,
    DecisionSource,
    FirstLifecycleStep,
    ModelCallStats,
    OllamaSemanticClassifier,
    RouteSelectionPrediction,
    RouterThresholds,
    SemanticRouterV2,
    TaskPrediction,
    normalize_request,
    parse_route_selection,
    parse_task_prediction,
    reduce_candidates,
    route_selection_schema,
    strict_json_object,
    task_prediction_schema,
)
from mind01.llm import LLMError
from mind01.tools.schemas import SCHEMA_BY_NAME


ROOT = Path(__file__).resolve().parents[1]


def route(
    prompt: str,
    *,
    mode: str = "read-only",
    write: bool = False,
    shell: bool = False,
):
    return SemanticRouterV2().route_typed(
        prompt,
        ROOT,
        mode=mode,
        allow_write=write,
        allow_shell=shell,
    )


def test_taxonomy_matrices_are_total_bounded_and_have_no_orphans() -> None:
    assert set(TASK_SPECIALISTS) == set(TaskClass)
    assert all(1 <= len(items) <= 5 for items in TASK_SPECIALISTS.values())
    assert set(TASK_SPECIALIST_FAMILIES) == {
        (task, specialist)
        for task, specialists in TASK_SPECIALISTS.items()
        for specialist in specialists
    }
    assert set(FAMILY_TOOLS) == set(ToolFamily)
    assert set(FAMILY_LIFECYCLE) == set(ToolFamily)
    assert set().union(*map(set, FAMILY_TOOLS.values())) <= set(SCHEMA_BY_NAME)
    assert set().union(*map(set, TASK_SPECIALIST_FAMILIES.values())) == set(ToolFamily)


def test_normalization_features_are_bounded_hints() -> None:
    normalized = normalize_request(
        "Review src/auth.py without changing files and do not run shell commands.",
        ROOT,
    )
    assert normalized.repository_context
    assert normalized.file_paths == ("src/auth.py",)
    assert normalized.edits_prohibited
    assert normalized.shell_prohibited
    assert not normalized.mutation_requested
    assert len(normalized.signals) < 20


def test_v2_new_mutation_verbs_set_mutation_requested() -> None:
    prompts = (
        "Add a new LLM provider option called 'groq' alongside openrouter.",
        "Insert a validation check before the request is dispatched.",
        "Append a fallback model to the provider chain.",
        "Rename the AgentConfig field 'model' to 'llm_model' everywhere in the codebase.",
        "Remove the legacy provider shim from config.py.",
        "Delete the unused compatibility module.",
    )
    for prompt in prompts:
        assert normalize_request(prompt, ROOT).mutation_requested, prompt


def test_v2_arithmetic_add_is_not_mutation() -> None:
    assert not normalize_request("Add 2 and 2.", ROOT).mutation_requested


def test_v2_bounded_constraint_keeps_mutation_intent() -> None:
    assert normalize_request(
        "Add a new LLM provider option called 'groq'. Do not change any existing provider's behavior.",
        ROOT,
    ).mutation_requested


def test_policy_response_and_tool_intersection_fail_closed() -> None:
    answer = route("Explain why immutable data structures are useful.")
    assert answer.response_mode == ExpectedOutputMode.FINAL_ANSWER
    assert answer.allowed_tools == answer.terminal_tools == ()
    assert answer.first_lifecycle_step == FirstLifecycleStep.ANSWER

    read_only = route("Edit src/auth.py to reject expired tokens.")
    assert read_only.response_mode == ExpectedOutputMode.BLOCKED
    assert not read_only.allowed_tools
    assert not set(read_only.terminal_tools) & {"edit_file", "write_file"}

    prohibited = route(
        "Delete every repository file with rm -rf.",
        mode="unsafe",
        write=True,
        shell=True,
    )
    assert prohibited.risk_level.value == "critical"
    assert prohibited.reason_code == ReasonCode.POLICY_BLOCKED
    assert prohibited.first_lifecycle_step == FirstLifecycleStep.REFUSAL
    assert prohibited.allowed_tools == ()

    clarify = route(
        "Fix the handler; it is not identified.",
        mode="write-approved",
        write=True,
    )
    assert clarify.response_mode == ExpectedOutputMode.CLARIFICATION
    assert clarify.first_lifecycle_step == FirstLifecycleStep.CLARIFICATION
    assert clarify.allowed_tools == ()


def test_lifecycle_never_mutates_before_inspection() -> None:
    mutation = route(
        "Modify src/cache.py to bound retries.",
        mode="write-approved",
        write=True,
    )
    assert mutation.task_class == TaskClass.MUTATION
    assert mutation.first_lifecycle_step == FirstLifecycleStep.INSPECTION
    assert set(mutation.allowed_tools) <= {"read_file", "search_code"}
    assert mutation.terminal_tools == ("edit_file",)

    understanding = route("Map this repository and summarize its packages.")
    assert understanding.first_lifecycle_step == FirstLifecycleStep.INSPECTION
    assert not set(understanding.allowed_tools) & {"edit_file", "write_file"}

    verification = route(
        "Run pytest for src/cache.py and report the result.",
        mode="write-approved",
        shell=True,
    )
    assert verification.first_lifecycle_step == FirstLifecycleStep.VERIFICATION
    assert verification.allowed_tools == ("run_command",)


def test_reason_codes_are_derived_from_resolved_fields() -> None:
    cases = (
        ("Find references to normalize_request in the repository.", ReasonCode.REFERENCE_SEARCH),
        ("Search the current documentation for retry guidance.", ReasonCode.DOCUMENTATION_LOOKUP),
        ("Recall the saved project decision about retries.", ReasonCode.MEMORY_LOOKUP),
        ("Explain cache eviction conceptually.", ReasonCode.DIRECT_EXPLANATION),
    )
    for prompt, expected in cases:
        assert route(prompt).reason_code == expected
    for state in (route(prompt) for prompt, _ in cases):
        reason_entries = [
            item for item in state.decision_trace if item.field == "reason_code"
        ]
        assert len(reason_entries) == 1
        assert reason_entries[0].source == DecisionSource.DETERMINISTIC_RULE


class LowConfidenceClassifier:
    model_identity = "low-confidence-test"

    def __init__(self) -> None:
        self.stats = ModelCallStats()

    def predict_task(self, request):  # type: ignore[no-untyped-def]
        return TaskPrediction(TaskClass.MUTATION, 0.1)

    def select_route(self, request, task_class, candidates):  # type: ignore[no-untyped-def]
        specialist = next(iter(candidates))
        return RouteSelectionPrediction(
            specialist,
            0.1,
            candidates[specialist][0],
            0.1,
        )


def test_low_confidence_abstains_without_permission_expansion() -> None:
    state = SemanticRouterV2(
        LowConfidenceClassifier(),
        thresholds=RouterThresholds(task_class=0.8),
    ).route_typed("Review this repository.", ROOT)
    assert state.abstained
    assert state.fallback_reason == "task_class_below_threshold"
    assert state.confidence <= 0.6
    assert not set(state.allowed_tools) & {"edit_file", "write_file", "run_command"}
    assert any(
        item.source == DecisionSource.FALLBACK
        for item in state.decision_trace
        if item.field in {"task_class", "specialist"}
    )


class ContradictoryClassifier:
    model_identity = "contradiction-test"

    def __init__(self, *, verification: bool = False) -> None:
        self.verification = verification
        self.stats = ModelCallStats()

    def predict_task(self, request):  # type: ignore[no-untyped-def]
        return TaskPrediction(
            TaskClass.VERIFICATION if self.verification else TaskClass.EXPLANATION,
            0.99,
        )

    def select_route(self, request, task_class, candidates):  # type: ignore[no-untyped-def]
        if self.verification:
            return RouteSelectionPrediction(
                Specialist.DEBUGGING,
                0.9,
                ToolFamily.FILE_INSPECTION,
                0.9,
            )
        return RouteSelectionPrediction(
            Specialist.REPOSITORY_INSPECTOR,
            0.9,
            ToolFamily.REPOSITORY_DISCOVERY,
            0.9,
        )


def test_model_policy_and_execution_family_disagreements_are_bounded() -> None:
    repository = SemanticRouterV2(ContradictoryClassifier()).route_typed(
        "Map this repository and identify its packages.", ROOT
    )
    assert repository.task_class == TaskClass.INSPECTION
    assert repository.immediate_family == ToolFamily.REPOSITORY_DISCOVERY
    assert repository.fallback_reason == "task_response_mode_disagreement"
    task_trace = next(
        entry for entry in repository.decision_trace if entry.field == "task_class"
    )
    assert task_trace.input["predicted_task_class"] == "explanation"
    assert task_trace.source == DecisionSource.COMPATIBILITY_MATRIX

    execution = SemanticRouterV2(
        ContradictoryClassifier(verification=True)
    ).route_typed(
        "Run diagnostic tests for failing src/api.py.",
        ROOT,
        mode="write-approved",
        allow_shell=True,
    )
    assert execution.immediate_family == ToolFamily.EXECUTION_VERIFICATION
    assert execution.first_lifecycle_step == FirstLifecycleStep.VERIFICATION
    assert execution.fallback_reason == "execution_family_disagreement"


def valid_task_payload() -> dict:
    return {
        "schema_version": "2.0",
        "task_class": "inspection",
        "confidence": 0.9,
        "alternatives": [{"task_class": "explanation", "confidence": 0.08}],
        "evidence_summary": "Repository evidence is requested.",
    }


@pytest.mark.parametrize(
    "raw",
    (
        "preamble " + json.dumps(valid_task_payload()),
        "{}",
        "null",
        '{"schema_version":"2.0","task_class":"inspection","task_class":"mutation","confidence":0.9,"alternatives":[],"evidence_summary":""}',
        "{malformed",
        json.dumps({**valid_task_payload(), "task_class": "invented"}),
        json.dumps({**valid_task_payload(), "confidence": None}),
        json.dumps({**valid_task_payload(), "extra": True}),
        "{" + '"padding":"' + ("x" * 9_000) + '"}',
    ),
)
def test_task_parser_rejects_malformed_or_unconstrained_output(raw: str) -> None:
    with pytest.raises(ValueError):
        parse_task_prediction(raw)


def test_strict_parsers_and_schemas_accept_only_shortlisted_values() -> None:
    parsed = parse_task_prediction(json.dumps(valid_task_payload()))
    assert parsed.task_class == TaskClass.INSPECTION
    assert task_prediction_schema()["additionalProperties"] is False

    request = normalize_request("Read src/agent.py.", ROOT)
    candidates = reduce_candidates(
        TaskClass.INSPECTION, request, ExpectedOutputMode.ACTION
    )
    specialist = Specialist.REPOSITORY_INSPECTOR
    payload = {
        "schema_version": "2.0",
        "specialist": specialist.value,
        "specialist_confidence": 0.9,
        "immediate_family": ToolFamily.FILE_INSPECTION.value,
        "family_confidence": 0.88,
        "alternative_family": ToolFamily.REPOSITORY_DISCOVERY.value,
        "evidence_summary": "A named file requires inspection.",
    }
    assert parse_route_selection(json.dumps(payload), candidates).immediate_family == ToolFamily.FILE_INSPECTION
    with pytest.raises(ValueError, match="shortlist"):
        parse_route_selection(
            json.dumps({**payload, "specialist": "implementation"}),
            candidates,
        )
    schema = route_selection_schema(candidates)
    assert {
        branch["properties"]["specialist"]["const"]
        for branch in schema["oneOf"]
    } == {item.value for item in candidates}
    with pytest.raises(ValueError, match="duplicate"):
        strict_json_object('{"a": 1, "a": 2}')


def test_every_final_route_has_trace_sources_and_passes_solver() -> None:
    prompts = (
        "Explain bounded retries.",
        "Read src/agent.py and summarize it.",
        "Find references to Agent in this repository.",
        "Run pytest for src/agent.py.",
        "Edit src/agent.py to bound retries.",
        "Fix the handler; it is not identified.",
    )
    for prompt in prompts:
        state = route(
            prompt,
            mode="write-approved",
            write=True,
            shell=True,
        )
        assert state.solver.valid
        traced = {entry.field for entry in state.decision_trace}
        assert {
            "task_class",
            "response_mode",
            "risk_level",
            "specialist",
            "immediate_family",
            "allowed_tools",
            "first_lifecycle_step",
            "reason_code",
            "hard_constraints",
            "solver",
        } <= traced


def test_v2_feature_flag_and_comparison_mode_preserve_runtime_contract(tmp_path: Path) -> None:
    v2 = Agent(
        AgentConfig.build(
            str(tmp_path),
            "test-model",
            "http://127.0.0.1:11434",
            4,
            False,
            True,
            semantic_router="v2",
        )
    )
    response = v2.ask("Explain bounded retries.")
    assert response.routing_decision["router_version"] == "semantic_router_v2"

    comparison = Agent(
        AgentConfig.build(
            str(tmp_path),
            "test-model",
            "http://127.0.0.1:11434",
            4,
            False,
            True,
            semantic_router="compare",
        )
    )
    compared = comparison.ask("Read src/agent.py and summarize it.")
    assert compared.routing_decision["schema_version"] == "1.0"
    assert comparison.last_router_comparison["runtime_router"] == "legacy"


def test_invalid_router_configuration_is_rejected() -> None:
    with pytest.raises(ValueError, match="semantic_router"):
        AgentConfig.build(".", "model", "http://127.0.0.1:11434", 4, False, True, semantic_router="random")


class QueuedClient:
    model = "queued-test-model"

    def __init__(self, outputs):  # type: ignore[no-untyped-def]
        self.outputs = list(outputs)

    def chat(self, messages, json_mode=True, *, response_schema=None):  # type: ignore[no-untyped-def]
        output = self.outputs.pop(0)
        if isinstance(output, Exception):
            raise output
        return output


def route_payload() -> dict:
    return {
        "schema_version": "2.0",
        "specialist": "repository_inspector",
        "specialist_confidence": 0.9,
        "immediate_family": "file_inspection",
        "family_confidence": 0.9,
        "alternative_family": "repository_discovery",
        "evidence_summary": "A named source file is requested.",
    }


def test_model_classifier_normal_budget_and_bounded_repair() -> None:
    task = json.dumps(valid_task_payload())
    selected = json.dumps(route_payload())
    normal = OllamaSemanticClassifier(QueuedClient([task, selected]))  # type: ignore[arg-type]
    state = SemanticRouterV2(normal).route_typed("Read src/agent.py.", ROOT)
    assert state.model_call_stats["model_calls"] == 2
    assert state.model_call_stats["retries"] == 0

    repaired = OllamaSemanticClassifier(  # type: ignore[arg-type]
        QueuedClient(["model refusal", task, selected])
    )
    repaired_state = SemanticRouterV2(repaired).route_typed(
        "Read src/agent.py.", ROOT
    )
    assert repaired_state.model_call_stats["model_calls"] == 3
    assert repaired_state.model_call_stats["retries"] == 1
    assert repaired_state.model_call_stats["schema_failures"] == 1


def test_model_classifier_repair_exhaustion_and_timeout_fall_back_safely() -> None:
    exhausted = OllamaSemanticClassifier(  # type: ignore[arg-type]
        QueuedClient(["not json", "still not json"])
    )
    state = SemanticRouterV2(exhausted).route_typed(
        "Read src/agent.py.", ROOT
    )
    assert state.abstained
    assert "ValueError" in state.fallback_reason
    assert not set(state.allowed_tools) & {"edit_file", "write_file"}

    timed_out = OllamaSemanticClassifier(  # type: ignore[arg-type]
        QueuedClient([LLMError("request timeout"), LLMError("request timeout")])
    )
    timeout_state = SemanticRouterV2(timed_out).route_typed(
        "Read src/agent.py.", ROOT
    )
    assert timeout_state.abstained
    assert timeout_state.model_call_stats["model_calls"] == 2
