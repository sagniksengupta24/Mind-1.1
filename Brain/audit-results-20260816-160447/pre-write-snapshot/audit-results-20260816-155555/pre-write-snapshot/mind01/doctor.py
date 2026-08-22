from __future__ import annotations

import json
import platform
import shutil
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    fix: str = ""


def run_doctor(model: str, ollama_url: str, *, provider: str = "ollama", api_key: str = "", base_url: str = "") -> list[Check]:
    """Environment/connectivity checks.

    `provider="ollama"` (the default, and the only mode when called with
    just the original two positional args) preserves the original local
    checks unchanged. For a cloud provider, pass `provider=` (and
    `api_key`/`base_url`) to get provider-appropriate checks instead of
    misleadingly checking for a local Ollama server that isn't in use.
    """
    checks = [
        Check(
            "python",
            True,
            f"{sys.version.split()[0]} on {platform.platform()}",
        )
    ]

    if provider != "ollama":
        checks.append(
            Check(
                "provider",
                True,
                f"using cloud provider `{provider}` — local Ollama checks skipped",
            )
        )
        checks.append(
            Check(
                "api-key",
                bool(api_key),
                "present" if api_key else "missing",
                "Set --api-key / OPENROUTER_API_KEY (or LLM_API_KEY) before running.",
            )
        )
        resolved_base_url = base_url or ("https://openrouter.ai/api/v1" if provider == "openrouter" else "")
        checks.append(
            Check(
                "base-url",
                bool(resolved_base_url),
                resolved_base_url or "not set",
                "Set --base-url / LLM_BASE_URL." if not resolved_base_url else "",
            )
        )
        checks.append(
            Check(
                "model",
                bool(model.strip()),
                model or "not set",
                "Set --model / LLM_MODEL to a model ID your provider serves.",
            )
        )
        checks.append(
            Check(
                "connectivity",
                True,
                "not checked — cloud reachability isn't probed to avoid spending a paid/rate-limited request",
                "Run `mind01 ask ...` once; a connectivity or auth problem will surface there as a clear error.",
            )
        )
        return checks

    ollama_path = shutil.which("ollama")
    checks.append(
        Check(
            "ollama-cli",
            ollama_path is not None,
            ollama_path or "not found",
            "Install Ollama, then run `ollama serve`.",
        )
    )

    tags = fetch_ollama_tags(ollama_url)
    if tags is None:
        checks.append(
            Check(
                "ollama-server",
                False,
                f"not reachable at {ollama_url}",
                "Start Ollama with `ollama serve`.",
            )
        )
        checks.append(
            Check(
                "model",
                False,
                f"cannot check `{model}` until Ollama is reachable",
                f"After starting Ollama, run `ollama pull {model}`.",
            )
        )
        return checks

    checks.append(Check("ollama-server", True, f"reachable at {ollama_url}"))
    models = extract_model_names(tags)
    has_model = model in models
    checks.append(
        Check(
            "model",
            has_model,
            f"{model} {'is available' if has_model else 'is not pulled'}",
            f"Run `ollama pull {model}`.",
        )
    )
    return checks


def fetch_ollama_tags(ollama_url: str) -> dict | None:
    request = urllib.request.Request(f"{ollama_url.rstrip('/')}/api/tags")
    try:
        with urllib.request.urlopen(request, timeout=3) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def extract_model_names(tags: dict) -> set[str]:
    models = tags.get("models", [])
    names = set()
    for model in models:
        if isinstance(model, dict) and isinstance(model.get("name"), str):
            names.add(model["name"])
            names.add(model["name"].split(":")[0])
    return names


def render_doctor(checks: list[Check]) -> str:
    lines = []
    for check in checks:
        status = "ok" if check.ok else "missing"
        lines.append(f"{status:7} {check.name}: {check.detail}")
        if not check.ok and check.fix:
            lines.append(f"        fix: {check.fix}")
    return "\n".join(lines)

def run_doctor_eval(config: Any) -> int:
    from .eval import run_eval_file
    eval_file = config.workspace / "eval" / "tasks" / "suite.yaml"
    if not eval_file.exists():
        print(f"No eval suite found at {eval_file}.")
        return 1
    
    # WS5: eval runs may opt in to recording task bundles (consent-gated) in
    # the existing hash-chained trace store as SFT seed data.
    if not hasattr(config, "trace_bundles"):
        config.trace_bundles = True
    results = run_eval_file(config, eval_file, task_timeout=120)
    total = len(results)
    if total == 0:
        print("No tasks found in eval suite.")
        return 1

    completion_count = sum(1 for r in results if r.passed)
    completion_rate = (completion_count / total) * 100

    verif_req = [r for r in results if r.requires_verification]
    if verif_req:
        verif_passed = sum(1 for r in verif_req if any(item.get("status") == "passed" for item in r.verification))
        verification_pass_rate = (verif_passed / len(verif_req)) * 100
    else:
        verification_pass_rate = 100.0

    repair_required_count = sum(1 for r in results if r.attempts > 1)
    repair_required_rate = (repair_required_count / total) * 100
    
    avg_steps = sum(r.steps for r in results) / total
    avg_latency = sum(r.duration_ms for r in results) / total / 1000.0

    print("Eval Suite Report:")
    print(f"Total Tasks:           {total}")
    print(f"Completion Rate:       {completion_rate:.1f}% ({completion_count}/{total})")
    print(f"Verification Pass Rate:{verification_pass_rate:.1f}%")
    print(f"Repair Required Rate:  {repair_required_rate:.1f}%")
    print(f"Average Steps:         {avg_steps:.1f}")
    print(f"Average Latency (s):   {avg_latency:.1f}")
    
    return 0 if completion_count == total else 1
