# Bad CDC Example: Unsafe Single-Flop Domain Crossing

This document shows a common unsafe clock domain crossing configuration.

## The Design Mistake
Passing an asynchronous logic signal directly into logic gates on the destination clock domain, or using only a single-stage register synchronizer.

```
clk_a       ---> [ Registers ] --(async_out)--> [ Comb Gates ] ---> [ D-FF ] clk_b
                                                                      (Metastable!)
```

## Non-compliant Code
```systemverilog
module bad_cdc (
  input logic clk_b,
  input logic async_signal,
  output logic out_b
);

  // UNSAFE: If async_signal transitions close to clk_b rise edge,
  // setup/hold time is violated, causing sync_reg to enter metastability.
  // The output out_b will carry unstable values into downstream logic gates.
  logic sync_reg;
  always_ff @(posedge clk_b) begin
    sync_reg <= async_signal;
  end

  assign out_b = sync_reg;

endmodule
```

## Why It Fails
If `sync_reg` becomes metastable, it takes time to settle to a stable state. Because its output is connected directly to logic gates, the unstable state propagates immediately. This results in undefined values in the capture domain.
