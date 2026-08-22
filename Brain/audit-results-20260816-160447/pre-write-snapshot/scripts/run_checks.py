from __future__ import annotations

import subprocess
import sys


COMMANDS = [
    [sys.executable, "-m", "pytest", "-q"],
    [sys.executable, "-m", "compileall", "-q", "mind01", "tests", "scripts"],
    [sys.executable, "-m", "mind01.eval", "validate"],
    [sys.executable, "-m", "mind01.eval", "run", "--suite", "regression", "--mock-model"],
    [sys.executable, "-m", "mind01.eval", "run", "--suite", "truthful-completion"],
    [sys.executable, "-m", "mind01.eval", "run", "--suite", "semantic-routing", "--partition", "development"],
    [
        sys.executable,
        "-m",
        "mind01.cli",
        "eval",
        "evals/basic.json",
        "--dry-run",
        "--workspace",
        ".",
        "--task-timeout",
        "5",
        "--repair-attempts",
        "1",
    ],
    [sys.executable, "scripts/check_package.py"],
]



def main() -> int:
    for command in COMMANDS:
        print("+", " ".join(command))
        completed = subprocess.run(command)
        if completed.returncode != 0:
            return completed.returncode
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
