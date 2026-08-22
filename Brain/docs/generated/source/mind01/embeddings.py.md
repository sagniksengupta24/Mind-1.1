# `mind01/embeddings.py`

## File purpose

This agent runtime file is reviewed at snapshot `c37d303421c80c75a072d789f33663bd1eccc1f99820e9e0c49178d1deaaa13c`. It contains 38 lines.

## Imports and module state

- [mind01/embeddings.py:1](../../../../mind01/embeddings.py#L1) imports `__future__` / annotations.
- [mind01/embeddings.py:3](../../../../mind01/embeddings.py#L3) imports `json`.
- [mind01/embeddings.py:4](../../../../mind01/embeddings.py#L4) imports `math`.

## Symbols

### `mind01.embeddings.cosine_similarity` — lines 7–19

- Source: [mind01/embeddings.py:7](../../../../mind01/embeddings.py#L7)
- Type: function
- Signature: `left: list[float], right: list[float]`
- Direct static callees: `len`, `sqrt`, `zip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.embeddings.pack_vector` — lines 22–23

- Source: [mind01/embeddings.py:22](../../../../mind01/embeddings.py#L22)
- Type: function
- Signature: `vector: list[float]`
- Direct static callees: `dumps`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.embeddings.unpack_vector` — lines 26–38

- Source: [mind01/embeddings.py:26](../../../../mind01/embeddings.py#L26)
- Type: function
- Signature: `raw: str`
- Direct static callees: `float`, `isinstance`, `loads`
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

### Lines 5–6

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–19

Defines `cosine_similarity` and its implementation control flow; direct static calls: len, sqrt, zip.

### Lines 20–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–23

Defines `pack_vector` and its implementation control flow; direct static calls: dumps.

### Lines 24–25

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 26–38

Defines `unpack_vector` and its implementation control flow; direct static calls: float, isinstance, loads.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
