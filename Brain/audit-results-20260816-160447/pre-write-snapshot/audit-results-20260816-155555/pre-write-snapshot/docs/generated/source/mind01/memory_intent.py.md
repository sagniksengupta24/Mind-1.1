# `mind01/memory_intent.py`

## File purpose

This sessions memory and RAG file is reviewed at snapshot `b6ff36f5ea8dfac7b10289881f35f0bf1cefd90607f0da9f68390f747e8e83f0`. It contains 73 lines.

## Imports and module state

- [mind01/memory_intent.py:1](../../../../mind01/memory_intent.py#L1) imports `__future__` / annotations.
- [mind01/memory_intent.py:3](../../../../mind01/memory_intent.py#L3) imports `re`.
- [mind01/memory_intent.py:4](../../../../mind01/memory_intent.py#L4) imports `dataclasses` / dataclass.
- [mind01/memory_intent.py:5](../../../../mind01/memory_intent.py#L5) imports `typing` / Optional.

## Symbols

### `mind01.memory_intent.MemoryIntent` — lines 9–13

- Source: [mind01/memory_intent.py:9](../../../../mind01/memory_intent.py#L9)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.REMEMBER_RE` — lines 16–19

- Source: [mind01/memory_intent.py:16](../../../../mind01/memory_intent.py#L16)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.RECALL_RE` — lines 20–23

- Source: [mind01/memory_intent.py:20](../../../../mind01/memory_intent.py#L20)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.detect_memory_intent` — lines 26–44

- Source: [mind01/memory_intent.py:26](../../../../mind01/memory_intent.py#L26)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `MemoryIntent`, `clean_recall_query`, `clean_remember_value`, `group`, `lower`, `normalize_key`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.normalize_key` — lines 47–55

- Source: [mind01/memory_intent.py:47](../../../../mind01/memory_intent.py#L47)
- Type: function
- Signature: `raw: str`
- Direct static callees: `lower`, `startswith`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.clean_remember_value` — lines 58–63

- Source: [mind01/memory_intent.py:58](../../../../mind01/memory_intent.py#L58)
- Type: function
- Signature: `raw: str`
- Direct static callees: `split`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.memory_intent.clean_recall_query` — lines 66–73

- Source: [mind01/memory_intent.py:66](../../../../mind01/memory_intent.py#L66)
- Type: function
- Signature: `raw: str`
- Direct static callees: `lower`, `split`, `startswith`, `strip`
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

### Lines 6–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–13

Defines class `MemoryIntent` and the behavior of its members.

### Lines 14–15

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 16–19

Implements module-level `Assign` behavior or data.

### Lines 20–23

Implements module-level `Assign` behavior or data.

### Lines 24–25

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 26–44

Defines `detect_memory_intent` and its implementation control flow; direct static calls: MemoryIntent, clean_recall_query, clean_remember_value, group, lower, normalize_key, search.

### Lines 45–46

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 47–55

Defines `normalize_key` and its implementation control flow; direct static calls: lower, startswith, strip.

### Lines 56–57

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 58–63

Defines `clean_remember_value` and its implementation control flow; direct static calls: split, strip.

### Lines 64–65

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 66–73

Defines `clean_recall_query` and its implementation control flow; direct static calls: lower, split, startswith, strip.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
