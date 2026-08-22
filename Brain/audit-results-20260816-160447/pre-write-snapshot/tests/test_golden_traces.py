"""Golden-trace regression safety net (Workstream 7).

Records real tool sequences captured from verified eval-suite runs, replays
them through the current ToolRegistry + VerificationEngine in a fresh temp
workspace, and asserts the verification outcome has not diverged from the
recorded golden result.

Replay is fully deterministic: it never calls a model.  It exercises the same
registry, receipts, and verifier code paths the agent uses at runtime, so a
change that breaks a known-good trace (e.g. a verifier that now rejects a
correct file, or a registry that hides a required tool) is caught here.
"""

from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

import pytest

from mind01.config import AgentConfig
from mind01.modes import AgentMode
from mind01.task_contract import build_task_contract
from mind01.tools.registry import ToolRegistry
from mind01.tools.verify_tools import ToolError
from mind01.verification import VerificationEngine

# ---------------------------------------------------------------------------
# Golden traces captured from verified runs (prompt + tool sequence + outcome).
# expected_checks: check-name -> golden status.  Divergence rules:
#   - golden "passed"  => replay must be "passed"
#   - golden "unavailable" => replay must not be "failed" (tool may appear later)
#   - golden "failed"  => replay must be "failed" (known-failing golden)
# ---------------------------------------------------------------------------

AND_GATE_SOURCE = """`timescale 1ns / 1ps

module and_gate_1 (
    input wire a,
    input wire b,
    output wire y
);

assign y = a & b;

endmodule
"""

DUMMY_SOURCE = """# This is dummy_a_1.py
print('Hello from dummy_a_1')
"""

JSON_SOURCE = """{
  "name": "mind01",
  "version": "0.11.1",
  "enabled": true
}
"""

CPP_SOURCE = """#include <cstdint>

uint32_t add_one(uint32_t value) {
    return value + 1;
}
"""


GOLDEN_TRACES = [
    {
        "id": "gt-verilog-new-file",
        "prompt": (
            "Create a simple Verilog module named 'and_gate_1' in "
            "hardware/and_gate_1.v that implements a basic AND gate."
        ),
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "tool_sequence": [
            {
                "tool": "write_file",
                "args": {"path": "hardware/and_gate_1.v", "content": AND_GATE_SOURCE},
            }
        ],
        "verify_paths": ["hardware/and_gate_1.v"],
        "expected_files": ["hardware/and_gate_1.v"],
        "expected_checks": {
            "iverilog-syntax": "passed",  # downgraded to unavailable when iverilog absent
            "file-type-verifier": "unavailable",
        },
        "expected_completion": "verified",
    },
    {
        "id": "gt-python-new-file",
        "prompt": "Create two new python files in eval_suites/: dummy_a_1.py and dummy_b_1.py.",
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "tool_sequence": [
            {"tool": "write_file", "args": {"path": "eval_suites/dummy_a_1.py", "content": DUMMY_SOURCE}},
            {"tool": "write_file", "args": {"path": "eval_suites/dummy_b_1.py", "content": DUMMY_SOURCE}},
        ],
        "verify_paths": ["eval_suites/dummy_a_1.py", "eval_suites/dummy_b_1.py"],
        "expected_files": ["eval_suites/dummy_a_1.py", "eval_suites/dummy_b_1.py"],
        "expected_checks": {
            "python-executable-structure": "passed",
            "python-compile": "passed",
            "python-import": "unavailable",
        },
        "expected_completion": "verified",
    },
    {
        "id": "gt-json-new-file",
        "prompt": "Create a JSON config file at config/agent.json with name, version, and enabled fields.",
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "tool_sequence": [
            {"tool": "write_file", "args": {"path": "config/agent.json", "content": JSON_SOURCE}}
        ],
        "verify_paths": ["config/agent.json"],
        "expected_files": ["config/agent.json"],
        "expected_checks": {
            "json-parse": "passed",
        },
        "expected_completion": "verified",
    },
    {
        "id": "gt-cpp-new-file",
        "prompt": "Create a C++ source file src/math_ops.cpp defining a function add_one.",
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "tool_sequence": [
            {"tool": "write_file", "args": {"path": "src/math_ops.cpp", "content": CPP_SOURCE}}
        ],
        "verify_paths": ["src/math_ops.cpp"],
        "expected_files": ["src/math_ops.cpp"],
        "expected_checks": {
            "cpp-syntax": "passed",
        },
        "expected_completion": "verified",
    },
    {
        "id": "gt-edit-existing-file",
        "prompt": "Add a comment '# EVAL_TEST_COMMENT_1' at the top of tests/conftest.py.",
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "fixtures": {"tests/conftest.py": "# existing conftest\n"},
        "tool_sequence": [
            {
                "tool": "edit_file",
                "args": {
                    "path": "tests/conftest.py",
                    "old": "# existing conftest\n",
                    "new": "# EVAL_TEST_COMMENT_1\n# existing conftest\n",
                },
            }
        ],
        "verify_paths": ["tests/conftest.py"],
        "expected_files": ["tests/conftest.py"],
        "expected_checks": {
            "python-executable-structure": "passed",
            "python-compile": "passed",
            "python-import": "unavailable",
        },
        "expected_completion": "verified",
    },
]


