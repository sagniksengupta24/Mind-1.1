from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


MAX_REQUEST_CHARS = 16_000
MAX_GOAL_CHARS = 4_000
MAX_SCOPE_ITEMS = 64
MAX_SCOPE_ITEM_CHARS = 512
MAX_MISSING_FIELDS = 16


class TaskClass(str, Enum):
    INSPECTION = "inspection"
    MUTATION = "mutation"
    VERIFICATION = "verification"
    EXPLANATION = "explanation"
    PLANNING = "planning"
    BLOCKED = "blocked"


class TargetKind(str, Enum):
    REPOSITORY = "repository"
    DIRECTORY = "directory"
    FILE = "file"
    SYMBOL = "symbol"
    COMMAND = "command"
    UNKNOWN = "unknown"


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AmbiguityLevel(str, Enum):
    NONE = "none"
    RESOLVABLE = "resolvable"
    BLOCKING = "blocking"


class ExpectedOutputMode(str, Enum):
    ACTION = "action"
    FINAL_ANSWER = "final_answer"
    CLARIFICATION = "clarification"
    BLOCKED = "blocked"


class Capability(str, Enum):
    WORKSPACE_READ = "workspace_read"
    WORKSPACE_WRITE = "workspace_write"
    SHELL = "shell"
    NETWORK = "network"
    RUNTIME_STATE = "runtime_state"


class InterpretationIncidentCode(str, Enum):
    MISSING_TARGET = "missing_target"
    MULTIPLE_TARGETS = "multiple_targets"
    MISSING_CAPABILITY = "missing_capability"
    MODE_MISMATCH = "mode_mismatch"
    UNSAFE_REQUEST = "unsafe_request"
    UNSUPPORTED_CAPABILITY = "unsupported_capability"
    PROMPT_INJECTION = "prompt_injection"


@dataclass(frozen=True)
class Ambiguity:
    level: AmbiguityLevel
    missing_fields: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if len(self.missing_fields) > MAX_MISSING_FIELDS:
            raise ValueError("ambiguity contains too many missing fields")
        if any(not item or len(item) > 96 for item in self.missing_fields):
            raise ValueError("ambiguity missing fields must be bounded non-empty strings")
        if self.level == AmbiguityLevel.NONE and self.missing_fields:
            raise ValueError("non-ambiguous intent cannot contain missing fields")

    def to_dict(self) -> dict[str, Any]:
        return {"level": self.level.value, "missing_fields": list(self.missing_fields)}

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "Ambiguity":
        _reject_extra(payload, {"level", "missing_fields"}, "ambiguity")
        return cls(
            level=AmbiguityLevel(str(payload["level"])),
            missing_fields=tuple(_bounded_strings(payload.get("missing_fields", []), "missing_fields")),
        )


