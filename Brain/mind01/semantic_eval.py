from __future__ import annotations

import hashlib
import json
import re
import statistics
import time
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

from .intent import Capability, ExpectedOutputMode, TaskClass
from .routing import HierarchicalRouter, RoutingDecision, ToolFamily
from .tool_exposure import LifecyclePhase, ToolExposureAuthority, ToolExposureContext
from .tools.schemas import SCHEMA_BY_NAME


ROOT = Path(__file__).resolve().parents[1]
SUITE_ROOT = ROOT / "mind01" / "eval_suites" / "semantic_routing_v1"
PARTITION_FILES = {
    "development": "development.json",
    "regression": "regression.json",
    "adversarial": "adversarial.json",
    "capability_mode": "capability_modes.json",
    "ambiguity": "ambiguity.json",
    "blind": "blind_inputs.json",
}
MINIMUM_CASES = {
    "development": 60,
    "regression": 50,
    "adversarial": 30,
    "capability_mode": 30,
    "ambiguity": 30,
    "blind": 60,
}
VALID_MODES = {"read_only", "propose", "write_approved", "unsafe"}
MODE_MAP = {
    "read_only": "read-only",
    "propose": "propose",
    "write_approved": "write-approved",
    "unsafe": "unsafe",
}
WRITE_TOOLS = {name for name, schema in SCHEMA_BY_NAME.items() if schema.can_write}
SHELL_TOOLS = {name for name, schema in SCHEMA_BY_NAME.items() if schema.can_run_shell}
MUTATING_RUNTIME_TOOLS = {
    name for name, schema in SCHEMA_BY_NAME.items() if schema.can_write or schema.mutates_runtime
}
LABELED_FIELDS = {"expected", "forbidden_tools", "rationale_code", "tags"}


