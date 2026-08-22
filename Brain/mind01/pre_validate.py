"""Static pre-validation gate for file-mutating actions.

Runs deterministic checks *before* any mutation reaches the filesystem:
1. Target file existence (for edit operations)
2. Syntactic validity (AST parse for Python, JSON parse, Verilog bracket balance)
3. Relative import integrity (Python only — checks that .module paths exist)

Invalid actions are rejected as ToolErrors, giving the model a chance to
self-repair without creating dirty state or wasting a mutation cycle.
"""
from __future__ import annotations

import ast
import json
import re
from dataclasses import asdict, dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Dict

from .tools.verify_tools import ToolError


class PreValidationError(ToolError):
    """A deterministic pre-validation check rejected a mutation before it
    touched the filesystem.

    Subclasses ``ToolError`` so the agent loop and API layer keep handling it
    as a recoverable tool error, while the routed-execution layer can
    distinguish it from runtime tool failures and report it as a failed
    (rolled-back) dispatch result.
    """


class PreValidationCode(str, Enum):
    VALID = "VALID"
    TARGET_NOT_FOUND = "TARGET_NOT_FOUND"
    SYNTAX_ERROR = "SYNTAX_ERROR"
    BROKEN_RELATIVE_IMPORT = "BROKEN_RELATIVE_IMPORT"


@dataclass(frozen=True)
class PreValidationResult:
    valid: bool
    code: str
    message: str
    details: Dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


# Tools that receive pre-validation checks.
_PREVALIDATED_TOOLS = frozenset({
    "write_file",
    "edit_file",
    "propose_write_file",
    "propose_edit_file",
})

# File suffixes eligible for syntax checking.
_PYTHON_SUFFIXES = frozenset({".py"})
_JSON_SUFFIXES = frozenset({".json"})
_VERILOG_SUFFIXES = frozenset({".v", ".sv", ".svh", ".vh"})

_OK = PreValidationResult(True, PreValidationCode.VALID.value, "", {})


def pre_validate_mutation(
    workspace: Path,
    tool_name: str,
    args: Dict[str, Any],
) -> PreValidationResult:
    """Run deterministic pre-validation for a mutation tool call.

    Returns a VALID result if no issues are detected.  Returns a specific
    failure code + message when a deterministic problem is found.
    """
    if tool_name not in _PREVALIDATED_TOOLS:
        return _OK

    raw_path = str(args.get("path", ""))
    if not raw_path:
        return _OK  # Schema validation will catch missing paths.

    root = workspace.resolve()
    target = (root / raw_path).resolve()

    # --- Check 1: edit target must exist ---
    if tool_name in {"edit_file", "propose_edit_file"}:
        result = _check_edit_target_exists(root, target, raw_path)
        if not result.valid:
            return result

    # --- Compute the content that will be written ---
    content = _resolve_content(root, target, tool_name, args)
    if content is None:
        return _OK  # Cannot determine content; let the tool handler validate.

    suffix = Path(raw_path).suffix.lower()

    # --- Check 2: syntactic validity ---
    syntax = _check_syntax(suffix, content, raw_path)
    if not syntax.valid:
        return syntax

    # --- Check 3: relative import integrity (Python only) ---
    if suffix in _PYTHON_SUFFIXES:
        imports = _check_import_integrity(root, target, content, raw_path)
        if not imports.valid:
            return imports

    return _OK


# ---------------------------------------------------------------------------
# Check implementations
# ---------------------------------------------------------------------------


def _check_edit_target_exists(
    root: Path,
    target: Path,
    raw_path: str,
) -> PreValidationResult:
    """For edit_file / propose_edit_file: the file must already exist."""
    if not target.is_file():
        return PreValidationResult(
            valid=False,
            code=PreValidationCode.TARGET_NOT_FOUND.value,
            message=f"edit_file target does not exist: {raw_path}. Use write_file to create new files.",
            details={"path": raw_path},
        )
    return _OK


def _check_syntax(
    suffix: str,
    content: str,
    raw_path: str,
) -> PreValidationResult:
    """Language-specific syntax check on the proposed file content."""
    if suffix in _PYTHON_SUFFIXES:
        return _check_python_syntax(content, raw_path)
    if suffix in _JSON_SUFFIXES:
        return _check_json_syntax(content, raw_path)
    if suffix in _VERILOG_SUFFIXES:
        return _check_verilog_syntax(content, raw_path)
    return _OK


def _check_python_syntax(content: str, raw_path: str) -> PreValidationResult:
    """AST-parse the proposed Python content."""
    try:
        ast.parse(content, filename=raw_path)
        return _OK
    except SyntaxError as exc:
        return PreValidationResult(
            valid=False,
            code=PreValidationCode.SYNTAX_ERROR.value,
            message=(
                f"Python syntax error in proposed content for {raw_path}: "
                f"{exc.msg} (line {exc.lineno}, col {exc.offset})"
            ),
            details={
                "path": raw_path,
                "language": "python",
                "line": exc.lineno,
                "col": exc.offset,
                "error": exc.msg or str(exc),
            },
        )


