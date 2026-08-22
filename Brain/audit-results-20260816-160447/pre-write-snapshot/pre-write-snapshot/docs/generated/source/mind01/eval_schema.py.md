# `mind01/eval_schema.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `8d57acccde85042998b79f0bc0e647693d9513f2628fdefb40e414ea0403e483`. It contains 124 lines.

## Imports and module state

- [mind01/eval_schema.py:1](../../../../mind01/eval_schema.py#L1) imports `__future__` / annotations.
- [mind01/eval_schema.py:3](../../../../mind01/eval_schema.py#L3) imports `hashlib`.
- [mind01/eval_schema.py:4](../../../../mind01/eval_schema.py#L4) imports `json`.
- [mind01/eval_schema.py:5](../../../../mind01/eval_schema.py#L5) imports `dataclasses` / dataclass.
- [mind01/eval_schema.py:5](../../../../mind01/eval_schema.py#L5) imports `dataclasses` / field.
- [mind01/eval_schema.py:6](../../../../mind01/eval_schema.py#L6) imports `pathlib` / Path.
- [mind01/eval_schema.py:7](../../../../mind01/eval_schema.py#L7) imports `typing` / Any.
- [mind01/eval_schema.py:9](../../../../mind01/eval_schema.py#L9) imports `action_parser` / ResponseMode.
- [mind01/eval_schema.py:10](../../../../mind01/eval_schema.py#L10) imports `tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `mind01.eval_schema.ACTION_BENCHMARK_VERSION` — lines 13–13

- Source: [mind01/eval_schema.py:13](../../../../mind01/eval_schema.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_schema.ActionBenchmarkCase` — lines 17–27

- Source: [mind01/eval_schema.py:17](../../../../mind01/eval_schema.py#L17)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_schema.ActionBenchmarkSuite` — lines 31–36

- Source: [mind01/eval_schema.py:31](../../../../mind01/eval_schema.py#L31)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_schema.default_action_suite_path` — lines 39–40

- Source: [mind01/eval_schema.py:39](../../../../mind01/eval_schema.py#L39)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_schema.load_action_suite` — lines 43–95

- Source: [mind01/eval_schema.py:43](../../../../mind01/eval_schema.py#L43)
- Type: function
- Signature: `path: Path | None=None`
- Direct static callees: `ActionBenchmarkCase`, `ActionBenchmarkSuite`, `ResponseMode`, `ValueError`, `add`, `append`, `bool`, `default_action_suite_path`, `encode`, `enumerate`, `get`, `hexdigest`, `int`, `isinstance`, `issubset`, `join`, `len`, `loads`, `max`, `min`, `read_text`, `resolve`, `set`, `sha256`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_schema.validate_eval_assets` — lines 98–124

- Source: [mind01/eval_schema.py:98](../../../../mind01/eval_schema.py#L98)
- Type: function
- Signature: `root: Path`
- Direct static callees: `ValueError`, `append`, `get`, `glob`, `isinstance`, `len`, `load_action_suite`, `load_truthful_suite`, `loads`, `read_text`, `relative_to`, `sorted`, `str`, `validate_semantic_routing_assets`
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

### Lines 11–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–27

Defines class `ActionBenchmarkCase` and the behavior of its members.

### Lines 28–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–36

Defines class `ActionBenchmarkSuite` and the behavior of its members.

### Lines 37–38

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 39–40

Defines `default_action_suite_path` and its implementation control flow; direct static calls: Path, resolve.

### Lines 41–42

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 43–72

Defines `load_action_suite` and its implementation control flow; direct static calls: ActionBenchmarkCase, ActionBenchmarkSuite, ResponseMode, ValueError, add, append, bool, default_action_suite_path, encode, enumerate, get, hexdigest, int, isinstance, issubset, join, len, loads, max, min, read_text, resolve, set, sha256, sorted, str, tuple.

### Lines 73–95

Defines `load_action_suite` and its implementation control flow; direct static calls: ActionBenchmarkCase, ActionBenchmarkSuite, ResponseMode, ValueError, add, append, bool, default_action_suite_path, encode, enumerate, get, hexdigest, int, isinstance, issubset, join, len, loads, max, min, read_text, resolve, set, sha256, sorted, str, tuple.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–124

Defines `validate_eval_assets` and its implementation control flow; direct static calls: ValueError, append, get, glob, isinstance, len, load_action_suite, load_truthful_suite, loads, read_text, relative_to, sorted, str, validate_semantic_routing_assets.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
