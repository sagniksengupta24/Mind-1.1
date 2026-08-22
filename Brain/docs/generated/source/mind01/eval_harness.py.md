# `mind01/eval_harness.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `b2bf07c407ded585771026bbd165bffeda17cf7a03cdf79fe8a90d2f7eafd674`. It contains 589 lines.

## Imports and module state

- [mind01/eval_harness.py:1](../../../../mind01/eval_harness.py#L1) imports `__future__` / annotations.
- [mind01/eval_harness.py:3](../../../../mind01/eval_harness.py#L3) imports `hashlib`.
- [mind01/eval_harness.py:4](../../../../mind01/eval_harness.py#L4) imports `json`.
- [mind01/eval_harness.py:5](../../../../mind01/eval_harness.py#L5) imports `platform`.
- [mind01/eval_harness.py:6](../../../../mind01/eval_harness.py#L6) imports `shutil`.
- [mind01/eval_harness.py:7](../../../../mind01/eval_harness.py#L7) imports `subprocess`.
- [mind01/eval_harness.py:8](../../../../mind01/eval_harness.py#L8) imports `sys`.
- [mind01/eval_harness.py:9](../../../../mind01/eval_harness.py#L9) imports `tempfile`.
- [mind01/eval_harness.py:10](../../../../mind01/eval_harness.py#L10) imports `time`.
- [mind01/eval_harness.py:11](../../../../mind01/eval_harness.py#L11) imports `uuid`.
- [mind01/eval_harness.py:12](../../../../mind01/eval_harness.py#L12) imports `collections` / Counter.
- [mind01/eval_harness.py:12](../../../../mind01/eval_harness.py#L12) imports `collections` / defaultdict.
- [mind01/eval_harness.py:13](../../../../mind01/eval_harness.py#L13) imports `dataclasses` / asdict.
- [mind01/eval_harness.py:13](../../../../mind01/eval_harness.py#L13) imports `dataclasses` / dataclass.
- [mind01/eval_harness.py:14](../../../../mind01/eval_harness.py#L14) imports `datetime` / datetime.
- [mind01/eval_harness.py:14](../../../../mind01/eval_harness.py#L14) imports `datetime` / timezone.
- [mind01/eval_harness.py:15](../../../../mind01/eval_harness.py#L15) imports `pathlib` / Path.
- [mind01/eval_harness.py:16](../../../../mind01/eval_harness.py#L16) imports `typing` / Any.
- [mind01/eval_harness.py:18](../../../../mind01/eval_harness.py#L18) imports `agent` / Agent.
- [mind01/eval_harness.py:19](../../../../mind01/eval_harness.py#L19) imports `action_parser` / ResponseMode.
- [mind01/eval_harness.py:19](../../../../mind01/eval_harness.py#L19) imports `action_parser` / canonical_response_schema.
- [mind01/eval_harness.py:19](../../../../mind01/eval_harness.py#L19) imports `action_parser` / parse_action_output.
- [mind01/eval_harness.py:20](../../../../mind01/eval_harness.py#L20) imports `completion` / CompletionAuthority.
- [mind01/eval_harness.py:20](../../../../mind01/eval_harness.py#L20) imports `completion` / VerificationEvidence.
- [mind01/eval_harness.py:21](../../../../mind01/eval_harness.py#L21) imports `config` / AgentConfig.
- [mind01/eval_harness.py:22](../../../../mind01/eval_harness.py#L22) imports `eval_schema` / ActionBenchmarkCase.
- [mind01/eval_harness.py:22](../../../../mind01/eval_harness.py#L22) imports `eval_schema` / ActionBenchmarkSuite.
- [mind01/eval_harness.py:22](../../../../mind01/eval_harness.py#L22) imports `eval_schema` / load_action_suite.
- [mind01/eval_harness.py:23](../../../../mind01/eval_harness.py#L23) imports `llm` / LLMError.
- [mind01/eval_harness.py:23](../../../../mind01/eval_harness.py#L23) imports `llm` / OllamaClient.
- [mind01/eval_harness.py:24](../../../../mind01/eval_harness.py#L24) imports `modes` / AgentMode.
- [mind01/eval_harness.py:25](../../../../mind01/eval_harness.py#L25) imports `patch_review` / review_patch.
- [mind01/eval_harness.py:26](../../../../mind01/eval_harness.py#L26) imports `prompts` / SYSTEM_PROMPT.
- [mind01/eval_harness.py:26](../../../../mind01/eval_harness.py#L26) imports `prompts` / build_action_instruction.
- [mind01/eval_harness.py:27](../../../../mind01/eval_harness.py#L27) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/eval_harness.py:28](../../../../mind01/eval_harness.py#L28) imports `version` / __version__.
- [mind01/eval_harness.py:29](../../../../mind01/eval_harness.py#L29) imports `self_correction` / WorkspaceSnapshot.
- [mind01/eval_harness.py:30](../../../../mind01/eval_harness.py#L30) imports `task_contract` / EvidenceType.
- [mind01/eval_harness.py:30](../../../../mind01/eval_harness.py#L30) imports `task_contract` / TaskContract.
- [mind01/eval_harness.py:30](../../../../mind01/eval_harness.py#L30) imports `task_contract` / TaskRequirement.

## Symbols

### `mind01.eval_harness.ActionCaseResult` — lines 34–51

- Source: [mind01/eval_harness.py:34](../../../../mind01/eval_harness.py#L34)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.ActionCaseResult.to_dict` — lines 50–51

- Source: [mind01/eval_harness.py:50](../../../../mind01/eval_harness.py#L50)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.run_action_benchmark` — lines 54–80

- Source: [mind01/eval_harness.py:54](../../../../mind01/eval_harness.py#L54)
- Type: function
- Signature: `*, model: str, ollama_url: str='http://127.0.0.1:11434', suite_path: Path | None=None, output_root: Path | None=None, timeout_seconds: int=120`
- Direct static callees: `OllamaClient`, `_run_action_case`, `append`, `build_action_report`, `cwd`, `dumps`, `join`, `load_action_suite`, `make_report_directory`, `model_metadata`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness._run_action_case` — lines 83–167

- Source: [mind01/eval_harness.py:83](../../../../mind01/eval_harness.py#L83)
- Type: function
- Signature: `client: OllamaClient, case: ActionBenchmarkCase, model_metadata: dict[str, Any]`
- Direct static callees: `ActionCaseResult`, `append`, `build_action_instruction`, `canonical_response_schema`, `chat`, `encode`, `extend`, `get`, `hexdigest`, `int`, `isinstance`, `monotonic`, `parse_action_output`, `range`, `sha256`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.build_action_report` — lines 170–232

- Source: [mind01/eval_harness.py:170](../../../../mind01/eval_harness.py#L170)
- Type: function
- Signature: `suite: ActionBenchmarkSuite, results: list[ActionCaseResult], model_metadata: dict[str, Any], output_mode: str`
- Direct static callees: `Counter`, `any`, `configuration_hash`, `cwd`, `dict`, `encode`, `get`, `git_commit`, `hexdigest`, `isoformat`, `items`, `len`, `now`, `platform`, `ratio`, `sha256`, `sorted`, `split`, `sum`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.aggregate_parser_report` — lines 235–256

- Source: [mind01/eval_harness.py:235](../../../../mind01/eval_harness.py#L235)
- Type: function
- Signature: `run_directory: Path`
- Direct static callees: `Counter`, `bool`, `dict`, `dumps`, `get`, `items`, `len`, `loads`, `read_text`, `sorted`, `str`, `sum`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.run_real_mutation_smoke` — lines 259–311

- Source: [mind01/eval_harness.py:259](../../../../mind01/eval_harness.py#L259)
- Type: function
- Signature: `*, model: str, ollama_url: str='http://127.0.0.1:11434', output_root: Path | None=None, repair_budget: int=2`
- Direct static callees: `Path`, `TemporaryDirectory`, `_run_mutation_fixture`, `all`, `append`, `bool`, `copytree`, `cwd`, `dumps`, `encode`, `git_commit`, `hexdigest`, `isoformat`, `len`, `loads`, `make_report_directory`, `now`, `read_text`, `rename`, `resolve`, `rglob`, `sha256`, `sum`, `with_suffix`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness._run_mutation_fixture` — lines 314–434

- Source: [mind01/eval_harness.py:314](../../../../mind01/eval_harness.py#L314)
- Type: function
- Signature: `*, workspace: Path, fixture: dict[str, Any], model: str, ollama_url: str, repair_budget: int`
- Direct static callees: `Agent`, `Counter`, `ValueError`, `_fixture_acceptance`, `_mutation_completion_decision`, `any`, `append`, `ask`, `bool`, `build`, `capture`, `changed_files`, `classify_acceptance_failure`, `diff`, `encode`, `get`, `hexdigest`, `int`, `len`, `list`, `lower`, `max`, `range`, `restore`, `review_patch`, `sha256`, `str`, `sum`, `to_dict`, `to_dicts`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness._mutation_completion_decision` — lines 437–514

- Source: [mind01/eval_harness.py:437](../../../../mind01/eval_harness.py#L437)
- Type: function
- Signature: `*, fixture: dict[str, Any], accepted: bool, acceptance_passed: bool, changed_files: list[str], patch_review: list[dict[str, Any]], rollback_performed: bool`
- Direct static callees: `CompletionAuthority`, `TaskContract`, `TaskRequirement`, `VerificationEvidence`, `any`, `append`, `decide`, `enumerate`, `get`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness._fixture_acceptance` — lines 517–544

- Source: [mind01/eval_harness.py:517](../../../../mind01/eval_harness.py#L517)
- Type: function
- Signature: `workspace: Path, acceptance: str`
- Direct static callees: `ValueError`, `_run_acceptance`, `all`, `exec_module`, `function`, `getattr`, `items`, `module_from_spec`, `spec_from_file_location`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness._run_acceptance` — lines 547–552

- Source: [mind01/eval_harness.py:547](../../../../mind01/eval_harness.py#L547)
- Type: function
- Signature: `argv: list[str], workspace: Path`
- Direct static callees: `run`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.classify_acceptance_failure` — lines 555–563

- Source: [mind01/eval_harness.py:555](../../../../mind01/eval_harness.py#L555)
- Type: function
- Signature: `output: str`
- Direct static callees: `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.make_report_directory` — lines 566–572

- Source: [mind01/eval_harness.py:566](../../../../mind01/eval_harness.py#L566)
- Type: function
- Signature: `root: Path, kind: str, seed: str`
- Direct static callees: `encode`, `gmtime`, `hexdigest`, `mkdir`, `sha256`, `strftime`, `time_ns`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.configuration_hash` — lines 575–577

- Source: [mind01/eval_harness.py:575](../../../../mind01/eval_harness.py#L575)
- Type: function
- Signature: `metadata: dict[str, Any], suite_hash: str`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.git_commit` — lines 580–585

- Source: [mind01/eval_harness.py:580](../../../../mind01/eval_harness.py#L580)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `run`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.eval_harness.ratio` — lines 588–589

- Source: [mind01/eval_harness.py:588](../../../../mind01/eval_harness.py#L588)
- Type: function
- Signature: `value: int, total: int`
- Direct static callees: none resolved
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

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports, comments, declarations, or configuration that establish the following implementation context.

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

Imports a dependency used by this module.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–26

Imports a dependency used by this module.

### Lines 27–27

Imports a dependency used by this module.

### Lines 28–28

Imports a dependency used by this module.

### Lines 29–29

Imports a dependency used by this module.

### Lines 30–30

Imports a dependency used by this module.

### Lines 31–33

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 34–51

Defines class `ActionCaseResult` and the behavior of its members.

### Lines 52–53

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 54–80

Defines `run_action_benchmark` and its implementation control flow; direct static calls: OllamaClient, _run_action_case, append, build_action_report, cwd, dumps, join, load_action_suite, make_report_directory, model_metadata, write_text.

### Lines 81–82

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 83–112

Defines `_run_action_case` and its implementation control flow; direct static calls: ActionCaseResult, append, build_action_instruction, canonical_response_schema, chat, encode, extend, get, hexdigest, int, isinstance, monotonic, parse_action_output, range, sha256, to_dict.

### Lines 113–142

Defines `_run_action_case` and its implementation control flow; direct static calls: ActionCaseResult, append, build_action_instruction, canonical_response_schema, chat, encode, extend, get, hexdigest, int, isinstance, monotonic, parse_action_output, range, sha256, to_dict.

### Lines 143–167

Defines `_run_action_case` and its implementation control flow; direct static calls: ActionCaseResult, append, build_action_instruction, canonical_response_schema, chat, encode, extend, get, hexdigest, int, isinstance, monotonic, parse_action_output, range, sha256, to_dict.

### Lines 168–169

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 170–199

Defines `build_action_report` and its implementation control flow; direct static calls: Counter, any, configuration_hash, cwd, dict, encode, get, git_commit, hexdigest, isoformat, items, len, now, platform, ratio, sha256, sorted, split, sum, to_dict.

### Lines 200–229

Defines `build_action_report` and its implementation control flow; direct static calls: Counter, any, configuration_hash, cwd, dict, encode, get, git_commit, hexdigest, isoformat, items, len, now, platform, ratio, sha256, sorted, split, sum, to_dict.

### Lines 230–232

Defines `build_action_report` and its implementation control flow; direct static calls: Counter, any, configuration_hash, cwd, dict, encode, get, git_commit, hexdigest, isoformat, items, len, now, platform, ratio, sha256, sorted, split, sum, to_dict.

### Lines 233–234

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 235–256

Defines `aggregate_parser_report` and its implementation control flow; direct static calls: Counter, bool, dict, dumps, get, items, len, loads, read_text, sorted, str, sum, write_text.

### Lines 257–258

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 259–288

Defines `run_real_mutation_smoke` and its implementation control flow; direct static calls: Path, TemporaryDirectory, _run_mutation_fixture, all, append, bool, copytree, cwd, dumps, encode, git_commit, hexdigest, isoformat, len, loads, make_report_directory, now, read_text, rename, resolve, rglob, sha256, sum, with_suffix, write_text.

### Lines 289–311

Defines `run_real_mutation_smoke` and its implementation control flow; direct static calls: Path, TemporaryDirectory, _run_mutation_fixture, all, append, bool, copytree, cwd, dumps, encode, git_commit, hexdigest, isoformat, len, loads, make_report_directory, now, read_text, rename, resolve, rglob, sha256, sum, with_suffix, write_text.

### Lines 312–313

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 314–343

Defines `_run_mutation_fixture` and its implementation control flow; direct static calls: Agent, Counter, ValueError, _fixture_acceptance, _mutation_completion_decision, any, append, ask, bool, build, capture, changed_files, classify_acceptance_failure, diff, encode, get, hexdigest, int, len, list, lower, max, range, restore, review_patch, sha256, str, sum, to_dict, to_dicts.

### Lines 344–373

Defines `_run_mutation_fixture` and its implementation control flow; direct static calls: Agent, Counter, ValueError, _fixture_acceptance, _mutation_completion_decision, any, append, ask, bool, build, capture, changed_files, classify_acceptance_failure, diff, encode, get, hexdigest, int, len, list, lower, max, range, restore, review_patch, sha256, str, sum, to_dict, to_dicts.

### Lines 374–403

Defines `_run_mutation_fixture` and its implementation control flow; direct static calls: Agent, Counter, ValueError, _fixture_acceptance, _mutation_completion_decision, any, append, ask, bool, build, capture, changed_files, classify_acceptance_failure, diff, encode, get, hexdigest, int, len, list, lower, max, range, restore, review_patch, sha256, str, sum, to_dict, to_dicts.

### Lines 404–433

Defines `_run_mutation_fixture` and its implementation control flow; direct static calls: Agent, Counter, ValueError, _fixture_acceptance, _mutation_completion_decision, any, append, ask, bool, build, capture, changed_files, classify_acceptance_failure, diff, encode, get, hexdigest, int, len, list, lower, max, range, restore, review_patch, sha256, str, sum, to_dict, to_dicts.

### Lines 434–434

Defines `_run_mutation_fixture` and its implementation control flow; direct static calls: Agent, Counter, ValueError, _fixture_acceptance, _mutation_completion_decision, any, append, ask, bool, build, capture, changed_files, classify_acceptance_failure, diff, encode, get, hexdigest, int, len, list, lower, max, range, restore, review_patch, sha256, str, sum, to_dict, to_dicts.

### Lines 435–436

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 437–466

Defines `_mutation_completion_decision` and its implementation control flow; direct static calls: CompletionAuthority, TaskContract, TaskRequirement, VerificationEvidence, any, append, decide, enumerate, get, str, tuple.

### Lines 467–496

Defines `_mutation_completion_decision` and its implementation control flow; direct static calls: CompletionAuthority, TaskContract, TaskRequirement, VerificationEvidence, any, append, decide, enumerate, get, str, tuple.

### Lines 497–514

Defines `_mutation_completion_decision` and its implementation control flow; direct static calls: CompletionAuthority, TaskContract, TaskRequirement, VerificationEvidence, any, append, decide, enumerate, get, str, tuple.

### Lines 515–516

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 517–544

Defines `_fixture_acceptance` and its implementation control flow; direct static calls: ValueError, _run_acceptance, all, exec_module, function, getattr, items, module_from_spec, spec_from_file_location, type.

### Lines 545–546

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 547–552

Defines `_run_acceptance` and its implementation control flow; direct static calls: run, type.

### Lines 553–554

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 555–563

Defines `classify_acceptance_failure` and its implementation control flow; direct static calls: lower.

### Lines 564–565

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 566–572

Defines `make_report_directory` and its implementation control flow; direct static calls: encode, gmtime, hexdigest, mkdir, sha256, strftime, time_ns, uuid4.

### Lines 573–574

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 575–577

Defines `configuration_hash` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 578–579

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 580–585

Defines `git_commit` and its implementation control flow; direct static calls: run, strip.

### Lines 586–587

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 588–589

Defines `ratio` and its implementation control flow; direct static calls: none resolved.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
