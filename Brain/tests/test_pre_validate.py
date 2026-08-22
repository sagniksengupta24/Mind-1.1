"""Unit tests for mind01.pre_validate — static pre-validation gate.

Tests cover:
- Edit target existence
- Python syntax checking (valid & invalid)
- JSON syntax checking
- Verilog bracket balance
- Relative import integrity
- Integration with ToolRegistry dispatch
"""
from __future__ import annotations

import json
import textwrap
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from mind01.pre_validate import (
    PreValidationCode,
    PreValidationResult,
    _PREVALIDATED_TOOLS,
    pre_validate_mutation,
)


# ---------------------------------------------------------------------------
# 1. Edit non-existent file → TARGET_NOT_FOUND
# ---------------------------------------------------------------------------


def test_edit_nonexistent_file_is_rejected(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "edit_file",
        {"path": "does_not_exist.py", "old": "x", "new": "y"},
    )
    assert not result.valid
    assert result.code == PreValidationCode.TARGET_NOT_FOUND.value
    assert "does_not_exist.py" in result.message
    assert "write_file" in result.message  # Helpful hint


# ---------------------------------------------------------------------------
# 2. Write valid Python → VALID
# ---------------------------------------------------------------------------


def test_write_valid_python_passes(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "module.py", "content": "def hello():\n    return 1\n"},
    )
    assert result.valid
    assert result.code == PreValidationCode.VALID.value


# ---------------------------------------------------------------------------
# 3. Write invalid Python → SYNTAX_ERROR with line/col
# ---------------------------------------------------------------------------


def test_write_invalid_python_is_rejected(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "broken.py", "content": "def bad(\n"},
    )
    assert not result.valid
    assert result.code == PreValidationCode.SYNTAX_ERROR.value
    assert "broken.py" in result.message
    assert result.details["language"] == "python"
    assert result.details["line"] is not None


# ---------------------------------------------------------------------------
# 4. Write invalid JSON → SYNTAX_ERROR
# ---------------------------------------------------------------------------


def test_write_invalid_json_is_rejected(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "config.json", "content": '{"key": value}'},
    )
    assert not result.valid
    assert result.code == PreValidationCode.SYNTAX_ERROR.value
    assert result.details["language"] == "json"


def test_write_valid_json_passes(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "config.json", "content": '{"key": "value"}'},
    )
    assert result.valid


# ---------------------------------------------------------------------------
# 5. Write with broken relative import → BROKEN_RELATIVE_IMPORT
# ---------------------------------------------------------------------------


def test_write_with_broken_relative_import_is_rejected(tmp_path: Path) -> None:
    # Create a package directory
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")

    content = textwrap.dedent("""\
        from .nonexistent_module import something

        def hello():
            return something()
    """)
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "mypkg/new_file.py", "content": content},
    )
    assert not result.valid
    assert result.code == PreValidationCode.BROKEN_RELATIVE_IMPORT.value
    assert ".nonexistent_module" in result.message


# ---------------------------------------------------------------------------
# 6. Write with valid relative import → VALID
# ---------------------------------------------------------------------------


def test_write_with_valid_relative_import_passes(tmp_path: Path) -> None:
    # Create a package directory with an existing module
    pkg = tmp_path / "mypkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "existing_module.py").write_text("value = 42\n", encoding="utf-8")

    content = textwrap.dedent("""\
        from .existing_module import value

        def hello():
            return value
    """)
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "mypkg/new_file.py", "content": content},
    )
    assert result.valid


# ---------------------------------------------------------------------------
# 7. Edit file simulated result syntax check
# ---------------------------------------------------------------------------


def test_edit_file_simulated_result_syntax_check(tmp_path: Path) -> None:
    """edit_file where old→new produces invalid Python."""
    target = tmp_path / "module.py"
    target.write_text("def hello():\n    return 1\n", encoding="utf-8")

    result = pre_validate_mutation(
        tmp_path,
        "edit_file",
        {"path": "module.py", "old": "def hello():\n    return 1\n", "new": "def hello(\n"},
    )
    assert not result.valid
    assert result.code == PreValidationCode.SYNTAX_ERROR.value
    assert "module.py" in result.message


