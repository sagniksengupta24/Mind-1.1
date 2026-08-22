from __future__ import annotations

import json
import random
import string

from mind01.action_parser import MAX_ARGUMENT_STRING_CHARS, MAX_MODEL_OUTPUT_CHARS, ParserFailureCode, parse_action_output


def test_parser_rejects_conflicting_and_oversized_actions() -> None:
    conflicting = json.dumps({"schema_version": "1.0", "response_type": "tool_call", "tool": "read_file", "arguments": {"path": "README.md"}, "summary": "done"})
    parsed = parse_action_output(conflicting)
    assert parsed.invalid_json and parsed.error_code == ParserFailureCode.CONFLICTING_ACTIONS.value
    oversized = parse_action_output("x" * (MAX_MODEL_OUTPUT_CHARS + 1))
    assert oversized.invalid_json and oversized.error_code == ParserFailureCode.ARGUMENT_TOO_LARGE.value
    body = {"schema_version": "1.0", "response_type": "tool_call", "tool": "read_file", "arguments": {"path": "x" * (MAX_ARGUMENT_STRING_CHARS + 1)}}
    action = parse_action_output(json.dumps(body))
    assert action.invalid_json and action.error_code == ParserFailureCode.ARGUMENT_TOO_LARGE.value


def test_parser_handles_malformed_inputs_without_raising() -> None:
    rng = random.Random(20260715)
    alphabet = string.ascii_letters + string.digits + "<>{}[]/:,\" "
    for _ in range(300):
        raw = "".join(rng.choice(alphabet) for _ in range(rng.randint(0, 400)))
        result = parse_action_output(raw)
        assert result.invalid_json or result.final is not None or result.tool_name is not None


def test_parser_accepts_one_canonical_action() -> None:
    parsed = parse_action_output(json.dumps({"schema_version": "1.0", "response_type": "tool_call", "tool": "read_file", "arguments": {"path": "README.md"}}))
    assert not parsed.invalid_json
    assert parsed.tool_name == "read_file"
