from __future__ import annotations

import ast
import re
import sqlite3
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .file_safety import FileSafetyError, ensure_text_file_safe, resolve_workspace_path


CODE_SUFFIXES = {".py", ".js", ".jsx", ".ts", ".tsx", ".v", ".sv", ".svh"}
SKIP_DIRS = {".git", ".mind01", ".pycache", "__pycache__", "node_modules", "dist", "build", ".venv", "venv"}


@dataclass
class SymbolHit:
    name: str
    kind: str
    path: str
    line: int
    signature: str


@dataclass
class FileSummary:
    path: str
    language: str
    imports: list[str]
    symbols: list[SymbolHit]


class CodeIndex:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.db_path = self.workspace / ".mind01" / "code_index.sqlite3"
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
                CREATE TABLE IF NOT EXISTS files (
                    path TEXT PRIMARY KEY,
                    language TEXT NOT NULL,
                    mtime REAL NOT NULL,
                    indexed_at INTEGER NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS symbols (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    kind TEXT NOT NULL,
                    path TEXT NOT NULL,
                    line INTEGER NOT NULL,
                    signature TEXT NOT NULL
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS imports (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    path TEXT NOT NULL,
                    imported TEXT NOT NULL
                )
                """
            )
            conn.execute("CREATE INDEX IF NOT EXISTS idx_symbols_name ON symbols(name)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_symbols_path ON symbols(path)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_imports_path ON imports(path)")

    def index_path(self, path: Path | None = None) -> int:
        try:
            root = resolve_workspace_path(self.workspace, str(path or "."))
        except FileSafetyError as exc:
            raise ValueError(str(exc)) from exc

        files = list(iter_code_files(root))
        indexed = 0
        with self._connect() as conn:
            for file_path in files:
                rel = str(file_path.relative_to(self.workspace))
                try:
                    ensure_text_file_safe(self.workspace, file_path, rel)
                    text = file_path.read_text(encoding="utf-8")
                except (OSError, FileSafetyError):
                    continue
                language = language_for(file_path)
                symbols, imports = parse_code_file(file_path, text)
                conn.execute("DELETE FROM files WHERE path = ?", (rel,))
                conn.execute("DELETE FROM symbols WHERE path = ?", (rel,))
                conn.execute("DELETE FROM imports WHERE path = ?", (rel,))
                conn.execute(
                    "INSERT INTO files(path, language, mtime, indexed_at) VALUES (?, ?, ?, ?)",
                    (rel, language, file_path.stat().st_mtime, int(time.time())),
                )
                for symbol in symbols:
                    conn.execute(
                        """
                        INSERT INTO symbols(name, kind, path, line, signature)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (symbol.name, symbol.kind, rel, symbol.line, symbol.signature),
                    )
                for imported in imports:
                    conn.execute(
                        "INSERT INTO imports(path, imported) VALUES (?, ?)",
                        (rel, imported),
                    )
                indexed += 1
        return indexed

    def search_symbols(self, query: str, limit: int = 20) -> list[SymbolHit]:
        pattern = f"%{query.strip()}%"
        with self._connect() as conn:
            rows = conn.execute(
                """
                SELECT name, kind, path, line, signature
                FROM symbols
                WHERE name LIKE ? OR signature LIKE ? OR path LIKE ?
                ORDER BY
                  CASE WHEN name = ? THEN 0
                       WHEN name LIKE ? THEN 1
                       ELSE 2 END,
                  path,
                  line
                LIMIT ?
                """,
                (pattern, pattern, pattern, query, f"{query}%", limit),
            ).fetchall()
        hits = [SymbolHit(*row) for row in rows]
        if hits:
            return hits
        return self._search_workspace_symbols(query, limit=limit)

    def _search_workspace_symbols(self, query: str, *, limit: int) -> list[SymbolHit]:
        """Search source directly when no persistent index has been built.

        Symbol inspection is a read operation. Requiring callers to run the
        runtime-mutating ``index_code`` action first made a fresh workspace
        unable to satisfy an otherwise valid read-only route. This bounded
        fallback parses source in memory and deliberately does not persist it.
        """

        needle = query.strip().casefold()
        if not needle or limit < 1:
            return []
        hits: list[SymbolHit] = []
        for file_path in iter_code_files(self.workspace):
            rel = str(file_path.relative_to(self.workspace))
            try:
                ensure_text_file_safe(self.workspace, file_path, rel)
                text = file_path.read_text(encoding="utf-8")
            except (OSError, FileSafetyError):
                continue
            symbols, _ = parse_code_file(file_path, text)
            for symbol in symbols:
                searchable = (symbol.name, symbol.signature, rel)
                if any(needle in item.casefold() for item in searchable):
                    hits.append(
                        SymbolHit(
                            name=symbol.name,
                            kind=symbol.kind,
                            path=rel,
                            line=symbol.line,
                            signature=symbol.signature,
                        )
                    )
        hits.sort(
            key=lambda item: (
                0 if item.name.casefold() == needle else 1 if item.name.casefold().startswith(needle) else 2,
                item.path,
                item.line,
            )
        )
        return hits[:limit]

    def file_summary(self, raw_path: str) -> FileSummary:
        path = raw_path.strip()
        with self._connect() as conn:
            file_row = conn.execute(
                "SELECT path, language FROM files WHERE path = ?",
                (path,),
            ).fetchone()
            if file_row is None:
                raise ValueError(f"File is not indexed: {path}")
            symbol_rows = conn.execute(
                """
                SELECT name, kind, path, line, signature
                FROM symbols
                WHERE path = ?
                ORDER BY line
                """,
                (path,),
            ).fetchall()
            import_rows = conn.execute(
                "SELECT imported FROM imports WHERE path = ? ORDER BY imported",
                (path,),
            ).fetchall()
        return FileSummary(
            path=file_row[0],
            language=file_row[1],
            imports=[row[0] for row in import_rows],
            symbols=[SymbolHit(*row) for row in symbol_rows],
        )

    def stats(self) -> tuple[int, int]:
        with self._connect() as conn:
            files = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
            symbols = conn.execute("SELECT COUNT(*) FROM symbols").fetchone()[0]
        return int(files), int(symbols)

    def stale_files(self) -> list[str]:
        stale: list[str] = []
        with self._connect() as conn:
            rows = conn.execute("SELECT path, mtime FROM files").fetchall()
        for rel, indexed_mtime in rows:
            path = self.workspace / rel
            if not path.exists():
                stale.append(rel)
                continue
            try:
                if path.stat().st_mtime != indexed_mtime:
                    stale.append(rel)
            except OSError:
                stale.append(rel)
        return sorted(stale)


def iter_code_files(root: Path) -> Iterable[Path]:
    items = root.rglob("*") if root.is_dir() else [root]
    for item in sorted(items):
        if any(part in SKIP_DIRS for part in item.parts):
            continue
        if item.is_file() and item.suffix.lower() in CODE_SUFFIXES:
            yield item


def language_for(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".py":
        return "python"
    if suffix in {".js", ".jsx"}:
        return "javascript"
    if suffix in {".ts", ".tsx"}:
        return "typescript"
    if suffix in {".v", ".sv", ".svh"}:
        return "verilog"
    return suffix.lstrip(".") or "text"


def parse_code_file(path: Path, text: str) -> tuple[list[SymbolHit], list[str]]:
    if path.suffix.lower() == ".py":
        return parse_python(path, text)
    return parse_lightweight(path, text)


def parse_python(path: Path, text: str) -> tuple[list[SymbolHit], list[str]]:
    symbols: list[SymbolHit] = []
    imports: list[str] = []
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return symbols, imports
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            symbols.append(
                SymbolHit(
                    name=node.name,
                    kind="function",
                    path=str(path),
                    line=node.lineno,
                    signature=python_signature(node),
                )
            )
        elif isinstance(node, ast.ClassDef):
            symbols.append(
                SymbolHit(
                    name=node.name,
                    kind="class",
                    path=str(path),
                    line=node.lineno,
                    signature=f"class {node.name}",
                )
            )
        elif isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            module = node.module or ""
            imports.append("." * node.level + module)
    return symbols, sorted(set(imports))


def python_signature(node: ast.FunctionDef | ast.AsyncFunctionDef) -> str:
    args = [arg.arg for arg in node.args.posonlyargs + node.args.args]
    if node.args.vararg:
        args.append("*" + node.args.vararg.arg)
    args.extend(arg.arg for arg in node.args.kwonlyargs)
    if node.args.kwarg:
        args.append("**" + node.args.kwarg.arg)
    prefix = "async def" if isinstance(node, ast.AsyncFunctionDef) else "def"
    return f"{prefix} {node.name}({', '.join(args)})"


LIGHTWEIGHT_PATTERNS = [
    ("function", re.compile(r"^\s*(?:export\s+)?(?:async\s+)?function\s+([A-Za-z_$][\w$]*)\s*\(([^)]*)\)", re.MULTILINE)),
    ("class", re.compile(r"^\s*(?:export\s+)?class\s+([A-Za-z_$][\w$]*)", re.MULTILINE)),
    ("function", re.compile(r"^\s*(?:export\s+)?(?:const|let|var)\s+([A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\(([^)]*)\)\s*=>", re.MULTILINE)),
    ("module", re.compile(r"^\s*module\s+([A-Za-z_][\w$]*)", re.MULTILINE)),
]
IMPORT_RE = re.compile(r"^\s*(?:import\s+.*?from\s+['\"]([^'\"]+)['\"]|import\s+['\"]([^'\"]+)['\"]|`include\s+\"([^\"]+)\")", re.MULTILINE)


def parse_lightweight(path: Path, text: str) -> tuple[list[SymbolHit], list[str]]:
    symbols: list[SymbolHit] = []
    for kind, pattern in LIGHTWEIGHT_PATTERNS:
        for match in pattern.finditer(text):
            name = match.group(1)
            signature = match.group(0).strip()
            line = text.count("\n", 0, match.start()) + 1
            symbols.append(SymbolHit(name=name, kind=kind, path=str(path), line=line, signature=signature[:240]))
    imports = []
    for match in IMPORT_RE.finditer(text):
        imports.extend(group for group in match.groups() if group)
    return symbols, sorted(set(imports))


def render_symbol_hits(hits: list[SymbolHit]) -> str:
    if not hits:
        return "(no symbols)"
    return "\n".join(
        f"{hit.path}:{hit.line}: {hit.kind} {hit.name} - {hit.signature}"
        for hit in hits
    )


def render_file_summary(summary: FileSummary) -> str:
    lines = [f"{summary.path} [{summary.language}]"]
    lines.append("imports:")
    lines.extend(f"- {item}" for item in summary.imports or ["(none)"])
    lines.append("symbols:")
    lines.extend(
        f"- {item.line}: {item.kind} {item.name} - {item.signature}"
        for item in summary.symbols
    )
    if not summary.symbols:
        lines.append("- (none)")
    return "\n".join(lines)
