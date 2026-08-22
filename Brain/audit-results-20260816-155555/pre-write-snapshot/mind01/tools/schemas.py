from __future__ import annotations

from dataclasses import dataclass
from typing import Any


NO_DEFAULT = object()
VALID_ARG_TYPES = {"str", "int", "bool"}
VALID_SAFETY_LEVELS = {"read", "write", "shell", "memory", "docs", "patch", "code", "project"}
VALID_MODES = {"read-only", "propose", "write-approved", "unsafe"}

READ_MODES = ("read-only", "propose", "write-approved", "unsafe")
PROPOSE_MODES = ("propose", "write-approved", "unsafe")
WRITE_MODES = ("write-approved", "unsafe")


def coerce_typed_value(name: str, type_name: str, value: Any) -> Any:
    if type_name == "str":
        if not isinstance(value, str):
            raise ValueError(f"Arg `{name}` must be a string.")
        return value
    if type_name == "int":
        if isinstance(value, bool):
            raise ValueError(f"Arg `{name}` must be an integer.")
        if isinstance(value, int):
            return value
        raise ValueError(f"Arg `{name}` must be an integer.")
    if type_name == "bool":
        if isinstance(value, bool):
            return value
        raise ValueError(f"Arg `{name}` must be a boolean.")
    raise ValueError(f"Unsupported arg type `{type_name}`.")


@dataclass(frozen=True)
class ArgSchema:
    name: str
    type_name: str
    description: str
    required: bool = False
    default: Any = NO_DEFAULT
    enum_values: tuple[Any, ...] = ()

    def __post_init__(self) -> None:
        if self.type_name not in VALID_ARG_TYPES:
            raise ValueError(f"Invalid arg type `{self.type_name}` for `{self.name}`.")
        if self.required and self.default is not NO_DEFAULT:
            raise ValueError(f"Required arg `{self.name}` cannot also define a default.")
        if self.enum_values:
            for value in self.enum_values:
                coerce_typed_value(self.name, self.type_name, value)

    def render_example(self) -> str:
        if self.default is not NO_DEFAULT:
            return repr(self.default)
        if self.enum_values:
            return repr(self.enum_values[0])
        examples = {"str": "'text'", "int": "1", "bool": "true"}
        return examples[self.type_name]


@dataclass(frozen=True)
class ToolSchema:
    name: str
    description: str
    args: tuple[ArgSchema, ...] = ()
    safety_level: str = "read"
    allowed_modes: tuple[str, ...] = READ_MODES
    approval_required: bool = False
    can_write: bool = False
    can_run_shell: bool = False
    mutates_runtime: bool = False
    output_summary: str = ""

    def __post_init__(self) -> None:
        if self.safety_level not in VALID_SAFETY_LEVELS:
            raise ValueError(f"Invalid safety level `{self.safety_level}` for `{self.name}`.")
        if not self.allowed_modes:
            raise ValueError(f"Tool `{self.name}` must define at least one allowed mode.")
        invalid_modes = sorted(set(self.allowed_modes) - VALID_MODES)
        if invalid_modes:
            raise ValueError(f"Tool `{self.name}` has invalid modes: {', '.join(invalid_modes)}")
        if not self.output_summary.strip():
            raise ValueError(f"Tool `{self.name}` must define an output summary.")
        arg_names = [arg.name for arg in self.args]
        duplicates = sorted({name for name in arg_names if arg_names.count(name) > 1})
        if duplicates:
            raise ValueError(f"Tool `{self.name}` has duplicate args: {', '.join(duplicates)}")

    @property
    def required(self) -> tuple[str, ...]:
        return tuple(arg.name for arg in self.args if arg.required)

    def arg_map(self) -> dict[str, ArgSchema]:
        return {arg.name: arg for arg in self.args}

    def render(self) -> str:
        args = ", ".join(
            f'"{arg.name}": {arg.render_example()}'
            for arg in self.args
        )
        meta = (
            f"safety={self.safety_level}; modes={','.join(self.allowed_modes)}; "
            f"approval_required={str(self.approval_required).lower()}; "
            f"can_write={str(self.can_write).lower()}; "
            f"can_run_shell={str(self.can_run_shell).lower()}; "
            f"mutates_runtime={str(self.mutates_runtime).lower()}"
        )
        return f"- {self.name}: {{{args}}} - {self.description} [{meta}] -> {self.output_summary}"

    def validate_args(self, args: dict[str, Any]) -> dict[str, Any]:
        if not isinstance(args, dict):
            raise ValueError(f"Args for tool `{self.name}` must be an object.")

        arg_map = self.arg_map()
        unknown = sorted(set(args) - set(arg_map))
        if unknown:
            raise ValueError(f"Unknown arg(s) for tool `{self.name}`: {', '.join(unknown)}.")

        normalized: dict[str, Any] = {}
        for arg in self.args:
            if arg.name not in args:
                if arg.required:
                    raise ValueError(f"Missing required arg `{arg.name}` for tool `{self.name}`.")
                if arg.default is not NO_DEFAULT:
                    normalized[arg.name] = arg.default
                continue

            value = args[arg.name]
            if value is None or (arg.type_name == "str" and value == ""):
                if arg.required:
                    raise ValueError(f"Missing required arg `{arg.name}` for tool `{self.name}`.")
                if arg.default is not NO_DEFAULT:
                    normalized[arg.name] = arg.default
                continue

            normalized_value = coerce_value(arg, value)
            if arg.enum_values and normalized_value not in arg.enum_values:
                allowed = ", ".join(repr(item) for item in arg.enum_values)
                raise ValueError(
                    f"Invalid value for arg `{arg.name}` on tool `{self.name}`. "
                    f"Allowed values: {allowed}."
                )
            normalized[arg.name] = normalized_value
        return normalized


