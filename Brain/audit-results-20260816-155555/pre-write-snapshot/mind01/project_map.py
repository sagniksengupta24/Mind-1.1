from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


SKIP_DIRS = {
    ".git",
    ".mind01",
    ".pycache",
    "__pycache__",
    "node_modules",
    "dist",
    "build",
    ".venv",
    "venv",
}

IMPORTANT_NAMES = {
    "README.md",
    "pyproject.toml",
    "package.json",
    "requirements.txt",
    "Makefile",
    "Dockerfile",
    "tsconfig.json",
}

SKIP_FILES = {
    ".DS_Store",
}


@dataclass
class ProjectMap:
    root: str
    total_files: int
    suffix_counts: Counter[str]
    important_files: list[str]
    sample_files: list[str]

    def render(self) -> str:
        suffix_lines = [
            f"{suffix or '[no extension]'}: {count}"
            for suffix, count in self.suffix_counts.most_common(12)
        ]
        return "\n".join(
            [
                f"root: {self.root}",
                f"total_files: {self.total_files}",
                "",
                "file_types:",
                *(f"- {line}" for line in suffix_lines),
                "",
                "important_files:",
                *(f"- {path}" for path in self.important_files or ["(none found)"]),
                "",
                "sample_files:",
                *(f"- {path}" for path in self.sample_files),
            ]
        )


def build_project_map(workspace: Path, path: str = ".", max_files: int = 250) -> ProjectMap:
    root = (workspace / path).resolve()
    if workspace.resolve() != root and workspace.resolve() not in root.parents:
        raise ValueError(f"Path escapes workspace: {path}")
    files = list(iter_project_files(root, workspace.resolve(), max_files=max_files))
    suffix_counts = Counter(file.suffix.lower() for file in files)
    important = [
        str(file.relative_to(workspace))
        for file in files
        if file.name in IMPORTANT_NAMES
    ]
    samples = [str(file.relative_to(workspace)) for file in files[:max_files]]
    return ProjectMap(
        root=str(root),
        total_files=len(files),
        suffix_counts=suffix_counts,
        important_files=important[:50],
        sample_files=samples[:max_files],
    )


def iter_project_files(root: Path, workspace: Path, max_files: int) -> Iterable[Path]:
    count = 0
    items = root.rglob("*") if root.is_dir() else [root]
    for item in sorted(items):
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        if not item.is_file() or item.name in SKIP_FILES:
            continue
        try:
            item.relative_to(workspace)
        except ValueError:
            continue
        yield item
        count += 1
        if count >= max_files:
            break
