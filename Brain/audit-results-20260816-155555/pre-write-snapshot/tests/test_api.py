from __future__ import annotations

import json
import shutil
import tempfile
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
import urllib.parse

from mind01.api import MindAPI
from mind01.modes import AgentMode


def run_api_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-api-"))
    try:
        (tmp / "src").mkdir()
        (tmp / "src" / "demo.py").write_text("def demo():\n    return 1\n", encoding="utf-8")
        api = MindAPI(
            tmp,
            "qwen2.5-coder:7b",
            "http://127.0.0.1:11434",
            api_token="test-token",
            max_steps=6,
        )
        assert api.mode == AgentMode.READ_ONLY

        try:
            MindAPI(tmp, "model", "http://127.0.0.1:11434", mode="bad-mode")
            raise AssertionError("invalid API mode was not rejected")
        except ValueError as exc:
            assert "Invalid mode" in str(exc)
        try:
            MindAPI(tmp, "model", "http://127.0.0.1:11434", api_token="token", cors_origin="*")
            raise AssertionError("wildcard CORS with auth was not rejected")
        except ValueError as exc:
            assert "Wildcard CORS" in str(exc)
        try:
            MindAPI(tmp, "model", "http://169.254.169.254:80", api_token="token")
            raise AssertionError("untrusted model endpoint was not rejected")
        except ValueError as exc:
            assert "not allowed" in str(exc)
        try:
            MindAPI(tmp, "model", "http://127.0.0.1:11434", mode="write-approved", allow_write=True)
            raise AssertionError("elevated API without token was not rejected")
        except ValueError as exc:
            assert "token is required" in str(exc)

        status, unauthorized = request_json(api, "GET", "/health")
        assert status == 401
        assert unauthorized["error"]["code"] == "unauthorized"

        status, health = request_json(api, "GET", "/health", token="test-token")
        assert status == 200
        assert health["mode"] == "read-only"
        assert "workspace" not in health
        assert health["workspace_name"] == tmp.name

        read_url = "/read-file?" + urllib.parse.urlencode({"path": "src/demo.py"})
        status, read_payload = request_json(api, "GET", read_url, token="test-token")
        assert status == 200 and "def demo" in read_payload["text"]

        status, escalation = request_json(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "hello", "mode": "unsafe", "allow_write": True, "dry_run": True},
        )
        assert status == 400
        assert "exceeds server maximum" in escalation["error"]["message"]

        status, ssrf = request_json(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "hello", "ollama_url": "http://169.254.169.254/latest", "dry_run": True},
        )
        assert status == 400
        assert "Client-controlled Ollama" in ssrf["error"]["message"]

        status, too_many_steps = request_json(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "hello", "max_steps": 100, "dry_run": True},
        )
        assert status == 400
        assert "server limit" in too_many_steps["error"]["message"]

        status, readonly_index = request_json(
            api, "POST", "/index", token="test-token", data={"path": ".", "mode": "propose"}
        )
        assert status == 400
        assert "exceeds server maximum" in readonly_index["error"]["message"]

        propose_api = MindAPI(
            tmp,
            "qwen2.5-coder:7b",
            "http://127.0.0.1:11434",
            mode="propose",
            api_token="test-token",
        )
        status, indexed = request_json(
            propose_api, "POST", "/index", token="test-token", data={"path": ".", "mode": "propose"}
        )
        assert status == 200 and indexed["indexed_files"] >= 1

        status, knowledge = request_json(
            propose_api,
            "POST",
            "/knowledge/refresh",
            token="test-token",
            data={"path": ".", "mode": "propose"},
        )
        assert status == 200 and knowledge["files"] >= 1 and knowledge["entities"] >= 1
        status, knowledge_hits = request_json(
            propose_api, "GET", "/knowledge?q=demo&limit=10", token="test-token"
        )
        assert status == 200
        assert any(hit["name"] == "demo" for hit in knowledge_hits["hits"])

        status, busy = _request_while_busy(api, token="test-token")
        assert status == 429 and busy["error"]["code"] == "server_busy"

        _test_real_session_context(api)
        _test_streaming_chat(api)

        huge_api = MindAPI(
            tmp,
            "qwen2.5-coder:7b",
            "http://127.0.0.1:11434",
            api_token="test-token",
            max_body_bytes=1024,
        )
        status, oversized = request_json(
            huge_api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "x" * 3000, "dry_run": True},
        )
        assert status == 400 and "too large" in oversized["error"]["message"]
    finally:
        shutil.rmtree(tmp)


