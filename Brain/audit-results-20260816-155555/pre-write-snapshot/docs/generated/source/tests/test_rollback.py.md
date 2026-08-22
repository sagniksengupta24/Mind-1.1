# `tests/test_rollback.py`

## File purpose

This testing file is reviewed at snapshot `e54d8abd3b355c6bc9e74ab017424e25c3027a838f2fb9f911c66bf82d295121`. It contains 159 lines.

## Imports and module state

- [tests/test_rollback.py:1](../../../../tests/test_rollback.py#L1) imports `__future__` / annotations.
- [tests/test_rollback.py:3](../../../../tests/test_rollback.py#L3) imports `contextlib`.
- [tests/test_rollback.py:4](../../../../tests/test_rollback.py#L4) imports `io`.
- [tests/test_rollback.py:5](../../../../tests/test_rollback.py#L5) imports `shutil`.
- [tests/test_rollback.py:6](../../../../tests/test_rollback.py#L6) imports `tempfile`.
- [tests/test_rollback.py:7](../../../../tests/test_rollback.py#L7) imports `pathlib` / Path.
- [tests/test_rollback.py:9](../../../../tests/test_rollback.py#L9) imports `mind01.cli` / main.
- [tests/test_rollback.py:10](../../../../tests/test_rollback.py#L10) imports `mind01.receipts` / ReceiptStore.
- [tests/test_rollback.py:10](../../../../tests/test_rollback.py#L10) imports `mind01.receipts` / sha256_file.
- [tests/test_rollback.py:11](../../../../tests/test_rollback.py#L11) imports `mind01.tools` / ToolRegistry.

## Symbols

### `tests.test_rollback.run_rollback_tests` — lines 14–135

- Source: [tests/test_rollback.py:14](../../../../tests/test_rollback.py#L14)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `ReceiptStore`, `ToolRegistry`, `call`, `exists`, `latest_receipt`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `run_cli_capture`, `run_cli_capture_code`, `sha256_file`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rollback.latest_receipt` — lines 138–141

- Source: [tests/test_rollback.py:138](../../../../tests/test_rollback.py#L138)
- Type: function
- Signature: `store: ReceiptStore`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rollback.run_cli_capture` — lines 144–147

- Source: [tests/test_rollback.py:144](../../../../tests/test_rollback.py#L144)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `run_cli_capture_code`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rollback.run_cli_capture_code` — lines 150–155

- Source: [tests/test_rollback.py:150](../../../../tests/test_rollback.py#L150)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `StringIO`, `cli_main`, `getvalue`, `redirect_stderr`, `redirect_stdout`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rollback.test_rollback_regressions` — lines 158–159

- Source: [tests/test_rollback.py:158](../../../../tests/test_rollback.py#L158)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_rollback_tests`
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

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–43

Defines `run_rollback_tests` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, latest_receipt, mkdir, mkdtemp, read_text, rmtree, run_cli_capture, run_cli_capture_code, sha256_file, str, write_text.

### Lines 44–73

Defines `run_rollback_tests` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, latest_receipt, mkdir, mkdtemp, read_text, rmtree, run_cli_capture, run_cli_capture_code, sha256_file, str, write_text.

### Lines 74–103

Defines `run_rollback_tests` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, latest_receipt, mkdir, mkdtemp, read_text, rmtree, run_cli_capture, run_cli_capture_code, sha256_file, str, write_text.

### Lines 104–133

Defines `run_rollback_tests` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, latest_receipt, mkdir, mkdtemp, read_text, rmtree, run_cli_capture, run_cli_capture_code, sha256_file, str, write_text.

### Lines 134–135

Defines `run_rollback_tests` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, latest_receipt, mkdir, mkdtemp, read_text, rmtree, run_cli_capture, run_cli_capture_code, sha256_file, str, write_text.

### Lines 136–137

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 138–141

Defines `latest_receipt` and its implementation control flow; direct static calls: list.

### Lines 142–143

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 144–147

Defines `run_cli_capture` and its implementation control flow; direct static calls: run_cli_capture_code.

### Lines 148–149

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 150–155

Defines `run_cli_capture_code` and its implementation control flow; direct static calls: StringIO, cli_main, getvalue, redirect_stderr, redirect_stdout.

### Lines 156–157

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 158–159

Defines `test_rollback_regressions` and its implementation control flow; direct static calls: run_rollback_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
