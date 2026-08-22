# `mind01/file_safety.py`

## File purpose

This filesystem and mutations file is reviewed at snapshot `ebc44394e52890251aaeaeea7e1c33eed72fe750002fb506f8657ddc273d89e3`. It contains 108 lines.

## Imports and module state

- [mind01/file_safety.py:1](../../../../mind01/file_safety.py#L1) imports `__future__` / annotations.
- [mind01/file_safety.py:3](../../../../mind01/file_safety.py#L3) imports `pathlib` / Path.

## Symbols

### `mind01.file_safety.MAX_TEXT_FILE_BYTES` — lines 6–6

- Source: [mind01/file_safety.py:6](../../../../mind01/file_safety.py#L6)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.TEXT_SAMPLE_BYTES` — lines 7–7

- Source: [mind01/file_safety.py:7](../../../../mind01/file_safety.py#L7)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.RUNTIME_DIR` — lines 8–8

- Source: [mind01/file_safety.py:8](../../../../mind01/file_safety.py#L8)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.SENSITIVE_RUNTIME_SUFFIXES` — lines 9–9

- Source: [mind01/file_safety.py:9](../../../../mind01/file_safety.py#L9)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.FileSafetyError` — lines 12–13

- Source: [mind01/file_safety.py:12](../../../../mind01/file_safety.py#L12)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.resolve_workspace_path` — lines 16–21

- Source: [mind01/file_safety.py:16](../../../../mind01/file_safety.py#L16)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `FileSafetyError`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.resolve_existing_path` — lines 24–28

- Source: [mind01/file_safety.py:24](../../../../mind01/file_safety.py#L24)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `FileSafetyError`, `exists`, `resolve_workspace_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.resolve_write_path` — lines 31–41

- Source: [mind01/file_safety.py:31](../../../../mind01/file_safety.py#L31)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `FileSafetyError`, `exists`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.relative_path` — lines 44–48

- Source: [mind01/file_safety.py:44](../../../../mind01/file_safety.py#L44)
- Type: function
- Signature: `workspace: Path, path: Path`
- Direct static callees: `FileSafetyError`, `relative_to`, `resolve`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.is_runtime_path` — lines 51–56

- Source: [mind01/file_safety.py:51](../../../../mind01/file_safety.py#L51)
- Type: function
- Signature: `workspace: Path, path: Path`
- Direct static callees: `bool`, `relative_to`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.ensure_not_runtime_path` — lines 59–65

- Source: [mind01/file_safety.py:59](../../../../mind01/file_safety.py#L59)
- Type: function
- Signature: `workspace: Path, path: Path, raw_path: str=''`
- Direct static callees: `FileSafetyError`, `is_file`, `is_runtime_path`, `lower`, `relative_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.ensure_text_file_safe` — lines 68–94

- Source: [mind01/file_safety.py:68](../../../../mind01/file_safety.py#L68)
- Type: function
- Signature: `workspace: Path, path: Path, raw_path: str=''`
- Direct static callees: `FileSafetyError`, `decode`, `ensure_not_runtime_path`, `is_file`, `read_bytes`, `relative_path`, `stat`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.read_text_file_safe` — lines 97–102

- Source: [mind01/file_safety.py:97](../../../../mind01/file_safety.py#L97)
- Type: function
- Signature: `workspace: Path, raw_path: str, max_bytes: int=MAX_TEXT_FILE_BYTES`
- Direct static callees: `FileSafetyError`, `ensure_text_file_safe`, `read_text`, `resolve_existing_path`, `stat`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.file_safety.ensure_write_target_safe` — lines 105–108

- Source: [mind01/file_safety.py:105](../../../../mind01/file_safety.py#L105)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `ensure_not_runtime_path`, `resolve_write_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–5

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 6–6

Implements module-level `Assign` behavior or data.

### Lines 7–7

Implements module-level `Assign` behavior or data.

### Lines 8–8

Implements module-level `Assign` behavior or data.

### Lines 9–9

Implements module-level `Assign` behavior or data.

### Lines 10–11

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 12–13

Defines class `FileSafetyError` and the behavior of its members.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–21

Defines `resolve_workspace_path` and its implementation control flow; direct static calls: FileSafetyError, resolve.

### Lines 22–23

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 24–28

Defines `resolve_existing_path` and its implementation control flow; direct static calls: FileSafetyError, exists, resolve_workspace_path.

### Lines 29–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–41

Defines `resolve_write_path` and its implementation control flow; direct static calls: FileSafetyError, exists, resolve.

### Lines 42–43

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 44–48

Defines `relative_path` and its implementation control flow; direct static calls: FileSafetyError, relative_to, resolve, str.

### Lines 49–50

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 51–56

Defines `is_runtime_path` and its implementation control flow; direct static calls: bool, relative_to, resolve.

### Lines 57–58

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 59–65

Defines `ensure_not_runtime_path` and its implementation control flow; direct static calls: FileSafetyError, is_file, is_runtime_path, lower, relative_path.

### Lines 66–67

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 68–94

Defines `ensure_text_file_safe` and its implementation control flow; direct static calls: FileSafetyError, decode, ensure_not_runtime_path, is_file, read_bytes, relative_path, stat, str.

### Lines 95–96

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 97–102

Defines `read_text_file_safe` and its implementation control flow; direct static calls: FileSafetyError, ensure_text_file_safe, read_text, resolve_existing_path, stat.

### Lines 103–104

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 105–108

Defines `ensure_write_target_safe` and its implementation control flow; direct static calls: ensure_not_runtime_path, resolve_write_path.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
