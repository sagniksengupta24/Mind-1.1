from __future__ import annotations

import json
from typing import Any, Dict

from .verify_tools import ToolResult, require_arg


def refresh_knowledge(registry: Any, args: Dict[str, Any]) -> ToolResult:
    counts = registry.knowledge.refresh(str(args.get("path", ".")))
    stats = registry.knowledge.stats()
    return ToolResult(f"Refreshed project knowledge: {json.dumps({**counts, **stats}, sort_keys=True)}")


def query_knowledge(registry: Any, args: Dict[str, Any]) -> ToolResult:
    query = require_arg(args, "query")
    hits = registry.knowledge.query(query, int(args.get("limit", 20)))
    if not hits:
        return ToolResult("(no project knowledge matches)")
    lines: list[str] = []
    for hit in hits:
        metadata = json.dumps(hit.metadata, sort_keys=True, ensure_ascii=False)
        lines.append(
            f"{hit.entity_id} {hit.entity_type} {hit.name} path={hit.path or '-'} "
            f"provenance={hit.provenance or '-'} metadata={metadata}"
        )
    return ToolResult("\n".join(lines))
