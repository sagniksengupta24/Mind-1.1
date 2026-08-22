from __future__ import annotations

import argparse
import hashlib
import importlib.util
import inspect
import json
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mind01.annotation_v3 import annotation_schema, derive_policy_constraints


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODEL = "qwen2.5-coder:7b"
EXPECTED_DIGEST = "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364"
EXPECTED_OLLAMA_VERSION = "0.32.0"
OLLAMA_URL = "http://127.0.0.1:11434"


def main() -> int:
    parser = argparse.ArgumentParser(description="Freeze a passing semantic-routing v3 evaluator")
    parser.add_argument("--calibration-report", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--timeout", type=int, default=30)
    args = parser.parse_args()

    report_path = Path(args.calibration_report).resolve()
    output = Path(args.output_dir).resolve()
    report = load(report_path)
    assert_passing_calibration(report)
    runner = load_runner()
    model = live_model_identity(args.timeout)
    if model["model"] != EXPECTED_MODEL or model["model_digest"] != EXPECTED_DIGEST:
        raise RuntimeError("evaluator freeze model identity mismatch")
    if model["ollama_version"] != EXPECTED_OLLAMA_VERSION:
        raise RuntimeError("evaluator freeze Ollama version mismatch")

    calibration_path = ROOT / "mind01/eval_suites/semantic_routing_v3/evaluator_calibration.json"
    cases = load(calibration_path)["cases"]
    dynamic_schemas = [
        annotation_schema(derive_policy_constraints(case))
        for case in cases
    ]
    prompt_contract = {
        "public_spec": runner.PUBLIC_SPEC,
        "tool_public_spec": runner.TOOL_PUBLIC_SPEC,
        "tool_descriptions": runner.TOOL_DESCRIPTIONS,
        "annotate_source": inspect.getsource(runner.annotate),
        "adjudicate_source": inspect.getsource(runner.adjudicate),
        "public_case_source": inspect.getsource(runner.public_case),
    }
    source_files = [
        ROOT / "mind01/annotation_v3.py",
        ROOT / "scripts/build_semantic_v3_assets.py",
        ROOT / "scripts/run_semantic_v3_annotation.py",
        ROOT / "scripts/freeze_semantic_v3_evaluator.py",
        ROOT / "tests/test_annotation_v3.py",
    ]
    source_manifest = {
        str(path.relative_to(ROOT)): sha256_bytes(path.read_bytes())
        for path in source_files
    }
    source_commit = git("rev-parse", "HEAD")
    summary = report["summary"]
    identity = {
        "evaluator_version": "semantic-routing-evaluator-v3",
        "source_commit": source_commit,
        "calibration_case_count": summary["case_count"],
        "calibration_schema_validity": summary["schema_validity"],
        "hard_constraint_consistency": summary["final_hard_constraint_consistency"],
        "task_class_agreement": summary["gold_agreement"]["task_class"],
        "immediate_family_agreement": summary["gold_agreement"]["immediate_family"],
        "allowed_tool_set_agreement": summary["gold_agreement"]["allowed_tool_set"],
        "lifecycle_agreement": summary["gold_agreement"]["lifecycle"],
        "rejected_case_count": summary["rejected_count"],
        "unresolved_critical_safety_conflicts": summary["critical_safety_disagreement_unresolved"],
        "contradictory_mutation_fields": summary["contradictory_mutation_fields"],
        "source_sha256": digest_json(source_manifest),
        "source_files": source_manifest,
        "prompt_sha256": digest_json(prompt_contract),
        "schema_sha256": digest_json(dynamic_schemas),
        "calibration_sha256": sha256_bytes(calibration_path.read_bytes()),
        "calibration_report_sha256": sha256_bytes(report_path.read_bytes()),
        "adjudication_contract_sha256": sha256_text(inspect.getsource(runner.adjudicate)),
        "accepted_label_sha256": report["accepted_label_sha256"],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "evaluator_identity.json", identity)
    write_json(output / "model_identity.json", model)
    write_json(output / "calibration_results.json", {
        "calibration_gate_passed": True,
        "report": str(report_path.relative_to(ROOT)),
        "report_sha256": identity["calibration_report_sha256"],
        "summary": summary,
    })
    print(json.dumps(identity, indent=2))
    return 0


def assert_passing_calibration(report: dict[str, Any]) -> None:
    summary = report.get("summary", {})
    if not report.get("complete") or not report.get("calibration_gate_passed"):
        raise RuntimeError("calibration report did not pass the complete gate")
    if summary.get("accepted_count") != 60 or summary.get("rejected_count") != 0:
        raise RuntimeError("calibration freeze requires 60 accepted and zero rejected cases")
    if summary.get("critical_safety_disagreement_unresolved") != 0:
        raise RuntimeError("calibration freeze has unresolved safety conflicts")
    if summary.get("contradictory_mutation_fields") != 0:
        raise RuntimeError("calibration freeze has contradictory mutation fields")


def live_model_identity(timeout: int) -> dict[str, Any]:
    version = get_json("/api/version", timeout)
    tags = get_json("/api/tags", timeout)
    item = next((entry for entry in tags.get("models", []) if entry.get("name") == EXPECTED_MODEL), {})
    details = item.get("details", {})
    return {
        "client_version": version.get("version", ""),
        "ollama_version": version.get("version", ""),
        "daemon_available": True,
        "endpoint": OLLAMA_URL,
        "model": EXPECTED_MODEL,
        "model_digest": item.get("digest", ""),
        "quantization": details.get("quantization_level", ""),
        "context_length": details.get("context_length", 32768),
        "output_mode": "json_schema",
        "timeout_seconds": 180,
        "annotator_a": {"temperature": 0.05, "seed_base": 32101},
        "annotator_b": {"temperature": 0.35, "seed_base": 42101},
        "adjudicator": {"temperature": 0.0, "seed_base": 52101},
    }


def get_json(endpoint: str, timeout: int) -> dict[str, Any]:
    request = urllib.request.Request(OLLAMA_URL + endpoint)
    with urllib.request.urlopen(request, timeout=timeout) as response:
        value = json.loads(response.read().decode("utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"Ollama {endpoint} returned a non-object")
    return value


def load_runner() -> Any:
    path = ROOT / "scripts/run_semantic_v3_annotation.py"
    spec = importlib.util.spec_from_file_location("semantic_v3_annotation_runner", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load semantic v3 annotation runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return value


def digest_json(value: Any) -> str:
    return sha256_text(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False))


def sha256_text(value: str) -> str:
    return sha256_bytes(value.encode("utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def write_json(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


if __name__ == "__main__":
    raise SystemExit(main())
