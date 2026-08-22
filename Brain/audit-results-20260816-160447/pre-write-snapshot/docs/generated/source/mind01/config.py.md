# `mind01/config.py`

## File purpose

This agent runtime file is reviewed at snapshot `1fdcb1786aa002263f71ef90326f32c582f472f7af41d4b637339eb4b352b1fe`. It contains 66 lines.

## Imports and module state

- [mind01/config.py:1](../../../../mind01/config.py#L1) imports `__future__` / annotations.
- [mind01/config.py:3](../../../../mind01/config.py#L3) imports `dataclasses` / dataclass.
- [mind01/config.py:4](../../../../mind01/config.py#L4) imports `pathlib` / Path.
- [mind01/config.py:6](../../../../mind01/config.py#L6) imports `modes` / AgentMode.
- [mind01/config.py:6](../../../../mind01/config.py#L6) imports `modes` / parse_agent_mode.

## Symbols

### `mind01.config.AgentConfig` — lines 10–66

- Source: [mind01/config.py:10](../../../../mind01/config.py#L10)
- Type: class
- Signature: `n/a`
- Direct static callees: `Path`, `ValueError`, `cls`, `dataclass`, `expanduser`, `int`, `parse_agent_mode`, `resolve`, `rstrip`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.config.AgentConfig.build` — lines 25–66

- Source: [mind01/config.py:25](../../../../mind01/config.py#L25)
- Type: method
- Signature: `cls, workspace: str, model: str, ollama_url: str, max_steps: int, yes: bool, dry_run: bool, trace: bool=False, allow_write: bool=False, allow_shell: bool=False, mode: str | AgentMode=AgentMode.READ_ONLY, request_timeout_seconds: int=120, semantic_router: str='legacy'`
- Direct static callees: `Path`, `ValueError`, `cls`, `expanduser`, `int`, `parse_agent_mode`, `resolve`, `rstrip`, `strip`
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

### Lines 7–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–39

Defines class `AgentConfig` and the behavior of its members.

### Lines 40–66

Defines class `AgentConfig` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
