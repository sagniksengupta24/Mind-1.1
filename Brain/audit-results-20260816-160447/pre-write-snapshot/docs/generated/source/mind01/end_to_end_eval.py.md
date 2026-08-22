# `mind01/end_to_end_eval.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `851069b2777b3766c4ad67c499d10cc7be38a31f55268ff9add40e01898ef1c3`. It contains 294 lines.

## Imports and module state

- [mind01/end_to_end_eval.py:1](../../../../mind01/end_to_end_eval.py#L1) imports `__future__` / annotations.
- [mind01/end_to_end_eval.py:3](../../../../mind01/end_to_end_eval.py#L3) imports `hashlib`.
- [mind01/end_to_end_eval.py:4](../../../../mind01/end_to_end_eval.py#L4) imports `json`.
- [mind01/end_to_end_eval.py:5](../../../../mind01/end_to_end_eval.py#L5) imports `platform`.
- [mind01/end_to_end_eval.py:6](../../../../mind01/end_to_end_eval.py#L6) imports `shutil`.
- [mind01/end_to_end_eval.py:7](../../../../mind01/end_to_end_eval.py#L7) imports `statistics`.
- [mind01/end_to_end_eval.py:8](../../../../mind01/end_to_end_eval.py#L8) imports `tempfile`.
- [mind01/end_to_end_eval.py:9](../../../../mind01/end_to_end_eval.py#L9) imports `time`.
- [mind01/end_to_end_eval.py:10](../../../../mind01/end_to_end_eval.py#L10) imports `datetime` / datetime.
- [mind01/end_to_end_eval.py:10](../../../../mind01/end_to_end_eval.py#L10) imports `datetime` / timezone.
- [mind01/end_to_end_eval.py:11](../../../../mind01/end_to_end_eval.py#L11) imports `pathlib` / Path.
- [mind01/end_to_end_eval.py:12](../../../../mind01/end_to_end_eval.py#L12) imports `typing` / Any.
- [mind01/end_to_end_eval.py:14](../../../../mind01/end_to_end_eval.py#L14) imports `action_parser` / ResponseMode.
- [mind01/end_to_end_eval.py:14](../../../../mind01/end_to_end_eval.py#L14) imports `action_parser` / canonical_response_schema.
- [mind01/end_to_end_eval.py:14](../../../../mind01/end_to_end_eval.py#L14) imports `action_parser` / parse_action_output.
- [mind01/end_to_end_eval.py:15](../../../../mind01/end_to_end_eval.py#L15) imports `llm` / LLMError.
- [mind01/end_to_end_eval.py:15](../../../../mind01/end_to_end_eval.py#L15) imports `llm` / OllamaClient.
- [mind01/end_to_end_eval.py:16](../../../../mind01/end_to_end_eval.py#L16) imports `prompts` / SYSTEM_PROMPT.
- [mind01/end_to_end_eval.py:16](../../../../mind01/end_to_end_eval.py#L16) imports `prompts` / build_action_instruction.
- [mind01/end_to_end_eval.py:17](../../../../mind01/end_to_end_eval.py#L17) imports `routed_execution` / DispatchAuthorizationError.
- [mind01/end_to_end_eval.py:17](../../../../mind01/end_to_end_eval.py#L17) imports `routed_execution` / RoutedExecutionSession.
- [mind01/end_to_end_eval.py:18](../../../../mind01/end_to_end_eval.py#L18) imports `semantic_eval_v2` / SUITE.
- [mind01/end_to_end_eval.py:18](../../../../mind01/end_to_end_eval.py#L18) imports `semantic_eval_v2` / load_v2_partition.
- [mind01/end_to_end_eval.py:18](../../../../mind01/end_to_end_eval.py#L18) imports `semantic_eval_v2` / validate_semantic_routing_v2.
- [mind01/end_to_end_eval.py:19](../../../../mind01/end_to_end_eval.py#L19) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/end_to_end_eval.py:20](../../../../mind01/end_to_end_eval.py#L20) imports `tool_exposure` / StaleRouteError.
- [mind01/end_to_end_eval.py:21](../../../../mind01/end_to_end_eval.py#L21) imports `tools.verify_tools` / ToolError.
- [mind01/end_to_end_eval.py:22](../../../../mind01/end_to_end_eval.py#L22) imports `version` / __version__.

## Symbols

### `mind01.end_to_end_eval.EXPECTED_MODEL_DIGEST` — lines 25–25

- Source: [mind01/end_to_end_eval.py:25](../../../../mind01/end_to_end_eval.py#L25)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval.run_live_end_to_end` — lines 28–51

- Source: [mind01/end_to_end_eval.py:28](../../../../mind01/end_to_end_eval.py#L28)
- Type: function
- Signature: `*, output: Path, model: str='qwen2.5-coder:7b', ollama_url: str='http://127.0.0.1:11434', seed: int | None=None, timeout_seconds: int=120, max_cases: int | None=None`
- Direct static callees: `LLMError`, `OllamaClient`, `_report`, `_run_case`, `_write`, `append`, `get`, `len`, `load_v2_partition`, `model_metadata`, `monotonic`, `validate_semantic_routing_v2`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._run_case` — lines 54–215

- Source: [mind01/end_to_end_eval.py:54](../../../../mind01/end_to_end_eval.py#L54)
- Type: function
- Signature: `client: OllamaClient, case: dict[str, Any], metadata: dict[str, Any]`
- Direct static callees: `Path`, `RoutedExecutionSession`, `TemporaryDirectory`, `_compiles`, `_json_hash`, `_sole_python_target`, `all`, `any`, `append`, `bool`, `build_action_instruction`, `canonical_response_schema`, `chat`, `copytree`, `dict`, `dispatch`, `encode`, `exists`, `extend`, `hexdigest`, `is_file`, `len`, `list`, `max`, `parse_action_output`, `range`, `read_bytes`, `relative_to`, `replace`, `rglob`, `route`, `sha256`, `sorted`, `str`, `to_dict`, `type`, `zip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._report` — lines 218–257

- Source: [mind01/end_to_end_eval.py:218](../../../../mind01/end_to_end_eval.py#L218)
- Type: function
- Signature: `results: list[dict[str, Any]], metadata: dict[str, Any], validation: dict[str, Any], seed: int | None, duration: float, complete: bool`
- Direct static callees: `Path`, `_file_hash`, `any`, `bool`, `encode`, `fmean`, `hexdigest`, `isoformat`, `len`, `now`, `platform`, `python_version`, `rate`, `round`, `sha256`, `sum`, `with_name`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._compiles` — lines 260–265

- Source: [mind01/end_to_end_eval.py:260](../../../../mind01/end_to_end_eval.py#L260)
- Type: function
- Signature: `path: Path`
- Direct static callees: `compile`, `read_text`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._write` — lines 268–272

- Source: [mind01/end_to_end_eval.py:268](../../../../mind01/end_to_end_eval.py#L268)
- Type: function
- Signature: `path: Path, payload: dict[str, Any]`
- Direct static callees: `dumps`, `mkdir`, `replace`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._sole_python_target` — lines 275–285

- Source: [mind01/end_to_end_eval.py:275](../../../../mind01/end_to_end_eval.py#L275)
- Type: function
- Signature: `routed: Any, workspace: Path`
- Direct static callees: `Path`, `append`, `fromkeys`, `is_file`, `len`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._json_hash` — lines 288–290

- Source: [mind01/end_to_end_eval.py:288](../../../../mind01/end_to_end_eval.py#L288)
- Type: function
- Signature: `payload: dict[str, Any]`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.end_to_end_eval._file_hash` — lines 293–294

- Source: [mind01/end_to_end_eval.py:293](../../../../mind01/end_to_end_eval.py#L293)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
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

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–21

Imports a dependency used by this module.

### Lines 22–22

Imports a dependency used by this module.

### Lines 23–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–25

Implements module-level `Assign` behavior or data.

### Lines 26–27

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 28–51

Defines `run_live_end_to_end` and its implementation control flow; direct static calls: LLMError, OllamaClient, _report, _run_case, _write, append, get, len, load_v2_partition, model_metadata, monotonic, validate_semantic_routing_v2.

### Lines 52–53

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 54–83

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 84–113

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 114–143

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 144–173

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 174–203

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 204–215

Defines `_run_case` and its implementation control flow; direct static calls: Path, RoutedExecutionSession, TemporaryDirectory, _compiles, _json_hash, _sole_python_target, all, any, append, bool, build_action_instruction, canonical_response_schema, chat, copytree, dict, dispatch, encode, exists, extend, hexdigest, is_file, len, list, max, parse_action_output, range, read_bytes, relative_to, replace, rglob, route, sha256, sorted, str, to_dict, type, zip.

### Lines 216–217

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 218–247

Defines `_report` and its implementation control flow; direct static calls: Path, _file_hash, any, bool, encode, fmean, hexdigest, isoformat, len, now, platform, python_version, rate, round, sha256, sum, with_name.

### Lines 248–257

Defines `_report` and its implementation control flow; direct static calls: Path, _file_hash, any, bool, encode, fmean, hexdigest, isoformat, len, now, platform, python_version, rate, round, sha256, sum, with_name.

### Lines 258–259

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 260–265

Defines `_compiles` and its implementation control flow; direct static calls: compile, read_text, str.

### Lines 266–267

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 268–272

Defines `_write` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

### Lines 273–274

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 275–285

Defines `_sole_python_target` and its implementation control flow; direct static calls: Path, append, fromkeys, is_file, len, tuple.

### Lines 286–287

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 288–290

Defines `_json_hash` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 291–292

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 293–294

Defines `_file_hash` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
