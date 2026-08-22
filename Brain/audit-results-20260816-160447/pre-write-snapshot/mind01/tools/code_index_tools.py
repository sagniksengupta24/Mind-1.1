from __future__ import annotations

from typing import Any, Dict

from ..code_index import render_file_summary, render_symbol_hits
from .verify_tools import ToolError, ToolResult, require_arg


def index_code(registry: Any, args: Dict[str, Any]) -> ToolResult:
    root = registry.resolve_path(str(args.get("path", ".")))
    try:
        count = registry.code_index.index_path(root)
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
    files, symbols = registry.code_index.stats()
    return ToolResult(f"Indexed {count} files. Current index: {files} files, {symbols} symbols.")


def search_symbols(registry: Any, args: Dict[str, Any]) -> ToolResult:
    query = require_arg(args, "query")
    limit = int(args.get("limit", 20))
    return ToolResult(render_symbol_hits(registry.code_index.search_symbols(query, limit=limit)))


def file_summary(registry: Any, args: Dict[str, Any]) -> ToolResult:
    path = require_arg(args, "path")
    try:
        return ToolResult(render_file_summary(registry.code_index.file_summary(path)))
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