def _check_json_syntax(content: str, raw_path: str) -> PreValidationResult:
    """JSON-parse the proposed content."""
    try:
        json.loads(content)
        return _OK
    except json.JSONDecodeError as exc:
        return PreValidationResult(
            valid=False,
            code=PreValidationCode.SYNTAX_ERROR.value,
            message=(
                f"JSON syntax error in proposed content for {raw_path}: "
                f"{exc.msg} (line {exc.lineno}, col {exc.colno})"
            ),
            details={
                "path": raw_path,
                "language": "json",
                "line": exc.lineno,
                "col": exc.colno,
                "error": exc.msg,
            },
        )


def _check_verilog_syntax(content: str, raw_path: str) -> PreValidationResult:
    """Basic Verilog bracket / module-endmodule balance check.

    This is a lightweight heuristic — not a full parser.  It catches the
    most common LLM-generated Verilog errors (mismatched begin/end,
    module/endmodule) without requiring an external tool.
    """
    # Strip single-line comments and string literals for counting.
    cleaned = re.sub(r'//[^\n]*', '', content)
    cleaned = re.sub(r'"[^"]*"', '""', cleaned)

    module_count = len(re.findall(r'\bmodule\b', cleaned))
    endmodule_count = len(re.findall(r'\bendmodule\b', cleaned))
    begin_count = len(re.findall(r'\bbegin\b', cleaned))
    end_count = len(re.findall(r'\bend\b', cleaned))

    issues: list[str] = []
    if module_count != endmodule_count:
        issues.append(
            f"module/endmodule mismatch: {module_count} module vs {endmodule_count} endmodule"
        )
    if begin_count != end_count:
        issues.append(
            f"begin/end mismatch: {begin_count} begin vs {end_count} end"
        )

    if issues:
        return PreValidationResult(
            valid=False,
            code=PreValidationCode.SYNTAX_ERROR.value,
            message=f"Verilog syntax issue in {raw_path}: {'; '.join(issues)}",
            details={
                "path": raw_path,
                "language": "verilog",
                "issues": issues,
            },
        )
    return _OK


def _check_import_integrity(
    root: Path,
    target: Path,
    content: str,
    raw_path: str,
) -> PreValidationResult:
    """Check that relative imports reference modules that exist in the workspace.

    Only checks *relative* imports (from .X import Y, from ..X import Y).
    Absolute and third-party imports are not validated since they may
    resolve at runtime via installed packages.
    """
    try:
        tree = ast.parse(content, filename=raw_path)
    except SyntaxError:
        return _OK  # Syntax check already caught this.

    package_dir = target.parent
    broken: list[str] = []

    for node in ast.walk(tree):
        if not isinstance(node, (ast.Import, ast.ImportFrom)):
            continue
        if not isinstance(node, ast.ImportFrom) or node.level == 0:
            continue  # Skip absolute imports.
        if node.module is None:
            continue  # `from . import X` — package-level import, skip.

        # Resolve the relative import path.
        base = package_dir
        for _ in range(node.level - 1):
            base = base.parent

        parts = node.module.split(".")
        # Check as module file (e.g., base / parts[0] / parts[1] / ... .py)
        module_path = base
        for part in parts:
            module_path = module_path / part

        module_file = module_path.with_suffix(".py")
        module_package = module_path / "__init__.py"

        if not module_file.is_file() and not module_package.is_file():
            # Check if the import is from the file being written itself
            # (self-referencing edits are fine).
            if module_file.resolve() == target.resolve():
                continue
            import_str = "." * node.level + node.module
            broken.append(import_str)

    if broken:
        return PreValidationResult(
            valid=False,
            code=PreValidationCode.BROKEN_RELATIVE_IMPORT.value,
            message=(
                f"Broken relative import(s) in proposed content for {raw_path}: "
                f"{', '.join(broken)}. "
                f"The referenced module(s) do not exist in the workspace."
            ),
            details={
                "path": raw_path,
                "broken_imports": broken,
            },
        )
    return _OK


# ---------------------------------------------------------------------------
# Content resolution
# ---------------------------------------------------------------------------


def _resolve_content(
    root: Path,
    target: Path,
    tool_name: str,
    args: Dict[str, Any],
) -> str | None:
    """Determine the final file content that would result from this action.

    Returns None when the content cannot be determined (e.g., missing args
    that the schema validator will catch).
    """
    if tool_name in {"write_file", "propose_write_file"}:
        content = args.get("content")
        return str(content) if content is not None else None

    if tool_name in {"edit_file", "propose_edit_file"}:
        old = args.get("old")
        new = args.get("new")
        if old is None or new is None:
            return None
        if not target.is_file():
            return None  # _check_edit_target_exists will catch this.
        try:
            current = target.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return None  # Let the tool handler deal with unreadable files.
        if str(old) not in current:
            return None  # Let the tool handler report "old text not found".
        return current.replace(str(old), str(new), 1)

    return None
