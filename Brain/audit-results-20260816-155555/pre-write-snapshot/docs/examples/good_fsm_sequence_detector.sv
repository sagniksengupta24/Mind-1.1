// Moore FSM: Detects serial bit sequence '11'
// Synthesizable RTL Implementation with separated state register and next-state logic
module good_fsm_sequence_detector (
  input logic clk,
  input logic rst_n,
  input logic din,
  output logic dout
);

  typedef enum logic [1:0] {
    ST_RESET = 2'b00,
    ST_SEEN1 = 2'b01,
    ST_SEEN11 = 2'b10
  } state_t;

  state_t state, next_state;

  // Process 1: State Register (Sequential logic)
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= ST_RESET;
    end else begin
      state <= next_state;
    end
  end

  // Process 2: Next-State Logic (Combinational logic)
  always_comb begin
    next_state = state; // Default assignment to prevent latch inference
    case (state)
      ST_RESET:  next_state = (din) ? ST_SEEN1  : ST_RESET;
      ST_SEEN1:  next_state = (din) ? ST_SEEN11 : ST_RESET;
      ST_SEEN11: next_state = (din) ? ST_SEEN11 : ST_RESET;
      default:   next_state = ST_RESET;
    endcase
  end

  // Process 3: Output Logic
  assign dout = (state == ST_SEEN11);

endmodule
