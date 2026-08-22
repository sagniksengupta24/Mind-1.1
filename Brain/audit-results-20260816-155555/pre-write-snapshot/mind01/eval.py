from __future__ import annotations

import contextlib
import argparse
import json
import re
import platform
import signal
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .agent import Agent
from .config import AgentConfig
from .version import __version__


@dataclass
class EvalResult:
    name: str
    category: str
    passed: bool
    response: str
    expected_contains: list[str]
    expected_groups: list[list[str]]
    steps: int
    attempts: int
    duration_ms: int
    trace: list[str]
    reason: str
    receipt_ids: list[str]
    verification: list[dict[str, Any]]
    requires_verification: bool = False
    false_success: bool = False
    timed_out: bool = False
    error: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category,
            "passed": self.passed,
            "response": self.response,
            "expected_contains": self.expected_contains,
            "expected_groups": self.expected_groups,
            "steps": self.steps,
            "attempts": self.attempts,
            "duration_ms": self.duration_ms,
            "trace": self.trace,
            "reason": self.reason,
            "receipt_ids": self.receipt_ids,
            "verification": self.verification,
            "requires_verification": self.requires_verification,
            "false_success": self.false_success,
            "timed_out": self.timed_out,
            "error": self.error,
        }


class EvalTimeout(RuntimeError):
    pass


def run_eval_file(
    config: AgentConfig,
    eval_file: Path,
    task_timeout: int | None = 120,
    repair_attempts: int = 1,
) -> list[EvalResult]:
    content = eval_file.read_text(encoding="utf-8")
    if eval_file.suffix in {".yaml", ".yml"}:
        import yaml
        data = yaml.safe_load(content)
    else:
        data = json.loads(content)
    tasks = data.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("Eval file must contain a `tasks` list.")
    default_category = str(data.get("category", "uncategorized"))

    results = []
    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            raise ValueError(f"Task {index} must be an object.")
        name = str(task.get("name", f"task-{index}"))
        category = str(task.get("category", default_category))
        if "prompt" not in task:
            raise ValueError(f"Task {index} `{name}` is missing required `prompt`.")
        prompt = str(task["prompt"])
        expected = [str(item) for item in task.get("expected_contains", [])]
        requires_verification = bool(task.get("requires_verification", False))
        groups = [
            [str(item) for item in group]
            for group in task.get("expected_groups", [])
            if isinstance(group, list)
        ]
        eval_check_command = str(task.get("eval_check_command", ""))
        has_real_check = bool(eval_check_command) and eval_check_command.strip() != "true"
        started = time.monotonic()
        response = ""
        steps = 0
        attempts = 0
        trace: list[str] = []
        timed_out = False
        error = ""
        passed = False
        matched = False
        verification: list[dict[str, Any]] = []
        reason = ""
        try:
            with timeout_after(task_timeout):
                agent = Agent(config)
                response, steps, attempts, trace, matched, verification = run_eval_task(
                    agent,
                    prompt,
                    expected,
                    groups,
                    max(0, repair_attempts),
                    eval_check_command=eval_check_command if has_real_check else "",
                )
        except EvalTimeout:
            timed_out = True
            error = f"Task timed out after {task_timeout} seconds."
            response = error
        except Exception as exc:  # Keep one bad task from hiding the full report.
            error = f"{type(exc).__name__}: {exc}"
            response = error
        duration_ms = int((time.monotonic() - started) * 1000)
        has_passed_verification = any(item.get("status") == "passed" for item in verification)

        check_passed = True
        if eval_check_command:
            proc = subprocess.run(
                eval_check_command,
                shell=True,
                cwd=config.workspace,
                text=True,
                capture_output=True
            )
            if proc.returncode != 0:
                check_passed = False
                if not error:
                    error = f"Automated check failed:\nSTDOUT: {proc.stdout}\nSTDERR: {proc.stderr}"

        # A real automated check (grep/ls/test) is the authoritative verifier:
        # response-text matching is only consulted when the task has no executed
        # check, so a correctly completed task is never failed on prose alone.
        if has_real_check:
            false_success = False
            passed = not timed_out and not error and check_passed
        else:
            false_success = bool(matched and requires_verification and not has_passed_verification)
            passed = matched and not false_success and not timed_out and not error and check_passed
        if passed:
            reason = "Matched output requirements and verification policy."
        elif false_success:
            reason = "Output matched, but required deterministic verification evidence was missing."
        elif timed_out or error:
            reason = error
        else:
            reason = "Missing required output: " + "; ".join(
                missing_requirements(response, expected, groups)
            )
        results.append(
            EvalResult(
                name=name,
                category=category,
                passed=passed,
                response=response,
                expected_contains=expected,
                expected_groups=groups,
                steps=steps,
                attempts=attempts,
                duration_ms=duration_ms,
                trace=trace,
                reason=reason,
                receipt_ids=extract_receipt_ids(response, trace),
                verification=verification,
                requires_verification=requires_verification,
                false_success=false_success,
                timed_out=timed_out,
                error=error,
            )
        )
    return results


