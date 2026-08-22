# `tests/test_semantic_benchmark_v2.py`

## File purpose

This testing file is reviewed at snapshot `24a2b0d20fb34d0542043c7a89eb3b5eb6d0f1b61891f83c004b013eb69c48b3`. It contains 78 lines.

## Imports and module state

- [tests/test_semantic_benchmark_v2.py:1](../../../../tests/test_semantic_benchmark_v2.py#L1) imports `__future__` / annotations.
- [tests/test_semantic_benchmark_v2.py:3](../../../../tests/test_semantic_benchmark_v2.py#L3) imports `json`.
- [tests/test_semantic_benchmark_v2.py:5](../../../../tests/test_semantic_benchmark_v2.py#L5) imports `pytest`.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / FORBIDDEN_MARKERS.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / HOLDOUT_ACCESS.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / SemanticBenchmarkError.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / load_split.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / run_case.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / safe_suite_path.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / semantic_near_duplicates.
- [tests/test_semantic_benchmark_v2.py:7](../../../../tests/test_semantic_benchmark_v2.py#L7) imports `mind01.semantic_benchmark_v2` / validate_suite.

## Symbols

### `tests.test_semantic_benchmark_v2.test_visible_fresh_suite_is_complete_disjoint_and_uncontaminated` — lines 19–31

- Source: [tests/test_semantic_benchmark_v2.py:19](../../../../tests/test_semantic_benchmark_v2.py#L19)
- Type: function
- Signature: `n/a`
- Direct static callees: `set`, `validate_suite`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_benchmark_v2.test_holdout_requires_explicit_one_shot_protocol` — lines 34–40

- Source: [tests/test_semantic_benchmark_v2.py:34](../../../../tests/test_semantic_benchmark_v2.py#L34)
- Type: function
- Signature: `n/a`
- Direct static callees: `exists`, `load_split`, `loads`, `raises`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_benchmark_v2.test_duplicate_and_near_duplicate_detection_is_deterministic` — lines 43–49

- Source: [tests/test_semantic_benchmark_v2.py:43](../../../../tests/test_semantic_benchmark_v2.py#L43)
- Type: function
- Signature: `n/a`
- Direct static callees: `semantic_near_duplicates`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_benchmark_v2.test_forbidden_marker_guard_covers_frozen_data_references` — lines 52–62

- Source: [tests/test_semantic_benchmark_v2.py:52](../../../../tests/test_semantic_benchmark_v2.py#L52)
- Type: function
- Signature: `n/a`
- Direct static callees: `any`, `casefold`, `dumps`, `raises`, `safe_suite_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_benchmark_v2.test_raw_outputs_cannot_change_expected_labels` — lines 65–78

- Source: [tests/test_semantic_benchmark_v2.py:65](../../../../tests/test_semantic_benchmark_v2.py#L65)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `dict`, `load_split`, `run_case`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 5–5

Imports a dependency used by this module.

### Lines 6–6

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–16

Imports a dependency used by this module.

### Lines 17–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–31

Defines `test_visible_fresh_suite_is_complete_disjoint_and_uncontaminated` and its implementation control flow; direct static calls: set, validate_suite.

### Lines 32–33

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 34–40

Defines `test_holdout_requires_explicit_one_shot_protocol` and its implementation control flow; direct static calls: exists, load_split, loads, raises, read_text.

### Lines 41–42

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 43–49

Defines `test_duplicate_and_near_duplicate_detection_is_deterministic` and its implementation control flow; direct static calls: semantic_near_duplicates.

### Lines 50–51

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 52–62

Defines `test_forbidden_marker_guard_covers_frozen_data_references` and its implementation control flow; direct static calls: any, casefold, dumps, raises, safe_suite_path.

### Lines 63–64

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 65–78

Defines `test_raw_outputs_cannot_change_expected_labels` and its implementation control flow; direct static calls: append, dict, load_split, run_case.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
