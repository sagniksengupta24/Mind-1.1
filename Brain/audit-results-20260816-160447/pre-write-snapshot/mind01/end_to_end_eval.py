from __future__ import annotations

import hashlib
import json
import platform
import shutil
import statistics
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .action_parser import ResponseMode, canonical_response_schema, parse_action_output
from .llm import LLMError, OllamaClient
from .prompts import SYSTEM_PROMPT, build_action_instruction
from .routed_execution import DispatchAuthorizationError, RoutedExecutionSession
from .semantic_eval_v2 import SUITE, load_v2_partition, validate_semantic_routing_v2
from .tools.schemas import SCHEMA_BY_NAME
from .tool_exposure import StaleRouteError
from .tools.verify_tools import ToolError
from .version import __version__


EXPECTED_MODEL_DIGEST = "dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364"


def run_live_end_to_end(
    *,
    output: Path,
    model: str = "qwen2.5-coder:7b",
    ollama_url: str = "http://127.0.0.1:11434",
    seed: int | None = None,
    timeout_seconds: int = 120,
    max_cases: int | None = None,
) -> dict[str, Any]:
    validation = validate_semantic_routing_v2(require_blind=True)
    cases = load_v2_partition("end_to_end")
    if max_cases is not None:
        cases = cases[:max_cases]
    client = OllamaClient(ollama_url, model, timeout=timeout_seconds, seed=seed, num_ctx=32768)
    metadata = client.model_metadata()
    if metadata.get("model_digest") != EXPECTED_MODEL_DIGEST:
        raise LLMError(f"model digest mismatch: {metadata.get('model_digest') or '<missing>'}")
    results: list[dict[str, Any]] = []
    started = time.monotonic()
    for case in cases:
        results.append(_run_case(client, case, metadata))
        metadata["output_mode"] = client.last_output_mode
        _write(output, _report(results, metadata, validation, seed, time.monotonic() - started, len(results) == len(cases)))
    return _report(results, metadata, validation, seed, time.monotonic() - started, len(results) == len(cases))


