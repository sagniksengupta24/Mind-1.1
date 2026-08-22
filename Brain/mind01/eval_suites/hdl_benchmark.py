"""Internal HDL / RTL Benchmark Suite for Mind1.1.

Evaluates LLMs and coding agents on Verilog / SystemVerilog RTL design and verification.
Features 16 VerilogEval-style benchmark problems (combinational logic, sequential circuits, FSMs)
with automated compilation, simulation against self-checking testbenches, and deterministic
evidence receipts via CompletionAuthority.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import re
import shutil
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from ..completion import CompletionAuthority, VerificationEvidence
from ..llm import OllamaClient
from ..sandbox import SandboxConfig, SandboxedExecutor


@dataclass
class HDLProblem:
    id: str
    name: str
    category: str
    prompt: str
    module_name: str
    reference_verilog: str
    testbench_verilog: str


def extract_verilog_code(raw_text: str) -> str:
    """Extract Verilog code block from markdown fences or return plain code."""
    if not raw_text:
        return ""
    fence_patterns = [
        r"```(?:verilog|systemverilog|v)\s*\n(.*?)```",
        r"```\s*\n(.*?)```",
    ]
    for pat in fence_patterns:
        match = re.search(pat, raw_text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return raw_text.strip()


def validate_verilog_code_structure(code: str, problem: HDLProblem) -> bool:
    """Validate that code defines the correct module name and port signature."""
    if not code:
        return False
    module_pat = re.compile(rf"\bmodule\s+{re.escape(problem.module_name)}\b", re.IGNORECASE)
    endmodule_pat = re.compile(r"\bendmodule\b", re.IGNORECASE)
    return bool(module_pat.search(code) and endmodule_pat.search(code))


class LLMVerilogGenerator:
    """Generates Verilog implementations for HDL problems using a real LLM endpoint."""

    def __init__(
        self,
        model: str = "qwen2.5-coder:7b",
        base_url: str = "http://127.0.0.1:11434",
        temperature: float = 0.0,
        timeout: int = 60,
    ) -> None:
        self.model = model
        self.base_url = base_url
        self.temperature = temperature
        self.timeout = timeout
        self.client = OllamaClient(
            base_url=self.base_url,
            model=self.model,
            timeout=self.timeout,
            temperature=self.temperature,
        )

    def generate(self, problem: HDLProblem) -> tuple[str, str]:
        """Generate Verilog code for a problem. Returns (raw_response, extracted_verilog)."""
        prompt = (
            f"You are an expert Verilog digital design engineer.\n"
            f"Write the complete, synthesizable Verilog implementation for the following module:\n\n"
            f"Problem: {problem.name} ({problem.category})\n"
            f"Specification: {problem.prompt}\n"
            f"Module Name MUST be exactly: {problem.module_name}\n\n"
            f"Requirements:\n"
            f"- Use standard Verilog-2001 or SystemVerilog constructs.\n"
            f"- Output the complete module definition starting with `module {problem.module_name}` and ending with `endmodule`.\n"
            f"- Provide ONLY the Verilog code enclosed in a ```verilog``` code block, with no explanations or conversational text."
        )
        messages = [
            {"role": "system", "content": "You are a Verilog RTL synthesis and digital design expert. Output only clean, working Verilog code."},
            {"role": "user", "content": prompt},
        ]
        raw_response = self.client.chat(messages, json_mode=False)
        extracted_code = extract_verilog_code(raw_response)
        return raw_response, extracted_code


class HDLBenchmarkHarness:
    """Harness that compiles, simulates, and verifies RTL problems."""

    def __init__(
        self,
        workspace: Path,
        model_name: str = "qwen2.5-coder:7b",
        require_simulation: bool = True,
    ) -> None:
        self.workspace = workspace.resolve()
        self.model_name = model_name
        self.require_simulation = require_simulation
        self.iverilog_path = shutil.which("iverilog")
        self.vvp_path = shutil.which("vvp")
        self.sandbox = SandboxedExecutor(self.workspace, SandboxConfig(workspace=self.workspace))

    def evaluate_problem(
        self,
        problem: HDLProblem,
        code_generator: Optional[Callable[[HDLProblem], str | tuple[str, str]]] = None,
    ) -> Dict[str, Any]:
        """Run benchmark evaluation for a single HDL problem."""
        start_time = time.monotonic()
        timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
        raw_response = ""
        generated_code = ""

        if code_generator:
            gen_result = code_generator(problem)
            if isinstance(gen_result, tuple):
                raw_response, generated_code = gen_result
            else:
                generated_code = gen_result
                raw_response = gen_result
        else:
            generated_code = problem.reference_verilog
            raw_response = problem.reference_verilog

        prob_dir = self.workspace / ".mind01" / "benchmarks" / problem.id
        prob_dir.mkdir(parents=True, exist_ok=True)

        dut_file = prob_dir / f"{problem.module_name}.v"
        tb_file = prob_dir / f"tb_{problem.module_name}.v"
        sim_out = prob_dir / f"{problem.module_name}.vvp"

        dut_file.write_text(generated_code, encoding="utf-8")
        tb_file.write_text(problem.testbench_verilog, encoding="utf-8")

        structure_valid = validate_verilog_code_structure(generated_code, problem)
        sim_passed = False
        compiler_output = ""
        sim_output = ""
        exit_code = -1
        compile_cmd: list[str] = []
        sim_cmd: list[str] = []
        failure_reason: Optional[str] = None

        if self.iverilog_path and self.vvp_path:
            compile_cmd = [self.iverilog_path, "-g2012", "-o", str(sim_out), str(dut_file), str(tb_file)]
            compile_res = self.sandbox.execute(
                compile_cmd,
                cwd=prob_dir,
                timeout_seconds=20,
            )
            compiler_output = compile_res.output.strip()
            exit_code = compile_res.returncode

            if compile_res.returncode != 0:
                failure_reason = "compile_error"
            elif not sim_out.exists():
                failure_reason = "compile_output_missing"
            else:
                sim_cmd = [self.vvp_path, str(sim_out)]
                sim_res = self.sandbox.execute(
                    sim_cmd,
                    cwd=prob_dir,
                    timeout_seconds=20,
                )
                sim_output = sim_res.output.strip()
                exit_code = sim_res.returncode
                if sim_res.returncode == 0 and "PASS" in sim_output:
                    sim_passed = True
                    failure_reason = None
                elif "FAIL" in sim_output:
                    failure_reason = "logic_error"
                else:
                    failure_reason = "simulation_error"
        else:
            if self.require_simulation:
                raise RuntimeError(
                    "iverilog and vvp are required for HDL benchmark execution. "
                    "Cannot verify simulation results without simulator tools."
                )
            compiler_output = "iverilog not found on host; simulation skipped (structural check only)"
            sim_passed = False
            exit_code = 1
            failure_reason = "simulator_missing"
            sim_output = f"Structural verification: {'PASSED' if structure_valid else 'FAILED'} (Simulation not run)"

        duration = time.monotonic() - start_time
        evidence_status = "passed" if sim_passed else "failed"

        evidence_id = f"ev_hdl_{problem.id}"
        full_command = compile_cmd + (["&&"] + sim_cmd if sim_cmd else [])
        evidence = VerificationEvidence(
            name=f"hdl-sim:{problem.id}",
            command=full_command if full_command else ["none"],
            status=evidence_status,
            exit_code=exit_code,
            duration_seconds=round(duration, 3),
            output_summary=f"Compiler:\n{compiler_output}\n\nSimulation:\n{sim_output}"[:2000],
            level="acceptance",
            selected_reason="hdl_benchmark",
            evidence_id=evidence_id,
            evidence_type="test-execution",
            proven_properties=(f"verilog_module:{problem.module_name}",),
        )

        authority = CompletionAuthority()
        decision = authority.decide(
            "verified" if sim_passed else "failed",
            task_contract=None,
            verification=[evidence],
            evidence_refs=[evidence_id],
        )

        return {
            "problem_id": problem.id,
            "problem_name": problem.name,
            "category": problem.category,
            "status": decision.status,
            "exit_code": exit_code,
            "sim_passed": sim_passed,
            "structure_valid": structure_valid,
            "failure_reason": failure_reason,
            "duration_seconds": round(duration, 3),
            "timestamp": timestamp,
            "raw_model_response": raw_response,
            "generated_verilog": generated_code,
            "compiler_command": compile_cmd,
            "compiler_output": compiler_output,
            "simulation_command": sim_cmd,
            "simulation_output": sim_output,
        }

    def run_suite(
        self,
        problems: Optional[List[HDLProblem]] = None,
        code_generator: Optional[Callable[[HDLProblem], str | tuple[str, str]]] = None,
        is_dry_run: bool = False,
    ) -> Dict[str, Any]:
        """Run all problems and aggregate pass rates and evidence."""
        suite = problems or BENCHMARK_PROBLEMS
        results = []
        passed_count = 0
        failure_breakdown: Dict[str, int] = {}

        for prob in suite:
            res = self.evaluate_problem(prob, code_generator)
            results.append(res)
            if res["status"] == "verified":
                passed_count += 1
            else:
                reason = res.get("failure_reason") or "unknown_failure"
                failure_breakdown[reason] = failure_breakdown.get(reason, 0) + 1

        total = len(suite)
        pass_rate = (passed_count / total * 100.0) if total else 0.0
        sim_desc = "iverilog + vvp" if (self.iverilog_path and self.vvp_path) else "none"

        report = {
            "benchmark_suite": "Mind1.1 HDL Benchmark Suite (VerilogEval-compatible)",
            "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "model_name": self.model_name,
            "is_dry_run": is_dry_run,
            "total_problems": total,
            "passed_problems": passed_count,
            "failed_problems": total - passed_count,
            "pass_rate_pct": round(pass_rate, 2),
            "simulator_used": sim_desc,
            "failure_breakdown": failure_breakdown,
            "results": results,
        }
        return report





BENCHMARK_PROBLEMS: List[HDLProblem] = [
    # 1. 4-to-1 MUX
    HDLProblem(
        id="comb_mux4",
        name="4-to-1 Multiplexer",
        category="combinational",
        prompt="Design a 4-to-1 multiplexer in Verilog. Inputs: [3:0] in, [1:0] sel. Output: out.",
        module_name="mux4",
        reference_verilog="""\
