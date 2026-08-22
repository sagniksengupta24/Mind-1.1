from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import subprocess
import tarfile
import zipfile
from collections import Counter, defaultdict, deque
from pathlib import Path
from typing import Any, Iterable, Mapping


ROOT = Path(__file__).resolve().parents[1]
GOVERNANCE = ROOT / "evaluation_governance/rc3_1"
FREEZE_PATH = GOVERNANCE / "freeze_manifest.json"
POLICY_PATH = GOVERNANCE / "selection_policy.json"
FINAL_COUNT = 120
EVALUATOR_FILES = (
    "mind01/annotation_v3.py",
    "mind01/eval_suites/semantic_routing_v3/annotation_contract.json",
    "mind01/eval_suites/semantic_routing_v3/evaluator_calibration.json",
    "mind01/eval_suites/semantic_routing_v3/public_scoring_contract.json",
    "mind01/eval_suites/semantic_routing_v3/schema.json",
    "scripts/build_semantic_v3_assets.py",
    "scripts/freeze_semantic_v3_evaluator.py",
    "scripts/run_semantic_v3_annotation.py",
    "tests/test_annotation_v3.py",
)
EVALUATION_SCRIPTS = (
    "scripts/author_semantic_v3_blind.py",
    "scripts/select_semantic_v3_blind_inputs.py",
    "scripts/validate_semantic_v3_blind_independence.py",
    "scripts/seal_semantic_v3_blind.py",
    "scripts/rc3_1_pipeline.py",
    "scripts/build_semantic_v3_assets.py",
    "scripts/freeze_semantic_v3_evaluator.py",
    "scripts/run_semantic_v3_annotation.py",
    "scripts/run_rc3_1_annotation.py",
    "scripts/run_rc3_1_sealed.py",
    "scripts/score_rc3_1_sealed.py",
)


class PipelineHold(RuntimeError):
    pass


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Evaluation-only RC3.1 blind reserve, selection, contamination, sealing, and gate controls"
    )
    sub = parser.add_subparsers(dest="command", required=True)

    freeze = sub.add_parser("verify-freeze", help="verify frozen runtime and evaluator hashes")
    freeze.add_argument("--output")

    reserve = sub.add_parser("build-reserve", help="build the predeclared untouched reserve input set")
    reserve.add_argument("--candidates", required=True)
    reserve.add_argument("--old-inputs", required=True)
    reserve.add_argument("--output", required=True)

    select = sub.add_parser("select", help="merge completed annotations and select 120 accepted cases")
    select.add_argument("--candidates", required=True)
    select.add_argument("--old-inputs", required=True)
    select.add_argument("--old-report", required=True)
    select.add_argument("--old-labels", required=True)
    select.add_argument("--reserve-inputs", required=True)
    select.add_argument("--reserve-report", required=True)
    select.add_argument("--reserve-labels", required=True)
    select.add_argument("--output-dir", required=True)

    contamination = sub.add_parser("scan-contamination", help="scan runtime and artifacts for private blind data")
    contamination.add_argument("--selected-inputs", required=True)
    contamination.add_argument("--private-labels", required=True)
    contamination.add_argument("--output", required=True)
    contamination.add_argument("--artifact", action="append", default=[])

    seal = sub.add_parser("seal", help="create an immutable fail-closed RC3.1 blind package")
    seal.add_argument("--selection-dir", required=True)
    seal.add_argument("--contamination-report", required=True)
    seal.add_argument("--evaluator-identity", required=True)
    seal.add_argument("--output-dir", required=True)

    gate = sub.add_parser("release-decision", help="compute RELEASE/HOLD/REJECT/PROCESS_INVALIDATED")
    gate.add_argument("--seal-manifest", required=True)
    gate.add_argument("--contamination-report", required=True)
    gate.add_argument("--verification", required=True)
    gate.add_argument("--execution-report")
    gate.add_argument("--score-report")
    gate.add_argument("--output", required=True)

    args = parser.parse_args()
    try:
        if args.command == "verify-freeze":
            result = verify_freeze()
            if args.output:
                write_json(Path(args.output), result, overwrite=True)
        elif args.command == "build-reserve":
            result = build_reserve(
                Path(args.candidates), Path(args.old_inputs), Path(args.output)
            )
        elif args.command == "select":
            result = select_final(
                candidates_path=Path(args.candidates),
                old_inputs_path=Path(args.old_inputs),
                old_report_path=Path(args.old_report),
                old_labels_path=Path(args.old_labels),
                reserve_inputs_path=Path(args.reserve_inputs),
                reserve_report_path=Path(args.reserve_report),
                reserve_labels_path=Path(args.reserve_labels),
                output_dir=Path(args.output_dir),
            )
        elif args.command == "scan-contamination":
            result = scan_contamination(
                Path(args.selected_inputs), Path(args.private_labels),
                Path(args.output), [Path(item) for item in args.artifact],
            )
        elif args.command == "seal":
            result = seal_package(
                Path(args.selection_dir), Path(args.contamination_report),
                Path(args.evaluator_identity), Path(args.output_dir),
            )
        else:
            result = release_decision(
                seal_manifest_path=Path(args.seal_manifest),
                contamination_path=Path(args.contamination_report),
                verification_path=Path(args.verification),
                execution_path=Path(args.execution_report) if args.execution_report else None,
                score_path=Path(args.score_report) if args.score_report else None,
                output_path=Path(args.output),
            )
    except PipelineHold as exc:
        print(json.dumps({"status": "HOLD", "reason": str(exc)}, indent=2))
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


