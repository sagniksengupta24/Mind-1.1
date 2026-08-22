# `scripts/freeze_semantic_routing_v1.py`

## File purpose

This automation and release file is reviewed at snapshot `b37bcb1e1ae271d0430a5ffb5195efaa4f684f4d76b2adcdaff0a8935f7e9e71`. It contains 426 lines.

## Imports and module state

- [scripts/freeze_semantic_routing_v1.py:1](../../../../scripts/freeze_semantic_routing_v1.py#L1) imports `__future__` / annotations.
- [scripts/freeze_semantic_routing_v1.py:3](../../../../scripts/freeze_semantic_routing_v1.py#L3) imports `hashlib`.
- [scripts/freeze_semantic_routing_v1.py:4](../../../../scripts/freeze_semantic_routing_v1.py#L4) imports `json`.
- [scripts/freeze_semantic_routing_v1.py:5](../../../../scripts/freeze_semantic_routing_v1.py#L5) imports `re`.
- [scripts/freeze_semantic_routing_v1.py:6](../../../../scripts/freeze_semantic_routing_v1.py#L6) imports `pathlib` / Path.
- [scripts/freeze_semantic_routing_v1.py:7](../../../../scripts/freeze_semantic_routing_v1.py#L7) imports `typing` / Any.

## Symbols

### `scripts.freeze_semantic_routing_v1.ROOT` — lines 10–10

- Source: [scripts/freeze_semantic_routing_v1.py:10](../../../../scripts/freeze_semantic_routing_v1.py#L10)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.OUTPUT` — lines 11–11

- Source: [scripts/freeze_semantic_routing_v1.py:11](../../../../scripts/freeze_semantic_routing_v1.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.TOOLS` — lines 13–37

- Source: [scripts/freeze_semantic_routing_v1.py:13](../../../../scripts/freeze_semantic_routing_v1.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.WRITE_TOOLS` — lines 38–38

- Source: [scripts/freeze_semantic_routing_v1.py:38](../../../../scripts/freeze_semantic_routing_v1.py#L38)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.MODES` — lines 39–39

- Source: [scripts/freeze_semantic_routing_v1.py:39](../../../../scripts/freeze_semantic_routing_v1.py#L39)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.PARTITIONS` — lines 40–47

- Source: [scripts/freeze_semantic_routing_v1.py:40](../../../../scripts/freeze_semantic_routing_v1.py#L40)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.expected` — lines 50–69

- Source: [scripts/freeze_semantic_routing_v1.py:50](../../../../scripts/freeze_semantic_routing_v1.py#L50)
- Type: function
- Signature: `intent_type: str, task_class: str, specialist: str, family: str, tools: list[str], response_mode: str, mutation: bool, risk: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.CORE` — lines 72–103

- Source: [scripts/freeze_semantic_routing_v1.py:72](../../../../scripts/freeze_semantic_routing_v1.py#L72)
- Type: constant
- Signature: `n/a`
- Direct static callees: `expected`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.CONTEXTS` — lines 105–118

- Source: [scripts/freeze_semantic_routing_v1.py:105](../../../../scripts/freeze_semantic_routing_v1.py#L105)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.capabilities` — lines 121–122

- Source: [scripts/freeze_semantic_routing_v1.py:121](../../../../scripts/freeze_semantic_routing_v1.py#L121)
- Type: function
- Signature: `overrides: dict[str, bool]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.core_cases` — lines 125–149

- Source: [scripts/freeze_semantic_routing_v1.py:125](../../../../scripts/freeze_semantic_routing_v1.py#L125)
- Type: function
- Signature: `partition: str, count: int, offset: int`
- Direct static callees: `append`, `capabilities`, `format`, `len`, `range`, `replace`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.adversarial_cases` — lines 152–190

- Source: [scripts/freeze_semantic_routing_v1.py:152](../../../../scripts/freeze_semantic_routing_v1.py#L152)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `capabilities`, `expected`, `format`, `len`, `range`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.capability_cases` — lines 193–221

- Source: [scripts/freeze_semantic_routing_v1.py:193](../../../../scripts/freeze_semantic_routing_v1.py#L193)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `capabilities`, `expected`, `format`, `get`, `len`, `range`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.ambiguity_cases` — lines 224–263

- Source: [scripts/freeze_semantic_routing_v1.py:224](../../../../scripts/freeze_semantic_routing_v1.py#L224)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `capabilities`, `expected`, `range`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.blind_cases` — lines 266–283

- Source: [scripts/freeze_semantic_routing_v1.py:266](../../../../scripts/freeze_semantic_routing_v1.py#L266)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `capabilities`, `format`, `len`, `range`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.schema` — lines 286–325

- Source: [scripts/freeze_semantic_routing_v1.py:286](../../../../scripts/freeze_semantic_routing_v1.py#L286)
- Type: function
- Signature: `n/a`
- Direct static callees: `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.tokens` — lines 328–329

- Source: [scripts/freeze_semantic_routing_v1.py:328](../../../../scripts/freeze_semantic_routing_v1.py#L328)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `findall`, `lower`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.validate_partition` — lines 332–368

- Source: [scripts/freeze_semantic_routing_v1.py:332](../../../../scripts/freeze_semantic_routing_v1.py#L332)
- Type: function
- Signature: `partition: str, cases: list[dict[str, Any]]`
- Direct static callees: `ValueError`, `add`, `append`, `len`, `set`, `sorted`, `tokens`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.write_json` — lines 371–372

- Source: [scripts/freeze_semantic_routing_v1.py:371](../../../../scripts/freeze_semantic_routing_v1.py#L371)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v1.main` — lines 375–422

- Source: [scripts/freeze_semantic_routing_v1.py:375](../../../../scripts/freeze_semantic_routing_v1.py#L375)
- Type: function
- Signature: `n/a`
- Direct static callees: `adversarial_cases`, `ambiguity_cases`, `blind_cases`, `capability_cases`, `core_cases`, `dumps`, `get`, `glob`, `hexdigest`, `isinstance`, `items`, `len`, `loads`, `mkdir`, `print`, `read_bytes`, `schema`, `sha256`, `sorted`, `str`, `sum`, `validate_partition`, `values`, `write_json`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–37

Implements module-level `Assign` behavior or data.

### Lines 38–38

Implements module-level `Assign` behavior or data.

### Lines 39–39

Implements module-level `Assign` behavior or data.

### Lines 40–47

Implements module-level `Assign` behavior or data.

### Lines 48–49

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 50–69

Defines `expected` and its implementation control flow; direct static calls: none resolved.

### Lines 70–71

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 72–101

Implements module-level `AnnAssign` behavior or data.

### Lines 102–103

Implements module-level `AnnAssign` behavior or data.

### Lines 104–104

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 105–118

Implements module-level `Assign` behavior or data.

### Lines 119–120

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 121–122

Defines `capabilities` and its implementation control flow; direct static calls: none resolved.

### Lines 123–124

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 125–149

Defines `core_cases` and its implementation control flow; direct static calls: append, capabilities, format, len, range, replace, sorted.

### Lines 150–151

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 152–181

Defines `adversarial_cases` and its implementation control flow; direct static calls: append, capabilities, expected, format, len, range, sorted.

### Lines 182–190

Defines `adversarial_cases` and its implementation control flow; direct static calls: append, capabilities, expected, format, len, range, sorted.

### Lines 191–192

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 193–221

Defines `capability_cases` and its implementation control flow; direct static calls: append, capabilities, expected, format, get, len, range, sorted.

### Lines 222–223

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 224–253

Defines `ambiguity_cases` and its implementation control flow; direct static calls: append, capabilities, expected, range, sorted.

### Lines 254–263

Defines `ambiguity_cases` and its implementation control flow; direct static calls: append, capabilities, expected, range, sorted.

### Lines 264–265

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 266–283

Defines `blind_cases` and its implementation control flow; direct static calls: append, capabilities, format, len, range.

### Lines 284–285

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 286–315

Defines `schema` and its implementation control flow; direct static calls: sorted.

### Lines 316–325

Defines `schema` and its implementation control flow; direct static calls: sorted.

### Lines 326–327

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 328–329

Defines `tokens` and its implementation control flow; direct static calls: findall, lower, set.

### Lines 330–331

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 332–361

Defines `validate_partition` and its implementation control flow; direct static calls: ValueError, add, append, len, set, sorted, tokens.

### Lines 362–368

Defines `validate_partition` and its implementation control flow; direct static calls: ValueError, add, append, len, set, sorted, tokens.

### Lines 369–370

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 371–372

Defines `write_json` and its implementation control flow; direct static calls: dumps, write_text.

### Lines 373–374

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 375–404

Defines `main` and its implementation control flow; direct static calls: adversarial_cases, ambiguity_cases, blind_cases, capability_cases, core_cases, dumps, get, glob, hexdigest, isinstance, items, len, loads, mkdir, print, read_bytes, schema, sha256, sorted, str, sum, validate_partition, values, write_json.

### Lines 405–422

Defines `main` and its implementation control flow; direct static calls: adversarial_cases, ambiguity_cases, blind_cases, capability_cases, core_cases, dumps, get, glob, hexdigest, isinstance, items, len, loads, mkdir, print, read_bytes, schema, sha256, sorted, str, sum, validate_partition, values, write_json.

### Lines 423–424

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 425–426

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
