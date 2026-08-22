# `mind01/policy.py`

## File purpose

This policy and security file is reviewed at snapshot `ed42885921a738f64076013f21155a76f6be2f73916cd7c4b9ebcde47da2bf6c`. It contains 70 lines.

## Imports and module state

- [mind01/policy.py:1](../../../../mind01/policy.py#L1) imports `__future__` / annotations.
- [mind01/policy.py:3](../../../../mind01/policy.py#L3) imports `dataclasses` / dataclass.
- [mind01/policy.py:4](../../../../mind01/policy.py#L4) imports `urllib.parse` / urlparse.
- [mind01/policy.py:6](../../../../mind01/policy.py#L6) imports `modes` / AgentMode.
- [mind01/policy.py:6](../../../../mind01/policy.py#L6) imports `modes` / parse_agent_mode.

## Symbols

### `mind01.policy._MODE_RANK` — lines 9–14

- Source: [mind01/policy.py:9](../../../../mind01/policy.py#L9)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.PolicyViolation` — lines 17–18

- Source: [mind01/policy.py:17](../../../../mind01/policy.py#L17)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.ServerPolicy` — lines 22–70

- Source: [mind01/policy.py:22](../../../../mind01/policy.py#L22)
- Type: class
- Signature: `n/a`
- Direct static callees: `PolicyViolation`, `dataclass`, `int`, `parse_agent_mode`, `rstrip`, `urlparse`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.ServerPolicy.resolve_mode` — lines 35–41

- Source: [mind01/policy.py:35](../../../../mind01/policy.py#L35)
- Type: method
- Signature: `self, requested: str | AgentMode | None`
- Direct static callees: `PolicyViolation`, `parse_agent_mode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.ServerPolicy.resolve_steps` — lines 43–52

- Source: [mind01/policy.py:43](../../../../mind01/policy.py#L43)
- Type: method
- Signature: `self, requested: object, default: int=8`
- Direct static callees: `PolicyViolation`, `int`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.ServerPolicy.validate_ollama_url` — lines 54–64

- Source: [mind01/policy.py:54](../../../../mind01/policy.py#L54)
- Type: method
- Signature: `self, url: str`
- Direct static callees: `PolicyViolation`, `rstrip`, `urlparse`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.policy.ServerPolicy.capabilities_for` — lines 66–70

- Source: [mind01/policy.py:66](../../../../mind01/policy.py#L66)
- Type: method
- Signature: `self, mode: AgentMode`
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

### Lines 9–14

Implements module-level `Assign` behavior or data.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–18

Defines class `PolicyViolation` and the behavior of its members.

### Lines 19–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–51

Defines class `ServerPolicy` and the behavior of its members.

### Lines 52–70

Defines class `ServerPolicy` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