def verify_freeze(root: Path = ROOT) -> dict[str, Any]:
    freeze = load_json(root / FREEZE_PATH.relative_to(ROOT))
    runtime = runtime_manifest(root)
    evaluator = {name: sha256(root / name) for name in EVALUATOR_FILES}
    runtime_hash = digest_json(runtime)
    evaluator_hash = digest_json(evaluator)
    errors: list[str] = []
    if len(runtime) != freeze["runtime_file_count"]:
        errors.append("runtime file count drift")
    if runtime_hash != freeze["runtime_manifest_sha256"]:
        errors.append("runtime source drift")
    if evaluator_hash != freeze["evaluator_manifest_sha256"]:
        errors.append("evaluator source or rubric drift")
    tag_present = bool(git("tag", "--list", "v0.11.0", root=root))
    if tag_present:
        errors.append("unauthorized v0.11.0 tag exists")
    result = {
        "schema_version": "1.0",
        "evaluation_repair": "RC3.1",
        "runtime_manifest_sha256": runtime_hash,
        "runtime_file_count": len(runtime),
        "evaluator_manifest_sha256": evaluator_hash,
        "evaluator_file_count": len(evaluator),
        "runtime_matches_freeze": not any("runtime" in item for item in errors),
        "evaluator_matches_freeze": not any("evaluator" in item for item in errors),
        "release_tag_present": tag_present,
        "errors": errors,
        "passed": not errors,
    }
    if errors:
        raise RuntimeError("freeze boundary failed: " + "; ".join(errors))
    return result


def runtime_manifest(root: Path = ROOT) -> dict[str, str]:
    names = git("ls-files", "mind01", root=root).splitlines()
    selected = []
    for name in names:
        if not name.endswith(".py"):
            continue
        lowered = name.casefold()
        if any(token in lowered for token in ("eval", "annotation_v3", "rc2_complete_run")):
            continue
        selected.append(name)
    return {name: sha256(root / name) for name in sorted(selected)}


def build_reserve(candidates_path: Path, old_inputs_path: Path, output_path: Path) -> dict[str, Any]:
    verify_freeze()
    policy = load_json(POLICY_PATH)
    candidates_path, old_inputs_path, output_path = map(resolve, (candidates_path, old_inputs_path, output_path))
    require_hash(candidates_path, policy["candidate_source_sha256"], "candidate pool")
    require_hash(old_inputs_path, policy["old_annotated_input_sha256"], "old blind inputs")
    candidates = load_json(candidates_path)["cases"]
    old_ids = {case["case_id"] for case in load_json(old_inputs_path)["cases"]}
    interrupted_ids = {case["case_id"] for case in candidates[: policy["previously_sampled_but_unsealed_prefix_count"]]}
    eligible = [
        case for case in candidates
        if case["case_id"] not in old_ids and case["case_id"] not in interrupted_ids
    ]
    eligible.sort(key=lambda case: stable_rank("rc3.1-reserve-v1", case["case_id"]))
    reserve_cases = eligible[: policy["reserve_annotation_count"]]
    if len(reserve_cases) != policy["reserve_annotation_count"]:
        raise PipelineHold("insufficient untouched reserve candidates")
    payload = {
        "schema_version": "3.0",
        "suite": "semantic-routing-blind-rc3.1-reserve-annotation",
        "selection_policy_sha256": sha256(POLICY_PATH),
        "candidate_source_sha256": sha256(candidates_path),
        "old_input_sha256": sha256(old_inputs_path),
        "excluded_old_count": len(old_ids),
        "excluded_interrupted_count": len(interrupted_ids),
        "case_count": len(reserve_cases),
        "selection_algorithm": policy["reserve_ranking"],
        "cases": reserve_cases,
    }
    write_json(output_path, payload, overwrite=False)
    return {
        "output": str(output_path),
        "reserve_case_count": len(reserve_cases),
        "reserve_case_ids": [case["case_id"] for case in reserve_cases],
        "reserve_input_sha256": sha256(output_path),
        "selection_policy_sha256": sha256(POLICY_PATH),
    }


