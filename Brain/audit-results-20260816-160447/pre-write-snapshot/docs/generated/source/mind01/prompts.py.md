# `mind01/prompts.py`

## File purpose

This model and context file is reviewed at snapshot `3b52643865fe4726b8df9515c18ed69b015ebd5b4a0f85e54c3d0e5433840a3f`. It contains 103 lines.

## Imports and module state

- [mind01/prompts.py:1](../../../../mind01/prompts.py#L1) imports `__future__` / annotations.
- [mind01/prompts.py:3](../../../../mind01/prompts.py#L3) imports `json`.
- [mind01/prompts.py:4](../../../../mind01/prompts.py#L4) imports `typing` / Any.
- [mind01/prompts.py:4](../../../../mind01/prompts.py#L4) imports `typing` / Mapping.
- [mind01/prompts.py:4](../../../../mind01/prompts.py#L4) imports `typing` / Sequence.
- [mind01/prompts.py:6](../../../../mind01/prompts.py#L6) imports `action_parser` / ACTION_SCHEMA_VERSION.
- [mind01/prompts.py:6](../../../../mind01/prompts.py#L6) imports `action_parser` / ResponseMode.
- [mind01/prompts.py:6](../../../../mind01/prompts.py#L6) imports `action_parser` / canonical_response_schema.
- [mind01/prompts.py:6](../../../../mind01/prompts.py#L6) imports `action_parser` / coerce_response_mode.

## Symbols

### `mind01.prompts.SYSTEM_PROMPT` — lines 9–18

- Source: [mind01/prompts.py:9](../../../../mind01/prompts.py#L9)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.prompts.build_action_instruction` — lines 21–84

- Source: [mind01/prompts.py:21](../../../../mind01/prompts.py#L21)
- Type: function
- Signature: `*, mode: ResponseMode | str, phase: str, allowed_tools: Sequence[str], tool_schemas: Mapping[str, Any], task_brief: str, plan_step: str='', recent_observation: str='', parser_error: str='', repair_response_type: str | None=None, normalized_intent: Mapping[str, Any] | None=None, routing_decision: Mapping[str, Any] | None=None, operating_mode: str='read-only'`
- Direct static callees: `append`, `canonical_response_schema`, `coerce_response_mode`, `dict`, `dumps`, `extend`, `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.prompts.canonical_tool_example` — lines 87–93

- Source: [mind01/prompts.py:87](../../../../mind01/prompts.py#L87)
- Type: function
- Signature: `name: str, arguments: dict[str, Any]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.prompts.canonical_final_example` — lines 96–103

- Source: [mind01/prompts.py:96](../../../../mind01/prompts.py#L96)
- Type: function
- Signature: `summary: str, status: str='unverified'`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–18

Implements module-level `Assign` behavior or data.

### Lines 19–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–50

Defines `build_action_instruction` and its implementation control flow; direct static calls: append, canonical_response_schema, coerce_response_mode, dict, dumps, extend, join.

### Lines 51–80

Defines `build_action_instruction` and its implementation control flow; direct static calls: append, canonical_response_schema, coerce_response_mode, dict, dumps, extend, join.

### Lines 81–84

Defines `build_action_instruction` and its implementation control flow; direct static calls: append, canonical_response_schema, coerce_response_mode, dict, dumps, extend, join.

### Lines 85–86

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 87–93

Defines `canonical_tool_example` and its implementation control flow; direct static calls: none resolved.

### Lines 94–95

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 96–103

Defines `canonical_final_example` and its implementation control flow; direct static calls: none resolved.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
