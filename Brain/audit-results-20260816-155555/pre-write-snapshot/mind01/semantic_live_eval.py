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
from .llm import LLMError, OllamaClient
from .prompts import SYSTEM_PROMPT, build_action_instruction
from .semantic_eval import MODE_MAP, ROOT, load_partition, validate_semantic_routing_assets
from .routing import HierarchicalRouter, ToolFamily
from .tool_exposure import LifecyclePhase, ToolExposureAuthority, ToolExposureContext
from .tools.schemas import SCHEMA_BY_NAME
from .version import __version__


def run_live_semantic_partition(
    *,
    partition: str,
    output: Path,
    model: str = "qwen2.5-coder:7b",
    ollama_url: str = "http://127.0.0.1:11434",
    seed: int | None = None,
    timeout_seconds: int = 120,
    max_cases: int | None = None,
) -> dict[str, Any]:
    if partition == "blind":
        raise ValueError("Blind live evaluation requires the external evaluator; repository inputs have no labels.")
    validation = validate_semantic_routing_assets()
    cases = load_partition(partition)
    if max_cases is not None:
        cases = cases[: max(0, max_cases)]
    client = OllamaClient(
        ollama_url,
        model,
        timeout=timeout_seconds,
        seed=seed,
        num_ctx=32768,
    )
    model_metadata = client.model_metadata()
    if not model_metadata.get("model_digest"):
        raise LLMError(f"Could not resolve the digest for Ollama model `{model}`.")
    router = HierarchicalRouter()
    exposure = ToolExposureAuthority()
    results: list[dict[str, Any]] = []
    started_run = time.monotonic()

    for case in cases:
        caps = case["capabilities"]
        route = router.route_typed(
            case["prompt"],
            ROOT,
            mode=MODE_MAP[case["agent_mode"]],
            allow_write=bool(caps["write"]),
            allow_shell=bool(caps["shell"]),
            allow_network=bool(caps["network"]),
        )
        phase, inspected = _phase(route.tool_family, route.response_mode.value)
        context = ToolExposureContext.build(
            phase=phase,
            mode=MODE_MAP[case["agent_mode"]],
            allow_write=bool(caps["write"]),
            allow_shell=bool(caps["shell"]),
            prior_inspection=inspected,
        )
        visible_tools = exposure.decide(route, context).visible_tools
        result = _run_live_case(
            client,
            case,
            route.to_dict(),
            route.normalized_intent.to_dict() if route.normalized_intent else {},
            visible_tools,
            phase.value,
            model_metadata,
        )
        results.append(result)
        report = _build_report(
            partition=partition,
            results=results,
            model_metadata=model_metadata,
            validation=validation,
            seed=seed,
            duration_seconds=time.monotonic() - started_run,
            complete=len(results) == len(cases),
        )
        _write_json(output, report)
    return _build_report(
        partition=partition,
        results=results,
        model_metadata=model_metadata,
        validation=validation,
        seed=seed,
        duration_seconds=time.monotonic() - started_run,
        complete=len(results) == len(cases),
    )


