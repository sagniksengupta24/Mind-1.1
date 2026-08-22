from __future__ import annotations

from dataclasses import asdict, dataclass, field, replace
from typing import Any, Literal, Mapping, Sequence

from .task_contract import EvidenceType, TaskContract, TaskRequirement


CompletionStatus = Literal[
    "verified",
    "partially_verified",
    "unverified",
    "failed",
    "blocked",
    "policy_denied",
    "rolled_back",
]

ALLOWED_COMPLETION_STATUSES: set[str] = {
    "verified",
    "partially_verified",
    "unverified",
    "failed",
    "blocked",
    "policy_denied",
    "rolled_back",
}


@dataclass(frozen=True)
class VerificationEvidence:
    name: str
    command: list[str]
    status: str
    exit_code: int | None
    duration_seconds: float
    output_summary: str = ""
    level: str = "acceptance"
    selected_reason: str = ""
    evidence_id: str = ""
    evidence_type: str = EvidenceType.BEHAVIORAL_TEST.value
    requirement_ids: tuple[str, ...] = ()
    proven_properties: tuple[str, ...] = ()
    unproven_properties: tuple[str, ...] = ()
    state_hash: str = ""
    observed_after_mutation: bool = True
    blocking: bool = True
    skipped: bool = False
    source: str = "runtime"

    @property
    def passed(self) -> bool:
        return self.status == "passed" and self.exit_code in (0, None) and not self.skipped

    @property
    def blocking_failed(self) -> bool:
        return self.blocking and (self.status == "failed" or self.skipped)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_mapping(cls, payload: Mapping[str, Any], *, fallback_id: str = "") -> "VerificationEvidence":
        duration_ms = payload.get("duration_ms", 0)
        duration = payload.get("duration_seconds", float(duration_ms or 0) / 1000.0)
        status = str(payload.get("status", "unavailable"))
        exit_code = payload.get("exit_code")
        if exit_code is None and status == "passed":
            exit_code = 0
        return cls(
            name=str(payload.get("name") or payload.get("check") or "verification"),
            command=[str(item) for item in payload.get("command", [])],
            status=status,
            exit_code=exit_code if isinstance(exit_code, int) else None,
            duration_seconds=float(duration or 0.0),
            output_summary=str(payload.get("output_summary", "")),
            level=str(payload.get("level", "acceptance")),
            selected_reason=str(payload.get("selected_reason", "")),
            evidence_id=str(payload.get("evidence_id") or fallback_id),
            evidence_type=str(payload.get("evidence_type", EvidenceType.ARTIFACT.value)),
            requirement_ids=tuple(str(item) for item in payload.get("requirement_ids", [])),
            proven_properties=tuple(str(item) for item in payload.get("proven_properties", [])),
            unproven_properties=tuple(str(item) for item in payload.get("unproven_properties", [])),
            state_hash=str(payload.get("state_hash", "")),
            observed_after_mutation=bool(payload.get("observed_after_mutation", True)),
            blocking=bool(payload.get("blocking", False)),
            skipped=bool(payload.get("skipped", False)),
            source=str(payload.get("source", "runtime")),
        )


@dataclass(frozen=True)
class CompletionDecision:
    status: CompletionStatus
    evidence_refs: tuple[str, ...]
    satisfied_requirements: tuple[str, ...]
    unmet_requirements: tuple[str, ...]
    rejected_evidence: tuple[str, ...]
    reasons: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CompletionContract:
    schema_version: str
    status: CompletionStatus
    objective: str
    specialist: str
    plan_summary: list[str]
    files_changed: list[str]
    verification: list[VerificationEvidence]
    repair_attempts: int
    rollback_available: bool
    remaining_uncertainty: list[str] = field(default_factory=list)
    patch_review: list[dict[str, Any]] = field(default_factory=list)
    failure_category: str = ""
    task_contract: dict[str, Any] = field(default_factory=dict)
    evidence_refs: list[str] = field(default_factory=list)
    satisfied_requirements: list[str] = field(default_factory=list)
    unmet_requirements: list[str] = field(default_factory=list)
    rejected_evidence: list[str] = field(default_factory=list)
    completion_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["verification"] = [item.to_dict() for item in self.verification]
        return payload

    def to_user_text(self) -> str:
        checks = ", ".join(f"{item.name}:{item.status}" for item in self.verification) or "none"
        changed = ", ".join(self.files_changed) or "none"
        uncertainty = "; ".join(self.remaining_uncertainty) or "none"
        unmet = ", ".join(self.unmet_requirements) or "none"
        return (
            f"status={self.status}\n"
            f"objective={self.objective}\n"
            f"files_changed={changed}\n"
            f"verification={checks}\n"
            f"unmet_requirements={unmet}\n"
            f"repair_attempts={self.repair_attempts}\n"
            f"remaining_uncertainty={uncertainty}"
        )


