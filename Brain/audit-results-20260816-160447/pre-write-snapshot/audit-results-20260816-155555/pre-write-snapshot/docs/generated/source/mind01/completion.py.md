# `mind01/completion.py`

## File purpose

This agent runtime file is reviewed at snapshot `afabc5db335e4e829359ffd40849d5d9f7b66de44f61f5c514491ed33e628f37`. It contains 419 lines.

## Imports and module state

- [mind01/completion.py:1](../../../../mind01/completion.py#L1) imports `__future__` / annotations.
- [mind01/completion.py:3](../../../../mind01/completion.py#L3) imports `dataclasses` / asdict.
- [mind01/completion.py:3](../../../../mind01/completion.py#L3) imports `dataclasses` / dataclass.
- [mind01/completion.py:3](../../../../mind01/completion.py#L3) imports `dataclasses` / field.
- [mind01/completion.py:3](../../../../mind01/completion.py#L3) imports `dataclasses` / replace.
- [mind01/completion.py:4](../../../../mind01/completion.py#L4) imports `typing` / Any.
- [mind01/completion.py:4](../../../../mind01/completion.py#L4) imports `typing` / Literal.
- [mind01/completion.py:4](../../../../mind01/completion.py#L4) imports `typing` / Mapping.
- [mind01/completion.py:4](../../../../mind01/completion.py#L4) imports `typing` / Sequence.
- [mind01/completion.py:6](../../../../mind01/completion.py#L6) imports `task_contract` / EvidenceType.
- [mind01/completion.py:6](../../../../mind01/completion.py#L6) imports `task_contract` / TaskContract.
- [mind01/completion.py:6](../../../../mind01/completion.py#L6) imports `task_contract` / TaskRequirement.

## Symbols

### `mind01.completion.CompletionStatus` — lines 9–17

- Source: [mind01/completion.py:9](../../../../mind01/completion.py#L9)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.ALLOWED_COMPLETION_STATUSES` — lines 19–27

- Source: [mind01/completion.py:19](../../../../mind01/completion.py#L19)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.VerificationEvidence` — lines 31–89

- Source: [mind01/completion.py:31](../../../../mind01/completion.py#L31)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `bool`, `cls`, `dataclass`, `float`, `get`, `isinstance`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.VerificationEvidence.passed` — lines 52–53

- Source: [mind01/completion.py:52](../../../../mind01/completion.py#L52)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.VerificationEvidence.blocking_failed` — lines 56–57

- Source: [mind01/completion.py:56](../../../../mind01/completion.py#L56)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.VerificationEvidence.to_dict` — lines 59–60

- Source: [mind01/completion.py:59](../../../../mind01/completion.py#L59)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.VerificationEvidence.from_mapping` — lines 63–89

- Source: [mind01/completion.py:63](../../../../mind01/completion.py#L63)
- Type: method
- Signature: `cls, payload: Mapping[str, Any], *, fallback_id: str=''`
- Direct static callees: `bool`, `cls`, `float`, `get`, `isinstance`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionDecision` — lines 93–102

- Source: [mind01/completion.py:93](../../../../mind01/completion.py#L93)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionDecision.to_dict` — lines 101–102

- Source: [mind01/completion.py:101](../../../../mind01/completion.py#L101)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionContract` — lines 106–144

- Source: [mind01/completion.py:106](../../../../mind01/completion.py#L106)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`, `field`, `join`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionContract.to_dict` — lines 126–129

- Source: [mind01/completion.py:126](../../../../mind01/completion.py#L126)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionContract.to_user_text` — lines 131–144

- Source: [mind01/completion.py:131](../../../../mind01/completion.py#L131)
- Type: method
- Signature: `self`
- Direct static callees: `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionAuthority` — lines 147–278

- Source: [mind01/completion.py:147](../../../../mind01/completion.py#L147)
- Type: class
- Signature: `n/a`
- Direct static callees: `CompletionDecision`, `_coerce_evidence`, `_evidence_for_requirement`, `any`, `append`, `bool`, `extend`, `fromkeys`, `get`, `issubset`, `join`, `mandatory_requirements`, `rstrip`, `startswith`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.CompletionAuthority.decide` — lines 154–278

- Source: [mind01/completion.py:154](../../../../mind01/completion.py#L154)
- Type: method
- Signature: `self, requested_status: str, *, task_contract: TaskContract | None, verification: Sequence[VerificationEvidence | Mapping[str, Any]], evidence_refs: Sequence[str]=(), patch_review: Sequence[Mapping[str, Any]]=(), changed_files: Sequence[str]=(), current_state_hash: str='', receipt_state_hash: str='', unauthorized_mutations: int=0, required_checks_skipped: Sequence[str]=(), rollback_performed: bool=False`
- Direct static callees: `CompletionDecision`, `_coerce_evidence`, `_evidence_for_requirement`, `any`, `append`, `bool`, `extend`, `fromkeys`, `get`, `issubset`, `join`, `mandatory_requirements`, `rstrip`, `startswith`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion._coerce_evidence` — lines 281–293

- Source: [mind01/completion.py:281](../../../../mind01/completion.py#L281)
- Type: function
- Signature: `verification: Sequence[VerificationEvidence | Mapping[str, Any]]`
- Direct static callees: `append`, `enumerate`, `from_mapping`, `isinstance`, `replace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion._evidence_for_requirement` — lines 296–305

- Source: [mind01/completion.py:296](../../../../mind01/completion.py#L296)
- Type: function
- Signature: `requirement: TaskRequirement, evidence: Sequence[VerificationEvidence]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.normalize_completion_status` — lines 308–360

- Source: [mind01/completion.py:308](../../../../mind01/completion.py#L308)
- Type: function
- Signature: `requested_status: str, *, verification: list[VerificationEvidence], patch_review: list[dict[str, Any]] | None=None, uncertainty: list[str] | None=None`
- Direct static callees: `CompletionAuthority`, `EvidenceType`, `TaskContract`, `TaskRequirement`, `append`, `decide`, `enumerate`, `extend`, `fromkeys`, `list`, `replace`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.completion.build_completion_contract` — lines 363–419

- Source: [mind01/completion.py:363](../../../../mind01/completion.py#L363)
- Type: function
- Signature: `*, objective: str, requested_status: str, specialist: str='general_reasoning', plan_summary: list[str] | None=None, files_changed: list[str] | None=None, verification: list[VerificationEvidence] | None=None, repair_attempts: int=0, rollback_available: bool=False, remaining_uncertainty: list[str] | None=None, patch_review: list[dict[str, Any]] | None=None, failure_category: str='', task_contract: TaskContract | None=None, current_state_hash: str='', receipt_state_hash: str='', unauthorized_mutations: int=0, required_checks_skipped: list[str] | None=None, rollback_performed: bool=False`
- Direct static callees: `CompletionAuthority`, `CompletionContract`, `_coerce_evidence`, `decide`, `extend`, `fromkeys`, `list`, `set`, `sorted`, `to_dict`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–17

Implements module-level `Assign` behavior or data.

### Lines 18–18

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 19–27

Implements module-level `AnnAssign` behavior or data.

### Lines 28–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–60

Defines class `VerificationEvidence` and the behavior of its members.

### Lines 61–89

Defines class `VerificationEvidence` and the behavior of its members.

### Lines 90–92

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 93–102

Defines class `CompletionDecision` and the behavior of its members.

### Lines 103–105

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 106–135

Defines class `CompletionContract` and the behavior of its members.

### Lines 136–144

Defines class `CompletionContract` and the behavior of its members.

### Lines 145–146

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 147–176

Defines class `CompletionAuthority` and the behavior of its members.

### Lines 177–206

Defines class `CompletionAuthority` and the behavior of its members.

### Lines 207–236

Defines class `CompletionAuthority` and the behavior of its members.

### Lines 237–266

Defines class `CompletionAuthority` and the behavior of its members.

### Lines 267–278

Defines class `CompletionAuthority` and the behavior of its members.

### Lines 279–280

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 281–293

Defines `_coerce_evidence` and its implementation control flow; direct static calls: append, enumerate, from_mapping, isinstance, replace.

### Lines 294–295

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 296–305

Defines `_evidence_for_requirement` and its implementation control flow; direct static calls: none resolved.

### Lines 306–307

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 308–337

Defines `normalize_completion_status` and its implementation control flow; direct static calls: CompletionAuthority, EvidenceType, TaskContract, TaskRequirement, append, decide, enumerate, extend, fromkeys, list, replace, tuple.

### Lines 338–360

Defines `normalize_completion_status` and its implementation control flow; direct static calls: CompletionAuthority, EvidenceType, TaskContract, TaskRequirement, append, decide, enumerate, extend, fromkeys, list, replace, tuple.

### Lines 361–362

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 363–392

Defines `build_completion_contract` and its implementation control flow; direct static calls: CompletionAuthority, CompletionContract, _coerce_evidence, decide, extend, fromkeys, list, set, sorted, to_dict.

### Lines 393–419

Defines `build_completion_contract` and its implementation control flow; direct static calls: CompletionAuthority, CompletionContract, _coerce_evidence, decide, extend, fromkeys, list, set, sorted, to_dict.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
