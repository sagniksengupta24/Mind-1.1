# Hinglish Technical Learning: Clock Domain Crossing

This document shows a bilingual Hinglish-English explanation of Clock Domain Crossing.

---

## Explanation

जब हम एक signal को एक clock domain (मान लो `CLK_A` running at 100MHz) से दूसरे clock domain (`CLK_B` running asynchronously at 250MHz) में भेजते हैं, तो उसे **Clock Domain Crossing (CDC)** कहते हैं।

### Metastability की Problem
अगर source domain का signal, destination domain की clock edge के बहुत पास (setup/hold window के अंदर) transition करता है, तो capture flip-flop का output 0 या 1 पर settle होने के बजाय बीच में ही अटक जाता है। इस unstable state को **Metastability** कहते हैं।

### Solution: Double Flip-Flop Synchronizer
इस problem को solve करने के लिए हम destination domain में दो flip-flops को series में लगाते हैं:

```
CLK_B edge:
async_signal ---> [ Flip-Flop 1 ] --(unstable)--> [ Flip-Flop 2 ] ---> sync_out
```

- **Flip-Flop 1** asynchronous input को capture करता है। भले ही इसका output metastable (unstable) हो जाए, इसे settle होने के लिए एक पूरा clock cycle मिलता है।
- **Flip-Flop 2** next clock edge पर उस settled stable logic level को capture करके सुरक्षित output forward करता है।

---

## SystemVerilog Code Example

```systemverilog
module cdc_synchronizer (
  input logic clk_b,
  input logic async_in,
  output logic sync_out
);

  logic reg_stage1;
  logic reg_stage2;

  always_ff @(posedge clk_b) begin
    reg_stage1 <= async_in;   // Stage 1: Samples asynchronous input
    reg_stage2 <= reg_stage1; // Stage 2: Captures stable logic value
  end

  assign sync_out = reg_stage2;

endmodule
```
Variable names, syntax (`always_ff`, `posedge`), and logic expressions logic strictly standard English script me maintain kiye gaye hain.
