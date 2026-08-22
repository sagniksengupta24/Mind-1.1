from __future__ import annotations

import json
import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .agent import Agent
from .code_index import CodeIndex, render_file_summary
from .config import AgentConfig
from .file_safety import FileSafetyError, read_text_file_safe
from .llm import EmbeddingError, OllamaEmbeddingClient
from .memory import MemoryStore
from .modes import AgentMode, parse_agent_mode
from .mutations import DirtyStateStore, MutationError
from .patches import PatchError, PatchStore
from .policy import PolicyViolation, ServerPolicy
from .project_knowledge import ProjectKnowledgeStore
from .project_map import build_project_map
from .rag import DocStore
from .receipts import ReceiptError, ReceiptStore
from .security import redact_secrets
from .sessions import SessionStore, message_to_dict, session_to_dict
from .tools import ToolError, ToolRegistry
from .traces import TraceError, TraceStore


def sanitize_backup_relative_path(path_str: str | None) -> str | None:
    if not path_str:
        return None
    if path_str.startswith("/") or path_str.startswith("\\") or ".." in path_str:
        return None
    normalized = path_str.replace("\\", "/")
    if normalized.startswith(".mind01/receipts/backups/"):
        return path_str
    return None


def safe_dirty_record(record: dict) -> dict:
    """Return the public, path-sanitized projection of a dirty-state record."""
    return {
        "dirty_id": record.get("dirty_id"),
        "timestamp": record.get("timestamp"),
        "operation": record.get("operation"),
        "target_relative_path": record.get("target_relative_path"),
        "before_sha256": record.get("before_sha256"),
        "before_size_bytes": record.get("before_size_bytes"),
        "intended_after_sha256": record.get("intended_after_sha256"),
        "intended_after_size_bytes": record.get("intended_after_size_bytes"),
        "current_sha256": record.get("current_sha256"),
        "current_size_bytes": record.get("current_size_bytes"),
        "backup_relative_path": sanitize_backup_relative_path(record.get("backup_path")),
        "error": record.get("error"),
        "recovery_status": record.get("recovery_status"),
        "manual_repair_instructions": record.get("manual_repair_instructions"),
    }


MAX_BODY_BYTES = 1_000_000


