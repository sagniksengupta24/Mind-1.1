from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Mapping, Optional, Sequence

from .security import redact_secrets


ACTION_SCHEMA_VERSION = "1.0"
MAX_MODEL_OUTPUT_CHARS = 64_000
MAX_ACTION_JSON_CHARS = 32_000
MAX_ARG_KEYS = 32
MAX_NESTING_DEPTH = 8
MAX_ARGUMENT_STRING_CHARS = 24_000


class ResponseMode(str, Enum):
    ACTION_REQUIRED = "ACTION_REQUIRED"
    FINAL_ALLOWED = "FINAL_ALLOWED"
    REPAIR_REQUIRED = "REPAIR_REQUIRED"


class ParserFailureCode(str, Enum):
    NO_ACTION = "NO_ACTION"
    MALFORMED_JSON = "MALFORMED_JSON"
    TRUNCATED_OUTPUT = "TRUNCATED_OUTPUT"
    UNKNOWN_TOOL = "UNKNOWN_TOOL"
    MISSING_ARGUMENT = "MISSING_ARGUMENT"
    WRONG_ARGUMENT_TYPE = "WRONG_ARGUMENT_TYPE"
    EXTRA_ARGUMENT = "EXTRA_ARGUMENT"
    MULTIPLE_ACTIONS = "MULTIPLE_ACTIONS"
    CONFLICTING_ACTIONS = "CONFLICTING_ACTIONS"
    PROSE_AROUND_ACTION = "PROSE_AROUND_ACTION"
    FINAL_ANSWER_WHEN_ACTION_REQUIRED = "FINAL_ANSWER_WHEN_ACTION_REQUIRED"
    TOOL_CALL_WHEN_FINAL_REQUIRED = "TOOL_CALL_WHEN_FINAL_REQUIRED"
    SCHEMA_VERSION_MISMATCH = "SCHEMA_VERSION_MISMATCH"
    ARGUMENT_TOO_LARGE = "ARGUMENT_TOO_LARGE"
    REPEATED_INVALID_ACTION = "REPEATED_INVALID_ACTION"
    UNSAFE_ACTION = "UNSAFE_ACTION"
    INTERNAL_PARSER_ERROR = "INTERNAL_PARSER_ERROR"


