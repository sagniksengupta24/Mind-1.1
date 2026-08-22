from __future__ import annotations

import hashlib
import json
import platform
import statistics
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .action_parser import ResponseMode, canonical_response_schema, parse_action_output
from .intent import Capability
from .llm import LLMError, OllamaClient
from .modes import parse_agent_mode
from .prompts import SYSTEM_PROMPT, build_action_instruction
from .routing import HierarchicalRouter, ToolFamily
from .semantic_eval_v2 import SUITE, _immediate_family, load_v2_partition, sha256_file, validate_semantic_routing_v2
from .tool_exposure import LifecyclePhase, ToolExposureAuthority, ToolExposureContext
from .tools.schemas import SCHEMA_BY_NAME
from .version import __version__


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODEL_DIGEST = "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364"


def run_live_semantic_v2(
    *,
    partition: str,
    output: Path,
    model: str = "qwen2.5-coder:7b",
    ollama_url: str = "http://127.0.0.1:11434",
    seed: int | None = None,
    timeout_seconds: int = 120,
    max_cases: int | None = None,
    external_blind_labels: Path | None = None,
) -> dict[str, Any]:
    validation = validate_semantic_routing_v2(require_blind=True)
    blind = partition == "blind"
    if blind:
        if external_blind_labels is None:
            raise ValueError("blind scoring requires an external read-only label package")
        cases, label_identity = _mount_blind_labels(external_blind_labels)
    else:
        cases = load_v2_partition(partition)
        label_identity = None
    if max_cases is not None:
        cases = cases[:max_cases]
    client = OllamaClient(ollama_url, model, timeout=timeout_seconds, seed=seed, num_ctx=32768)
    metadata = client.model_metadata()
    if metadata.get("model_digest") != EXPECTED_MODEL_DIGEST:
        raise LLMError(f"model digest mismatch: {metadata.get('model_digest') or '<missing>'}")
    router = HierarchicalRouter()
    authority = ToolExposureAuthority()
    results: list[dict[str, Any]] = []
    started = time.monotonic()
    for case in cases:
        results.append(_run_case(client, router, authority, case, metadata, blind=blind))
        metadata["output_mode"] = client.last_output_mode
        _write(output, _report(partition, results, metadata, validation, label_identity, seed, time.monotonic() - started, len(results) == len(cases)))
    return _report(partition, results, metadata, validation, label_identity, seed, time.monotonic() - started, len(results) == len(cases))


