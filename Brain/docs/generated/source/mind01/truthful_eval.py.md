# `mind01/truthful_eval.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `e208c5a9c9e86712012a68940a5c4887e9e9f1c34bc08954ece7136fb4a6859b`. It contains 138 lines.

## Imports and module state

- [mind01/truthful_eval.py:1](../../../../mind01/truthful_eval.py#L1) imports `__future__` / annotations.
- [mind01/truthful_eval.py:3](../../../../mind01/truthful_eval.py#L3) imports `hashlib`.
- [mind01/truthful_eval.py:4](../../../../mind01/truthful_eval.py#L4) imports `json`.
- [mind01/truthful_eval.py:5](../../../../mind01/truthful_eval.py#L5) imports `pathlib` / Path.
- [mind01/truthful_eval.py:6](../../../../mind01/truthful_eval.py#L6) imports `typing` / Any.
- [mind01/truthful_eval.py:8](../../../../mind01/truthful_eval.py#L8) imports `completion` / CompletionAuthority.
- [mind01/truthful_eval.py:8](../../../../mind01/truthful_eval.py#L8) imports `completion` / VerificationEvidence.
- [mind01/truthful_eval.py:9](../../../../mind01/truthful_eval.py#L9) imports `task_contract` / EvidenceType.
- [mind01/truthful_eval.py:9](../../../../mind01/truthful_eval.py#L9) imports `task_contract` / TaskContract.
- [mind01/truthful_eval.py:9](../../../../mind01/truthful_eval.py#L9) imports `task_contract` / TaskRequirement.
- [mind01/truthful_eval.py:10](../../../../mind01/truthful_eval.py#L10) imports `version` / __version__.

## Symbols

### `mind01.truthful_eval.TRUTHFUL_COMPLETION_VERSION` — lines 13–13

- Source: [mind01/truthful_eval.py:13](../../../../mind01/truthful_eval.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.truthful_eval.default_truthful_suite_path` — lines 16–17

- Source: [mind01/truthful_eval.py:16](../../../../mind01/truthful_eval.py#L16)
- Type: function
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.truthful_eval.load_truthful_suite` — lines 20–36

- Source: [mind01/truthful_eval.py:20](../../../../mind01/truthful_eval.py#L20)
- Type: function
- Signature: `path: Path | None=None`
- Direct static callees: `ValueError`, `any`, `default_truthful_suite_path`, `encode`, `get`, `hexdigest`, `isinstance`, `len`, `loads`, `read_text`, `resolve`, `set`, `sha256`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.truthful_eval.run_truthful_completion_regression` — lines 39–90

- Source: [mind01/truthful_eval.py:39](../../../../mind01/truthful_eval.py#L39)
- Type: function
- Signature: `path: Path | None=None`
- Direct static callees: `CompletionAuthority`, `_contract_for_case`, `_evidence_from_case`, `append`, `bool`, `decide`, `get`, `int`, `len`, `list`, `load_truthful_suite`, `str`, `sum`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.truthful_eval._contract_for_case` — lines 93–120

- Source: [mind01/truthful_eval.py:93](../../../../mind01/truthful_eval.py#L93)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `EvidenceType`, `TaskContract`, `TaskRequirement`, `get`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.truthful_eval._evidence_from_case` — lines 123–138

- Source: [mind01/truthful_eval.py:123](../../../../mind01/truthful_eval.py#L123)
- Type: function
- Signature: `item: dict[str, Any]`
- Direct static callees: `VerificationEvidence`, `bool`, `get`, `str`, `tuple`
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

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–17

Defines `default_truthful_suite_path` and its implementation control flow; direct static calls: Path, resolve.

### Lines 18–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–36

Defines `load_truthful_suite` and its implementation control flow; direct static calls: ValueError, any, default_truthful_suite_path, encode, get, hexdigest, isinstance, len, loads, read_text, resolve, set, sha256, str.

### Lines 37–38

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 39–68

Defines `run_truthful_completion_regression` and its implementation control flow; direct static calls: CompletionAuthority, _contract_for_case, _evidence_from_case, append, bool, decide, get, int, len, list, load_truthful_suite, str, sum, to_dict.

### Lines 69–90

Defines `run_truthful_completion_regression` and its implementation control flow; direct static calls: CompletionAuthority, _contract_for_case, _evidence_from_case, append, bool, decide, get, int, len, list, load_truthful_suite, str, sum, to_dict.

### Lines 91–92

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 93–120

Defines `_contract_for_case` and its implementation control flow; direct static calls: EvidenceType, TaskContract, TaskRequirement, get, str, tuple.

### Lines 121–122

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 123–138

Defines `_evidence_from_case` and its implementation control flow; direct static calls: VerificationEvidence, bool, get, str, tuple.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
