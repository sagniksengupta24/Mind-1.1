# `mind01/intent.py`

## File purpose

This agent runtime file is reviewed at snapshot `25aacb119bac443c40adf9562b33b77a3b79c0e4a8386631eba831471b08791a`. It contains 242 lines.

## Imports and module state

- [mind01/intent.py:1](../../../../mind01/intent.py#L1) imports `__future__` / annotations.
- [mind01/intent.py:3](../../../../mind01/intent.py#L3) imports `hashlib`.
- [mind01/intent.py:4](../../../../mind01/intent.py#L4) imports `json`.
- [mind01/intent.py:5](../../../../mind01/intent.py#L5) imports `dataclasses` / dataclass.
- [mind01/intent.py:6](../../../../mind01/intent.py#L6) imports `enum` / Enum.
- [mind01/intent.py:7](../../../../mind01/intent.py#L7) imports `typing` / Any.
- [mind01/intent.py:7](../../../../mind01/intent.py#L7) imports `typing` / Mapping.

## Symbols

### `mind01.intent.MAX_REQUEST_CHARS` — lines 10–10

- Source: [mind01/intent.py:10](../../../../mind01/intent.py#L10)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.MAX_GOAL_CHARS` — lines 11–11

- Source: [mind01/intent.py:11](../../../../mind01/intent.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.MAX_SCOPE_ITEMS` — lines 12–12

- Source: [mind01/intent.py:12](../../../../mind01/intent.py#L12)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.MAX_SCOPE_ITEM_CHARS` — lines 13–13

- Source: [mind01/intent.py:13](../../../../mind01/intent.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.MAX_MISSING_FIELDS` — lines 14–14

- Source: [mind01/intent.py:14](../../../../mind01/intent.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.TaskClass` — lines 17–23

- Source: [mind01/intent.py:17](../../../../mind01/intent.py#L17)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.TargetKind` — lines 26–32

- Source: [mind01/intent.py:26](../../../../mind01/intent.py#L26)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.RiskLevel` — lines 35–39

- Source: [mind01/intent.py:35](../../../../mind01/intent.py#L35)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.AmbiguityLevel` — lines 42–45

- Source: [mind01/intent.py:42](../../../../mind01/intent.py#L42)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.ExpectedOutputMode` — lines 48–52

- Source: [mind01/intent.py:48](../../../../mind01/intent.py#L48)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.Capability` — lines 55–60

- Source: [mind01/intent.py:55](../../../../mind01/intent.py#L55)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.InterpretationIncidentCode` — lines 63–70

- Source: [mind01/intent.py:63](../../../../mind01/intent.py#L63)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.Ambiguity` — lines 74–95

- Source: [mind01/intent.py:74](../../../../mind01/intent.py#L74)
- Type: class
- Signature: `n/a`
- Direct static callees: `AmbiguityLevel`, `ValueError`, `_bounded_strings`, `_reject_extra`, `any`, `cls`, `dataclass`, `get`, `len`, `list`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.Ambiguity.__post_init__` — lines 78–84

- Source: [mind01/intent.py:78](../../../../mind01/intent.py#L78)
- Type: method
- Signature: `self`
- Direct static callees: `ValueError`, `any`, `len`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.Ambiguity.to_dict` — lines 86–87

- Source: [mind01/intent.py:86](../../../../mind01/intent.py#L86)
- Type: method
- Signature: `self`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.Ambiguity.from_dict` — lines 90–95

- Source: [mind01/intent.py:90](../../../../mind01/intent.py#L90)
- Type: method
- Signature: `cls, payload: Mapping[str, Any]`
- Direct static callees: `AmbiguityLevel`, `_bounded_strings`, `_reject_extra`, `cls`, `get`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.NormalizedIntent` — lines 99–199

- Source: [mind01/intent.py:99](../../../../mind01/intent.py#L99)
- Type: class
- Signature: `n/a`
- Direct static callees: `Capability`, `ExpectedOutputMode`, `InterpretationIncidentCode`, `RiskLevel`, `TargetKind`, `TaskClass`, `ValueError`, `_bounded_strings`, `_reject_extra`, `_strict_bool`, `any`, `cls`, `dataclass`, `from_dict`, `isinstance`, `join`, `len`, `list`, `set`, `sorted`, `startswith`, `str`, `to_dict`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.NormalizedIntent.__post_init__` — lines 120–138

- Source: [mind01/intent.py:120](../../../../mind01/intent.py#L120)
- Type: method
- Signature: `self`
- Direct static callees: `ValueError`, `any`, `len`, `set`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.NormalizedIntent.to_dict` — lines 140–161

- Source: [mind01/intent.py:140](../../../../mind01/intent.py#L140)
- Type: method
- Signature: `self`
- Direct static callees: `list`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.NormalizedIntent.from_dict` — lines 164–199

- Source: [mind01/intent.py:164](../../../../mind01/intent.py#L164)
- Type: method
- Signature: `cls, payload: Mapping[str, Any]`
- Direct static callees: `Capability`, `ExpectedOutputMode`, `InterpretationIncidentCode`, `RiskLevel`, `TargetKind`, `TaskClass`, `ValueError`, `_bounded_strings`, `_reject_extra`, `_strict_bool`, `cls`, `from_dict`, `isinstance`, `join`, `set`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent.intent_identity` — lines 202–219

- Source: [mind01/intent.py:202](../../../../mind01/intent.py#L202)
- Type: function
- Signature: `request: str, *, mode: str, granted_capabilities: tuple[Capability, ...], prior_inspection: bool`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `join`, `sha256`, `sorted`, `split`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent._reject_extra` — lines 222–225

- Source: [mind01/intent.py:222](../../../../mind01/intent.py#L222)
- Type: function
- Signature: `payload: Mapping[str, Any], allowed: set[str], label: str`
- Direct static callees: `ValueError`, `join`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent._bounded_strings` — lines 228–236

- Source: [mind01/intent.py:228](../../../../mind01/intent.py#L228)
- Type: function
- Signature: `value: Any, label: str`
- Direct static callees: `ValueError`, `append`, `isinstance`, `len`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.intent._strict_bool` — lines 239–242

- Source: [mind01/intent.py:239](../../../../mind01/intent.py#L239)
- Type: function
- Signature: `value: Any, label: str`
- Direct static callees: `ValueError`, `isinstance`
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

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–23

Defines class `TaskClass` and the behavior of its members.

### Lines 24–25

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 26–32

Defines class `TargetKind` and the behavior of its members.

### Lines 33–34

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 35–39

Defines class `RiskLevel` and the behavior of its members.

### Lines 40–41

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 42–45

Defines class `AmbiguityLevel` and the behavior of its members.

### Lines 46–47

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 48–52

Defines class `ExpectedOutputMode` and the behavior of its members.

### Lines 53–54

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 55–60

Defines class `Capability` and the behavior of its members.

### Lines 61–62

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 63–70

Defines class `InterpretationIncidentCode` and the behavior of its members.

### Lines 71–73

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 74–95

Defines class `Ambiguity` and the behavior of its members.

### Lines 96–98

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 99–128

Defines class `NormalizedIntent` and the behavior of its members.

### Lines 129–158

Defines class `NormalizedIntent` and the behavior of its members.

### Lines 159–188

Defines class `NormalizedIntent` and the behavior of its members.

### Lines 189–199

Defines class `NormalizedIntent` and the behavior of its members.

### Lines 200–201

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 202–219

Defines `intent_identity` and its implementation control flow; direct static calls: dumps, encode, hexdigest, join, sha256, sorted, split, strip.

### Lines 220–221

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 222–225

Defines `_reject_extra` and its implementation control flow; direct static calls: ValueError, join, set, sorted.

### Lines 226–227

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 228–236

Defines `_bounded_strings` and its implementation control flow; direct static calls: ValueError, append, isinstance, len.

### Lines 237–238

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 239–242

Defines `_strict_bool` and its implementation control flow; direct static calls: ValueError, isinstance.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
