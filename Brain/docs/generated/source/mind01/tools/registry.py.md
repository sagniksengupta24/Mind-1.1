# `mind01/tools/registry.py`

## File purpose

This tool system file is reviewed at snapshot `55cef7b1b26fa3d7771bd70019369d388ab56997d96889b1c972855577373954`. It contains 194 lines.

## Imports and module state

- [mind01/tools/registry.py:1](../../../../../mind01/tools/registry.py#L1) imports `__future__` / annotations.
- [mind01/tools/registry.py:3](../../../../../mind01/tools/registry.py#L3) imports `time`.
- [mind01/tools/registry.py:4](../../../../../mind01/tools/registry.py#L4) imports `pathlib` / Path.
- [mind01/tools/registry.py:5](../../../../../mind01/tools/registry.py#L5) imports `typing` / Any.
- [mind01/tools/registry.py:5](../../../../../mind01/tools/registry.py#L5) imports `typing` / Callable.
- [mind01/tools/registry.py:5](../../../../../mind01/tools/registry.py#L5) imports `typing` / Dict.
- [mind01/tools/registry.py:7](../../../../../mind01/tools/registry.py#L7) imports `code_index` / CodeIndex.
- [mind01/tools/registry.py:8](../../../../../mind01/tools/registry.py#L8) imports `file_safety` / FileSafetyError.
- [mind01/tools/registry.py:8](../../../../../mind01/tools/registry.py#L8) imports `file_safety` / resolve_workspace_path.
- [mind01/tools/registry.py:9](../../../../../mind01/tools/registry.py#L9) imports `memory` / MemoryStore.
- [mind01/tools/registry.py:10](../../../../../mind01/tools/registry.py#L10) imports `project_knowledge` / ProjectKnowledgeStore.
- [mind01/tools/registry.py:11](../../../../../mind01/tools/registry.py#L11) imports `modes` / AgentMode.
- [mind01/tools/registry.py:11](../../../../../mind01/tools/registry.py#L11) imports `modes` / parse_agent_mode.
- [mind01/tools/registry.py:12](../../../../../mind01/tools/registry.py#L12) imports `patches` / PatchStore.
- [mind01/tools/registry.py:13](../../../../../mind01/tools/registry.py#L13) imports `rag` / DocStore.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / TraceError.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / TraceStore.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / duration_ms.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / extract_receipt_id.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / sanitize_args.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / summarize_result.
- [mind01/tools/registry.py:14](../../../../../mind01/tools/registry.py#L14) imports `traces` / trace_event_base.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / code_index_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / docs_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / file_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / knowledge_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / memory_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / patch_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / project_tools.
- [mind01/tools/registry.py:23](../../../../../mind01/tools/registry.py#L23) imports `` / shell_tools.
- [mind01/tools/registry.py:24](../../../../../mind01/tools/registry.py#L24) imports `schemas` / SCHEMA_BY_NAME.
- [mind01/tools/registry.py:24](../../../../../mind01/tools/registry.py#L24) imports `schemas` / ToolSchema.
- [mind01/tools/registry.py:24](../../../../../mind01/tools/registry.py#L24) imports `schemas` / validate_schema_registry.
- [mind01/tools/registry.py:24](../../../../../mind01/tools/registry.py#L24) imports `schemas` / validate_tool_args.
- [mind01/tools/registry.py:25](../../../../../mind01/tools/registry.py#L25) imports `verify_tools` / ToolError.
- [mind01/tools/registry.py:25](../../../../../mind01/tools/registry.py#L25) imports `verify_tools` / ToolResult.

## Symbols

### `mind01.tools.registry.ToolHandler` — lines 28–28

- Source: [mind01/tools/registry.py:28](../../../../../mind01/tools/registry.py#L28)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry` — lines 31–194

- Source: [mind01/tools/registry.py:31](../../../../../mind01/tools/registry.py#L31)
- Type: class
- Signature: `n/a`
- Direct static callees: `CodeIndex`, `DocStore`, `MemoryStore`, `PatchStore`, `ProjectKnowledgeStore`, `ToolError`, `TraceStore`, `_append_trace`, `_enforce_schema_policy`, `append`, `dict`, `duration_ms`, `extract_receipt_id`, `isinstance`, `join`, `parse_agent_mode`, `perf_counter`, `registered_tools`, `resolve`, `resolve_workspace_path`, `sanitize_args`, `sorted`, `str`, `summarize_result`, `trace_event_base`, `update`, `validate_schema_registry`, `validate_tool_args`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry.__init__` — lines 32–80

- Source: [mind01/tools/registry.py:32](../../../../../mind01/tools/registry.py#L32)
- Type: method
- Signature: `self, workspace: Path, yes: bool=False, allow_write: bool=False, allow_shell: bool=False, mode: str | AgentMode=AgentMode.READ_ONLY, session_id: str | None=None, model_name: str | None=None`
- Direct static callees: `CodeIndex`, `DocStore`, `MemoryStore`, `PatchStore`, `ProjectKnowledgeStore`, `TraceStore`, `parse_agent_mode`, `registered_tools`, `resolve`, `validate_schema_registry`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry.call` — lines 82–143

- Source: [mind01/tools/registry.py:82](../../../../../mind01/tools/registry.py#L82)
- Type: method
- Signature: `self, name: str, args: Dict[str, Any]`
- Direct static callees: `ToolError`, `_append_trace`, `_enforce_schema_policy`, `dict`, `duration_ms`, `extract_receipt_id`, `isinstance`, `perf_counter`, `sanitize_args`, `str`, `summarize_result`, `trace_event_base`, `update`, `validate_tool_args`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry.registered_tools` — lines 145–146

- Source: [mind01/tools/registry.py:145](../../../../../mind01/tools/registry.py#L145)
- Type: method
- Signature: `self`
- Direct static callees: `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry.resolve_path` — lines 148–152

- Source: [mind01/tools/registry.py:148](../../../../../mind01/tools/registry.py#L148)
- Type: method
- Signature: `self, raw_path: str`
- Direct static callees: `ToolError`, `resolve_workspace_path`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry._enforce_schema_policy` — lines 154–186

- Source: [mind01/tools/registry.py:154](../../../../../mind01/tools/registry.py#L154)
- Type: method
- Signature: `self, schema: ToolSchema`
- Direct static callees: `ToolError`, `join`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.tools.registry.ToolRegistry._append_trace` — lines 188–194

- Source: [mind01/tools/registry.py:188](../../../../../mind01/tools/registry.py#L188)
- Type: method
- Signature: `self, event: dict[str, Any], required: bool=False`
- Direct static callees: `ToolError`, `append`
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

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–22

Imports a dependency used by this module.

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports a dependency used by this module.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–27

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 28–28

Implements module-level `Assign` behavior or data.

### Lines 29–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–60

Defines class `ToolRegistry` and the behavior of its members.

### Lines 61–90

Defines class `ToolRegistry` and the behavior of its members.

### Lines 91–120

Defines class `ToolRegistry` and the behavior of its members.

### Lines 121–150

Defines class `ToolRegistry` and the behavior of its members.

### Lines 151–180

Defines class `ToolRegistry` and the behavior of its members.

### Lines 181–194

Defines class `ToolRegistry` and the behavior of its members.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
