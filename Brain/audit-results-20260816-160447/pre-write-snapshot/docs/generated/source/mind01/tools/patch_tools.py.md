# `mind01/tools/patch_tools.py`

## File purpose

This tool system file is reviewed at snapshot `a063e2568cc8d569e6860cf5536036f800bd5429789a6d2b68c34c4492073c6c`. It contains 113 lines.

## Imports and module state

- [mind01/tools/patch_tools.py:1](../../../../../mind01/tools/patch_tools.py#L1) imports `__future__` / annotations.
- [mind01/tools/patch_tools.py:3](../../../../../mind01/tools/patch_tools.py#L3) imports `shutil`.
- [mind01/tools/patch_tools.py:4](../../../../../mind01/tools/patch_tools.py#L4) imports `subprocess`.
- [mind01/tools/patch_tools.py:5](../../../../../mind01/tools/patch_tools.py#L5) imports `tempfile`.
- [mind01/tools/patch_tools.py:6](../../../../../mind01/tools/patch_tools.py#L6) imports `pathlib` / Path.
- [mind01/tools/patch_tools.py:7](../../../../../mind01/tools/patch_tools.py#L7) imports `typing` / Any.
- [mind01/tools/patch_tools.py:7](../../../../../mind01/tools/patch_tools.py#L7) imports `typing` / Dict.
- [mind01/tools/patch_tools.py:9](../../../../../mind01/tools/patch_tools.py#L9) imports `file_safety` / FileSafetyError.
- [mind01/tools/patch_tools.py:9](../../../../../mind01/tools/patch_tools.py#L9) imports `file_safety` / ensure_text_file_safe.
- [mind01/tools/patch_tools.py:9](../../../../../mind01/tools/patch_tools.py#L9) imports `file_safety` / ensure_write_target_safe.
- [mind01/tools/patch_tools.py:10](../../../../../mind01/tools/patch_tools.py#L10) imports `patches` / PatchError.
- [mind01/tools/patch_tools.py:10](../../../../../mind01/tools/patch_tools.py#L10) imports `patches` / PatchProposal.
- [mind01/tools/patch_tools.py:11](../../../../../mind01/tools/patch_tools.py#L11) imports `shell_tools` / parse_allowed_command.
- [mind01/tools/patch_tools.py:12](../../../../../mind01/tools/patch_tools.py#L12) imports `verify_tools` / ToolError.
- [mind01/tools/patch_tools.py:12](../../../../../mind01/tools/patch_tools.py#L12) imports `verify_tools` / ToolResult.
- [mind01/tools/patch_tools.py:12](../../../../../mind01/tools/patch_tools.py#L12) imports `verify_tools` / require_arg.

## Symbols

### `mind01.tools.patch_tools.propose_write_file` — lines 15–26

- Source: [mind01/tools/patch_tools.py:15](../../../../../mind01/tools/patch_tools.py#L15)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `get`, `propose_write`, `require_arg`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.patch_tools.propose_edit_file` — lines 29–39

- Source: [mind01/tools/patch_tools.py:29](../../../../../mind01/tools/patch_tools.py#L29)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `get`, `propose_edit`, `require_arg`, `show`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.patch_tools.list_patches` — lines 42–43

- Source: [mind01/tools/patch_tools.py:42](../../../../../mind01/tools/patch_tools.py#L42)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolResult`, `render_list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.patch_tools.show_patch` — lines 46–51

- Source: [mind01/tools/patch_tools.py:46](../../../../../mind01/tools/patch_tools.py#L46)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `ToolResult`, `int`, `require_arg`, `show`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.patch_tools.test_patch` — lines 54–89

- Source: [mind01/tools/patch_tools.py:54](../../../../../mind01/tools/patch_tools.py#L54)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `Path`, `TemporaryDirectory`, `ToolError`, `ToolResult`, `apply_patch_proposal`, `copytree`, `get`, `ignore_patterns`, `int`, `parse_allowed_command`, `require_arg`, `run`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.patch_tools.apply_patch_proposal` — lines 92–113

- Source: [mind01/tools/patch_tools.py:92](../../../../../mind01/tools/patch_tools.py#L92)
- Type: function
- Signature: `workspace: Path, proposal: PatchProposal`
- Direct static callees: `ToolError`, `ensure_text_file_safe`, `ensure_write_target_safe`, `mkdir`, `read_text`, `replace`, `str`, `write_text`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–26

Defines `propose_write_file` and its implementation control flow; direct static calls: ToolError, ToolResult, get, propose_write, require_arg, str.

### Lines 27–28

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 29–39

Defines `propose_edit_file` and its implementation control flow; direct static calls: ToolError, ToolResult, get, propose_edit, require_arg, show, str.

### Lines 40–41

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 42–43

Defines `list_patches` and its implementation control flow; direct static calls: ToolResult, render_list.

### Lines 44–45

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 46–51

Defines `show_patch` and its implementation control flow; direct static calls: ToolError, ToolResult, int, require_arg, show, str.

### Lines 52–53

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 54–83

Defines `test_patch` and its implementation control flow; direct static calls: Path, TemporaryDirectory, ToolError, ToolResult, apply_patch_proposal, copytree, get, ignore_patterns, int, parse_allowed_command, require_arg, run, str.

### Lines 84–89

Defines `test_patch` and its implementation control flow; direct static calls: Path, TemporaryDirectory, ToolError, ToolResult, apply_patch_proposal, copytree, get, ignore_patterns, int, parse_allowed_command, require_arg, run, str.

### Lines 90–91

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 92–113

Defines `apply_patch_proposal` and its implementation control flow; direct static calls: ToolError, ensure_text_file_safe, ensure_write_target_safe, mkdir, read_text, replace, str, write_text.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
