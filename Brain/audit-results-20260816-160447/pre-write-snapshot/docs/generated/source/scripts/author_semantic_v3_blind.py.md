# `scripts/author_semantic_v3_blind.py`

## File purpose

This automation and release file is reviewed at snapshot `424a79be65520c1fbd61a932736d4ddb7c7addbe62902fd19a7f2510aabaf988`. It contains 241 lines.

## Imports and module state

- [scripts/author_semantic_v3_blind.py:1](../../../../scripts/author_semantic_v3_blind.py#L1) imports `__future__` / annotations.
- [scripts/author_semantic_v3_blind.py:3](../../../../scripts/author_semantic_v3_blind.py#L3) imports `argparse`.
- [scripts/author_semantic_v3_blind.py:4](../../../../scripts/author_semantic_v3_blind.py#L4) imports `hashlib`.
- [scripts/author_semantic_v3_blind.py:5](../../../../scripts/author_semantic_v3_blind.py#L5) imports `json`.
- [scripts/author_semantic_v3_blind.py:6](../../../../scripts/author_semantic_v3_blind.py#L6) imports `dataclasses` / dataclass.
- [scripts/author_semantic_v3_blind.py:7](../../../../scripts/author_semantic_v3_blind.py#L7) imports `pathlib` / Path.
- [scripts/author_semantic_v3_blind.py:8](../../../../scripts/author_semantic_v3_blind.py#L8) imports `typing` / Any.

## Symbols

### `scripts.author_semantic_v3_blind.TOPICS` — lines 11–18

- Source: [scripts/author_semantic_v3_blind.py:11](../../../../scripts/author_semantic_v3_blind.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.VARIANT_FRAMES` — lines 20–27

- Source: [scripts/author_semantic_v3_blind.py:20](../../../../scripts/author_semantic_v3_blind.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.Archetype` — lines 31–47

- Source: [scripts/author_semantic_v3_blind.py:31](../../../../scripts/author_semantic_v3_blind.py#L31)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.ACTION_ARCHETYPES` — lines 50–78

- Source: [scripts/author_semantic_v3_blind.py:50](../../../../scripts/author_semantic_v3_blind.py#L50)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Archetype`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.NO_ACTION_ARCHETYPES` — lines 81–91

- Source: [scripts/author_semantic_v3_blind.py:81](../../../../scripts/author_semantic_v3_blind.py#L81)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Archetype`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.main` — lines 94–198

- Source: [scripts/author_semantic_v3_blind.py:94](../../../../scripts/author_semantic_v3_blind.py#L94)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `FileExistsError`, `Path`, `RuntimeError`, `add_argument`, `append`, `dumps`, `enumerate`, `error`, `exists`, `format`, `get`, `is_file`, `len`, `load_json`, `parse_args`, `print`, `range`, `replace`, `resolve`, `sha256`, `str`, `sum`, `write_fixture`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.write_fixture` — lines 201–217

- Source: [scripts/author_semantic_v3_blind.py:201](../../../../scripts/author_semantic_v3_blind.py#L201)
- Type: function
- Signature: `path: Path, ordinal: int, kind: str`
- Direct static callees: `mkdir`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.write_json` — lines 220–226

- Source: [scripts/author_semantic_v3_blind.py:220](../../../../scripts/author_semantic_v3_blind.py#L220)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `FileExistsError`, `dumps`, `exists`, `mkdir`, `replace`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.load_json` — lines 229–233

- Source: [scripts/author_semantic_v3_blind.py:229](../../../../scripts/author_semantic_v3_blind.py#L229)
- Type: function
- Signature: `path: Path`
- Direct static callees: `RuntimeError`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.author_semantic_v3_blind.sha256` — lines 236–237

- Source: [scripts/author_semantic_v3_blind.py:236](../../../../scripts/author_semantic_v3_blind.py#L236)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
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

### Lines 9–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–18

Implements module-level `Assign` behavior or data.

### Lines 19–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–27

Implements module-level `Assign` behavior or data.

### Lines 28–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–47

Defines class `Archetype` and the behavior of its members.

### Lines 48–49

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 50–78

Implements module-level `Assign` behavior or data.

### Lines 79–80

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 81–91

Implements module-level `Assign` behavior or data.

### Lines 92–93

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 94–123

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, FileExistsError, Path, RuntimeError, add_argument, append, dumps, enumerate, error, exists, format, get, is_file, len, load_json, parse_args, print, range, replace, resolve, sha256, str, sum, write_fixture, write_json.

### Lines 124–153

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, FileExistsError, Path, RuntimeError, add_argument, append, dumps, enumerate, error, exists, format, get, is_file, len, load_json, parse_args, print, range, replace, resolve, sha256, str, sum, write_fixture, write_json.

### Lines 154–183

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, FileExistsError, Path, RuntimeError, add_argument, append, dumps, enumerate, error, exists, format, get, is_file, len, load_json, parse_args, print, range, replace, resolve, sha256, str, sum, write_fixture, write_json.

### Lines 184–198

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, FileExistsError, Path, RuntimeError, add_argument, append, dumps, enumerate, error, exists, format, get, is_file, len, load_json, parse_args, print, range, replace, resolve, sha256, str, sum, write_fixture, write_json.

### Lines 199–200

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 201–217

Defines `write_fixture` and its implementation control flow; direct static calls: mkdir, write_text.

### Lines 218–219

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 220–226

Defines `write_json` and its implementation control flow; direct static calls: FileExistsError, dumps, exists, mkdir, replace, with_suffix, write_text.

### Lines 227–228

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 229–233

Defines `load_json` and its implementation control flow; direct static calls: RuntimeError, isinstance, loads, read_text.

### Lines 234–235

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 236–237

Defines `sha256` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

### Lines 238–239

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 240–241

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
