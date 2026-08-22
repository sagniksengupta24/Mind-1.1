from __future__ import annotations

import json
import io
import sys
import tarfile
import zipfile
from pathlib import Path

import pytest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
import rc3_1_pipeline as pipeline  # noqa: E402


def minimal_policy(*, missing_family: bool = False) -> dict:
    return {
        "coverage": {
            "public_categories_required": [],
            "task_classes_required": ["inspection"],
            "immediate_families_required": ["never_present" if missing_family else "file_inspection"],
            "immediate_tools_required": ["read_file"],
            "response_modes_required": ["action"],
            "lifecycle_requirements": ["single_action"],
        }
    }


def synthetic_pool(count: int = 125) -> tuple[list[str], dict, dict]:
    ids, cases, labels = [], {}, {}
    for index in range(count):
        case_id = f"synthetic-{index:03d}"
        ids.append(case_id)
        cases[case_id] = {
            "case_id": case_id,
            "prompt": f"Inspect synthetic fixture {index}",
            "partition": "test",
            "workspace_fixture": f"fixture-{index}",
            "agent_mode": "read_only",
            "capabilities": {"workspace_read": True, "workspace_write": False, "shell": False, "network": False},
            "public_facts": {
                "requested_operation": "inspect", "target_state": "exists_unique",
                "route_state": "none", "unsafe_operation": False, "prompt_injection": False,
                "unsupported_operation": False, "self_contained": False,
                "repository_resolvable": False,
            },
            "authoring_metadata": {
                "archetype": f"group-{index % 25:02d}",
                "fixture_kind": "standard",
            },
        }
        labels[case_id] = {
            "task_class": "inspection",
            "immediate_tool_family": "file_inspection",
            "allowed_immediate_tools": ["read_file"],
            "response_mode": "action",
            "reason_code": f"synthetic_reason_{index % 20}",
            "required_lifecycle": [{"phase": "inspection", "allowed_tools": ["read_file"]}],
            "allowed_alternative_lifecycles": [],
            "terminal_tool_family": None,
            "terminal_mutation_expected": False,
        }
    return ids, cases, labels


def test_exactly_120_preselected_with_one_rejection_cannot_produce_120() -> None:
    ids, cases, labels = synthetic_pool(120)
    with pytest.raises(pipeline.PipelineHold):
        pipeline.coverage_selection(ids[:-1], cases, labels, minimal_policy())


def test_sufficient_accepted_reserve_produces_120() -> None:
    ids, cases, labels = synthetic_pool(125)
    selected, report = pipeline.coverage_selection(ids, cases, labels, minimal_policy())
    assert len(selected) == 120
    assert report["passed"]


def test_rejected_cases_are_never_eligible() -> None:
    states = {"a": {"state": "accepted"}, "b": {"state": "rejected"}}
    assert pipeline.eligible_case_ids(states, ["a", "b"]) == ["a"]


def test_unresolved_cases_are_never_eligible() -> None:
    states = {"a": {"state": "accepted"}, "b": {"state": "unresolved"}}
    assert pipeline.eligible_case_ids(states, ["a", "b"]) == ["a"]


def test_selection_is_deterministic() -> None:
    ids, cases, labels = synthetic_pool(125)
    first, _ = pipeline.coverage_selection(ids, cases, labels, minimal_policy())
    second, _ = pipeline.coverage_selection(list(reversed(ids)), cases, labels, minimal_policy())
    assert first == second


def test_coverage_constraints_are_enforced() -> None:
    ids, cases, labels = synthetic_pool(125)
    with pytest.raises(pipeline.PipelineHold, match="coverage"):
        pipeline.coverage_selection(ids, cases, labels, minimal_policy(missing_family=True))


def test_changing_selection_policy_changes_identity_hash(tmp_path: Path) -> None:
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    left.write_text('{"required":120}\n', encoding="utf-8")
    right.write_text('{"required":121}\n', encoding="utf-8")
    assert pipeline.sha256(left) != pipeline.sha256(right)


