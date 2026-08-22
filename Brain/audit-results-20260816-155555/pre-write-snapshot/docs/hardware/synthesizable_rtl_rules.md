# Synthesizable RTL Design Rules

## 1. Definition
Register-Transfer Level (RTL) code defines how data flows between registers on active clock edges. Synthesizable RTL code is code that can be compiled by a logic synthesis tool (like Design Compiler or Yosys) into a target gate-level netlist.

## 2. Core Rules
* **No Simulation Constructs**: Do not use `#delay`, `initial` blocks, `fork/join`, `real`, `time`, `$display`, or `$finish` in modules intended for synthesis.
* **Explicit Widths**: Always define bit widths for all constants and vectors (e.g. use `8'hFF` or `8'd255` instead of `'hFF` or `255`).
* **Complete Conditional Paths**: Assign default values to combinational outputs under all branches (like `default` in case statements or `else` in if-else trees) to prevent compiler latch inference.
* **Strict Assignment Categories**:
  - Use blocking assignments (`=`) in combinational blocks (`always_comb`).
  - Use non-blocking assignments (`<=`) in sequential blocks (`always_ff @(posedge clk)`).

## 3. Examples

### Good (Synthesizable Accumulator)
```systemverilog
module accumulator (
  input logic clk,
  input logic rst_n,
  input logic [7:0] data_in,
  output logic [15:0] acc_out
);
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      acc_out <= 16'd0;
    end else begin
      acc_out <= acc_out + {8'd0, data_in};
    end
  end
endmodule
```

### Bad (Non-Synthesizable Initial Block & Delays)
```systemverilog
module bad_acc (
  input clk, rst,
  input [7:0] val,
  output reg [15:0] out
);
  initial out = 0; // BAD: initial block is ignored or illegal in ASIC synthesis

  always @(posedge clk) begin
    #5 out <= out + val; // BAD: #5 delay is ignored during logic synthesis
  end
endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Using implicit wire declarations (e.g., omitting `logic` or `wire`).
  - *Recommendation*: Use `default_nettype none` at the top of your files to catch undeclared signal errors.
- **Mistake**: Inferring latches by omitting output defaults in combinational case blocks.
  - *Recommendation*: Initialize outputs to safe default values at the beginning of comb always blocks.
