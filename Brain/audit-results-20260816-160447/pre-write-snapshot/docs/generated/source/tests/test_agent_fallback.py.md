# `tests/test_agent_fallback.py`

## File purpose

This testing file is reviewed at snapshot `96e077965041eefe791d3a8bd026fe45a1bd51648bed813f7850cc62ee1bbdc6`. It contains 171 lines.

## Imports and module state

- [tests/test_agent_fallback.py:1](../../../../tests/test_agent_fallback.py#L1) imports `__future__` / annotations.
- [tests/test_agent_fallback.py:3](../../../../tests/test_agent_fallback.py#L3) imports `shutil`.
- [tests/test_agent_fallback.py:4](../../../../tests/test_agent_fallback.py#L4) imports `tempfile`.
- [tests/test_agent_fallback.py:5](../../../../tests/test_agent_fallback.py#L5) imports `json`.
- [tests/test_agent_fallback.py:6](../../../../tests/test_agent_fallback.py#L6) imports `pathlib` / Path.
- [tests/test_agent_fallback.py:7](../../../../tests/test_agent_fallback.py#L7) imports `unittest.mock` / patch.
- [tests/test_agent_fallback.py:9](../../../../tests/test_agent_fallback.py#L9) imports `mind01.agent` / Agent.
- [tests/test_agent_fallback.py:9](../../../../tests/test_agent_fallback.py#L9) imports `mind01.agent` / build_deterministic_domain_repair_answer.
- [tests/test_agent_fallback.py:9](../../../../tests/test_agent_fallback.py#L9) imports `mind01.agent` / build_preflight_deterministic_answer.
- [tests/test_agent_fallback.py:9](../../../../tests/test_agent_fallback.py#L9) imports `mind01.agent` / get_final_quality_issue.
- [tests/test_agent_fallback.py:15](../../../../tests/test_agent_fallback.py#L15) imports `mind01.config` / AgentConfig.
- [tests/test_agent_fallback.py:16](../../../../tests/test_agent_fallback.py#L16) imports `mind01.modes` / AgentMode.
- [tests/test_agent_fallback.py:17](../../../../tests/test_agent_fallback.py#L17) imports `mind01.prompts` / SYSTEM_PROMPT.

## Symbols

### `tests.test_agent_fallback._config` — lines 20–30

- Source: [tests/test_agent_fallback.py:20](../../../../tests/test_agent_fallback.py#L20)
- Type: function
- Signature: `tmp: Path, mode: AgentMode=AgentMode.READ_ONLY, max_steps: int=4`
- Direct static callees: `build`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_system_prompt_has_strict_examples` — lines 33–36

- Source: [tests/test_agent_fallback.py:33](../../../../tests/test_agent_fallback.py#L33)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_canonical_final_and_route_state` — lines 39–50

- Source: [tests/test_agent_fallback.py:39](../../../../tests/test_agent_fallback.py#L39)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `Path`, `_config`, `ask`, `dumps`, `mkdtemp`, `object`, `rmtree`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_malformed_action_is_repaired_without_executing_loose_json` — lines 53–70

- Source: [tests/test_agent_fallback.py:53](../../../../tests/test_agent_fallback.py#L53)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `AssertionError`, `Path`, `_config`, `any`, `ask`, `dumps`, `mkdtemp`, `object`, `rmtree`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_repository_answer_requires_real_tool_grounding` — lines 73–90

- Source: [tests/test_agent_fallback.py:73](../../../../tests/test_agent_fallback.py#L73)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `Path`, `_config`, `any`, `ask`, `dumps`, `mkdtemp`, `object`, `rmtree`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_generation_only_task_cannot_mutate_workspace` — lines 93–108

- Source: [tests/test_agent_fallback.py:93](../../../../tests/test_agent_fallback.py#L93)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `AssertionError`, `Path`, `_config`, `any`, `ask`, `dumps`, `mkdtemp`, `object`, `rmtree`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_benchmark_specific_canned_repair_was_removed` — lines 111–114

- Source: [tests/test_agent_fallback.py:111](../../../../tests/test_agent_fallback.py#L111)
- Type: function
- Signature: `n/a`
- Direct static callees: `build_deterministic_domain_repair_answer`, `build_preflight_deterministic_answer`, `get_final_quality_issue`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_route_policy_blocks_unrelated_mutation_tool` — lines 117–140

- Source: [tests/test_agent_fallback.py:117](../../../../tests/test_agent_fallback.py#L117)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `Path`, `_config`, `any`, `ask`, `dumps`, `mkdtemp`, `object`, `original_call`, `rmtree`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.test_successful_mutation_attaches_verification_evidence` — lines 143–160

- Source: [tests/test_agent_fallback.py:143](../../../../tests/test_agent_fallback.py#L143)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `Path`, `_config`, `any`, `ask`, `dumps`, `mkdtemp`, `object`, `rmtree`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_agent_fallback.run_agent_fallback_tests` — lines 163–171

- Source: [tests/test_agent_fallback.py:163](../../../../tests/test_agent_fallback.py#L163)
- Type: function
- Signature: `n/a`
- Direct static callees: `test_benchmark_specific_canned_repair_was_removed`, `test_canonical_final_and_route_state`, `test_generation_only_task_cannot_mutate_workspace`, `test_malformed_action_is_repaired_without_executing_loose_json`, `test_repository_answer_requires_real_tool_grounding`, `test_route_policy_blocks_unrelated_mutation_tool`, `test_successful_mutation_attaches_verification_evidence`, `test_system_prompt_has_strict_examples`
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

### Lines 9–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–30

Defines `_config` and its implementation control flow; direct static calls: build, str.

### Lines 31–32

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 33–36

Defines `test_system_prompt_has_strict_examples` and its implementation control flow; direct static calls: none resolved.

### Lines 37–38

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 39–50

Defines `test_canonical_final_and_route_state` and its implementation control flow; direct static calls: Agent, Path, _config, ask, dumps, mkdtemp, object, rmtree.

### Lines 51–52

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 53–70

Defines `test_malformed_action_is_repaired_without_executing_loose_json` and its implementation control flow; direct static calls: Agent, AssertionError, Path, _config, any, ask, dumps, mkdtemp, object, rmtree.

### Lines 71–72

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 73–90

Defines `test_repository_answer_requires_real_tool_grounding` and its implementation control flow; direct static calls: Agent, Path, _config, any, ask, dumps, mkdtemp, object, rmtree, write_text.

### Lines 91–92

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 93–108

Defines `test_generation_only_task_cannot_mutate_workspace` and its implementation control flow; direct static calls: Agent, AssertionError, Path, _config, any, ask, dumps, mkdtemp, object, rmtree.

### Lines 109–110

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 111–114

Defines `test_benchmark_specific_canned_repair_was_removed` and its implementation control flow; direct static calls: build_deterministic_domain_repair_answer, build_preflight_deterministic_answer, get_final_quality_issue.

### Lines 115–116

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 117–140

Defines `test_route_policy_blocks_unrelated_mutation_tool` and its implementation control flow; direct static calls: Agent, Path, _config, any, ask, dumps, mkdtemp, object, original_call, rmtree, write_text.

### Lines 141–142

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 143–160

Defines `test_successful_mutation_attaches_verification_evidence` and its implementation control flow; direct static calls: Agent, Path, _config, any, ask, dumps, mkdtemp, object, rmtree, write_text.

### Lines 161–162

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 163–171

Defines `run_agent_fallback_tests` and its implementation control flow; direct static calls: test_benchmark_specific_canned_repair_was_removed, test_canonical_final_and_route_state, test_generation_only_task_cannot_mutate_workspace, test_malformed_action_is_repaired_without_executing_loose_json, test_repository_answer_requires_real_tool_grounding, test_route_policy_blocks_unrelated_mutation_tool, test_successful_mutation_attaches_verification_evidence, test_system_prompt_has_strict_examples.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
