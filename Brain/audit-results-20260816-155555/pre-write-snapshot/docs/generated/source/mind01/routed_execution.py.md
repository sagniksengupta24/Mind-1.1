# `mind01/routed_execution.py`

## File purpose

This agent runtime file is reviewed at snapshot `04680eebdf83d75b2ee42567dc9be305720a680c1e7468b22113287259168a90`. It contains 305 lines.

## Imports and module state

- [mind01/routed_execution.py:1](../../../../mind01/routed_execution.py#L1) imports `__future__` / annotations.
- [mind01/routed_execution.py:3](../../../../mind01/routed_execution.py#L3) imports `re`.
- [mind01/routed_execution.py:4](../../../../mind01/routed_execution.py#L4) imports `dataclasses` / dataclass.
- [mind01/routed_execution.py:5](../../../../mind01/routed_execution.py#L5) imports `pathlib` / Path.
- [mind01/routed_execution.py:6](../../../../mind01/routed_execution.py#L6) imports `typing` / Callable.
- [mind01/routed_execution.py:8](../../../../mind01/routed_execution.py#L8) imports `intent` / Capability.
- [mind01/routed_execution.py:8](../../../../mind01/routed_execution.py#L8) imports `intent` / ExpectedOutputMode.
- [mind01/routed_execution.py:9](../../../../mind01/routed_execution.py#L9) imports `modes` / AgentMode.
- [mind01/routed_execution.py:9](../../../../mind01/routed_execution.py#L9) imports `modes` / parse_agent_mode.
- [mind01/routed_execution.py:10](../../../../mind01/routed_execution.py#L10) imports `receipts` / ReceiptStore.
- [mind01/routed_execution.py:11](../../../../mind01/routed_execution.py#L11) imports `routing` / HierarchicalRouter.
- [mind01/routed_execution.py:11](../../../../mind01/routed_execution.py#L11) imports `routing` / RoutingDecision.
- [mind01/routed_execution.py:11](../../../../mind01/routed_execution.py#L11) imports `routing` / ToolFamily.
- [mind01/routed_execution.py:12](../../../../mind01/routed_execution.py#L12) imports `tool_exposure` / LifecyclePhase.
- [mind01/routed_execution.py:12](../../../../mind01/routed_execution.py#L12) imports `tool_exposure` / StaleRouteError.
- [mind01/routed_execution.py:12](../../../../mind01/routed_execution.py#L12) imports `tool_exposure` / ToolExposureAuthority.
- [mind01/routed_execution.py:12](../../../../mind01/routed_execution.py#L12) imports `tool_exposure` / ToolExposureContext.
- [mind01/routed_execution.py:12](../../../../mind01/routed_execution.py#L12) imports `tool_exposure` / ToolExposureDecision.
- [mind01/routed_execution.py:19](../../../../mind01/routed_execution.py#L19) imports `tools.registry` / ToolRegistry.
- [mind01/routed_execution.py:20](../../../../mind01/routed_execution.py#L20) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/routed_execution.py:21](../../../../mind01/routed_execution.py#L21) imports `tools.verify_tools` / ToolError.
- [mind01/routed_execution.py:21](../../../../mind01/routed_execution.py#L21) imports `tools.verify_tools` / ToolResult.

## Symbols

### `mind01.routed_execution.DISCOVERY_TOOLS` — lines 24–24

- Source: [mind01/routed_execution.py:24](../../../../mind01/routed_execution.py#L24)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.INSPECTION_TOOLS` — lines 25–25

- Source: [mind01/routed_execution.py:25](../../../../mind01/routed_execution.py#L25)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RECEIPT_RE` — lines 26–26

- Source: [mind01/routed_execution.py:26](../../../../mind01/routed_execution.py#L26)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.DispatchAuthorizationError` — lines 29–30

- Source: [mind01/routed_execution.py:29](../../../../mind01/routed_execution.py#L29)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedStep` — lines 34–38

- Source: [mind01/routed_execution.py:34](../../../../mind01/routed_execution.py#L34)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.DispatchEvidence` — lines 42–54

- Source: [mind01/routed_execution.py:42](../../../../mind01/routed_execution.py#L42)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession` — lines 57–294

- Source: [mind01/routed_execution.py:57](../../../../mind01/routed_execution.py#L57)
- Type: class
- Signature: `n/a`
- Direct static callees: `DispatchAuthorizationError`, `DispatchEvidence`, `HierarchicalRouter`, `ReceiptStore`, `RoutedStep`, `StaleRouteError`, `ToolExposureAuthority`, `ToolRegistry`, `_authorize`, `_context`, `_discovered_file_paths`, `_ground_existing_file_argument`, `_new_registry`, `_phase`, `_receipt_id`, `_useful_discovery`, `add`, `append`, `build`, `call`, `clear`, `decide`, `dict`, `extend`, `fingerprint`, `fromkeys`, `get`, `group`, `is_current_for`, `is_file`, `isinstance`, `len`, `match`, `parse_agent_mode`, `relative_to`, `resolve`, `resolve_path`, `rollback`, `route_typed`, `set`, `sorted`, `splitlines`, `str`, `strip`, `tuple`, `verify`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession.__init__` — lines 65–88

- Source: [mind01/routed_execution.py:65](../../../../mind01/routed_execution.py#L65)
- Type: method
- Signature: `self, workspace: Path, *, mode: str | AgentMode=AgentMode.READ_ONLY, allow_write: bool=False, allow_shell: bool=False, allow_network: bool=False, registry: ToolRegistry | None=None`
- Direct static callees: `HierarchicalRouter`, `ToolExposureAuthority`, `_new_registry`, `parse_agent_mode`, `resolve`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession.route` — lines 90–102

- Source: [mind01/routed_execution.py:90](../../../../mind01/routed_execution.py#L90)
- Type: method
- Signature: `self, prompt: str`
- Direct static callees: `RoutedStep`, `_context`, `decide`, `route_typed`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession.reconfigure` — lines 104–121

- Source: [mind01/routed_execution.py:104](../../../../mind01/routed_execution.py#L104)
- Type: method
- Signature: `self, *, mode: str | AgentMode | None=None, allow_write: bool | None=None, allow_shell: bool | None=None, allow_network: bool | None=None`
- Direct static callees: `_new_registry`, `parse_agent_mode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession.dispatch` — lines 123–172

- Source: [mind01/routed_execution.py:123](../../../../mind01/routed_execution.py#L123)
- Type: method
- Signature: `self, step: RoutedStep, tool: str, args: dict[str, object], *, verify: Callable[[Path], bool] | None=None`
- Direct static callees: `DispatchEvidence`, `ReceiptStore`, `_authorize`, `_discovered_file_paths`, `_ground_existing_file_argument`, `_receipt_id`, `_useful_discovery`, `append`, `call`, `clear`, `rollback`, `set`, `str`, `verify`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._authorize` — lines 174–195

- Source: [mind01/routed_execution.py:174](../../../../mind01/routed_execution.py#L174)
- Type: method
- Signature: `self, step: RoutedStep, tool: str`
- Direct static callees: `DispatchAuthorizationError`, `StaleRouteError`, `_context`, `fingerprint`, `is_current_for`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._ground_existing_file_argument` — lines 197–239

- Source: [mind01/routed_execution.py:197](../../../../mind01/routed_execution.py#L197)
- Type: method
- Signature: `self, step: RoutedStep, tool: str, args: dict[str, object]`
- Direct static callees: `append`, `dict`, `fromkeys`, `get`, `is_file`, `isinstance`, `len`, `relative_to`, `resolve_path`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._discovered_file_paths` — lines 241–258

- Source: [mind01/routed_execution.py:241](../../../../mind01/routed_execution.py#L241)
- Type: method
- Signature: `self, tool: str, observation: str`
- Direct static callees: `add`, `append`, `extend`, `group`, `is_file`, `match`, `relative_to`, `resolve_path`, `set`, `splitlines`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._context` — lines 260–270

- Source: [mind01/routed_execution.py:260](../../../../mind01/routed_execution.py#L260)
- Type: method
- Signature: `self, route: RoutingDecision`
- Direct static callees: `_phase`, `build`, `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._phase` — lines 272–285

- Source: [mind01/routed_execution.py:272](../../../../mind01/routed_execution.py#L272)
- Type: method
- Signature: `self, route: RoutingDecision`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution.RoutedExecutionSession._new_registry` — lines 287–294

- Source: [mind01/routed_execution.py:287](../../../../mind01/routed_execution.py#L287)
- Type: method
- Signature: `self`
- Direct static callees: `ToolRegistry`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution._receipt_id` — lines 297–301

- Source: [mind01/routed_execution.py:297](../../../../mind01/routed_execution.py#L297)
- Type: function
- Signature: `result: ToolResult`
- Direct static callees: `DispatchAuthorizationError`, `group`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routed_execution._useful_discovery` — lines 304–305

- Source: [mind01/routed_execution.py:304](../../../../mind01/routed_execution.py#L304)
- Type: function
- Signature: `observation: str`
- Direct static callees: `lower`, `strip`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–18

Imports a dependency used by this module.

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–21

Imports a dependency used by this module.

### Lines 22–23

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 24–24

Implements module-level `Assign` behavior or data.

### Lines 25–25

Implements module-level `Assign` behavior or data.

### Lines 26–26

Implements module-level `Assign` behavior or data.

### Lines 27–28

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 29–30

Defines class `DispatchAuthorizationError` and the behavior of its members.

### Lines 31–33

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 34–38

Defines class `RoutedStep` and the behavior of its members.

### Lines 39–41

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 42–54

Defines class `DispatchEvidence` and the behavior of its members.

### Lines 55–56

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 57–86

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 87–116

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 117–146

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 147–176

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 177–206

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 207–236

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 237–266

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 267–294

Defines class `RoutedExecutionSession` and the behavior of its members.

### Lines 295–296

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 297–301

Defines `_receipt_id` and its implementation control flow; direct static calls: DispatchAuthorizationError, group, search.

### Lines 302–303

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 304–305

Defines `_useful_discovery` and its implementation control flow; direct static calls: lower, strip.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
