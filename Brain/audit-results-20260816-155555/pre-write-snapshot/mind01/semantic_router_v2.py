"""Versioned staged semantic router for local, schema-constrained classifiers.

Semantic model judgment is deliberately limited to task class and a reduced
specialist/family selection. Policy, risk, tools, lifecycle, reason codes,
compatibility, confidence fallback, and the final validity decision are
deterministic.
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import dataclass, field, replace
from enum import Enum
from pathlib import Path
from typing import Any, Mapping, Protocol

from .intent import (
    Ambiguity,
    AmbiguityLevel,
    Capability,
    ExpectedOutputMode,
    InterpretationIncidentCode,
    NormalizedIntent,
    RiskLevel,
    TargetKind,
    TaskClass,
)
from .llm import LLMError, Message, OllamaClient
from .modes import AgentMode, parse_agent_mode
from .routing import (
    ReasonCode,
    RoutingDecision,
    Specialist,
    ToolFamily,
    _capability_fingerprint,
)
from .tool_exposure import LifecyclePhase
from .tools.schemas import SCHEMA_BY_NAME


SCHEMA_VERSION = "2.0"
ROUTER_VERSION = "semantic_router_v2"
MAX_ROUTING_OUTPUT_BYTES = 8_192
MUTATION_TOOLS = frozenset(
    name
    for name, schema in SCHEMA_BY_NAME.items()
    if schema.can_write or schema.mutates_runtime
)
LIVE_WRITE_TOOLS = frozenset(
    name for name, schema in SCHEMA_BY_NAME.items() if schema.can_write
)
SHELL_TOOLS = frozenset(
    name for name, schema in SCHEMA_BY_NAME.items() if schema.can_run_shell
)


class DecisionSource(str, Enum):
    MODEL = "model"
    DETERMINISTIC_RULE = "deterministic_rule"
    POLICY_ENGINE = "policy_engine"
    COMPATIBILITY_MATRIX = "compatibility_matrix"
    FALLBACK = "fallback"
    DEFAULT = "default"


class ConstraintSeverity(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    PROHIBITED = "prohibited"


class FirstLifecycleStep(str, Enum):
    INSPECTION = LifecyclePhase.INSPECTION.value
    PROPOSAL = LifecyclePhase.PROPOSAL.value
    MUTATION = LifecyclePhase.MUTATION.value
    VERIFICATION = LifecyclePhase.VERIFICATION.value
    ANSWER = LifecyclePhase.ANSWER.value
    CLARIFICATION = "clarification"
    REFUSAL = "refusal"


@dataclass(frozen=True)
class DecisionTraceEntry:
    field: str
    source: DecisionSource
    rule: str
    input: Mapping[str, Any]
    output: Any

    def to_dict(self) -> dict[str, Any]:
        return {
            "field": self.field,
            "source": self.source.value,
            "rule": self.rule,
            "input": _json_safe(dict(self.input)),
            "output": _json_safe(self.output),
        }


@dataclass(frozen=True)
class HardConstraint:
    identifier: str
    trigger: str
    source: DecisionSource
    severity: ConstraintSeverity
    effect: str
    override_policy: str = "not_overridable"

    def to_dict(self) -> dict[str, str]:
        return {
            "identifier": self.identifier,
            "trigger": self.trigger,
            "source": self.source.value,
            "severity": self.severity.value,
            "effect": self.effect,
            "override_policy": self.override_policy,
        }


@dataclass(frozen=True)
class NormalizedRequest:
    text: str
    repository_context: bool
    mutation_requested: bool
    proposal_requested: bool
    execution_requested: bool
    explanation_only: bool
    external_information: bool
    security_sensitive: bool
    debugging_requested: bool
    missing_context: bool
    file_paths: tuple[str, ...]
    verification_requested: bool
    tools_prohibited: bool
    edits_prohibited: bool
    shell_prohibited: bool
    network_prohibited: bool
    destructive_operation: bool
    protected_path: bool
    outside_workspace: bool
    programming_language: str
    requested_artifact: str
    signals: tuple[str, ...]

    def public_features(self) -> dict[str, Any]:
        """Return bounded non-secret hints suitable for classifier prompts."""

        return {
            "repository_context": self.repository_context,
            "mutation_requested": self.mutation_requested,
            "proposal_requested": self.proposal_requested,
            "execution_requested": self.execution_requested,
            "explanation_only": self.explanation_only,
            "external_information": self.external_information,
            "security_sensitive": self.security_sensitive,
            "debugging_requested": self.debugging_requested,
            "missing_context": self.missing_context,
            "file_reference_count": len(self.file_paths),
            "verification_requested": self.verification_requested,
            "tools_prohibited": self.tools_prohibited,
            "edits_prohibited": self.edits_prohibited,
            "programming_language": self.programming_language,
            "requested_artifact": self.requested_artifact,
        }

    def to_dict(self) -> dict[str, Any]:
        return {
            **self.public_features(),
            "text": self.text,
            "file_paths": list(self.file_paths),
            "shell_prohibited": self.shell_prohibited,
            "network_prohibited": self.network_prohibited,
            "destructive_operation": self.destructive_operation,
            "protected_path": self.protected_path,
            "outside_workspace": self.outside_workspace,
            "signals": list(self.signals),
        }


@dataclass(frozen=True)
class AlternativeTask:
    task_class: TaskClass
    confidence: float


@dataclass(frozen=True)
class TaskPrediction:
    task_class: TaskClass
    confidence: float
    alternatives: tuple[AlternativeTask, ...] = ()
    evidence_summary: str = ""
    source: DecisionSource = DecisionSource.MODEL


@dataclass(frozen=True)
class RouteSelectionPrediction:
    specialist: Specialist
    specialist_confidence: float
    immediate_family: ToolFamily
    family_confidence: float
    alternative_family: ToolFamily | None = None
    evidence_summary: str = ""
    source: DecisionSource = DecisionSource.MODEL


@dataclass
class ModelCallStats:
    calls: int = 0
    retries: int = 0
    schema_failures: int = 0
    latency_ms: float = 0.0
    parsing_ms: float = 0.0
    estimated_input_chars: int = 0
    estimated_output_chars: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "model_calls": self.calls,
            "retries": self.retries,
            "schema_failures": self.schema_failures,
            "latency_ms": round(self.latency_ms, 3),
            "parsing_ms": round(self.parsing_ms, 3),
            "estimated_input_chars": self.estimated_input_chars,
            "estimated_output_chars": self.estimated_output_chars,
        }


class SemanticClassifier(Protocol):
    stats: ModelCallStats
    model_identity: str

    def predict_task(self, request: NormalizedRequest) -> TaskPrediction:
        ...

    def select_route(
        self,
        request: NormalizedRequest,
        task_class: TaskClass,
        candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
    ) -> RouteSelectionPrediction:
        ...


@dataclass(frozen=True)
class RouterThresholds:
    task_class: float = 0.70
    specialist: float = 0.68
    immediate_family: float = 0.66
    disagreement: float = 0.12


@dataclass(frozen=True)
class SolverResult:
    valid: bool
    violations: tuple[str, ...]
    repairs_applied: tuple[str, ...]
    final_confidence: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "valid": self.valid,
            "violations": list(self.violations),
            "repairs_applied": list(self.repairs_applied),
            "final_confidence": self.final_confidence,
        }


@dataclass(frozen=True)
class SemanticRouteState:
    request_id: str
    normalized_request: NormalizedRequest
    task_class: TaskClass
    response_mode: ExpectedOutputMode
    risk_level: RiskLevel
    hard_constraints: tuple[HardConstraint, ...]
    specialist: Specialist
    immediate_family: ToolFamily
    allowed_tools: tuple[str, ...]
    terminal_tools: tuple[str, ...]
    first_lifecycle_step: FirstLifecycleStep
    reason_code: ReasonCode
    confidence: float
    abstained: bool
    fallback_reason: str
    decision_trace: tuple[DecisionTraceEntry, ...]
    schema_version: str
    router_version: str
    model_identity: str
    model_call_stats: Mapping[str, Any]
    solver: SolverResult
    candidate_specialists: tuple[Specialist, ...] = ()

    def __post_init__(self) -> None:
        if self.schema_version != SCHEMA_VERSION:
            raise ValueError("unsupported semantic route state schema version")
        if self.router_version != ROUTER_VERSION:
            raise ValueError("unsupported semantic router version")
        if not self.request_id.startswith("route-"):
            raise ValueError("invalid semantic route request id")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("semantic route confidence must be between zero and one")
        unknown = (set(self.allowed_tools) | set(self.terminal_tools)) - set(SCHEMA_BY_NAME)
        if unknown:
            raise ValueError(f"semantic route contains unknown tools: {sorted(unknown)}")
        if self.response_mode != ExpectedOutputMode.ACTION and self.allowed_tools:
            raise ValueError("non-action semantic route cannot expose tools")
        if not self.solver.valid:
            raise ValueError("final semantic route must pass the constraint solver")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "normalized_request": self.normalized_request.to_dict(),
            "task_class": self.task_class.value,
            "response_mode": self.response_mode.value,
            "risk_level": self.risk_level.value,
            "hard_constraints": [item.to_dict() for item in self.hard_constraints],
            "specialist": self.specialist.value,
            "immediate_family": self.immediate_family.value,
            "allowed_tools": list(self.allowed_tools),
            "terminal_tools": list(self.terminal_tools),
            "first_lifecycle_step": self.first_lifecycle_step.value,
            "reason_code": self.reason_code.value,
            "confidence": self.confidence,
            "abstained": self.abstained,
            "fallback_reason": self.fallback_reason,
            "decision_trace": [item.to_dict() for item in self.decision_trace],
            "schema_version": self.schema_version,
            "router_version": self.router_version,
            "model_identity": self.model_identity,
            "model_call_stats": dict(self.model_call_stats),
            "solver": self.solver.to_dict(),
            "candidate_specialists": [item.value for item in self.candidate_specialists],
        }


# The first level limits semantic competition. The second level is the only set
# of families the model can see for a selected specialist.
TASK_SPECIALISTS: dict[TaskClass, tuple[Specialist, ...]] = {
    TaskClass.INSPECTION: (
        Specialist.REPOSITORY_INSPECTOR,
        Specialist.DOCUMENTATION,
        Specialist.DEBUGGING,
        Specialist.SECURITY_REVIEW,
        Specialist.GENERAL,
    ),
    TaskClass.MUTATION: (Specialist.IMPLEMENTATION,),
    TaskClass.VERIFICATION: (
        Specialist.VERIFICATION,
        Specialist.DEBUGGING,
        Specialist.SECURITY_REVIEW,
    ),
    TaskClass.EXPLANATION: (
        Specialist.GENERAL,
        Specialist.DOCUMENTATION,
        Specialist.SECURITY_REVIEW,
    ),
    TaskClass.PLANNING: (
        Specialist.IMPLEMENTATION,
        Specialist.DOCUMENTATION,
        Specialist.SECURITY_REVIEW,
        Specialist.GENERAL,
    ),
    TaskClass.BLOCKED: (
        Specialist.SECURITY_REVIEW,
        Specialist.IMPLEMENTATION,
        Specialist.GENERAL,
    ),
}

TASK_SPECIALIST_FAMILIES: dict[
    tuple[TaskClass, Specialist], tuple[ToolFamily, ...]
] = {
    (TaskClass.INSPECTION, Specialist.REPOSITORY_INSPECTOR): (
        ToolFamily.REPOSITORY_DISCOVERY,
        ToolFamily.FILE_INSPECTION,
        ToolFamily.SYMBOL_INSPECTION,
        ToolFamily.PATCH_INSPECTION,
    ),
    (TaskClass.INSPECTION, Specialist.DOCUMENTATION): (
        ToolFamily.DOCUMENTATION_RETRIEVAL,
        ToolFamily.FILE_INSPECTION,
    ),
    (TaskClass.INSPECTION, Specialist.DEBUGGING): (ToolFamily.FILE_INSPECTION,),
    (TaskClass.INSPECTION, Specialist.SECURITY_REVIEW): (ToolFamily.FILE_INSPECTION,),
    (TaskClass.INSPECTION, Specialist.GENERAL): (
        ToolFamily.MEMORY_RETRIEVAL,
        ToolFamily.REPOSITORY_DISCOVERY,
    ),
    (TaskClass.MUTATION, Specialist.IMPLEMENTATION): (
        ToolFamily.TARGETED_MUTATION,
        ToolFamily.FILE_CREATION,
    ),
    (TaskClass.VERIFICATION, Specialist.VERIFICATION): (
        ToolFamily.EXECUTION_VERIFICATION,
        ToolFamily.PATCH_INSPECTION,
    ),
    (TaskClass.VERIFICATION, Specialist.DEBUGGING): (
        ToolFamily.FILE_INSPECTION,
        ToolFamily.EXECUTION_VERIFICATION,
    ),
    (TaskClass.VERIFICATION, Specialist.SECURITY_REVIEW): (
        ToolFamily.FILE_INSPECTION,
        ToolFamily.EXECUTION_VERIFICATION,
    ),
    (TaskClass.EXPLANATION, Specialist.GENERAL): (ToolFamily.FINAL_RESPONSE,),
    (TaskClass.EXPLANATION, Specialist.DOCUMENTATION): (
        ToolFamily.FINAL_RESPONSE,
        ToolFamily.DOCUMENTATION_RETRIEVAL,
    ),
    (TaskClass.EXPLANATION, Specialist.SECURITY_REVIEW): (ToolFamily.FINAL_RESPONSE,),
    (TaskClass.PLANNING, Specialist.IMPLEMENTATION): (
        ToolFamily.MUTATION_PROPOSAL,
        ToolFamily.FINAL_RESPONSE,
    ),
    (TaskClass.PLANNING, Specialist.DOCUMENTATION): (
        ToolFamily.DOCUMENTATION_RETRIEVAL,
        ToolFamily.FINAL_RESPONSE,
    ),
    (TaskClass.PLANNING, Specialist.SECURITY_REVIEW): (
        ToolFamily.FILE_INSPECTION,
        ToolFamily.FINAL_RESPONSE,
    ),
    (TaskClass.PLANNING, Specialist.GENERAL): (ToolFamily.FINAL_RESPONSE,),
    (TaskClass.BLOCKED, Specialist.SECURITY_REVIEW): (ToolFamily.BLOCKED,),
    (TaskClass.BLOCKED, Specialist.IMPLEMENTATION): (ToolFamily.CLARIFICATION,),
    (TaskClass.BLOCKED, Specialist.GENERAL): (
        ToolFamily.BLOCKED,
        ToolFamily.CLARIFICATION,
    ),
}

FAMILY_TOOLS: dict[ToolFamily, frozenset[str]] = {
    ToolFamily.REPOSITORY_DISCOVERY: frozenset({"project_map", "list_files"}),
    ToolFamily.FILE_INSPECTION: frozenset({"read_file", "search_code", "file_summary"}),
    ToolFamily.SYMBOL_INSPECTION: frozenset({"search_symbols", "search_code", "index_code"}),
    ToolFamily.DOCUMENTATION_RETRIEVAL: frozenset(
        {"search_docs", "query_knowledge", "refresh_knowledge"}
    ),
    ToolFamily.EXECUTION_VERIFICATION: frozenset({"run_command", "test_patch"}),
    ToolFamily.MUTATION_PROPOSAL: frozenset(
        {"propose_edit_file", "propose_write_file"}
    ),
    ToolFamily.TARGETED_MUTATION: frozenset({"edit_file"}),
    ToolFamily.FILE_CREATION: frozenset({"write_file"}),
    ToolFamily.PATCH_INSPECTION: frozenset(
        {"list_patches", "show_patch", "test_patch"}
    ),
    ToolFamily.MEMORY_RETRIEVAL: frozenset({"recall", "list_memories"}),
    ToolFamily.FINAL_RESPONSE: frozenset(),
    ToolFamily.CLARIFICATION: frozenset(),
    ToolFamily.BLOCKED: frozenset(),
}

SPECIALIST_TOOLS: dict[Specialist, frozenset[str]] = {
    Specialist.GENERAL: frozenset(
        {"project_map", "list_files", "recall", "list_memories"}
    ),
    Specialist.REPOSITORY_INSPECTOR: frozenset(
        {
            "project_map",
            "list_files",
            "read_file",
            "search_code",
            "search_symbols",
            "index_code",
            "file_summary",
            "list_patches",
            "show_patch",
        }
    ),
    Specialist.IMPLEMENTATION: frozenset(
        {
            "read_file",
            "search_code",
            "propose_edit_file",
            "propose_write_file",
            "edit_file",
            "write_file",
        }
    ),
    Specialist.VERIFICATION: frozenset(
        {"read_file", "search_code", "run_command", "test_patch", "list_patches", "show_patch"}
    ),
    Specialist.DEBUGGING: frozenset(
        {"read_file", "search_code", "file_summary", "run_command", "test_patch"}
    ),
    Specialist.DOCUMENTATION: frozenset(
        {"read_file", "search_code", "search_docs", "query_knowledge", "refresh_knowledge"}
    ),
    Specialist.SECURITY_REVIEW: frozenset(
        {"read_file", "search_code", "run_command"}
    ),
}

TASK_TOOLS: dict[TaskClass, frozenset[str]] = {
    TaskClass.INSPECTION: frozenset(SCHEMA_BY_NAME) - MUTATION_TOOLS - SHELL_TOOLS,
    TaskClass.MUTATION: frozenset(
        {"read_file", "search_code", "edit_file", "write_file"}
    ),
    TaskClass.VERIFICATION: frozenset(
        {"read_file", "search_code", "run_command", "test_patch", "list_patches", "show_patch"}
    ),
    TaskClass.EXPLANATION: frozenset(),
    TaskClass.PLANNING: frozenset(
        {
            "read_file",
            "search_code",
            "search_docs",
            "query_knowledge",
            "propose_edit_file",
            "propose_write_file",
        }
    ),
    TaskClass.BLOCKED: frozenset(),
}


class RuleBasedSemanticClassifier:
    """Explainable development/CI classifier; production may inject Ollama."""

    def __init__(self) -> None:
        self.stats = ModelCallStats()
        self.model_identity = "deterministic-fixture-classifier"

    def reset_route_stats(self) -> None:
        self.stats = ModelCallStats()

    def predict_task(self, request: NormalizedRequest) -> TaskPrediction:
        if request.destructive_operation or request.outside_workspace:
            task = TaskClass.BLOCKED
            confidence = 0.98
        elif request.missing_context and request.mutation_requested:
            task = TaskClass.BLOCKED
            confidence = 0.94
        elif request.explanation_only:
            task = TaskClass.EXPLANATION
            confidence = 0.94
        elif request.requested_artifact == "plan":
            task = TaskClass.PLANNING
            confidence = 0.88
        elif request.tools_prohibited and not request.mutation_requested:
            task = TaskClass.EXPLANATION
            confidence = 0.92
        elif request.mutation_requested:
            task = TaskClass.MUTATION
            confidence = 0.91
        elif request.proposal_requested:
            task = TaskClass.PLANNING
            confidence = 0.91
        elif request.execution_requested or request.verification_requested:
            task = TaskClass.VERIFICATION
            confidence = 0.90
        elif request.requested_artifact in {"memory", "patch"}:
            task = TaskClass.INSPECTION
            confidence = 0.92
        elif request.repository_context or request.external_information:
            task = TaskClass.INSPECTION
            confidence = 0.86
        else:
            task = TaskClass.EXPLANATION
            confidence = 0.78
        return TaskPrediction(task, confidence, source=DecisionSource.DETERMINISTIC_RULE)

    def select_route(
        self,
        request: NormalizedRequest,
        task_class: TaskClass,
        candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
    ) -> RouteSelectionPrediction:
        specialist = next(iter(candidates))
        family = candidates[specialist][0]
        text = request.text.casefold()
        if task_class == TaskClass.BLOCKED:
            specialist = (
                Specialist.IMPLEMENTATION
                if request.missing_context and not request.destructive_operation
                else Specialist.SECURITY_REVIEW
            )
        elif request.security_sensitive and Specialist.SECURITY_REVIEW in candidates:
            specialist = Specialist.SECURITY_REVIEW
        elif request.external_information and Specialist.DOCUMENTATION in candidates:
            specialist = Specialist.DOCUMENTATION
        elif request.debugging_requested:
            if Specialist.DEBUGGING in candidates:
                specialist = Specialist.DEBUGGING
        elif task_class == TaskClass.VERIFICATION and Specialist.VERIFICATION in candidates:
            specialist = Specialist.VERIFICATION
        elif task_class in {TaskClass.MUTATION, TaskClass.PLANNING} and Specialist.IMPLEMENTATION in candidates:
            specialist = Specialist.IMPLEMENTATION
        elif re.search(r"\b(?:memory|remembered|decision log|recall)\b", text) and Specialist.GENERAL in candidates:
            specialist = Specialist.GENERAL
        elif Specialist.REPOSITORY_INSPECTOR in candidates:
            specialist = Specialist.REPOSITORY_INSPECTOR

        families = candidates[specialist]
        family = families[0]
        if task_class == TaskClass.BLOCKED:
            family = (
                ToolFamily.CLARIFICATION
                if request.missing_context and ToolFamily.CLARIFICATION in families
                else ToolFamily.BLOCKED
            )
        elif task_class == TaskClass.EXPLANATION or request.explanation_only:
            family = ToolFamily.FINAL_RESPONSE
        elif task_class == TaskClass.MUTATION:
            family = (
                ToolFamily.FILE_CREATION
                if request.requested_artifact == "new_file"
                else ToolFamily.TARGETED_MUTATION
            )
        elif task_class == TaskClass.PLANNING and request.proposal_requested:
            family = ToolFamily.MUTATION_PROPOSAL
        elif re.search(r"\b(?:symbol|definition|references?|call sites?)\b", text) and ToolFamily.SYMBOL_INSPECTION in families:
            family = ToolFamily.SYMBOL_INSPECTION
        elif re.search(r"\b(?:documentation|docs|manual|guidance|knowledge)\b", text) and ToolFamily.DOCUMENTATION_RETRIEVAL in families:
            family = ToolFamily.DOCUMENTATION_RETRIEVAL
        elif re.search(r"\b(?:patch|proposal|diff)\b", text) and ToolFamily.PATCH_INSPECTION in families:
            family = ToolFamily.PATCH_INSPECTION
        elif re.search(r"\b(?:memory|remembered|decision log|recall)\b", text) and ToolFamily.MEMORY_RETRIEVAL in families:
            family = ToolFamily.MEMORY_RETRIEVAL
        elif task_class == TaskClass.VERIFICATION and ToolFamily.EXECUTION_VERIFICATION in families:
            family = ToolFamily.EXECUTION_VERIFICATION
        elif request.file_paths and ToolFamily.FILE_INSPECTION in families:
            family = ToolFamily.FILE_INSPECTION
        return RouteSelectionPrediction(
            specialist=specialist,
            specialist_confidence=0.88,
            immediate_family=family,
            family_confidence=0.86,
            source=DecisionSource.DETERMINISTIC_RULE,
        )


class OllamaSemanticClassifier:
    """Two-stage JSON-Schema classifier with at most one repair call overall."""

    def __init__(self, client: "OllamaClient | Any") -> None:
        self.client = client
        self.stats = ModelCallStats()
        self.model_identity = client.model
        self._repair_used = False
        self.raw_outputs: list[str] = []

    def reset_route_stats(self) -> None:
        self.stats = ModelCallStats()
        self._repair_used = False
        self.raw_outputs.clear()

    def predict_task(self, request: NormalizedRequest) -> TaskPrediction:
        definitions = {
            "inspection": "Read or retrieve evidence before answering; no requested mutation.",
            "mutation": "Apply an authorized repository change, not merely describe one.",
            "verification": "Run a check or establish whether behavior/build/tests pass.",
            "explanation": "Answer from general knowledge without repository or external retrieval.",
            "planning": "Produce a plan or reviewable change proposal without applying it.",
            "blocked": "Unsafe, unsupported, or missing essential mutation context.",
        }
        schema = task_prediction_schema()
        system = (
            "Classify only the task class. Do not select tools, specialists, risk, "
            "lifecycle, or reason codes. Boundaries: explanation wins only when no "
            "evidence retrieval is requested; inspection includes repository, "
            "documentation, and saved-memory retrieval; verification means execute/check, not "
            "explain a failure; planning does not apply changes; blocked is for a "
            "prohibition or essential missing mutation target. Return only schema JSON.\n"
            f"Taxonomy: {json.dumps(definitions, sort_keys=True)}"
        )
        user = json.dumps(
            {"request": request.text, "normalization_hints": request.public_features()},
            sort_keys=True,
        )
        payload = self._call(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            schema,
            parse_task_prediction,
        )
        return payload

    def select_route(
        self,
        request: NormalizedRequest,
        task_class: TaskClass,
        candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
    ) -> RouteSelectionPrediction:
        candidate_payload = {
            specialist.value: {
                "purpose": SPECIALIST_PURPOSE[specialist],
                "families": [
                    {
                        "family": family.value,
                        "purpose": FAMILY_PURPOSE[family],
                        "boundary": FAMILY_BOUNDARY[family],
                        "lifecycle": FAMILY_LIFECYCLE[family].value,
                    }
                    for family in families
                ],
            }
            for specialist, families in candidates.items()
        }
        schema = route_selection_schema(candidates)
        system = (
            "Choose one specialist and one of that specialist's immediate families. "
            "Use only the supplied candidates. The family is the next semantic "
            "capability, not permission to execute. Return only schema JSON."
        )
        user = json.dumps(
            {
                "request": request.text,
                "task_class": task_class.value,
                "candidate_specialists": candidate_payload,
                "normalization_hints": request.public_features(),
            },
            sort_keys=True,
        )
        return self._call(
            [{"role": "system", "content": system}, {"role": "user", "content": user}],
            schema,
            lambda raw: parse_route_selection(raw, candidates),
        )

    def _call(self, messages: list[Message], schema: dict[str, Any], parser: Any) -> Any:
        self.stats.calls += 1
        self.stats.estimated_input_chars += sum(len(item["content"]) for item in messages)
        try:
            call_started = time.perf_counter()
            raw = self.client.chat(messages, json_mode=True, response_schema=schema)
            self.stats.latency_ms += (time.perf_counter() - call_started) * 1000
            self.raw_outputs.append(raw)
            self.stats.estimated_output_chars += len(raw)
            parse_started = time.perf_counter()
            parsed = parser(raw)
            self.stats.parsing_ms += (time.perf_counter() - parse_started) * 1000
            return parsed
        except (ValueError, LLMError) as first_error:
            self.stats.schema_failures += 1
            if self._repair_used or self.stats.calls >= 3:
                raise
            self._repair_used = True
            self.stats.retries += 1
            self.stats.calls += 1
            repair = {
                "role": "system",
                "content": (
                    "The previous response failed strict validation. Return exactly one "
                    "JSON object matching the supplied schema; no prose or markdown. "
                    f"Validation error: {str(first_error)[:240]}"
                ),
            }
            call_started = time.perf_counter()
            raw = self.client.chat([*messages, repair], json_mode=True, response_schema=schema)
            self.stats.latency_ms += (time.perf_counter() - call_started) * 1000
            self.raw_outputs.append(raw)
            self.stats.estimated_output_chars += len(raw)
            parse_started = time.perf_counter()
            parsed = parser(raw)
            self.stats.parsing_ms += (time.perf_counter() - parse_started) * 1000
            return parsed


FAMILY_PURPOSE: dict[ToolFamily, str] = {
    family: family.value.replace("_", " ") for family in ToolFamily
}
SPECIALIST_PURPOSE: dict[Specialist, str] = {
    Specialist.GENERAL: "Direct explanation or saved-memory retrieval without domain execution.",
    Specialist.REPOSITORY_INSPECTOR: "Repository structure, files, symbols, references, and existing patches.",
    Specialist.IMPLEMENTATION: "Plans, proposals, and authorized source changes.",
    Specialist.VERIFICATION: "Requested tests, builds, compilers, linters, simulations, and pass/fail checks.",
    Specialist.DEBUGGING: "Diagnosis of a reported failure, wrong result, exception, or failing behavior.",
    Specialist.DOCUMENTATION: "Documentation and project-knowledge retrieval or comparison.",
    Specialist.SECURITY_REVIEW: "Security-sensitive inspection, verification, and prohibited operations.",
}
FAMILY_BOUNDARY: dict[ToolFamily, str] = {
    ToolFamily.REPOSITORY_DISCOVERY: "Choose for repository inventory, not a known file.",
    ToolFamily.FILE_INSPECTION: "Choose for known file content, not symbol-wide lookup.",
    ToolFamily.SYMBOL_INSPECTION: "Choose for definitions/references, not file summary.",
    ToolFamily.DOCUMENTATION_RETRIEVAL: "Choose for docs/knowledge evidence, not source edits.",
    ToolFamily.EXECUTION_VERIFICATION: "Choose to run a check, not explain one.",
    ToolFamily.MUTATION_PROPOSAL: "Choose for a reviewable proposal, not live application.",
    ToolFamily.TARGETED_MUTATION: "Choose for an existing-file edit, not new file creation.",
    ToolFamily.FILE_CREATION: "Choose for a new/full file, not a targeted replacement.",
    ToolFamily.PATCH_INSPECTION: "Choose for an existing patch/diff, not source discovery.",
    ToolFamily.MEMORY_RETRIEVAL: "Choose for saved memory, not repository source.",
    ToolFamily.FINAL_RESPONSE: "Choose when no tool evidence is needed.",
    ToolFamily.CLARIFICATION: "Choose when a required user choice is missing.",
    ToolFamily.BLOCKED: "Choose for prohibited or unsupported execution.",
}
FAMILY_LIFECYCLE: dict[ToolFamily, FirstLifecycleStep] = {
    ToolFamily.REPOSITORY_DISCOVERY: FirstLifecycleStep.INSPECTION,
    ToolFamily.FILE_INSPECTION: FirstLifecycleStep.INSPECTION,
    ToolFamily.SYMBOL_INSPECTION: FirstLifecycleStep.INSPECTION,
    ToolFamily.DOCUMENTATION_RETRIEVAL: FirstLifecycleStep.INSPECTION,
    ToolFamily.EXECUTION_VERIFICATION: FirstLifecycleStep.VERIFICATION,
    ToolFamily.MUTATION_PROPOSAL: FirstLifecycleStep.INSPECTION,
    ToolFamily.TARGETED_MUTATION: FirstLifecycleStep.INSPECTION,
    ToolFamily.FILE_CREATION: FirstLifecycleStep.MUTATION,
    ToolFamily.PATCH_INSPECTION: FirstLifecycleStep.INSPECTION,
    ToolFamily.MEMORY_RETRIEVAL: FirstLifecycleStep.INSPECTION,
    ToolFamily.FINAL_RESPONSE: FirstLifecycleStep.ANSWER,
    ToolFamily.CLARIFICATION: FirstLifecycleStep.CLARIFICATION,
    ToolFamily.BLOCKED: FirstLifecycleStep.REFUSAL,
}


class SemanticRouterV2:
    def __init__(
        self,
        classifier: SemanticClassifier | None = None,
        *,
        thresholds: RouterThresholds | None = None,
        model_identity: str = "deterministic-fixture-classifier",
    ) -> None:
        self.classifier = classifier or RuleBasedSemanticClassifier()
        self.thresholds = thresholds or RouterThresholds()
        self.model_identity = getattr(self.classifier, "model_identity", model_identity)

    def route_typed(
        self,
        prompt: str,
        workspace: Path,
        *,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        allow_write: bool = False,
        allow_shell: bool = False,
        allow_network: bool = False,
        prior_inspection: bool = False,
    ) -> SemanticRouteState:
        del prior_inspection  # The state always describes the first lifecycle step.
        reset_stats = getattr(self.classifier, "reset_route_stats", None)
        if callable(reset_stats):
            reset_stats()
        started = time.perf_counter()
        normalized_mode = parse_agent_mode(mode)
        request = normalize_request(prompt, workspace)
        trace: list[DecisionTraceEntry] = [
            DecisionTraceEntry(
                "normalized_request",
                DecisionSource.DETERMINISTIC_RULE,
                "bounded_request_normalization",
                {"request_length": len(prompt), "workspace": "current_workspace"},
                request.to_dict(),
            )
        ]
        constraints = evaluate_policy(
            request,
            normalized_mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
            allow_network=allow_network,
        )
        response_mode = resolve_response_mode(request, constraints, normalized_mode)
        risk = resolve_risk(request, constraints)
        try:
            task_prediction = self.classifier.predict_task(request)
        except (ValueError, LLMError, TimeoutError) as exc:
            task_prediction = TaskPrediction(
                TaskClass.BLOCKED if request.mutation_requested else TaskClass.INSPECTION,
                0.0,
                evidence_summary="classifier failure",
                source=DecisionSource.FALLBACK,
            )
            classifier_error = type(exc).__name__
        else:
            classifier_error = ""

        task_class = task_prediction.task_class
        task_source = task_prediction.source
        task_confidence = task_prediction.confidence
        abstained = False
        fallback_reason = ""
        if response_mode == ExpectedOutputMode.BLOCKED:
            task_class = TaskClass.BLOCKED
        elif response_mode == ExpectedOutputMode.CLARIFICATION:
            task_class = TaskClass.BLOCKED
        elif task_prediction.confidence < self.thresholds.task_class:
            abstained = True
            fallback_reason = classifier_error or "task_class_below_threshold"
            if request.missing_context:
                task_class = TaskClass.BLOCKED
                response_mode = ExpectedOutputMode.CLARIFICATION
            elif request.repository_context:
                task_class = TaskClass.INSPECTION
            else:
                task_class = TaskClass.EXPLANATION
                response_mode = ExpectedOutputMode.FINAL_ANSWER
        elif (
            task_class == TaskClass.EXPLANATION
            and not request.repository_context
            and not request.external_information
            and request.requested_artifact not in {"memory", "patch"}
        ):
            response_mode = ExpectedOutputMode.FINAL_ANSWER
        if (
            task_class == TaskClass.EXPLANATION
            and response_mode == ExpectedOutputMode.ACTION
            and (
                request.repository_context
                or request.external_information
                or request.requested_artifact in {"memory", "patch"}
            )
        ):
            task_class = TaskClass.INSPECTION
            task_source = DecisionSource.COMPATIBILITY_MATRIX
            task_confidence = min(task_confidence, 0.75)
            fallback_reason = fallback_reason or "task_response_mode_disagreement"
        trace.extend(
            (
                DecisionTraceEntry(
                    "task_class",
                    task_source if not abstained else DecisionSource.FALLBACK,
                    "task_prediction_with_threshold",
                    {
                        "confidence": task_prediction.confidence,
                        "threshold": self.thresholds.task_class,
                        "predicted_task_class": task_prediction.task_class.value,
                    },
                    task_class.value,
                ),
                DecisionTraceEntry(
                    "response_mode",
                    DecisionSource.POLICY_ENGINE,
                    "intent_policy_response_resolution",
                    {"constraint_ids": [item.identifier for item in constraints]},
                    response_mode.value,
                ),
                DecisionTraceEntry(
                    "risk_level",
                    DecisionSource.POLICY_ENGINE,
                    "maximum_constraint_and_operation_risk",
                    {"constraint_severities": [item.severity.value for item in constraints]},
                    risk.value,
                ),
            )
        )

        candidates = reduce_candidates(task_class, request, response_mode)
        trace.append(
            DecisionTraceEntry(
                "candidate_specialists",
                DecisionSource.COMPATIBILITY_MATRIX,
                "task_specialist_family_reduction",
                {"task_class": task_class.value},
                {
                    specialist.value: [family.value for family in families]
                    for specialist, families in candidates.items()
                },
            )
        )
        selection: RouteSelectionPrediction
        if abstained:
            selection = safe_selection(task_class, request, candidates)
        else:
            try:
                selection = self.classifier.select_route(
                    request, task_class, candidates
                )
            except (ValueError, LLMError, TimeoutError) as exc:
                selection = safe_selection(task_class, request, candidates)
                abstained = True
                fallback_reason = fallback_reason or f"route_selection_{type(exc).__name__}"

        if (
            selection.specialist_confidence < self.thresholds.specialist
            or selection.family_confidence < self.thresholds.immediate_family
        ):
            selection = safe_selection(task_class, request, candidates)
            abstained = True
            fallback_reason = fallback_reason or "specialist_or_family_below_threshold"
        if (
            selection.specialist not in candidates
            or selection.immediate_family not in candidates.get(selection.specialist, ())
        ):
            selection = safe_selection(task_class, request, candidates)
            abstained = True
            fallback_reason = fallback_reason or "classifier_returned_incompatible_route"
        if (
            task_class == TaskClass.VERIFICATION
            and selection.specialist == Specialist.DEBUGGING
            and not request.debugging_requested
            and Specialist.VERIFICATION in candidates
            and selection.immediate_family
            in candidates[Specialist.VERIFICATION]
        ):
            selection = replace(
                selection,
                specialist=Specialist.VERIFICATION,
                specialist_confidence=min(selection.specialist_confidence, 0.75),
                source=DecisionSource.COMPATIBILITY_MATRIX,
            )
            fallback_reason = fallback_reason or "verification_specialist_disagreement"
        if (
            task_class == TaskClass.VERIFICATION
            and request.execution_requested
            and selection.immediate_family == ToolFamily.FILE_INSPECTION
            and ToolFamily.EXECUTION_VERIFICATION
            in candidates.get(selection.specialist, ())
        ):
            selection = replace(
                selection,
                immediate_family=ToolFamily.EXECUTION_VERIFICATION,
                family_confidence=min(selection.family_confidence, 0.75),
                source=DecisionSource.COMPATIBILITY_MATRIX,
            )
            fallback_reason = fallback_reason or "execution_family_disagreement"

        specialist = selection.specialist
        family = terminal_family_for_response(
            selection.immediate_family, response_mode, request
        )
        terminal_tools, tool_trace = resolve_terminal_tools(
            task_class,
            specialist,
            family,
            response_mode,
            request,
            normalized_mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
            allow_network=allow_network,
        )
        lifecycle = resolve_lifecycle(
            response_mode,
            task_class,
            family,
            request,
            terminal_tools,
        )
        allowed_tools = resolve_first_step_tools(
            lifecycle,
            terminal_tools,
            specialist,
            request,
            normalized_mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
        )
        reason = derive_reason_code(
            task_class, response_mode, specialist, family, lifecycle, request, constraints
        )
        confidence = round(
            min(
                task_confidence,
                selection.specialist_confidence,
                selection.family_confidence,
            ),
            3,
        )
        if abstained:
            confidence = min(confidence, 0.60)
        state_fields = {
            "task_class": task_class,
            "response_mode": response_mode,
            "specialist": specialist,
            "family": family,
            "allowed_tools": allowed_tools,
            "terminal_tools": terminal_tools,
            "lifecycle": lifecycle,
            "reason": reason,
            "confidence": confidence,
        }
        solved_fields, solver = solve_constraints(
            state_fields, request, constraints, candidates
        )
        task_class = solved_fields["task_class"]
        response_mode = solved_fields["response_mode"]
        specialist = solved_fields["specialist"]
        family = solved_fields["family"]
        allowed_tools = solved_fields["allowed_tools"]
        terminal_tools = solved_fields["terminal_tools"]
        lifecycle = solved_fields["lifecycle"]
        reason = solved_fields["reason"]
        confidence = solved_fields["confidence"]
        if solver.repairs_applied:
            abstained = True
            fallback_reason = fallback_reason or "constraint_solver_safe_repair"

        trace.extend(
            (
                DecisionTraceEntry(
                    "specialist",
                    selection.source if not abstained else DecisionSource.FALLBACK,
                    "restricted_candidate_selection",
                    {
                        "confidence": selection.specialist_confidence,
                        "candidates": [item.value for item in candidates],
                    },
                    specialist.value,
                ),
                DecisionTraceEntry(
                    "immediate_family",
                    selection.source,
                    "restricted_family_selection",
                    {
                        "selected_specialist": specialist.value,
                        "valid_families": [
                            item.value for item in candidates.get(specialist, ())
                        ],
                    },
                    family.value,
                ),
                DecisionTraceEntry(
                    "allowed_tools",
                    DecisionSource.DETERMINISTIC_RULE,
                    "trusted_set_intersection_then_lifecycle_scope",
                    tool_trace,
                    list(allowed_tools),
                ),
                DecisionTraceEntry(
                    "first_lifecycle_step",
                    DecisionSource.DETERMINISTIC_RULE,
                    "lifecycle_compatibility_matrix",
                    {
                        "response_mode": response_mode.value,
                        "task_class": task_class.value,
                        "family": family.value,
                    },
                    lifecycle.value,
                ),
                DecisionTraceEntry(
                    "reason_code",
                    DecisionSource.DETERMINISTIC_RULE,
                    "resolved_route_reason_derivation",
                    {
                        "task_class": task_class.value,
                        "family": family.value,
                        "lifecycle": lifecycle.value,
                    },
                    reason.value,
                ),
                DecisionTraceEntry(
                    "hard_constraints",
                    DecisionSource.POLICY_ENGINE,
                    "deterministic_constraint_evaluation",
                    {"mode": normalized_mode.value},
                    [item.to_dict() for item in constraints],
                ),
                DecisionTraceEntry(
                    "solver",
                    DecisionSource.COMPATIBILITY_MATRIX,
                    "cross_field_consistency_solver",
                    {"candidate_count": len(candidates)},
                    solver.to_dict(),
                ),
            )
        )
        stats = getattr(self.classifier, "stats", ModelCallStats()).to_dict()
        stats["deterministic_resolution_ms"] = round(
            (time.perf_counter() - started) * 1000
            - float(stats.get("latency_ms", 0.0))
            - float(stats.get("parsing_ms", 0.0)),
            3,
        )
        return SemanticRouteState(
            request_id=route_identity(prompt, normalized_mode, allow_write, allow_shell),
            normalized_request=request,
            task_class=task_class,
            response_mode=response_mode,
            risk_level=risk,
            hard_constraints=constraints,
            specialist=specialist,
            immediate_family=family,
            allowed_tools=allowed_tools,
            terminal_tools=terminal_tools,
            first_lifecycle_step=lifecycle,
            reason_code=reason,
            confidence=confidence,
            abstained=abstained,
            fallback_reason=fallback_reason,
            decision_trace=tuple(trace),
            schema_version=SCHEMA_VERSION,
            router_version=ROUTER_VERSION,
            model_identity=self.model_identity,
            model_call_stats=stats,
            solver=solver,
            candidate_specialists=tuple(candidates),
        )

    def legacy_decision(
        self,
        state: SemanticRouteState,
        *,
        mode: str | AgentMode,
        allow_write: bool,
        allow_shell: bool,
        allow_network: bool = False,
    ) -> RoutingDecision:
        """Project v2 state into the stable v1 runtime contract."""

        normalized_mode = parse_agent_mode(mode)
        granted = granted_capabilities(
            normalized_mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
            allow_network=allow_network,
        )
        required: list[Capability] = []
        if state.response_mode == ExpectedOutputMode.ACTION:
            required.append(Capability.WORKSPACE_READ)
        if state.task_class == TaskClass.MUTATION:
            required.append(Capability.WORKSPACE_WRITE)
        if set(state.terminal_tools) & SHELL_TOOLS:
            required.append(Capability.SHELL)
        if set(state.terminal_tools) & {
            name for name, schema in SCHEMA_BY_NAME.items() if schema.mutates_runtime
        }:
            required.append(Capability.RUNTIME_STATE)
        missing = tuple(item for item in dict.fromkeys(required) if item not in granted)
        target_kind = TargetKind.FILE if state.normalized_request.file_paths else (
            TargetKind.REPOSITORY
            if state.normalized_request.repository_context
            else TargetKind.UNKNOWN
        )
        incidents: list[InterpretationIncidentCode] = []
        if state.normalized_request.missing_context:
            incidents.append(InterpretationIncidentCode.MISSING_TARGET)
        if missing:
            incidents.append(InterpretationIncidentCode.MISSING_CAPABILITY)
        intent = NormalizedIntent(
            schema_version="1.0",
            intent_id=state.request_id.replace("route-", "intent-", 1),
            original_request=state.normalized_request.text,
            goal=state.normalized_request.text[:4000],
            intent_type=state.reason_code.value,
            task_class=state.task_class,
            target_scope=state.normalized_request.file_paths,
            target_kind=target_kind,
            mutation_intent=state.normalized_request.mutation_requested,
            verification_intent=state.normalized_request.verification_requested,
            research_intent=state.normalized_request.external_information,
            requires_prior_inspection=state.first_lifecycle_step == FirstLifecycleStep.INSPECTION
            and state.immediate_family
            in {
                ToolFamily.TARGETED_MUTATION,
                ToolFamily.MUTATION_PROPOSAL,
            },
            risk_level=state.risk_level,
            ambiguity=Ambiguity(
                AmbiguityLevel.BLOCKING if state.normalized_request.missing_context else AmbiguityLevel.NONE,
                ("target_scope",) if state.normalized_request.missing_context else (),
            ),
            required_capabilities=tuple(dict.fromkeys(required)),
            forbidden_capabilities=tuple(
                item
                for item, forbidden in (
                    (Capability.WORKSPACE_WRITE, state.normalized_request.edits_prohibited),
                    (Capability.SHELL, state.normalized_request.shell_prohibited),
                    (Capability.NETWORK, state.normalized_request.network_prohibited),
                )
                if forbidden and item not in required
            ),
            expected_output_mode=state.response_mode,
            deterministic_signals=state.normalized_request.signals,
            interpretation_incidents=tuple(incidents),
        )
        return RoutingDecision(
            schema_version="1.0",
            intent_id=intent.intent_id,
            intent_type=intent.intent_type,
            task_class=state.task_class,
            specialist=state.specialist,
            tool_family=state.immediate_family,
            preferred_tools=state.terminal_tools,
            fallback_tools=(),
            response_mode=state.response_mode,
            reason_code=state.reason_code,
            risk_level=state.risk_level,
            requires_prior_inspection=intent.requires_prior_inspection,
            required_capabilities=intent.required_capabilities,
            missing_capabilities=missing,
            confidence=state.confidence,
            deterministic_signals=intent.deterministic_signals,
            model_signals=tuple(
                item.output
                for item in state.decision_trace
                if item.source == DecisionSource.MODEL
                and isinstance(item.output, str)
            )[:16],
            capability_fingerprint=_capability_fingerprint(granted, normalized_mode.value),
            normalized_intent=intent,
        )


_PATH_RE = re.compile(
    r"(?<![\w./-])((?:(?:\.\.?/)|/)?[\w.-]+(?:/[\w.-]+)*\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md|txt))(?=$|[\s`'\",:;!?.()])",
    re.IGNORECASE,
)


def normalize_request(prompt: str, workspace: Path) -> NormalizedRequest:
    original = prompt.strip()
    if not original:
        raise ValueError("routing request cannot be empty")
    if len(original) > 16_000:
        raise ValueError("routing request exceeds 16000 characters")
    text = " ".join(original.split())
    folded = text.casefold()
    paths = tuple(dict.fromkeys(match.group(1) for match in _PATH_RE.finditer(text)))[:64]
    repository = bool(paths) or bool(
        re.search(r"\b(?:repository|repo|codebase|workspace|source tree)\b", folded)
    )
    mutation_verb_spans = tuple(
        m.span()
        for m in re.finditer(
            r"\b(?:edit|modify|implement|refactor|apply|write|create|replace|remove|rename|fix|add|insert|append|delete)\b",
            folded,
        )
    )
    mutation = bool(mutation_verb_spans)
    # A "do not change X" phrase is only a full prohibition when it covers
    # every mutation verb in the request; as a bounded constraint inside an
    # otherwise-mutating request it must not suppress the mutation intent.
    edits_prohibited_re = r"\b(?:do not|don't|without|no)\b[^.;]{0,40}\b(?:edit|modif|chang|writ|apply|mutat)"
    read_only_mode = bool(re.search(r"\bread[- ]only\b", folded))
    prohibition = re.search(edits_prohibited_re, folded)
    if read_only_mode:
        mutation = False
    elif prohibition is not None:
        pstart, pend = prohibition.span()
        mutation = any(
            not (pstart <= vstart < pend) for vstart, _ in mutation_verb_spans
        )
    edits_prohibited = bool(prohibition) or read_only_mode
    # "Add 2 and 2"-style arithmetic is a question, not a code mutation.
    if re.search(r"\badd\b\s+\d+\s+(?:and|plus|\+)", folded):
        mutation = False
    proposal = bool(
        re.search(
            r"\b(?:propose|draft)\b[^.;]{0,48}\b(?:patch|change|edit|new file|file)\b|\bproposed new file\b",
            folded,
        )
    )
    execution = bool(
        re.search(r"^(?:please\s+)?(?:run|execute|compile|lint|test|verify|build)\b", folded)
        or re.search(r"\band (?:run|execute|compile|lint|test|verify|build)\b", folded)
    )
    verification = execution or bool(
        re.search(r"\b(?:prove|confirm|validate) (?:the |that )?", folded)
    )
    tools_prohibited = bool(
        re.search(
            r"\b(?:without|no)\s+(?:calling |using )?tools?\b|\b(?:do not|don't)\s+(?:call|use)\s+(?:any )?tools?\b",
            folded,
        )
    )
    explanation = bool(
        re.search(r"^(?:please\s+)?(?:explain|describe|compare|what|why|how)\b", folded)
    ) and not repository and not execution and not mutation
    missing_context = bool(
        mutation
        and not paths
        and re.search(
            r"\b(?:it|this|the handler|the file|the function|something|unspecified)\b",
            folded,
        )
    )
    external = bool(
        re.search(r"\b(?:external|online|internet|latest|current documentation|web)\b", folded)
    )
    security = bool(
        re.search(
            r"\b(?:security|authentication|authorization|secret|credential|ssrf|injection|privilege|exploit|vulnerability)\b",
            folded,
        )
    )
    debugging = bool(
        re.search(
            r"\b(?:debug|diagnos\w*|failing|failure|exception|traceback|wrong result)\b",
            folded,
        )
    )
    destructive = bool(
        re.search(
            r"\b(?:rm\s+-rf|drop database|erase all|delete every|wipe|destroy|bypass (?:policy|authorization))\b",
            folded,
        )
    )
    protected = any(
        path.startswith((".git/", ".mind01/"))
        or path in {".env", "SECURITY.md"}
        for path in paths
    ) or bool(re.search(r"(?<!\w)(?:\.git/|\.mind01/|\.env\b)", folded))
    outside = any(path.startswith("../") or path.startswith("/") for path in paths)
    shell_prohibited = bool(
        re.search(r"\b(?:do not|don't|without|no)\b[^.;]{0,24}\b(?:shell|command)", folded)
    )
    network_prohibited = bool(
        re.search(r"\b(?:offline|no network|without (?:the )?(?:internet|network))\b", folded)
    )
    language = ""
    for name, pattern in (
        ("verilog", r"\b(?:verilog|systemverilog|rtl|iverilog)\b|\.sv\b|\.v\b"),
        ("cpp", r"\b(?:c\+\+|cpp|cmake)\b|\.(?:cc|cpp|hpp)\b"),
        ("python", r"\b(?:python|pytest)\b|\.py\b"),
        ("mathematics", r"\b(?:theorem|integral|derivative|equation|proof)\b"),
    ):
        if re.search(pattern, folded):
            language = name
            break
    if re.search(r"\b(?:patch|diff|change proposal)\b", folded):
        artifact = "patch"
    elif re.search(r"\b(?:memory|remembered|decision log|recall)\b", folded):
        artifact = "memory"
    elif re.search(r"\b(?:new file|create (?:a|the) file)\b", folded):
        artifact = "new_file"
    elif re.search(r"\b(?:plan|roadmap|implementation outline)\b", folded):
        artifact = "plan"
    elif re.search(r"\b(?:documentation|readme|docstring|guide)\b", folded):
        artifact = "documentation"
    elif paths:
        artifact = "existing_file"
    else:
        artifact = ""
    signals = tuple(
        name
        for name, present in (
            ("repository_context", repository),
            ("mutation_requested", mutation),
            ("proposal_requested", proposal),
            ("execution_requested", execution),
            ("explanation_only", explanation),
            ("external_information", external),
            ("security_sensitive", security),
            ("debugging_requested", debugging),
            ("missing_context", missing_context),
            ("verification_requested", verification),
            ("tools_prohibited", tools_prohibited),
            ("edits_prohibited", edits_prohibited),
            ("shell_prohibited", shell_prohibited),
            ("network_prohibited", network_prohibited),
            ("destructive_operation", destructive),
            ("protected_path", protected),
            ("outside_workspace", outside),
        )
        if present
    )
    del workspace  # Paths are never resolved or opened during routing.
    return NormalizedRequest(
        text=text,
        repository_context=repository,
        mutation_requested=mutation,
        proposal_requested=proposal,
        execution_requested=execution,
        explanation_only=explanation,
        external_information=external,
        security_sensitive=security,
        debugging_requested=debugging,
        missing_context=missing_context,
        file_paths=paths,
        verification_requested=verification,
        tools_prohibited=tools_prohibited,
        edits_prohibited=edits_prohibited,
        shell_prohibited=shell_prohibited,
        network_prohibited=network_prohibited,
        destructive_operation=destructive,
        protected_path=protected,
        outside_workspace=outside,
        programming_language=language,
        requested_artifact=artifact,
        signals=signals,
    )


def evaluate_policy(
    request: NormalizedRequest,
    mode: AgentMode,
    *,
    allow_write: bool,
    allow_shell: bool,
    allow_network: bool,
) -> tuple[HardConstraint, ...]:
    constraints: list[HardConstraint] = []

    def add(
        identifier: str,
        trigger: str,
        severity: ConstraintSeverity,
        effect: str,
        override: str = "not_overridable",
    ) -> None:
        constraints.append(
            HardConstraint(
                identifier,
                trigger,
                DecisionSource.POLICY_ENGINE,
                severity,
                effect,
                override,
            )
        )

    if mode == AgentMode.READ_ONLY:
        add(
            "read_only",
            f"mode={mode.value}",
            ConstraintSeverity.HIGH
            if request.mutation_requested or request.proposal_requested
            else ConstraintSeverity.INFO,
            "remove_mutation_tools",
        )
    elif not allow_write:
        add(
            "live_write_not_authorized",
            "allow_write=false",
            ConstraintSeverity.MEDIUM if request.mutation_requested else ConstraintSeverity.INFO,
            "remove_live_write_tools",
        )
    if request.edits_prohibited:
        add("user_no_mutation", "explicit edit prohibition", ConstraintSeverity.HIGH, "remove_mutation_tools")
    if request.tools_prohibited:
        add("user_no_tools", "explicit tool prohibition", ConstraintSeverity.HIGH, "remove_all_tools")
    if request.shell_prohibited or not allow_shell:
        add(
            "no_shell",
            f"user={request.shell_prohibited}; allow_shell={allow_shell}",
            ConstraintSeverity.MEDIUM if request.execution_requested else ConstraintSeverity.INFO,
            "remove_shell_tools",
        )
    if request.network_prohibited or not allow_network:
        add(
            "no_network",
            f"user={request.network_prohibited}; allow_network={allow_network}",
            ConstraintSeverity.MEDIUM if request.external_information else ConstraintSeverity.INFO,
            "remove_network_tools",
        )
    if request.protected_path:
        add("protected_path", "protected repository path referenced", ConstraintSeverity.HIGH, "remove_mutation_tools")
    if request.destructive_operation:
        add("destructive_operation", "destructive semantic signal", ConstraintSeverity.PROHIBITED, "refuse")
    if request.outside_workspace:
        add("out_of_workspace", "parent or absolute path referenced", ConstraintSeverity.PROHIBITED, "refuse")
    if request.verification_requested:
        add("verification_required", "explicit verification intent", ConstraintSeverity.INFO, "verification_lifecycle")
    if request.explanation_only:
        add("explanation_only", "direct non-grounded explanation", ConstraintSeverity.INFO, "answer_without_tools")
    if request.missing_context:
        add("missing_required_context", "mutation target is unresolved", ConstraintSeverity.HIGH, "clarify")
    return tuple(constraints)


def resolve_response_mode(
    request: NormalizedRequest,
    constraints: tuple[HardConstraint, ...],
    mode: AgentMode,
) -> ExpectedOutputMode:
    identifiers = {item.identifier for item in constraints}
    if identifiers & {"destructive_operation", "out_of_workspace"}:
        return ExpectedOutputMode.BLOCKED
    if "missing_required_context" in identifiers:
        return ExpectedOutputMode.CLARIFICATION
    if request.explanation_only or request.tools_prohibited:
        return ExpectedOutputMode.FINAL_ANSWER
    if request.mutation_requested and (mode == AgentMode.READ_ONLY or "user_no_mutation" in identifiers):
        return ExpectedOutputMode.BLOCKED
    return ExpectedOutputMode.ACTION


def resolve_risk(
    request: NormalizedRequest, constraints: tuple[HardConstraint, ...]
) -> RiskLevel:
    identifiers = {item.identifier for item in constraints}
    if identifiers & {"destructive_operation", "out_of_workspace"}:
        return RiskLevel.CRITICAL
    if (
        request.mutation_requested
        or request.security_sensitive
        or identifiers & {"protected_path", "missing_required_context"}
    ):
        return RiskLevel.HIGH
    if request.execution_requested or request.external_information:
        return RiskLevel.MEDIUM
    return RiskLevel.LOW


def reduce_candidates(
    task_class: TaskClass,
    request: NormalizedRequest,
    response_mode: ExpectedOutputMode,
) -> dict[Specialist, tuple[ToolFamily, ...]]:
    specialists = list(TASK_SPECIALISTS[task_class])
    preferred: list[Specialist] = []
    if request.security_sensitive and Specialist.SECURITY_REVIEW in specialists:
        preferred.append(Specialist.SECURITY_REVIEW)
    if request.external_information and Specialist.DOCUMENTATION in specialists:
        preferred.append(Specialist.DOCUMENTATION)
    if request.programming_language in {"python", "cpp", "verilog"}:
        for item in (Specialist.DEBUGGING, Specialist.VERIFICATION, Specialist.IMPLEMENTATION):
            if item in specialists:
                preferred.append(item)
    preferred.extend(specialists)
    ordered = tuple(dict.fromkeys(preferred))[:5]
    candidates: dict[Specialist, tuple[ToolFamily, ...]] = {}
    for specialist in ordered:
        families = TASK_SPECIALIST_FAMILIES[(task_class, specialist)]
        if response_mode == ExpectedOutputMode.FINAL_ANSWER:
            families = tuple(item for item in families if item == ToolFamily.FINAL_RESPONSE)
        elif response_mode == ExpectedOutputMode.CLARIFICATION:
            families = tuple(item for item in families if item == ToolFamily.CLARIFICATION)
        elif response_mode == ExpectedOutputMode.BLOCKED:
            families = tuple(item for item in families if item == ToolFamily.BLOCKED)
        if families:
            candidates[specialist] = families
    if not candidates:
        if response_mode == ExpectedOutputMode.CLARIFICATION:
            candidates = {Specialist.GENERAL: (ToolFamily.CLARIFICATION,)}
        elif response_mode == ExpectedOutputMode.BLOCKED:
            candidates = {Specialist.SECURITY_REVIEW: (ToolFamily.BLOCKED,)}
        elif response_mode == ExpectedOutputMode.FINAL_ANSWER:
            candidates = {Specialist.GENERAL: (ToolFamily.FINAL_RESPONSE,)}
        else:
            candidates = {
                Specialist.REPOSITORY_INSPECTOR: (
                    ToolFamily.REPOSITORY_DISCOVERY,
                )
            }
    return candidates


def safe_selection(
    task_class: TaskClass,
    request: NormalizedRequest,
    candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
) -> RouteSelectionPrediction:
    if (
        task_class == TaskClass.INSPECTION
        and request.repository_context
        and Specialist.REPOSITORY_INSPECTOR in candidates
    ):
        specialist = Specialist.REPOSITORY_INSPECTOR
    elif Specialist.GENERAL in candidates:
        specialist = Specialist.GENERAL
    elif Specialist.REPOSITORY_INSPECTOR in candidates:
        specialist = Specialist.REPOSITORY_INSPECTOR
    else:
        specialist = next(iter(candidates))
    families = candidates[specialist]
    preferred = (
        ToolFamily.CLARIFICATION
        if request.missing_context and ToolFamily.CLARIFICATION in families
        else ToolFamily.BLOCKED
        if task_class == TaskClass.BLOCKED and ToolFamily.BLOCKED in families
        else ToolFamily.FINAL_RESPONSE
        if ToolFamily.FINAL_RESPONSE in families
        else ToolFamily.REPOSITORY_DISCOVERY
        if ToolFamily.REPOSITORY_DISCOVERY in families
        else families[0]
    )
    return RouteSelectionPrediction(
        specialist,
        0.60,
        preferred,
        0.60,
        source=DecisionSource.FALLBACK,
    )


def terminal_family_for_response(
    family: ToolFamily,
    response_mode: ExpectedOutputMode,
    request: NormalizedRequest,
) -> ToolFamily:
    if response_mode == ExpectedOutputMode.FINAL_ANSWER:
        return ToolFamily.FINAL_RESPONSE
    if response_mode == ExpectedOutputMode.CLARIFICATION:
        return ToolFamily.CLARIFICATION
    if response_mode == ExpectedOutputMode.BLOCKED:
        return ToolFamily.BLOCKED
    if request.tools_prohibited:
        return ToolFamily.FINAL_RESPONSE
    return family


def resolve_terminal_tools(
    task_class: TaskClass,
    specialist: Specialist,
    family: ToolFamily,
    response_mode: ExpectedOutputMode,
    request: NormalizedRequest,
    mode: AgentMode,
    *,
    allow_write: bool,
    allow_shell: bool,
    allow_network: bool,
) -> tuple[tuple[str, ...], dict[str, Any]]:
    del allow_network  # No current registry tool has network authority.
    response_set = (
        frozenset(SCHEMA_BY_NAME)
        if response_mode == ExpectedOutputMode.ACTION
        else frozenset()
    )
    policy_set = frozenset(
        name
        for name, schema in SCHEMA_BY_NAME.items()
        if mode.value in schema.allowed_modes
        and (not schema.can_write or allow_write)
        and (not schema.can_run_shell or allow_shell)
    )
    user_set = frozenset(SCHEMA_BY_NAME)
    if request.tools_prohibited:
        user_set = frozenset()
    if request.edits_prohibited:
        user_set -= LIVE_WRITE_TOOLS
    if request.shell_prohibited:
        user_set -= SHELL_TOOLS
    sets = {
        "route_capability": TASK_TOOLS[task_class],
        "policy_permitted": policy_set,
        "response_mode": response_set,
        "specialist": SPECIALIST_TOOLS[specialist],
        "family": FAMILY_TOOLS[family],
        "user_authorized": user_set,
    }
    if family == ToolFamily.EXECUTION_VERIFICATION and not re.search(
        r"\b(?:patch|proposal|diff)\b", request.text.casefold()
    ):
        sets["family"] = sets["family"] - {"test_patch"}
    resolved = set(SCHEMA_BY_NAME)
    removed: dict[str, list[str]] = {name: [] for name in SCHEMA_BY_NAME}
    for set_name, allowed in sets.items():
        for tool in set(SCHEMA_BY_NAME) - set(allowed):
            removed[tool].append(set_name)
        resolved &= set(allowed)
    trace = {
        "precedence": [
            "route_capability",
            "policy_permitted",
            "response_mode",
            "specialist",
            "family",
            "user_authorized",
        ],
        "input_sets": {name: sorted(values) for name, values in sets.items()},
        "removed_by": {
            name: reasons for name, reasons in sorted(removed.items()) if reasons
        },
        "retained": sorted(resolved),
    }
    return tuple(sorted(resolved)), trace


def resolve_lifecycle(
    response_mode: ExpectedOutputMode,
    task_class: TaskClass,
    family: ToolFamily,
    request: NormalizedRequest,
    terminal_tools: tuple[str, ...],
) -> FirstLifecycleStep:
    del terminal_tools
    if response_mode == ExpectedOutputMode.FINAL_ANSWER:
        return FirstLifecycleStep.ANSWER
    if response_mode == ExpectedOutputMode.CLARIFICATION:
        return FirstLifecycleStep.CLARIFICATION
    if response_mode == ExpectedOutputMode.BLOCKED:
        return FirstLifecycleStep.REFUSAL
    if task_class == TaskClass.MUTATION and request.requested_artifact != "new_file":
        return FirstLifecycleStep.INSPECTION
    if task_class == TaskClass.PLANNING and family == ToolFamily.MUTATION_PROPOSAL:
        return (
            FirstLifecycleStep.INSPECTION
            if request.file_paths and request.requested_artifact != "new_file"
            else FirstLifecycleStep.PROPOSAL
        )
    return FAMILY_LIFECYCLE[family]


def resolve_first_step_tools(
    lifecycle: FirstLifecycleStep,
    terminal_tools: tuple[str, ...],
    specialist: Specialist,
    request: NormalizedRequest,
    mode: AgentMode,
    *,
    allow_write: bool,
    allow_shell: bool,
) -> tuple[str, ...]:
    if lifecycle in {
        FirstLifecycleStep.ANSWER,
        FirstLifecycleStep.CLARIFICATION,
        FirstLifecycleStep.REFUSAL,
    }:
        return ()
    if lifecycle == FirstLifecycleStep.INSPECTION and (
        set(terminal_tools) & MUTATION_TOOLS
        or specialist in {Specialist.DEBUGGING, Specialist.SECURITY_REVIEW}
    ):
        candidates = ("read_file", "search_code") if request.file_paths else ("project_map", "search_code")
    else:
        candidates = terminal_tools
    permitted = []
    for name in candidates:
        schema = SCHEMA_BY_NAME.get(name)
        if schema is None or mode.value not in schema.allowed_modes:
            continue
        if schema.can_write and not allow_write:
            continue
        if schema.can_run_shell and not allow_shell:
            continue
        permitted.append(name)
    return tuple(dict.fromkeys(permitted))


def derive_reason_code(
    task_class: TaskClass,
    response_mode: ExpectedOutputMode,
    specialist: Specialist,
    family: ToolFamily,
    lifecycle: FirstLifecycleStep,
    request: NormalizedRequest,
    constraints: tuple[HardConstraint, ...],
) -> ReasonCode:
    del specialist, lifecycle
    identifiers = {item.identifier for item in constraints}
    text = request.text.casefold()
    if response_mode == ExpectedOutputMode.BLOCKED:
        return (
            ReasonCode.POLICY_BLOCKED
            if identifiers & {"destructive_operation", "out_of_workspace"}
            else ReasonCode.MUTATION_REQUIRES_APPROVAL
        )
    if response_mode == ExpectedOutputMode.CLARIFICATION:
        return ReasonCode.CLARIFICATION_MISSING_TARGET
    if family == ToolFamily.FINAL_RESPONSE:
        return (
            ReasonCode.PLANNING_RESPONSE
            if task_class == TaskClass.PLANNING
            else ReasonCode.DIRECT_EXPLANATION
        )
    if family == ToolFamily.REPOSITORY_DISCOVERY:
        return (
            ReasonCode.REPOSITORY_RESOLVES_TARGET
            if request.missing_context
            else ReasonCode.REPOSITORY_INVENTORY
        )
    if family == ToolFamily.SYMBOL_INSPECTION:
        return (
            ReasonCode.REFERENCE_SEARCH
            if re.search(r"\breferences?|call sites?\b", text)
            else ReasonCode.SYMBOL_LOOKUP
        )
    if family == ToolFamily.DOCUMENTATION_RETRIEVAL:
        return ReasonCode.DOCUMENTATION_LOOKUP
    if family == ToolFamily.EXECUTION_VERIFICATION:
        if re.search(r"\b(?:compile|compiler)\b", text):
            return ReasonCode.COMPILATION_CHECK
        if re.search(r"\blint", text):
            return ReasonCode.LINT_CHECK
        if re.search(r"\btests?|pytest|simulation\b", text):
            return ReasonCode.TEST_EXECUTION
        return ReasonCode.COMMAND_EXECUTION
    if family == ToolFamily.MUTATION_PROPOSAL:
        return (
            ReasonCode.NEW_FILE_PATCH_PROPOSAL
            if request.requested_artifact == "new_file"
            else ReasonCode.EXISTING_FILE_PATCH_PROPOSAL
        )
    if family == ToolFamily.TARGETED_MUTATION:
        return ReasonCode.APPROVED_TARGETED_EDIT
    if family == ToolFamily.FILE_CREATION:
        return (
            ReasonCode.APPROVED_FILE_CREATION
            if request.requested_artifact == "new_file"
            else ReasonCode.APPROVED_FULL_FILE_REPLACEMENT
        )
    if family == ToolFamily.PATCH_INSPECTION:
        return (
            ReasonCode.PATCH_TEST
            if request.verification_requested
            else ReasonCode.PATCH_REVIEW
        )
    if family == ToolFamily.MEMORY_RETRIEVAL:
        return ReasonCode.MEMORY_LOOKUP
    if family == ToolFamily.FILE_INSPECTION:
        if request.security_sensitive:
            return ReasonCode.SECURITY_INSPECTION
        if task_class == TaskClass.VERIFICATION:
            return ReasonCode.INSPECT_BEFORE_MUTATE
        return ReasonCode.DIRECT_FILE_READ
    return ReasonCode.SAFE_FALLBACK


def solve_constraints(
    fields: dict[str, Any],
    request: NormalizedRequest,
    constraints: tuple[HardConstraint, ...],
    candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
) -> tuple[dict[str, Any], SolverResult]:
    result = dict(fields)
    violations: list[str] = []
    repairs: list[str] = []
    identifiers = {item.identifier for item in constraints}
    response = result["response_mode"]
    if response != ExpectedOutputMode.ACTION and result["allowed_tools"]:
        violations.append("non_action_with_tools")
        result["allowed_tools"] = ()
        repairs.append("cleared_tools_for_terminal_response")
    if response != ExpectedOutputMode.ACTION and result["terminal_tools"]:
        violations.append("non_action_with_terminal_tools")
        result["terminal_tools"] = ()
        repairs.append("cleared_terminal_tools_for_terminal_response")
    if identifiers & {"read_only", "protected_path"}:
        filtered = tuple(item for item in result["allowed_tools"] if item not in MUTATION_TOOLS)
        terminal = tuple(item for item in result["terminal_tools"] if item not in MUTATION_TOOLS)
        if filtered != result["allowed_tools"] or terminal != result["terminal_tools"]:
            violations.append("mutation_tool_under_read_only_constraint")
            result["allowed_tools"] = filtered
            result["terminal_tools"] = terminal
            repairs.append("removed_mutation_tools")
    if identifiers & {"user_no_mutation", "live_write_not_authorized"}:
        filtered = tuple(item for item in result["allowed_tools"] if item not in LIVE_WRITE_TOOLS)
        terminal = tuple(item for item in result["terminal_tools"] if item not in LIVE_WRITE_TOOLS)
        if filtered != result["allowed_tools"] or terminal != result["terminal_tools"]:
            violations.append("live_write_without_authorization")
            result["allowed_tools"] = filtered
            result["terminal_tools"] = terminal
            repairs.append("removed_live_write_tools")
    if result["specialist"] not in candidates:
        violations.append("specialist_outside_candidate_matrix")
    elif result["family"] not in candidates[result["specialist"]]:
        terminal_exception = (
            response == ExpectedOutputMode.FINAL_ANSWER and result["family"] == ToolFamily.FINAL_RESPONSE
        ) or (
            response == ExpectedOutputMode.BLOCKED and result["family"] == ToolFamily.BLOCKED
        ) or (
            response == ExpectedOutputMode.CLARIFICATION and result["family"] == ToolFamily.CLARIFICATION
        )
        if not terminal_exception:
            violations.append("family_incompatible_with_specialist")
    expected_lifecycle = (
        FirstLifecycleStep.ANSWER
        if response == ExpectedOutputMode.FINAL_ANSWER
        else FirstLifecycleStep.CLARIFICATION
        if response == ExpectedOutputMode.CLARIFICATION
        else FirstLifecycleStep.REFUSAL
        if response == ExpectedOutputMode.BLOCKED
        else result["lifecycle"]
    )
    if result["lifecycle"] != expected_lifecycle:
        violations.append("lifecycle_incompatible_with_response")
        result["lifecycle"] = expected_lifecycle
        repairs.append("aligned_lifecycle_with_response")
    if response == ExpectedOutputMode.ACTION and not result["allowed_tools"]:
        violations.append("action_lifecycle_has_no_available_tool")
        result.update(
            {
                "task_class": TaskClass.BLOCKED,
                "response_mode": ExpectedOutputMode.BLOCKED,
                "specialist": Specialist.GENERAL,
                "family": ToolFamily.BLOCKED,
                "allowed_tools": (),
                "terminal_tools": (),
                "lifecycle": FirstLifecycleStep.REFUSAL,
                "reason": ReasonCode.MISSING_CAPABILITY,
                "confidence": min(float(result["confidence"]), 0.5),
            }
        )
        repairs.append("failed_closed_missing_tool")
    # Reason is always recomputed after any safe repair.
    recomputed_reason = derive_reason_code(
        result["task_class"],
        result["response_mode"],
        result["specialist"],
        result["family"],
        result["lifecycle"],
        request,
        constraints,
    )
    if result["reason"] != recomputed_reason:
        violations.append("reason_incompatible_with_resolved_route")
        result["reason"] = recomputed_reason
        repairs.append("rederived_reason_code")
    unresolved = [
        item
        for item in violations
        if item
        in {
            "specialist_outside_candidate_matrix",
            "family_incompatible_with_specialist",
        }
    ]
    valid = not unresolved
    confidence = round(max(0.0, float(result["confidence"]) - 0.05 * len(repairs)), 3)
    result["confidence"] = confidence
    return result, SolverResult(valid, tuple(violations), tuple(repairs), confidence)


def task_prediction_schema() -> dict[str, Any]:
    values = [item.value for item in TaskClass]
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "task_class", "confidence", "alternatives", "evidence_summary"],
        "properties": {
            "schema_version": {"type": "string", "const": SCHEMA_VERSION},
            "task_class": {"type": "string", "enum": values},
            "confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "alternatives": {
                "type": "array",
                "maxItems": 2,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["task_class", "confidence"],
                    "properties": {
                        "task_class": {"type": "string", "enum": values},
                        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    },
                },
            },
            "evidence_summary": {"type": "string", "maxLength": 240},
        },
    }


def route_selection_schema(
    candidates: Mapping[Specialist, tuple[ToolFamily, ...]]
) -> dict[str, Any]:
    required = [
        "schema_version",
        "specialist",
        "specialist_confidence",
        "immediate_family",
        "family_confidence",
        "alternative_family",
        "evidence_summary",
    ]
    branches = []
    for specialist, candidate_families in candidates.items():
        families = [family.value for family in candidate_families]
        branches.append(
            {
                "type": "object",
                "additionalProperties": False,
                "required": required,
                "properties": {
                    "schema_version": {"type": "string", "const": SCHEMA_VERSION},
                    "specialist": {"type": "string", "const": specialist.value},
                    "specialist_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "immediate_family": {"type": "string", "enum": families},
                    "family_confidence": {
                        "type": "number",
                        "minimum": 0,
                        "maximum": 1,
                    },
                    "alternative_family": {
                        "anyOf": [
                            {"type": "string", "enum": families},
                            {"type": "null"},
                        ]
                    },
                    "evidence_summary": {"type": "string", "maxLength": 240},
                },
            }
        )
    return {"oneOf": branches}


def parse_task_prediction(raw: str) -> TaskPrediction:
    payload = strict_json_object(raw)
    required = {
        "schema_version",
        "task_class",
        "confidence",
        "alternatives",
        "evidence_summary",
    }
    _exact_fields(payload, required)
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError("task prediction schema mismatch")
    confidence = _confidence(payload["confidence"])
    alternatives_raw = payload["alternatives"]
    if not isinstance(alternatives_raw, list) or len(alternatives_raw) > 2:
        raise ValueError("task alternatives must be an array with at most two items")
    alternatives = []
    for item in alternatives_raw:
        if not isinstance(item, dict):
            raise ValueError("task alternative must be an object")
        _exact_fields(item, {"task_class", "confidence"})
        alternatives.append(
            AlternativeTask(TaskClass(item["task_class"]), _confidence(item["confidence"]))
        )
    evidence = payload["evidence_summary"]
    if not isinstance(evidence, str) or len(evidence) > 240:
        raise ValueError("task evidence summary must be a bounded string")
    return TaskPrediction(
        TaskClass(payload["task_class"]), confidence, tuple(alternatives), evidence
    )


def parse_route_selection(
    raw: str,
    candidates: Mapping[Specialist, tuple[ToolFamily, ...]],
) -> RouteSelectionPrediction:
    payload = strict_json_object(raw)
    required = {
        "schema_version",
        "specialist",
        "specialist_confidence",
        "immediate_family",
        "family_confidence",
        "alternative_family",
        "evidence_summary",
    }
    _exact_fields(payload, required)
    if payload["schema_version"] != SCHEMA_VERSION:
        raise ValueError("route selection schema mismatch")
    specialist = Specialist(payload["specialist"])
    if specialist not in candidates:
        raise ValueError("specialist is outside the supplied shortlist")
    family = ToolFamily(payload["immediate_family"])
    if family not in candidates[specialist]:
        raise ValueError("family is incompatible with the selected specialist")
    alternative_raw = payload["alternative_family"]
    alternative = None if alternative_raw is None else ToolFamily(alternative_raw)
    if alternative is not None and alternative not in candidates[specialist]:
        raise ValueError("alternative family is incompatible with the selected specialist")
    evidence = payload["evidence_summary"]
    if not isinstance(evidence, str) or len(evidence) > 240:
        raise ValueError("route evidence summary must be a bounded string")
    return RouteSelectionPrediction(
        specialist,
        _confidence(payload["specialist_confidence"]),
        family,
        _confidence(payload["family_confidence"]),
        alternative,
        evidence,
    )


def strict_json_object(raw: str) -> dict[str, Any]:
    if not isinstance(raw, str):
        raise ValueError("model output must be text")
    if len(raw.encode("utf-8")) > MAX_ROUTING_OUTPUT_BYTES:
        raise ValueError("model output exceeds routing limit")

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        result: dict[str, Any] = {}
        for key, value in items:
            if key in result:
                raise ValueError(f"duplicate JSON field: {key}")
            result[key] = value
        return result

    try:
        payload = json.loads(raw, object_pairs_hook=pairs)
    except json.JSONDecodeError as exc:
        raise ValueError("model output is not exactly one JSON object") from exc
    if not isinstance(payload, dict):
        raise ValueError("model output must be a JSON object")
    return payload


def granted_capabilities(
    mode: AgentMode,
    *,
    allow_write: bool,
    allow_shell: bool,
    allow_network: bool,
) -> tuple[Capability, ...]:
    result = [Capability.WORKSPACE_READ]
    if mode in {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
        result.append(Capability.RUNTIME_STATE)
    if allow_write and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
        result.append(Capability.WORKSPACE_WRITE)
    if allow_shell and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
        result.append(Capability.SHELL)
    if allow_network:
        result.append(Capability.NETWORK)
    return tuple(result)


def route_identity(
    prompt: str, mode: AgentMode, allow_write: bool, allow_shell: bool
) -> str:
    payload = json.dumps(
        {
            "prompt": " ".join(prompt.strip().split()),
            "mode": mode.value,
            "allow_write": allow_write,
            "allow_shell": allow_shell,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"route-{hashlib.sha256(payload.encode('utf-8')).hexdigest()[:24]}"


def _confidence(value: Any) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError("confidence must be numeric")
    number = float(value)
    if not 0 <= number <= 1:
        raise ValueError("confidence must be between zero and one")
    return number


def _exact_fields(payload: Mapping[str, Any], required: set[str]) -> None:
    missing = required - set(payload)
    extra = set(payload) - required
    if missing:
        raise ValueError(f"missing fields: {', '.join(sorted(missing))}")
    if extra:
        raise ValueError(f"unknown fields: {', '.join(sorted(extra))}")


def _json_safe(value: Any) -> Any:
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, Mapping):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (tuple, list, set, frozenset)):
        return [_json_safe(item) for item in value]
    return value