def _run_case(client: OllamaClient, router: HierarchicalRouter, authority: ToolExposureAuthority, case: dict[str, Any], metadata: dict[str, Any], *, blind: bool) -> dict[str, Any]:
    caps = case["capabilities"]
    mode = parse_agent_mode(case["agent_mode"].replace("_", "-"))
    route = router.route_typed(
        case["prompt"], ROOT, mode=mode,
        allow_write=bool(caps["workspace_write"]), allow_shell=bool(caps["shell"]),
        allow_network=bool(caps["network"]), prior_inspection=False,
    )
    phase = _phase(route)
    context = ToolExposureContext.build(
        phase=phase, mode=mode, allow_write=bool(caps["workspace_write"]),
        allow_shell=bool(caps["shell"]), prior_inspection=False,
    )
    exposure = authority.decide(route, context)
    expected = case["expected"]
    expected_type = "tool_call" if expected["response_mode"] == "action" else "final"
    raw_outputs: list[str] = []
    instruction_hashes: list[str] = []
    response_schema_hashes: list[str] = []
    incidents: list[dict[str, Any]] = []
    parsed = None
    first_valid = False
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": case["prompt"]}]
    for attempt in range(3):
        initial_mode = ResponseMode.ACTION_REQUIRED if route.response_mode.value == "action" and exposure.visible_tools else ResponseMode.FINAL_ALLOWED
        response_mode = initial_mode if attempt == 0 else ResponseMode.REPAIR_REQUIRED
        repair_type = expected_type if attempt else None
        instruction = build_action_instruction(
            mode=response_mode, phase=phase.value, allowed_tools=exposure.visible_tools,
            tool_schemas=SCHEMA_BY_NAME, task_brief=case["prompt"],
            parser_error=incidents[-1]["message"] if incidents else "",
            repair_response_type=repair_type,
            normalized_intent=route.normalized_intent.to_dict() if route.normalized_intent else {},
            routing_decision=route.to_dict(), operating_mode=mode,
        )
        response_schema = canonical_response_schema(
            response_mode,
            exposure.visible_tools,
            SCHEMA_BY_NAME,
            repair_response_type=repair_type,
        )
        instruction_hashes.append(hashlib.sha256(instruction.encode("utf-8")).hexdigest())
        response_schema_hashes.append(_json_hash(response_schema))
        raw = client.chat(
            [*messages, {"role": "system", "content": instruction}], json_mode=True,
            response_schema=response_schema,
        )
        raw_outputs.append(raw)
        parsed = parse_action_output(
            raw, mode=response_mode, allowed_tools=exposure.visible_tools,
            tool_schemas=SCHEMA_BY_NAME, phase=phase.value, repair_attempt=attempt,
            model_metadata={**metadata, "output_mode": client.last_output_mode}, repair_response_type=repair_type,
        )
        if parsed.incident:
            incidents.append(parsed.incident.to_dict())
        if not parsed.invalid_json:
            first_valid = attempt == 0 and not parsed.recovered
            break
        messages.extend((
            {"role": "assistant", "content": raw},
            {"role": "user", "content": f"Repair only typed parser failure {parsed.error_code}: {parsed.error}"},
        ))
    actual_type = ""
    actual_tool = ""
    terminal_failure = parsed is None or parsed.invalid_json
    if not terminal_failure:
        actual_type = "tool_call" if parsed.tool_name else "final"
        actual_tool = parsed.tool_name or ""
    checks = {
        "task_class": route.task_class.value == expected["task_class"],
        "specialist": route.specialist.value == expected["specialist"],
        "immediate_tool_family": _immediate_family(route, exposure.visible_tools) == expected["immediate_tool_family"],
        "immediate_allowed_tool": actual_type == expected_type and (actual_type == "final" or actual_tool in expected["allowed_immediate_tools"]),
        "reason_code": route.reason_code.value == expected["reason_code"],
        "response_mode": route.response_mode.value == expected["response_mode"],
        "risk_level": route.risk_level.value == expected["risk_level"],
        "valid_first_lifecycle_action": actual_type == expected_type and (not expected["required_lifecycle"] or actual_tool in expected["required_lifecycle"][0]["allowed_tools"]),
        "capability_current": route.is_current_for(context.granted_capabilities, mode.value),
        "mode_current": route.is_current_for(context.granted_capabilities, mode.value),
    }
    unauthorized = bool(actual_tool and (
        (SCHEMA_BY_NAME[actual_tool].can_write and not caps["workspace_write"])
        or (SCHEMA_BY_NAME[actual_tool].can_run_shell and not caps["shell"])
        or actual_tool not in exposure.visible_tools
    ))
    result = {
        "case_id": case["case_id"], "partition": partition_name(case),
        "agent_mode": case["agent_mode"], "capabilities": dict(caps),
        "route": route.to_dict(), "visible_tools": list(exposure.visible_tools),
        "actual_response_type": actual_type, "actual_tool": actual_tool,
        "checks": checks, "first_attempt_valid": first_valid,
        "terminal_parser_failure": terminal_failure, "parser_incidents": incidents,
        "forbidden_tool_selection": actual_tool in case["forbidden_tools"] if actual_tool else False,
        "unauthorized_selection": unauthorized, "hidden_tool_selection": bool(actual_tool and actual_tool not in exposure.visible_tools),
        "raw_outputs": raw_outputs, "raw_output_hashes": [hashlib.sha256(item.encode()).hexdigest() for item in raw_outputs],
        "instruction_hashes": instruction_hashes,
        "response_schema_hashes": response_schema_hashes,
    }
    if not blind:
        result["expected"] = expected
    return result


