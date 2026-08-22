# `scripts/evaluate_semantic_router.py`

## File purpose

This automation and release file is reviewed at snapshot `1be191614d2abdf13be58a4a20ff0bc0e5b7d232701d9c5124d1d5603b20daf5`. It contains 232 lines.

## Imports and module state

- [scripts/evaluate_semantic_router.py:3](../../../../scripts/evaluate_semantic_router.py#L3) imports `__future__` / annotations.
- [scripts/evaluate_semantic_router.py:5](../../../../scripts/evaluate_semantic_router.py#L5) imports `argparse`.
- [scripts/evaluate_semantic_router.py:6](../../../../scripts/evaluate_semantic_router.py#L6) imports `hashlib`.
- [scripts/evaluate_semantic_router.py:7](../../../../scripts/evaluate_semantic_router.py#L7) imports `json`.
- [scripts/evaluate_semantic_router.py:8](../../../../scripts/evaluate_semantic_router.py#L8) imports `os`.
- [scripts/evaluate_semantic_router.py:9](../../../../scripts/evaluate_semantic_router.py#L9) imports `sys`.
- [scripts/evaluate_semantic_router.py:10](../../../../scripts/evaluate_semantic_router.py#L10) imports `time`.
- [scripts/evaluate_semantic_router.py:11](../../../../scripts/evaluate_semantic_router.py#L11) imports `datetime` / datetime.
- [scripts/evaluate_semantic_router.py:11](../../../../scripts/evaluate_semantic_router.py#L11) imports `datetime` / timezone.
- [scripts/evaluate_semantic_router.py:12](../../../../scripts/evaluate_semantic_router.py#L12) imports `pathlib` / Path.
- [scripts/evaluate_semantic_router.py:13](../../../../scripts/evaluate_semantic_router.py#L13) imports `typing` / Any.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / DEVELOPMENT_GATES.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / HOLDOUT_ACCESS.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / HOLDOUT_GATES.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / SemanticBenchmarkError.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / deterministic_order.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / evaluate_gates.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / load_split.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / legacy_v2_disagreements.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / run_case.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / score_results.
- [scripts/evaluate_semantic_router.py:18](../../../../scripts/evaluate_semantic_router.py#L18) imports `mind01.semantic_benchmark_v2` / validate_suite.
- [scripts/evaluate_semantic_router.py:31](../../../../scripts/evaluate_semantic_router.py#L31) imports `mind01.version` / __version__.

## Symbols

### `scripts.evaluate_semantic_router.ROOT` — lines 15–15

- Source: [scripts/evaluate_semantic_router.py:15](../../../../scripts/evaluate_semantic_router.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.evaluate_semantic_router.parser` — lines 34–51

- Source: [scripts/evaluate_semantic_router.py:34](../../../../scripts/evaluate_semantic_router.py#L34)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `add_argument`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.evaluate_semantic_router.atomic_json` — lines 54–61

- Source: [scripts/evaluate_semantic_router.py:54](../../../../scripts/evaluate_semantic_router.py#L54)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `mkdir`, `replace`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.evaluate_semantic_router.main` — lines 64–190

- Source: [scripts/evaluate_semantic_router.py:64](../../../../scripts/evaluate_semantic_router.py#L64)
- Type: function
- Signature: `argv: list[str] | None=None`
- Direct static callees: `SemanticBenchmarkError`, `atomic_json`, `deterministic_order`, `dumps`, `evaluate_gates`, `exists`, `fromtimestamp`, `get`, `hexdigest`, `isoformat`, `legacy_v2_disagreements`, `list`, `load_split`, `loads`, `mkdir`, `now`, `parse_args`, `parser`, `print`, `read_bytes`, `read_text`, `round`, `run_ablation`, `run_case`, `score_results`, `sha256`, `str`, `time`, `validate_suite`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.evaluate_semantic_router.run_ablation` — lines 193–228

- Source: [scripts/evaluate_semantic_router.py:193](../../../../scripts/evaluate_semantic_router.py#L193)
- Type: function
- Signature: `args: argparse.Namespace, cases: list[dict[str, Any]], integrity: dict[str, Any]`
- Direct static callees: `deterministic_order`, `run_case`, `score_results`
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

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–16

Implements module-level `Expr` behavior or data.

### Lines 17–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–30

Imports a dependency used by this module.

### Lines 31–31

Imports a dependency used by this module.

### Lines 32–33

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 34–51

Defines `parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument.

### Lines 52–53

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 54–61

Defines `atomic_json` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

### Lines 62–63

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 64–93

Defines `main` and its implementation control flow; direct static calls: SemanticBenchmarkError, atomic_json, deterministic_order, dumps, evaluate_gates, exists, fromtimestamp, get, hexdigest, isoformat, legacy_v2_disagreements, list, load_split, loads, mkdir, now, parse_args, parser, print, read_bytes, read_text, round, run_ablation, run_case, score_results, sha256, str, time, validate_suite, values.

### Lines 94–123

Defines `main` and its implementation control flow; direct static calls: SemanticBenchmarkError, atomic_json, deterministic_order, dumps, evaluate_gates, exists, fromtimestamp, get, hexdigest, isoformat, legacy_v2_disagreements, list, load_split, loads, mkdir, now, parse_args, parser, print, read_bytes, read_text, round, run_ablation, run_case, score_results, sha256, str, time, validate_suite, values.

### Lines 124–153

Defines `main` and its implementation control flow; direct static calls: SemanticBenchmarkError, atomic_json, deterministic_order, dumps, evaluate_gates, exists, fromtimestamp, get, hexdigest, isoformat, legacy_v2_disagreements, list, load_split, loads, mkdir, now, parse_args, parser, print, read_bytes, read_text, round, run_ablation, run_case, score_results, sha256, str, time, validate_suite, values.

### Lines 154–183

Defines `main` and its implementation control flow; direct static calls: SemanticBenchmarkError, atomic_json, deterministic_order, dumps, evaluate_gates, exists, fromtimestamp, get, hexdigest, isoformat, legacy_v2_disagreements, list, load_split, loads, mkdir, now, parse_args, parser, print, read_bytes, read_text, round, run_ablation, run_case, score_results, sha256, str, time, validate_suite, values.

### Lines 184–190

Defines `main` and its implementation control flow; direct static calls: SemanticBenchmarkError, atomic_json, deterministic_order, dumps, evaluate_gates, exists, fromtimestamp, get, hexdigest, isoformat, legacy_v2_disagreements, list, load_split, loads, mkdir, now, parse_args, parser, print, read_bytes, read_text, round, run_ablation, run_case, score_results, sha256, str, time, validate_suite, values.

### Lines 191–192

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 193–222

Defines `run_ablation` and its implementation control flow; direct static calls: deterministic_order, run_case, score_results.

### Lines 223–228

Defines `run_ablation` and its implementation control flow; direct static calls: deterministic_order, run_case, score_results.

### Lines 229–230

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 231–232

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
