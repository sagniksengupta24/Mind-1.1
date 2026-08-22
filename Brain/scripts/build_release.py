from __future__ import annotations

import argparse
import re
import shutil
import tempfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_VERSION_TEXT = (ROOT / "mind01" / "version.py").read_text(encoding="utf-8")
_VERSION_MATCH = re.search(r'__version__\s*=\s*["\']([^"\']+)["\']', _VERSION_TEXT)
if not _VERSION_MATCH:
    raise RuntimeError("Could not read the centralized Mind1.1 version.")
__version__ = _VERSION_MATCH.group(1)

ROOT_FILES = {
    ".env.example",
    ".gitignore",
    "CHANGELOG.md",
    "LICENSE_STATUS.md",
    "MANIFEST.in",
    "README.md",
    "SECURITY.md",
    "THREAT_MODEL.md",
    "pyproject.toml",
}
SOURCE_DIRS = {"mind01", "tests", "scripts", "docs", "examples"}
EVAL_FILES = {
    "README.md",
    "basic.json",
    "coding.json",
    "docs_rag.json",
    "failure_taxonomy.md",
    "full_suite.json",
    "indic_languages.json",
    "mind_foundation.json",
    "memory.json",
    "repo_analysis.json",
    "safety.json",
    "scoring_rubric.md",
    "semiconductor.json",
}
EXCLUDED_PARTS = {
    ".git",
    ".mind01",
    ".pytest_cache",
    "__pycache__",
    "build",
    "dist",
}
EXCLUDED_SUFFIXES = {".pyc", ".pyo", ".sqlite3", ".db", ".coverage"}


def should_copy(path: Path) -> bool:
    if any(part in EXCLUDED_PARTS or part.endswith(".egg-info") for part in path.parts):
        return False
    if path.suffix in EXCLUDED_SUFFIXES:
        return False
    return True


def copy_tree(source: Path, target: Path) -> None:
    for path in source.rglob("*"):
        relative = path.relative_to(source)
        if not should_copy(relative):
            continue
        destination = target / relative
        if path.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
        elif path.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, destination)


def build_release(root: Path, output_dir: Path) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    package_name = f"Mind-Agent-v{__version__}"
    with tempfile.TemporaryDirectory(prefix="mind-release-") as temp_dir:
        stage = Path(temp_dir) / package_name
        stage.mkdir()
        for name in sorted(ROOT_FILES):
            source = root / name
            if source.exists():
                shutil.copy2(source, stage / name)
        for name in sorted(SOURCE_DIRS):
            source = root / name
            if source.exists():
                copy_tree(source, stage / name)
        eval_target = stage / "evals"
        eval_target.mkdir()
        for name in sorted(EVAL_FILES):
            source = root / "evals" / name
            if source.exists():
                shutil.copy2(source, eval_target / name)
        archive = output_dir / f"{package_name}.zip"
        archive.unlink(missing_ok=True)
        with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as zipped:
            for path in sorted(stage.rglob("*")):
                if path.is_file():
                    zipped.write(path, path.relative_to(stage.parent))
        return archive


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a clean Mind1.1 source release.")
    parser.add_argument("--output-dir", default="dist")
    args = parser.parse_args()
    root = ROOT
    output = Path(args.output_dir).expanduser()
    if not output.is_absolute():
        output = root / output
    archive = build_release(root, output.resolve())
    print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