def arg(
    name: str,
    type_name: str,
    description: str,
    *,
    required: bool = False,
    default: Any = NO_DEFAULT,
    enum_values: tuple[Any, ...] = (),
) -> ArgSchema:
    return ArgSchema(
        name=name,
        type_name=type_name,
        description=description,
        required=required,
        default=default,
        enum_values=enum_values,
    )


TOOL_SCHEMAS = [
    ToolSchema(
        "list_files",
        "List workspace files.",
        (arg("path", "str", "Workspace-relative path to list.", default="."),),
        safety_level="read",
        output_summary="Newline-delimited workspace-relative file paths.",
    ),
    ToolSchema(
        "project_map",
        "Summarize files and file types.",
        (arg("path", "str", "Workspace-relative root to summarize.", default="."),),
        safety_level="project",
        output_summary="Compact project map text.",
    ),
    ToolSchema(
        "read_file",
        "Read a text file.",
        (arg("path", "str", "Workspace-relative file path.", required=True),),
        safety_level="read",
        output_summary="Redacted file text, truncated for safety.",
    ),
    ToolSchema(
        "search_code",
        "Search file contents.",
        (
            arg("query", "str", "Case-insensitive text query.", required=True),
            arg("path", "str", "Workspace-relative search root.", default="."),
        ),
        safety_level="read",
        output_summary="Matching file lines with paths and line numbers.",
    ),
    ToolSchema(
        "index_code",
        "Index code files and symbols.",
        (arg("path", "str", "Workspace-relative path to index.", default="."),),
        safety_level="code",
        allowed_modes=PROPOSE_MODES,
        mutates_runtime=True,
        output_summary="Indexed file and symbol counts.",
    ),
    ToolSchema(
        "search_symbols",
        "Search code symbols; use the persistent index when present and a read-only source scan otherwise.",
        (
            arg("query", "str", "Symbol or signature search text.", required=True),
            arg("limit", "int", "Maximum results.", default=20),
        ),
        safety_level="code",
        output_summary="Matching symbols with workspace-relative source locations.",
    ),
    ToolSchema(
        "file_summary",
        "Show indexed imports and symbols for a file.",
        (arg("path", "str", "Workspace-relative indexed file path.", required=True),),
        safety_level="code",
        output_summary="Indexed imports and symbols for one file.",
    ),
    ToolSchema(
        "write_file",
        "Write a source file when explicitly allowed.",
        (
            arg("path", "str", "Workspace-relative file path.", required=True),
            arg("content", "str", "Full replacement file content.", required=True),
        ),
        safety_level="write",
        allowed_modes=WRITE_MODES,
        approval_required=True,
        can_write=True,
        output_summary="Write confirmation with relative path.",
    ),
    ToolSchema(
        "edit_file",
        "Edit a source file when explicitly allowed.",
        (
            arg("path", "str", "Workspace-relative file path.", required=True),
            arg("old", "str", "Exact text to replace.", required=True),
            arg("new", "str", "Replacement text.", required=True),
        ),
        safety_level="write",
        allowed_modes=WRITE_MODES,
        approval_required=True,
        can_write=True,
        output_summary="Edit confirmation with relative path.",
    ),
    ToolSchema(
        "propose_write_file",
        "Create a reviewable write proposal.",
        (
            arg("path", "str", "Workspace-relative file path.", required=True),
            arg("content", "str", "Proposed file content.", required=True),
            arg("reason", "str", "Short reason for the proposal.", default=""),
        ),
        safety_level="patch",
        allowed_modes=PROPOSE_MODES,
        mutates_runtime=True,
        output_summary="Patch proposal id and review instructions.",
    ),
    ToolSchema(
        "propose_edit_file",
        "Create a reviewable edit proposal.",
        (
            arg("path", "str", "Workspace-relative file path.", required=True),
            arg("old", "str", "Exact text to replace.", required=True),
            arg("new", "str", "Replacement text.", required=True),
            arg("reason", "str", "Short reason for the proposal.", default=""),
        ),
        safety_level="patch",
        allowed_modes=PROPOSE_MODES,
        mutates_runtime=True,
        output_summary="Patch proposal id and diff preview.",
    ),
    ToolSchema(
        "list_patches",
        "List pending patch proposals.",
        (),
        safety_level="patch",
        output_summary="Pending patch proposal list.",
    ),
    ToolSchema(
        "show_patch",
        "Show a patch diff.",
        (arg("id", "int", "Patch proposal id.", required=True),),
        safety_level="patch",
        output_summary="Patch metadata and unified diff.",
    ),
    ToolSchema(
        "test_patch",
        "Apply a patch in a temporary copy and run an allowlisted test command.",
        (
            arg("id", "int", "Patch proposal id.", required=True),
            arg("command", "str", "Allowlisted test command.", default="python3 -B tests/smoke_test.py"),
        ),
        safety_level="shell",
        allowed_modes=WRITE_MODES,
        can_run_shell=True,
        output_summary="Patch test pass/fail status, exit code, and command output.",
    ),
    ToolSchema(
        "run_command",
        "Run an allowlisted command when shell is enabled.",
        (
            arg("command", "str", "Allowlisted command line.", required=True),
            arg("timeout_seconds", "int", "Command timeout in seconds.", default=60),
            arg("output_limit", "int", "Maximum output characters to return.", default=20000),
        ),
        safety_level="shell",
        allowed_modes=WRITE_MODES,
        approval_required=True,
        can_run_shell=True,
        output_summary="Exit code and truncated command output.",
    ),
    ToolSchema(
        "remember",
        "Save a memory.",
        (
            arg("key", "str", "Short memory key.", required=True),
            arg("value", "str", "Memory text.", required=True),
            arg("tags", "str", "Comma-separated tags.", default=""),
            arg("source", "str", "Memory source label.", default="agent"),
            arg("importance", "int", "Memory importance score from 0 to 10.", default=1),
        ),
        safety_level="memory",
        allowed_modes=WRITE_MODES,
        mutates_runtime=True,
        output_summary="Memory creation or dedupe status.",
    ),
    ToolSchema(
        "recall",
        "Search memories.",
        (
            arg("query", "str", "Memory search query.", required=True),
            arg("limit", "int", "Maximum memories to return.", default=8),
            arg("tags", "str", "Comma-separated required tags.", default=""),
        ),
        safety_level="memory",
        output_summary="Matching memories or no-match marker.",
    ),
    ToolSchema(
        "list_memories",
        "List saved memories.",
        (
            arg("limit", "int", "Maximum memories to return.", default=50),
            arg("tags", "str", "Comma-separated required tags.", default=""),
        ),
        safety_level="memory",
        output_summary="Recent saved memories.",
    ),
    ToolSchema(
        "update_memory",
        "Update a memory.",
        (
            arg("id", "int", "Memory id.", required=True),
            arg("value", "str", "New memory text.", required=True),
            arg("tags", "str", "Optional replacement tags."),
            arg("source", "str", "Optional replacement source."),
            arg("importance", "int", "Optional replacement importance score."),
        ),
        safety_level="memory",
        allowed_modes=WRITE_MODES,
        mutates_runtime=True,
        output_summary="Memory update status.",
    ),
    ToolSchema(
        "delete_memory",
        "Delete a memory.",
        (arg("id", "int", "Memory id.", required=True),),
        safety_level="memory",
        allowed_modes=WRITE_MODES,
        mutates_runtime=True,
        output_summary="Memory deletion status.",
    ),
    ToolSchema(
        "refresh_knowledge",
        "Refresh the provenance-aware project entity and relation graph.",
        (arg("path", "str", "Workspace-relative code path to refresh.", default="."),),
        safety_level="project",
        allowed_modes=PROPOSE_MODES,
        mutates_runtime=True,
        output_summary="Counts for refreshed files, symbols, imports, entities, and relations.",
    ),
    ToolSchema(
        "query_knowledge",
        "Query provenance-aware project entities.",
        (
            arg("query", "str", "Entity name, path, symbol, or metadata query.", required=True),
            arg("limit", "int", "Maximum entities to return.", default=20),
        ),
        safety_level="project",
        output_summary="Matching project entities with source provenance.",
    ),
    ToolSchema(
        "search_docs",
        "Search indexed docs with ranked keyword or optional embedding retrieval.",
        (
            arg("query", "str", "Docs search query.", required=True),
            arg("limit", "int", "Maximum docs hits.", default=6),
            arg(
                "embed",
                "str",
                "Whether to use embeddings.",
                default="false",
                enum_values=("", "false", "true", "0", "1", "no", "yes"),
            ),
            arg("embedding_model", "str", "Ollama embedding model name.", default="nomic-embed-text"),
            arg("ollama_url", "str", "Ollama server URL.", default="http://127.0.0.1:11434"),
        ),
        safety_level="docs",
        output_summary="Ranked docs snippets with scores.",
    ),
]

