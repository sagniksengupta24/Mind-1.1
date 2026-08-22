# `mind01/annotation_v3.py`

## File purpose

This agent runtime file is reviewed at snapshot `0590c07a39723b61e0d3c5f4a5d535639cc5b0c7bed1cfdfacbd477e671cfaba`. It contains 721 lines.

## Imports and module state

- [mind01/annotation_v3.py:1](../../../../mind01/annotation_v3.py#L1) imports `__future__` / annotations.
- [mind01/annotation_v3.py:3](../../../../mind01/annotation_v3.py#L3) imports `hashlib`.
- [mind01/annotation_v3.py:4](../../../../mind01/annotation_v3.py#L4) imports `itertools`.
- [mind01/annotation_v3.py:5](../../../../mind01/annotation_v3.py#L5) imports `json`.
- [mind01/annotation_v3.py:6](../../../../mind01/annotation_v3.py#L6) imports `dataclasses` / dataclass.
- [mind01/annotation_v3.py:7](../../../../mind01/annotation_v3.py#L7) imports `typing` / Any.
- [mind01/annotation_v3.py:7](../../../../mind01/annotation_v3.py#L7) imports `typing` / Mapping.

## Symbols

### `mind01.annotation_v3.TASK_CLASSES` — lines 10–10

- Source: [mind01/annotation_v3.py:10](../../../../mind01/annotation_v3.py#L10)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.SPECIALISTS` — lines 11–11

- Source: [mind01/annotation_v3.py:11](../../../../mind01/annotation_v3.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.RESPONSE_MODES` — lines 12–12

- Source: [mind01/annotation_v3.py:12](../../../../mind01/annotation_v3.py#L12)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.RISK_LEVELS` — lines 13–13

- Source: [mind01/annotation_v3.py:13](../../../../mind01/annotation_v3.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.PHASES` — lines 14–14

- Source: [mind01/annotation_v3.py:14](../../../../mind01/annotation_v3.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.TOOL_FAMILIES` — lines 15–19

- Source: [mind01/annotation_v3.py:15](../../../../mind01/annotation_v3.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.TOOLS` — lines 20–26

- Source: [mind01/annotation_v3.py:20](../../../../mind01/annotation_v3.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.TOOL_FAMILIES_BY_TOOL` — lines 27–42

- Source: [mind01/annotation_v3.py:27](../../../../mind01/annotation_v3.py#L27)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.SIDE_EFFECT_TOOLS` — lines 43–46

- Source: [mind01/annotation_v3.py:43](../../../../mind01/annotation_v3.py#L43)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.LIVE_MUTATION_TOOLS` — lines 47–47

- Source: [mind01/annotation_v3.py:47](../../../../mind01/annotation_v3.py#L47)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.SHELL_TOOLS` — lines 48–48

- Source: [mind01/annotation_v3.py:48](../../../../mind01/annotation_v3.py#L48)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.PROPOSAL_TOOLS` — lines 49–49

- Source: [mind01/annotation_v3.py:49](../../../../mind01/annotation_v3.py#L49)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.EXISTING_FILE_OPERATIONS` — lines 50–50

- Source: [mind01/annotation_v3.py:50](../../../../mind01/annotation_v3.py#L50)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.MUTATION_OPERATIONS` — lines 51–51

- Source: [mind01/annotation_v3.py:51](../../../../mind01/annotation_v3.py#L51)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.REASON_CODES` — lines 52–63

- Source: [mind01/annotation_v3.py:52](../../../../mind01/annotation_v3.py#L52)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.LABEL_FIELDS` — lines 64–70

- Source: [mind01/annotation_v3.py:64](../../../../mind01/annotation_v3.py#L64)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.PolicyConstraints` — lines 74–149

- Source: [mind01/annotation_v3.py:74](../../../../mind01/annotation_v3.py#L74)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.PolicyConstraints.to_dict` — lines 103–149

- Source: [mind01/annotation_v3.py:103](../../../../mind01/annotation_v3.py#L103)
- Type: method
- Signature: `self`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.derive_policy_constraints` — lines 152–398

- Source: [mind01/annotation_v3.py:152](../../../../mind01/annotation_v3.py#L152)
- Type: function
- Signature: `case: Mapping[str, Any]`
- Direct static callees: `PolicyConstraints`, `ValueError`, `append`, `bool`, `extend`, `get`, `isinstance`, `set`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.validate_annotation` — lines 401–545

- Source: [mind01/annotation_v3.py:401](../../../../mind01/annotation_v3.py#L401)
- Type: function
- Signature: `case: Mapping[str, Any], label: Mapping[str, Any], constraints: PolicyConstraints | None=None`
- Direct static callees: `_enum`, `_lifecycle_payload`, `_string_set`, `_validate_lifecycle`, `any`, `append`, `bool`, `derive_policy_constraints`, `enumerate`, `float`, `get`, `intersection`, `isinstance`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.annotation_schema` — lines 548–634

- Source: [mind01/annotation_v3.py:548](../../../../mind01/annotation_v3.py#L548)
- Type: function
- Signature: `constraints: PolicyConstraints | None=None`
- Direct static callees: `_lifecycle_payload`, `list`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.annotation_agreement` — lines 637–650

- Source: [mind01/annotation_v3.py:637](../../../../mind01/annotation_v3.py#L637)
- Type: function
- Signature: `left: Mapping[str, Any], right: Mapping[str, Any]`
- Direct static callees: `_lifecycle_signature`, `all`, `get`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.semantic_label_projection` — lines 653–654

- Source: [mind01/annotation_v3.py:653](../../../../mind01/annotation_v3.py#L653)
- Type: function
- Signature: `label: Mapping[str, Any]`
- Direct static callees: `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3.label_sha256` — lines 657–659

- Source: [mind01/annotation_v3.py:657](../../../../mind01/annotation_v3.py#L657)
- Type: function
- Signature: `labels: list[Mapping[str, Any]]`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3._enum` — lines 662–664

- Source: [mind01/annotation_v3.py:662](../../../../mind01/annotation_v3.py#L662)
- Type: function
- Signature: `errors: list[str], label: Mapping[str, Any], field: str, values: set[str]`
- Direct static callees: `append`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3._string_set` — lines 667–676

- Source: [mind01/annotation_v3.py:667](../../../../mind01/annotation_v3.py#L667)
- Type: function
- Signature: `errors: list[str], value: Any, allowed: set[str], field: str`
- Direct static callees: `any`, `append`, `isinstance`, `issubset`, `len`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3._validate_lifecycle` — lines 679–692

- Source: [mind01/annotation_v3.py:679](../../../../mind01/annotation_v3.py#L679)
- Type: function
- Signature: `errors: list[str], value: Any, field: str`
- Direct static callees: `_string_set`, `append`, `dict`, `enumerate`, `get`, `isinstance`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3._lifecycle_payload` — lines 695–701

- Source: [mind01/annotation_v3.py:695](../../../../mind01/annotation_v3.py#L695)
- Type: function
- Signature: `lifecycle: tuple[tuple[str, tuple[str, ...]], ...]`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.annotation_v3._lifecycle_signature` — lines 704–721

- Source: [mind01/annotation_v3.py:704](../../../../mind01/annotation_v3.py#L704)
- Type: function
- Signature: `label: Mapping[str, Any]`
- Direct static callees: `add`, `dumps`, `get`, `product`, `set`, `sorted`, `str`, `tuple`, `update`
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

### Lines 8–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Implements module-level `Assign` behavior or data.

### Lines 11–11

Implements module-level `Assign` behavior or data.

### Lines 12–12

Implements module-level `Assign` behavior or data.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–14

Implements module-level `Assign` behavior or data.

### Lines 15–19

Implements module-level `Assign` behavior or data.

### Lines 20–26

Implements module-level `Assign` behavior or data.

### Lines 27–42

Implements module-level `Assign` behavior or data.

### Lines 43–46

Implements module-level `Assign` behavior or data.

### Lines 47–47

Implements module-level `Assign` behavior or data.

### Lines 48–48

Implements module-level `Assign` behavior or data.

### Lines 49–49

Implements module-level `Assign` behavior or data.

### Lines 50–50

Implements module-level `Assign` behavior or data.

### Lines 51–51

Implements module-level `Assign` behavior or data.

### Lines 52–63

Implements module-level `Assign` behavior or data.

### Lines 64–70

Implements module-level `Assign` behavior or data.

### Lines 71–73

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 74–103

Defines class `PolicyConstraints` and the behavior of its members.

### Lines 104–133

Defines class `PolicyConstraints` and the behavior of its members.

### Lines 134–149

Defines class `PolicyConstraints` and the behavior of its members.

### Lines 150–151

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 152–181

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 182–211

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 212–241

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 242–271

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 272–301

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 302–331

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 332–361

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 362–391

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 392–398

Defines `derive_policy_constraints` and its implementation control flow; direct static calls: PolicyConstraints, ValueError, append, bool, extend, get, isinstance, set, sorted, str, tuple.

### Lines 399–400

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 401–430

Defines `validate_annotation` and its implementation control flow; direct static calls: _enum, _lifecycle_payload, _string_set, _validate_lifecycle, any, append, bool, derive_policy_constraints, enumerate, float, get, intersection, isinstance, set, sorted.

### Lines 431–460

Defines `validate_annotation` and its implementation control flow; direct static calls: _enum, _lifecycle_payload, _string_set, _validate_lifecycle, any, append, bool, derive_policy_constraints, enumerate, float, get, intersection, isinstance, set, sorted.

### Lines 461–490

Defines `validate_annotation` and its implementation control flow; direct static calls: _enum, _lifecycle_payload, _string_set, _validate_lifecycle, any, append, bool, derive_policy_constraints, enumerate, float, get, intersection, isinstance, set, sorted.

### Lines 491–520

Defines `validate_annotation` and its implementation control flow; direct static calls: _enum, _lifecycle_payload, _string_set, _validate_lifecycle, any, append, bool, derive_policy_constraints, enumerate, float, get, intersection, isinstance, set, sorted.

### Lines 521–545

Defines `validate_annotation` and its implementation control flow; direct static calls: _enum, _lifecycle_payload, _string_set, _validate_lifecycle, any, append, bool, derive_policy_constraints, enumerate, float, get, intersection, isinstance, set, sorted.

### Lines 546–547

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 548–577

Defines `annotation_schema` and its implementation control flow; direct static calls: _lifecycle_payload, list, set, sorted.

### Lines 578–607

Defines `annotation_schema` and its implementation control flow; direct static calls: _lifecycle_payload, list, set, sorted.

### Lines 608–634

Defines `annotation_schema` and its implementation control flow; direct static calls: _lifecycle_payload, list, set, sorted.

### Lines 635–636

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 637–650

Defines `annotation_agreement` and its implementation control flow; direct static calls: _lifecycle_signature, all, get, set.

### Lines 651–652

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 653–654

Defines `semantic_label_projection` and its implementation control flow; direct static calls: sorted.

### Lines 655–656

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 657–659

Defines `label_sha256` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256.

### Lines 660–661

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 662–664

Defines `_enum` and its implementation control flow; direct static calls: append, get.

### Lines 665–666

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 667–676

Defines `_string_set` and its implementation control flow; direct static calls: any, append, isinstance, issubset, len, set.

### Lines 677–678

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 679–692

Defines `_validate_lifecycle` and its implementation control flow; direct static calls: _string_set, append, dict, enumerate, get, isinstance, set.

### Lines 693–694

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 695–701

Defines `_lifecycle_payload` and its implementation control flow; direct static calls: list.

### Lines 702–703

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 704–721

Defines `_lifecycle_signature` and its implementation control flow; direct static calls: add, dumps, get, product, set, sorted, str, tuple, update.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
