from __future__ import annotations

from pathlib import Path
import sys

from mind01.completion import CompletionAuthority, VerificationEvidence
from mind01.eval_harness import _mutation_completion_decision
from mind01.patch_review import review_patch
from mind01.self_correction import SelfCorrectionController
from mind01.task_contract import EvidenceType, TaskContract, TaskRequirement, build_task_contract
from mind01.truthful_eval import load_truthful_suite, run_truthful_completion_regression
from mind01.verification import VerificationEngine


def test_truthful_completion_suite_has_25_adversarial_cases_and_zero_false_success() -> None:
    suite = load_truthful_suite()
    assert len(suite["cases"]) >= 25
    result = run_truthful_completion_regression()
    assert result["passed"] == result["total"]
    assert result["total"] >= 28
    assert result["false_success_count"] == 0
    assert result["verified_result_count"] > 0
    assert result["verified_with_complete_mapping_count"] == result["verified_result_count"]


def test_compile_and_structure_cannot_verify_behavior() -> None:
    contract = _behavior_contract()
    evidence = [
        _evidence("syntax", EvidenceType.SYNTAX, "R-BEHAVIOR"),
        _evidence("structure", EvidenceType.SOURCE_STRUCTURE, "R-BEHAVIOR"),
    ]
    decision = CompletionAuthority().decide(
        "verified",
        task_contract=contract,
        verification=evidence,
        evidence_refs=[item.evidence_id for item in evidence],
        changed_files=["source.py"],
        current_state_hash="post",
        receipt_state_hash="post",
    )
    assert decision.status == "unverified"
    assert decision.unmet_requirements == ("R-BEHAVIOR",)


