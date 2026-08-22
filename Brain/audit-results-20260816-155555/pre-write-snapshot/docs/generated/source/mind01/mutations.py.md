# `mind01/mutations.py`

## File purpose

This filesystem and mutations file is reviewed at snapshot `05446c4bc04c45b5cbaf2dfee7b47290dc484a27d1619d1a3e7d99189f3bcbd1`. It contains 333 lines.

## Imports and module state

- [mind01/mutations.py:1](../../../../mind01/mutations.py#L1) imports `__future__` / annotations.
- [mind01/mutations.py:3](../../../../mind01/mutations.py#L3) imports `hashlib`.
- [mind01/mutations.py:4](../../../../mind01/mutations.py#L4) imports `json`.
- [mind01/mutations.py:5](../../../../mind01/mutations.py#L5) imports `os`.
- [mind01/mutations.py:6](../../../../mind01/mutations.py#L6) imports `shutil`.
- [mind01/mutations.py:7](../../../../mind01/mutations.py#L7) imports `time`.
- [mind01/mutations.py:8](../../../../mind01/mutations.py#L8) imports `uuid`.
- [mind01/mutations.py:9](../../../../mind01/mutations.py#L9) imports `dataclasses` / dataclass.
- [mind01/mutations.py:10](../../../../mind01/mutations.py#L10) imports `datetime` / datetime.
- [mind01/mutations.py:10](../../../../mind01/mutations.py#L10) imports `datetime` / timezone.
- [mind01/mutations.py:11](../../../../mind01/mutations.py#L11) imports `pathlib` / Path.
- [mind01/mutations.py:12](../../../../mind01/mutations.py#L12) imports `typing` / Callable.
- [mind01/mutations.py:14](../../../../mind01/mutations.py#L14) imports `file_safety` / FileSafetyError.
- [mind01/mutations.py:14](../../../../mind01/mutations.py#L14) imports `file_safety` / ensure_write_target_safe.
- [mind01/mutations.py:14](../../../../mind01/mutations.py#L14) imports `file_safety` / relative_path.

## Symbols

### `mind01.mutations.MutationError` — lines 17–27

- Source: [mind01/mutations.py:17](../../../../mind01/mutations.py#L17)
- Type: class
- Signature: `n/a`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.MutationError.__init__` — lines 18–27

- Source: [mind01/mutations.py:18](../../../../mind01/mutations.py#L18)
- Type: method
- Signature: `self, message: str, *, restored: bool=False, dirty_id: str | None=None`
- Direct static callees: `__init__`, `super`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.FileState` — lines 31–34

- Source: [mind01/mutations.py:31](../../../../mind01/mutations.py#L31)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.MutationResult` — lines 38–46

- Source: [mind01/mutations.py:38](../../../../mind01/mutations.py#L38)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore` — lines 49–134

- Source: [mind01/mutations.py:49](../../../../mind01/mutations.py#L49)
- Type: class
- Signature: `n/a`
- Direct static callees: `MutationError`, `_path`, `append`, `dumps`, `exists`, `get`, `glob`, `isinstance`, `isoformat`, `join`, `len`, `list`, `loads`, `make_dirty_id`, `mkdir`, `now`, `read_text`, `relative_path`, `resolve`, `sorted`, `startswith`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.__init__` — lines 50–53

- Source: [mind01/mutations.py:50](../../../../mind01/mutations.py#L50)
- Type: method
- Signature: `self, workspace: Path`
- Direct static callees: `mkdir`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.create` — lines 55–92

- Source: [mind01/mutations.py:55](../../../../mind01/mutations.py#L55)
- Type: method
- Signature: `self, *, operation: str, target: Path, before: FileState, intended_after: FileState, current: FileState, backup_path: str | None, error: str, recovery_status: str`
- Direct static callees: `_path`, `dumps`, `isoformat`, `make_dirty_id`, `now`, `relative_path`, `str`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.list` — lines 94–103

- Source: [mind01/mutations.py:94](../../../../mind01/mutations.py#L94)
- Type: method
- Signature: `self, limit: int=50`
- Direct static callees: `append`, `glob`, `len`, `loads`, `read_text`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.get` — lines 105–115

- Source: [mind01/mutations.py:105](../../../../mind01/mutations.py#L105)
- Type: method
- Signature: `self, dirty_id: str`
- Direct static callees: `MutationError`, `_path`, `exists`, `isinstance`, `loads`, `read_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.render_list` — lines 117–126

- Source: [mind01/mutations.py:117](../../../../mind01/mutations.py#L117)
- Type: method
- Signature: `self, limit: int=50`
- Direct static callees: `get`, `join`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore.render_show` — lines 128–129

- Source: [mind01/mutations.py:128](../../../../mind01/mutations.py#L128)
- Type: method
- Signature: `self, dirty_id: str`
- Direct static callees: `dumps`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.DirtyStateStore._path` — lines 131–134

- Source: [mind01/mutations.py:131](../../../../mind01/mutations.py#L131)
- Type: method
- Signature: `self, dirty_id: str`
- Direct static callees: `MutationError`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.execute_content_mutation` — lines 137–227

- Source: [mind01/mutations.py:137](../../../../mind01/mutations.py#L137)
- Type: function
- Signature: `*, workspace: Path, raw_path: str, operation: str, receipt_id: str, content: str | None, delete: bool, write_success_metadata: Callable[[MutationResult], None]`
- Direct static callees: `DirtyStateStore`, `MutationError`, `MutationResult`, `create`, `create_backup`, `ensure_write_target_safe`, `exists`, `file_state`, `fsync_directory`, `intended_state`, `mkdir`, `relative_path`, `replace`, `resolve`, `restore_previous_state`, `str`, `type`, `unlink`, `verify_state`, `verify_state_matches`, `write_success_metadata`, `write_temp_file`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.create_backup` — lines 230–240

- Source: [mind01/mutations.py:230](../../../../mind01/mutations.py#L230)
- Type: function
- Signature: `workspace: Path, target: Path, receipt_id: str`
- Direct static callees: `MutationError`, `copy2`, `mkdir`, `relative_path`, `replace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.restore_previous_state` — lines 243–266

- Source: [mind01/mutations.py:243](../../../../mind01/mutations.py#L243)
- Type: function
- Signature: `workspace: Path, target: Path, before: FileState, backup_path: str | None`
- Direct static callees: `MutationError`, `copy2`, `exists`, `fsync_directory`, `is_file`, `mkdir`, `resolve`, `unlink`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.write_temp_file` — lines 269–278

- Source: [mind01/mutations.py:269](../../../../mind01/mutations.py#L269)
- Type: function
- Signature: `target: Path, content: str`
- Direct static callees: `MutationError`, `fileno`, `flush`, `fsync`, `open`, `uuid4`, `write`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.verify_state` — lines 281–284

- Source: [mind01/mutations.py:281](../../../../mind01/mutations.py#L281)
- Type: function
- Signature: `path: Path, expected: FileState, label: str`
- Direct static callees: `MutationError`, `file_state`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.verify_state_matches` — lines 287–291

- Source: [mind01/mutations.py:287](../../../../mind01/mutations.py#L287)
- Type: function
- Signature: `actual: FileState, expected: FileState, rel_path: str`
- Direct static callees: `MutationError`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.intended_state` — lines 294–300

- Source: [mind01/mutations.py:294](../../../../mind01/mutations.py#L294)
- Type: function
- Signature: `content: str | None, delete: bool`
- Direct static callees: `FileState`, `MutationError`, `encode`, `hexdigest`, `len`, `sha256`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.file_state` — lines 303–306

- Source: [mind01/mutations.py:303](../../../../mind01/mutations.py#L303)
- Type: function
- Signature: `path: Path`
- Direct static callees: `FileState`, `exists`, `sha256_file`, `stat`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.sha256_file` — lines 309–314

- Source: [mind01/mutations.py:309](../../../../mind01/mutations.py#L309)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `iter`, `open`, `read`, `sha256`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.fsync_directory` — lines 317–327

- Source: [mind01/mutations.py:317](../../../../mind01/mutations.py#L317)
- Type: function
- Signature: `path: Path`
- Direct static callees: `close`, `fsync`, `open`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.mutations.make_dirty_id` — lines 330–333

- Source: [mind01/mutations.py:330](../../../../mind01/mutations.py#L330)
- Type: function
- Signature: `operation: str`
- Direct static callees: `isalnum`, `join`, `now`, `strftime`, `time_ns`, `uuid4`
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

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–27

Defines class `MutationError` and the behavior of its members.

### Lines 28–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–34

Defines class `FileState` and the behavior of its members.

### Lines 35–37

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 38–46

Defines class `MutationResult` and the behavior of its members.

### Lines 47–48

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 49–78

Defines class `DirtyStateStore` and the behavior of its members.

### Lines 79–108

Defines class `DirtyStateStore` and the behavior of its members.

### Lines 109–134

Defines class `DirtyStateStore` and the behavior of its members.

### Lines 135–136

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 137–166

Defines `execute_content_mutation` and its implementation control flow; direct static calls: DirtyStateStore, MutationError, MutationResult, create, create_backup, ensure_write_target_safe, exists, file_state, fsync_directory, intended_state, mkdir, relative_path, replace, resolve, restore_previous_state, str, type, unlink, verify_state, verify_state_matches, write_success_metadata, write_temp_file.

### Lines 167–196

Defines `execute_content_mutation` and its implementation control flow; direct static calls: DirtyStateStore, MutationError, MutationResult, create, create_backup, ensure_write_target_safe, exists, file_state, fsync_directory, intended_state, mkdir, relative_path, replace, resolve, restore_previous_state, str, type, unlink, verify_state, verify_state_matches, write_success_metadata, write_temp_file.

### Lines 197–226

Defines `execute_content_mutation` and its implementation control flow; direct static calls: DirtyStateStore, MutationError, MutationResult, create, create_backup, ensure_write_target_safe, exists, file_state, fsync_directory, intended_state, mkdir, relative_path, replace, resolve, restore_previous_state, str, type, unlink, verify_state, verify_state_matches, write_success_metadata, write_temp_file.

### Lines 227–227

Defines `execute_content_mutation` and its implementation control flow; direct static calls: DirtyStateStore, MutationError, MutationResult, create, create_backup, ensure_write_target_safe, exists, file_state, fsync_directory, intended_state, mkdir, relative_path, replace, resolve, restore_previous_state, str, type, unlink, verify_state, verify_state_matches, write_success_metadata, write_temp_file.

### Lines 228–229

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 230–240

Defines `create_backup` and its implementation control flow; direct static calls: MutationError, copy2, mkdir, relative_path, replace.

### Lines 241–242

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 243–266

Defines `restore_previous_state` and its implementation control flow; direct static calls: MutationError, copy2, exists, fsync_directory, is_file, mkdir, resolve, unlink.

### Lines 267–268

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 269–278

Defines `write_temp_file` and its implementation control flow; direct static calls: MutationError, fileno, flush, fsync, open, uuid4, write.

### Lines 279–280

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 281–284

Defines `verify_state` and its implementation control flow; direct static calls: MutationError, file_state.

### Lines 285–286

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 287–291

Defines `verify_state_matches` and its implementation control flow; direct static calls: MutationError.

### Lines 292–293

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 294–300

Defines `intended_state` and its implementation control flow; direct static calls: FileState, MutationError, encode, hexdigest, len, sha256.

### Lines 301–302

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 303–306

Defines `file_state` and its implementation control flow; direct static calls: FileState, exists, sha256_file, stat.

### Lines 307–308

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 309–314

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, iter, open, read, sha256, update.

### Lines 315–316

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 317–327

Defines `fsync_directory` and its implementation control flow; direct static calls: close, fsync, open, str.

### Lines 328–329

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 330–333

Defines `make_dirty_id` and its implementation control flow; direct static calls: isalnum, join, now, strftime, time_ns, uuid4.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