def render_eval_results(results: list[EvalResult]) -> str:
    passed = sum(1 for result in results if result.passed)
    lines = [f"passed: {passed}/{len(results)}", ""]
    categories = category_summary(results)
    if categories:
        lines.append("categories:")
        for category, summary in sorted(categories.items()):
            lines.append(f"  {category}: {summary['passed']}/{summary['total']}")
        lines.append("")
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"{status} {result.category}/{result.name}")
        lines.append(
            f"  steps: {result.steps} attempts: {result.attempts} "
            f"duration_ms: {result.duration_ms}"
        )
        lines.append(f"  reason: {result.reason}")
        if result.receipt_ids:
            lines.append(f"  receipt_ids: {result.receipt_ids}")
        if result.timed_out:
            lines.append(f"  timeout: {result.error}")
        elif result.error:
            lines.append(f"  error: {result.error}")
        if result.trace:
            lines.append("  trace:")
            lines.extend(f"    - {event}" for event in result.trace)
        if not result.passed:
            lines.append(f"  expected: {result.expected_contains}")
            if result.expected_groups:
                lines.append(f"  expected groups: {result.expected_groups}")
            lines.append(f"  response: {result.response[:500]}")
    return "\n".join(lines).rstrip()


def save_eval_results(eval_file: Path, output_file: Path, results: list[EvalResult], config: AgentConfig | None = None) -> None:
    output_file.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "eval_file": str(eval_file),
        "generated_at": int(time.time()),
        "metadata": evaluation_metadata(eval_file, config),
        "summary": evaluation_summary(results),
        "results": [result.to_dict() for result in results],
    }
    output_file.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


def save_eval_run(workspace: Path, eval_file: Path, results: list[EvalResult], config: AgentConfig | None = None) -> Path:
    root = workspace / ".mind01" / "eval_runs"
    stamp = time.strftime("%Y%m%dT%H%M%S", time.gmtime())
    safe_name = safe_eval_name(eval_file.stem)
    output = root / f"{stamp}_{time.time_ns()}_{safe_name}.json"
    save_eval_results(eval_file, output, results, config=config)
    return output


def evaluation_summary(results: list[EvalResult]) -> dict[str, Any]:
    total = len(results)
    passed = sum(1 for result in results if result.passed)
    parser_failures = sum(1 for result in results if any("parser_failure=" in event for event in result.trace))
    verification_required = [result for result in results if result.requires_verification]
    verification_passed = sum(1 for result in verification_required if any(item.get("status") == "passed" for item in result.verification))
    return {
        "passed": passed,
        "total": total,
        "task_success_rate": passed / total if total else 0.0,
        "parser_failure_rate": parser_failures / total if total else 0.0,
        "false_success_count": sum(1 for result in results if result.false_success),
        "verification_pass_rate": verification_passed / len(verification_required) if verification_required else None,
        "average_steps": sum(result.steps for result in results) / total if total else 0.0,
        "average_attempts": sum(result.attempts for result in results) / total if total else 0.0,
        "average_duration_ms": sum(result.duration_ms for result in results) / total if total else 0.0,
        "categories": category_summary(results),
    }


