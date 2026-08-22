# `tests/test_docs_rag.py`

## File purpose

This testing file is reviewed at snapshot `295bbebdcf5839b2afb778827c5458c89704395e19cdceea951db16c4300e340`. It contains 66 lines.

## Imports and module state

- [tests/test_docs_rag.py:1](../../../../tests/test_docs_rag.py#L1) imports `__future__` / annotations.
- [tests/test_docs_rag.py:3](../../../../tests/test_docs_rag.py#L3) imports `shutil`.
- [tests/test_docs_rag.py:4](../../../../tests/test_docs_rag.py#L4) imports `tempfile`.
- [tests/test_docs_rag.py:5](../../../../tests/test_docs_rag.py#L5) imports `pathlib` / Path.
- [tests/test_docs_rag.py:7](../../../../tests/test_docs_rag.py#L7) imports `mind01.rag` / DocStore.

## Symbols

### `tests.test_docs_rag.run_docs_rag_tests` — lines 10–62

- Source: [tests/test_docs_rag.py:10](../../../../tests/test_docs_rag.py#L10)
- Type: function
- Signature: `n/a`
- Direct static callees: `DocStore`, `Path`, `index_path`, `join`, `len`, `mkdir`, `mkdtemp`, `read_text`, `rmtree`, `search`, `stale_files`, `startswith`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.test_docs_rag.test_docs_rag_regressions` — lines 65–66

- Source: [tests/test_docs_rag.py:65](../../../../tests/test_docs_rag.py#L65)
- Type: function
- Signature: `n/a`
- Direct static callees: `run_docs_rag_tests`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–39

Defines `run_docs_rag_tests` and its implementation control flow; direct static calls: DocStore, Path, index_path, join, len, mkdir, mkdtemp, read_text, rmtree, search, stale_files, startswith, write_text.

### Lines 40–62

Defines `run_docs_rag_tests` and its implementation control flow; direct static calls: DocStore, Path, index_path, join, len, mkdir, mkdtemp, read_text, rmtree, search, stale_files, startswith, write_text.

### Lines 63–64

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 65–66

Defines `test_docs_rag_regressions` and its implementation control flow; direct static calls: run_docs_rag_tests.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
