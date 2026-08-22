from __future__ import annotations

import json

from mind01.action_parser import (
    ActionParseError,
    ParserFailureCode,
    ResponseMode,
    parse_action_output,
    parse_action_output_strict,
)


def tool_call(tool: str, arguments: dict) -> str:
    return json.dumps({"schema_version": "1.0", "response_type": "tool_call", "tool": tool, "arguments": arguments})


def final(summary: str, status: str = "unverified", refs: list[str] | None = None) -> str:
    return json.dumps({"schema_version": "1.0", "response_type": "final", "status": status, "summary": summary, "evidence_refs": refs or []})


def expect_error(raw: str, code: ParserFailureCode, **kwargs) -> None:  # type: ignore[no-untyped-def]
    try:
        parse_action_output_strict(raw, **kwargs)
        raise AssertionError(f"parser did not reject {raw!r}")
    except ActionParseError as exc:
        assert exc.code == code
        assert exc.record is not None
        assert len(exc.record.raw_output_hash) == 64


def test_canonical_tool_and_final_responses() -> None:
    action = parse_action_output_strict(tool_call("read_file", {"path": "README.md"}))
    assert action.tool_name == "read_file"
    assert action.tool_args == {"path": "README.md"}
    done = parse_action_output_strict(final("Done."))
    assert done.final == "Done."
    assert done.final_status == "unverified"


def test_typed_parser_failures_and_mode_enforcement() -> None:
    expect_error("not json", ParserFailureCode.MALFORMED_JSON)
    expect_error('{"schema_version":"1.0"', ParserFailureCode.TRUNCATED_OUTPUT)
    expect_error(tool_call("not_visible", {}), ParserFailureCode.UNKNOWN_TOOL, allowed_tools=["read_file"])
    expect_error(tool_call("read_file", {}), ParserFailureCode.MISSING_ARGUMENT, allowed_tools=["read_file"])
    expect_error(tool_call("read_file", {"path": 3}), ParserFailureCode.WRONG_ARGUMENT_TYPE, allowed_tools=["read_file"])
    expect_error(tool_call("read_file", {"path": "x", "extra": "y"}), ParserFailureCode.EXTRA_ARGUMENT, allowed_tools=["read_file"])
    expect_error(final("too soon"), ParserFailureCode.FINAL_ANSWER_WHEN_ACTION_REQUIRED, mode=ResponseMode.ACTION_REQUIRED)
    expect_error(tool_call("read_file", {"path": "README.md"}), ParserFailureCode.TOOL_CALL_WHEN_FINAL_REQUIRED, mode=ResponseMode.REPAIR_REQUIRED, repair_response_type="final")
    expect_error('{"schema_version":"2.0","response_type":"final","status":"unverified","summary":"x","evidence_refs":[]}', ParserFailureCode.SCHEMA_VERSION_MISMATCH)


def test_multiple_conflicting_and_legacy_formats_are_rejected() -> None:
    one = tool_call("read_file", {"path": "README.md"})
    expect_error(one + one, ParserFailureCode.MULTIPLE_ACTIONS)
    mixed = json.dumps({"schema_version": "1.0", "response_type": "tool_call", "tool": "read_file", "arguments": {"path": "README.md"}, "summary": "also final"})
    expect_error(mixed, ParserFailureCode.CONFLICTING_ACTIONS)
    expect_error('<action_json>{"tool":"read_file","args":{}}</action_json>', ParserFailureCode.SCHEMA_VERSION_MISMATCH)


def test_safe_single_object_extraction_is_recorded_as_incident() -> None:
    parsed = parse_action_output("```json\n" + final("Done") + "\n```")
    assert not parsed.invalid_json
    assert parsed.recovered
    assert parsed.incident is not None
    assert parsed.incident.error_code == ParserFailureCode.PROSE_AROUND_ACTION.value
    assert parsed.incident.recovered


def run_action_parser_tests() -> None:
    test_canonical_tool_and_final_responses()
    test_typed_parser_failures_and_mode_enforcement()
    test_multiple_conflicting_and_legacy_formats_are_rejected()
    test_safe_single_object_extraction_is_recorded_as_incident()


def test_action_parser_regressions() -> None:
    run_action_parser_tests()
