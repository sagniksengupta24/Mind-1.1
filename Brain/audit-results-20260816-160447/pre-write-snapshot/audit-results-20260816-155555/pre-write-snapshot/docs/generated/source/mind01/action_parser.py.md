# `mind01/action_parser.py`

## File purpose

This action protocol and parser file is reviewed at snapshot `ebbbfdd086fb3bf015ad82a211021f6796b9655c4dfecd353722644da525de18`. It contains 526 lines.

## Imports and module state

- [mind01/action_parser.py:1](../../../../mind01/action_parser.py#L1) imports `__future__` / annotations.
- [mind01/action_parser.py:3](../../../../mind01/action_parser.py#L3) imports `hashlib`.
- [mind01/action_parser.py:4](../../../../mind01/action_parser.py#L4) imports `json`.
- [mind01/action_parser.py:5](../../../../mind01/action_parser.py#L5) imports `dataclasses` / asdict.
- [mind01/action_parser.py:5](../../../../mind01/action_parser.py#L5) imports `dataclasses` / dataclass.
- [mind01/action_parser.py:5](../../../../mind01/action_parser.py#L5) imports `dataclasses` / field.
- [mind01/action_parser.py:6](../../../../mind01/action_parser.py#L6) imports `datetime` / datetime.
- [mind01/action_parser.py:6](../../../../mind01/action_parser.py#L6) imports `datetime` / timezone.
- [mind01/action_parser.py:7](../../../../mind01/action_parser.py#L7) imports `enum` / Enum.
- [mind01/action_parser.py:8](../../../../mind01/action_parser.py#L8) imports `typing` / Any.
- [mind01/action_parser.py:8](../../../../mind01/action_parser.py#L8) imports `typing` / Dict.
- [mind01/action_parser.py:8](../../../../mind01/action_parser.py#L8) imports `typing` / Mapping.
- [mind01/action_parser.py:8](../../../../mind01/action_parser.py#L8) imports `typing` / Optional.
- [mind01/action_parser.py:8](../../../../mind01/action_parser.py#L8) imports `typing` / Sequence.
- [mind01/action_parser.py:10](../../../../mind01/action_parser.py#L10) imports `security` / redact_secrets.

## Symbols

### `mind01.action_parser.ACTION_SCHEMA_VERSION` — lines 13–13

- Source: [mind01/action_parser.py:13](../../../../mind01/action_parser.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.MAX_MODEL_OUTPUT_CHARS` — lines 14–14

- Source: [mind01/action_parser.py:14](../../../../mind01/action_parser.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.MAX_ACTION_JSON_CHARS` — lines 15–15

- Source: [mind01/action_parser.py:15](../../../../mind01/action_parser.py#L15)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.MAX_ARG_KEYS` — lines 16–16

- Source: [mind01/action_parser.py:16](../../../../mind01/action_parser.py#L16)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.MAX_NESTING_DEPTH` — lines 17–17

- Source: [mind01/action_parser.py:17](../../../../mind01/action_parser.py#L17)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.MAX_ARGUMENT_STRING_CHARS` — lines 18–18

- Source: [mind01/action_parser.py:18](../../../../mind01/action_parser.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ResponseMode` — lines 21–24

- Source: [mind01/action_parser.py:21](../../../../mind01/action_parser.py#L21)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ParserFailureCode` — lines 27–44

- Source: [mind01/action_parser.py:27](../../../../mind01/action_parser.py#L27)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ParserFailureRecord` — lines 48–62

- Source: [mind01/action_parser.py:48](../../../../mind01/action_parser.py#L48)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ParserFailureRecord.to_dict` — lines 61–62

- Source: [mind01/action_parser.py:61](../../../../mind01/action_parser.py#L61)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ActionParseError` — lines 65–75

- Source: [mind01/action_parser.py:65](../../../../mind01/action_parser.py#L65)
- Type: class
- Signature: `n/a`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ActionParseError.__init__` — lines 66–75

- Source: [mind01/action_parser.py:66](../../../../mind01/action_parser.py#L66)
- Type: method
- Signature: `self, code: ParserFailureCode, message: str, *, record: ParserFailureRecord | None=None`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.ParsedAction` — lines 79–90

- Source: [mind01/action_parser.py:79](../../../../mind01/action_parser.py#L79)
- Type: class
- Signature: `n/a`
- Direct static callees: `field`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.TOOL_CALL_FIELDS` — lines 93–93

- Source: [mind01/action_parser.py:93](../../../../mind01/action_parser.py#L93)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.FINAL_FIELDS` — lines 94–94

- Source: [mind01/action_parser.py:94](../../../../mind01/action_parser.py#L94)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.FINAL_STATUSES` — lines 95–103

- Source: [mind01/action_parser.py:95](../../../../mind01/action_parser.py#L95)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.canonical_response_schema` — lines 106–129

- Source: [mind01/action_parser.py:106](../../../../mind01/action_parser.py#L106)
- Type: function
- Signature: `mode: ResponseMode | str, allowed_tools: Sequence[str], tool_schemas: Mapping[str, Any] | None=None, *, repair_response_type: str | None=None`
- Direct static callees: `_default_tool_schemas`, `_final_json_schema`, `_tool_call_json_schema`, `append`, `coerce_response_mode`, `len`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._tool_call_json_schema` — lines 132–177

- Source: [mind01/action_parser.py:132](../../../../mind01/action_parser.py#L132)
- Type: function
- Signature: `allowed_tools: Sequence[str], schemas: Mapping[str, Any]`
- Direct static callees: `append`, `get`, `len`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._final_json_schema` — lines 180–192

- Source: [mind01/action_parser.py:180](../../../../mind01/action_parser.py#L180)
- Type: function
- Signature: `n/a`
- Direct static callees: `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.parse_action_output` — lines 195–258

- Source: [mind01/action_parser.py:195](../../../../mind01/action_parser.py#L195)
- Type: function
- Signature: `raw: str, *, mode: ResponseMode | str=ResponseMode.FINAL_ALLOWED, allowed_tools: Sequence[str] | None=None, tool_schemas: Mapping[str, Any] | None=None, allow_extraction: bool=True, phase: str='model_response', repair_attempt: int=0, model_metadata: Mapping[str, Any] | None=None, repair_response_type: str | None=None`
- Direct static callees: `ParsedAction`, `_default_tool_schemas`, `canonical_response_schema`, `dict`, `isinstance`, `list`, `make_failure_record`, `parse_action_output_strict`, `repr`, `str`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.parse_action_output_strict` — lines 261–348

- Source: [mind01/action_parser.py:261](../../../../mind01/action_parser.py#L261)
- Type: function
- Signature: `raw: str, *, mode: ResponseMode | str=ResponseMode.FINAL_ALLOWED, allowed_tools: Sequence[str] | None=None, tool_schemas: Mapping[str, Any] | None=None, allow_extraction: bool=True, phase: str='model_response', repair_attempt: int=0, model_metadata: Mapping[str, Any] | None=None, repair_response_type: str | None=None`
- Direct static callees: `_default_tool_schemas`, `_fail`, `_nesting_depth`, `_parse_final`, `_parse_tool_call`, `any`, `canonical_response_schema`, `coerce_response_mode`, `dict`, `extract_complete_json_objects`, `get`, `isinstance`, `len`, `list`, `loads`, `looks_truncated_json`, `make_failure_record`, `repr`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._parse_tool_call` — lines 351–398

- Source: [mind01/action_parser.py:351](../../../../mind01/action_parser.py#L351)
- Type: function
- Signature: `body: dict[str, Any], raw: str, visible_tools: list[str], schemas: Mapping[str, Any], context: dict[str, Any], recovered: bool, incident: ParserFailureRecord | None`
- Direct static callees: `ParsedAction`, `_contains_oversized_string`, `_fail`, `isinstance`, `join`, `len`, `set`, `sorted`, `startswith`, `str`, `validate_args`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._parse_final` — lines 401–433

- Source: [mind01/action_parser.py:401](../../../../mind01/action_parser.py#L401)
- Type: function
- Signature: `body: dict[str, Any], raw: str, context: dict[str, Any], recovered: bool, incident: ParserFailureRecord | None`
- Direct static callees: `ParsedAction`, `_contains_oversized_string`, `_fail`, `any`, `isinstance`, `join`, `list`, `set`, `sorted`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.extract_complete_json_objects` — lines 436–453

- Source: [mind01/action_parser.py:436](../../../../mind01/action_parser.py#L436)
- Type: function
- Signature: `text: str`
- Direct static callees: `JSONDecoder`, `append`, `find`, `isinstance`, `len`, `max`, `raw_decode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.looks_truncated_json` — lines 456–459

- Source: [mind01/action_parser.py:456](../../../../mind01/action_parser.py#L456)
- Type: function
- Signature: `text: str`
- Direct static callees: `count`, `lstrip`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.coerce_response_mode` — lines 462–468

- Source: [mind01/action_parser.py:462](../../../../mind01/action_parser.py#L462)
- Type: function
- Signature: `mode: ResponseMode | str`
- Direct static callees: `ResponseMode`, `ValueError`, `isinstance`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser.make_failure_record` — lines 471–497

- Source: [mind01/action_parser.py:471](../../../../mind01/action_parser.py#L471)
- Type: function
- Signature: `code: ParserFailureCode, message: str, raw: str, *, phase: str, allowed_tools: Sequence[str], expected_schema: dict[str, Any], repair_attempt: int, model_metadata: Mapping[str, Any], recovered: bool=False`
- Direct static callees: `ParserFailureRecord`, `dict`, `encode`, `hexdigest`, `int`, `isoformat`, `join`, `max`, `now`, `redact_secrets`, `set`, `sha256`, `sorted`, `split`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._fail` — lines 500–502

- Source: [mind01/action_parser.py:500](../../../../mind01/action_parser.py#L500)
- Type: function
- Signature: `code: ParserFailureCode, message: str, raw: str, context: dict[str, Any]`
- Direct static callees: `ActionParseError`, `make_failure_record`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._default_tool_schemas` — lines 505–508

- Source: [mind01/action_parser.py:505](../../../../mind01/action_parser.py#L505)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._contains_oversized_string` — lines 511–518

- Source: [mind01/action_parser.py:511](../../../../mind01/action_parser.py#L511)
- Type: function
- Signature: `value: Any`
- Direct static callees: `_contains_oversized_string`, `any`, `isinstance`, `len`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.action_parser._nesting_depth` — lines 521–526

- Source: [mind01/action_parser.py:521](../../../../mind01/action_parser.py#L521)
- Type: function
- Signature: `value: Any, depth: int=0`
- Direct static callees: `_nesting_depth`, `isinstance`, `max`, `values`
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

### Lines 14–14

Implements module-level `Assign` behavior or data.

### Lines 15–15

Implements module-level `Assign` behavior or data.

### Lines 16–16

Implements module-level `Assign` behavior or data.

### Lines 17–17

Implements module-level `Assign` behavior or data.

### Lines 18–18

Implements module-level `Assign` behavior or data.

### Lines 19–20

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 21–24

Defines class `ResponseMode` and the behavior of its members.

### Lines 25–26

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 27–44

Defines class `ParserFailureCode` and the behavior of its members.

### Lines 45–47

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 48–62

Defines class `ParserFailureRecord` and the behavior of its members.

### Lines 63–64

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 65–75

Defines class `ActionParseError` and the behavior of its members.

### Lines 76–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–90

Defines class `ParsedAction` and the behavior of its members.

### Lines 91–92

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 93–93

Implements module-level `Assign` behavior or data.

### Lines 94–94

Implements module-level `Assign` behavior or data.

### Lines 95–103

Implements module-level `Assign` behavior or data.

### Lines 104–105

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 106–129

Defines `canonical_response_schema` and its implementation control flow; direct static calls: _default_tool_schemas, _final_json_schema, _tool_call_json_schema, append, coerce_response_mode, len.

### Lines 130–131

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 132–161

Defines `_tool_call_json_schema` and its implementation control flow; direct static calls: append, get, len, list.

### Lines 162–177

Defines `_tool_call_json_schema` and its implementation control flow; direct static calls: append, get, len, list.

### Lines 178–179

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 180–192

Defines `_final_json_schema` and its implementation control flow; direct static calls: sorted.

### Lines 193–194

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 195–224

Defines `parse_action_output` and its implementation control flow; direct static calls: ParsedAction, _default_tool_schemas, canonical_response_schema, dict, isinstance, list, make_failure_record, parse_action_output_strict, repr, str, type.

### Lines 225–254

Defines `parse_action_output` and its implementation control flow; direct static calls: ParsedAction, _default_tool_schemas, canonical_response_schema, dict, isinstance, list, make_failure_record, parse_action_output_strict, repr, str, type.

### Lines 255–258

Defines `parse_action_output` and its implementation control flow; direct static calls: ParsedAction, _default_tool_schemas, canonical_response_schema, dict, isinstance, list, make_failure_record, parse_action_output_strict, repr, str, type.

### Lines 259–260

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 261–290

Defines `parse_action_output_strict` and its implementation control flow; direct static calls: _default_tool_schemas, _fail, _nesting_depth, _parse_final, _parse_tool_call, any, canonical_response_schema, coerce_response_mode, dict, extract_complete_json_objects, get, isinstance, len, list, loads, looks_truncated_json, make_failure_record, repr, strip.

### Lines 291–320

Defines `parse_action_output_strict` and its implementation control flow; direct static calls: _default_tool_schemas, _fail, _nesting_depth, _parse_final, _parse_tool_call, any, canonical_response_schema, coerce_response_mode, dict, extract_complete_json_objects, get, isinstance, len, list, loads, looks_truncated_json, make_failure_record, repr, strip.

### Lines 321–348

Defines `parse_action_output_strict` and its implementation control flow; direct static calls: _default_tool_schemas, _fail, _nesting_depth, _parse_final, _parse_tool_call, any, canonical_response_schema, coerce_response_mode, dict, extract_complete_json_objects, get, isinstance, len, list, loads, looks_truncated_json, make_failure_record, repr, strip.

### Lines 349–350

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 351–380

Defines `_parse_tool_call` and its implementation control flow; direct static calls: ParsedAction, _contains_oversized_string, _fail, isinstance, join, len, set, sorted, startswith, str, validate_args.

### Lines 381–398

Defines `_parse_tool_call` and its implementation control flow; direct static calls: ParsedAction, _contains_oversized_string, _fail, isinstance, join, len, set, sorted, startswith, str, validate_args.

### Lines 399–400

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 401–430

Defines `_parse_final` and its implementation control flow; direct static calls: ParsedAction, _contains_oversized_string, _fail, any, isinstance, join, list, set, sorted, strip.

### Lines 431–433

Defines `_parse_final` and its implementation control flow; direct static calls: ParsedAction, _contains_oversized_string, _fail, any, isinstance, join, list, set, sorted, strip.

### Lines 434–435

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 436–453

Defines `extract_complete_json_objects` and its implementation control flow; direct static calls: JSONDecoder, append, find, isinstance, len, max, raw_decode.

### Lines 454–455

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 456–459

Defines `looks_truncated_json` and its implementation control flow; direct static calls: count, lstrip, startswith.

### Lines 460–461

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 462–468

Defines `coerce_response_mode` and its implementation control flow; direct static calls: ResponseMode, ValueError, isinstance, str.

### Lines 469–470

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 471–497

Defines `make_failure_record` and its implementation control flow; direct static calls: ParserFailureRecord, dict, encode, hexdigest, int, isoformat, join, max, now, redact_secrets, set, sha256, sorted, split.

### Lines 498–499

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 500–502

Defines `_fail` and its implementation control flow; direct static calls: ActionParseError, make_failure_record.

### Lines 503–504

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 505–508

Defines `_default_tool_schemas` and its implementation control flow; direct static calls: none resolved.

### Lines 509–510

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 511–518

Defines `_contains_oversized_string` and its implementation control flow; direct static calls: _contains_oversized_string, any, isinstance, len, values.

### Lines 519–520

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 521–526

Defines `_nesting_depth` and its implementation control flow; direct static calls: _nesting_depth, isinstance, max, values.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
