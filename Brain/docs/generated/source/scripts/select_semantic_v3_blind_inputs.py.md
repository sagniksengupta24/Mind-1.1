# `scripts/select_semantic_v3_blind_inputs.py`

## File purpose

This automation and release file is reviewed at snapshot `43a622d8340983d20df7448252535c0a088dc753689a3cec1ff70c92df2b43bb`. It contains 45 lines.

## Imports and module state

- [scripts/select_semantic_v3_blind_inputs.py:8](../../../../scripts/select_semantic_v3_blind_inputs.py#L8) imports `__future__` / annotations.
- [scripts/select_semantic_v3_blind_inputs.py:10](../../../../scripts/select_semantic_v3_blind_inputs.py#L10) imports `argparse`.
- [scripts/select_semantic_v3_blind_inputs.py:11](../../../../scripts/select_semantic_v3_blind_inputs.py#L11) imports `json`.
- [scripts/select_semantic_v3_blind_inputs.py:12](../../../../scripts/select_semantic_v3_blind_inputs.py#L12) imports `pathlib` / Path.
- [scripts/select_semantic_v3_blind_inputs.py:14](../../../../scripts/select_semantic_v3_blind_inputs.py#L14) imports `rc3_1_pipeline` / select_final.

## Symbols

### `scripts.select_semantic_v3_blind_inputs.main` — lines 17–41

- Source: [scripts/select_semantic_v3_blind_inputs.py:17](../../../../scripts/select_semantic_v3_blind_inputs.py#L17)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `dumps`, `parse_args`, `print`, `select_final`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–6

Implements module-level `Expr` behavior or data.

### Lines 7–7

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–41

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, dumps, parse_args, print, select_final.

### Lines 42–43

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 44–45

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
