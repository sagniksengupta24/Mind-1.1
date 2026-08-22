from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.build_release import build_release


def run(argv: list[str], expected_exit_codes: tuple[int, ...] = (0,), timeout: int = 300) -> dict[str, Any]:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
        )
        output = completed.stdout or ""
        exit_code: int | None = completed.returncode
    except (OSError, subprocess.TimeoutExpired) as exc:
        output = f"{type(exc).__name__}: {exc}"
        exit_code = None
    return {
        "command": argv,
        "cwd": str(ROOT),
        "exit_code": exit_code,
        "expected_exit_codes": list(expected_exit_codes),
        "outcome_as_expected": exit_code in expected_exit_codes,
        "duration_seconds": round(time.monotonic() - started, 3),
        "output_sha256": hashlib.sha256(output.encode("utf-8", errors="replace")).hexdigest(),
        "output": output if len(output) <= 20_000 else output[:20_000] + "\n[retained command output truncated at 20000 characters]\n",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Capture canonical v0.11 candidate checks.")
    parser.add_argument("--output-dir", default="evaluation_results/v0.11.0-release")
    args = parser.parse_args()
    output = (ROOT / args.output_dir).resolve() if not Path(args.output_dir).is_absolute() else Path(args.output_dir)
    artifacts = output / "artifacts"
    artifacts.mkdir(parents=True, exist_ok=True)

    commands: list[tuple[list[str], tuple[int, ...], int]] = [
        ([sys.executable, "-m", "pip", "install", "-e", ".[dev]", "--no-build-isolation"], (0,), 300),
        ([sys.executable, "-m", "pytest", "-q"], (0,), 300),
        ([sys.executable, "-m", "compileall", "-q", "mind01", "tests", "scripts"], (0,), 120),
        ([sys.executable, "scripts/run_checks.py"], (0,), 300),
        ([sys.executable, "-m", "mind01.eval", "validate"], (0,), 120),
        ([sys.executable, "-m", "mind01.eval", "run", "--suite", "regression", "--mock-model"], (0,), 120),
        ([sys.executable, "-m", "mind01.eval", "run", "--suite", "truthful-completion"], (0,), 120),
        ([sys.executable, "-m", "mind01.eval", "run", "--suite", "semantic-routing", "--partition", "development"], (0,), 120),
        # The complete deterministic set is expected to fail 16 contradictory,
        # frozen adversarial mutation-intent labels.  Exit 1 is retained, not hidden.
        ([sys.executable, "-m", "mind01.eval", "run", "--suite", "semantic-routing"], (1,), 120),
        ([sys.executable, "scripts/check_package.py"], (0,), 120),
        ([sys.executable, "-m", "mind01.cli", "--version"], (0,), 30),
        ([sys.executable, "-c", "import mind01; print(mind01.__version__)"], (0,), 30),
        (
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
                str(artifacts),
            ],
            (0,),
            300,
        ),
    ]
    results = [run(argv, expected, timeout) for argv, expected, timeout in commands]
    source_archive = build_release(ROOT, artifacts)
    payload = {
        "schema_version": "1.0",
        "commands": results,
        "all_outcomes_as_expected": all(item["outcome_as_expected"] for item in results),
        "expected_known_failure": "The full deterministic semantic suite exits 1 for 16 frozen contradictory mutation-intent labels.",
        "source_archive": str(source_archive.relative_to(output)),
    }
    (output / "commands.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"commands": len(results), "all_outcomes_as_expected": payload["all_outcomes_as_expected"]}, indent=2))
    return 0 if payload["all_outcomes_as_expected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