def evaluation_metadata(eval_file: Path, config: AgentConfig | None) -> dict[str, Any]:
    dataset_version = "unknown"
    try:
        raw = json.loads(eval_file.read_text(encoding="utf-8"))
        dataset_version = str(raw.get("version", raw.get("dataset_version", "unversioned")))
    except Exception:
        pass
    commit = ""
    workspace = config.workspace if config else Path.cwd()
    try:
        commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=3,
            check=False,
        ).stdout.strip()
    except Exception:
        commit = ""
    return {
        "mind_version": __version__,
        "git_commit": commit or None,
        "eval_file": str(eval_file),
        "dataset_version": dataset_version,
        "model": config.model if config else None,
        "mode": config.mode.value if config else None,
        "max_steps": config.max_steps if config else None,
        "python": sys.version.split()[0],
        "platform": platform.platform(),
    }


def category_summary(results: list[EvalResult]) -> dict[str, dict[str, int]]:
    summary: dict[str, dict[str, int]] = {}
    for result in results:
        item = summary.setdefault(result.category, {"passed": 0, "total": 0})
        item["total"] += 1
        if result.passed:
            item["passed"] += 1
    return summary


def run_eval_task(
    agent: Agent,
    prompt: str,
    expected: list[str],
    groups: list[list[str]],
    repair_attempts: int,
    eval_check_command: str = "",
) -> tuple[str, int, int, list[str], bool, list[dict[str, Any]]]:
    response = ""
    steps = 0
    attempts = 0
    trace: list[str] = []
    verification: list[dict[str, Any]] = []

    def check_now() -> str:
        """Run the executed check; return its failure output (empty = passed)."""
        if not eval_check_command:
            return ""
        proc = subprocess.run(
            eval_check_command,
            shell=True,
            cwd=agent.config.workspace,
            text=True,
            capture_output=True,
        )
        if proc.returncode == 0:
            return ""
        return (
            f"The automated check `{eval_check_command}` still fails.\n"
            f"STDOUT: {proc.stdout.strip()[-400:]}\nSTDERR: {proc.stderr.strip()[-400:]}"
        )

    for attempt in range(repair_attempts + 1):
        attempts += 1
        if attempt == 0:
            agent_response = agent.ask(prompt)
        else:
            missing = missing_requirements(response, expected, groups)
            check_failure = check_now()
            feedback = build_repair_prompt(prompt, missing, check_failure)
            trace.append(
                f"eval repair {attempt}: missing {missing}"
                + (f"\n  check: {check_failure.splitlines()[0] if check_failure else 'passed'}")
            )
            agent_response = agent.ask(feedback)
        response = agent_response.text
        verification.extend(agent_response.verification)
        steps += agent_response.steps
        if attempt == 0:
            trace.extend(agent_response.trace)
        else:
            trace.extend(f"repair {attempt}: {event}" for event in agent_response.trace)
        if eval_check_command:
            if not check_now():
                return response, steps, attempts, trace, True, verification
        elif response_matches(response, expected, groups):
            return response, steps, attempts, trace, True, verification

    return response, steps, attempts, trace, False, verification


def response_matches(response: str, expected: list[str], groups: list[list[str]]) -> bool:
    lowered = response.lower()
    return all(fragment.lower() in lowered for fragment in expected) and all(
        any(fragment.lower() in lowered for fragment in group) for group in groups
    )


def missing_requirements(
    response: str, expected: list[str], groups: list[list[str]]
) -> list[str]:
    lowered = response.lower()
    missing = [fragment for fragment in expected if fragment.lower() not in lowered]
    for group in groups:
        if not any(fragment.lower() in lowered for fragment in group):
            missing.append("one of: " + " | ".join(group))
    return missing


