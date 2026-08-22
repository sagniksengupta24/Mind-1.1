from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.build_release import build_release


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_command(
    argv: list[str],
    *,
    timeout: int = 240,
    cwd: Path = ROOT,
) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=cwd,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            env={**os.environ, "PYTHONNOUSERSITE": "1"},
        )
        return {
            "command": argv,
            "cwd": str(cwd),
            "exit_code": completed.returncode,
            "duration_seconds": round(time.monotonic() - started, 3),
            "output": completed.stdout or "",
        }
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {
            "command": argv,
            "cwd": str(cwd),
            "exit_code": None,
            "duration_seconds": round(time.monotonic() - started, 3),
            "output": f"{type(exc).__name__}: {exc}",
        }


def git_text(*args: str) -> str | None:
    result = run_command(["git", *args], timeout=10)
    if result["exit_code"] != 0:
        return None
    return str(result["output"]).strip() or None


def tool_version(argv: list[str]) -> dict[str, Any]:
    path = shutil.which(argv[0])
    if not path:
        return {"available": False, "path": None, "version": None}
    result = run_command(argv, timeout=10)
    return {
        "available": result["exit_code"] == 0,
        "path": path,
        "version": str(result["output"]).strip()[:500],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate retained Mind1.1 release evidence.")
    parser.add_argument("--release", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()

    output = Path(args.output_dir).expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    artifacts = output / "artifacts"
    artifacts.mkdir(exist_ok=True)

    commit = git_text("rev-parse", "HEAD")
    tree = git_text("rev-parse", "HEAD^{tree}")
    branch = git_text("branch", "--show-current")
    dirty_output = git_text("status", "--porcelain")
    dirty = dirty_output is not None

    commands = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "compileall", "-q", "mind01", "tests", "scripts"],
        [sys.executable, "-m", "mind01.eval", "validate"],
        [sys.executable, "-m", "mind01.eval", "run", "--suite", "regression", "--mock-model"],
        [sys.executable, "-m", "mind01.eval", "run", "--suite", "truthful-completion"],
        [sys.executable, "scripts/check_package.py"],
        [sys.executable, "-m", "mind01.cli", "--version"],
        [sys.executable, "-c", "import mind01; print(mind01.__version__)"],
    ]
    command_results = [run_command(command) for command in commands]

    source_archive = build_release(ROOT, artifacts)
    with tempfile.TemporaryDirectory(prefix="mind-release-wheel-") as directory:
        staging = Path(directory) / "source"
        staging.mkdir()
        with zipfile.ZipFile(source_archive) as archive:
            archive.extractall(staging)
        staged_roots = [path for path in staging.iterdir() if path.is_dir()]
        if len(staged_roots) != 1:
            raise RuntimeError("Source archive must contain exactly one project root.")
        wheel_result = run_command(
            [
                sys.executable,
                "-m",
                "pip",
                "wheel",
                ".",
                "--no-deps",
                "--no-build-isolation",
                "--no-index",
                "--wheel-dir",
                str(Path(directory) / "wheel"),
            ],
            cwd=staged_roots[0],
        )
        command_results.append(wheel_result)
        wheels = list((Path(directory) / "wheel").glob("*.whl"))
        wheel = artifacts / wheels[0].name if len(wheels) == 1 else None
        if wheel is not None:
            shutil.copy2(wheels[0], wheel)

    from mind01.truthful_eval import run_truthful_completion_regression

    truthful = run_truthful_completion_regression()
    (output / "truthful_completion.json").write_text(
        json.dumps(truthful, indent=2) + "\n", encoding="utf-8"
    )
    (output / "commands.json").write_text(
        json.dumps(command_results, indent=2) + "\n", encoding="utf-8"
    )

    config_identity = {
        "release": args.release,
        "commands": commands,
        "python_executable": sys.executable,
    }
    configuration_sha = hashlib.sha256(
        json.dumps(config_identity, sort_keys=True).encode("utf-8")
    ).hexdigest()
    all_commands_passed = all(item["exit_code"] == 0 for item in command_results)
    verified_count = int(truthful["verified_result_count"])
    complete_count = int(truthful["verified_with_complete_mapping_count"])
    gate_passed = bool(
        all_commands_passed
        and not dirty
        and truthful["passed"] == truthful["total"]
        and truthful["false_success_count"] == 0
        and verified_count > 0
        and verified_count == complete_count
        and commit
        and tree
        and wheel
    )
    manifest = {
        "schema_version": "1.0",
        "release": args.release,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": commit,
        "git_tree": tree,
        "git_branch": branch,
        "dirty": dirty,
        "source_archive": str(source_archive.relative_to(output)),
        "source_archive_sha256": sha256_file(source_archive),
        "wheel": str(wheel.relative_to(output)) if wheel else None,
        "wheel_sha256": sha256_file(wheel) if wheel else None,
        "model_name": None,
        "model_digest": None,
        "ollama_version": tool_version(["ollama", "--version"]),
        "system_prompt_sha256": sha256_file(ROOT / "mind01" / "prompts.py"),
        "tool_schema_sha256": sha256_file(ROOT / "mind01" / "tools" / "schemas.py"),
        "suite_sha256": truthful["suite_sha256"],
        "configuration_sha256": configuration_sha,
        "environment": {
            "python": sys.version,
            "platform": platform.platform(),
            "docker": tool_version(["docker", "--version"]),
            "iverilog": tool_version(["iverilog", "-V"]),
            "verilator": tool_version(["verilator", "--version"]),
            "yosys": tool_version(["yosys", "-V"]),
            "z3": tool_version(["z3", "--version"]),
        },
        "commands": [
            {
                "command": item["command"],
                "exit_code": item["exit_code"],
                "duration_seconds": item["duration_seconds"],
            }
            for item in command_results
        ],
        "results": {
            "release_gate_passed": gate_passed,
            "all_deterministic_commands_passed": all_commands_passed,
            "truthful_completion": {
                "passed": truthful["passed"],
                "total": truthful["total"],
                "false_success_count": truthful["false_success_count"],
                "verified_result_count": verified_count,
                "verified_with_complete_mapping_count": complete_count,
            },
            "live_model": "not_run",
            "hidden_coding": "not_run",
            "security_sandbox": "not_run",
            "performance": "not_run",
        },
        "known_limitations": [
            "No live-model benchmark was run for v0.10.0.",
            "Historical 62% semantic tool-family and 2/3 mutation reports are not retained locally.",
            "Host execution is controlled but not sandboxed.",
            "Authentication remains a single local token.",
            "Ordinary evaluation datasets are not yet versioned or split.",
            "No open-source redistribution license has been selected.",
            "Release evidence is hash-addressed but not externally signed.",
        ],
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    report = render_report(manifest)
    (output / "report.md").write_text(report, encoding="utf-8")
    print(json.dumps(manifest, indent=2))
    return 0 if gate_passed else 1


def render_report(manifest: dict[str, Any]) -> str:
    result = manifest["results"]
    truthful = result["truthful_completion"]
    status = "PASSED" if result["release_gate_passed"] else "FAILED"
    return f"""# Mind1.1 {manifest['release']} release evidence

Release gate: **{status}**

## Identity

- Commit: `{manifest['git_commit']}`
- Tree: `{manifest['git_tree']}`
- Branch: `{manifest['git_branch']}`
- Dirty before verification: `{manifest['dirty']}`
- Source SHA-256: `{manifest['source_archive_sha256']}`
- Wheel SHA-256: `{manifest['wheel_sha256']}`
- Suite SHA-256: `{manifest['suite_sha256']}`

## Deterministic results

- Canonical commands passed: `{result['all_deterministic_commands_passed']}`
- Truthful-completion cases: `{truthful['passed']}/{truthful['total']}`
- False successes: `{truthful['false_success_count']}`
- Verified controls with complete evidence mapping: `{truthful['verified_with_complete_mapping_count']}/{truthful['verified_result_count']}`

## Evidence categories not run

- Live model: `{result['live_model']}`
- Hidden coding: `{result['hidden_coding']}`
- Sandbox security: `{result['security_sandbox']}`
- Performance: `{result['performance']}`

## Known limitations

""" + "".join(f"- {item}\n" for item in manifest["known_limitations"])


if __name__ == "__main__":
    raise SystemExit(main())
