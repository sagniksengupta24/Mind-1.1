from __future__ import annotations

import time
from pathlib import Path
from typing import Any, Callable, Dict

from ..code_index import CodeIndex
from ..file_safety import FileSafetyError, resolve_workspace_path
from ..memory import MemoryStore
from ..project_knowledge import ProjectKnowledgeStore
from ..modes import AgentMode, parse_agent_mode
from ..patches import PatchStore
from ..rag import DocStore
from ..traces import (
    TraceError,
    TraceStore,
    duration_ms,
    extract_receipt_id,
    sanitize_args,
    summarize_result,
    trace_event_base,
)
from . import code_index_tools, docs_tools, file_tools, knowledge_tools, memory_tools, patch_tools, project_tools, shell_tools
from .schemas import SCHEMA_BY_NAME, ToolSchema, validate_schema_registry, validate_tool_args
from .verify_tools import ToolError, ToolResult


ToolHandler = Callable[["ToolRegistry", Dict[str, Any]], ToolResult]


class ToolRegistry:
    def __init__(
        self,
        workspace: Path,
        yes: bool = False,
        allow_write: bool = False,
        allow_shell: bool = False,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        session_id: str | None = None,
        model_name: str | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.yes = yes
        self.allow_write = allow_write
        self.allow_shell = allow_shell
        self.mode = parse_agent_mode(mode)
        self.session_id = session_id
        self.model_name = model_name
        self.memory = MemoryStore(self.workspace)
        self.docs = DocStore(self.workspace)
        self.code_index = CodeIndex(self.workspace)
        self.patches = PatchStore(self.workspace)
        self.knowledge = ProjectKnowledgeStore(self.workspace)
        self.traces = TraceStore(self.workspace)
        self._tools: Dict[str, ToolHandler] = {
            "list_files": file_tools.list_files,
            "project_map": project_tools.project_map,
            "read_file": file_tools.read_file,
            "search_code": file_tools.search_code,
            "index_code": code_index_tools.index_code,
            "search_symbols": code_index_tools.search_symbols,
            "file_summary": code_index_tools.file_summary,
            "write_file": file_tools.write_file,
            "edit_file": file_tools.edit_file,
            "propose_write_file": patch_tools.propose_write_file,
            "propose_edit_file": patch_tools.propose_edit_file,
            "list_patches": patch_tools.list_patches,
            "show_patch": patch_tools.show_patch,
            "test_patch": patch_tools.test_patch,
            "run_command": shell_tools.run_command,
            "remember": memory_tools.remember,
            "recall": memory_tools.recall,
            "list_memories": memory_tools.list_memories,
            "update_memory": memory_tools.update_memory,
            "delete_memory": memory_tools.delete_memory,
            "search_docs": docs_tools.search_docs,
            "refresh_knowledge": knowledge_tools.refresh_knowledge,
            "query_knowledge": knowledge_tools.query_knowledge,
        }
        validate_schema_registry(self.registered_tools())

    def call(self, name: str, args: Dict[str, Any]) -> ToolResult:
        start = time.perf_counter()
        event = trace_event_base(
            event_type="tool_call",
            mode=self.mode.value,
            session_id=self.session_id,
            model_name=self.model_name,
        )
        event.update(
            {
                "tool_name": name,
                "raw_args": sanitize_args(args if isinstance(args, dict) else {}),
                "normalized_args": None,
                "policy_decision": "pending",
                "tool_result_summary": None,
                "receipt_id": None,
                "error": None,
            }
        )
        try:
            normalized_args = validate_tool_args(name, args)
        except ValueError as exc:
            event["policy_decision"] = "schema_rejected"
            event["error"] = str(exc)
            event["duration_ms"] = duration_ms(start)
            self._append_trace(event)
            raise ToolError(str(exc)) from exc
        event["normalized_args"] = sanitize_args(normalized_args)
        if name not in self._tools:
            event["policy_decision"] = "unknown_tool"
            event["error"] = f"Unknown tool: {name}"
            event["duration_ms"] = duration_ms(start)
            self._append_trace(event)
            raise ToolError(f"Unknown tool: {name}")
        try:
            self._enforce_schema_policy(SCHEMA_BY_NAME[name])
        except ToolError as exc:
            event["policy_decision"] = "blocked"
            event["error"] = str(exc)
            event["duration_ms"] = duration_ms(start)
            self._append_trace(event)
            raise
        schema = SCHEMA_BY_NAME[name]
        if schema.can_write or schema.can_run_shell:
            pre_event = dict(event)
            pre_event["policy_decision"] = "allowed_pre_dispatch"
            pre_event["duration_ms"] = duration_ms(start)
            self._append_trace(pre_event, required=True)
        # --- Static pre-validation gate (Workstream 2) ---
        from ..pre_validate import PreValidationError, _PREVALIDATED_TOOLS, pre_validate_mutation

        if name in _PREVALIDATED_TOOLS:
            pv = pre_validate_mutation(self.workspace, name, normalized_args)
            if not pv.valid:
                event["policy_decision"] = "pre_validation_rejected"
                event["error"] = f"[{pv.code}] {pv.message}"
                event["pre_validation"] = pv.to_dict()
                event["duration_ms"] = duration_ms(start)
                self._append_trace(event)
                raise PreValidationError(f"Pre-validation failed: [{pv.code}] {pv.message}")
        try:
            result = self._tools[name](self, normalized_args)
        except ToolError as exc:
            event["policy_decision"] = "allowed"
            event["error"] = str(exc)
            event["duration_ms"] = duration_ms(start)
            self._append_trace(event)
            raise
        event["policy_decision"] = "allowed"
        event["tool_result_summary"] = summarize_result(result.text)
        event["receipt_id"] = extract_receipt_id(result.text)
        event["duration_ms"] = duration_ms(start)
        self._append_trace(event)
        return result

    def registered_tools(self) -> list[str]:
        return sorted(self._tools)

    def resolve_path(self, raw_path: str) -> Path:
        try:
            return resolve_workspace_path(self.workspace, raw_path)
        except FileSafetyError as exc:
            raise ToolError(str(exc)) from exc

    def _enforce_schema_policy(self, schema: ToolSchema) -> None:
        mode_value = self.mode.value
        if mode_value not in schema.allowed_modes:
            allowed = ", ".join(schema.allowed_modes)
            raise ToolError(
                f"Tool `{schema.name}` is not allowed in mode `{mode_value}`. "
                f"Allowed modes: {allowed}."
            )
        if schema.can_write:
            if self.mode not in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
                raise ToolError(
                    f"Tool `{schema.name}` can write source files and requires "
                    "`write-approved` or `unsafe` mode."
                )
            if not self.allow_write:
                raise ToolError(
                    f"Tool `{schema.name}` requires `--allow-write` in mode `{mode_value}`."
                )
        if schema.can_run_shell:
            if self.mode not in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
                raise ToolError(
                    f"Tool `{schema.name}` can run shell commands and requires "
                    "`write-approved` or `unsafe` mode."
                )
            if not self.allow_shell:
                raise ToolError(
                    f"Tool `{schema.name}` requires `--allow-shell` in mode `{mode_value}`."
                )
        if schema.mutates_runtime and self.mode == AgentMode.READ_ONLY:
            raise ToolError(
                f"Tool `{schema.name}` mutates Mind runtime state and is blocked "
                "in `read-only` mode."
            )

    def _append_trace(self, event: dict[str, Any], required: bool = False) -> None:
        try:
            self.traces.append(event)
        except TraceError as exc:
            if required:
                raise ToolError("Required trace event could not be written.") from exc
            return
