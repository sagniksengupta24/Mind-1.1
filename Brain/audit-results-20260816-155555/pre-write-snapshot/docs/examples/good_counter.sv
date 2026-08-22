// Device: 4-bit up-counter with synchronous active-high reset
// Synthesizable RTL Implementation
module good_counter (
  input logic clk,
  input logic rst,
  input logic enable,
  output logic [3:0] count
);

  always_ff @(posedge clk) begin
    if (rst) begin
      count <= 4'd0;
    end else if (enable) begin
      count <= count + 4'd1;
    end
  end

endmodule
