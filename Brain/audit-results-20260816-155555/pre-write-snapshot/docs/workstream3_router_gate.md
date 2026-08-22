# Workstream 3 — Router validation harness and v2-default gate

Status: harness existed on the branch; baseline run + gate decision documented
here.

## What the harness provides

`scripts/evaluate_semantic_router.py` (with `mind01/semantic_benchmark_v2.py`)
reports, per split:

- accuracy per field: task class, specialist, immediate family, response
  mode, risk level, reason code, allowed tools, first lifecycle step,
  hard-constraint consistency, all-field exact acceptance;
- per-class / per-family / per-risk breakdowns and confusion matrices;
- safety invariants: `invalid_combination_rate`, `unauthorized_mutations`,
  `unsafe_selections`, `parser_failure_rate`;
- gate evaluation against frozen thresholds (`DEVELOPMENT_GATES`,
  `HOLDOUT_GATES`);
- four-way ablation (legacy / staged-no-constraints /
  staged-candidate-reduction / full_v2);
- deterministic CI mode (no Ollama) plus opt-in `--live` mode.

## Baseline results (this machine, this branch)

Deterministic CI classifier on the 100-case development split — this
validates the harness and the deterministic plumbing, NOT the 7B model:

| field | accuracy |
|---|---|
| task_class | 1.00 |
| specialist | 1.00 |
| immediate_family | 1.00 |
| response_mode | 1.00 |
| risk_level | 1.00 |
| reason_code | 1.00 |
| allowed_tools | 1.00 |
| first_lifecycle_step | 1.00 |
| hard_constraint_consistency | 1.00 |
| all_field_exact_acceptance | 1.00 |
| invalid_combination_rate | 0.00 |
| unsafe_selections | 0.00 |

All DEVELOPMENT_GATES passed in deterministic mode. The ablation shows the
same fixture classifier at 1.0 for full_v2 and legacy at
task=0.95 / specialist=0.90 / family=0.95 / reason=0.86 / risk=0.75.

**Honest limitation**: the deterministic fixture classifier is not evidence
of local model quality (the docs already state this). A live 7B-model run on
the 100-case development split is the real gate and was not executed here
because CPU-only Ollama was consumed by the Workstream 0 suite re-run; the
harness is ready (`--live`).

## v2-default gate (in writing)

v2 becomes the default router only when **all** of the following hold:

1. A **live** (Ollama, real 7B) run of the 100-case development split passes
   every DEVELOPMENT_GATES threshold, notably:
   - `task_class_accuracy >= 0.88`
   - `specialist_accuracy >= 0.82`
   - `immediate_family_accuracy >= 0.78`
   - `reason_code_accuracy >= 0.75`
   - `all_field_exact_acceptance >= 0.65`
   - `invalid_combination_rate == 0.0`, `unsafe_selections == 0.0`,
     `unauthorized_mutations == 0.0`
2. A one-shot internal-holdout run (40 cases, `--confirm-holdout-once`)
   passes HOLDOUT_GATES (`task_class >= 0.82`, `specialist >= 0.75`,
   `all_field >= 0.55`, zero safety violations).
3. The legacy router's live numbers are known on the same split so the
   before/after delta is reported, not assumed.

Rationale for the thresholds: they are the frozen values already enforced by
`DEVELOPMENT_GATES`/`HOLDOUT_GATES` in `semantic_benchmark_v2.py`; the
highest bar (all-field ≥ 0.65) is what guards cross-field consistency, the
stated v0.11.1 bottleneck. Safety invariants are absolute (must be zero).
Until a live run meets these, the default stays `legacy` and v2 remains
opt-in via `--semantic-router v2` / `compare`.

## Failure cases to watch

The RC3.1 evidence (documented in `docs/routing.md`) shows the weak fields
on a real 7B model are reason code and all-field acceptance; those two gates
are expected to be the binding constraints, which is precisely the design
intent.
