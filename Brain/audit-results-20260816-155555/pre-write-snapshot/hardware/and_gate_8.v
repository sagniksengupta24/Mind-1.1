`timescale 1ns / 1ps

module and_gate_8 (
    input [7:0] a,
    input [7:0] b,
    output reg [7:0] y
);

assign y = a & b;

endmodule