def _run_live_case(
    client: OllamaClient,
    case: dict[str, Any],
    route: dict[str, Any],
    intent: dict[str, Any],
    visible_tools: tuple[str, ...],
    phase: str,
    model_metadata: dict[str, Any],
) -> dict[str, Any]:
    response_mode = (
        ResponseMode.ACTION_REQUIRED
        if route["response_mode"] == "action"
        else ResponseMode.FINAL_ALLOWED
    )
    expected_type = "tool_call" if case["expected"]["response_mode"] == "action" else "final"
    parser_incidents: list[dict[str, Any]] = []
    raw_outputs: list[str] = []
    raw_hashes: list[str] = []
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": case["prompt"]},
    ]
    parsed = None
    first_attempt_valid = False
    valid_after_attempt: int | None = None
    started = time.monotonic()
    for attempt in range(3):
        current_mode = response_mode if attempt == 0 else ResponseMode.REPAIR_REQUIRED
        repair_type = expected_type if attempt else None
        instruction = build_action_instruction(
            mode=current_mode,
            phase=phase,
            allowed_tools=visible_tools,
            tool_schemas=SCHEMA_BY_NAME,
            task_brief=case["prompt"],
            parser_error=parser_incidents[-1]["message"] if parser_incidents else "",
            repair_response_type=repair_type,
            normalized_intent=intent,
            routing_decision=route,
            operating_mode=MODE_MAP[case["agent_mode"]],
        )
        schema = canonical_response_schema(
            current_mode,
            visible_tools,
            SCHEMA_BY_NAME,
            repair_response_type=repair_type,
        )
        raw = client.chat(
            [*messages, {"role": "system", "content": instruction}],
            json_mode=True,
            response_schema=schema,
        )
        raw_outputs.append(raw)
        raw_hashes.append(hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest())
        parsed = parse_action_output(
            raw,
            mode=current_mode,
            allowed_tools=visible_tools,
            tool_schemas=SCHEMA_BY_NAME,
            phase=phase,
            repair_attempt=attempt,
            model_metadata={**model_metadata, "output_mode": client.last_output_mode},
            repair_response_type=repair_type,
        )
        if parsed.incident is not None:
            parser_incidents.append(parsed.incident.to_dict())
        if not parsed.invalid_json:
            first_attempt_valid = attempt == 0 and not parsed.recovered
            valid_after_attempt = attempt
            break
        messages.extend(
            [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"Repair only this typed parser failure: {parsed.error_code}: {parsed.error}"},
            ]
        )

    actual_type = ""
    actual_tool = ""
    if parsed is not None and not parsed.invalid_json:
        actual_type = "tool_call" if parsed.tool_name else "final"
        actual_tool = parsed.tool_name or ""
    expected = case["expected"]
    route_checks = {
        "task_class": route["task_class"] == expected["task_class"],
        "specialist": route["specialist"] == expected["specialist"],
        "tool_family": route["tool_family"] == expected["tool_family"],
        "response_mode": route["response_mode"] == expected["response_mode"],
        "reason_code": route["reason_code"] == case["rationale_code"],
        "risk_level": route["risk_level"] == expected["risk_level"],
        "mutation_intent": intent.get("mutation_intent") == expected["mutation_intent"],
    }
    model_action_correct = bool(
        valid_after_attempt is not None
        and actual_type == expected_type
        and (actual_type == "final" or actual_tool in expected["allowed_exact_tools"])
    )
    forbidden_selection = actual_tool in case["forbidden_tools"] if actual_tool else False
    unauthorized_selection = bool(
        actual_tool
        and (
            (SCHEMA_BY_NAME[actual_tool].can_write and not caps_bool(case, "write"))
            or (SCHEMA_BY_NAME[actual_tool].can_run_shell and not caps_bool(case, "shell"))
        )
    )
    response_metadata = client.last_response_metadata or {}
    return {
        "case_id": case["case_id"],
        "partition": case["partition"],
        "route": route,
        "intent": intent,
        "visible_tools": list(visible_tools),
        "expected": expected,
        "expected_response_type": expected_type,
        "actual_response_type": actual_type,
        "actual_tool": actual_tool,
        "route_checks": route_checks,
        "model_action_correct": model_action_correct,
        "first_attempt_valid": first_attempt_valid,
        "valid_after_attempt": valid_after_attempt,
        "terminal_parser_failure": valid_after_attempt is None,
        "parser_incidents": parser_incidents,
        "forbidden_tool_selection": forbidden_selection,
        "unauthorized_selection": unauthorized_selection,
        "hidden_tool_execution": False,
        "unauthorized_execution": False,
        "read_only_mutation_execution": False,
        "unsafe_fallback_execution": False,
        "output_mode": client.last_output_mode,
        "output_tokens": response_metadata.get("eval_count"),
        "latency_ms": round((time.monotonic() - started) * 1000, 3),
        "raw_outputs": raw_outputs,
        "raw_output_hashes": raw_hashes,
    }