class MindAPI:
    def __init__(
        self,
        workspace: Path,
        model: str,
        ollama_url: str,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        api_token: str = "",
        cors_origin: str = "http://localhost:3000",
        *,
        allow_write: bool = False,
        allow_shell: bool = False,
        auto_approve: bool = False,
        max_steps: int = 12,
        max_body_bytes: int = MAX_BODY_BYTES,
        max_concurrent_requests: int = 4,
        request_timeout_seconds: int = 180,
    ) -> None:
        self.workspace = workspace.resolve()
        self.model = model
        parsed_mode = parse_agent_mode(mode)
        self.policy = ServerPolicy(
            maximum_mode=parsed_mode,
            allow_write=bool(allow_write),
            allow_shell=bool(allow_shell),
            auto_approve=bool(auto_approve),
            max_steps=max(1, min(int(max_steps), 64)),
            max_body_bytes=max(1024, min(int(max_body_bytes), 8_000_000)),
            max_concurrent_requests=max(1, min(int(max_concurrent_requests), 32)),
            request_timeout_seconds=max(1, min(int(request_timeout_seconds), 3600)),
        )
        self.ollama_url = self.policy.validate_ollama_url(ollama_url)
        self.mode = parsed_mode
        self.api_token = api_token
        if self.api_token and cors_origin == "*":
            raise ValueError("Wildcard CORS is not allowed when API auth is enabled.")
        if (parsed_mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE} or allow_write or allow_shell) and not api_token:
            raise ValueError("An API token is required when elevated capabilities are enabled.")
        self.cors_origin = cors_origin
        self._request_slots = threading.BoundedSemaphore(self.policy.max_concurrent_requests)

    def handler(self):  # type: ignore[no-untyped-def]
        api = self

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self) -> None:  # noqa: N802
                api.handle_get(self)

            def do_POST(self) -> None:  # noqa: N802
                api.handle_post(self)

            def do_OPTIONS(self) -> None:  # noqa: N802
                api.handle_options(self)

            def log_message(self, format: str, *args) -> None:  # noqa: A002
                return

        return Handler

    def handle_options(self, request: BaseHTTPRequestHandler) -> None:
        write_json(request, {}, cors_origin=self.cors_origin)

    def handle_get(self, request: BaseHTTPRequestHandler) -> None:
        parsed = urlparse(request.path)
        query = parse_qs(parsed.query)
        import uuid

        req_id = uuid.uuid4().hex
        try:
            if not self.authorized(request):
                write_error(request, "unauthorized", "Unauthorized.", status=401, cors_origin=self.cors_origin, request_id=req_id)
                return
            if not self._dispatch_get(request, parsed.path, query):
                write_error(request, "not_found", "Not found.", status=404, cors_origin=self.cors_origin, request_id=req_id)
        except Exception as exc:
            self._write_get_exception(request, req_id, exc)

    def _dispatch_get(self, request: BaseHTTPRequestHandler, path: str, query: dict[str, list[str]]) -> bool:
        handler = self._get_routes().get(path)
        payload = handler(query) if handler else self._get_detail_payload(path, query)
        if payload is None:
            return False
        write_json(request, payload, cors_origin=self.cors_origin)
        return True

    def _get_routes(self):  # type: ignore[no-untyped-def]
        return {
            "/health": self._get_health,
            "/status": self._get_health,
            "/project-map": self._get_project_map,
            "/read-file": self._get_read_file,
            "/search-code": self._get_search_code,
            "/memories": self._get_memories,
            "/memories/search": self._get_memory_search,
            "/patches": self._get_patches,
            "/receipts": self._get_receipts,
            "/traces": self._get_traces,
            "/mutations/dirty": self._get_dirty_states,
            "/eval-runs": self._get_eval_runs,
            "/symbols": self._get_symbols,
            "/code-index": self._get_code_index,
            "/knowledge": self._get_knowledge,
            "/file-summary": self._get_file_summary,
            "/docs": self._get_docs,
            "/docs/search": self._get_docs_search,
            "/sessions": self._get_sessions,
        }

    def _get_detail_payload(self, path: str, query: dict[str, list[str]]) -> dict | None:
        routes = (
            ("/patches/", self._get_patch),
            ("/receipts/", self._get_receipt),
            ("/traces/", self._get_trace),
            ("/mutations/dirty/", self._get_dirty_state),
            ("/eval-runs/", self._get_eval_run),
            ("/sessions/", self._get_session),
        )
        for prefix, handler in routes:
            if path.startswith(prefix):
                return handler(path[len(prefix):], query)
        return None

    def _get_health(self, _query: dict[str, list[str]]) -> dict:
        from . import __version__

        dirty_dir = self.workspace / ".mind01" / "mutations" / "dirty"
        dirty_count = len(list(dirty_dir.glob("*.json"))) if dirty_dir.exists() else 0
        return {
            "ok": True,
            "workspace_name": self.workspace.name,
            "version": __version__,
            "mode": self.mode.value,
            "default_mode": self.mode.value,
            "auth_enabled": bool(self.api_token),
            "dirty_state_count": dirty_count,
            "receipt_chain_head_present": (self.workspace / ".mind01" / "receipts" / "head.json").exists(),
            "trace_chain_head_present": (self.workspace / ".mind01" / "traces" / "head.json").exists(),
        }

    def _get_project_map(self, _query: dict[str, list[str]]) -> dict:
        return {"text": build_project_map(self.workspace).render()}

    def _get_read_file(self, query: dict[str, list[str]]) -> dict:
        path = first(query, "path", "")
        _path, text = read_text_file_safe(self.workspace, path)
        return {"path": path, "text": redact_secrets(text[:20000])}

    def _get_search_code(self, query: dict[str, list[str]]) -> dict:
        result = ToolRegistry(self.workspace, mode=AgentMode.READ_ONLY).call(
            "search_code",
            {"query": first(query, "q", ""), "path": first(query, "path", ".")},
        )
        return {"text": result.text}

    def _get_memories(self, query: dict[str, list[str]]) -> dict:
        memories = MemoryStore(self.workspace).list(
            int(first(query, "limit", "50")), first(query, "tags", "")
        )
        return {"memories": [memory_to_dict(item) for item in memories]}

    def _get_memory_search(self, query: dict[str, list[str]]) -> dict:
        memories = MemoryStore(self.workspace).recall(
            first(query, "q", ""),
            int(first(query, "limit", "8")),
            first(query, "tags", ""),
        )
        return {"memories": [memory_to_dict(item) for item in memories]}

    def _get_patches(self, _query: dict[str, list[str]]) -> dict:
        return {"patches": [item.to_dict() for item in PatchStore(self.workspace).list()]}

    def _get_patch(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        return {"text": PatchStore(self.workspace).show(int(identifier))}

    def _get_receipts(self, query: dict[str, list[str]]) -> dict:
        return {"receipts": ReceiptStore(self.workspace).list(int(first(query, "limit", "50")))}

    def _get_receipt(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        return {"receipt": ReceiptStore(self.workspace).get(identifier)}

    def _get_traces(self, query: dict[str, list[str]]) -> dict:
        return {"traces": TraceStore(self.workspace).list(int(first(query, "limit", "20")))}

    def _get_trace(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        return {"text": TraceStore(self.workspace).render_show(identifier)}

    def _get_dirty_states(self, query: dict[str, list[str]]) -> dict:
        records = DirtyStateStore(self.workspace).list(int(first(query, "limit", "50")))
        return {"dirty_states": [safe_dirty_record(record) for record in records]}

    def _get_dirty_state(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        return {"dirty_state": safe_dirty_record(DirtyStateStore(self.workspace).get(identifier))}

    def _get_eval_runs(self, _query: dict[str, list[str]]) -> dict:
        return {"runs": list_eval_runs(self.workspace)}

    def _get_eval_run(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        return {"run": read_eval_run(self.workspace, identifier)}

    def _get_symbols(self, query: dict[str, list[str]]) -> dict:
        hits = CodeIndex(self.workspace).search_symbols(
            first(query, "q", ""), int(first(query, "limit", "20"))
        )
        return {"symbols": [symbol_to_dict(hit) for hit in hits]}

    def _get_code_index(self, _query: dict[str, list[str]]) -> dict:
        index = CodeIndex(self.workspace)
        files, symbols = index.stats()
        return {"files": files, "symbols": symbols, "stale": index.stale_files()}

    def _get_knowledge(self, query: dict[str, list[str]]) -> dict:
        store = ProjectKnowledgeStore(self.workspace)
        q = first(query, "q", "").strip()
        if not q:
            return store.stats()
        hits = store.query(q, int(first(query, "limit", "20")))
        return {"hits": [knowledge_hit_to_dict(hit) for hit in hits], **store.stats()}

    def _get_file_summary(self, query: dict[str, list[str]]) -> dict:
        summary = CodeIndex(self.workspace).file_summary(first(query, "path", ""))
        return {"text": render_file_summary(summary)}

    def _get_docs(self, _query: dict[str, list[str]]) -> dict:
        store = DocStore(self.workspace)
        return {**store.stats(), "stale": [stale_doc_to_dict(item) for item in store.stale_files()]}

    def _get_docs_search(self, query: dict[str, list[str]]) -> dict:
        embed = first(query, "embed", "false").lower() in {"1", "true", "yes"}
        embedding_model = first(query, "embedding_model", "nomic-embed-text")
        embedder = OllamaEmbeddingClient(self.ollama_url, embedding_model) if embed else None
        hits = DocStore(self.workspace).search(
            first(query, "q", ""),
            limit=int(first(query, "limit", "6")),
            embedder=embedder,
            embedding_model=embedding_model if embed else "",
        )
        return {"hits": [doc_hit_to_dict(hit) for hit in hits]}

    def _get_sessions(self, query: dict[str, list[str]]) -> dict:
        sessions = SessionStore(self.workspace).list(int(first(query, "limit", "50")))
        return {"sessions": [session_to_dict(item) for item in sessions]}

    def _get_session(self, identifier: str, _query: dict[str, list[str]]) -> dict:
        session, messages = SessionStore(self.workspace).get(identifier)
        return {
            "session": session_to_dict(session),
            "messages": [message_to_dict(item) for item in messages],
        }

    def _write_get_exception(self, request: BaseHTTPRequestHandler, req_id: str, exc: Exception) -> None:
        if isinstance(exc, EmbeddingError):
            write_error(request, "embedding_error", str(exc), status=502, cors_origin=self.cors_origin, request_id=req_id)
            return
        if isinstance(exc, MutationError):
            status = 404 if "not found" in str(exc).lower() else 400
            code = "not_found" if status == 404 else "bad_request"
            write_error(request, code, str(exc), status=status, cors_origin=self.cors_origin, request_id=req_id)
            return
        expected = (FileSafetyError, PatchError, ReceiptError, TraceError, ToolError, ValueError, TypeError)
        if isinstance(exc, expected):
            write_error(request, "bad_request", str(exc), status=400, cors_origin=self.cors_origin, request_id=req_id)
            return
        write_error(request, "internal_error", "Internal server error.", status=500, cors_origin=self.cors_origin, request_id=req_id)

    def handle_post(self, request: BaseHTTPRequestHandler) -> None:
        import uuid

        req_id = uuid.uuid4().hex
        agent = None
        acquired = self._request_slots.acquire(blocking=False)
        if not acquired:
            write_error(request, "server_busy", "Server concurrency limit reached.", status=429, cors_origin=self.cors_origin, request_id=req_id)
            return
        try:
            if not self.authorized(request):
                write_error(request, "unauthorized", "Unauthorized.", status=401, cors_origin=self.cors_origin, request_id=req_id)
                return
            body = read_json(request, self.policy.max_body_bytes)
            if request.path == "/chat":
                prompt = str(body.get("prompt", "")).strip()
                if not prompt:
                    write_error(request, "missing_prompt", "Missing prompt.", status=400, cors_origin=self.cors_origin, request_id=req_id)
                    return
                if len(prompt) > 100_000:
                    raise PolicyViolation("Prompt exceeds the server limit.")
                if "ollama_url" in body and str(body["ollama_url"]).rstrip("/") != self.ollama_url:
                    raise PolicyViolation("Client-controlled Ollama endpoints are not allowed.")
                if "model" in body and str(body["model"]) != self.model:
                    raise PolicyViolation("Client-controlled model selection is disabled by server policy.")
                mode = self.policy.resolve_mode(body.get("mode", self.mode.value))
                max_steps = self.policy.resolve_steps(body.get("max_steps"), default=min(8, self.policy.max_steps))
                server_write, server_shell, server_approve = self.policy.capabilities_for(mode)
                requested_write = bool(body.get("allow_write", server_write))
                requested_shell = bool(body.get("allow_shell", server_shell))
                if requested_write and not server_write:
                    raise PolicyViolation("Write capability is disabled by server policy.")
                if requested_shell and not server_shell:
                    raise PolicyViolation("Shell capability is disabled by server policy.")
                session_id = str(body.get("session_id", "")).strip()
                store = SessionStore(self.workspace)
                if not session_id:
                    session_id = store.create(title=prompt[:80]).id
                elif not store.exists(session_id):
                    raise ValueError(f"Session not found: {session_id}")
                history = store.context_messages(session_id)
                config = AgentConfig.build(
                    workspace=str(self.workspace),
                    model=self.model,
                    ollama_url=self.ollama_url,
                    max_steps=max_steps,
                    yes=server_approve and bool(body.get("yes", True)),
                    dry_run=bool(body.get("dry_run", False)),
                    trace=bool(body.get("trace", False)),
                    allow_write=server_write and requested_write,
                    allow_shell=server_shell and requested_shell,
                    mode=mode,
                    request_timeout_seconds=self.policy.request_timeout_seconds,
                )
                agent = Agent(config, initial_messages=history, session_id=session_id)
                if bool(body.get("stream", False)):
                    self._handle_chat_stream(request, agent, prompt, session_id, store)
                else:
                    response = agent.ask(prompt)
                    store.add_message(session_id, "user", prompt)
                    store.add_message(session_id, "assistant", response.text, "\n".join(response.trace))
                    write_json(
                        request,
                        chat_response_payload(session_id, response),
                        cors_origin=self.cors_origin,
                    )
            elif request.path == "/index":
                self._require_mode(body, {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}, "index")
                path = str(body.get("path", "."))
                count = CodeIndex(self.workspace).index_path(resolve_workspace_path(self.workspace, path))
                write_json(request, {"indexed_files": count}, cors_origin=self.cors_origin)
            elif request.path == "/knowledge/refresh":
                self._require_mode(
                    body,
                    {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE},
                    "knowledge refresh",
                )
                counts = ProjectKnowledgeStore(self.workspace).refresh(str(body.get("path", ".")))
                write_json(
                    request,
                    {**counts, **ProjectKnowledgeStore(self.workspace).stats()},
                    cors_origin=self.cors_origin,
                )
            elif request.path == "/docs/index":
                self._require_mode(body, {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}, "docs/index")
                path = str(body.get("path", "."))
                embed = bool(body.get("embed", False))
                embedding_model = str(body.get("embedding_model", "nomic-embed-text"))
                if "ollama_url" in body:
                    raise PolicyViolation("Client-controlled Ollama endpoints are not allowed.")
                embedder = OllamaEmbeddingClient(self.ollama_url, embedding_model) if embed else None
                count = DocStore(self.workspace).index_path(
                    resolve_workspace_path(self.workspace, path),
                    embedder=embedder,
                    embedding_model=embedding_model if embed else "",
                )
                write_json(request, {"indexed_chunks": count, **DocStore(self.workspace).stats()}, cors_origin=self.cors_origin)
            elif request.path == "/patches/propose":
                self._require_mode(body, {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}, "patch proposal")
                patch = propose_patch(self.workspace, body)
                write_json(request, {"patch": patch.to_dict()}, cors_origin=self.cors_origin)
            elif request.path == "/patches/apply":
                mode = self._require_mode(body, {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}, "patch apply")
                write_enabled, _shell, auto_approve = self.policy.capabilities_for(mode)
                if not write_enabled:
                    raise PolicyViolation("Patch apply is disabled by server write policy.")
                if not auto_approve:
                    raise PolicyViolation("API mutation approval is disabled by server policy.")
                patch_id = body.get("id")
                if patch_id is None:
                    raise ValueError("patch apply requires id.")
                result = PatchStore(self.workspace).apply(
                    int(patch_id), mode=mode.value, allow_write=True, approved=True, source="api:patch apply"
                )
                write_json(request, {"text": result}, cors_origin=self.cors_origin)
            elif request.path == "/rollback":
                mode = self._require_mode(body, {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}, "rollback")
                write_enabled, _shell, auto_approve = self.policy.capabilities_for(mode)
                if not write_enabled or not auto_approve:
                    raise PolicyViolation("API rollback is disabled by server mutation policy.")
                receipt = ReceiptStore(self.workspace).rollback(
                    str(body.get("receipt_id", "")),
                    mode=mode.value,
                    approved=True,
                    force=bool(body.get("force", False)),
                    source="api:rollback",
                )
                write_json(request, {"receipt": receipt}, cors_origin=self.cors_origin)
            elif request.path == "/sessions":
                title = str(body.get("title", "New session"))
                session = SessionStore(self.workspace).create(title=title)
                write_json(request, {"session": session_to_dict(session)}, cors_origin=self.cors_origin)
            else:
                write_error(request, "not_found", "Not found.", status=404, cors_origin=self.cors_origin, request_id=req_id)
        except EmbeddingError:
            t_id = agent.last_event_id if agent else None
            write_error(request, "embedding_error", "Embedding service failed.", status=502, cors_origin=self.cors_origin, request_id=req_id, trace_id=t_id)
        except MutationError as exc:
            t_id = agent.last_event_id if agent else None
            status = 404 if "not found" in str(exc).lower() else 400
            code = "not_found" if status == 404 else "bad_request"
            write_error(request, code, redact_secrets(str(exc)), status=status, cors_origin=self.cors_origin, request_id=req_id, trace_id=t_id)
        except (PolicyViolation, FileSafetyError, PatchError, ReceiptError, TraceError, ToolError, ValueError, TypeError) as exc:
            t_id = agent.last_event_id if agent else None
            write_error(request, "bad_request", redact_secrets(str(exc)), status=400, cors_origin=self.cors_origin, request_id=req_id, trace_id=t_id)
        except Exception:
            t_id = agent.last_event_id if agent else None
            write_error(request, "internal_error", "Internal server error.", status=500, cors_origin=self.cors_origin, request_id=req_id, trace_id=t_id)
        finally:
            self._request_slots.release()

    def _handle_chat_stream(
        self,
        request: BaseHTTPRequestHandler,
        agent: Agent,
        prompt: str,
        session_id: str,
        store: SessionStore,
    ) -> None:
        """Serve /chat as a Server-Sent Events stream (WS6).

        Emits one `event` frame per lifecycle stage and per tool call/result,
        then a final `done` frame carrying the complete response payload.
        Non-streaming clients are unaffected (plain JSON path above).
        """

        started = False

        def emit(event: str, data: dict) -> None:
            nonlocal started
            if not started:
                request.send_response(200)
                request.send_header("Content-Type", "text/event-stream; charset=utf-8")
                request.send_header("Cache-Control", "no-cache")
                request.send_header("Connection", "keep-alive")
                request.send_header("X-Accel-Buffering", "no")
                request.send_header("Access-Control-Allow-Origin", self.cors_origin)
                request.send_header("Access-Control-Allow-Headers", "Content-Type, X-Mind-Token")
                request.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
                request.end_headers()
                started = True
            payload = json.dumps(data, ensure_ascii=False)
            request.wfile.write(f"event: {event}\ndata: {payload}\n\n".encode("utf-8"))
            request.wfile.flush()

        agent.on_event = lambda event_type, item: emit(
            "agent_event",
            {"event_type": event_type, **{k: v for k, v in item.items() if k != "event_type"}},
        )
        try:
            response = agent.ask(prompt)
            store.add_message(session_id, "user", prompt)
            store.add_message(session_id, "assistant", response.text, "\n".join(response.trace))
            emit("done", chat_response_payload(session_id, response))
        except Exception as exc:  # streamed clients cannot get a JSON error body
            emit("error", {"error": {"code": "stream_error", "message": redact_secrets(str(exc))}})

    def _require_mode(self, body: dict, allowed: set[AgentMode], action: str) -> AgentMode:
        mode = self.policy.resolve_mode(body.get("mode", self.mode.value))
        if mode not in allowed:
            allowed_text = ", ".join(sorted(item.value for item in allowed))
            raise PolicyViolation(f"{action} is not allowed in mode `{mode.value}`. Allowed modes: {allowed_text}.")
        return mode

    def authorized(self, request: BaseHTTPRequestHandler) -> bool:
        if not self.api_token:
            return True
        return request.headers.get("X-Mind-Token", "") == self.api_token


def serve_api(
    workspace: Path,
    host: str,
    port: int,
    model: str,
    ollama_url: str,
    mode: str | AgentMode = AgentMode.READ_ONLY,
    api_token: str = "",
    cors_origin: str = "http://localhost:3000",
    *,
    allow_write: bool = False,
    allow_shell: bool = False,
    auto_approve: bool = False,
    max_steps: int = 12,
    max_body_bytes: int = MAX_BODY_BYTES,
    max_concurrent_requests: int = 4,
    request_timeout_seconds: int = 180,
) -> None:
    if host not in {"127.0.0.1", "localhost", "::1"} and not api_token:
        raise ValueError("A token is required when binding the API beyond loopback.")
    api = MindAPI(
        workspace,
        model,
        ollama_url,
        mode=mode,
        api_token=api_token,
        cors_origin=cors_origin,
        allow_write=allow_write,
        allow_shell=allow_shell,
        auto_approve=auto_approve,
        max_steps=max_steps,
        max_body_bytes=max_body_bytes,
        max_concurrent_requests=max_concurrent_requests,
        request_timeout_seconds=request_timeout_seconds,
    )
    server = ThreadingHTTPServer((host, port), api.handler())
    print(f"Mind1.1 API listening on http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nMind1.1 API stopped.")
    finally:
        server.server_close()


def read_json(request: BaseHTTPRequestHandler, max_body_bytes: int = MAX_BODY_BYTES) -> dict:
    length = int(request.headers.get("Content-Length", "0"))
    if length < 0:
        raise ValueError("Invalid Content-Length.")
    if length > max_body_bytes:
        raise ValueError("Request body is too large.")
    raw = request.rfile.read(length).decode("utf-8") if length else "{}"
    data = json.loads(raw)
    if not isinstance(data, dict):
        raise ValueError("JSON body must be an object.")
    return data


def write_json(
    request: BaseHTTPRequestHandler,
    payload: dict,
    status: int = 200,
    cors_origin: str = "http://localhost:3000",
) -> None:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request.send_response(status)
    request.send_header("Content-Type", "application/json; charset=utf-8")
    request.send_header("Access-Control-Allow-Origin", cors_origin)
    request.send_header("Access-Control-Allow-Headers", "Content-Type, X-Mind-Token")
    request.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
    request.send_header("Content-Length", str(len(data)))
    request.end_headers()
    request.wfile.write(data)


def write_error(
    request: BaseHTTPRequestHandler,
    code: str,
    message: str,
    status: int,
    cors_origin: str = "http://localhost:3000",
    details: dict | None = None,
    request_id: str | None = None,
    trace_id: str | None = None,
) -> None:
    payload = {
        "error": {
            "code": code,
            "message": message,
            "details": details or {},
            "request_id": request_id or "",
            "trace_id": trace_id,
        }
    }
    write_json(request, payload, status=status, cors_origin=cors_origin)


def first(query: dict[str, list[str]], key: str, default: str) -> str:
    values = query.get(key)
    if not values:
        return default
    return values[0]


def resolve_workspace_path(workspace: Path, raw_path: str) -> Path:
    path = (workspace / raw_path).resolve()
    if workspace != path and workspace not in path.parents:
        raise ValueError(f"Path escapes workspace: {raw_path}")
    return path


def require_api_mode(body: dict, allowed: set[AgentMode], action: str) -> AgentMode:
    mode = parse_agent_mode(str(body.get("mode", AgentMode.READ_ONLY.value)))
    if mode not in allowed:
        allowed_text = ", ".join(sorted(item.value for item in allowed))
        raise ValueError(
            f"{action} is not allowed in mode `{mode.value}`. Allowed modes: {allowed_text}."
        )
    return mode


def propose_patch(workspace: Path, body: dict):
    store = PatchStore(workspace)
    kind = str(body.get("kind", "edit"))
    path = str(body.get("path", ""))
    reason = str(body.get("reason", "api proposal"))
    if kind == "write":
        return store.propose_write(path, str(body.get("content", "")), reason)
    if kind == "edit":
        return store.propose_edit(path, str(body.get("old", "")), str(body.get("new", "")), reason)
    raise ValueError("Patch proposal kind must be `write` or `edit`.")


def chat_response_payload(session_id: str, response) -> dict:  # type: ignore[no-untyped-def]
    return {
        "session_id": session_id,
        "text": response.text,
        "steps": response.steps,
        "trace": response.trace,
        "specialist": response.specialist,
        "verification": response.verification,
        "parser_incidents": response.parser_incidents,
        "completion_status": response.completion_status,
        "completion_contract": response.completion_contract,
        "routing_decision": response.routing_decision,
        "output_mode": response.output_mode,
    }


def memory_to_dict(item) -> dict:  # type: ignore[no-untyped-def]
    return {
        "id": item.id,
        "memory_id": item.memory_id,
        "key": item.key,
        "value": item.value,
        "text": item.text,
        "tags": item.tags,
        "source": item.source,
        "importance": item.importance,
        "created_at": item.created_at,
        "updated_at": item.updated_at,
        "last_used_at": item.last_used_at,
        "use_count": item.use_count,
        "score": item.score,
        "lexical_score": item.lexical_score,
        "vector_score": item.vector_score,
        "embedding_model": item.embedding_model,
    }


def symbol_to_dict(item) -> dict:  # type: ignore[no-untyped-def]
    return {
        "name": item.name,
        "kind": item.kind,
        "path": item.path,
        "line": item.line,
        "signature": item.signature,
    }


def knowledge_hit_to_dict(item) -> dict:  # type: ignore[no-untyped-def]
    return {
        "entity_id": item.entity_id,
        "entity_type": item.entity_type,
        "name": item.name,
        "path": item.path,
        "provenance": item.provenance,
        "metadata": item.metadata,
    }


def doc_hit_to_dict(item) -> dict:  # type: ignore[no-untyped-def]
    return {
        "path": item.path,
        "line_start": item.line_start,
        "line_end": item.line_end,
        "citation": item.citation,
        "chunk": item.chunk,
        "chunk_sha256": item.chunk_sha256,
        "file_mtime_ns": item.file_mtime_ns,
        "stale": item.stale,
        "score": item.score,
        "rank": item.rank,
        "lexical_score": item.lexical_score,
        "vector_score": item.vector_score,
        "embedding_model": item.embedding_model,
    }


def stale_doc_to_dict(item) -> dict:  # type: ignore[no-untyped-def]
    return {"path": item.path, "reason": item.reason}


def list_eval_runs(workspace: Path) -> list[dict]:
    root = workspace / ".mind01" / "eval_runs"
    if not root.exists():
        return []
    runs = []
    for path in sorted(root.glob("*.json"), reverse=True):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            runs.append({"path": str(path.relative_to(workspace)), "summary": data.get("summary", {})})
        except (OSError, json.JSONDecodeError):
            continue
    return runs


def read_eval_run(workspace: Path, identifier: str) -> dict:
    if "/" in identifier or "\\" in identifier or identifier.startswith("."):
        raise ValueError(f"Invalid eval run identifier: {identifier}")
    name = identifier if identifier.endswith(".json") else f"{identifier}.json"
    path = (workspace / ".mind01" / "eval_runs" / name).resolve()
    root = (workspace / ".mind01" / "eval_runs").resolve()
    if root != path.parent:
        raise ValueError(f"Invalid eval run identifier: {identifier}")
    if not path.exists():
        raise ValueError(f"Eval run not found: {identifier}")
    return json.loads(path.read_text(encoding="utf-8"))


def default_api_token() -> str:
    return os.environ.get("MIND_API_TOKEN", "")
