# `mind01/eval.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `79d6ae2b9aa7eafdf3668cdb9e178e2c89d602489e729cb0758f0fc16b42ff8e`. It contains 642 lines.

## Imports and module state

- [mind01/eval.py:1](../../../../mind01/eval.py#L1) imports `__future__` / annotations.
- [mind01/eval.py:3](../../../../mind01/eval.py#L3) imports `contextlib`.
- [mind01/eval.py:4](../../../../mind01/eval.py#L4) imports `argparse`.
- [mind01/eval.py:5](../../../../mind01/eval.py#L5) imports `json`.
- [mind01/eval.py:6](../../../../mind01/eval.py#L6) imports `re`.
- [mind01/eval.py:7](../../../../mind01/eval.py#L7) imports `platform`.
- [mind01/eval.py:8](../../../../mind01/eval.py#L8) imports `signal`.
- [mind01/eval.py:9](../../../../mind01/eval.py#L9) imports `subprocess`.
- [mind01/eval.py:10](../../../../mind01/eval.py#L10) imports `sys`.
- [mind01/eval.py:11](../../../../mind01/eval.py#L11) imports `time`.
- [mind01/eval.py:12](../../../../mind01/eval.py#L12) imports `dataclasses` / dataclass.
- [mind01/eval.py:13](../../../../mind01/eval.py#L13) imports `pathlib` / Path.
- [mind01/eval.py:14](../../../../mind01/eval.py#L14) imports `typing` / Any.
- [mind01/eval.py:16](../../../../mind01/eval.py#L16) imports `agent` / Agent.
- [mind01/eval.py:17](../../../../mind01/eval.py#L17) imports `config` / AgentConfig.
- [mind01/eval.py:18](../../../../mind01/eval.py#L18) imports `version` / __version__.

## Symbols

### `mind01.eval.EvalResult` — lines 22–60

- Source: [mind01/eval.py:22](../../../../mind01/eval.py#L22)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.EvalResult.to_dict` — lines 41–60

- Source: [mind01/eval.py:41](../../../../mind01/eval.py#L41)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.EvalTimeout` — lines 63–64

- Source: [mind01/eval.py:63](../../../../mind01/eval.py#L63)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.run_eval_file` — lines 67–158

- Source: [mind01/eval.py:67](../../../../mind01/eval.py#L67)
- Type: function
- Signature: `config: AgentConfig, eval_file: Path, task_timeout: int | None=120, repair_attempts: int=1`
- Direct static callees: `Agent`, `EvalResult`, `ValueError`, `any`, `append`, `bool`, `enumerate`, `extract_receipt_ids`, `get`, `int`, `isinstance`, `join`, `loads`, `max`, `missing_requirements`, `monotonic`, `read_text`, `run_eval_task`, `str`, `timeout_after`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.render_eval_results` — lines 161–192

- Source: [mind01/eval.py:161](../../../../mind01/eval.py#L161)
- Type: function
- Signature: `results: list[EvalResult]`
- Direct static callees: `append`, `category_summary`, `extend`, `items`, `join`, `len`, `rstrip`, `sorted`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.save_eval_results` — lines 195–204

- Source: [mind01/eval.py:195](../../../../mind01/eval.py#L195)
- Type: function
- Signature: `eval_file: Path, output_file: Path, results: list[EvalResult], config: AgentConfig | None=None`
- Direct static callees: `dumps`, `evaluation_metadata`, `evaluation_summary`, `int`, `mkdir`, `str`, `time`, `to_dict`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.save_eval_run` — lines 207–213

- Source: [mind01/eval.py:207](../../../../mind01/eval.py#L207)
- Type: function
- Signature: `workspace: Path, eval_file: Path, results: list[EvalResult], config: AgentConfig | None=None`
- Direct static callees: `gmtime`, `safe_eval_name`, `save_eval_results`, `strftime`, `time_ns`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.evaluation_summary` — lines 216–233

- Source: [mind01/eval.py:216](../../../../mind01/eval.py#L216)
- Type: function
- Signature: `results: list[EvalResult]`
- Direct static callees: `any`, `category_summary`, `get`, `len`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.evaluation_metadata` — lines 236–267

- Source: [mind01/eval.py:236](../../../../mind01/eval.py#L236)
- Type: function
- Signature: `eval_file: Path, config: AgentConfig | None`
- Direct static callees: `cwd`, `get`, `loads`, `platform`, `read_text`, `run`, `split`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.category_summary` — lines 270–277

- Source: [mind01/eval.py:270](../../../../mind01/eval.py#L270)
- Type: function
- Signature: `results: list[EvalResult]`
- Direct static callees: `setdefault`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.run_eval_task` — lines 280–312

- Source: [mind01/eval.py:280](../../../../mind01/eval.py#L280)
- Type: function
- Signature: `agent: Agent, prompt: str, expected: list[str], groups: list[list[str]], repair_attempts: int`
- Direct static callees: `append`, `ask`, `build_repair_prompt`, `extend`, `missing_requirements`, `range`, `response_matches`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.response_matches` — lines 315–319

- Source: [mind01/eval.py:315](../../../../mind01/eval.py#L315)
- Type: function
- Signature: `response: str, expected: list[str], groups: list[list[str]]`
- Direct static callees: `all`, `any`, `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.missing_requirements` — lines 322–330

- Source: [mind01/eval.py:322](../../../../mind01/eval.py#L322)
- Type: function
- Signature: `response: str, expected: list[str], groups: list[list[str]]`
- Direct static callees: `any`, `append`, `join`, `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.build_repair_prompt` — lines 333–342

- Source: [mind01/eval.py:333](../../../../mind01/eval.py#L333)
- Type: function
- Signature: `original_prompt: str, missing: list[str]`
- Direct static callees: `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.extract_receipt_ids` — lines 345–352

- Source: [mind01/eval.py:345](../../../../mind01/eval.py#L345)
- Type: function
- Signature: `response: str, trace: list[str]`
- Direct static callees: `append`, `finditer`, `group`, `join`, `rstrip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.safe_eval_name` — lines 355–357

- Source: [mind01/eval.py:355](../../../../mind01/eval.py#L355)
- Type: function
- Signature: `name: str`
- Direct static callees: `isalnum`, `join`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.timeout_after` — lines 361–379

- Source: [mind01/eval.py:361](../../../../mind01/eval.py#L361)
- Type: function
- Signature: `seconds: int | None`
- Direct static callees: `EvalTimeout`, `getitimer`, `getsignal`, `setitimer`, `signal`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.main` — lines 382–600

- Source: [mind01/eval.py:382](../../../../mind01/eval.py#L382)
- Type: function
- Signature: `argv: list[str] | None=None`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `add_parser`, `add_subparsers`, `aggregate_parser_report`, `dumps`, `error`, `expanduser`, `mkdir`, `parse_args`, `print`, `resolve`, `run_action_benchmark`, `run_deterministic_semantic_routing`, `run_live_end_to_end`, `run_live_semantic_partition`, `run_live_semantic_v2`, `run_mock_protocol_regression`, `run_rc2_complete_live`, `run_real_mutation_smoke`, `run_truthful_completion_regression`, `str`, `type`, `validate_eval_assets`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval.run_mock_protocol_regression` — lines 603–638

- Source: [mind01/eval.py:603](../../../../mind01/eval.py#L603)
- Type: function
- Signature: `limit: int=25`
- Direct static callees: `append`, `dumps`, `len`, `load_action_suite`, `min`, `parse_action_output`
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

### Lines 15–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–51

Defines class `EvalResult` and the behavior of its members.

### Lines 52–60

Defines class `EvalResult` and the behavior of its members.

### Lines 61–62

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 63–64

Defines class `EvalTimeout` and the behavior of its members.

### Lines 65–66

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 67–96

Defines `run_eval_file` and its implementation control flow; direct static calls: Agent, EvalResult, ValueError, any, append, bool, enumerate, extract_receipt_ids, get, int, isinstance, join, loads, max, missing_requirements, monotonic, read_text, run_eval_task, str, timeout_after, type.

### Lines 97–126

Defines `run_eval_file` and its implementation control flow; direct static calls: Agent, EvalResult, ValueError, any, append, bool, enumerate, extract_receipt_ids, get, int, isinstance, join, loads, max, missing_requirements, monotonic, read_text, run_eval_task, str, timeout_after, type.

### Lines 127–156

Defines `run_eval_file` and its implementation control flow; direct static calls: Agent, EvalResult, ValueError, any, append, bool, enumerate, extract_receipt_ids, get, int, isinstance, join, loads, max, missing_requirements, monotonic, read_text, run_eval_task, str, timeout_after, type.

### Lines 157–158

Defines `run_eval_file` and its implementation control flow; direct static calls: Agent, EvalResult, ValueError, any, append, bool, enumerate, extract_receipt_ids, get, int, isinstance, join, loads, max, missing_requirements, monotonic, read_text, run_eval_task, str, timeout_after, type.

### Lines 159–160

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 161–190

Defines `render_eval_results` and its implementation control flow; direct static calls: append, category_summary, extend, items, join, len, rstrip, sorted, sum.

### Lines 191–192

Defines `render_eval_results` and its implementation control flow; direct static calls: append, category_summary, extend, items, join, len, rstrip, sorted, sum.

### Lines 193–194

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 195–204

Defines `save_eval_results` and its implementation control flow; direct static calls: dumps, evaluation_metadata, evaluation_summary, int, mkdir, str, time, to_dict, write_text.

### Lines 205–206

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 207–213

Defines `save_eval_run` and its implementation control flow; direct static calls: gmtime, safe_eval_name, save_eval_results, strftime, time_ns.

### Lines 214–215

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 216–233

Defines `evaluation_summary` and its implementation control flow; direct static calls: any, category_summary, get, len, sum.

### Lines 234–235

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 236–265

Defines `evaluation_metadata` and its implementation control flow; direct static calls: cwd, get, loads, platform, read_text, run, split, str, strip.

### Lines 266–267

Defines `evaluation_metadata` and its implementation control flow; direct static calls: cwd, get, loads, platform, read_text, run, split, str, strip.

### Lines 268–269

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 270–277

Defines `category_summary` and its implementation control flow; direct static calls: setdefault.

### Lines 278–279

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 280–309

Defines `run_eval_task` and its implementation control flow; direct static calls: append, ask, build_repair_prompt, extend, missing_requirements, range, response_matches.

### Lines 310–312

Defines `run_eval_task` and its implementation control flow; direct static calls: append, ask, build_repair_prompt, extend, missing_requirements, range, response_matches.

### Lines 313–314

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 315–319

Defines `response_matches` and its implementation control flow; direct static calls: all, any, lower.

### Lines 320–321

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 322–330

Defines `missing_requirements` and its implementation control flow; direct static calls: any, append, join, lower.

### Lines 331–332

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 333–342

Defines `build_repair_prompt` and its implementation control flow; direct static calls: join.

### Lines 343–344

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 345–352

Defines `extract_receipt_ids` and its implementation control flow; direct static calls: append, finditer, group, join, rstrip.

### Lines 353–354

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 355–357

Defines `safe_eval_name` and its implementation control flow; direct static calls: isalnum, join, strip.

### Lines 358–360

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 361–379

Defines `timeout_after` and its implementation control flow; direct static calls: EvalTimeout, getitimer, getsignal, setitimer, signal.

### Lines 380–381

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 382–411

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 412–441

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 442–471

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 472–501

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 502–531

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 532–561

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 562–591

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 592–600

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, add_parser, add_subparsers, aggregate_parser_report, dumps, error, expanduser, mkdir, parse_args, print, resolve, run_action_benchmark, run_deterministic_semantic_routing, run_live_end_to_end, run_live_semantic_partition, run_live_semantic_v2, run_mock_protocol_regression, run_rc2_complete_live, run_real_mutation_smoke, run_truthful_completion_regression, str, type, validate_eval_assets, write_text.

### Lines 601–602

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 603–632

Defines `run_mock_protocol_regression` and its implementation control flow; direct static calls: append, dumps, len, load_action_suite, min, parse_action_output.

### Lines 633–638

Defines `run_mock_protocol_regression` and its implementation control flow; direct static calls: append, dumps, len, load_action_suite, min, parse_action_output.

### Lines 639–640

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 641–642

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
