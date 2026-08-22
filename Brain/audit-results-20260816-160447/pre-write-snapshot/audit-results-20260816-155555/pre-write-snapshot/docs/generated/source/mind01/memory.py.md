# `mind01/memory.py`

## File purpose

This sessions memory and RAG file is reviewed at snapshot `24086d81d361b3e7e21995e93f2c39bf9c0aa263d20e150d2534a92a7eab01c7`. It contains 367 lines.

## Imports and module state

- [mind01/memory.py:1](../../../../mind01/memory.py#L1) imports `__future__` / annotations.
- [mind01/memory.py:3](../../../../mind01/memory.py#L3) imports `sqlite3`.
- [mind01/memory.py:4](../../../../mind01/memory.py#L4) imports `time`.
- [mind01/memory.py:5](../../../../mind01/memory.py#L5) imports `dataclasses` / dataclass.
- [mind01/memory.py:6](../../../../mind01/memory.py#L6) imports `pathlib` / Path.
- [mind01/memory.py:7](../../../../mind01/memory.py#L7) imports `typing` / List.
- [mind01/memory.py:7](../../../../mind01/memory.py#L7) imports `typing` / Protocol.
- [mind01/memory.py:9](../../../../mind01/memory.py#L9) imports `embeddings` / cosine_similarity.
- [mind01/memory.py:9](../../../../mind01/memory.py#L9) imports `embeddings` / pack_vector.
- [mind01/memory.py:9](../../../../mind01/memory.py#L9) imports `embeddings` / unpack_vector.
- [mind01/memory.py:10](../../../../mind01/memory.py#L10) imports `security` / redact_secrets.

## Symbols

### `mind01.memory.MemoryHit` — lines 14–36

- Source: [mind01/memory.py:14](../../../../mind01/memory.py#L14)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryHit.memory_id` — lines 31–32

- Source: [mind01/memory.py:31](../../../../mind01/memory.py#L31)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryHit.text` — lines 35–36

- Source: [mind01/memory.py:35](../../../../mind01/memory.py#L35)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.Embedder` — lines 39–41

- Source: [mind01/memory.py:39](../../../../mind01/memory.py#L39)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.Embedder.embed` — lines 40–41

- Source: [mind01/memory.py:40](../../../../mind01/memory.py#L40)
- Type: method
- Signature: `self, text: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore` — lines 44–258

- Source: [mind01/memory.py:44](../../../../mind01/memory.py#L44)
- Type: class
- Signature: `n/a`
- Direct static callees: `ValueError`, `_connect`, `_init_db`, `_migrate_db`, `append`, `clean_text`, `connect`, `embed`, `execute`, `executemany`, `extend`, `fetchall`, `fetchone`, `int`, `items`, `join`, `make_embedding`, `max`, `mkdir`, `normalize_importance`, `normalize_tags`, `parse_tags`, `rank_memory_rows`, `row_to_hit`, `strip`, `tags_match`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.__init__` — lines 45–48

- Source: [mind01/memory.py:45](../../../../mind01/memory.py#L45)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `_init_db`, `mkdir`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore._connect` — lines 50–54

- Source: [mind01/memory.py:50](../../../../mind01/memory.py#L50)
- Type: method
- Signature: `self`
- Direct static callees: `connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore._init_db` — lines 56–85

- Source: [mind01/memory.py:56](../../../../mind01/memory.py#L56)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `_migrate_db`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore._migrate_db` — lines 87–101

- Source: [mind01/memory.py:87](../../../../mind01/memory.py#L87)
- Type: method
- Signature: `self, conn: sqlite3.Connection`
- Direct static callees: `execute`, `fetchall`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.remember` — lines 103–157

- Source: [mind01/memory.py:103](../../../../mind01/memory.py#L103)
- Type: method
- Signature: `self, key: str, value: str, tags: str='', source: str='user', importance: int=1, embedder: Embedder | None=None, embedding_model: str=''`
- Direct static callees: `ValueError`, `_connect`, `clean_text`, `execute`, `fetchone`, `int`, `make_embedding`, `normalize_importance`, `normalize_tags`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.recall` — lines 159–194

- Source: [mind01/memory.py:159](../../../../mind01/memory.py#L159)
- Type: method
- Signature: `self, query: str, limit: int=8, tags: str='', embedder: Embedder | None=None, embedding_model: str='', record_use: bool=False`
- Direct static callees: `_connect`, `embed`, `execute`, `executemany`, `fetchall`, `int`, `max`, `parse_tags`, `rank_memory_rows`, `strip`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.list` — lines 196–211

- Source: [mind01/memory.py:196](../../../../mind01/memory.py#L196)
- Type: method
- Signature: `self, limit: int=50, tags: str=''`
- Direct static callees: `_connect`, `execute`, `fetchall`, `int`, `max`, `parse_tags`, `row_to_hit`, `tags_match`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.update` — lines 213–251

- Source: [mind01/memory.py:213](../../../../mind01/memory.py#L213)
- Type: method
- Signature: `self, memory_id: int, value: str, tags: str | None=None, source: str | None=None, importance: int | None=None, embedder: Embedder | None=None, embedding_model: str=''`
- Direct static callees: `ValueError`, `_connect`, `append`, `clean_text`, `execute`, `extend`, `int`, `join`, `make_embedding`, `normalize_importance`, `normalize_tags`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.MemoryStore.delete` — lines 253–258

- Source: [mind01/memory.py:253](../../../../mind01/memory.py#L253)
- Type: method
- Signature: `self, memory_id: int`
- Direct static callees: `ValueError`, `_connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.row_to_hit` — lines 261–277

- Source: [mind01/memory.py:261](../../../../mind01/memory.py#L261)
- Type: function
- Signature: `row: tuple, score: float=0.0, lexical_score: int=0, vector_score: float=0.0`
- Direct static callees: `MemoryHit`, `int`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.rank_memory_rows` — lines 280–304

- Source: [mind01/memory.py:280](../../../../mind01/memory.py#L280)
- Type: function
- Signature: `rows: list[tuple], query: str, tag_filter: list[str], query_vector: list[float], embedding_model: str`
- Direct static callees: `append`, `cosine_similarity`, `float`, `int`, `lexical_score`, `max`, `row_to_hit`, `sort`, `str`, `tags_match`, `unpack_vector`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.lexical_score` — lines 307–320

- Source: [mind01/memory.py:307](../../../../mind01/memory.py#L307)
- Type: function
- Signature: `key: str, value: str, tags: str, query: str`
- Direct static callees: `count`, `items`, `lower`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.clean_text` — lines 323–324

- Source: [mind01/memory.py:323](../../../../mind01/memory.py#L323)
- Type: function
- Signature: `text: str`
- Direct static callees: `redact_secrets`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.normalize_tags` — lines 327–329

- Source: [mind01/memory.py:327](../../../../mind01/memory.py#L327)
- Type: function
- Signature: `tags: str`
- Direct static callees: `join`, `parse_tags`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.parse_tags` — lines 332–341

- Source: [mind01/memory.py:332](../../../../mind01/memory.py#L332)
- Type: function
- Signature: `tags: str`
- Direct static callees: `add`, `append`, `lower`, `set`, `split`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.tags_match` — lines 344–346

- Source: [mind01/memory.py:344](../../../../mind01/memory.py#L344)
- Type: function
- Signature: `tags: str, required: list[str]`
- Direct static callees: `all`, `parse_tags`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.normalize_importance` — lines 349–356

- Source: [mind01/memory.py:349](../../../../mind01/memory.py#L349)
- Type: function
- Signature: `value: int`
- Direct static callees: `ValueError`, `int`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory.make_embedding` — lines 359–367

- Source: [mind01/memory.py:359](../../../../mind01/memory.py#L359)
- Type: function
- Signature: `embedder: Embedder | None, text: str, embedding_model: str`
- Direct static callees: `embed`, `pack_vector`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–36

Defines class `MemoryHit` and the behavior of its members.

### Lines 37–38

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 39–41

Defines class `Embedder` and the behavior of its members.

### Lines 42–43

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 44–73

Defines class `MemoryStore` and the behavior of its members.

### Lines 74–103

Defines class `MemoryStore` and the behavior of its members.

### Lines 104–133

Defines class `MemoryStore` and the behavior of its members.

### Lines 134–163

Defines class `MemoryStore` and the behavior of its members.

### Lines 164–193

Defines class `MemoryStore` and the behavior of its members.

### Lines 194–223

Defines class `MemoryStore` and the behavior of its members.

### Lines 224–253

Defines class `MemoryStore` and the behavior of its members.

### Lines 254–258

Defines class `MemoryStore` and the behavior of its members.

### Lines 259–260

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 261–277

Defines `row_to_hit` and its implementation control flow; direct static calls: MemoryHit, int, str.

### Lines 278–279

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 280–304

Defines `rank_memory_rows` and its implementation control flow; direct static calls: append, cosine_similarity, float, int, lexical_score, max, row_to_hit, sort, str, tags_match, unpack_vector.

### Lines 305–306

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 307–320

Defines `lexical_score` and its implementation control flow; direct static calls: count, items, lower, split.

### Lines 321–322

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 323–324

Defines `clean_text` and its implementation control flow; direct static calls: redact_secrets, str, strip.

### Lines 325–326

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 327–329

Defines `normalize_tags` and its implementation control flow; direct static calls: join, parse_tags.

### Lines 330–331

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 332–341

Defines `parse_tags` and its implementation control flow; direct static calls: add, append, lower, set, split, str, strip.

### Lines 342–343

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 344–346

Defines `tags_match` and its implementation control flow; direct static calls: all, parse_tags, set.

### Lines 347–348

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 349–356

Defines `normalize_importance` and its implementation control flow; direct static calls: ValueError, int.

### Lines 357–358

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 359–367

Defines `make_embedding` and its implementation control flow; direct static calls: embed, pack_vector.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
