from __future__ import annotations

import hashlib
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Protocol

from .embeddings import cosine_similarity, pack_vector, unpack_vector
from .file_safety import FileSafetyError, ensure_text_file_safe


TEXT_SUFFIXES = {".txt", ".md", ".rst", ".py", ".v", ".sv", ".svh", ".vh"}


@dataclass
class DocHit:
    path: str
    chunk: str
    score: int = 0
    lexical_score: int = 0
    vector_score: float = 0.0
    embedding_model: str = ""
    line_start: int = 1
    line_end: int = 1
    chunk_sha256: str = ""
    file_mtime_ns: int = 0
    stale: bool = False
    rank: float = 0.0

    @property
    def citation(self) -> str:
        return f"{self.path}:L{self.line_start}-L{self.line_end}"


@dataclass
class StaleDocFile:
    path: str
    reason: str


class Embedder(Protocol):
    def embed(self, text: str) -> list[float]:
        ...


class DocStore:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.db_path = self.workspace / ".mind01" / "docs.sqlite3"
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.fts_enabled = False
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
                CREATE TABLE IF NOT EXISTS doc_chunks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    chunk TEXT NOT NULL,
                    embedding TEXT NOT NULL DEFAULT '',
                    embedding_model TEXT NOT NULL DEFAULT ''
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS doc_files (
                    path TEXT PRIMARY KEY,
                    mtime_ns INTEGER NOT NULL,
                    size INTEGER NOT NULL,
                    sha256 TEXT NOT NULL,
                    indexed_at_ns INTEGER NOT NULL
                )
                """
            )
            self._migrate_db(conn)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_doc_path ON doc_chunks(path)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_doc_embedding_model ON doc_chunks(embedding_model)")
            self.fts_enabled = self._init_fts(conn)

    def _migrate_db(self, conn: sqlite3.Connection) -> None:
        columns = {row[1] for row in conn.execute("PRAGMA table_info(doc_chunks)").fetchall()}
        if "embedding" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN embedding TEXT NOT NULL DEFAULT ''")
        if "embedding_model" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN embedding_model TEXT NOT NULL DEFAULT ''")
        if "line_start" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN line_start INTEGER NOT NULL DEFAULT 1")
        if "line_end" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN line_end INTEGER NOT NULL DEFAULT 1")
        if "chunk_sha256" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN chunk_sha256 TEXT NOT NULL DEFAULT ''")
        if "file_mtime_ns" not in columns:
            conn.execute("ALTER TABLE doc_chunks ADD COLUMN file_mtime_ns INTEGER NOT NULL DEFAULT 0")

    def _init_fts(self, conn: sqlite3.Connection) -> bool:
        try:
            conn.execute(
                """
                CREATE VIRTUAL TABLE IF NOT EXISTS doc_chunks_fts
                USING fts5(path UNINDEXED, chunk, chunk_id UNINDEXED)
                """
            )
        except sqlite3.OperationalError:
            return False
        return True

    def index_path(
        self,
        path: Path,
        embedder: Embedder | None = None,
        embedding_model: str = "",
    ) -> int:
        root = path.expanduser().resolve()
        files = list(self._iter_files(root))
        count = 0
        with self._connect() as conn:
            for file_path in files:
                rel = self._display_path(file_path)
                if self.fts_enabled:
                    conn.execute("DELETE FROM doc_chunks_fts WHERE path = ?", (rel,))
                conn.execute("DELETE FROM doc_chunks WHERE path = ?", (rel,))
                try:
                    ensure_text_file_safe(self.workspace, file_path, rel)
                    raw = file_path.read_bytes()
                except (OSError, FileSafetyError):
                    continue
                text = raw.decode("utf-8", errors="ignore")
                stat = file_path.stat()
                file_mtime_ns = int(stat.st_mtime_ns)
                for chunk in chunk_text_with_lines(text):
                    embedding = ""
                    stored_model = ""
                    if embedder is not None:
                        vector = embedder.embed(chunk.text)
                        embedding = pack_vector(vector) if vector else ""
                        stored_model = embedding_model
                    cursor = conn.execute(
                        """
                        INSERT INTO doc_chunks(
                            path, chunk, embedding, embedding_model,
                            line_start, line_end, chunk_sha256, file_mtime_ns
                        )
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        """,
                        (
                            rel,
                            chunk.text,
                            embedding,
                            stored_model,
                            chunk.line_start,
                            chunk.line_end,
                            hashlib.sha256(chunk.text.encode("utf-8")).hexdigest(),
                            file_mtime_ns,
                        ),
                    )
                    if self.fts_enabled:
                        conn.execute(
                            """
                            INSERT INTO doc_chunks_fts(path, chunk, chunk_id)
                            VALUES (?, ?, ?)
                            """,
                            (rel, chunk.text, int(cursor.lastrowid)),
                        )
                    count += 1
                conn.execute(
                    """
                    INSERT INTO doc_files(path, mtime_ns, size, sha256, indexed_at_ns)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT(path) DO UPDATE SET
                        mtime_ns = excluded.mtime_ns,
                        size = excluded.size,
                        sha256 = excluded.sha256,
                        indexed_at_ns = excluded.indexed_at_ns
                    """,
                    (
                        rel,
                        int(stat.st_mtime_ns),
                        int(stat.st_size),
                        hashlib.sha256(raw).hexdigest(),
                        time.time_ns(),
                    ),
                )
        return count

    def search(
        self,
        query: str,
        limit: int = 6,
        embedder: Embedder | None = None,
        embedding_model: str = "",
    ) -> List[DocHit]:
        terms = [term for term in query.split() if term]
        if not terms:
            return []
        query_vector = embedder.embed(query) if embedder is not None else []
        rows = self._candidate_rows(terms, limit, bool(query_vector), embedding_model)
        stale_paths = {item.path for item in self.stale_files()}
        hits = []
        for row in rows:
            lexical_score = score_chunk(row["path"], row["chunk"], terms)
            vector_score = 0.0
            if query_vector and row["embedding"]:
                vector_score = cosine_similarity(query_vector, unpack_vector(row["embedding"]))
            rank_bonus = int(max(0.0, -float(row["rank"])) * 1000)
            score = lexical_score + int(max(vector_score, 0.0) * 100) + rank_bonus
            hits.append(
                DocHit(
                    path=row["path"],
                    chunk=row["chunk"],
                    score=score,
                    lexical_score=lexical_score,
                    vector_score=vector_score,
                    embedding_model=row["embedding_model"],
                    line_start=int(row["line_start"]),
                    line_end=int(row["line_end"]),
                    chunk_sha256=row["chunk_sha256"],
                    file_mtime_ns=int(row["file_mtime_ns"]),
                    stale=row["path"] in stale_paths,
                    rank=float(row["rank"]),
                )
            )
        hits = [hit for hit in hits if hit.lexical_score > 0 or hit.vector_score > 0.0]
        hits.sort(key=lambda hit: (-hit.score, -hit.vector_score, hit.path))
        return hits[:limit]

    def stats(self) -> dict[str, int]:
        with self._connect() as conn:
            chunks = conn.execute("SELECT COUNT(*) FROM doc_chunks").fetchone()[0]
            embedded = conn.execute(
                "SELECT COUNT(*) FROM doc_chunks WHERE embedding != ''"
            ).fetchone()[0]
            files = conn.execute("SELECT COUNT(DISTINCT path) FROM doc_chunks").fetchone()[0]
        return {
            "chunks": int(chunks),
            "embedded_chunks": int(embedded),
            "files": int(files),
            "stale_files": len(self.stale_files()),
        }

    def stale_files(self) -> list[StaleDocFile]:
        stale = []
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT path, mtime_ns, size, sha256 FROM doc_files ORDER BY path"
            ).fetchall()
        for row in rows:
            rel_path = str(row[0])
            file_path = (self.workspace / rel_path).resolve()
            if self.workspace != file_path and self.workspace not in file_path.parents:
                stale.append(StaleDocFile(rel_path, "path escapes workspace"))
                continue
            if not file_path.exists():
                stale.append(StaleDocFile(rel_path, "deleted"))
                continue
            try:
                stat = file_path.stat()
            except OSError:
                stale.append(StaleDocFile(rel_path, "unreadable"))
                continue
            if int(stat.st_size) != int(row[2]) or int(stat.st_mtime_ns) != int(row[1]):
                try:
                    current_hash = hashlib.sha256(file_path.read_bytes()).hexdigest()
                except OSError:
                    stale.append(StaleDocFile(rel_path, "unreadable"))
                    continue
                if current_hash != str(row[3]):
                    stale.append(StaleDocFile(rel_path, "changed"))
        return stale

    def _candidate_rows(
        self,
        terms: list[str],
        limit: int,
        include_embeddings: bool,
        embedding_model: str = "",
    ) -> list[dict[str, object]]:
        with self._connect() as conn:
            keyword_rows = self._fts_rows(conn, terms, limit)
            if not keyword_rows:
                keyword_rows = self._keyword_rows(conn, terms, limit)
            if not include_embeddings:
                return keyword_rows
            model_clause = "AND embedding_model = ?" if embedding_model else ""
            model_params = [embedding_model] if embedding_model else []
            embedding_rows = [
                row_to_dict(row)
                for row in conn.execute(
                f"""
                SELECT
                    path, chunk, embedding, embedding_model,
                    line_start, line_end, chunk_sha256, file_mtime_ns,
                    0.0 AS rank
                FROM doc_chunks
                WHERE embedding != '' {model_clause}
                LIMIT ?
                """,
                model_params + [max(limit * 50, 500)],
                ).fetchall()
            ]

        seen = set()
        rows = []
        for row in keyword_rows + embedding_rows:
            key = (row["path"], row["chunk_sha256"])
            if key in seen:
                continue
            seen.add(key)
            rows.append(row)
        return rows

    def _fts_rows(
        self,
        conn: sqlite3.Connection,
        terms: list[str],
        limit: int,
    ) -> list[dict[str, object]]:
        if not self.fts_enabled:
            return []
        query = build_fts_query(terms)
        if not query:
            return []
        try:
            rows = conn.execute(
                """
                SELECT
                    c.path, c.chunk, c.embedding, c.embedding_model,
                    c.line_start, c.line_end, c.chunk_sha256, c.file_mtime_ns,
                    f.rank AS rank
                FROM doc_chunks_fts f
                JOIN doc_chunks c ON c.id = f.chunk_id
                WHERE doc_chunks_fts MATCH ?
                ORDER BY f.rank
                LIMIT ?
                """,
                (query, max(limit * 8, limit)),
            ).fetchall()
        except sqlite3.OperationalError:
            return []
        return [row_to_dict(row) for row in rows]

    def _keyword_rows(
        self,
        conn: sqlite3.Connection,
        terms: list[str],
        limit: int,
    ) -> list[dict[str, object]]:
        where = " OR ".join(["chunk LIKE ? OR path LIKE ?" for _ in terms])
        if not where:
            return []
        params: list[str] = []
        for term in terms:
            like = f"%{term}%"
            params.extend([like, like])
        rows = conn.execute(
            f"""
            SELECT
                path, chunk, embedding, embedding_model,
                line_start, line_end, chunk_sha256, file_mtime_ns,
                0.0 AS rank
            FROM doc_chunks
            WHERE {where}
            LIMIT ?
            """,
            params + [max(limit * 8, limit)],
        ).fetchall()
        return [row_to_dict(row) for row in rows]

    def _iter_files(self, root: Path) -> Iterable[Path]:
        if root.is_file():
            if root.suffix.lower() in TEXT_SUFFIXES:
                yield root
            return
        for item in root.rglob("*"):
            if ".mind01" in item.parts:
                continue
            if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES:
                yield item

    def _display_path(self, path: Path) -> str:
        try:
            return str(path.relative_to(self.workspace))
        except ValueError:
            return str(path)


def chunk_text(text: str, size: int = 1200, overlap: int = 150) -> list[str]:
    clean = text.replace("\r\n", "\n")
    chunks = []
    start = 0
    while start < len(clean):
        end = min(start + size, len(clean))
        chunk = clean[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(clean):
            break
        start = max(end - overlap, start + 1)
    return chunks


@dataclass(frozen=True)
class TextChunk:
    text: str
    line_start: int
    line_end: int


def chunk_text_with_lines(text: str, size: int = 1200, overlap_lines: int = 2) -> list[TextChunk]:
    clean = text.replace("\r\n", "\n")
    lines = clean.splitlines()
    if not lines and clean:
        lines = [clean]
    chunks: list[TextChunk] = []
    start = 0
    while start < len(lines):
        current: list[str] = []
        char_count = 0
        index = start
        while index < len(lines):
            line = lines[index]
            next_count = char_count + len(line) + (1 if current else 0)
            if current and next_count > size:
                break
            current.append(line)
            char_count = next_count
            index += 1
            if char_count >= size:
                break
        if not current:
            current.append(lines[start])
            index = start + 1
        chunk = "\n".join(current).strip()
        if chunk:
            chunks.append(TextChunk(chunk, start + 1, index))
        if index >= len(lines):
            break
        start = max(index - overlap_lines, start + 1)
    return chunks


def score_chunk(path: str, chunk: str, terms: list[str]) -> int:
    path_lower = path.lower()
    chunk_lower = chunk.lower()
    score = 0
    for term in terms:
        lowered = term.lower()
        score += chunk_lower.count(lowered) * 5
        score += path_lower.count(lowered) * 3
        if lowered in path_lower:
            score += 2
    return score


def build_fts_query(terms: list[str]) -> str:
    safe_terms = []
    for term in terms:
        cleaned = "".join(ch for ch in term if ch.isalnum() or ch in {"_", "-"}).strip("-")
        if cleaned:
            safe_terms.append(f'"{cleaned}"')
    return " OR ".join(safe_terms)


def row_to_dict(row: tuple) -> dict[str, object]:
    return {
        "path": str(row[0]),
        "chunk": str(row[1]),
        "embedding": str(row[2]),
        "embedding_model": str(row[3]),
        "line_start": int(row[4]),
        "line_end": int(row[5]),
        "chunk_sha256": str(row[6]),
        "file_mtime_ns": int(row[7]),
        "rank": float(row[8]),
    }