def test_changing_one_input_changes_set_hash(tmp_path: Path) -> None:
    left = tmp_path / "left.json"
    right = tmp_path / "right.json"
    left.write_text('{"cases":[{"case_id":"a"}]}\n', encoding="utf-8")
    right.write_text('{"cases":[{"case_id":"b"}]}\n', encoding="utf-8")
    assert pipeline.sha256(left) != pipeline.sha256(right)


def test_old_superseded_set_is_not_current() -> None:
    freeze = pipeline.load_json(pipeline.FREEZE_PATH)
    assert freeze["old_seal_status"].startswith("SUPERSEDED")
    assert freeze["old_blind_input_hash"] != "semantic-routing-blind-rc3.1"


def test_untracked_evaluation_scripts_block_sealing(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pipeline, "git", lambda *args, **kwargs: "scripts/rc3_1_pipeline.py")
    with pytest.raises(RuntimeError, match="untracked evaluation scripts"):
        pipeline.script_manifest(require_tracked=True)


def test_evaluator_source_drift_blocks_freeze(monkeypatch: pytest.MonkeyPatch) -> None:
    original = pipeline.sha256
    monkeypatch.setattr(
        pipeline,
        "sha256",
        lambda path: "0" * 64 if str(path).endswith("annotation_v3.py") else original(path),
    )
    with pytest.raises(RuntimeError, match="evaluator"):
        pipeline.verify_freeze()


def test_runtime_source_drift_blocks_freeze(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(pipeline, "runtime_manifest", lambda root=pipeline.ROOT: {"runtime.py": "changed"})
    with pytest.raises(RuntimeError, match="runtime"):
        pipeline.verify_freeze()


def test_contamination_in_artifact_is_blocking(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.zip"
    private = b'{"labels":[{"case_id":"blind-secret"}]}'
    with zipfile.ZipFile(artifact, "w") as archive:
        archive.writestr("pkg/private_labels.json", private)
    report = pipeline.scan_artifact(artifact, private, pipeline.hashlib.sha256(private).hexdigest(), ["blind-secret"])
    assert not report["passed"]
    assert report["blocking_findings"]


def test_private_labels_absent_from_runtime_artifact(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.zip"
    private = b'{"labels":[{"case_id":"blind-secret"}]}'
    with zipfile.ZipFile(artifact, "w") as archive:
        archive.writestr("pkg/runtime.py", "VERSION = '0.11.0.dev0'\n")
    report = pipeline.scan_artifact(artifact, private, pipeline.hashlib.sha256(private).hexdigest(), ["blind-secret"])
    assert report["passed"]


def test_private_labels_in_sdist_are_blocking(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.tar.gz"
    private = b'{"labels":[{"case_id":"blind-secret"}]}'
    info = tarfile.TarInfo("pkg/private_labels.json")
    info.size = len(private)
    with tarfile.open(artifact, "w:gz") as archive:
        archive.addfile(info, io.BytesIO(private))
    report = pipeline.scan_artifact(
        artifact, private, pipeline.hashlib.sha256(private).hexdigest(), ["blind-secret"]
    )
    assert not report["passed"]
    assert report["members_scanned"] == 1


def test_existing_sealed_artifact_cannot_be_overwritten(tmp_path: Path) -> None:
    output = tmp_path / "sealed"
    output.mkdir()
    (output / "manifest.json").write_text("{}\n", encoding="utf-8")
    with pytest.raises(FileExistsError, match="refusing to overwrite"):
        pipeline.ensure_new_directory(output)


def test_fewer_than_120_accepted_candidates_produces_hold() -> None:
    ids, cases, labels = synthetic_pool(119)
    with pytest.raises(pipeline.PipelineHold):
        pipeline.coverage_selection(ids, cases, labels, minimal_policy())


def test_write_json_refuses_existing_identity(tmp_path: Path) -> None:
    path = tmp_path / "identity.json"
    pipeline.write_json(path, {"version": 1}, overwrite=False)
    with pytest.raises(FileExistsError):
        pipeline.write_json(path, {"version": 2}, overwrite=False)


def test_public_projection_excludes_authoring_and_labels() -> None:
    _, cases, _ = synthetic_pool(1)
    public = pipeline.public_input(cases["synthetic-000"])
    assert "authoring_metadata" not in public
    assert "annotation" not in public