def _test_real_session_context(api: MindAPI) -> None:
    first_output = json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"Noted.","evidence_refs":[]})
    with patch("mind01.agent.OllamaClient.chat", return_value=first_output):
        status, first = request_json(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "My project codename is Atlas."},
        )
    assert status == 200
    session_id = first["session_id"]

    def second_chat(_client, messages, json_mode=False, response_schema=None):  # type: ignore[no-untyped-def]
        joined = "\n".join(item["content"] for item in messages)
        assert "My project codename is Atlas." in joined
        assert "Noted." in joined
        return json.dumps({"schema_version":"1.0","response_type":"final","status":"unverified","summary":"Your project codename is Atlas.","evidence_refs":[]})

    with patch("mind01.agent.OllamaClient.chat", new=second_chat):
        status, second = request_json(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "What is my project codename?", "session_id": session_id},
        )
    assert status == 200
    assert second["text"] == "Your project codename is Atlas."


def _request_while_busy(api: MindAPI, token: str) -> tuple[int, dict]:
    acquired = 0
    try:
        for _ in range(api.policy.max_concurrent_requests):
            api._request_slots.acquire()
            acquired += 1
        return request_json(api, "POST", "/chat", token=token, data={"prompt": "hello", "dry_run": True})
    finally:
        for _ in range(acquired):
            api._request_slots.release()


def request_json(
    api: MindAPI,
    method: str,
    path: str,
    token: str = "",
    data: dict | None = None,
) -> tuple[int, dict]:
    headers: dict[str, str] = {}
    body = b""
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body))
    if token:
        headers["X-Mind-Token"] = token
    request = FakeRequest(path, headers, body)
    if method == "GET":
        api.handle_get(request)
    else:
        api.handle_post(request)
    payload = json.loads(request.wfile.getvalue().decode("utf-8"))
    return request.status, payload


class FakeRequest:
    def __init__(self, path: str, headers: dict[str, str], body: bytes) -> None:
        self.path = path
        self.headers = headers
        self.rfile = BytesIO(body)
        self.wfile = BytesIO()
        self.status = 0
        self.response_headers: list[tuple[str, str]] = []

    def send_response(self, status: int) -> None:
        self.status = status

    def send_header(self, key: str, value: str) -> None:
        self.response_headers.append((key, value))

    def end_headers(self) -> None:
        return


def _test_streaming_chat(api: MindAPI) -> None:
    final = json.dumps(
        {
            "schema_version": "1.0",
            "response_type": "final",
            "status": "unverified",
            "summary": "Streamed hello.",
            "evidence_refs": [],
        }
    )

    def streamed_chat(_client, messages, json_mode=False, response_schema=None):  # type: ignore[no-untyped-def]
        return final

    with patch("mind01.agent.OllamaClient.chat", new=streamed_chat):
        status, stream = request_stream(
            api,
            "POST",
            "/chat",
            token="test-token",
            data={"prompt": "Say hello", "stream": True},
        )
    assert status == 200
    content_type = dict(stream["headers"]).get("Content-Type", "")
    assert content_type.startswith("text/event-stream"), content_type
    events = parse_sse(stream["body"])
    types = [event["event"] for event in events]
    assert "agent_event" in types, f"expected lifecycle events in stream: {types}"
    assert types[-1] == "done", f"expected trailing done event: {types}"
    done = events[-1]["data"]
    assert done["text"] == "Streamed hello."
    assert done["session_id"]
    # The stream must contain at least the prompt lifecycle event.
    agent_events = [event for event in events if event["event"] == "agent_event"]
    assert any(event["data"].get("event_type") == "agent_prompt" for event in agent_events)


def request_stream(
    api: MindAPI,
    method: str,
    path: str,
    token: str = "",
    data: dict | None = None,
) -> tuple[int, dict]:
    headers: dict[str, str] = {}
    body = b""
    if data is not None:
        body = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
        headers["Content-Length"] = str(len(body))
    if token:
        headers["X-Mind-Token"] = token
    request = FakeRequest(path, headers, body)
    api.handle_post(request)
    raw = request.wfile.getvalue().decode("utf-8")
    return request.status, {"headers": request.response_headers, "body": raw}


def parse_sse(raw: str) -> list[dict]:
    events: list[dict] = []
    current: dict = {"event": "message", "data": {}}
    for line in raw.splitlines():
        if not line.strip():
            if current.get("data"):
                events.append(current)
            current = {"event": "message", "data": {}}
            continue
        if line.startswith("event: "):
            current["event"] = line[len("event: "):]
        elif line.startswith("data: "):
            current["data"] = json.loads(line[len("data: "):])
    if current.get("data"):
        events.append(current)
    return events


def test_api_security_and_sessions() -> None:
    run_api_tests()
