# `tests/test_architecture.py`

## File purpose

This testing file is reviewed at snapshot `b449b4846f163bc5ff2155675c1aa145f2e29785d849d9ee1b5006c012abde4b`. It contains 115 lines.

## Imports and module state

- [tests/test_architecture.py:1](../../../../tests/test_architecture.py#L1) imports `__future__` / annotations.
- [tests/test_architecture.py:3](../../../../tests/test_architecture.py#L3) imports `json`.
- [tests/test_architecture.py:4](../../../../tests/test_architecture.py#L4) imports `shutil`.
- [tests/test_architecture.py:5](../../../../tests/test_architecture.py#L5) imports `tempfile`.
- [tests/test_architecture.py:6](../../../../tests/test_architecture.py#L6) imports `pathlib` / Path.
- [tests/test_architecture.py:8](../../../../tests/test_architecture.py#L8) imports `mind01.planning` / Planner.
- [tests/test_architecture.py:9](../../../../tests/test_architecture.py#L9) imports `mind01.policy` / PolicyViolation.
- [tests/test_architecture.py:9](../../../../tests/test_architecture.py#L9) imports `mind01.policy` / ServerPolicy.
- [tests/test_architecture.py:10](../../../../tests/test_architecture.py#L10) imports `mind01.routing` / HierarchicalRouter.
- [tests/test_architecture.py:11](../../../../tests/test_architecture.py#L11) imports `mind01.skills` / SkillRegistry.
- [tests/test_architecture.py:12](../../../../tests/test_architecture.py#L12) imports `mind01.state` / AgentState.
- [tests/test_architecture.py:12](../../../../tests/test_architecture.py#L12) imports `mind01.state` / AgentPhase.
- [tests/test_architecture.py:13](../../../../tests/test_architecture.py#L13) imports `mind01.verification` / VerificationEngine.
- [tests/test_architecture.py:14](../../../../tests/test_architecture.py#L14) imports `mind01.modes` / AgentMode.

## Symbols

### `tests.test_architecture.test_router_planner_and_skill_registry` — lines 17–50

- Source: [tests/test_architecture.py:17](../../../../tests/test_architecture.py#L17)
- Type: function
- Signature: `n/a`
- Direct static callees: `HierarchicalRouter`, `Path`, `Planner`, `SkillRegistry`, `any`, `build`, `mkdtemp`, `names`, `rmtree`, `route`, `select`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_architecture.test_agent_state_loop_counters` — lines 53–60

- Source: [tests/test_architecture.py:53](../../../../tests/test_architecture.py#L53)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentState`, `record_action`, `record_error`, `transition`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_architecture.test_server_policy_caps_privileges_and_endpoint` — lines 63–82

- Source: [tests/test_architecture.py:63](../../../../tests/test_architecture.py#L63)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `ServerPolicy`, `resolve_mode`, `resolve_steps`, `validate_ollama_url`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_architecture.test_verification_engine_reports_real_evidence` — lines 85–96

- Source: [tests/test_architecture.py:85](../../../../tests/test_architecture.py#L85)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `VerificationEngine`, `any`, `mkdtemp`, `rmtree`, `verify_paths`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_architecture.test_agent_config_rejects_unbounded_execution` — lines 99–115

- Source: [tests/test_architecture.py:99](../../../../tests/test_architecture.py#L99)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `build`, `str`
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

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–46

Defines `test_router_planner_and_skill_registry` and its implementation control flow; direct static calls: HierarchicalRouter, Path, Planner, SkillRegistry, any, build, mkdtemp, names, rmtree, route, select.

### Lines 47–50

Defines `test_router_planner_and_skill_registry` and its implementation control flow; direct static calls: HierarchicalRouter, Path, Planner, SkillRegistry, any, build, mkdtemp, names, rmtree, route, select.

### Lines 51–52

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 53–60

Defines `test_agent_state_loop_counters` and its implementation control flow; direct static calls: AgentState, record_action, record_error, transition.

### Lines 61–62

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 63–82

Defines `test_server_policy_caps_privileges_and_endpoint` and its implementation control flow; direct static calls: AssertionError, ServerPolicy, resolve_mode, resolve_steps, validate_ollama_url.

### Lines 83–84

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 85–96

Defines `test_verification_engine_reports_real_evidence` and its implementation control flow; direct static calls: Path, VerificationEngine, any, mkdtemp, rmtree, verify_paths, write_text.

### Lines 97–98

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 99–115

Defines `test_agent_config_rejects_unbounded_execution` and its implementation control flow; direct static calls: AssertionError, build, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