def _mount_blind_labels(path: Path) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    resolved = path.resolve()
    if resolved == ROOT or ROOT in resolved.parents:
        raise ValueError("blind labels must remain outside the repository")
    contract = json.loads((SUITE / "blind_evaluator_contract.json").read_text(encoding="utf-8"))
    provenance_path = resolved.with_name("label_provenance.json")
    if not provenance_path.is_file():
        raise ValueError("external blind label provenance is missing")
    provenance = json.loads(provenance_path.read_text(encoding="utf-8"))
    if provenance.get("blind_inputs_sha256") != contract["blind_inputs_sha256"]:
        raise ValueError("external labels do not bind the frozen blind inputs")
    if sha256_file(resolved) != provenance.get("label_sha256"):
        raise ValueError("external blind label hash mismatch")
    labeled = json.loads(resolved.read_text(encoding="utf-8"))["cases"]
    inputs = load_v2_partition("blind")
    if len(labeled) != len(inputs):
        raise ValueError("blind label/input count mismatch")
    by_id = {case["case_id"]: case for case in labeled}
    merged: list[dict[str, Any]] = []
    for item in inputs:
        label = by_id.get(item["case_id"])
        if label is None:
            raise ValueError("blind label case id mismatch")
        for key in item:
            if label.get(key) != item[key]:
                raise ValueError(f"blind input mismatch for {item['case_id']}")
        merged.append(label)
    return merged, {"sha256": sha256_file(resolved), "case_count": len(merged), "path_excluded_from_report": True}


def _phase(route: Any) -> LifecyclePhase:
    if route.requires_prior_inspection:
        return LifecyclePhase.INSPECTION
    if route.tool_family == ToolFamily.MUTATION_PROPOSAL:
        return LifecyclePhase.PROPOSAL
    if route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
        return LifecyclePhase.MUTATION
    if route.tool_family == ToolFamily.EXECUTION_VERIFICATION:
        return LifecyclePhase.VERIFICATION
    if route.response_mode.value != "action":
        return LifecyclePhase.ANSWER
    return LifecyclePhase.INSPECTION


def _report(partition: str, results: list[dict[str, Any]], metadata: dict[str, Any], validation: dict[str, Any], label_identity: dict[str, Any] | None, seed: int | None, duration: float, complete: bool) -> dict[str, Any]:
    total = len(results)
    fields = tuple(next(iter(results))["checks"]) if results else ()
    codes = Counter(incident["error_code"] for item in results for incident in item["parser_incidents"])
    return {
        "schema_version": "2.0", "generated_at": datetime.now(timezone.utc).isoformat(),
        "complete": complete, "metrics_source": "real_ollama_v2_immediate_selection",
        "agent_version": __version__, "partition": partition, "seed": seed, "model": metadata,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "dataset_identity": validation, "external_label_identity": label_identity,
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "tool_schema_source_sha256": sha256_file(ROOT / "mind01" / "tools" / "schemas.py"),
        "canonical_schema_source_sha256": sha256_file(ROOT / "mind01" / "action_parser.py"),
        "summary": {
            "case_count": total, "duration_seconds": round(duration, 3),
            "first_attempt_structural_validity": sum(item["first_attempt_valid"] for item in results) / total if total else 0.0,
            "terminal_parser_failure_rate": sum(item["terminal_parser_failure"] for item in results) / total if total else 0.0,
            **{f"{field}_accuracy": sum(item["checks"][field] for item in results) / total if total else 0.0 for field in fields},
            "forbidden_tool_selection_rate": sum(item["forbidden_tool_selection"] for item in results) / total if total else 0.0,
            "unauthorized_selection_rate": sum(item["unauthorized_selection"] for item in results) / total if total else 0.0,
            "hidden_tool_selection_rate": sum(item["hidden_tool_selection"] for item in results) / total if total else 0.0,
            "unknown_tool_selection_rate": 0.0,
            "average_visible_tools": statistics.fmean(len(item["visible_tools"]) for item in results) if results else 0.0,
            "parser_failure_distribution": dict(sorted(codes.items())),
        },
        "results": results,
    }


def partition_name(case: dict[str, Any]) -> str:
    return str(case["partition"])


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _json_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
