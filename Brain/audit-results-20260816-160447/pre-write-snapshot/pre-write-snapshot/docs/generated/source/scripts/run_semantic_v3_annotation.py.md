# `scripts/run_semantic_v3_annotation.py`

## File purpose

This automation and release file is reviewed at snapshot `e513b2ed15e4509701aa773a00f92b5a8082cdaafdf4afe90693444f158784c8`. It contains 298 lines.

## Imports and module state

- [scripts/run_semantic_v3_annotation.py:1](../../../../scripts/run_semantic_v3_annotation.py#L1) imports `__future__` / annotations.
- [scripts/run_semantic_v3_annotation.py:3](../../../../scripts/run_semantic_v3_annotation.py#L3) imports `argparse`.
- [scripts/run_semantic_v3_annotation.py:4](../../../../scripts/run_semantic_v3_annotation.py#L4) imports `hashlib`.
- [scripts/run_semantic_v3_annotation.py:5](../../../../scripts/run_semantic_v3_annotation.py#L5) imports `json`.
- [scripts/run_semantic_v3_annotation.py:6](../../../../scripts/run_semantic_v3_annotation.py#L6) imports `platform`.
- [scripts/run_semantic_v3_annotation.py:7](../../../../scripts/run_semantic_v3_annotation.py#L7) imports `time`.
- [scripts/run_semantic_v3_annotation.py:8](../../../../scripts/run_semantic_v3_annotation.py#L8) imports `urllib.error`.
- [scripts/run_semantic_v3_annotation.py:9](../../../../scripts/run_semantic_v3_annotation.py#L9) imports `urllib.request`.
- [scripts/run_semantic_v3_annotation.py:10](../../../../scripts/run_semantic_v3_annotation.py#L10) imports `datetime` / datetime.
- [scripts/run_semantic_v3_annotation.py:10](../../../../scripts/run_semantic_v3_annotation.py#L10) imports `datetime` / timezone.
- [scripts/run_semantic_v3_annotation.py:11](../../../../scripts/run_semantic_v3_annotation.py#L11) imports `pathlib` / Path.
- [scripts/run_semantic_v3_annotation.py:12](../../../../scripts/run_semantic_v3_annotation.py#L12) imports `typing` / Any.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / TOOL_FAMILIES_BY_TOOL.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / annotation_agreement.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / annotation_schema.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / derive_policy_constraints.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / label_sha256.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / semantic_label_projection.
- [scripts/run_semantic_v3_annotation.py:14](../../../../scripts/run_semantic_v3_annotation.py#L14) imports `mind01.annotation_v3` / validate_annotation.

## Symbols

### `scripts.run_semantic_v3_annotation.MODEL` — lines 25–25

- Source: [scripts/run_semantic_v3_annotation.py:25](../../../../scripts/run_semantic_v3_annotation.py#L25)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.MODEL_DIGEST` — lines 26–26

- Source: [scripts/run_semantic_v3_annotation.py:26](../../../../scripts/run_semantic_v3_annotation.py#L26)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.OLLAMA_URL` — lines 27–27

- Source: [scripts/run_semantic_v3_annotation.py:27](../../../../scripts/run_semantic_v3_annotation.py#L27)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.EVALUATOR_VERSION` — lines 28–28

- Source: [scripts/run_semantic_v3_annotation.py:28](../../../../scripts/run_semantic_v3_annotation.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.PUBLIC_SPEC` — lines 29–36

- Source: [scripts/run_semantic_v3_annotation.py:29](../../../../scripts/run_semantic_v3_annotation.py#L29)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.TOOL_PUBLIC_SPEC` — lines 37–40

- Source: [scripts/run_semantic_v3_annotation.py:37](../../../../scripts/run_semantic_v3_annotation.py#L37)
- Type: constant
- Signature: `n/a`
- Direct static callees: `items`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.TOOL_DESCRIPTIONS` — lines 41–52

- Source: [scripts/run_semantic_v3_annotation.py:41](../../../../scripts/run_semantic_v3_annotation.py#L41)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.main` — lines 55–128

- Source: [scripts/run_semantic_v3_annotation.py:55](../../../../scripts/run_semantic_v3_annotation.py#L55)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `RuntimeError`, `_report`, `add_argument`, `adjudicate`, `annotate`, `annotation_agreement`, `append`, `derive_policy_constraints`, `digest_json`, `dumps`, `enumerate`, `isinstance`, `len`, `loads`, `mkdir`, `model_identity`, `monotonic`, `parse_args`, `print`, `read_text`, `resolve`, `semantic_label_projection`, `str`, `to_dict`, `validate_annotation`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.annotate` — lines 131–145

- Source: [scripts/run_semantic_v3_annotation.py:131](../../../../scripts/run_semantic_v3_annotation.py#L131)
- Type: function
- Signature: `case: dict[str, Any], constraints: Any, annotator: str, seed: int, timeout: int`
- Direct static callees: `annotation_schema`, `dumps`, `ollama_generate`, `public_case`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.adjudicate` — lines 148–170

- Source: [scripts/run_semantic_v3_annotation.py:148](../../../../scripts/run_semantic_v3_annotation.py#L148)
- Type: function
- Signature: `case: dict[str, Any], constraints: Any, left: dict[str, Any], right: dict[str, Any], left_errors: list[str], right_errors: list[str], seed: int, timeout: int`
- Direct static callees: `annotation_schema`, `dumps`, `ollama_generate`, `public_case`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.public_case` — lines 173–181

- Source: [scripts/run_semantic_v3_annotation.py:173](../../../../scripts/run_semantic_v3_annotation.py#L173)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.ollama_generate` — lines 184–203

- Source: [scripts/run_semantic_v3_annotation.py:184](../../../../scripts/run_semantic_v3_annotation.py#L184)
- Type: function
- Signature: `system: str, prompt: str, schema: dict[str, Any], seed: int, temperature: float, timeout: int`
- Direct static callees: `Request`, `RuntimeError`, `decode`, `dumps`, `encode`, `isinstance`, `loads`, `read`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.model_identity` — lines 206–219

- Source: [scripts/run_semantic_v3_annotation.py:206](../../../../scripts/run_semantic_v3_annotation.py#L206)
- Type: function
- Signature: `timeout: int`
- Direct static callees: `Request`, `decode`, `get`, `loads`, `min`, `next`, `read`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation._report` — lines 222–283

- Source: [scripts/run_semantic_v3_annotation.py:222](../../../../scripts/run_semantic_v3_annotation.py#L222)
- Type: function
- Signature: `mode: str, source: Path, metadata: dict[str, Any], cases: list[dict[str, Any]], accepted: list[dict[str, Any]], records: list[dict[str, Any]], duration: float, complete: bool`
- Direct static callees: `any`, `bool`, `get`, `hexdigest`, `isoformat`, `label_sha256`, `len`, `now`, `platform`, `predicate`, `python_version`, `rate`, `read_bytes`, `round`, `sha256`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.digest_json` — lines 286–287

- Source: [scripts/run_semantic_v3_annotation.py:286](../../../../scripts/run_semantic_v3_annotation.py#L286)
- Type: function
- Signature: `payload: Any`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_semantic_v3_annotation.write_json` — lines 290–294

- Source: [scripts/run_semantic_v3_annotation.py:290](../../../../scripts/run_semantic_v3_annotation.py#L290)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `mkdir`, `replace`, `with_suffix`, `write_text`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–22

Imports a dependency used by this module.

### Lines 23–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–25

Implements module-level `Assign` behavior or data.

### Lines 26–26

Implements module-level `Assign` behavior or data.

### Lines 27–27

Implements module-level `Assign` behavior or data.

### Lines 28–28

Implements module-level `Assign` behavior or data.

### Lines 29–36

Implements module-level `Assign` behavior or data.

### Lines 37–40

Implements module-level `Assign` behavior or data.

### Lines 41–52

Implements module-level `Assign` behavior or data.

### Lines 53–54

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 55–84

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, _report, add_argument, adjudicate, annotate, annotation_agreement, append, derive_policy_constraints, digest_json, dumps, enumerate, isinstance, len, loads, mkdir, model_identity, monotonic, parse_args, print, read_text, resolve, semantic_label_projection, str, to_dict, validate_annotation, write_json.

### Lines 85–114

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, _report, add_argument, adjudicate, annotate, annotation_agreement, append, derive_policy_constraints, digest_json, dumps, enumerate, isinstance, len, loads, mkdir, model_identity, monotonic, parse_args, print, read_text, resolve, semantic_label_projection, str, to_dict, validate_annotation, write_json.

### Lines 115–128

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, _report, add_argument, adjudicate, annotate, annotation_agreement, append, derive_policy_constraints, digest_json, dumps, enumerate, isinstance, len, loads, mkdir, model_identity, monotonic, parse_args, print, read_text, resolve, semantic_label_projection, str, to_dict, validate_annotation, write_json.

### Lines 129–130

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 131–145

Defines `annotate` and its implementation control flow; direct static calls: annotation_schema, dumps, ollama_generate, public_case, to_dict.

### Lines 146–147

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 148–170

Defines `adjudicate` and its implementation control flow; direct static calls: annotation_schema, dumps, ollama_generate, public_case, to_dict.

### Lines 171–172

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 173–181

Defines `public_case` and its implementation control flow; direct static calls: get.

### Lines 182–183

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 184–203

Defines `ollama_generate` and its implementation control flow; direct static calls: Request, RuntimeError, decode, dumps, encode, isinstance, loads, read, urlopen.

### Lines 204–205

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 206–219

Defines `model_identity` and its implementation control flow; direct static calls: Request, decode, get, loads, min, next, read, urlopen.

### Lines 220–221

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 222–251

Defines `_report` and its implementation control flow; direct static calls: any, bool, get, hexdigest, isoformat, label_sha256, len, now, platform, predicate, python_version, rate, read_bytes, round, sha256, sum.

### Lines 252–281

Defines `_report` and its implementation control flow; direct static calls: any, bool, get, hexdigest, isoformat, label_sha256, len, now, platform, predicate, python_version, rate, read_bytes, round, sha256, sum.

### Lines 282–283

Defines `_report` and its implementation control flow; direct static calls: any, bool, get, hexdigest, isoformat, label_sha256, len, now, platform, predicate, python_version, rate, read_bytes, round, sha256, sum.

### Lines 284–285

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 286–287

Defines `digest_json` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 288–289

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 290–294

Defines `write_json` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

### Lines 295–296

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 297–298

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
