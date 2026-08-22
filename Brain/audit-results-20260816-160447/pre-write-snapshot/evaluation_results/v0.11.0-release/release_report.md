# Mind1.1 v0.11.0 candidate release report

Release gate: **FAILED/BLOCKED**

This is version `0.11.0.dev0`, not a stable v0.11.0 release. No release tag is authorized.

## Architecture

The candidate adds a strict normalized intent, five-stage hierarchical deterministic routing, finite specialists/tool families/reason codes, capability-bound route identity, explicit ambiguity, and one lifecycle-scoped tool-exposure authority. Parser, policy, execution, verification, and completion remain separate authorities.

## Deterministic evidence

- Labeled route checks: 184/200
- First structural validity: 1.0
- Task class / specialist / tool family: 1.0 / 1.0 / 1.0
- Mutation intent: 0.92
- Frozen failures: 16

## Live development evidence

Retained complete development runs: 2. These are development-tuning runs, not independent blind runs. See each retained JSON report for raw per-case outputs.

## Gate blockers

- No independently controlled external blind labels/evaluator.
- Repository blind inputs are derived from visible archetypes and cannot prove independent blind performance.
- Zero complete end-to-end live runs including blind evaluation; at least three are required.
- Mandatory blind accuracy metrics are unavailable.
- Frozen adversarial labels contain 16 contradictory mutation-intent expectations.
- Semantic live runs select actions but do not execute tools.

## Safety boundary

No forbidden or unauthorized selection was observed in retained labeled runs. Execution safety cannot be inferred from a no-dispatch harness. v0.10 false-success, receipts, rollback, and policy tests remain mandatory deterministic checks. Host-executed verification is controlled but not sandboxed.

## Decision

Do not publish or tag v0.11.0 and do not begin or claim v0.12. Create a newly frozen, independently authored blind package and corrected dataset version before a future release candidate.
