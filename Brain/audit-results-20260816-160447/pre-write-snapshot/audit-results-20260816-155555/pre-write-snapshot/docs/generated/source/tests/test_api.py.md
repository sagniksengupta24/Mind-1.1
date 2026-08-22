# `tests/test_api.py`

## File purpose

This testing file is reviewed at snapshot `d93a6939114363c7e7091ad467223af40282638840a7b6103cb2f31814a3ebcc`. It contains 237 lines.

## Imports and module state

- [tests/test_api.py:1](../../../../tests/test_api.py#L1) imports `__future__` / annotations.
- [tests/test_api.py:3](../../../../tests/test_api.py#L3) imports `json`.
- [tests/test_api.py:4](../../../../tests/test_api.py#L4) imports `shutil`.
- [tests/test_api.py:5](../../../../tests/test_api.py#L5) imports `tempfile`.
- [tests/test_api.py:6](../../../../tests/test_api.py#L6) imports `io` / BytesIO.
- [tests/test_api.py:7](../../../../tests/test_api.py#L7) imports `pathlib` / Path.
- [tests/test_api.py:8](../../../../tests/test_api.py#L8) imports `unittest.mock` / patch.
- [tests/test_api.py:9](../../../../tests/test_api.py#L9) imports `urllib.parse`.
- [tests/test_api.py:11](../../../../tests/test_api.py#L11) imports `mind01.api` / MindAPI.
- [tests/test_api.py:12](../../../../tests/test_api.py#L12) imports `mind01.modes` / AgentMode.

## Symbols

### `tests.test_api.run_api_tests` — lines 15–147

- Source: [tests/test_api.py:15](../../../../tests/test_api.py#L15)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `MindAPI`, `Path`, `_request_while_busy`, `_test_real_session_context`, `any`, `mkdir`, `mkdtemp`, `request_json`, `rmtree`, `str`, `urlencode`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api._test_real_session_context` — lines 150–178

- Source: [tests/test_api.py:150](../../../../tests/test_api.py#L150)
- Type: function
- Signature: `api: MindAPI`
- Direct static callees: `dumps`, `join`, `patch`, `request_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api._request_while_busy` — lines 181–190

- Source: [tests/test_api.py:181](../../../../tests/test_api.py#L181)
- Type: function
- Signature: `api: MindAPI, token: str`
- Direct static callees: `acquire`, `range`, `release`, `request_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.request_json` — lines 193–214

- Source: [tests/test_api.py:193](../../../../tests/test_api.py#L193)
- Type: function
- Signature: `api: MindAPI, method: str, path: str, token: str='', data: dict | None=None`
- Direct static callees: `FakeRequest`, `decode`, `dumps`, `encode`, `getvalue`, `handle_get`, `handle_post`, `len`, `loads`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.FakeRequest` — lines 217–233

- Source: [tests/test_api.py:217](../../../../tests/test_api.py#L217)
- Type: class
- Signature: `n/a`
- Direct static callees: `BytesIO`, `append`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.FakeRequest.__init__` — lines 218–224

- Source: [tests/test_api.py:218](../../../../tests/test_api.py#L218)
- Type: method
- Signature: `self, path: str, headers: dict[str, str], body: bytes`
- Direct static callees: `BytesIO`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.FakeRequest.send_response` — lines 226–227

- Source: [tests/test_api.py:226](../../../../tests/test_api.py#L226)
- Type: method
- Signature: `self, status: int`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.FakeRequest.send_header` — lines 229–230

- Source: [tests/test_api.py:229](../../../../tests/test_api.py#L229)
- Type: method
- Signature: `self, key: str, value: str`
- Direct static callees: `append`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.FakeRequest.end_headers` — lines 232–233

- Source: [tests/test_api.py:232](../../../../tests/test_api.py#L232)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_api.test_api_security_and_sessions` — lines 236–237

- Source: [tests/test_api.py:236](../../../../tests/test_api.py#L236)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_api_tests`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–44

Defines `run_api_tests` and its implementation control flow; direct static calls: AssertionError, MindAPI, Path, _request_while_busy, _test_real_session_context, any, mkdir, mkdtemp, request_json, rmtree, str, urlencode, write_text.

### Lines 45–74

Defines `run_api_tests` and its implementation control flow; direct static calls: AssertionError, MindAPI, Path, _request_while_busy, _test_real_session_context, any, mkdir, mkdtemp, request_json, rmtree, str, urlencode, write_text.

### Lines 75–104

Defines `run_api_tests` and its implementation control flow; direct static calls: AssertionError, MindAPI, Path, _request_while_busy, _test_real_session_context, any, mkdir, mkdtemp, request_json, rmtree, str, urlencode, write_text.

### Lines 105–134

Defines `run_api_tests` and its implementation control flow; direct static calls: AssertionError, MindAPI, Path, _request_while_busy, _test_real_session_context, any, mkdir, mkdtemp, request_json, rmtree, str, urlencode, write_text.

### Lines 135–147

Defines `run_api_tests` and its implementation control flow; direct static calls: AssertionError, MindAPI, Path, _request_while_busy, _test_real_session_context, any, mkdir, mkdtemp, request_json, rmtree, str, urlencode, write_text.

### Lines 148–149

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 150–178

Defines `_test_real_session_context` and its implementation control flow; direct static calls: dumps, join, patch, request_json.

### Lines 179–180

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 181–190

Defines `_request_while_busy` and its implementation control flow; direct static calls: acquire, range, release, request_json.

### Lines 191–192

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 193–214

Defines `request_json` and its implementation control flow; direct static calls: FakeRequest, decode, dumps, encode, getvalue, handle_get, handle_post, len, loads, str.

### Lines 215–216

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 217–233

Defines class `FakeRequest` and the behavior of its members.

### Lines 234–235

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 236–237

Defines `test_api_security_and_sessions` and its implementation control flow; direct static calls: run_api_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
