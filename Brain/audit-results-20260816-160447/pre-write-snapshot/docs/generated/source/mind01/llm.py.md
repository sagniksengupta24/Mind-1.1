# `mind01/llm.py`

## File purpose

This model and context file is reviewed at snapshot `d94b287454a2f2d7d6dff59ba693a52ee7f58935cdf1f977d073c4c5daf17f45`. It contains 268 lines.

## Imports and module state

- [mind01/llm.py:1](../../../../mind01/llm.py#L1) imports `__future__` / annotations.
- [mind01/llm.py:3](../../../../mind01/llm.py#L3) imports `json`.
- [mind01/llm.py:4](../../../../mind01/llm.py#L4) imports `re`.
- [mind01/llm.py:5](../../../../mind01/llm.py#L5) imports `urllib.error`.
- [mind01/llm.py:6](../../../../mind01/llm.py#L6) imports `urllib.request`.
- [mind01/llm.py:7](../../../../mind01/llm.py#L7) imports `dataclasses` / dataclass.
- [mind01/llm.py:8](../../../../mind01/llm.py#L8) imports `typing` / Any.
- [mind01/llm.py:8](../../../../mind01/llm.py#L8) imports `typing` / Dict.
- [mind01/llm.py:8](../../../../mind01/llm.py#L8) imports `typing` / List.

## Symbols

### `mind01.llm.Message` — lines 11–11

- Source: [mind01/llm.py:11](../../../../mind01/llm.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.LLMError` — lines 14–17

- Source: [mind01/llm.py:14](../../../../mind01/llm.py#L14)
- Type: class
- Signature: `n/a`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.LLMError.__init__` — lines 15–17

- Source: [mind01/llm.py:15](../../../../mind01/llm.py#L15)
- Type: method
- Signature: `self, message: str, *, status_code: int | None=None`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.EmbeddingError` — lines 20–21

- Source: [mind01/llm.py:20](../../../../mind01/llm.py#L20)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaClient` — lines 25–177

- Source: [mind01/llm.py:25](../../../../mind01/llm.py#L25)
- Type: class
- Signature: `n/a`
- Direct static callees: `LLMError`, `Request`, `_chat_payload`, `_http_error_detail`, `bool`, `decode`, `dict`, `dumps`, `encode`, `get`, `groups`, `isinstance`, `loads`, `lower`, `map`, `match`, `min`, `read`, `str`, `supports_json_schema`, `tuple`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaClient.model_metadata` — lines 38–78

- Source: [mind01/llm.py:38](../../../../mind01/llm.py#L38)
- Type: method
- Signature: `self`
- Direct static callees: `Request`, `decode`, `dict`, `dumps`, `encode`, `get`, `isinstance`, `loads`, `min`, `read`, `str`, `supports_json_schema`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaClient.supports_json_schema` — lines 80–94

- Source: [mind01/llm.py:80](../../../../mind01/llm.py#L80)
- Type: method
- Signature: `self, *, refresh: bool=False`
- Direct static callees: `Request`, `bool`, `decode`, `get`, `groups`, `isinstance`, `loads`, `map`, `match`, `min`, `read`, `str`, `tuple`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaClient.chat` — lines 96–135

- Source: [mind01/llm.py:96](../../../../mind01/llm.py#L96)
- Type: method
- Signature: `self, messages: List[Message], json_mode: bool=True, *, response_schema: dict[str, Any] | None=None`
- Direct static callees: `_chat_payload`, `bool`, `supports_json_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaClient._chat_payload` — lines 137–177

- Source: [mind01/llm.py:137](../../../../mind01/llm.py#L137)
- Type: method
- Signature: `self, payload: dict[str, Any]`
- Direct static callees: `LLMError`, `Request`, `_http_error_detail`, `decode`, `dumps`, `encode`, `get`, `isinstance`, `loads`, `lower`, `read`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm._http_error_detail` — lines 180–192

- Source: [mind01/llm.py:180](../../../../mind01/llm.py#L180)
- Type: function
- Signature: `exc: urllib.error.HTTPError`
- Direct static callees: `decode`, `get`, `isinstance`, `join`, `loads`, `read`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaEmbeddingClient` — lines 196–258

- Source: [mind01/llm.py:196](../../../../mind01/llm.py#L196)
- Type: class
- Signature: `n/a`
- Direct static callees: `EmbeddingError`, `Request`, `_embed_legacy`, `_embed_new`, `_post`, `coerce_vector`, `decode`, `dumps`, `encode`, `get`, `isinstance`, `loads`, `read`, `str`, `strip`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaEmbeddingClient.embed` — lines 201–216

- Source: [mind01/llm.py:201](../../../../mind01/llm.py#L201)
- Type: method
- Signature: `self, text: str`
- Direct static callees: `EmbeddingError`, `_embed_legacy`, `_embed_new`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaEmbeddingClient._embed_new` — lines 218–227

- Source: [mind01/llm.py:218](../../../../mind01/llm.py#L218)
- Type: method
- Signature: `self, text: str`
- Direct static callees: `EmbeddingError`, `_post`, `coerce_vector`, `get`, `isinstance`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaEmbeddingClient._embed_legacy` — lines 229–234

- Source: [mind01/llm.py:229](../../../../mind01/llm.py#L229)
- Type: method
- Signature: `self, text: str`
- Direct static callees: `EmbeddingError`, `_post`, `coerce_vector`, `get`, `isinstance`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.OllamaEmbeddingClient._post` — lines 236–258

- Source: [mind01/llm.py:236](../../../../mind01/llm.py#L236)
- Type: method
- Signature: `self, endpoint: str, payload: dict`
- Direct static callees: `EmbeddingError`, `Request`, `decode`, `dumps`, `encode`, `isinstance`, `loads`, `read`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.llm.coerce_vector` — lines 261–268

- Source: [mind01/llm.py:261](../../../../mind01/llm.py#L261)
- Type: function
- Signature: `values: list`
- Direct static callees: `EmbeddingError`, `append`, `float`
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

### Lines 9–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Implements module-level `Assign` behavior or data.

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–17

Defines class `LLMError` and the behavior of its members.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–21

Defines class `EmbeddingError` and the behavior of its members.

### Lines 22–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–54

Defines class `OllamaClient` and the behavior of its members.

### Lines 55–84

Defines class `OllamaClient` and the behavior of its members.

### Lines 85–114

Defines class `OllamaClient` and the behavior of its members.

### Lines 115–144

Defines class `OllamaClient` and the behavior of its members.

### Lines 145–174

Defines class `OllamaClient` and the behavior of its members.

### Lines 175–177

Defines class `OllamaClient` and the behavior of its members.

### Lines 178–179

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 180–192

Defines `_http_error_detail` and its implementation control flow; direct static calls: decode, get, isinstance, join, loads, read, split.

### Lines 193–195

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 196–225

Defines class `OllamaEmbeddingClient` and the behavior of its members.

### Lines 226–255

Defines class `OllamaEmbeddingClient` and the behavior of its members.

### Lines 256–258

Defines class `OllamaEmbeddingClient` and the behavior of its members.

### Lines 259–260

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 261–268

Defines `coerce_vector` and its implementation control flow; direct static calls: EmbeddingError, append, float.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