def select_final(
    *,
    candidates_path: Path,
    old_inputs_path: Path,
    old_report_path: Path,
    old_labels_path: Path,
    reserve_inputs_path: Path,
    reserve_report_path: Path,
    reserve_labels_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    freeze_result = verify_freeze()
    policy = load_json(POLICY_PATH)
    paths = [
        candidates_path, old_inputs_path, old_report_path, old_labels_path,
        reserve_inputs_path, reserve_report_path, reserve_labels_path,
    ]
    candidates_path, old_inputs_path, old_report_path, old_labels_path, reserve_inputs_path, reserve_report_path, reserve_labels_path = map(resolve, paths)
    output_dir = resolve(output_dir)
    ensure_new_directory(output_dir)
    require_hash(candidates_path, policy["candidate_source_sha256"], "candidate pool")
    require_hash(old_inputs_path, policy["old_annotated_input_sha256"], "old blind inputs")
    all_cases = {case["case_id"]: case for case in load_json(candidates_path)["cases"]}
    old_inputs = load_json(old_inputs_path)
    reserve_inputs = load_json(reserve_inputs_path)
    if reserve_inputs["selection_policy_sha256"] != sha256(POLICY_PATH):
        raise RuntimeError("reserve input policy hash mismatch")
    pool_ids = [case["case_id"] for case in old_inputs["cases"]] + [
        case["case_id"] for case in reserve_inputs["cases"]
    ]
    if len(pool_ids) != policy["combined_candidate_plus_reserve_count"] or len(set(pool_ids)) != len(pool_ids):
        raise RuntimeError("combined candidate-plus-reserve pool identity mismatch")
    old_states, old_annotations = annotation_evidence(old_report_path, old_labels_path, old_inputs_path)
    reserve_states, reserve_annotations = annotation_evidence(
        reserve_report_path, reserve_labels_path, reserve_inputs_path
    )
    states = {**old_states, **reserve_states}
    annotations = {**old_annotations, **reserve_annotations}
    if set(states) != set(pool_ids):
        raise RuntimeError("annotation states do not cover the complete candidate-plus-reserve pool")
    eligible_ids = eligible_case_ids(states, pool_ids)
    if len(eligible_ids) < policy["required_final_count"]:
        raise PipelineHold(policy["insufficient_accepted_action"])
    selected_ids, coverage = coverage_selection(
        eligible_ids, all_cases, annotations, policy
    )
    if len(selected_ids) != FINAL_COUNT:
        raise PipelineHold(f"coverage-constrained selector produced {len(selected_ids)} cases")
    selected_set = set(selected_ids)
    if any(states[case_id]["state"] != "accepted" for case_id in selected_ids):
        raise RuntimeError("rejected, unresolved, or errored case selected")
    public_cases = [public_input(all_cases[case_id]) for case_id in selected_ids]
    private_labels = [
        {"case_id": case_id, "annotation": annotations[case_id]}
        for case_id in selected_ids
    ]
    public_payload = {
        "schema_version": "3.1",
        "partition": "external_blind",
        "case_count": FINAL_COUNT,
        "cases": public_cases,
    }
    private_payload = {
        "schema_version": "3.1",
        "blind_set_version": "semantic-routing-blind-rc3.1",
        "labels": private_labels,
    }
    public_path = output_dir / "public_inputs.json"
    private_path = output_dir / "private_labels.json"
    write_json(public_path, public_payload, overwrite=False)
    write_json(private_path, private_payload, overwrite=False)
    accepted_annotation_hash = digest_json([
        {"case_id": case_id, "annotation": annotations[case_id]}
        for case_id in eligible_ids
    ])
    identity = {
        "schema_version": "1.0",
        "blind_set_version": "semantic-routing-blind-rc3.1",
        "selection_policy_sha256": sha256(POLICY_PATH),
        "candidate_pool_sha256": sha256(candidates_path),
        "combined_pool_case_count": len(pool_ids),
        "accepted_annotation_count": len(eligible_ids),
        "accepted_annotation_set_sha256": accepted_annotation_hash,
        "selected_case_count": FINAL_COUNT,
        "selected_case_ids": selected_ids,
        "selected_input_sha256": sha256(public_path),
        "selected_label_sha256": sha256(private_path),
        "evaluator_frozen_commit": load_json(FREEZE_PATH)["evaluator_frozen_commit"],
        "runtime_frozen_commit": load_json(FREEZE_PATH)["runtime_frozen_commit"],
        "evaluation_script_hashes": script_manifest(require_tracked=False),
        "old_blind_input_hash": policy["old_annotated_input_sha256"],
        "old_set_status": "SUPERSEDED — insufficient accepted annotations after frozen evaluation",
        "timestamp_source": "reserve annotation report generated_at",
        "created_at": load_json(reserve_report_path).get("generated_at"),
    }
    write_json(output_dir / "selected_set.json", identity, overwrite=False)
    write_json(output_dir / "coverage_report.json", coverage, overwrite=False)
    write_json(output_dir / "selection_audit.json", {
        "selection_algorithm": policy["final_ranking"],
        "selected": [
            {
                "case_id": case_id,
                "annotation_state": states[case_id]["state"],
                "rank": stable_rank("rc3.1-final-v1", case_id),
                "coverage_tokens": sorted(case_coverage(all_cases[case_id], annotations[case_id])),
            }
            for case_id in selected_ids
        ],
        "accepted_reserve_not_selected": sorted(set(eligible_ids) - selected_set),
        "ineligible": [states[case_id] for case_id in pool_ids if states[case_id]["state"] != "accepted"],
    }, overwrite=False)
    write_json(output_dir / "candidate_pool.json", {
        "candidate_source_sha256": sha256(candidates_path),
        "old_inputs_sha256": sha256(old_inputs_path),
        "reserve_inputs_sha256": sha256(reserve_inputs_path),
        "combined_case_count": len(pool_ids),
        "case_ids": pool_ids,
        "annotation_state_counts": dict(Counter(item["state"] for item in states.values())),
        "freeze": freeze_result,
    }, overwrite=False)
    write_json(output_dir / "supersession.json", {
        "schema_version": "1.0",
        "old_status": "SUPERSEDED — insufficient accepted annotations after frozen evaluation",
        "old_set_hash": policy["old_annotated_input_sha256"],
        "old_set_size": 120,
        "old_accepted": 117,
        "old_rejected": 3,
        "reason": "preselection left no reserve after three frozen-evaluator rejections",
        "successor_set_hash": identity["selected_input_sha256"],
        "successor_identity": "semantic-routing-blind-rc3.1",
    }, overwrite=False)
    return identity


def annotation_evidence(
    report_path: Path, labels_path: Path, inputs_path: Path
) -> tuple[dict[str, dict[str, Any]], dict[str, dict[str, Any]]]:
    report = load_json(report_path)
    labels = load_json(labels_path)
    inputs = load_json(inputs_path)
    if not report.get("complete"):
        raise RuntimeError(f"annotation report incomplete: {report_path}")
    if report["source"]["sha256"] != sha256(inputs_path):
        raise RuntimeError(f"annotation source hash mismatch: {report_path}")
    input_ids = [case["case_id"] for case in inputs["cases"]]
    records = {record["case_id"]: record for record in report["records"]}
    annotations = {item["case_id"]: item["annotation"] for item in labels["labels"]}
    if set(records) != set(input_ids):
        raise RuntimeError("annotation report does not cover every input case")
    states: dict[str, dict[str, Any]] = {}
    for case_id in input_ids:
        record = records[case_id]
        if record["accepted"]:
            if case_id not in annotations:
                raise RuntimeError(f"accepted case {case_id} has no private label")
            state = "accepted"
        elif record.get("adjudication_errors"):
            state = "rejected"
        else:
            state = "unresolved"
        states[case_id] = {
            "case_id": case_id,
            "state": state,
            "resolution": record.get("resolution"),
            "reasons": record.get("adjudication_errors", []),
            "report_sha256": sha256(report_path),
        }
    return states, annotations


def eligible_case_ids(
    states: Mapping[str, Mapping[str, Any]], case_ids: Iterable[str]
) -> list[str]:
    return sorted(
        (case_id for case_id in case_ids if states[case_id]["state"] == "accepted"),
        key=lambda case_id: stable_rank("rc3.1-final-v1", case_id),
    )


def coverage_selection(
    eligible_ids: list[str],
    cases: Mapping[str, dict[str, Any]],
    annotations: Mapping[str, dict[str, Any]],
    policy: Mapping[str, Any],
) -> tuple[list[str], dict[str, Any]]:
    eligible_ids = sorted(
        eligible_ids,
        key=lambda case_id: stable_rank("rc3.1-final-v1", case_id),
    )
    requirements = required_coverage_tokens(policy)
    token_map = {
        case_id: case_coverage(cases[case_id], annotations[case_id])
        for case_id in eligible_ids
    }
    selected: list[str] = []
    selected_set: set[str] = set()
    lifecycle_counts: Counter[str] = Counter()
    uncovered = set(requirements)
    while uncovered:
        choices = []
        for case_id in eligible_ids:
            if case_id in selected_set:
                continue
            signature = lifecycle_signature(annotations[case_id])
            if lifecycle_counts[signature] >= FINAL_COUNT // 10:
                continue
            gain = len(token_map[case_id] & uncovered)
            if gain:
                choices.append((-gain, stable_rank("rc3.1-final-v1", case_id), case_id))
        if not choices:
            raise PipelineHold("accepted candidate pool cannot satisfy coverage: " + ", ".join(sorted(uncovered)))
        _, _, case_id = min(choices)
        selected.append(case_id)
        selected_set.add(case_id)
        lifecycle_counts[lifecycle_signature(annotations[case_id])] += 1
        uncovered -= token_map[case_id]
    groups: dict[str, deque[str]] = defaultdict(deque)
    for case_id in eligible_ids:
        if case_id not in selected_set:
            groups[cases[case_id]["authoring_metadata"]["archetype"]].append(case_id)
    order = deque(sorted(groups))
    stalled = 0
    while len(selected) < FINAL_COUNT and order:
        group = order.popleft()
        queue = groups[group]
        picked = False
        while queue:
            case_id = queue.popleft()
            signature = lifecycle_signature(annotations[case_id])
            if lifecycle_counts[signature] < FINAL_COUNT // 10:
                selected.append(case_id)
                selected_set.add(case_id)
                lifecycle_counts[signature] += 1
                picked = True
                break
        if queue:
            order.append(group)
        if picked:
            stalled = 0
        else:
            stalled += 1
            if stalled > len(order) + 1:
                break
    observed = set().union(*(token_map[case_id] for case_id in selected)) if selected else set()
    missing = sorted(requirements - observed)
    maximum_share = max(lifecycle_counts.values(), default=0) / FINAL_COUNT
    report = {
        "passed": len(selected) == FINAL_COUNT and not missing and maximum_share <= 0.10,
        "required_tokens": sorted(requirements),
        "observed_tokens": sorted(observed),
        "missing_tokens": missing,
        "selected_count": len(selected),
        "maximum_identical_lifecycle_signature_share": maximum_share,
        "lifecycle_signature_counts": dict(sorted(lifecycle_counts.items())),
        "language_counts": {"English": len(selected)},
    }
    if not report["passed"]:
        raise PipelineHold("final selection coverage failed")
    return selected, report


def required_coverage_tokens(policy: Mapping[str, Any]) -> set[str]:
    coverage = policy["coverage"]
    tokens = {f"public:{item}" for item in coverage["public_categories_required"]}
    tokens |= {f"task:{item}" for item in coverage["task_classes_required"]}
    tokens |= {f"family:{item}" for item in coverage["immediate_families_required"]}
    tokens |= {f"tool:{item}" for item in coverage["immediate_tools_required"]}
    tokens |= {f"response:{item}" for item in coverage["response_modes_required"]}
    tokens |= {f"lifecycle:{item}" for item in coverage["lifecycle_requirements"]}
    return tokens


def case_coverage(case: Mapping[str, Any], annotation: Mapping[str, Any]) -> set[str]:
    tokens = {f"task:{annotation['task_class']}", f"family:{annotation['immediate_tool_family']}", f"response:{annotation['response_mode']}"}
    tokens |= {f"tool:{tool}" for tool in annotation["allowed_immediate_tools"]}
    tokens |= {f"public:{item}" for item in public_categories(case)}
    lifecycle = annotation["required_lifecycle"]
    if annotation["response_mode"] != "action" or not lifecycle:
        tokens.add("lifecycle:no_tool")
    if len(lifecycle) == 1:
        tokens.add("lifecycle:single_action")
    if len(lifecycle) >= 2:
        tokens.add("lifecycle:multi_step")
    if annotation["terminal_mutation_expected"]:
        tokens.add("lifecycle:terminal_mutation")
    if case.get("authoring_metadata", {}).get("fixture_kind") == "rollback":
        tokens.add("lifecycle:rollback_fixture")
    return tokens


def public_categories(case: Mapping[str, Any]) -> set[str]:
    metadata = case.get("authoring_metadata", {})
    archetype = str(metadata.get("archetype", ""))
    facts = case["public_facts"]
    categories: set[str] = set()
    mapping = {
        "repository_discovery": {"repository-map", "repository-list", "alternative-discovery", "resolvable-ambiguity"},
        "direct_inspection": {"direct-file", "dependency-inspection"},
        "symbol_lookup": {"symbol-definition", "symbol-callers", "locate-then-read"},
        "documentation": {"documentation-search", "knowledge-query"},
        "proposal": {"proposal-existing", "proposal-existing-crosscheck", "proposal-new", "inspect-before-proposal"},
        "mutation": {"approved-edit", "rollback-edit", "approved-replacement", "approved-creation", "inspect-before-mutation"},
    }
    for category, archetypes in mapping.items():
        if archetype in archetypes:
            categories.add(category)
    if facts["requested_operation"] in {"run_tests", "compile", "shell"} and not facts["unsafe_operation"]:
        categories.add("verification")
    if archetype == "readonly-mutation": categories.add("read_only_block")
    if archetype == "missing-shell": categories.add("missing_capability")
    if facts["target_state"] == "exists_multiple": categories.add("ambiguity")
    if facts["unsafe_operation"]: categories.add("unsafe")
    if facts["unsupported_operation"]: categories.add("unsupported")
    if facts["self_contained"]: categories.add("final_answer")
    if facts["route_state"] != "none": categories.add("stale_route")
    if facts["prompt_injection"]: categories.add("prompt_injection")
    if metadata.get("fixture_kind") == "rollback": categories.add("rollback")
    return categories


def scan_contamination(
    selected_inputs_path: Path,
    private_labels_path: Path,
    output_path: Path,
    artifacts: list[Path] | None = None,
) -> dict[str, Any]:
    freeze = verify_freeze()
    selected_inputs_path = resolve(selected_inputs_path)
    private_labels_path = resolve(private_labels_path)
    output_path = resolve(output_path)
    inputs = load_json(selected_inputs_path)
    labels = load_json(private_labels_path)
    case_ids = [case["case_id"] for case in inputs["cases"]]
    if {item["case_id"] for item in labels["labels"]} != set(case_ids):
        raise RuntimeError("private label IDs do not match selected public inputs")
    blocking: list[dict[str, Any]] = []
    allowed: list[dict[str, Any]] = []
    tracked = git("ls-files", root=ROOT).splitlines()
    for name in tracked:
        path = ROOT / name
        if not path.is_file():
            continue
        data = path.read_bytes()
        found_ids = [case_id for case_id in case_ids if case_id.encode() in data]
        if not found_ids:
            continue
        finding = {"path": name, "case_ids": found_ids[:10], "count": len(found_ids)}
        if evaluation_only_path(name):
            allowed.append(finding)
        else:
            blocking.append({**finding, "reason": "blind case ID in runtime-visible tracked file"})
    private_bytes = private_labels_path.read_bytes()
    private_hash = hashlib.sha256(private_bytes).hexdigest()
    private_fragments = private_label_fragments(labels)
    for name in tracked:
        path = ROOT / name
        if not path.is_file() or evaluation_only_path(name):
            continue
        data = path.read_bytes()
        fragment_hits = [digest for digest, fragment in private_fragments if fragment in data]
        if private_bytes in data or private_hash.encode() in data or fragment_hits:
            blocking.append({
                "path": name,
                "reason": "private blind annotation content in runtime-visible tracked file",
                "annotation_fragment_hashes": fragment_hits[:10],
            })
    artifact_reports = []
    for artifact in artifacts or []:
        artifact = resolve(artifact)
        report = scan_artifact(
            artifact, private_bytes, private_hash, case_ids, private_fragments
        )
        artifact_reports.append(report)
        blocking.extend(report["blocking_findings"])
    changed = git("diff", "--name-only", load_json(FREEZE_PATH)["runtime_frozen_commit"], "--", root=ROOT).splitlines()
    frozen_changes = [
        name for name in changed
        if name in EVALUATOR_FILES or name in runtime_manifest(ROOT)
    ]
    if frozen_changes:
        blocking.append({"reason": "frozen source changed since freeze", "paths": frozen_changes})
    report = {
        "schema_version": "1.0",
        "selected_inputs_sha256": sha256(selected_inputs_path),
        "private_labels_sha256": private_hash,
        "selected_case_count": len(case_ids),
        "tracked_file_count_scanned": len(tracked),
        "git_diff_since_freeze": changed,
        "allowed_evaluation_only_references": allowed,
        "artifact_reports": artifact_reports,
        "freeze": freeze,
        "contamination_findings_blocking": len(blocking),
        "blocking_findings": blocking,
        "passed": not blocking,
    }
    write_json(output_path, report, overwrite=True)
    return report


def scan_artifact(
    path: Path,
    private_bytes: bytes,
    private_hash: str,
    case_ids: list[str],
    private_fragments: list[tuple[str, bytes]] | None = None,
) -> dict[str, Any]:
    findings: list[dict[str, Any]] = []
    members = 0
    def inspect_member(name: str, data: bytes) -> None:
        if private_bytes in data or private_hash.encode() in data:
            findings.append({"artifact": str(path), "member": name, "reason": "private labels embedded"})
        found_ids = [case_id for case_id in case_ids if case_id.encode() in data]
        if found_ids:
            findings.append({
                "artifact": str(path), "member": name,
                "reason": "blind case IDs embedded", "case_ids": found_ids[:10],
            })
        fragment_hits = [
            digest for digest, fragment in (private_fragments or []) if fragment in data
        ]
        if fragment_hits:
            findings.append({
                "artifact": str(path), "member": name,
                "reason": "private annotation fragments embedded",
                "annotation_fragment_hashes": fragment_hits[:10],
            })
        if "private_label" in name.casefold() or name.casefold().endswith("labels.json"):
            findings.append({"artifact": str(path), "member": name, "reason": "private label filename packaged"})
    if zipfile.is_zipfile(path):
        with zipfile.ZipFile(path) as archive:
            for name in archive.namelist():
                if name.endswith("/"):
                    continue
                members += 1
                inspect_member(name, archive.read(name))
    elif tarfile.is_tarfile(path):
        with tarfile.open(path, "r:*") as archive:
            for member in archive.getmembers():
                if not member.isfile():
                    continue
                extracted = archive.extractfile(member)
                if extracted is None:
                    continue
                members += 1
                inspect_member(member.name, extracted.read())
    else:
        data = path.read_bytes()
        members = 1
        if private_bytes in data or private_hash.encode() in data:
            findings.append({"artifact": str(path), "reason": "private labels embedded"})
        found_ids = [case_id for case_id in case_ids if case_id.encode() in data]
        if found_ids:
            findings.append({
                "artifact": str(path), "reason": "blind case IDs embedded",
                "case_ids": found_ids[:10],
            })
    return {
        "artifact": str(path),
        "sha256": sha256(path),
        "members_scanned": members,
        "blocking_findings": findings,
        "passed": not findings,
    }


def private_label_fragments(labels: Mapping[str, Any]) -> list[tuple[str, bytes]]:
    fragments: list[tuple[str, bytes]] = []
    for item in labels["labels"]:
        canonical = json.dumps(
            item["annotation"], sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
        if len(canonical) < 32:
            continue
        fragments.append((hashlib.sha256(canonical).hexdigest(), canonical))
    return fragments


def seal_package(
    selection_dir: Path,
    contamination_path: Path,
    evaluator_identity_path: Path,
    output_dir: Path,
) -> dict[str, Any]:
    freeze = verify_freeze()
    selection_dir, contamination_path, evaluator_identity_path, output_dir = map(
        resolve, (selection_dir, contamination_path, evaluator_identity_path, output_dir)
    )
    ensure_new_directory(output_dir)
    selected = load_json(selection_dir / "selected_set.json")
    coverage = load_json(selection_dir / "coverage_report.json")
    pool = load_json(selection_dir / "candidate_pool.json")
    contamination = load_json(contamination_path)
    evaluator = load_json(evaluator_identity_path)
    inputs = load_json(selection_dir / "public_inputs.json")
    labels = load_json(selection_dir / "private_labels.json")
    if selected["selection_policy_sha256"] != sha256(POLICY_PATH):
        raise RuntimeError("selection policy drift")
    if selected["candidate_pool_sha256"] != load_json(POLICY_PATH)["candidate_source_sha256"]:
        raise RuntimeError("candidate-pool drift")
    if selected["selected_case_count"] != FINAL_COUNT or inputs["case_count"] != FINAL_COUNT:
        raise RuntimeError("seal requires exactly 120 selected public inputs")
    if selected["selected_input_sha256"] != sha256(selection_dir / "public_inputs.json"):
        raise RuntimeError("selected public-input hash drift")
    if selected["selected_label_sha256"] != sha256(selection_dir / "private_labels.json"):
        raise RuntimeError("selected private-label hash drift")
    ordered_input_ids = [case["case_id"] for case in inputs["cases"]]
    if ordered_input_ids != selected["selected_case_ids"]:
        raise RuntimeError("selected case order or identity drift")
    label_ids = {item["case_id"] for item in labels["labels"]}
    input_ids = {case["case_id"] for case in inputs["cases"]}
    if len(label_ids) != FINAL_COUNT or label_ids != input_ids:
        raise RuntimeError("seal requires one accepted private label for every selected input")
    if not coverage["passed"]:
        raise RuntimeError("selection coverage failed")
    if contamination["contamination_findings_blocking"] != 0 or not contamination["passed"]:
        raise RuntimeError("contamination gate failed")
    if contamination["selected_inputs_sha256"] != selected["selected_input_sha256"]:
        raise RuntimeError("contamination report covers different public inputs")
    if contamination["private_labels_sha256"] != selected["selected_label_sha256"]:
        raise RuntimeError("contamination report covers different private labels")
    if evaluator["source_commit"] != load_json(FREEZE_PATH)["evaluator_frozen_commit"]:
        raise RuntimeError("evaluator identity commit drift")
    if sha256(evaluator_identity_path) != load_json(FREEZE_PATH)["evaluator_identity_sha256"]:
        raise RuntimeError("evaluator identity hash drift")
    scripts = script_manifest(require_tracked=True)
    if selected["evaluation_script_hashes"] != scripts:
        raise RuntimeError("evaluation scripts changed after final selection")
    audit = load_json(selection_dir / "selection_audit.json")
    if len(audit["selected"]) != FINAL_COUNT or any(
        item["annotation_state"] != "accepted" for item in audit["selected"]
    ):
        raise RuntimeError("seal requires 120 accepted annotation states")
    public_dir = output_dir / "public_inputs"
    private_dir = output_dir / "private_labels"
    manifests_dir = output_dir / "manifests"
    public_dir.mkdir(parents=True)
    private_dir.mkdir(parents=True)
    manifests_dir.mkdir(parents=True)
    shutil.copy2(selection_dir / "public_inputs.json", public_dir / "inputs.json")
    shutil.copy2(selection_dir / "private_labels.json", private_dir / "labels.json")
    os.chmod(private_dir / "labels.json", stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    manifest_sources = {
        "evaluator_identity.json": evaluator_identity_path,
        "runtime_freeze.json": FREEZE_PATH,
        "candidate_pool.json": selection_dir / "candidate_pool.json",
        "selection_policy.json": POLICY_PATH,
        "selected_set.json": selection_dir / "selected_set.json",
        "coverage_report.json": selection_dir / "coverage_report.json",
        "selection_audit.json": selection_dir / "selection_audit.json",
        "supersession.json": selection_dir / "supersession.json",
        "contamination_report.json": contamination_path,
    }
    for name, source in manifest_sources.items():
        shutil.copy2(source, manifests_dir / name)
    hashes = tree_manifest(output_dir)
    write_json(output_dir / "hashes.json", hashes, overwrite=False)
    content_hash = digest_json(hashes)
    seal_manifest = {
        "schema_version": "1.0",
        "seal_version": "semantic-routing-blind-rc3.1",
        "sealed_package_valid": True,
        "public_input_sha256": sha256(public_dir / "inputs.json"),
        "private_label_sha256": sha256(private_dir / "labels.json"),
        "selection_policy_sha256": sha256(POLICY_PATH),
        "candidate_pool_sha256": selected["candidate_pool_sha256"],
        "evaluator_identity_sha256": sha256(evaluator_identity_path),
        "runtime_manifest_sha256": freeze["runtime_manifest_sha256"],
        "evaluation_script_hashes": scripts,
        "contamination_report_sha256": sha256(contamination_path),
        "package_content_sha256": content_hash,
        "selected_case_count": FINAL_COUNT,
        "private_labels_runtime_visible": False,
    }
    write_json(manifests_dir / "seal_manifest.json", seal_manifest, overwrite=False)
    return seal_manifest


def release_decision(
    *,
    seal_manifest_path: Path,
    contamination_path: Path,
    verification_path: Path,
    execution_path: Path | None,
    score_path: Path | None,
    output_path: Path,
) -> dict[str, Any]:
    try:
        freeze = verify_freeze()
    except RuntimeError as exc:
        decision = "PROCESS_INVALIDATED"
        reasons = [str(exc)]
        freeze = {"passed": False}
    else:
        seal = load_json(resolve(seal_manifest_path))
        contamination = load_json(resolve(contamination_path))
        verification = load_json(resolve(verification_path))
        reasons = []
        if not seal.get("sealed_package_valid"):
            reasons.append("sealed package invalid")
        if contamination.get("contamination_findings_blocking") != 0:
            reasons.append("blocking contamination finding")
        if not verification.get("canonical_tests_pass"):
            reasons.append("canonical tests failed")
        if not verification.get("package_hygiene_pass"):
            reasons.append("package hygiene failed")
        if not execution_path or not score_path:
            reasons.append("sealed execution and scoring pending")
            decision = "HOLD"
        else:
            execution = load_json(resolve(execution_path))
            score = load_json(resolve(score_path))
            if execution.get("completed_case_count") != FINAL_COUNT:
                reasons.append("not all 120 runtime cases completed")
            for key in ("unauthorized_mutations", "unsafe_actions"):
                if execution.get(key) != 0:
                    reasons.append(f"{key} is nonzero")
            if not score.get("frozen_thresholds_available"):
                reasons.append("release thresholds were not predeclared")
            summary = score.get("summary", {})
            if summary.get("false_success_rate") is None:
                reasons.append("false-success rate is unavailable under the selection-only protocol")
            if reasons:
                decision = "HOLD"
            else:
                decision = "RELEASE" if score.get("all_frozen_gates_passed") else "REJECT"
    result = {
        "schema_version": "1.0",
        "decision": decision,
        "reasons": reasons,
        "freeze": freeze,
        "v0.11.0_tag_created": False,
    }
    write_json(resolve(output_path), result, overwrite=True)
    return result


def script_manifest(*, require_tracked: bool) -> dict[str, str]:
    tracked = set(git("ls-files", root=ROOT).splitlines())
    missing = [name for name in EVALUATION_SCRIPTS if name not in tracked]
    if require_tracked and missing:
        raise RuntimeError("untracked evaluation scripts block sealing: " + ", ".join(missing))
    return {
        name: sha256(ROOT / name)
        for name in EVALUATION_SCRIPTS
        if (ROOT / name).is_file()
    }


def lifecycle_signature(annotation: Mapping[str, Any]) -> str:
    return digest_json({
        "response_mode": annotation["response_mode"],
        "reason_code": annotation["reason_code"],
        "required": annotation["required_lifecycle"],
        "alternatives": annotation["allowed_alternative_lifecycles"],
        "terminal_family": annotation["terminal_tool_family"],
    })[:16]


def public_input(case: Mapping[str, Any]) -> dict[str, Any]:
    return {
        key: case[key]
        for key in (
            "case_id", "partition", "prompt", "workspace_fixture",
            "agent_mode", "capabilities", "public_facts",
        )
    }


def evaluation_only_path(name: str) -> bool:
    return name.startswith(("scripts/", "evaluation_governance/")) or name in {
        "tests/test_rc3_1_pipeline.py",
    }


def tree_manifest(root: Path) -> dict[str, str]:
    return {
        str(path.relative_to(root)): sha256(path)
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def stable_rank(salt: str, case_id: str) -> str:
    return hashlib.sha256(f"{salt}:{case_id}".encode()).hexdigest()


def require_hash(path: Path, expected: str, label: str) -> None:
    actual = sha256(path)
    if actual != expected:
        raise RuntimeError(f"{label} hash mismatch: {actual} != {expected}")


def ensure_new_directory(path: Path) -> None:
    if path.exists():
        if any(path.iterdir()):
            raise FileExistsError(f"refusing to overwrite existing output: {path}")
    else:
        path.mkdir(parents=True)


def write_json(path: Path, value: Any, *, overwrite: bool) -> None:
    path = resolve(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"refusing to overwrite existing file: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def load_json(path: Path) -> dict[str, Any]:
    path = resolve(path)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(resolve(path).read_bytes()).hexdigest()


def digest_json(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
    ).hexdigest()


def resolve(path: Path) -> Path:
    return path if path.is_absolute() else (ROOT / path).resolve()


def git(*args: str, root: Path = ROOT) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


if __name__ == "__main__":
    raise SystemExit(main())
