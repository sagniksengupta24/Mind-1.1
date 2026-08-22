# `mind01/semantic_eval.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `19d2ed49d1f898c08f95f01d1f904618544164ef1beeedbcd6d6171ead14f5aa`. It contains 425 lines.

## Imports and module state

- [mind01/semantic_eval.py:1](../../../../mind01/semantic_eval.py#L1) imports `__future__` / annotations.
- [mind01/semantic_eval.py:3](../../../../mind01/semantic_eval.py#L3) imports `hashlib`.
- [mind01/semantic_eval.py:4](../../../../mind01/semantic_eval.py#L4) imports `json`.
- [mind01/semantic_eval.py:5](../../../../mind01/semantic_eval.py#L5) imports `re`.
- [mind01/semantic_eval.py:6](../../../../mind01/semantic_eval.py#L6) imports `statistics`.
- [mind01/semantic_eval.py:7](../../../../mind01/semantic_eval.py#L7) imports `time`.
- [mind01/semantic_eval.py:8](../../../../mind01/semantic_eval.py#L8) imports `collections` / Counter.
- [mind01/semantic_eval.py:8](../../../../mind01/semantic_eval.py#L8) imports `collections` / defaultdict.
- [mind01/semantic_eval.py:9](../../../../mind01/semantic_eval.py#L9) imports `pathlib` / Path.
- [mind01/semantic_eval.py:10](../../../../mind01/semantic_eval.py#L10) imports `typing` / Any.
- [mind01/semantic_eval.py:10](../../../../mind01/semantic_eval.py#L10) imports `typing` / Iterable.
- [mind01/semantic_eval.py:12](../../../../mind01/semantic_eval.py#L12) imports `intent` / Capability.
- [mind01/semantic_eval.py:12](../../../../mind01/semantic_eval.py#L12) imports `intent` / ExpectedOutputMode.
- [mind01/semantic_eval.py:12](../../../../mind01/semantic_eval.py#L12) imports `intent` / TaskClass.
- [mind01/semantic_eval.py:13](../../../../mind01/semantic_eval.py#L13) imports `routing` / HierarchicalRouter.
- [mind01/semantic_eval.py:13](../../../../mind01/semantic_eval.py#L13) imports `routing` / RoutingDecision.
- [mind01/semantic_eval.py:13](../../../../mind01/semantic_eval.py#L13) imports `routing` / ToolFamily.
- [mind01/semantic_eval.py:14](../../../../mind01/semantic_eval.py#L14) imports `tool_exposure` / LifecyclePhase.
- [mind01/semantic_eval.py:14](../../../../mind01/semantic_eval.py#L14) imports `tool_exposure` / ToolExposureAuthority.
- [mind01/semantic_eval.py:14](../../../../mind01/semantic_eval.py#L14) imports `tool_exposure` / ToolExposureContext.
- [mind01/semantic_eval.py:15](../../../../mind01/semantic_eval.py#L15) imports `tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `mind01.semantic_eval.ROOT` — lines 18–18

- Source: [mind01/semantic_eval.py:18](../../../../mind01/semantic_eval.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.SUITE_ROOT` — lines 19–19

- Source: [mind01/semantic_eval.py:19](../../../../mind01/semantic_eval.py#L19)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.PARTITION_FILES` — lines 20–27

- Source: [mind01/semantic_eval.py:20](../../../../mind01/semantic_eval.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.MINIMUM_CASES` — lines 28–35

- Source: [mind01/semantic_eval.py:28](../../../../mind01/semantic_eval.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.VALID_MODES` — lines 36–36

- Source: [mind01/semantic_eval.py:36](../../../../mind01/semantic_eval.py#L36)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.MODE_MAP` — lines 37–42

- Source: [mind01/semantic_eval.py:37](../../../../mind01/semantic_eval.py#L37)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.WRITE_TOOLS` — lines 43–43

- Source: [mind01/semantic_eval.py:43](../../../../mind01/semantic_eval.py#L43)
- Type: constant
- Signature: `n/a`
- Direct static callees: `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.SHELL_TOOLS` — lines 44–44

- Source: [mind01/semantic_eval.py:44](../../../../mind01/semantic_eval.py#L44)
- Type: constant
- Signature: `n/a`
- Direct static callees: `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.MUTATING_RUNTIME_TOOLS` — lines 45–47

- Source: [mind01/semantic_eval.py:45](../../../../mind01/semantic_eval.py#L45)
- Type: constant
- Signature: `n/a`
- Direct static callees: `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.LABELED_FIELDS` — lines 48–48

- Source: [mind01/semantic_eval.py:48](../../../../mind01/semantic_eval.py#L48)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.SemanticDatasetError` — lines 51–52

- Source: [mind01/semantic_eval.py:51](../../../../mind01/semantic_eval.py#L51)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.sha256_file` — lines 55–56

- Source: [mind01/semantic_eval.py:55](../../../../mind01/semantic_eval.py#L55)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.load_partition` — lines 59–68

- Source: [mind01/semantic_eval.py:59](../../../../mind01/semantic_eval.py#L59)
- Type: function
- Signature: `partition: str`
- Direct static callees: `SemanticDatasetError`, `get`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.validate_semantic_routing_assets` — lines 71–135

- Source: [mind01/semantic_eval.py:71](../../../../mind01/semantic_eval.py#L71)
- Type: function
- Signature: `root: Path=ROOT`
- Direct static callees: `SemanticDatasetError`, `_tokens`, `_validate_case`, `add`, `append`, `get`, `isinstance`, `items`, `len`, `loads`, `read_text`, `set`, `sha256_file`, `sum`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.run_deterministic_semantic_routing` — lines 138–290

- Source: [mind01/semantic_eval.py:138](../../../../mind01/semantic_eval.py#L138)
- Type: function
- Signature: `partitions: Iterable[str]=('development', 'regression', 'adversarial', 'capability_mode', 'ambiguity')`
- Direct static callees: `HierarchicalRouter`, `SemanticDatasetError`, `ToolExposureAuthority`, `_clarification_accuracy`, `_evaluation_phase`, `_failure_taxonomy`, `_group_performance`, `_incorrect_autonomous_assumption_rate`, `_unnecessary_clarification_rate`, `all`, `append`, `bool`, `build`, `decide`, `defaultdict`, `fmean`, `from_dict`, `getattr`, `items`, `len`, `list`, `load_partition`, `metric`, `perf_counter`, `round`, `route_typed`, `set`, `sorted`, `str`, `sum`, `to_dict`, `validate_semantic_routing_assets`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval.validate_external_blind_labels` — lines 293–310

- Source: [mind01/semantic_eval.py:293](../../../../mind01/semantic_eval.py#L293)
- Type: function
- Signature: `path: Path, expected_input_hash: str`
- Direct static callees: `SemanticDatasetError`, `get`, `isinstance`, `len`, `loads`, `read_text`, `resolve`, `sha256_file`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._validate_case` — lines 313–350

- Source: [mind01/semantic_eval.py:313](../../../../mind01/semantic_eval.py#L313)
- Type: function
- Signature: `case: Any, partition: str`
- Direct static callees: `SemanticDatasetError`, `all`, `get`, `isinstance`, `len`, `set`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._tokens` — lines 353–354

- Source: [mind01/semantic_eval.py:353](../../../../mind01/semantic_eval.py#L353)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `findall`, `lower`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._evaluation_phase` — lines 357–364

- Source: [mind01/semantic_eval.py:357](../../../../mind01/semantic_eval.py#L357)
- Type: function
- Signature: `route: RoutingDecision`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._failure_taxonomy` — lines 367–376

- Source: [mind01/semantic_eval.py:367](../../../../mind01/semantic_eval.py#L367)
- Type: function
- Signature: `failures: list[dict[str, Any]]`
- Direct static callees: `Counter`, `dict`, `items`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._group_performance` — lines 379–398

- Source: [mind01/semantic_eval.py:379](../../../../mind01/semantic_eval.py#L379)
- Type: function
- Signature: `results: list[dict[str, Any]], field: str, *, expected_field: bool=False`
- Direct static callees: `append`, `defaultdict`, `items`, `len`, `sorted`, `str`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._clarification_accuracy` — lines 401–409

- Source: [mind01/semantic_eval.py:401](../../../../mind01/semantic_eval.py#L401)
- Type: function
- Signature: `results: list[dict[str, Any]]`
- Direct static callees: `len`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._unnecessary_clarification_rate` — lines 412–417

- Source: [mind01/semantic_eval.py:412](../../../../mind01/semantic_eval.py#L412)
- Type: function
- Signature: `results: list[dict[str, Any]]`
- Direct static callees: `len`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval._incorrect_autonomous_assumption_rate` — lines 420–425

- Source: [mind01/semantic_eval.py:420](../../../../mind01/semantic_eval.py#L420)
- Type: function
- Signature: `results: list[dict[str, Any]]`
- Direct static callees: `len`, `sum`
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

Imports a dependency used by this module.

### Lines 11–11

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–18

Implements module-level `Assign` behavior or data.

### Lines 19–19

Implements module-level `Assign` behavior or data.

### Lines 20–27

Implements module-level `Assign` behavior or data.

### Lines 28–35

Implements module-level `Assign` behavior or data.

### Lines 36–36

Implements module-level `Assign` behavior or data.

### Lines 37–42

Implements module-level `Assign` behavior or data.

### Lines 43–43

Implements module-level `Assign` behavior or data.

### Lines 44–44

Implements module-level `Assign` behavior or data.

### Lines 45–47

Implements module-level `Assign` behavior or data.

### Lines 48–48

Implements module-level `Assign` behavior or data.

### Lines 49–50

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 51–52

Defines class `SemanticDatasetError` and the behavior of its members.

### Lines 53–54

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 55–56

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

### Lines 57–58

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 59–68

Defines `load_partition` and its implementation control flow; direct static calls: SemanticDatasetError, get, isinstance, loads, read_text.

### Lines 69–70

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 71–100

Defines `validate_semantic_routing_assets` and its implementation control flow; direct static calls: SemanticDatasetError, _tokens, _validate_case, add, append, get, isinstance, items, len, loads, read_text, set, sha256_file, sum, values.

### Lines 101–130

Defines `validate_semantic_routing_assets` and its implementation control flow; direct static calls: SemanticDatasetError, _tokens, _validate_case, add, append, get, isinstance, items, len, loads, read_text, set, sha256_file, sum, values.

### Lines 131–135

Defines `validate_semantic_routing_assets` and its implementation control flow; direct static calls: SemanticDatasetError, _tokens, _validate_case, add, append, get, isinstance, items, len, loads, read_text, set, sha256_file, sum, values.

### Lines 136–137

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 138–167

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 168–197

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 198–227

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 228–257

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 258–287

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 288–290

Defines `run_deterministic_semantic_routing` and its implementation control flow; direct static calls: HierarchicalRouter, SemanticDatasetError, ToolExposureAuthority, _clarification_accuracy, _evaluation_phase, _failure_taxonomy, _group_performance, _incorrect_autonomous_assumption_rate, _unnecessary_clarification_rate, all, append, bool, build, decide, defaultdict, fmean, from_dict, getattr, items, len, list, load_partition, metric, perf_counter, round, route_typed, set, sorted, str, sum, to_dict, validate_semantic_routing_assets, values.

### Lines 291–292

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 293–310

Defines `validate_external_blind_labels` and its implementation control flow; direct static calls: SemanticDatasetError, get, isinstance, len, loads, read_text, resolve, sha256_file, str.

### Lines 311–312

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 313–342

Defines `_validate_case` and its implementation control flow; direct static calls: SemanticDatasetError, all, get, isinstance, len, set, values.

### Lines 343–350

Defines `_validate_case` and its implementation control flow; direct static calls: SemanticDatasetError, all, get, isinstance, len, set, values.

### Lines 351–352

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 353–354

Defines `_tokens` and its implementation control flow; direct static calls: findall, lower, set.

### Lines 355–356

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 357–364

Defines `_evaluation_phase` and its implementation control flow; direct static calls: none resolved.

### Lines 365–366

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 367–376

Defines `_failure_taxonomy` and its implementation control flow; direct static calls: Counter, dict, items, sorted.

### Lines 377–378

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 379–398

Defines `_group_performance` and its implementation control flow; direct static calls: append, defaultdict, items, len, sorted, str, sum.

### Lines 399–400

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 401–409

Defines `_clarification_accuracy` and its implementation control flow; direct static calls: len, sum.

### Lines 410–411

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 412–417

Defines `_unnecessary_clarification_rate` and its implementation control flow; direct static calls: len, sum.

### Lines 418–419

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 420–425

Defines `_incorrect_autonomous_assumption_rate` and its implementation control flow; direct static calls: len, sum.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
