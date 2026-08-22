# Setup and Hold Slack Derivations

This document shows mathematical derivations for calculating setup and hold slack.

## 1. Setup Slack Derivation

The setup constraint ensures that data arrives at the destination register before the setup window starts.

$$\text{Data Arrival Time} = T_{\text{cq}} + T_{\text{comb}}$$
$$\text{Data Required Time} = T_{\text{clk}} - T_{\text{setup}} + T_{\text{skew}}$$

For a stable design, the arrival time must be less than or equal to the required time:
$$T_{\text{cq}} + T_{\text{comb}} \le T_{\text{clk}} - T_{\text{setup}} + T_{\text{skew}}$$

We define setup slack as:
$$\text{Slack}_{\text{setup}} = (T_{\text{clk}} + T_{\text{skew}}) - (T_{\text{cq}} + T_{\text{comb}} + T_{\text{setup}})$$
- **Slack > 0**: Setup timing is met.
- **Slack < 0**: Setup violation occurs (needs lower combinational delay $T_{\text{comb}}$ or a larger clock period $T_{\text{clk}}$).

---

## 2. Hold Slack Derivation

The hold constraint ensures that the source register does not overwrite the destination register before the hold window ends.

$$\text{Data Arrival Time} = T_{\text{cq}} + T_{\text{comb}}$$
$$\text{Data Required Time} = T_{\text{hold}} + T_{\text{skew}}$$

To prevent hold violations, the arrival time must exceed the required time:
$$T_{\text{cq}} + T_{\text{comb}} \ge T_{\text{hold}} + T_{\text{skew}}$$

We define hold slack as:
$$\text{Slack}_{\text{hold}} = (T_{\text{cq}} + T_{\text{comb}}) - (T_{\text{hold}} + T_{\text{skew}})$$
- **Slack > 0**: Hold timing is met.
- **Slack < 0**: Hold violation occurs (needs more combinational delay $T_{\text{comb}}$).