module mux4 (
    input wire [3:0] in,
    input wire [1:0] sel,
    output reg out
);
    always @(*) begin
        case (sel)
            2'b00: out = in[0];
            2'b01: out = in[1];
            2'b10: out = in[2];
            2'b11: out = in[3];
            default: out = 1'b0;
        endcase
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_mux4;
    reg [3:0] in;
    reg [1:0] sel;
    wire out;
    integer i, s;

    mux4 uut (.in(in), .sel(sel), .out(out));

    initial begin
        for (i = 0; i < 16; i = i + 1) begin
            in = i[3:0];
            for (s = 0; s < 4; s = s + 1) begin
                sel = s[1:0];
                #5;
                if (out !== in[sel]) begin
                    $display("FAIL: in=%b sel=%b out=%b expected=%b", in, sel, out, in[sel]);
                    $fatal(1);
                end
            end
        end
        $display("PASS: mux4 testbench completed successfully.");
        $finish;
    end
endmodule
""",
    ),

    # 2. 3-to-8 Decoder
    HDLProblem(
        id="comb_decoder38",
        name="3-to-8 Decoder with Enable",
        category="combinational",
        prompt="Design a 3-to-8 binary decoder with an active-high enable input in Verilog. Inputs: [2:0] in, enable. Output: [7:0] out.",
        module_name="decoder38",
        reference_verilog="""\
