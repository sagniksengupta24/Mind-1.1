from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class AgentPhase(str, Enum):
    RECEIVE = "receive"
    CLASSIFY = "classify"
    PLAN = "plan"
    GATHER_CONTEXT = "gather_context"
    MODEL_CALL = "model_call"
    PARSE = "parse"
    POLICY_CHECK = "policy_check"
    EXECUTE = "execute"
    OBSERVE = "observe"
    VERIFY = "verify"
    REPLAN_OR_FINISH = "replan_or_finish"
    FINISHED = "finished"
    FAILED = "failed"


@dataclass(frozen=True)
class PlanStep:
    id: str
    description: str
    required_tools: tuple[str, ...] = ()
    verification: tuple[str, ...] = ()


@dataclass(frozen=True)
class ExecutionPlan:
    objective: str
    assumptions: tuple[str, ...]
    constraints: tuple[str, ...]
    steps: tuple[PlanStep, ...]
    likely_files: tuple[str, ...]
    permitted_tools: tuple[str, ...]
    verification: tuple[str, ...]
    risk_level: str
    completion_criteria: tuple[str, ...]

    def compact_text(self) -> str:
        step_text = "; ".join(f"{step.id}:{step.description}" for step in self.steps)
        checks = ", ".join(self.verification) or "none"
        return (
            f"Objective: {self.objective}\n"
            f"Risk: {self.risk_level}\n"
            f"Steps: {step_text}\n"
            f"Verification: {checks}"
        )


@dataclass
class AgentState:
    objective: str
    mode: str
    max_steps: int
    phase: AgentPhase = AgentPhase.RECEIVE
    specialist: str = "general_reasoning"
    route_confidence: float = 0.0
    plan: ExecutionPlan | None = None
    observations: list[str] = field(default_factory=list)
    tool_results: list[dict[str, Any]] = field(default_factory=list)
    verification_results: list[dict[str, Any]] = field(default_factory=list)
    remaining_steps: int = 0
    parse_retries_remaining: int = 2
    replan_retries_remaining: int = 1
    repeated_actions: dict[str, int] = field(default_factory=dict)
    repeated_errors: dict[str, int] = field(default_factory=dict)
    no_progress_count: int = 0
    completed: bool = False
    failure_reason: str = ""
    response_mode: str = "FINAL_ALLOWED"
    parser_incidents: list[dict[str, Any]] = field(default_factory=list)
    visible_tools: tuple[str, ...] = ()
    output_mode: str = ""
    evidence_refs: dict[str, dict[str, Any]] = field(default_factory=dict)
    mutation_seen: bool = False
    patch_review: list[dict[str, Any]] = field(default_factory=list)
    task_contract: dict[str, Any] = field(default_factory=dict)
    completion_contract: dict[str, Any] = field(default_factory=dict)
    normalized_intent: dict[str, Any] = field(default_factory=dict)
    routing_decision: dict[str, Any] = field(default_factory=dict)
    changed_files: list[str] = field(default_factory=list)
    current_state_hash: str = ""
    receipt_state_hash: str = ""
    unauthorized_mutations: int = 0
    required_checks_skipped: list[str] = field(default_factory=list)
    rollback_performed: bool = False

    def __post_init__(self) -> None:
        if self.remaining_steps <= 0:
            self.remaining_steps = self.max_steps

    def transition(self, phase: AgentPhase) -> None:
        self.phase = phase

    def record_action(self, signature: str) -> int:
        count = self.repeated_actions.get(signature, 0) + 1
        self.repeated_actions[signature] = count
        return count

    def record_error(self, error: str) -> int:
        normalized = error.strip()[:300]
        count = self.repeated_errors.get(normalized, 0) + 1
        self.repeated_errors[normalized] = count
        return count
