# SystemVerilog FSM Coding Style

## 1. Definition
Finite State Machines (FSMs) in digital logic transition between states based on current state and input conditions. For synthesis stability and timing verification, a clean state-separation coding style is required.

## 2. Core Rules
* **Separate Registers from Next-State Logic**: Use a strict two-process or three-process FSM architecture.
  - Process 1: A sequential block (`always_ff`) to update the current state register on active clock edges.
  - Process 2: A combinational block (`always_comb`) to calculate next-state transitions.
  - Process 3 (Optional): A combinational block or sequential registers to assign outputs.
* **Explicit Enums**: Declare states using enumerated types with explicit widths and encoding schemes (e.g. `typedef enum logic [1:0] {IDLE=2'd0, S1=2'd1, S2=2'd2} state_t;`).
* **Avoid Latch Inference**: Initialize the `next_state` variable to `current_state` or a default state at the start of your combinational block.

## 3. Examples

### Good (Moore FSM Sequence Detector '11')
```systemverilog
module sequence_detector (
  input logic clk,
  input logic rst_n,
  input logic x,
  output logic detected
);
  typedef enum logic [1:0] {
    ST_IDLE  = 2'b00,
    ST_SEEN1 = 2'b01,
    ST_SEEN11= 2'b10
  } state_t;

  state_t state, next_state;

  // Process 1: State Register (Sequential)
  always_ff @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
      state <= ST_IDLE;
    end else begin
      state <= next_state;
    end
  end

  // Process 2: Next-State Logic (Combinational)
  always_comb begin
    next_state = state; // Default assignment to avoid latch inference
    case (state)
      ST_IDLE:  next_state = (x) ? ST_SEEN1  : ST_IDLE;
      ST_SEEN1: next_state = (x) ? ST_SEEN11 : ST_IDLE;
      ST_SEEN11:next_state = (x) ? ST_SEEN11 : ST_IDLE;
      default:  next_state = ST_IDLE;
    endcase
  end

  // Process 3: Output Logic
  assign detected = (state == ST_SEEN11);

endmodule
```

### Bad (Single-Process FSM with Output Timing Risks)
```systemverilog
module bad_fsm (
  input clk, rst, x,
  output reg out
);
  reg [1:0] state;
  // Single-process is harder to analyze, optimizes poorly, and increases output delay.
  always @(posedge clk or posedge rst) begin
    if (rst) begin
      state <= 0;
      out <= 0;
    end else begin
      case (state)
        0: begin
          if (x) state <= 1;
          out <= 0;
        end
        1: begin
          if (x) begin state <= 2; out <= 1; end
          else begin state <= 0; out <= 0; end
        end
        // Missing default or complete state mapping inferring bad transitions
      endcase
    end
  end
endmodule
```

## 4. Common Mistakes & Recommendations
- **Mistake**: Forgetting default branches in case statements.
  - *Recommendation*: Always write a `default` case and assign all variables to prevent latches.
- **Mistake**: Using blocking assignments (`=`) in sequential state registers.
  - *Recommendation*: Use `state <= next_state` to avoid race conditions in simulation.
