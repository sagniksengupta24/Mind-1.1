# `scripts/rc3_1_pipeline.py`

## File purpose

This automation and release file is reviewed at snapshot `09a46725fcaaa10f16758d5d7e1cdaef497e251f37761c5834d531d128f108d6`. It contains 966 lines.

## Imports and module state

- [scripts/rc3_1_pipeline.py:1](../../../../scripts/rc3_1_pipeline.py#L1) imports `__future__` / annotations.
- [scripts/rc3_1_pipeline.py:3](../../../../scripts/rc3_1_pipeline.py#L3) imports `argparse`.
- [scripts/rc3_1_pipeline.py:4](../../../../scripts/rc3_1_pipeline.py#L4) imports `hashlib`.
- [scripts/rc3_1_pipeline.py:5](../../../../scripts/rc3_1_pipeline.py#L5) imports `json`.
- [scripts/rc3_1_pipeline.py:6](../../../../scripts/rc3_1_pipeline.py#L6) imports `os`.
- [scripts/rc3_1_pipeline.py:7](../../../../scripts/rc3_1_pipeline.py#L7) imports `shutil`.
- [scripts/rc3_1_pipeline.py:8](../../../../scripts/rc3_1_pipeline.py#L8) imports `stat`.
- [scripts/rc3_1_pipeline.py:9](../../../../scripts/rc3_1_pipeline.py#L9) imports `subprocess`.
- [scripts/rc3_1_pipeline.py:10](../../../../scripts/rc3_1_pipeline.py#L10) imports `tarfile`.
- [scripts/rc3_1_pipeline.py:11](../../../../scripts/rc3_1_pipeline.py#L11) imports `zipfile`.
- [scripts/rc3_1_pipeline.py:12](../../../../scripts/rc3_1_pipeline.py#L12) imports `collections` / Counter.
- [scripts/rc3_1_pipeline.py:12](../../../../scripts/rc3_1_pipeline.py#L12) imports `collections` / defaultdict.
- [scripts/rc3_1_pipeline.py:12](../../../../scripts/rc3_1_pipeline.py#L12) imports `collections` / deque.
- [scripts/rc3_1_pipeline.py:13](../../../../scripts/rc3_1_pipeline.py#L13) imports `pathlib` / Path.
- [scripts/rc3_1_pipeline.py:14](../../../../scripts/rc3_1_pipeline.py#L14) imports `typing` / Any.
- [scripts/rc3_1_pipeline.py:14](../../../../scripts/rc3_1_pipeline.py#L14) imports `typing` / Iterable.
- [scripts/rc3_1_pipeline.py:14](../../../../scripts/rc3_1_pipeline.py#L14) imports `typing` / Mapping.

## Symbols

### `scripts.rc3_1_pipeline.ROOT` — lines 17–17

- Source: [scripts/rc3_1_pipeline.py:17](../../../../scripts/rc3_1_pipeline.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.GOVERNANCE` — lines 18–18

- Source: [scripts/rc3_1_pipeline.py:18](../../../../scripts/rc3_1_pipeline.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.FREEZE_PATH` — lines 19–19

- Source: [scripts/rc3_1_pipeline.py:19](../../../../scripts/rc3_1_pipeline.py#L19)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.POLICY_PATH` — lines 20–20

- Source: [scripts/rc3_1_pipeline.py:20](../../../../scripts/rc3_1_pipeline.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.FINAL_COUNT` — lines 21–21

- Source: [scripts/rc3_1_pipeline.py:21](../../../../scripts/rc3_1_pipeline.py#L21)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.EVALUATOR_FILES` — lines 22–32

- Source: [scripts/rc3_1_pipeline.py:22](../../../../scripts/rc3_1_pipeline.py#L22)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.EVALUATION_SCRIPTS` — lines 33–45

- Source: [scripts/rc3_1_pipeline.py:33](../../../../scripts/rc3_1_pipeline.py#L33)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.PipelineHold` — lines 48–49

- Source: [scripts/rc3_1_pipeline.py:48](../../../../scripts/rc3_1_pipeline.py#L48)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.main` — lines 52–140

- Source: [scripts/rc3_1_pipeline.py:52](../../../../scripts/rc3_1_pipeline.py#L52)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `add_parser`, `add_subparsers`, `build_reserve`, `dumps`, `parse_args`, `print`, `release_decision`, `scan_contamination`, `seal_package`, `select_final`, `str`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.verify_freeze` — lines 143–174

- Source: [scripts/rc3_1_pipeline.py:143](../../../../scripts/rc3_1_pipeline.py#L143)
- Type: function
- Signature: `root: Path=ROOT`
- Direct static callees: `RuntimeError`, `any`, `append`, `bool`, `digest_json`, `git`, `join`, `len`, `load_json`, `relative_to`, `runtime_manifest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.runtime_manifest` — lines 177–187

- Source: [scripts/rc3_1_pipeline.py:177](../../../../scripts/rc3_1_pipeline.py#L177)
- Type: function
- Signature: `root: Path=ROOT`
- Direct static callees: `any`, `append`, `casefold`, `endswith`, `git`, `sha256`, `sorted`, `splitlines`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.build_reserve` — lines 190–226

- Source: [scripts/rc3_1_pipeline.py:190](../../../../scripts/rc3_1_pipeline.py#L190)
- Type: function
- Signature: `candidates_path: Path, old_inputs_path: Path, output_path: Path`
- Direct static callees: `PipelineHold`, `len`, `load_json`, `map`, `require_hash`, `sha256`, `sort`, `stable_rank`, `str`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.select_final` — lines 229–360

- Source: [scripts/rc3_1_pipeline.py:229](../../../../scripts/rc3_1_pipeline.py#L229)
- Type: function
- Signature: `*, candidates_path: Path, old_inputs_path: Path, old_report_path: Path, old_labels_path: Path, reserve_inputs_path: Path, reserve_report_path: Path, reserve_labels_path: Path, output_dir: Path`
- Direct static callees: `Counter`, `PipelineHold`, `RuntimeError`, `annotation_evidence`, `any`, `case_coverage`, `coverage_selection`, `dict`, `digest_json`, `eligible_case_ids`, `ensure_new_directory`, `get`, `len`, `load_json`, `map`, `public_input`, `require_hash`, `resolve`, `script_manifest`, `set`, `sha256`, `sorted`, `stable_rank`, `values`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.annotation_evidence` — lines 363–396

- Source: [scripts/rc3_1_pipeline.py:363](../../../../scripts/rc3_1_pipeline.py#L363)
- Type: function
- Signature: `report_path: Path, labels_path: Path, inputs_path: Path`
- Direct static callees: `RuntimeError`, `get`, `load_json`, `set`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.eligible_case_ids` — lines 399–405

- Source: [scripts/rc3_1_pipeline.py:399](../../../../scripts/rc3_1_pipeline.py#L399)
- Type: function
- Signature: `states: Mapping[str, Mapping[str, Any]], case_ids: Iterable[str]`
- Direct static callees: `sorted`, `stable_rank`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.coverage_selection` — lines 408–487

- Source: [scripts/rc3_1_pipeline.py:408](../../../../scripts/rc3_1_pipeline.py#L408)
- Type: function
- Signature: `eligible_ids: list[str], cases: Mapping[str, dict[str, Any]], annotations: Mapping[str, dict[str, Any]], policy: Mapping[str, Any]`
- Direct static callees: `Counter`, `PipelineHold`, `add`, `append`, `case_coverage`, `defaultdict`, `deque`, `dict`, `items`, `join`, `len`, `lifecycle_signature`, `max`, `min`, `popleft`, `required_coverage_tokens`, `set`, `sorted`, `stable_rank`, `union`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.required_coverage_tokens` — lines 490–498

- Source: [scripts/rc3_1_pipeline.py:490](../../../../scripts/rc3_1_pipeline.py#L490)
- Type: function
- Signature: `policy: Mapping[str, Any]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.case_coverage` — lines 501–516

- Source: [scripts/rc3_1_pipeline.py:501](../../../../scripts/rc3_1_pipeline.py#L501)
- Type: function
- Signature: `case: Mapping[str, Any], annotation: Mapping[str, Any]`
- Direct static callees: `add`, `get`, `len`, `public_categories`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.public_categories` — lines 519–546

- Source: [scripts/rc3_1_pipeline.py:519](../../../../scripts/rc3_1_pipeline.py#L519)
- Type: function
- Signature: `case: Mapping[str, Any]`
- Direct static callees: `add`, `get`, `items`, `set`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.scan_contamination` — lines 549–625

- Source: [scripts/rc3_1_pipeline.py:549](../../../../scripts/rc3_1_pipeline.py#L549)
- Type: function
- Signature: `selected_inputs_path: Path, private_labels_path: Path, output_path: Path, artifacts: list[Path] | None=None`
- Direct static callees: `RuntimeError`, `append`, `encode`, `evaluation_only_path`, `extend`, `git`, `hexdigest`, `is_file`, `len`, `load_json`, `private_label_fragments`, `read_bytes`, `resolve`, `runtime_manifest`, `scan_artifact`, `set`, `sha256`, `splitlines`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.scan_artifact` — lines 628–691

- Source: [scripts/rc3_1_pipeline.py:628](../../../../scripts/rc3_1_pipeline.py#L628)
- Type: function
- Signature: `path: Path, private_bytes: bytes, private_hash: str, case_ids: list[str], private_fragments: list[tuple[str, bytes]] | None=None`
- Direct static callees: `ZipFile`, `append`, `casefold`, `encode`, `endswith`, `extractfile`, `getmembers`, `inspect_member`, `is_tarfile`, `is_zipfile`, `isfile`, `namelist`, `open`, `read`, `read_bytes`, `sha256`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.private_label_fragments` — lines 694–703

- Source: [scripts/rc3_1_pipeline.py:694](../../../../scripts/rc3_1_pipeline.py#L694)
- Type: function
- Signature: `labels: Mapping[str, Any]`
- Direct static callees: `append`, `dumps`, `encode`, `hexdigest`, `len`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.seal_package` — lines 706–803

- Source: [scripts/rc3_1_pipeline.py:706](../../../../scripts/rc3_1_pipeline.py#L706)
- Type: function
- Signature: `selection_dir: Path, contamination_path: Path, evaluator_identity_path: Path, output_dir: Path`
- Direct static callees: `RuntimeError`, `any`, `chmod`, `copy2`, `digest_json`, `ensure_new_directory`, `items`, `len`, `load_json`, `map`, `mkdir`, `script_manifest`, `sha256`, `tree_manifest`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.release_decision` — lines 806–862

- Source: [scripts/rc3_1_pipeline.py:806](../../../../scripts/rc3_1_pipeline.py#L806)
- Type: function
- Signature: `*, seal_manifest_path: Path, contamination_path: Path, verification_path: Path, execution_path: Path | None, score_path: Path | None, output_path: Path`
- Direct static callees: `append`, `get`, `load_json`, `resolve`, `str`, `verify_freeze`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.script_manifest` — lines 865–874

- Source: [scripts/rc3_1_pipeline.py:865](../../../../scripts/rc3_1_pipeline.py#L865)
- Type: function
- Signature: `*, require_tracked: bool`
- Direct static callees: `RuntimeError`, `git`, `is_file`, `join`, `set`, `sha256`, `splitlines`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.lifecycle_signature` — lines 877–884

- Source: [scripts/rc3_1_pipeline.py:877](../../../../scripts/rc3_1_pipeline.py#L877)
- Type: function
- Signature: `annotation: Mapping[str, Any]`
- Direct static callees: `digest_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.public_input` — lines 887–894

- Source: [scripts/rc3_1_pipeline.py:887](../../../../scripts/rc3_1_pipeline.py#L887)
- Type: function
- Signature: `case: Mapping[str, Any]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.evaluation_only_path` — lines 897–900

- Source: [scripts/rc3_1_pipeline.py:897](../../../../scripts/rc3_1_pipeline.py#L897)
- Type: function
- Signature: `name: str`
- Direct static callees: `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.tree_manifest` — lines 903–908

- Source: [scripts/rc3_1_pipeline.py:903](../../../../scripts/rc3_1_pipeline.py#L903)
- Type: function
- Signature: `root: Path`
- Direct static callees: `is_file`, `relative_to`, `rglob`, `sha256`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.stable_rank` — lines 911–912

- Source: [scripts/rc3_1_pipeline.py:911](../../../../scripts/rc3_1_pipeline.py#L911)
- Type: function
- Signature: `salt: str, case_id: str`
- Direct static callees: `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.require_hash` — lines 915–918

- Source: [scripts/rc3_1_pipeline.py:915](../../../../scripts/rc3_1_pipeline.py#L915)
- Type: function
- Signature: `path: Path, expected: str, label: str`
- Direct static callees: `RuntimeError`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.ensure_new_directory` — lines 921–926

- Source: [scripts/rc3_1_pipeline.py:921](../../../../scripts/rc3_1_pipeline.py#L921)
- Type: function
- Signature: `path: Path`
- Direct static callees: `FileExistsError`, `any`, `exists`, `iterdir`, `mkdir`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.write_json` — lines 929–936

- Source: [scripts/rc3_1_pipeline.py:929](../../../../scripts/rc3_1_pipeline.py#L929)
- Type: function
- Signature: `path: Path, value: Any, *, overwrite: bool`
- Direct static callees: `FileExistsError`, `dumps`, `exists`, `mkdir`, `replace`, `resolve`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.load_json` — lines 939–944

- Source: [scripts/rc3_1_pipeline.py:939](../../../../scripts/rc3_1_pipeline.py#L939)
- Type: function
- Signature: `path: Path`
- Direct static callees: `RuntimeError`, `isinstance`, `loads`, `read_text`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.sha256` — lines 947–948

- Source: [scripts/rc3_1_pipeline.py:947](../../../../scripts/rc3_1_pipeline.py#L947)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `resolve`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.digest_json` — lines 951–954

- Source: [scripts/rc3_1_pipeline.py:951](../../../../scripts/rc3_1_pipeline.py#L951)
- Type: function
- Signature: `value: Any`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.resolve` — lines 957–958

- Source: [scripts/rc3_1_pipeline.py:957](../../../../scripts/rc3_1_pipeline.py#L957)
- Type: function
- Signature: `path: Path`
- Direct static callees: `is_absolute`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.rc3_1_pipeline.git` — lines 961–962

- Source: [scripts/rc3_1_pipeline.py:961](../../../../scripts/rc3_1_pipeline.py#L961)
- Type: function
- Signature: `*args: str, root: Path=ROOT`
- Direct static callees: `check_output`, `strip`
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

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–17

Implements module-level `Assign` behavior or data.

### Lines 18–18

Implements module-level `Assign` behavior or data.

### Lines 19–19

Implements module-level `Assign` behavior or data.

### Lines 20–20

Implements module-level `Assign` behavior or data.

### Lines 21–21

Implements module-level `Assign` behavior or data.

### Lines 22–32

Implements module-level `Assign` behavior or data.

### Lines 33–45

Implements module-level `Assign` behavior or data.

### Lines 46–47

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 48–49

Defines class `PipelineHold` and the behavior of its members.

### Lines 50–51

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 52–81

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, build_reserve, dumps, parse_args, print, release_decision, scan_contamination, seal_package, select_final, str, verify_freeze, write_json.

### Lines 82–111

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, build_reserve, dumps, parse_args, print, release_decision, scan_contamination, seal_package, select_final, str, verify_freeze, write_json.

### Lines 112–140

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, build_reserve, dumps, parse_args, print, release_decision, scan_contamination, seal_package, select_final, str, verify_freeze, write_json.

### Lines 141–142

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 143–172

Defines `verify_freeze` and its implementation control flow; direct static calls: RuntimeError, any, append, bool, digest_json, git, join, len, load_json, relative_to, runtime_manifest, sha256.

### Lines 173–174

Defines `verify_freeze` and its implementation control flow; direct static calls: RuntimeError, any, append, bool, digest_json, git, join, len, load_json, relative_to, runtime_manifest, sha256.

### Lines 175–176

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 177–187

Defines `runtime_manifest` and its implementation control flow; direct static calls: any, append, casefold, endswith, git, sha256, sorted, splitlines.

### Lines 188–189

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 190–219

Defines `build_reserve` and its implementation control flow; direct static calls: PipelineHold, len, load_json, map, require_hash, sha256, sort, stable_rank, str, verify_freeze, write_json.

### Lines 220–226

Defines `build_reserve` and its implementation control flow; direct static calls: PipelineHold, len, load_json, map, require_hash, sha256, sort, stable_rank, str, verify_freeze, write_json.

### Lines 227–228

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 229–258

Defines `select_final` and its implementation control flow; direct static calls: Counter, PipelineHold, RuntimeError, annotation_evidence, any, case_coverage, coverage_selection, dict, digest_json, eligible_case_ids, ensure_new_directory, get, len, load_json, map, public_input, require_hash, resolve, script_manifest, set, sha256, sorted, stable_rank, values, verify_freeze, write_json.

### Lines 259–288

Defines `select_final` and its implementation control flow; direct static calls: Counter, PipelineHold, RuntimeError, annotation_evidence, any, case_coverage, coverage_selection, dict, digest_json, eligible_case_ids, ensure_new_directory, get, len, load_json, map, public_input, require_hash, resolve, script_manifest, set, sha256, sorted, stable_rank, values, verify_freeze, write_json.

### Lines 289–318

Defines `select_final` and its implementation control flow; direct static calls: Counter, PipelineHold, RuntimeError, annotation_evidence, any, case_coverage, coverage_selection, dict, digest_json, eligible_case_ids, ensure_new_directory, get, len, load_json, map, public_input, require_hash, resolve, script_manifest, set, sha256, sorted, stable_rank, values, verify_freeze, write_json.

### Lines 319–348

Defines `select_final` and its implementation control flow; direct static calls: Counter, PipelineHold, RuntimeError, annotation_evidence, any, case_coverage, coverage_selection, dict, digest_json, eligible_case_ids, ensure_new_directory, get, len, load_json, map, public_input, require_hash, resolve, script_manifest, set, sha256, sorted, stable_rank, values, verify_freeze, write_json.

### Lines 349–360

Defines `select_final` and its implementation control flow; direct static calls: Counter, PipelineHold, RuntimeError, annotation_evidence, any, case_coverage, coverage_selection, dict, digest_json, eligible_case_ids, ensure_new_directory, get, len, load_json, map, public_input, require_hash, resolve, script_manifest, set, sha256, sorted, stable_rank, values, verify_freeze, write_json.

### Lines 361–362

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 363–392

Defines `annotation_evidence` and its implementation control flow; direct static calls: RuntimeError, get, load_json, set, sha256.

### Lines 393–396

Defines `annotation_evidence` and its implementation control flow; direct static calls: RuntimeError, get, load_json, set, sha256.

### Lines 397–398

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 399–405

Defines `eligible_case_ids` and its implementation control flow; direct static calls: sorted, stable_rank.

### Lines 406–407

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 408–437

Defines `coverage_selection` and its implementation control flow; direct static calls: Counter, PipelineHold, add, append, case_coverage, defaultdict, deque, dict, items, join, len, lifecycle_signature, max, min, popleft, required_coverage_tokens, set, sorted, stable_rank, union, values.

### Lines 438–467

Defines `coverage_selection` and its implementation control flow; direct static calls: Counter, PipelineHold, add, append, case_coverage, defaultdict, deque, dict, items, join, len, lifecycle_signature, max, min, popleft, required_coverage_tokens, set, sorted, stable_rank, union, values.

### Lines 468–487

Defines `coverage_selection` and its implementation control flow; direct static calls: Counter, PipelineHold, add, append, case_coverage, defaultdict, deque, dict, items, join, len, lifecycle_signature, max, min, popleft, required_coverage_tokens, set, sorted, stable_rank, union, values.

### Lines 488–489

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 490–498

Defines `required_coverage_tokens` and its implementation control flow; direct static calls: none resolved.

### Lines 499–500

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 501–516

Defines `case_coverage` and its implementation control flow; direct static calls: add, get, len, public_categories.

### Lines 517–518

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 519–546

Defines `public_categories` and its implementation control flow; direct static calls: add, get, items, set, str.

### Lines 547–548

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 549–578

Defines `scan_contamination` and its implementation control flow; direct static calls: RuntimeError, append, encode, evaluation_only_path, extend, git, hexdigest, is_file, len, load_json, private_label_fragments, read_bytes, resolve, runtime_manifest, scan_artifact, set, sha256, splitlines, verify_freeze, write_json.

### Lines 579–608

Defines `scan_contamination` and its implementation control flow; direct static calls: RuntimeError, append, encode, evaluation_only_path, extend, git, hexdigest, is_file, len, load_json, private_label_fragments, read_bytes, resolve, runtime_manifest, scan_artifact, set, sha256, splitlines, verify_freeze, write_json.

### Lines 609–625

Defines `scan_contamination` and its implementation control flow; direct static calls: RuntimeError, append, encode, evaluation_only_path, extend, git, hexdigest, is_file, len, load_json, private_label_fragments, read_bytes, resolve, runtime_manifest, scan_artifact, set, sha256, splitlines, verify_freeze, write_json.

### Lines 626–627

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 628–657

Defines `scan_artifact` and its implementation control flow; direct static calls: ZipFile, append, casefold, encode, endswith, extractfile, getmembers, inspect_member, is_tarfile, is_zipfile, isfile, namelist, open, read, read_bytes, sha256, str.

### Lines 658–687

Defines `scan_artifact` and its implementation control flow; direct static calls: ZipFile, append, casefold, encode, endswith, extractfile, getmembers, inspect_member, is_tarfile, is_zipfile, isfile, namelist, open, read, read_bytes, sha256, str.

### Lines 688–691

Defines `scan_artifact` and its implementation control flow; direct static calls: ZipFile, append, casefold, encode, endswith, extractfile, getmembers, inspect_member, is_tarfile, is_zipfile, isfile, namelist, open, read, read_bytes, sha256, str.

### Lines 692–693

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 694–703

Defines `private_label_fragments` and its implementation control flow; direct static calls: append, dumps, encode, hexdigest, len, sha256.

### Lines 704–705

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 706–735

Defines `seal_package` and its implementation control flow; direct static calls: RuntimeError, any, chmod, copy2, digest_json, ensure_new_directory, items, len, load_json, map, mkdir, script_manifest, sha256, tree_manifest, verify_freeze, write_json.

### Lines 736–765

Defines `seal_package` and its implementation control flow; direct static calls: RuntimeError, any, chmod, copy2, digest_json, ensure_new_directory, items, len, load_json, map, mkdir, script_manifest, sha256, tree_manifest, verify_freeze, write_json.

### Lines 766–795

Defines `seal_package` and its implementation control flow; direct static calls: RuntimeError, any, chmod, copy2, digest_json, ensure_new_directory, items, len, load_json, map, mkdir, script_manifest, sha256, tree_manifest, verify_freeze, write_json.

### Lines 796–803

Defines `seal_package` and its implementation control flow; direct static calls: RuntimeError, any, chmod, copy2, digest_json, ensure_new_directory, items, len, load_json, map, mkdir, script_manifest, sha256, tree_manifest, verify_freeze, write_json.

### Lines 804–805

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 806–835

Defines `release_decision` and its implementation control flow; direct static calls: append, get, load_json, resolve, str, verify_freeze, write_json.

### Lines 836–862

Defines `release_decision` and its implementation control flow; direct static calls: append, get, load_json, resolve, str, verify_freeze, write_json.

### Lines 863–864

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 865–874

Defines `script_manifest` and its implementation control flow; direct static calls: RuntimeError, git, is_file, join, set, sha256, splitlines.

### Lines 875–876

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 877–884

Defines `lifecycle_signature` and its implementation control flow; direct static calls: digest_json.

### Lines 885–886

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 887–894

Defines `public_input` and its implementation control flow; direct static calls: none resolved.

### Lines 895–896

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 897–900

Defines `evaluation_only_path` and its implementation control flow; direct static calls: startswith.

### Lines 901–902

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 903–908

Defines `tree_manifest` and its implementation control flow; direct static calls: is_file, relative_to, rglob, sha256, sorted, str.

### Lines 909–910

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 911–912

Defines `stable_rank` and its implementation control flow; direct static calls: encode, hexdigest, sha256.

### Lines 913–914

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 915–918

Defines `require_hash` and its implementation control flow; direct static calls: RuntimeError, sha256.

### Lines 919–920

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 921–926

Defines `ensure_new_directory` and its implementation control flow; direct static calls: FileExistsError, any, exists, iterdir, mkdir.

### Lines 927–928

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 929–936

Defines `write_json` and its implementation control flow; direct static calls: FileExistsError, dumps, exists, mkdir, replace, resolve, with_suffix, write_text.

### Lines 937–938

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 939–944

Defines `load_json` and its implementation control flow; direct static calls: RuntimeError, isinstance, loads, read_text, resolve.

### Lines 945–946

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 947–948

Defines `sha256` and its implementation control flow; direct static calls: hexdigest, read_bytes, resolve, sha256.

### Lines 949–950

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 951–954

Defines `digest_json` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 955–956

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 957–958

Defines `resolve` and its implementation control flow; direct static calls: is_absolute, resolve.

### Lines 959–960

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 961–962

Defines `git` and its implementation control flow; direct static calls: check_output, strip.

### Lines 963–964

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 965–966

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
