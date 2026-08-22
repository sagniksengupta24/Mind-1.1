# `mind01/verification.py`

## File purpose

This verification and correction file is reviewed at snapshot `bd5f563dd400248bd64ccd453a659e8ee3a29858d18b6ae568a03b567274871d`. It contains 293 lines.

## Imports and module state

- [mind01/verification.py:1](../../../../mind01/verification.py#L1) imports `__future__` / annotations.
- [mind01/verification.py:3](../../../../mind01/verification.py#L3) imports `ast`.
- [mind01/verification.py:4](../../../../mind01/verification.py#L4) imports `json`.
- [mind01/verification.py:5](../../../../mind01/verification.py#L5) imports `re`.
- [mind01/verification.py:6](../../../../mind01/verification.py#L6) imports `shutil`.
- [mind01/verification.py:7](../../../../mind01/verification.py#L7) imports `subprocess`.
- [mind01/verification.py:8](../../../../mind01/verification.py#L8) imports `sys`.
- [mind01/verification.py:9](../../../../mind01/verification.py#L9) imports `time`.
- [mind01/verification.py:10](../../../../mind01/verification.py#L10) imports `dataclasses` / asdict.
- [mind01/verification.py:10](../../../../mind01/verification.py#L10) imports `dataclasses` / dataclass.
- [mind01/verification.py:10](../../../../mind01/verification.py#L10) imports `dataclasses` / replace.
- [mind01/verification.py:11](../../../../mind01/verification.py#L11) imports `pathlib` / Path.
- [mind01/verification.py:12](../../../../mind01/verification.py#L12) imports `typing` / Sequence.
- [mind01/verification.py:14](../../../../mind01/verification.py#L14) imports `task_contract` / EVIDENCE_TAXONOMY.
- [mind01/verification.py:14](../../../../mind01/verification.py#L14) imports `task_contract` / EvidenceType.
- [mind01/verification.py:14](../../../../mind01/verification.py#L14) imports `task_contract` / TaskContract.
- [mind01/verification.py:14](../../../../mind01/verification.py#L14) imports `task_contract` / requirement_ids_for_evidence.

## Symbols

### `mind01.verification.VerificationResult` — lines 23–42

- Source: [mind01/verification.py:23](../../../../mind01/verification.py#L23)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationResult.to_dict` — lines 41–42

- Source: [mind01/verification.py:41](../../../../mind01/verification.py#L41)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine` — lines 45–273

- Source: [mind01/verification.py:45](../../../../mind01/verification.py#L45)
- Type: class
- Signature: `n/a`
- Direct static callees: `Path`, `VerificationResult`, `_classify_evidence`, `_evidence_type_for_check`, `_parse_json`, `_python_executable_structure`, `_python_imports`, `_python_symbol_contract`, `_run`, `any`, `append`, `compile`, `exists`, `extend`, `get`, `getattr`, `int`, `isinstance`, `join`, `list`, `loads`, `lower`, `mandatory_requirements`, `map`, `parse`, `perf_counter`, `read_text`, `relative_to`, `replace`, `requirement_ids_for_evidence`, `resolve`, `run`, `search`, `str`, `tuple`, `walk`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine.__init__` — lines 46–49

- Source: [mind01/verification.py:46](../../../../mind01/verification.py#L46)
- Type: method
- Signature: `self, workspace: Path, timeout_seconds: int=60, output_limit: int=4000`
- Direct static callees: `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine.verify_paths` — lines 51–116

- Source: [mind01/verification.py:51](../../../../mind01/verification.py#L51)
- Type: method
- Signature: `self, paths: Sequence[str], full_project: bool=False, *, contract: TaskContract | None=None, mutation_state_hash: str=''`
- Direct static callees: `Path`, `VerificationResult`, `_classify_evidence`, `_parse_json`, `_python_executable_structure`, `_python_imports`, `_python_symbol_contract`, `_run`, `any`, `append`, `exists`, `extend`, `lower`, `mandatory_requirements`, `resolve`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._parse_json` — lines 118–124

- Source: [mind01/verification.py:118](../../../../mind01/verification.py#L118)
- Type: method
- Signature: `self, path: Path`
- Direct static callees: `VerificationResult`, `int`, `loads`, `perf_counter`, `read_text`, `relative_to`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._python_executable_structure` — lines 126–161

- Source: [mind01/verification.py:126](../../../../mind01/verification.py#L126)
- Type: method
- Signature: `self, path: Path`
- Direct static callees: `VerificationResult`, `append`, `compile`, `getattr`, `int`, `isinstance`, `join`, `map`, `parse`, `perf_counter`, `read_text`, `relative_to`, `search`, `str`, `walk`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._python_symbol_contract` — lines 163–213

- Source: [mind01/verification.py:163](../../../../mind01/verification.py#L163)
- Type: method
- Signature: `self, paths: Sequence[str], contract: TaskContract`
- Direct static callees: `VerificationResult`, `append`, `exists`, `get`, `int`, `isinstance`, `lower`, `parse`, `perf_counter`, `read_text`, `resolve`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._python_imports` — lines 215–234

- Source: [mind01/verification.py:215](../../../../mind01/verification.py#L215)
- Type: method
- Signature: `self, paths: Sequence[str]`
- Direct static callees: `_run`, `append`, `exists`, `lower`, `resolve`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._classify_evidence` — lines 236–251

- Source: [mind01/verification.py:236](../../../../mind01/verification.py#L236)
- Type: method
- Signature: `self, result: VerificationResult, contract: TaskContract | None, mutation_state_hash: str`
- Direct static callees: `_evidence_type_for_check`, `replace`, `requirement_ids_for_evidence`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification.VerificationEngine._run` — lines 253–273

- Source: [mind01/verification.py:253](../../../../mind01/verification.py#L253)
- Type: method
- Signature: `self, argv: tuple[str, ...], name: str, blocking: bool`
- Direct static callees: `Path`, `VerificationResult`, `int`, `isinstance`, `list`, `perf_counter`, `run`, `str`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.verification._evidence_type_for_check` — lines 276–293

- Source: [mind01/verification.py:276](../../../../mind01/verification.py#L276)
- Type: function
- Signature: `check: str, declared: str`
- Direct static callees: `EvidenceType`, `startswith`
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

### Lines 14–19

Imports a dependency used by this module.

### Lines 20–22

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 23–42

Defines class `VerificationResult` and the behavior of its members.

### Lines 43–44

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 45–74

Defines class `VerificationEngine` and the behavior of its members.

### Lines 75–104

Defines class `VerificationEngine` and the behavior of its members.

### Lines 105–134

Defines class `VerificationEngine` and the behavior of its members.

### Lines 135–164

Defines class `VerificationEngine` and the behavior of its members.

### Lines 165–194

Defines class `VerificationEngine` and the behavior of its members.

### Lines 195–224

Defines class `VerificationEngine` and the behavior of its members.

### Lines 225–254

Defines class `VerificationEngine` and the behavior of its members.

### Lines 255–273

Defines class `VerificationEngine` and the behavior of its members.

### Lines 274–275

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 276–293

Defines `_evidence_type_for_check` and its implementation control flow; direct static calls: EvidenceType, startswith.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
