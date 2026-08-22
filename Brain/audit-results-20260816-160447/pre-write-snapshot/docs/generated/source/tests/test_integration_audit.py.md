# `tests/test_integration_audit.py`

## File purpose

This testing file is reviewed at snapshot `3a5cb65b9dae9a1e9f39e92e461049bf50d6e105c6a172f0d5c7ccd7b68c8f44`. It contains 108 lines.

## Imports and module state

- [tests/test_integration_audit.py:1](../../../../tests/test_integration_audit.py#L1) imports `__future__` / annotations.
- [tests/test_integration_audit.py:3](../../../../tests/test_integration_audit.py#L3) imports `shutil`.
- [tests/test_integration_audit.py:4](../../../../tests/test_integration_audit.py#L4) imports `tempfile`.
- [tests/test_integration_audit.py:5](../../../../tests/test_integration_audit.py#L5) imports `pathlib` / Path.
- [tests/test_integration_audit.py:7](../../../../tests/test_integration_audit.py#L7) imports `mind01.patches` / PatchError.
- [tests/test_integration_audit.py:7](../../../../tests/test_integration_audit.py#L7) imports `mind01.patches` / PatchStore.
- [tests/test_integration_audit.py:8](../../../../tests/test_integration_audit.py#L8) imports `mind01.receipts` / ReceiptError.
- [tests/test_integration_audit.py:8](../../../../tests/test_integration_audit.py#L8) imports `mind01.receipts` / ReceiptStore.
- [tests/test_integration_audit.py:9](../../../../tests/test_integration_audit.py#L9) imports `mind01.tools` / ToolError.
- [tests/test_integration_audit.py:9](../../../../tests/test_integration_audit.py#L9) imports `mind01.tools` / ToolRegistry.
- [tests/test_integration_audit.py:10](../../../../tests/test_integration_audit.py#L10) imports `mind01.traces` / TraceError.
- [tests/test_integration_audit.py:10](../../../../tests/test_integration_audit.py#L10) imports `mind01.traces` / TraceStore.

## Symbols

### `tests.test_integration_audit.run_integration_audit_tests` — lines 13–17

- Source: [tests/test_integration_audit.py:13](../../../../tests/test_integration_audit.py#L13)
- Type: function
- Signature: `n/a`
- Direct static callees: `test_required_trace_blocks_patch_apply`, `test_required_trace_blocks_rollback`, `test_required_trace_blocks_shell`, `test_required_trace_blocks_write_file`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_integration_audit.test_required_trace_blocks_write_file` — lines 20–34

- Source: [tests/test_integration_audit.py:20](../../../../tests/test_integration_audit.py#L20)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `ToolRegistry`, `call`, `exists`, `mkdtemp`, `rmtree`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_integration_audit.test_required_trace_blocks_shell` — lines 37–50

- Source: [tests/test_integration_audit.py:37](../../../../tests/test_integration_audit.py#L37)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `ToolRegistry`, `call`, `mkdtemp`, `rmtree`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_integration_audit.test_required_trace_blocks_patch_apply` — lines 53–76

- Source: [tests/test_integration_audit.py:53](../../../../tests/test_integration_audit.py#L53)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `PatchStore`, `Path`, `apply`, `mkdir`, `mkdtemp`, `propose_edit`, `read_text`, `rmtree`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_integration_audit.test_required_trace_blocks_rollback` — lines 79–104

- Source: [tests/test_integration_audit.py:79](../../../../tests/test_integration_audit.py#L79)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `ReceiptStore`, `ToolRegistry`, `call`, `list`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `rollback`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_integration_audit.failing_append` — lines 107–108

- Source: [tests/test_integration_audit.py:107](../../../../tests/test_integration_audit.py#L107)
- Type: function
- Signature: `self, event`
- Direct static callees: `TraceError`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–17

Defines `run_integration_audit_tests` and its implementation control flow; direct static calls: test_required_trace_blocks_patch_apply, test_required_trace_blocks_rollback, test_required_trace_blocks_shell, test_required_trace_blocks_write_file.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–34

Defines `test_required_trace_blocks_write_file` and its implementation control flow; direct static calls: AssertionError, Path, ToolRegistry, call, exists, mkdtemp, rmtree, str.

### Lines 35–36

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 37–50

Defines `test_required_trace_blocks_shell` and its implementation control flow; direct static calls: AssertionError, Path, ToolRegistry, call, mkdtemp, rmtree, str.

### Lines 51–52

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 53–76

Defines `test_required_trace_blocks_patch_apply` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, apply, mkdir, mkdtemp, propose_edit, read_text, rmtree, str, write_text.

### Lines 77–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–104

Defines `test_required_trace_blocks_rollback` and its implementation control flow; direct static calls: AssertionError, Path, ReceiptStore, ToolRegistry, call, list, mkdir, mkdtemp, read_text, rmtree, rollback, str, write_text.

### Lines 105–106

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 107–108

Defines `failing_append` and its implementation control flow; direct static calls: TraceError.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
