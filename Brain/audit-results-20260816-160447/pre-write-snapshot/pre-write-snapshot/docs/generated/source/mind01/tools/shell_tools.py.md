# `mind01/tools/shell_tools.py`

## File purpose

This tool system file is reviewed at snapshot `5c3ca18ddaa5bfbcd900e65ce1bedd9759e7554631a566e9744e1e6939b52961`. It contains 211 lines.

## Imports and module state

- [mind01/tools/shell_tools.py:1](../../../../../mind01/tools/shell_tools.py#L1) imports `__future__` / annotations.
- [mind01/tools/shell_tools.py:3](../../../../../mind01/tools/shell_tools.py#L3) imports `os`.
- [mind01/tools/shell_tools.py:4](../../../../../mind01/tools/shell_tools.py#L4) imports `shlex`.
- [mind01/tools/shell_tools.py:5](../../../../../mind01/tools/shell_tools.py#L5) imports `shutil`.
- [mind01/tools/shell_tools.py:6](../../../../../mind01/tools/shell_tools.py#L6) imports `subprocess`.
- [mind01/tools/shell_tools.py:7](../../../../../mind01/tools/shell_tools.py#L7) imports `pathlib` / Path.
- [mind01/tools/shell_tools.py:8](../../../../../mind01/tools/shell_tools.py#L8) imports `typing` / Any.
- [mind01/tools/shell_tools.py:8](../../../../../mind01/tools/shell_tools.py#L8) imports `typing` / Dict.
- [mind01/tools/shell_tools.py:10](../../../../../mind01/tools/shell_tools.py#L10) imports `verify_tools` / ToolError.
- [mind01/tools/shell_tools.py:10](../../../../../mind01/tools/shell_tools.py#L10) imports `verify_tools` / ToolResult.
- [mind01/tools/shell_tools.py:10](../../../../../mind01/tools/shell_tools.py#L10) imports `verify_tools` / approve.
- [mind01/tools/shell_tools.py:10](../../../../../mind01/tools/shell_tools.py#L10) imports `verify_tools` / require_arg.

## Symbols

### `mind01.tools.shell_tools.ALLOWED_COMMANDS` — lines 13–13

- Source: [mind01/tools/shell_tools.py:13](../../../../../mind01/tools/shell_tools.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.DISALLOWED_EXECUTABLES` — lines 14–29

- Source: [mind01/tools/shell_tools.py:14](../../../../../mind01/tools/shell_tools.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.ALLOWED_GIT_SUBCOMMANDS` — lines 30–39

- Source: [mind01/tools/shell_tools.py:30](../../../../../mind01/tools/shell_tools.py#L30)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.BLOCKED_SHELL_TOKENS` — lines 40–40

- Source: [mind01/tools/shell_tools.py:40](../../../../../mind01/tools/shell_tools.py#L40)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.BLOCKED_SHELL_CHARS` — lines 41–41

- Source: [mind01/tools/shell_tools.py:41](../../../../../mind01/tools/shell_tools.py#L41)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.BLOCKED_PYTHON_ARGS` — lines 42–42

- Source: [mind01/tools/shell_tools.py:42](../../../../../mind01/tools/shell_tools.py#L42)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.DEFAULT_TIMEOUT_SECONDS` — lines 43–43

- Source: [mind01/tools/shell_tools.py:43](../../../../../mind01/tools/shell_tools.py#L43)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.MAX_TIMEOUT_SECONDS` — lines 44–44

- Source: [mind01/tools/shell_tools.py:44](../../../../../mind01/tools/shell_tools.py#L44)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.DEFAULT_OUTPUT_LIMIT` — lines 45–45

- Source: [mind01/tools/shell_tools.py:45](../../../../../mind01/tools/shell_tools.py#L45)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.MAX_OUTPUT_LIMIT` — lines 46–46

- Source: [mind01/tools/shell_tools.py:46](../../../../../mind01/tools/shell_tools.py#L46)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.run_command` — lines 49–116

- Source: [mind01/tools/shell_tools.py:49](../../../../../mind01/tools/shell_tools.py#L49)
- Type: function
- Signature: `registry: Any, args: Dict[str, Any]`
- Direct static callees: `Path`, `Popen`, `ToolError`, `ToolResult`, `approve`, `bounded_int`, `communicate`, `fromkeys`, `get`, `join`, `kill`, `killpg`, `mkdir`, `parse_allowed_command`, `require_arg`, `str`, `validate_workspace_command_paths`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.parse_allowed_command` — lines 119–181

- Source: [mind01/tools/shell_tools.py:119](../../../../../mind01/tools/shell_tools.py#L119)
- Type: function
- Signature: `command: str`
- Direct static callees: `Path`, `ToolError`, `any`, `join`, `len`, `lower`, `sorted`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.validate_workspace_command_paths` — lines 184–197

- Source: [mind01/tools/shell_tools.py:184](../../../../../mind01/tools/shell_tools.py#L184)
- Type: function
- Signature: `arguments: list[str], workspace: Path`
- Direct static callees: `Path`, `ToolError`, `expanduser`, `is_absolute`, `resolve`, `split`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.validate_command_is_allowed` — lines 200–201

- Source: [mind01/tools/shell_tools.py:200](../../../../../mind01/tools/shell_tools.py#L200)
- Type: function
- Signature: `command: str`
- Direct static callees: `parse_allowed_command`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.shell_tools.bounded_int` — lines 204–211

- Source: [mind01/tools/shell_tools.py:204](../../../../../mind01/tools/shell_tools.py#L204)
- Type: function
- Signature: `value: Any, minimum: int, maximum: int, name: str`
- Direct static callees: `ToolError`, `int`
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

Imports a dependency used by this module.

### Lines 11–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–29

Implements module-level `Assign` behavior or data.

### Lines 30–39

Implements module-level `Assign` behavior or data.

### Lines 40–40

Implements module-level `Assign` behavior or data.

### Lines 41–41

Implements module-level `Assign` behavior or data.

### Lines 42–42

Implements module-level `Assign` behavior or data.

### Lines 43–43

Implements module-level `Assign` behavior or data.

### Lines 44–44

Implements module-level `Assign` behavior or data.

### Lines 45–45

Implements module-level `Assign` behavior or data.

### Lines 46–46

Implements module-level `Assign` behavior or data.

### Lines 47–48

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 49–78

Defines `run_command` and its implementation control flow; direct static calls: Path, Popen, ToolError, ToolResult, approve, bounded_int, communicate, fromkeys, get, join, kill, killpg, mkdir, parse_allowed_command, require_arg, str, validate_workspace_command_paths, which.

### Lines 79–108

Defines `run_command` and its implementation control flow; direct static calls: Path, Popen, ToolError, ToolResult, approve, bounded_int, communicate, fromkeys, get, join, kill, killpg, mkdir, parse_allowed_command, require_arg, str, validate_workspace_command_paths, which.

### Lines 109–116

Defines `run_command` and its implementation control flow; direct static calls: Path, Popen, ToolError, ToolResult, approve, bounded_int, communicate, fromkeys, get, join, kill, killpg, mkdir, parse_allowed_command, require_arg, str, validate_workspace_command_paths, which.

### Lines 117–118

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 119–148

Defines `parse_allowed_command` and its implementation control flow; direct static calls: Path, ToolError, any, join, len, lower, sorted, split.

### Lines 149–178

Defines `parse_allowed_command` and its implementation control flow; direct static calls: Path, ToolError, any, join, len, lower, sorted, split.

### Lines 179–181

Defines `parse_allowed_command` and its implementation control flow; direct static calls: Path, ToolError, any, join, len, lower, sorted, split.

### Lines 182–183

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 184–197

Defines `validate_workspace_command_paths` and its implementation control flow; direct static calls: Path, ToolError, expanduser, is_absolute, resolve, split, startswith.

### Lines 198–199

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 200–201

Defines `validate_command_is_allowed` and its implementation control flow; direct static calls: parse_allowed_command.

### Lines 202–203

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 204–211

Defines `bounded_int` and its implementation control flow; direct static calls: ToolError, int.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