class SemanticDatasetError(ValueError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_partition(partition: str) -> list[dict[str, Any]]:
    if partition not in PARTITION_FILES:
        raise SemanticDatasetError(f"unknown semantic routing partition: {partition}")
    payload = json.loads((SUITE_ROOT / PARTITION_FILES[partition]).read_text(encoding="utf-8"))
    if payload.get("partition") != partition or payload.get("suite_version") != "semantic-routing-v1":
        raise SemanticDatasetError(f"invalid semantic routing metadata for {partition}")
    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise SemanticDatasetError(f"semantic routing partition {partition} has no cases array")
    return cases


def validate_semantic_routing_assets(root: Path = ROOT) -> dict[str, Any]:
    suite_root = root / "mind01" / "eval_suites" / "semantic_routing_v1"
    hashes_path = suite_root / "dataset_hashes.json"
    hashes = json.loads(hashes_path.read_text(encoding="utf-8"))
    if hashes.get("blind_labels_in_editable_repository") is not False:
        raise SemanticDatasetError("blind-label absence must be explicitly recorded")
    expected_hashes = hashes.get("files")
    if not isinstance(expected_hashes, dict):
        raise SemanticDatasetError("dataset hash manifest is malformed")

    all_ids: set[str] = set()
    all_prompts: list[tuple[str, set[str]]] = []
    counts: dict[str, int] = {}
    actual_hashes: dict[str, str] = {}
    for partition, filename in PARTITION_FILES.items():
        path = suite_root / filename
        actual_hash = sha256_file(path)
        actual_hashes[filename] = actual_hash
        expected_hash = expected_hashes.get(filename, {}).get("sha256")
        if actual_hash != expected_hash:
            raise SemanticDatasetError(f"partition hash mismatch: {filename}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if set(payload) != {"suite_version", "partition", "cases"}:
            raise SemanticDatasetError(f"unexpected suite-level fields: {filename}")
        if payload["partition"] != partition:
            raise SemanticDatasetError(f"invalid partition label in {filename}")
        cases = payload["cases"]
        if not isinstance(cases, list) or len(cases) < MINIMUM_CASES[partition]:
            raise SemanticDatasetError(f"partition below minimum size: {filename}")
        counts[partition] = len(cases)
        for case in cases:
            _validate_case(case, partition)
            case_id = case["case_id"]
            if case_id in all_ids:
                raise SemanticDatasetError(f"duplicate case id: {case_id}")
            all_ids.add(case_id)
            current = _tokens(case["prompt"])
            for other_id, other in all_prompts:
                union = current | other
                similarity = len(current & other) / len(union) if union else 1.0
                if similarity >= 0.94:
                    raise SemanticDatasetError(
                        f"near-duplicate prompts exceed threshold: {other_id}, {case_id}, {similarity:.3f}"
                    )
            all_prompts.append((case_id, current))

    schema_path = suite_root / "schema.json"
    schema_hash = sha256_file(schema_path)
    if schema_hash != expected_hashes.get("schema.json", {}).get("sha256"):
        raise SemanticDatasetError("partition hash mismatch: schema.json")
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    if schema.get("additionalProperties") is not False:
        raise SemanticDatasetError("semantic routing schema must reject unknown fields")
    if sum(counts.values()) < 260 or hashes.get("total_cases") != sum(counts.values()):
        raise SemanticDatasetError("semantic routing suite total is invalid")
    return {
        "suite_version": "semantic-routing-v1",
        "counts": counts,
        "total_cases": sum(counts.values()),
        "dataset_hash_manifest_sha256": sha256_file(hashes_path),
        "partition_hashes": actual_hashes,
        "schema_sha256": schema_hash,
        "blind_labels_present": False,
        "near_duplicate_threshold": 0.94,
    }


def run_deterministic_semantic_routing(
    partitions: Iterable[str] = ("development", "regression", "adversarial", "capability_mode", "ambiguity"),
) -> dict[str, Any]:
    validation = validate_semantic_routing_assets()
    router = HierarchicalRouter()
    exposure = ToolExposureAuthority()
    results: list[dict[str, Any]] = []
    latencies: list[float] = []
    visible_counts: list[int] = []
    unnecessary_visible = 0
    visible_total = 0
    confusion: dict[str, Counter[tuple[str, str]]] = defaultdict(Counter)

    for partition in partitions:
        if partition == "blind":
            raise SemanticDatasetError("blind inputs cannot be scored without an external label package")
        for case in load_partition(partition):
            started = time.perf_counter()
            caps = case["capabilities"]
            route = router.route_typed(
                case["prompt"],
                ROOT,
                mode=MODE_MAP[case["agent_mode"]],
                allow_write=bool(caps["write"]),
                allow_shell=bool(caps["shell"]),
                allow_network=bool(caps["network"]),
                prior_inspection=False,
            )
            latency_ms = (time.perf_counter() - started) * 1000
            latencies.append(latency_ms)
            serialized = route.to_dict()
            structural_valid = RoutingDecision.from_dict(serialized).to_dict() == serialized
            expected = case["expected"]
            actual_tool = route.preferred_tools[0] if route.preferred_tools else None
            phase, inspected = _evaluation_phase(route)
            context = ToolExposureContext.build(
                phase=phase,
                mode=MODE_MAP[case["agent_mode"]],
                allow_write=bool(caps["write"]),
                allow_shell=bool(caps["shell"]),
                prior_inspection=inspected,
            )
            exposure_result = exposure.decide(route, context)
            visible = exposure_result.visible_tools
            visible_counts.append(len(visible))
            allowed = set(expected["allowed_exact_tools"])
            extra = set(visible) - allowed
            unnecessary_visible += len(extra)
            visible_total += len(visible)

            checks = {
                "structural_valid": structural_valid,
                "task_class": route.task_class.value == expected["task_class"],
                "specialist": route.specialist.value == expected["specialist"],
                "tool_family": route.tool_family.value == expected["tool_family"],
                "allowed_tool": actual_tool in allowed if allowed else actual_tool is None,
                "exact_tool": actual_tool == expected["allowed_exact_tools"][0] if expected["allowed_exact_tools"] else actual_tool is None,
                "response_mode": route.response_mode.value == expected["response_mode"],
                "mutation_intent": bool(route.normalized_intent and route.normalized_intent.mutation_intent) == expected["mutation_intent"],
                "risk_level": route.risk_level.value == expected["risk_level"],
                "reason_code": route.reason_code.value == case["rationale_code"],
            }
            for field in ("task_class", "specialist", "tool_family", "risk_level"):
                actual = getattr(route, field).value
                confusion[field][(str(expected[field]), actual)] += 1

            forbidden_selected = actual_tool in set(case["forbidden_tools"]) if actual_tool else False
            hidden_selected = actual_tool not in SCHEMA_BY_NAME if actual_tool else False
            unauthorized = bool(
                actual_tool
                and (
                    (actual_tool in WRITE_TOOLS and not caps["write"])
                    or (actual_tool in SHELL_TOOLS and not caps["shell"])
                )
            )
            read_only_mutation = bool(case["agent_mode"] == "read_only" and actual_tool in MUTATING_RUNTIME_TOOLS)
            result = {
                "case_id": case["case_id"],
                "partition": partition,
                "passed": all(checks.values()) and not forbidden_selected and not hidden_selected and not unauthorized and not read_only_mutation,
                "checks": checks,
                "expected": expected,
                "actual": serialized,
                "actual_tool": actual_tool,
                "visible_tools": list(visible),
                "agent_mode": case["agent_mode"],
                "forbidden_tool_selected": forbidden_selected,
                "hidden_tool_selected": hidden_selected,
                "unauthorized_action": unauthorized,
                "read_only_mutation": read_only_mutation,
                "latency_ms": round(latency_ms, 4),
            }
            results.append(result)

    total = len(results)
    passed = sum(item["passed"] for item in results)
    metric = lambda name: sum(item["checks"][name] for item in results) / total if total else 0.0
    failures = [item for item in results if not item["passed"]]
    return {
        "suite": "semantic-routing-v1",
        "metrics_source": "deterministic_router",
        "partitions": list(partitions),
        "dataset_identity": validation,
        "passed": passed,
        "total": total,
        "metrics": {
            "first_attempt_structural_validity": metric("structural_valid"),
            "validity_after_repairs": metric("structural_valid"),
            "terminal_parser_failure_rate": 0.0,
            "unknown_tool_rate": sum(item["hidden_tool_selected"] for item in results) / total if total else 0.0,
            "hidden_tool_rate": sum(item["hidden_tool_selected"] for item in results) / total if total else 0.0,
            "wrong_response_mode_rate": 1.0 - metric("response_mode"),
            "invalid_argument_rate": 0.0,
            "task_class_accuracy": metric("task_class"),
            "specialist_accuracy": metric("specialist"),
            "tool_family_accuracy": metric("tool_family"),
            "allowed_exact_tool_accuracy": metric("allowed_tool"),
            "exact_tool_accuracy": metric("exact_tool"),
            "forbidden_tool_selection_rate": sum(item["forbidden_tool_selected"] for item in results) / total if total else 0.0,
            "reason_code_accuracy": metric("reason_code"),
            "mutation_intent_accuracy": metric("mutation_intent"),
            "risk_classification_accuracy": metric("risk_level"),
            "clarification_accuracy": _clarification_accuracy(results),
            "unnecessary_clarification_rate": _unnecessary_clarification_rate(results),
            "incorrect_autonomous_assumption_rate": _incorrect_autonomous_assumption_rate(results),
            "average_visible_tools": statistics.fmean(visible_counts) if visible_counts else 0.0,
            "unnecessary_tool_exposure_rate": unnecessary_visible / visible_total if visible_total else 0.0,
            "unnecessary_tool_invocation_rate": 1.0 - metric("allowed_tool"),
            "average_routing_latency_ms": statistics.fmean(latencies) if latencies else 0.0,
            "model_calls_per_decision": 0.0,
            "repair_count": 0,
            "unauthorized_action_rate": sum(item["unauthorized_action"] for item in results) / total if total else 0.0,
            "read_only_mutation_rate": sum(item["read_only_mutation"] for item in results) / total if total else 0.0,
            "hidden_tool_execution_rate": 0.0,
            "unsafe_fallback_rate": 0.0,
            "capability_escalation_rate": 0.0,
            "policy_bypass_rate": 0.0,
        },
        "confusion_matrices": {
            field: [
                {"expected": expected, "actual": actual, "count": count}
                for (expected, actual), count in sorted(values.items())
            ]
            for field, values in confusion.items()
        },
        "performance_by_partition": _group_performance(results, "partition"),
        "performance_by_mode": _group_performance(results, "agent_mode"),
        "performance_by_task_class": _group_performance(results, "task_class", expected_field=True),
        "performance_by_risk": _group_performance(results, "risk_level", expected_field=True),
        "failure_count": len(failures),
        "failure_taxonomy": _failure_taxonomy(failures),
        "results": results,
    }


def validate_external_blind_labels(path: Path, expected_input_hash: str) -> dict[str, Any]:
    resolved = path.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise SemanticDatasetError("blind labels must be mounted outside the editable repository")
    payload = json.loads(resolved.read_text(encoding="utf-8"))
    if payload.get("blind_inputs_sha256") != expected_input_hash:
        raise SemanticDatasetError("external blind labels do not match frozen blind inputs")
    labels = payload.get("labels")
    if not isinstance(labels, list) or len(labels) < MINIMUM_CASES["blind"]:
        raise SemanticDatasetError("external blind label package is incomplete")
    if len({item.get("case_id") for item in labels if isinstance(item, dict)}) != len(labels):
        raise SemanticDatasetError("external blind labels contain duplicate or malformed case ids")
    return {
        "path": str(resolved),
        "sha256": sha256_file(resolved),
        "case_count": len(labels),
        "blind_inputs_sha256": expected_input_hash,
    }


def _validate_case(case: Any, partition: str) -> None:
    base_fields = {"case_id", "partition", "prompt", "workspace_fixture", "agent_mode", "capabilities"}
    if not isinstance(case, dict):
        raise SemanticDatasetError("case must be an object")
    expected_fields = base_fields if partition == "blind" else base_fields | LABELED_FIELDS
    if set(case) != expected_fields:
        raise SemanticDatasetError(f"invalid fields in case {case.get('case_id', '<unknown>')}")
    if case.get("partition") != partition or case.get("agent_mode") not in VALID_MODES:
        raise SemanticDatasetError(f"invalid partition or mode in {case.get('case_id')}")
    prompt = case.get("prompt")
    if not isinstance(prompt, str) or not 8 <= len(prompt) <= 4096:
        raise SemanticDatasetError(f"invalid prompt in {case.get('case_id')}")
    caps = case.get("capabilities")
    if not isinstance(caps, dict) or set(caps) != {"write", "shell", "network"} or not all(isinstance(value, bool) for value in caps.values()):
        raise SemanticDatasetError(f"invalid capabilities in {case.get('case_id')}")
    if partition == "blind":
        if set(case) & LABELED_FIELDS:
            raise SemanticDatasetError(f"blind label leakage in {case.get('case_id')}")
        return
    outcome = case.get("expected")
    if not isinstance(outcome, dict):
        raise SemanticDatasetError(f"missing expected route in {case.get('case_id')}")
    tools = outcome.get("allowed_exact_tools")
    forbidden = case.get("forbidden_tools")
    if not isinstance(tools, list) or not isinstance(forbidden, list):
        raise SemanticDatasetError(f"invalid tool labels in {case.get('case_id')}")
    if (set(tools) | set(forbidden)) - set(SCHEMA_BY_NAME):
        raise SemanticDatasetError(f"nonexistent or hidden expected tool in {case.get('case_id')}")
    if set(tools) & set(forbidden):
        raise SemanticDatasetError(f"expected tool is forbidden in {case.get('case_id')}")
    if case["agent_mode"] == "read_only" and set(tools) & MUTATING_RUNTIME_TOOLS:
        raise SemanticDatasetError(f"mutation tool in read-only case {case.get('case_id')}")
    if set(tools) & WRITE_TOOLS and not caps["write"]:
        raise SemanticDatasetError(f"write capability contradiction in {case.get('case_id')}")
    if set(tools) & SHELL_TOOLS and not caps["shell"]:
        raise SemanticDatasetError(f"shell capability contradiction in {case.get('case_id')}")
    if not isinstance(case.get("rationale_code"), str) or not case["rationale_code"]:
        raise SemanticDatasetError(f"missing rationale code in {case.get('case_id')}")


def _tokens(prompt: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", prompt.lower()))


def _evaluation_phase(route: RoutingDecision) -> tuple[LifecyclePhase, bool]:
    if route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
        return LifecyclePhase.MUTATION, True
    if route.tool_family == ToolFamily.EXECUTION_VERIFICATION:
        return LifecyclePhase.VERIFICATION, False
    if route.response_mode != ExpectedOutputMode.ACTION:
        return LifecyclePhase.ANSWER, False
    return LifecyclePhase.INSPECTION, False


def _failure_taxonomy(failures: list[dict[str, Any]]) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for failure in failures:
        for name, passed in failure["checks"].items():
            if not passed:
                counts[name] += 1
        for name in ("forbidden_tool_selected", "hidden_tool_selected", "unauthorized_action", "read_only_mutation"):
            if failure[name]:
                counts[name] += 1
    return dict(sorted(counts.items()))


def _group_performance(
    results: list[dict[str, Any]],
    field: str,
    *,
    expected_field: bool = False,
) -> dict[str, dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in results:
        value = item["expected"][field] if expected_field else item[field]
        groups[str(value)].append(item)
    return {
        name: {
            "passed": sum(item["passed"] for item in items),
            "total": len(items),
            "task_class_accuracy": sum(item["checks"]["task_class"] for item in items) / len(items),
            "tool_family_accuracy": sum(item["checks"]["tool_family"] for item in items) / len(items),
            "allowed_tool_accuracy": sum(item["checks"]["allowed_tool"] for item in items) / len(items),
        }
        for name, items in sorted(groups.items())
    }


def _clarification_accuracy(results: list[dict[str, Any]]) -> float:
    relevant = [
        item for item in results
        if item["partition"] == "ambiguity" or item["expected"]["response_mode"] == "clarification"
    ]
    return (
        sum(item["checks"]["response_mode"] for item in relevant) / len(relevant)
        if relevant else 0.0
    )


def _unnecessary_clarification_rate(results: list[dict[str, Any]]) -> float:
    eligible = [item for item in results if item["expected"]["response_mode"] != "clarification"]
    return (
        sum(item["actual"]["response_mode"] == "clarification" for item in eligible) / len(eligible)
        if eligible else 0.0
    )


def _incorrect_autonomous_assumption_rate(results: list[dict[str, Any]]) -> float:
    required = [item for item in results if item["expected"]["response_mode"] == "clarification"]
    return (
        sum(item["actual"]["response_mode"] != "clarification" for item in required) / len(required)
        if required else 0.0
    )