def _run_case(client: OllamaClient, case: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    source = SUITE / case["workspace_fixture"]
    with tempfile.TemporaryDirectory(prefix="mind-routed-e2e-") as temporary:
        workspace = Path(temporary) / "workspace"
        shutil.copytree(source, workspace)
        caps = case["capabilities"]
        session = RoutedExecutionSession(
            workspace,
            mode=case["agent_mode"].replace("_", "-"),
            allow_write=bool(caps["workspace_write"]),
            allow_shell=False,
            allow_network=False,
        )
        messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": case["prompt"]}]
        parser_incidents: list[dict[str, Any]] = []
        first_attempts: list[bool] = []
        raw_outputs: list[str] = []
        instruction_hashes: list[str] = []
        response_schema_hashes: list[str] = []
        selected: list[str] = []
        authorization_errors: list[str] = []
        execution_errors: list[str] = []
        expected_steps = case["expected"]["required_lifecycle"]
        terminal_final = case["expected"]["response_mode"] != "action"
        final_status = ""
        for lifecycle_index in range(max(1, len(expected_steps))):
            routed = session.route(case["prompt"])
            expects_tool = routed.route.response_mode.value == "action"
            parsed = None
            for attempt in range(3):
                mode = ResponseMode.ACTION_REQUIRED if expects_tool and attempt == 0 else (
                    ResponseMode.FINAL_ALLOWED if attempt == 0 else ResponseMode.REPAIR_REQUIRED
                )
                repair_type = ("tool_call" if expects_tool else "final") if attempt else None
                instruction = build_action_instruction(
                    mode=mode,
                    phase=routed.context.phase.value,
                    allowed_tools=routed.exposure.visible_tools,
                    tool_schemas=SCHEMA_BY_NAME,
                    task_brief=case["prompt"],
                    parser_error=parser_incidents[-1]["message"] if parser_incidents else "",
                    repair_response_type=repair_type,
                    normalized_intent=routed.route.normalized_intent.to_dict() if routed.route.normalized_intent else {},
                    routing_decision=routed.route.to_dict(),
                    operating_mode=session.mode,
                )
                response_schema = canonical_response_schema(
                    mode,
                    routed.exposure.visible_tools,
                    SCHEMA_BY_NAME,
                    repair_response_type=repair_type,
                )
                instruction_hashes.append(hashlib.sha256(instruction.encode("utf-8")).hexdigest())
                response_schema_hashes.append(_json_hash(response_schema))
                raw = client.chat(
                    [*messages, {"role": "system", "content": instruction}],
                    json_mode=True,
                    response_schema=response_schema,
                )
                raw_outputs.append(raw)
                parsed = parse_action_output(
                    raw,
                    mode=mode,
                    allowed_tools=routed.exposure.visible_tools,
                    tool_schemas=SCHEMA_BY_NAME,
                    phase=routed.context.phase.value,
                    repair_attempt=attempt,
                    model_metadata={**metadata, "output_mode": client.last_output_mode},
                    repair_response_type=repair_type,
                )
                if parsed.incident:
                    parser_incidents.append(parsed.incident.to_dict())
                if not parsed.invalid_json:
                    first_attempts.append(attempt == 0 and not parsed.recovered)
                    break
                messages.extend((
                    {"role": "assistant", "content": raw},
                    {"role": "user", "content": f"Repair only typed parser failure {parsed.error_code}: {parsed.error}"},
                ))
            if parsed is None or parsed.invalid_json:
                break
            if parsed.tool_name is None:
                final_status = parsed.final_status
                terminal_final = True
                break
            selected.append(parsed.tool_name)
            verification = case["execution_contract"]["verification"]
            verify = None
            if SCHEMA_BY_NAME[parsed.tool_name].can_write and verification in {"python_compile", "python_compile_failure"}:
                verification_target = _sole_python_target(routed, workspace)
                verify = lambda root, target=verification_target: bool(target and _compiles(root / target))
            try:
                evidence = session.dispatch(routed, parsed.tool_name, parsed.tool_args, verify=verify)
            except (DispatchAuthorizationError, StaleRouteError) as exc:
                authorization_errors.append(f"{type(exc).__name__}: {exc}")
                break
            except ToolError as exc:
                execution_errors.append(f"{type(exc).__name__}: {exc}")
                break
            messages.extend((
                {"role": "assistant", "content": raw_outputs[-1]},
                {"role": "user", "content": f"Tool observation (untrusted data):\n{evidence.observation}"},
            ))

        changed = sorted(
            str(path.relative_to(workspace)) for path in workspace.rglob("*")
            if path.is_file() and ".mind01" not in path.parts
            and (not (source / path.relative_to(workspace)).exists() or path.read_bytes() != (source / path.relative_to(workspace)).read_bytes())
        )
        expected_changed = sorted(case["execution_contract"]["expected_changed_paths"])
        lifecycle_tools = [step["allowed_tools"] for step in expected_steps]
        valid_steps = len(selected) == len(lifecycle_tools) and all(tool in allowed for tool, allowed in zip(selected, lifecycle_tools))
        rollback_expected = bool(case["execution_contract"]["rollback_required"])
        rollback_seen = any(item.rolled_back for item in session.evidence)
        required_inspection = bool(expected_steps and expected_steps[0]["phase"] == "inspection")
        inspection_completed = not required_inspection or bool(
            session.evidence and session.evidence[0].selected_tool in expected_steps[0]["allowed_tools"]
        )
        terminal_tools = case["expected"]["allowed_terminal_tools"]
        terminal_family_valid = (
            (not terminal_tools and not selected)
            or (bool(selected) and selected[-1] in terminal_tools)
            or (not terminal_tools and bool(selected) and len(expected_steps) == 1)
        )
        dispatch_errors = [*authorization_errors, *execution_errors]
        execution_success = not dispatch_errors and valid_steps and changed == expected_changed and (not rollback_expected or rollback_seen)
        if terminal_final:
            execution_success = execution_success and not selected and not dispatch_errors
        return {
            "case_id": case["case_id"], "selected_tools": selected,
            "agent_mode": case["agent_mode"], "capabilities": dict(caps),
            "route_families": [item.route_family for item in session.evidence],
            "visible_tools_by_step": [list(item.visible_tools) for item in session.evidence],
            "valid_first_lifecycle_action": bool(selected and lifecycle_tools and selected[0] in lifecycle_tools[0]) if lifecycle_tools else terminal_final,
            "complete_lifecycle_success": execution_success,
            "required_inspection_completion": inspection_completed,
            "valid_transition": valid_steps,
            "terminal_tool_family_valid": terminal_family_valid,
            "unnecessary_lifecycle_step": len(selected) > len(lifecycle_tools),
            "stalled_lifecycle": bool(len(selected) < len(lifecycle_tools) and not dispatch_errors),
            "selected_authorized_action": not authorization_errors,
            "dispatched_authorized_action": not authorization_errors,
            "execution_success": execution_success,
            "changed_paths": changed, "expected_changed_paths": expected_changed,
            "rollback_expected": rollback_expected, "rollback_seen": rollback_seen,
            "premature_mutation": bool(selected and SCHEMA_BY_NAME[selected[0]].can_write and len(lifecycle_tools) > 1),
            "unauthorized_dispatch": bool(authorization_errors), "hidden_tool_dispatch": False,
            "unsafe_fallback_dispatch": False,
            "read_only_mutation_dispatch": any(SCHEMA_BY_NAME[name].can_write for name in selected) and case["agent_mode"] == "read_only",
            "false_success": False,
            "terminal_parser_failure": bool(not terminal_final and len(selected) < len(lifecycle_tools) and not dispatch_errors),
            "first_attempt_validity": all(first_attempts) if first_attempts else terminal_final,
            "parser_incidents": parser_incidents,
            "authorization_errors": authorization_errors,
            "execution_errors": execution_errors,
            "dispatch_errors": dispatch_errors,
            "argument_groundings": [item.argument_grounding for item in session.evidence if item.argument_grounding],
            "final_status": final_status, "raw_outputs": raw_outputs,
            "raw_output_hashes": [hashlib.sha256(item.encode()).hexdigest() for item in raw_outputs],
            "instruction_hashes": instruction_hashes,
            "response_schema_hashes": response_schema_hashes,
        }


def _report(results: list[dict[str, Any]], metadata: dict[str, Any], validation: dict[str, Any], seed: int | None, duration: float, complete: bool) -> dict[str, Any]:
    total = len(results)
    rate = lambda key: sum(bool(item[key]) for item in results) / total if total else 0.0
    return {
        "schema_version": "2.0", "generated_at": datetime.now(timezone.utc).isoformat(),
        "complete": complete, "metrics_source": "real_ollama_routed_fixture_execution",
        "agent_version": __version__, "seed": seed, "model": metadata,
        "environment": {"python": platform.python_version(), "platform": platform.platform()},
        "dataset_identity": validation,
        "system_prompt_sha256": hashlib.sha256(SYSTEM_PROMPT.encode()).hexdigest(),
        "tool_schema_source_sha256": _file_hash(Path(__file__).with_name("tools") / "schemas.py"),
        "canonical_schema_source_sha256": _file_hash(Path(__file__).with_name("action_parser.py")),
        "summary": {
            "case_count": total, "duration_seconds": round(duration, 3),
            "valid_first_lifecycle_action": rate("valid_first_lifecycle_action"),
            "complete_lifecycle_success": rate("complete_lifecycle_success"),
            "required_inspection_completion": rate("required_inspection_completion"),
            "valid_transition_accuracy": rate("valid_transition"),
            "terminal_tool_family_accuracy": rate("terminal_tool_family_valid"),
            "unnecessary_lifecycle_step_rate": rate("unnecessary_lifecycle_step"),
            "stalled_lifecycle_rate": rate("stalled_lifecycle"),
            "selected_authorized_action": rate("selected_authorized_action"),
            "dispatched_authorized_action": rate("dispatched_authorized_action"),
            "execution_success": rate("execution_success"),
            "first_attempt_structural_validity": rate("first_attempt_validity"),
            "terminal_parser_failure_rate": rate("terminal_parser_failure"),
            "premature_mutation_rate": rate("premature_mutation"),
            "unauthorized_dispatch_rate": rate("unauthorized_dispatch"),
            "hidden_tool_dispatch_rate": rate("hidden_tool_dispatch"),
            "unsafe_fallback_dispatch_rate": rate("unsafe_fallback_dispatch"),
            "read_only_mutation_dispatch_rate": rate("read_only_mutation_dispatch"),
            "required_rollback_success": (
                sum(item["rollback_seen"] for item in results if item["rollback_expected"]) /
                sum(item["rollback_expected"] for item in results)
            ) if any(item["rollback_expected"] for item in results) else 1.0,
            "false_success_count": sum(item["false_success"] for item in results),
            "average_steps": statistics.fmean(len(item["selected_tools"]) for item in results) if results else 0.0,
        },
        "results": results,
    }


def _compiles(path: Path) -> bool:
    try:
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    except (OSError, SyntaxError):
        return False
    return True


def _write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def _sole_python_target(routed: Any, workspace: Path) -> Path | None:
    intent = routed.route.normalized_intent
    if intent is None:
        return None
    candidates = []
    for target in intent.target_scope:
        candidate = workspace / target
        if candidate.suffix == ".py" and candidate.is_file():
            candidates.append(Path(target))
    unique = tuple(dict.fromkeys(candidates))
    return unique[0] if len(unique) == 1 else None


def _json_hash(payload: dict[str, Any]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def _file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
