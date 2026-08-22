# `tests/test_traces.py`

## File purpose

This testing file is reviewed at snapshot `2b44db919b9e6db729f5627b7deb6a289e99d69a6e87e7c72be52c3964269ef4`. It contains 114 lines.

## Imports and module state

- [tests/test_traces.py:1](../../../../tests/test_traces.py#L1) imports `__future__` / annotations.
- [tests/test_traces.py:3](../../../../tests/test_traces.py#L3) imports `contextlib`.
- [tests/test_traces.py:4](../../../../tests/test_traces.py#L4) imports `io`.
- [tests/test_traces.py:5](../../../../tests/test_traces.py#L5) imports `json`.
- [tests/test_traces.py:6](../../../../tests/test_traces.py#L6) imports `shutil`.
- [tests/test_traces.py:7](../../../../tests/test_traces.py#L7) imports `tempfile`.
- [tests/test_traces.py:8](../../../../tests/test_traces.py#L8) imports `pathlib` / Path.
- [tests/test_traces.py:10](../../../../tests/test_traces.py#L10) imports `mind01.agent` / Agent.
- [tests/test_traces.py:11](../../../../tests/test_traces.py#L11) imports `mind01.cli` / main.
- [tests/test_traces.py:12](../../../../tests/test_traces.py#L12) imports `mind01.config` / AgentConfig.
- [tests/test_traces.py:13](../../../../tests/test_traces.py#L13) imports `mind01.tools` / ToolError.
- [tests/test_traces.py:13](../../../../tests/test_traces.py#L13) imports `mind01.tools` / ToolRegistry.
- [tests/test_traces.py:14](../../../../tests/test_traces.py#L14) imports `mind01.traces` / TraceStore.

## Symbols

### `tests.test_traces.run_trace_tests` — lines 17–91

- Source: [tests/test_traces.py:17](../../../../tests/test_traces.py#L17)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `AssertionError`, `Path`, `ToolRegistry`, `TraceStore`, `any`, `ask`, `build`, `call`, `dumps`, `join`, `list`, `loads`, `mkdir`, `mkdtemp`, `read_events`, `rmtree`, `run_cli_capture`, `splitlines`, `str`, `strip`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_traces.read_events` — lines 94–102

- Source: [tests/test_traces.py:94](../../../../tests/test_traces.py#L94)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `append`, `glob`, `loads`, `read_text`, `sorted`, `splitlines`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_traces.run_cli_capture` — lines 105–110

- Source: [tests/test_traces.py:105](../../../../tests/test_traces.py#L105)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `StringIO`, `cli_main`, `getvalue`, `redirect_stderr`, `redirect_stdout`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_traces.test_trace_regressions` — lines 113–114

- Source: [tests/test_traces.py:113](../../../../tests/test_traces.py#L113)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_trace_tests`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

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

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–46

Defines `run_trace_tests` and its implementation control flow; direct static calls: Agent, AssertionError, Path, ToolRegistry, TraceStore, any, ask, build, call, dumps, join, list, loads, mkdir, mkdtemp, read_events, rmtree, run_cli_capture, splitlines, str, strip, write_text.

### Lines 47–76

Defines `run_trace_tests` and its implementation control flow; direct static calls: Agent, AssertionError, Path, ToolRegistry, TraceStore, any, ask, build, call, dumps, join, list, loads, mkdir, mkdtemp, read_events, rmtree, run_cli_capture, splitlines, str, strip, write_text.

### Lines 77–91

Defines `run_trace_tests` and its implementation control flow; direct static calls: Agent, AssertionError, Path, ToolRegistry, TraceStore, any, ask, build, call, dumps, join, list, loads, mkdir, mkdtemp, read_events, rmtree, run_cli_capture, splitlines, str, strip, write_text.

### Lines 92–93

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 94–102

Defines `read_events` and its implementation control flow; direct static calls: append, glob, loads, read_text, sorted, splitlines, strip.

### Lines 103–104

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 105–110

Defines `run_cli_capture` and its implementation control flow; direct static calls: StringIO, cli_main, getvalue, redirect_stderr, redirect_stdout.

### Lines 111–112

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 113–114

Defines `test_trace_regressions` and its implementation control flow; direct static calls: run_trace_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
