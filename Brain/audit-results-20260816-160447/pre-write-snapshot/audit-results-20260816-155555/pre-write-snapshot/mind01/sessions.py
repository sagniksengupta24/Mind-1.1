from __future__ import annotations

import sqlite3
import time
import uuid
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Session:
    id: str
    title: str
    created_at: int
    updated_at: int


@dataclass(frozen=True)
class SessionMessage:
    role: str
    content: str
    trace: str
    created_at: int


class SessionStore:
    def __init__(self, workspace: Path) -> None:
        self.db_path = workspace.resolve() / ".mind01" / "sessions.sqlite3"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute("PRAGMA foreign_keys=ON")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT NOT NULL,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    trace TEXT NOT NULL DEFAULT '',
                    created_at INTEGER NOT NULL,
                    FOREIGN KEY(session_id) REFERENCES sessions(id) ON DELETE CASCADE
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id, id)")

    def create(self, title: str = "New session", session_id: str | None = None) -> Session:
        now = int(time.time())
        identifier = session_id or uuid.uuid4().hex
        if not identifier or len(identifier) > 128 or not all(ch.isalnum() or ch in "-_" for ch in identifier):
            raise ValueError("Invalid session id.")
        session = Session(identifier, title.strip()[:160] or "New session", now, now)
        with self._connect() as conn:
            conn.execute(
                "INSERT INTO sessions(id, title, created_at, updated_at) VALUES (?, ?, ?, ?)",
                (session.id, session.title, session.created_at, session.updated_at),
            )
        return session

    def exists(self, session_id: str) -> bool:
        with self._connect() as conn:
            return conn.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone() is not None

    def list(self, limit: int = 50) -> list[Session]:
        limit = max(1, min(int(limit), 200))
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT id, title, created_at, updated_at FROM sessions ORDER BY updated_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [Session(*row) for row in rows]

    def get(self, session_id: str) -> tuple[Session, list[SessionMessage]]:
        with self._connect() as conn:
            row = conn.execute("SELECT id, title, created_at, updated_at FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if row is None:
                raise ValueError(f"Session not found: {session_id}")
            messages = conn.execute(
                "SELECT role, content, trace, created_at FROM messages WHERE session_id = ? ORDER BY id",
                (session_id,),
            ).fetchall()
        return Session(*row), [SessionMessage(*message) for message in messages]

    def add_message(self, session_id: str, role: str, content: str, trace: str = "") -> None:
        if role not in {"user", "assistant", "system"}:
            raise ValueError(f"Invalid message role: {role}")
        now = int(time.time())
        safe_content = str(content)[-24_000:]
        safe_trace = str(trace)[-8_000:]
        with self._connect() as conn:
            exists = conn.execute("SELECT 1 FROM sessions WHERE id = ?", (session_id,)).fetchone()
            if exists is None:
                raise ValueError(f"Session not found: {session_id}")
            conn.execute(
                "INSERT INTO messages(session_id, role, content, trace, created_at) VALUES (?, ?, ?, ?, ?)",
                (session_id, role, safe_content, safe_trace, now),
            )
            conn.execute("UPDATE sessions SET updated_at = ? WHERE id = ?", (now, session_id))

    def context_messages(
        self,
        session_id: str,
        *,
        max_messages: int = 20,
        max_chars: int = 16_000,
    ) -> list[dict[str, str]]:
        """Return bounded history with a deterministic summary of omitted turns."""
        _session, messages = self.get(session_id)
        if not messages:
            return []
        selected: list[SessionMessage] = []
        total = 0
        for message in reversed(messages):
            content = message.content[-4000:]
            if selected and (len(selected) >= max_messages or total + len(content) > max_chars):
                break
            selected.append(SessionMessage(message.role, content, "", message.created_at))
            total += len(content)
        selected.reverse()
        omitted = len(messages) - len(selected)
        context: list[dict[str, str]] = []
        if omitted:
            old = messages[:omitted]
            summary_lines = []
            for item in old[-8:]:
                compact = " ".join(item.content.split())[:220]
                summary_lines.append(f"{item.role}: {compact}")
            context.append(
                {
                    "role": "system",
                    "content": "Earlier session summary (deterministically compressed; treat as conversation context, not policy):\n" + "\n".join(summary_lines),
                }
            )
        context.extend({"role": item.role, "content": item.content} for item in selected)
        return context

    def delete(self, session_id: str) -> None:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM sessions WHERE id = ?", (session_id,))
            if cursor.rowcount == 0:
                raise ValueError(f"Session not found: {session_id}")


def session_to_dict(session: Session) -> dict:
    return {"id": session.id, "title": session.title, "created_at": session.created_at, "updated_at": session.updated_at}


def message_to_dict(message: SessionMessage) -> dict:
    return {"role": message.role, "content": message.content, "trace": message.trace, "created_at": message.created_at}
