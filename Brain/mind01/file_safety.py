from __future__ import annotations

from pathlib import Path


MAX_TEXT_FILE_BYTES = 1_000_000
TEXT_SAMPLE_BYTES = 4096
RUNTIME_DIR = ".mind01"
SENSITIVE_RUNTIME_SUFFIXES = {".sqlite", ".sqlite3", ".db", ".json"}


class FileSafetyError(RuntimeError):
    pass


def resolve_workspace_path(workspace: Path, raw_path: str) -> Path:
    root = workspace.resolve()
    candidate = (root / raw_path).resolve()
    if root != candidate and root not in candidate.parents:
        raise FileSafetyError(f"Path escapes workspace: {raw_path}")
    return candidate


def resolve_existing_path(workspace: Path, raw_path: str) -> Path:
    path = resolve_workspace_path(workspace, raw_path)
    if not path.exists():
        raise FileSafetyError(f"Path does not exist: {raw_path}")
    return path


def resolve_write_path(workspace: Path, raw_path: str) -> Path:
    root = workspace.resolve()
    target = (root / raw_path).resolve()
    if root != target and root not in target.parents:
        raise FileSafetyError(f"Path escapes workspace: {raw_path}")
    if target.exists():
        return target
    parent = target.parent.resolve()
    if root != parent and root not in parent.parents:
        raise FileSafetyError(f"Path escapes workspace: {raw_path}")
    return target


def relative_path(workspace: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(workspace.resolve()))
    except ValueError as exc:
        raise FileSafetyError("Path escapes workspace.") from exc


def is_runtime_path(workspace: Path, path: Path) -> bool:
    try:
        rel = path.resolve().relative_to(workspace.resolve())
    except ValueError:
        return False
    return bool(rel.parts) and rel.parts[0] == RUNTIME_DIR


def ensure_not_runtime_path(workspace: Path, path: Path, raw_path: str = "") -> None:
    if is_runtime_path(workspace, path):
        display = raw_path or relative_path(workspace, path)
        suffix = path.suffix.lower()
        if suffix in SENSITIVE_RUNTIME_SUFFIXES or path.is_file():
            raise FileSafetyError(f"Runtime file access is blocked: {display}")
        raise FileSafetyError(f"Runtime path access is blocked: {display}")


def ensure_text_file_safe(workspace: Path, path: Path, raw_path: str = "") -> None:
    ensure_not_runtime_path(workspace, path, raw_path)
    if not path.is_file():
        display = raw_path or str(path)
        raise FileSafetyError(f"Not a file: {display}")
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise FileSafetyError("Could not inspect file safely.") from exc
    if size > MAX_TEXT_FILE_BYTES:
        display = raw_path or relative_path(workspace, path)
        raise FileSafetyError(
            f"File is too large to read safely: {display} "
            f"({size} bytes > {MAX_TEXT_FILE_BYTES} bytes)."
        )
    try:
        sample = path.read_bytes()[:TEXT_SAMPLE_BYTES]
    except OSError as exc:
        raise FileSafetyError("Could not read file sample safely.") from exc
    if b"\x00" in sample:
        display = raw_path or relative_path(workspace, path)
        raise FileSafetyError(f"Binary file reads are blocked: {display}")
    try:
        sample.decode("utf-8")
    except UnicodeDecodeError as exc:
        display = raw_path or relative_path(workspace, path)
        raise FileSafetyError(f"Non-UTF-8/binary file reads are blocked: {display}") from exc


def read_text_file_safe(workspace: Path, raw_path: str, max_bytes: int = MAX_TEXT_FILE_BYTES) -> tuple[Path, str]:
    path = resolve_existing_path(workspace, raw_path)
    ensure_text_file_safe(workspace, path, raw_path)
    if path.stat().st_size > max_bytes:
        raise FileSafetyError(f"File is too large to read safely: {raw_path}")
    return path, path.read_text(encoding="utf-8")


def ensure_write_target_safe(workspace: Path, raw_path: str) -> Path:
    path = resolve_write_path(workspace, raw_path)
    ensure_not_runtime_path(workspace, path, raw_path)
    return path
