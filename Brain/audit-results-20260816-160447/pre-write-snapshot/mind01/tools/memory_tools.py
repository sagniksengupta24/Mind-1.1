from __future__ import annotations

from typing import Any, Dict

from .verify_tools import ToolError, ToolResult, require_arg


def remember(registry: Any, args: Dict[str, Any]) -> ToolResult:
    key = require_arg(args, "key")
    value = require_arg(args, "value")
    tags = str(args.get("tags", ""))
    source = str(args.get("source", "agent"))
    importance = int(args.get("importance", 1))
    try:
        return ToolResult(registry.memory.remember(key, value, tags, source, importance))
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


def recall(registry: Any, args: Dict[str, Any]) -> ToolResult:
    query = require_arg(args, "query")
    limit = int(args.get("limit", 8))
    tags = str(args.get("tags", ""))
    hits = registry.memory.recall(query, limit=limit, tags=tags)
    if not hits:
        return ToolResult("(no memories)")
    return ToolResult(render_memories(hits))


def list_memories(registry: Any, args: Dict[str, Any]) -> ToolResult:
    limit = int(args.get("limit", 50))
    tags = str(args.get("tags", ""))
    hits = registry.memory.list(limit=limit, tags=tags)
    if not hits:
        return ToolResult("(no memories)")
    return ToolResult(render_memories(hits))


def update_memory(registry: Any, args: Dict[str, Any]) -> ToolResult:
    memory_id = int(require_arg(args, "id"))
    value = require_arg(args, "value")
    tags = args.get("tags")
    source = args.get("source")
    importance = args.get("importance")
    try:
        return ToolResult(
            registry.memory.update(
                memory_id,
                value,
                str(tags) if tags is not None else None,
                str(source) if source is not None else None,
                int(importance) if importance is not None else None,
            )
        )
    except ValueError as exc:
        raise ToolError(str(exc)) from exc


def render_memories(hits: list[Any]) -> str:
    return "\n\n".join(
        (
            f"{hit.id}: {hit.key} [{hit.tags}] source={hit.source} "
            f"importance={hit.importance} use_count={hit.use_count} "
            f"created_at={hit.created_at} updated_at={hit.updated_at} "
            f"score={hit.score:.1f}\n{hit.value}"
        )
        for hit in hits
    )


def delete_memory(registry: Any, args: Dict[str, Any]) -> ToolResult:
    memory_id = int(require_arg(args, "id"))
    try:
        return ToolResult(registry.memory.delete(memory_id))
    except ValueError as exc:
        raise ToolError(str(exc)) from exc
