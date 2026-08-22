from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
SUITE = ROOT / "mind01" / "eval_suites" / "semantic_routing_v2"
PARTITION_FILES = {
    "development": "development.json",
    "regression": "regression.json",
    "adversarial": "adversarial.json",
    "capability_mode": "capability_modes.json",
    "ambiguity": "ambiguity.json",
    "lifecycle": "lifecycle.json",
    "end_to_end": "end_to_end.json",
    "blind": "blind_inputs.json",
}
VISIBLE_MINIMUMS = {
    "development": 60,
    "regression": 50,
    "adversarial": 30,
    "capability_mode": 30,
    "ambiguity": 30,
    "lifecycle": 40,
    "end_to_end": 24,
}
BASE_FIELDS = {
    "case_id", "source_case_id", "partition", "prompt", "workspace_fixture",
    "agent_mode", "capabilities",
}
LABELED_FIELDS = {"expected", "forbidden_tools", "tags"}
TASK_CLASSES = {"inspection", "mutation", "verification", "explanation", "planning", "blocked"}
SPECIALISTS = {"general", "repository_inspector", "implementation", "verification", "debugging", "documentation", "security_review"}
TOOL_FAMILIES = {
    "repository_discovery", "file_inspection", "symbol_inspection",
    "documentation_retrieval", "execution_verification", "mutation_proposal",
    "targeted_mutation", "file_creation", "patch_inspection",
    "memory_retrieval", "final_response", "clarification", "blocked",
}
TOOLS = {
    "list_files", "project_map", "read_file", "search_code", "index_code",
    "search_symbols", "file_summary", "write_file", "edit_file",
    "propose_write_file", "propose_edit_file", "list_patches", "show_patch",
    "test_patch", "run_command", "remember", "recall", "list_memories",
    "update_memory", "delete_memory", "search_docs", "refresh_knowledge",
    "query_knowledge",
}
SIDE_EFFECT_TOOLS = {
    "index_code", "write_file", "edit_file", "propose_write_file",
    "propose_edit_file", "remember", "update_memory", "delete_memory",
    "refresh_knowledge",
}
LIVE_MUTATION_TOOLS = {"write_file", "edit_file", "remember", "update_memory", "delete_memory"}
SHELL_TOOLS = {"run_command", "test_patch"}


class SemanticV2Error(ValueError):
    pass


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_v2_partition(partition: str) -> list[dict[str, Any]]:
    filename = PARTITION_FILES[partition]
    payload = json.loads((SUITE / filename).read_text(encoding="utf-8"))
    cases = payload.get("cases")
    if not isinstance(cases, list):
        raise SemanticV2Error(f"{filename} has no cases array")
    return cases


def validate_semantic_routing_v2(*, require_blind: bool = False) -> dict[str, Any]:
    manifest_path = SUITE / "dataset_hashes.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    hashes = manifest.get("hashes")
    if not isinstance(hashes, dict):
        raise SemanticV2Error("v2 hash manifest is malformed")
    for filename, expected_hash in hashes.items():
        path = SUITE / filename
        if not path.is_file() or sha256_file(path) != expected_hash:
            raise SemanticV2Error(f"v2 partition hash mismatch: {filename}")

    all_cases: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for partition, minimum in VISIBLE_MINIMUMS.items():
        cases = load_v2_partition(partition)
        if len(cases) < minimum:
            raise SemanticV2Error(f"{partition} has {len(cases)} cases; requires {minimum}")
        for case in cases:
            _validate_case(case, partition, blind=False)
        counts[partition] = len(cases)
        all_cases.extend(cases)

    blind_path = SUITE / PARTITION_FILES["blind"]
    if blind_path.is_file():
        blind = load_v2_partition("blind")
        if len(blind) < 100:
            raise SemanticV2Error("blind v2 requires at least 100 cases")
        for case in blind:
            _validate_case(case, "blind", blind=True)
        _validate_blind_contract(blind, manifest)
        counts["blind"] = len(blind)
        all_cases.extend(blind)
    elif require_blind:
        raise SemanticV2Error("blind v2 inputs are not frozen")

    identifiers = [case["case_id"] for case in all_cases]
    if len(identifiers) != len(set(identifiers)):
        raise SemanticV2Error("duplicate v2 case id")
    duplicate = _find_duplicate(all_cases)
    if duplicate is not None:
        raise SemanticV2Error(f"duplicate or near-duplicate prompts: {duplicate[0]} and {duplicate[1]}")
    _validate_migration(manifest)
    _validate_fixture_hashes()
    return {
        "suite_version": "semantic-routing-v2",
        "counts": counts,
        "total_cases": sum(counts.values()),
        "visible_frozen": bool(manifest.get("frozen_visible")),
        "blind_frozen": bool(manifest.get("blind_frozen")),
        "hash_manifest_sha256": sha256_file(manifest_path),
        "hashes": hashes,
        "duplicate_thresholds": {
            "token_jaccard": 0.82,
            "character_trigram_cosine": 0.92,
        },
    }


