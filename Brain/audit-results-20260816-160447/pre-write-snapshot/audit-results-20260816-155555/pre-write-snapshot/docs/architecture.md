# Mind1.1 Architecture — v0.11 development candidate

Mind1.1 is a local-first, Ollama-backed AI engineering runtime. The model proposes actions; deterministic code owns permissions, routing, retry budgets, persistence, audit integrity, and verification.

It is not a foundation model and it is not a production multi-user service.

## Execution lifecycle

```text
RECEIVE
  -> NORMALIZE_INTENT (strict typed request)
  -> CLASSIFY (task class)
  -> RESOLVE_RISK_AND_CAPABILITIES
  -> SELECT_SPECIALIST
  -> SELECT_TOOL_FAMILY
  -> PLAN (typed ExecutionPlan)
  -> GATHER_CONTEXT
  -> SCOPE_TOOLS
  -> MODEL_CALL (JSON Schema when supported; JSON fallback)
  -> PARSE (canonical versioned JSON schema)
  -> POLICY_CHECK
  -> EXECUTE (ToolRegistry)
  -> OBSERVE
  -> VERIFY (file-type adapters)
  -> PATCH_REVIEW
  -> REPAIR_ROLLBACK_OR_FINISH
```

`AgentState` records the objective, typed route, normalized intent, phase, specialist, visible tools, plan, observations, tool results, verification evidence, remaining budget, repeated actions, repeated errors, and completion status. `RecoveryController` owns bounded parser repair, duplicate-action detection, and repeated-tool-error handling.

Before any mutation, `task_contract.py` creates a conservative typed acceptance contract. `completion.py` is the only authority that may convert model intent and runtime evidence into `verified`, `partially_verified`, `unverified`, `failed`, `blocked`, `policy_denied`, or `rolled_back` status. The agent exposes the resulting completion contract through the API.

## Canonical response protocol

Only schema version `1.0` JSON objects are active. Tool calls contain `schema_version`, `response_type=tool_call`, `tool`, and `arguments`. Finals contain `schema_version`, `response_type=final`, `status`, `summary`, and `evidence_refs`. Unknown fields, hidden tools, invalid arguments, multiple objects, contradictory fields, and response-mode mismatches are rejected.

`ACTION_REQUIRED`, `FINAL_ALLOWED`, and `REPAIR_REQUIRED` make the expected response explicit. Parser incidents use a typed taxonomy, a SHA-256 raw-output identifier, a redacted bounded excerpt, phase, visible tools, expected schema, repair index, and model metadata.

The model sees only phase-scoped tools. Tool descriptions and argument types come from the same `ToolSchema` objects used for runtime validation. Server mode and capability checks remain authoritative after parsing.

Ollama capability detection selects JSON Schema constraints on supported versions and JSON mode otherwise. A schema rejection falls back once to JSON mode; it never falls back to unconstrained prose.

## Mutation correction

Each source mutation creates a receipt and backup, then runs a file-type verifier and high-signal patch review. Blocking verification or review triggers receipt-backed rollback. Repeated identical actions and repeated failures stop within bounded budgets. Real-mutation fixtures must fail acceptance before agent execution, and intentionally invalid Python templates use a non-`.py` suffix until copied into an isolated workspace.

Completion status is derived from runtime evidence. `verified` requires a referenced passing evidence record, and blocking failures or review findings override model claims.

## Intelligence layers

### Hierarchical routing

`intent.py` and `routing.py` implement a strict normalized request and five distinct decisions: task class, risk/capabilities, specialist, tool family, and exact-tool candidates. Finite enums and reason codes reject cosmetic or unknown routes. The route records deterministic/model signals and a capability fingerprint; stale reuse under different authority fails closed. Planning requirements and mutation intent are represented separately, so repository analysis does not grant editing tools.

`tool_exposure.py` is the sole policy-aware route-to-model-schema authority. It filters by phase, mode, capability, prior inspection, target/mutation state, and canonical side-effect metadata. Existing-file proposals expose only `read_file` until inspection succeeds; proposal and live apply are never exposed together. Routing does not return domain answers or completion claims.

