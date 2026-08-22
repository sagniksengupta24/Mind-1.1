# Clock Domain Crossing (CDC) and Metastability

## 1. Definition
* **Metastability**: An unstable state where a flip-flop output fails to settle to a stable high (1) or low (0) voltage within the required clock-to-output delay. This occurs when asynchronous input signals transition within the flip-flop's setup and hold timing windows.
* **Clock Domain Crossing (CDC)**: Passing a signal from logic running on one clock domain ($CLK_A$) to another clock domain ($CLK_B$) running asynchronously.

## 2. Core Rules
* **Single-Bit Signals**: Must be synchronized using a minimum of a **2-stage D-FF synchronizer** (two serial registers clocked by the destination clock $CLK_B$).
* **Multi-Bit Signals**: Never synchronize multi-bit data vectors using independent parallel 2-stage synchronizers (skew differences cause read errors).
* **Multi-Bit Synchronization Techniques**:
  - Use a handshake protocol (Ready/Valid interfaces).
  - Use an asynchronous FIFO (First-In, First-Out memory) using Gray-code pointer conversions.
  - Convert data paths to Gray-code when incrementing values.

## 3. Examples

### Good (Single-Bit 2-stage Flip-Flop Synchronizer)
```systemverilog
module cdc_sync (
  input logic clk_b,
  input logic async_in,
  output logic sync_out
);
  logic sync_reg_1;

  always_ff @(posedge clk_b) begin
    sync_reg_1 <= async_in;
    sync_out   <= sync_reg_1;
  end
endmodule
```

### Bad (Unsafe Parallel Multi-Bit Synchronization)
```systemverilog
module bad_multi_bit_cdc (
  input clk_b,
  input [3:0] async_data,
  output [3:0] sync_data
);
  // BAD: Parallel 2-stage registers can read data bits on different clock edges due to path delays (skew).
  cdc_sync bit0 (.clk_b(clk_b), .async_in(async_data[0]), .sync_out(sync_data[0]));
  cdc_sync bit1 (.clk_b(clk_b), .async_in(async_data[1]), .sync_out(sync_data[1]));
  cdc_sync bit2 (.clk_b(clk_b), .async_in(async_data[2]), .sync_out(sync_data[2]));
  cdc_sync bit3 (.clk_b(clk_b), .async_in(async_data[3]), .sync_out(sync_data[3]));
endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Using a single-flop synchronizer. If metastability occurs on the output of the first flip-flop, it will propagate directly to the downstream circuit.
  - *Recommendation*: Always use at least 2 stages, or 3 stages for ultra-high reliability applications.
- **Mistake**: Failing to register inputs before domain crossings.
  - *Recommendation*: Register signals in the source clock domain before crossing domains to minimize combinational skew.
