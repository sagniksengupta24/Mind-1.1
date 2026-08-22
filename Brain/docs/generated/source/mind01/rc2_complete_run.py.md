# `mind01/rc2_complete_run.py`

## File purpose

This agent runtime file is reviewed at snapshot `3fd6c2aef2a30364924e99959d106fe603c79231783e1c1039e988ba52360190`. It contains 271 lines.

## Imports and module state

- [mind01/rc2_complete_run.py:1](../../../../mind01/rc2_complete_run.py#L1) imports `__future__` / annotations.
- [mind01/rc2_complete_run.py:3](../../../../mind01/rc2_complete_run.py#L3) imports `hashlib`.
- [mind01/rc2_complete_run.py:4](../../../../mind01/rc2_complete_run.py#L4) imports `json`.
- [mind01/rc2_complete_run.py:5](../../../../mind01/rc2_complete_run.py#L5) imports `os`.
- [mind01/rc2_complete_run.py:6](../../../../mind01/rc2_complete_run.py#L6) imports `stat`.
- [mind01/rc2_complete_run.py:7](../../../../mind01/rc2_complete_run.py#L7) imports `subprocess`.
- [mind01/rc2_complete_run.py:8](../../../../mind01/rc2_complete_run.py#L8) imports `time`.
- [mind01/rc2_complete_run.py:9](../../../../mind01/rc2_complete_run.py#L9) imports `datetime` / datetime.
- [mind01/rc2_complete_run.py:9](../../../../mind01/rc2_complete_run.py#L9) imports `datetime` / timezone.
- [mind01/rc2_complete_run.py:10](../../../../mind01/rc2_complete_run.py#L10) imports `pathlib` / Path.
- [mind01/rc2_complete_run.py:11](../../../../mind01/rc2_complete_run.py#L11) imports `typing` / Any.
- [mind01/rc2_complete_run.py:13](../../../../mind01/rc2_complete_run.py#L13) imports `end_to_end_eval` / run_live_end_to_end.
- [mind01/rc2_complete_run.py:14](../../../../mind01/rc2_complete_run.py#L14) imports `prompts` / SYSTEM_PROMPT.
- [mind01/rc2_complete_run.py:15](../../../../mind01/rc2_complete_run.py#L15) imports `semantic_eval_v2` / SUITE.
- [mind01/rc2_complete_run.py:15](../../../../mind01/rc2_complete_run.py#L15) imports `semantic_eval_v2` / sha256_file.
- [mind01/rc2_complete_run.py:15](../../../../mind01/rc2_complete_run.py#L15) imports `semantic_eval_v2` / validate_semantic_routing_v2.
- [mind01/rc2_complete_run.py:16](../../../../mind01/rc2_complete_run.py#L16) imports `semantic_live_eval_v2` / EXPECTED_MODEL_DIGEST.
- [mind01/rc2_complete_run.py:16](../../../../mind01/rc2_complete_run.py#L16) imports `semantic_live_eval_v2` / run_live_semantic_v2.
- [mind01/rc2_complete_run.py:17](../../../../mind01/rc2_complete_run.py#L17) imports `truthful_eval` / run_truthful_completion_regression.
- [mind01/rc2_complete_run.py:18](../../../../mind01/rc2_complete_run.py#L18) imports `version` / __version__.

## Symbols

### `mind01.rc2_complete_run.ROOT` — lines 21–21

- Source: [mind01/rc2_complete_run.py:21](../../../../mind01/rc2_complete_run.py#L21)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run.VISIBLE_PARTITIONS` — lines 22–29

- Source: [mind01/rc2_complete_run.py:22](../../../../mind01/rc2_complete_run.py#L22)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run.EVALUATOR_VERSION` — lines 30–30

- Source: [mind01/rc2_complete_run.py:30](../../../../mind01/rc2_complete_run.py#L30)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run.run_rc2_complete_live` — lines 33–133

- Source: [mind01/rc2_complete_run.py:33](../../../../mind01/rc2_complete_run.py#L33)
- Type: function
- Signature: `*, output_root: Path, run_name: str, seed: int, external_blind_labels: Path, model: str='qwen2.5-coder:7b', ollama_url: str='http://127.0.0.1:11434', timeout_seconds: int=180`
- Direct static callees: `_aggregate`, `_component`, `_release_identity`, `_require_consistent_model_identity`, `_require_external_read_only_labels`, `_require_frozen_source`, `_require_same_frozen_source`, `_write`, `all`, `evaluate_run_gates`, `isoformat`, `monotonic`, `now`, `resolve`, `round`, `run_live_end_to_end`, `run_live_semantic_v2`, `run_truthful_completion_regression`, `type`, `update`, `validate_semantic_routing_v2`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run.evaluate_run_gates` — lines 136–175

- Source: [mind01/rc2_complete_run.py:136](../../../../mind01/rc2_complete_run.py#L136)
- Type: function
- Signature: `reports: dict[str, dict[str, Any]]`
- Direct static callees: `all`, `get`, `sum`, `weighted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._aggregate` — lines 178–186

- Source: [mind01/rc2_complete_run.py:178](../../../../mind01/rc2_complete_run.py#L178)
- Type: function
- Signature: `reports: dict[str, dict[str, Any]]`
- Direct static callees: `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._release_identity` — lines 189–211

- Source: [mind01/rc2_complete_run.py:189](../../../../mind01/rc2_complete_run.py#L189)
- Type: function
- Signature: `validation: dict[str, Any]`
- Direct static callees: `_git`, `encode`, `hexdigest`, `sha256`, `sha256_file`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._require_consistent_model_identity` — lines 214–223

- Source: [mind01/rc2_complete_run.py:214](../../../../mind01/rc2_complete_run.py#L214)
- Type: function
- Signature: `reports: dict[str, dict[str, Any]], seed: int`
- Direct static callees: `ValueError`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._require_external_read_only_labels` — lines 226–233

- Source: [mind01/rc2_complete_run.py:226](../../../../mind01/rc2_complete_run.py#L226)
- Type: function
- Signature: `path: Path`
- Direct static callees: `S_IMODE`, `ValueError`, `is_file`, `stat`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._require_frozen_source` — lines 236–238

- Source: [mind01/rc2_complete_run.py:236](../../../../mind01/rc2_complete_run.py#L236)
- Type: function
- Signature: `n/a`
- Direct static callees: `ValueError`, `_git`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._require_same_frozen_source` — lines 241–244

- Source: [mind01/rc2_complete_run.py:241](../../../../mind01/rc2_complete_run.py#L241)
- Type: function
- Signature: `commit: str`
- Direct static callees: `ValueError`, `_git`, `_require_frozen_source`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._git` — lines 247–256

- Source: [mind01/rc2_complete_run.py:247](../../../../mind01/rc2_complete_run.py#L247)
- Type: function
- Signature: `*args: str`
- Direct static callees: `run`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._component` — lines 259–264

- Source: [mind01/rc2_complete_run.py:259](../../../../mind01/rc2_complete_run.py#L259)
- Type: function
- Signature: `path: Path, report: dict[str, Any]`
- Direct static callees: `bool`, `get`, `relative_to`, `resolve`, `sha256_file`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.rc2_complete_run._write` — lines 267–271

- Source: [mind01/rc2_complete_run.py:267](../../../../mind01/rc2_complete_run.py#L267)
- Type: function
- Signature: `path: Path, payload: dict[str, Any]`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–21

Implements module-level `Assign` behavior or data.

### Lines 22–29

Implements module-level `Assign` behavior or data.

### Lines 30–30

Implements module-level `Assign` behavior or data.

### Lines 31–32

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 33–62

Defines `run_rc2_complete_live` and its implementation control flow; direct static calls: _aggregate, _component, _release_identity, _require_consistent_model_identity, _require_external_read_only_labels, _require_frozen_source, _require_same_frozen_source, _write, all, evaluate_run_gates, isoformat, monotonic, now, resolve, round, run_live_end_to_end, run_live_semantic_v2, run_truthful_completion_regression, type, update, validate_semantic_routing_v2, values.

### Lines 63–92

Defines `run_rc2_complete_live` and its implementation control flow; direct static calls: _aggregate, _component, _release_identity, _require_consistent_model_identity, _require_external_read_only_labels, _require_frozen_source, _require_same_frozen_source, _write, all, evaluate_run_gates, isoformat, monotonic, now, resolve, round, run_live_end_to_end, run_live_semantic_v2, run_truthful_completion_regression, type, update, validate_semantic_routing_v2, values.

### Lines 93–122

Defines `run_rc2_complete_live` and its implementation control flow; direct static calls: _aggregate, _component, _release_identity, _require_consistent_model_identity, _require_external_read_only_labels, _require_frozen_source, _require_same_frozen_source, _write, all, evaluate_run_gates, isoformat, monotonic, now, resolve, round, run_live_end_to_end, run_live_semantic_v2, run_truthful_completion_regression, type, update, validate_semantic_routing_v2, values.

### Lines 123–133

Defines `run_rc2_complete_live` and its implementation control flow; direct static calls: _aggregate, _component, _release_identity, _require_consistent_model_identity, _require_external_read_only_labels, _require_frozen_source, _require_same_frozen_source, _write, all, evaluate_run_gates, isoformat, monotonic, now, resolve, round, run_live_end_to_end, run_live_semantic_v2, run_truthful_completion_regression, type, update, validate_semantic_routing_v2, values.

### Lines 134–135

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 136–165

Defines `evaluate_run_gates` and its implementation control flow; direct static calls: all, get, sum, weighted.

### Lines 166–175

Defines `evaluate_run_gates` and its implementation control flow; direct static calls: all, get, sum, weighted.

### Lines 176–177

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 178–186

Defines `_aggregate` and its implementation control flow; direct static calls: sum.

### Lines 187–188

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 189–211

Defines `_release_identity` and its implementation control flow; direct static calls: _git, encode, hexdigest, sha256, sha256_file.

### Lines 212–213

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 214–223

Defines `_require_consistent_model_identity` and its implementation control flow; direct static calls: ValueError, get.

### Lines 224–225

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 226–233

Defines `_require_external_read_only_labels` and its implementation control flow; direct static calls: S_IMODE, ValueError, is_file, stat.

### Lines 234–235

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 236–238

Defines `_require_frozen_source` and its implementation control flow; direct static calls: ValueError, _git.

### Lines 239–240

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 241–244

Defines `_require_same_frozen_source` and its implementation control flow; direct static calls: ValueError, _git, _require_frozen_source.

### Lines 245–246

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 247–256

Defines `_git` and its implementation control flow; direct static calls: run, strip.

### Lines 257–258

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 259–264

Defines `_component` and its implementation control flow; direct static calls: bool, get, relative_to, resolve, sha256_file, str.

### Lines 265–266

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 267–271

Defines `_write` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
