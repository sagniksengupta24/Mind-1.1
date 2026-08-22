from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import urlparse

from .modes import AgentMode, parse_agent_mode


_MODE_RANK = {
    AgentMode.READ_ONLY: 0,
    AgentMode.PROPOSE: 1,
    AgentMode.WRITE_APPROVED: 2,
    AgentMode.UNSAFE: 3,
}


class PolicyViolation(ValueError):
    pass


@dataclass(frozen=True)
class ServerPolicy:
    maximum_mode: AgentMode = AgentMode.READ_ONLY
    allow_write: bool = False
    allow_shell: bool = False
    auto_approve: bool = False
    max_steps: int = 12
    max_body_bytes: int = 1_000_000
    max_concurrent_requests: int = 4
    request_timeout_seconds: int = 180
    require_auth_for_mutations: bool = True
    allowed_ollama_hosts: tuple[str, ...] = ("127.0.0.1", "localhost", "::1")
    allowed_ollama_ports: tuple[int, ...] = (11434,)

    def resolve_mode(self, requested: str | AgentMode | None) -> AgentMode:
        mode = parse_agent_mode(requested or AgentMode.READ_ONLY)
        if _MODE_RANK[mode] > _MODE_RANK[self.maximum_mode]:
            raise PolicyViolation(
                f"Requested mode `{mode.value}` exceeds server maximum `{self.maximum_mode.value}`."
            )
        return mode

    def resolve_steps(self, requested: object, default: int = 8) -> int:
        try:
            value = int(requested if requested is not None else default)
        except (TypeError, ValueError) as exc:
            raise PolicyViolation("max_steps must be an integer.") from exc
        if value < 1:
            raise PolicyViolation("max_steps must be at least 1.")
        if value > self.max_steps:
            raise PolicyViolation(f"max_steps exceeds server limit of {self.max_steps}.")
        return value

    def validate_ollama_url(self, url: str) -> str:
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"}:
            raise PolicyViolation("Ollama URL must use http or https.")
        if parsed.username or parsed.password or parsed.query or parsed.fragment:
            raise PolicyViolation("Ollama URL contains unsupported components.")
        host = parsed.hostname or ""
        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        if host not in self.allowed_ollama_hosts or port not in self.allowed_ollama_ports:
            raise PolicyViolation("Ollama endpoint is not allowed by server policy.")
        return url.rstrip("/")

    def capabilities_for(self, mode: AgentMode) -> tuple[bool, bool, bool]:
        write = self.allow_write and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}
        shell = self.allow_shell and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}
        approve = self.auto_approve and write
        return write, shell, approve
