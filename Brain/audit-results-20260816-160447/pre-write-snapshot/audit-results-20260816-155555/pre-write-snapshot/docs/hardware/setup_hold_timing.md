# Setup and Hold Timing Constraints

## 1. Definition
* **Setup Time ($T_{\text{setup}}$)**: The minimum time an input data signal must remain stable *before* the active clock edge.
* **Hold Time ($T_{\text{hold}}$)**: The minimum time an input data signal must remain stable *after* the active clock edge.
* **Clock-to-Output Delay ($T_{\text{cq}}$)**: The delay from the active clock edge to the update of the flip-flop's output signal.
* **Combinational Delay ($T_{\text{comb}}$)**: The delay along the combinational path between launch and capture registers.
* **Clock Skew ($T_{\text{skew}}$)**: The difference in clock signal arrival times at the launch and capture registers.

## 2. Core Timing Equations

### Setup Constraint
To prevent setup violations, the data must arrive at the capture register before the setup window begins:
$$T_{\text{cq}} + T_{\text{comb}} + T_{\text{setup}} \le T_{\text{clk}} + T_{\text{skew}}$$
Where:
* $T_{\text{clk}}$ = Clock period.
* Max allowable combinational delay:
  $$T_{\text{comb, max}} = T_{\text{clk}} - T_{\text{cq}} - T_{\text{setup}} + T_{\text{skew}}$$

### Hold Constraint
To prevent hold violations, the data must remain stable long enough for the capture register to lock the state:
$$T_{\text{cq}} + T_{\text{comb}} \ge T_{\text{hold}} + T_{\text{skew}}$$
Where:
* Min required combinational delay:
  $$T_{\text{comb, min}} = T_{\text{hold}} - T_{\text{cq}} + T_{\text{skew}}$$

## 3. Examples

### Calculation Example: Setup Margin (Slack)
* Given:
  - $T_{\text{clk}} = 10.0\text{ns}$ (100MHz clock)
  - $T_{\text{cq}} = 1.0\text{ns}$
  - $T_{\text{comb}} = 7.5\text{ns}$
  - $T_{\text{setup}} = 0.5\text{ns}$
  - $T_{\text{skew}} = 0.1\text{ns}$
* Calculation:
  $$\text{Slack}_{\text{setup}} = (T_{\text{clk}} + T_{\text{skew}}) - (T_{\text{cq}} + T_{\text{comb}} + T_{\text{setup}})$$
  $$\text{Slack}_{\text{setup}} = (10.0 + 0.1) - (1.0 + 7.5 + 0.5)$$
  $$\text{Slack}_{\text{setup}} = 10.1 - 9.0 = 1.1\text{ns} \quad (\text{PASS})$$

## 4. Common Mistakes & Recommendations
- **Mistake**: Lowering the clock period (higher frequency) to fix hold violations. Clock period is not a variable in the hold time constraint equation.
  - *Recommendation*: Introduce buffer delays into the combinational path to fix hold violations.
- **Mistake**: Reversing the sign of clock skew. Skew helps setup time if positive, but hurts hold time.
  - *Recommendation*: Use standard definitions where positive skew means the capture clock arrives after the launch clock.
