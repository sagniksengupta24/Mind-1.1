from __future__ import annotations

from typing import Any, Dict

from ..llm import EmbeddingError, OllamaEmbeddingClient
from ..security import redact_secrets
from .verify_tools import ToolError, ToolResult, require_arg


def search_docs(registry: Any, args: Dict[str, Any]) -> ToolResult:
    query = require_arg(args, "query")
    limit = int(args.get("limit", 6))
    embed = str(args.get("embed", "")).lower() in {"1", "true", "yes"}
    embedding_model = str(args.get("embedding_model", "nomic-embed-text"))
    embedder = None
    if embed:
        embedder = OllamaEmbeddingClient(
            str(args.get("ollama_url", "http://127.0.0.1:11434")),
            embedding_model,
        )
    try:
        hits = registry.docs.search(
            query,
            limit=limit,
            embedder=embedder,
            embedding_model=embedding_model if embed else "",
        )
    except EmbeddingError as exc:
        raise ToolError(str(exc)) from exc
    if not hits:
        return ToolResult("(no docs found; run `index-docs` first)")
    return ToolResult(
        "\n\n".join(
            f"{hit.citation} score={hit.score}{render_vector_score(hit.vector_score)}"
            f"{render_stale(hit.stale)}\n"
            f"{redact_secrets(hit.chunk[:1200])}"
            for hit in hits
        )
    )


def render_vector_score(score: float) -> str:
    if score == 0.0:
        return ""
    return f" vector={score:.3f}"


def render_stale(stale: bool) -> str:
    return " stale=true" if stale else ""
