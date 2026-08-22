`timescale 1ns / 1ps

module and_gate_10 (
    input wire a,
    input wire b,
    output reg y
);

assign y = a & b;

endmodule