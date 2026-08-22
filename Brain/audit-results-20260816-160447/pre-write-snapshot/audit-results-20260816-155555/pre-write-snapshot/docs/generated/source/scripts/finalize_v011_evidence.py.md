# `scripts/finalize_v011_evidence.py`

## File purpose

This automation and release file is reviewed at snapshot `aaaa94c12d786045e9d6441d4671ab6fdbcb0d197cbab7367a87788e643ca825`. It contains 434 lines.

## Imports and module state

- [scripts/finalize_v011_evidence.py:1](../../../../scripts/finalize_v011_evidence.py#L1) imports `__future__` / annotations.
- [scripts/finalize_v011_evidence.py:3](../../../../scripts/finalize_v011_evidence.py#L3) imports `argparse`.
- [scripts/finalize_v011_evidence.py:4](../../../../scripts/finalize_v011_evidence.py#L4) imports `hashlib`.
- [scripts/finalize_v011_evidence.py:5](../../../../scripts/finalize_v011_evidence.py#L5) imports `json`.
- [scripts/finalize_v011_evidence.py:6](../../../../scripts/finalize_v011_evidence.py#L6) imports `platform`.
- [scripts/finalize_v011_evidence.py:7](../../../../scripts/finalize_v011_evidence.py#L7) imports `statistics`.
- [scripts/finalize_v011_evidence.py:8](../../../../scripts/finalize_v011_evidence.py#L8) imports `subprocess`.
- [scripts/finalize_v011_evidence.py:9](../../../../scripts/finalize_v011_evidence.py#L9) imports `sys`.
- [scripts/finalize_v011_evidence.py:10](../../../../scripts/finalize_v011_evidence.py#L10) imports `datetime` / datetime.
- [scripts/finalize_v011_evidence.py:10](../../../../scripts/finalize_v011_evidence.py#L10) imports `datetime` / timezone.
- [scripts/finalize_v011_evidence.py:11](../../../../scripts/finalize_v011_evidence.py#L11) imports `pathlib` / Path.
- [scripts/finalize_v011_evidence.py:12](../../../../scripts/finalize_v011_evidence.py#L12) imports `typing` / Any.
- [scripts/finalize_v011_evidence.py:18](../../../../scripts/finalize_v011_evidence.py#L18) imports `mind01.prompts` / SYSTEM_PROMPT.
- [scripts/finalize_v011_evidence.py:19](../../../../scripts/finalize_v011_evidence.py#L19) imports `mind01.semantic_eval` / load_partition.
- [scripts/finalize_v011_evidence.py:19](../../../../scripts/finalize_v011_evidence.py#L19) imports `mind01.semantic_eval` / run_deterministic_semantic_routing.
- [scripts/finalize_v011_evidence.py:19](../../../../scripts/finalize_v011_evidence.py#L19) imports `mind01.semantic_eval` / validate_semantic_routing_assets.
- [scripts/finalize_v011_evidence.py:20](../../../../scripts/finalize_v011_evidence.py#L20) imports `mind01.version` / __version__.

## Symbols

### `scripts.finalize_v011_evidence.ROOT` — lines 15–15

- Source: [scripts/finalize_v011_evidence.py:15](../../../../scripts/finalize_v011_evidence.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.RUN_DIRECTORIES` — lines 23–30

- Source: [scripts/finalize_v011_evidence.py:23](../../../../scripts/finalize_v011_evidence.py#L23)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.sha256_file` — lines 33–38

- Source: [scripts/finalize_v011_evidence.py:33](../../../../scripts/finalize_v011_evidence.py#L33)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `iter`, `open`, `read`, `sha256`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.write_json` — lines 41–43

- Source: [scripts/finalize_v011_evidence.py:41](../../../../scripts/finalize_v011_evidence.py#L41)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `mkdir`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.read_json` — lines 46–51

- Source: [scripts/finalize_v011_evidence.py:46](../../../../scripts/finalize_v011_evidence.py#L46)
- Type: function
- Signature: `path: Path`
- Direct static callees: `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.git_text` — lines 54–63

- Source: [scripts/finalize_v011_evidence.py:54](../../../../scripts/finalize_v011_evidence.py#L54)
- Type: function
- Signature: `*args: str`
- Direct static callees: `run`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.derive_live_metrics` — lines 66–128

- Source: [scripts/finalize_v011_evidence.py:66](../../../../scripts/finalize_v011_evidence.py#L66)
- Type: function
- Signature: `payload: dict[str, Any], partition: str`
- Direct static callees: `bool`, `get`, `incident_codes`, `int`, `isinstance`, `items`, `len`, `load_partition`, `max`, `setdefault`, `sorted`, `str`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.retained_runs` — lines 131–154

- Source: [scripts/finalize_v011_evidence.py:131](../../../../scripts/finalize_v011_evidence.py#L131)
- Type: function
- Signature: `output: Path`
- Direct static callees: `append`, `bool`, `derive_live_metrics`, `get`, `glob`, `items`, `mkdir`, `read_json`, `relative_to`, `sha256_file`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.aggregate` — lines 157–187

- Source: [scripts/finalize_v011_evidence.py:157](../../../../scripts/finalize_v011_evidence.py#L157)
- Type: function
- Signature: `runs: dict[str, list[dict[str, Any]]]`
- Direct static callees: `float`, `fmean`, `get`, `isinstance`, `items`, `len`, `max`, `min`, `pstdev`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.artifact_identity` — lines 190–201

- Source: [scripts/finalize_v011_evidence.py:190](../../../../scripts/finalize_v011_evidence.py#L190)
- Type: function
- Signature: `output: Path`
- Direct static callees: `is_file`, `iterdir`, `mkdir`, `relative_to`, `sha256_file`, `sorted`, `stat`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.render_failure_analysis` — lines 204–239

- Source: [scripts/finalize_v011_evidence.py:204](../../../../scripts/finalize_v011_evidence.py#L204)
- Type: function
- Signature: `deterministic: dict[str, Any], runs: dict[str, list[dict[str, Any]]]`
- Direct static callees: `append`, `dumps`, `extend`, `get`, `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.render_release_report` — lines 242–283

- Source: [scripts/finalize_v011_evidence.py:242](../../../../scripts/finalize_v011_evidence.py#L242)
- Type: function
- Signature: `manifest: dict[str, Any]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.finalize_v011_evidence.main` — lines 286–430

- Source: [scripts/finalize_v011_evidence.py:286](../../../../scripts/finalize_v011_evidence.py#L286)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `aggregate`, `artifact_identity`, `dumps`, `encode`, `get`, `git_text`, `hexdigest`, `is_absolute`, `is_file`, `isinstance`, `isoformat`, `items`, `mkdir`, `next`, `now`, `parse_args`, `platform`, `print`, `render_failure_analysis`, `render_release_report`, `resolve`, `retained_runs`, `run_deterministic_semantic_routing`, `sha256`, `sha256_file`, `str`, `validate_semantic_routing_assets`, `write_json`, `write_text`
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

### Lines 13–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–16

Implements module-level `Expr` behavior or data.

### Lines 17–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–22

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 23–30

Implements module-level `Assign` behavior or data.

### Lines 31–32

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 33–38

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, iter, open, read, sha256, update.

### Lines 39–40

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 41–43

Defines `write_json` and its implementation control flow; direct static calls: dumps, mkdir, write_text.

### Lines 44–45

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 46–51

Defines `read_json` and its implementation control flow; direct static calls: isinstance, loads, read_text.

### Lines 52–53

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 54–63

Defines `git_text` and its implementation control flow; direct static calls: run, strip.

### Lines 64–65

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 66–95

Defines `derive_live_metrics` and its implementation control flow; direct static calls: bool, get, incident_codes, int, isinstance, items, len, load_partition, max, setdefault, sorted, str, sum.

### Lines 96–125

Defines `derive_live_metrics` and its implementation control flow; direct static calls: bool, get, incident_codes, int, isinstance, items, len, load_partition, max, setdefault, sorted, str, sum.

### Lines 126–128

Defines `derive_live_metrics` and its implementation control flow; direct static calls: bool, get, incident_codes, int, isinstance, items, len, load_partition, max, setdefault, sorted, str, sum.

### Lines 129–130

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 131–154

Defines `retained_runs` and its implementation control flow; direct static calls: append, bool, derive_live_metrics, get, glob, items, mkdir, read_json, relative_to, sha256_file, sorted, str.

### Lines 155–156

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 157–186

Defines `aggregate` and its implementation control flow; direct static calls: float, fmean, get, isinstance, items, len, max, min, pstdev.

### Lines 187–187

Defines `aggregate` and its implementation control flow; direct static calls: float, fmean, get, isinstance, items, len, max, min, pstdev.

### Lines 188–189

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 190–201

Defines `artifact_identity` and its implementation control flow; direct static calls: is_file, iterdir, mkdir, relative_to, sha256_file, sorted, stat, str.

### Lines 202–203

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 204–233

Defines `render_failure_analysis` and its implementation control flow; direct static calls: append, dumps, extend, get, join.

### Lines 234–239

Defines `render_failure_analysis` and its implementation control flow; direct static calls: append, dumps, extend, get, join.

### Lines 240–241

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 242–271

Defines `render_release_report` and its implementation control flow; direct static calls: none resolved.

### Lines 272–283

Defines `render_release_report` and its implementation control flow; direct static calls: none resolved.

### Lines 284–285

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 286–315

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, aggregate, artifact_identity, dumps, encode, get, git_text, hexdigest, is_absolute, is_file, isinstance, isoformat, items, mkdir, next, now, parse_args, platform, print, render_failure_analysis, render_release_report, resolve, retained_runs, run_deterministic_semantic_routing, sha256, sha256_file, str, validate_semantic_routing_assets, write_json, write_text.

### Lines 316–345

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, aggregate, artifact_identity, dumps, encode, get, git_text, hexdigest, is_absolute, is_file, isinstance, isoformat, items, mkdir, next, now, parse_args, platform, print, render_failure_analysis, render_release_report, resolve, retained_runs, run_deterministic_semantic_routing, sha256, sha256_file, str, validate_semantic_routing_assets, write_json, write_text.

### Lines 346–375

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, aggregate, artifact_identity, dumps, encode, get, git_text, hexdigest, is_absolute, is_file, isinstance, isoformat, items, mkdir, next, now, parse_args, platform, print, render_failure_analysis, render_release_report, resolve, retained_runs, run_deterministic_semantic_routing, sha256, sha256_file, str, validate_semantic_routing_assets, write_json, write_text.

### Lines 376–405

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, aggregate, artifact_identity, dumps, encode, get, git_text, hexdigest, is_absolute, is_file, isinstance, isoformat, items, mkdir, next, now, parse_args, platform, print, render_failure_analysis, render_release_report, resolve, retained_runs, run_deterministic_semantic_routing, sha256, sha256_file, str, validate_semantic_routing_assets, write_json, write_text.

### Lines 406–430

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, aggregate, artifact_identity, dumps, encode, get, git_text, hexdigest, is_absolute, is_file, isinstance, isoformat, items, mkdir, next, now, parse_args, platform, print, render_failure_analysis, render_release_report, resolve, retained_runs, run_deterministic_semantic_routing, sha256, sha256_file, str, validate_semantic_routing_assets, write_json, write_text.

### Lines 431–432

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 433–434

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
