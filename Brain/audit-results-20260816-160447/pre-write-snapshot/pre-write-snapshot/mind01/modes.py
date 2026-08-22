from __future__ import annotations

from enum import Enum


class AgentMode(str, Enum):
    READ_ONLY = "read-only"
    PROPOSE = "propose"
    WRITE_APPROVED = "write-approved"
    UNSAFE = "unsafe"


def parse_agent_mode(value: str | AgentMode | None) -> AgentMode:
    if value is None:
        return AgentMode.READ_ONLY
    if isinstance(value, AgentMode):
        return value
    try:
        return AgentMode(value)
    except ValueError as exc:
        allowed = ", ".join(mode.value for mode in AgentMode)
        raise ValueError(f"Invalid mode `{value}`. Allowed modes: {allowed}.") from exc


def mode_choices() -> list[str]:
    return [mode.value for mode in AgentMode]
