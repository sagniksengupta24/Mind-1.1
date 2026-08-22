"""Crash-safe orchestration around the frozen RC3 annotation implementation."""

from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

from mind01.annotation_v3 import (
    annotation_agreement,
    derive_policy_constraints,
    semantic_label_projection,
    validate_annotation,
)
from run_semantic_v3_annotation import (
    MODEL_DIGEST,
    _report,
    adjudicate,
    annotate,
    model_identity,
)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Resume-safe RC3.1 orchestration using the byte-frozen RC3 annotator"
    )
    parser.add_argument("--input", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    result = run(Path(args.input), Path(args.output_dir), args.timeout, args.resume)
    print(json.dumps({"output": str(Path(args.output_dir).resolve()), "summary": result["summary"]}, indent=2))
    return 0 if result["summary"]["accepted_count"] == result["summary"]["processed_count"] else 1


def run(source: Path, output: Path, timeout: int, resume: bool) -> dict[str, Any]:
    source, output = source.resolve(), output.resolve()
    cases = json.loads(source.read_text(encoding="utf-8"))["cases"]
    if output.exists() and any(output.iterdir()) and not resume:
        raise FileExistsError(f"existing annotation state requires --resume: {output}")
    output.mkdir(parents=True, exist_ok=True)
    records_dir, labels_dir = output / "records", output / "accepted_labels"
    records_dir.mkdir(exist_ok=True)
    labels_dir.mkdir(exist_ok=True)
    final_report = output / "report.json"
    final_labels = output / "labels.json"
    if final_report.exists() or final_labels.exists():
        if not (final_report.exists() and final_labels.exists() and resume):
            raise RuntimeError("partial final annotation artifacts require manual audit")
        report = load(final_report)
        if not report.get("complete"):
            raise RuntimeError("final report is not complete")
        return report
    metadata = model_identity(timeout)
    if metadata["model_digest"] != MODEL_DIGEST:
        raise RuntimeError("annotation model digest mismatch")
    started = time.monotonic()
    for index, case in enumerate(cases):
        record_path = records_dir / f"{index:03d}-{case['case_id']}.json"
        label_path = labels_dir / f"{index:03d}-{case['case_id']}.json"
        if record_path.exists():
            record = load(record_path)
            if record["case_id"] != case["case_id"]:
                raise RuntimeError("annotation checkpoint case identity mismatch")
            if record["accepted"] != label_path.exists():
                raise RuntimeError("annotation checkpoint label-state mismatch")
            continue
        record, annotation = annotate_case(case, index, timeout)
        write_new(record_path, record)
        if annotation is not None:
            write_new(label_path, {"case_id": case["case_id"], "annotation": annotation})
        records, accepted = load_state(cases, records_dir, labels_dir)
        write_atomic(
            output / "checkpoint.json",
            _report("blind", source, metadata, cases, accepted, records, time.monotonic() - started, False),
        )
    records, accepted = load_state(cases, records_dir, labels_dir)
    if len(records) != len(cases):
        raise RuntimeError("annotation did not reach a terminal state for every candidate")
    report = _report("blind", source, metadata, cases, accepted, records, time.monotonic() - started, True)
    write_new(final_report, report)
    write_new(final_labels, {"schema_version": "3.0", "labels": accepted})
    return report


def annotate_case(case: dict[str, Any], index: int, timeout: int) -> tuple[dict[str, Any], dict[str, Any] | None]:
    constraints = derive_policy_constraints(case)
    left = annotate(case, constraints, "A", 32101 + index, timeout)
    right = annotate(case, constraints, "B", 42101 + index, timeout)
    left_errors = validate_annotation(case, left, constraints)
    right_errors = validate_annotation(case, right, constraints)
    agreement = annotation_agreement(left, right) if not left_errors and not right_errors else {}
    exact = not left_errors and not right_errors and semantic_label_projection(left) == semantic_label_projection(right)
    if exact:
        final = left
        adjudicated = False
        errors: list[str] = []
        resolution = "independent_exact_agreement"
    else:
        final = adjudicate(
            case, constraints, left, right, left_errors, right_errors, 52101 + index, timeout
        )
        adjudicated = True
        errors = validate_annotation(case, final, constraints)
        resolution = "isolated_adjudication" if not errors else "rejected_after_adjudication"
    record = {
        "case_id": case["case_id"],
        "constraints_sha256": digest_json(constraints.to_dict()),
        "annotator_a_schema_valid": isinstance(left, dict),
        "annotator_b_schema_valid": isinstance(right, dict),
        "annotator_a_consistency_errors": left_errors,
        "annotator_b_consistency_errors": right_errors,
        "agreement": agreement,
        "adjudicated": adjudicated,
        "adjudication_errors": errors,
        "resolution": resolution,
        "accepted": not errors,
    }
    return record, final if not errors else None


def load_state(
    cases: list[dict[str, Any]], records_dir: Path, labels_dir: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    records, accepted = [], []
    for index, case in enumerate(cases):
        stem = f"{index:03d}-{case['case_id']}.json"
        record_path, label_path = records_dir / stem, labels_dir / stem
        if not record_path.exists():
            break
        records.append(load(record_path))
        if label_path.exists():
            accepted.append(load(label_path))
    return records, accepted


def digest_json(value: Any) -> str:
    import hashlib
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} must contain an object")
    return value


def write_new(path: Path, value: Any) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite annotation evidence: {path}")
    write_atomic(path, value)


def write_atomic(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


if __name__ == "__main__":
    raise SystemExit(main())
