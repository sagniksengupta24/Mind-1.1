from __future__ import annotations

import argparse
import builtins
import shutil
import tempfile
from pathlib import Path

from mind01.api import MindAPI
from mind01.cli import require_patch_apply_policy
from mind01.config import AgentConfig
from mind01.modes import AgentMode, parse_agent_mode
from mind01.tools import ToolError, ToolRegistry
from mind01.tools.schemas import SCHEMA_BY_NAME


def run_mode_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-modes-"))
    try:
        (tmp / "src").mkdir()
        (tmp / "src" / "demo.py").write_text("def demo():\n    return 'ok'\n")

        default_config = AgentConfig.build(
            workspace=str(tmp),
            model="qwen2.5-coder:7b",
            ollama_url="http://127.0.0.1:11434",
            max_steps=1,
            yes=True,
            dry_run=True,
        )
        assert default_config.mode == AgentMode.READ_ONLY
        assert AgentConfig(workspace=tmp).mode == AgentMode.READ_ONLY
        assert MindAPI(tmp, "qwen2.5-coder:7b", "http://127.0.0.1:11434").mode == AgentMode.READ_ONLY
        assert parse_agent_mode("read-only") == AgentMode.READ_ONLY
        assert parse_agent_mode("propose") == AgentMode.PROPOSE
        assert parse_agent_mode("write-approved") == AgentMode.WRITE_APPROVED
        assert parse_agent_mode("unsafe") == AgentMode.UNSAFE
        try:
            parse_agent_mode("write")
            raise AssertionError("invalid mode was not rejected")
        except ValueError as exc:
            assert "Invalid mode" in str(exc)

        read_only = ToolRegistry(tmp, yes=True)
        assert read_only.mode == AgentMode.READ_ONLY
        assert "src/demo.py" in read_only.call("list_files", {"path": "."}).text
        assert "def demo" in read_only.call("read_file", {"path": "src/demo.py"}).text
        assert "src/demo.py:2" in read_only.call("search_code", {"query": "return"}).text
        assert "total_files" in read_only.call("project_map", {"path": "."}).text

        for tool_name, args in (
            ("write_file", {"path": "src/x.py", "content": "x = 1\n"}),
            ("edit_file", {"path": "src/demo.py", "old": "ok", "new": "fine"}),
            ("run_command", {"command": "python3 --version"}),
            ("remember", {"key": "k", "value": "v"}),
            ("index_code", {"path": "."}),
        ):
            try:
                read_only.call(tool_name, args)
                raise AssertionError(f"{tool_name} was not blocked in read-only")
            except ToolError as exc:
                assert "read-only" in str(exc) or "not allowed" in str(exc)

        propose = ToolRegistry(tmp, yes=True, mode="propose")
        proposal = propose.call(
            "propose_write_file",
            {"path": "src/proposed.py", "content": "x = 1\n"},
        ).text
        assert "Proposed patch" in proposal
        assert not (tmp / "src" / "proposed.py").exists()
        assert "Indexed" in propose.call("index_code", {"path": "."}).text
        try:
            propose.call("write_file", {"path": "src/direct.py", "content": "x = 1\n"})
            raise AssertionError("direct write was not blocked in propose mode")
        except ToolError as exc:
            assert "propose" in str(exc)
        try:
            propose.call("run_command", {"command": "python3 --version"})
            raise AssertionError("shell command was not blocked in propose mode")
        except ToolError as exc:
            assert "propose" in str(exc)
        try:
            require_patch_apply_policy(argparse.Namespace(mode="propose", yes=True))
            raise AssertionError("patch apply was not blocked in propose mode")
        except ToolError as exc:
            assert "patch apply is not allowed" in str(exc)

        write_no_yes = ToolRegistry(tmp, yes=False, allow_write=True, mode="write-approved")
        original_input = builtins.input
        builtins.input = lambda prompt="": (_ for _ in ()).throw(EOFError())
        try:
            try:
                write_no_yes.call("write_file", {"path": "src/needs_yes.py", "content": "x = 1\n"})
                raise AssertionError("write without approval/yes was not blocked")
            except ToolError as exc:
                assert "approval required" in str(exc).lower()
        finally:
            builtins.input = original_input

        write_mode = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            allow_shell=True,
            mode="write-approved",
        )
        assert "Wrote src/allowed.py" in write_mode.call(
            "write_file",
            {"path": "src/allowed.py", "content": "x = 1\n"},
        ).text
        assert "exit_code=0" in write_mode.call(
            "run_command",
            {"command": "python3 --version"},
        ).text

        shell_without_flag = ToolRegistry(tmp, yes=True, mode="write-approved")
        try:
            shell_without_flag.call("run_command", {"command": "python3 --version"})
            raise AssertionError("shell without allow_shell was not blocked")
        except ToolError as exc:
            assert "--allow-shell" in str(exc)

        assert AgentConfig(workspace=tmp).mode != AgentMode.UNSAFE
        assert SCHEMA_BY_NAME["write_file"].allowed_modes == ("write-approved", "unsafe")
        assert SCHEMA_BY_NAME["propose_write_file"].allowed_modes == (
            "propose",
            "write-approved",
            "unsafe",
        )
        assert SCHEMA_BY_NAME["run_command"].can_run_shell
    finally:
        shutil.rmtree(tmp)


def test_mode_regressions() -> None:
    run_mode_tests()