@dataclass(frozen=True)
class ParserFailureRecord:
    error_code: str
    message: str
    phase: str
    raw_output_hash: str
    redacted_raw_output_excerpt: str
    expected_schema: dict[str, Any]
    allowed_tools: list[str]
    repair_attempt_number: int
    model_metadata: dict[str, Any]
    timestamp: str
    recovered: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class ActionParseError(ValueError):
    def __init__(
        self,
        code: ParserFailureCode,
        message: str,
        *,
        record: ParserFailureRecord | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.record = record


@dataclass
class ParsedAction:
    final: Optional[str] = None
    final_status: str = ""
    evidence_refs: list[str] = field(default_factory=list)
    tool_name: Optional[str] = None
    tool_args: Dict[str, Any] = field(default_factory=dict)
    invalid_json: bool = False
    error: str = ""
    error_code: str = ""
    recovered: bool = False
    incident: ParserFailureRecord | None = None
    raw_object: dict[str, Any] = field(default_factory=dict)


TOOL_CALL_FIELDS = {"schema_version", "response_type", "tool", "arguments"}
FINAL_FIELDS = {"schema_version", "response_type", "status", "summary", "evidence_refs"}
FINAL_STATUSES = {
    "verified",
    "partially_verified",
    "unverified",
    "failed",
    "blocked",
    "policy_denied",
    "rolled_back",
}


def canonical_response_schema(
    mode: ResponseMode | str,
    allowed_tools: Sequence[str],
    tool_schemas: Mapping[str, Any] | None = None,
    *,
    repair_response_type: str | None = None,
) -> dict[str, Any]:
    response_mode = coerce_response_mode(mode)
    schemas = tool_schemas or _default_tool_schemas()
    variants: list[dict[str, Any]] = []
    if response_mode != ResponseMode.FINAL_ALLOWED or repair_response_type == "tool_call":
        variants.append(_tool_call_json_schema(allowed_tools, schemas))
    elif response_mode == ResponseMode.FINAL_ALLOWED:
        if allowed_tools:
            variants.append(_tool_call_json_schema(allowed_tools, schemas))
        variants.append(_final_json_schema())
    if response_mode == ResponseMode.REPAIR_REQUIRED and repair_response_type != "tool_call":
        variants = [_final_json_schema()] if repair_response_type == "final" else [
            _tool_call_json_schema(allowed_tools, schemas),
            _final_json_schema(),
        ]
    if response_mode == ResponseMode.ACTION_REQUIRED:
        variants = [_tool_call_json_schema(allowed_tools, schemas)]
    return variants[0] if len(variants) == 1 else {"oneOf": variants}


def _tool_call_json_schema(allowed_tools: Sequence[str], schemas: Mapping[str, Any]) -> dict[str, Any]:
    tool_variants: list[dict[str, Any]] = []
    for name in allowed_tools:
        schema = schemas.get(name)
        properties: dict[str, Any] = {}
        required: list[str] = []
        if schema is not None:
            for argument in schema.args:
                json_type = {"str": "string", "int": "integer", "bool": "boolean"}[argument.type_name]
                item: dict[str, Any] = {"type": json_type}
                if argument.enum_values:
                    item["enum"] = list(argument.enum_values)
                properties[argument.name] = item
                if argument.required:
                    required.append(argument.name)
        tool_variants.append(
            {
                "type": "object",
                "additionalProperties": False,
                "required": ["schema_version", "response_type", "tool", "arguments"],
                "properties": {
                    "schema_version": {"const": ACTION_SCHEMA_VERSION},
                    "response_type": {"const": "tool_call"},
                    "tool": {"const": name},
                    "arguments": {
                        "type": "object",
                        "additionalProperties": False,
                        "properties": properties,
                        "required": required,
                    },
                },
            }
        )
    if not tool_variants:
        return {
            "type": "object",
            "additionalProperties": False,
            "required": ["schema_version", "response_type", "tool", "arguments"],
            "properties": {
                "schema_version": {"const": ACTION_SCHEMA_VERSION},
                "response_type": {"const": "tool_call"},
                "tool": {"enum": []},
                "arguments": {"type": "object"},
            },
        }
    return tool_variants[0] if len(tool_variants) == 1 else {"oneOf": tool_variants}


def _final_json_schema() -> dict[str, Any]:
    return {
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "response_type", "status", "summary", "evidence_refs"],
        "properties": {
            "schema_version": {"const": ACTION_SCHEMA_VERSION},
            "response_type": {"const": "final"},
            "status": {"enum": sorted(FINAL_STATUSES)},
            "summary": {"type": "string"},
            "evidence_refs": {"type": "array", "items": {"type": "string"}},
        },
    }


def parse_action_output(
    raw: str,
    *,
    mode: ResponseMode | str = ResponseMode.FINAL_ALLOWED,
    allowed_tools: Sequence[str] | None = None,
    tool_schemas: Mapping[str, Any] | None = None,
    allow_extraction: bool = True,
    phase: str = "model_response",
    repair_attempt: int = 0,
    model_metadata: Mapping[str, Any] | None = None,
    repair_response_type: str | None = None,
) -> ParsedAction:
    try:
        return parse_action_output_strict(
            raw,
            mode=mode,
            allowed_tools=allowed_tools,
            tool_schemas=tool_schemas,
            allow_extraction=allow_extraction,
            phase=phase,
            repair_attempt=repair_attempt,
            model_metadata=model_metadata,
            repair_response_type=repair_response_type,
        )
    except ActionParseError as exc:
        record = exc.record or make_failure_record(
            exc.code,
            str(exc),
            raw,
            phase=phase,
            allowed_tools=list(allowed_tools or _default_tool_schemas()),
            expected_schema=canonical_response_schema(
                mode,
                list(allowed_tools or _default_tool_schemas()),
                tool_schemas,
                repair_response_type=repair_response_type,
            ),
            repair_attempt=repair_attempt,
            model_metadata=dict(model_metadata or {}),
        )
        return ParsedAction(
            invalid_json=True,
            error=str(exc),
            error_code=exc.code.value,
            incident=record,
        )
    except Exception as exc:  # The model must never crash the runtime parser.
        code = ParserFailureCode.INTERNAL_PARSER_ERROR
        message = f"Internal parser error: {type(exc).__name__}."
        return ParsedAction(
            invalid_json=True,
            error=message,
            error_code=code.value,
            incident=make_failure_record(
                code,
                message,
                raw if isinstance(raw, str) else repr(raw),
                phase=phase,
                allowed_tools=list(allowed_tools or ()),
                expected_schema={},
                repair_attempt=repair_attempt,
                model_metadata=dict(model_metadata or {}),
            ),
        )


