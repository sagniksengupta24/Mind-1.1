# `scripts/freeze_semantic_v3_evaluator.py`

## File purpose

This automation and release file is reviewed at snapshot `a1554171e168a308b99c58d9afc2fa2e46887c0f803a459597e28eb79872155b`. It contains 188 lines.

## Imports and module state

- [scripts/freeze_semantic_v3_evaluator.py:1](../../../../scripts/freeze_semantic_v3_evaluator.py#L1) imports `__future__` / annotations.
- [scripts/freeze_semantic_v3_evaluator.py:3](../../../../scripts/freeze_semantic_v3_evaluator.py#L3) imports `argparse`.
- [scripts/freeze_semantic_v3_evaluator.py:4](../../../../scripts/freeze_semantic_v3_evaluator.py#L4) imports `hashlib`.
- [scripts/freeze_semantic_v3_evaluator.py:5](../../../../scripts/freeze_semantic_v3_evaluator.py#L5) imports `importlib.util`.
- [scripts/freeze_semantic_v3_evaluator.py:6](../../../../scripts/freeze_semantic_v3_evaluator.py#L6) imports `inspect`.
- [scripts/freeze_semantic_v3_evaluator.py:7](../../../../scripts/freeze_semantic_v3_evaluator.py#L7) imports `json`.
- [scripts/freeze_semantic_v3_evaluator.py:8](../../../../scripts/freeze_semantic_v3_evaluator.py#L8) imports `subprocess`.
- [scripts/freeze_semantic_v3_evaluator.py:9](../../../../scripts/freeze_semantic_v3_evaluator.py#L9) imports `urllib.request`.
- [scripts/freeze_semantic_v3_evaluator.py:10](../../../../scripts/freeze_semantic_v3_evaluator.py#L10) imports `datetime` / datetime.
- [scripts/freeze_semantic_v3_evaluator.py:10](../../../../scripts/freeze_semantic_v3_evaluator.py#L10) imports `datetime` / timezone.
- [scripts/freeze_semantic_v3_evaluator.py:11](../../../../scripts/freeze_semantic_v3_evaluator.py#L11) imports `pathlib` / Path.
- [scripts/freeze_semantic_v3_evaluator.py:12](../../../../scripts/freeze_semantic_v3_evaluator.py#L12) imports `typing` / Any.
- [scripts/freeze_semantic_v3_evaluator.py:14](../../../../scripts/freeze_semantic_v3_evaluator.py#L14) imports `mind01.annotation_v3` / annotation_schema.
- [scripts/freeze_semantic_v3_evaluator.py:14](../../../../scripts/freeze_semantic_v3_evaluator.py#L14) imports `mind01.annotation_v3` / derive_policy_constraints.

## Symbols

### `scripts.freeze_semantic_v3_evaluator.ROOT` — lines 17–17

- Source: [scripts/freeze_semantic_v3_evaluator.py:17](../../../../scripts/freeze_semantic_v3_evaluator.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.EXPECTED_MODEL` — lines 18–18

- Source: [scripts/freeze_semantic_v3_evaluator.py:18](../../../../scripts/freeze_semantic_v3_evaluator.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.EXPECTED_DIGEST` — lines 19–19

- Source: [scripts/freeze_semantic_v3_evaluator.py:19](../../../../scripts/freeze_semantic_v3_evaluator.py#L19)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.EXPECTED_OLLAMA_VERSION` — lines 20–20

- Source: [scripts/freeze_semantic_v3_evaluator.py:20](../../../../scripts/freeze_semantic_v3_evaluator.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.OLLAMA_URL` — lines 21–21

- Source: [scripts/freeze_semantic_v3_evaluator.py:21](../../../../scripts/freeze_semantic_v3_evaluator.py#L21)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.main` — lines 24–102

- Source: [scripts/freeze_semantic_v3_evaluator.py:24](../../../../scripts/freeze_semantic_v3_evaluator.py#L24)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `RuntimeError`, `add_argument`, `annotation_schema`, `assert_passing_calibration`, `derive_policy_constraints`, `digest_json`, `dumps`, `getsource`, `git`, `isoformat`, `live_model_identity`, `load`, `load_runner`, `mkdir`, `now`, `parse_args`, `print`, `read_bytes`, `relative_to`, `resolve`, `sha256_bytes`, `sha256_text`, `str`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.assert_passing_calibration` — lines 105–114

- Source: [scripts/freeze_semantic_v3_evaluator.py:105](../../../../scripts/freeze_semantic_v3_evaluator.py#L105)
- Type: function
- Signature: `report: dict[str, Any]`
- Direct static callees: `RuntimeError`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.live_model_identity` — lines 117–136

- Source: [scripts/freeze_semantic_v3_evaluator.py:117](../../../../scripts/freeze_semantic_v3_evaluator.py#L117)
- Type: function
- Signature: `timeout: int`
- Direct static callees: `get`, `get_json`, `next`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.get_json` — lines 139–145

- Source: [scripts/freeze_semantic_v3_evaluator.py:139](../../../../scripts/freeze_semantic_v3_evaluator.py#L139)
- Type: function
- Signature: `endpoint: str, timeout: int`
- Direct static callees: `Request`, `RuntimeError`, `decode`, `isinstance`, `loads`, `read`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.load_runner` — lines 148–155

- Source: [scripts/freeze_semantic_v3_evaluator.py:148](../../../../scripts/freeze_semantic_v3_evaluator.py#L148)
- Type: function
- Signature: `n/a`
- Direct static callees: `RuntimeError`, `exec_module`, `module_from_spec`, `spec_from_file_location`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.git` — lines 158–159

- Source: [scripts/freeze_semantic_v3_evaluator.py:158](../../../../scripts/freeze_semantic_v3_evaluator.py#L158)
- Type: function
- Signature: `*args: str`
- Direct static callees: `check_output`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.load` — lines 162–166

- Source: [scripts/freeze_semantic_v3_evaluator.py:162](../../../../scripts/freeze_semantic_v3_evaluator.py#L162)
- Type: function
- Signature: `path: Path`
- Direct static callees: `RuntimeError`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.digest_json` — lines 169–170

- Source: [scripts/freeze_semantic_v3_evaluator.py:169](../../../../scripts/freeze_semantic_v3_evaluator.py#L169)
- Type: function
- Signature: `value: Any`
- Direct static callees: `dumps`, `sha256_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.sha256_text` — lines 173–174

- Source: [scripts/freeze_semantic_v3_evaluator.py:173](../../../../scripts/freeze_semantic_v3_evaluator.py#L173)
- Type: function
- Signature: `value: str`
- Direct static callees: `encode`, `sha256_bytes`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.sha256_bytes` — lines 177–178

- Source: [scripts/freeze_semantic_v3_evaluator.py:177](../../../../scripts/freeze_semantic_v3_evaluator.py#L177)
- Type: function
- Signature: `value: bytes`
- Direct static callees: `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_v3_evaluator.write_json` — lines 181–184

- Source: [scripts/freeze_semantic_v3_evaluator.py:181](../../../../scripts/freeze_semantic_v3_evaluator.py#L181)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `dumps`, `replace`, `with_suffix`, `write_text`
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

### Lines 22–23

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 24–53

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, add_argument, annotation_schema, assert_passing_calibration, derive_policy_constraints, digest_json, dumps, getsource, git, isoformat, live_model_identity, load, load_runner, mkdir, now, parse_args, print, read_bytes, relative_to, resolve, sha256_bytes, sha256_text, str, write_json.

### Lines 54–83

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, add_argument, annotation_schema, assert_passing_calibration, derive_policy_constraints, digest_json, dumps, getsource, git, isoformat, live_model_identity, load, load_runner, mkdir, now, parse_args, print, read_bytes, relative_to, resolve, sha256_bytes, sha256_text, str, write_json.

### Lines 84–102

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, add_argument, annotation_schema, assert_passing_calibration, derive_policy_constraints, digest_json, dumps, getsource, git, isoformat, live_model_identity, load, load_runner, mkdir, now, parse_args, print, read_bytes, relative_to, resolve, sha256_bytes, sha256_text, str, write_json.

### Lines 103–104

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 105–114

Defines `assert_passing_calibration` and its implementation control flow; direct static calls: RuntimeError, get.

### Lines 115–116

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 117–136

Defines `live_model_identity` and its implementation control flow; direct static calls: get, get_json, next.

### Lines 137–138

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 139–145

Defines `get_json` and its implementation control flow; direct static calls: Request, RuntimeError, decode, isinstance, loads, read, urlopen.

### Lines 146–147

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 148–155

Defines `load_runner` and its implementation control flow; direct static calls: RuntimeError, exec_module, module_from_spec, spec_from_file_location.

### Lines 156–157

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 158–159

Defines `git` and its implementation control flow; direct static calls: check_output, strip.

### Lines 160–161

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 162–166

Defines `load` and its implementation control flow; direct static calls: RuntimeError, isinstance, loads, read_text.

### Lines 167–168

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 169–170

Defines `digest_json` and its implementation control flow; direct static calls: dumps, sha256_text.

### Lines 171–172

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 173–174

Defines `sha256_text` and its implementation control flow; direct static calls: encode, sha256_bytes.

### Lines 175–176

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 177–178

Defines `sha256_bytes` and its implementation control flow; direct static calls: hexdigest, sha256.

### Lines 179–180

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 181–184

Defines `write_json` and its implementation control flow; direct static calls: dumps, replace, with_suffix, write_text.

### Lines 185–186

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 187–188

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
