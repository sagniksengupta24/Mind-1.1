# Reset Design Guidelines

## 1. Definition
Resets initialize registers to known states at system startup or after error events. Design choices between synchronous and asynchronous resets impact logic footprint, routing overhead, and timing verification.

## 2. Core Rules
* **Synchronous Reset**: Reset assertion and deassertion are sampled only on active clock edges.
  - Advantage: Eliminates glitch risks, synthesizes to combinational logic inputs, simplifies timing analysis.
  - Disadvantage: Requires active clock to execute reset.
* **Asynchronous Reset**: Reset assertion and deassertion take effect immediately, independent of clock cycles.
  - Advantage: Works without active clocks.
  - Disadvantage: Deassertion must be synchronized to prevent metastability hazards.
* **Mind Default**: Use synchronous resets by default unless asynchronous resets are explicitly requested.
* **Reset Synchronizers**: Always synchronize asynchronous resets upon deassertion to meet register recovery and removal constraints.

## 3. Examples

### Good (Synchronous Reset D-FF)
```systemverilog
module dff_sync_rst (
  input logic clk,
  input logic rst,
  input logic d,
  output logic q
);
  always_ff @(posedge clk) begin
    if (rst) begin
      q <= 1'b0;
    end else begin
      q <= d;
    end
  end
endmodule
```

### Good (Synchronized Asynchronous Reset Deassertion)
```systemverilog
module reset_bridge (
  input logic clk,
  input logic async_rst_n,
  output logic sync_rst_n
);
  logic rst_reg_1;

  always_ff @(posedge clk or negedge async_rst_n) begin
    if (!async_rst_n) begin
      rst_reg_1  <= 1'b0;
      sync_rst_n <= 1'b0;
    end else begin
      rst_reg_1  <= 1'b1;
      sync_rst_n <= rst_reg_1;
    end
  end
endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Clocking asynchronous resets inside synchronous always blocks (e.g. `always @(posedge clk) if (rst) ...` but keeping `rst` in the sensitivity list).
  - *Recommendation*: Ensure the sensitivity list matches the conditional branch triggers.
- **Mistake**: Using asynchronous resets without synchronizing their deassertion. This can cause some registers to exit reset a clock cycle before others, leading to state corruption.
  - *Recommendation*: Use a reset bridge/synchronizer to align the reset deassertion edge.
