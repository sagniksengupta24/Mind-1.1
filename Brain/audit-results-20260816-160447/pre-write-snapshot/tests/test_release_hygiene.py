from __future__ import annotations

import shutil
import subprocess
import sys
import tarfile
import tempfile
import zipfile

from scripts.build_release import build_release
from pathlib import Path

from mind01 import __version__


def test_version_is_centralized() -> None:
    root = Path(__file__).resolve().parents[1]
    pyproject = (root / "pyproject.toml").read_text(encoding="utf-8")
    assert f'version = "{__version__}"' in pyproject


def test_built_artifacts_exclude_private_runtime_state() -> None:
    root = Path(__file__).resolve().parents[1]
    out = Path(tempfile.mkdtemp(prefix="mind-dist-"))
    try:
        archive = build_release(root, out / "source-archive")
        source = out / "source"
        source.mkdir()
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(source)
        staged_roots = [path for path in source.iterdir() if path.is_dir()]
        assert len(staged_roots) == 1
        completed = subprocess.run(
            [sys.executable, "-m", "pip", "wheel", ".", "--no-deps", "--no-build-isolation", "--wheel-dir", str(out)],
            cwd=staged_roots[0],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=120,
        )
        assert completed.returncode == 0, completed.stdout
        names: list[str] = []
        for artifact in out.iterdir():
            if artifact.suffix == ".whl":
                with zipfile.ZipFile(artifact) as archive:
                    names.extend(archive.namelist())
        forbidden = (".mind01", "sessions.sqlite3", "memory.sqlite3", "traces/", "receipts/")
        assert not any(any(token in name for token in forbidden) for name in names)
        assert any(name.endswith("broken.py.fixture") for name in names)
        assert not any(name.endswith("real_mutation/syntax/broken.py") for name in names)
        assert any(name.endswith("test_calc.py.fixture") for name in names)
        assert not any(name.endswith("real_mutation/failing_test/test_calc.py") for name in names)
    finally:
        shutil.rmtree(out)


def test_clean_source_release_excludes_working_state_and_history() -> None:
    root = Path(__file__).resolve().parents[1]
    out = Path(tempfile.mkdtemp(prefix="mind-source-release-"))
    try:
        archive = build_release(root, out)
        assert archive.exists()
        with zipfile.ZipFile(archive) as zipped:
            names = zipped.namelist()
        forbidden = (
            ".mind01",
            "__pycache__",
            ".pytest_cache",
            ".coverage",
            "raw_benchmark_outputs",
            "results_v0_",
            ".sqlite3",
            ".egg-info",
        )
        assert not any(any(token in name for token in forbidden) for name in names)
        assert any(name.endswith("mind01/agent.py") for name in names)
        assert any(name.endswith("SECURITY.md") for name in names)
    finally:
        shutil.rmtree(out)
