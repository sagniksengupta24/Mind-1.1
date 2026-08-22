"""Model-agnostic LLM provider adapter layer.

`mind01.llm.OllamaClient` talks to a locally-running Ollama server.
This module adds a second, duck-type-compatible client for any
OpenAI-compatible cloud endpoint (OpenRouter, Together, Groq,
Fireworks, a self-hosted vLLM/TGI server, ...), so the agent can run
30B-70B+ open-weight models (DeepSeek, Qwen, Llama, ...) via a
provider's GPUs instead of downloading and running them locally.

Every client this module hands out — Ollama or cloud — exposes the
same surface that `Agent` and `OllamaSemanticClassifier` already rely
on:

    chat(messages, json_mode=True, response_schema=None) -> str
    .timeout                 (settable int, seconds)
    .last_output_mode        (str, set after each chat() call)
    .last_server_version     (str, informational)
    .last_response_metadata  (dict | None)

`build_llm_client(config)` is the single seam the rest of the agent
needs to know about: it reads `AgentConfig.provider` (itself resolved
from CLI flags / env vars in `config.py`) and returns the right
client. No other module needs to branch on provider.

Switching models or providers is therefore always a config/env-var
change, never an agent-logic change.
"""

from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from dataclasses import dataclass, field
from typing import Any, Callable, Iterator

from .llm import LLMError, Message, OllamaClient

__all__ = [
    "OpenAICompatibleClient",
    "build_llm_client",
    "DEFAULT_OPENROUTER_BASE_URL",
    "DEFAULT_FREE_OPENROUTER_MODELS",
]


DEFAULT_OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# A short, curated chain of capable OpenRouter models that have historically
# had a free ":free" variant. Used only when the caller hasn't configured a
# model/fallback chain of their own (LLM_MODEL / LLM_FALLBACK_MODELS) — model
# availability on OpenRouter's free tier changes over time, so treat this as
# a reasonable starting point, not a guarantee.
DEFAULT_FREE_OPENROUTER_MODELS: tuple[str, ...] = (
    "deepseek/deepseek-chat-v3.1:free",
    "qwen/qwen3-235b-a22b:free",
    "meta-llama/llama-3.3-70b-instruct:free",
)

_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


