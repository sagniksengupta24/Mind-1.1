from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from mind01.semantic_eval_v2 import SemanticV2Error, SUITE, load_v2_partition, validate_semantic_routing_v2


ROOT = Path(__file__).resolve().parents[1]
V1 = ROOT / "mind01" / "eval_suites" / "semantic_routing_v1"


def test_v1_assets_remain_byte_identical() -> None:
    recorded = json.loads((V1 / "dataset_hashes.json").read_text(encoding="utf-8"))
    for filename, metadata in recorded["files"].items():
        actual = hashlib.sha256((V1 / filename).read_bytes()).hexdigest()
        assert actual == metadata["sha256"]


def test_v2_visible_draft_is_complete_and_consistent() -> None:
    result = validate_semantic_routing_v2(require_blind=False)
    assert result["visible_frozen"] is True
    expected_visible_counts = {
        "development": 60,
        "regression": 50,
        "adversarial": 30,
        "capability_mode": 30,
        "ambiguity": 30,
        "lifecycle": 40,
        "end_to_end": 24,
    }
    assert {key: result["counts"][key] for key in expected_visible_counts} == expected_visible_counts
    assert sum(expected_visible_counts.values()) == 264


def test_existing_file_goals_expect_inspection_before_terminal_action() -> None:
    cases = [
        case
        for partition in ("development", "regression", "capability_mode", "lifecycle", "end_to_end")
        for case in load_v2_partition(partition)
    ]
    multistep = [case for case in cases if case["expected"]["terminal_tool_family"] is not None]
    assert multistep
    for case in multistep:
        expected = case["expected"]
        assert expected["required_lifecycle"][0]["phase"] == "inspection"
        assert not expected["immediate_action_side_effect"]
        assert expected["required_lifecycle"][-1]["allowed_tools"] == expected["allowed_terminal_tools"]


def test_all_sixteen_v1_contradictions_have_individual_reviews() -> None:
    report = json.loads((SUITE / "migration_report.json").read_text(encoding="utf-8"))
    contradictions = set(report["contradictory_v1_case_ids"])
    assert len(contradictions) == 16
    entries = {entry["old_case_id"]: entry for entry in report["migrations"]}
    for case_id in contradictions:
        entry = entries[case_id]
        assert entry["old_label_issue"] == "contradictory"
        assert len(entry["reason"]) > 40
        review = entry["independent_semantic_review"]
        assert review["immediate_action_has_side_effect"] is False
        assert review["mode_permits_mutation"] is False
        assert review["correct_response"] == "blocking"
        assert review["terminal_mutation_expected"] is False


def test_v2_end_to_end_fixtures_are_valid_python() -> None:
    for case in load_v2_partition("end_to_end"):
        fixture = SUITE / case["workspace_fixture"]
        compile((fixture / "module.py").read_text(encoding="utf-8"), str(fixture / "module.py"), "exec")
        compile((fixture / "test_module.py").read_text(encoding="utf-8"), str(fixture / "test_module.py"), "exec")


def test_blind_is_required_only_after_external_authoring() -> None:
    if (SUITE / "blind_inputs.json").exists():
        assert validate_semantic_routing_v2(require_blind=True)["counts"]["blind"] >= 100
    else:
        with pytest.raises(SemanticV2Error, match="blind v2 inputs are not frozen"):
            validate_semantic_routing_v2(require_blind=True)
