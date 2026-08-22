"""Run the fresh v0.11.1 semantic router benchmark."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from mind01.semantic_benchmark_v2 import (
    DEVELOPMENT_GATES,
    HOLDOUT_ACCESS,
    HOLDOUT_GATES,
    SemanticBenchmarkError,
    deterministic_order,
    evaluate_gates,
    load_split,
    legacy_v2_disagreements,
    run_case,
    score_results,
    validate_suite,
)
from mind01.version import __version__


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser()
    result.add_argument("--router", choices=("legacy", "v2"), default="v2")
    result.add_argument(
        "--split",
        choices=("examples", "development", "internal_holdout"),
        default="development",
    )
    result.add_argument("--model", default="qwen2.5-coder:7b")
    result.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    result.add_argument("--seed", type=int, default=11103)
    result.add_argument("--output-dir", type=Path, required=True)
    result.add_argument("--timeout", type=int, default=120)
    result.add_argument("--live", action="store_true")
    result.add_argument("--resume", action="store_true")
    result.add_argument("--confirm-holdout-once", action="store_true")
    result.add_argument("--ablation", action="store_true")
    return result


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    if args.split == "internal_holdout":
        if not args.confirm_holdout_once:
            raise SemanticBenchmarkError(
                "holdout requires --confirm-holdout-once after development is frozen"
            )
        if HOLDOUT_ACCESS.exists():
            raise SemanticBenchmarkError(
                "internal holdout has already been opened; reruns are prohibited"
            )
    integrity = validate_suite(include_holdout=args.split == "internal_holdout")
    cases = load_split(
        args.split, open_holdout=args.split == "internal_holdout"
    )
    args.output_dir.mkdir(parents=True, exist_ok=True)
    if args.ablation:
        if args.split != "development" or args.live:
            raise SemanticBenchmarkError(
                "ablation is deterministic and development-only"
            )
        report = run_ablation(args, cases, integrity)
        path = args.output_dir / "ablation.json"
        atomic_json(path, report)
        print(json.dumps(report, indent=2, sort_keys=True))
        return 0

    started = time.time()
    checkpoint_path = args.output_dir / f"{args.split}-checkpoint.json"
    completed: dict[str, dict[str, Any]] = {}
    if args.resume and checkpoint_path.exists():
        previous = json.loads(checkpoint_path.read_text(encoding="utf-8"))
        completed = {
            item["case_id"]: item for item in previous.get("results", [])
        }
    for case in deterministic_order(cases, args.seed):
        case_id = str(case["case_id"])
        if case_id in completed:
            continue
        completed[case_id] = run_case(
            case,
            router_name=args.router,
            live=args.live,
            model=args.model,
            ollama_url=args.ollama_url,
            timeout=args.timeout,
            seed=args.seed,
        )
        atomic_json(
            checkpoint_path,
            {
                "schema_version": "1.0",
                "split": args.split,
                "seed": args.seed,
                "results": list(completed.values()),
            },
        )
    results = [completed[str(case["case_id"])] for case in cases]
    scored = score_results(results)
    gates = (
        HOLDOUT_GATES
        if args.split == "internal_holdout"
        else DEVELOPMENT_GATES
        if args.split == "development"
        else {}
    )
    gate_result = evaluate_gates(scored["metrics"], gates) if gates else {}
    report = {
        "schema_version": "1.0",
        "suite": "semantic-routing-v2.1-fresh",
        "agent_version": __version__,
        "router": args.router,
        "run_mode": "live_ollama" if args.live else "deterministic_ci",
        "model": args.model if args.live else "deterministic-fixture-classifier",
        "requested_model": args.model,
        "seed": args.seed,
        "timeout_seconds": args.timeout,
        "split": args.split,
        "started_at": datetime.fromtimestamp(started, timezone.utc).isoformat(),
        "duration_seconds": round(time.time() - started, 3),
        "integrity": integrity,
        **scored,
        "gates": gate_result,
        "legacy_v2_disagreements": legacy_v2_disagreements(cases, results),
        "results": results,
    }
    report_path = args.output_dir / f"{args.split}-report.json"
    atomic_json(report_path, report)
    digest = hashlib.sha256(report_path.read_bytes()).hexdigest()
    atomic_json(
        args.output_dir / f"{args.split}-summary.json",
        {
            key: report[key]
            for key in (
                "schema_version",
                "suite",
                "agent_version",
                "router",
                "run_mode",
                "model",
                "seed",
                "split",
                "duration_seconds",
                "metrics",
                "per_class_accuracy",
                "per_family_accuracy",
                "per_risk_accuracy",
                "confusion_matrices",
                "gates",
            )
        }
        | {"full_report_sha256": digest},
    )
    if args.split == "internal_holdout":
        atomic_json(
            HOLDOUT_ACCESS,
            {
                "schema_version": "1.0",
                "opened_at": datetime.now(timezone.utc).isoformat(),
                "command": "evaluate_semantic_router --split internal_holdout --confirm-holdout-once",
                "run_mode": report["run_mode"],
                "report_sha256": digest,
                "development_frozen": True,
            },
        )
    print(json.dumps({key: report[key] for key in ("split", "run_mode", "metrics", "gates")}, indent=2, sort_keys=True))
    return 0 if not gate_result or gate_result["passed"] else 1


def run_ablation(
    args: argparse.Namespace,
    cases: list[dict[str, Any]],
    integrity: dict[str, Any],
) -> dict[str, Any]:
    variants = (
        ("legacy", "legacy"),
        ("staged_no_constraints", "staged_no_constraints"),
        ("staged_candidate_reduction", "staged_candidate_reduction"),
        ("full_v2", "full_v2"),
    )
    reports: dict[str, Any] = {}
    for name, variant in variants:
        results = [
            run_case(
                case,
                router_name="legacy" if variant == "legacy" else "v2",
                live=False,
                model=args.model,
                ollama_url=args.ollama_url,
                timeout=args.timeout,
                seed=args.seed,
                variant=variant,
            )
            for case in deterministic_order(cases, args.seed)
        ]
        reports[name] = score_results(results)
    return {
        "schema_version": "1.0",
        "suite": "semantic-routing-v2.1-fresh",
        "agent_version": __version__,
        "split": "development",
        "seed": args.seed,
        "integrity": integrity,
        "variants": reports,
    }


if __name__ == "__main__":
    raise SystemExit(main())
