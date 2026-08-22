from __future__ import annotations

import json

import pytest

from mind01.semantic_benchmark_v2 import (
    FORBIDDEN_MARKERS,
    HOLDOUT_ACCESS,
    SemanticBenchmarkError,
    load_split,
    run_case,
    safe_suite_path,
    semantic_near_duplicates,
    validate_suite,
)


def test_visible_fresh_suite_is_complete_disjoint_and_uncontaminated() -> None:
    result = validate_suite()
    assert result["counts"] == {"examples": 100, "development": 100}
    assert result["validated_cases"] == 200
    assert result["duplicate_count"] == 0
    assert result["near_duplicate_pairs_at_0_985"] == 0
    assert result["contamination_findings"] == 0
    assert result["holdout_opened"] is False
    assert set(result["partition_hashes"]) == {
        "examples.json",
        "development.json",
        "internal_holdout.json",
    }


def test_holdout_requires_explicit_one_shot_protocol() -> None:
    with pytest.raises(SemanticBenchmarkError, match="holdout is closed"):
        load_split("internal_holdout")
    if HOLDOUT_ACCESS.exists():
        access = json.loads(HOLDOUT_ACCESS.read_text(encoding="utf-8"))
        assert access["development_frozen"] is True
        assert "--confirm-holdout-once" in access["command"]


def test_duplicate_and_near_duplicate_detection_is_deterministic() -> None:
    cases = [
        {"case_id": "a", "prompt": "Inspect the parser state now"},
        {"case_id": "b", "prompt": "Inspect the parser state now"},
        {"case_id": "c", "prompt": "Explain a theorem"},
    ]
    assert semantic_near_duplicates(cases) == [("a", "b", 1.0)]


def test_forbidden_marker_guard_covers_frozen_data_references() -> None:
    serialized = {
        "prompt": "ordinary fresh prompt",
        "metadata": "independent authoring",
    }
    text = json.dumps(serialized).casefold()
    assert not any(marker in text for marker in FORBIDDEN_MARKERS)
    contaminated = text + " " + FORBIDDEN_MARKERS[0]
    assert any(marker in contaminated for marker in FORBIDDEN_MARKERS)
    with pytest.raises(SemanticBenchmarkError, match="outside its suite"):
        safe_suite_path("../../evaluation_results/v0.11.0-rc3-1/private.json")


def test_raw_outputs_cannot_change_expected_labels() -> None:
    case = load_split("development")[0]
    result = run_case(
        case,
        router_name="v2",
        live=False,
        model="unused",
        ollama_url="http://127.0.0.1:11434",
        timeout=1,
        seed=11103,
    )
    expected = dict(result["expected"])
    result["raw_outputs"].append('{"task_class":"invented"}')
    assert result["expected"] == expected
