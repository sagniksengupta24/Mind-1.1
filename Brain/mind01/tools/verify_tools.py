from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict


class ToolError(RuntimeError):
    pass


@dataclass
class ToolResult:
    text: str


def require_arg(args: Dict[str, Any], name: str) -> str:
    value = args.get(name)
    if value is None or str(value) == "":
        raise ToolError(f"Missing required arg: {name}")
    return str(value)


def approve(registry: Any, prompt: str) -> bool:
    if registry.yes:
        return True
    try:
        answer = input(f"{prompt} [y/N] ").strip().lower()
    except EOFError as exc:
        raise ToolError("User approval required, but no interactive input is available.") from exc
    if answer not in {"y", "yes"}:
        raise ToolError("User denied action.")
    return True


def require_write_permission(registry: Any) -> None:
    if not registry.allow_write:
        raise ToolError(
            "Source file writes are disabled. Re-run with `--allow-write` "
            "to enable write_file/edit_file."
        )
