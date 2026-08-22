from __future__ import annotations

import hashlib
import json
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .agent import Agent
from .action_parser import ResponseMode, canonical_response_schema, parse_action_output
from .completion import CompletionAuthority, VerificationEvidence
from .config import AgentConfig
from .eval_schema import ActionBenchmarkCase, ActionBenchmarkSuite, load_action_suite
from .llm import LLMError, OllamaClient
from .modes import AgentMode
from .patch_review import review_patch
from .prompts import SYSTEM_PROMPT, build_action_instruction
from .sandbox import SandboxConfig, SandboxedExecutor, SandboxError
from .tools.schemas import SCHEMA_BY_NAME
from .version import __version__
from .self_correction import WorkspaceSnapshot
from .task_contract import EvidenceType, TaskContract, TaskRequirement


@dataclass
class ActionCaseResult:
    id: str
    category: str
    first_attempt_valid: bool
    valid_after_attempt: int | None
    terminal_parser_failure: bool
    actual_response_type: str
    actual_tool: str
    expected_family_match: bool
    parser_failures: list[dict[str, Any]]
    output_mode: str
    output_tokens: int | None
    latency_ms: int
    attempts: int
    raw_output_hashes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def run_action_benchmark(
    *,
    model: str,
    ollama_url: str = "http://127.0.0.1:11434",
    suite_path: Path | None = None,
    output_root: Path | None = None,
    timeout_seconds: int = 120,
) -> Path:
    suite = load_action_suite(suite_path)
    client = OllamaClient(ollama_url, model, timeout=timeout_seconds)
    model_metadata = client.model_metadata()
    results: list[ActionCaseResult] = []
    for case in suite.cases:
        results.append(_run_action_case(client, case, model_metadata))
    report = build_action_report(suite, results, model_metadata, client.last_output_mode)
    root = output_root or Path.cwd() / "evaluation_results"
    run_dir = make_report_directory(root, "action", suite.source_hash)
    (run_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    incidents = [incident for result in results for incident in result.parser_failures]
    (run_dir / "parser_incidents.jsonl").write_text(
        "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in incidents),
        encoding="utf-8",
    )
    (run_dir / "manifest.json").write_text(
        json.dumps(report["metadata"], indent=2, ensure_ascii=False), encoding="utf-8"
    )
    return run_dir


def _run_action_case(client: OllamaClient, case: ActionBenchmarkCase, model_metadata: dict[str, Any]) -> ActionCaseResult:
    parser_failures: list[dict[str, Any]] = []
    hashes: list[str] = []
    first_valid = False
    valid_after: int | None = None
    actual_type = ""
    actual_tool = ""
    output_tokens: int | None = None
    started = time.monotonic()
    attempts = 0
    mode = case.mode
    error_text = ""
    messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": case.prompt}]
    max_attempts = case.max_repair_attempts if case.repair_allowed else 0
    for attempt in range(max_attempts + 1):
        attempts = attempt + 1
        current_mode = mode if attempt == 0 else ResponseMode.REPAIR_REQUIRED
        repair_type = case.repair_response_type
        if attempt > 0 and not repair_type and mode == ResponseMode.ACTION_REQUIRED:
            repair_type = "tool_call"
        instruction = build_action_instruction(
            mode=current_mode,
            phase=case.category,
            allowed_tools=case.allowed_tools,
            tool_schemas=SCHEMA_BY_NAME,
            task_brief=case.prompt,
            parser_error=error_text,
            repair_response_type=repair_type,
        )
        schema = canonical_response_schema(
            current_mode,
            case.allowed_tools,
            SCHEMA_BY_NAME,
            repair_response_type=repair_type,
        )
        raw = client.chat([*messages, {"role": "system", "content": instruction}], json_mode=True, response_schema=schema)
        hashes.append(hashlib.sha256(raw.encode("utf-8", errors="replace")).hexdigest())
        metadata = client.last_response_metadata or {}
        eval_count = metadata.get("eval_count")
        if isinstance(eval_count, int):
            output_tokens = eval_count
        parsed = parse_action_output(
            raw,
            mode=current_mode,
            allowed_tools=case.allowed_tools,
            tool_schemas=SCHEMA_BY_NAME,
            phase=case.category,
            repair_attempt=attempt,
            model_metadata={**model_metadata, "output_mode": client.last_output_mode},
            repair_response_type=repair_type,
        )
        if parsed.incident is not None:
            parser_failures.append(parsed.incident.to_dict())
        if not parsed.invalid_json:
            valid_after = attempt
            first_valid = attempt == 0 and not parsed.recovered
            actual_type = "tool_call" if parsed.tool_name else "final"
            actual_tool = parsed.tool_name or ""
            break
        error_text = f"{parsed.error_code}: {parsed.error}"
        messages.extend(
            [
                {"role": "assistant", "content": raw},
                {"role": "user", "content": f"Repair the invalid response only. {error_text}"},
            ]
        )
    family_match = (
        actual_type == case.expected_response_type
        and (actual_type == "final" or actual_tool in case.expected_tools)
    )
    return ActionCaseResult(
        id=case.id,
        category=case.category,
        first_attempt_valid=first_valid,
        valid_after_attempt=valid_after,
        terminal_parser_failure=valid_after is None,
        actual_response_type=actual_type,
        actual_tool=actual_tool,
        expected_family_match=family_match,
        parser_failures=parser_failures,
        output_mode=client.last_output_mode,
        output_tokens=output_tokens,
        latency_ms=int((time.monotonic() - started) * 1000),
        attempts=attempts,
        raw_output_hashes=hashes,
    )


def build_action_report(
    suite: ActionBenchmarkSuite,
    results: list[ActionCaseResult],
    model_metadata: dict[str, Any],
    output_mode: str,
) -> dict[str, Any]:
    total = len(results)
    failures = [incident for result in results for incident in result.parser_failures]
    category_counts = Counter(item.get("error_code", "UNKNOWN") for item in failures)
    tools = Counter(result.actual_tool for result in results if result.actual_tool)
    first_valid = sum(result.first_attempt_valid for result in results)
    after_one = sum(result.valid_after_attempt is not None and result.valid_after_attempt <= 1 for result in results)
    after_two = sum(result.valid_after_attempt is not None and result.valid_after_attempt <= 2 for result in results)
    terminal = sum(result.terminal_parser_failure for result in results)
    unknown = sum(any(item.get("error_code") == "UNKNOWN_TOOL" for item in result.parser_failures) for result in results)
    wrong_mode_codes = {"FINAL_ANSWER_WHEN_ACTION_REQUIRED", "TOOL_CALL_WHEN_FINAL_REQUIRED"}
    wrong_mode = sum(any(item.get("error_code") in wrong_mode_codes for item in result.parser_failures) for result in results)
    extraction = sum(any(item.get("error_code") == "PROSE_AROUND_ACTION" for item in result.parser_failures) for result in results)
    semantic = sum(result.expected_family_match for result in results)
    token_values = [result.output_tokens for result in results if result.output_tokens is not None]
    return {
        "metadata": {
            "agent_version": __version__,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "git_commit": git_commit(Path.cwd()),
            "benchmark_version": suite.benchmark_version,
            "benchmark_hash": suite.source_hash,
            "configuration_hash": configuration_hash(model_metadata, suite.source_hash),
            "prompt_hash": hashlib.sha256(SYSTEM_PROMPT.encode("utf-8")).hexdigest(),
            "model": model_metadata.get("model"),
            "model_digest": model_metadata.get("model_digest"),
            "ollama_version": model_metadata.get("ollama_version"),
            "structured_output_capability": model_metadata.get("json_schema_supported"),
            "output_mode": output_mode,
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "metrics_source": "real_ollama",
        },
        "summary": {
            "case_count": total,
            "first_attempt_valid_count": first_valid,
            "first_attempt_valid_rate": ratio(first_valid, total),
            "valid_after_one_repair_count": after_one,
            "valid_after_one_repair_rate": ratio(after_one, total),
            "valid_after_two_repairs_count": after_two,
            "valid_after_two_repairs_rate": ratio(after_two, total),
            "terminal_parser_failure_count": terminal,
            "terminal_parser_failure_rate": ratio(terminal, total),
            "unknown_tool_count": unknown,
            "unknown_tool_rate": ratio(unknown, total),
            "wrong_mode_count": wrong_mode,
            "wrong_mode_rate": ratio(wrong_mode, total),
            "extraction_recovery_count": extraction,
            "extraction_recovery_rate": ratio(extraction, total),
            "expected_tool_family_match_count": semantic,
            "expected_tool_family_match_rate": ratio(semantic, total),
            "average_output_tokens": sum(token_values) / len(token_values) if token_values else None,
            "average_latency_ms": sum(result.latency_ms for result in results) / total if total else 0.0,
            "failure_category_distribution": dict(sorted(category_counts.items())),
            "tool_call_distribution": dict(sorted(tools.items())),
        },
        "results": [result.to_dict() for result in results],
    }


def aggregate_parser_report(run_directory: Path) -> dict[str, Any]:
    report_path = run_directory / "report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    results = report.get("results", [])
    incidents = [item for result in results for item in result.get("parser_failures", [])]
    by_phase: dict[str, int] = Counter(str(item.get("phase", "")) for item in incidents)
    by_model: dict[str, int] = Counter(str(item.get("model_metadata", {}).get("model", "")) for item in incidents)
    by_category: dict[str, int] = Counter(str(item.get("error_code", "")) for item in incidents)
    recovered = sum(bool(item.get("recovered")) for item in incidents)
    terminal = sum(bool(result.get("terminal_parser_failure")) for result in results)
    payload = {
        "run_directory": str(run_directory),
        "incident_count": len(incidents),
        "first_attempt_failure_count": sum(not bool(result.get("first_attempt_valid")) for result in results),
        "recovered_incident_count": recovered,
        "terminal_failure_count": terminal,
        "frequency_by_category": dict(sorted(by_category.items())),
        "failures_by_phase": dict(sorted(by_phase.items())),
        "failures_by_model": dict(sorted(by_model.items())),
    }
    (run_directory / "parser_report.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def run_real_mutation_smoke(
    *,
    model: str,
    ollama_url: str = "http://127.0.0.1:11434",
    output_root: Path | None = None,
    repair_budget: int = 2,
) -> Path:
    suite_root = Path(__file__).resolve().parent / "eval_suites" / "real_mutation"
    manifest = json.loads((suite_root / "manifest.json").read_text(encoding="utf-8"))
    root = output_root or Path.cwd() / "evaluation_results"
    run_dir = make_report_directory(root, "mutation", hashlib.sha256(json.dumps(manifest, sort_keys=True).encode()).hexdigest())
    results: list[dict[str, Any]] = []
    with tempfile.TemporaryDirectory(prefix="mind-real-mutation-") as temp:
        temp_root = Path(temp)
        for fixture in manifest["fixtures"]:
            workspace = temp_root / fixture["id"]
            shutil.copytree(suite_root / fixture["source_dir"], workspace)
            for template in workspace.rglob("*.fixture"):
                template.rename(template.with_suffix(""))
            results.append(
                _run_mutation_fixture(
                    workspace=workspace,
                    fixture=fixture,
                    model=model,
                    ollama_url=ollama_url,
                    repair_budget=repair_budget,
                )
            )
    accepted = sum(bool(item["accepted"]) for item in results)
    report = {
        "metadata": {
            "agent_version": __version__,
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "suite": "real-mutation",
            "suite_schema_version": manifest["schema_version"],
            "metrics_source": "real_ollama",
            "git_commit": git_commit(Path.cwd()),
        },
        "summary": {
            "passed": accepted,
            "total": len(results),
            "all_preconditions_failed": all(item["precondition_failed"] for item in results),
            "unauthorized_mutations": sum(item["unauthorized_mutations"] for item in results),
            "unsafe_actions": sum(item["unsafe_actions"] for item in results),
            "false_successes": sum(item["false_successes"] for item in results),
            "rollbacks": sum(item["rollbacks"] for item in results),
        },
        "results": results,
    }
    (run_dir / "report.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    (run_dir / "manifest.json").write_text(json.dumps(report["metadata"], indent=2), encoding="utf-8")
    return run_dir


def _run_mutation_fixture(
    *,
    workspace: Path,
    fixture: dict[str, Any],
    model: str,
    ollama_url: str,
    repair_budget: int,
) -> dict[str, Any]:
    initial = WorkspaceSnapshot.capture(workspace)
    precondition_passed, precondition_output = _fixture_acceptance(workspace, fixture["acceptance"])
    if precondition_passed:
        raise ValueError(f"Real mutation fixture already passes acceptance: {fixture['id']}")
    attempts: list[dict[str, Any]] = []
    feedback = ""
    patch_hashes: Counter[str] = Counter()
    accepted = False
    rollbacks = 0
    final_response = ""
    completion_status = "failed"
    last_acceptance_passed = False
    last_review: list[dict[str, Any]] = []
    last_changed: list[str] = []
    for attempt_index in range(repair_budget + 1):
        before = WorkspaceSnapshot.capture(workspace)
        prompt = fixture["task"]
        if feedback:
            prompt += "\n\nPrevious repair did not pass deterministic acceptance. Failure class: " + feedback
        config = AgentConfig.build(
            workspace=str(workspace),
            model=model,
            ollama_url=ollama_url,
            max_steps=10,
            yes=True,
            dry_run=False,
            allow_write=True,
            allow_shell=True,
            mode=AgentMode.WRITE_APPROVED,
            request_timeout_seconds=180,
        )
        agent = Agent(config)
        response = agent.ask(prompt)
        final_response = response.text
        completion_status = response.completion_status
        after = WorkspaceSnapshot.capture(workspace)
        changed = before.changed_files(after)
        diff = before.diff(after)
        patch_hash = hashlib.sha256(diff.encode("utf-8", errors="replace")).hexdigest()
        patch_hashes[patch_hash] += 1
        review = review_patch(
            diff_text=diff,
            changed_files=changed,
            expected_paths=list(fixture.get("expected_paths", [])),
            protected_paths=list(fixture.get("protected_paths", [])) + [".mind01", ".git"],
        ).to_dicts()
        acceptance_passed, acceptance_output = _fixture_acceptance(workspace, fixture["acceptance"])
        blocking_review = any(item.get("severity") == "blocking" for item in review)
        expected_changed = any(path in changed for path in fixture.get("expected_paths", []))
        accepted = acceptance_passed and expected_changed and not blocking_review
        last_acceptance_passed = acceptance_passed
        last_review = review
        last_changed = changed
        rolled_back = False
        no_progress = patch_hashes[patch_hash] > 1 or not changed
        if not accepted and changed:
            before.restore()
            rollbacks += 1
            rolled_back = True
        attempts.append(
            {
                "index": attempt_index + 1,
                "files_changed": changed,
                "tool_calls": [item["tool"] for item in (agent.last_state.tool_results if agent.last_state else [])],
                "parser_incidents": response.parser_incidents,
                "verification": response.verification,
                "patch_review": review,
                "acceptance_passed": acceptance_passed,
                "acceptance_output": acceptance_output[-2000:],
                "completion_status": response.completion_status,
                "rolled_back": rolled_back,
                "no_progress": no_progress,
            }
        )
        if accepted or no_progress:
            break
        feedback = classify_acceptance_failure(acceptance_output)
    final = WorkspaceSnapshot.capture(workspace)
    final_changed = initial.changed_files(final)
    unsafe_codes = {"UNSAFE_ACTION"}
    unauthorized = sum(
        1 for attempt in attempts for incident in attempt["parser_incidents"]
        if incident.get("error_code") == "UNKNOWN_TOOL" and "write" in incident.get("message", "").lower()
    )
    unsafe = sum(
        1 for attempt in attempts for incident in attempt["parser_incidents"]
        if incident.get("error_code") in unsafe_codes
    )
    false_success = int(not accepted and completion_status == "verified")
    completion_decision = _mutation_completion_decision(
        fixture=fixture,
        accepted=accepted,
        acceptance_passed=last_acceptance_passed,
        changed_files=final_changed or last_changed,
        patch_review=last_review,
        rollback_performed=bool(rollbacks and not accepted),
    )
    return {
        "id": fixture["id"],
        "precondition_failed": not precondition_passed,
        "precondition_output": precondition_output[-2000:],
        "accepted": accepted,
        "files_changed": final_changed,
        "attempts": attempts,
        "repair_attempts": max(0, len(attempts) - 1),
        "rollbacks": rollbacks,
        "unauthorized_mutations": unauthorized,
        "unsafe_actions": unsafe,
        "false_successes": false_success,
        "final_completion_status": completion_decision.status,
        "completion_contract": completion_decision.to_dict(),
        "model_summary": final_response[:2000],
    }


def _mutation_completion_decision(
    *,
    fixture: dict[str, Any],
    accepted: bool,
    acceptance_passed: bool,
    changed_files: list[str],
    patch_review: list[dict[str, Any]],
    rollback_performed: bool,
):  # type: ignore[no-untyped-def]
    acceptance_types = {
        "compileall": (EvidenceType.SYNTAX,),
        "pytest": (EvidenceType.BEHAVIORAL_TEST, EvidenceType.REGRESSION_TEST),
        "hidden_feature": (EvidenceType.BEHAVIORAL_TEST, EvidenceType.REGRESSION_TEST),
    }[str(fixture["acceptance"])]
    contract = TaskContract(
        schema_version="1.0",
        contract_id=f"real-mutation-{fixture['id']}",
        normalized_goal=str(fixture["task"]),
        task_type="real_mutation_acceptance",
        target_scope=tuple(str(item) for item in fixture.get("expected_paths", [])),
        forbidden_scope=tuple(str(item) for item in fixture.get("protected_paths", [])) + (".git", ".mind01"),
        expected_artifacts=tuple(str(item) for item in fixture.get("expected_paths", [])),
        required_symbols=(),
        required_signatures={},
        behavioral_requirements=("Independent fixture acceptance passes",),
        regression_requirements=("Protected behavior is preserved",),
        security_requirements=(),
        requirements=(
            TaskRequirement("R-ACCEPTANCE", "Independent fixture acceptance passes", acceptance_types),
            TaskRequirement("R-SCOPE", "Mutation remains in expected scope", (EvidenceType.PATCH_REVIEW,)),
        ),
        rollback_conditions=("Rejected fixture mutation",),
        completion_criteria=("Acceptance and scope evidence pass",),
        mutation_required=True,
    )
    evidence: list[VerificationEvidence] = []
    for index, kind in enumerate(acceptance_types, start=1):
        evidence.append(
            VerificationEvidence(
                name=f"fixture-{fixture['acceptance']}",
                command=[str(fixture["acceptance"])],
                status="passed" if acceptance_passed else "failed",
                exit_code=0 if acceptance_passed else 1,
                duration_seconds=0.0,
                evidence_id=f"fixture-acceptance-{index:03d}",
                evidence_type=kind.value,
                requirement_ids=("R-ACCEPTANCE",),
                state_hash="post",
                blocking=True,
                source="independent_fixture_acceptance",
            )
        )
    scope_passed = accepted and not any(item.get("severity") == "blocking" for item in patch_review)
    evidence.append(
        VerificationEvidence(
            name="fixture-scope-review",
            command=[],
            status="passed" if scope_passed else "failed",
            exit_code=0 if scope_passed else 1,
            duration_seconds=0.0,
            evidence_id="fixture-scope-001",
            evidence_type=EvidenceType.PATCH_REVIEW.value,
            requirement_ids=("R-SCOPE",),
            state_hash="post",
            blocking=True,
            source="independent_fixture_scope",
        )
    )
    return CompletionAuthority().decide(
        "verified" if accepted else "failed",
        task_contract=contract,
        verification=evidence,
        evidence_refs=[item.evidence_id for item in evidence],
        patch_review=patch_review,
        changed_files=changed_files,
        current_state_hash="post",
        rollback_performed=rollback_performed,
    )


def _fixture_acceptance(workspace: Path, acceptance: str) -> tuple[bool, str]:
    if acceptance == "compileall":
        return _run_acceptance([sys.executable, "-m", "compileall", "-q", "."], workspace)
    if acceptance == "pytest":
        return _run_acceptance([sys.executable, "-m", "pytest", "-q"], workspace)
    if acceptance == "hidden_feature":
        try:
            import importlib.util

            path = workspace / "text_utils.py"
            spec = importlib.util.spec_from_file_location("mind_hidden_text_utils", path)
            if spec is None or spec.loader is None:
                return False, "hidden acceptance could not load implementation"
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            function = getattr(module, "normalize_identifier")
            cases = {
                "  Hello, World!  ": "hello_world",
                "Already__Clean": "already_clean",
                "123 value": "123_value",
                "---": "",
            }
            passed = all(function(value) == expected for value, expected in cases.items())
            preserved = getattr(module, "preserve")(" Keep ") == " Keep "
            return passed and preserved, "hidden behavioral acceptance passed" if passed and preserved else "hidden behavioral acceptance failed"
        except Exception as exc:
            return False, f"hidden behavioral acceptance raised {type(exc).__name__}"
    raise ValueError(f"Unknown fixture acceptance adapter: {acceptance}")


def _run_acceptance(argv: list[str], workspace: Path) -> tuple[bool, str]:
    try:
        config = SandboxConfig(
            workspace=workspace,
            timeout_seconds=60,
            max_output_bytes=4000,
            allow_network=False,
        )
        executor = SandboxedExecutor(workspace, config)
        res = executor.execute(argv, cwd=workspace, timeout_seconds=60)
        return res.returncode == 0 and not res.timed_out, (res.output or "")[-4000:]
    except (OSError, SandboxError) as exc:
        return False, f"{type(exc).__name__}: {exc}"


def classify_acceptance_failure(output: str) -> str:
    text = output.lower()
    if "syntaxerror" in text or "syntax error" in text:
        return "syntax or compilation failure; inspect executable source structure"
    if "failed" in text or "assertionerror" in text:
        return "behavioral test failure; inspect the implementation and preserve tests"
    if "hidden behavioral acceptance" in text:
        return "hidden behavioral contract failure; inspect the documented contract and executable definitions"
    return "deterministic acceptance failure; inspect evidence and make a minimal in-scope repair"


def make_report_directory(root: Path, kind: str, seed: str) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    suffix = hashlib.sha256(f"{seed}:{time.time_ns()}:{uuid.uuid4().hex}".encode()).hexdigest()[:8]
    path = root / f"{stamp}-{kind}-{suffix}"
    path.mkdir()
    return path


def configuration_hash(metadata: dict[str, Any], suite_hash: str) -> str:
    payload = json.dumps({"metadata": metadata, "suite_hash": suite_hash}, sort_keys=True, default=str)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def git_commit(workspace: Path) -> str | None:
    try:
        result = subprocess.run(["git", "rev-parse", "HEAD"], cwd=workspace, text=True, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, timeout=3)
        return result.stdout.strip() or None if result.returncode == 0 else None
    except (OSError, subprocess.TimeoutExpired):
        return None


def ratio(value: int, total: int) -> float:
    return value / total if total else 0.0