def run_deterministic_semantic_v2(partitions: tuple[str, ...] | None = None) -> dict[str, Any]:
    """Score typed routing and exposure without making a model call or dispatch."""
    from .modes import parse_agent_mode
    from .routing import HierarchicalRouter, ToolFamily
    from .tool_exposure import LifecyclePhase, ToolExposureAuthority, ToolExposureContext

    selected = partitions or tuple(VISIBLE_MINIMUMS)
    router = HierarchicalRouter()
    authority = ToolExposureAuthority()
    results: list[dict[str, Any]] = []
    for partition in selected:
        for case in load_v2_partition(partition):
            caps = case["capabilities"]
            mode = parse_agent_mode(case["agent_mode"].replace("_", "-"))
            route = router.route_typed(
                case["prompt"], ROOT, mode=mode,
                allow_write=bool(caps["workspace_write"]),
                allow_shell=bool(caps["shell"]),
                allow_network=bool(caps["network"]),
            )
            phase = LifecyclePhase.INSPECTION
            if not route.requires_prior_inspection:
                if route.tool_family == ToolFamily.MUTATION_PROPOSAL:
                    phase = LifecyclePhase.PROPOSAL
                elif route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
                    phase = LifecyclePhase.MUTATION
                elif route.tool_family == ToolFamily.EXECUTION_VERIFICATION:
                    phase = LifecyclePhase.VERIFICATION
                elif route.response_mode.value != "action":
                    phase = LifecyclePhase.ANSWER
            context = ToolExposureContext.build(
                phase=phase, mode=mode, allow_write=bool(caps["workspace_write"]),
                allow_shell=bool(caps["shell"]), prior_inspection=False,
            )
            visible = authority.decide(route, context).visible_tools
            expected = case["expected"]
            checks = {
                "task_class": route.task_class.value == expected["task_class"],
                "specialist": route.specialist.value == expected["specialist"],
                "immediate_tool_family": _immediate_family(route, visible) == expected["immediate_tool_family"],
                "immediate_allowed_tool": (
                    bool(set(visible) & set(expected["allowed_immediate_tools"]))
                    if expected["response_mode"] == "action"
                    else not visible
                ),
                "reason_code": route.reason_code.value == expected["reason_code"],
                "response_mode": route.response_mode.value == expected["response_mode"],
                "risk_level": route.risk_level.value == expected["risk_level"],
                "capability_current": route.is_current_for(context.granted_capabilities, mode.value),
            }
            results.append({
                "case_id": case["case_id"], "partition": partition,
                "checks": checks, "route": route.to_dict(), "visible_tools": list(visible),
            })
    total = len(results)
    fields = tuple(results[0]["checks"]) if results else ()
    metrics = {
        f"{field}_accuracy": sum(item["checks"][field] for item in results) / total if total else 0.0
        for field in fields
    }
    failures = [item for item in results if not all(item["checks"].values())]
    return {
        "suite": "semantic-routing-v2", "metrics_source": "deterministic_router_and_exposure",
        "partitions": list(selected), "passed": total - len(failures), "total": total,
        "metrics": metrics, "failure_count": len(failures), "failures": failures,
    }


def _immediate_family(route: Any, visible_tools: tuple[str, ...]) -> str:
    if visible_tools and route.requires_prior_inspection and set(visible_tools) <= {"read_file", "search_code", "file_summary"}:
        return "file_inspection"
    return route.tool_family.value


