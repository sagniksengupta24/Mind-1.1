# `scripts/freeze_semantic_routing_v2.py`

## File purpose

This automation and release file is reviewed at snapshot `a1a0c85ad8ff9ebb677ac36edfa14322f8bafa6ec59343364b146e346ce04742`. It contains 476 lines.

## Imports and module state

- [scripts/freeze_semantic_routing_v2.py:1](../../../../scripts/freeze_semantic_routing_v2.py#L1) imports `__future__` / annotations.
- [scripts/freeze_semantic_routing_v2.py:3](../../../../scripts/freeze_semantic_routing_v2.py#L3) imports `argparse`.
- [scripts/freeze_semantic_routing_v2.py:4](../../../../scripts/freeze_semantic_routing_v2.py#L4) imports `hashlib`.
- [scripts/freeze_semantic_routing_v2.py:5](../../../../scripts/freeze_semantic_routing_v2.py#L5) imports `json`.
- [scripts/freeze_semantic_routing_v2.py:6](../../../../scripts/freeze_semantic_routing_v2.py#L6) imports `datetime` / datetime.
- [scripts/freeze_semantic_routing_v2.py:6](../../../../scripts/freeze_semantic_routing_v2.py#L6) imports `datetime` / timezone.
- [scripts/freeze_semantic_routing_v2.py:7](../../../../scripts/freeze_semantic_routing_v2.py#L7) imports `pathlib` / Path.
- [scripts/freeze_semantic_routing_v2.py:8](../../../../scripts/freeze_semantic_routing_v2.py#L8) imports `typing` / Any.

## Symbols

### `scripts.freeze_semantic_routing_v2.ROOT` — lines 11–11

- Source: [scripts/freeze_semantic_routing_v2.py:11](../../../../scripts/freeze_semantic_routing_v2.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.V1` — lines 12–12

- Source: [scripts/freeze_semantic_routing_v2.py:12](../../../../scripts/freeze_semantic_routing_v2.py#L12)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.V2` — lines 13–13

- Source: [scripts/freeze_semantic_routing_v2.py:13](../../../../scripts/freeze_semantic_routing_v2.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.VISIBLE_PARTITIONS` — lines 14–20

- Source: [scripts/freeze_semantic_routing_v2.py:14](../../../../scripts/freeze_semantic_routing_v2.py#L14)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.TOOLS` — lines 22–29

- Source: [scripts/freeze_semantic_routing_v2.py:22](../../../../scripts/freeze_semantic_routing_v2.py#L22)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.SIDE_EFFECT_TOOLS` — lines 30–34

- Source: [scripts/freeze_semantic_routing_v2.py:30](../../../../scripts/freeze_semantic_routing_v2.py#L30)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.LIVE_MUTATION_TOOLS` — lines 35–35

- Source: [scripts/freeze_semantic_routing_v2.py:35](../../../../scripts/freeze_semantic_routing_v2.py#L35)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.PROPOSAL_TOOLS` — lines 36–36

- Source: [scripts/freeze_semantic_routing_v2.py:36](../../../../scripts/freeze_semantic_routing_v2.py#L36)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.TASK_CLASSES` — lines 37–37

- Source: [scripts/freeze_semantic_routing_v2.py:37](../../../../scripts/freeze_semantic_routing_v2.py#L37)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.SPECIALISTS` — lines 38–38

- Source: [scripts/freeze_semantic_routing_v2.py:38](../../../../scripts/freeze_semantic_routing_v2.py#L38)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.TOOL_FAMILIES` — lines 39–44

- Source: [scripts/freeze_semantic_routing_v2.py:39](../../../../scripts/freeze_semantic_routing_v2.py#L39)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.RESPONSE_MODES` — lines 45–45

- Source: [scripts/freeze_semantic_routing_v2.py:45](../../../../scripts/freeze_semantic_routing_v2.py#L45)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.RISK_LEVELS` — lines 46–46

- Source: [scripts/freeze_semantic_routing_v2.py:46](../../../../scripts/freeze_semantic_routing_v2.py#L46)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.CONTRADICTORY_V1_CASES` — lines 49–54

- Source: [scripts/freeze_semantic_routing_v2.py:49](../../../../scripts/freeze_semantic_routing_v2.py#L49)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.ADVERSARIAL_USER_MUTATION_GOAL` — lines 58–74

- Source: [scripts/freeze_semantic_routing_v2.py:58](../../../../scripts/freeze_semantic_routing_v2.py#L58)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.ADVERSARIAL_REVIEW_RATIONALE` — lines 75–91

- Source: [scripts/freeze_semantic_routing_v2.py:75](../../../../scripts/freeze_semantic_routing_v2.py#L75)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.sha256_file` — lines 94–95

- Source: [scripts/freeze_semantic_routing_v2.py:94](../../../../scripts/freeze_semantic_routing_v2.py#L94)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.write_json` — lines 98–100

- Source: [scripts/freeze_semantic_routing_v2.py:98](../../../../scripts/freeze_semantic_routing_v2.py#L98)
- Type: function
- Signature: `path: Path, payload: Any`
- Direct static callees: `dumps`, `mkdir`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.lifecycle_step` — lines 103–104

- Source: [scripts/freeze_semantic_routing_v2.py:103](../../../../scripts/freeze_semantic_routing_v2.py#L103)
- Type: function
- Signature: `phase: str, tools: list[str]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.immediate_phase` — lines 107–116

- Source: [scripts/freeze_semantic_routing_v2.py:107](../../../../scripts/freeze_semantic_routing_v2.py#L107)
- Type: function
- Signature: `family: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.convert_case` — lines 119–196

- Source: [scripts/freeze_semantic_routing_v2.py:119](../../../../scripts/freeze_semantic_routing_v2.py#L119)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `any`, `bool`, `get`, `immediate_phase`, `int`, `lifecycle_step`, `list`, `rsplit`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.make_case` — lines 199–237

- Source: [scripts/freeze_semantic_routing_v2.py:199](../../../../scripts/freeze_semantic_routing_v2.py#L199)
- Type: function
- Signature: `*, case_id: str, partition: str, prompt: str, mode: str, write: bool, shell: bool, task: str, specialist: str, immediate_family: str, immediate_tools: list[str], terminal_family: str | None, terminal_tools: list[str], lifecycle: list[dict[str, Any]], response: str, user_mutation: bool, immediate_side_effect: bool, terminal_mutation: bool, risk: str, reason: str, forbidden: list[str], fixture: str | None=None, tags: list[str] | None=None, execution_contract: dict[str, Any] | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.lifecycle_cases` — lines 240–259

- Source: [scripts/freeze_semantic_routing_v2.py:240](../../../../scripts/freeze_semantic_routing_v2.py#L240)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `dict`, `enumerate`, `lifecycle_step`, `make_case`, `replace`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.end_to_end_cases` — lines 262–295

- Source: [scripts/freeze_semantic_routing_v2.py:262](../../../../scripts/freeze_semantic_routing_v2.py#L262)
- Type: function
- Signature: `n/a`
- Direct static callees: `append`, `dict`, `len`, `lifecycle_step`, `make_case`, `mkdir`, `range`, `sorted`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.schema` — lines 298–346

- Source: [scripts/freeze_semantic_routing_v2.py:298](../../../../scripts/freeze_semantic_routing_v2.py#L298)
- Type: function
- Signature: `n/a`
- Direct static callees: `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.validate_case` — lines 349–375

- Source: [scripts/freeze_semantic_routing_v2.py:349](../../../../scripts/freeze_semantic_routing_v2.py#L349)
- Type: function
- Signature: `case: dict[str, Any]`
- Direct static callees: `any`, `len`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.freeze_semantic_routing_v2.main` — lines 378–472

- Source: [scripts/freeze_semantic_routing_v2.py:378](../../../../scripts/freeze_semantic_routing_v2.py#L378)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `RuntimeError`, `add_argument`, `append`, `convert_case`, `dumps`, `end_to_end_cases`, `exists`, `get`, `int`, `isoformat`, `items`, `len`, `lifecycle_cases`, `loads`, `mkdir`, `now`, `parse_args`, `print`, `read_text`, `rsplit`, `schema`, `sha256_file`, `sorted`, `str`, `validate_case`, `values`, `write_json`, `zip`
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

### Lines 9–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Implements module-level `Assign` behavior or data.

### Lines 12–12

Implements module-level `Assign` behavior or data.

### Lines 13–13

Implements module-level `Assign` behavior or data.

### Lines 14–20

Implements module-level `Assign` behavior or data.

### Lines 21–21

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 22–29

Implements module-level `Assign` behavior or data.

### Lines 30–34

Implements module-level `Assign` behavior or data.

### Lines 35–35

Implements module-level `Assign` behavior or data.

### Lines 36–36

Implements module-level `Assign` behavior or data.

### Lines 37–37

Implements module-level `Assign` behavior or data.

### Lines 38–38

Implements module-level `Assign` behavior or data.

### Lines 39–44

Implements module-level `Assign` behavior or data.

### Lines 45–45

Implements module-level `Assign` behavior or data.

### Lines 46–46

Implements module-level `Assign` behavior or data.

### Lines 47–48

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 49–54

Implements module-level `Assign` behavior or data.

### Lines 55–57

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 58–74

Implements module-level `Assign` behavior or data.

### Lines 75–91

Implements module-level `Assign` behavior or data.

### Lines 92–93

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 94–95

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–100

Defines `write_json` and its implementation control flow; direct static calls: dumps, mkdir, write_text.

### Lines 101–102

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 103–104

Defines `lifecycle_step` and its implementation control flow; direct static calls: none resolved.

### Lines 105–106

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 107–116

Defines `immediate_phase` and its implementation control flow; direct static calls: none resolved.

### Lines 117–118

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 119–148

Defines `convert_case` and its implementation control flow; direct static calls: any, bool, get, immediate_phase, int, lifecycle_step, list, rsplit.

### Lines 149–178

Defines `convert_case` and its implementation control flow; direct static calls: any, bool, get, immediate_phase, int, lifecycle_step, list, rsplit.

### Lines 179–196

Defines `convert_case` and its implementation control flow; direct static calls: any, bool, get, immediate_phase, int, lifecycle_step, list, rsplit.

### Lines 197–198

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 199–228

Defines `make_case` and its implementation control flow; direct static calls: none resolved.

### Lines 229–237

Defines `make_case` and its implementation control flow; direct static calls: none resolved.

### Lines 238–239

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 240–259

Defines `lifecycle_cases` and its implementation control flow; direct static calls: append, dict, enumerate, lifecycle_step, make_case, replace, sorted.

### Lines 260–261

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 262–291

Defines `end_to_end_cases` and its implementation control flow; direct static calls: append, dict, len, lifecycle_step, make_case, mkdir, range, sorted, write_text.

### Lines 292–295

Defines `end_to_end_cases` and its implementation control flow; direct static calls: append, dict, len, lifecycle_step, make_case, mkdir, range, sorted, write_text.

### Lines 296–297

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 298–327

Defines `schema` and its implementation control flow; direct static calls: sorted.

### Lines 328–346

Defines `schema` and its implementation control flow; direct static calls: sorted.

### Lines 347–348

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 349–375

Defines `validate_case` and its implementation control flow; direct static calls: any, len, set.

### Lines 376–377

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 378–407

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, RuntimeError, add_argument, append, convert_case, dumps, end_to_end_cases, exists, get, int, isoformat, items, len, lifecycle_cases, loads, mkdir, now, parse_args, print, read_text, rsplit, schema, sha256_file, sorted, str, validate_case, values, write_json, zip.

### Lines 408–437

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, RuntimeError, add_argument, append, convert_case, dumps, end_to_end_cases, exists, get, int, isoformat, items, len, lifecycle_cases, loads, mkdir, now, parse_args, print, read_text, rsplit, schema, sha256_file, sorted, str, validate_case, values, write_json, zip.

### Lines 438–467

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, RuntimeError, add_argument, append, convert_case, dumps, end_to_end_cases, exists, get, int, isoformat, items, len, lifecycle_cases, loads, mkdir, now, parse_args, print, read_text, rsplit, schema, sha256_file, sorted, str, validate_case, values, write_json, zip.

### Lines 468–472

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, RuntimeError, add_argument, append, convert_case, dumps, end_to_end_cases, exists, get, int, isoformat, items, len, lifecycle_cases, loads, mkdir, now, parse_args, print, read_text, rsplit, schema, sha256_file, sorted, str, validate_case, values, write_json, zip.

### Lines 473–474

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 475–476

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
