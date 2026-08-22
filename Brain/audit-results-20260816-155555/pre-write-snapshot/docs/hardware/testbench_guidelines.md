# Testbench Design and Verification Guidelines

## 1. Definition
A testbench is a non-synthesizable simulation wrapper used to apply stimulus signals to a Device Under Test (DUT) and verify its logical outputs.

## 2. Core Rules
* **Use Simulation-Only Constructs**: Testbenches can use non-synthesizable commands (`initial`, `always` without edges, `#` delays, `$display`, `$finish`).
* **Clock Generation**: Implement stable clocks using free-running loops (e.g. `always #5 clk = ~clk;`).
* **Self-checking Logic**: Avoid manual waveform inspection. Use automatic assertion statements or conditional value comparisons to flag failures.
* **Exiting Cleanly**: Always use `$finish` to terminate the simulation run once the test vectors finish executing.

## 3. Examples

### Good (Self-checking 8-bit Adder Testbench)
```systemverilog
`timescale 1ns/1ps

module adder_tb;
  logic clk;
  logic [7:0] a, b;
  logic [8:0] sum;

  // Instantiate the Device Under Test (DUT)
  adder dut (
    .a(a),
    .b(b),
    .sum(sum)
  );

  // Clock generator (100MHz)
  initial clk = 0;
  always #5 clk = ~clk;

  // Stimulus process
  initial begin
    // Apply vectors synchronously
    a = 8'd0; b = 8'd0;
    #10;
    assert (sum == 9'd0) else $error("Test failed at vector 1. sum=%d", sum);

    a = 8'd10; b = 8'd20;
    #10;
    assert (sum == 9'd30) else $error("Test failed at vector 2. sum=%d", sum);

    a = 8'hFF; b = 8'h01;
    #10;
    assert (sum == 9'h100) else $error("Test failed at vector 3. sum=%d", sum);

    $display("All tests completed successfully!");
    $finish;
  end

endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Forgetting to initialize the clock signal. In Verilog, uninitialized logic starts as `X` (undefined), meaning `clk = ~clk` will remain `X` indefinitely.
  - *Recommendation*: Use an `initial clk = 0;` block.
- **Mistake**: Omitting `$finish`, causing the simulation to hang or run indefinitely.
  - *Recommendation*: Ensure every execution path terminates with `$finish`.
