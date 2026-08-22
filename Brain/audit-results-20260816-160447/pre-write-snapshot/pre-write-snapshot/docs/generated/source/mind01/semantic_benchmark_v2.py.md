# `mind01/semantic_benchmark_v2.py`

## File purpose

This agent runtime file is reviewed at snapshot `8ae9725f3faa247aca063c5a10009f4380da92e31eaf6b04028f5edee2df6051`. It contains 687 lines.

## Imports and module state

- [mind01/semantic_benchmark_v2.py:3](../../../../mind01/semantic_benchmark_v2.py#L3) imports `__future__` / annotations.
- [mind01/semantic_benchmark_v2.py:5](../../../../mind01/semantic_benchmark_v2.py#L5) imports `hashlib`.
- [mind01/semantic_benchmark_v2.py:6](../../../../mind01/semantic_benchmark_v2.py#L6) imports `json`.
- [mind01/semantic_benchmark_v2.py:7](../../../../mind01/semantic_benchmark_v2.py#L7) imports `math`.
- [mind01/semantic_benchmark_v2.py:8](../../../../mind01/semantic_benchmark_v2.py#L8) imports `random`.
- [mind01/semantic_benchmark_v2.py:9](../../../../mind01/semantic_benchmark_v2.py#L9) imports `re`.
- [mind01/semantic_benchmark_v2.py:10](../../../../mind01/semantic_benchmark_v2.py#L10) imports `statistics`.
- [mind01/semantic_benchmark_v2.py:11](../../../../mind01/semantic_benchmark_v2.py#L11) imports `time`.
- [mind01/semantic_benchmark_v2.py:12](../../../../mind01/semantic_benchmark_v2.py#L12) imports `collections` / Counter.
- [mind01/semantic_benchmark_v2.py:12](../../../../mind01/semantic_benchmark_v2.py#L12) imports `collections` / defaultdict.
- [mind01/semantic_benchmark_v2.py:13](../../../../mind01/semantic_benchmark_v2.py#L13) imports `pathlib` / Path.
- [mind01/semantic_benchmark_v2.py:14](../../../../mind01/semantic_benchmark_v2.py#L14) imports `typing` / Any.
- [mind01/semantic_benchmark_v2.py:14](../../../../mind01/semantic_benchmark_v2.py#L14) imports `typing` / Iterable.
- [mind01/semantic_benchmark_v2.py:14](../../../../mind01/semantic_benchmark_v2.py#L14) imports `typing` / Mapping.
- [mind01/semantic_benchmark_v2.py:16](../../../../mind01/semantic_benchmark_v2.py#L16) imports `intent` / ExpectedOutputMode.
- [mind01/semantic_benchmark_v2.py:17](../../../../mind01/semantic_benchmark_v2.py#L17) imports `llm` / OllamaClient.
- [mind01/semantic_benchmark_v2.py:18](../../../../mind01/semantic_benchmark_v2.py#L18) imports `routing` / HierarchicalRouter.
- [mind01/semantic_benchmark_v2.py:18](../../../../mind01/semantic_benchmark_v2.py#L18) imports `routing` / ToolFamily.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / FAMILY_LIFECYCLE.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / FAMILY_TOOLS.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / LIVE_WRITE_TOOLS.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / OllamaSemanticClassifier.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / RuleBasedSemanticClassifier.
- [mind01/semantic_benchmark_v2.py:19](../../../../mind01/semantic_benchmark_v2.py#L19) imports `semantic_router_v2` / SemanticRouterV2.
- [mind01/semantic_benchmark_v2.py:27](../../../../mind01/semantic_benchmark_v2.py#L27) imports `version` / __version__.

## Symbols

### `mind01.semantic_benchmark_v2.ROOT` — lines 30–30

- Source: [mind01/semantic_benchmark_v2.py:30](../../../../mind01/semantic_benchmark_v2.py#L30)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.SUITE` — lines 31–31

- Source: [mind01/semantic_benchmark_v2.py:31](../../../../mind01/semantic_benchmark_v2.py#L31)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.MANIFEST` — lines 32–32

- Source: [mind01/semantic_benchmark_v2.py:32](../../../../mind01/semantic_benchmark_v2.py#L32)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.HOLDOUT_ACCESS` — lines 33–33

- Source: [mind01/semantic_benchmark_v2.py:33](../../../../mind01/semantic_benchmark_v2.py#L33)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.SPLITS` — lines 34–34

- Source: [mind01/semantic_benchmark_v2.py:34](../../../../mind01/semantic_benchmark_v2.py#L34)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.SCORED_FIELDS` — lines 35–45

- Source: [mind01/semantic_benchmark_v2.py:35](../../../../mind01/semantic_benchmark_v2.py#L35)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.FORBIDDEN_MARKERS` — lines 46–53

- Source: [mind01/semantic_benchmark_v2.py:46](../../../../mind01/semantic_benchmark_v2.py#L46)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.DEVELOPMENT_GATES` — lines 54–71

- Source: [mind01/semantic_benchmark_v2.py:54](../../../../mind01/semantic_benchmark_v2.py#L54)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.HOLDOUT_GATES` — lines 72–82

- Source: [mind01/semantic_benchmark_v2.py:72](../../../../mind01/semantic_benchmark_v2.py#L72)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.SemanticBenchmarkError` — lines 85–86

- Source: [mind01/semantic_benchmark_v2.py:85](../../../../mind01/semantic_benchmark_v2.py#L85)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.safe_suite_path` — lines 89–95

- Source: [mind01/semantic_benchmark_v2.py:89](../../../../mind01/semantic_benchmark_v2.py#L89)
- Type: function
- Signature: `filename: str`
- Direct static callees: `SemanticBenchmarkError`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.sha256_file` — lines 98–99

- Source: [mind01/semantic_benchmark_v2.py:98](../../../../mind01/semantic_benchmark_v2.py#L98)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.load_manifest` — lines 102–106

- Source: [mind01/semantic_benchmark_v2.py:102](../../../../mind01/semantic_benchmark_v2.py#L102)
- Type: function
- Signature: `n/a`
- Direct static callees: `SemanticBenchmarkError`, `get`, `loads`, `read_text`, `safe_suite_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.load_split` — lines 109–126

- Source: [mind01/semantic_benchmark_v2.py:109](../../../../mind01/semantic_benchmark_v2.py#L109)
- Type: function
- Signature: `split: str, *, open_holdout: bool=False`
- Direct static callees: `SemanticBenchmarkError`, `get`, `isinstance`, `loads`, `read_text`, `safe_suite_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.validate_suite` — lines 129–221

- Source: [mind01/semantic_benchmark_v2.py:129](../../../../mind01/semantic_benchmark_v2.py#L129)
- Type: function
- Signature: `*, include_holdout: bool=False`
- Direct static callees: `Counter`, `SemanticBenchmarkError`, `add`, `any`, `append`, `canonical_hash`, `casefold`, `dict`, `dumps`, `get`, `items`, `join`, `len`, `load_manifest`, `load_split`, `pop`, `safe_suite_path`, `semantic_near_duplicates`, `set`, `sha256_file`, `sorted`, `split`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.semantic_near_duplicates` — lines 224–241

- Source: [mind01/semantic_benchmark_v2.py:224](../../../../mind01/semantic_benchmark_v2.py#L224)
- Type: function
- Signature: `cases: Iterable[Mapping[str, Any]], threshold: float=0.985`
- Direct static callees: `append`, `casefold`, `enumerate`, `findall`, `len`, `round`, `set`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.canonical_hash` — lines 244–246

- Source: [mind01/semantic_benchmark_v2.py:244](../../../../mind01/semantic_benchmark_v2.py#L244)
- Type: function
- Signature: `value: Any`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.run_case` — lines 249–322

- Source: [mind01/semantic_benchmark_v2.py:249](../../../../mind01/semantic_benchmark_v2.py#L249)
- Type: function
- Signature: `case: Mapping[str, Any], *, router_name: str, live: bool, model: str, ollama_url: str, timeout: int, seed: int, variant: str='full_v2'`
- Direct static callees: `OllamaClient`, `OllamaSemanticClassifier`, `RuleBasedSemanticClassifier`, `SemanticRouterV2`, `ablate_state`, `bool`, `dict`, `float`, `get`, `getattr`, `int`, `legacy_case`, `len`, `list`, `perf_counter`, `policy_overrode_model`, `project_actual`, `round`, `route_typed`, `set`, `str`, `to_dict`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.project_actual` — lines 325–347

- Source: [mind01/semantic_benchmark_v2.py:325](../../../../mind01/semantic_benchmark_v2.py#L325)
- Type: function
- Signature: `state: Mapping[str, Any]`
- Direct static callees: `get`, `isinstance`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.legacy_case` — lines 350–387

- Source: [mind01/semantic_benchmark_v2.py:350](../../../../mind01/semantic_benchmark_v2.py#L350)
- Type: function
- Signature: `case: Mapping[str, Any]`
- Direct static callees: `HierarchicalRouter`, `ToolFamily`, `append`, `bool`, `list`, `route_typed`, `sorted`, `str`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.ablate_state` — lines 390–412

- Source: [mind01/semantic_benchmark_v2.py:390](../../../../mind01/semantic_benchmark_v2.py#L390)
- Type: function
- Signature: `state: dict[str, Any], variant: str`
- Direct static callees: `SemanticBenchmarkError`, `ToolFamily`, `dumps`, `loads`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.score_results` — lines 415–525

- Source: [mind01/semantic_benchmark_v2.py:415](../../../../mind01/semantic_benchmark_v2.py#L415)
- Type: function
- Signature: `results: list[Mapping[str, Any]]`
- Direct static callees: `SemanticBenchmarkError`, `all`, `bool`, `confusion_matrix`, `float`, `fmean`, `get`, `grouped_accuracy`, `int`, `len`, `normalize_field`, `percentile`, `sorted`, `str`, `sum`, `unauthorized_mutation`, `unsafe_selection`, `valid_combination`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.grouped_accuracy` — lines 528–543

- Source: [mind01/semantic_benchmark_v2.py:528](../../../../mind01/semantic_benchmark_v2.py#L528)
- Type: function
- Signature: `results: Iterable[Mapping[str, Any]], field: str`
- Direct static callees: `Counter`, `get`, `items`, `normalize_field`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.confusion_matrix` — lines 546–557

- Source: [mind01/semantic_benchmark_v2.py:546](../../../../mind01/semantic_benchmark_v2.py#L546)
- Type: function
- Signature: `results: Iterable[Mapping[str, Any]], field: str`
- Direct static callees: `Counter`, `get`, `items`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.normalize_field` — lines 560–567

- Source: [mind01/semantic_benchmark_v2.py:560](../../../../mind01/semantic_benchmark_v2.py#L560)
- Type: function
- Signature: `field: str, value: Any`
- Direct static callees: `get`, `isinstance`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.valid_combination` — lines 570–590

- Source: [mind01/semantic_benchmark_v2.py:570](../../../../mind01/semantic_benchmark_v2.py#L570)
- Type: function
- Signature: `actual: Mapping[str, Any]`
- Direct static callees: `get`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.unsafe_selection` — lines 593–598

- Source: [mind01/semantic_benchmark_v2.py:593](../../../../mind01/semantic_benchmark_v2.py#L593)
- Type: function
- Signature: `item: Mapping[str, Any]`
- Direct static callees: `bool`, `get`, `int`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.policy_overrode_model` — lines 601–611

- Source: [mind01/semantic_benchmark_v2.py:601](../../../../mind01/semantic_benchmark_v2.py#L601)
- Type: function
- Signature: `state: Mapping[str, Any]`
- Direct static callees: `bool`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.legacy_v2_disagreements` — lines 614–635

- Source: [mind01/semantic_benchmark_v2.py:614](../../../../mind01/semantic_benchmark_v2.py#L614)
- Type: function
- Signature: `cases: list[Mapping[str, Any]], results: list[Mapping[str, Any]]`
- Direct static callees: `Counter`, `dict`, `get`, `items`, `legacy_case`, `normalize_field`, `project_actual`, `sorted`, `update`, `zip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.unauthorized_mutation` — lines 638–646

- Source: [mind01/semantic_benchmark_v2.py:638](../../../../mind01/semantic_benchmark_v2.py#L638)
- Type: function
- Signature: `item: Mapping[str, Any]`
- Direct static callees: `bool`, `get`, `int`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.percentile` — lines 649–653

- Source: [mind01/semantic_benchmark_v2.py:649](../../../../mind01/semantic_benchmark_v2.py#L649)
- Type: function
- Signature: `values: list[float], fraction: float`
- Direct static callees: `ceil`, `len`, `max`, `min`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.evaluate_gates` — lines 656–679

- Source: [mind01/semantic_benchmark_v2.py:656](../../../../mind01/semantic_benchmark_v2.py#L656)
- Type: function
- Signature: `metrics: Mapping[str, float], gates: Mapping[str, tuple[str, float]]`
- Direct static callees: `all`, `float`, `items`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_benchmark_v2.deterministic_order` — lines 682–687

- Source: [mind01/semantic_benchmark_v2.py:682](../../../../mind01/semantic_benchmark_v2.py#L682)
- Type: function
- Signature: `cases: list[dict[str, Any]], seed: int`
- Direct static callees: `Random`, `list`, `shuffle`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Implements module-level `Expr` behavior or data.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports, comments, declarations, or configuration that establish the following implementation context.

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

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–26

Imports a dependency used by this module.

### Lines 27–27

Imports a dependency used by this module.

### Lines 28–29

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 30–30

Implements module-level `Assign` behavior or data.

### Lines 31–31

Implements module-level `Assign` behavior or data.

### Lines 32–32

Implements module-level `Assign` behavior or data.

### Lines 33–33

Implements module-level `Assign` behavior or data.

### Lines 34–34

Implements module-level `Assign` behavior or data.

### Lines 35–45

Implements module-level `Assign` behavior or data.

### Lines 46–53

Implements module-level `Assign` behavior or data.

### Lines 54–71

Implements module-level `Assign` behavior or data.

### Lines 72–82

Implements module-level `Assign` behavior or data.

### Lines 83–84

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 85–86

Defines class `SemanticBenchmarkError` and the behavior of its members.

### Lines 87–88

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 89–95

Defines `safe_suite_path` and its implementation control flow; direct static calls: SemanticBenchmarkError, resolve.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–99

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

### Lines 100–101

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 102–106

Defines `load_manifest` and its implementation control flow; direct static calls: SemanticBenchmarkError, get, loads, read_text, safe_suite_path.

### Lines 107–108

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 109–126

Defines `load_split` and its implementation control flow; direct static calls: SemanticBenchmarkError, get, isinstance, loads, read_text, safe_suite_path.

### Lines 127–128

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 129–158

Defines `validate_suite` and its implementation control flow; direct static calls: Counter, SemanticBenchmarkError, add, any, append, canonical_hash, casefold, dict, dumps, get, items, join, len, load_manifest, load_split, pop, safe_suite_path, semantic_near_duplicates, set, sha256_file, sorted, split, str.

### Lines 159–188

Defines `validate_suite` and its implementation control flow; direct static calls: Counter, SemanticBenchmarkError, add, any, append, canonical_hash, casefold, dict, dumps, get, items, join, len, load_manifest, load_split, pop, safe_suite_path, semantic_near_duplicates, set, sha256_file, sorted, split, str.

### Lines 189–218

Defines `validate_suite` and its implementation control flow; direct static calls: Counter, SemanticBenchmarkError, add, any, append, canonical_hash, casefold, dict, dumps, get, items, join, len, load_manifest, load_split, pop, safe_suite_path, semantic_near_duplicates, set, sha256_file, sorted, split, str.

### Lines 219–221

Defines `validate_suite` and its implementation control flow; direct static calls: Counter, SemanticBenchmarkError, add, any, append, canonical_hash, casefold, dict, dumps, get, items, join, len, load_manifest, load_split, pop, safe_suite_path, semantic_near_duplicates, set, sha256_file, sorted, split, str.

### Lines 222–223

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 224–241

Defines `semantic_near_duplicates` and its implementation control flow; direct static calls: append, casefold, enumerate, findall, len, round, set, str.

### Lines 242–243

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 244–246

Defines `canonical_hash` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 247–248

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 249–278

Defines `run_case` and its implementation control flow; direct static calls: OllamaClient, OllamaSemanticClassifier, RuleBasedSemanticClassifier, SemanticRouterV2, ablate_state, bool, dict, float, get, getattr, int, legacy_case, len, list, perf_counter, policy_overrode_model, project_actual, round, route_typed, set, str, to_dict, type.

### Lines 279–308

Defines `run_case` and its implementation control flow; direct static calls: OllamaClient, OllamaSemanticClassifier, RuleBasedSemanticClassifier, SemanticRouterV2, ablate_state, bool, dict, float, get, getattr, int, legacy_case, len, list, perf_counter, policy_overrode_model, project_actual, round, route_typed, set, str, to_dict, type.

### Lines 309–322

Defines `run_case` and its implementation control flow; direct static calls: OllamaClient, OllamaSemanticClassifier, RuleBasedSemanticClassifier, SemanticRouterV2, ablate_state, bool, dict, float, get, getattr, int, legacy_case, len, list, perf_counter, policy_overrode_model, project_actual, round, route_typed, set, str, to_dict, type.

### Lines 323–324

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 325–347

Defines `project_actual` and its implementation control flow; direct static calls: get, isinstance, sorted.

### Lines 348–349

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 350–379

Defines `legacy_case` and its implementation control flow; direct static calls: HierarchicalRouter, ToolFamily, append, bool, list, route_typed, sorted, str, to_dict.

### Lines 380–387

Defines `legacy_case` and its implementation control flow; direct static calls: HierarchicalRouter, ToolFamily, append, bool, list, route_typed, sorted, str, to_dict.

### Lines 388–389

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 390–412

Defines `ablate_state` and its implementation control flow; direct static calls: SemanticBenchmarkError, ToolFamily, dumps, loads, sorted.

### Lines 413–414

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 415–444

Defines `score_results` and its implementation control flow; direct static calls: SemanticBenchmarkError, all, bool, confusion_matrix, float, fmean, get, grouped_accuracy, int, len, normalize_field, percentile, sorted, str, sum, unauthorized_mutation, unsafe_selection, valid_combination.

### Lines 445–474

Defines `score_results` and its implementation control flow; direct static calls: SemanticBenchmarkError, all, bool, confusion_matrix, float, fmean, get, grouped_accuracy, int, len, normalize_field, percentile, sorted, str, sum, unauthorized_mutation, unsafe_selection, valid_combination.

### Lines 475–504

Defines `score_results` and its implementation control flow; direct static calls: SemanticBenchmarkError, all, bool, confusion_matrix, float, fmean, get, grouped_accuracy, int, len, normalize_field, percentile, sorted, str, sum, unauthorized_mutation, unsafe_selection, valid_combination.

### Lines 505–525

Defines `score_results` and its implementation control flow; direct static calls: SemanticBenchmarkError, all, bool, confusion_matrix, float, fmean, get, grouped_accuracy, int, len, normalize_field, percentile, sorted, str, sum, unauthorized_mutation, unsafe_selection, valid_combination.

### Lines 526–527

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 528–543

Defines `grouped_accuracy` and its implementation control flow; direct static calls: Counter, get, items, normalize_field, sorted, str.

### Lines 544–545

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 546–557

Defines `confusion_matrix` and its implementation control flow; direct static calls: Counter, get, items, sorted, str.

### Lines 558–559

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 560–567

Defines `normalize_field` and its implementation control flow; direct static calls: get, isinstance, sorted, str, tuple.

### Lines 568–569

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 570–590

Defines `valid_combination` and its implementation control flow; direct static calls: get, set.

### Lines 591–592

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 593–598

Defines `unsafe_selection` and its implementation control flow; direct static calls: bool, get, int, set.

### Lines 599–600

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 601–611

Defines `policy_overrode_model` and its implementation control flow; direct static calls: bool, get.

### Lines 612–613

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 614–635

Defines `legacy_v2_disagreements` and its implementation control flow; direct static calls: Counter, dict, get, items, legacy_case, normalize_field, project_actual, sorted, update, zip.

### Lines 636–637

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 638–646

Defines `unauthorized_mutation` and its implementation control flow; direct static calls: bool, get, int, set.

### Lines 647–648

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 649–653

Defines `percentile` and its implementation control flow; direct static calls: ceil, len, max, min.

### Lines 654–655

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 656–679

Defines `evaluate_gates` and its implementation control flow; direct static calls: all, float, items, values.

### Lines 680–681

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 682–687

Defines `deterministic_order` and its implementation control flow; direct static calls: Random, list, shuffle.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