def test_wrong_symbol_and_signature_are_blocking(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text("def wrong(value, extra):\n    return value\n", encoding="utf-8")
    contract = build_task_contract(
        "Implement function expected(value) in source.py",
        mutation_required=True,
        specialist="code_modification",
    )
    results = VerificationEngine(tmp_path).verify_paths(
        ["source.py"], contract=contract, mutation_state_hash="post"
    )
    symbol = next(item for item in results if item.check == "python-symbol:expected")
    signature = next(item for item in results if item.check == "python-signature:expected")
    assert symbol.status == "failed" and symbol.blocking
    assert signature.status == "failed" and signature.blocking


def test_function_in_docstring_is_not_executable_symbol(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text('"""\ndef expected(value):\n    return value\n"""\n', encoding="utf-8")
    contract = build_task_contract(
        "Implement function expected(value) in source.py",
        mutation_required=True,
        specialist="code_modification",
    )
    results = VerificationEngine(tmp_path).verify_paths(
        ["source.py"], contract=contract, mutation_state_hash="post"
    )
    structure = next(item for item in results if item.check == "python-executable-structure")
    symbol = next(item for item in results if item.check == "python-symbol:expected")
    assert structure.status == "failed"
    assert symbol.status == "failed"


def test_import_failure_is_blocking_and_not_behavioral_evidence(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text("import dependency_that_does_not_exist\n", encoding="utf-8")
    contract = build_task_contract(
        "Implement Python behavior in source.py",
        mutation_required=True,
        specialist="code_modification",
    )
    results = VerificationEngine(tmp_path).verify_paths(
        ["source.py"],
        full_project=True,
        contract=contract,
        mutation_state_hash="post",
    )
    imported = next(item for item in results if item.check == "python-import:source.py")
    assert imported.status == "failed"
    assert imported.blocking
    assert imported.evidence_type == EvidenceType.IMPORTABILITY.value
    assert "correct behavior" in imported.unproven_properties


def test_patch_review_blocks_deleted_tests_weakened_assertions_and_swallowed_exceptions() -> None:
    deleted = review_patch(
        diff_text="--- a/tests/test_x.py\n+++ /dev/null\n-assert value\n",
        changed_files=["tests/test_x.py"],
    )
    weakened = review_patch(
        diff_text="--- a/tests/test_x.py\n+++ b/tests/test_x.py\n-assert value == 2\n+value == 2\n",
        changed_files=["tests/test_x.py"],
    )
    swallowed = review_patch(
        diff_text="--- a/source.py\n+++ b/source.py\n+except Exception: pass\n",
        changed_files=["source.py"],
    )
    assert {item.code for item in deleted.findings if item.severity == "blocking"} >= {"tests-deleted"}
    assert {item.code for item in weakened.findings if item.severity == "blocking"} >= {"assertions-weakened"}
    assert {item.code for item in swallowed.findings if item.severity == "blocking"} >= {"broad-exception-swallow"}


def test_task_contract_is_serializable_and_hash_stable() -> None:
    contract = build_task_contract(
        "Implement function calculate_total(items) in src/calculate.py and preserve tests",
        mutation_required=True,
        specialist="code_modification",
    )
    restored = TaskContract.from_dict(contract.to_dict())
    assert restored.sha256() == contract.sha256()
    assert restored.required_symbols == ("calculate_total",)
    assert restored.required_signatures == {"calculate_total": ("items",)}
    rebuilt = build_task_contract(
        "Implement function calculate_total(items) in src/calculate.py and preserve tests",
        mutation_required=True,
        specialist="code_modification",
    )
    assert rebuilt.contract_id == contract.contract_id


def test_failed_post_write_acceptance_is_rolled_back(tmp_path: Path) -> None:
    target = tmp_path / "source.py"
    target.write_text("value = 1\n", encoding="utf-8")

    def make_bad_change(workspace: Path, _state) -> str:  # type: ignore[no-untyped-def]
        (workspace / "source.py").write_text("value = 2\n", encoding="utf-8")
        return "changed source"

    outcome = SelfCorrectionController(tmp_path, repair_budget=0).run(
        objective="change source",
        repair_executors=[make_bad_change],
        verification_commands=[[sys.executable, "-c", "raise SystemExit(1)"]],
        expected_paths=["source.py"],
    )
    assert target.read_text(encoding="utf-8") == "value = 1\n"
    assert outcome.attempts[0].rolled_back
    assert outcome.contract.status == "failed"


def test_real_mutation_harness_uses_completion_authority() -> None:
    fixture = {
        "id": "feature",
        "task": "Implement independently accepted behavior",
        "acceptance": "hidden_feature",
        "expected_paths": ["source.py"],
        "protected_paths": ["tests"],
    }
    accepted = _mutation_completion_decision(
        fixture=fixture,
        accepted=True,
        acceptance_passed=True,
        changed_files=["source.py"],
        patch_review=[{"severity": "info", "code": "review-clean"}],
        rollback_performed=False,
    )
    rejected = _mutation_completion_decision(
        fixture=fixture,
        accepted=False,
        acceptance_passed=False,
        changed_files=[],
        patch_review=[{"severity": "info", "code": "review-clean"}],
        rollback_performed=True,
    )
    assert accepted.status == "verified"
    assert accepted.unmet_requirements == ()
    assert rejected.status == "rolled_back"


def _behavior_contract() -> TaskContract:
    return TaskContract(
        schema_version="1.0",
        contract_id="test-contract",
        normalized_goal="Implement behavior",
        task_type="implement_function",
        target_scope=("source.py",),
        forbidden_scope=(".git", ".mind01", "tests"),
        expected_artifacts=("source.py",),
        required_symbols=(),
        required_signatures={},
        behavioral_requirements=("Behavior passes",),
        regression_requirements=(),
        security_requirements=(),
        requirements=(
            TaskRequirement("R-BEHAVIOR", "Behavior passes", (EvidenceType.BEHAVIORAL_TEST,)),
        ),
        rollback_conditions=("failure",),
        completion_criteria=("evidence",),
        mutation_required=True,
        baseline_state_hash="pre",
    )


def _evidence(identifier: str, kind: EvidenceType, requirement: str) -> VerificationEvidence:
    return VerificationEvidence(
        name=identifier,
        command=["check"],
        status="passed",
        exit_code=0,
        duration_seconds=0.0,
        evidence_id=identifier,
        evidence_type=kind.value,
        requirement_ids=(requirement,),
        state_hash="post",
    )
