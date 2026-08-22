# Semantic routing design — v0.11.1 development

Semantic routing v2 is a staged, typed control layer between a request and the
runtime's exact action selection. It does not grant permissions and it does not
claim task completion.

```text
bounded normalization
  -> task-class model decision
  -> deterministic response mode, policy, constraints, and risk
  -> task-compatible specialist shortlist
  -> specialist + immediate-family model decision
  -> deterministic tool intersection
  -> deterministic first lifecycle step
  -> deterministic reason code
  -> cross-field solver
  -> confidence fallback or final typed route
```

Normal routing makes at most two semantic model calls. One bounded repair is
available across the complete route, so an exceptional route makes at most
three calls. Deterministic fields make no model call. The local model never
selects tools, lifecycle, reason code, risk, constraints, or permissions.

## Why v2 exists

The frozen RC3.1 process completed all 120 cases with perfect schema
consistency, no parser failures, no timeouts, and no unsafe or unauthorized
selection. Its aggregate semantic metrics remained weak, including 70% task
class, 53.33% specialist, 49.17% immediate family, 26.67% reason code, and 5%
all-field acceptance. The mechanical result was `HOLD`.

That evidence indicates semantic coupling and cross-field consistency—not
structural parsing—are the current bottlenecks. These aggregate results are
historical motivation only. v2 was not tuned against individual RC3.1 prompts,
labels, routes, outputs, failures, identifiers, or evaluator explanations, and
no improvement on RC3.1 is claimed.

## Typed state and decision trace

`SemanticRouteState` records:

- request identity and bounded normalized features;
- task class, response mode, risk, hard constraints, specialist, and immediate
  family;
- immediate allowed tools and terminal tools;
- first lifecycle step and canonical reason code;
- confidence, abstention, and fallback reason;
- schema/router/model identity and per-route call/latency/retry statistics;
- compatibility-solver validity, violations, and safe repairs;
- a field-level decision trace.

Every trace entry names one of `model`, `deterministic_rule`,
`policy_engine`, `compatibility_matrix`, `fallback`, or `default`. Trace inputs
contain bounded features and public taxonomy values, never system prompts,
secrets, or hidden evaluation labels.

## Model stages

Call 1 sees only the six task classes with contrasting definitions and boundary
rules. It returns a schema-versioned class, confidence, at most two
alternatives, and a short evidence summary.

Deterministic response/policy resolution then reduces the specialist set to at
most five choices. Call 2 sees only those specialists and their compatible
families. Every family has a short purpose, a positive boundary, a contrast,
and an allowed lifecycle. The model cannot invent taxonomy values because both
calls use closed JSON Schemas and strict duplicate-aware parsing.

The CI classifier implements the same protocol without Ollama. It is intended
for deterministic integration and invariant tests, not as evidence of local
model quality.

## Policy and hard constraints

Constraints are typed records with identifier, trigger, source, severity,
effect, and override policy. Current deterministic signals cover read-only
operation, absent live-write or shell authority, explicit no-tool/no-edit
requests, offline operation, protected and out-of-workspace paths, destructive
operations, requested verification, explanation-only intent, and missing
mutation context.

Response mode is resolved before tools:

- final answer exposes no tools and begins with `answer`;
- clarification exposes no tools and begins with `clarification`;
- blocked/refusal exposes no tools and begins with `refusal`;
- action routes proceed to the compatibility and permission stages;
- mutation without applicable authority fails closed;
- missing essential mutation context asks instead of guessing.

Risk is policy-derived. Model output cannot lower it.

## Compatibility and candidate reduction

Two complete matrices define `task class -> specialists` and
`(task class, specialist) -> immediate families`. They retain the existing
public enums and reject orphan or cross-hierarchy values. Repository context,
language, security intent, requested artifact, and response mode may reorder or
remove candidates but never add a matrix-incompatible value. Low confidence,
schema failure, timeout, or incompatible output selects a recorded safe
fallback; it never selects the first enum implicitly and never expands tools.

## Tool intersection and lifecycle

Terminal tool permission is the intersection, in this precedence order:

```text
task capability
∩ mode/policy permission
∩ response-mode permission
∩ specialist capability
∩ family capability
∩ explicit user authorization
```

Unknown tools are absent from every trusted set and therefore fail closed. The
trace records every input set and which set removed each tool. First-step tools
are then narrowed again by lifecycle: existing-file edits and proposals expose
inspection before mutation/proposal, repository understanding starts with
inspection, verification uses verification tools, and terminal modes expose
none. Existing `ToolExposureAuthority` and `ToolRegistry` remain authoritative
downstream checks.

## Reason codes and consistency

The model does not classify the flat reason-code enum. A deterministic mapping
derives exactly one existing `ReasonCode` from the resolved response, task,
family, lifecycle, normalized artifact, and constraints. No public enum was
removed.

The final solver detects terminal responses with tools, read-only mutation,
specialist/family incompatibility, response/lifecycle conflict, missing
tool-dependent lifecycle capability, and reason mismatch. It applies only
listed safe repairs (clear terminal tools, remove unauthorized tools, align a
terminal lifecycle, rederive the reason, or fail closed). Unrelated fields are
never replaced with a generic route.

## Activation and rollback

The default remains the legacy router until live development and one-shot
internal-holdout evidence passes:

```bash
mind01 ask --semantic-router legacy ...
mind01 ask --semantic-router v2 ...
mind01 ask --semantic-router compare ...
```

`compare` runs v2 as a shadow, records field disagreements, and returns the
legacy route to the runtime. Normal `legacy` and `v2` modes execute only the
selected router. Rollback is the configuration-only switch back to `legacy`;
the old router and `RoutingDecision` contract remain intact.

## Fresh evaluation and blind-data separation

The new suite contains 240 independently authored cases: 100 examples, 100
development cases, and a 40-case internal holdout. Each case records provenance,
stable identity/hash, all route labels, difficulty, ambiguity, and split. The
validator checks hashes, split counts, duplicates, high-similarity pairs, and
forbidden frozen-data markers.

Development and holdout are separate files. Ordinary validation cannot parse
the holdout. Its runner requires an explicit one-shot confirmation and records
the access. This internal holdout is not a release benchmark.

```bash
python3 scripts/evaluate_semantic_router.py \
  --router v2 \
  --split development \
  --model qwen2.5-coder:7b \
  --seed 11103 \
  --output-dir evaluation_results/v0.11.1-dev
```

Add `--live` for Ollama. CI never requires Ollama. A future release still
requires a newly and independently authored sealed benchmark.

## Known limitations

A 7B model can still confuse mixed intent and close taxonomy boundaries.
Development templates cannot represent all real repository language. The
benchmark evaluates route decisions, not successful tool execution or the full
agent lifecycle. The internal holdout is small and shares the authoring
framework. No new sealed release benchmark has been run.
