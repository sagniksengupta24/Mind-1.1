# `tests/test_mutation_transactions.py`

## File purpose

This testing file is reviewed at snapshot `95b8c03dcc32086e5211565495bba1cd71ba2e4c5a0c2f8d6d34c85cc28681b2`. It contains 249 lines.

## Imports and module state

- [tests/test_mutation_transactions.py:1](../../../../tests/test_mutation_transactions.py#L1) imports `__future__` / annotations.
- [tests/test_mutation_transactions.py:3](../../../../tests/test_mutation_transactions.py#L3) imports `contextlib`.
- [tests/test_mutation_transactions.py:4](../../../../tests/test_mutation_transactions.py#L4) imports `io`.
- [tests/test_mutation_transactions.py:5](../../../../tests/test_mutation_transactions.py#L5) imports `json`.
- [tests/test_mutation_transactions.py:6](../../../../tests/test_mutation_transactions.py#L6) imports `shutil`.
- [tests/test_mutation_transactions.py:7](../../../../tests/test_mutation_transactions.py#L7) imports `tempfile`.
- [tests/test_mutation_transactions.py:8](../../../../tests/test_mutation_transactions.py#L8) imports `pathlib` / Path.
- [tests/test_mutation_transactions.py:10](../../../../tests/test_mutation_transactions.py#L10) imports `mind01.mutations`.
- [tests/test_mutation_transactions.py:11](../../../../tests/test_mutation_transactions.py#L11) imports `mind01.cli` / main.
- [tests/test_mutation_transactions.py:12](../../../../tests/test_mutation_transactions.py#L12) imports `mind01.patches` / PatchError.
- [tests/test_mutation_transactions.py:12](../../../../tests/test_mutation_transactions.py#L12) imports `mind01.patches` / PatchStore.
- [tests/test_mutation_transactions.py:13](../../../../tests/test_mutation_transactions.py#L13) imports `mind01.receipts` / ReceiptError.
- [tests/test_mutation_transactions.py:13](../../../../tests/test_mutation_transactions.py#L13) imports `mind01.receipts` / ReceiptStore.
- [tests/test_mutation_transactions.py:13](../../../../tests/test_mutation_transactions.py#L13) imports `mind01.receipts` / sha256_file.
- [tests/test_mutation_transactions.py:14](../../../../tests/test_mutation_transactions.py#L14) imports `mind01.tools` / ToolError.
- [tests/test_mutation_transactions.py:14](../../../../tests/test_mutation_transactions.py#L14) imports `mind01.tools` / ToolRegistry.

## Symbols

### `tests.test_mutation_transactions.run_mutation_transaction_tests` — lines 17–24

- Source: [tests/test_mutation_transactions.py:17](../../../../tests/test_mutation_transactions.py#L17)
- Type: function
- Signature: `n/a`
- Direct static callees: `test_dirty_cli_commands`, `test_failure_before_replace_leaves_original_unchanged`, `test_patch_apply_validation_and_restore`, `test_receipt_failure_after_replace_restores_and_has_no_success_receipt`, `test_restore_failure_creates_dirty_record`, `test_rollback_transaction_and_hash_policy`, `test_write_and_edit_transaction_success`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_write_and_edit_transaction_success` — lines 27–47

- Source: [tests/test_mutation_transactions.py:27](../../../../tests/test_mutation_transactions.py#L27)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `ReceiptStore`, `ToolRegistry`, `call`, `exists`, `list`, `mkdtemp`, `read_text`, `rmtree`, `sha256_file`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_failure_before_replace_leaves_original_unchanged` — lines 50–72

- Source: [tests/test_mutation_transactions.py:50](../../../../tests/test_mutation_transactions.py#L50)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `MutationError`, `Path`, `ReceiptStore`, `ToolRegistry`, `call`, `list`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_receipt_failure_after_replace_restores_and_has_no_success_receipt` — lines 75–97

- Source: [tests/test_mutation_transactions.py:75](../../../../tests/test_mutation_transactions.py#L75)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `ReceiptError`, `ReceiptStore`, `ToolRegistry`, `call`, `list`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_restore_failure_creates_dirty_record` — lines 100–134

- Source: [tests/test_mutation_transactions.py:100](../../../../tests/test_mutation_transactions.py#L100)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `DirtyStateStore`, `MutationError`, `Path`, `ReceiptError`, `ToolRegistry`, `call`, `len`, `list`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_rollback_transaction_and_hash_policy` — lines 137–168

- Source: [tests/test_mutation_transactions.py:137](../../../../tests/test_mutation_transactions.py#L137)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `ReceiptStore`, `ToolRegistry`, `call`, `list`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `rollback`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_patch_apply_validation_and_restore` — lines 171–214

- Source: [tests/test_mutation_transactions.py:171](../../../../tests/test_mutation_transactions.py#L171)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `PatchStore`, `Path`, `ReceiptError`, `apply`, `dumps`, `mkdir`, `mkdtemp`, `propose_edit`, `read_text`, `rmtree`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.test_dirty_cli_commands` — lines 217–240

- Source: [tests/test_mutation_transactions.py:217](../../../../tests/test_mutation_transactions.py#L217)
- Type: function
- Signature: `n/a`
- Direct static callees: `DirtyStateStore`, `FileState`, `Path`, `create`, `loads`, `mkdir`, `mkdtemp`, `rmtree`, `run_cli_capture`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_mutation_transactions.run_cli_capture` — lines 243–249

- Source: [tests/test_mutation_transactions.py:243](../../../../tests/test_mutation_transactions.py#L243)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `StringIO`, `cli_main`, `getvalue`, `redirect_stderr`, `redirect_stdout`
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

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–24

Defines `run_mutation_transaction_tests` and its implementation control flow; direct static calls: test_dirty_cli_commands, test_failure_before_replace_leaves_original_unchanged, test_patch_apply_validation_and_restore, test_receipt_failure_after_replace_restores_and_has_no_success_receipt, test_restore_failure_creates_dirty_record, test_rollback_transaction_and_hash_policy, test_write_and_edit_transaction_success.

### Lines 25–26

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 27–47

Defines `test_write_and_edit_transaction_success` and its implementation control flow; direct static calls: Path, ReceiptStore, ToolRegistry, call, exists, list, mkdtemp, read_text, rmtree, sha256_file.

### Lines 48–49

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 50–72

Defines `test_failure_before_replace_leaves_original_unchanged` and its implementation control flow; direct static calls: AssertionError, MutationError, Path, ReceiptStore, ToolRegistry, call, list, mkdir, mkdtemp, read_text, rmtree, str, write_text.

### Lines 73–74

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 75–97

Defines `test_receipt_failure_after_replace_restores_and_has_no_success_receipt` and its implementation control flow; direct static calls: AssertionError, Path, ReceiptError, ReceiptStore, ToolRegistry, call, list, mkdir, mkdtemp, read_text, rmtree, str, write_text.

### Lines 98–99

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 100–129

Defines `test_restore_failure_creates_dirty_record` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, MutationError, Path, ReceiptError, ToolRegistry, call, len, list, mkdir, mkdtemp, read_text, rmtree, str, write_text.

### Lines 130–134

Defines `test_restore_failure_creates_dirty_record` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, MutationError, Path, ReceiptError, ToolRegistry, call, len, list, mkdir, mkdtemp, read_text, rmtree, str, write_text.

### Lines 135–136

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 137–166

Defines `test_rollback_transaction_and_hash_policy` and its implementation control flow; direct static calls: AssertionError, Path, ReceiptStore, ToolRegistry, call, list, mkdir, mkdtemp, read_text, rmtree, rollback, str, write_text.

### Lines 167–168

Defines `test_rollback_transaction_and_hash_policy` and its implementation control flow; direct static calls: AssertionError, Path, ReceiptStore, ToolRegistry, call, list, mkdir, mkdtemp, read_text, rmtree, rollback, str, write_text.

### Lines 169–170

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 171–200

Defines `test_patch_apply_validation_and_restore` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, apply, dumps, mkdir, mkdtemp, propose_edit, read_text, rmtree, str, write_text.

### Lines 201–214

Defines `test_patch_apply_validation_and_restore` and its implementation control flow; direct static calls: AssertionError, PatchStore, Path, ReceiptError, apply, dumps, mkdir, mkdtemp, propose_edit, read_text, rmtree, str, write_text.

### Lines 215–216

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 217–240

Defines `test_dirty_cli_commands` and its implementation control flow; direct static calls: DirtyStateStore, FileState, Path, create, loads, mkdir, mkdtemp, rmtree, run_cli_capture, str, write_text.

### Lines 241–242

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 243–249

Defines `run_cli_capture` and its implementation control flow; direct static calls: StringIO, cli_main, getvalue, redirect_stderr, redirect_stdout.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