module decoder38 (
    input wire [2:0] in,
    input wire enable,
    output reg [7:0] out
);
    always @(*) begin
        if (!enable) begin
            out = 8'b00000000;
        end else begin
            out = 8'b00000001 << in;
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_decoder38;
    reg [2:0] in;
    reg enable;
    wire [7:0] out;
    integer i;

    decoder38 uut (.in(in), .enable(enable), .out(out));

    initial begin
        enable = 0;
        for (i = 0; i < 8; i = i + 1) begin
            in = i[2:0];
            #5;
            if (out !== 8'h00) begin
                $display("FAIL: Disabled decoder out=%h expected=00", out);
                $fatal(1);
            end
        end
        enable = 1;
        for (i = 0; i < 8; i = i + 1) begin
            in = i[2:0];
            #5;
            if (out !== (8'h01 << in)) begin
                $display("FAIL: Enabled in=%d out=%b expected=%b", in, out, (8'h01 << in));
                $fatal(1);
            end
        end
        $display("PASS: decoder38 testbench completed successfully.");
        $finish;
    end
endmodule
""",
    ),

    # 3. 4-bit Priority Encoder
    HDLProblem(
        id="comb_priority_enc",
        name="4-bit Priority Encoder",
        category="combinational",
        prompt="Design a 4-bit priority encoder in Verilog where in[3] has highest priority. Inputs: [3:0] in. Outputs: [1:0] out, valid.",
        module_name="priority_enc4",
        reference_verilog="""\
module priority_enc4 (
    input wire [3:0] in,
    output reg [1:0] out,
    output reg valid
);
    always @(*) begin
        valid = 1'b1;
        if (in[3]) out = 2'b11;
        else if (in[2]) out = 2'b10;
        else if (in[1]) out = 2'b01;
        else if (in[0]) out = 2'b00;
        else begin
            out = 2'b00;
            valid = 1'b0;
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_priority_enc4;
    reg [3:0] in;
    wire [1:0] out;
    wire valid;

    priority_enc4 uut (.in(in), .out(out), .valid(valid));

    initial begin
        in = 4'b0000; #5;
        if (valid !== 0) $fatal(1, "FAIL valid for 0000");

        in = 4'b0001; #5;
        if (valid !== 1 || out !== 2'b00) $fatal(1, "FAIL 0001");

        in = 4'b0110; #5;
        if (valid !== 1 || out !== 2'b10) $fatal(1, "FAIL 0110");

        in = 4'b1011; #5;
        if (valid !== 1 || out !== 2'b11) $fatal(1, "FAIL 1011");

        $display("PASS: priority_enc4 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 4. 8-bit ALU
    HDLProblem(
        id="comb_alu8",
        name="8-bit Arithmetic Logic Unit",
        category="combinational",
        prompt="Design an 8-bit ALU in Verilog with ops 0:ADD, 1:SUB, 2:AND, 3:OR, 4:XOR, 5:NOT, 6:SHL, 7:SHR. Inputs: [7:0] a, b, [2:0] opcode. Outputs: [7:0] result, zero, carry.",
        module_name="alu8",
        reference_verilog="""\
module alu8 (
    input wire [7:0] a,
    input wire [7:0] b,
    input wire [2:0] opcode,
    output reg [7:0] result,
    output wire zero,
    output reg carry
);
    reg [8:0] sum;

    always @(*) begin
        carry = 1'b0;
        case (opcode)
            3'b000: begin
                sum = a + b;
                result = sum[7:0];
                carry = sum[8];
            end
            3'b001: begin
                sum = a - b;
                result = sum[7:0];
                carry = (a < b);
            end
            3'b010: result = a & b;
            3'b011: result = a | b;
            3'b100: result = a ^ b;
            3'b101: result = ~a;
            3'b110: result = a << 1;
            3'b111: result = a >> 1;
            default: result = 8'h00;
        endcase
    end

    assign zero = (result == 8'h00);
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_alu8;
    reg [7:0] a, b;
    reg [2:0] opcode;
    wire [7:0] result;
    wire zero, carry;

    alu8 uut (.a(a), .b(b), .opcode(opcode), .result(result), .zero(zero), .carry(carry));

    initial begin
        a = 8'd250; b = 8'd10; opcode = 3'b000; #5;
        if (result !== 8'd4 || carry !== 1 || zero !== 0) $fatal(1, "FAIL ADD carry");

        a = 8'd50; b = 8'd50; opcode = 3'b001; #5;
        if (result !== 8'd0 || zero !== 1) $fatal(1, "FAIL SUB zero");

        a = 8'hFF; b = 8'h0F; opcode = 3'b010; #5;
        if (result !== 8'h0F) $fatal(1, "FAIL AND");

        $display("PASS: alu8 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 5. 4-bit Carry Lookahead Adder
    HDLProblem(
        id="comb_cla4",
        name="4-bit Carry-Lookahead Adder",
        category="combinational",
        prompt="Design a 4-bit Carry-Lookahead Adder in Verilog with generate and propagate logic. Inputs: [3:0] a, b, cin. Outputs: [3:0] sum, cout.",
        module_name="cla4",
        reference_verilog="""\
module cla4 (
    input wire [3:0] a,
    input wire [3:0] b,
    input wire cin,
    output wire [3:0] sum,
    output wire cout
);
    wire [3:0] g, p, c;

    assign g = a & b;
    assign p = a ^ b;

    assign c[0] = cin;
    assign c[1] = g[0] | (p[0] & cin);
    assign c[2] = g[1] | (p[1] & g[0]) | (p[1] & p[0] & cin);
    assign c[3] = g[2] | (p[2] & g[1]) | (p[2] & p[1] & g[0]) | (p[2] & p[1] & p[0] & cin);
    assign cout = g[3] | (p[3] & g[2]) | (p[3] & p[2] & g[1]) | (p[3] & p[2] & p[1] & g[0]) | (p[3] & p[2] & p[1] & p[0] & cin);

    assign sum = p ^ c;
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_cla4;
    reg [3:0] a, b;
    reg cin;
    wire [3:0] sum;
    wire cout;

    cla4 uut (.a(a), .b(b), .cin(cin), .sum(sum), .cout(cout));

    initial begin
        a = 4'd5; b = 4'd3; cin = 0; #5;
        if (sum !== 4'd8 || cout !== 0) $fatal(1, "FAIL 5+3");

        a = 4'd15; b = 4'd1; cin = 0; #5;
        if (sum !== 4'd0 || cout !== 1) $fatal(1, "FAIL 15+1");

        $display("PASS: cla4 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 6. 8-bit Parity Generator
    HDLProblem(
        id="comb_parity8",
        name="8-bit Even & Odd Parity Generator",
        category="combinational",
        prompt="Design an 8-bit parity generator in Verilog. Inputs: [7:0] data. Outputs: even_parity, odd_parity.",
        module_name="parity8",
        reference_verilog="""\
module parity8 (
    input wire [7:0] data,
    output wire even_parity,
    output wire odd_parity
);
    assign even_parity = ^data;
    assign odd_parity = ~even_parity;
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_parity8;
    reg [7:0] data;
    wire even_parity, odd_parity;

    parity8 uut (.data(data), .even_parity(even_parity), .odd_parity(odd_parity));

    initial begin
        data = 8'b00000000; #5;
        if (even_parity !== 0 || odd_parity !== 1) $fatal(1, "FAIL 0");

        data = 8'b10000001; #5;
        if (even_parity !== 0 || odd_parity !== 1) $fatal(1, "FAIL 2 ones");

        data = 8'b10100001; #5;
        if (even_parity !== 1 || odd_parity !== 0) $fatal(1, "FAIL 3 ones");

        $display("PASS: parity8 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 7. Binary to Gray Converter
    HDLProblem(
        id="comb_gray_conv",
        name="4-bit Binary to Gray Code Converter",
        category="combinational",
        prompt="Design a 4-bit Binary to Gray code converter in Verilog. Inputs: [3:0] bin. Outputs: [3:0] gray.",
        module_name="bin_to_gray4",
        reference_verilog="""\
module bin_to_gray4 (
    input wire [3:0] bin,
    output wire [3:0] gray
);
    assign gray = {bin[3], bin[3:1] ^ bin[2:0]};
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_bin_to_gray4;
    reg [3:0] bin;
    wire [3:0] gray;

    bin_to_gray4 uut (.bin(bin), .gray(gray));

    initial begin
        bin = 4'b0011; #5; // bin 3 -> gray 0010 (2)
        if (gray !== 4'b0010) $fatal(1, "FAIL 3");

        bin = 4'b0111; #5; // bin 7 -> gray 0100 (4)
        if (gray !== 4'b0100) $fatal(1, "FAIL 7");

        $display("PASS: bin_to_gray4 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 8. 8-bit Comparator
    HDLProblem(
        id="comb_comparator8",
        name="8-bit Magnitude Comparator",
        category="combinational",
        prompt="Design an 8-bit magnitude comparator in Verilog. Inputs: [7:0] a, b. Outputs: greater, equal, less.",
        module_name="comparator8",
        reference_verilog="""\
module comparator8 (
    input wire [7:0] a,
    input wire [7:0] b,
    output wire greater,
    output wire equal,
    output wire less
);
    assign greater = (a > b);
    assign equal   = (a == b);
    assign less    = (a < b);
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_comparator8;
    reg [7:0] a, b;
    wire greater, equal, less;

    comparator8 uut (.a(a), .b(b), .greater(greater), .equal(equal), .less(less));

    initial begin
        a = 8'd10; b = 8'd20; #5;
        if (greater !== 0 || equal !== 0 || less !== 1) $fatal(1, "FAIL less");

        a = 8'd42; b = 8'd42; #5;
        if (greater !== 0 || equal !== 1 || less !== 0) $fatal(1, "FAIL equal");

        $display("PASS: comparator8 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 9. 4-bit Johnson Counter
    HDLProblem(
        id="seq_johnson_counter",
        name="4-bit Johnson Counter",
        category="sequential",
        prompt="Design a 4-bit Johnson counter in Verilog with synchronous reset. Inputs: clk, rst. Output: [3:0] q.",
        module_name="johnson4",
        reference_verilog="""\
module johnson4 (
    input wire clk,
    input wire rst,
    output reg [3:0] q
);
    always @(posedge clk) begin
        if (rst) begin
            q <= 4'b0000;
        end else begin
            q <= {q[2:0], ~q[3]};
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_johnson4;
    reg clk, rst;
    wire [3:0] q;

    johnson4 uut (.clk(clk), .rst(rst), .q(q));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; #15;
        rst = 0;
        @(posedge clk); #1; if (q !== 4'b0001) $fatal(1, "FAIL state 1");
        @(posedge clk); #1; if (q !== 4'b0011) $fatal(1, "FAIL state 2");
        @(posedge clk); #1; if (q !== 4'b0111) $fatal(1, "FAIL state 3");
        @(posedge clk); #1; if (q !== 4'b1111) $fatal(1, "FAIL state 4");
        @(posedge clk); #1; if (q !== 4'b1110) $fatal(1, "FAIL state 5");
        $display("PASS: johnson4 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 10. 8-bit Universal Shift Register
    HDLProblem(
        id="seq_shift_reg",
        name="8-bit Universal Shift Register",
        category="sequential",
        prompt="Design an 8-bit universal shift register in Verilog with modes 0:Hold, 1:Shift Left, 2:Shift Right, 3:Parallel Load. Inputs: clk, rst, [1:0] mode, [7:0] d_in, s_left_in, s_right_in. Output: [7:0] q.",
        module_name="shift_reg8",
        reference_verilog="""\
module shift_reg8 (
    input wire clk,
    input wire rst,
    input wire [1:0] mode,
    input wire [7:0] d_in,
    input wire s_left_in,
    input wire s_right_in,
    output reg [7:0] q
);
    always @(posedge clk) begin
        if (rst) begin
            q <= 8'h00;
        end else begin
            case (mode)
                2'b00: q <= q;
                2'b01: q <= {q[6:0], s_left_in};
                2'b10: q <= {s_right_in, q[7:1]};
                2'b11: q <= d_in;
            endcase
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_shift_reg8;
    reg clk, rst;
    reg [1:0] mode;
    reg [7:0] d_in;
    reg s_left_in, s_right_in;
    wire [7:0] q;

    shift_reg8 uut (.clk(clk), .rst(rst), .mode(mode), .d_in(d_in), .s_left_in(s_left_in), .s_right_in(s_right_in), .q(q));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; mode = 0; d_in = 8'hAA; s_left_in = 1; s_right_in = 1; #15;
        rst = 0;
        mode = 2'b11; @(posedge clk); #1; if (q !== 8'hAA) $fatal(1, "FAIL load");
        mode = 2'b01; @(posedge clk); #1; if (q !== 8'h55) $fatal(1, "FAIL shl");
        $display("PASS: shift_reg8 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 11. Parameterized PWM Generator
    HDLProblem(
        id="seq_pwm_gen",
        name="8-bit PWM Generator",
        category="sequential",
        prompt="Design an 8-bit PWM generator in Verilog. Inputs: clk, rst, [7:0] duty. Output: pwm_out.",
        module_name="pwm8",
        reference_verilog="""\
module pwm8 (
    input wire clk,
    input wire rst,
    input wire [7:0] duty,
    output reg pwm_out
);
    reg [7:0] counter;

    always @(posedge clk) begin
        if (rst) begin
            counter <= 8'd0;
            pwm_out <= 1'b0;
        end else begin
            counter <= counter + 1'b1;
            pwm_out <= (counter < duty);
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_pwm8;
    reg clk, rst;
    reg [7:0] duty;
    wire pwm_out;

    pwm8 uut (.clk(clk), .rst(rst), .duty(duty), .pwm_out(pwm_out));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; duty = 8'd128; #15;
        rst = 0;
        @(posedge clk); #1; if (pwm_out !== 1'b1) $fatal(1, "FAIL initial high");
        $display("PASS: pwm8 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 12. Dual-Edge Triggered Flip-Flop
    HDLProblem(
        id="seq_dff_dual_edge",
        name="Dual-Edge Triggered Flip-Flop",
        category="sequential",
        prompt="Design a dual-edge triggered flip-flop in Verilog that updates output on both rising and falling clock edges. Inputs: clk, rst, d. Output: q.",
        module_name="dual_edge_dff",
        reference_verilog="""\
module dual_edge_dff (
    input wire clk,
    input wire rst,
    input wire d,
    output wire q
);
    reg q_pos, q_neg;

    always @(posedge clk or posedge rst) begin
        if (rst) q_pos <= 1'b0;
        else q_pos <= d ^ q_neg;
    end

    always @(negedge clk or posedge rst) begin
        if (rst) q_neg <= 1'b0;
        else q_neg <= d ^ q_pos;
    end

    assign q = q_pos ^ q_neg;
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_dual_edge_dff;
    reg clk, rst, d;
    wire q;

    dual_edge_dff uut (.clk(clk), .rst(rst), .d(d), .q(q));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; d = 0; #15;
        rst = 0;
        d = 1; @(posedge clk); #1; if (q !== 1'b1) $fatal(1, "FAIL posedge");
        d = 0; @(negedge clk); #1; if (q !== 1'b0) $fatal(1, "FAIL negedge");
        $display("PASS: dual_edge_dff passed.");
        $finish;
    end
endmodule
""",
    ),

    # 13. Moore 1011 Sequence Detector
    HDLProblem(
        id="fsm_seq_det_moore",
        name="Moore 1011 Sequence Detector",
        category="fsm",
        prompt="Design a Moore finite state machine in Verilog to detect sequence 1011 with synchronous reset. Inputs: clk, rst, data_in. Output: detected.",
        module_name="seq_moore1011",
        reference_verilog="""\
module seq_moore1011 (
    input wire clk,
    input wire rst,
    input wire data_in,
    output reg detected
);
    localparam S0 = 3'd0, S1 = 3'd1, S10 = 3'd2, S101 = 3'd3, S1011 = 3'd4;
    reg [2:0] state, next_state;

    always @(posedge clk) begin
        if (rst) state <= S0;
        else state <= next_state;
    end

    always @(*) begin
        case (state)
            S0: next_state = data_in ? S1 : S0;
            S1: next_state = data_in ? S1 : S10;
            S10: next_state = data_in ? S101 : S0;
            S101: next_state = data_in ? S1011 : S10;
            S1011: next_state = data_in ? S1 : S10;
            default: next_state = S0;
        endcase
    end

    always @(*) begin
        detected = (state == S1011);
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_seq_moore1011;
    reg clk, rst, data_in;
    wire detected;

    seq_moore1011 uut (.clk(clk), .rst(rst), .data_in(data_in), .detected(detected));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; data_in = 0; #15;
        rst = 0;
        @(posedge clk); data_in = 1;
        @(posedge clk); data_in = 0;
        @(posedge clk); data_in = 1;
        @(posedge clk); data_in = 1;
        @(posedge clk); #1;
        if (detected !== 1'b1) $fatal(1, "FAIL did not detect 1011");
        $display("PASS: seq_moore1011 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 14. Mealy 1101 Sequence Detector
    HDLProblem(
        id="fsm_seq_det_mealy",
        name="Mealy 1101 Sequence Detector",
        category="fsm",
        prompt="Design a Mealy finite state machine in Verilog to detect sequence 1101 (overlapping). Inputs: clk, rst, data_in. Output: detected.",
        module_name="seq_mealy1101",
        reference_verilog="""\
module seq_mealy1101 (
    input wire clk,
    input wire rst,
    input wire data_in,
    output reg detected
);
    localparam S0 = 2'd0, S1 = 2'd1, S11 = 2'd2, S110 = 2'd3;
    reg [1:0] state, next_state;

    always @(posedge clk) begin
        if (rst) state <= S0;
        else state <= next_state;
    end

    always @(*) begin
        detected = 1'b0;
        case (state)
            S0: next_state = data_in ? S1 : S0;
            S1: next_state = data_in ? S11 : S0;
            S11: next_state = data_in ? S11 : S110;
            S110: begin
                if (data_in) begin
                    detected = 1'b1;
                    next_state = S1;
                end else begin
                    next_state = S0;
                end
            end
            default: next_state = S0;
        endcase
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_seq_mealy1101;
    reg clk, rst, data_in;
    wire detected;

    seq_mealy1101 uut (.clk(clk), .rst(rst), .data_in(data_in), .detected(detected));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; data_in = 0; #15;
        rst = 0;
        @(posedge clk); data_in = 1;
        @(posedge clk); data_in = 1;
        @(posedge clk); data_in = 0;
        @(posedge clk); data_in = 1; #1;
        if (detected !== 1'b1) $fatal(1, "FAIL Mealy 1101 not detected");
        $display("PASS: seq_mealy1101 passed.");
        $finish;
    end
endmodule
""",
    ),

    # 15. Traffic Light Controller
    HDLProblem(
        id="fsm_traffic_light",
        name="Traffic Light Controller FSM",
        category="fsm",
        prompt="Design a 4-state traffic light controller in Verilog with main road and side road lights. Inputs: clk, rst, sensor. Outputs: [2:0] main_light, [2:0] side_light (Red, Yellow, Green encoded as 3-bit one-hot).",
        module_name="traffic_light_fsm",
        reference_verilog="""\
module traffic_light_fsm (
    input wire clk,
    input wire rst,
    input wire sensor,
    output reg [2:0] main_light,
    output reg [2:0] side_light
);
    localparam S_MG_SR = 2'd0, S_MY_SR = 2'd1, S_MR_SG = 2'd2, S_MR_SY = 2'd3;
    localparam RED = 3'b100, YELLOW = 3'b010, GREEN = 3'b001;

    reg [1:0] state, next_state;

    always @(posedge clk) begin
        if (rst) state <= S_MG_SR;
        else state <= next_state;
    end

    always @(*) begin
        case (state)
            S_MG_SR: next_state = sensor ? S_MY_SR : S_MG_SR;
            S_MY_SR: next_state = S_MR_SG;
            S_MR_SG: next_state = S_MR_SY;
            S_MR_SY: next_state = S_MG_SR;
            default: next_state = S_MG_SR;
        endcase
    end

    always @(*) begin
        case (state)
            S_MG_SR: begin main_light = GREEN; side_light = RED; end
            S_MY_SR: begin main_light = YELLOW; side_light = RED; end
            S_MR_SG: begin main_light = RED; side_light = GREEN; end
            S_MR_SY: begin main_light = RED; side_light = YELLOW; end
            default: begin main_light = RED; side_light = RED; end
        endcase
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_traffic_light_fsm;
    reg clk, rst, sensor;
    wire [2:0] main_light, side_light;

    traffic_light_fsm uut (.clk(clk), .rst(rst), .sensor(sensor), .main_light(main_light), .side_light(side_light));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; sensor = 0; #15;
        rst = 0;
        sensor = 1; @(posedge clk); #1;
        @(posedge clk); #1; if (side_light !== 3'b001) $fatal(1, "FAIL side light not green");
        $display("PASS: traffic_light_fsm passed.");
        $finish;
    end
endmodule
""",
    ),

    # 16. Synchronous FIFO Controller
    HDLProblem(
        id="fsm_fifo_ctrl",
        name="Synchronous FIFO Controller",
        category="fsm",
        prompt="Design a synchronous FIFO controller in Verilog with depth 8. Inputs: clk, rst, wr_en, rd_en. Outputs: [2:0] wr_ptr, rd_ptr, [3:0] count, full, empty.",
        module_name="fifo_ctrl",
        reference_verilog="""\
module fifo_ctrl (
    input wire clk,
    input wire rst,
    input wire wr_en,
    input wire rd_en,
    output reg [2:0] wr_ptr,
    output reg [2:0] rd_ptr,
    output reg [3:0] count,
    output wire full,
    output wire empty
);
    assign full  = (count == 4'd8);
    assign empty = (count == 4'd0);

    always @(posedge clk) begin
        if (rst) begin
            wr_ptr <= 3'd0;
            rd_ptr <= 3'd0;
            count  <= 4'd0;
        end else begin
            case ({wr_en && !full, rd_en && !empty})
                2'b10: begin
                    wr_ptr <= wr_ptr + 1'b1;
                    count  <= count + 1'b1;
                end
                2'b01: begin
                    rd_ptr <= rd_ptr + 1'b1;
                    count  <= count - 1'b1;
                end
                2'b11: begin
                    wr_ptr <= wr_ptr + 1'b1;
                    rd_ptr <= rd_ptr + 1'b1;
                end
                default: ;
            endcase
        end
    end
endmodule
""",
        testbench_verilog="""\
`timescale 1ns/1ps
module tb_fifo_ctrl;
    reg clk, rst, wr_en, rd_en;
    wire [2:0] wr_ptr, rd_ptr;
    wire [3:0] count;
    wire full, empty;

    fifo_ctrl uut (.clk(clk), .rst(rst), .wr_en(wr_en), .rd_en(rd_en), .wr_ptr(wr_ptr), .rd_ptr(rd_ptr), .count(count), .full(full), .empty(empty));

    always #5 clk = ~clk;

    initial begin
        clk = 0; rst = 1; wr_en = 0; rd_en = 0; #15;
        rst = 0;
        if (empty !== 1 || full !== 0) $fatal(1, "FAIL init");
        wr_en = 1; @(posedge clk); #1;
        if (empty !== 0 || count !== 4'd1) $fatal(1, "FAIL write");
        $display("PASS: fifo_ctrl passed.");
        $finish;
    end
endmodule
""",
    ),
]


def generate_markdown_report(report: Dict[str, Any]) -> str:
    """Generate a clean markdown report table for evidence artifacts."""
    md = [
        f"# Mind1.1 HDL / Verilog Benchmark Results",
        f"",
        f"- **Model / Target**: `{report['model_name']}`",
        f"- **Date**: {report['timestamp']}",
        f"- **Simulator**: `{report['simulator_used']}`",
        f"- **Mode**: `{'DRY RUN (reference code)' if report.get('is_dry_run') else 'REAL MODEL INFERENCE'}`",
        f"- **Pass Rate**: **{report['passed_problems']}/{report['total_problems']} ({report['pass_rate_pct']}%)**",
        f"",
        f"### Failure Breakdown",
        f"",
    ]
    if report.get("failure_breakdown"):
        for reason, count in report["failure_breakdown"].items():
            md.append(f"- **{reason}**: {count}")
    else:
        md.append("- No failures")

    md.extend([
        f"",
        f"### Problem Breakdown",
        f"",
        f"| Problem ID | Name | Category | Status | Exit Code | Failure Reason | Duration |",
        f"|:---|:---|:---|:---|:---|:---|:---|",
    ])
    for r in report["results"]:
        status_badge = "✅ VERIFIED" if r["status"] == "verified" else "❌ FAILED"
        reason = r.get("failure_reason") or "—"
        md.append(
            f"| `{r['problem_id']}` | {r['problem_name']} | {r['category']} | {status_badge} | {r['exit_code']} | {reason} | {r['duration_seconds']}s |"
        )
    md.append("")
    return "\n".join(md)


def main() -> None:
    parser = argparse.ArgumentParser(description="Mind1.1 Internal HDL Benchmark Runner")
    parser.add_argument("--model", default="qwen2.5-coder:7b", help="Model name / identifier")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434", help="Ollama server URL")
    parser.add_argument("--dry-run", action="store_true", help="Run with reference implementation")
    parser.add_argument("--output", default="", help="Optional output JSON report path")
    args = parser.parse_args()

    workspace = Path.cwd()
    model_name = f"{args.model} (dry-run)" if args.dry_run else args.model
    harness = HDLBenchmarkHarness(workspace, model_name=model_name, require_simulation=True)

    if args.dry_run:
        code_gen = None
    else:
        generator = LLMVerilogGenerator(model=args.model, base_url=args.ollama_url)
        code_gen = generator.generate

    report = harness.run_suite(code_generator=code_gen, is_dry_run=args.dry_run)

    print(f"\n=======================================================")
    print(f"Mind1.1 HDL Benchmark: {report['passed_problems']}/{report['total_problems']} Passed ({report['pass_rate_pct']}%)")
    print(f"Model: {report['model_name']} | Simulator: {report['simulator_used']}")
    print(f"=======================================================\n")

    md_content = generate_markdown_report(report)
    print(md_content)

    out_file = Path(args.output) if args.output else workspace / ".mind01" / "benchmarks" / "hdl_benchmark_results.json"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"\nSaved structured results to: {out_file}")


if __name__ == "__main__":
    main()


