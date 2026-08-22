# `mind01/recovery.py`

## File purpose

This verification and correction file is reviewed at snapshot `bf37cb8a349ce895bc0aedb741a9987ebce4ebadf8b5bcbe633afc0da14a0797`. It contains 52 lines.

## Imports and module state

- [mind01/recovery.py:1](../../../../mind01/recovery.py#L1) imports `__future__` / annotations.
- [mind01/recovery.py:3](../../../../mind01/recovery.py#L3) imports `dataclasses` / dataclass.
- [mind01/recovery.py:5](../../../../mind01/recovery.py#L5) imports `state` / AgentState.

## Symbols

### `mind01.recovery.RecoveryDecision` — lines 9–12

- Source: [mind01/recovery.py:9](../../../../mind01/recovery.py#L9)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.recovery.RecoveryController` — lines 15–52

- Source: [mind01/recovery.py:15](../../../../mind01/recovery.py#L15)
- Type: class
- Signature: `n/a`
- Direct static callees: `RecoveryDecision`, `join`, `record_action`, `record_error`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.recovery.RecoveryController.parser_failure` — lines 16–38

- Source: [mind01/recovery.py:16](../../../../mind01/recovery.py#L16)
- Type: method
- Signature: `self, state: AgentState, error: str, *, error_code: str='MALFORMED_JSON', expected_mode: str='REPAIR_REQUIRED', allowed_tools: tuple[str, ...]=(), raw_output_hash: str=''`
- Direct static callees: `RecoveryDecision`, `join`, `record_error`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.recovery.RecoveryController.repeated_action` — lines 40–46

- Source: [mind01/recovery.py:40](../../../../mind01/recovery.py#L40)
- Type: method
- Signature: `self, state: AgentState, signature: str`
- Direct static callees: `RecoveryDecision`, `record_action`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.recovery.RecoveryController.tool_error` — lines 48–52

- Source: [mind01/recovery.py:48](../../../../mind01/recovery.py#L48)
- Type: method
- Signature: `self, state: AgentState, error: str`
- Direct static callees: `RecoveryDecision`, `record_error`
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

### Lines 6–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–12

Defines class `RecoveryDecision` and the behavior of its members.

### Lines 13–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–44

Defines class `RecoveryController` and the behavior of its members.

### Lines 45–52

Defines class `RecoveryController` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
