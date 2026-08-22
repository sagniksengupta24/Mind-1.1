# Changelog

## 0.11.1.dev0 — Staged semantic routing reliability

- Added an opt-in two-call semantic router with deterministic normalization,
  policy/risk resolution, candidate reduction, tool intersection, lifecycle,
  reason codes, confidence fallback, and a cross-field solver.
- Added complete field-level decision provenance and per-route model-call,
  latency, retry, abstention, fallback, violation, and repair records.
- Preserved the legacy router and stable runtime contract behind
  `--semantic-router legacy|v2|compare`.
- Added a fresh 240-case examples/development/internal-holdout suite with
  deterministic identities, hashes, provenance, duplicate checks, and frozen
  benchmark contamination guards.
- Added deterministic/live evaluation, checkpoint/resume, field metrics,
  confusion matrices, one-shot holdout control, and four-way ablation.
- Kept the candidate in development status. No release tag or release-readiness
  claim is authorized.

## 0.11.0.dev0 — Semantic Routing Reliability candidate

- Added strict `NormalizedIntent` and `RoutingDecision` schemas with bounded fields, finite enums/reason codes, reproducible identities, typed incidents, and stale-capability rejection.
- Split routing into task, risk/capability, specialist, tool-family, and exact-tool stages.
- Centralized phase/mode/capability/prior-inspection filtering in one tool-exposure authority.
- Required existing-file proposals to inspect exact source before exposing the bounded replacement proposal schema.
- Added frozen development, regression, adversarial, capability/mode, ambiguity, and unlabeled blind-input partitions with hash validation.
- Added deterministic semantic metrics and a bounded real-Ollama harness retaining raw per-case outputs and model identity.
- Preserved the initial failed development run instead of rewriting labels or weakening the parser.
- The release gate remains failed/blocked until an independent blind evaluator and three complete retained live runs satisfy every mandatory threshold.

## 0.10.0 — Truthful Completion and Reproducible Evidence

- Added typed pre-mutation task and acceptance contracts.
- Added a normalized evidence taxonomy that records proven and unproven properties.
- Consolidated final status decisions under one `CompletionAuthority` used by the agent, correction controller, and real-mutation harness.
- Prevented compilation, AST structure, importability, symbol lookup, or regression-only evidence from satisfying behavioral requirements.
- Added executable symbol and signature verification for Python tasks.
- Added current-state, receipt-integrity, scope, skipped-check, unauthorized-mutation, and stale-evidence enforcement.
- Made failed post-write self-correction attempts restore their pre-attempt snapshots.
- Added a versioned 25-case adversarial false-success suite plus positive evidence-mapping controls.
- Added the mandatory current-state audit, pre-transformation baseline, and risk-ranked release backlog.

## 0.9.1 — Real Action Reliability

- Replaced active XML/tagged/prose alternatives with one canonical versioned JSON protocol.
- Added explicit action, final-allowed, and repair response modes.
- Added typed, redacted parser incidents, safe single-object extraction, and two-attempt repair.
- Added phase-scoped tool schemas backed by runtime validation definitions.
- Added Ollama JSON Schema capability detection with a safe JSON fallback.
- Made completion status runtime-authoritative and evidence-referenced.
- Connected mutation receipts to deterministic verification, patch review, and rollback.
- Added a versioned 50-case real action benchmark and parser report.
- Added three precondition-failing isolated real-mutation fixtures.
- Added `python -m mind01.eval` validation, mock regression, action, smoke, and parser-report commands.
- Added `mind01 --version` and synchronized package/API/report versioning.

## 0.8.0 — Research-grade architecture upgrade

- Replaced benchmark-specific answer repairs with generic bounded recovery.
- Added explicit agent phases and typed execution plans.
- Added hierarchical specialist routing and reusable skill registry.
- Added deterministic verification evidence for Python, JSON, C/C++, and HDL.
- Made API privileges, model, Ollama URL, limits, and approvals server-authoritative.
- Restored bounded conversation context for API sessions.
- Enabled SQLite WAL and busy timeouts for runtime stores.
- Added locked, concurrency-safe trace and receipt chain updates.
- Added provenance-aware project knowledge entities and relations.
- Hardened host command environment and documented that it is not a sandbox.
- Added security, session, concurrency, routing, verification, release, and graph tests.
- Centralized version at 0.8.0 and added evaluation metadata/false-success tracking.
