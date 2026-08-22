# `mind01/code_index.py`

## File purpose

This agent runtime file is reviewed at snapshot `31bf32adefc59639331974a56c8774f40544938fa9b4e12de2edab8a9d37b97b`. It contains 361 lines.

## Imports and module state

- [mind01/code_index.py:1](../../../../mind01/code_index.py#L1) imports `__future__` / annotations.
- [mind01/code_index.py:3](../../../../mind01/code_index.py#L3) imports `ast`.
- [mind01/code_index.py:4](../../../../mind01/code_index.py#L4) imports `re`.
- [mind01/code_index.py:5](../../../../mind01/code_index.py#L5) imports `sqlite3`.
- [mind01/code_index.py:6](../../../../mind01/code_index.py#L6) imports `time`.
- [mind01/code_index.py:7](../../../../mind01/code_index.py#L7) imports `dataclasses` / dataclass.
- [mind01/code_index.py:8](../../../../mind01/code_index.py#L8) imports `pathlib` / Path.
- [mind01/code_index.py:9](../../../../mind01/code_index.py#L9) imports `typing` / Iterable.
- [mind01/code_index.py:11](../../../../mind01/code_index.py#L11) imports `file_safety` / FileSafetyError.
- [mind01/code_index.py:11](../../../../mind01/code_index.py#L11) imports `file_safety` / ensure_text_file_safe.
- [mind01/code_index.py:11](../../../../mind01/code_index.py#L11) imports `file_safety` / resolve_workspace_path.

## Symbols

### `mind01.code_index.CODE_SUFFIXES` — lines 14–14

- Source: [mind01/code_index.py:14](../../../../mind01/code_index.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.SKIP_DIRS` — lines 15–15

- Source: [mind01/code_index.py:15](../../../../mind01/code_index.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.SymbolHit` — lines 19–24

- Source: [mind01/code_index.py:19](../../../../mind01/code_index.py#L19)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.FileSummary` — lines 28–32

- Source: [mind01/code_index.py:28](../../../../mind01/code_index.py#L28)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex` — lines 35–240

- Source: [mind01/code_index.py:35](../../../../mind01/code_index.py#L35)
- Type: class
- Signature: `n/a`
- Direct static callees: `FileSummary`, `SymbolHit`, `ValueError`, `_connect`, `_init_db`, `_search_workspace_symbols`, `any`, `append`, `casefold`, `connect`, `ensure_text_file_safe`, `execute`, `exists`, `fetchall`, `fetchone`, `int`, `iter_code_files`, `language_for`, `list`, `mkdir`, `parse_code_file`, `read_text`, `relative_to`, `resolve`, `resolve_workspace_path`, `sort`, `sorted`, `startswith`, `stat`, `str`, `strip`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.__init__` — lines 36–40

- Source: [mind01/code_index.py:36](../../../../mind01/code_index.py#L36)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `_init_db`, `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex._connect` — lines 42–46

- Source: [mind01/code_index.py:42](../../../../mind01/code_index.py#L42)
- Type: method
- Signature: `self`
- Direct static callees: `connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex._init_db` — lines 48–83

- Source: [mind01/code_index.py:48](../../../../mind01/code_index.py#L48)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.index_path` — lines 85–124

- Source: [mind01/code_index.py:85](../../../../mind01/code_index.py#L85)
- Type: method
- Signature: `self, path: Path | None=None`
- Direct static callees: `ValueError`, `_connect`, `ensure_text_file_safe`, `execute`, `int`, `iter_code_files`, `language_for`, `list`, `parse_code_file`, `read_text`, `relative_to`, `resolve_workspace_path`, `stat`, `str`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.search_symbols` — lines 126–147

- Source: [mind01/code_index.py:126](../../../../mind01/code_index.py#L126)
- Type: method
- Signature: `self, query: str, limit: int=20`
- Direct static callees: `SymbolHit`, `_connect`, `_search_workspace_symbols`, `execute`, `fetchall`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex._search_workspace_symbols` — lines 149–189

- Source: [mind01/code_index.py:149](../../../../mind01/code_index.py#L149)
- Type: method
- Signature: `self, query: str, *, limit: int`
- Direct static callees: `SymbolHit`, `any`, `append`, `casefold`, `ensure_text_file_safe`, `iter_code_files`, `parse_code_file`, `read_text`, `relative_to`, `sort`, `startswith`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.file_summary` — lines 191–218

- Source: [mind01/code_index.py:191](../../../../mind01/code_index.py#L191)
- Type: method
- Signature: `self, raw_path: str`
- Direct static callees: `FileSummary`, `SymbolHit`, `ValueError`, `_connect`, `execute`, `fetchall`, `fetchone`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.stats` — lines 220–224

- Source: [mind01/code_index.py:220](../../../../mind01/code_index.py#L220)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`, `fetchone`, `int`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.CodeIndex.stale_files` — lines 226–240

- Source: [mind01/code_index.py:226](../../../../mind01/code_index.py#L226)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `append`, `execute`, `exists`, `fetchall`, `sorted`, `stat`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.iter_code_files` — lines 243–249

- Source: [mind01/code_index.py:243](../../../../mind01/code_index.py#L243)
- Type: function
- Signature: `root: Path`
- Direct static callees: `any`, `is_dir`, `is_file`, `lower`, `rglob`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.language_for` — lines 252–262

- Source: [mind01/code_index.py:252](../../../../mind01/code_index.py#L252)
- Type: function
- Signature: `path: Path`
- Direct static callees: `lower`, `lstrip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.parse_code_file` — lines 265–268

- Source: [mind01/code_index.py:265](../../../../mind01/code_index.py#L265)
- Type: function
- Signature: `path: Path, text: str`
- Direct static callees: `lower`, `parse_lightweight`, `parse_python`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.parse_python` — lines 271–304

- Source: [mind01/code_index.py:271](../../../../mind01/code_index.py#L271)
- Type: function
- Signature: `path: Path, text: str`
- Direct static callees: `SymbolHit`, `append`, `extend`, `isinstance`, `parse`, `python_signature`, `set`, `sorted`, `str`, `walk`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.python_signature` — lines 307–315

- Source: [mind01/code_index.py:307](../../../../mind01/code_index.py#L307)
- Type: function
- Signature: `node: ast.FunctionDef | ast.AsyncFunctionDef`
- Direct static callees: `append`, `extend`, `isinstance`, `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.LIGHTWEIGHT_PATTERNS` — lines 318–323

- Source: [mind01/code_index.py:318](../../../../mind01/code_index.py#L318)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.IMPORT_RE` — lines 324–324

- Source: [mind01/code_index.py:324](../../../../mind01/code_index.py#L324)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.parse_lightweight` — lines 327–338

- Source: [mind01/code_index.py:327](../../../../mind01/code_index.py#L327)
- Type: function
- Signature: `path: Path, text: str`
- Direct static callees: `SymbolHit`, `append`, `count`, `extend`, `finditer`, `group`, `groups`, `set`, `sorted`, `start`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.render_symbol_hits` — lines 341–347

- Source: [mind01/code_index.py:341](../../../../mind01/code_index.py#L341)
- Type: function
- Signature: `hits: list[SymbolHit]`
- Direct static callees: `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.code_index.render_file_summary` — lines 350–361

- Source: [mind01/code_index.py:350](../../../../mind01/code_index.py#L350)
- Type: function
- Signature: `summary: FileSummary`
- Direct static callees: `append`, `extend`, `join`
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

Imports a dependency used by this module.

### Lines 10–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–14

Implements module-level `Assign` behavior or data.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–24

Defines class `SymbolHit` and the behavior of its members.

### Lines 25–27

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 28–32

Defines class `FileSummary` and the behavior of its members.

### Lines 33–34

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 35–64

Defines class `CodeIndex` and the behavior of its members.

### Lines 65–94

Defines class `CodeIndex` and the behavior of its members.

### Lines 95–124

Defines class `CodeIndex` and the behavior of its members.

### Lines 125–154

Defines class `CodeIndex` and the behavior of its members.

### Lines 155–184

Defines class `CodeIndex` and the behavior of its members.

### Lines 185–214

Defines class `CodeIndex` and the behavior of its members.

### Lines 215–240

Defines class `CodeIndex` and the behavior of its members.

### Lines 241–242

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 243–249

Defines `iter_code_files` and its implementation control flow; direct static calls: any, is_dir, is_file, lower, rglob, sorted.

### Lines 250–251

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 252–262

Defines `language_for` and its implementation control flow; direct static calls: lower, lstrip.

### Lines 263–264

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 265–268

Defines `parse_code_file` and its implementation control flow; direct static calls: lower, parse_lightweight, parse_python.

### Lines 269–270

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 271–300

Defines `parse_python` and its implementation control flow; direct static calls: SymbolHit, append, extend, isinstance, parse, python_signature, set, sorted, str, walk.

### Lines 301–304

Defines `parse_python` and its implementation control flow; direct static calls: SymbolHit, append, extend, isinstance, parse, python_signature, set, sorted, str, walk.

### Lines 305–306

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 307–315

Defines `python_signature` and its implementation control flow; direct static calls: append, extend, isinstance, join.

### Lines 316–317

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 318–323

Implements module-level `Assign` behavior or data.

### Lines 324–324

Implements module-level `Assign` behavior or data.

### Lines 325–326

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 327–338

Defines `parse_lightweight` and its implementation control flow; direct static calls: SymbolHit, append, count, extend, finditer, group, groups, set, sorted, start, str, strip.

### Lines 339–340

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 341–347

Defines `render_symbol_hits` and its implementation control flow; direct static calls: join.

### Lines 348–349

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 350–361

Defines `render_file_summary` and its implementation control flow; direct static calls: append, extend, join.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
