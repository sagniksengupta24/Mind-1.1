# Workstream 5 — Cold-start trace collection and supervised fine-tuning (SFT)

Status: **PLAN-ONLY** (per user direction). The trace-collection half is
implemented and tested; the fine-tuning half is a written design that is not
executed in this pass.

## What is implemented (this pass)

Task bundles are recorded into the **existing** hash-chained `TraceStore`
(`.mind01/traces/*.jsonl`), extending it — no parallel logging system:

- `TraceStore.record_task_bundle()` appends a `task_bundle` event with:
  sanitized prompt summary (sha256 + redacted bounded preview), action
  sequence (tool + sanitized args), verification results, completion status,
  step count, latency, workspace name, session id, model name.
- Recording is **consent-gated**: a bundle is only written when
  `consent=True` and a consent source is recorded. The `agent` only calls it
  when `AgentConfig.trace_bundles=True` (`--trace-bundles`).
- `doctor --eval` enables bundle recording for eval-suite runs, so every
  suite task produces a bundle usable as SFT seed data.
- Tests: `tests/test_trace_bundles.py` (recording, consent-gating, chain
  integrity, sanitization).

## Why bundles and not raw logs

The action sequence (what the model actually did, in order) plus the
verification result is exactly the (prompt → behavior → outcome) triple a
protocol-fine-tune needs. The hash chain guarantees no bundle is silently
rewritten, satisfying the constraint not to weaken the receipt/hash-chain
system.

## Filtering rule (mandatory)

Only **verified-successful** traces enter the training set. A bundle is
eligible when `completion_status == "verified"` (runtime-owned deterministic
evidence) or, for eval-suite runs, when the task's `eval_check_command`
passed. Failed/repair-heavy runs are excluded from seed data but retained for
later preference-style analysis.

## Cold-start seed data (cloud use, strictly bounded)

Per the original constraints, cloud use is permitted **only** for generating
offline training traces:

- Must be explicitly opt-in (a flag/env var the user sets), never on by
  default.
- Used only against the Workstream 0 task suite offline; never for live
  inference on user data.
- Every generated trace is labeled with its data source
  (`consent_source: "cloud_seed_<provider>"`) and stored in a
  separately removable export directory (`.mind01/sft_seed/`).
- The bundle schema makes provenance explicit and removable by source.

## SFT design (not executed this pass)

Target: qwen2.5-coder:7b (the local baseline model).

1. **Data assembly**: filter bundles to verified-successful runs; require a
   minimum of a few hundred examples before training (current suite is 50
   tasks; a few repeated runs + opt-in cloud seed would be needed).
2. **Format**: reconstruct the canonical protocol input/output pairs from
   each bundle — the action instruction (prompt, phase, visible tools,
   schemas) as the input, and the parsed canonical JSON action as the target.
   This teaches the model the local protocol/action format, not general
   coding.
3. **QLoRA** (not RL/PPO — out of scope for this pass): 4-bit base model,
   `target_modules` include **MLP projection layers** (gate/up/down) plus
   attention q/k/v/o — the original instruction explicitly requires MLP
   layers, not only attention.
4. **Training**: standard SFT loss (cross-entropy on target tokens), LR
   ~2e-4, a few epochs with early stopping on a held-out slice of bundles.
5. **Eval gate**: before/after delta on the Workstream 0 suite with the
   fine-tuned model. If the delta is not a clear improvement, the fine-tune
   is not presented as a win. The suite report (`doctor --eval`) already
   measures completion rate, verification pass rate, REPAIR_REQUIRED rate,
   average steps, and average latency.

## Not in scope this pass

- RLHF / PPO loops.
- Any cloud model at inference time.
- Training runs (hardware: CPU-only, no GPU — a 7B QLoRA run is not
  practical on this machine without a GPU; the design documents what to run
  when one is available).
