# `scripts/build_release.py`

## File purpose

This automation and release file is reviewed at snapshot `f94ff9bfe27aa52d176e20cbfd9661e80190dfc0b97f04176ef1a9ff18a991e1`. It contains 119 lines.

## Imports and module state

- [scripts/build_release.py:1](../../../../scripts/build_release.py#L1) imports `__future__` / annotations.
- [scripts/build_release.py:3](../../../../scripts/build_release.py#L3) imports `argparse`.
- [scripts/build_release.py:4](../../../../scripts/build_release.py#L4) imports `re`.
- [scripts/build_release.py:5](../../../../scripts/build_release.py#L5) imports `shutil`.
- [scripts/build_release.py:6](../../../../scripts/build_release.py#L6) imports `tempfile`.
- [scripts/build_release.py:7](../../../../scripts/build_release.py#L7) imports `zipfile`.
- [scripts/build_release.py:8](../../../../scripts/build_release.py#L8) imports `pathlib` / Path.

## Symbols

### `scripts.build_release.ROOT` — lines 10–10

- Source: [scripts/build_release.py:10](../../../../scripts/build_release.py#L10)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release._VERSION_TEXT` — lines 11–11

- Source: [scripts/build_release.py:11](../../../../scripts/build_release.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release._VERSION_MATCH` — lines 12–12

- Source: [scripts/build_release.py:12](../../../../scripts/build_release.py#L12)
- Type: constant
- Signature: `n/a`
- Direct static callees: `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.__version__` — lines 15–15

- Source: [scripts/build_release.py:15](../../../../scripts/build_release.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: `group`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.ROOT_FILES` — lines 17–27

- Source: [scripts/build_release.py:17](../../../../scripts/build_release.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.SOURCE_DIRS` — lines 28–28

- Source: [scripts/build_release.py:28](../../../../scripts/build_release.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.EVAL_FILES` — lines 29–43

- Source: [scripts/build_release.py:29](../../../../scripts/build_release.py#L29)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.EXCLUDED_PARTS` — lines 44–51

- Source: [scripts/build_release.py:44](../../../../scripts/build_release.py#L44)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.EXCLUDED_SUFFIXES` — lines 52–52

- Source: [scripts/build_release.py:52](../../../../scripts/build_release.py#L52)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.should_copy` — lines 55–60

- Source: [scripts/build_release.py:55](../../../../scripts/build_release.py#L55)
- Type: function
- Signature: `path: Path`
- Direct static callees: `any`, `endswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.copy_tree` — lines 63–73

- Source: [scripts/build_release.py:63](../../../../scripts/build_release.py#L63)
- Type: function
- Signature: `source: Path, target: Path`
- Direct static callees: `copy2`, `is_dir`, `is_file`, `mkdir`, `relative_to`, `rglob`, `should_copy`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.build_release` — lines 76–102

- Source: [scripts/build_release.py:76](../../../../scripts/build_release.py#L76)
- Type: function
- Signature: `root: Path, output_dir: Path`
- Direct static callees: `Path`, `TemporaryDirectory`, `ZipFile`, `copy2`, `copy_tree`, `exists`, `is_file`, `mkdir`, `relative_to`, `rglob`, `sorted`, `unlink`, `write`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.build_release.main` — lines 105–115

- Source: [scripts/build_release.py:105](../../../../scripts/build_release.py#L105)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `add_argument`, `build_release`, `expanduser`, `is_absolute`, `parse_args`, `print`, `resolve`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Implements module-level `Assign` behavior or data.

### Lines 11–11

Implements module-level `Assign` behavior or data.

### Lines 12–12

Implements module-level `Assign` behavior or data.

### Lines 13–14

Implements module-level `If` behavior or data.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–27

Implements module-level `Assign` behavior or data.

### Lines 28–28

Implements module-level `Assign` behavior or data.

### Lines 29–43

Implements module-level `Assign` behavior or data.

### Lines 44–51

Implements module-level `Assign` behavior or data.

### Lines 52–52

Implements module-level `Assign` behavior or data.

### Lines 53–54

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 55–60

Defines `should_copy` and its implementation control flow; direct static calls: any, endswith.

### Lines 61–62

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 63–73

Defines `copy_tree` and its implementation control flow; direct static calls: copy2, is_dir, is_file, mkdir, relative_to, rglob, should_copy.

### Lines 74–75

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 76–102

Defines `build_release` and its implementation control flow; direct static calls: Path, TemporaryDirectory, ZipFile, copy2, copy_tree, exists, is_file, mkdir, relative_to, rglob, sorted, unlink, write.

### Lines 103–104

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 105–115

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, add_argument, build_release, expanduser, is_absolute, parse_args, print, resolve.

### Lines 116–117

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 118–119

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
