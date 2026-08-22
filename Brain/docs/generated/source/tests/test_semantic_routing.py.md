# `tests/test_semantic_routing.py`

## File purpose

This testing file is reviewed at snapshot `ce5c5c84c6582c45e91d90cd895bb93f4d974dbf65c59364bf4f114dcc1fe3da`. It contains 369 lines.

## Imports and module state

- [tests/test_semantic_routing.py:1](../../../../tests/test_semantic_routing.py#L1) imports `__future__` / annotations.
- [tests/test_semantic_routing.py:3](../../../../tests/test_semantic_routing.py#L3) imports `json`.
- [tests/test_semantic_routing.py:4](../../../../tests/test_semantic_routing.py#L4) imports `shutil`.
- [tests/test_semantic_routing.py:5](../../../../tests/test_semantic_routing.py#L5) imports `pathlib` / Path.
- [tests/test_semantic_routing.py:7](../../../../tests/test_semantic_routing.py#L7) imports `pytest`.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / AmbiguityLevel.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / Capability.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / ExpectedOutputMode.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / NormalizedIntent.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / RiskLevel.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / TargetKind.
- [tests/test_semantic_routing.py:9](../../../../tests/test_semantic_routing.py#L9) imports `mind01.intent` / TaskClass.
- [tests/test_semantic_routing.py:18](../../../../tests/test_semantic_routing.py#L18) imports `mind01.routing` / HierarchicalRouter.
- [tests/test_semantic_routing.py:18](../../../../tests/test_semantic_routing.py#L18) imports `mind01.routing` / ReasonCode.
- [tests/test_semantic_routing.py:18](../../../../tests/test_semantic_routing.py#L18) imports `mind01.routing` / RoutingDecision.
- [tests/test_semantic_routing.py:18](../../../../tests/test_semantic_routing.py#L18) imports `mind01.routing` / Specialist.
- [tests/test_semantic_routing.py:18](../../../../tests/test_semantic_routing.py#L18) imports `mind01.routing` / ToolFamily.
- [tests/test_semantic_routing.py:25](../../../../tests/test_semantic_routing.py#L25) imports `mind01.semantic_eval` / SemanticDatasetError.
- [tests/test_semantic_routing.py:25](../../../../tests/test_semantic_routing.py#L25) imports `mind01.semantic_eval` / run_deterministic_semantic_routing.
- [tests/test_semantic_routing.py:25](../../../../tests/test_semantic_routing.py#L25) imports `mind01.semantic_eval` / validate_external_blind_labels.
- [tests/test_semantic_routing.py:25](../../../../tests/test_semantic_routing.py#L25) imports `mind01.semantic_eval` / validate_semantic_routing_assets.
- [tests/test_semantic_routing.py:31](../../../../tests/test_semantic_routing.py#L31) imports `mind01.semantic_live_eval` / run_live_semantic_partition.
- [tests/test_semantic_routing.py:32](../../../../tests/test_semantic_routing.py#L32) imports `mind01.tool_exposure` / LifecyclePhase.
- [tests/test_semantic_routing.py:32](../../../../tests/test_semantic_routing.py#L32) imports `mind01.tool_exposure` / StaleRouteError.
- [tests/test_semantic_routing.py:32](../../../../tests/test_semantic_routing.py#L32) imports `mind01.tool_exposure` / ToolExposureAuthority.
- [tests/test_semantic_routing.py:32](../../../../tests/test_semantic_routing.py#L32) imports `mind01.tool_exposure` / ToolExposureContext.

## Symbols

### `tests.test_semantic_routing.ROOT` — lines 40–40

- Source: [tests/test_semantic_routing.py:40](../../../../tests/test_semantic_routing.py#L40)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.typed_route` — lines 43–56

- Source: [tests/test_semantic_routing.py:43](../../../../tests/test_semantic_routing.py#L43)
- Type: function
- Signature: `prompt: str, *, mode: str='read-only', write: bool=False, shell: bool=False`
- Direct static callees: `HierarchicalRouter`, `route_typed`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_all_typed_taxonomies_are_finite_and_nonempty` — lines 59–74

- Source: [tests/test_semantic_routing.py:59](../../../../tests/test_semantic_routing.py#L59)
- Type: function
- Signature: `n/a`
- Direct static callees: `len`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_intent_and_route_round_trip_reject_unknown_fields` — lines 77–95

- Source: [tests/test_semantic_routing.py:77](../../../../tests/test_semantic_routing.py#L77)
- Type: function
- Signature: `n/a`
- Direct static callees: `from_dict`, `raises`, `to_dict`, `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_modes_capabilities_and_confidence_fail_closed` — lines 98–116

- Source: [tests/test_semantic_routing.py:98](../../../../tests/test_semantic_routing.py#L98)
- Type: function
- Signature: `n/a`
- Direct static callees: `raises`, `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_proposal_apply_and_prior_inspection_are_distinct` — lines 119–198

- Source: [tests/test_semantic_routing.py:119](../../../../tests/test_semantic_routing.py#L119)
- Type: function
- Signature: `n/a`
- Direct static callees: `ToolExposureAuthority`, `build`, `decide`, `set`, `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_safe_fallback_no_fallback_and_stale_route` — lines 201–226

- Source: [tests/test_semantic_routing.py:201](../../../../tests/test_semantic_routing.py#L201)
- Type: function
- Signature: `n/a`
- Direct static callees: `ToolExposureAuthority`, `build`, `decide`, `raises`, `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_ambiguity_final_answer_and_equivalent_requests` — lines 229–251

- Source: [tests/test_semantic_routing.py:229](../../../../tests/test_semantic_routing.py#L229)
- Type: function
- Signature: `n/a`
- Direct static callees: `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_tool_exposure_is_stable_and_minimal` — lines 254–268

- Source: [tests/test_semantic_routing.py:254](../../../../tests/test_semantic_routing.py#L254)
- Type: function
- Signature: `n/a`
- Direct static callees: `ToolExposureAuthority`, `build`, `decide`, `set`, `typed_route`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_frozen_dataset_identity_and_blind_separation` — lines 271–297

- Source: [tests/test_semantic_routing.py:271](../../../../tests/test_semantic_routing.py#L271)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `copytree`, `mkdir`, `raises`, `read_text`, `validate_external_blind_labels`, `validate_semantic_routing_assets`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_deterministic_semantic_metrics_preserve_frozen_failures` — lines 300–326

- Source: [tests/test_semantic_routing.py:300](../../../../tests/test_semantic_routing.py#L300)
- Type: function
- Signature: `n/a`
- Direct static callees: `approx`, `run_deterministic_semantic_routing`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_semantic_routing.test_live_harness_retains_raw_case_evidence` — lines 329–369

- Source: [tests/test_semantic_routing.py:329](../../../../tests/test_semantic_routing.py#L329)
- Type: function
- Signature: `monkeypatch, tmp_path: Path`
- Direct static callees: `dumps`, `get`, `loads`, `read_text`, `run_live_semantic_partition`, `setattr`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–17

Imports a dependency used by this module.

### Lines 18–24

Imports a dependency used by this module.

### Lines 25–30

Imports a dependency used by this module.

### Lines 31–31

Imports a dependency used by this module.

### Lines 32–37

Imports a dependency used by this module.

### Lines 38–39

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 40–40

Implements module-level `Assign` behavior or data.

### Lines 41–42

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 43–56

Defines `typed_route` and its implementation control flow; direct static calls: HierarchicalRouter, route_typed.

### Lines 57–58

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 59–74

Defines `test_all_typed_taxonomies_are_finite_and_nonempty` and its implementation control flow; direct static calls: len, set.

### Lines 75–76

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 77–95

Defines `test_intent_and_route_round_trip_reject_unknown_fields` and its implementation control flow; direct static calls: from_dict, raises, to_dict, typed_route.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–116

Defines `test_modes_capabilities_and_confidence_fail_closed` and its implementation control flow; direct static calls: raises, typed_route.

### Lines 117–118

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 119–148

Defines `test_proposal_apply_and_prior_inspection_are_distinct` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, set, typed_route.

### Lines 149–178

Defines `test_proposal_apply_and_prior_inspection_are_distinct` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, set, typed_route.

### Lines 179–198

Defines `test_proposal_apply_and_prior_inspection_are_distinct` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, set, typed_route.

### Lines 199–200

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 201–226

Defines `test_safe_fallback_no_fallback_and_stale_route` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, raises, typed_route.

### Lines 227–228

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 229–251

Defines `test_ambiguity_final_answer_and_equivalent_requests` and its implementation control flow; direct static calls: typed_route.

### Lines 252–253

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 254–268

Defines `test_tool_exposure_is_stable_and_minimal` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, set, typed_route.

### Lines 269–270

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 271–297

Defines `test_frozen_dataset_identity_and_blind_separation` and its implementation control flow; direct static calls: copytree, mkdir, raises, read_text, validate_external_blind_labels, validate_semantic_routing_assets, write_text.

### Lines 298–299

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 300–326

Defines `test_deterministic_semantic_metrics_preserve_frozen_failures` and its implementation control flow; direct static calls: approx, run_deterministic_semantic_routing.

### Lines 327–328

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 329–358

Defines `test_live_harness_retains_raw_case_evidence` and its implementation control flow; direct static calls: dumps, get, loads, read_text, run_live_semantic_partition, setattr.

### Lines 359–369

Defines `test_live_harness_retains_raw_case_evidence` and its implementation control flow; direct static calls: dumps, get, loads, read_text, run_live_semantic_partition, setattr.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
