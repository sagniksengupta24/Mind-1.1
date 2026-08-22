# `mind01/receipts.py`

## File purpose

This persistence and traces file is reviewed at snapshot `3d0c62859e59e9fa32789dd3897948992f0bc0c08b7227786fb3ce8769e8e886`. It contains 515 lines.

## Imports and module state

- [mind01/receipts.py:1](../../../../mind01/receipts.py#L1) imports `__future__` / annotations.
- [mind01/receipts.py:3](../../../../mind01/receipts.py#L3) imports `hashlib`.
- [mind01/receipts.py:4](../../../../mind01/receipts.py#L4) imports `json`.
- [mind01/receipts.py:5](../../../../mind01/receipts.py#L5) imports `subprocess`.
- [mind01/receipts.py:6](../../../../mind01/receipts.py#L6) imports `time`.
- [mind01/receipts.py:7](../../../../mind01/receipts.py#L7) imports `uuid`.
- [mind01/receipts.py:8](../../../../mind01/receipts.py#L8) imports `dataclasses` / dataclass.
- [mind01/receipts.py:9](../../../../mind01/receipts.py#L9) imports `datetime` / datetime.
- [mind01/receipts.py:9](../../../../mind01/receipts.py#L9) imports `datetime` / timezone.
- [mind01/receipts.py:10](../../../../mind01/receipts.py#L10) imports `pathlib` / Path.
- [mind01/receipts.py:11](../../../../mind01/receipts.py#L11) imports `typing` / Callable.
- [mind01/receipts.py:13](../../../../mind01/receipts.py#L13) imports `file_safety` / FileSafetyError.
- [mind01/receipts.py:13](../../../../mind01/receipts.py#L13) imports `file_safety` / ensure_write_target_safe.
- [mind01/receipts.py:13](../../../../mind01/receipts.py#L13) imports `file_safety` / relative_path.
- [mind01/receipts.py:14](../../../../mind01/receipts.py#L14) imports `mutations` / MutationError.
- [mind01/receipts.py:14](../../../../mind01/receipts.py#L14) imports `mutations` / MutationResult.
- [mind01/receipts.py:14](../../../../mind01/receipts.py#L14) imports `mutations` / execute_content_mutation.
- [mind01/receipts.py:15](../../../../mind01/receipts.py#L15) imports `locking` / file_lock.
- [mind01/receipts.py:16](../../../../mind01/receipts.py#L16) imports `traces` / TraceError.
- [mind01/receipts.py:16](../../../../mind01/receipts.py#L16) imports `traces` / TraceStore.
- [mind01/receipts.py:16](../../../../mind01/receipts.py#L16) imports `traces` / sanitize_args.
- [mind01/receipts.py:16](../../../../mind01/receipts.py#L16) imports `traces` / trace_event_base.

## Symbols

### `mind01.receipts.ReceiptError` — lines 19–20

- Source: [mind01/receipts.py:19](../../../../mind01/receipts.py#L19)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptContext` — lines 24–30

- Source: [mind01/receipts.py:24](../../../../mind01/receipts.py#L24)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore` — lines 33–284

- Source: [mind01/receipts.py:33](../../../../mind01/receipts.py#L33)
- Type: class
- Signature: `n/a`
- Direct static callees: `ReceiptContext`, `ReceiptError`, `TraceStore`, `_receipt_path`, `_resolve_original_backup`, `_trace_required`, `_write_receipt_unlocked`, `append`, `bool`, `canonical_json`, `dump`, `dumps`, `ensure_write_target_safe`, `exists`, `file_lock`, `fileno`, `flush`, `fsync`, `get`, `glob`, `hexdigest`, `is_file`, `isinstance`, `join`, `len`, `list`, `loads`, `mkdir`, `open`, `perform_verified_content_mutation`, `print`, `read_text`, `replace`, `resolve`, `sanitize_args`, `sha256`, `sha256_file`, `sorted`, `startswith`, `str`, `trace_event_base`, `unlink`, `uuid4`, `validate_rollback_source`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.__init__` — lines 34–39

- Source: [mind01/receipts.py:34](../../../../mind01/receipts.py#L34)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.list` — lines 41–53

- Source: [mind01/receipts.py:41](../../../../mind01/receipts.py#L41)
- Type: method
- Signature: `self, limit: int=50`
- Direct static callees: `append`, `glob`, `len`, `loads`, `read_text`, `sorted`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.get` — lines 55–65

- Source: [mind01/receipts.py:55](../../../../mind01/receipts.py#L55)
- Type: method
- Signature: `self, receipt_id: str`
- Direct static callees: `ReceiptError`, `_receipt_path`, `exists`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.render_list` — lines 67–76

- Source: [mind01/receipts.py:67](../../../../mind01/receipts.py#L67)
- Type: method
- Signature: `self, limit: int=50`
- Direct static callees: `get`, `join`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.render_show` — lines 78–79

- Source: [mind01/receipts.py:78](../../../../mind01/receipts.py#L78)
- Type: method
- Signature: `self, receipt_id: str`
- Direct static callees: `dumps`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.rollback` — lines 81–150

- Source: [mind01/receipts.py:81](../../../../mind01/receipts.py#L81)
- Type: method
- Signature: `self, receipt_id: str, *, mode: str, approved: bool, force: bool=False, source: str='rollback'`
- Direct static callees: `ReceiptContext`, `ReceiptError`, `_resolve_original_backup`, `_trace_required`, `bool`, `ensure_write_target_safe`, `exists`, `get`, `perform_verified_content_mutation`, `read_text`, `sanitize_args`, `sha256_file`, `str`, `trace_event_base`, `validate_rollback_source`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore.write_receipt` — lines 152–154

- Source: [mind01/receipts.py:152](../../../../mind01/receipts.py#L152)
- Type: method
- Signature: `self, receipt: dict`
- Direct static callees: `_write_receipt_unlocked`, `file_lock`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore._write_receipt_unlocked` — lines 156–259

- Source: [mind01/receipts.py:156](../../../../mind01/receipts.py#L156)
- Type: method
- Signature: `self, receipt: dict`
- Direct static callees: `ReceiptError`, `_receipt_path`, `append`, `canonical_json`, `dump`, `exists`, `fileno`, `flush`, `fsync`, `get`, `glob`, `hexdigest`, `isinstance`, `len`, `loads`, `open`, `print`, `read_text`, `replace`, `sha256`, `sorted`, `startswith`, `str`, `unlink`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore._receipt_path` — lines 261–264

- Source: [mind01/receipts.py:261](../../../../mind01/receipts.py#L261)
- Type: method
- Signature: `self, receipt_id: str`
- Direct static callees: `ReceiptError`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore._resolve_original_backup` — lines 266–278

- Source: [mind01/receipts.py:266](../../../../mind01/receipts.py#L266)
- Type: method
- Signature: `self, receipt: dict, receipt_id: str`
- Direct static callees: `ReceiptError`, `bool`, `get`, `is_file`, `isinstance`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.ReceiptStore._trace_required` — lines 280–284

- Source: [mind01/receipts.py:280](../../../../mind01/receipts.py#L280)
- Type: method
- Signature: `self, event: dict`
- Direct static callees: `ReceiptError`, `TraceStore`, `append`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.perform_verified_file_mutation` — lines 287–296

- Source: [mind01/receipts.py:287](../../../../mind01/receipts.py#L287)
- Type: function
- Signature: `workspace: Path, raw_path: str, context: ReceiptContext, mutator: Callable[[Path], None], after_must_exist: bool=True`
- Direct static callees: `ReceiptError`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.perform_verified_content_mutation` — lines 299–370

- Source: [mind01/receipts.py:299](../../../../mind01/receipts.py#L299)
- Type: function
- Signature: `workspace: Path, raw_path: str, context: ReceiptContext, content: str | None, *, delete: bool=False`
- Direct static callees: `ReceiptError`, `ReceiptStore`, `ensure_write_target_safe`, `execute_content_mutation`, `git_status_summary`, `isoformat`, `make_receipt_id`, `now`, `relative_path`, `resolve`, `str`, `write_receipt`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.validate_rollback_source` — lines 373–385

- Source: [mind01/receipts.py:373](../../../../mind01/receipts.py#L373)
- Type: function
- Signature: `receipt: dict, receipt_id: str`
- Direct static callees: `ReceiptError`, `get`, `isinstance`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.make_receipt_id` — lines 388–390

- Source: [mind01/receipts.py:388](../../../../mind01/receipts.py#L388)
- Type: function
- Signature: `operation_type: str`
- Direct static callees: `now`, `strftime`, `time_ns`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.sha256_file` — lines 393–398

- Source: [mind01/receipts.py:393](../../../../mind01/receipts.py#L393)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `iter`, `open`, `read`, `sha256`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.git_status_summary` — lines 401–415

- Source: [mind01/receipts.py:401](../../../../mind01/receipts.py#L401)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `run`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.canonical_json` — lines 418–428

- Source: [mind01/receipts.py:418](../../../../mind01/receipts.py#L418)
- Type: function
- Signature: `data: dict`
- Direct static callees: `dumps`, `encode`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.receipts.verify_receipt_chain` — lines 431–515

- Source: [mind01/receipts.py:431](../../../../mind01/receipts.py#L431)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `ReceiptStore`, `add`, `canonical_json`, `exists`, `get`, `glob`, `hexdigest`, `len`, `loads`, `read_text`, `set`, `sha256`, `sorted`, `startswith`, `str`
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

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–20

Defines class `ReceiptError` and the behavior of its members.

### Lines 21–23

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 24–30

Defines class `ReceiptContext` and the behavior of its members.

### Lines 31–32

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 33–62

Defines class `ReceiptStore` and the behavior of its members.

### Lines 63–92

Defines class `ReceiptStore` and the behavior of its members.

### Lines 93–122

Defines class `ReceiptStore` and the behavior of its members.

### Lines 123–152

Defines class `ReceiptStore` and the behavior of its members.

### Lines 153–182

Defines class `ReceiptStore` and the behavior of its members.

### Lines 183–212

Defines class `ReceiptStore` and the behavior of its members.

### Lines 213–242

Defines class `ReceiptStore` and the behavior of its members.

### Lines 243–272

Defines class `ReceiptStore` and the behavior of its members.

### Lines 273–284

Defines class `ReceiptStore` and the behavior of its members.

### Lines 285–286

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 287–296

Defines `perform_verified_file_mutation` and its implementation control flow; direct static calls: ReceiptError.

### Lines 297–298

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 299–328

Defines `perform_verified_content_mutation` and its implementation control flow; direct static calls: ReceiptError, ReceiptStore, ensure_write_target_safe, execute_content_mutation, git_status_summary, isoformat, make_receipt_id, now, relative_path, resolve, str, write_receipt.

### Lines 329–358

Defines `perform_verified_content_mutation` and its implementation control flow; direct static calls: ReceiptError, ReceiptStore, ensure_write_target_safe, execute_content_mutation, git_status_summary, isoformat, make_receipt_id, now, relative_path, resolve, str, write_receipt.

### Lines 359–370

Defines `perform_verified_content_mutation` and its implementation control flow; direct static calls: ReceiptError, ReceiptStore, ensure_write_target_safe, execute_content_mutation, git_status_summary, isoformat, make_receipt_id, now, relative_path, resolve, str, write_receipt.

### Lines 371–372

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 373–385

Defines `validate_rollback_source` and its implementation control flow; direct static calls: ReceiptError, get, isinstance.

### Lines 386–387

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 388–390

Defines `make_receipt_id` and its implementation control flow; direct static calls: now, strftime, time_ns, uuid4.

### Lines 391–392

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 393–398

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, iter, open, read, sha256, update.

### Lines 399–400

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 401–415

Defines `git_status_summary` and its implementation control flow; direct static calls: run.

### Lines 416–417

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 418–428

Defines `canonical_json` and its implementation control flow; direct static calls: dumps, encode, items.

### Lines 429–430

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 431–460

Defines `verify_receipt_chain` and its implementation control flow; direct static calls: ReceiptStore, add, canonical_json, exists, get, glob, hexdigest, len, loads, read_text, set, sha256, sorted, startswith, str.

### Lines 461–490

Defines `verify_receipt_chain` and its implementation control flow; direct static calls: ReceiptStore, add, canonical_json, exists, get, glob, hexdigest, len, loads, read_text, set, sha256, sorted, startswith, str.

### Lines 491–515

Defines `verify_receipt_chain` and its implementation control flow; direct static calls: ReceiptStore, add, canonical_json, exists, get, glob, hexdigest, len, loads, read_text, set, sha256, sorted, startswith, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