def test_edit_file_valid_result_passes(tmp_path: Path) -> None:
    """edit_file where old→new produces valid Python."""
    target = tmp_path / "module.py"
    target.write_text("value = 1\n", encoding="utf-8")

    result = pre_validate_mutation(
        tmp_path,
        "edit_file",
        {"path": "module.py", "old": "value = 1", "new": "value = 2"},
    )
    assert result.valid


# ---------------------------------------------------------------------------
# 8. Non-Python files skip import check → VALID
# ---------------------------------------------------------------------------


def test_non_python_files_skip_import_check(tmp_path: Path) -> None:
    # JavaScript with something that looks like an import
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "app.js", "content": "import {foo} from './bar';\nconsole.log(foo);\n"},
    )
    assert result.valid


# ---------------------------------------------------------------------------
# 9. Verilog basic syntax check
# ---------------------------------------------------------------------------


def test_verilog_mismatched_module_endmodule_is_rejected(tmp_path: Path) -> None:
    content = textwrap.dedent("""\
        module and_gate(input a, input b, output y);
            assign y = a & b;
        // missing endmodule
    """)
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "and_gate.v", "content": content},
    )
    assert not result.valid
    assert result.code == PreValidationCode.SYNTAX_ERROR.value
    assert "module/endmodule mismatch" in result.message


def test_verilog_valid_module_passes(tmp_path: Path) -> None:
    content = textwrap.dedent("""\
        module and_gate(input a, input b, output y);
            assign y = a & b;
        endmodule
    """)
    result = pre_validate_mutation(
        tmp_path,
        "write_file",
        {"path": "and_gate.v", "content": content},
    )
    assert result.valid


# ---------------------------------------------------------------------------
# 10. ToolRegistry integration test
# ---------------------------------------------------------------------------


def test_prevalidation_integrated_in_registry(tmp_path: Path) -> None:
    """Prove that ToolRegistry.call() rejects an invalid write_file
    via pre-validation before the tool handler ever runs."""
    from mind01.modes import AgentMode
    from mind01.tools.registry import ToolRegistry
    from mind01.tools.verify_tools import ToolError

    registry = ToolRegistry(
        tmp_path,
        yes=True,
        allow_write=True,
        mode=AgentMode.WRITE_APPROVED,
    )

    # Attempt to write_file with invalid Python — should be rejected by
    # pre-validation, not by the file handler.
    with pytest.raises(ToolError, match="Pre-validation failed"):
        registry.call("write_file", {"path": "bad.py", "content": "def broken(\n"})


# ---------------------------------------------------------------------------
# Bonus: propose_edit_file also gets pre-validated
# ---------------------------------------------------------------------------


def test_propose_edit_nonexistent_file_is_rejected(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "propose_edit_file",
        {"path": "nonexistent.py", "old": "x", "new": "y"},
    )
    assert not result.valid
    assert result.code == PreValidationCode.TARGET_NOT_FOUND.value


# ---------------------------------------------------------------------------
# Serialization test
# ---------------------------------------------------------------------------


def test_prevalidation_result_serializable() -> None:
    result = PreValidationResult(
        valid=False,
        code=PreValidationCode.SYNTAX_ERROR.value,
        message="test error",
        details={"line": 1},
    )
    payload = result.to_dict()
    assert isinstance(payload, dict)
    assert payload["valid"] is False
    assert payload["code"] == "SYNTAX_ERROR"
    # Verify JSON-serializable
    json.dumps(payload)


# ---------------------------------------------------------------------------
# Non-mutation tools are not pre-validated
# ---------------------------------------------------------------------------


def test_read_file_not_prevalidated(tmp_path: Path) -> None:
    result = pre_validate_mutation(
        tmp_path,
        "read_file",
        {"path": "anything.py"},
    )
    assert result.valid
    assert result.code == PreValidationCode.VALID.value
