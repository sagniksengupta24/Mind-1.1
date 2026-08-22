`timescale 1ns / 1ps

module and_gate_2 (
  input a,
  input b,
  output reg y
);

assign y = a & b;

endmodule