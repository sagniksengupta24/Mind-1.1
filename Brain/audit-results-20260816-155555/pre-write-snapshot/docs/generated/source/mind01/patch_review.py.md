# `mind01/patch_review.py`

## File purpose

This filesystem and mutations file is reviewed at snapshot `cc4337699c470f835eaab33bc661077918495e73f3ceb5f9edde592392173d67`. It contains 80 lines.

## Imports and module state

- [mind01/patch_review.py:1](../../../../mind01/patch_review.py#L1) imports `__future__` / annotations.
- [mind01/patch_review.py:3](../../../../mind01/patch_review.py#L3) imports `re`.
- [mind01/patch_review.py:4](../../../../mind01/patch_review.py#L4) imports `dataclasses` / asdict.
- [mind01/patch_review.py:4](../../../../mind01/patch_review.py#L4) imports `dataclasses` / dataclass.
- [mind01/patch_review.py:5](../../../../mind01/patch_review.py#L5) imports `pathlib` / PurePosixPath.

## Symbols

### `mind01.patch_review.PatchFinding` — lines 9–16

- Source: [mind01/patch_review.py:9](../../../../mind01/patch_review.py#L9)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.PatchFinding.to_dict` — lines 15–16

- Source: [mind01/patch_review.py:15](../../../../mind01/patch_review.py#L15)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.PatchReviewResult` — lines 20–28

- Source: [mind01/patch_review.py:20](../../../../mind01/patch_review.py#L20)
- Type: class
- Signature: `n/a`
- Direct static callees: `any`, `dataclass`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.PatchReviewResult.blocking` — lines 24–25

- Source: [mind01/patch_review.py:24](../../../../mind01/patch_review.py#L24)
- Type: method
- Signature: `self`
- Direct static callees: `any`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.PatchReviewResult.to_dicts` — lines 27–28

- Source: [mind01/patch_review.py:27](../../../../mind01/patch_review.py#L27)
- Type: method
- Signature: `self`
- Direct static callees: `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.review_patch` — lines 31–76

- Source: [mind01/patch_review.py:31](../../../../mind01/patch_review.py#L31)
- Type: function
- Signature: `*, diff_text: str, changed_files: list[str], expected_paths: list[str] | None=None, protected_paths: list[str] | None=None`
- Direct static callees: `PatchFinding`, `PatchReviewResult`, `PurePosixPath`, `any`, `append`, `endswith`, `len`, `lower`, `normalise_path`, `rstrip`, `search`, `splitlines`, `startswith`, `strip`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.patch_review.normalise_path` — lines 79–80

- Source: [mind01/patch_review.py:79](../../../../mind01/patch_review.py#L79)
- Type: function
- Signature: `path: str`
- Direct static callees: `replace`, `strip`
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

### Lines 9–16

Defines class `PatchFinding` and the behavior of its members.

### Lines 17–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–28

Defines class `PatchReviewResult` and the behavior of its members.

### Lines 29–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–60

Defines `review_patch` and its implementation control flow; direct static calls: PatchFinding, PatchReviewResult, PurePosixPath, any, append, endswith, len, lower, normalise_path, rstrip, search, splitlines, startswith, strip, sum.

### Lines 61–76

Defines `review_patch` and its implementation control flow; direct static calls: PatchFinding, PatchReviewResult, PurePosixPath, any, append, endswith, len, lower, normalise_path, rstrip, search, splitlines, startswith, strip, sum.

### Lines 77–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–80

Defines `normalise_path` and its implementation control flow; direct static calls: replace, strip.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
