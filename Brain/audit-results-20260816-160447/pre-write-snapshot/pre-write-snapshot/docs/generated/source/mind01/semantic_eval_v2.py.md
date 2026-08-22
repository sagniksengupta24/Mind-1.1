# `mind01/semantic_eval_v2.py`

## File purpose

This evaluation and release governance file is reviewed at snapshot `3e5b8aab6a4b571ba0e6cb762571a63b2938230c4b79b7c979e6e1478a822646`. It contains 384 lines.

## Imports and module state

- [mind01/semantic_eval_v2.py:1](../../../../mind01/semantic_eval_v2.py#L1) imports `__future__` / annotations.
- [mind01/semantic_eval_v2.py:3](../../../../mind01/semantic_eval_v2.py#L3) imports `hashlib`.
- [mind01/semantic_eval_v2.py:4](../../../../mind01/semantic_eval_v2.py#L4) imports `json`.
- [mind01/semantic_eval_v2.py:5](../../../../mind01/semantic_eval_v2.py#L5) imports `math`.
- [mind01/semantic_eval_v2.py:6](../../../../mind01/semantic_eval_v2.py#L6) imports `re`.
- [mind01/semantic_eval_v2.py:7](../../../../mind01/semantic_eval_v2.py#L7) imports `pathlib` / Path.
- [mind01/semantic_eval_v2.py:8](../../../../mind01/semantic_eval_v2.py#L8) imports `typing` / Any.

## Symbols

### `mind01.semantic_eval_v2.ROOT` — lines 11–11

- Source: [mind01/semantic_eval_v2.py:11](../../../../mind01/semantic_eval_v2.py#L11)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.SUITE` — lines 12–12

- Source: [mind01/semantic_eval_v2.py:12](../../../../mind01/semantic_eval_v2.py#L12)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.PARTITION_FILES` — lines 13–22

- Source: [mind01/semantic_eval_v2.py:13](../../../../mind01/semantic_eval_v2.py#L13)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.VISIBLE_MINIMUMS` — lines 23–31

- Source: [mind01/semantic_eval_v2.py:23](../../../../mind01/semantic_eval_v2.py#L23)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.BASE_FIELDS` — lines 32–35

- Source: [mind01/semantic_eval_v2.py:32](../../../../mind01/semantic_eval_v2.py#L32)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.LABELED_FIELDS` — lines 36–36

- Source: [mind01/semantic_eval_v2.py:36](../../../../mind01/semantic_eval_v2.py#L36)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.TASK_CLASSES` — lines 37–37

- Source: [mind01/semantic_eval_v2.py:37](../../../../mind01/semantic_eval_v2.py#L37)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.SPECIALISTS` — lines 38–38

- Source: [mind01/semantic_eval_v2.py:38](../../../../mind01/semantic_eval_v2.py#L38)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.TOOL_FAMILIES` — lines 39–44

- Source: [mind01/semantic_eval_v2.py:39](../../../../mind01/semantic_eval_v2.py#L39)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.TOOLS` — lines 45–52

- Source: [mind01/semantic_eval_v2.py:45](../../../../mind01/semantic_eval_v2.py#L45)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.SIDE_EFFECT_TOOLS` — lines 53–57

- Source: [mind01/semantic_eval_v2.py:53](../../../../mind01/semantic_eval_v2.py#L53)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.LIVE_MUTATION_TOOLS` — lines 58–58

- Source: [mind01/semantic_eval_v2.py:58](../../../../mind01/semantic_eval_v2.py#L58)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.SHELL_TOOLS` — lines 59–59

- Source: [mind01/semantic_eval_v2.py:59](../../../../mind01/semantic_eval_v2.py#L59)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.SemanticV2Error` — lines 62–63

- Source: [mind01/semantic_eval_v2.py:62](../../../../mind01/semantic_eval_v2.py#L62)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.sha256_file` — lines 66–67

- Source: [mind01/semantic_eval_v2.py:66](../../../../mind01/semantic_eval_v2.py#L66)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `read_bytes`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.load_v2_partition` — lines 70–76

- Source: [mind01/semantic_eval_v2.py:70](../../../../mind01/semantic_eval_v2.py#L70)
- Type: function
- Signature: `partition: str`
- Direct static callees: `SemanticV2Error`, `get`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.validate_semantic_routing_v2` — lines 79–134

- Source: [mind01/semantic_eval_v2.py:79](../../../../mind01/semantic_eval_v2.py#L79)
- Type: function
- Signature: `*, require_blind: bool=False`
- Direct static callees: `SemanticV2Error`, `_find_duplicate`, `_validate_blind_contract`, `_validate_case`, `_validate_fixture_hashes`, `_validate_migration`, `bool`, `extend`, `get`, `is_file`, `isinstance`, `items`, `len`, `load_v2_partition`, `loads`, `read_text`, `set`, `sha256_file`, `sum`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2.run_deterministic_semantic_v2` — lines 137–202

- Source: [mind01/semantic_eval_v2.py:137](../../../../mind01/semantic_eval_v2.py#L137)
- Type: function
- Signature: `partitions: tuple[str, ...] | None=None`
- Direct static callees: `HierarchicalRouter`, `ToolExposureAuthority`, `_immediate_family`, `all`, `append`, `bool`, `build`, `decide`, `is_current_for`, `len`, `list`, `load_v2_partition`, `parse_agent_mode`, `replace`, `route_typed`, `set`, `sum`, `to_dict`, `tuple`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._immediate_family` — lines 205–208

- Source: [mind01/semantic_eval_v2.py:205](../../../../mind01/semantic_eval_v2.py#L205)
- Type: function
- Signature: `route: Any, visible_tools: tuple[str, ...]`
- Direct static callees: `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._validate_case` — lines 211–283

- Source: [mind01/semantic_eval_v2.py:211](../../../../mind01/semantic_eval_v2.py#L211)
- Type: function
- Signature: `case: Any, partition: str, *, blind: bool`
- Direct static callees: `SemanticV2Error`, `_tool_list`, `all`, `any`, `get`, `isinstance`, `len`, `set`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._tool_list` — lines 286–289

- Source: [mind01/semantic_eval_v2.py:286](../../../../mind01/semantic_eval_v2.py#L286)
- Type: function
- Signature: `value: Any, case_id: str`
- Direct static callees: `SemanticV2Error`, `isinstance`, `len`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._validate_migration` — lines 292–312

- Source: [mind01/semantic_eval_v2.py:292](../../../../mind01/semantic_eval_v2.py#L292)
- Type: function
- Signature: `manifest: dict[str, Any]`
- Direct static callees: `SemanticV2Error`, `get`, `isinstance`, `len`, `loads`, `read_text`, `set`, `sha256_file`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._validate_blind_contract` — lines 315–330

- Source: [mind01/semantic_eval_v2.py:315](../../../../mind01/semantic_eval_v2.py#L315)
- Type: function
- Signature: `blind: list[dict[str, Any]], manifest: dict[str, Any]`
- Direct static callees: `SemanticV2Error`, `get`, `is_file`, `len`, `loads`, `read_text`, `sha256_file`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._validate_fixture_hashes` — lines 333–337

- Source: [mind01/semantic_eval_v2.py:333](../../../../mind01/semantic_eval_v2.py#L333)
- Type: function
- Signature: `n/a`
- Direct static callees: `SemanticV2Error`, `any`, `is_dir`, `is_file`, `load_v2_partition`, `rglob`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._tokens` — lines 340–341

- Source: [mind01/semantic_eval_v2.py:340](../../../../mind01/semantic_eval_v2.py#L340)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `findall`, `lower`, `set`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._trigrams` — lines 344–350

- Source: [mind01/semantic_eval_v2.py:344](../../../../mind01/semantic_eval_v2.py#L344)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `get`, `len`, `lower`, `max`, `range`, `strip`, `sub`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._cosine` — lines 353–357

- Source: [mind01/semantic_eval_v2.py:353](../../../../mind01/semantic_eval_v2.py#L353)
- Type: function
- Signature: `left: dict[str, int], right: dict[str, int]`
- Direct static callees: `get`, `items`, `sqrt`, `sum`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_eval_v2._find_duplicate` — lines 360–384

- Source: [mind01/semantic_eval_v2.py:360](../../../../mind01/semantic_eval_v2.py#L360)
- Type: function
- Signature: `cases: list[dict[str, Any]]`
- Direct static callees: `_cosine`, `_tokens`, `_trigrams`, `append`, `join`, `len`, `lower`, `split`, `str`
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

### Lines 13–22

Implements module-level `Assign` behavior or data.

### Lines 23–31

Implements module-level `Assign` behavior or data.

### Lines 32–35

Implements module-level `Assign` behavior or data.

### Lines 36–36

Implements module-level `Assign` behavior or data.

### Lines 37–37

Implements module-level `Assign` behavior or data.

### Lines 38–38

Implements module-level `Assign` behavior or data.

### Lines 39–44

Implements module-level `Assign` behavior or data.

### Lines 45–52

Implements module-level `Assign` behavior or data.

### Lines 53–57

Implements module-level `Assign` behavior or data.

### Lines 58–58

Implements module-level `Assign` behavior or data.

### Lines 59–59

Implements module-level `Assign` behavior or data.

### Lines 60–61

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 62–63

Defines class `SemanticV2Error` and the behavior of its members.

### Lines 64–65

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 66–67

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, read_bytes, sha256.

### Lines 68–69

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 70–76

Defines `load_v2_partition` and its implementation control flow; direct static calls: SemanticV2Error, get, isinstance, loads, read_text.

### Lines 77–78

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 79–108

Defines `validate_semantic_routing_v2` and its implementation control flow; direct static calls: SemanticV2Error, _find_duplicate, _validate_blind_contract, _validate_case, _validate_fixture_hashes, _validate_migration, bool, extend, get, is_file, isinstance, items, len, load_v2_partition, loads, read_text, set, sha256_file, sum, values.

### Lines 109–134

Defines `validate_semantic_routing_v2` and its implementation control flow; direct static calls: SemanticV2Error, _find_duplicate, _validate_blind_contract, _validate_case, _validate_fixture_hashes, _validate_migration, bool, extend, get, is_file, isinstance, items, len, load_v2_partition, loads, read_text, set, sha256_file, sum, values.

### Lines 135–136

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 137–166

Defines `run_deterministic_semantic_v2` and its implementation control flow; direct static calls: HierarchicalRouter, ToolExposureAuthority, _immediate_family, all, append, bool, build, decide, is_current_for, len, list, load_v2_partition, parse_agent_mode, replace, route_typed, set, sum, to_dict, tuple, values.

### Lines 167–196

Defines `run_deterministic_semantic_v2` and its implementation control flow; direct static calls: HierarchicalRouter, ToolExposureAuthority, _immediate_family, all, append, bool, build, decide, is_current_for, len, list, load_v2_partition, parse_agent_mode, replace, route_typed, set, sum, to_dict, tuple, values.

### Lines 197–202

Defines `run_deterministic_semantic_v2` and its implementation control flow; direct static calls: HierarchicalRouter, ToolExposureAuthority, _immediate_family, all, append, bool, build, decide, is_current_for, len, list, load_v2_partition, parse_agent_mode, replace, route_typed, set, sum, to_dict, tuple, values.

### Lines 203–204

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 205–208

Defines `_immediate_family` and its implementation control flow; direct static calls: set.

### Lines 209–210

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 211–240

Defines `_validate_case` and its implementation control flow; direct static calls: SemanticV2Error, _tool_list, all, any, get, isinstance, len, set, values.

### Lines 241–270

Defines `_validate_case` and its implementation control flow; direct static calls: SemanticV2Error, _tool_list, all, any, get, isinstance, len, set, values.

### Lines 271–283

Defines `_validate_case` and its implementation control flow; direct static calls: SemanticV2Error, _tool_list, all, any, get, isinstance, len, set, values.

### Lines 284–285

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 286–289

Defines `_tool_list` and its implementation control flow; direct static calls: SemanticV2Error, isinstance, len, set.

### Lines 290–291

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 292–312

Defines `_validate_migration` and its implementation control flow; direct static calls: SemanticV2Error, get, isinstance, len, loads, read_text, set, sha256_file.

### Lines 313–314

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 315–330

Defines `_validate_blind_contract` and its implementation control flow; direct static calls: SemanticV2Error, get, is_file, len, loads, read_text, sha256_file, strip.

### Lines 331–332

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 333–337

Defines `_validate_fixture_hashes` and its implementation control flow; direct static calls: SemanticV2Error, any, is_dir, is_file, load_v2_partition, rglob, str.

### Lines 338–339

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 340–341

Defines `_tokens` and its implementation control flow; direct static calls: findall, lower, set.

### Lines 342–343

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 344–350

Defines `_trigrams` and its implementation control flow; direct static calls: get, len, lower, max, range, strip, sub.

### Lines 351–352

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 353–357

Defines `_cosine` and its implementation control flow; direct static calls: get, items, sqrt, sum, values.

### Lines 358–359

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 360–384

Defines `_find_duplicate` and its implementation control flow; direct static calls: _cosine, _tokens, _trigrams, append, join, len, lower, split, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
