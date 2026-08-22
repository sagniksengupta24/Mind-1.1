from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterable

from mind01.annotation_v3 import derive_policy_constraints


ROOT = Path(__file__).resolve().parents[1]
EVAL_SUITES = ROOT / "mind01/eval_suites"
SEQUENCE_THRESHOLD = 0.88
BIGRAM_JACCARD_THRESHOLD = 0.72
SEMANTIC_SIGNATURE_THRESHOLD = 0.80
MINIMUM_VALIDATED = 150


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate semantic-routing v3 blind independence")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--report", required=True)
    args = parser.parse_args()
    source = Path(args.input).resolve()
    output = Path(args.output).resolve()
    report_path = Path(args.report).resolve()
    for destination in (output, report_path):
        if destination.exists():
            raise FileExistsError(f"refusing to overwrite existing output: {destination}")
    raw = load(source)
    historical = historical_prompts(source)
    accepted: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    seen: list[tuple[str, dict[str, Any]]] = []
    for case in raw["cases"]:
        structural_errors = validate_public_case(case)
        duplicate = closest_duplicate(case, (*historical, *seen))
        if structural_errors or duplicate is not None:
            rejected.append({
                "case_id": case.get("case_id"),
                "structural_errors": structural_errors,
                "duplicate": duplicate,
            })
            continue
        accepted.append(case)
        seen.append((case["prompt"], case))
    lifecycle_counts = Counter(
        case["authoring_metadata"]["lifecycle_template"]
        for case in accepted
    )
    max_lifecycle_share = max(lifecycle_counts.values(), default=0) / len(accepted) if accepted else 0.0
    if len(accepted) < MINIMUM_VALIDATED:
        raise RuntimeError(f"only {len(accepted)} independent raw cases remain; need {MINIMUM_VALIDATED}")
    if max_lifecycle_share > 0.10:
        raise RuntimeError(f"authoring lifecycle-template share {max_lifecycle_share:.3f} exceeds 10%")
    accepted_payload = {
        "schema_version": "3.0",
        "suite": "semantic-routing-blind-v3-independent-candidates",
        "raw_case_count": len(raw["cases"]),
        "deduplicated_case_count": len(accepted),
        "cases": accepted,
    }
    report = {
        "schema_version": "1.0",
        "source": str(source),
        "source_sha256": sha256(source),
        "historical_prompt_count": len(historical),
        "raw_case_count": len(raw["cases"]),
        "accepted_after_validation": len(accepted),
        "rejected_count": len(rejected),
        "thresholds": {
            "sequence_similarity": SEQUENCE_THRESHOLD,
            "token_bigram_jaccard": BIGRAM_JACCARD_THRESHOLD,
            "structured_semantic_signature": SEMANTIC_SIGNATURE_THRESHOLD,
        },
        "duplicate_sources": [
            "semantic_routing_v1",
            "semantic_routing_v2",
            "semantic_routing_v3_visible_and_calibration",
            "previous_failed_rc2_blind_inputs",
            "current_raw_set",
        ],
        "max_authoring_lifecycle_template_share": max_lifecycle_share,
        "lifecycle_template_counts": dict(sorted(lifecycle_counts.items())),
        "rejections": rejected,
    }
    write_json(output, accepted_payload)
    write_json(report_path, report)
    print(json.dumps({
        "output": str(output),
        "report": str(report_path),
        "raw": len(raw["cases"]),
        "accepted": len(accepted),
        "rejected": len(rejected),
        "max_lifecycle_template_share": max_lifecycle_share,
        "output_sha256": sha256(output),
    }, indent=2))
    return 0


def validate_public_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    required = {"case_id", "prompt", "agent_mode", "capabilities", "public_facts", "workspace_fixture"}
    missing = sorted(required - set(case))
    if missing:
        errors.append(f"missing public fields: {missing}")
        return errors
    if not isinstance(case["prompt"], str) or len(case["prompt"].split()) < 7:
        errors.append("prompt is too short")
    try:
        derive_policy_constraints(case)
    except (TypeError, ValueError) as exc:
        errors.append(str(exc))
    return errors