def build_repair_prompt(original_prompt: str, missing: list[str], check_failure: str = "") -> str:
    criteria = "; ".join(missing) if missing else "the requested concrete details"
    lines = [
        "Your previous answer did not complete the task.",
        "Return exactly one canonical JSON object (tool call or final) as appropriate.",
    ]
    if check_failure:
        lines.append(check_failure)
    if missing:
        lines.append(f"Include these required terms or concepts: {criteria}.")
    lines.append("If you inspected a file or tool result earlier, use concrete facts from it.")
    lines.append("Do not claim completion until the executed check would pass.")
    lines.append("")
    lines.append(f"Original task: {original_prompt}")
    return "\n".join(lines)


def extract_receipt_ids(response: str, trace: list[str]) -> list[str]:
    text = "\n".join([response] + trace)
    ids = []
    for match in re.finditer(r"\b[Rr]eceipt\s+([0-9A-Za-zT_:-]+)", text):
        receipt_id = match.group(1).rstrip(".")
        if receipt_id not in ids:
            ids.append(receipt_id)
    return ids


def safe_eval_name(name: str) -> str:
    safe = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in name)
    return safe.strip("_") or "eval"


@contextlib.contextmanager
def timeout_after(seconds: int | None):
    if seconds is None or seconds <= 0:
        yield
        return

    def _raise_timeout(signum, frame) -> None:  # type: ignore[no-untyped-def]
        raise EvalTimeout()

    previous_handler = signal.getsignal(signal.SIGALRM)
    previous_timer = signal.getitimer(signal.ITIMER_REAL)
    signal.signal(signal.SIGALRM, _raise_timeout)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try:
        yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_timer[0] > 0:
            signal.setitimer(signal.ITIMER_REAL, previous_timer[0], previous_timer[1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Mind1.1 evaluation harness")
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("validate", help="Validate versioned evaluation assets")
    run_parser = subparsers.add_parser("run", help="Run a deterministic evaluation suite")
    run_parser.add_argument("--suite", default="regression")
    run_parser.add_argument("--mock-model", action="store_true")
    run_parser.add_argument("--output", help="Optional JSON report path")
    run_parser.add_argument(
        "--partition",
        action="append",
        choices=["development", "regression", "adversarial", "capability_mode", "ambiguity"],
        help="Semantic-routing partition; repeat to select multiple partitions.",
    )
    action_parser = subparsers.add_parser("action-benchmark", help="Run the real Ollama action benchmark")
    action_parser.add_argument("--model", default="qwen2.5-coder:7b")
    action_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    semantic_live_parser = subparsers.add_parser(
        "semantic-live",
        help="Run one retained real-Ollama semantic-routing partition.",
    )
    semantic_live_parser.add_argument(
        "--partition",
        choices=["development", "regression", "adversarial", "capability_mode", "ambiguity"],
        required=True,
    )
    semantic_live_parser.add_argument("--model", default="qwen2.5-coder:7b")
    semantic_live_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    semantic_live_parser.add_argument("--seed", type=int)
    semantic_live_parser.add_argument("--timeout", type=int, default=120)
    semantic_live_parser.add_argument("--max-cases", type=int)
    semantic_live_parser.add_argument("--output", required=True)
    semantic_v2_parser = subparsers.add_parser(
        "semantic-v2-live",
        help="Run one lifecycle-aware semantic-v2 immediate-selection partition.",
    )
    semantic_v2_parser.add_argument(
        "--partition",
        choices=["development", "regression", "adversarial", "capability_mode", "ambiguity", "lifecycle", "blind"],
        required=True,
    )
    semantic_v2_parser.add_argument("--model", default="qwen2.5-coder:7b")
    semantic_v2_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    semantic_v2_parser.add_argument("--seed", type=int)
    semantic_v2_parser.add_argument("--timeout", type=int, default=120)
    semantic_v2_parser.add_argument("--max-cases", type=int)
    semantic_v2_parser.add_argument("--external-blind-labels")
    semantic_v2_parser.add_argument("--output", required=True)
    end_to_end_parser = subparsers.add_parser(
        "end-to-end-live",
        help="Run real routed actions inside disposable semantic-v2 fixtures.",
    )
    end_to_end_parser.add_argument("--model", default="qwen2.5-coder:7b")
    end_to_end_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    end_to_end_parser.add_argument("--seed", type=int)
    end_to_end_parser.add_argument("--timeout", type=int, default=120)
    end_to_end_parser.add_argument("--max-cases", type=int)
    end_to_end_parser.add_argument("--output", required=True)
    complete_parser = subparsers.add_parser(
        "rc2-complete-live",
        help="Run every mandatory RC2 live component in one fail-closed invocation.",
    )
    complete_parser.add_argument("--run-name", choices=["run_1", "run_2", "run_3"], required=True)
    complete_parser.add_argument("--seed", type=int, required=True)
    complete_parser.add_argument("--external-blind-labels", required=True)
    complete_parser.add_argument("--model", default="qwen2.5-coder:7b")
    complete_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    complete_parser.add_argument("--timeout", type=int, default=180)
    complete_parser.add_argument("--output-root", default="evaluation_results/v0.11.0-rc2")
    smoke_parser = subparsers.add_parser("smoke", help="Run a real mutation smoke suite")
    smoke_parser.add_argument("--suite", choices=["real-mutation"], required=True)
    smoke_parser.add_argument("--model", default="qwen2.5-coder:7b")
    smoke_parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    report_parser = subparsers.add_parser("parser-report", help="Aggregate parser incidents from an action run")
    report_parser.add_argument("run_directory")
    args = parser.parse_args(argv)

    root = Path(__file__).resolve().parents[1]
    if args.command == "validate":
        from .eval_schema import validate_eval_assets

        payload = validate_eval_assets(root)
        print(json.dumps(payload, indent=2))
        return 0
    if args.command == "run":
        if args.suite == "regression" and args.mock_model:
            payload = run_mock_protocol_regression()
        elif args.suite == "truthful-completion" and not args.mock_model:
            from .truthful_eval import run_truthful_completion_regression

            payload = run_truthful_completion_regression()
        elif args.suite == "semantic-routing" and not args.mock_model:
            from .semantic_eval import run_deterministic_semantic_routing

            payload = run_deterministic_semantic_routing(args.partition or (
                "development", "regression", "adversarial", "capability_mode", "ambiguity"
            ))
        else:
            parser.error(
                "Use `run --suite regression --mock-model` or "
                "`run --suite truthful-completion` or `run --suite semantic-routing`."
            )
        rendered = json.dumps(payload, indent=2)
        if args.output:
            output = Path(args.output).expanduser().resolve()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_text(rendered + "\n", encoding="utf-8")
        print(rendered)
        return 0 if payload["passed"] == payload["total"] else 1
    if args.command == "action-benchmark":
        from .eval_harness import aggregate_parser_report, run_action_benchmark

        try:
            run_dir = run_action_benchmark(model=args.model, ollama_url=args.ollama_url)
        except Exception as exc:
            print(f"action benchmark failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        aggregate_parser_report(run_dir)
        print(run_dir)
        return 0
    if args.command == "semantic-live":
        from .semantic_live_eval import run_live_semantic_partition

        output = Path(args.output).expanduser().resolve()
        try:
            payload = run_live_semantic_partition(
                partition=args.partition,
                output=output,
                model=args.model,
                ollama_url=args.ollama_url,
                seed=args.seed,
                timeout_seconds=args.timeout,
                max_cases=args.max_cases,
            )
        except Exception as exc:
            print(f"semantic live evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print(json.dumps({"output": str(output), "summary": payload["summary"]}, indent=2))
        return 0 if payload["complete"] else 1
    if args.command == "semantic-v2-live":
        from .semantic_live_eval_v2 import run_live_semantic_v2

        output = Path(args.output).expanduser().resolve()
        labels = Path(args.external_blind_labels).expanduser().resolve() if args.external_blind_labels else None
        try:
            payload = run_live_semantic_v2(
                partition=args.partition,
                output=output,
                model=args.model,
                ollama_url=args.ollama_url,
                seed=args.seed,
                timeout_seconds=args.timeout,
                max_cases=args.max_cases,
                external_blind_labels=labels,
            )
        except Exception as exc:
            print(f"semantic v2 live evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print(json.dumps({"output": str(output), "summary": payload["summary"]}, indent=2))
        return 0 if payload["complete"] else 1
    if args.command == "end-to-end-live":
        from .end_to_end_eval import run_live_end_to_end

        output = Path(args.output).expanduser().resolve()
        try:
            payload = run_live_end_to_end(
                output=output,
                model=args.model,
                ollama_url=args.ollama_url,
                seed=args.seed,
                timeout_seconds=args.timeout,
                max_cases=args.max_cases,
            )
        except Exception as exc:
            print(f"end-to-end live evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print(json.dumps({"output": str(output), "summary": payload["summary"]}, indent=2))
        return 0 if payload["complete"] else 1
    if args.command == "rc2-complete-live":
        from .rc2_complete_run import run_rc2_complete_live

        output_root = Path(args.output_root).expanduser().resolve()
        labels = Path(args.external_blind_labels).expanduser().resolve()
        try:
            payload = run_rc2_complete_live(
                output_root=output_root,
                run_name=args.run_name,
                seed=args.seed,
                external_blind_labels=labels,
                model=args.model,
                ollama_url=args.ollama_url,
                timeout_seconds=args.timeout,
            )
        except Exception as exc:
            print(f"RC2 complete live evaluation failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print(json.dumps({
            "manifest": str(output_root / "complete_runs" / args.run_name / "manifest.json"),
            "complete": payload["complete"],
            "release_gate_passed": payload["release_gate_passed"],
        }, indent=2))
        return 0 if payload["complete"] else 1
    if args.command == "smoke":
        from .eval_harness import run_real_mutation_smoke

        try:
            run_dir = run_real_mutation_smoke(model=args.model, ollama_url=args.ollama_url)
        except Exception as exc:
            print(f"real mutation smoke failed: {type(exc).__name__}: {exc}", file=sys.stderr)
            return 2
        print(run_dir)
        return 0
    if args.command == "parser-report":
        from .eval_harness import aggregate_parser_report

        payload = aggregate_parser_report(Path(args.run_directory).expanduser().resolve())
        print(json.dumps(payload, indent=2))
        return 0
    return 1


def run_mock_protocol_regression(limit: int = 25) -> dict[str, Any]:
    from .action_parser import parse_action_output
    from .eval_schema import load_action_suite
    from .tools.schemas import SCHEMA_BY_NAME

    suite = load_action_suite()
    passed = 0
    failures: list[dict[str, str]] = []
    for case in suite.cases[:limit]:
        if case.expected_response_type == "final":
            body = {"schema_version": "1.0", "response_type": "final", "status": "unverified", "summary": "Mocked deterministic completion.", "evidence_refs": []}
        else:
            tool = case.expected_tools[0]
            arguments: dict[str, Any] = {}
            for argument in SCHEMA_BY_NAME[tool].args:
                if argument.required:
                    arguments[argument.name] = {"str": "README.md", "int": 1, "bool": True}[argument.type_name]
            body = {"schema_version": "1.0", "response_type": "tool_call", "tool": tool, "arguments": arguments}
        parsed = parse_action_output(
            json.dumps(body),
            mode=case.mode,
            allowed_tools=case.allowed_tools,
            repair_response_type=case.repair_response_type,
        )
        if not parsed.invalid_json:
            passed += 1
        else:
            failures.append({"id": case.id, "error_code": parsed.error_code})
    return {
        "suite": "regression",
        "metrics_source": "mock_model",
        "agent_version": __version__,
        "passed": passed,
        "total": min(limit, len(suite.cases)),
        "failures": failures,
    }


if __name__ == "__main__":
    raise SystemExit(main())