@dataclass
class OpenAICompatibleClient:
    """Chat client for any OpenAI-compatible ``/chat/completions`` endpoint.

    Works unmodified with OpenRouter and with any other OpenAI-compatible
    provider by pointing ``base_url``/``api_key`` at it. Inference always
    runs on the provider's infrastructure; nothing is downloaded locally.
    """

    base_url: str
    model: str
    api_key: str = ""
    timeout: int = 120
    temperature: float = 0.2
    top_p: float = 0.9
    fallback_models: tuple[str, ...] = ()
    site_url: str = ""
    app_name: str = "mind01"
    max_retries: int = 2
    retry_backoff_seconds: float = 1.5

    # duck-typed surface expected by Agent / OllamaSemanticClassifier
    last_output_mode: str = "json"
    last_server_version: str = ""
    last_response_metadata: dict[str, Any] | None = None
    last_model_used: str = ""

    # tri-state: None = untested, True/False = learned from a live call
    _json_schema_capability: bool | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        self.base_url = self.base_url.rstrip("/")
        self.last_server_version = self.model

    # ------------------------------------------------------------------
    # duck-typed surface (matches OllamaClient)
    # ------------------------------------------------------------------

    def model_metadata(self) -> dict[str, Any]:
        return {
            "model": self.model,
            "provider_base_url": self.base_url,
            "model_digest": "",
            "json_schema_supported": bool(self._json_schema_capability),
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
                "timeout_seconds": self.timeout,
            },
        }

    def supports_json_schema(self, *, refresh: bool = False) -> bool:
        if refresh:
            self._json_schema_capability = None
        # Conservative default: unknown until a live call proves it, so we
        # never burn a request assuming strict structured-output support
        # most OpenRouter models don't have.
        return bool(self._json_schema_capability)

    def chat(
        self,
        messages: list[Message],
        json_mode: bool = True,
        *,
        response_schema: dict[str, Any] | None = None,
    ) -> str:
        """Non-streaming chat call. Tries `model`, then each entry in
        `fallback_models` in order, on retryable failures."""
        models_to_try = [self.model, *self.fallback_models]
        last_error: LLMError | None = None
        for candidate in models_to_try:
            try:
                return self._chat_one_model(candidate, messages, json_mode, response_schema)
            except LLMError as exc:
                last_error = exc
                if exc.status_code in {401, 403}:
                    raise  # auth problems won't improve on another model
                continue
        assert last_error is not None
        raise last_error

    def chat_stream(
        self,
        messages: list[Message],
        *,
        json_mode: bool = True,
        response_schema: dict[str, Any] | None = None,
        on_token: Callable[[str], None] | None = None,
    ) -> Iterator[str]:
        """Yield content deltas as they stream in over SSE."""
        payload = self._build_payload(self.model, messages, json_mode, response_schema)
        payload["stream"] = True
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers=self._headers(),
            method="POST",
        )
        try:
            response = urllib.request.urlopen(request, timeout=self.timeout)
        except urllib.error.HTTPError as exc:
            raise self._http_error(exc, self.model) from exc
        except urllib.error.URLError as exc:
            raise LLMError(f"Could not reach {self.base_url}: {exc.reason}") from exc

        with response:
            for raw_line in response:
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line or not line.startswith("data:"):
                    continue
                data = line[len("data:"):].strip()
                if data == "[DONE]":
                    break
                try:
                    chunk = json.loads(data)
                except json.JSONDecodeError:
                    continue
                choices = chunk.get("choices") or []
                if not choices:
                    continue
                delta = choices[0].get("delta", {}).get("content")
                if delta:
                    if on_token:
                        on_token(delta)
                    yield delta

    def chat_with_tools(
        self,
        messages: list[Message],
        tools: list[dict[str, Any]],
        *,
        tool_choice: str | dict[str, Any] = "auto",
    ) -> dict[str, Any]:
        """Native OpenAI-style function/tool calling. Returns the raw
        assistant `message` dict (may contain `tool_calls`) so callers
        decide how to interpret it — this layer stays agent-agnostic."""
        payload: dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "tools": tools,
            "tool_choice": tool_choice,
            "temperature": self.temperature,
            "stream": False,
        }
        body = self._post("/chat/completions", payload)
        try:
            return body["choices"][0]["message"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected tool-call response: {str(body)[:500]}") from exc

    # ------------------------------------------------------------------
    # internals
    # ------------------------------------------------------------------

    def _build_payload(
        self,
        model: str,
        messages: list[Message],
        json_mode: bool,
        response_schema: dict[str, Any] | None,
    ) -> dict[str, Any]:
        payload: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": self.temperature,
            "top_p": self.top_p,
            "stream": False,
        }
        if response_schema and self.supports_json_schema():
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {"name": "agent_action", "schema": response_schema, "strict": True},
            }
            self.last_output_mode = "json_schema"
        elif json_mode:
            payload["response_format"] = {"type": "json_object"}
            self.last_output_mode = "json"
        else:
            self.last_output_mode = "text"
        return payload

    def _chat_one_model(
        self,
        model: str,
        messages: list[Message],
        json_mode: bool,
        response_schema: dict[str, Any] | None,
    ) -> str:
        payload = self._build_payload(model, messages, json_mode, response_schema)
        schema_mode = "json_schema" in json.dumps(payload.get("response_format", {}))
        try:
            body = self._post("/chat/completions", payload)
            if response_schema and schema_mode:
                self._json_schema_capability = True
        except LLMError as exc:
            retry_as_json_object = (
                response_schema
                and schema_mode
                and self._json_schema_capability is not False
                and exc.status_code in {400, 422}
            )
            if not retry_as_json_object:
                raise
            # This deployment/model rejects structured `json_schema` output;
            # learn that and fall back to plain JSON mode, never unconstrained
            # prose, mirroring OllamaClient's own fallback behavior.
            self._json_schema_capability = False
            payload["response_format"] = {"type": "json_object"} if json_mode else None
            if payload["response_format"] is None:
                payload.pop("response_format", None)
            self.last_output_mode = "json_fallback" if json_mode else "text"
            body = self._post("/chat/completions", payload)

        self.last_model_used = model
        try:
            choice = body["choices"][0]
            content = choice["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise LLMError(f"Unexpected response from `{model}`: {str(body)[:500]}") from exc
        if content is None:
            raise LLMError(f"Empty completion content from `{model}`: {str(body)[:500]}")
        usage = body.get("usage") if isinstance(body, dict) else None
        if isinstance(usage, dict):
            self.last_response_metadata = dict(usage)
        return content

    def _headers(self) -> dict[str, str]:
        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        if "openrouter.ai" in self.base_url:
            # Optional but recommended by OpenRouter for attribution/rankings.
            if self.site_url:
                headers["HTTP-Referer"] = self.site_url
            if self.app_name:
                headers["X-Title"] = self.app_name
        return headers

    def _post(self, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        data = json.dumps(payload).encode("utf-8")
        delay = self.retry_backoff_seconds
        last_exc: LLMError | None = None
        for attempt in range(self.max_retries + 1):
            request = urllib.request.Request(
                f"{self.base_url}{path}",
                data=data,
                headers=self._headers(),
                method="POST",
            )
            try:
                with urllib.request.urlopen(request, timeout=self.timeout) as response:
                    raw = response.read().decode("utf-8")
                try:
                    return json.loads(raw)
                except json.JSONDecodeError as exc:
                    raise LLMError(f"Unexpected response body: {raw[:500]}") from exc
            except urllib.error.HTTPError as exc:
                error = self._http_error(exc, payload.get("model", self.model))
                last_exc = error
                if error.status_code in _RETRYABLE_STATUS_CODES and attempt < self.max_retries:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise error from exc
            except urllib.error.URLError as exc:
                last_exc = LLMError(f"Could not reach {self.base_url}: {exc.reason}")
                if attempt < self.max_retries:
                    time.sleep(delay)
                    delay *= 2
                    continue
                raise last_exc from exc
        assert last_exc is not None
        raise last_exc

    def _http_error(self, exc: urllib.error.HTTPError, model: str) -> LLMError:
        detail = _extract_error_detail(exc)
        if exc.code == 401:
            return LLMError("Authentication failed: check your API key.", status_code=401)
        if exc.code == 402:
            return LLMError(f"Provider requires payment/credits for `{model}`.", status_code=402)
        if exc.code == 404:
            return LLMError(f"Model `{model}` not found at {self.base_url}.", status_code=404)
        if exc.code == 429:
            suffix = f" {detail}" if detail else ""
            return LLMError(f"Rate limited by provider for `{model}`.{suffix}", status_code=429)
        suffix = f": {detail}" if detail else "."
        return LLMError(f"{self.base_url} HTTP {exc.code} rejected the request{suffix}", status_code=exc.code)


def _extract_error_detail(exc: urllib.error.HTTPError) -> str:
    try:
        raw = exc.read().decode("utf-8", errors="replace")[:1000]
    except (OSError, ValueError):
        return ""
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        return " ".join(raw.split())[:300]
    if isinstance(body, dict):
        err = body.get("error")
        if isinstance(err, dict) and isinstance(err.get("message"), str):
            return " ".join(err["message"].split())[:300]
        if isinstance(err, str):
            return " ".join(err.split())[:300]
    return ""


def build_llm_client(config: Any) -> Any:
    """Factory: turn an `AgentConfig` into a concrete, duck-typed LLM client.

    This is the *only* place that branches on provider. `Agent`,
    `OllamaSemanticClassifier`, and everything downstream just call
    `.chat(...)` on whatever comes back — switching providers/models is
    purely a config/env-var change (`AgentConfig.provider`, `.model`,
    `.api_key`, `.base_url`, `.fallback_models`), never an agent-logic one.
    """
    provider = (getattr(config, "provider", "ollama") or "ollama").strip().lower()

    if provider == "ollama":
        return OllamaClient(config.ollama_url, config.model, timeout=config.request_timeout_seconds)

    if provider in {"openrouter", "openai_compatible", "openai"}:
        base_url = config.base_url or (DEFAULT_OPENROUTER_BASE_URL if provider == "openrouter" else "")
        if not base_url:
            raise ValueError(
                f"base_url is required for provider `{provider}` "
                "(set --base-url or LLM_BASE_URL)."
            )
        if provider == "openrouter" and not config.api_key:
            raise ValueError(
                "OpenRouter requires an API key (set --api-key or OPENROUTER_API_KEY)."
            )
        return OpenAICompatibleClient(
            base_url=base_url,
            model=config.model,
            api_key=config.api_key,
            timeout=config.request_timeout_seconds,
            fallback_models=tuple(config.fallback_models),
            site_url=config.site_url,
            app_name=config.app_name,
        )

    raise ValueError(
        f"Unknown LLM provider `{provider}`. Use one of: ollama, openrouter, openai_compatible."
    )
