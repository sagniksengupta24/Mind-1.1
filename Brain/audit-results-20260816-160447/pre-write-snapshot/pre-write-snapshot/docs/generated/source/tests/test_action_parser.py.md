# `tests/test_action_parser.py`

## File purpose

This testing file is reviewed at snapshot `4077d299441c1d668fe209e2bebcaadb5f31784628e5812455a203ca4340a9c1`. It contains 78 lines.

## Imports and module state

- [tests/test_action_parser.py:1](../../../../tests/test_action_parser.py#L1) imports `__future__` / annotations.
- [tests/test_action_parser.py:3](../../../../tests/test_action_parser.py#L3) imports `json`.
- [tests/test_action_parser.py:5](../../../../tests/test_action_parser.py#L5) imports `mind01.action_parser` / ActionParseError.
- [tests/test_action_parser.py:5](../../../../tests/test_action_parser.py#L5) imports `mind01.action_parser` / ParserFailureCode.
- [tests/test_action_parser.py:5](../../../../tests/test_action_parser.py#L5) imports `mind01.action_parser` / ResponseMode.
- [tests/test_action_parser.py:5](../../../../tests/test_action_parser.py#L5) imports `mind01.action_parser` / parse_action_output.
- [tests/test_action_parser.py:5](../../../../tests/test_action_parser.py#L5) imports `mind01.action_parser` / parse_action_output_strict.

## Symbols

### `tests.test_action_parser.tool_call` — lines 14–15

- Source: [tests/test_action_parser.py:14](../../../../tests/test_action_parser.py#L14)
- Type: function
- Signature: `tool: str, arguments: dict`
- Direct static callees: `dumps`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.final` — lines 18–19

- Source: [tests/test_action_parser.py:18](../../../../tests/test_action_parser.py#L18)
- Type: function
- Signature: `summary: str, status: str='unverified', refs: list[str] | None=None`
- Direct static callees: `dumps`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.expect_error` — lines 22–29

- Source: [tests/test_action_parser.py:22](../../../../tests/test_action_parser.py#L22)
- Type: function
- Signature: `raw: str, code: ParserFailureCode, **kwargs`
- Direct static callees: `AssertionError`, `len`, `parse_action_output_strict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.test_canonical_tool_and_final_responses` — lines 32–38

- Source: [tests/test_action_parser.py:32](../../../../tests/test_action_parser.py#L32)
- Type: function
- Signature: `n/a`
- Direct static callees: `final`, `parse_action_output_strict`, `tool_call`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.test_typed_parser_failures_and_mode_enforcement` — lines 41–50

- Source: [tests/test_action_parser.py:41](../../../../tests/test_action_parser.py#L41)
- Type: function
- Signature: `n/a`
- Direct static callees: `expect_error`, `final`, `tool_call`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.test_multiple_conflicting_and_legacy_formats_are_rejected` — lines 53–58

- Source: [tests/test_action_parser.py:53](../../../../tests/test_action_parser.py#L53)
- Type: function
- Signature: `n/a`
- Direct static callees: `dumps`, `expect_error`, `tool_call`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.test_safe_single_object_extraction_is_recorded_as_incident` — lines 61–67

- Source: [tests/test_action_parser.py:61](../../../../tests/test_action_parser.py#L61)
- Type: function
- Signature: `n/a`
- Direct static callees: `final`, `parse_action_output`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.run_action_parser_tests` — lines 70–74

- Source: [tests/test_action_parser.py:70](../../../../tests/test_action_parser.py#L70)
- Type: function
- Signature: `n/a`
- Direct static callees: `test_canonical_tool_and_final_responses`, `test_multiple_conflicting_and_legacy_formats_are_rejected`, `test_safe_single_object_extraction_is_recorded_as_incident`, `test_typed_parser_failures_and_mode_enforcement`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_parser.test_action_parser_regressions` — lines 77–78

- Source: [tests/test_action_parser.py:77](../../../../tests/test_action_parser.py#L77)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_action_parser_tests`
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

### Lines 5–11

Imports a dependency used by this module.

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–15

Defines `tool_call` and its implementation control flow; direct static calls: dumps.

### Lines 16–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–19

Defines `final` and its implementation control flow; direct static calls: dumps.

### Lines 20–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–29

Defines `expect_error` and its implementation control flow; direct static calls: AssertionError, len, parse_action_output_strict.

### Lines 30–31

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 32–38

Defines `test_canonical_tool_and_final_responses` and its implementation control flow; direct static calls: final, parse_action_output_strict, tool_call.

### Lines 39–40

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 41–50

Defines `test_typed_parser_failures_and_mode_enforcement` and its implementation control flow; direct static calls: expect_error, final, tool_call.

### Lines 51–52

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 53–58

Defines `test_multiple_conflicting_and_legacy_formats_are_rejected` and its implementation control flow; direct static calls: dumps, expect_error, tool_call.

### Lines 59–60

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 61–67

Defines `test_safe_single_object_extraction_is_recorded_as_incident` and its implementation control flow; direct static calls: final, parse_action_output.

### Lines 68–69

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 70–74

Defines `run_action_parser_tests` and its implementation control flow; direct static calls: test_canonical_tool_and_final_responses, test_multiple_conflicting_and_legacy_formats_are_rejected, test_safe_single_object_extraction_is_recorded_as_incident, test_typed_parser_failures_and_mode_enforcement.

### Lines 75–76

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 77–78

Defines `test_action_parser_regressions` and its implementation control flow; direct static calls: run_action_parser_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
