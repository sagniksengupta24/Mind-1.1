# `tests/test_routed_execution.py`

## File purpose

This testing file is reviewed at snapshot `6a99092d3e730a066597878afa666f2bf5a1a2cc7e0fa0fb007bb61aaa0a717d`. It contains 232 lines.

## Imports and module state

- [tests/test_routed_execution.py:1](../../../../tests/test_routed_execution.py#L1) imports `__future__` / annotations.
- [tests/test_routed_execution.py:3](../../../../tests/test_routed_execution.py#L3) imports `pathlib` / Path.
- [tests/test_routed_execution.py:5](../../../../tests/test_routed_execution.py#L5) imports `pytest`.
- [tests/test_routed_execution.py:7](../../../../tests/test_routed_execution.py#L7) imports `mind01.action_parser` / ResponseMode.
- [tests/test_routed_execution.py:7](../../../../tests/test_routed_execution.py#L7) imports `mind01.action_parser` / parse_action_output.
- [tests/test_routed_execution.py:8](../../../../tests/test_routed_execution.py#L8) imports `mind01.routed_execution` / DispatchAuthorizationError.
- [tests/test_routed_execution.py:8](../../../../tests/test_routed_execution.py#L8) imports `mind01.routed_execution` / RoutedExecutionSession.
- [tests/test_routed_execution.py:9](../../../../tests/test_routed_execution.py#L9) imports `mind01.tool_exposure` / StaleRouteError.
- [tests/test_routed_execution.py:10](../../../../tests/test_routed_execution.py#L10) imports `mind01.tools.registry` / ToolRegistry.
- [tests/test_routed_execution.py:11](../../../../tests/test_routed_execution.py#L11) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `tests.test_routed_execution.workspace` — lines 14–19

- Source: [tests/test_routed_execution.py:14](../../../../tests/test_routed_execution.py#L14)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_hidden_and_unauthorized_tools_never_reach_registry` — lines 22–40

- Source: [tests/test_routed_execution.py:22](../../../../tests/test_routed_execution.py#L22)
- Type: function
- Signature: `tmp_path: Path, monkeypatch: pytest.MonkeyPatch`
- Direct static callees: `RoutedExecutionSession`, `ToolRegistry`, `append`, `dispatch`, `original`, `raises`, `read_text`, `route`, `setattr`, `startswith`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_propose_mode_cannot_dispatch_a_live_write` — lines 43–53

- Source: [tests/test_routed_execution.py:43](../../../../tests/test_routed_execution.py#L43)
- Type: function
- Signature: `tmp_path: Path, monkeypatch: pytest.MonkeyPatch`
- Direct static callees: `RoutedExecutionSession`, `ToolRegistry`, `append`, `dispatch`, `raises`, `read_text`, `route`, `setattr`, `startswith`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_mode_and_capability_changes_invalidate_route_and_exposure` — lines 56–67

- Source: [tests/test_routed_execution.py:56](../../../../tests/test_routed_execution.py#L56)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `raises`, `reconfigure`, `route`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_required_inspection_transitions_to_proposal_and_live_edit` — lines 70–95

- Source: [tests/test_routed_execution.py:70](../../../../tests/test_routed_execution.py#L70)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `mkdir`, `read_text`, `route`, `startswith`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_discovery_can_transition_to_bounded_file_read` — lines 98–107

- Source: [tests/test_routed_execution.py:98](../../../../tests/test_routed_execution.py#L98)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `route`, `set`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_symbol_search_works_without_persistently_indexing_workspace` — lines 110–123

- Source: [tests/test_routed_execution.py:110](../../../../tests/test_routed_execution.py#L110)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `route`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_empty_discovery_does_not_advance_lifecycle` — lines 126–133

- Source: [tests/test_routed_execution.py:126](../../../../tests/test_routed_execution.py#L126)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `route`, `set`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_missing_read_path_is_grounded_only_to_one_explicit_existing_target` — lines 136–146

- Source: [tests/test_routed_execution.py:136](../../../../tests/test_routed_execution.py#L136)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `raises`, `route`, `workspace`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_missing_edit_path_can_only_ground_to_the_authorized_existing_target` — lines 149–163

- Source: [tests/test_routed_execution.py:149](../../../../tests/test_routed_execution.py#L149)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `read_text`, `route`, `startswith`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_failed_post_write_verification_rolls_back` — lines 166–182

- Source: [tests/test_routed_execution.py:166](../../../../tests/test_routed_execution.py#L166)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `_compiles`, `dispatch`, `read_bytes`, `route`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_rejected_mutation_preserves_source_and_records_no_success` — lines 185–200

- Source: [tests/test_routed_execution.py:185](../../../../tests/test_routed_execution.py#L185)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `raises`, `read_bytes`, `route`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_parser_repair_cannot_expand_exposure` — lines 203–216

- Source: [tests/test_routed_execution.py:203](../../../../tests/test_routed_execution.py#L203)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `parse_action_output`, `read_text`, `route`, `startswith`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution.test_route_confidence_cannot_override_dispatch_policy` — lines 219–224

- Source: [tests/test_routed_execution.py:219](../../../../tests/test_routed_execution.py#L219)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `RoutedExecutionSession`, `dispatch`, `raises`, `route`, `workspace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_routed_execution._compiles` — lines 227–232

- Source: [tests/test_routed_execution.py:227](../../../../tests/test_routed_execution.py#L227)
- Type: function
- Signature: `path: Path`
- Direct static callees: `compile`, `read_text`, `str`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

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

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–19

Defines `workspace` and its implementation control flow; direct static calls: write_text.

### Lines 20–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–40

Defines `test_hidden_and_unauthorized_tools_never_reach_registry` and its implementation control flow; direct static calls: RoutedExecutionSession, ToolRegistry, append, dispatch, original, raises, read_text, route, setattr, startswith, workspace.

### Lines 41–42

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 43–53

Defines `test_propose_mode_cannot_dispatch_a_live_write` and its implementation control flow; direct static calls: RoutedExecutionSession, ToolRegistry, append, dispatch, raises, read_text, route, setattr, startswith, workspace.

### Lines 54–55

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 56–67

Defines `test_mode_and_capability_changes_invalidate_route_and_exposure` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, raises, reconfigure, route, workspace.

### Lines 68–69

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 70–95

Defines `test_required_inspection_transitions_to_proposal_and_live_edit` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, mkdir, read_text, route, startswith, workspace.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–107

Defines `test_discovery_can_transition_to_bounded_file_read` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, route, set, workspace.

### Lines 108–109

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 110–123

Defines `test_symbol_search_works_without_persistently_indexing_workspace` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, route, workspace.

### Lines 124–125

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 126–133

Defines `test_empty_discovery_does_not_advance_lifecycle` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, route, set, workspace.

### Lines 134–135

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 136–146

Defines `test_missing_read_path_is_grounded_only_to_one_explicit_existing_target` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, raises, route, workspace, write_text.

### Lines 147–148

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 149–163

Defines `test_missing_edit_path_can_only_ground_to_the_authorized_existing_target` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, read_text, route, startswith, workspace.

### Lines 164–165

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 166–182

Defines `test_failed_post_write_verification_rolls_back` and its implementation control flow; direct static calls: RoutedExecutionSession, _compiles, dispatch, read_bytes, route, workspace.

### Lines 183–184

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 185–200

Defines `test_rejected_mutation_preserves_source_and_records_no_success` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, raises, read_bytes, route, workspace.

### Lines 201–202

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 203–216

Defines `test_parser_repair_cannot_expand_exposure` and its implementation control flow; direct static calls: RoutedExecutionSession, parse_action_output, read_text, route, startswith, workspace.

### Lines 217–218

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 219–224

Defines `test_route_confidence_cannot_override_dispatch_policy` and its implementation control flow; direct static calls: RoutedExecutionSession, dispatch, raises, route, workspace.

### Lines 225–226

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 227–232

Defines `_compiles` and its implementation control flow; direct static calls: compile, read_text, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
