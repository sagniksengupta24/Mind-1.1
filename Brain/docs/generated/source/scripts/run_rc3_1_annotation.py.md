# `scripts/run_rc3_1_annotation.py`

## File purpose

This automation and release file is reviewed at snapshot `46372418c9187743cac417819587d0ff468d52d750f49da4fac646680e49e8b0`. It contains 166 lines.

## Imports and module state

- [scripts/run_rc3_1_annotation.py:3](../../../../scripts/run_rc3_1_annotation.py#L3) imports `__future__` / annotations.
- [scripts/run_rc3_1_annotation.py:5](../../../../scripts/run_rc3_1_annotation.py#L5) imports `argparse`.
- [scripts/run_rc3_1_annotation.py:6](../../../../scripts/run_rc3_1_annotation.py#L6) imports `json`.
- [scripts/run_rc3_1_annotation.py:7](../../../../scripts/run_rc3_1_annotation.py#L7) imports `time`.
- [scripts/run_rc3_1_annotation.py:8](../../../../scripts/run_rc3_1_annotation.py#L8) imports `pathlib` / Path.
- [scripts/run_rc3_1_annotation.py:9](../../../../scripts/run_rc3_1_annotation.py#L9) imports `typing` / Any.
- [scripts/run_rc3_1_annotation.py:11](../../../../scripts/run_rc3_1_annotation.py#L11) imports `mind01.annotation_v3` / annotation_agreement.
- [scripts/run_rc3_1_annotation.py:11](../../../../scripts/run_rc3_1_annotation.py#L11) imports `mind01.annotation_v3` / derive_policy_constraints.
- [scripts/run_rc3_1_annotation.py:11](../../../../scripts/run_rc3_1_annotation.py#L11) imports `mind01.annotation_v3` / semantic_label_projection.
- [scripts/run_rc3_1_annotation.py:11](../../../../scripts/run_rc3_1_annotation.py#L11) imports `mind01.annotation_v3` / validate_annotation.
- [scripts/run_rc3_1_annotation.py:17](../../../../scripts/run_rc3_1_annotation.py#L17) imports `run_semantic_v3_annotation` / MODEL_DIGEST.
- [scripts/run_rc3_1_annotation.py:17](../../../../scripts/run_rc3_1_annotation.py#L17) imports `run_semantic_v3_annotation` / _report.
- [scripts/run_rc3_1_annotation.py:17](../../../../scripts/run_rc3_1_annotation.py#L17) imports `run_semantic_v3_annotation` / adjudicate.
- [scripts/run_rc3_1_annotation.py:17](../../../../scripts/run_rc3_1_annotation.py#L17) imports `run_semantic_v3_annotation` / annotate.
- [scripts/run_rc3_1_annotation.py:17](../../../../scripts/run_rc3_1_annotation.py#L17) imports `run_semantic_v3_annotation` / model_identity.

## Symbols

### `scripts.run_rc3_1_annotation.main` — lines 26–37

- Source: [scripts/run_rc3_1_annotation.py:26](../../../../scripts/run_rc3_1_annotation.py#L26)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `dumps`, `parse_args`, `print`, `resolve`, `run`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.run` — lines 40–87

- Source: [scripts/run_rc3_1_annotation.py:40](../../../../scripts/run_rc3_1_annotation.py#L40)
- Type: function
- Signature: `source: Path, output: Path, timeout: int, resume: bool`
- Direct static callees: `FileExistsError`, `RuntimeError`, `_report`, `annotate_case`, `any`, `enumerate`, `exists`, `get`, `iterdir`, `len`, `load`, `load_state`, `loads`, `mkdir`, `model_identity`, `monotonic`, `read_text`, `resolve`, `write_atomic`, `write_new`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.annotate_case` — lines 90–123

- Source: [scripts/run_rc3_1_annotation.py:90](../../../../scripts/run_rc3_1_annotation.py#L90)
- Type: function
- Signature: `case: dict[str, Any], index: int, timeout: int`
- Direct static callees: `adjudicate`, `annotate`, `annotation_agreement`, `derive_policy_constraints`, `digest_json`, `isinstance`, `semantic_label_projection`, `to_dict`, `validate_annotation`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.load_state` — lines 126–138

- Source: [scripts/run_rc3_1_annotation.py:126](../../../../scripts/run_rc3_1_annotation.py#L126)
- Type: function
- Signature: `cases: list[dict[str, Any]], records_dir: Path, labels_dir: Path`
- Direct static callees: `append`, `enumerate`, `exists`, `load`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.digest_json` — lines 141–143

- Source: [scripts/run_rc3_1_annotation.py:141](../../../../scripts/run_rc3_1_annotation.py#L141)
- Type: function
- Signature: `value: Any`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.load` — lines 146–150

- Source: [scripts/run_rc3_1_annotation.py:146](../../../../scripts/run_rc3_1_annotation.py#L146)
- Type: function
- Signature: `path: Path`
- Direct static callees: `RuntimeError`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.write_new` — lines 153–156

- Source: [scripts/run_rc3_1_annotation.py:153](../../../../scripts/run_rc3_1_annotation.py#L153)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `FileExistsError`, `exists`, `write_atomic`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_annotation.write_atomic` — lines 159–162

- Source: [scripts/run_rc3_1_annotation.py:159](../../../../scripts/run_rc3_1_annotation.py#L159)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `dumps`, `replace`, `with_suffix`, `write_text`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–16

Imports a dependency used by this module.

### Lines 17–23

Imports a dependency used by this module.

### Lines 24–25

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 26–37

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, dumps, parse_args, print, resolve, run, str.

### Lines 38–39

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 40–69

Defines `run` and its implementation control flow; direct static calls: FileExistsError, RuntimeError, _report, annotate_case, any, enumerate, exists, get, iterdir, len, load, load_state, loads, mkdir, model_identity, monotonic, read_text, resolve, write_atomic, write_new.

### Lines 70–87

Defines `run` and its implementation control flow; direct static calls: FileExistsError, RuntimeError, _report, annotate_case, any, enumerate, exists, get, iterdir, len, load, load_state, loads, mkdir, model_identity, monotonic, read_text, resolve, write_atomic, write_new.

### Lines 88–89

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 90–119

Defines `annotate_case` and its implementation control flow; direct static calls: adjudicate, annotate, annotation_agreement, derive_policy_constraints, digest_json, isinstance, semantic_label_projection, to_dict, validate_annotation.

### Lines 120–123

Defines `annotate_case` and its implementation control flow; direct static calls: adjudicate, annotate, annotation_agreement, derive_policy_constraints, digest_json, isinstance, semantic_label_projection, to_dict, validate_annotation.

### Lines 124–125

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 126–138

Defines `load_state` and its implementation control flow; direct static calls: append, enumerate, exists, load.

### Lines 139–140

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 141–143

Defines `digest_json` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 144–145

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 146–150

Defines `load` and its implementation control flow; direct static calls: RuntimeError, isinstance, loads, read_text.

### Lines 151–152

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 153–156

Defines `write_new` and its implementation control flow; direct static calls: FileExistsError, exists, write_atomic.

### Lines 157–158

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 159–162

Defines `write_atomic` and its implementation control flow; direct static calls: dumps, replace, with_suffix, write_text.

### Lines 163–164

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 165–166

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
