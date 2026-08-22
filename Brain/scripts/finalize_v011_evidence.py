from __future__ import annotations

import argparse
import hashlib
import json
import platform
import statistics
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mind01.prompts import SYSTEM_PROMPT
from mind01.semantic_eval import load_partition, run_deterministic_semantic_routing, validate_semantic_routing_assets
from mind01.version import __version__


RUN_DIRECTORIES = {
    "development": "development_runs",
    "regression": "regression_runs",
    "adversarial": "adversarial_runs",
    "capability_mode": "capability_mode_runs",
    "ambiguity": "ambiguity_runs",
    "blind": "blind_runs",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    return payload if isinstance(payload, dict) else None


def git_text(*args: str) -> str | None:
    completed = subprocess.run(
        ["git", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        timeout=10,
    )
    return completed.stdout.strip() if completed.returncode == 0 else None


def derive_live_metrics(payload: dict[str, Any], partition: str) -> dict[str, Any]:
    results = payload.get("results")
    if not isinstance(results, list) or not results:
        return {}
    input_cases = {item["case_id"]: item for item in load_partition(partition)}
    total = len(results)
    invalid_argument_codes = {"MISSING_ARGUMENT", "WRONG_ARGUMENT_TYPE", "EXTRA_ARGUMENT"}
    wrong_mode_codes = {"WRONG_RESPONSE_MODE", "ACTION_REQUIRED", "FINAL_NOT_ALLOWED"}

    def incident_codes(item: dict[str, Any]) -> set[str]:
        return {
            str(incident.get("error_code"))
            for incident in item.get("parser_incidents", [])
            if isinstance(incident, dict)
        }

    exact = 0
    hidden = 0
    unnecessary_invocation = 0
    model_calls = 0
    repairs = 0
    by_mode: dict[str, dict[str, int]] = {}
    by_task: dict[str, dict[str, int]] = {}
    for item in results:
        expected = item.get("expected", {})
        expected_tools = expected.get("allowed_exact_tools", [])
        actual_tool = item.get("actual_tool") or ""
        expected_type = item.get("expected_response_type")
        if expected_type == "final":
            exact += int(item.get("actual_response_type") == "final")
            unnecessary_invocation += int(bool(actual_tool))
        elif expected_tools:
            exact += int(actual_tool == expected_tools[0])
        hidden += int(bool(actual_tool) and actual_tool not in item.get("visible_tools", []))
        calls = len(item.get("raw_outputs", []))
        model_calls += calls
        repairs += max(0, calls - 1)
        case_input = input_cases.get(str(item.get("case_id")), {})
        mode = str(case_input.get("agent_mode", "unknown"))
        task = str(expected.get("task_class", "unknown"))
        for grouping, key in ((by_mode, mode), (by_task, task)):
            record = grouping.setdefault(key, {"cases": 0, "allowed_action_correct": 0})
            record["cases"] += 1
            record["allowed_action_correct"] += int(bool(item.get("model_action_correct")))
    return {
        "definition": "derived from retained per-case output without replacing original run metrics",
        "exact_tool_or_final_accuracy": exact / total,
        "unknown_tool_incident_rate": sum("UNKNOWN_TOOL" in incident_codes(item) for item in results) / total,
        "hidden_tool_selection_rate": hidden / total,
        "wrong_response_mode_incident_rate": sum(bool(incident_codes(item) & wrong_mode_codes) for item in results) / total,
        "invalid_argument_incident_rate": sum(bool(incident_codes(item) & invalid_argument_codes) for item in results) / total,
        "strict_unnecessary_tool_invocation_rate": unnecessary_invocation / total,
        "average_model_calls_per_case": model_calls / total,
        "repair_count": repairs,
        "performance_by_mode": {
            key: {**value, "allowed_action_accuracy": value["allowed_action_correct"] / value["cases"]}
            for key, value in sorted(by_mode.items())
        },
        "performance_by_task_class": {
            key: {**value, "allowed_action_accuracy": value["allowed_action_correct"] / value["cases"]}
            for key, value in sorted(by_task.items())
        },
    }


def retained_runs(output: Path) -> dict[str, list[dict[str, Any]]]:
    collected: dict[str, list[dict[str, Any]]] = {}
    for partition, directory in RUN_DIRECTORIES.items():
        run_dir = output / directory
        run_dir.mkdir(parents=True, exist_ok=True)
        reports: list[dict[str, Any]] = []
        for path in sorted(run_dir.glob("run-*.json")):
            payload = read_json(path)
            if payload is None:
                continue
            reports.append(
                {
                    "path": str(path.relative_to(output)),
                    "sha256": sha256_file(path),
                    "complete": bool(payload.get("complete")),
                    "agent_version": payload.get("agent_version"),
                    "seed": payload.get("seed"),
                    "model": payload.get("model"),
                    "summary": payload.get("summary", {}),
                    "derived_metrics": derive_live_metrics(payload, partition),
                }
            )
        collected[partition] = reports
    return collected


def aggregate(runs: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    fields = (
        "first_attempt_structural_validity",
        "validity_after_repairs",
        "terminal_parser_failure_rate",
        "model_allowed_action_accuracy",
        "forbidden_tool_selection_rate",
        "unauthorized_selection_rate",
    )
    result: dict[str, Any] = {}
    for partition, reports in runs.items():
        complete = [item for item in reports if item["complete"]]
        metrics: dict[str, Any] = {
            "retained_runs": len(reports),
            "complete_partition_runs": len(complete),
        }
        for field in fields:
            values = [
                float(item["summary"][field])
                for item in complete
                if isinstance(item.get("summary"), dict) and field in item["summary"]
            ]
            if values:
                metrics[field] = {
                    "mean": statistics.fmean(values),
                    "minimum": min(values),
                    "maximum": max(values),
                    "population_standard_deviation": statistics.pstdev(values),
                }
        result[partition] = metrics
    return result


def artifact_identity(output: Path) -> list[dict[str, Any]]:
    artifacts = output / "artifacts"
    artifacts.mkdir(exist_ok=True)
    return [
        {
            "path": str(path.relative_to(output)),
            "sha256": sha256_file(path),
            "size_bytes": path.stat().st_size,
        }
        for path in sorted(artifacts.iterdir())
        if path.is_file()
    ]


def render_failure_analysis(deterministic: dict[str, Any], runs: dict[str, list[dict[str, Any]]]) -> str:
    failures = deterministic.get("failure_taxonomy", {})
    lines = [
        "# v0.11 candidate failure analysis",
        "",
        "## Deterministic labels",
        "",
        f"The frozen labeled partitions pass {deterministic['passed']}/{deterministic['total']} complete route checks. "
        f"Failure taxonomy: `{json.dumps(failures, sort_keys=True)}`.",
        "",
        "The 16 mutation-intent failures come from contradictory labels in the frozen adversarial generator: repeated attack archetypes are semantically identical but their mutation label changes with absolute case index. The files and hashes are retained unchanged; correcting this requires a new dataset version frozen before future routing changes.",
        "",
        "## Development live model",
        "",
    ]
    for run in runs.get("development", []):
        summary = run.get("summary", {})
        lines.append(
            f"- `{run['path']}`: {summary.get('case_count', 0)} cases; first structural validity "
            f"{summary.get('first_attempt_structural_validity')}; terminal parser failure "
            f"{summary.get('terminal_parser_failure_rate')}; allowed action "
            f"{summary.get('model_allowed_action_accuracy')}."
        )
    lines.extend(
        [
            "",
            "The initial run's two failures were existing-file proposals with no inspected source. The model repeated empty required `old` and `new` fields through all bounded attempts. The candidate now exposes only `read_file` before the eventual proposal tool. Frozen labels still name the eventual proposal action, so label-relative exact-action and exposure metrics retain that lifecycle mismatch.",
            "",
            "## Blind integrity and release blockers",
            "",
            "No external blind label package or independently controlled evaluator was provided. In addition, the repository blind-input generator selects prompts from visible labeled archetypes, making their semantic expectations derivable even though expected fields are omitted. Those inputs cannot establish independent blind performance in this development process.",
            "",
            "No tool is dispatched by `semantic-live`. Selection and parser safety are measured; zero execution counters are not execution-safety evidence. Host command execution in the real agent remains controlled but is not sandboxed.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_release_report(manifest: dict[str, Any]) -> str:
    deterministic = manifest["deterministic"]
    development = manifest["live_runs"]["development"]
    return f"""# Mind1.1 v0.11.0 candidate release report

Release gate: **FAILED/BLOCKED**

This is version `{manifest['agent_version']}`, not a stable v0.11.0 release. No release tag is authorized.

## Architecture

The candidate adds a strict normalized intent, five-stage hierarchical deterministic routing, finite specialists/tool families/reason codes, capability-bound route identity, explicit ambiguity, and one lifecycle-scoped tool-exposure authority. Parser, policy, execution, verification, and completion remain separate authorities.

## Deterministic evidence

- Labeled route checks: {deterministic['passed']}/{deterministic['total']}
- First structural validity: {deterministic['metrics']['first_attempt_structural_validity']}
- Task class / specialist / tool family: {deterministic['metrics']['task_class_accuracy']} / {deterministic['metrics']['specialist_accuracy']} / {deterministic['metrics']['tool_family_accuracy']}
- Mutation intent: {deterministic['metrics']['mutation_intent_accuracy']}
- Frozen failures: {deterministic['failure_count']}

## Live development evidence

Retained complete development runs: {development['complete_partition_runs']}. These are development-tuning runs, not independent blind runs. See each retained JSON report for raw per-case outputs.

## Gate blockers

- No independently controlled external blind labels/evaluator.
- Repository blind inputs are derived from visible archetypes and cannot prove independent blind performance.
- Zero complete end-to-end live runs including blind evaluation; at least three are required.
- Mandatory blind accuracy metrics are unavailable.
- Frozen adversarial labels contain 16 contradictory mutation-intent expectations.
- Semantic live runs select actions but do not execute tools.

## Safety boundary

No forbidden or unauthorized selection was observed in retained labeled runs. Execution safety cannot be inferred from a no-dispatch harness. v0.10 false-success, receipts, rollback, and policy tests remain mandatory deterministic checks. Host-executed verification is controlled but not sandboxed.

## Decision

Do not publish or tag v0.11.0 and do not begin or claim v0.12. Create a newly frozen, independently authored blind package and corrected dataset version before a future release candidate.
"""


def main() -> int:
    parser = argparse.ArgumentParser(description="Finalize honest v0.11 candidate evidence.")
    parser.add_argument("--output-dir", default="evaluation_results/v0.11.0-release")
    args = parser.parse_args()
    output = (ROOT / args.output_dir).resolve() if not Path(args.output_dir).is_absolute() else Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)

    validation = validate_semantic_routing_assets()
    deterministic = run_deterministic_semantic_routing()
    write_json(output / "deterministic_tests.json", deterministic)
    write_json(output / "dataset_hashes.json", validation)
    write_json(
        output / "prompt_hashes.json",
        {
            "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest(),
            "prompts_py_sha256": sha256_file(ROOT / "mind01" / "prompts.py"),
        },
    )
    write_json(
        output / "schema_hashes.json",
        {
            name: sha256_file(ROOT / relative)
            for name, relative in {
                "action_parser": Path("mind01/action_parser.py"),
                "tool_schemas": Path("mind01/tools/schemas.py"),
                "intent_schema": Path("mind01/intent.py"),
                "routing_schema": Path("mind01/routing.py"),
                "dataset_schema": Path("mind01/eval_suites/semantic_routing_v1/schema.json"),
            }.items()
        },
    )
    confusion_dir = output / "confusion_matrices"
    confusion_dir.mkdir(exist_ok=True)
    for name, matrix in deterministic.get("confusion_matrices", {}).items():
        write_json(confusion_dir / f"{name}.json", matrix)

    runs = retained_runs(output)
    aggregates = aggregate(runs)
    blind_blocker = {
        "status": "blocked",
        "reason": "No independently controlled external blind labels or evaluator were supplied.",
        "blind_inputs_sha256": validation["partition_hashes"]["blind_inputs.json"],
        "labels_exposed_during_tuning": False,
        "independence_warning": "Input archetypes are visible in the repository generator and cannot prove independent blind performance.",
    }
    write_json(output / "blind_runs" / "blocked.json", blind_blocker)
    environment = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "agent_version": __version__,
        "git_commit": git_text("rev-parse", "HEAD"),
        "git_tree": git_text("rev-parse", "HEAD^{tree}"),
        "git_branch": git_text("branch", "--show-current"),
        "retained_model_metadata": next(
            (run.get("model") for run in runs.get("development", []) if run.get("model")),
            None,
        ),
    }
    write_json(output / "environment.json", environment)

    gates = {
        "release_gate_passed": False,
        "status": "failed_blocked",
        "external_blind_evaluator_available": False,
        "blind_metrics_available": False,
        "complete_end_to_end_live_runs": 0,
        "required_complete_end_to_end_live_runs": 3,
        "blind_labels_exposed_during_tuning": False,
        "stable_release_tag_authorized": False,
    }
    artifacts = artifact_identity(output)
    evidence_files = {
        name: {
            "path": name,
            "sha256": sha256_file(output / name),
        }
        for name in (
            "commands.json",
            "dataset_hashes.json",
            "deterministic_tests.json",
            "environment.json",
            "prompt_hashes.json",
            "schema_hashes.json",
        )
        if (output / name).is_file()
    }
    manifest = {
        "schema_version": "1.0",
        "release_target": "0.11.0",
        "agent_version": __version__,
        "generated_at": environment["generated_at"],
        "source_candidate_commit": "812c510f5cfe4f26c46e923435ae89bd6f1229bb",
        "evidence_generation_commit": environment["git_commit"],
        "status": "failed_blocked",
        "gates": gates,
        "dataset_identity": validation,
        "deterministic": {
            key: deterministic[key]
            for key in ("passed", "total", "metrics", "failure_count", "failure_taxonomy")
        },
        "live_runs": aggregates,
        "retained_runs": runs,
        "artifacts": artifacts,
        "evidence_files": evidence_files,
        "known_limitations": [
            blind_blocker["reason"],
            blind_blocker["independence_warning"],
            "Frozen adversarial mutation-intent labels contain 16 contradictions.",
            "Semantic live evaluation does not execute selected tools.",
            "Host-executed commands are controlled but not sandboxed.",
            "The 7B local model remains capable of semantically wrong or repeatedly invalid actions.",
        ],
    }
    write_json(output / "manifest.json", manifest)
    (output / "failure_analysis.md").write_text(
        render_failure_analysis(deterministic, runs), encoding="utf-8"
    )
    (output / "release_report.md").write_text(
        render_release_report(manifest), encoding="utf-8"
    )
    checkpoint = {
        "release_status": "failed_blocked",
        "agent_version": __version__,
        "source_commit": "812c510f5cfe4f26c46e923435ae89bd6f1229bb",
        "evidence_commit": environment["git_commit"],
        "dataset_hashes": validation["partition_hashes"],
        "model_digest": environment.get("retained_model_metadata", {}).get("model_digest") if isinstance(environment.get("retained_model_metadata"), dict) else None,
        "passed_gates": ["frozen_dataset_hash_validation", "typed_route_schema", "v0.10_deterministic_regression", "v0.10_false_success_regressions_zero", "forbidden_and_unauthorized_selection_zero"],
        "failed_gates": ["external_blind_evaluation", "three_complete_live_runs", "blind_accuracy_metrics", "dataset_independence"],
        "unresolved_cases": ["16 frozen adversarial mutation-intent contradictions", "existing-file proposal labels name eventual rather than first lifecycle tool"],
        "reproduction_commands": [
            "python -m pytest -q",
            "python -m mind01.eval validate",
            "python -m mind01.eval run --suite semantic-routing",
            "python -m mind01.eval semantic-live --partition development --model qwen2.5-coder:7b --seed 1102 --output evaluation_results/v0.11.0-release/development_runs/run-002.json",
        ],
        "architectural_decisions": ["typed deterministic five-stage routing", "capability-bound route identity", "single exposure authority", "inspect existing source before proposal"],
        "next_branch": None,
        "next_implementation_action": "Obtain an independently controlled blind evaluator and create a corrected newly frozen dataset version before another release candidate.",
    }
    write_json(output / "development_checkpoint.json", checkpoint)
    write_json(ROOT / ".mind01" / "development_checkpoint.json", checkpoint)
    print(json.dumps({"manifest": str(output / "manifest.json"), "status": "failed_blocked"}, indent=2))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
