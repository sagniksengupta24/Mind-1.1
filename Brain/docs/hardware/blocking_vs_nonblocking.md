# Blocking vs. Non-blocking Assignments

## 1. Definition
Verilog/SystemVerilog supports two types of signal assignment operators:
* **Blocking Assignment (`=`)**: Evaluates the right-hand side and assigns to the left-hand side immediately, blocking subsequent statement executions in the same block.
* **Non-blocking Assignment (`<=`)**: Evaluates the right-hand side immediately but schedules the assignment update for the end of the current simulation time step (Non-blocking Assignment event queue).

## 2. Core Rules
* **Sequential Logic**: Always use non-blocking assignments (`<=`) inside sequential always blocks (`always_ff @(posedge clk)`).
* **Combinational Logic**: Always use blocking assignments (`=`) inside combinational always blocks (`always_comb`).
* **No Mixing**: Never mix blocking and non-blocking assignments in the same `always` block.
* **Assigning to the Same Variable**: Do not assign values to the same variable from multiple `always` blocks.

## 3. Examples

### Good (Sequential Shift Register using Non-blocking)
```systemverilog
module shift_reg (
  input logic clk,
  input logic d,
  output logic q1, q2
);
  always_ff @(posedge clk) begin
    q1 <= d;  // Schedules update.
    q2 <= q1; // Evaluates prior q1 value, updating synchronously.
  end
endmodule
```

### Bad (Sequential Race Hazard using Blocking)
```systemverilog
module bad_shift_reg (
  input clk, d,
  output reg q1, q2
);
  always @(posedge clk) begin
    q1 = d;  // Immediate update: q1 takes value of d.
    q2 = q1; // Immediate update: q2 takes value of updated q1. Race condition occurs!
  end
endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Using blocking assignments in register paths. This introduces race conditions in simulation that mismatch the synthesized hardware logic.
  - *Recommendation*: Double-check that all registers use `<=`.
- **Mistake**: Using non-blocking assignments in combinational assignment trees, creating delta-delay anomalies.
  - *Recommendation*: Use `always_comb` and `=` for combinational paths.
