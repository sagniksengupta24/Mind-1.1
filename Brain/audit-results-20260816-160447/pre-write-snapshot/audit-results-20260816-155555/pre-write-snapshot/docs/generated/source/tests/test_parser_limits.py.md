# `tests/test_parser_limits.py`

## File purpose

This testing file is reviewed at snapshot `f19408d357b2a448046e14701cf3ce128ca1b7f2b535aa06f781b9722ca8283b`. It contains 33 lines.

## Imports and module state

- [tests/test_parser_limits.py:1](../../../../tests/test_parser_limits.py#L1) imports `__future__` / annotations.
- [tests/test_parser_limits.py:3](../../../../tests/test_parser_limits.py#L3) imports `json`.
- [tests/test_parser_limits.py:4](../../../../tests/test_parser_limits.py#L4) imports `random`.
- [tests/test_parser_limits.py:5](../../../../tests/test_parser_limits.py#L5) imports `string`.
- [tests/test_parser_limits.py:7](../../../../tests/test_parser_limits.py#L7) imports `mind01.action_parser` / MAX_ARGUMENT_STRING_CHARS.
- [tests/test_parser_limits.py:7](../../../../tests/test_parser_limits.py#L7) imports `mind01.action_parser` / MAX_MODEL_OUTPUT_CHARS.
- [tests/test_parser_limits.py:7](../../../../tests/test_parser_limits.py#L7) imports `mind01.action_parser` / ParserFailureCode.
- [tests/test_parser_limits.py:7](../../../../tests/test_parser_limits.py#L7) imports `mind01.action_parser` / parse_action_output.

## Symbols

### `tests.test_parser_limits.test_parser_rejects_conflicting_and_oversized_actions` — lines 10–18

- Source: [tests/test_parser_limits.py:10](../../../../tests/test_parser_limits.py#L10)
- Type: function
- Signature: `n/a`
- Direct static callees: `dumps`, `parse_action_output`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_parser_limits.test_parser_handles_malformed_inputs_without_raising` — lines 21–27

- Source: [tests/test_parser_limits.py:21](../../../../tests/test_parser_limits.py#L21)
- Type: function
- Signature: `n/a`
- Direct static callees: `Random`, `choice`, `join`, `parse_action_output`, `randint`, `range`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_parser_limits.test_parser_accepts_one_canonical_action` — lines 30–33

- Source: [tests/test_parser_limits.py:30](../../../../tests/test_parser_limits.py#L30)
- Type: function
- Signature: `n/a`
- Direct static callees: `dumps`, `parse_action_output`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–18

Defines `test_parser_rejects_conflicting_and_oversized_actions` and its implementation control flow; direct static calls: dumps, parse_action_output.

### Lines 19–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–27

Defines `test_parser_handles_malformed_inputs_without_raising` and its implementation control flow; direct static calls: Random, choice, join, parse_action_output, randint, range.

### Lines 28–29

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 30–33

Defines `test_parser_accepts_one_canonical_action` and its implementation control flow; direct static calls: dumps, parse_action_output.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