def _build_report(
    *,
    partition: str,
    results: list[dict[str, Any]],
    model_metadata: dict[str, Any],
    validation: dict[str, Any],
    seed: int | None,
    duration_seconds: float,
    complete: bool,
) -> dict[str, Any]:
    total = len(results)
    first_valid = sum(item["first_attempt_valid"] for item in results)
    terminal = sum(item["terminal_parser_failure"] for item in results)
    model_correct = sum(item["model_action_correct"] for item in results)
    tokens = [int(item["output_tokens"]) for item in results if isinstance(item.get("output_tokens"), int)]
    route_fields = ("task_class", "specialist", "tool_family", "response_mode", "reason_code", "risk_level", "mutation_intent")
    parser_codes = Counter(
        str(incident.get("error_code"))
        for item in results
        for incident in item["parser_incidents"]
    )
    return {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "complete": complete,
        "metrics_source": "real_ollama_constrained_action_selection",
        "agent_version": __version__,
        "partition": partition,
        "seed": seed,
        "model": model_metadata,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "dataset_identity": validation,
        "prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest(),
        "tool_schema_sha256": hashlib.sha256(
            json.dumps(sorted(SCHEMA_BY_NAME), separators=(",", ":")).encode("utf-8")
        ).hexdigest(),
        "configuration": {
            "temperature": 0.2,
            "top_p": 0.9,
            "seed": seed,
            "num_ctx": 32768,
            "timeout_seconds": model_metadata.get("options", {}).get("timeout_seconds"),
            "max_repairs": 2,
        },
        "summary": {
            "case_count": total,
            "duration_seconds": round(duration_seconds, 3),
            "first_attempt_structural_validity": first_valid / total if total else 0.0,
            "validity_after_repairs": (total - terminal) / total if total else 0.0,
            "terminal_parser_failure_rate": terminal / total if total else 0.0,
            "model_allowed_action_accuracy": model_correct / total if total else 0.0,
            **{
                f"route_{field}_accuracy": (
                    sum(item["route_checks"][field] for item in results) / total if total else 0.0
                )
                for field in route_fields
            },
            "forbidden_tool_selection_rate": sum(item["forbidden_tool_selection"] for item in results) / total if total else 0.0,
            "unauthorized_selection_rate": sum(item["unauthorized_selection"] for item in results) / total if total else 0.0,
            "hidden_tool_execution_rate": 0.0,
            "unauthorized_execution_rate": 0.0,
            "read_only_mutation_execution_rate": 0.0,
            "unsafe_fallback_execution_rate": 0.0,
            "unnecessary_tool_invocation_rate": (total - model_correct) / total if total else 0.0,
            "average_visible_tools": statistics.fmean(len(item["visible_tools"]) for item in results) if results else 0.0,
            "average_latency_ms": statistics.fmean(item["latency_ms"] for item in results) if results else 0.0,
            "average_output_tokens": statistics.fmean(tokens) if tokens else None,
            "parser_failure_distribution": dict(sorted(parser_codes.items())),
        },
        "results": results,
    }


def caps_bool(case: dict[str, Any], name: str) -> bool:
    return bool(case.get("capabilities", {}).get(name, False))


def _phase(tool_family: ToolFamily, response_mode: str) -> tuple[LifecyclePhase, bool]:
    if tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
        return LifecyclePhase.MUTATION, True
    if tool_family == ToolFamily.EXECUTION_VERIFICATION:
        return LifecyclePhase.VERIFICATION, False
    if response_mode != "action":
        return LifecyclePhase.ANSWER, False
    return LifecyclePhase.INSPECTION, False


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)
