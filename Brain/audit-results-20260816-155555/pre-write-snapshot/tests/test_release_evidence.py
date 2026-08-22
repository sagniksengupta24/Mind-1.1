from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

from scripts.generate_release_evidence import sha256_file


def test_release_hash_helper_is_content_addressed(tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.bin"
    artifact.write_bytes(b"mind-release-evidence")
    assert sha256_file(artifact) == hashlib.sha256(b"mind-release-evidence").hexdigest()


def test_release_evidence_script_is_directly_importable() -> None:
    root = Path(__file__).resolve().parents[1]
    completed = subprocess.run(
        [sys.executable, "scripts/generate_release_evidence.py", "--help"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=10,
    )
    assert completed.returncode == 0, completed.stdout
    assert "Generate retained Mind1.1 release evidence" in completed.stdout
