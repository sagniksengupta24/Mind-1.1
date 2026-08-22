from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import mind01


def test_version_is_0111_dev0_everywhere() -> None:
    root = Path(__file__).resolve().parents[1]
    assert mind01.__version__ == "0.11.1.dev0"
    assert 'version = "0.11.1.dev0"' in (root / "pyproject.toml").read_text(encoding="utf-8")
    assert '__version__ = "0.11.1.dev0"' in (root / "mind01" / "version.py").read_text(encoding="utf-8")


def test_cli_version() -> None:
    completed = subprocess.run(
        [sys.executable, "-m", "mind01.cli", "--version"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
    )
    assert completed.returncode == 0
    assert completed.stdout.strip() == "mind01 0.11.1.dev0"