SCHEMA_BY_NAME = {schema.name: schema for schema in TOOL_SCHEMAS}


def render_tool_docs() -> str:
    return "\n".join(schema.render() for schema in TOOL_SCHEMAS)


def validate_tool_args(name: str, args: dict[str, Any]) -> dict[str, Any]:
    schema = SCHEMA_BY_NAME.get(name)
    if schema is None:
        raise ValueError(f"Unknown tool: {name}")
    return schema.validate_args(args)


def validate_schema_registry(registered_tools: list[str] | tuple[str, ...]) -> None:
    registered = list(registered_tools)
    duplicates = sorted({schema.name for schema in TOOL_SCHEMAS if schema_names().count(schema.name) > 1})
    if duplicates:
        raise ValueError(f"Duplicate schemas: {', '.join(duplicates)}")

    registered_set = set(registered)
    schema_set = set(SCHEMA_BY_NAME)
    missing = sorted(registered_set - schema_set)
    extra = sorted(schema_set - registered_set)
    if missing:
        raise ValueError(f"Registered tools missing schemas: {', '.join(missing)}")
    if extra:
        raise ValueError(f"Schemas exist for unregistered tools: {', '.join(extra)}")


def schema_names() -> list[str]:
    return [schema.name for schema in TOOL_SCHEMAS]


def coerce_value(arg_schema: ArgSchema, value: Any) -> Any:
    return coerce_typed_value(arg_schema.name, arg_schema.type_name, value)


def validate_value_type(name: str, type_name: str, value: Any) -> None:
    coerce_typed_value(name, type_name, value)
