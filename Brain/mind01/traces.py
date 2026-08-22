from __future__ import annotations

import hashlib
import json
import re
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .security import redact_secrets, redact_structure
from .locking import file_lock


RECEIPT_RE = re.compile(r"\b[Rr]eceipt\s+([0-9A-Za-zT_:-]+)")
SENSITIVE_ARG_NAMES = {"api_key", "apikey", "authorization", "password", "secret", "token"}
CONTENT_ARG_NAMES = {"content", "old", "new", "value"}


class TraceError(RuntimeError):
    pass


class TraceStore:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.root = self.workspace / ".mind01" / "traces"
        self.root.mkdir(parents=True, exist_ok=True)

    def append(self, event: dict[str, Any]) -> dict[str, Any]:
        with file_lock(self.root / ".chain.lock"):
            return self._append_unlocked(event)

    def _append_unlocked(self, event: dict[str, Any]) -> dict[str, Any]:
        import os
        item = redact_structure(dict(event))
        item.setdefault("timestamp", datetime.now(timezone.utc).isoformat())
        item.setdefault("event_id", uuid.uuid4().hex)
        item.setdefault("trace_id", item["event_id"])

        head_path = self.root / "head.json"
        prev_hash = None
        if head_path.exists():
            try:
                head_data = json.loads(head_path.read_text(encoding="utf-8"))
                if not isinstance(head_data, dict) or "event_hash" not in head_data:
                    raise TraceError("head.json is invalid or corrupted")
                prev_hash = head_data["event_hash"]
            except Exception as exc:
                raise TraceError(f"head.json exists but is invalid/corrupted: {exc}") from exc

            actual_last_hash = self._get_last_event_hash_fallback()
            if actual_last_hash != prev_hash:
                raise TraceError("head.json is inconsistent with the latest trace event in logs")
        else:
            prev_hash = self._get_last_event_hash_fallback()

        item["previous_event_hash"] = prev_hash
        from .receipts import canonical_json
        event_hash = hashlib.sha256(canonical_json(item)).hexdigest()
        item["event_hash"] = event_hash

        path = self._daily_path()
        try:
            with path.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(item, sort_keys=True, ensure_ascii=False) + "\n")
        except OSError as exc:
            raise TraceError("Could not write trace event.") from exc

        temp_head = head_path.parent / f".head.json.tmp-{uuid.uuid4().hex}"
        try:
            temp_head.write_text(
                json.dumps(
                    {"event_id": item["event_id"], "event_hash": event_hash},
                    indent=2,
                    sort_keys=True,
                ),
                encoding="utf-8",
            )
            os.replace(temp_head, head_path)
        except Exception as exc:
            raise TraceError(f"Could not write trace head atomically: {exc}") from exc

        return item

    def _get_last_event_hash_fallback(self) -> str | None:
        for path in sorted(self.root.glob("*.jsonl"), reverse=True):
            try:
                with path.open("rb") as handle:
                    lines = handle.readlines()
                    for line in reversed(lines):
                        line_str = line.decode("utf-8").strip()
                        if not line_str:
                            continue
                        try:
                            data = json.loads(line_str)
                            if isinstance(data, dict) and "event_hash" in data:
                                return data["event_hash"]
                        except json.JSONDecodeError:
                            continue
            except OSError:
                continue
        return None

    def list(self, limit: int = 20) -> list[dict[str, Any]]:
        files = sorted(self.root.glob("*.jsonl"), reverse=True)
        rendered = []
        for path in files[:limit]:
            rendered.append(
                {
                    "file": path.name,
                    "path": str(path.relative_to(self.workspace)),
                    "size_bytes": path.stat().st_size,
                    "events": count_jsonl_lines(path),
                }
            )
        return rendered

    def render_list(self, limit: int = 20) -> str:
        items = self.list(limit=limit)
        if not items:
            return "(no traces)"
        return "\n".join(
            f"{item['file']} events={item['events']} size={item['size_bytes']} path={item['path']}"
            for item in items
        )

    def render_show(self, identifier: str) -> str:
        if "/" in identifier or "\\" in identifier or identifier.startswith("."):
            raise TraceError(f"Invalid trace identifier: {identifier}")
        file_path = self.root / identifier
        if file_path.suffix != ".jsonl":
            file_path = self.root / f"{identifier}.jsonl"
        if file_path.exists():
            try:
                return file_path.read_text(encoding="utf-8")
            except OSError as exc:
                raise TraceError(f"Could not read trace file: {identifier}") from exc
        event = self.find_event(identifier)
        if event is None:
            raise TraceError(f"Trace not found: {identifier}")
        return json.dumps(event, indent=2, sort_keys=True, ensure_ascii=False)

    def find_event(self, trace_id: str) -> dict[str, Any] | None:
        for path in sorted(self.root.glob("*.jsonl"), reverse=True):
            try:
                with path.open("r", encoding="utf-8") as handle:
                    for line in handle:
                        if not line.strip():
                            continue
                        event = json.loads(line)
                        if event.get("trace_id") == trace_id or event.get("event_id") == trace_id:
                            return event
            except (OSError, json.JSONDecodeError):
                continue
        return None

    def record_task_bundle(self, bundle: dict[str, Any]) -> dict[str, Any]:
        """Append a complete task-run bundle to the existing hash chain (WS5).

        A bundle aggregates one agent run: the (sanitized) prompt, the action
        sequence, verification results, and completion status.  It lives in the
        same TraceStore and chain as every other event — no parallel logging
        system — and is the seed source for supervised fine-tuning.

        Bundle fields are sanitized before storage (secrets redacted, file
        contents hashed/previewed).  The caller sets ``consent`` explicitly;
        consent-free runs store the bundle only when ``consent`` is true.
        """

        consent = bool(bundle.get("consent", False))
        if not consent:
            return {"consent_required": True, "event_id": None}
        payload = dict(bundle)
        payload["prompt"] = summarize_text(str(payload.get("prompt", "")))
        for step in payload.get("action_sequence", []):
            if isinstance(step, dict) and "args" in step:
                step["args"] = sanitize_args(step.get("args") or {})
        return self.append(
            {
                "event_type": "task_bundle",
                "session_id": payload.get("session_id"),
                "model_name": payload.get("model_name"),
                "mode": payload.get("mode"),
                "consent": True,
                "consent_source": payload.get("consent_source", "unknown"),
                "prompt": payload.get("prompt"),
                "action_sequence": payload.get("action_sequence", []),
                "verification": payload.get("verification", []),
                "completion_status": payload.get("completion_status", ""),
                "steps": payload.get("steps", 0),
                "latency_ms": payload.get("latency_ms", 0),
                "workspace_name": payload.get("workspace_name"),
            }
        )

    def _daily_path(self) -> Path:
        day = datetime.now(timezone.utc).strftime("%Y%m%d")
        return self.root / f"{day}.jsonl"


