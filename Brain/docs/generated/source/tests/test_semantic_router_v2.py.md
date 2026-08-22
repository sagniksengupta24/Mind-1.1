# `tests/test_semantic_router_v2.py`

## File purpose

This testing file is reviewed at snapshot `8d9f2ef461da86dea858443e5c377a2caa9146a38f6ce4713ed5468ea9f65433`. It contains 439 lines.

## Imports and module state

- [tests/test_semantic_router_v2.py:1](../../../../tests/test_semantic_router_v2.py#L1) imports `__future__` / annotations.
- [tests/test_semantic_router_v2.py:3](../../../../tests/test_semantic_router_v2.py#L3) imports `json`.
- [tests/test_semantic_router_v2.py:4](../../../../tests/test_semantic_router_v2.py#L4) imports `pathlib` / Path.
- [tests/test_semantic_router_v2.py:6](../../../../tests/test_semantic_router_v2.py#L6) imports `pytest`.
- [tests/test_semantic_router_v2.py:8](../../../../tests/test_semantic_router_v2.py#L8) imports `mind01.agent` / Agent.
- [tests/test_semantic_router_v2.py:9](../../../../tests/test_semantic_router_v2.py#L9) imports `mind01.config` / AgentConfig.
- [tests/test_semantic_router_v2.py:10](../../../../tests/test_semantic_router_v2.py#L10) imports `mind01.intent` / ExpectedOutputMode.
- [tests/test_semantic_router_v2.py:10](../../../../tests/test_semantic_router_v2.py#L10) imports `mind01.intent` / TaskClass.
- [tests/test_semantic_router_v2.py:11](../../../../tests/test_semantic_router_v2.py#L11) imports `mind01.routing` / ReasonCode.
- [tests/test_semantic_router_v2.py:11](../../../../tests/test_semantic_router_v2.py#L11) imports `mind01.routing` / Specialist.
- [tests/test_semantic_router_v2.py:11](../../../../tests/test_semantic_router_v2.py#L11) imports `mind01.routing` / ToolFamily.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / FAMILY_LIFECYCLE.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / FAMILY_TOOLS.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / TASK_SPECIALIST_FAMILIES.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / TASK_SPECIALISTS.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / DecisionSource.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / FirstLifecycleStep.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / ModelCallStats.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / OllamaSemanticClassifier.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / RouteSelectionPrediction.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / RouterThresholds.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / SemanticRouterV2.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / TaskPrediction.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / normalize_request.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / parse_route_selection.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / parse_task_prediction.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / reduce_candidates.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / route_selection_schema.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / strict_json_object.
- [tests/test_semantic_router_v2.py:12](../../../../tests/test_semantic_router_v2.py#L12) imports `mind01.semantic_router_v2` / task_prediction_schema.
- [tests/test_semantic_router_v2.py:33](../../../../tests/test_semantic_router_v2.py#L33) imports `mind01.llm` / LLMError.
- [tests/test_semantic_router_v2.py:34](../../../../tests/test_semantic_router_v2.py#L34) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `tests.test_semantic_router_v2.ROOT` — lines 37–37

- Source: [tests/test_semantic_router_v2.py:37](../../../../tests/test_semantic_router_v2.py#L37)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.route` — lines 40–53

- Source: [tests/test_semantic_router_v2.py:40](../../../../tests/test_semantic_router_v2.py#L40)
- Type: function
- Signature: `prompt: str, *, mode: str='read-only', write: bool=False, shell: bool=False`
- Direct static callees: `SemanticRouterV2`, `route_typed`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_taxonomy_matrices_are_total_bounded_and_have_no_orphans` — lines 56–67

- Source: [tests/test_semantic_router_v2.py:56](../../../../tests/test_semantic_router_v2.py#L56)
- Type: function
- Signature: `n/a`
- Direct static callees: `all`, `items`, `len`, `map`, `set`, `union`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_normalization_features_are_bounded_hints` — lines 70–80

- Source: [tests/test_semantic_router_v2.py:70](../../../../tests/test_semantic_router_v2.py#L70)
- Type: function
- Signature: `n/a`
- Direct static callees: `len`, `normalize_request`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_policy_response_and_tool_intersection_fail_closed` — lines 83–112

- Source: [tests/test_semantic_router_v2.py:83](../../../../tests/test_semantic_router_v2.py#L83)
- Type: function
- Signature: `n/a`
- Direct static callees: `route`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_lifecycle_never_mutates_before_inspection` — lines 115–136

- Source: [tests/test_semantic_router_v2.py:115](../../../../tests/test_semantic_router_v2.py#L115)
- Type: function
- Signature: `n/a`
- Direct static callees: `route`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_reason_codes_are_derived_from_resolved_fields` — lines 139–153

- Source: [tests/test_semantic_router_v2.py:139](../../../../tests/test_semantic_router_v2.py#L139)
- Type: function
- Signature: `n/a`
- Direct static callees: `len`, `route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.LowConfidenceClassifier` — lines 156–172

- Source: [tests/test_semantic_router_v2.py:156](../../../../tests/test_semantic_router_v2.py#L156)
- Type: class
- Signature: `n/a`
- Direct static callees: `ModelCallStats`, `RouteSelectionPrediction`, `TaskPrediction`, `iter`, `next`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.LowConfidenceClassifier.__init__` — lines 159–160

- Source: [tests/test_semantic_router_v2.py:159](../../../../tests/test_semantic_router_v2.py#L159)
- Type: method
- Signature: `self`
- Direct static callees: `ModelCallStats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.LowConfidenceClassifier.predict_task` — lines 162–163

- Source: [tests/test_semantic_router_v2.py:162](../../../../tests/test_semantic_router_v2.py#L162)
- Type: method
- Signature: `self, request`
- Direct static callees: `TaskPrediction`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.LowConfidenceClassifier.select_route` — lines 165–172

- Source: [tests/test_semantic_router_v2.py:165](../../../../tests/test_semantic_router_v2.py#L165)
- Type: method
- Signature: `self, request, task_class, candidates`
- Direct static callees: `RouteSelectionPrediction`, `iter`, `next`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_low_confidence_abstains_without_permission_expansion` — lines 175–188

- Source: [tests/test_semantic_router_v2.py:175](../../../../tests/test_semantic_router_v2.py#L175)
- Type: function
- Signature: `n/a`
- Direct static callees: `LowConfidenceClassifier`, `RouterThresholds`, `SemanticRouterV2`, `any`, `route_typed`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.ContradictoryClassifier` — lines 191–217

- Source: [tests/test_semantic_router_v2.py:191](../../../../tests/test_semantic_router_v2.py#L191)
- Type: class
- Signature: `n/a`
- Direct static callees: `ModelCallStats`, `RouteSelectionPrediction`, `TaskPrediction`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.ContradictoryClassifier.__init__` — lines 194–196

- Source: [tests/test_semantic_router_v2.py:194](../../../../tests/test_semantic_router_v2.py#L194)
- Type: method
- Signature: `self, *, verification: bool=False`
- Direct static callees: `ModelCallStats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.ContradictoryClassifier.predict_task` — lines 198–202

- Source: [tests/test_semantic_router_v2.py:198](../../../../tests/test_semantic_router_v2.py#L198)
- Type: method
- Signature: `self, request`
- Direct static callees: `TaskPrediction`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.ContradictoryClassifier.select_route` — lines 204–217

- Source: [tests/test_semantic_router_v2.py:204](../../../../tests/test_semantic_router_v2.py#L204)
- Type: method
- Signature: `self, request, task_class, candidates`
- Direct static callees: `RouteSelectionPrediction`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_model_policy_and_execution_family_disagreements_are_bounded` — lines 220–243

- Source: [tests/test_semantic_router_v2.py:220](../../../../tests/test_semantic_router_v2.py#L220)
- Type: function
- Signature: `n/a`
- Direct static callees: `ContradictoryClassifier`, `SemanticRouterV2`, `next`, `route_typed`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.valid_task_payload` — lines 246–253

- Source: [tests/test_semantic_router_v2.py:246](../../../../tests/test_semantic_router_v2.py#L246)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_task_parser_rejects_malformed_or_unconstrained_output` — lines 270–272

- Source: [tests/test_semantic_router_v2.py:270](../../../../tests/test_semantic_router_v2.py#L270)
- Type: function
- Signature: `raw: str`
- Direct static callees: `dumps`, `parametrize`, `parse_task_prediction`, `raises`, `valid_task_payload`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_strict_parsers_and_schemas_accept_only_shortlisted_values` — lines 275–306

- Source: [tests/test_semantic_router_v2.py:275](../../../../tests/test_semantic_router_v2.py#L275)
- Type: function
- Signature: `n/a`
- Direct static callees: `dumps`, `normalize_request`, `parse_route_selection`, `parse_task_prediction`, `raises`, `reduce_candidates`, `route_selection_schema`, `strict_json_object`, `task_prediction_schema`, `valid_task_payload`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_every_final_route_has_trace_sources_and_passes_solver` — lines 309–338

- Source: [tests/test_semantic_router_v2.py:309](../../../../tests/test_semantic_router_v2.py#L309)
- Type: function
- Signature: `n/a`
- Direct static callees: `route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_v2_feature_flag_and_comparison_mode_preserve_runtime_contract` — lines 341–369

- Source: [tests/test_semantic_router_v2.py:341](../../../../tests/test_semantic_router_v2.py#L341)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `Agent`, `ask`, `build`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_invalid_router_configuration_is_rejected` — lines 372–374

- Source: [tests/test_semantic_router_v2.py:372](../../../../tests/test_semantic_router_v2.py#L372)
- Type: function
- Signature: `n/a`
- Direct static callees: `build`, `raises`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.QueuedClient` — lines 377–387

- Source: [tests/test_semantic_router_v2.py:377](../../../../tests/test_semantic_router_v2.py#L377)
- Type: class
- Signature: `n/a`
- Direct static callees: `isinstance`, `list`, `pop`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.QueuedClient.__init__` — lines 380–381

- Source: [tests/test_semantic_router_v2.py:380](../../../../tests/test_semantic_router_v2.py#L380)
- Type: method
- Signature: `self, outputs`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.QueuedClient.chat` — lines 383–387

- Source: [tests/test_semantic_router_v2.py:383](../../../../tests/test_semantic_router_v2.py#L383)
- Type: method
- Signature: `self, messages, json_mode=True, *, response_schema=None`
- Direct static callees: `isinstance`, `pop`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.route_payload` — lines 390–399

- Source: [tests/test_semantic_router_v2.py:390](../../../../tests/test_semantic_router_v2.py#L390)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_model_classifier_normal_budget_and_bounded_repair` — lines 402–418

- Source: [tests/test_semantic_router_v2.py:402](../../../../tests/test_semantic_router_v2.py#L402)
- Type: function
- Signature: `n/a`
- Direct static callees: `OllamaSemanticClassifier`, `QueuedClient`, `SemanticRouterV2`, `dumps`, `route_payload`, `route_typed`, `valid_task_payload`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_router_v2.test_model_classifier_repair_exhaustion_and_timeout_fall_back_safely` — lines 421–439

- Source: [tests/test_semantic_router_v2.py:421](../../../../tests/test_semantic_router_v2.py#L421)
- Type: function
- Signature: `n/a`
- Direct static callees: `LLMError`, `OllamaSemanticClassifier`, `QueuedClient`, `SemanticRouterV2`, `route_typed`, `set`
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

### Lines 12–32

Imports a dependency used by this module.

### Lines 33–33

Imports a dependency used by this module.

### Lines 34–34

Imports a dependency used by this module.

### Lines 35–36

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 37–37

Implements module-level `Assign` behavior or data.

### Lines 38–39

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 40–53

Defines `route` and its implementation control flow; direct static calls: SemanticRouterV2, route_typed.

### Lines 54–55

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 56–67

Defines `test_taxonomy_matrices_are_total_bounded_and_have_no_orphans` and its implementation control flow; direct static calls: all, items, len, map, set, union, values.

### Lines 68–69

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 70–80

Defines `test_normalization_features_are_bounded_hints` and its implementation control flow; direct static calls: len, normalize_request.

### Lines 81–82

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 83–112

Defines `test_policy_response_and_tool_intersection_fail_closed` and its implementation control flow; direct static calls: route, set.

### Lines 113–114

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 115–136

Defines `test_lifecycle_never_mutates_before_inspection` and its implementation control flow; direct static calls: route, set.

### Lines 137–138

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 139–153

Defines `test_reason_codes_are_derived_from_resolved_fields` and its implementation control flow; direct static calls: len, route.

### Lines 154–155

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 156–172

Defines class `LowConfidenceClassifier` and the behavior of its members.

### Lines 173–174

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 175–188

Defines `test_low_confidence_abstains_without_permission_expansion` and its implementation control flow; direct static calls: LowConfidenceClassifier, RouterThresholds, SemanticRouterV2, any, route_typed, set.

### Lines 189–190

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 191–217

Defines class `ContradictoryClassifier` and the behavior of its members.

### Lines 218–219

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 220–243

Defines `test_model_policy_and_execution_family_disagreements_are_bounded` and its implementation control flow; direct static calls: ContradictoryClassifier, SemanticRouterV2, next, route_typed.

### Lines 244–245

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 246–253

Defines `valid_task_payload` and its implementation control flow; direct static calls: none resolved.

### Lines 254–269

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 270–272

Defines `test_task_parser_rejects_malformed_or_unconstrained_output` and its implementation control flow; direct static calls: dumps, parametrize, parse_task_prediction, raises, valid_task_payload.

### Lines 273–274

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 275–304

Defines `test_strict_parsers_and_schemas_accept_only_shortlisted_values` and its implementation control flow; direct static calls: dumps, normalize_request, parse_route_selection, parse_task_prediction, raises, reduce_candidates, route_selection_schema, strict_json_object, task_prediction_schema, valid_task_payload.

### Lines 305–306

Defines `test_strict_parsers_and_schemas_accept_only_shortlisted_values` and its implementation control flow; direct static calls: dumps, normalize_request, parse_route_selection, parse_task_prediction, raises, reduce_candidates, route_selection_schema, strict_json_object, task_prediction_schema, valid_task_payload.

### Lines 307–308

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 309–338

Defines `test_every_final_route_has_trace_sources_and_passes_solver` and its implementation control flow; direct static calls: route.

### Lines 339–340

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 341–369

Defines `test_v2_feature_flag_and_comparison_mode_preserve_runtime_contract` and its implementation control flow; direct static calls: Agent, ask, build, str.

### Lines 370–371

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 372–374

Defines `test_invalid_router_configuration_is_rejected` and its implementation control flow; direct static calls: build, raises.

### Lines 375–376

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 377–387

Defines class `QueuedClient` and the behavior of its members.

### Lines 388–389

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 390–399

Defines `route_payload` and its implementation control flow; direct static calls: none resolved.

### Lines 400–401

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 402–418

Defines `test_model_classifier_normal_budget_and_bounded_repair` and its implementation control flow; direct static calls: OllamaSemanticClassifier, QueuedClient, SemanticRouterV2, dumps, route_payload, route_typed, valid_task_payload.

### Lines 419–420

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 421–439

Defines `test_model_classifier_repair_exhaustion_and_timeout_fall_back_safely` and its implementation control flow; direct static calls: LLMError, OllamaSemanticClassifier, QueuedClient, SemanticRouterV2, route_typed, set.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
