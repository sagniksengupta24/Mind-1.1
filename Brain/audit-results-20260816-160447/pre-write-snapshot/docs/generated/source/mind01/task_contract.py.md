# `mind01/task_contract.py`

## File purpose

This agent runtime file is reviewed at snapshot `f304f1e8de8f95327c885f4ddd4dfd48a25519f8b73fa71f44105a084d1d97f5`. It contains 363 lines.

## Imports and module state

- [mind01/task_contract.py:1](../../../../mind01/task_contract.py#L1) imports `__future__` / annotations.
- [mind01/task_contract.py:3](../../../../mind01/task_contract.py#L3) imports `hashlib`.
- [mind01/task_contract.py:4](../../../../mind01/task_contract.py#L4) imports `json`.
- [mind01/task_contract.py:5](../../../../mind01/task_contract.py#L5) imports `re`.
- [mind01/task_contract.py:6](../../../../mind01/task_contract.py#L6) imports `dataclasses` / asdict.
- [mind01/task_contract.py:6](../../../../mind01/task_contract.py#L6) imports `dataclasses` / dataclass.
- [mind01/task_contract.py:6](../../../../mind01/task_contract.py#L6) imports `dataclasses` / field.
- [mind01/task_contract.py:7](../../../../mind01/task_contract.py#L7) imports `enum` / Enum.
- [mind01/task_contract.py:8](../../../../mind01/task_contract.py#L8) imports `pathlib` / Path.
- [mind01/task_contract.py:9](../../../../mind01/task_contract.py#L9) imports `typing` / Any.
- [mind01/task_contract.py:9](../../../../mind01/task_contract.py#L9) imports `typing` / Iterable.

## Symbols

### `mind01.task_contract.EvidenceType` — lines 12–26

- Source: [mind01/task_contract.py:12](../../../../mind01/task_contract.py#L12)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.EvidenceSemantics` — lines 30–33

- Source: [mind01/task_contract.py:30](../../../../mind01/task_contract.py#L30)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.EVIDENCE_TAXONOMY` — lines 36–107

- Source: [mind01/task_contract.py:36](../../../../mind01/task_contract.py#L36)
- Type: constant
- Signature: `n/a`
- Direct static callees: `EvidenceSemantics`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskRequirement` — lines 111–120

- Source: [mind01/task_contract.py:111](../../../../mind01/task_contract.py#L111)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskRequirement.to_dict` — lines 117–120

- Source: [mind01/task_contract.py:117](../../../../mind01/task_contract.py#L117)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskContract` — lines 124–192

- Source: [mind01/task_contract.py:124](../../../../mind01/task_contract.py#L124)
- Type: class
- Signature: `n/a`
- Direct static callees: `EvidenceType`, `TaskRequirement`, `asdict`, `bool`, `cls`, `dataclass`, `dict`, `dumps`, `encode`, `field`, `get`, `hexdigest`, `items`, `list`, `sha256`, `str`, `to_dict`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskContract.to_dict` — lines 144–150

- Source: [mind01/task_contract.py:144](../../../../mind01/task_contract.py#L144)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`, `items`, `list`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskContract.from_dict` — lines 153–185

- Source: [mind01/task_contract.py:153](../../../../mind01/task_contract.py#L153)
- Type: method
- Signature: `cls, payload: dict[str, Any]`
- Direct static callees: `EvidenceType`, `TaskRequirement`, `bool`, `cls`, `dict`, `get`, `items`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskContract.sha256` — lines 187–189

- Source: [mind01/task_contract.py:187](../../../../mind01/task_contract.py#L187)
- Type: method
- Signature: `self`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.TaskContract.mandatory_requirements` — lines 191–192

- Source: [mind01/task_contract.py:191](../../../../mind01/task_contract.py#L191)
- Type: method
- Signature: `self`
- Direct static callees: `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract._FILE_RE` — lines 195–198

- Source: [mind01/task_contract.py:195](../../../../mind01/task_contract.py#L195)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract._CALLABLE_PATTERNS` — lines 199–210

- Source: [mind01/task_contract.py:199](../../../../mind01/task_contract.py#L199)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.build_task_contract` — lines 213–338

- Source: [mind01/task_contract.py:213](../../../../mind01/task_contract.py#L213)
- Type: function
- Signature: `goal: str, *, mutation_required: bool, specialist: str='general_reasoning', baseline_state_hash: str=''`
- Direct static callees: `TaskContract`, `TaskRequirement`, `any`, `append`, `bool`, `dumps`, `encode`, `endswith`, `enumerate`, `extend`, `finditer`, `fromkeys`, `group`, `hexdigest`, `join`, `lower`, `search`, `sha256`, `split`, `strip`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.requirement_ids_for_evidence` — lines 341–350

- Source: [mind01/task_contract.py:341](../../../../mind01/task_contract.py#L341)
- Type: function
- Signature: `contract: TaskContract | None, evidence_type: EvidenceType | str`
- Direct static callees: `EvidenceType`, `isinstance`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.task_contract.state_hash` — lines 353–363

- Source: [mind01/task_contract.py:353](../../../../mind01/task_contract.py#L353)
- Type: function
- Signature: `workspace: Path, paths: Iterable[str]`
- Direct static callees: `encode`, `exists`, `hexdigest`, `is_file`, `read_bytes`, `resolve`, `set`, `sha256`, `sorted`, `update`
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

### Lines 10–11

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 12–26

Defines class `EvidenceType` and the behavior of its members.

### Lines 27–29

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 30–33

Defines class `EvidenceSemantics` and the behavior of its members.

### Lines 34–35

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 36–65

Implements module-level `AnnAssign` behavior or data.

### Lines 66–95

Implements module-level `AnnAssign` behavior or data.

### Lines 96–107

Implements module-level `AnnAssign` behavior or data.

### Lines 108–110

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 111–120

Defines class `TaskRequirement` and the behavior of its members.

### Lines 121–123

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 124–153

Defines class `TaskContract` and the behavior of its members.

### Lines 154–183

Defines class `TaskContract` and the behavior of its members.

### Lines 184–192

Defines class `TaskContract` and the behavior of its members.

### Lines 193–194

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 195–198

Implements module-level `Assign` behavior or data.

### Lines 199–210

Implements module-level `Assign` behavior or data.

### Lines 211–212

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 213–242

Defines `build_task_contract` and its implementation control flow; direct static calls: TaskContract, TaskRequirement, any, append, bool, dumps, encode, endswith, enumerate, extend, finditer, fromkeys, group, hexdigest, join, lower, search, sha256, split, strip, tuple.

### Lines 243–272

Defines `build_task_contract` and its implementation control flow; direct static calls: TaskContract, TaskRequirement, any, append, bool, dumps, encode, endswith, enumerate, extend, finditer, fromkeys, group, hexdigest, join, lower, search, sha256, split, strip, tuple.

### Lines 273–302

Defines `build_task_contract` and its implementation control flow; direct static calls: TaskContract, TaskRequirement, any, append, bool, dumps, encode, endswith, enumerate, extend, finditer, fromkeys, group, hexdigest, join, lower, search, sha256, split, strip, tuple.

### Lines 303–332

Defines `build_task_contract` and its implementation control flow; direct static calls: TaskContract, TaskRequirement, any, append, bool, dumps, encode, endswith, enumerate, extend, finditer, fromkeys, group, hexdigest, join, lower, search, sha256, split, strip, tuple.

### Lines 333–338

Defines `build_task_contract` and its implementation control flow; direct static calls: TaskContract, TaskRequirement, any, append, bool, dumps, encode, endswith, enumerate, extend, finditer, fromkeys, group, hexdigest, join, lower, search, sha256, split, strip, tuple.

### Lines 339–340

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 341–350

Defines `requirement_ids_for_evidence` and its implementation control flow; direct static calls: EvidenceType, isinstance, tuple.

### Lines 351–352

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 353–363

Defines `state_hash` and its implementation control flow; direct static calls: encode, exists, hexdigest, is_file, read_bytes, resolve, set, sha256, sorted, update.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
