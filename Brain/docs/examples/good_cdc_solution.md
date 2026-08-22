# Good CDC Example: Safe Multi-Flop Synchronization

This document shows a safe CDC synchronizer implementation.

## The Solution
Use at least two stages of flip-flops in the destination clock domain. The first flip-flop captures the asynchronous input and is allowed to go metastable. By the time the next clock edge arrives, the signal is highly likely to have settled to a stable logic level, which is then captured by the second flip-flop.

```
clk_b       ---> [ D-FF Stage 1 ] --(metastable_out)--> [ D-FF Stage 2 ] ---> sync_out
```

## Compliant Code
```systemverilog
module good_cdc (
  input logic clk_b,
  input logic async_signal,
  output logic sync_out
);

  logic stage1_reg;
  logic stage2_reg;

  // Double Flip-Flop Synchronizer
  always_ff @(posedge clk_b) begin
    stage1_reg <= async_signal; // First stage samples raw input, allows settling time
    stage2_reg <= stage1_reg;   // Second stage samples stable logic level
  end

  assign sync_out = stage2_reg;

endmodule
```

## Why It Works
Metastability decays exponentially over time. Introducing a full clock cycle of settling time between stage 1 and stage 2 exponentially reduces the probability of metastability propagating into the downstream logic.
    $$\text{Failure Probability} \propto e^{-T / \tau}$$
Where $T$ is the clock period and $\tau$ is the flip-flop's resolution time constant.
