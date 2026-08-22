`timescale 1ns / 1ps

module and_gate_4 (
    input wire [3:0] a,
    input wire [3:0] b,
    output reg [3:0] y
);

assign y = a & b;

endmodule