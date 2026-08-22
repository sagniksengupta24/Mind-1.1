# `mind01/semantic_live_eval_v2.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `f64619b6bb54f4018528c0a744940d2057abc665a1fedcd4f700517d1504747c`. It contains 255 lines.

## Imports and module state

- [mind01/semantic_live_eval_v2.py:1](../../../../mind01/semantic_live_eval_v2.py#L1) imports `__future__` / annotations.
- [mind01/semantic_live_eval_v2.py:3](../../../../mind01/semantic_live_eval_v2.py#L3) imports `hashlib`.
- [mind01/semantic_live_eval_v2.py:4](../../../../mind01/semantic_live_eval_v2.py#L4) imports `json`.
- [mind01/semantic_live_eval_v2.py:5](../../../../mind01/semantic_live_eval_v2.py#L5) imports `platform`.
- [mind01/semantic_live_eval_v2.py:6](../../../../mind01/semantic_live_eval_v2.py#L6) imports `statistics`.
- [mind01/semantic_live_eval_v2.py:7](../../../../mind01/semantic_live_eval_v2.py#L7) imports `time`.
- [mind01/semantic_live_eval_v2.py:8](../../../../mind01/semantic_live_eval_v2.py#L8) imports `collections` / Counter.
- [mind01/semantic_live_eval_v2.py:9](../../../../mind01/semantic_live_eval_v2.py#L9) imports `datetime` / datetime.
- [mind01/semantic_live_eval_v2.py:9](../../../../mind01/semantic_live_eval_v2.py#L9) imports `datetime` / timezone.
- [mind01/semantic_live_eval_v2.py:10](../../../../mind01/semantic_live_eval_v2.py#L10) imports `pathlib` / Path.
- [mind01/semantic_live_eval_v2.py:11](../../../../mind01/semantic_live_eval_v2.py#L11) imports `typing` / Any.
- [mind01/semantic_live_eval_v2.py:13](../../../../mind01/semantic_live_eval_v2.py#L13) imports `action_parser` / ResponseMode.
- [mind01/semantic_live_eval_v2.py:13](../../../../mind01/semantic_live_eval_v2.py#L13) imports `action_parser` / canonical_response_schema.
- [mind01/semantic_live_eval_v2.py:13](../../../../mind01/semantic_live_eval_v2.py#L13) imports `action_parser` / parse_action_output.
- [mind01/semantic_live_eval_v2.py:14](../../../../mind01/semantic_live_eval_v2.py#L14) imports `intent` / Capability.
- [mind01/semantic_live_eval_v2.py:15](../../../../mind01/semantic_live_eval_v2.py#L15) imports `llm` / LLMError.
- [mind01/semantic_live_eval_v2.py:15](../../../../mind01/semantic_live_eval_v2.py#L15) imports `llm` / OllamaClient.
- [mind01/semantic_live_eval_v2.py:16](../../../../mind01/semantic_live_eval_v2.py#L16) imports `modes` / parse_agent_mode.
- [mind01/semantic_live_eval_v2.py:17](../../../../mind01/semantic_live_eval_v2.py#L17) imports `prompts` / SYSTEM_PROMPT.
- [mind01/semantic_live_eval_v2.py:17](../../../../mind01/semantic_live_eval_v2.py#L17) imports `prompts` / build_action_instruction.
- [mind01/semantic_live_eval_v2.py:18](../../../../mind01/semantic_live_eval_v2.py#L18) imports `routing` / HierarchicalRouter.
- [mind01/semantic_live_eval_v2.py:18](../../../../mind01/semantic_live_eval_v2.py#L18) imports `routing` / ToolFamily.
- [mind01/semantic_live_eval_v2.py:19](../../../../mind01/semantic_live_eval_v2.py#L19) imports `semantic_eval_v2` / SUITE.
- [mind01/semantic_live_eval_v2.py:19](../../../../mind01/semantic_live_eval_v2.py#L19) imports `semantic_eval_v2` / _immediate_family.
- [mind01/semantic_live_eval_v2.py:19](../../../../mind01/semantic_live_eval_v2.py#L19) imports `semantic_eval_v2` / load_v2_partition.
- [mind01/semantic_live_eval_v2.py:19](../../../../mind01/semantic_live_eval_v2.py#L19) imports `semantic_eval_v2` / sha256_file.
- [mind01/semantic_live_eval_v2.py:19](../../../../mind01/semantic_live_eval_v2.py#L19) imports `semantic_eval_v2` / validate_semantic_routing_v2.
- [mind01/semantic_live_eval_v2.py:20](../../../../mind01/semantic_live_eval_v2.py#L20) imports `tool_exposure` / LifecyclePhase.
- [mind01/semantic_live_eval_v2.py:20](../../../../mind01/semantic_live_eval_v2.py#L20) imports `tool_exposure` / ToolExposureAuthority.
- [mind01/semantic_live_eval_v2.py:20](../../../../mind01/semantic_live_eval_v2.py#L20) imports `tool_exposure` / ToolExposureContext.
- [mind01/semantic_live_eval_v2.py:21](../../../../mind01/semantic_live_eval_v2.py#L21) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/semantic_live_eval_v2.py:22](../../../../mind01/semantic_live_eval_v2.py#L22) imports `version` / __version__.

## Symbols

### `mind01.semantic_live_eval_v2.ROOT` — lines 25–25

- Source: [mind01/semantic_live_eval_v2.py:25](../../../../mind01/semantic_live_eval_v2.py#L25)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2.EXPECTED_MODEL_DIGEST` — lines 26–26

- Source: [mind01/semantic_live_eval_v2.py:26](../../../../mind01/semantic_live_eval_v2.py#L26)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2.run_live_semantic_v2` — lines 29–63

- Source: [mind01/semantic_live_eval_v2.py:29](../../../../mind01/semantic_live_eval_v2.py#L29)
- Type: function
- Signature: `*, partition: str, output: Path, model: str='qwen2.5-coder:7b', ollama_url: str='http://127.0.0.1:11434', seed: int | None=None, timeout_seconds: int=120, max_cases: int | None=None, external_blind_labels: Path | None=None`
- Direct static callees: `HierarchicalRouter`, `LLMError`, `OllamaClient`, `ToolExposureAuthority`, `ValueError`, `_mount_blind_labels`, `_report`, `_run_case`, `_write`, `append`, `get`, `len`, `load_v2_partition`, `model_metadata`, `monotonic`, `validate_semantic_routing_v2`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._run_case` — lines 66–166

- Source: [mind01/semantic_live_eval_v2.py:66](../../../../mind01/semantic_live_eval_v2.py#L66)
- Type: function
- Signature: `client: OllamaClient, router: HierarchicalRouter, authority: ToolExposureAuthority, case: dict[str, Any], metadata: dict[str, Any], *, blind: bool`
- Direct static callees: `_immediate_family`, `_json_hash`, `_phase`, `append`, `bool`, `build`, `build_action_instruction`, `canonical_response_schema`, `chat`, `decide`, `dict`, `encode`, `extend`, `hexdigest`, `is_current_for`, `list`, `parse_action_output`, `parse_agent_mode`, `partition_name`, `range`, `replace`, `route_typed`, `sha256`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._mount_blind_labels` — lines 169–196

- Source: [mind01/semantic_live_eval_v2.py:169](../../../../mind01/semantic_live_eval_v2.py#L169)
- Type: function
- Signature: `path: Path`
- Direct static callees: `ValueError`, `append`, `get`, `is_file`, `len`, `load_v2_partition`, `loads`, `read_text`, `resolve`, `sha256_file`, `with_name`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._phase` — lines 199–210

- Source: [mind01/semantic_live_eval_v2.py:199](../../../../mind01/semantic_live_eval_v2.py#L199)
- Type: function
- Signature: `route: Any`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._report` — lines 213–239

- Source: [mind01/semantic_live_eval_v2.py:213](../../../../mind01/semantic_live_eval_v2.py#L213)
- Type: function
- Signature: `partition: str, results: list[dict[str, Any]], metadata: dict[str, Any], validation: dict[str, Any], label_identity: dict[str, Any] | None, seed: int | None, duration: float, complete: bool`
- Direct static callees: `Counter`, `dict`, `encode`, `fmean`, `hexdigest`, `isoformat`, `items`, `iter`, `len`, `next`, `now`, `platform`, `python_version`, `round`, `sha256`, `sha256_file`, `sorted`, `sum`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2.partition_name` — lines 242–243

- Source: [mind01/semantic_live_eval_v2.py:242](../../../../mind01/semantic_live_eval_v2.py#L242)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._write` — lines 246–250

- Source: [mind01/semantic_live_eval_v2.py:246](../../../../mind01/semantic_live_eval_v2.py#L246)
- Type: function
- Signature: `path: Path, payload: dict[str, Any]`
- Direct static callees: `dumps`, `mkdir`, `replace`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval_v2._json_hash` — lines 253–255

- Source: [mind01/semantic_live_eval_v2.py:253](../../../../mind01/semantic_live_eval_v2.py#L253)
- Type: function
- Signature: `payload: dict[str, Any]`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
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

### Lines 26–26

Implements module-level `Assign` behavior or data.

### Lines 27–28

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 29–58

Defines `run_live_semantic_v2` and its implementation control flow; direct static calls: HierarchicalRouter, LLMError, OllamaClient, ToolExposureAuthority, ValueError, _mount_blind_labels, _report, _run_case, _write, append, get, len, load_v2_partition, model_metadata, monotonic, validate_semantic_routing_v2.

### Lines 59–63

Defines `run_live_semantic_v2` and its implementation control flow; direct static calls: HierarchicalRouter, LLMError, OllamaClient, ToolExposureAuthority, ValueError, _mount_blind_labels, _report, _run_case, _write, append, get, len, load_v2_partition, model_metadata, monotonic, validate_semantic_routing_v2.

### Lines 64–65

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 66–95

Defines `_run_case` and its implementation control flow; direct static calls: _immediate_family, _json_hash, _phase, append, bool, build, build_action_instruction, canonical_response_schema, chat, decide, dict, encode, extend, hexdigest, is_current_for, list, parse_action_output, parse_agent_mode, partition_name, range, replace, route_typed, sha256, to_dict.

### Lines 96–125

Defines `_run_case` and its implementation control flow; direct static calls: _immediate_family, _json_hash, _phase, append, bool, build, build_action_instruction, canonical_response_schema, chat, decide, dict, encode, extend, hexdigest, is_current_for, list, parse_action_output, parse_agent_mode, partition_name, range, replace, route_typed, sha256, to_dict.

### Lines 126–155

Defines `_run_case` and its implementation control flow; direct static calls: _immediate_family, _json_hash, _phase, append, bool, build, build_action_instruction, canonical_response_schema, chat, decide, dict, encode, extend, hexdigest, is_current_for, list, parse_action_output, parse_agent_mode, partition_name, range, replace, route_typed, sha256, to_dict.

### Lines 156–166

Defines `_run_case` and its implementation control flow; direct static calls: _immediate_family, _json_hash, _phase, append, bool, build, build_action_instruction, canonical_response_schema, chat, decide, dict, encode, extend, hexdigest, is_current_for, list, parse_action_output, parse_agent_mode, partition_name, range, replace, route_typed, sha256, to_dict.

### Lines 167–168

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 169–196

Defines `_mount_blind_labels` and its implementation control flow; direct static calls: ValueError, append, get, is_file, len, load_v2_partition, loads, read_text, resolve, sha256_file, with_name.

### Lines 197–198

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 199–210

Defines `_phase` and its implementation control flow; direct static calls: none resolved.

### Lines 211–212

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 213–239

Defines `_report` and its implementation control flow; direct static calls: Counter, dict, encode, fmean, hexdigest, isoformat, items, iter, len, next, now, platform, python_version, round, sha256, sha256_file, sorted, sum, tuple.

### Lines 240–241

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 242–243

Defines `partition_name` and its implementation control flow; direct static calls: str.

### Lines 244–245

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 246–250

Defines `_write` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

### Lines 251–252

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 253–255

Defines `_json_hash` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
