# `tests/test_audit_chains.py`

## File purpose

This testing file is reviewed at snapshot `32ce7ffb594082632564b229248dad13d6d803100a24feba7652c5b4842ebb99`. It contains 452 lines.

## Imports and module state

- [tests/test_audit_chains.py:1](../../../../tests/test_audit_chains.py#L1) imports `__future__` / annotations.
- [tests/test_audit_chains.py:3](../../../../tests/test_audit_chains.py#L3) imports `json`.
- [tests/test_audit_chains.py:4](../../../../tests/test_audit_chains.py#L4) imports `shutil`.
- [tests/test_audit_chains.py:5](../../../../tests/test_audit_chains.py#L5) imports `tempfile`.
- [tests/test_audit_chains.py:6](../../../../tests/test_audit_chains.py#L6) imports `pathlib` / Path.
- [tests/test_audit_chains.py:7](../../../../tests/test_audit_chains.py#L7) imports `uuid`.
- [tests/test_audit_chains.py:9](../../../../tests/test_audit_chains.py#L9) imports `mind01.receipts` / ReceiptStore.
- [tests/test_audit_chains.py:9](../../../../tests/test_audit_chains.py#L9) imports `mind01.receipts` / verify_receipt_chain.
- [tests/test_audit_chains.py:10](../../../../tests/test_audit_chains.py#L10) imports `mind01.traces` / TraceStore.
- [tests/test_audit_chains.py:10](../../../../tests/test_audit_chains.py#L10) imports `mind01.traces` / verify_trace_chain.
- [tests/test_audit_chains.py:11](../../../../tests/test_audit_chains.py#L11) imports `mind01.mutations` / DirtyStateStore.
- [tests/test_audit_chains.py:11](../../../../tests/test_audit_chains.py#L11) imports `mind01.mutations` / FileState.
- [tests/test_audit_chains.py:12](../../../../tests/test_audit_chains.py#L12) imports `mind01.api` / MindAPI.
- [tests/test_audit_chains.py:13](../../../../tests/test_audit_chains.py#L13) imports `test_api` / request_json.

## Symbols

### `tests.test_audit_chains.run_audit_chain_tests` — lines 16–444

- Source: [tests/test_audit_chains.py:16](../../../../tests/test_audit_chains.py#L16)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `DirtyStateStore`, `FileState`, `MindAPI`, `OSError`, `Path`, `ReceiptStore`, `StringIO`, `TraceStore`, `append`, `create`, `dumps`, `endswith`, `exists`, `get`, `getvalue`, `glob`, `join`, `len`, `list`, `loads`, `mkdir`, `mkdtemp`, `original_replace`, `read_text`, `request_json`, `rmtree`, `splitlines`, `str`, `unlink`, `verify_receipt_chain`, `verify_trace_chain`, `write_receipt`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_audit_chains.test_audit_chain_regressions` — lines 451–452

- Source: [tests/test_audit_chains.py:451](../../../../tests/test_audit_chains.py#L451)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_audit_chain_tests`
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

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–45

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 46–75

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 76–105

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 106–135

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 136–165

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 166–195

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 196–225

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 226–255

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 256–285

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 286–315

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 316–345

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 346–375

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 376–405

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 406–435

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 436–444

Defines `run_audit_chain_tests` and its implementation control flow; direct static calls: AssertionError, DirtyStateStore, FileState, MindAPI, OSError, Path, ReceiptStore, StringIO, TraceStore, append, create, dumps, endswith, exists, get, getvalue, glob, join, len, list, loads, mkdir, mkdtemp, original_replace, read_text, request_json, rmtree, splitlines, str, unlink, verify_receipt_chain, verify_trace_chain, write_receipt, write_text.

### Lines 445–446

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 447–448

Implements module-level `If` behavior or data.

### Lines 449–450

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 451–452

Defines `test_audit_chain_regressions` and its implementation control flow; direct static calls: run_audit_chain_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
