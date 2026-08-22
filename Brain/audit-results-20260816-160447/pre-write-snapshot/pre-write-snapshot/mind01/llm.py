from __future__ import annotations

import json
import re
import urllib.error
import urllib.request
from dataclasses import dataclass
from typing import Any, Dict, List


Message = Dict[str, str]


class LLMError(RuntimeError):
    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


class EmbeddingError(RuntimeError):
    pass


@dataclass
class OllamaClient:
    base_url: str
    model: str
    timeout: int = 120
    _json_schema_capability: bool | None = None
    last_output_mode: str = "json"
    last_server_version: str = ""
    last_response_metadata: dict[str, Any] | None = None
    temperature: float = 0.2
    top_p: float = 0.9
    seed: int | None = None
    num_ctx: int | None = None

    def model_metadata(self) -> dict[str, Any]:
        metadata: dict[str, Any] = {
            "model": self.model,
            "ollama_version": self.last_server_version,
            "model_digest": "",
            "json_schema_supported": self.supports_json_schema(),
        }
        request = urllib.request.Request(
            f"{self.base_url}/api/show",
            data=json.dumps({"model": self.model}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=min(self.timeout, 10)) as response:
                body = json.loads(response.read().decode("utf-8"))
            if isinstance(body, dict):
                details = body.get("details") if isinstance(body.get("details"), dict) else {}
                metadata["model_digest"] = str(body.get("digest") or details.get("digest") or "")
        except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError):
            pass
        tags_request = urllib.request.Request(f"{self.base_url}/api/tags", method="GET")
        try:
            with urllib.request.urlopen(tags_request, timeout=min(self.timeout, 10)) as response:
                tags = json.loads(response.read().decode("utf-8"))
            for item in tags.get("models", []) if isinstance(tags, dict) else []:
                if isinstance(item, dict) and str(item.get("name")) == self.model:
                    metadata["model_digest"] = str(item.get("digest") or metadata["model_digest"])
                    metadata["details"] = dict(item.get("details", {})) if isinstance(item.get("details"), dict) else {}
                    break
        except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError):
            pass
        metadata["options"] = {
            "temperature": self.temperature,
            "top_p": self.top_p,
            "seed": self.seed,
            "num_ctx": self.num_ctx,
            "timeout_seconds": self.timeout,
        }
        metadata["ollama_version"] = self.last_server_version
        return metadata

    def supports_json_schema(self, *, refresh: bool = False) -> bool:
        if self._json_schema_capability is not None and not refresh:
            return self._json_schema_capability
        request = urllib.request.Request(f"{self.base_url}/api/version", method="GET")
        try:
            with urllib.request.urlopen(request, timeout=min(self.timeout, 5)) as response:
                body = json.loads(response.read().decode("utf-8"))
            version = str(body.get("version", "")) if isinstance(body, dict) else ""
            self.last_server_version = version
            match = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
            # Ollama supports JSON Schema format objects in current 0.5+ releases.
            self._json_schema_capability = bool(match and tuple(map(int, match.groups())) >= (0, 5, 0))
        except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError):
            self._json_schema_capability = False
        return self._json_schema_capability

    def chat(
        self,
        messages: List[Message],
        json_mode: bool = True,
        *,
        response_schema: dict[str, Any] | None = None,
    ) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }
        if self.seed is not None:
            payload["options"]["seed"] = self.seed
        if self.num_ctx is not None:
            payload["options"]["num_ctx"] = self.num_ctx
        schema_mode = bool(response_schema and self.supports_json_schema())
        if schema_mode:
            payload["format"] = response_schema
            self.last_output_mode = "json_schema"
        elif json_mode:
            payload["format"] = "json"
            self.last_output_mode = "json"
        else:
            self.last_output_mode = "text"
        try:
            return self._chat_payload(payload)
        except LLMError as exc:
            # Older Ollama servers can report a version but reject schema objects.
            # Retry once using JSON mode, never unconstrained prose.
            if not schema_mode or exc.status_code not in {400, 422}:
                raise
            self._json_schema_capability = False
            payload["format"] = "json"
            self.last_output_mode = "json_fallback"
            return self._chat_payload(payload)

    def _chat_payload(self, payload: dict[str, Any]) -> str:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}/api/chat",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.HTTPError as exc:
            detail = _http_error_detail(exc)
            if exc.code == 404 and "model" in detail.lower() and "not found" in detail.lower():
                raise LLMError(
                    f"Ollama model `{self.model}` is not installed. Run "
                    f"`ollama pull {self.model}` first.",
                    status_code=exc.code,
                ) from exc
            suffix = f": {detail}" if detail else "."
            raise LLMError(
                f"Ollama HTTP {exc.code} rejected the request{suffix}",
                status_code=exc.code,
            ) from exc
        except urllib.error.URLError as exc:
            raise LLMError(
                "Could not reach Ollama. Start it with `ollama serve` and pull "
                f"`{self.model}` first."
            ) from exc

        try:
            body = json.loads(raw)
            if isinstance(body, dict):
                self.last_response_metadata = {
                    key: body.get(key)
                    for key in ("prompt_eval_count", "eval_count", "total_duration", "load_duration", "eval_duration")
                    if key in body
                }
            return body["message"]["content"]
        except (KeyError, json.JSONDecodeError) as exc:
            raise LLMError(f"Unexpected Ollama response: {raw[:500]}") from exc