def historical_prompts(raw_source: Path) -> list[tuple[str, dict[str, Any]]]:
    prompts: list[tuple[str, dict[str, Any]]] = []
    for path in sorted(EVAL_SUITES.glob("semantic_routing_v[123]/*.json")):
        if path.resolve() == raw_source or "blind-v3" in path.name:
            continue
        try:
            payload = load(path)
        except (json.JSONDecodeError, RuntimeError):
            continue
        for case in payload.get("cases", []):
            prompt = case.get("prompt")
            if isinstance(prompt, str):
                prompts.append((prompt, case))
    return prompts


def closest_duplicate(
    candidate: dict[str, Any],
    existing: Iterable[tuple[str, dict[str, Any]]],
) -> dict[str, Any] | None:
    prompt = candidate["prompt"]
    normalized = normalize(prompt)
    bigrams = token_ngrams(normalized, 2)
    signature = semantic_signature(candidate)
    closest: dict[str, Any] | None = None
    closest_score = 0.0
    for prior_prompt, prior_case in existing:
        prior_normalized = normalize(prior_prompt)
        if normalized == prior_normalized:
            return {"kind": "exact", "prior_case_id": prior_case.get("case_id"), "score": 1.0}
        sequence = SequenceMatcher(None, normalized, prior_normalized, autojunk=False).ratio()
        bigram = jaccard(bigrams, token_ngrams(prior_normalized, 2))
        semantic = semantic_similarity(signature, semantic_signature(prior_case))
        score = max(sequence / SEQUENCE_THRESHOLD, bigram / BIGRAM_JACCARD_THRESHOLD, semantic / SEMANTIC_SIGNATURE_THRESHOLD)
        if score > closest_score:
            closest_score = score
            closest = {
                "kind": "near",
                "prior_case_id": prior_case.get("case_id"),
                "sequence": round(sequence, 4),
                "bigram_jaccard": round(bigram, 4),
                "semantic_signature": round(semantic, 4),
            }
        if sequence >= SEQUENCE_THRESHOLD or bigram >= BIGRAM_JACCARD_THRESHOLD or semantic >= SEMANTIC_SIGNATURE_THRESHOLD:
            return closest
    return None


def semantic_signature(case: dict[str, Any]) -> tuple[tuple[str, ...], frozenset[str]]:
    facts = case.get("public_facts", {})
    capabilities = case.get("capabilities", {})
    policy = (
        str(case.get("agent_mode", "")),
        str(facts.get("requested_operation", "")),
        str(facts.get("target_state", "")),
        str(facts.get("route_state", "")),
        str(bool(facts.get("unsafe_operation"))),
        str(bool(facts.get("unsupported_operation"))),
        str(bool(facts.get("self_contained"))),
        str(bool(facts.get("repository_resolvable"))),
        str(bool(capabilities.get("workspace_write"))),
        str(bool(capabilities.get("shell"))),
    )
    content = frozenset(
        token for token in normalize(str(case.get("prompt", ""))).split()
        if len(token) > 4 and token not in STOPWORDS
    )
    return policy, content


def semantic_similarity(
    left: tuple[tuple[str, ...], frozenset[str]],
    right: tuple[tuple[str, ...], frozenset[str]],
) -> float:
    if left[0] != right[0]:
        return 0.0
    return jaccard(left[1], right[1])


STOPWORDS = {
    "about", "after", "before", "change", "current", "existing", "implementation",
    "project", "repository", "report", "source", "without", "workspace",
}


def normalize(value: str) -> str:
    value = re.sub(r"\d+", "<n>", value.casefold())
    value = re.sub(r"[^a-z0-9_< >]+", " ", value)
    return " ".join(value.split())


def token_ngrams(value: str, size: int) -> frozenset[tuple[str, ...]]:
    tokens = value.split()
    return frozenset(tuple(tokens[index:index + size]) for index in range(len(tokens) - size + 1))


def jaccard(left: Iterable[Any], right: Iterable[Any]) -> float:
    left_set, right_set = set(left), set(right)
    union = left_set | right_set
    return len(left_set & right_set) / len(union) if union else 1.0


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise RuntimeError(f"{path} must contain an object")
    return value


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"refusing to overwrite existing output: {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


if __name__ == "__main__":
    raise SystemExit(main())
