from __future__ import annotations

import hashlib
import json
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path

from .code_index import iter_code_files, language_for, parse_code_file
from .file_safety import FileSafetyError, ensure_text_file_safe, resolve_workspace_path


@dataclass(frozen=True)
class KnowledgeHit:
    entity_id: str
    entity_type: str
    name: str
    path: str
    provenance: str
    metadata: dict


class ProjectKnowledgeStore:
    """Small provenance-aware project graph stored in SQLite.

    This is intentionally not an autonomous memory oracle. Facts are derived
    from files, carry hashes/provenance, and are replaced when source files
    change.
    """

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.db_path = self.workspace / ".mind01" / "project_knowledge.sqlite3"
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
                CREATE TABLE IF NOT EXISTS entities (
                    entity_id TEXT PRIMARY KEY,
                    entity_type TEXT NOT NULL,
                    name TEXT NOT NULL,
                    path TEXT NOT NULL DEFAULT '',
                    source_hash TEXT NOT NULL DEFAULT '',
                    provenance TEXT NOT NULL DEFAULT '',
                    metadata_json TEXT NOT NULL DEFAULT '{}',
                    updated_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS relations (
                    source_id TEXT NOT NULL,
                    predicate TEXT NOT NULL,
                    target_id TEXT NOT NULL,
                    provenance TEXT NOT NULL DEFAULT '',
                    updated_at INTEGER NOT NULL,
                    PRIMARY KEY(source_id, predicate, target_id),
                    FOREIGN KEY(source_id) REFERENCES entities(entity_id) ON DELETE CASCADE,
                    FOREIGN KEY(target_id) REFERENCES entities(entity_id) ON DELETE CASCADE
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_entities_name ON entities(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_entities_path ON entities(path)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_relations_target ON relations(target_id)")

    def refresh(self, raw_path: str = ".") -> dict[str, int]:
        try:
            root = resolve_workspace_path(self.workspace, raw_path)
        except FileSafetyError as exc:
            raise ValueError(str(exc)) from exc
        files = list(iter_code_files(root))
        counts = {"files": 0, "symbols": 0, "imports": 0}
        now = int(time.time())
        with self._connect() as conn:
            for file_path in files:
                rel = str(file_path.relative_to(self.workspace))
                try:
                    ensure_text_file_safe(self.workspace, file_path, rel)
                    text = file_path.read_text(encoding="utf-8")
                except (OSError, FileSafetyError, UnicodeDecodeError):
                    continue
                digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
                file_id = _entity_id("file", rel)
                existing = conn.execute(
                    "SELECT source_hash FROM entities WHERE entity_id = ?", (file_id,)
                ).fetchone()
                if existing and existing[0] == digest:
                    counts["files"] += 1
                    continue
                old_ids = [
                    row[0]
                    for row in conn.execute(
                        "SELECT entity_id FROM entities WHERE path = ? AND entity_type != 'file'", (rel,)
                    ).fetchall()
                ]
                for entity_id in old_ids:
                    conn.execute("DELETE FROM entities WHERE entity_id = ?", (entity_id,))
                conn.execute(
                    """
                    INSERT INTO entities(entity_id, entity_type, name, path, source_hash, provenance, metadata_json, updated_at)
                    VALUES (?, 'file', ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(entity_id) DO UPDATE SET
                        source_hash=excluded.source_hash,
                        provenance=excluded.provenance,
                        metadata_json=excluded.metadata_json,
                        updated_at=excluded.updated_at
                    """,
                    (
                        file_id,
                        file_path.name,
                        rel,
                        digest,
                        rel,
                        json.dumps({"language": language_for(file_path), "size": len(text.encode('utf-8'))}),
                        now,
                    ),
                )
                symbols, imports = parse_code_file(file_path, text)
                for symbol in symbols:
                    symbol_id = _entity_id(symbol.kind, f"{rel}:{symbol.line}:{symbol.name}")
                    conn.execute(
                        "INSERT OR REPLACE INTO entities VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (
                            symbol_id,
                            symbol.kind,
                            symbol.name,
                            rel,
                            digest,
                            f"{rel}:L{symbol.line}",
                            json.dumps({"signature": symbol.signature, "line": symbol.line}),
                            now,
                        ),
                    )
                    conn.execute(
                        "INSERT OR REPLACE INTO relations VALUES (?, 'defines', ?, ?, ?)",
                        (file_id, symbol_id, f"{rel}:L{symbol.line}", now),
                    )
                    counts["symbols"] += 1
                for imported in imports:
                    module_id = _entity_id("module", imported)
                    conn.execute(
                        "INSERT OR IGNORE INTO entities VALUES (?, 'module', ?, '', '', ?, '{}', ?)",
                        (module_id, imported, rel, now),
                    )
                    conn.execute(
                        "INSERT OR REPLACE INTO relations VALUES (?, 'imports', ?, ?, ?)",
                        (file_id, module_id, rel, now),
                    )
                    counts["imports"] += 1
                counts["files"] += 1
        return counts

    def query(self, term: str, limit: int = 20) -> list[KnowledgeHit]:
        query = term.strip()
        if not query:
            return []
        limit = max(1, min(int(limit), 100))
        pattern = f"%{query}%"
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT entity_id, entity_type, name, path, provenance, metadata_json
                FROM entities
                WHERE name LIKE ? OR path LIKE ? OR metadata_json LIKE ?
                ORDER BY CASE WHEN name = ? THEN 0 WHEN name LIKE ? THEN 1 ELSE 2 END, updated_at DESC
                LIMIT ?
                """,
                (pattern, pattern, pattern, query, f"{query}%", limit),
            ).fetchall()
        hits: list[KnowledgeHit] = []
        for row in rows:
            try:
                metadata = json.loads(row[5])
            except json.JSONDecodeError:
                metadata = {}
            hits.append(KnowledgeHit(row[0], row[1], row[2], row[3], row[4], metadata))
        return hits

    def relations_for(self, entity_id: str, limit: int = 50) -> list[dict[str, str]]:
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT r.predicate, r.source_id, s.name, r.target_id, t.name, r.provenance
                FROM relations r
                JOIN entities s ON s.entity_id = r.source_id
                JOIN entities t ON t.entity_id = r.target_id
                WHERE r.source_id = ? OR r.target_id = ?
                LIMIT ?
                """,
                (entity_id, entity_id, max(1, min(limit, 200))),
            ).fetchall()
        return [
            {
                "predicate": row[0],
                "source_id": row[1],
                "source_name": row[2],
                "target_id": row[3],
                "target_name": row[4],
                "provenance": row[5],
            }
            for row in rows
        ]

    def stats(self) -> dict[str, int]:
        with self._connect() as conn:
            entities = int(conn.execute("SELECT COUNT(*) FROM entities").fetchone()[0])
            relations = int(conn.execute("SELECT COUNT(*) FROM relations").fetchone()[0])
        return {"entities": entities, "relations": relations}


def _entity_id(entity_type: str, key: str) -> str:
    digest = hashlib.sha256(f"{entity_type}:{key}".encode("utf-8")).hexdigest()[:24]
    return f"{entity_type}:{digest}"
