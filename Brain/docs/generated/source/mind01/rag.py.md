# `mind01/rag.py`

## File purpose

This sessions memory and RAG file is reviewed at snapshot `059e3927191356440f535b77927e9cc72ba4d1856ece4d3a33b2b7019657f071`. It contains 485 lines.

## Imports and module state

- [mind01/rag.py:1](../../../../mind01/rag.py#L1) imports `__future__` / annotations.
- [mind01/rag.py:3](../../../../mind01/rag.py#L3) imports `hashlib`.
- [mind01/rag.py:4](../../../../mind01/rag.py#L4) imports `sqlite3`.
- [mind01/rag.py:5](../../../../mind01/rag.py#L5) imports `time`.
- [mind01/rag.py:6](../../../../mind01/rag.py#L6) imports `dataclasses` / dataclass.
- [mind01/rag.py:7](../../../../mind01/rag.py#L7) imports `pathlib` / Path.
- [mind01/rag.py:8](../../../../mind01/rag.py#L8) imports `typing` / Iterable.
- [mind01/rag.py:8](../../../../mind01/rag.py#L8) imports `typing` / List.
- [mind01/rag.py:8](../../../../mind01/rag.py#L8) imports `typing` / Protocol.
- [mind01/rag.py:10](../../../../mind01/rag.py#L10) imports `embeddings` / cosine_similarity.
- [mind01/rag.py:10](../../../../mind01/rag.py#L10) imports `embeddings` / pack_vector.
- [mind01/rag.py:10](../../../../mind01/rag.py#L10) imports `embeddings` / unpack_vector.
- [mind01/rag.py:11](../../../../mind01/rag.py#L11) imports `file_safety` / FileSafetyError.
- [mind01/rag.py:11](../../../../mind01/rag.py#L11) imports `file_safety` / ensure_text_file_safe.

## Symbols

### `mind01.rag.TEXT_SUFFIXES` — lines 14–14

- Source: [mind01/rag.py:14](../../../../mind01/rag.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocHit` — lines 18–34

- Source: [mind01/rag.py:18](../../../../mind01/rag.py#L18)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocHit.citation` — lines 33–34

- Source: [mind01/rag.py:33](../../../../mind01/rag.py#L33)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.StaleDocFile` — lines 38–40

- Source: [mind01/rag.py:38](../../../../mind01/rag.py#L38)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.Embedder` — lines 43–45

- Source: [mind01/rag.py:43](../../../../mind01/rag.py#L43)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.Embedder.embed` — lines 44–45

- Source: [mind01/rag.py:44](../../../../mind01/rag.py#L44)
- Type: method
- Signature: `self, text: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore` — lines 48–394

- Source: [mind01/rag.py:48](../../../../mind01/rag.py#L48)
- Type: class
- Signature: `n/a`
- Direct static callees: `DocHit`, `StaleDocFile`, `_candidate_rows`, `_connect`, `_display_path`, `_fts_rows`, `_init_db`, `_init_fts`, `_iter_files`, `_keyword_rows`, `_migrate_db`, `add`, `append`, `bool`, `build_fts_query`, `chunk_text_with_lines`, `connect`, `cosine_similarity`, `decode`, `embed`, `encode`, `ensure_text_file_safe`, `execute`, `exists`, `expanduser`, `extend`, `fetchall`, `fetchone`, `float`, `hexdigest`, `int`, `is_file`, `join`, `len`, `list`, `lower`, `max`, `mkdir`, `pack_vector`, `read_bytes`, `relative_to`, `resolve`, `rglob`, `row_to_dict`, `score_chunk`, `set`, `sha256`, `sort`, `split`, `stale_files`, `stat`, `str`, `time_ns`, `unpack_vector`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore.__init__` — lines 49–54

- Source: [mind01/rag.py:49](../../../../mind01/rag.py#L49)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `_init_db`, `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._connect` — lines 56–60

- Source: [mind01/rag.py:56](../../../../mind01/rag.py#L56)
- Type: method
- Signature: `self`
- Direct static callees: `connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._init_db` — lines 62–89

- Source: [mind01/rag.py:62](../../../../mind01/rag.py#L62)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `_init_fts`, `_migrate_db`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._migrate_db` — lines 91–104

- Source: [mind01/rag.py:91](../../../../mind01/rag.py#L91)
- Type: method
- Signature: `self, conn: sqlite3.Connection`
- Direct static callees: `execute`, `fetchall`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._init_fts` — lines 106–116

- Source: [mind01/rag.py:106](../../../../mind01/rag.py#L106)
- Type: method
- Signature: `self, conn: sqlite3.Connection`
- Direct static callees: `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore.index_path` — lines 118–194

- Source: [mind01/rag.py:118](../../../../mind01/rag.py#L118)
- Type: method
- Signature: `self, path: Path, embedder: Embedder | None=None, embedding_model: str=''`
- Direct static callees: `_connect`, `_display_path`, `_iter_files`, `chunk_text_with_lines`, `decode`, `embed`, `encode`, `ensure_text_file_safe`, `execute`, `expanduser`, `hexdigest`, `int`, `list`, `pack_vector`, `read_bytes`, `resolve`, `sha256`, `stat`, `time_ns`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore.search` — lines 196–235

- Source: [mind01/rag.py:196](../../../../mind01/rag.py#L196)
- Type: method
- Signature: `self, query: str, limit: int=6, embedder: Embedder | None=None, embedding_model: str=''`
- Direct static callees: `DocHit`, `_candidate_rows`, `append`, `bool`, `cosine_similarity`, `embed`, `float`, `int`, `max`, `score_chunk`, `sort`, `split`, `stale_files`, `unpack_vector`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore.stats` — lines 237–249

- Source: [mind01/rag.py:237](../../../../mind01/rag.py#L237)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`, `fetchone`, `int`, `len`, `stale_files`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore.stale_files` — lines 251–279

- Source: [mind01/rag.py:251](../../../../mind01/rag.py#L251)
- Type: method
- Signature: `self`
- Direct static callees: `StaleDocFile`, `_connect`, `append`, `execute`, `exists`, `fetchall`, `hexdigest`, `int`, `read_bytes`, `resolve`, `sha256`, `stat`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._candidate_rows` — lines 281–320

- Source: [mind01/rag.py:281](../../../../mind01/rag.py#L281)
- Type: method
- Signature: `self, terms: list[str], limit: int, include_embeddings: bool, embedding_model: str=''`
- Direct static callees: `_connect`, `_fts_rows`, `_keyword_rows`, `add`, `append`, `execute`, `fetchall`, `max`, `row_to_dict`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._fts_rows` — lines 322–350

- Source: [mind01/rag.py:322](../../../../mind01/rag.py#L322)
- Type: method
- Signature: `self, conn: sqlite3.Connection, terms: list[str], limit: int`
- Direct static callees: `build_fts_query`, `execute`, `fetchall`, `max`, `row_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._keyword_rows` — lines 352–377

- Source: [mind01/rag.py:352](../../../../mind01/rag.py#L352)
- Type: method
- Signature: `self, conn: sqlite3.Connection, terms: list[str], limit: int`
- Direct static callees: `execute`, `extend`, `fetchall`, `join`, `max`, `row_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._iter_files` — lines 379–388

- Source: [mind01/rag.py:379](../../../../mind01/rag.py#L379)
- Type: method
- Signature: `self, root: Path`
- Direct static callees: `is_file`, `lower`, `rglob`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.DocStore._display_path` — lines 390–394

- Source: [mind01/rag.py:390](../../../../mind01/rag.py#L390)
- Type: method
- Signature: `self, path: Path`
- Direct static callees: `relative_to`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.chunk_text` — lines 397–409

- Source: [mind01/rag.py:397](../../../../mind01/rag.py#L397)
- Type: function
- Signature: `text: str, size: int=1200, overlap: int=150`
- Direct static callees: `append`, `len`, `max`, `min`, `replace`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.TextChunk` — lines 413–416

- Source: [mind01/rag.py:413](../../../../mind01/rag.py#L413)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.chunk_text_with_lines` — lines 419–449

- Source: [mind01/rag.py:419](../../../../mind01/rag.py#L419)
- Type: function
- Signature: `text: str, size: int=1200, overlap_lines: int=2`
- Direct static callees: `TextChunk`, `append`, `join`, `len`, `max`, `replace`, `splitlines`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.score_chunk` — lines 452–462

- Source: [mind01/rag.py:452](../../../../mind01/rag.py#L452)
- Type: function
- Signature: `path: str, chunk: str, terms: list[str]`
- Direct static callees: `count`, `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.build_fts_query` — lines 465–471

- Source: [mind01/rag.py:465](../../../../mind01/rag.py#L465)
- Type: function
- Signature: `terms: list[str]`
- Direct static callees: `append`, `isalnum`, `join`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rag.row_to_dict` — lines 474–485

- Source: [mind01/rag.py:474](../../../../mind01/rag.py#L474)
- Type: function
- Signature: `row: tuple`
- Direct static callees: `float`, `int`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports a dependency used by this module.

### Lines 5–5

Imports a dependency used by this module.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–14

Implements module-level `Assign` behavior or data.

### Lines 15–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–34

Defines class `DocHit` and the behavior of its members.

### Lines 35–37

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 38–40

Defines class `StaleDocFile` and the behavior of its members.

### Lines 41–42

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 43–45

Defines class `Embedder` and the behavior of its members.

### Lines 46–47

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 48–77

Defines class `DocStore` and the behavior of its members.

### Lines 78–107

Defines class `DocStore` and the behavior of its members.

### Lines 108–137

Defines class `DocStore` and the behavior of its members.

### Lines 138–167

Defines class `DocStore` and the behavior of its members.

### Lines 168–197

Defines class `DocStore` and the behavior of its members.

### Lines 198–227

Defines class `DocStore` and the behavior of its members.

### Lines 228–257

Defines class `DocStore` and the behavior of its members.

### Lines 258–287

Defines class `DocStore` and the behavior of its members.

### Lines 288–317

Defines class `DocStore` and the behavior of its members.

### Lines 318–347

Defines class `DocStore` and the behavior of its members.

### Lines 348–377

Defines class `DocStore` and the behavior of its members.

### Lines 378–394

Defines class `DocStore` and the behavior of its members.

### Lines 395–396

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 397–409

Defines `chunk_text` and its implementation control flow; direct static calls: append, len, max, min, replace, strip.

### Lines 410–412

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 413–416

Defines class `TextChunk` and the behavior of its members.

### Lines 417–418

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 419–448

Defines `chunk_text_with_lines` and its implementation control flow; direct static calls: TextChunk, append, join, len, max, replace, splitlines, strip.

### Lines 449–449

Defines `chunk_text_with_lines` and its implementation control flow; direct static calls: TextChunk, append, join, len, max, replace, splitlines, strip.

### Lines 450–451

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 452–462

Defines `score_chunk` and its implementation control flow; direct static calls: count, lower.

### Lines 463–464

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 465–471

Defines `build_fts_query` and its implementation control flow; direct static calls: append, isalnum, join, strip.

### Lines 472–473

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 474–485

Defines `row_to_dict` and its implementation control flow; direct static calls: float, int, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
