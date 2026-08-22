# `tests/test_rc3_1_pipeline.py`

## File purpose

This testing file is reviewed at snapshot `aa2ed26bd5dd61e4a38ed4fcbf78d3319e6ef992789e4355109676abdda53308`. It contains 207 lines.

## Imports and module state

- [tests/test_rc3_1_pipeline.py:1](../../../../tests/test_rc3_1_pipeline.py#L1) imports `__future__` / annotations.
- [tests/test_rc3_1_pipeline.py:3](../../../../tests/test_rc3_1_pipeline.py#L3) imports `json`.
- [tests/test_rc3_1_pipeline.py:4](../../../../tests/test_rc3_1_pipeline.py#L4) imports `io`.
- [tests/test_rc3_1_pipeline.py:5](../../../../tests/test_rc3_1_pipeline.py#L5) imports `sys`.
- [tests/test_rc3_1_pipeline.py:6](../../../../tests/test_rc3_1_pipeline.py#L6) imports `tarfile`.
- [tests/test_rc3_1_pipeline.py:7](../../../../tests/test_rc3_1_pipeline.py#L7) imports `zipfile`.
- [tests/test_rc3_1_pipeline.py:8](../../../../tests/test_rc3_1_pipeline.py#L8) imports `pathlib` / Path.
- [tests/test_rc3_1_pipeline.py:10](../../../../tests/test_rc3_1_pipeline.py#L10) imports `pytest`.
- [tests/test_rc3_1_pipeline.py:15](../../../../tests/test_rc3_1_pipeline.py#L15) imports `rc3_1_pipeline`.

## Symbols

### `tests.test_rc3_1_pipeline.SCRIPTS` — lines 13–13

- Source: [tests/test_rc3_1_pipeline.py:13](../../../../tests/test_rc3_1_pipeline.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.minimal_policy` — lines 18–28

- Source: [tests/test_rc3_1_pipeline.py:18](../../../../tests/test_rc3_1_pipeline.py#L18)
- Type: function
- Signature: `*, missing_family: bool=False`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.synthetic_pool` — lines 31–65

- Source: [tests/test_rc3_1_pipeline.py:31](../../../../tests/test_rc3_1_pipeline.py#L31)
- Type: function
- Signature: `count: int=125`
- Direct static callees: `append`, `range`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_exactly_120_preselected_with_one_rejection_cannot_produce_120` — lines 68–71

- Source: [tests/test_rc3_1_pipeline.py:68](../../../../tests/test_rc3_1_pipeline.py#L68)
- Type: function
- Signature: `n/a`
- Direct static callees: `coverage_selection`, `minimal_policy`, `raises`, `synthetic_pool`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_sufficient_accepted_reserve_produces_120` — lines 74–78

- Source: [tests/test_rc3_1_pipeline.py:74](../../../../tests/test_rc3_1_pipeline.py#L74)
- Type: function
- Signature: `n/a`
- Direct static callees: `coverage_selection`, `len`, `minimal_policy`, `synthetic_pool`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_rejected_cases_are_never_eligible` — lines 81–83

- Source: [tests/test_rc3_1_pipeline.py:81](../../../../tests/test_rc3_1_pipeline.py#L81)
- Type: function
- Signature: `n/a`
- Direct static callees: `eligible_case_ids`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_unresolved_cases_are_never_eligible` — lines 86–88

- Source: [tests/test_rc3_1_pipeline.py:86](../../../../tests/test_rc3_1_pipeline.py#L86)
- Type: function
- Signature: `n/a`
- Direct static callees: `eligible_case_ids`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_selection_is_deterministic` — lines 91–95

- Source: [tests/test_rc3_1_pipeline.py:91](../../../../tests/test_rc3_1_pipeline.py#L91)
- Type: function
- Signature: `n/a`
- Direct static callees: `coverage_selection`, `list`, `minimal_policy`, `reversed`, `synthetic_pool`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_coverage_constraints_are_enforced` — lines 98–101

- Source: [tests/test_rc3_1_pipeline.py:98](../../../../tests/test_rc3_1_pipeline.py#L98)
- Type: function
- Signature: `n/a`
- Direct static callees: `coverage_selection`, `minimal_policy`, `raises`, `synthetic_pool`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_changing_selection_policy_changes_identity_hash` — lines 104–109

- Source: [tests/test_rc3_1_pipeline.py:104](../../../../tests/test_rc3_1_pipeline.py#L104)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `sha256`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_changing_one_input_changes_set_hash` — lines 112–117

- Source: [tests/test_rc3_1_pipeline.py:112](../../../../tests/test_rc3_1_pipeline.py#L112)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `sha256`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_old_superseded_set_is_not_current` — lines 120–123

- Source: [tests/test_rc3_1_pipeline.py:120](../../../../tests/test_rc3_1_pipeline.py#L120)
- Type: function
- Signature: `n/a`
- Direct static callees: `load_json`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_untracked_evaluation_scripts_block_sealing` — lines 126–129

- Source: [tests/test_rc3_1_pipeline.py:126](../../../../tests/test_rc3_1_pipeline.py#L126)
- Type: function
- Signature: `monkeypatch: pytest.MonkeyPatch`
- Direct static callees: `raises`, `script_manifest`, `setattr`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_evaluator_source_drift_blocks_freeze` — lines 132–140

- Source: [tests/test_rc3_1_pipeline.py:132](../../../../tests/test_rc3_1_pipeline.py#L132)
- Type: function
- Signature: `monkeypatch: pytest.MonkeyPatch`
- Direct static callees: `endswith`, `original`, `raises`, `setattr`, `str`, `verify_freeze`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_runtime_source_drift_blocks_freeze` — lines 143–146

- Source: [tests/test_rc3_1_pipeline.py:143](../../../../tests/test_rc3_1_pipeline.py#L143)
- Type: function
- Signature: `monkeypatch: pytest.MonkeyPatch`
- Direct static callees: `raises`, `setattr`, `verify_freeze`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_contamination_in_artifact_is_blocking` — lines 149–156

- Source: [tests/test_rc3_1_pipeline.py:149](../../../../tests/test_rc3_1_pipeline.py#L149)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `ZipFile`, `hexdigest`, `scan_artifact`, `sha256`, `writestr`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_private_labels_absent_from_runtime_artifact` — lines 159–165

- Source: [tests/test_rc3_1_pipeline.py:159](../../../../tests/test_rc3_1_pipeline.py#L159)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `ZipFile`, `hexdigest`, `scan_artifact`, `sha256`, `writestr`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_private_labels_in_sdist_are_blocking` — lines 168–179

- Source: [tests/test_rc3_1_pipeline.py:168](../../../../tests/test_rc3_1_pipeline.py#L168)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `BytesIO`, `TarInfo`, `addfile`, `hexdigest`, `len`, `open`, `scan_artifact`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_existing_sealed_artifact_cannot_be_overwritten` — lines 182–187

- Source: [tests/test_rc3_1_pipeline.py:182](../../../../tests/test_rc3_1_pipeline.py#L182)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `ensure_new_directory`, `mkdir`, `raises`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_fewer_than_120_accepted_candidates_produces_hold` — lines 190–193

- Source: [tests/test_rc3_1_pipeline.py:190](../../../../tests/test_rc3_1_pipeline.py#L190)
- Type: function
- Signature: `n/a`
- Direct static callees: `coverage_selection`, `minimal_policy`, `raises`, `synthetic_pool`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_write_json_refuses_existing_identity` — lines 196–200

- Source: [tests/test_rc3_1_pipeline.py:196](../../../../tests/test_rc3_1_pipeline.py#L196)
- Type: function
- Signature: `tmp_path: Path`
- Direct static callees: `raises`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_rc3_1_pipeline.test_public_projection_excludes_authoring_and_labels` — lines 203–207

- Source: [tests/test_rc3_1_pipeline.py:203](../../../../tests/test_rc3_1_pipeline.py#L203)
- Type: function
- Signature: `n/a`
- Direct static callees: `public_input`, `synthetic_pool`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–14

Implements module-level `Expr` behavior or data.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–28

Defines `minimal_policy` and its implementation control flow; direct static calls: none resolved.

### Lines 29–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–60

Defines `synthetic_pool` and its implementation control flow; direct static calls: append, range.

### Lines 61–65

Defines `synthetic_pool` and its implementation control flow; direct static calls: append, range.

### Lines 66–67

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 68–71

Defines `test_exactly_120_preselected_with_one_rejection_cannot_produce_120` and its implementation control flow; direct static calls: coverage_selection, minimal_policy, raises, synthetic_pool.

### Lines 72–73

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 74–78

Defines `test_sufficient_accepted_reserve_produces_120` and its implementation control flow; direct static calls: coverage_selection, len, minimal_policy, synthetic_pool.

### Lines 79–80

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 81–83

Defines `test_rejected_cases_are_never_eligible` and its implementation control flow; direct static calls: eligible_case_ids.

### Lines 84–85

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 86–88

Defines `test_unresolved_cases_are_never_eligible` and its implementation control flow; direct static calls: eligible_case_ids.

### Lines 89–90

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 91–95

Defines `test_selection_is_deterministic` and its implementation control flow; direct static calls: coverage_selection, list, minimal_policy, reversed, synthetic_pool.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–101

Defines `test_coverage_constraints_are_enforced` and its implementation control flow; direct static calls: coverage_selection, minimal_policy, raises, synthetic_pool.

### Lines 102–103

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 104–109

Defines `test_changing_selection_policy_changes_identity_hash` and its implementation control flow; direct static calls: sha256, write_text.

### Lines 110–111

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 112–117

Defines `test_changing_one_input_changes_set_hash` and its implementation control flow; direct static calls: sha256, write_text.

### Lines 118–119

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 120–123

Defines `test_old_superseded_set_is_not_current` and its implementation control flow; direct static calls: load_json, startswith.

### Lines 124–125

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 126–129

Defines `test_untracked_evaluation_scripts_block_sealing` and its implementation control flow; direct static calls: raises, script_manifest, setattr.

### Lines 130–131

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 132–140

Defines `test_evaluator_source_drift_blocks_freeze` and its implementation control flow; direct static calls: endswith, original, raises, setattr, str, verify_freeze.

### Lines 141–142

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 143–146

Defines `test_runtime_source_drift_blocks_freeze` and its implementation control flow; direct static calls: raises, setattr, verify_freeze.

### Lines 147–148

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 149–156

Defines `test_contamination_in_artifact_is_blocking` and its implementation control flow; direct static calls: ZipFile, hexdigest, scan_artifact, sha256, writestr.

### Lines 157–158

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 159–165

Defines `test_private_labels_absent_from_runtime_artifact` and its implementation control flow; direct static calls: ZipFile, hexdigest, scan_artifact, sha256, writestr.

### Lines 166–167

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 168–179

Defines `test_private_labels_in_sdist_are_blocking` and its implementation control flow; direct static calls: BytesIO, TarInfo, addfile, hexdigest, len, open, scan_artifact, sha256.

### Lines 180–181

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 182–187

Defines `test_existing_sealed_artifact_cannot_be_overwritten` and its implementation control flow; direct static calls: ensure_new_directory, mkdir, raises, write_text.

### Lines 188–189

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 190–193

Defines `test_fewer_than_120_accepted_candidates_produces_hold` and its implementation control flow; direct static calls: coverage_selection, minimal_policy, raises, synthetic_pool.

### Lines 194–195

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 196–200

Defines `test_write_json_refuses_existing_identity` and its implementation control flow; direct static calls: raises, write_json.

### Lines 201–202

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 203–207

Defines `test_public_projection_excludes_authoring_and_labels` and its implementation control flow; direct static calls: public_input, synthetic_pool.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
