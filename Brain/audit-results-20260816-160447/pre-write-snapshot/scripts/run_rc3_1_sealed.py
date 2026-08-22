"""Run the frozen RC2 semantic-routing protocol on RC3.1 public inputs only."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from mind01.action_parser import ResponseMode, canonical_response_schema, parse_action_output
from mind01.llm import LLMError, OllamaClient
from mind01.modes import parse_agent_mode
from mind01.prompts import SYSTEM_PROMPT, build_action_instruction
from mind01.routing import HierarchicalRouter, ToolFamily
from mind01.semantic_eval_v2 import _immediate_family
from mind01.tool_exposure import LifecyclePhase, ToolExposureAuthority, ToolExposureContext
from mind01.tools.schemas import SCHEMA_BY_NAME
from mind01.version import __version__

from rc3_1_pipeline import FREEZE_PATH, load_json, runtime_manifest, digest_json, sha256


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODEL_DIGEST = "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Execute sealed RC3.1 public inputs without mounting private labels"
    )
    parser.add_argument("--public-inputs", required=True)
    parser.add_argument("--seal-manifest", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--model", default="qwen2.5-coder:7b")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument("--seed", type=int, default=11103)
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    report = run_public_inputs(
        public_inputs=Path(args.public_inputs),
        seal_manifest=Path(args.seal_manifest),
        output_dir=Path(args.output_dir),
        model=args.model,
        ollama_url=args.ollama_url,
        seed=args.seed,
        timeout=args.timeout,
        resume=args.resume,
    )
    print(json.dumps({"complete": report["complete"], "completed_case_count": report["completed_case_count"]}, indent=2))
    return 0


def run_public_inputs(
    *, public_inputs: Path, seal_manifest: Path, output_dir: Path,
    model: str, ollama_url: str, seed: int, timeout: int, resume: bool,
) -> dict[str, Any]:
    public_inputs = public_inputs.resolve()
    seal_manifest = seal_manifest.resolve()
    output_dir = output_dir.resolve()
    payload = load_json(public_inputs)
    seal = load_json(seal_manifest)
    freeze = load_json(FREEZE_PATH)
    if sha256(public_inputs) != seal["public_input_sha256"]:
        raise RuntimeError("public inputs do not match the sealed identity")
    if payload.get("case_count") != 120 or len(payload.get("cases", [])) != 120:
        raise RuntimeError("sealed execution requires exactly 120 public cases")
    if digest_json(runtime_manifest()) != freeze["runtime_manifest_sha256"]:
        raise RuntimeError("runtime drift blocks sealed execution")
    report_path = output_dir / "report.json"
    raw_dir = output_dir / "raw_outputs"
    if output_dir.exists() and not resume:
        raise FileExistsError(f"refusing to overwrite existing execution: {output_dir}")
    output_dir.mkdir(parents=True, exist_ok=True)
    raw_dir.mkdir(exist_ok=True)
    prior = load_json(report_path) if report_path.exists() else None
    if prior and prior["public_input_sha256"] != sha256(public_inputs):
        raise RuntimeError("resume input identity mismatch")
    results = list(prior.get("results", [])) if prior else []
    completed = {item["case_id"] for item in results}
    client = OllamaClient(ollama_url, model, timeout=timeout, seed=seed, num_ctx=32768)
    metadata = client.model_metadata()
    if metadata.get("model_digest") != EXPECTED_MODEL_DIGEST:
        raise LLMError(f"model digest mismatch: {metadata.get('model_digest') or '<missing>'}")
    started_at = prior.get("started_at") if prior else now()
    started = time.monotonic()
    router = HierarchicalRouter()
    authority = ToolExposureAuthority()
    for case in payload["cases"]:
        if case["case_id"] in completed:
            continue
        result, raw = run_case(client, router, authority, case, metadata)
        raw_path = raw_dir / f"{case['case_id']}.json"
        write_new_json(raw_path, raw)
        result["raw_output_file_sha256"] = sha256(raw_path)
        results.append(result)
        report = execution_report(
            results, metadata, public_inputs, seal_manifest, seal, freeze,
            model, ollama_url, seed, timeout, started_at, time.monotonic() - started,
        )
        write_atomic(report_path, report)
    return execution_report(
        results, metadata, public_inputs, seal_manifest, seal, freeze,
        model, ollama_url, seed, timeout, started_at, time.monotonic() - started,
    )


def run_case(
    client: OllamaClient,
    router: HierarchicalRouter,
    authority: ToolExposureAuthority,
    case: dict[str, Any],
    metadata: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    caps = case["capabilities"]
    mode = parse_agent_mode(case["agent_mode"].replace("_", "-"))
    route = router.route_typed(
        case["prompt"], ROOT, mode=mode,
        allow_write=bool(caps["workspace_write"]), allow_shell=bool(caps["shell"]),
        allow_network=bool(caps["network"]), prior_inspection=False,
    )
    phase = phase_for(route)
    context = ToolExposureContext.build(
        phase=phase, mode=mode, allow_write=bool(caps["workspace_write"]),
        allow_shell=bool(caps["shell"]), prior_inspection=False,
    )
    exposure = authority.decide(route, context)
    expected_type = "tool_call" if route.response_mode.value == "action" and exposure.visible_tools else "final"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": case["prompt"]}]
    raws: list[str] = []
    incidents: list[dict[str, Any]] = []
    parsed = None
    error: str | None = None
    for attempt in range(3):
        response_mode = (
            ResponseMode.ACTION_REQUIRED if expected_type == "tool_call" else ResponseMode.FINAL_ALLOWED
        ) if attempt == 0 else ResponseMode.REPAIR_REQUIRED
        instruction = build_action_instruction(
            mode=response_mode, phase=phase.value, allowed_tools=exposure.visible_tools,
            tool_schemas=SCHEMA_BY_NAME, task_brief=case["prompt"],
            parser_error=incidents[-1]["message"] if incidents else "",
            repair_response_type=expected_type if attempt else None,
            normalized_intent=route.normalized_intent.to_dict() if route.normalized_intent else {},
            routing_decision=route.to_dict(), operating_mode=mode,
        )
        schema = canonical_response_schema(
            response_mode, exposure.visible_tools, SCHEMA_BY_NAME,
            repair_response_type=expected_type if attempt else None,
        )
        try:
            raw = client.chat(
                [*messages, {"role": "system", "content": instruction}],
                json_mode=True, response_schema=schema,
            )
        except LLMError as exc:
            error = str(exc)
            break
        raws.append(raw)
        parsed = parse_action_output(
            raw, mode=response_mode, allowed_tools=exposure.visible_tools,
            tool_schemas=SCHEMA_BY_NAME, phase=phase.value, repair_attempt=attempt,
            model_metadata={**metadata, "output_mode": client.last_output_mode},
            repair_response_type=expected_type if attempt else None,
        )
        if parsed.incident:
            incidents.append(parsed.incident.to_dict())
        if not parsed.invalid_json:
            break
        messages.extend((
            {"role": "assistant", "content": raw},
            {"role": "user", "content": f"Repair only typed parser failure {parsed.error_code}: {parsed.error}"},
        ))
    terminal_failure = parsed is None or parsed.invalid_json
    actual_tool = "" if terminal_failure else (parsed.tool_name or "")
    actual_type = "" if terminal_failure else ("tool_call" if actual_tool else "final")
    unauthorized = bool(actual_tool and (
        actual_tool not in exposure.visible_tools
        or (SCHEMA_BY_NAME[actual_tool].can_write and not caps["workspace_write"])
        or (SCHEMA_BY_NAME[actual_tool].can_run_shell and not caps["shell"])
    ))
    result = {
        "case_id": case["case_id"],
        "route": route.to_dict(),
        "immediate_tool_family": _immediate_family(route, exposure.visible_tools),
        "visible_tools": list(exposure.visible_tools),
        "actual_response_type": actual_type,
        "actual_tool": actual_tool,
        "first_attempt_valid": len(raws) == 1 and not terminal_failure and not parsed.recovered,
        "terminal_parser_failure": terminal_failure,
        "parser_incidents": incidents,
        "unauthorized_selection": unauthorized,
        "unsafe_action": unauthorized,
        "error": error,
        "timed_out": bool(error and "timed out" in error.casefold()),
    }
    raw_record = {
        "case_id": case["case_id"],
        "raw_outputs": raws,
        "raw_output_hashes": [hashlib.sha256(item.encode()).hexdigest() for item in raws],
    }
    return result, raw_record


def phase_for(route: Any) -> LifecyclePhase:
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


def execution_report(
    results: list[dict[str, Any]], metadata: dict[str, Any], public_inputs: Path,
    seal_manifest: Path, seal: dict[str, Any], freeze: dict[str, Any], model: str,
    ollama_url: str, seed: int, timeout: int, started_at: str, duration: float,
) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "protocol": "unchanged-rc2-semantic-selection",
        "complete": len(results) == 120,
        "completed_case_count": len(results),
        "started_at": started_at,
        "finished_at": now() if len(results) == 120 else None,
        "duration_seconds_current_process": round(duration, 3),
        "execution_commit": git_head(),
        "runtime_frozen_commit": freeze["runtime_frozen_commit"],
        "runtime_manifest_sha256": digest_json(runtime_manifest()),
        "agent_version": __version__,
        "model": metadata,
        "configuration": {"model": model, "ollama_url": ollama_url, "seed": seed, "timeout": timeout, "num_ctx": 32768},
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "public_input_sha256": sha256(public_inputs),
        "seal_manifest_sha256": sha256(seal_manifest),
        "seal_package_content_sha256": seal["package_content_sha256"],
        "private_labels_mounted": False,
        "raw_outputs_stored_separately": True,
        "unauthorized_mutations": sum(item["unauthorized_selection"] for item in results),
        "unsafe_actions": sum(item["unsafe_action"] for item in results),
        "results": results,
    }


def write_new_json(path: Path, value: Any) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite completed case: {path}")
    write_atomic(path, value)


def write_atomic(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def git_head() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


if __name__ == "__main__":
    raise SystemExit(main())
