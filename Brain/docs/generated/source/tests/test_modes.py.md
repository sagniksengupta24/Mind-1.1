# `tests/test_modes.py`

## File purpose

This testing file is reviewed at snapshot `5fba89bcb1067b2de976dcc3760ff4587d412eeb92c9453bac2b95f0a62025b1`. It contains 136 lines.

## Imports and module state

- [tests/test_modes.py:1](../../../../tests/test_modes.py#L1) imports `__future__` / annotations.
- [tests/test_modes.py:3](../../../../tests/test_modes.py#L3) imports `argparse`.
- [tests/test_modes.py:4](../../../../tests/test_modes.py#L4) imports `builtins`.
- [tests/test_modes.py:5](../../../../tests/test_modes.py#L5) imports `shutil`.
- [tests/test_modes.py:6](../../../../tests/test_modes.py#L6) imports `tempfile`.
- [tests/test_modes.py:7](../../../../tests/test_modes.py#L7) imports `pathlib` / Path.
- [tests/test_modes.py:9](../../../../tests/test_modes.py#L9) imports `mind01.api` / MindAPI.
- [tests/test_modes.py:10](../../../../tests/test_modes.py#L10) imports `mind01.cli` / require_patch_apply_policy.
- [tests/test_modes.py:11](../../../../tests/test_modes.py#L11) imports `mind01.config` / AgentConfig.
- [tests/test_modes.py:12](../../../../tests/test_modes.py#L12) imports `mind01.modes` / AgentMode.
- [tests/test_modes.py:12](../../../../tests/test_modes.py#L12) imports `mind01.modes` / parse_agent_mode.
- [tests/test_modes.py:13](../../../../tests/test_modes.py#L13) imports `mind01.tools` / ToolError.
- [tests/test_modes.py:13](../../../../tests/test_modes.py#L13) imports `mind01.tools` / ToolRegistry.
- [tests/test_modes.py:14](../../../../tests/test_modes.py#L14) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `tests.test_modes.run_mode_tests` — lines 17–132

- Source: [tests/test_modes.py:17](../../../../tests/test_modes.py#L17)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentConfig`, `AssertionError`, `EOFError`, `MindAPI`, `Namespace`, `Path`, `ToolRegistry`, `build`, `call`, `exists`, `lower`, `mkdir`, `mkdtemp`, `parse_agent_mode`, `require_patch_apply_policy`, `rmtree`, `str`, `throw`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_modes.test_mode_regressions` — lines 135–136

- Source: [tests/test_modes.py:135](../../../../tests/test_modes.py#L135)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_mode_tests`
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

Imports a dependency used by this module.

### Lines 8–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–46

Defines `run_mode_tests` and its implementation control flow; direct static calls: AgentConfig, AssertionError, EOFError, MindAPI, Namespace, Path, ToolRegistry, build, call, exists, lower, mkdir, mkdtemp, parse_agent_mode, require_patch_apply_policy, rmtree, str, throw, write_text.

### Lines 47–76

Defines `run_mode_tests` and its implementation control flow; direct static calls: AgentConfig, AssertionError, EOFError, MindAPI, Namespace, Path, ToolRegistry, build, call, exists, lower, mkdir, mkdtemp, parse_agent_mode, require_patch_apply_policy, rmtree, str, throw, write_text.

### Lines 77–106

Defines `run_mode_tests` and its implementation control flow; direct static calls: AgentConfig, AssertionError, EOFError, MindAPI, Namespace, Path, ToolRegistry, build, call, exists, lower, mkdir, mkdtemp, parse_agent_mode, require_patch_apply_policy, rmtree, str, throw, write_text.

### Lines 107–132

Defines `run_mode_tests` and its implementation control flow; direct static calls: AgentConfig, AssertionError, EOFError, MindAPI, Namespace, Path, ToolRegistry, build, call, exists, lower, mkdir, mkdtemp, parse_agent_mode, require_patch_apply_policy, rmtree, str, throw, write_text.

### Lines 133–134

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 135–136

Defines `test_mode_regressions` and its implementation control flow; direct static calls: run_mode_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