class CompletionAuthority:
    """The single authority for completion status.

    Model-requested status is an input, never proof. A verified decision requires
    current, passing, task-relevant evidence for every mandatory requirement.
    """

    def decide(
        self,
        requested_status: str,
        *,
        task_contract: TaskContract | None,
        verification: Sequence[VerificationEvidence | Mapping[str, Any]],
        evidence_refs: Sequence[str] = (),
        patch_review: Sequence[Mapping[str, Any]] = (),
        changed_files: Sequence[str] = (),
        current_state_hash: str = "",
        receipt_state_hash: str = "",
        unauthorized_mutations: int = 0,
        required_checks_skipped: Sequence[str] = (),
        rollback_performed: bool = False,
    ) -> CompletionDecision:
        requested = requested_status if requested_status in ALLOWED_COMPLETION_STATUSES else "unverified"
        evidence = _coerce_evidence(verification)
        by_id = {item.evidence_id: item for item in evidence if item.evidence_id}
        rejected: list[str] = []
        reasons: list[str] = []

        for reference in evidence_refs:
            if reference not in by_id:
                rejected.append(reference)
                reasons.append(f"stale or unknown evidence reference: {reference}")

        blocking_review = any(
            str(item.get("severity", "")) == "blocking" and not bool(item.get("resolved_by_rollback"))
            for item in patch_review
        )
        blocking_failure = any(item.blocking_failed for item in evidence)
        scope_violation = False
        if task_contract and task_contract.mutation_required:
            for changed in changed_files:
                if any(
                    changed == forbidden or changed.startswith(forbidden.rstrip("/") + "/")
                    for forbidden in task_contract.forbidden_scope
                ):
                    scope_violation = True
                if task_contract.target_scope and not any(
                    changed == target or changed.startswith(target.rstrip("/") + "/")
                    for target in task_contract.target_scope
                ):
                    scope_violation = True
        if scope_violation:
            reasons.append("mutation escaped the authorized task scope")
        if unauthorized_mutations:
            reasons.append("unauthorized mutation detected")
        if required_checks_skipped:
            reasons.append("mandatory checks were skipped: " + ", ".join(required_checks_skipped))
        if receipt_state_hash and current_state_hash and receipt_state_hash != current_state_hash:
            reasons.append("final workspace state does not match mutation receipt")

        valid: list[VerificationEvidence] = []
        for item in evidence:
            if not item.passed:
                continue
            if task_contract and task_contract.mutation_required and not item.observed_after_mutation:
                rejected.append(item.evidence_id or item.name)
                continue
            if current_state_hash and item.state_hash and item.state_hash != current_state_hash:
                rejected.append(item.evidence_id or item.name)
                continue
            valid.append(item)

        requirements = task_contract.mandatory_requirements() if task_contract else ()
        satisfied: list[str] = []
        unmet: list[str] = []
        required_evidence_ids: list[str] = []
        for requirement in requirements:
            matched = _evidence_for_requirement(requirement, valid)
            present_types = {item.evidence_type for item in matched}
            required_types = {item.value for item in requirement.required_evidence}
            if required_types.issubset(present_types):
                satisfied.append(requirement.id)
                required_evidence_ids.extend(item.evidence_id for item in matched if item.evidence_id)
            else:
                unmet.append(requirement.id)

        hard_failure = bool(
            blocking_review
            or blocking_failure
            or unauthorized_mutations
            or scope_violation
            or required_checks_skipped
            or (receipt_state_hash and current_state_hash and receipt_state_hash != current_state_hash)
        )
        if hard_failure:
            status: CompletionStatus = "rolled_back" if rollback_performed else "failed"
        elif rollback_performed:
            status = "rolled_back"
            reasons.append("mutation was rolled back")
        elif requirements and not unmet:
            status = "verified"
            reasons.append("all mandatory requirements have current task-relevant evidence")
        elif requirements and satisfied:
            status = "partially_verified"
            reasons.append("only a subset of mandatory requirements has evidence")
        elif task_contract and task_contract.mutation_required:
            status = "unverified"
            reasons.append("mutation has no complete task-relevant acceptance evidence")
        elif requested == "verified":
            referenced_pass = any(reference in by_id and by_id[reference].passed for reference in evidence_refs)
            if referenced_pass and not rejected:
                status = "verified"
            else:
                status = "unverified"
                reasons.append("verified status lacks a current referenced passing evidence record")
        else:
            status = requested  # type: ignore[assignment]

        if requested in {"failed", "blocked", "policy_denied"} and not requirements:
            status = requested  # type: ignore[assignment]
        if rejected and status == "verified":
            status = "unverified"
            reasons.append("one or more supplied evidence references are invalid")

        return CompletionDecision(
            status=status,
            evidence_refs=tuple(dict.fromkeys(required_evidence_ids)),
            satisfied_requirements=tuple(satisfied),
            unmet_requirements=tuple(unmet),
            rejected_evidence=tuple(dict.fromkeys(rejected)),
            reasons=tuple(dict.fromkeys(reasons)),
        )


