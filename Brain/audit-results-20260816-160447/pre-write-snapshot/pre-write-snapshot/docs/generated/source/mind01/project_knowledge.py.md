# `mind01/project_knowledge.py`

## File purpose

This project knowledge file is reviewed at snapshot `c2c1605a4d7630711aaf2dbc6018c892c3f3ad734c4ca446dd84894a00d52ceb`. It contains 226 lines.

## Imports and module state

- [mind01/project_knowledge.py:1](../../../../mind01/project_knowledge.py#L1) imports `__future__` / annotations.
- [mind01/project_knowledge.py:3](../../../../mind01/project_knowledge.py#L3) imports `hashlib`.
- [mind01/project_knowledge.py:4](../../../../mind01/project_knowledge.py#L4) imports `json`.
- [mind01/project_knowledge.py:5](../../../../mind01/project_knowledge.py#L5) imports `sqlite3`.
- [mind01/project_knowledge.py:6](../../../../mind01/project_knowledge.py#L6) imports `time`.
- [mind01/project_knowledge.py:7](../../../../mind01/project_knowledge.py#L7) imports `dataclasses` / dataclass.
- [mind01/project_knowledge.py:8](../../../../mind01/project_knowledge.py#L8) imports `pathlib` / Path.
- [mind01/project_knowledge.py:10](../../../../mind01/project_knowledge.py#L10) imports `code_index` / iter_code_files.
- [mind01/project_knowledge.py:10](../../../../mind01/project_knowledge.py#L10) imports `code_index` / language_for.
- [mind01/project_knowledge.py:10](../../../../mind01/project_knowledge.py#L10) imports `code_index` / parse_code_file.
- [mind01/project_knowledge.py:11](../../../../mind01/project_knowledge.py#L11) imports `file_safety` / FileSafetyError.
- [mind01/project_knowledge.py:11](../../../../mind01/project_knowledge.py#L11) imports `file_safety` / ensure_text_file_safe.
- [mind01/project_knowledge.py:11](../../../../mind01/project_knowledge.py#L11) imports `file_safety` / resolve_workspace_path.

## Symbols

### `mind01.project_knowledge.KnowledgeHit` — lines 15–21

- Source: [mind01/project_knowledge.py:15](../../../../mind01/project_knowledge.py#L15)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore` — lines 24–221

- Source: [mind01/project_knowledge.py:24](../../../../mind01/project_knowledge.py#L24)
- Type: class
- Signature: `n/a`
- Direct static callees: `KnowledgeHit`, `ValueError`, `_connect`, `_entity_id`, `_init_db`, `append`, `connect`, `dumps`, `encode`, `ensure_text_file_safe`, `execute`, `fetchall`, `fetchone`, `hexdigest`, `int`, `iter_code_files`, `language_for`, `len`, `list`, `loads`, `max`, `min`, `mkdir`, `parse_code_file`, `read_text`, `relative_to`, `resolve`, `resolve_workspace_path`, `sha256`, `str`, `strip`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore.__init__` — lines 32–36

- Source: [mind01/project_knowledge.py:32](../../../../mind01/project_knowledge.py#L32)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `_init_db`, `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore._connect` — lines 38–43

- Source: [mind01/project_knowledge.py:38](../../../../mind01/project_knowledge.py#L38)
- Type: method
- Signature: `self`
- Direct static callees: `connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore._init_db` — lines 45–77

- Source: [mind01/project_knowledge.py:45](../../../../mind01/project_knowledge.py#L45)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore.refresh` — lines 79–164

- Source: [mind01/project_knowledge.py:79](../../../../mind01/project_knowledge.py#L79)
- Type: method
- Signature: `self, raw_path: str='.'`
- Direct static callees: `ValueError`, `_connect`, `_entity_id`, `dumps`, `encode`, `ensure_text_file_safe`, `execute`, `fetchall`, `fetchone`, `hexdigest`, `int`, `iter_code_files`, `language_for`, `len`, `list`, `parse_code_file`, `read_text`, `relative_to`, `resolve_workspace_path`, `sha256`, `str`, `time`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore.query` — lines 166–190

- Source: [mind01/project_knowledge.py:166](../../../../mind01/project_knowledge.py#L166)
- Type: method
- Signature: `self, term: str, limit: int=20`
- Direct static callees: `KnowledgeHit`, `_connect`, `append`, `execute`, `fetchall`, `int`, `loads`, `max`, `min`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore.relations_for` — lines 192–215

- Source: [mind01/project_knowledge.py:192](../../../../mind01/project_knowledge.py#L192)
- Type: method
- Signature: `self, entity_id: str, limit: int=50`
- Direct static callees: `_connect`, `execute`, `fetchall`, `max`, `min`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge.ProjectKnowledgeStore.stats` — lines 217–221

- Source: [mind01/project_knowledge.py:217](../../../../mind01/project_knowledge.py#L217)
- Type: method
- Signature: `self`
- Direct static callees: `_connect`, `execute`, `fetchone`, `int`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.project_knowledge._entity_id` — lines 224–226

- Source: [mind01/project_knowledge.py:224](../../../../mind01/project_knowledge.py#L224)
- Type: function
- Signature: `entity_type: str, key: str`
- Direct static callees: `encode`, `hexdigest`, `sha256`
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

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–14

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 15–21

Defines class `KnowledgeHit` and the behavior of its members.

### Lines 22–23

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 24–53

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 54–83

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 84–113

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 114–143

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 144–173

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 174–203

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 204–221

Defines class `ProjectKnowledgeStore` and the behavior of its members.

### Lines 222–223

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 224–226

Defines `_entity_id` and its implementation control flow; direct static calls: encode, hexdigest, sha256.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
