from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from mind01 import __version__
from scripts.build_release import build_release


def main() -> int:
    root = ROOT
    with tempfile.TemporaryDirectory(prefix="mind-package-check-") as directory:
        temp = Path(directory)
        wheel_dir = temp / "wheel"
        install_dir = temp / "install"
        wheel_dir.mkdir()
        install_dir.mkdir()
        source_archive = build_release(root, temp / "source-archive")
        source_dir = temp / "source"
        source_dir.mkdir()
        with zipfile.ZipFile(source_archive) as archive:
            archive.extractall(source_dir)
        source_roots = [path for path in source_dir.iterdir() if path.is_dir()]
        if len(source_roots) != 1:
            print("Expected exactly one staged source root.")
            return 1
        staged_root = source_roots[0]
        pip_env = dict(os.environ)
        pip_env.update({"PIP_DISABLE_PIP_VERSION_CHECK": "1", "PIP_NO_CACHE_DIR": "1"})
        build = subprocess.run(
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
                str(wheel_dir),
            ],
            cwd=staged_root,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            env=pip_env,
        )
        if build.returncode != 0:
            print(build.stdout)
            return build.returncode
        wheels = list(wheel_dir.glob("*.whl"))
        if len(wheels) != 1:
            print(f"Expected one wheel, found {len(wheels)}.")
            return 1
        wheel = wheels[0]
        with zipfile.ZipFile(wheel) as archive:
            names = archive.namelist()
        forbidden = (".mind01", ".sqlite3", "traces/", "receipts/", "__pycache__")
        if any(any(token in name for token in forbidden) for name in names):
            print("Wheel contains forbidden runtime state.")
            return 1
        materialized_fixtures = (
            "real_mutation/syntax/broken.py",
            "real_mutation/failing_test/test_calc.py",
        )
        if any(name.endswith(materialized_fixtures) for name in names):
            print("Wheel contains a materialized evaluation fixture.")
            return 1
        required_templates = (
            "real_mutation/syntax/broken.py.fixture",
            "real_mutation/failing_test/test_calc.py.fixture",
        )
        if not all(any(name.endswith(template) for name in names) for template in required_templates):
            print("Wheel is missing an evaluation fixture template.")
            return 1
        install = subprocess.run(
            [sys.executable, "-m", "pip", "install", "--no-deps", "--no-index", "--target", str(install_dir), str(wheel)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
            env=pip_env,
        )
        if install.returncode != 0:
            print(install.stdout)
            return install.returncode
        env = dict(os.environ)
        env["PYTHONPATH"] = str(install_dir)
        check = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import mind01; "
                    "from mind01.agent import Agent; "
                    "from mind01.api import MindAPI; "
                    f"assert mind01.__version__ == {__version__!r}; "
                    "print(mind01.__version__, Agent.__name__, MindAPI.__name__)"
                ),
            ],
            cwd=temp,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=30,
        )
        print(check.stdout.strip())
        return check.returncode


if __name__ == "__main__":
    raise SystemExit(main())