def _coerce_evidence(
    verification: Sequence[VerificationEvidence | Mapping[str, Any]],
) -> list[VerificationEvidence]:
    result: list[VerificationEvidence] = []
    for index, item in enumerate(verification, start=1):
        if isinstance(item, VerificationEvidence):
            evidence = item
        else:
            evidence = VerificationEvidence.from_mapping(item, fallback_id=f"evidence-{index:03d}")
        if not evidence.evidence_id:
            evidence = replace(evidence, evidence_id=f"evidence-{index:03d}")
        result.append(evidence)
    return result


def _evidence_for_requirement(
    requirement: TaskRequirement,
    evidence: Sequence[VerificationEvidence],
) -> list[VerificationEvidence]:
    allowed = {item.value for item in requirement.required_evidence}
    return [
        item
        for item in evidence
        if requirement.id in item.requirement_ids and item.evidence_type in allowed
    ]


def normalize_completion_status(
    requested_status: str,
    *,
    verification: list[VerificationEvidence],
    patch_review: list[dict[str, Any]] | None = None,
    uncertainty: list[str] | None = None,
) -> tuple[CompletionStatus, list[str]]:
    """Compatibility wrapper around the authoritative completion decision."""

    prepared: list[VerificationEvidence] = []
    for index, item in enumerate(verification, start=1):
        prepared.append(
            replace(
                item,
                evidence_id=item.evidence_id or f"evidence-{index:03d}",
                requirement_ids=item.requirement_ids or ("R-ACCEPTANCE",),
            )
        )
    contract = None
    if prepared:
        required_types = tuple(
            dict.fromkeys(EvidenceType(item.evidence_type) for item in prepared if item.passed)
        )
        if required_types:
            contract = TaskContract(
                schema_version="1.0",
                contract_id="compatibility-contract",
                normalized_goal="compatibility completion",
                task_type="acceptance",
                target_scope=(),
                forbidden_scope=(),
                expected_artifacts=(),
                required_symbols=(),
                required_signatures={},
                behavioral_requirements=(),
                regression_requirements=(),
                security_requirements=(),
                requirements=(TaskRequirement("R-ACCEPTANCE", "Acceptance evidence passes", required_types),),
                rollback_conditions=(),
                completion_criteria=(),
                mutation_required=True,
            )
    decision = CompletionAuthority().decide(
        requested_status,
        task_contract=contract,
        verification=prepared,
        evidence_refs=[item.evidence_id for item in prepared],
        patch_review=patch_review or [],
    )
    remaining = list(uncertainty or [])
    if decision.status != "verified":
        remaining.extend(decision.reasons)
    return decision.status, list(dict.fromkeys(remaining))


def build_completion_contract(
    *,
    objective: str,
    requested_status: str,
    specialist: str = "general_reasoning",
    plan_summary: list[str] | None = None,
    files_changed: list[str] | None = None,
    verification: list[VerificationEvidence] | None = None,
    repair_attempts: int = 0,
    rollback_available: bool = False,
    remaining_uncertainty: list[str] | None = None,
    patch_review: list[dict[str, Any]] | None = None,
    failure_category: str = "",
    task_contract: TaskContract | None = None,
    current_state_hash: str = "",
    receipt_state_hash: str = "",
    unauthorized_mutations: int = 0,
    required_checks_skipped: list[str] | None = None,
    rollback_performed: bool = False,
) -> CompletionContract:
    evidence = _coerce_evidence(list(verification or []))
    review = list(patch_review or [])
    decision = CompletionAuthority().decide(
        requested_status,
        task_contract=task_contract,
        verification=evidence,
        evidence_refs=[item.evidence_id for item in evidence],
        patch_review=review,
        changed_files=files_changed or [],
        current_state_hash=current_state_hash,
        receipt_state_hash=receipt_state_hash,
        unauthorized_mutations=unauthorized_mutations,
        required_checks_skipped=required_checks_skipped or [],
        rollback_performed=rollback_performed,
    )
    uncertainty = list(remaining_uncertainty or [])
    uncertainty.extend(decision.reasons)
    return CompletionContract(
        schema_version="1.0",
        status=decision.status,
        objective=objective,
        specialist=specialist,
        plan_summary=list(plan_summary or []),
        files_changed=sorted(set(files_changed or [])),
        verification=evidence,
        repair_attempts=repair_attempts,
        rollback_available=rollback_available,
        remaining_uncertainty=list(dict.fromkeys(uncertainty)),
        patch_review=review,
        failure_category=failure_category,
        task_contract=task_contract.to_dict() if task_contract else {},
        evidence_refs=list(decision.evidence_refs),
        satisfied_requirements=list(decision.satisfied_requirements),
        unmet_requirements=list(decision.unmet_requirements),
        rejected_evidence=list(decision.rejected_evidence),
        completion_reasons=list(decision.reasons),
    )
