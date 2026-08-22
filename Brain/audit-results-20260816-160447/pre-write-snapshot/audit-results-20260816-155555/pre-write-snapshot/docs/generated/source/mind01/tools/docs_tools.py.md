# `mind01/tools/docs_tools.py`

## File purpose

This tool system file is reviewed at snapshot `517030a8eb95a78d09bf2db324a775cf9027473530bb9d3fcda2260a1e629fbe`. It contains 49 lines.

## Imports and module state

- [mind01/tools/docs_tools.py:1](../../../../../mind01/tools/docs_tools.py#L1) imports `__future__` / annotations.
- [mind01/tools/docs_tools.py:3](../../../../../mind01/tools/docs_tools.py#L3) imports `typing` / Any.
- [mind01/tools/docs_tools.py:3](../../../../../mind01/tools/docs_tools.py#L3) imports `typing` / Dict.
- [mind01/tools/docs_tools.py:5](../../../../../mind01/tools/docs_tools.py#L5) imports `llm` / EmbeddingError.
- [mind01/tools/docs_tools.py:5](../../../../../mind01/tools/docs_tools.py#L5) imports `llm` / OllamaEmbeddingClient.
- [mind01/tools/docs_tools.py:6](../../../../../mind01/tools/docs_tools.py#L6) imports `security` / redact_secrets.
- [mind01/tools/docs_tools.py:7](../../../../../mind01/tools/docs_tools.py#L7) imports `verify_tools` / ToolError.
- [mind01/tools/docs_tools.py:7](../../../../../mind01/tools/docs_tools.py#L7) imports `verify_tools` / ToolResult.
- [mind01/tools/docs_tools.py:7](../../../../../mind01/tools/docs_tools.py#L7) imports `verify_tools` / require_arg.

## Symbols

### `mind01.tools.docs_tools.search_docs` — lines 10–39

- Source: [mind01/tools/docs_tools.py:10](../../../../../mind01/tools/docs_tools.py#L10)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `OllamaEmbeddingClient`, `ToolError`, `ToolResult`, `get`, `int`, `join`, `lower`, `redact_secrets`, `render_stale`, `render_vector_score`, `require_arg`, `search`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.docs_tools.render_vector_score` — lines 42–45

- Source: [mind01/tools/docs_tools.py:42](../../../../../mind01/tools/docs_tools.py#L42)
- Type: function
- Signature: `score: float`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.docs_tools.render_stale` — lines 48–49

- Source: [mind01/tools/docs_tools.py:48](../../../../../mind01/tools/docs_tools.py#L48)
- Type: function
- Signature: `stale: bool`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 5–5

Imports a dependency used by this module.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–39

Defines `search_docs` and its implementation control flow; direct static calls: OllamaEmbeddingClient, ToolError, ToolResult, get, int, join, lower, redact_secrets, render_stale, render_vector_score, require_arg, search, str.

### Lines 40–41

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 42–45

Defines `render_vector_score` and its implementation control flow; direct static calls: none resolved.

### Lines 46–47

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 48–49

Defines `render_stale` and its implementation control flow; direct static calls: none resolved.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
