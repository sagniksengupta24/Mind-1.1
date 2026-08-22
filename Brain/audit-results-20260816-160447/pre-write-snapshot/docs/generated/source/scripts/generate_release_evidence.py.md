# `scripts/generate_release_evidence.py`

## File purpose

This automation and release file is reviewed at snapshot `57fde4c772b7d4677216bffe84f4e45bf2e62adb67ea02b702645fb4191f2c6a`. It contains 283 lines.

## Imports and module state

- [scripts/generate_release_evidence.py:1](../../../../scripts/generate_release_evidence.py#L1) imports `__future__` / annotations.
- [scripts/generate_release_evidence.py:3](../../../../scripts/generate_release_evidence.py#L3) imports `argparse`.
- [scripts/generate_release_evidence.py:4](../../../../scripts/generate_release_evidence.py#L4) imports `hashlib`.
- [scripts/generate_release_evidence.py:5](../../../../scripts/generate_release_evidence.py#L5) imports `json`.
- [scripts/generate_release_evidence.py:6](../../../../scripts/generate_release_evidence.py#L6) imports `os`.
- [scripts/generate_release_evidence.py:7](../../../../scripts/generate_release_evidence.py#L7) imports `platform`.
- [scripts/generate_release_evidence.py:8](../../../../scripts/generate_release_evidence.py#L8) imports `shutil`.
- [scripts/generate_release_evidence.py:9](../../../../scripts/generate_release_evidence.py#L9) imports `subprocess`.
- [scripts/generate_release_evidence.py:10](../../../../scripts/generate_release_evidence.py#L10) imports `sys`.
- [scripts/generate_release_evidence.py:11](../../../../scripts/generate_release_evidence.py#L11) imports `tempfile`.
- [scripts/generate_release_evidence.py:12](../../../../scripts/generate_release_evidence.py#L12) imports `time`.
- [scripts/generate_release_evidence.py:13](../../../../scripts/generate_release_evidence.py#L13) imports `zipfile`.
- [scripts/generate_release_evidence.py:14](../../../../scripts/generate_release_evidence.py#L14) imports `datetime` / datetime.
- [scripts/generate_release_evidence.py:14](../../../../scripts/generate_release_evidence.py#L14) imports `datetime` / timezone.
- [scripts/generate_release_evidence.py:15](../../../../scripts/generate_release_evidence.py#L15) imports `pathlib` / Path.
- [scripts/generate_release_evidence.py:16](../../../../scripts/generate_release_evidence.py#L16) imports `typing` / Any.
- [scripts/generate_release_evidence.py:20](../../../../scripts/generate_release_evidence.py#L20) imports `scripts.build_release` / build_release.

## Symbols

### `scripts.generate_release_evidence.ROOT` — lines 18–18

- Source: [scripts/generate_release_evidence.py:18](../../../../scripts/generate_release_evidence.py#L18)
- Type: constant
- Signature: `n/a`
- Direct static callees: `Path`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.sha256_file` — lines 23–28

- Source: [scripts/generate_release_evidence.py:23](../../../../scripts/generate_release_evidence.py#L23)
- Type: function
- Signature: `path: Path`
- Direct static callees: `hexdigest`, `iter`, `open`, `read`, `sha256`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.run_command` — lines 31–62

- Source: [scripts/generate_release_evidence.py:31](../../../../scripts/generate_release_evidence.py#L31)
- Type: function
- Signature: `argv: list[str], *, timeout: int=240, cwd: Path=ROOT`
- Direct static callees: `monotonic`, `round`, `run`, `str`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.git_text` — lines 65–69

- Source: [scripts/generate_release_evidence.py:65](../../../../scripts/generate_release_evidence.py#L65)
- Type: function
- Signature: `*args: str`
- Direct static callees: `run_command`, `str`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.tool_version` — lines 72–81

- Source: [scripts/generate_release_evidence.py:72](../../../../scripts/generate_release_evidence.py#L72)
- Type: function
- Signature: `argv: list[str]`
- Direct static callees: `run_command`, `str`, `strip`, `which`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.main` — lines 84–242

- Source: [scripts/generate_release_evidence.py:84](../../../../scripts/generate_release_evidence.py#L84)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `Path`, `RuntimeError`, `TemporaryDirectory`, `ZipFile`, `add_argument`, `all`, `append`, `bool`, `build_release`, `copy2`, `dumps`, `encode`, `expanduser`, `extractall`, `git_text`, `glob`, `hexdigest`, `int`, `is_dir`, `isoformat`, `iterdir`, `len`, `list`, `mkdir`, `now`, `parse_args`, `platform`, `print`, `relative_to`, `render_report`, `resolve`, `run_command`, `run_truthful_completion_regression`, `sha256`, `sha256_file`, `str`, `tool_version`, `write_text`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `scripts.generate_release_evidence.render_report` — lines 245–279

- Source: [scripts/generate_release_evidence.py:245](../../../../scripts/generate_release_evidence.py#L245)
- Type: function
- Signature: `manifest: dict[str, Any]`
- Direct static callees: `join`
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

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 18–18

Implements module-level `Assign` behavior or data.

### Lines 19–19

Implements module-level `Expr` behavior or data.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–22

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 23–28

Defines `sha256_file` and its implementation control flow; direct static calls: hexdigest, iter, open, read, sha256, update.

### Lines 29–30

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 31–60

Defines `run_command` and its implementation control flow; direct static calls: monotonic, round, run, str, type.

### Lines 61–62

Defines `run_command` and its implementation control flow; direct static calls: monotonic, round, run, str, type.

### Lines 63–64

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 65–69

Defines `git_text` and its implementation control flow; direct static calls: run_command, str, strip.

### Lines 70–71

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 72–81

Defines `tool_version` and its implementation control flow; direct static calls: run_command, str, strip, which.

### Lines 82–83

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 84–113

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 114–143

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 144–173

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 174–203

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 204–233

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 234–242

Defines `main` and its implementation control flow; direct static calls: ArgumentParser, Path, RuntimeError, TemporaryDirectory, ZipFile, add_argument, all, append, bool, build_release, copy2, dumps, encode, expanduser, extractall, git_text, glob, hexdigest, int, is_dir, isoformat, iterdir, len, list, mkdir, now, parse_args, platform, print, relative_to, render_report, resolve, run_command, run_truthful_completion_regression, sha256, sha256_file, str, tool_version, write_text.

### Lines 243–244

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 245–274

Defines `render_report` and its implementation control flow; direct static calls: join.

### Lines 275–279

Defines `render_report` and its implementation control flow; direct static calls: join.

### Lines 280–281

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 282–283

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
