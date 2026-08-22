# `scripts/score_rc3_1_sealed.py`

## File purpose

This automation and release file is reviewed at snapshot `7deab8d93ffd201c538317ec11b5526df33dc30d403e111a9f32e5c0bbf6b9fa`. It contains 203 lines.

## Imports and module state

- [scripts/score_rc3_1_sealed.py:3](../../../../scripts/score_rc3_1_sealed.py#L3) imports `__future__` / annotations.
- [scripts/score_rc3_1_sealed.py:5](../../../../scripts/score_rc3_1_sealed.py#L5) imports `argparse`.
- [scripts/score_rc3_1_sealed.py:6](../../../../scripts/score_rc3_1_sealed.py#L6) imports `json`.
- [scripts/score_rc3_1_sealed.py:7](../../../../scripts/score_rc3_1_sealed.py#L7) imports `math`.
- [scripts/score_rc3_1_sealed.py:8](../../../../scripts/score_rc3_1_sealed.py#L8) imports `collections` / Counter.
- [scripts/score_rc3_1_sealed.py:8](../../../../scripts/score_rc3_1_sealed.py#L8) imports `collections` / defaultdict.
- [scripts/score_rc3_1_sealed.py:9](../../../../scripts/score_rc3_1_sealed.py#L9) imports `pathlib` / Path.
- [scripts/score_rc3_1_sealed.py:10](../../../../scripts/score_rc3_1_sealed.py#L10) imports `typing` / Any.
- [scripts/score_rc3_1_sealed.py:12](../../../../scripts/score_rc3_1_sealed.py#L12) imports `rc3_1_pipeline` / load_json.
- [scripts/score_rc3_1_sealed.py:12](../../../../scripts/score_rc3_1_sealed.py#L12) imports `rc3_1_pipeline` / sha256.

## Symbols

### `scripts.score_rc3_1_sealed.ROOT` — lines 15–15

- Source: [scripts/score_rc3_1_sealed.py:15](../../../../scripts/score_rc3_1_sealed.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.CONTRACT` — lines 16–16

- Source: [scripts/score_rc3_1_sealed.py:16](../../../../scripts/score_rc3_1_sealed.py#L16)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.main` — lines 19–32

- Source: [scripts/score_rc3_1_sealed.py:19](../../../../scripts/score_rc3_1_sealed.py#L19)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `dumps`, `parse_args`, `print`, `score`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.score` — lines 35–106

- Source: [scripts/score_rc3_1_sealed.py:35](../../../../scripts/score_rc3_1_sealed.py#L35)
- Type: function
- Signature: `execution_path: Path, labels_path: Path, seal_path: Path, output_path: Path, rc2_path: Path | None=None`
- Direct static callees: `FileExistsError`, `RuntimeError`, `all`, `compare_rc2`, `dumps`, `endswith`, `exists`, `get`, `grouped`, `isinstance`, `items`, `len`, `load_json`, `metric_summary`, `mkdir`, `resolve`, `score_case`, `set`, `sha256`, `values`, `wilson`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.score_case` — lines 109–148

- Source: [scripts/score_rc3_1_sealed.py:109](../../../../scripts/score_rc3_1_sealed.py#L109)
- Type: function
- Signature: `actual: dict[str, Any], expected: dict[str, Any]`
- Direct static callees: `all`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.metric_summary` — lines 151–170

- Source: [scripts/score_rc3_1_sealed.py:151](../../../../scripts/score_rc3_1_sealed.py#L151)
- Type: function
- Signature: `scored: list[dict[str, Any]]`
- Direct static callees: `len`, `sum`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.grouped` — lines 173–180

- Source: [scripts/score_rc3_1_sealed.py:173](../../../../scripts/score_rc3_1_sealed.py#L173)
- Type: function
- Signature: `scored: list[dict[str, Any]], field: str`
- Direct static callees: `append`, `defaultdict`, `items`, `len`, `sorted`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.compare_rc2` — lines 183–191

- Source: [scripts/score_rc3_1_sealed.py:183](../../../../scripts/score_rc3_1_sealed.py#L183)
- Type: function
- Signature: `metrics: dict[str, Any], report: dict[str, Any] | None`
- Direct static callees: `bool`, `get`, `isinstance`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.score_rc3_1_sealed.wilson` — lines 194–199

- Source: [scripts/score_rc3_1_sealed.py:194](../../../../scripts/score_rc3_1_sealed.py#L194)
- Type: function
- Signature: `rate: float, total: int`
- Direct static callees: `max`, `min`, `sqrt`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Implements module-level `Expr` behavior or data.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports, comments, declarations, or configuration that establish the following implementation context.

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

Imports a dependency used by this module.

### Lines 11–11

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–16

Implements module-level `Assign` behavior or data.

### Lines 17–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–32

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, dumps, parse_args, print, score.

### Lines 33–34

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 35–64

Defines `score` and its implementation control flow; direct static calls: FileExistsError, RuntimeError, all, compare_rc2, dumps, endswith, exists, get, grouped, isinstance, items, len, load_json, metric_summary, mkdir, resolve, score_case, set, sha256, values, wilson, write_text.

### Lines 65–94

Defines `score` and its implementation control flow; direct static calls: FileExistsError, RuntimeError, all, compare_rc2, dumps, endswith, exists, get, grouped, isinstance, items, len, load_json, metric_summary, mkdir, resolve, score_case, set, sha256, values, wilson, write_text.

### Lines 95–106

Defines `score` and its implementation control flow; direct static calls: FileExistsError, RuntimeError, all, compare_rc2, dumps, endswith, exists, get, grouped, isinstance, items, len, load_json, metric_summary, mkdir, resolve, score_case, set, sha256, values, wilson, write_text.

### Lines 107–108

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 109–138

Defines `score_case` and its implementation control flow; direct static calls: all, values.

### Lines 139–148

Defines `score_case` and its implementation control flow; direct static calls: all, values.

### Lines 149–150

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 151–170

Defines `metric_summary` and its implementation control flow; direct static calls: len, sum, tuple.

### Lines 171–172

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 173–180

Defines `grouped` and its implementation control flow; direct static calls: append, defaultdict, items, len, sorted, sum.

### Lines 181–182

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 183–191

Defines `compare_rc2` and its implementation control flow; direct static calls: bool, get, isinstance, items.

### Lines 192–193

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 194–199

Defines `wilson` and its implementation control flow; direct static calls: max, min, sqrt.

### Lines 200–201

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 202–203

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
