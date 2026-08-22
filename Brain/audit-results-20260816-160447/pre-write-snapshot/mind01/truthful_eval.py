from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from .completion import CompletionAuthority, VerificationEvidence
from .task_contract import EvidenceType, TaskContract, TaskRequirement
from .version import __version__


TRUTHFUL_COMPLETION_VERSION = "truthful-completion-v1"


def default_truthful_suite_path() -> Path:
    return Path(__file__).resolve().parent / "eval_suites" / "truthful_completion_v1.json"


def load_truthful_suite(path: Path | None = None) -> dict[str, Any]:
    source = (path or default_truthful_suite_path()).resolve()
    text = source.read_text(encoding="utf-8")
    payload = json.loads(text)
    if payload.get("schema_version") != "1.0":
        raise ValueError("Truthful completion suite schema_version must be '1.0'.")
    if payload.get("suite_version") != TRUTHFUL_COMPLETION_VERSION:
        raise ValueError("Unsupported truthful completion suite version.")
    cases = payload.get("cases")
    if not isinstance(cases, list) or len(cases) < 25:
        raise ValueError("Truthful completion suite must contain at least 25 cases.")
    identifiers = [str(item.get("id", "")) for item in cases if isinstance(item, dict)]
    if len(identifiers) != len(cases) or any(not item for item in identifiers) or len(set(identifiers)) != len(identifiers):
        raise ValueError("Truthful completion cases require unique non-empty ids.")
    payload["source_path"] = str(source)
    payload["source_sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return payload


def run_truthful_completion_regression(path: Path | None = None) -> dict[str, Any]:
    suite = load_truthful_suite(path)
    results: list[dict[str, Any]] = []
    false_successes = 0
    complete_mappings = 0
    for case in suite["cases"]:
        contract = _contract_for_case(case)
        evidence = [_evidence_from_case(item) for item in case.get("evidence", [])]
        decision = CompletionAuthority().decide(
            str(case.get("requested_status", "verified")),
            task_contract=contract,
            verification=evidence,
            evidence_refs=[str(item) for item in case.get("evidence_refs", [])],
            patch_review=list(case.get("patch_review", [])),
            changed_files=[str(item) for item in case.get("changed_files", ["source.py"])],
            current_state_hash=str(case.get("current_state_hash", "post")),
            receipt_state_hash=str(case.get("receipt_state_hash", "post")),
            unauthorized_mutations=int(case.get("unauthorized_mutations", 0)),
            required_checks_skipped=[str(item) for item in case.get("required_checks_skipped", [])],
            rollback_performed=bool(case.get("rollback_performed", False)),
        )
        expected = str(case["expected_status"])
        passed = decision.status == expected
        false_success = decision.status == "verified" and expected != "verified"
        false_successes += int(false_success)
        if decision.status == "verified" and not decision.unmet_requirements and decision.evidence_refs:
            complete_mappings += 1
        results.append(
            {
                "id": case["id"],
                "passed": passed,
                "expected_status": expected,
                "actual_status": decision.status,
                "false_success": false_success,
                "decision": decision.to_dict(),
            }
        )
    passed_count = sum(bool(item["passed"]) for item in results)
    verified_count = sum(item["actual_status"] == "verified" for item in results)
    return {
        "suite": TRUTHFUL_COMPLETION_VERSION,
        "schema_version": "1.0",
        "metrics_source": "deterministic_adversarial",
        "agent_version": __version__,
        "suite_sha256": suite["source_sha256"],
        "passed": passed_count,
        "total": len(results),
        "false_success_count": false_successes,
        "verified_result_count": verified_count,
        "verified_with_complete_mapping_count": complete_mappings,
        "results": results,
    }


def _contract_for_case(case: dict[str, Any]) -> TaskContract:
    requirements = tuple(
        TaskRequirement(
            id=str(item["id"]),
            description=str(item.get("description", item["id"])),
            required_evidence=tuple(EvidenceType(value) for value in item.get("required_evidence", [])),
        )
        for item in case.get("requirements", [])
    )
    return TaskContract(
        schema_version="1.0",
        contract_id=f"contract-{case['id']}",
        normalized_goal=str(case.get("goal", case["id"])),
        task_type="adversarial_mutation",
        target_scope=tuple(str(item) for item in case.get("target_scope", ["source.py"])),
        forbidden_scope=(".git", ".mind01", "tests"),
        expected_artifacts=("source.py",),
        required_symbols=(),
        required_signatures={},
        behavioral_requirements=("Behavior must pass",),
        regression_requirements=("Regressions must pass",),
        security_requirements=(),
        requirements=requirements,
        rollback_conditions=("Any blocking failure",),
        completion_criteria=("All requirements have current evidence",),
        mutation_required=True,
        baseline_state_hash="pre",
    )


def _evidence_from_case(item: dict[str, Any]) -> VerificationEvidence:
    return VerificationEvidence(
        name=str(item.get("name", item.get("id", "evidence"))),
        command=["deterministic-adversarial-check"],
        status=str(item.get("status", "passed")),
        exit_code=0 if item.get("status", "passed") == "passed" else 1,
        duration_seconds=0.0,
        evidence_id=str(item.get("id", "")),
        evidence_type=str(item.get("type", EvidenceType.ARTIFACT.value)),
        requirement_ids=tuple(str(value) for value in item.get("requirement_ids", [])),
        state_hash=str(item.get("state_hash", "post")),
        observed_after_mutation=bool(item.get("observed_after_mutation", True)),
        blocking=bool(item.get("blocking", True)),
        skipped=bool(item.get("skipped", False)),
        source="deterministic_adversarial_suite",
    )
