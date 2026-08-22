# `mind01/project_map.py`

## File purpose

This agent runtime file is reviewed at snapshot `d5127e4a2409d63e223973e92c526040bf0f43a3074385e34cb4c84375eff911`. It contains 102 lines.

## Imports and module state

- [mind01/project_map.py:1](../../../../mind01/project_map.py#L1) imports `__future__` / annotations.
- [mind01/project_map.py:3](../../../../mind01/project_map.py#L3) imports `collections` / Counter.
- [mind01/project_map.py:4](../../../../mind01/project_map.py#L4) imports `dataclasses` / dataclass.
- [mind01/project_map.py:5](../../../../mind01/project_map.py#L5) imports `pathlib` / Path.
- [mind01/project_map.py:6](../../../../mind01/project_map.py#L6) imports `typing` / Iterable.

## Symbols

### `mind01.project_map.SKIP_DIRS` — lines 9–19

- Source: [mind01/project_map.py:9](../../../../mind01/project_map.py#L9)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.IMPORTANT_NAMES` — lines 21–29

- Source: [mind01/project_map.py:21](../../../../mind01/project_map.py#L21)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.SKIP_FILES` — lines 31–33

- Source: [mind01/project_map.py:31](../../../../mind01/project_map.py#L31)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.ProjectMap` — lines 37–63

- Source: [mind01/project_map.py:37](../../../../mind01/project_map.py#L37)
- Type: class
- Signature: `n/a`
- Direct static callees: `join`, `most_common`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.ProjectMap.render` — lines 44–63

- Source: [mind01/project_map.py:44](../../../../mind01/project_map.py#L44)
- Type: method
- Signature: `self`
- Direct static callees: `join`, `most_common`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.build_project_map` — lines 66–84

- Source: [mind01/project_map.py:66](../../../../mind01/project_map.py#L66)
- Type: function
- Signature: `workspace: Path, path: str='.', max_files: int=250`
- Direct static callees: `Counter`, `ProjectMap`, `ValueError`, `iter_project_files`, `len`, `list`, `lower`, `relative_to`, `resolve`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_map.iter_project_files` — lines 87–102

- Source: [mind01/project_map.py:87](../../../../mind01/project_map.py#L87)
- Type: function
- Signature: `root: Path, workspace: Path, max_files: int`
- Direct static callees: `any`, `is_dir`, `is_file`, `relative_to`, `rglob`, `sorted`
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

### Lines 7–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–19

Implements module-level `Assign` behavior or data.

### Lines 20–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–29

Implements module-level `Assign` behavior or data.

### Lines 30–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–33

Implements module-level `Assign` behavior or data.

### Lines 34–36

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 37–63

Defines class `ProjectMap` and the behavior of its members.

### Lines 64–65

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 66–84

Defines `build_project_map` and its implementation control flow; direct static calls: Counter, ProjectMap, ValueError, iter_project_files, len, list, lower, relative_to, resolve, str.

### Lines 85–86

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 87–102

Defines `iter_project_files` and its implementation control flow; direct static calls: any, is_dir, is_file, relative_to, rglob, sorted.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