def _validate_case(case: Any, partition: str, *, blind: bool) -> None:
    if not isinstance(case, dict):
        raise SemanticV2Error("v2 case must be an object")
    required = BASE_FIELDS if blind else BASE_FIELDS | LABELED_FIELDS
    allowed = required | ({"execution_contract"} if partition == "end_to_end" and not blind else set())
    if set(case) != required and not (set(case) == allowed and "execution_contract" in case):
        raise SemanticV2Error(f"invalid fields in {case.get('case_id', '<unknown>')}")
    if case.get("partition") != partition:
        raise SemanticV2Error(f"partition mismatch in {case.get('case_id')}")
    if case.get("agent_mode") not in {"read_only", "propose", "write_approved", "unsafe"}:
        raise SemanticV2Error(f"invalid mode in {case.get('case_id')}")
    prompt = case.get("prompt")
    if not isinstance(prompt, str) or not 8 <= len(prompt) <= 4096:
        raise SemanticV2Error(f"invalid prompt in {case.get('case_id')}")
    caps = case.get("capabilities")
    if not isinstance(caps, dict) or set(caps) != {"workspace_read", "workspace_write", "shell", "network"}:
        raise SemanticV2Error(f"invalid capabilities in {case.get('case_id')}")
    if not all(isinstance(value, bool) for value in caps.values()):
        raise SemanticV2Error(f"invalid capability values in {case.get('case_id')}")
    if blind:
        if set(case) & LABELED_FIELDS:
            raise SemanticV2Error(f"blind labels leaked in {case.get('case_id')}")
        return

    expected = case.get("expected")
    if not isinstance(expected, dict):
        raise SemanticV2Error(f"missing expected object in {case.get('case_id')}")
    expected_fields = {
        "task_class", "specialist", "immediate_tool_family", "allowed_immediate_tools",
        "terminal_tool_family", "allowed_terminal_tools", "required_lifecycle",
        "allowed_alternative_lifecycles", "response_mode", "user_mutation_goal",
        "immediate_action_side_effect", "terminal_mutation_expected", "risk_level",
        "reason_code",
    }
    if set(expected) != expected_fields:
        raise SemanticV2Error(f"invalid expected fields in {case.get('case_id')}")
    if expected["task_class"] not in TASK_CLASSES or expected["specialist"] not in SPECIALISTS:
        raise SemanticV2Error(f"invalid task or specialist in {case.get('case_id')}")
    if expected["immediate_tool_family"] not in TOOL_FAMILIES or expected["terminal_tool_family"] not in TOOL_FAMILIES | {None}:
        raise SemanticV2Error(f"invalid family in {case.get('case_id')}")
    immediate = _tool_list(expected["allowed_immediate_tools"], case["case_id"])
    terminal = _tool_list(expected["allowed_terminal_tools"], case["case_id"])
    forbidden = _tool_list(case["forbidden_tools"], case["case_id"])
    if (set(immediate) | set(terminal)) & set(forbidden):
        raise SemanticV2Error(f"expected and forbidden tool overlap in {case['case_id']}")
    lifecycle = expected["required_lifecycle"]
    if not isinstance(lifecycle, list):
        raise SemanticV2Error(f"invalid lifecycle in {case['case_id']}")
    for step in lifecycle:
        if not isinstance(step, dict) or set(step) != {"phase", "allowed_tools"}:
            raise SemanticV2Error(f"invalid lifecycle step in {case['case_id']}")
        if step["phase"] not in {"inspection", "proposal", "mutation", "verification", "answer"}:
            raise SemanticV2Error(f"invalid lifecycle phase in {case['case_id']}")
        if not _tool_list(step["allowed_tools"], case["case_id"]):
            raise SemanticV2Error(f"empty lifecycle step in {case['case_id']}")
    if expected["response_mode"] not in {"action", "final_answer", "clarification", "blocked"}:
        raise SemanticV2Error(f"invalid response mode in {case['case_id']}")
    if expected["risk_level"] not in {"low", "medium", "high", "critical"}:
        raise SemanticV2Error(f"invalid risk in {case['case_id']}")
    if not all(isinstance(expected[name], bool) for name in ("user_mutation_goal", "immediate_action_side_effect", "terminal_mutation_expected")):
        raise SemanticV2Error(f"invalid mutation split in {case['case_id']}")
    if expected["immediate_action_side_effect"] != any(tool in SIDE_EFFECT_TOOLS for tool in immediate):
        raise SemanticV2Error(f"immediate side-effect contradiction in {case['case_id']}")
    if not caps["workspace_write"] and set(immediate) & LIVE_MUTATION_TOOLS:
        raise SemanticV2Error(f"immediate write without capability in {case['case_id']}")
    if not caps["shell"] and set(immediate) & SHELL_TOOLS:
        raise SemanticV2Error(f"immediate shell without capability in {case['case_id']}")
    if expected["response_mode"] != "action" and (immediate or lifecycle):
        raise SemanticV2Error(f"non-action case exposes lifecycle tools in {case['case_id']}")
    if expected["terminal_tool_family"] is None and terminal:
        raise SemanticV2Error(f"terminal tools without terminal family in {case['case_id']}")
    if expected["terminal_tool_family"] is not None and (not terminal or len(lifecycle) < 2):
        raise SemanticV2Error(f"terminal family lacks sequence in {case['case_id']}")


def _tool_list(value: Any, case_id: str) -> list[str]:
    if not isinstance(value, list) or len(value) != len(set(value)) or not set(value) <= TOOLS:
        raise SemanticV2Error(f"invalid tool list in {case_id}")
    return value


