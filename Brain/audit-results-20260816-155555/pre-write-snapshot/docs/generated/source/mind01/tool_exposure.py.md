# `mind01/tool_exposure.py`

## File purpose

This agent runtime file is reviewed at snapshot `c5c74e3eef7f66873b72c58150f62966eace91c59b210d716cbb1978fe785477`. It contains 217 lines.

## Imports and module state

- [mind01/tool_exposure.py:1](../../../../mind01/tool_exposure.py#L1) imports `__future__` / annotations.
- [mind01/tool_exposure.py:3](../../../../mind01/tool_exposure.py#L3) imports `hashlib`.
- [mind01/tool_exposure.py:4](../../../../mind01/tool_exposure.py#L4) imports `json`.
- [mind01/tool_exposure.py:5](../../../../mind01/tool_exposure.py#L5) imports `dataclasses` / dataclass.
- [mind01/tool_exposure.py:6](../../../../mind01/tool_exposure.py#L6) imports `enum` / Enum.
- [mind01/tool_exposure.py:8](../../../../mind01/tool_exposure.py#L8) imports `intent` / Capability.
- [mind01/tool_exposure.py:8](../../../../mind01/tool_exposure.py#L8) imports `intent` / ExpectedOutputMode.
- [mind01/tool_exposure.py:9](../../../../mind01/tool_exposure.py#L9) imports `modes` / AgentMode.
- [mind01/tool_exposure.py:9](../../../../mind01/tool_exposure.py#L9) imports `modes` / parse_agent_mode.
- [mind01/tool_exposure.py:10](../../../../mind01/tool_exposure.py#L10) imports `routing` / RoutingDecision.
- [mind01/tool_exposure.py:10](../../../../mind01/tool_exposure.py#L10) imports `routing` / ToolFamily.
- [mind01/tool_exposure.py:11](../../../../mind01/tool_exposure.py#L11) imports `tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `mind01.tool_exposure.LifecyclePhase` — lines 14–19

- Source: [mind01/tool_exposure.py:14](../../../../mind01/tool_exposure.py#L14)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.StaleRouteError` — lines 22–23

- Source: [mind01/tool_exposure.py:22](../../../../mind01/tool_exposure.py#L22)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureContext` — lines 27–84

- Source: [mind01/tool_exposure.py:27](../../../../mind01/tool_exposure.py#L27)
- Type: class
- Signature: `n/a`
- Direct static callees: `LifecyclePhase`, `append`, `cls`, `dataclass`, `dumps`, `encode`, `hexdigest`, `isinstance`, `list`, `parse_agent_mode`, `set`, `sha256`, `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureContext.build` — lines 38–68

- Source: [mind01/tool_exposure.py:38](../../../../mind01/tool_exposure.py#L38)
- Type: method
- Signature: `cls, *, phase: LifecyclePhase | str, mode: AgentMode | str, allow_write: bool, allow_shell: bool, prior_inspection: bool, mutation_seen: bool=False, discovery_seen: bool=False, discovery_scope: tuple[str, ...]=(), target_exists: bool | None=None`
- Direct static callees: `LifecyclePhase`, `append`, `cls`, `isinstance`, `parse_agent_mode`, `set`, `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureContext.fingerprint` — lines 70–84

- Source: [mind01/tool_exposure.py:70](../../../../mind01/tool_exposure.py#L70)
- Type: method
- Signature: `self`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `list`, `sha256`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureDecision` — lines 88–92

- Source: [mind01/tool_exposure.py:88](../../../../mind01/tool_exposure.py#L88)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureAuthority` — lines 95–217

- Source: [mind01/tool_exposure.py:95](../../../../mind01/tool_exposure.py#L95)
- Type: class
- Signature: `n/a`
- Direct static callees: `StaleRouteError`, `ToolExposureDecision`, `_exclusion_reason`, `append`, `fingerprint`, `fromkeys`, `get`, `is_current_for`, `parse_agent_mode`, `set`, `sorted`, `startswith`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureAuthority.decide` — lines 102–143

- Source: [mind01/tool_exposure.py:102](../../../../mind01/tool_exposure.py#L102)
- Type: method
- Signature: `self, route: RoutingDecision, context: ToolExposureContext`
- Direct static callees: `StaleRouteError`, `ToolExposureDecision`, `_exclusion_reason`, `append`, `fingerprint`, `fromkeys`, `is_current_for`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureAuthority.legacy_visible_tools` — lines 145–191

- Source: [mind01/tool_exposure.py:145](../../../../mind01/tool_exposure.py#L145)
- Type: method
- Signature: `self, *, permitted_tools: tuple[str, ...], mutation_required: bool, planning_required: bool, specialist: str, mode: AgentMode | str, inspected: bool, mutation_seen: bool, allow_write: bool, allow_shell: bool`
- Direct static callees: `append`, `parse_agent_mode`, `set`, `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tool_exposure.ToolExposureAuthority._exclusion_reason` — lines 194–217

- Source: [mind01/tool_exposure.py:194](../../../../mind01/tool_exposure.py#L194)
- Type: method
- Signature: `name: str, route: RoutingDecision, context: ToolExposureContext`
- Direct static callees: `get`, `set`, `startswith`
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

### Lines 12–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–19

Defines class `LifecyclePhase` and the behavior of its members.

### Lines 20–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–23

Defines class `StaleRouteError` and the behavior of its members.

### Lines 24–26

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 27–56

Defines class `ToolExposureContext` and the behavior of its members.

### Lines 57–84

Defines class `ToolExposureContext` and the behavior of its members.

### Lines 85–87

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 88–92

Defines class `ToolExposureDecision` and the behavior of its members.

### Lines 93–94

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 95–124

Defines class `ToolExposureAuthority` and the behavior of its members.

### Lines 125–154

Defines class `ToolExposureAuthority` and the behavior of its members.

### Lines 155–184

Defines class `ToolExposureAuthority` and the behavior of its members.

### Lines 185–214

Defines class `ToolExposureAuthority` and the behavior of its members.

### Lines 215–217

Defines class `ToolExposureAuthority` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
