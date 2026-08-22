# `mind01/sessions.py`

## File purpose

This sessions memory and RAG file is reviewed at snapshot `f240566f719084f0824e818a120019aa624523ad616c3fcd38ba273432769ef2`. It contains 168 lines.

## Imports and module state

- [mind01/sessions.py:1](../../../../mind01/sessions.py#L1) imports `__future__` / annotations.
- [mind01/sessions.py:3](../../../../mind01/sessions.py#L3) imports `sqlite3`.
- [mind01/sessions.py:4](../../../../mind01/sessions.py#L4) imports `time`.
- [mind01/sessions.py:5](../../../../mind01/sessions.py#L5) imports `uuid`.
- [mind01/sessions.py:6](../../../../mind01/sessions.py#L6) imports `dataclasses` / dataclass.
- [mind01/sessions.py:7](../../../../mind01/sessions.py#L7) imports `pathlib` / Path.

## Symbols

### `mind01.sessions.Session` — lines 11–15

- Source: [mind01/sessions.py:11](../../../../mind01/sessions.py#L11)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionMessage` — lines 19–23

- Source: [mind01/sessions.py:19](../../../../mind01/sessions.py#L19)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore` — lines 26–160

- Source: [mind01/sessions.py:26](../../../../mind01/sessions.py#L26)
- Type: class
- Signature: `n/a`
- Direct static callees: `Session`, `SessionMessage`, `ValueError`, `_connect`, `_init_db`, `all`, `append`, `connect`, `execute`, `extend`, `fetchall`, `fetchone`, `get`, `int`, `isalnum`, `join`, `len`, `max`, `min`, `mkdir`, `resolve`, `reverse`, `reversed`, `split`, `str`, `strip`, `time`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.__init__` — lines 27–30

- Source: [mind01/sessions.py:27](../../../../mind01/sessions.py#L27)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `_init_db`, `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore._connect` — lines 32–37

- Source: [mind01/sessions.py:32](../../../../mind01/sessions.py#L32)
- Type: method
- Signature: `self`
- Direct static callees: `connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore._init_db` — lines 39–64

- Source: [mind01/sessions.py:39](../../../../mind01/sessions.py#L39)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.create` — lines 66–77

- Source: [mind01/sessions.py:66](../../../../mind01/sessions.py#L66)
- Type: method
- Signature: `self, title: str='New session', session_id: str | None=None`
- Direct static callees: `Session`, `ValueError`, `_connect`, `all`, `execute`, `int`, `isalnum`, `len`, `strip`, `time`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.exists` — lines 79–81

- Source: [mind01/sessions.py:79](../../../../mind01/sessions.py#L79)
- Type: method
- Signature: `self, session_id: str`
- Direct static callees: `_connect`, `execute`, `fetchone`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.list` — lines 83–90

- Source: [mind01/sessions.py:83](../../../../mind01/sessions.py#L83)
- Type: method
- Signature: `self, limit: int=50`
- Direct static callees: `Session`, `_connect`, `execute`, `fetchall`, `int`, `max`, `min`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.get` — lines 92–101

- Source: [mind01/sessions.py:92](../../../../mind01/sessions.py#L92)
- Type: method
- Signature: `self, session_id: str`
- Direct static callees: `Session`, `SessionMessage`, `ValueError`, `_connect`, `execute`, `fetchall`, `fetchone`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.add_message` — lines 103–117

- Source: [mind01/sessions.py:103](../../../../mind01/sessions.py#L103)
- Type: method
- Signature: `self, session_id: str, role: str, content: str, trace: str=''`
- Direct static callees: `ValueError`, `_connect`, `execute`, `fetchone`, `int`, `str`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.context_messages` — lines 119–154

- Source: [mind01/sessions.py:119](../../../../mind01/sessions.py#L119)
- Type: method
- Signature: `self, session_id: str, *, max_messages: int=20, max_chars: int=16000`
- Direct static callees: `SessionMessage`, `append`, `extend`, `get`, `join`, `len`, `reverse`, `reversed`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.SessionStore.delete` — lines 156–160

- Source: [mind01/sessions.py:156](../../../../mind01/sessions.py#L156)
- Type: method
- Signature: `self, session_id: str`
- Direct static callees: `ValueError`, `_connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.session_to_dict` — lines 163–164

- Source: [mind01/sessions.py:163](../../../../mind01/sessions.py#L163)
- Type: function
- Signature: `session: Session`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.sessions.message_to_dict` — lines 167–168

- Source: [mind01/sessions.py:167](../../../../mind01/sessions.py#L167)
- Type: function
- Signature: `message: SessionMessage`
- Direct static callees: none resolved
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

### Lines 8–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–15

Defines class `Session` and the behavior of its members.

### Lines 16–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–23

Defines class `SessionMessage` and the behavior of its members.

### Lines 24–25

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 26–55

Defines class `SessionStore` and the behavior of its members.

### Lines 56–85

Defines class `SessionStore` and the behavior of its members.

### Lines 86–115

Defines class `SessionStore` and the behavior of its members.

### Lines 116–145

Defines class `SessionStore` and the behavior of its members.

### Lines 146–160

Defines class `SessionStore` and the behavior of its members.

### Lines 161–162

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 163–164

Defines `session_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 165–166

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 167–168

Defines `message_to_dict` and its implementation control flow; direct static calls: none resolved.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
