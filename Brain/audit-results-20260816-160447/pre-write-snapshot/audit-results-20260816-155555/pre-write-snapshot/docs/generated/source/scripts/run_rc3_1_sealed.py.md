# `scripts/run_rc3_1_sealed.py`

## File purpose

This automation and release file is reviewed at snapshot `397b25dd1197d5a231cd6161fcf4e918a1d2d7ac0068862d93583f9be681815b`. It contains 276 lines.

## Imports and module state

- [scripts/run_rc3_1_sealed.py:3](../../../../scripts/run_rc3_1_sealed.py#L3) imports `__future__` / annotations.
- [scripts/run_rc3_1_sealed.py:5](../../../../scripts/run_rc3_1_sealed.py#L5) imports `argparse`.
- [scripts/run_rc3_1_sealed.py:6](../../../../scripts/run_rc3_1_sealed.py#L6) imports `hashlib`.
- [scripts/run_rc3_1_sealed.py:7](../../../../scripts/run_rc3_1_sealed.py#L7) imports `json`.
- [scripts/run_rc3_1_sealed.py:8](../../../../scripts/run_rc3_1_sealed.py#L8) imports `platform`.
- [scripts/run_rc3_1_sealed.py:9](../../../../scripts/run_rc3_1_sealed.py#L9) imports `subprocess`.
- [scripts/run_rc3_1_sealed.py:10](../../../../scripts/run_rc3_1_sealed.py#L10) imports `time`.
- [scripts/run_rc3_1_sealed.py:11](../../../../scripts/run_rc3_1_sealed.py#L11) imports `datetime` / datetime.
- [scripts/run_rc3_1_sealed.py:11](../../../../scripts/run_rc3_1_sealed.py#L11) imports `datetime` / timezone.
- [scripts/run_rc3_1_sealed.py:12](../../../../scripts/run_rc3_1_sealed.py#L12) imports `pathlib` / Path.
- [scripts/run_rc3_1_sealed.py:13](../../../../scripts/run_rc3_1_sealed.py#L13) imports `typing` / Any.
- [scripts/run_rc3_1_sealed.py:15](../../../../scripts/run_rc3_1_sealed.py#L15) imports `mind01.action_parser` / ResponseMode.
- [scripts/run_rc3_1_sealed.py:15](../../../../scripts/run_rc3_1_sealed.py#L15) imports `mind01.action_parser` / canonical_response_schema.
- [scripts/run_rc3_1_sealed.py:15](../../../../scripts/run_rc3_1_sealed.py#L15) imports `mind01.action_parser` / parse_action_output.
- [scripts/run_rc3_1_sealed.py:16](../../../../scripts/run_rc3_1_sealed.py#L16) imports `mind01.llm` / LLMError.
- [scripts/run_rc3_1_sealed.py:16](../../../../scripts/run_rc3_1_sealed.py#L16) imports `mind01.llm` / OllamaClient.
- [scripts/run_rc3_1_sealed.py:17](../../../../scripts/run_rc3_1_sealed.py#L17) imports `mind01.modes` / parse_agent_mode.
- [scripts/run_rc3_1_sealed.py:18](../../../../scripts/run_rc3_1_sealed.py#L18) imports `mind01.prompts` / SYSTEM_PROMPT.
- [scripts/run_rc3_1_sealed.py:18](../../../../scripts/run_rc3_1_sealed.py#L18) imports `mind01.prompts` / build_action_instruction.
- [scripts/run_rc3_1_sealed.py:19](../../../../scripts/run_rc3_1_sealed.py#L19) imports `mind01.routing` / HierarchicalRouter.
- [scripts/run_rc3_1_sealed.py:19](../../../../scripts/run_rc3_1_sealed.py#L19) imports `mind01.routing` / ToolFamily.
- [scripts/run_rc3_1_sealed.py:20](../../../../scripts/run_rc3_1_sealed.py#L20) imports `mind01.semantic_eval_v2` / _immediate_family.
- [scripts/run_rc3_1_sealed.py:21](../../../../scripts/run_rc3_1_sealed.py#L21) imports `mind01.tool_exposure` / LifecyclePhase.
- [scripts/run_rc3_1_sealed.py:21](../../../../scripts/run_rc3_1_sealed.py#L21) imports `mind01.tool_exposure` / ToolExposureAuthority.
- [scripts/run_rc3_1_sealed.py:21](../../../../scripts/run_rc3_1_sealed.py#L21) imports `mind01.tool_exposure` / ToolExposureContext.
- [scripts/run_rc3_1_sealed.py:22](../../../../scripts/run_rc3_1_sealed.py#L22) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.
- [scripts/run_rc3_1_sealed.py:23](../../../../scripts/run_rc3_1_sealed.py#L23) imports `mind01.version` / __version__.
- [scripts/run_rc3_1_sealed.py:25](../../../../scripts/run_rc3_1_sealed.py#L25) imports `rc3_1_pipeline` / FREEZE_PATH.
- [scripts/run_rc3_1_sealed.py:25](../../../../scripts/run_rc3_1_sealed.py#L25) imports `rc3_1_pipeline` / load_json.
- [scripts/run_rc3_1_sealed.py:25](../../../../scripts/run_rc3_1_sealed.py#L25) imports `rc3_1_pipeline` / runtime_manifest.
- [scripts/run_rc3_1_sealed.py:25](../../../../scripts/run_rc3_1_sealed.py#L25) imports `rc3_1_pipeline` / digest_json.
- [scripts/run_rc3_1_sealed.py:25](../../../../scripts/run_rc3_1_sealed.py#L25) imports `rc3_1_pipeline` / sha256.

## Symbols

### `scripts.run_rc3_1_sealed.ROOT` — lines 28–28

- Source: [scripts/run_rc3_1_sealed.py:28](../../../../scripts/run_rc3_1_sealed.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.EXPECTED_MODEL_DIGEST` — lines 29–29

- Source: [scripts/run_rc3_1_sealed.py:29](../../../../scripts/run_rc3_1_sealed.py#L29)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.main` — lines 32–56

- Source: [scripts/run_rc3_1_sealed.py:32](../../../../scripts/run_rc3_1_sealed.py#L32)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `dumps`, `parse_args`, `print`, `run_public_inputs`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.run_public_inputs` — lines 59–110

- Source: [scripts/run_rc3_1_sealed.py:59](../../../../scripts/run_rc3_1_sealed.py#L59)
- Type: function
- Signature: `*, public_inputs: Path, seal_manifest: Path, output_dir: Path, model: str, ollama_url: str, seed: int, timeout: int, resume: bool`
- Direct static callees: `FileExistsError`, `HierarchicalRouter`, `LLMError`, `OllamaClient`, `RuntimeError`, `ToolExposureAuthority`, `append`, `digest_json`, `execution_report`, `exists`, `get`, `len`, `list`, `load_json`, `mkdir`, `model_metadata`, `monotonic`, `now`, `resolve`, `run_case`, `runtime_manifest`, `sha256`, `write_atomic`, `write_new_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.run_case` — lines 113–206

- Source: [scripts/run_rc3_1_sealed.py:113](../../../../scripts/run_rc3_1_sealed.py#L113)
- Type: function
- Signature: `client: OllamaClient, router: HierarchicalRouter, authority: ToolExposureAuthority, case: dict[str, Any], metadata: dict[str, Any]`
- Direct static callees: `_immediate_family`, `append`, `bool`, `build`, `build_action_instruction`, `canonical_response_schema`, `casefold`, `chat`, `decide`, `encode`, `extend`, `hexdigest`, `len`, `list`, `parse_action_output`, `parse_agent_mode`, `phase_for`, `range`, `replace`, `route_typed`, `sha256`, `str`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.phase_for` — lines 209–220

- Source: [scripts/run_rc3_1_sealed.py:209](../../../../scripts/run_rc3_1_sealed.py#L209)
- Type: function
- Signature: `route: Any`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.execution_report` — lines 223–251

- Source: [scripts/run_rc3_1_sealed.py:223](../../../../scripts/run_rc3_1_sealed.py#L223)
- Type: function
- Signature: `results: list[dict[str, Any]], metadata: dict[str, Any], public_inputs: Path, seal_manifest: Path, seal: dict[str, Any], freeze: dict[str, Any], model: str, ollama_url: str, seed: int, timeout: int, started_at: str, duration: float`
- Direct static callees: `digest_json`, `git_head`, `len`, `now`, `platform`, `python_version`, `round`, `runtime_manifest`, `sha256`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.write_new_json` — lines 254–257

- Source: [scripts/run_rc3_1_sealed.py:254](../../../../scripts/run_rc3_1_sealed.py#L254)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `FileExistsError`, `exists`, `write_atomic`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.write_atomic` — lines 260–264

- Source: [scripts/run_rc3_1_sealed.py:260](../../../../scripts/run_rc3_1_sealed.py#L260)
- Type: function
- Signature: `path: Path, value: Any`
- Direct static callees: `dumps`, `mkdir`, `replace`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.now` — lines 267–268

- Source: [scripts/run_rc3_1_sealed.py:267](../../../../scripts/run_rc3_1_sealed.py#L267)
- Type: function
- Signature: `n/a`
- Direct static callees: `isoformat`, `now`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.run_rc3_1_sealed.git_head` — lines 271–272

- Source: [scripts/run_rc3_1_sealed.py:271](../../../../scripts/run_rc3_1_sealed.py#L271)
- Type: function
- Signature: `n/a`
- Direct static callees: `check_output`, `strip`
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

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports, comments, declarations, or configuration that establish the following implementation context.

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

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–27

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 28–28

Implements module-level `Assign` behavior or data.

### Lines 29–29

Implements module-level `Assign` behavior or data.

### Lines 30–31

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 32–56

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, dumps, parse_args, print, run_public_inputs.

### Lines 57–58

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 59–88

Defines `run_public_inputs` and its implementation control flow; direct static calls: FileExistsError, HierarchicalRouter, LLMError, OllamaClient, RuntimeError, ToolExposureAuthority, append, digest_json, execution_report, exists, get, len, list, load_json, mkdir, model_metadata, monotonic, now, resolve, run_case, runtime_manifest, sha256, write_atomic, write_new_json.

### Lines 89–110

Defines `run_public_inputs` and its implementation control flow; direct static calls: FileExistsError, HierarchicalRouter, LLMError, OllamaClient, RuntimeError, ToolExposureAuthority, append, digest_json, execution_report, exists, get, len, list, load_json, mkdir, model_metadata, monotonic, now, resolve, run_case, runtime_manifest, sha256, write_atomic, write_new_json.

### Lines 111–112

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 113–142

Defines `run_case` and its implementation control flow; direct static calls: _immediate_family, append, bool, build, build_action_instruction, canonical_response_schema, casefold, chat, decide, encode, extend, hexdigest, len, list, parse_action_output, parse_agent_mode, phase_for, range, replace, route_typed, sha256, str, to_dict.

### Lines 143–172

Defines `run_case` and its implementation control flow; direct static calls: _immediate_family, append, bool, build, build_action_instruction, canonical_response_schema, casefold, chat, decide, encode, extend, hexdigest, len, list, parse_action_output, parse_agent_mode, phase_for, range, replace, route_typed, sha256, str, to_dict.

### Lines 173–202

Defines `run_case` and its implementation control flow; direct static calls: _immediate_family, append, bool, build, build_action_instruction, canonical_response_schema, casefold, chat, decide, encode, extend, hexdigest, len, list, parse_action_output, parse_agent_mode, phase_for, range, replace, route_typed, sha256, str, to_dict.

### Lines 203–206

Defines `run_case` and its implementation control flow; direct static calls: _immediate_family, append, bool, build, build_action_instruction, canonical_response_schema, casefold, chat, decide, encode, extend, hexdigest, len, list, parse_action_output, parse_agent_mode, phase_for, range, replace, route_typed, sha256, str, to_dict.

### Lines 207–208

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 209–220

Defines `phase_for` and its implementation control flow; direct static calls: none resolved.

### Lines 221–222

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 223–251

Defines `execution_report` and its implementation control flow; direct static calls: digest_json, git_head, len, now, platform, python_version, round, runtime_manifest, sha256, sum.

### Lines 252–253

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 254–257

Defines `write_new_json` and its implementation control flow; direct static calls: FileExistsError, exists, write_atomic.

### Lines 258–259

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 260–264

Defines `write_atomic` and its implementation control flow; direct static calls: dumps, mkdir, replace, with_suffix, write_text.

### Lines 265–266

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 267–268

Defines `now` and its implementation control flow; direct static calls: isoformat, now.

### Lines 269–270

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 271–272

Defines `git_head` and its implementation control flow; direct static calls: check_output, strip.

### Lines 273–274

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 275–276

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