See `docs/routing.md` for the schemas, ambiguity behavior, lifecycle rules, and evaluation boundaries.

### Structured planning

`planning.py` creates a typed plan with objective, assumptions, constraints, ordered steps, likely files, permitted tools, verification, risk, and completion criteria. Mutation and repository-grounded tasks must inspect evidence before a final answer.

### Reusable skills

`skills.py` contains modular procedures for repository analysis, safe editing, debugging, Python verification, API security review, Verilog verification, and documentation retrieval. Skills constrain behavior; they are not exact-prompt answer templates.

### Project knowledge

`project_knowledge.py` maintains a small provenance-aware SQLite graph of files, symbols, modules, and `defines`/`imports` relationships. Every extracted fact carries a source path, line provenance when available, and a source hash. Refreshing a changed file replaces stale derived entities.

## Tool and policy boundary

`ToolRegistry` validates every action against one canonical schema before dispatch. Mode and capability checks are deterministic:

- `read-only`: inspection only
- `propose`: inspection plus runtime indexes and patch proposals
- `write-approved`: explicit source writes and host commands only when separately enabled
- `unsafe`: elevated mode, but still subject to schemas, workspace safety, and command restrictions

Host command execution is **not a sandbox**. It uses `shell=False`, an allowlist, a sanitized environment, a controlled working directory, time/output limits, and a new process session. Python scripts and tests can still execute repository-controlled code.

## API trust boundary

`ServerPolicy` is authoritative. A request may reduce privilege, but cannot increase it.

The server controls:

- maximum mode
- write and shell capability
- non-interactive mutation approval
- model and Ollama endpoint
- maximum steps
- body size
- request concurrency

Ollama URLs are restricted to configured loopback hosts and ports. Elevated API capability requires an API token. Binding beyond loopback without a token is rejected. Internal exceptions are not returned to clients.

## Sessions and context

`SessionStore` uses SQLite WAL mode and per-operation connections. The API restores bounded prior messages before each model call. Recent turns are retained; older turns are deterministically compressed. Conversation history, long-term memory, project knowledge, docs retrieval, and temporary observations remain separate stores.

## Deterministic verification

`VerificationEngine` selects adapters from changed paths:

- Python: `compileall`, with project pytest support
- JSON: parse validation
- C/C++: compiler syntax and warnings when available
- Verilog/SystemVerilog: Icarus syntax when available
- JavaScript/TypeScript: project test hook when requested and available

Every result records check, status, duration, output summary, failure category, confidence, and whether it blocks completion. The agent must label unavailable verification honestly.

Every result also records an evidence type, mapped requirement IDs, post-mutation state identity, proven properties, and unproven properties. Syntax and structure evidence cannot satisfy behavioral requirements. Python verification can separately check executable top-level symbols, requested signatures, and importability; project regression tests require authorized host execution.

## Audit and mutation integrity

Receipts and traces are hash chained. Cross-thread and POSIX cross-process file locks protect head-read, record-write, and head-update sequences. Head files are atomically replaced. Receipt-chain verification follows hashes rather than filename ordering, so concurrent writers cannot invalidate the chain merely by completing out of lexical order.

SQLite stores use WAL and busy timeouts for safer concurrent access.

## Runtime storage

```text
.mind01/
  code_index.sqlite3
  docs.sqlite3
  memory.sqlite3
  project_knowledge.sqlite3
  sessions.sqlite3
  patches.json
  receipts/
  traces/
  eval_runs/
  runtime-home/
  tmp/
```

Runtime files are excluded from release artifacts and blocked from ordinary source-file tools.

## Remaining production gaps

- Host execution is controlled but not container-isolated.
- Authentication is a single local token, not multi-user RBAC.
- Audit chains are tamper-evident, not cryptographically signed by an external key.
- No distributed locking or multi-process job scheduler.
- Local-model quality remains dependent on the selected Ollama model.
- Verification adapters are intentionally small and do not yet cover every build system.
- Semantic routing is not release-verified without externally controlled blind labels and three complete retained live runs.
