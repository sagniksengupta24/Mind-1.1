from __future__ import annotations

import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import List, Protocol

from .embeddings import cosine_similarity, pack_vector, unpack_vector
from .security import redact_secrets


@dataclass
class MemoryHit:
    id: int
    key: str
    value: str
    tags: str
    created_at: int
    updated_at: int
    source: str
    importance: int
    last_used_at: int
    use_count: int
    embedding_model: str = ""
    score: float = 0.0
    lexical_score: int = 0
    vector_score: float = 0.0

    @property
    def memory_id(self) -> int:
        return self.id

    @property
    def text(self) -> str:
        return self.value


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]:
        ...


class MemoryStore:
    def __init__(self, workspace: Path) -> None:
        self.db_path = workspace / ".mind01" / "memory.sqlite3"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5.0)
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL,
                    value TEXT NOT NULL,
                    tags TEXT NOT NULL DEFAULT '',
                    created_at INTEGER NOT NULL,
                    updated_at INTEGER NOT NULL DEFAULT 0,
                    source TEXT NOT NULL DEFAULT 'user',
                    importance INTEGER NOT NULL DEFAULT 1,
                    last_used_at INTEGER NOT NULL DEFAULT 0,
                    use_count INTEGER NOT NULL DEFAULT 0,
                    embedding TEXT NOT NULL DEFAULT '',
                    embedding_model TEXT NOT NULL DEFAULT ''
                )
                """
            )
            self._migrate_db(conn)
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_key ON memories(key)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_tags ON memories(tags)"
            )
            conn.execute(
                "CREATE INDEX IF NOT EXISTS idx_memories_updated ON memories(updated_at)"
            )

    def _migrate_db(self, conn: sqlite3.Connection) -> None:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(memories)").fetchall()}
        additions = {
            "updated_at": "ALTER TABLE memories ADD COLUMN updated_at INTEGER NOT NULL DEFAULT 0",
            "source": "ALTER TABLE memories ADD COLUMN source TEXT NOT NULL DEFAULT 'user'",
            "importance": "ALTER TABLE memories ADD COLUMN importance INTEGER NOT NULL DEFAULT 1",
            "last_used_at": "ALTER TABLE memories ADD COLUMN last_used_at INTEGER NOT NULL DEFAULT 0",
            "use_count": "ALTER TABLE memories ADD COLUMN use_count INTEGER NOT NULL DEFAULT 0",
            "embedding": "ALTER TABLE memories ADD COLUMN embedding TEXT NOT NULL DEFAULT ''",
            "embedding_model": "ALTER TABLE memories ADD COLUMN embedding_model TEXT NOT NULL DEFAULT ''",
        }
        for column, statement in additions.items():
            if column not in columns:
                conn.execute(statement)
        conn.execute("UPDATE memories SET updated_at = created_at WHERE updated_at = 0")

    def remember(
        self,
        key: str,
        value: str,
        tags: str = "",
        source: str = "user",
        importance: int = 1,
        embedder: Embedder | None = None,
        embedding_model: str = "",
    ) -> str:
        key = clean_text(key)
        value = clean_text(value)
        tags = normalize_tags(tags)
        source = clean_text(source or "user")
        importance = normalize_importance(importance)
        if not key:
            raise ValueError("Memory key cannot be empty.")
        if not value:
            raise ValueError("Memory value cannot be empty.")
        embedding = make_embedding(embedder, value, embedding_model)
        now = int(time.time())
        with self._connect() as conn:
            existing = conn.execute(
                """
                SELECT id FROM memories
                WHERE key = ? AND value = ? AND tags = ?
                LIMIT 1
                """,
                (key, value, tags),
            ).fetchone()
            if existing is not None:
                return f"Memory `{key}` already exists."
            conn.execute(
                """
                INSERT INTO memories(
                    key, value, tags, created_at, updated_at, source,
                    importance, last_used_at, use_count, embedding, embedding_model
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    key,
                    value,
                    tags,
                    now,
                    now,
                    source,
                    importance,
                    0,
                    0,
                    embedding,
                    embedding_model if embedding else "",
                ),
            )
        return f"Remembered `{key}`."

    def recall(
        self,
        query: str,
        limit: int = 8,
        tags: str = "",
        embedder: Embedder | None = None,
        embedding_model: str = "",
        record_use: bool = False,
    ) -> List[MemoryHit]:
        query = query.strip()
        tag_filter = parse_tags(tags)
        query_vector = embedder.embed(query) if embedder is not None and query else []
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, key, value, tags, created_at, updated_at, source,
                       importance, last_used_at, use_count, embedding, embedding_model
                FROM memories
                ORDER BY updated_at DESC, id DESC
                LIMIT 500
                """
            ).fetchall()
            hits = rank_memory_rows(rows, query, tag_filter, query_vector, embedding_model)
            selected = hits[: max(0, int(limit))]
            if record_use and selected:
                now = int(time.time())
                ids = [hit.id for hit in selected]
                conn.executemany(
                    """
                    UPDATE memories
                    SET use_count = use_count + 1, last_used_at = ?
                    WHERE id = ?
                    """,
                    [(now, memory_id) for memory_id in ids],
                )
        return selected

    def list(self, limit: int = 50, tags: str = "") -> List[MemoryHit]:
        tag_filter = parse_tags(tags)
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT id, key, value, tags, created_at, updated_at, source,
                       importance, last_used_at, use_count, embedding, embedding_model
                FROM memories
                ORDER BY updated_at DESC, id DESC
                LIMIT 500
                """,
            ).fetchall()
        hits = [row_to_hit(row) for row in rows]
        if tag_filter:
            hits = [hit for hit in hits if tags_match(hit.tags, tag_filter)]
        return hits[: max(0, int(limit))]

    def update(
        self,
        memory_id: int,
        value: str,
        tags: str | None = None,
        source: str | None = None,
        importance: int | None = None,
        embedder: Embedder | None = None,
        embedding_model: str = "",
    ) -> str:
        value = clean_text(value)
        if not value:
            raise ValueError("Memory value cannot be empty.")
        now = int(time.time())
        updates = ["value = ?", "updated_at = ?"]
        params: list[object] = [value, now]
        if tags is not None:
            updates.append("tags = ?")
            params.append(normalize_tags(tags))
        if source is not None:
            updates.append("source = ?")
            params.append(clean_text(source or "user"))
        if importance is not None:
            updates.append("importance = ?")
            params.append(normalize_importance(importance))
        embedding = make_embedding(embedder, value, embedding_model)
        if embedder is not None:
            updates.append("embedding = ?")
            updates.append("embedding_model = ?")
            params.extend([embedding, embedding_model if embedding else ""])
        params.append(memory_id)
        with self._connect() as conn:
            cursor = conn.execute(
                f"UPDATE memories SET {', '.join(updates)} WHERE id = ?",
                params,
            )
        if cursor.rowcount == 0:
            raise ValueError(f"Memory not found: {memory_id}")
        return f"Updated memory {memory_id}."

    def delete(self, memory_id: int) -> str:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM memories WHERE id = ?", (memory_id,))
        if cursor.rowcount == 0:
            raise ValueError(f"Memory not found: {memory_id}")
        return f"Deleted memory {memory_id}."