@dataclass(frozen=True)
class NormalizedIntent:
    schema_version: str
    intent_id: str
    original_request: str
    goal: str
    intent_type: str
    task_class: TaskClass
    target_scope: tuple[str, ...]
    target_kind: TargetKind
    mutation_intent: bool
    verification_intent: bool
    research_intent: bool
    requires_prior_inspection: bool
    risk_level: RiskLevel
    ambiguity: Ambiguity
    required_capabilities: tuple[Capability, ...]
    forbidden_capabilities: tuple[Capability, ...]
    expected_output_mode: ExpectedOutputMode
    deterministic_signals: tuple[str, ...] = ()
    interpretation_incidents: tuple[InterpretationIncidentCode, ...] = ()

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise ValueError("unsupported normalized-intent schema version")
        if not self.intent_id.startswith("intent-") or len(self.intent_id) > 80:
            raise ValueError("invalid intent id")
        if not self.original_request or len(self.original_request) > MAX_REQUEST_CHARS:
            raise ValueError("original request must be a bounded non-empty string")
        if not self.goal or len(self.goal) > MAX_GOAL_CHARS:
            raise ValueError("goal must be a bounded non-empty string")
        if not self.intent_type or len(self.intent_type) > 96:
            raise ValueError("intent type must be a bounded non-empty string")
        if len(self.target_scope) > MAX_SCOPE_ITEMS:
            raise ValueError("target scope contains too many entries")
        if any(not item or len(item) > MAX_SCOPE_ITEM_CHARS for item in self.target_scope):
            raise ValueError("target scope entries must be bounded non-empty strings")
        if set(self.required_capabilities) & set(self.forbidden_capabilities):
            raise ValueError("a capability cannot be both required and forbidden")
        if len(self.deterministic_signals) > 64:
            raise ValueError("too many deterministic intent signals")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "intent_id": self.intent_id,
            "original_request": self.original_request,
            "goal": self.goal,
            "intent_type": self.intent_type,
            "task_class": self.task_class.value,
            "target_scope": list(self.target_scope),
            "target_kind": self.target_kind.value,
            "mutation_intent": self.mutation_intent,
            "verification_intent": self.verification_intent,
            "research_intent": self.research_intent,
            "requires_prior_inspection": self.requires_prior_inspection,
            "risk_level": self.risk_level.value,
            "ambiguity": self.ambiguity.to_dict(),
            "required_capabilities": [item.value for item in self.required_capabilities],
            "forbidden_capabilities": [item.value for item in self.forbidden_capabilities],
            "expected_output_mode": self.expected_output_mode.value,
            "deterministic_signals": list(self.deterministic_signals),
            "interpretation_incidents": [item.value for item in self.interpretation_incidents],
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "NormalizedIntent":
        fields = {
            "schema_version", "intent_id", "original_request", "goal", "intent_type", "task_class",
            "target_scope", "target_kind", "mutation_intent", "verification_intent", "research_intent",
            "requires_prior_inspection", "risk_level", "ambiguity", "required_capabilities",
            "forbidden_capabilities", "expected_output_mode", "deterministic_signals",
            "interpretation_incidents",
        }
        _reject_extra(payload, fields, "normalized intent")
        missing = fields - set(payload)
        if missing:
            raise ValueError(f"normalized intent missing fields: {', '.join(sorted(missing))}")
        ambiguity = payload["ambiguity"]
        if not isinstance(ambiguity, Mapping):
            raise ValueError("ambiguity must be an object")
        return cls(
            schema_version=str(payload["schema_version"]),
            intent_id=str(payload["intent_id"]),
            original_request=str(payload["original_request"]),
            goal=str(payload["goal"]),
            intent_type=str(payload["intent_type"]),
            task_class=TaskClass(str(payload["task_class"])),
            target_scope=tuple(_bounded_strings(payload["target_scope"], "target_scope")),
            target_kind=TargetKind(str(payload["target_kind"])),
            mutation_intent=_strict_bool(payload["mutation_intent"], "mutation_intent"),
            verification_intent=_strict_bool(payload["verification_intent"], "verification_intent"),
            research_intent=_strict_bool(payload["research_intent"], "research_intent"),
            requires_prior_inspection=_strict_bool(payload["requires_prior_inspection"], "requires_prior_inspection"),
            risk_level=RiskLevel(str(payload["risk_level"])),
            ambiguity=Ambiguity.from_dict(ambiguity),
            required_capabilities=tuple(Capability(value) for value in _bounded_strings(payload["required_capabilities"], "required_capabilities")),
            forbidden_capabilities=tuple(Capability(value) for value in _bounded_strings(payload["forbidden_capabilities"], "forbidden_capabilities")),
            expected_output_mode=ExpectedOutputMode(str(payload["expected_output_mode"])),
            deterministic_signals=tuple(_bounded_strings(payload["deterministic_signals"], "deterministic_signals")),
            interpretation_incidents=tuple(InterpretationIncidentCode(value) for value in _bounded_strings(payload["interpretation_incidents"], "interpretation_incidents")),
        )


def intent_identity(
    request: str,
    *,
    mode: str,
    granted_capabilities: tuple[Capability, ...],
    prior_inspection: bool,
) -> str:
    identity = json.dumps(
        {
            "request": " ".join(request.strip().split()),
            "mode": mode,
            "granted_capabilities": sorted(item.value for item in granted_capabilities),
            "prior_inspection": prior_inspection,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return f"intent-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:24]}"


def _reject_extra(payload: Mapping[str, Any], allowed: set[str], label: str) -> None:
    extra = set(payload) - allowed
    if extra:
        raise ValueError(f"{label} contains unknown fields: {', '.join(sorted(extra))}")


def _bounded_strings(value: Any, label: str) -> list[str]:
    if not isinstance(value, (list, tuple)):
        raise ValueError(f"{label} must be an array")
    result = []
    for item in value:
        if not isinstance(item, str) or not item or len(item) > MAX_SCOPE_ITEM_CHARS:
            raise ValueError(f"{label} must contain bounded non-empty strings")
        result.append(item)
    return result


def _strict_bool(value: Any, label: str) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{label} must be a boolean")
    return value
