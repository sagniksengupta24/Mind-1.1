# `tests/test_action_reliability.py`

## File purpose

This testing file is reviewed at snapshot `296a9dfe7b2dd44b19c22ae7d4803ca6715ca50583934332ada1b105d1479337`. It contains 219 lines.

## Imports and module state

- [tests/test_action_reliability.py:1](../../../../tests/test_action_reliability.py#L1) imports `__future__` / annotations.
- [tests/test_action_reliability.py:3](../../../../tests/test_action_reliability.py#L3) imports `json`.
- [tests/test_action_reliability.py:4](../../../../tests/test_action_reliability.py#L4) imports `shutil`.
- [tests/test_action_reliability.py:5](../../../../tests/test_action_reliability.py#L5) imports `tempfile`.
- [tests/test_action_reliability.py:6](../../../../tests/test_action_reliability.py#L6) imports `urllib.error`.
- [tests/test_action_reliability.py:7](../../../../tests/test_action_reliability.py#L7) imports `io` / BytesIO.
- [tests/test_action_reliability.py:8](../../../../tests/test_action_reliability.py#L8) imports `pathlib` / Path.
- [tests/test_action_reliability.py:9](../../../../tests/test_action_reliability.py#L9) imports `unittest.mock` / patch.
- [tests/test_action_reliability.py:11](../../../../tests/test_action_reliability.py#L11) imports `mind01.action_parser` / ResponseMode.
- [tests/test_action_reliability.py:11](../../../../tests/test_action_reliability.py#L11) imports `mind01.action_parser` / canonical_response_schema.
- [tests/test_action_reliability.py:11](../../../../tests/test_action_reliability.py#L11) imports `mind01.action_parser` / parse_action_output.
- [tests/test_action_reliability.py:12](../../../../tests/test_action_reliability.py#L12) imports `mind01.agent` / _runtime_completion_status.
- [tests/test_action_reliability.py:12](../../../../tests/test_action_reliability.py#L12) imports `mind01.agent` / _visible_tools.
- [tests/test_action_reliability.py:13](../../../../tests/test_action_reliability.py#L13) imports `mind01.agent` / Agent.
- [tests/test_action_reliability.py:14](../../../../tests/test_action_reliability.py#L14) imports `mind01.config` / AgentConfig.
- [tests/test_action_reliability.py:15](../../../../tests/test_action_reliability.py#L15) imports `mind01.eval` / run_mock_protocol_regression.
- [tests/test_action_reliability.py:16](../../../../tests/test_action_reliability.py#L16) imports `mind01.eval_harness` / _fixture_acceptance.
- [tests/test_action_reliability.py:16](../../../../tests/test_action_reliability.py#L16) imports `mind01.eval_harness` / aggregate_parser_report.
- [tests/test_action_reliability.py:16](../../../../tests/test_action_reliability.py#L16) imports `mind01.eval_harness` / build_action_report.
- [tests/test_action_reliability.py:17](../../../../tests/test_action_reliability.py#L17) imports `mind01.eval_schema` / load_action_suite.
- [tests/test_action_reliability.py:18](../../../../tests/test_action_reliability.py#L18) imports `mind01.llm` / OllamaClient.
- [tests/test_action_reliability.py:19](../../../../tests/test_action_reliability.py#L19) imports `mind01.llm` / LLMError.
- [tests/test_action_reliability.py:20](../../../../tests/test_action_reliability.py#L20) imports `mind01.modes` / AgentMode.
- [tests/test_action_reliability.py:21](../../../../tests/test_action_reliability.py#L21) imports `mind01.routing` / HierarchicalRouter.
- [tests/test_action_reliability.py:22](../../../../tests/test_action_reliability.py#L22) imports `mind01.state` / AgentState.
- [tests/test_action_reliability.py:23](../../../../tests/test_action_reliability.py#L23) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.
- [tests/test_action_reliability.py:24](../../../../tests/test_action_reliability.py#L24) imports `mind01.verification` / VerificationEngine.
- [tests/test_action_reliability.py:25](../../../../tests/test_action_reliability.py#L25) imports `mind01.completion` / VerificationEvidence.
- [tests/test_action_reliability.py:25](../../../../tests/test_action_reliability.py#L25) imports `mind01.completion` / normalize_completion_status.

## Symbols

### `tests.test_action_reliability.FakeResponse` — lines 28–39

- Source: [tests/test_action_reliability.py:28](../../../../tests/test_action_reliability.py#L28)
- Type: class
- Signature: `n/a`
- Direct static callees: `dumps`, `encode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.FakeResponse.__init__` — lines 29–30

- Source: [tests/test_action_reliability.py:29](../../../../tests/test_action_reliability.py#L29)
- Type: method
- Signature: `self, payload: dict`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.FakeResponse.__enter__` — lines 32–33

- Source: [tests/test_action_reliability.py:32](../../../../tests/test_action_reliability.py#L32)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.FakeResponse.__exit__` — lines 35–36

- Source: [tests/test_action_reliability.py:35](../../../../tests/test_action_reliability.py#L35)
- Type: method
- Signature: `self, *args`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.FakeResponse.read` — lines 38–39

- Source: [tests/test_action_reliability.py:38](../../../../tests/test_action_reliability.py#L38)
- Type: method
- Signature: `self`
- Direct static callees: `dumps`, `encode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_action_suite_is_versioned_and_has_fifty_cases` — lines 42–46

- Source: [tests/test_action_reliability.py:42](../../../../tests/test_action_reliability.py#L42)
- Type: function
- Signature: `n/a`
- Direct static callees: `len`, `load_action_suite`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_every_visible_schema_matches_runtime_validation` — lines 49–54

- Source: [tests/test_action_reliability.py:49](../../../../tests/test_action_reliability.py#L49)
- Type: function
- Signature: `n/a`
- Direct static callees: `canonical_response_schema`, `issubset`, `load_action_suite`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_mock_protocol_regression_is_explicitly_mocked` — lines 57–60

- Source: [tests/test_action_reliability.py:57](../../../../tests/test_action_reliability.py#L57)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_mock_protocol_regression`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_inspection_phase_hides_mutation_tools` — lines 63–70

- Source: [tests/test_action_reliability.py:63](../../../../tests/test_action_reliability.py#L63)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentState`, `HierarchicalRouter`, `Path`, `_visible_tools`, `route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_server_route_still_limits_visible_tools` — lines 73–76

- Source: [tests/test_action_reliability.py:73](../../../../tests/test_action_reliability.py#L73)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentState`, `HierarchicalRouter`, `Path`, `_visible_tools`, `route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_runtime_downgrades_verified_without_evidence` — lines 79–82

- Source: [tests/test_action_reliability.py:79](../../../../tests/test_action_reliability.py#L79)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentState`, `_runtime_completion_status`, `dumps`, `parse_action_output`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_runtime_accepts_verified_with_referenced_evidence` — lines 85–90

- Source: [tests/test_action_reliability.py:85](../../../../tests/test_action_reliability.py#L85)
- Type: function
- Signature: `n/a`
- Direct static callees: `AgentState`, `_runtime_completion_status`, `append`, `dumps`, `parse_action_output`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_ollama_json_schema_capability_detection_supported` — lines 93–97

- Source: [tests/test_action_reliability.py:93](../../../../tests/test_action_reliability.py#L93)
- Type: function
- Signature: `n/a`
- Direct static callees: `FakeResponse`, `OllamaClient`, `patch`, `supports_json_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_ollama_json_schema_capability_detection_fallback` — lines 100–103

- Source: [tests/test_action_reliability.py:100](../../../../tests/test_action_reliability.py#L100)
- Type: function
- Signature: `n/a`
- Direct static callees: `OSError`, `OllamaClient`, `patch`, `supports_json_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_ollama_missing_model_404_is_reported_as_missing_model` — lines 106–124

- Source: [tests/test_action_reliability.py:106](../../../../tests/test_action_reliability.py#L106)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `BytesIO`, `HTTPError`, `OllamaClient`, `chat`, `object`, `patch`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_ollama_schema_rejection_falls_back_only_for_400_or_422` — lines 127–138

- Source: [tests/test_action_reliability.py:127](../../../../tests/test_action_reliability.py#L127)
- Type: function
- Signature: `n/a`
- Direct static callees: `LLMError`, `OllamaClient`, `chat`, `object`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_real_mutation_templates_fail_preconditions` — lines 141–155

- Source: [tests/test_action_reliability.py:141](../../../../tests/test_action_reliability.py#L141)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `TemporaryDirectory`, `_fixture_acceptance`, `copytree`, `rename`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_invalid_syntax_is_not_shipped_as_python_source` — lines 158–161

- Source: [tests/test_action_reliability.py:158](../../../../tests/test_action_reliability.py#L158)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `exists`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_parser_report_aggregates_without_raw_output` — lines 164–179

- Source: [tests/test_action_reliability.py:164](../../../../tests/test_action_reliability.py#L164)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `aggregate_parser_report`, `dumps`, `exists`, `mkdir`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_python_verifier_rejects_definitions_trapped_in_strings` — lines 182–188

- Source: [tests/test_action_reliability.py:182](../../../../tests/test_action_reliability.py#L182)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `VerificationEngine`, `next`, `verify_paths`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_completion_overrides_failed_when_acceptance_proves_success` — lines 191–195

- Source: [tests/test_action_reliability.py:191](../../../../tests/test_action_reliability.py#L191)
- Type: function
- Signature: `n/a`
- Direct static callees: `VerificationEvidence`, `normalize_completion_status`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_action_reliability.test_non_executable_mutation_is_rolled_back_then_repaired` — lines 198–219

- Source: [tests/test_action_reliability.py:198](../../../../tests/test_action_reliability.py#L198)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `Agent`, `any`, `ask`, `build`, `dumps`, `object`, `read_text`, `startswith`, `str`, `write_text`
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

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–21

Imports a dependency used by this module.

### Lines 22–22

Imports a dependency used by this module.

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports a dependency used by this module.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–27

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 28–39

Defines class `FakeResponse` and the behavior of its members.

### Lines 40–41

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 42–46

Defines `test_action_suite_is_versioned_and_has_fifty_cases` and its implementation control flow; direct static calls: len, load_action_suite.

### Lines 47–48

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 49–54

Defines `test_every_visible_schema_matches_runtime_validation` and its implementation control flow; direct static calls: canonical_response_schema, issubset, load_action_suite, set.

### Lines 55–56

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 57–60

Defines `test_mock_protocol_regression_is_explicitly_mocked` and its implementation control flow; direct static calls: run_mock_protocol_regression.

### Lines 61–62

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 63–70

Defines `test_inspection_phase_hides_mutation_tools` and its implementation control flow; direct static calls: AgentState, HierarchicalRouter, Path, _visible_tools, route.

### Lines 71–72

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 73–76

Defines `test_server_route_still_limits_visible_tools` and its implementation control flow; direct static calls: AgentState, HierarchicalRouter, Path, _visible_tools, route.

### Lines 77–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–82

Defines `test_runtime_downgrades_verified_without_evidence` and its implementation control flow; direct static calls: AgentState, _runtime_completion_status, dumps, parse_action_output.

### Lines 83–84

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 85–90

Defines `test_runtime_accepts_verified_with_referenced_evidence` and its implementation control flow; direct static calls: AgentState, _runtime_completion_status, append, dumps, parse_action_output.

### Lines 91–92

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 93–97

Defines `test_ollama_json_schema_capability_detection_supported` and its implementation control flow; direct static calls: FakeResponse, OllamaClient, patch, supports_json_schema.

### Lines 98–99

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 100–103

Defines `test_ollama_json_schema_capability_detection_fallback` and its implementation control flow; direct static calls: OSError, OllamaClient, patch, supports_json_schema.

### Lines 104–105

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 106–124

Defines `test_ollama_missing_model_404_is_reported_as_missing_model` and its implementation control flow; direct static calls: AssertionError, BytesIO, HTTPError, OllamaClient, chat, object, patch, str.

### Lines 125–126

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 127–138

Defines `test_ollama_schema_rejection_falls_back_only_for_400_or_422` and its implementation control flow; direct static calls: LLMError, OllamaClient, chat, object.

### Lines 139–140

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 141–155

Defines `test_real_mutation_templates_fail_preconditions` and its implementation control flow; direct static calls: Path, TemporaryDirectory, _fixture_acceptance, copytree, rename, resolve.

### Lines 156–157

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 158–161

Defines `test_invalid_syntax_is_not_shipped_as_python_source` and its implementation control flow; direct static calls: Path, exists, resolve.

### Lines 162–163

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 164–179

Defines `test_parser_report_aggregates_without_raw_output` and its implementation control flow; direct static calls: aggregate_parser_report, dumps, exists, mkdir, write_text.

### Lines 180–181

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 182–188

Defines `test_python_verifier_rejects_definitions_trapped_in_strings` and its implementation control flow; direct static calls: VerificationEngine, next, verify_paths, write_text.

### Lines 189–190

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 191–195

Defines `test_completion_overrides_failed_when_acceptance_proves_success` and its implementation control flow; direct static calls: VerificationEvidence, normalize_completion_status.

### Lines 196–197

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 198–219

Defines `test_non_executable_mutation_is_rolled_back_then_repaired` and its implementation control flow; direct static calls: Agent, any, ask, build, dumps, object, read_text, startswith, str, write_text.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
