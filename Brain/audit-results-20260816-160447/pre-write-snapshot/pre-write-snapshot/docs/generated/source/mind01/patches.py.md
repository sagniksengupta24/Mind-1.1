# `mind01/patches.py`

## File purpose

This filesystem and mutations file is reviewed at snapshot `7ec6939c4ff01cb454018471f4602a20b1f3e67e8002c2625de0ef336fda50ab`. It contains 249 lines.

## Imports and module state

- [mind01/patches.py:1](../../../../mind01/patches.py#L1) imports `__future__` / annotations.
- [mind01/patches.py:3](../../../../mind01/patches.py#L3) imports `difflib`.
- [mind01/patches.py:4](../../../../mind01/patches.py#L4) imports `json`.
- [mind01/patches.py:5](../../../../mind01/patches.py#L5) imports `time`.
- [mind01/patches.py:6](../../../../mind01/patches.py#L6) imports `dataclasses` / dataclass.
- [mind01/patches.py:7](../../../../mind01/patches.py#L7) imports `pathlib` / Path.
- [mind01/patches.py:8](../../../../mind01/patches.py#L8) imports `typing` / Any.
- [mind01/patches.py:10](../../../../mind01/patches.py#L10) imports `file_safety` / FileSafetyError.
- [mind01/patches.py:10](../../../../mind01/patches.py#L10) imports `file_safety` / ensure_text_file_safe.
- [mind01/patches.py:10](../../../../mind01/patches.py#L10) imports `file_safety` / ensure_write_target_safe.
- [mind01/patches.py:10](../../../../mind01/patches.py#L10) imports `file_safety` / resolve_workspace_path.
- [mind01/patches.py:16](../../../../mind01/patches.py#L16) imports `receipts` / ReceiptContext.
- [mind01/patches.py:16](../../../../mind01/patches.py#L16) imports `receipts` / ReceiptError.
- [mind01/patches.py:16](../../../../mind01/patches.py#L16) imports `receipts` / perform_verified_content_mutation.
- [mind01/patches.py:17](../../../../mind01/patches.py#L17) imports `traces` / TraceError.
- [mind01/patches.py:17](../../../../mind01/patches.py#L17) imports `traces` / TraceStore.
- [mind01/patches.py:17](../../../../mind01/patches.py#L17) imports `traces` / sanitize_args.
- [mind01/patches.py:17](../../../../mind01/patches.py#L17) imports `traces` / trace_event_base.

## Symbols

### `mind01.patches.PatchError` — lines 20–21

- Source: [mind01/patches.py:20](../../../../mind01/patches.py#L20)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchProposal` — lines 25–58

- Source: [mind01/patches.py:25](../../../../mind01/patches.py#L25)
- Type: class
- Signature: `n/a`
- Direct static callees: `cls`, `get`, `int`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchProposal.from_dict` — lines 36–46

- Source: [mind01/patches.py:36](../../../../mind01/patches.py#L36)
- Type: method
- Signature: `cls, data: dict[str, Any]`
- Direct static callees: `cls`, `get`, `int`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchProposal.to_dict` — lines 48–58

- Source: [mind01/patches.py:48](../../../../mind01/patches.py#L48)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore` — lines 61–249

- Source: [mind01/patches.py:61](../../../../mind01/patches.py#L61)
- Type: class
- Signature: `n/a`
- Direct static callees: `PatchError`, `PatchProposal`, `ReceiptContext`, `TraceStore`, `_append`, `_ensure_text`, `_new`, `_read`, `_remove`, `_resolve`, `_resolve_existing_text`, `_resolve_write`, `_trace_required`, `_write`, `append`, `dumps`, `ensure_text_file_safe`, `ensure_write_target_safe`, `exists`, `from_dict`, `get`, `int`, `join`, `list`, `loads`, `max`, `mkdir`, `perform_verified_content_mutation`, `read_text`, `replace`, `resolve`, `resolve_workspace_path`, `sanitize_args`, `splitlines`, `str`, `time`, `to_dict`, `trace_event_base`, `unified_diff`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.__init__` — lines 62–65

- Source: [mind01/patches.py:62](../../../../mind01/patches.py#L62)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.propose_write` — lines 67–72

- Source: [mind01/patches.py:67](../../../../mind01/patches.py#L67)
- Type: method
- Signature: `self, path: str, content: str, reason: str=''`
- Direct static callees: `_append`, `_new`, `_resolve_write`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.propose_edit` — lines 74–85

- Source: [mind01/patches.py:74](../../../../mind01/patches.py#L74)
- Type: method
- Signature: `self, path: str, old: str, new: str, reason: str=''`
- Direct static callees: `PatchError`, `_append`, `_new`, `_resolve_existing_text`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.list` — lines 87–88

- Source: [mind01/patches.py:87](../../../../mind01/patches.py#L87)
- Type: method
- Signature: `self`
- Direct static callees: `_read`, `from_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.get` — lines 90–94

- Source: [mind01/patches.py:90](../../../../mind01/patches.py#L90)
- Type: method
- Signature: `self, patch_id: int`
- Direct static callees: `PatchError`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.show` — lines 96–122

- Source: [mind01/patches.py:96](../../../../mind01/patches.py#L96)
- Type: method
- Signature: `self, patch_id: int`
- Direct static callees: `PatchError`, `_ensure_text`, `_resolve`, `exists`, `get`, `join`, `read_text`, `replace`, `splitlines`, `unified_diff`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.apply` — lines 124–179

- Source: [mind01/patches.py:124](../../../../mind01/patches.py#L124)
- Type: method
- Signature: `self, patch_id: int, mode: str='write-approved', allow_write: bool=False, approved: bool=False, source: str='patch_apply'`
- Direct static callees: `PatchError`, `ReceiptContext`, `_ensure_text`, `_remove`, `_resolve_write`, `_trace_required`, `get`, `perform_verified_content_mutation`, `read_text`, `replace`, `sanitize_args`, `str`, `trace_event_base`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.discard` — lines 181–184

- Source: [mind01/patches.py:181](../../../../mind01/patches.py#L181)
- Type: method
- Signature: `self, patch_id: int`
- Direct static callees: `_remove`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore.render_list` — lines 186–192

- Source: [mind01/patches.py:186](../../../../mind01/patches.py#L186)
- Type: method
- Signature: `self`
- Direct static callees: `join`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._new` — lines 194–203

- Source: [mind01/patches.py:194](../../../../mind01/patches.py#L194)
- Type: method
- Signature: `self, kind: str, path: str, reason: str`
- Direct static callees: `PatchProposal`, `int`, `list`, `max`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._append` — lines 205–208

- Source: [mind01/patches.py:205](../../../../mind01/patches.py#L205)
- Type: method
- Signature: `self, proposal: PatchProposal`
- Direct static callees: `_read`, `_write`, `append`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._remove` — lines 210–212

- Source: [mind01/patches.py:210](../../../../mind01/patches.py#L210)
- Type: method
- Signature: `self, patch_id: int`
- Direct static callees: `_read`, `_write`, `int`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._read` — lines 214–217

- Source: [mind01/patches.py:214](../../../../mind01/patches.py#L214)
- Type: method
- Signature: `self`
- Direct static callees: `exists`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._write` — lines 219–220

- Source: [mind01/patches.py:219](../../../../mind01/patches.py#L219)
- Type: method
- Signature: `self, items: list[dict[str, Any]]`
- Direct static callees: `dumps`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._resolve` — lines 222–226

- Source: [mind01/patches.py:222](../../../../mind01/patches.py#L222)
- Type: method
- Signature: `self, raw_path: str`
- Direct static callees: `PatchError`, `resolve_workspace_path`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._resolve_write` — lines 228–232

- Source: [mind01/patches.py:228](../../../../mind01/patches.py#L228)
- Type: method
- Signature: `self, raw_path: str`
- Direct static callees: `PatchError`, `ensure_write_target_safe`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._resolve_existing_text` — lines 234–237

- Source: [mind01/patches.py:234](../../../../mind01/patches.py#L234)
- Type: method
- Signature: `self, raw_path: str`
- Direct static callees: `_ensure_text`, `_resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._ensure_text` — lines 239–243

- Source: [mind01/patches.py:239](../../../../mind01/patches.py#L239)
- Type: method
- Signature: `self, path: Path, raw_path: str`
- Direct static callees: `PatchError`, `ensure_text_file_safe`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patches.PatchStore._trace_required` — lines 245–249

- Source: [mind01/patches.py:245](../../../../mind01/patches.py#L245)
- Type: method
- Signature: `self, event: dict[str, Any]`
- Direct static callees: `PatchError`, `TraceStore`, `append`
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

### Lines 10–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–21

Defines class `PatchError` and the behavior of its members.

### Lines 22–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–54

Defines class `PatchProposal` and the behavior of its members.

### Lines 55–58

Defines class `PatchProposal` and the behavior of its members.

### Lines 59–60

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 61–90

Defines class `PatchStore` and the behavior of its members.

### Lines 91–120

Defines class `PatchStore` and the behavior of its members.

### Lines 121–150

Defines class `PatchStore` and the behavior of its members.

### Lines 151–180

Defines class `PatchStore` and the behavior of its members.

### Lines 181–210

Defines class `PatchStore` and the behavior of its members.

### Lines 211–240

Defines class `PatchStore` and the behavior of its members.

### Lines 241–249

Defines class `PatchStore` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
