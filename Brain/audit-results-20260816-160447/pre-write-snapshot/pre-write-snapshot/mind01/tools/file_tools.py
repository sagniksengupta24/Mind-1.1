from __future__ import annotations

from typing import Any, Dict, Iterable

from ..file_safety import (
    FileSafetyError,
    ensure_text_file_safe,
    ensure_write_target_safe,
    read_text_file_safe,
    relative_path,
)
from ..receipts import ReceiptContext, ReceiptError, perform_verified_content_mutation
from ..security import redact_secrets
from .verify_tools import ToolError, ToolResult, approve, require_arg, require_write_permission


TEXT_SUFFIXES = {
    ".py",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".json",
    ".md",
    ".txt",
    ".v",
    ".sv",
    ".svh",
    ".vh",
    ".c",
    ".cpp",
    ".h",
    ".hpp",
}

SKIP_DIRS = {".mind01", "evals", "node_modules", "__pycache__", ".git"}


def list_files(registry: Any, args: Dict[str, Any]) -> ToolResult:
    root = registry.resolve_path(str(args.get("path", ".")))
    if not root.exists():
        raise ToolError(f"Path does not exist: {root}")
    files = []
    for item in sorted(root.rglob("*") if root.is_dir() else [root]):
        if SKIP_DIRS & set(item.parts):
            continue
        if item.is_file():
            files.append(str(item.relative_to(registry.workspace)))
        if len(files) >= 300:
            files.append("... truncated ...")
            break
    return ToolResult("\n".join(files) or "(no files)")


def read_file(registry: Any, args: Dict[str, Any]) -> ToolResult:
    raw_path = require_arg(args, "path")
    try:
        path, text = read_text_file_safe(registry.workspace, raw_path)
    except FileSafetyError as exc:
        raise ToolError(str(exc)) from exc
    return ToolResult(redact_secrets(text[:20000]))


def search_code(registry: Any, args: Dict[str, Any]) -> ToolResult:
    query = require_arg(args, "query")
    root = registry.resolve_path(str(args.get("path", ".")))
    if root.is_file():
        try:
            ensure_text_file_safe(registry.workspace, root)
        except FileSafetyError as exc:
            raise ToolError(str(exc)) from exc
    hits = []
    for file_path in iter_text_files(root):
        try:
            ensure_text_file_safe(registry.workspace, file_path)
            rel = relative_path(registry.workspace, file_path)
            for idx, line in enumerate(
                file_path.read_text(encoding="utf-8").splitlines(),
                start=1,
            ):
                if query.lower() in line.lower():
                    hits.append(f"{rel}:{idx}: {redact_secrets(line[:240])}")
                    if len(hits) >= 100:
                        return ToolResult("\n".join(hits))
        except (OSError, FileSafetyError):
            continue
    return ToolResult("\n".join(hits) or "(no matches)")


def write_file(registry: Any, args: Dict[str, Any]) -> ToolResult:
    raw_path = require_arg(args, "path")
    try:
        path = ensure_write_target_safe(registry.workspace, raw_path)
    except FileSafetyError as exc:
        raise ToolError(str(exc)) from exc
    content = require_arg(args, "content")
    require_write_permission(registry)
    approved = approve(registry, f"Write file {path.relative_to(registry.workspace)}?")

    try:
        receipt = perform_verified_content_mutation(
            registry.workspace,
            raw_path,
            ReceiptContext(
                operation_type="write_file",
                mode=registry.mode.value,
                allow_write=registry.allow_write,
                approved=approved,
                source="write_file",
            ),
            content,
        )
    except ReceiptError as exc:
        raise ToolError(str(exc)) from exc
    return ToolResult(
        f"Wrote {path.relative_to(registry.workspace)} "
        f"(receipt {receipt['receipt_id']})"
    )


def edit_file(registry: Any, args: Dict[str, Any]) -> ToolResult:
    raw_path = require_arg(args, "path")
    try:
        path = ensure_write_target_safe(registry.workspace, raw_path)
        ensure_text_file_safe(registry.workspace, path, raw_path)
    except FileSafetyError as exc:
        raise ToolError(str(exc)) from exc
    old = require_arg(args, "old")
    new = require_arg(args, "new")
    text = path.read_text(encoding="utf-8")
    if old not in text:
        raise ToolError("Exact `old` text was not found.")
    require_write_permission(registry)
    approved = approve(registry, f"Edit file {path.relative_to(registry.workspace)}?")

    updated_text = text.replace(old, new, 1)

    try:
        receipt = perform_verified_content_mutation(
            registry.workspace,
            raw_path,
            ReceiptContext(
                operation_type="edit_file",
                mode=registry.mode.value,
                allow_write=registry.allow_write,
                approved=approved,
                source="edit_file",
            ),
            updated_text,
        )
    except ReceiptError as exc:
        raise ToolError(str(exc)) from exc
    return ToolResult(
        f"Edited {path.relative_to(registry.workspace)} "
        f"(receipt {receipt['receipt_id']})"
    )


def iter_text_files(root: Path) -> Iterable[Path]:
    items = root.rglob("*") if root.is_dir() else [root]
    for item in items:
        if SKIP_DIRS & set(item.parts):
            continue
        if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES:
            yield item
