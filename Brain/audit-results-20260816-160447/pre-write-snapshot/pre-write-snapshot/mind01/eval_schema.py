from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .action_parser import ResponseMode
from .tools.schemas import SCHEMA_BY_NAME


ACTION_BENCHMARK_VERSION = "action-reliability-v1"


@dataclass(frozen=True)
class ActionBenchmarkCase:
    id: str
    category: str
    prompt: str
    mode: ResponseMode
    allowed_tools: tuple[str, ...]
    expected_tools: tuple[str, ...] = ()
    expected_response_type: str = "tool_call"
    repair_response_type: str | None = None
    repair_allowed: bool = True
    max_repair_attempts: int = 2


@dataclass(frozen=True)
class ActionBenchmarkSuite:
    schema_version: str
    benchmark_version: str
    cases: tuple[ActionBenchmarkCase, ...]
    source_path: Path
    source_hash: str


def default_action_suite_path() -> Path:
    return Path(__file__).resolve().parent / "eval_suites" / "action_reliability_v1.json"


def load_action_suite(path: Path | None = None) -> ActionBenchmarkSuite:
    source = (path or default_action_suite_path()).resolve()
    text = source.read_text(encoding="utf-8")
    data = json.loads(text)
    if data.get("schema_version") != "1.0":
        raise ValueError("Action benchmark schema_version must be '1.0'.")
    raw_cases = data.get("cases")
    if not isinstance(raw_cases, list) or len(raw_cases) < 50:
        raise ValueError("Action benchmark must contain at least 50 cases.")
    cases: list[ActionBenchmarkCase] = []
    ids: set[str] = set()
    for index, item in enumerate(raw_cases, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Action benchmark case {index} must be an object.")
        identifier = str(item.get("id", ""))
        if not identifier or identifier in ids:
            raise ValueError(f"Action benchmark case {index} has a missing or duplicate id.")
        ids.add(identifier)
        mode = ResponseMode(str(item.get("mode", "")))
        allowed = tuple(str(name) for name in item.get("allowed_tools", []))
        unknown = sorted(set(allowed) - set(SCHEMA_BY_NAME))
        if unknown:
            raise ValueError(f"Case {identifier} exposes unknown tools: {', '.join(unknown)}")
        expected_type = str(item.get("expected_response_type", "tool_call"))
        expected_tools = tuple(str(name) for name in item.get("expected_tools", []))
        if expected_type == "tool_call" and not expected_tools:
            raise ValueError(f"Case {identifier} must define expected_tools.")
        if not set(expected_tools).issubset(allowed):
            raise ValueError(f"Case {identifier} expects a hidden tool.")
        repair_type = item.get("repair_response_type")
        if repair_type is not None and repair_type not in {"tool_call", "final"}:
            raise ValueError(f"Case {identifier} has invalid repair_response_type.")
        cases.append(
            ActionBenchmarkCase(
                id=identifier,
                category=str(item.get("category", "uncategorized")),
                prompt=str(item.get("prompt", "")),
                mode=mode,
                allowed_tools=allowed,
                expected_tools=expected_tools,
                expected_response_type=expected_type,
                repair_response_type=str(repair_type) if repair_type else None,
                repair_allowed=bool(item.get("repair_allowed", True)),
                max_repair_attempts=max(0, min(int(item.get("max_repair_attempts", 2)), 2)),
            )
        )
    return ActionBenchmarkSuite(
        schema_version="1.0",
        benchmark_version=str(data.get("benchmark_version", ACTION_BENCHMARK_VERSION)),
        cases=tuple(cases),
        source_path=source,
        source_hash=hashlib.sha256(text.encode("utf-8")).hexdigest(),
    )


def validate_eval_assets(root: Path) -> dict[str, Any]:
    from .semantic_eval import validate_semantic_routing_assets
    from .truthful_eval import load_truthful_suite

    ordinary_tasks = 0
    files = []
    for path in sorted((root / "evals").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        tasks = data.get("tasks")
        if not isinstance(tasks, list):
            raise ValueError(f"{path} does not contain a tasks list.")
        ordinary_tasks += len(tasks)
        files.append(str(path.relative_to(root)))
    suite = load_action_suite()
    truthful = load_truthful_suite()
    semantic = validate_semantic_routing_assets(root)
    return {
        "ordinary_eval_files": files,
        "ordinary_task_count": ordinary_tasks,
        "action_benchmark_cases": len(suite.cases),
        "action_benchmark_version": suite.benchmark_version,
        "action_benchmark_hash": suite.source_hash,
        "truthful_completion_cases": len(truthful["cases"]),
        "truthful_completion_version": truthful["suite_version"],
        "truthful_completion_hash": truthful["source_sha256"],
        "semantic_routing": semantic,
    }
