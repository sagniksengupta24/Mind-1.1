# `mind01/self_correction.py`

## File purpose

This verification and correction file is reviewed at snapshot `64bc6fe0435a33452e5e0d8afdf05e27cb38b093a0d91da1570ef788fe0cda33`. It contains 381 lines.

## Imports and module state

- [mind01/self_correction.py:1](../../../../mind01/self_correction.py#L1) imports `__future__` / annotations.
- [mind01/self_correction.py:3](../../../../mind01/self_correction.py#L3) imports `difflib`.
- [mind01/self_correction.py:4](../../../../mind01/self_correction.py#L4) imports `hashlib`.
- [mind01/self_correction.py:5](../../../../mind01/self_correction.py#L5) imports `os`.
- [mind01/self_correction.py:6](../../../../mind01/self_correction.py#L6) imports `shutil`.
- [mind01/self_correction.py:7](../../../../mind01/self_correction.py#L7) imports `subprocess`.
- [mind01/self_correction.py:8](../../../../mind01/self_correction.py#L8) imports `time`.
- [mind01/self_correction.py:9](../../../../mind01/self_correction.py#L9) imports `dataclasses` / asdict.
- [mind01/self_correction.py:9](../../../../mind01/self_correction.py#L9) imports `dataclasses` / dataclass.
- [mind01/self_correction.py:9](../../../../mind01/self_correction.py#L9) imports `dataclasses` / field.
- [mind01/self_correction.py:10](../../../../mind01/self_correction.py#L10) imports `enum` / Enum.
- [mind01/self_correction.py:11](../../../../mind01/self_correction.py#L11) imports `pathlib` / Path.
- [mind01/self_correction.py:12](../../../../mind01/self_correction.py#L12) imports `typing` / Callable.
- [mind01/self_correction.py:12](../../../../mind01/self_correction.py#L12) imports `typing` / Iterable.
- [mind01/self_correction.py:12](../../../../mind01/self_correction.py#L12) imports `typing` / Sequence.
- [mind01/self_correction.py:14](../../../../mind01/self_correction.py#L14) imports `completion` / CompletionContract.
- [mind01/self_correction.py:14](../../../../mind01/self_correction.py#L14) imports `completion` / VerificationEvidence.
- [mind01/self_correction.py:14](../../../../mind01/self_correction.py#L14) imports `completion` / build_completion_contract.
- [mind01/self_correction.py:15](../../../../mind01/self_correction.py#L15) imports `patch_review` / review_patch.

## Symbols

### `mind01.self_correction.FailureCategory` — lines 18–33

- Source: [mind01/self_correction.py:18](../../../../mind01/self_correction.py#L18)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.VerificationFailure` — lines 37–46

- Source: [mind01/self_correction.py:37](../../../../mind01/self_correction.py#L37)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.VerificationFailure.to_dict` — lines 43–46

- Source: [mind01/self_correction.py:43](../../../../mind01/self_correction.py#L43)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.RepairPlan` — lines 50–53

- Source: [mind01/self_correction.py:50](../../../../mind01/self_correction.py#L50)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.RepairAttempt` — lines 57–71

- Source: [mind01/self_correction.py:57](../../../../mind01/self_correction.py#L57)
- Type: class
- Signature: `n/a`
- Direct static callees: `asdict`, `dataclass`, `field`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.RepairAttempt.to_dict` — lines 67–71

- Source: [mind01/self_correction.py:67](../../../../mind01/self_correction.py#L67)
- Type: method
- Signature: `self`
- Direct static callees: `asdict`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.CorrectionState` — lines 75–81

- Source: [mind01/self_correction.py:75](../../../../mind01/self_correction.py#L75)
- Type: class
- Signature: `n/a`
- Direct static callees: `field`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.CorrectionOutcome` — lines 85–95

- Source: [mind01/self_correction.py:85](../../../../mind01/self_correction.py#L85)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.CorrectionOutcome.to_dict` — lines 90–95

- Source: [mind01/self_correction.py:90](../../../../mind01/self_correction.py#L90)
- Type: method
- Signature: `self`
- Direct static callees: `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.RepairExecutor` — lines 98–98

- Source: [mind01/self_correction.py:98](../../../../mind01/self_correction.py#L98)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot` — lines 101–146

- Source: [mind01/self_correction.py:101](../../../../mind01/self_correction.py#L101)
- Type: class
- Signature: `n/a`
- Direct static callees: `as_posix`, `capture`, `changed_files`, `cls`, `decode_for_diff`, `extend`, `get`, `is_file`, `items`, `join`, `mkdir`, `read_bytes`, `relative_to`, `remove_empty_dirs`, `resolve`, `rglob`, `set`, `should_skip_snapshot_path`, `sorted`, `splitlines`, `unified_diff`, `unlink`, `write_bytes`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot.__init__` — lines 102–104

- Source: [mind01/self_correction.py:102](../../../../mind01/self_correction.py#L102)
- Type: method
- Signature: `self, workspace: Path, files: dict[str, bytes]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot.capture` — lines 107–114

- Source: [mind01/self_correction.py:107](../../../../mind01/self_correction.py#L107)
- Type: method
- Signature: `cls, workspace: Path`
- Direct static callees: `as_posix`, `cls`, `is_file`, `read_bytes`, `relative_to`, `resolve`, `rglob`, `should_skip_snapshot_path`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot.changed_files` — lines 116–118

- Source: [mind01/self_correction.py:116](../../../../mind01/self_correction.py#L116)
- Type: method
- Signature: `self, other: 'WorkspaceSnapshot'`
- Direct static callees: `get`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot.diff` — lines 120–133

- Source: [mind01/self_correction.py:120](../../../../mind01/self_correction.py#L120)
- Type: method
- Signature: `self, other: 'WorkspaceSnapshot'`
- Direct static callees: `changed_files`, `decode_for_diff`, `extend`, `get`, `join`, `splitlines`, `unified_diff`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.WorkspaceSnapshot.restore` — lines 135–146

- Source: [mind01/self_correction.py:135](../../../../mind01/self_correction.py#L135)
- Type: method
- Signature: `self`
- Direct static callees: `capture`, `changed_files`, `items`, `mkdir`, `remove_empty_dirs`, `sorted`, `unlink`, `write_bytes`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.should_skip_snapshot_path` — lines 149–151

- Source: [mind01/self_correction.py:149](../../../../mind01/self_correction.py#L149)
- Type: function
- Signature: `path: Path, root: Path`
- Direct static callees: `any`, `relative_to`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.remove_empty_dirs` — lines 154–160

- Source: [mind01/self_correction.py:154](../../../../mind01/self_correction.py#L154)
- Type: function
- Signature: `root: Path`
- Direct static callees: `is_dir`, `len`, `rglob`, `rmdir`, `should_skip_snapshot_path`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.decode_for_diff` — lines 163–167

- Source: [mind01/self_correction.py:163](../../../../mind01/self_correction.py#L163)
- Type: function
- Signature: `content: bytes`
- Direct static callees: `decode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.classify_failure` — lines 170–194

- Source: [mind01/self_correction.py:170](../../../../mind01/self_correction.py#L170)
- Type: function
- Signature: `output: str, *, exit_code: int | None=None, timed_out: bool=False`
- Direct static callees: `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.repair_plan_for_failure` — lines 197–210

- Source: [mind01/self_correction.py:197](../../../../mind01/self_correction.py#L197)
- Type: function
- Signature: `failure: VerificationFailure, changed_files: list[str]`
- Direct static callees: `RepairPlan`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.run_command_verification` — lines 213–256

- Source: [mind01/self_correction.py:213](../../../../mind01/self_correction.py#L213)
- Type: function
- Signature: `workspace: Path, command: Sequence[str], *, timeout_seconds: int=60, name: str='command'`
- Direct static callees: `VerificationEvidence`, `isinstance`, `list`, `perf_counter`, `round`, `run`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.SelfCorrectionController` — lines 259–365

- Source: [mind01/self_correction.py:259](../../../../mind01/self_correction.py#L259)
- Type: class
- Signature: `n/a`
- Direct static callees: `CorrectionOutcome`, `CorrectionState`, `RepairAttempt`, `VerificationFailure`, `all`, `any`, `append`, `bool`, `build_completion_contract`, `capture`, `changed_files`, `diff`, `enumerate`, `executor`, `first_failure`, `get`, `len`, `max`, `min`, `range`, `repair_plan_for_failure`, `resolve`, `restore`, `review_patch`, `run_command_verification`, `sha256_text`, `to_dicts`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.SelfCorrectionController.__init__` — lines 260–262

- Source: [mind01/self_correction.py:260](../../../../mind01/self_correction.py#L260)
- Type: method
- Signature: `self, workspace: Path, *, repair_budget: int=2`
- Direct static callees: `max`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.SelfCorrectionController.run` — lines 264–365

- Source: [mind01/self_correction.py:264](../../../../mind01/self_correction.py#L264)
- Type: method
- Signature: `self, *, objective: str, repair_executors: Sequence[RepairExecutor], verification_commands: Sequence[Sequence[str]], expected_paths: list[str] | None=None`
- Direct static callees: `CorrectionOutcome`, `CorrectionState`, `RepairAttempt`, `VerificationFailure`, `all`, `any`, `append`, `bool`, `build_completion_contract`, `capture`, `changed_files`, `diff`, `enumerate`, `executor`, `first_failure`, `get`, `len`, `max`, `min`, `range`, `repair_plan_for_failure`, `restore`, `review_patch`, `run_command_verification`, `sha256_text`, `to_dicts`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.first_failure` — lines 368–377

- Source: [mind01/self_correction.py:368](../../../../mind01/self_correction.py#L368)
- Type: function
- Signature: `verification: Iterable[VerificationEvidence]`
- Direct static callees: `VerificationFailure`, `classify_failure`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.self_correction.sha256_text` — lines 380–381

- Source: [mind01/self_correction.py:380](../../../../mind01/self_correction.py#L380)
- Type: function
- Signature: `text: str`
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

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–33

Defines class `FailureCategory` and the behavior of its members.

### Lines 34–36

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 37–46

Defines class `VerificationFailure` and the behavior of its members.

### Lines 47–49

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 50–53

Defines class `RepairPlan` and the behavior of its members.

### Lines 54–56

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 57–71

Defines class `RepairAttempt` and the behavior of its members.

### Lines 72–74

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 75–81

Defines class `CorrectionState` and the behavior of its members.

### Lines 82–84

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 85–95

Defines class `CorrectionOutcome` and the behavior of its members.

### Lines 96–97

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 98–98

Implements module-level `Assign` behavior or data.

### Lines 99–100

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 101–130

Defines class `WorkspaceSnapshot` and the behavior of its members.

### Lines 131–146

Defines class `WorkspaceSnapshot` and the behavior of its members.

### Lines 147–148

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 149–151

Defines `should_skip_snapshot_path` and its implementation control flow; direct static calls: any, relative_to.

### Lines 152–153

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 154–160

Defines `remove_empty_dirs` and its implementation control flow; direct static calls: is_dir, len, rglob, rmdir, should_skip_snapshot_path, sorted.

### Lines 161–162

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 163–167

Defines `decode_for_diff` and its implementation control flow; direct static calls: decode.

### Lines 168–169

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 170–194

Defines `classify_failure` and its implementation control flow; direct static calls: lower.

### Lines 195–196

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 197–210

Defines `repair_plan_for_failure` and its implementation control flow; direct static calls: RepairPlan.

### Lines 211–212

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 213–242

Defines `run_command_verification` and its implementation control flow; direct static calls: VerificationEvidence, isinstance, list, perf_counter, round, run, str.

### Lines 243–256

Defines `run_command_verification` and its implementation control flow; direct static calls: VerificationEvidence, isinstance, list, perf_counter, round, run, str.

### Lines 257–258

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 259–288

Defines class `SelfCorrectionController` and the behavior of its members.

### Lines 289–318

Defines class `SelfCorrectionController` and the behavior of its members.

### Lines 319–348

Defines class `SelfCorrectionController` and the behavior of its members.

### Lines 349–365

Defines class `SelfCorrectionController` and the behavior of its members.

### Lines 366–367

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 368–377

Defines `first_failure` and its implementation control flow; direct static calls: VerificationFailure, classify_failure.

### Lines 378–379

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 380–381

Defines `sha256_text` and its implementation control flow; direct static calls: encode, hexdigest, sha256.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
