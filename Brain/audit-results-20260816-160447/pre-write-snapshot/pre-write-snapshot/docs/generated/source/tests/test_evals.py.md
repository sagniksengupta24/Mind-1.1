# `tests/test_evals.py`

## File purpose

This testing file is reviewed at snapshot `90b9ae8f364093eaa40aaccdda8c0791dc61a5f52ddb90c04e9c7d6e3c48809b`. It contains 115 lines.

## Imports and module state

- [tests/test_evals.py:1](../../../../tests/test_evals.py#L1) imports `__future__` / annotations.
- [tests/test_evals.py:3](../../../../tests/test_evals.py#L3) imports `json`.
- [tests/test_evals.py:4](../../../../tests/test_evals.py#L4) imports `shutil`.
- [tests/test_evals.py:5](../../../../tests/test_evals.py#L5) imports `tempfile`.
- [tests/test_evals.py:6](../../../../tests/test_evals.py#L6) imports `pathlib` / Path.
- [tests/test_evals.py:8](../../../../tests/test_evals.py#L8) imports `mind01` / __version__.
- [tests/test_evals.py:9](../../../../tests/test_evals.py#L9) imports `mind01.config` / AgentConfig.
- [tests/test_evals.py:10](../../../../tests/test_evals.py#L10) imports `mind01.eval` / category_summary.
- [tests/test_evals.py:10](../../../../tests/test_evals.py#L10) imports `mind01.eval` / main.
- [tests/test_evals.py:10](../../../../tests/test_evals.py#L10) imports `mind01.eval` / render_eval_results.
- [tests/test_evals.py:10](../../../../tests/test_evals.py#L10) imports `mind01.eval` / run_eval_file.
- [tests/test_evals.py:10](../../../../tests/test_evals.py#L10) imports `mind01.eval` / save_eval_run.

## Symbols

### `tests.test_evals.run_eval_suite_tests` — lines 19–72

- Source: [tests/test_evals.py:19](../../../../tests/test_evals.py#L19)
- Type: function
- Signature: `n/a`
- Direct static callees: `AssertionError`, `Path`, `all`, `build`, `category_summary`, `exists`, `get`, `isinstance`, `len`, `loads`, `mkdtemp`, `read_text`, `render_eval_results`, `resolve`, `rmtree`, `run_eval_file`, `save_eval_run`, `sorted`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_evals.test_eval_suite_regressions` — lines 75–76

- Source: [tests/test_evals.py:75](../../../../tests/test_evals.py#L75)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_eval_suite_tests`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_evals.test_eval_validate_and_run_output_are_separately_scoped` — lines 79–115

- Source: [tests/test_evals.py:79](../../../../tests/test_evals.py#L79)
- Type: function
- Signature: `tmp_path: Path, capsys`
- Direct static callees: `eval_main`, `loads`, `read_text`, `readouterr`, `str`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–16

Imports a dependency used by this module.

### Lines 17–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–48

Defines `run_eval_suite_tests` and its implementation control flow; direct static calls: AssertionError, Path, all, build, category_summary, exists, get, isinstance, len, loads, mkdtemp, read_text, render_eval_results, resolve, rmtree, run_eval_file, save_eval_run, sorted, str, write_text.

### Lines 49–72

Defines `run_eval_suite_tests` and its implementation control flow; direct static calls: AssertionError, Path, all, build, category_summary, exists, get, isinstance, len, loads, mkdtemp, read_text, render_eval_results, resolve, rmtree, run_eval_file, save_eval_run, sorted, str, write_text.

### Lines 73–74

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 75–76

Defines `test_eval_suite_regressions` and its implementation control flow; direct static calls: run_eval_suite_tests.

### Lines 77–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–108

Defines `test_eval_validate_and_run_output_are_separately_scoped` and its implementation control flow; direct static calls: eval_main, loads, read_text, readouterr, str.

### Lines 109–115

Defines `test_eval_validate_and_run_output_are_separately_scoped` and its implementation control flow; direct static calls: eval_main, loads, read_text, readouterr, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