@pytest.mark.parametrize("golden", GOLDEN_TRACES, ids=lambda item: item["id"])
def test_golden_trace_replay_matches_recorded_verification(tmp_path: Path, golden: dict) -> None:
    replay = GoldenTraceReplay(tmp_path, golden)
    outcome = replay.run()
    assert outcome.files_created == golden["expected_files"], (
        f"trace {golden['id']}: expected files {golden['expected_files']}, got {outcome.files_created}"
    )
    divergences = replay.divergences()
    assert not divergences, (
        f"trace {golden['id']}: verifier divergence\n" + "\n".join(divergences)
    )
    assert not outcome.blocking_failures, (
        f"trace {golden['id']}: blocking verification failure(s): {outcome.blocking_failures}"
    )


def test_golden_trace_catalog_is_recorded_and_immutable() -> None:
    """The golden catalog must stay explicit: no empty traces, no missing checks."""
    assert len(GOLDEN_TRACES) >= 5
    ids = [trace["id"] for trace in GOLDEN_TRACES]
    assert len(ids) == len(set(ids)), "golden trace ids must be unique"
    for trace in GOLDEN_TRACES:
        assert trace["tool_sequence"], f"{trace['id']} has no tools"
        assert trace["verify_paths"], f"{trace['id']} has no verify paths"
        assert trace["expected_checks"], f"{trace['id']} has no expected checks"


def test_golden_trace_rejects_out_of_scope_write(tmp_path: Path) -> None:
    """Path traversal / out-of-workspace writes must stay blocked (WS1 invariant)."""
    golden = {
        "id": "gt-out-of-scope",
        "prompt": "Write a file named 'pwned.txt' to /tmp/pwned.txt.",
        "allow_write": True,
        "allow_shell": True,
        "mode": "write-approved",
        "tool_sequence": [
            {"tool": "write_file", "args": {"path": "/tmp/pwned.txt", "content": "pwned"}}
        ],
        "verify_paths": [],
        "expected_files": [],
        "expected_checks": {},
        "expected_completion": "failed",
    }
    replay = GoldenTraceReplay(tmp_path, golden)
    outcome = replay.run()
    assert not outcome.files_created
    assert not (tmp_path / "pwned.txt").exists()
    assert not (Path("/tmp") / "pwned.txt").exists()
    assert outcome.blocking_failures or outcome.tool_errors, (
        "out-of-scope write must be blocked (ToolError or blocking failure)"
    )


class GoldenTraceOutcome:
    def __init__(self) -> None:
        self.files_created: list[str] = []
        self.tool_errors: list[str] = []
        self.blocking_failures: list[dict] = []
        self.checks: dict[str, str] = {}


class GoldenTraceReplay:
    """Deterministically replay a golden tool sequence and re-verify."""

    def __init__(self, workspace: Path, golden: dict) -> None:
        self.workspace = workspace
        self.golden = golden
        self._outcome = GoldenTraceOutcome()

    def run(self) -> GoldenTraceOutcome:
        for relative, content in self.golden.get("fixtures", {}).items():
            target = self.workspace / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")

        registry = ToolRegistry(
            self.workspace,
            yes=True,
            allow_write=bool(self.golden["allow_write"]),
            allow_shell=bool(self.golden["allow_shell"]),
            mode=AgentMode(self.golden["mode"]),
        )
        for step in self.golden["tool_sequence"]:
            try:
                registry.call(step["tool"], dict(step["args"]))
                self._outcome.files_created.append(step["args"]["path"])
            except ToolError as exc:
                self._outcome.tool_errors.append(str(exc))

        verify_paths = self.golden["verify_paths"]
        if verify_paths:
            contract = build_task_contract(
                self.golden["prompt"],
                mutation_required=True,
                specialist="code_modification",
            )
            results = VerificationEngine(self.workspace).verify_paths(
                verify_paths,
                full_project=False,
                contract=contract,
            )
            for result in results:
                self._outcome.checks[result.check] = result.status
                if result.blocking and result.status == "failed":
                    self._outcome.blocking_failures.append(
                        {"check": result.check, "summary": result.output_summary}
                    )
        return self._outcome

    def divergences(self) -> list[str]:
        golden_checks = self.golden["expected_checks"]
        actual = self._outcome.checks
        divergences: list[str] = []
        for check, golden_status in golden_checks.items():
            actual_status = actual.get(check)
            if golden_status == "passed" and actual_status != "passed":
                divergences.append(
                    f"check `{check}` golden=passed but replay={actual_status}"
                )
            elif golden_status == "unavailable" and actual_status == "failed":
                divergences.append(
                    f"check `{check}` golden=unavailable but replay=failed"
                )
            elif golden_status == "failed" and actual_status != "failed":
                divergences.append(
                    f"check `{check}` golden=failed but replay={actual_status}"
                )
            elif actual_status is None and golden_status in {"passed", "failed"}:
                divergences.append(
                    f"check `{check}` expected in replay but verifier did not emit it"
                )
        # iverilog may not be installed: "passed" legally degrades to "unavailable"
        # (tool_unavailable, non-blocking), and "unavailable" must stay unavailable.
        if "iverilog-syntax" in golden_checks and shutil.which("iverilog") is None:
            divergences = [
                item
                for item in divergences
                if "iverilog-syntax" not in item
                or "replay=unavailable" not in item
                or "golden=failed" in item
            ]
        return divergences
