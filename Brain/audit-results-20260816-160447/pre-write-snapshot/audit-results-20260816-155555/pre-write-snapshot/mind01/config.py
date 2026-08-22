from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from .modes import AgentMode, parse_agent_mode

_KNOWN_PROVIDERS = {"ollama", "openrouter", "openai_compatible", "openai"}


def _env_model_list(name: str) -> tuple[str, ...]:
    raw = os.environ.get(name, "")
    return tuple(item.strip() for item in raw.split(",") if item.strip())


@dataclass(frozen=True)
class AgentConfig:
    workspace: Path
    model: str = "qwen2.5-coder:7b"
    ollama_url: str = "http://127.0.0.1:11434"
    max_steps: int = 8
    yes: bool = False
    dry_run: bool = False
    trace: bool = False
    allow_write: bool = False
    allow_shell: bool = False
    mode: AgentMode = AgentMode.READ_ONLY
    request_timeout_seconds: int = 120
    semantic_router: str = "legacy"
    trace_bundles: bool = False

    # --- cloud LLM provider adapter -----------------------------------
    # Default ("ollama") preserves existing local-first behavior exactly.
    # Set provider to "openrouter" (or "openai_compatible" for any other
    # OpenAI-compatible endpoint) to run inference on a provider's GPUs
    # instead of locally. All of these are resolved from env vars in
    # `build()` when not passed explicitly, so switching providers/models
    # never requires touching agent code — see README / .env.example.
    provider: str = "ollama"
    api_key: str = ""
    base_url: str = ""
    fallback_models: tuple[str, ...] = ()
    site_url: str = ""
    app_name: str = "mind01"

    @classmethod
    def build(
        cls,
        workspace: str,
        model: str,
        ollama_url: str,
        max_steps: int,
        yes: bool,
        dry_run: bool,
        trace: bool = False,
        allow_write: bool = False,
        allow_shell: bool = False,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        request_timeout_seconds: int = 120,
        semantic_router: str = "legacy",
        trace_bundles: bool = False,
        provider: str | None = None,
        api_key: str | None = None,
        base_url: str | None = None,
        fallback_models: tuple[str, ...] | list[str] | None = None,
        site_url: str | None = None,
        app_name: str | None = None,
    ) -> "AgentConfig":
        root = Path(workspace).expanduser().resolve()
        clean_model = model.strip()
        clean_url = ollama_url.strip().rstrip("/")
        if not clean_model:
            raise ValueError("model must not be empty.")
        if not clean_url:
            raise ValueError("ollama_url must not be empty.")
        if not 1 <= int(max_steps) <= 64:
            raise ValueError("max_steps must be between 1 and 64.")
        if not 1 <= int(request_timeout_seconds) <= 3600:
            raise ValueError("request_timeout_seconds must be between 1 and 3600.")
        if semantic_router not in {"legacy", "v2", "compare"}:
            raise ValueError("semantic_router must be legacy, v2, or compare.")
        if not isinstance(trace_bundles, bool):
            raise ValueError("trace_bundles must be a bool.")

        # Any of these left as None (i.e. not explicitly passed by the
        # caller) fall back to environment variables, so a bare
        # `AgentConfig.build(...)` call from a script, notebook, or the
        # HTTP API picks up provider config the same way the CLI does.
        resolved_provider = (
            provider if provider is not None else os.environ.get("LLM_PROVIDER", "ollama")
        ).strip().lower()
        if resolved_provider not in _KNOWN_PROVIDERS:
            raise ValueError(
                "provider must be one of: " + ", ".join(sorted(_KNOWN_PROVIDERS))
            )

        default_key_env = "OPENROUTER_API_KEY" if resolved_provider == "openrouter" else "LLM_API_KEY"
        resolved_api_key = (
            api_key
            if api_key is not None
            else os.environ.get(default_key_env) or os.environ.get("LLM_API_KEY", "")
        )
        resolved_base_url = base_url if base_url is not None else os.environ.get("LLM_BASE_URL", "")
        resolved_fallbacks = (
            tuple(fallback_models)
            if fallback_models is not None
            else _env_model_list("LLM_FALLBACK_MODELS")
        )
        resolved_site_url = site_url if site_url is not None else os.environ.get("LLM_SITE_URL", "")
        resolved_app_name = (
            app_name if app_name is not None else os.environ.get("LLM_APP_NAME", "mind01")
        )

        return cls(
            workspace=root,
            model=clean_model,
            ollama_url=clean_url,
            max_steps=int(max_steps),
            yes=yes,
            dry_run=dry_run,
            trace=trace,
            allow_write=allow_write,
            allow_shell=allow_shell,
            mode=parse_agent_mode(mode),
            request_timeout_seconds=int(request_timeout_seconds),
            semantic_router=semantic_router,
            trace_bundles=trace_bundles,
            provider=resolved_provider,
            api_key=resolved_api_key,
            base_url=resolved_base_url,
            fallback_models=resolved_fallbacks,
            site_url=resolved_site_url,
            app_name=resolved_app_name,
        )
