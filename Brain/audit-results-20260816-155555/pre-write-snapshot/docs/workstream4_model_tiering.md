# Workstream 4 — Data-driven model tiering (decision record)

Status: **PLAN / DEFERRED with measured justification** (no code change yet).

## Measured hardware facts (this machine)

- **No GPU**: `nvidia-smi` absent; inference is CPU-only via Ollama.
- **RAM**: 30 GB total, ~23 GB free at baseline, 8 GB swap.
- **CPU**: 20 cores.
- **Model available**: only `qwen2.5-coder:7b` is pulled.
- **Measured baseline latency** (Workstream 0, 50-task suite, qwen2.5-coder:7b):
  avg 15.1 s/task on CPU-only inference.

## What the workstream asked for

> Add a risk/complexity classifier before MODEL_CALL. Route low-risk/simple
> tasks to the existing 7B model; route medium/high-risk tasks to a larger
> local model IF one is available on this machine — check actual available
> RAM/VRAM first and pick a real, installable model size, don't assume 32B
> is available. Instrument REPAIR_REQUIRED and eval-suite completion rate per
> tier.

## Decision

**Do not build tiering yet.** Rationale, from actual measurements:

1. **No larger model is realistically usable.** A 14B Q4 quant needs ~9 GB of
   RAM (fits in 23 GB free) but runs at roughly 2–3 tokens/s on CPU (7B runs
   ~5–8 tokens/s). The tiering overhead (extra classifier call + slower large
   model) would **increase** latency on exactly the tasks the eval already
   struggles with, and the eval is model-latency-bound (15 s avg/task).

2. **The bottleneck is not model size.** The Workstream 0 baseline showed the
   failures are routing misclassification (inspection prompts sent to a
   no-tool terminal) and a tool-exposure deadlock for new-file targets. A
   bigger model cannot fix a route that exposes zero tools. Tiering before
   fixing routing would be optimizing the wrong layer.

3. **The classifier itself would be a model call** on a model that is already
   the thing being tiered — a circular dependency with no independent
   signal, and it would double the per-request model latency for every task.

## What would change the decision

- A GPU becomes available (then a 13–14B Q4 becomes viable for the high tier).
- The Workstream 0 suite reaches a plateau on routing+exposure fixes and the
  remaining failures are demonstrably model-capability-limited (verified by a
  larger model succeeding where 7B fails, on a held-out set).
- A deterministic (non-model) complexity/risk classifier can be derived from
  the existing task contract (target scope size, mutation vs inspection,
  blast radius) with a measured precision/recall before it is allowed to
  route anything.

## Instrumentation that already exists for when tiering is built

- `AgentState.route_confidence`, `risk_level`, and the task contract provide
  the features a deterministic tier assignment would use.
- `REPAIR_REQUIRED` rate and per-tier completion rate are already reported by
  `doctor --eval` (the suite report), so a before/after delta per tier is
  measurable with no new harness.

## Gate for WS4

Tiering is only enabled after (a) routing + exposure fixes are in and the
eval suite's completion rate is re-measured, and (b) a non-model risk
classifier has been validated against the suite with precision ≥ 0.90 on
high-risk labels.