def parse_action_output_strict(
    raw: str,
    *,
    mode: ResponseMode | str = ResponseMode.FINAL_ALLOWED,
    allowed_tools: Sequence[str] | None = None,
    tool_schemas: Mapping[str, Any] | None = None,
    allow_extraction: bool = True,
    phase: str = "model_response",
    repair_attempt: int = 0,
    model_metadata: Mapping[str, Any] | None = None,
    repair_response_type: str | None = None,
) -> ParsedAction:
    response_mode = coerce_response_mode(mode)
    schemas = tool_schemas or _default_tool_schemas()
    visible_tools = list(allowed_tools if allowed_tools is not None else schemas)
    expected = canonical_response_schema(
        response_mode,
        visible_tools,
        schemas,
        repair_response_type=repair_response_type,
    )
    context = {
        "phase": phase,
        "allowed_tools": visible_tools,
        "expected_schema": expected,
        "repair_attempt": repair_attempt,
        "model_metadata": dict(model_metadata or {}),
    }
    if not isinstance(raw, str):
        _fail(ParserFailureCode.NO_ACTION, "Model output must be text.", repr(raw), context)
    if len(raw) > MAX_MODEL_OUTPUT_CHARS:
        _fail(ParserFailureCode.ARGUMENT_TOO_LARGE, "Model output exceeds the size limit.", raw, context)
    stripped = raw.strip()
    if not stripped:
        _fail(ParserFailureCode.NO_ACTION, "Model returned no action object.", raw, context)

    recovered = False
    recovery_incident: ParserFailureRecord | None = None
    try:
        body = json.loads(stripped)
    except json.JSONDecodeError as exc:
        candidates = extract_complete_json_objects(stripped)
        if len(candidates) > 1:
            _fail(ParserFailureCode.MULTIPLE_ACTIONS, "Multiple JSON objects are not allowed.", raw, context)
        if len(candidates) == 1 and allow_extraction:
            body, start, end = candidates[0]
            outside = stripped[:start] + stripped[end:]
            if not outside.strip():
                _fail(ParserFailureCode.MALFORMED_JSON, f"Malformed JSON: {exc.msg}.", raw, context)
            recovered = True
            recovery_incident = make_failure_record(
                ParserFailureCode.PROSE_AROUND_ACTION,
                "Recovered exactly one valid JSON object from surrounding structural noise.",
                raw,
                recovered=True,
                **context,
            )
        else:
            code = ParserFailureCode.TRUNCATED_OUTPUT if looks_truncated_json(stripped) else ParserFailureCode.MALFORMED_JSON
            _fail(code, f"Malformed JSON: {exc.msg}.", raw, context)

    if not isinstance(body, dict):
        _fail(ParserFailureCode.NO_ACTION, "Response must be one JSON object.", raw, context)
    if len(stripped) > MAX_ACTION_JSON_CHARS:
        _fail(ParserFailureCode.ARGUMENT_TOO_LARGE, "Action JSON exceeds the size limit.", raw, context)
    if _nesting_depth(body) > MAX_NESTING_DEPTH:
        _fail(ParserFailureCode.ARGUMENT_TOO_LARGE, "Action JSON is nested too deeply.", raw, context)
    if body.get("schema_version") != ACTION_SCHEMA_VERSION:
        _fail(
            ParserFailureCode.SCHEMA_VERSION_MISMATCH,
            f"schema_version must be {ACTION_SCHEMA_VERSION!r}.",
            raw,
            context,
        )
    response_type = body.get("response_type")
    if response_type == "tool_call":
        if response_mode == ResponseMode.REPAIR_REQUIRED and repair_response_type == "final":
            _fail(ParserFailureCode.TOOL_CALL_WHEN_FINAL_REQUIRED, "Repair must return a final response.", raw, context)
        return _parse_tool_call(body, raw, visible_tools, schemas, context, recovered, recovery_incident)
    if response_type == "final":
        if response_mode == ResponseMode.ACTION_REQUIRED:
            _fail(ParserFailureCode.FINAL_ANSWER_WHEN_ACTION_REQUIRED, "A tool call is required in the current phase.", raw, context)
        if response_mode == ResponseMode.REPAIR_REQUIRED and repair_response_type == "tool_call":
            _fail(ParserFailureCode.FINAL_ANSWER_WHEN_ACTION_REQUIRED, "Repair must return a tool call.", raw, context)
        return _parse_final(body, raw, context, recovered, recovery_incident)
    if "tool" in body and any(key in body for key in {"summary", "status", "evidence_refs"}):
        _fail(ParserFailureCode.CONFLICTING_ACTIONS, "Response mixes tool-call and final fields.", raw, context)
    _fail(ParserFailureCode.NO_ACTION, "response_type must be 'tool_call' or 'final'.", raw, context)


