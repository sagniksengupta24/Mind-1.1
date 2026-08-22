# `scripts/build_semantic_v3_assets.py`

## File purpose

This automation and release file is reviewed at snapshot `8d86122c86972b40ea7e929fbd142fbbbb1e17d1c83e857126dc80451a7c0716`. It contains 390 lines.

## Imports and module state

- [scripts/build_semantic_v3_assets.py:1](../../../../scripts/build_semantic_v3_assets.py#L1) imports `__future__` / annotations.
- [scripts/build_semantic_v3_assets.py:3](../../../../scripts/build_semantic_v3_assets.py#L3) imports `hashlib`.
- [scripts/build_semantic_v3_assets.py:4](../../../../scripts/build_semantic_v3_assets.py#L4) imports `json`.
- [scripts/build_semantic_v3_assets.py:5](../../../../scripts/build_semantic_v3_assets.py#L5) imports `re`.
- [scripts/build_semantic_v3_assets.py:6](../../../../scripts/build_semantic_v3_assets.py#L6) imports `copy` / deepcopy.
- [scripts/build_semantic_v3_assets.py:7](../../../../scripts/build_semantic_v3_assets.py#L7) imports `datetime` / datetime.
- [scripts/build_semantic_v3_assets.py:7](../../../../scripts/build_semantic_v3_assets.py#L7) imports `datetime` / timezone.
- [scripts/build_semantic_v3_assets.py:8](../../../../scripts/build_semantic_v3_assets.py#L8) imports `pathlib` / Path.
- [scripts/build_semantic_v3_assets.py:9](../../../../scripts/build_semantic_v3_assets.py#L9) imports `typing` / Any.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / LABEL_FIELDS.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / REASON_CODES.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / SPECIALISTS.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / TASK_CLASSES.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / TOOL_FAMILIES.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / TOOL_FAMILIES_BY_TOOL.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / TOOLS.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / annotation_schema.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / derive_policy_constraints.
- [scripts/build_semantic_v3_assets.py:11](../../../../scripts/build_semantic_v3_assets.py#L11) imports `mind01.annotation_v3` / validate_annotation.

## Symbols

### `scripts.build_semantic_v3_assets.ROOT` — lines 25–25

- Source: [scripts/build_semantic_v3_assets.py:25](../../../../scripts/build_semantic_v3_assets.py#L25)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.V2` — lines 26–26

- Source: [scripts/build_semantic_v3_assets.py:26](../../../../scripts/build_semantic_v3_assets.py#L26)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.V3` — lines 27–27

- Source: [scripts/build_semantic_v3_assets.py:27](../../../../scripts/build_semantic_v3_assets.py#L27)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.PARTITIONS` — lines 28–35

- Source: [scripts/build_semantic_v3_assets.py:28](../../../../scripts/build_semantic_v3_assets.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.main` — lines 38–94

- Source: [scripts/build_semantic_v3_assets.py:38](../../../../scripts/build_semantic_v3_assets.py#L38)
- Type: function
- Signature: `n/a`
- Direct static callees: `RuntimeError`, `_annotation_contract`, `_build_execution_cases`, `_calibration_cases`, `_dataset_schema`, `_migrate_case`, `_scoring_contract`, `_validate_cases`, `any`, `dumps`, `exists`, `extend`, `isoformat`, `items`, `iterdir`, `len`, `load`, `mkdir`, `now`, `print`, `str`, `write`, `zip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._migrate_case` — lines 97–109

- Source: [scripts/build_semantic_v3_assets.py:97](../../../../scripts/build_semantic_v3_assets.py#L97)
- Type: function
- Signature: `source: dict[str, Any], partition: str`
- Direct static callees: `_allowed_immediate_families`, `_public_facts`, `deepcopy`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._public_facts` — lines 112–165

- Source: [scripts/build_semantic_v3_assets.py:112](../../../../scripts/build_semantic_v3_assets.py#L112)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `any`, `casefold`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._allowed_immediate_families` — lines 168–175

- Source: [scripts/build_semantic_v3_assets.py:168](../../../../scripts/build_semantic_v3_assets.py#L168)
- Type: function
- Signature: `expected: dict[str, Any]`
- Direct static callees: `get`, `set`, `sorted`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._build_execution_cases` — lines 178–211

- Source: [scripts/build_semantic_v3_assets.py:178](../../../../scripts/build_semantic_v3_assets.py#L178)
- Type: function
- Signature: `n/a`
- Direct static callees: `_allowed_immediate_families`, `_execution_prompt`, `_public_facts`, `append`, `deepcopy`, `load`, `mkdir`, `range`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._execution_prompt` — lines 214–223

- Source: [scripts/build_semantic_v3_assets.py:214](../../../../scripts/build_semantic_v3_assets.py#L214)
- Type: function
- Signature: `archetype: int, index: int`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._calibration_cases` — lines 226–255

- Source: [scripts/build_semantic_v3_assets.py:226](../../../../scripts/build_semantic_v3_assets.py#L226)
- Type: function
- Signature: `migrated: dict[str, list[dict[str, Any]]]`
- Direct static callees: `_curated_calibration_cases`, `add`, `all`, `append`, `deepcopy`, `enumerate`, `extend`, `get`, `items`, `len`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._curated_calibration_cases` — lines 258–315

- Source: [scripts/build_semantic_v3_assets.py:258](../../../../scripts/build_semantic_v3_assets.py#L258)
- Type: function
- Signature: `migrated: dict[str, list[dict[str, Any]]]`
- Direct static callees: `RuntimeError`, `bool`, `deepcopy`, `len`, `list`, `next`, `pick`, `predicate`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._validate_cases` — lines 318–323

- Source: [scripts/build_semantic_v3_assets.py:318](../../../../scripts/build_semantic_v3_assets.py#L318)
- Type: function
- Signature: `cases: list[dict[str, Any]]`
- Direct static callees: `RuntimeError`, `derive_policy_constraints`, `validate_annotation`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._dataset_schema` — lines 326–338

- Source: [scripts/build_semantic_v3_assets.py:326](../../../../scripts/build_semantic_v3_assets.py#L326)
- Type: function
- Signature: `n/a`
- Direct static callees: `annotation_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._annotation_contract` — lines 341–359

- Source: [scripts/build_semantic_v3_assets.py:341](../../../../scripts/build_semantic_v3_assets.py#L341)
- Type: function
- Signature: `n/a`
- Direct static callees: `annotation_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets._scoring_contract` — lines 362–376

- Source: [scripts/build_semantic_v3_assets.py:362](../../../../scripts/build_semantic_v3_assets.py#L362)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.load` — lines 379–380

- Source: [scripts/build_semantic_v3_assets.py:379](../../../../scripts/build_semantic_v3_assets.py#L379)
- Type: function
- Signature: `path: Path`
- Direct static callees: `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_semantic_v3_assets.write` — lines 383–386

- Source: [scripts/build_semantic_v3_assets.py:383](../../../../scripts/build_semantic_v3_assets.py#L383)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`, `write_bytes`
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

### Lines 11–22

Imports a dependency used by this module.

### Lines 23–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–25

Implements module-level `Assign` behavior or data.

### Lines 26–26

Implements module-level `Assign` behavior or data.

### Lines 27–27

Implements module-level `Assign` behavior or data.

### Lines 28–35

Implements module-level `Assign` behavior or data.

### Lines 36–37

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 38–67

Defines `main` and its implementation control flow; direct static calls: RuntimeError, _annotation_contract, _build_execution_cases, _calibration_cases, _dataset_schema, _migrate_case, _scoring_contract, _validate_cases, any, dumps, exists, extend, isoformat, items, iterdir, len, load, mkdir, now, print, str, write, zip.

### Lines 68–94

Defines `main` and its implementation control flow; direct static calls: RuntimeError, _annotation_contract, _build_execution_cases, _calibration_cases, _dataset_schema, _migrate_case, _scoring_contract, _validate_cases, any, dumps, exists, extend, isoformat, items, iterdir, len, load, mkdir, now, print, str, write, zip.

### Lines 95–96

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 97–109

Defines `_migrate_case` and its implementation control flow; direct static calls: _allowed_immediate_families, _public_facts, deepcopy.

### Lines 110–111

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 112–141

Defines `_public_facts` and its implementation control flow; direct static calls: any, casefold.

### Lines 142–165

Defines `_public_facts` and its implementation control flow; direct static calls: any, casefold.

### Lines 166–167

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 168–175

Defines `_allowed_immediate_families` and its implementation control flow; direct static calls: get, set, sorted, update.

### Lines 176–177

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 178–207

Defines `_build_execution_cases` and its implementation control flow; direct static calls: _allowed_immediate_families, _execution_prompt, _public_facts, append, deepcopy, load, mkdir, range, write_text.

### Lines 208–211

Defines `_build_execution_cases` and its implementation control flow; direct static calls: _allowed_immediate_families, _execution_prompt, _public_facts, append, deepcopy, load, mkdir, range, write_text.

### Lines 212–213

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 214–223

Defines `_execution_prompt` and its implementation control flow; direct static calls: none resolved.

### Lines 224–225

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 226–255

Defines `_calibration_cases` and its implementation control flow; direct static calls: _curated_calibration_cases, add, all, append, deepcopy, enumerate, extend, get, items, len, set, sorted.

### Lines 256–257

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 258–287

Defines `_curated_calibration_cases` and its implementation control flow; direct static calls: RuntimeError, bool, deepcopy, len, list, next, pick, predicate, values.

### Lines 288–315

Defines `_curated_calibration_cases` and its implementation control flow; direct static calls: RuntimeError, bool, deepcopy, len, list, next, pick, predicate, values.

### Lines 316–317

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 318–323

Defines `_validate_cases` and its implementation control flow; direct static calls: RuntimeError, derive_policy_constraints, validate_annotation.

### Lines 324–325

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 326–338

Defines `_dataset_schema` and its implementation control flow; direct static calls: annotation_schema.

### Lines 339–340

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 341–359

Defines `_annotation_contract` and its implementation control flow; direct static calls: annotation_schema.

### Lines 360–361

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 362–376

Defines `_scoring_contract` and its implementation control flow; direct static calls: none resolved.

### Lines 377–378

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 379–380

Defines `load` and its implementation control flow; direct static calls: loads, read_text.

### Lines 381–382

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 383–386

Defines `write` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256, write_bytes.

### Lines 387–388

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 389–390

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
