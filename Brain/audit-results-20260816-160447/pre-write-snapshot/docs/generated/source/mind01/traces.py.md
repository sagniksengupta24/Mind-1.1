# `mind01/traces.py`

## File purpose

This persistence and traces file is reviewed at snapshot `44dd539f852b740b6426960529d05ee295e920ee0e5f8d8de71291562db7d32e`. It contains 352 lines.

## Imports and module state

- [mind01/traces.py:1](../../../../mind01/traces.py#L1) imports `__future__` / annotations.
- [mind01/traces.py:3](../../../../mind01/traces.py#L3) imports `hashlib`.
- [mind01/traces.py:4](../../../../mind01/traces.py#L4) imports `json`.
- [mind01/traces.py:5](../../../../mind01/traces.py#L5) imports `re`.
- [mind01/traces.py:6](../../../../mind01/traces.py#L6) imports `time`.
- [mind01/traces.py:7](../../../../mind01/traces.py#L7) imports `uuid`.
- [mind01/traces.py:8](../../../../mind01/traces.py#L8) imports `datetime` / datetime.
- [mind01/traces.py:8](../../../../mind01/traces.py#L8) imports `datetime` / timezone.
- [mind01/traces.py:9](../../../../mind01/traces.py#L9) imports `pathlib` / Path.
- [mind01/traces.py:10](../../../../mind01/traces.py#L10) imports `typing` / Any.
- [mind01/traces.py:12](../../../../mind01/traces.py#L12) imports `security` / redact_secrets.
- [mind01/traces.py:13](../../../../mind01/traces.py#L13) imports `locking` / file_lock.

## Symbols

### `mind01.traces.RECEIPT_RE` — lines 16–16

- Source: [mind01/traces.py:16](../../../../mind01/traces.py#L16)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.SENSITIVE_ARG_NAMES` — lines 17–17

- Source: [mind01/traces.py:17](../../../../mind01/traces.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.CONTENT_ARG_NAMES` — lines 18–18

- Source: [mind01/traces.py:18](../../../../mind01/traces.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceError` — lines 21–22

- Source: [mind01/traces.py:21](../../../../mind01/traces.py#L21)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore` — lines 25–161

- Source: [mind01/traces.py:25](../../../../mind01/traces.py#L25)
- Type: class
- Signature: `n/a`
- Direct static callees: `TraceError`, `_append_unlocked`, `_daily_path`, `_get_last_event_hash_fallback`, `append`, `canonical_json`, `count_jsonl_lines`, `decode`, `dict`, `dumps`, `exists`, `file_lock`, `find_event`, `get`, `glob`, `hexdigest`, `isinstance`, `isoformat`, `join`, `list`, `loads`, `mkdir`, `now`, `open`, `read_text`, `readlines`, `relative_to`, `replace`, `resolve`, `reversed`, `setdefault`, `sha256`, `sorted`, `startswith`, `stat`, `str`, `strftime`, `strip`, `uuid4`, `write`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.__init__` — lines 26–29

- Source: [mind01/traces.py:26](../../../../mind01/traces.py#L26)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.append` — lines 31–33

- Source: [mind01/traces.py:31](../../../../mind01/traces.py#L31)
- Type: method
- Signature: `self, event: dict[str, Any]`
- Direct static callees: `_append_unlocked`, `file_lock`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore._append_unlocked` — lines 35–85

- Source: [mind01/traces.py:35](../../../../mind01/traces.py#L35)
- Type: method
- Signature: `self, event: dict[str, Any]`
- Direct static callees: `TraceError`, `_daily_path`, `_get_last_event_hash_fallback`, `canonical_json`, `dict`, `dumps`, `exists`, `hexdigest`, `isinstance`, `isoformat`, `loads`, `now`, `open`, `read_text`, `replace`, `setdefault`, `sha256`, `uuid4`, `write`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore._get_last_event_hash_fallback` — lines 87–104

- Source: [mind01/traces.py:87](../../../../mind01/traces.py#L87)
- Type: method
- Signature: `self`
- Direct static callees: `decode`, `glob`, `isinstance`, `loads`, `open`, `readlines`, `reversed`, `sorted`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.list` — lines 106–118

- Source: [mind01/traces.py:106](../../../../mind01/traces.py#L106)
- Type: method
- Signature: `self, limit: int=20`
- Direct static callees: `append`, `count_jsonl_lines`, `glob`, `relative_to`, `sorted`, `stat`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.render_list` — lines 120–127

- Source: [mind01/traces.py:120](../../../../mind01/traces.py#L120)
- Type: method
- Signature: `self, limit: int=20`
- Direct static callees: `join`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.render_show` — lines 129–143

- Source: [mind01/traces.py:129](../../../../mind01/traces.py#L129)
- Type: method
- Signature: `self, identifier: str`
- Direct static callees: `TraceError`, `dumps`, `exists`, `find_event`, `read_text`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore.find_event` — lines 145–157

- Source: [mind01/traces.py:145](../../../../mind01/traces.py#L145)
- Type: method
- Signature: `self, trace_id: str`
- Direct static callees: `get`, `glob`, `loads`, `open`, `sorted`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.TraceStore._daily_path` — lines 159–161

- Source: [mind01/traces.py:159](../../../../mind01/traces.py#L159)
- Type: method
- Signature: `self`
- Direct static callees: `now`, `strftime`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.trace_event_base` — lines 164–176

- Source: [mind01/traces.py:164](../../../../mind01/traces.py#L164)
- Type: function
- Signature: `*, event_type: str, mode: str, session_id: str | None=None, model_name: str | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.sanitize_args` — lines 179–195

- Source: [mind01/traces.py:179](../../../../mind01/traces.py#L179)
- Type: function
- Signature: `args: dict[str, Any]`
- Direct static callees: `any`, `dumps`, `isinstance`, `items`, `lower`, `redact_secrets`, `summarize_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.summarize_text` — lines 198–204

- Source: [mind01/traces.py:198](../../../../mind01/traces.py#L198)
- Type: function
- Signature: `text: str, limit: int=160`
- Direct static callees: `encode`, `hexdigest`, `len`, `redact_secrets`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.summarize_prompt` — lines 207–208

- Source: [mind01/traces.py:207](../../../../mind01/traces.py#L207)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `summarize_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.summarize_result` — lines 211–216

- Source: [mind01/traces.py:211](../../../../mind01/traces.py#L211)
- Type: function
- Signature: `text: str, limit: int=300`
- Direct static callees: `encode`, `len`, `redact_secrets`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.extract_receipt_id` — lines 219–223

- Source: [mind01/traces.py:219](../../../../mind01/traces.py#L219)
- Type: function
- Signature: `text: str`
- Direct static callees: `group`, `rstrip`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.count_jsonl_lines` — lines 226–231

- Source: [mind01/traces.py:226](../../../../mind01/traces.py#L226)
- Type: function
- Signature: `path: Path`
- Direct static callees: `open`, `strip`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.duration_ms` — lines 234–235

- Source: [mind01/traces.py:234](../../../../mind01/traces.py#L234)
- Type: function
- Signature: `start: float`
- Direct static callees: `int`, `perf_counter`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.traces.verify_trace_chain` — lines 238–352

- Source: [mind01/traces.py:238](../../../../mind01/traces.py#L238)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `TraceStore`, `canonical_json`, `exists`, `get`, `glob`, `hexdigest`, `loads`, `open`, `read_text`, `sha256`, `sorted`, `strip`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–16

Implements module-level `Assign` behavior or data.

### Lines 17–17

Implements module-level `Assign` behavior or data.

### Lines 18–18

Implements module-level `Assign` behavior or data.

### Lines 19–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–22

Defines class `TraceError` and the behavior of its members.

### Lines 23–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–54

Defines class `TraceStore` and the behavior of its members.

### Lines 55–84

Defines class `TraceStore` and the behavior of its members.

### Lines 85–114

Defines class `TraceStore` and the behavior of its members.

### Lines 115–144

Defines class `TraceStore` and the behavior of its members.

### Lines 145–161

Defines class `TraceStore` and the behavior of its members.

### Lines 162–163

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 164–176

Defines `trace_event_base` and its implementation control flow; direct static calls: none resolved.

### Lines 177–178

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 179–195

Defines `sanitize_args` and its implementation control flow; direct static calls: any, dumps, isinstance, items, lower, redact_secrets, summarize_text.

### Lines 196–197

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 198–204

Defines `summarize_text` and its implementation control flow; direct static calls: encode, hexdigest, len, redact_secrets, sha256.

### Lines 205–206

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 207–208

Defines `summarize_prompt` and its implementation control flow; direct static calls: summarize_text.

### Lines 209–210

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 211–216

Defines `summarize_result` and its implementation control flow; direct static calls: encode, len, redact_secrets.

### Lines 217–218

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 219–223

Defines `extract_receipt_id` and its implementation control flow; direct static calls: group, rstrip, search.

### Lines 224–225

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 226–231

Defines `count_jsonl_lines` and its implementation control flow; direct static calls: open, strip, sum.

### Lines 232–233

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 234–235

Defines `duration_ms` and its implementation control flow; direct static calls: int, perf_counter.

### Lines 236–237

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 238–267

Defines `verify_trace_chain` and its implementation control flow; direct static calls: TraceStore, canonical_json, exists, get, glob, hexdigest, loads, open, read_text, sha256, sorted, strip.

### Lines 268–297

Defines `verify_trace_chain` and its implementation control flow; direct static calls: TraceStore, canonical_json, exists, get, glob, hexdigest, loads, open, read_text, sha256, sorted, strip.

### Lines 298–327

Defines `verify_trace_chain` and its implementation control flow; direct static calls: TraceStore, canonical_json, exists, get, glob, hexdigest, loads, open, read_text, sha256, sorted, strip.

### Lines 328–352

Defines `verify_trace_chain` and its implementation control flow; direct static calls: TraceStore, canonical_json, exists, get, glob, hexdigest, loads, open, read_text, sha256, sorted, strip.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