def _parse_tool_call(
    body: dict[str, Any],
    raw: str,
    visible_tools: list[str],
    schemas: Mapping[str, Any],
    context: dict[str, Any],
    recovered: bool,
    incident: ParserFailureRecord | None,
) -> ParsedAction:
    unknown_fields = sorted(set(body) - TOOL_CALL_FIELDS)
    if unknown_fields:
        code = ParserFailureCode.CONFLICTING_ACTIONS if set(unknown_fields) & {"summary", "status", "evidence_refs"} else ParserFailureCode.EXTRA_ARGUMENT
        _fail(code, f"Unknown tool-call field(s): {', '.join(unknown_fields)}.", raw, context)
    for field_name in ("tool", "arguments"):
        if field_name not in body:
            _fail(ParserFailureCode.MISSING_ARGUMENT, f"Tool call requires `{field_name}`.", raw, context)
    tool = body["tool"]
    arguments = body["arguments"]
    if not isinstance(tool, str) or not tool:
        _fail(ParserFailureCode.WRONG_ARGUMENT_TYPE, "`tool` must be a non-empty string.", raw, context)
    if tool not in schemas:
        _fail(ParserFailureCode.UNKNOWN_TOOL, f"Unknown or hidden tool: {tool}.", raw, context)
    if tool not in visible_tools:
        schema = schemas[tool]
        code = ParserFailureCode.UNSAFE_ACTION if schema.can_write or schema.can_run_shell else ParserFailureCode.UNKNOWN_TOOL
        _fail(code, f"Tool is not permitted in the current phase: {tool}.", raw, context)
    if not isinstance(arguments, dict):
        _fail(ParserFailureCode.WRONG_ARGUMENT_TYPE, "`arguments` must be an object.", raw, context)
    if len(arguments) > MAX_ARG_KEYS or _contains_oversized_string(arguments):
        _fail(ParserFailureCode.ARGUMENT_TOO_LARGE, "Tool arguments exceed parser limits.", raw, context)
    try:
        normalized = schemas[tool].validate_args(arguments)
    except ValueError as exc:
        message = str(exc)
        if message.startswith("Missing required"):
            code = ParserFailureCode.MISSING_ARGUMENT
        elif message.startswith("Unknown arg"):
            code = ParserFailureCode.EXTRA_ARGUMENT
        else:
            code = ParserFailureCode.WRONG_ARGUMENT_TYPE
        _fail(code, message, raw, context)
    return ParsedAction(
        tool_name=tool,
        tool_args=normalized,
        recovered=recovered,
        incident=incident,
        raw_object=body,
    )