def trace_event_base(
    *,
    event_type: str,
    mode: str,
    session_id: str | None = None,
    model_name: str | None = None,
) -> dict[str, Any]:
    return {
        "event_type": event_type,
        "session_id": session_id,
        "mode": mode,
        "model_name": model_name,
    }


def sanitize_args(args: dict[str, Any]) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for key, value in args.items():
        lowered = key.lower()
        if lowered in SENSITIVE_ARG_NAMES or any(token in lowered for token in SENSITIVE_ARG_NAMES):
            sanitized[key] = "[REDACTED]"
            continue
        if isinstance(value, str):
            if lowered in CONTENT_ARG_NAMES:
                sanitized[key] = summarize_text(value)
            else:
                sanitized[key] = redact_secrets(value)
        elif isinstance(value, (int, float, bool)) or value is None:
            sanitized[key] = value
        else:
            sanitized[key] = summarize_text(json.dumps(value, sort_keys=True, default=str))
    return sanitized


def summarize_text(text: str, limit: int = 160) -> dict[str, Any]:
    redacted = redact_secrets(text)
    return {
        "sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "size": len(text.encode("utf-8")),
        "preview": redacted[:limit],
    }


def summarize_prompt(prompt: str) -> dict[str, Any]:
    return summarize_text(prompt, limit=160)


