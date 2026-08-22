from __future__ import annotations

from typing import Any, Dict

from ..project_map import build_project_map
from .verify_tools import ToolResult


def project_map(registry: Any, args: Dict[str, Any]) -> ToolResult:
    path = str(args.get("path", "."))
    project = build_project_map(registry.workspace, path=path)
    return ToolResult(project.render())
