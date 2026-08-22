// Self-checking Testbench Example
// Simulation-Only Code
`timescale 1ns/1ps

module good_self_checking_adder_tb;
  logic clk;
  logic [3:0] a, b;
  logic [4:0] sum;

  // Instantiate Device Under Test
  add_sub dut (
    .a(a),
    .b(b),
    .ctrl(1'b0), // Add mode
    .out(sum)
  );

  // Clock generation
  initial clk = 0;
  always #5 clk = ~clk;

  initial begin
    // Apply inputs synchronously
    @(posedge clk);
    a = 4'd2; b = 4'd3;
    #1; // Sample offset
    assert (sum == 5'd5) else $error("Vector 1 failed: expected 5, got %d", sum);

    @(posedge clk);
    a = 4'd15; b = 4'd1;
    #1;
    assert (sum == 5'd16) else $error("Vector 2 failed: expected 16, got %d", sum);

    @(posedge clk);
    a = 4'd8; b = 4'd8;
    #1;
    assert (sum == 5'd16) else $error("Vector 3 failed: expected 16, got %d", sum);

    $display("All test vectors successfully verified!");
    $finish;
  end

endmodule