def summarize_result(text: str, limit: int = 300) -> dict[str, Any]:
    redacted = redact_secrets(text)
    return {
        "size": len(text.encode("utf-8")),
        "preview": redacted[:limit],
    }


def extract_receipt_id(text: str) -> str | None:
    match = RECEIPT_RE.search(text)
    if not match:
        return None
    return match.group(1).rstrip(".")


def count_jsonl_lines(path: Path) -> int:
    try:
        with path.open("r", encoding="utf-8") as handle:
            return sum(1 for line in handle if line.strip())
    except OSError:
        return 0


def duration_ms(start: float) -> int:
    return int((time.perf_counter() - start) * 1000)


def verify_trace_chain(workspace: Path) -> dict:
    store = TraceStore(workspace)
    trace_files = sorted(store.root.glob("*.jsonl"))

    if not trace_files:
        head_path = store.root / "head.json"
        if head_path.exists():
            return {
                "status": "invalid",
                "message": "head.json exists but no trace files found",
                "verified_count": 0,
                "legacy_count": 0,
            }
        return {
            "status": "empty",
            "message": "No trace events found.",
            "verified_count": 0,
            "legacy_count": 0,
        }

    legacy_count = 0
    verified_count = 0
    last_hash = None
    from .receipts import canonical_json

    for path in trace_files:
        try:
            with path.open("r", encoding="utf-8") as handle:
                for line in handle:
                    if not line.strip():
                        continue
                    data = json.loads(line)
                    if "event_hash" not in data:
                        if verified_count > 0:
                            return {
                                "status": "invalid",
                                "message": f"Legacy event {data.get('event_id')} found after verified events in chain.",
                                "verified_count": verified_count,
                                "legacy_count": legacy_count,
                            }
                        legacy_count += 1
                        continue

                    stored_hash = data["event_hash"]
                    expected_hash = hashlib.sha256(canonical_json(data)).hexdigest()
                    if stored_hash != expected_hash:
                        return {
                            "status": "invalid",
                            "message": f"Hash mismatch in trace event {data.get('event_id')}. Stored: {stored_hash}, Computed: {expected_hash}",
                            "verified_count": verified_count,
                            "legacy_count": legacy_count,
                        }

                    stored_prev_hash = data.get("previous_event_hash")
                    if stored_prev_hash != last_hash:
                        return {
                            "status": "invalid",
                            "message": f"Link mismatch in trace event {data.get('event_id')}. Expected previous: {last_hash}, Stored: {stored_prev_hash}",
                            "verified_count": verified_count,
                            "legacy_count": legacy_count,
                        }

                    last_hash = stored_hash
                    verified_count += 1
        except Exception as exc:
            return {
                "status": "invalid",
                "message": f"Could not read trace file {path.name}: {exc}",
                "verified_count": verified_count,
                "legacy_count": legacy_count,
            }

    # Verify head.json
    head_path = store.root / "head.json"
    if not head_path.exists():
        if verified_count > 0:
            return {
                "status": "invalid",
                "message": "head.json is missing but verified trace events exist",
                "verified_count": verified_count,
                "legacy_count": legacy_count,
            }
        return {
            "status": "valid_with_legacy",
            "message": "Only legacy trace events exist, no chain head.",
            "verified_count": 0,
            "legacy_count": legacy_count,
        }

    try:
        head_data = json.loads(head_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {
            "status": "invalid",
            "message": f"Could not read head.json: {exc}",
            "verified_count": verified_count,
            "legacy_count": legacy_count,
        }

    head_hash = head_data.get("event_hash")
    if head_hash != last_hash:
        return {
            "status": "invalid",
            "message": f"head.json points to event hash {head_hash}, but chain end is {last_hash}",
            "verified_count": verified_count,
            "legacy_count": legacy_count,
        }

    status = "valid" if legacy_count == 0 else "valid_with_legacy"
    return {
        "status": status,
        "message": "Trace chain is healthy.",
        "verified_count": verified_count,
        "legacy_count": legacy_count,
    }
