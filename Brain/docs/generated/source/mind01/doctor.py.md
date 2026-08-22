# `mind01/doctor.py`

## File purpose

This agent runtime file is reviewed at snapshot `5621ade56e11891454d8bd39f95918bf03701d89d284d31f39f7811582677dc0`. It contains 98 lines.

## Imports and module state

- [mind01/doctor.py:1](../../../../mind01/doctor.py#L1) imports `__future__` / annotations.
- [mind01/doctor.py:3](../../../../mind01/doctor.py#L3) imports `json`.
- [mind01/doctor.py:4](../../../../mind01/doctor.py#L4) imports `platform`.
- [mind01/doctor.py:5](../../../../mind01/doctor.py#L5) imports `shutil`.
- [mind01/doctor.py:6](../../../../mind01/doctor.py#L6) imports `sys`.
- [mind01/doctor.py:7](../../../../mind01/doctor.py#L7) imports `urllib.error`.
- [mind01/doctor.py:8](../../../../mind01/doctor.py#L8) imports `urllib.request`.
- [mind01/doctor.py:9](../../../../mind01/doctor.py#L9) imports `dataclasses` / dataclass.

## Symbols

### `mind01.doctor.Check` — lines 13–17

- Source: [mind01/doctor.py:13](../../../../mind01/doctor.py#L13)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.doctor.run_doctor` — lines 20–69

- Source: [mind01/doctor.py:20](../../../../mind01/doctor.py#L20)
- Type: function
- Signature: `model: str, ollama_url: str`
- Direct static callees: `Check`, `append`, `extract_model_names`, `fetch_ollama_tags`, `platform`, `split`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.doctor.fetch_ollama_tags` — lines 72–78

- Source: [mind01/doctor.py:72](../../../../mind01/doctor.py#L72)
- Type: function
- Signature: `ollama_url: str`
- Direct static callees: `Request`, `decode`, `loads`, `read`, `rstrip`, `urlopen`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.doctor.extract_model_names` — lines 81–88

- Source: [mind01/doctor.py:81](../../../../mind01/doctor.py#L81)
- Type: function
- Signature: `tags: dict`
- Direct static callees: `add`, `get`, `isinstance`, `set`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.doctor.render_doctor` — lines 91–98

- Source: [mind01/doctor.py:91](../../../../mind01/doctor.py#L91)
- Type: function
- Signature: `checks: list[Check]`
- Direct static callees: `append`, `join`
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

### Lines 10–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–17

Defines class `Check` and the behavior of its members.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–49

Defines `run_doctor` and its implementation control flow; direct static calls: Check, append, extract_model_names, fetch_ollama_tags, platform, split, which.

### Lines 50–69

Defines `run_doctor` and its implementation control flow; direct static calls: Check, append, extract_model_names, fetch_ollama_tags, platform, split, which.

### Lines 70–71

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 72–78

Defines `fetch_ollama_tags` and its implementation control flow; direct static calls: Request, decode, loads, read, rstrip, urlopen.

### Lines 79–80

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 81–88

Defines `extract_model_names` and its implementation control flow; direct static calls: add, get, isinstance, set, split.

### Lines 89–90

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 91–98

Defines `render_doctor` and its implementation control flow; direct static calls: append, join.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