def _validate_migration(manifest: dict[str, Any]) -> None:
    report_path = SUITE / "migration_report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    if report.get("migration_count") != 200 or len(report.get("migrations", [])) != 200:
        raise SemanticV2Error("migration report must document all 200 v1 cases")
    contradictions = report.get("contradictory_v1_case_ids")
    if not isinstance(contradictions, list) or len(contradictions) != 16:
        raise SemanticV2Error("migration report must identify all 16 contradictions")
    for entry in report["migrations"]:
        required = {
            "old_case_id", "new_case_id", "old_label", "new_label", "reason",
            "old_label_issue", "reviewer_identity_or_process", "timestamp",
            "source_dataset_hash", "destination_dataset_hash",
            "independent_semantic_review",
        }
        if set(entry) != required:
            raise SemanticV2Error(f"incomplete migration entry: {entry.get('old_case_id')}")
        if entry["old_case_id"] in contradictions and not isinstance(entry["independent_semantic_review"], dict):
            raise SemanticV2Error(f"contradiction lacks semantic review: {entry['old_case_id']}")
    if manifest["hashes"].get("migration_report.json") != sha256_file(report_path):
        raise SemanticV2Error("migration report hash mismatch")


def _validate_blind_contract(blind: list[dict[str, Any]], manifest: dict[str, Any]) -> None:
    contract_path = SUITE / "blind_evaluator_contract.json"
    hash_path = SUITE / "blind_inputs.sha256"
    if not contract_path.is_file() or not hash_path.is_file():
        raise SemanticV2Error("blind evaluator contract or input hash is missing")
    expected = hash_path.read_text(encoding="utf-8").strip()
    actual = sha256_file(SUITE / "blind_inputs.json")
    if expected != actual or manifest["hashes"].get("blind_inputs.json") != actual:
        raise SemanticV2Error("blind input hash mismatch")
    contract = json.loads(contract_path.read_text(encoding="utf-8"))
    if contract.get("blind_inputs_sha256") != actual or contract.get("case_count") != len(blind):
        raise SemanticV2Error("blind contract identity mismatch")
    if contract.get("labels_stored_in_repository") is not False:
        raise SemanticV2Error("blind contract does not prohibit repository labels")
    if manifest.get("blind_frozen") is not True:
        raise SemanticV2Error("blind inputs exist but are not marked frozen")


def _validate_fixture_hashes() -> None:
    for case in load_v2_partition("end_to_end"):
        fixture = SUITE / str(case["workspace_fixture"])
        if not fixture.is_dir() or not any(path.is_file() for path in fixture.rglob("*")):
            raise SemanticV2Error(f"missing fixture: {case['case_id']}")


def _tokens(prompt: str) -> set[str]:
    return set(re.findall(r"[a-z0-9_]+", prompt.lower()))


def _trigrams(prompt: str) -> dict[str, int]:
    normalized = re.sub(r"\s+", " ", prompt.lower()).strip()
    grams: dict[str, int] = {}
    for index in range(max(0, len(normalized) - 2)):
        gram = normalized[index:index + 3]
        grams[gram] = grams.get(gram, 0) + 1
    return grams


def _cosine(left: dict[str, int], right: dict[str, int]) -> float:
    numerator = sum(value * right.get(key, 0) for key, value in left.items())
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    return numerator / (left_norm * right_norm) if left_norm and right_norm else 0.0


def _find_duplicate(cases: list[dict[str, Any]]) -> tuple[str, str] | None:
    """Reject exact duplicates globally and near duplicates touching blind data.

    The visible v2 corpus intentionally preserves historical v1 prompts and adds
    controlled lifecycle variants, so similarity alone is not an integrity
    failure there.  Blind prompts are new material: every blind/visible and
    blind/blind pair is subject to the documented lexical plus character test.
    """
    seen: list[tuple[str, str, str, set[str], dict[str, int]]] = []
    for case in cases:
        prompt = " ".join(case["prompt"].lower().split())
        tokens = _tokens(prompt)
        trigrams = _trigrams(prompt)
        partition = str(case["partition"])
        for other_id, other_partition, other_prompt, other_tokens, other_trigrams in seen:
            if prompt == other_prompt:
                return other_id, case["case_id"]
            if "blind" not in {partition, other_partition}:
                continue
            union = tokens | other_tokens
            jaccard = len(tokens & other_tokens) / len(union) if union else 0.0
            if jaccard >= 0.82 and _cosine(trigrams, other_trigrams) >= 0.92:
                return other_id, case["case_id"]
        seen.append((case["case_id"], partition, prompt, tokens, trigrams))
    return None