def row_to_hit(row: tuple, score: float = 0.0, lexical_score: int = 0, vector_score: float = 0.0) -> MemoryHit:
    return MemoryHit(
        id=int(row[0]),
        key=str(row[1]),
        value=str(row[2]),
        tags=str(row[3]),
        created_at=int(row[4]),
        updated_at=int(row[5]),
        source=str(row[6]),
        importance=int(row[7]),
        last_used_at=int(row[8]),
        use_count=int(row[9]),
        embedding_model=str(row[11]),
        score=score,
        lexical_score=lexical_score,
        vector_score=vector_score,
    )


def rank_memory_rows(
    rows: list[tuple],
    query: str,
    tag_filter: list[str],
    query_vector: list[float],
    embedding_model: str,
) -> list[MemoryHit]:
    hits = []
    for row in rows:
        tags = str(row[3])
        if tag_filter and not tags_match(tags, tag_filter):
            continue
        lexical = lexical_score(str(row[1]), str(row[2]), tags, query)
        vector = 0.0
        stored_model = str(row[11])
        if query_vector and row[10] and (not embedding_model or stored_model == embedding_model):
            vector = cosine_similarity(query_vector, unpack_vector(str(row[10])))
        if query and lexical <= 0 and vector <= 0.0:
            continue
        importance = int(row[7])
        use_count = int(row[9])
        score = float(lexical + (importance * 10) + (use_count * 3) + int(max(vector, 0.0) * 100))
        hits.append(row_to_hit(row, score=score, lexical_score=lexical, vector_score=vector))
    hits.sort(key=lambda hit: (-hit.score, -hit.updated_at, -hit.id))
    return hits


def lexical_score(key: str, value: str, tags: str, query: str) -> int:
    terms = [term.lower() for term in query.split() if term]
    if not terms:
        return 0
    haystacks = {
        key.lower(): 8,
        tags.lower(): 6,
        value.lower(): 4,
    }
    score = 0
    for term in terms:
        for text, weight in haystacks.items():
            score += text.count(term) * weight
    return score


def clean_text(text: str) -> str:
    return redact_secrets(str(text).strip())


def normalize_tags(tags: str) -> str:
    parsed = parse_tags(tags)
    return ",".join(parsed)


def parse_tags(tags: str) -> list[str]:
    seen = set()
    parsed = []
    for raw in str(tags).split(","):
        tag = raw.strip().lower()
        if not tag or tag in seen:
            continue
        seen.add(tag)
        parsed.append(tag)
    return parsed


def tags_match(tags: str, required: list[str]) -> bool:
    available = set(parse_tags(tags))
    return all(tag in available for tag in required)


def normalize_importance(value: int) -> int:
    try:
        importance = int(value)
    except (TypeError, ValueError) as exc:
        raise ValueError("Memory importance must be an integer.") from exc
    if importance < 0 or importance > 10:
        raise ValueError("Memory importance must be between 0 and 10.")
    return importance


def make_embedding(
    embedder: Embedder | None,
    text: str,
    embedding_model: str,
) -> str:
    if embedder is None:
        return ""
    vector = embedder.embed(text)
    return pack_vector(vector) if vector else ""
