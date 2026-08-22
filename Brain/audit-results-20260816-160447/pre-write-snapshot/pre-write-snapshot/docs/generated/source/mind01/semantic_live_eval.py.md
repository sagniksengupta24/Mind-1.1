# `mind01/semantic_live_eval.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `b5f3df9a78f913731ddd91a9ec1fe01c334b2a756f58419533197c7212524546`. It contains 331 lines.

## Imports and module state

- [mind01/semantic_live_eval.py:1](../../../../mind01/semantic_live_eval.py#L1) imports `__future__` / annotations.
- [mind01/semantic_live_eval.py:3](../../../../mind01/semantic_live_eval.py#L3) imports `hashlib`.
- [mind01/semantic_live_eval.py:4](../../../../mind01/semantic_live_eval.py#L4) imports `json`.
- [mind01/semantic_live_eval.py:5](../../../../mind01/semantic_live_eval.py#L5) imports `platform`.
- [mind01/semantic_live_eval.py:6](../../../../mind01/semantic_live_eval.py#L6) imports `statistics`.
- [mind01/semantic_live_eval.py:7](../../../../mind01/semantic_live_eval.py#L7) imports `time`.
- [mind01/semantic_live_eval.py:8](../../../../mind01/semantic_live_eval.py#L8) imports `collections` / Counter.
- [mind01/semantic_live_eval.py:9](../../../../mind01/semantic_live_eval.py#L9) imports `datetime` / datetime.
- [mind01/semantic_live_eval.py:9](../../../../mind01/semantic_live_eval.py#L9) imports `datetime` / timezone.
- [mind01/semantic_live_eval.py:10](../../../../mind01/semantic_live_eval.py#L10) imports `pathlib` / Path.
- [mind01/semantic_live_eval.py:11](../../../../mind01/semantic_live_eval.py#L11) imports `typing` / Any.
- [mind01/semantic_live_eval.py:13](../../../../mind01/semantic_live_eval.py#L13) imports `action_parser` / ResponseMode.
- [mind01/semantic_live_eval.py:13](../../../../mind01/semantic_live_eval.py#L13) imports `action_parser` / canonical_response_schema.
- [mind01/semantic_live_eval.py:13](../../../../mind01/semantic_live_eval.py#L13) imports `action_parser` / parse_action_output.
- [mind01/semantic_live_eval.py:14](../../../../mind01/semantic_live_eval.py#L14) imports `llm` / LLMError.
- [mind01/semantic_live_eval.py:14](../../../../mind01/semantic_live_eval.py#L14) imports `llm` / OllamaClient.
- [mind01/semantic_live_eval.py:15](../../../../mind01/semantic_live_eval.py#L15) imports `prompts` / SYSTEM_PROMPT.
- [mind01/semantic_live_eval.py:15](../../../../mind01/semantic_live_eval.py#L15) imports `prompts` / build_action_instruction.
- [mind01/semantic_live_eval.py:16](../../../../mind01/semantic_live_eval.py#L16) imports `semantic_eval` / MODE_MAP.
- [mind01/semantic_live_eval.py:16](../../../../mind01/semantic_live_eval.py#L16) imports `semantic_eval` / ROOT.
- [mind01/semantic_live_eval.py:16](../../../../mind01/semantic_live_eval.py#L16) imports `semantic_eval` / load_partition.
- [mind01/semantic_live_eval.py:16](../../../../mind01/semantic_live_eval.py#L16) imports `semantic_eval` / validate_semantic_routing_assets.
- [mind01/semantic_live_eval.py:17](../../../../mind01/semantic_live_eval.py#L17) imports `routing` / HierarchicalRouter.
- [mind01/semantic_live_eval.py:17](../../../../mind01/semantic_live_eval.py#L17) imports `routing` / ToolFamily.
- [mind01/semantic_live_eval.py:18](../../../../mind01/semantic_live_eval.py#L18) imports `tool_exposure` / LifecyclePhase.
- [mind01/semantic_live_eval.py:18](../../../../mind01/semantic_live_eval.py#L18) imports `tool_exposure` / ToolExposureAuthority.
- [mind01/semantic_live_eval.py:18](../../../../mind01/semantic_live_eval.py#L18) imports `tool_exposure` / ToolExposureContext.
- [mind01/semantic_live_eval.py:19](../../../../mind01/semantic_live_eval.py#L19) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/semantic_live_eval.py:20](../../../../mind01/semantic_live_eval.py#L20) imports `version` / __version__.

## Symbols

### `mind01.semantic_live_eval.run_live_semantic_partition` — lines 23–101

- Source: [mind01/semantic_live_eval.py:23](../../../../mind01/semantic_live_eval.py#L23)
- Type: function
- Signature: `*, partition: str, output: Path, model: str='qwen2.5-coder:7b', ollama_url: str='http://127.0.0.1:11434', seed: int | None=None, timeout_seconds: int=120, max_cases: int | None=None`
- Direct static callees: `HierarchicalRouter`, `LLMError`, `OllamaClient`, `ToolExposureAuthority`, `ValueError`, `_build_report`, `_phase`, `_run_live_case`, `_write_json`, `append`, `bool`, `build`, `decide`, `get`, `len`, `load_partition`, `max`, `model_metadata`, `monotonic`, `route_typed`, `to_dict`, `validate_semantic_routing_assets`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval._run_live_case` — lines 104–237

- Source: [mind01/semantic_live_eval.py:104](../../../../mind01/semantic_live_eval.py#L104)
- Type: function
- Signature: `client: OllamaClient, case: dict[str, Any], route: dict[str, Any], intent: dict[str, Any], visible_tools: tuple[str, ...], phase: str, model_metadata: dict[str, Any]`
- Direct static callees: `append`, `bool`, `build_action_instruction`, `canonical_response_schema`, `caps_bool`, `chat`, `encode`, `extend`, `get`, `hexdigest`, `list`, `monotonic`, `parse_action_output`, `range`, `round`, `sha256`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval._build_report` — lines 240–310

- Source: [mind01/semantic_live_eval.py:240](../../../../mind01/semantic_live_eval.py#L240)
- Type: function
- Signature: `*, partition: str, results: list[dict[str, Any]], model_metadata: dict[str, Any], validation: dict[str, Any], seed: int | None, duration_seconds: float, complete: bool`
- Direct static callees: `Counter`, `dict`, `dumps`, `encode`, `fmean`, `get`, `hexdigest`, `int`, `isinstance`, `isoformat`, `items`, `len`, `now`, `platform`, `python_version`, `round`, `sha256`, `sorted`, `str`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval.caps_bool` — lines 313–314

- Source: [mind01/semantic_live_eval.py:313](../../../../mind01/semantic_live_eval.py#L313)
- Type: function
- Signature: `case: dict[str, Any], name: str`
- Direct static callees: `bool`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval._phase` — lines 317–324

- Source: [mind01/semantic_live_eval.py:317](../../../../mind01/semantic_live_eval.py#L317)
- Type: function
- Signature: `tool_family: ToolFamily, response_mode: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_live_eval._write_json` — lines 327–331

- Source: [mind01/semantic_live_eval.py:327](../../../../mind01/semantic_live_eval.py#L327)
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

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–22

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 23–52

Defines `run_live_semantic_partition` and its implementation control flow; direct static calls: HierarchicalRouter, LLMError, OllamaClient, ToolExposureAuthority, ValueError, _build_report, _phase, _run_live_case, _write_json, append, bool, build, decide, get, len, load_partition, max, model_metadata, monotonic, route_typed, to_dict, validate_semantic_routing_assets.

### Lines 53–82

Defines `run_live_semantic_partition` and its implementation control flow; direct static calls: HierarchicalRouter, LLMError, OllamaClient, ToolExposureAuthority, ValueError, _build_report, _phase, _run_live_case, _write_json, append, bool, build, decide, get, len, load_partition, max, model_metadata, monotonic, route_typed, to_dict, validate_semantic_routing_assets.

### Lines 83–101

Defines `run_live_semantic_partition` and its implementation control flow; direct static calls: HierarchicalRouter, LLMError, OllamaClient, ToolExposureAuthority, ValueError, _build_report, _phase, _run_live_case, _write_json, append, bool, build, decide, get, len, load_partition, max, model_metadata, monotonic, route_typed, to_dict, validate_semantic_routing_assets.

### Lines 102–103

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 104–133

Defines `_run_live_case` and its implementation control flow; direct static calls: append, bool, build_action_instruction, canonical_response_schema, caps_bool, chat, encode, extend, get, hexdigest, list, monotonic, parse_action_output, range, round, sha256, to_dict.

### Lines 134–163

Defines `_run_live_case` and its implementation control flow; direct static calls: append, bool, build_action_instruction, canonical_response_schema, caps_bool, chat, encode, extend, get, hexdigest, list, monotonic, parse_action_output, range, round, sha256, to_dict.

### Lines 164–193

Defines `_run_live_case` and its implementation control flow; direct static calls: append, bool, build_action_instruction, canonical_response_schema, caps_bool, chat, encode, extend, get, hexdigest, list, monotonic, parse_action_output, range, round, sha256, to_dict.

### Lines 194–223

Defines `_run_live_case` and its implementation control flow; direct static calls: append, bool, build_action_instruction, canonical_response_schema, caps_bool, chat, encode, extend, get, hexdigest, list, monotonic, parse_action_output, range, round, sha256, to_dict.

### Lines 224–237

Defines `_run_live_case` and its implementation control flow; direct static calls: append, bool, build_action_instruction, canonical_response_schema, caps_bool, chat, encode, extend, get, hexdigest, list, monotonic, parse_action_output, range, round, sha256, to_dict.

### Lines 238–239

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 240–269

Defines `_build_report` and its implementation control flow; direct static calls: Counter, dict, dumps, encode, fmean, get, hexdigest, int, isinstance, isoformat, items, len, now, platform, python_version, round, sha256, sorted, str, sum.

### Lines 270–299

Defines `_build_report` and its implementation control flow; direct static calls: Counter, dict, dumps, encode, fmean, get, hexdigest, int, isinstance, isoformat, items, len, now, platform, python_version, round, sha256, sorted, str, sum.

### Lines 300–310

Defines `_build_report` and its implementation control flow; direct static calls: Counter, dict, dumps, encode, fmean, get, hexdigest, int, isinstance, isoformat, items, len, now, platform, python_version, round, sha256, sorted, str, sum.

### Lines 311–312

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 313–314

Defines `caps_bool` and its implementation control flow; direct static calls: bool, get.

### Lines 315–316

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 317–324

Defines `_phase` and its implementation control flow; direct static calls: none resolved.

### Lines 325–326

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 327–331

Defines `_write_json` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
