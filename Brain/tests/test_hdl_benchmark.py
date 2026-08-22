"""Tests for Mind1.1 Internal HDL Benchmark Suite."""

from pathlib import Path
import pytest
from mind01.eval_suites.hdl_benchmark import (
    BENCHMARK_PROBLEMS,
    HDLBenchmarkHarness,
    extract_verilog_code,
    validate_verilog_code_structure,
)


def test_hdl_benchmark_problem_count():
    assert len(BENCHMARK_PROBLEMS) == 16
    categories = {p.category for p in BENCHMARK_PROBLEMS}
    assert "combinational" in categories
    assert "sequential" in categories
    assert "fsm" in categories


def test_hdl_benchmark_structure_validation():
    p = BENCHMARK_PROBLEMS[0]
    assert validate_verilog_code_structure(p.reference_verilog, p) is True
    assert validate_verilog_code_structure("module wrong_name (); endmodule", p) is False
    assert validate_verilog_code_structure("", p) is False


def test_hdl_benchmark_verilog_extraction():
    fenced = "Here is your Verilog:\n```verilog\nmodule foo ();\nendmodule\n```\nEnjoy!"
    assert extract_verilog_code(fenced) == "module foo ();\nendmodule"

    plain = "module foo ();\nendmodule"
    assert extract_verilog_code(plain) == "module foo ();\nendmodule"


def test_hdl_benchmark_requires_real_simulation_tools(tmp_path: Path):
    harness = HDLBenchmarkHarness(tmp_path, model_name="TestNoSim", require_simulation=True)
    # Simulate simulator tool missing
    harness.iverilog_path = None
    harness.vvp_path = None

    p = BENCHMARK_PROBLEMS[0]
    with pytest.raises(RuntimeError, match="iverilog and vvp are required"):
        harness.evaluate_problem(p)

    # In non-strict mode, missing simulator MUST report sim_passed=False and status='failed'
    harness_non_strict = HDLBenchmarkHarness(tmp_path, model_name="TestNoSim", require_simulation=False)
    harness_non_strict.iverilog_path = None
    harness_non_strict.vvp_path = None
    res = harness_non_strict.evaluate_problem(p)
    assert res["sim_passed"] is False
    assert res["status"] == "failed"
    assert res["failure_reason"] == "simulator_missing"


def test_hdl_benchmark_fails_broken_code_simulation(tmp_path: Path):
    harness = HDLBenchmarkHarness(tmp_path, model_name="TestBrokenCode", require_simulation=True)
    p = BENCHMARK_PROBLEMS[0]

    # 1. Syntax / Compile error
    broken_syntax = "module mux4 (syntax error here; endmodule"
    res_compile_err = harness.evaluate_problem(p, code_generator=lambda _: broken_syntax)
    assert res_compile_err["sim_passed"] is False
    assert res_compile_err["status"] == "failed"
    assert res_compile_err["failure_reason"] == "compile_error"
    assert res_compile_err["exit_code"] != 0

    # 2. Logic error
    broken_logic = """\
module mux4 (
    input wire [3:0] in,
    input wire [1:0] sel,
    output reg out
);
    always @(*) begin
        out = 1'b0; // Always wrong for nonzero inputs
    end
endmodule
"""
    res_logic_err = harness.evaluate_problem(p, code_generator=lambda _: broken_logic)
    assert res_logic_err["sim_passed"] is False
    assert res_logic_err["status"] == "failed"
    assert res_logic_err["failure_reason"] == "logic_error"
    assert res_logic_err["exit_code"] != 0


def test_hdl_benchmark_real_simulation_execution(tmp_path: Path):
    harness = HDLBenchmarkHarness(tmp_path, model_name="TestModelRealSim", require_simulation=True)
    assert harness.iverilog_path is not None, "iverilog must be installed for this test"
    assert harness.vvp_path is not None, "vvp must be installed for this test"

    # Run first 3 problems with reference code through real iverilog & vvp
    report = harness.run_suite(BENCHMARK_PROBLEMS[:3], is_dry_run=True)
    assert report["total_problems"] == 3
    assert report["passed_problems"] == 3
    assert report["pass_rate_pct"] == 100.0
    assert report["is_dry_run"] is True
    for res in report["results"]:
        assert res["status"] == "verified"
        assert res["sim_passed"] is True
        assert res["exit_code"] == 0
        assert "PASS" in res["simulation_output"]
        assert len(res["compiler_command"]) > 0
        assert len(res["simulation_command"]) > 0

