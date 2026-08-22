# `mind01/tools/file_tools.py`

## File purpose

This tool system file is reviewed at snapshot `16de8c48d0ecc977ba7e5109d11d5fe87ea855e470308ca677885e8310a79801`. It contains 165 lines.

## Imports and module state

- [mind01/tools/file_tools.py:1](../../../../../mind01/tools/file_tools.py#L1) imports `__future__` / annotations.
- [mind01/tools/file_tools.py:3](../../../../../mind01/tools/file_tools.py#L3) imports `typing` / Any.
- [mind01/tools/file_tools.py:3](../../../../../mind01/tools/file_tools.py#L3) imports `typing` / Dict.
- [mind01/tools/file_tools.py:3](../../../../../mind01/tools/file_tools.py#L3) imports `typing` / Iterable.
- [mind01/tools/file_tools.py:5](../../../../../mind01/tools/file_tools.py#L5) imports `file_safety` / FileSafetyError.
- [mind01/tools/file_tools.py:5](../../../../../mind01/tools/file_tools.py#L5) imports `file_safety` / ensure_text_file_safe.
- [mind01/tools/file_tools.py:5](../../../../../mind01/tools/file_tools.py#L5) imports `file_safety` / ensure_write_target_safe.
- [mind01/tools/file_tools.py:5](../../../../../mind01/tools/file_tools.py#L5) imports `file_safety` / read_text_file_safe.
- [mind01/tools/file_tools.py:5](../../../../../mind01/tools/file_tools.py#L5) imports `file_safety` / relative_path.
- [mind01/tools/file_tools.py:12](../../../../../mind01/tools/file_tools.py#L12) imports `receipts` / ReceiptContext.
- [mind01/tools/file_tools.py:12](../../../../../mind01/tools/file_tools.py#L12) imports `receipts` / ReceiptError.
- [mind01/tools/file_tools.py:12](../../../../../mind01/tools/file_tools.py#L12) imports `receipts` / perform_verified_content_mutation.
- [mind01/tools/file_tools.py:13](../../../../../mind01/tools/file_tools.py#L13) imports `security` / redact_secrets.
- [mind01/tools/file_tools.py:14](../../../../../mind01/tools/file_tools.py#L14) imports `verify_tools` / ToolError.
- [mind01/tools/file_tools.py:14](../../../../../mind01/tools/file_tools.py#L14) imports `verify_tools` / ToolResult.
- [mind01/tools/file_tools.py:14](../../../../../mind01/tools/file_tools.py#L14) imports `verify_tools` / approve.
- [mind01/tools/file_tools.py:14](../../../../../mind01/tools/file_tools.py#L14) imports `verify_tools` / require_arg.
- [mind01/tools/file_tools.py:14](../../../../../mind01/tools/file_tools.py#L14) imports `verify_tools` / require_write_permission.

## Symbols

### `mind01.tools.file_tools.TEXT_SUFFIXES` — lines 17–34

- Source: [mind01/tools/file_tools.py:17](../../../../../mind01/tools/file_tools.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.SKIP_DIRS` — lines 36–36

- Source: [mind01/tools/file_tools.py:36](../../../../../mind01/tools/file_tools.py#L36)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.list_files` — lines 39–52

- Source: [mind01/tools/file_tools.py:39](../../../../../mind01/tools/file_tools.py#L39)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `append`, `exists`, `get`, `is_dir`, `is_file`, `join`, `len`, `relative_to`, `resolve_path`, `rglob`, `set`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.read_file` — lines 55–61

- Source: [mind01/tools/file_tools.py:55](../../../../../mind01/tools/file_tools.py#L55)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `read_text_file_safe`, `redact_secrets`, `require_arg`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.search_code` — lines 64–87

- Source: [mind01/tools/file_tools.py:64](../../../../../mind01/tools/file_tools.py#L64)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `append`, `ensure_text_file_safe`, `enumerate`, `get`, `is_file`, `iter_text_files`, `join`, `len`, `lower`, `read_text`, `redact_secrets`, `relative_path`, `require_arg`, `resolve_path`, `splitlines`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.write_file` — lines 90–118

- Source: [mind01/tools/file_tools.py:90](../../../../../mind01/tools/file_tools.py#L90)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ReceiptContext`, `ToolError`, `ToolResult`, `approve`, `ensure_write_target_safe`, `perform_verified_content_mutation`, `relative_to`, `require_arg`, `require_write_permission`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.edit_file` — lines 121–156

- Source: [mind01/tools/file_tools.py:121](../../../../../mind01/tools/file_tools.py#L121)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ReceiptContext`, `ToolError`, `ToolResult`, `approve`, `ensure_text_file_safe`, `ensure_write_target_safe`, `perform_verified_content_mutation`, `read_text`, `relative_to`, `replace`, `require_arg`, `require_write_permission`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.file_tools.iter_text_files` — lines 159–165

- Source: [mind01/tools/file_tools.py:159](../../../../../mind01/tools/file_tools.py#L159)
- Type: function
- Signature: `root: Path`
- Direct static callees: `is_dir`, `is_file`, `lower`, `rglob`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 5–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–34

Implements module-level `Assign` behavior or data.

### Lines 35–35

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 36–36

Implements module-level `Assign` behavior or data.

### Lines 37–38

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 39–52

Defines `list_files` and its implementation control flow; direct static calls: ToolError, ToolResult, append, exists, get, is_dir, is_file, join, len, relative_to, resolve_path, rglob, set, sorted, str.

### Lines 53–54

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 55–61

Defines `read_file` and its implementation control flow; direct static calls: ToolError, ToolResult, read_text_file_safe, redact_secrets, require_arg, str.

### Lines 62–63

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 64–87

Defines `search_code` and its implementation control flow; direct static calls: ToolError, ToolResult, append, ensure_text_file_safe, enumerate, get, is_file, iter_text_files, join, len, lower, read_text, redact_secrets, relative_path, require_arg, resolve_path, splitlines, str.

### Lines 88–89

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 90–118

Defines `write_file` and its implementation control flow; direct static calls: ReceiptContext, ToolError, ToolResult, approve, ensure_write_target_safe, perform_verified_content_mutation, relative_to, require_arg, require_write_permission, str.

### Lines 119–120

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 121–150

Defines `edit_file` and its implementation control flow; direct static calls: ReceiptContext, ToolError, ToolResult, approve, ensure_text_file_safe, ensure_write_target_safe, perform_verified_content_mutation, read_text, relative_to, replace, require_arg, require_write_permission, str.

### Lines 151–156

Defines `edit_file` and its implementation control flow; direct static calls: ReceiptContext, ToolError, ToolResult, approve, ensure_text_file_safe, ensure_write_target_safe, perform_verified_content_mutation, read_text, relative_to, replace, require_arg, require_write_permission, str.

### Lines 157–158

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 159–165

Defines `iter_text_files` and its implementation control flow; direct static calls: is_dir, is_file, lower, rglob, set.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