def _http_error_detail(exc: urllib.error.HTTPError) -> str:
    """Extract Ollama's bounded JSON error without obscuring the HTTP cause."""
    try:
        raw = exc.read().decode("utf-8", errors="replace")[:1000]
    except (OSError, ValueError):
        return ""
    try:
        body = json.loads(raw)
    except json.JSONDecodeError:
        return " ".join(raw.split())[:300]
    if isinstance(body, dict) and isinstance(body.get("error"), str):
        return " ".join(body["error"].split())[:300]
    return ""


@dataclass
class OllamaEmbeddingClient:
    base_url: str
    model: str = "nomic-embed-text"
    timeout: int = 120

    def embed(self, text: str) -> list[float]:
        trimmed = text.strip()
        if not trimmed:
            return []
        first_error = None
        try:
            return self._embed_new(trimmed)
        except EmbeddingError as exc:
            first_error = exc
        try:
            return self._embed_legacy(trimmed)
        except EmbeddingError as exc:
            raise EmbeddingError(
                f"Could not get embeddings from Ollama model `{self.model}`. "
                "Start Ollama and pull the embedding model first."
            ) from first_error or exc

    def _embed_new(self, text: str) -> list[float]:
        body = self._post("/api/embed", {"model": self.model, "input": text})
        embeddings = body.get("embeddings")
        if (
            isinstance(embeddings, list)
            and embeddings
            and isinstance(embeddings[0], list)
        ):
            return coerce_vector(embeddings[0])
        raise EmbeddingError(f"Unexpected Ollama /api/embed response: {str(body)[:500]}")

    def _embed_legacy(self, text: str) -> list[float]:
        body = self._post("/api/embeddings", {"model": self.model, "prompt": text})
        embedding = body.get("embedding")
        if isinstance(embedding, list):
            return coerce_vector(embedding)
        raise EmbeddingError(f"Unexpected Ollama /api/embeddings response: {str(body)[:500]}")

    def _post(self, endpoint: str, payload: dict) -> dict:
        data = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            f"{self.base_url}{endpoint}",
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                raw = response.read().decode("utf-8")
        except urllib.error.URLError as exc:
            raise EmbeddingError(
                "Could not reach Ollama embeddings. Start it with `ollama serve` "
                f"and pull `{self.model}` first."
            ) from exc
        try:
            body = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise EmbeddingError(f"Unexpected Ollama embeddings response: {raw[:500]}") from exc
        if not isinstance(body, dict):
            raise EmbeddingError(f"Unexpected Ollama embeddings response: {raw[:500]}")
        return body


def coerce_vector(values: list) -> list[float]:
    vector = []
    for value in values:
        try:
            vector.append(float(value))
        except (TypeError, ValueError) as exc:
            raise EmbeddingError("Embedding vector contained a non-numeric value.") from exc
    return vector
