from __future__ import annotations

import builtins
import shutil
import tempfile
from pathlib import Path

from mind01.tools import ToolError, ToolRegistry, parse_allowed_command


def run_shell_safety_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-shell-safety-"))
    repo_root = Path(__file__).resolve().parents[1]
    source_sleep_script = repo_root / "tests" / "fixtures" / "sleep.py"
    source_long_output_script = repo_root / "tests" / "fixtures" / "long_output.py"
    sleep_script = tmp / "sleep.py"
    long_output_script = tmp / "long_output.py"
    shutil.copy2(source_sleep_script, sleep_script)
    shutil.copy2(source_long_output_script, long_output_script)
    try:
        shell_tools = ToolRegistry(
            tmp,
            yes=True,
            allow_shell=True,
            mode="write-approved",
        )

        dangerous = [
            "python3 --version; git status",
            "python3 --version && git status",
            "python3 --version | cat",
            "python3 --version > out.txt",
            "python3 $(echo --version)",
            "curl http://example.com",
            "rm -rf /",
            "python3 -c 'print(1)'",
            "node -e 'console.log(1)'",
        ]
        for command in dangerous:
            try:
                parse_allowed_command(command)
                raise AssertionError(f"dangerous shell input was not blocked: {command}")
            except ToolError:
                pass

        read_only_shell = ToolRegistry(
            tmp,
            yes=True,
            allow_shell=True,
            mode="read-only",
        )
        try:
            read_only_shell.call("run_command", {"command": "python3 --version"})
            raise AssertionError("read-only shell execution was not blocked")
        except ToolError as exc:
            assert "read-only" in str(exc)

        assert "exit_code=0" in shell_tools.call(
            "run_command",
            {"command": "python3 --version"},
        ).text

        try:
            shell_tools.call(
                "run_command",
                {"command": f"python3 {sleep_script}", "timeout_seconds": 1},
            )
            raise AssertionError("command timeout was not enforced")
        except ToolError as exc:
            assert "timed out after 1 seconds" in str(exc)

        output = shell_tools.call(
                "run_command",
                {
                    "command": f"python3 {long_output_script}",
                    "output_limit": 10,
                },
        ).text
        assert "TAIL" in output
        assert len(output.split("\n", 1)[1]) <= 10

        write_read_only = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            mode="read-only",
        )
        try:
            write_read_only.call("write_file", {"path": "x.txt", "content": "x"})
            raise AssertionError("read-only write was not blocked")
        except ToolError as exc:
            assert "read-only" in str(exc)

        propose = ToolRegistry(tmp, yes=True, mode="propose")
        assert "Proposed patch" in propose.call(
            "propose_write_file",
            {"path": "x.txt", "content": "x"},
        ).text
        try:
            propose.call("write_file", {"path": "x.txt", "content": "x"})
            raise AssertionError("propose direct write was not blocked")
        except ToolError as exc:
            assert "propose" in str(exc)

        write_no_yes = ToolRegistry(
            tmp,
            yes=False,
            allow_write=True,
            mode="write-approved",
        )
        original_input = builtins.input
        builtins.input = lambda prompt="": (_ for _ in ()).throw(EOFError())
        try:
            try:
                write_no_yes.call("write_file", {"path": "needs-approval.txt", "content": "x"})
                raise AssertionError("write-approved approval gate was not enforced")
            except ToolError as exc:
                assert "approval required" in str(exc).lower()
        finally:
            builtins.input = original_input
    finally:
        shutil.rmtree(tmp)


def test_shell_safety() -> None:
    run_shell_safety_tests()