def _parse_final(
    body: dict[str, Any],
    raw: str,
    context: dict[str, Any],
    recovered: bool,
    incident: ParserFailureRecord | None,
) -> ParsedAction:
    unknown_fields = sorted(set(body) - FINAL_FIELDS)
    if unknown_fields:
        code = ParserFailureCode.CONFLICTING_ACTIONS if "tool" in unknown_fields or "arguments" in unknown_fields else ParserFailureCode.EXTRA_ARGUMENT
        _fail(code, f"Unknown final field(s): {', '.join(unknown_fields)}.", raw, context)
    for name in ("status", "summary", "evidence_refs"):
        if name not in body:
            _fail(ParserFailureCode.MISSING_ARGUMENT, f"Final response requires `{name}`.", raw, context)
    status = body["status"]
    summary = body["summary"]
    evidence_refs = body["evidence_refs"]
    if status not in FINAL_STATUSES:
        _fail(ParserFailureCode.WRONG_ARGUMENT_TYPE, "Final `status` is invalid.", raw, context)
    if not isinstance(summary, str) or not summary.strip():
        _fail(ParserFailureCode.WRONG_ARGUMENT_TYPE, "Final `summary` must be a non-empty string.", raw, context)
    if not isinstance(evidence_refs, list) or any(not isinstance(item, str) for item in evidence_refs):
        _fail(ParserFailureCode.WRONG_ARGUMENT_TYPE, "Final `evidence_refs` must be an array of strings.", raw, context)
    if _contains_oversized_string(body):
        _fail(ParserFailureCode.ARGUMENT_TOO_LARGE, "Final response exceeds parser limits.", raw, context)
    return ParsedAction(
        final=summary.strip(),
        final_status=status,
        evidence_refs=list(evidence_refs),
        recovered=recovered,
        incident=incident,
        raw_object=body,
    )


def extract_complete_json_objects(text: str) -> list[tuple[Any, int, int]]:
    decoder = json.JSONDecoder()
    candidates: list[tuple[Any, int, int]] = []
    index = 0
    while index < len(text):
        start = text.find("{", index)
        if start < 0:
            break
        try:
            value, length = decoder.raw_decode(text[start:])
        except json.JSONDecodeError:
            index = start + 1
            continue
        end = start + length
        if isinstance(value, dict):
            candidates.append((value, start, end))
        index = max(end, start + 1)
    return candidates


def looks_truncated_json(text: str) -> bool:
    return text.lstrip().startswith("{") and (
        text.count("{") > text.count("}") or text.count('"') % 2 == 1
    )


def coerce_response_mode(mode: ResponseMode | str) -> ResponseMode:
    if isinstance(mode, ResponseMode):
        return mode
    try:
        return ResponseMode(str(mode))
    except ValueError as exc:
        raise ValueError(f"Unknown response mode: {mode}") from exc


def make_failure_record(
    code: ParserFailureCode,
    message: str,
    raw: str,
    *,
    phase: str,
    allowed_tools: Sequence[str],
    expected_schema: dict[str, Any],
    repair_attempt: int,
    model_metadata: Mapping[str, Any],
    recovered: bool = False,
) -> ParserFailureRecord:
    encoded = raw.encode("utf-8", errors="replace")
    excerpt = redact_secrets(" ".join(raw.split()))[:500]
    return ParserFailureRecord(
        error_code=code.value,
        message=message[:500],
        phase=phase,
        raw_output_hash=hashlib.sha256(encoded).hexdigest(),
        redacted_raw_output_excerpt=excerpt,
        expected_schema=expected_schema,
        allowed_tools=sorted(set(allowed_tools)),
        repair_attempt_number=max(0, int(repair_attempt)),
        model_metadata=dict(model_metadata),
        timestamp=datetime.now(timezone.utc).isoformat(),
        recovered=recovered,
    )


def _fail(code: ParserFailureCode, message: str, raw: str, context: dict[str, Any]) -> None:
    record = make_failure_record(code, message, raw, **context)
    raise ActionParseError(code, message, record=record)


def _default_tool_schemas() -> Mapping[str, Any]:
    from .tools.schemas import SCHEMA_BY_NAME

    return SCHEMA_BY_NAME


def _contains_oversized_string(value: Any) -> bool:
    if isinstance(value, str):
        return len(value) > MAX_ARGUMENT_STRING_CHARS
    if isinstance(value, dict):
        return any(_contains_oversized_string(item) for item in value.values())
    if isinstance(value, list):
        return any(_contains_oversized_string(item) for item in value)
    return False


def _nesting_depth(value: Any, depth: int = 0) -> int:
    if isinstance(value, dict):
        return depth if not value else max(_nesting_depth(item, depth + 1) for item in value.values())
    if isinstance(value, list):
        return depth if not value else max(_nesting_depth(item, depth + 1) for item in value)
    return depth
