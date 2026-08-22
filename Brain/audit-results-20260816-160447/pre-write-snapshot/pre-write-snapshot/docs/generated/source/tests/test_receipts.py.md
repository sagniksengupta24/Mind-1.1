# `tests/test_receipts.py`

## File purpose

This testing file is reviewed at snapshot `470fbf2cf99ee6a59f15ee84444ec46114e9a14adaaf0b30cc1c96168937bf9c`. It contains 124 lines.

## Imports and module state

- [tests/test_receipts.py:1](../../../../tests/test_receipts.py#L1) imports `__future__` / annotations.
- [tests/test_receipts.py:3](../../../../tests/test_receipts.py#L3) imports `contextlib`.
- [tests/test_receipts.py:4](../../../../tests/test_receipts.py#L4) imports `io`.
- [tests/test_receipts.py:5](../../../../tests/test_receipts.py#L5) imports `json`.
- [tests/test_receipts.py:6](../../../../tests/test_receipts.py#L6) imports `shutil`.
- [tests/test_receipts.py:7](../../../../tests/test_receipts.py#L7) imports `tempfile`.
- [tests/test_receipts.py:8](../../../../tests/test_receipts.py#L8) imports `pathlib` / Path.
- [tests/test_receipts.py:10](../../../../tests/test_receipts.py#L10) imports `mind01.cli` / main.
- [tests/test_receipts.py:11](../../../../tests/test_receipts.py#L11) imports `mind01.patches` / PatchStore.
- [tests/test_receipts.py:12](../../../../tests/test_receipts.py#L12) imports `mind01.receipts` / ReceiptError.
- [tests/test_receipts.py:12](../../../../tests/test_receipts.py#L12) imports `mind01.receipts` / ReceiptStore.
- [tests/test_receipts.py:12](../../../../tests/test_receipts.py#L12) imports `mind01.receipts` / sha256_file.
- [tests/test_receipts.py:13](../../../../tests/test_receipts.py#L13) imports `mind01.tools` / ToolError.
- [tests/test_receipts.py:13](../../../../tests/test_receipts.py#L13) imports `mind01.tools` / ToolRegistry.

## Symbols

### `tests.test_receipts.run_receipt_tests` — lines 16–106

- Source: [tests/test_receipts.py:16](../../../../tests/test_receipts.py#L16)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `PatchStore`, `Path`, `ReceiptError`, `ReceiptStore`, `ToolRegistry`, `apply`, `call`, `exists`, `latest_receipt`, `len`, `loads`, `mkdir`, `mkdtemp`, `propose_edit`, `rmtree`, `run_cli_capture`, `sha256_file`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_receipts.latest_receipt` — lines 109–112

- Source: [tests/test_receipts.py:109](../../../../tests/test_receipts.py#L109)
- Type: function
- Signature: `store: ReceiptStore`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_receipts.run_cli_capture` — lines 115–120

- Source: [tests/test_receipts.py:115](../../../../tests/test_receipts.py#L115)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `StringIO`, `cli_main`, `getvalue`, `redirect_stderr`, `redirect_stdout`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_receipts.test_receipt_regressions` — lines 123–124

- Source: [tests/test_receipts.py:123](../../../../tests/test_receipts.py#L123)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_receipt_tests`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–45

Defines `run_receipt_tests` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, ReceiptStore, ToolRegistry, apply, call, exists, latest_receipt, len, loads, mkdir, mkdtemp, propose_edit, rmtree, run_cli_capture, sha256_file, str.

### Lines 46–75

Defines `run_receipt_tests` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, ReceiptStore, ToolRegistry, apply, call, exists, latest_receipt, len, loads, mkdir, mkdtemp, propose_edit, rmtree, run_cli_capture, sha256_file, str.

### Lines 76–105

Defines `run_receipt_tests` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, ReceiptStore, ToolRegistry, apply, call, exists, latest_receipt, len, loads, mkdir, mkdtemp, propose_edit, rmtree, run_cli_capture, sha256_file, str.

### Lines 106–106

Defines `run_receipt_tests` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, ReceiptStore, ToolRegistry, apply, call, exists, latest_receipt, len, loads, mkdir, mkdtemp, propose_edit, rmtree, run_cli_capture, sha256_file, str.

### Lines 107–108

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 109–112

Defines `latest_receipt` and its implementation control flow; direct static calls: list.

### Lines 113–114

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 115–120

Defines `run_cli_capture` and its implementation control flow; direct static calls: StringIO, cli_main, getvalue, redirect_stderr, redirect_stdout.

### Lines 121–122

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 123–124

Defines `test_receipt_regressions` and its implementation control flow; direct static calls: run_receipt_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
