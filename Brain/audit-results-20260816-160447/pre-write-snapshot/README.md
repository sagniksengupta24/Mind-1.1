# Mind1.1 v0.11.1 development candidate

Mind1.1 is a **local-first AI engineering-agent runtime** for repository work, coding, debugging, verification, semiconductor/VLSI assistance, mathematics, Indian-language technical learning, project memory, and documentation retrieval.

It is not a foundation model. It runs an Ollama-compatible local model by default and adds the engineering system around it: strict actions, routing, planning, controlled tools, deterministic verification, persistent sessions, provenance-aware project knowledge, receipts, rollback, traces, and evaluations. It can also run inference on a cloud, OpenAI-compatible provider such as OpenRouter instead of locally — see [docs/llm_providers.md](docs/llm_providers.md).

## v0.11.1 candidate status

The current branch adds an opt-in staged semantic router for a local 7B model:
two small constrained semantic decisions, deterministic policy/risk/tools/
lifecycle/reason resolution, compatibility matrices, explicit confidence
fallback, a cross-field solver, and complete field provenance. Exact action
selection remains constrained by the canonical JSON schema and validated again
by policy before dispatch.

This checkout is a **development candidate, not a verified v0.11.1 release**.
The frozen RC3.1 process completed all 120 cases with perfect schema
consistency and no parser failures, timeouts, unsafe selections, or unauthorized
mutations, but its aggregate semantic metrics missed the release thresholds;
the mechanical decision remains `HOLD`. v0.11.1 uses only those aggregate
metrics as historical motivation and makes no claim of improved RC3.1
performance. See [the routing design](docs/routing.md).

The legacy router remains the default. Use `--semantic-router v2` to opt in or
`--semantic-router compare` to shadow v2 while retaining legacy runtime
behavior.

The first retained 60-case development run exposed a general lifecycle defect: two existing-file proposals reached `propose_edit_file` without source text and failed strict required-argument validation. The candidate now requires exact-file inspection first. Both the original run and subsequent evidence are retained; frozen labels are not rewritten.

## v0.10.0 truthful-completion foundation

v0.10.0 makes completion status depend on a typed task contract and task-relevant evidence. Before mutation, the runtime records target and forbidden scope, expected artifacts and symbols, behavioral and regression requirements, required evidence types, rollback conditions, and completion criteria.

Each verification result declares its evidence type, mapped requirement IDs, state hash, proven properties, and explicitly unproven properties. Compilation proves syntax only. AST structure proves limited executable-source properties only. Import, symbol, signature, behavioral, regression, patch-review, and receipt-integrity evidence remain distinct.

`CompletionAuthority` is the single final-status decision point for the agent, correction controller, and real-mutation harness. A mutation is `verified` only when every mandatory requirement has current passing evidence, scope and receipts match, no mandatory check was skipped, no blocking finding remains, and no unauthorized mutation occurred. Failed post-write correction attempts are restored before another attempt.

The deterministic `truthful-completion-v1` suite contains 25 adversarial false-success cases plus positive mapping controls:

```bash
python -m mind01.eval run --suite truthful-completion
```

## v0.9.1 action protocol foundation

The v0.9.1 foundation established real local-model action reliability. The active model protocol is exactly one versioned JSON object per turn; XML, tagged text, Markdown-wrapped alternatives, and plain-prose fallback are not active runtime formats.

Tool call:

```json
{"schema_version":"1.0","response_type":"tool_call","tool":"read_file","arguments":{"path":"README.md"}}
```

Final response:

```json
{"schema_version":"1.0","response_type":"final","status":"unverified","summary":"Repository inspection is complete.","evidence_refs":[]}
```

Each turn has one runtime-selected mode:

- `ACTION_REQUIRED`: only a permitted tool call is valid.
- `FINAL_ALLOWED`: a permitted tool call or final response is valid.
- `REPAIR_REQUIRED`: only a compact correction of the preceding invalid object is valid.

The parser classifies failures as `NO_ACTION`, `MALFORMED_JSON`, `TRUNCATED_OUTPUT`, `UNKNOWN_TOOL`, `MISSING_ARGUMENT`, `WRONG_ARGUMENT_TYPE`, `EXTRA_ARGUMENT`, `MULTIPLE_ACTIONS`, `CONFLICTING_ACTIONS`, `PROSE_AROUND_ACTION`, mode mismatches, schema-version mismatch, oversize, repeated-invalid, unsafe-action, or internal-parser failures. Incident records contain hashes and redacted bounded excerpts, never unrestricted raw output.

The Ollama client detects JSON Schema support and uses a schema object when supported, otherwise it falls back to JSON mode. The parser and server policy still validate every response. Tools are exposed by current phase: inspection cannot see mutation tools, mutation requires an approved mutation route plus prior inspection, and verification tools appear only where route and server capabilities permit them.

Parser repair is limited to two compact attempts. Safe extraction can recover exactly one complete, fully valid JSON object from harmless surrounding structural noise; it records an incident and never guesses tools or arguments.

Live file mutation follows:

```text
snapshot/receipt -> mutation -> deterministic verification -> patch review
                 -> accept, compact repair, or receipt-backed rollback
```

Completion status is runtime-authoritative. A model request for `verified` is downgraded without a referenced passing evidence record, while blocking verification or patch review forces failure.

The versioned action benchmark contains 50 inspection, mutation, verification, recovery, and final-response cases. The real-mutation suite contains three fixtures that fail preconditions before execution: syntax repair, failing-test repair, and a hidden-acceptance small feature. Invalid Python is stored as `broken.py.fixture` and materialized only in the isolated workspace.

Local deterministic evidence for this checkout is documented by the test and evaluation commands below. A fresh real Ollama result must be generated before claiming the action-validity targets or coding success; mocked results are labeled separately.

## Execution lifecycle

The runtime now follows an explicit lifecycle:

```text
RECEIVE → CLASSIFY → PLAN → GATHER_CONTEXT → MODEL_CALL → PARSE
        → POLICY_CHECK → EXECUTE → OBSERVE → VERIFY/REVIEW → REPAIR_OR_FINISH
```

```text
Task
  ↓
Current phase
  ↓
Allowed tool subset
  ↓
Constrained model response
  ↓
Strict parser
  ├── Valid → policy → execute
  └── Invalid → classify → compact repair
                              ├── Valid → execute
                              └── Repeated failure → stop
```

The engineering foundation also includes:

- server-authoritative API privileges and trusted Ollama endpoint policy;
- real API conversation restoration with bounded context and summaries;
- hierarchical specialist routing and reusable skill selection;
- typed execution plans for non-trivial or mutating work;
- pluggable deterministic verification with structured evidence;
- bounded typed parser repair, duplicate-action detection, repeated-error detection, and no-progress termination;
- concurrency-safe receipt and trace hash-chain updates;
- SQLite WAL and busy timeouts for runtime stores;
- provenance-aware project knowledge for files, symbols, modules, imports, and definitions;
- evaluation metadata, verification requirements, and false-success tracking;
- one centralized package version and clean-release tooling.

Benchmark-specific canned answers and exact benchmark prompt classifiers are not used by the runtime.

## Reality check

On a 16 GB MacBook Air, use a compact local model such as `qwen2.5-coder:7b`. The runtime can make a small model more reliable and auditable, but orchestration cannot turn it into a frontier model. Quality remains dependent on the selected model, repository, available verification tools, and task difficulty.

## Requirements

- Python 3.10 or newer; Python 3.11+ recommended
- Ollama for live model calls
- No mandatory cloud service
- Optional local compilers, test runners, linters, Verilog tools, or Docker for additional verification/isolation

```bash
brew install ollama
ollama serve
ollama pull qwen2.5-coder:7b
```

Optional documentation embeddings:

```bash
ollama pull nomic-embed-text
```

## Quick start

```bash
python3 -m mind01.cli doctor
python3 -m mind01.cli ask "Inspect this repository and summarize its architecture" --workspace .
python3 scripts/run_checks.py
```

Dry-run evaluation without a model call:

```bash
python3 -m mind01.cli eval evals/basic.json --dry-run --workspace .
```

## Operating modes

The default is `read-only`.

- `read-only`: inspection, search, retrieval, status, and safe answers only.
- `propose`: permits indexes, project-knowledge refresh, and patch proposals; direct source mutation remains blocked.
- `write-approved`: source mutation requires server/CLI write capability and explicit approval.
- `unsafe`: enables the maximum configured capability but does not bypass schemas, workspace boundaries, command policy, or verification reporting.

Examples:

```bash
python3 -m mind01.cli index-code --workspace . --mode propose
python3 -m mind01.cli ask "Fix the failing parser test" \
  --workspace . --mode write-approved --allow-write --yes
python3 -m mind01.cli ask "Run the targeted tests" \
  --workspace . --mode write-approved --allow-shell --yes
```

### Write tasks and self-verification (shell policy)

`--allow-write` and `--allow-shell` are independent privileges:

- `--allow-write` grants mutation (`edit_file`, `write_file`). The agent can
  apply edits without shell access.
- `--allow-shell` grants execution (`run_command`, `test_patch`) from the
  allowlist of `python3`, `pytest`, `ruff`, `mypy`, and read-only `git`
  subcommands, with sanitized environment and bounded output.

**Self-verification of a write task requires `--allow-shell`.** Every mutation
route carries a verification strategy (e.g. `python syntax`, `targeted tests`)
and a `verify` plan step that runs through `run_command`; `CompletionAuthority`
marks a mutation `verified` only when every mandatory requirement has current,
passing, task-relevant evidence — evidence that only command execution can
produce. Without `--allow-shell`:

- the `verify` step has no executable tool (`run_command` and `test_patch` are
  hidden and raise `ToolError` if called), and
- the task completes with status `unverified` (or `failed` if the model claims
  `verified` without evidence), never `verified`.

The agent must therefore never claim `verified` for a write task run without
`--allow-shell`; the runtime will not accept it. Granting `--allow-shell` is a
meaningful privilege: allowlisted commands run repository code on the host (see
`SECURITY.md`). For unsupervised write runs, use `--allow-write` alone when
edit-only results are acceptable, and add `--allow-shell` only when the
operator wants the agent to run checks and can accept host command execution.

## Intelligence architecture

### Typed hierarchical routing

The v0.11.1 router produces a strict `SemanticRouteState` and adapts it to the
stable `RoutingDecision` runtime contract. Model call 1 selects task class.
Policy and risk are then resolved deterministically, and a compatibility matrix
reduces the specialist/family candidates for model call 2. Tools, first
lifecycle step, reason code, and final consistency are deterministic. Routes
carry a capability fingerprint and fail closed when reused under a different
mode or authority. Current specialist categories include:

- general reasoning;
- repository understanding;
- code modification and debugging;
- testing and verification;
- docs/RAG and memory retrieval;
- mathematics;
- Python, C/C++, and Verilog verification;
- security review.

Routing uses deterministic capability/file signals where reliable and conservative general fallback elsewhere. Confidence is diagnostic, never authorization. Blocking ambiguity is clarified; repository-resolvable ambiguity is inspected. Proposal and apply tools are distinct, and existing-file proposals require inspection before their proposal schema becomes visible. It does not use hardcoded benchmark answers.

### Typed planning

Non-trivial and mutation tasks receive an execution plan containing objective, assumptions, constraints, steps, likely files, tools, risk, verification requirements, and completion criteria. Plans are execution metadata—not unrestricted chain-of-thought.

### Reusable skills

Skills define trigger conditions, tool permissions, procedure, verification requirements, failure conditions, and output expectations. Initial skills cover repository analysis, safe editing, debugging, feature work, refactoring, tests, Python verification, API security, Verilog verification, and documentation retrieval.

### Deterministic verification

The verification engine reports structured evidence rather than a vague “looks correct.” Available adapters include:

- Python compilation and repository tests;
- JSON parsing;
- C/C++ compiler syntax checks;
- Verilog syntax/simulation when Icarus Verilog is installed;
- JavaScript/TypeScript project-script discovery and checks when available.

A change is not reported as verified unless a relevant check actually passes. Missing tools are reported as unavailable or unverified.

## API security model

Start a default loopback, read-only API:

```bash
MIND_API_TOKEN=dev-token python3 -m mind01.cli serve-api \
  --workspace . --host 127.0.0.1 --port 8765 \
  --cors-origin http://localhost:3000
```

An elevated API must be explicitly configured by the server operator:

```bash
MIND_API_TOKEN=dev-token python3 -m mind01.cli serve-api \
  --workspace . --mode write-approved --allow-write --auto-approve
```

Security invariants:

- clients may request less privilege, never more than the server maximum;
- clients cannot choose an arbitrary model or Ollama URL;
- non-loopback binding requires a token;
- elevated capabilities require a token;
- request size, prompt size, step count, and concurrency are bounded;
- mutation routes require server-enabled mode, write capability, and approval policy;
- internal exceptions are not returned verbatim as 500 responses.

See `docs/api.md`, `SECURITY.md`, and `THREAT_MODEL.md`. A capability audit of the OpenRouter integration — raw test traces, router defects found and fixed, and the shell-policy decision — is recorded in [docs/capability_audit_openrouter_20260816.md](docs/capability_audit_openrouter_20260816.md).

## Persistent sessions

`session_id` now restores actual prior conversation messages before an API model call. The session store:

- keeps recent turns;
- deterministically summarizes omitted older turns;
- bounds stored content and trace size;
- separates sessions;
- uses SQLite WAL and a busy timeout.

Conversation history, long-term memory, documentation retrieval, project knowledge, and temporary tool observations remain separate sources.

## Project knowledge

Project knowledge is a lightweight SQLite graph with provenance and source hashes. It currently represents files, symbols, modules, `defines`, and `imports` relationships and invalidates source-derived facts when files change.

Inside the agent, use `refresh_knowledge` and `query_knowledge`. From the CLI:

```bash
python3 -m mind01.cli knowledge refresh --workspace . --mode propose
python3 -m mind01.cli knowledge query Agent --workspace .
python3 -m mind01.cli knowledge status --workspace .
```

Through the API:

```text
GET  /knowledge
GET  /knowledge?q=Agent&limit=20
POST /knowledge/refresh   {"path":".", "mode":"propose"}
```

## File and execution safety

File safety blocks workspace traversal, symlink escape, runtime-state access, unsafe writes, binary reads, and oversized reads.

Command execution uses argument arrays with `shell=False`, allowlisted executables, metacharacter checks, a sanitized environment, controlled working/runtime directories, timeout handling, output limits, and process-group termination where supported.

**Host execution is not a sandbox.** Repository-controlled code can still be dangerous. An optional external container/process isolation layer should be used for untrusted projects.

## Receipts, rollback, and traces

Successful mutations create verified receipts and backups under `.mind01/receipts/`. Tool and agent events are stored under `.mind01/traces/`.

Receipt and trace chain-head updates are protected by process/thread locks and atomic replacement. Chain verification traverses hashes from the current head and detects broken, disconnected, cyclic, or forked records.

```bash
python3 -m mind01.cli receipts --workspace . list
python3 -m mind01.cli traces --workspace . list
python3 -m mind01.cli rollback <receipt_id> \
  --workspace . --mode write-approved --yes
```

## Documentation, memory, and code indexes

```bash
python3 -m mind01.cli index-docs docs --workspace . --mode propose
python3 -m mind01.cli search-docs clock --workspace .
python3 -m mind01.cli index-code --workspace . --mode propose
python3 -m mind01.cli memory --workspace . list
```

Documentation hits carry line citations. Long-term memory is tagged and ranked. Secret-looking values are redacted according to the implemented patterns, but redaction should not be treated as perfect data-loss prevention.

## Evaluation

Evaluation runs record:

- Mind1.1 version and Git commit when available;
- dataset version, model, mode, max steps, Python, and platform;
- success rate, parser failure rate, verification pass rate, false-success count, retries, steps, and duration;
- per-task verification evidence.

Tasks may set `requires_verification: true`. A textually correct-looking answer without passed deterministic evidence then counts as a false success and fails.

Validate all versioned assets and run the explicitly mocked protocol regression:

```bash
python -m mind01.eval validate
python -m mind01.eval run --suite regression --mock-model
python -m mind01.eval run --suite semantic-routing --partition development
```

Run real-model evaluations separately:

```bash
python -m mind01.eval action-benchmark --model qwen2.5-coder:7b
python -m mind01.eval smoke --suite real-mutation --model qwen2.5-coder:7b
python -m mind01.eval parser-report evaluation_results/<action-run>
python -m mind01.eval semantic-live \
  --partition development \
  --model qwen2.5-coder:7b \
  --seed 1101 \
  --output evaluation_results/v0.11.0-release/development_runs/run-001.json
python -m mind01.eval semantic-v2-live \
  --partition lifecycle \
  --seed 11101 \
  --output evaluation_results/v0.11.0-rc2/visible_runs/run_1/lifecycle.json
python -m mind01.eval end-to-end-live \
  --seed 11101 \
  --output evaluation_results/v0.11.0-rc2/end_to_end_runs/run_1.json
python -m mind01.eval rc2-complete-live \
  --run-name run_1 --seed 11101 \
  --external-blind-labels /read-only/mount/labels.json \
  --output-root evaluation_results/v0.11.0-rc2
```

Semantic routing v2 separates the user goal, immediate next action, eventual terminal family, required/alternative lifecycle, forbidden actions, and completion response. Existing-file proposal and write requests expose inspection first. The v2 corpus adds lifecycle and disposable end-to-end fixture partitions while preserving every v1 byte as historical evidence; its migration report documents all 200 v1 cases and independently reviews the 16 contradictory mutation-intent labels.

Semantic live reports require the exact `qwen2.5-coder:7b` model and retain its digest, Ollama client/daemon identity, JSON Schema capability, context size, seed, temperature, timeouts, raw output hashes/content, parser incidents, route fields, exposed tools, and exact model choices. `semantic-v2-live` measures immediate selection only. `end-to-end-live` separately dispatches selected safe actions in temporary fixture copies, records lifecycle transitions, verifies writes, and rolls back failed verification. Structural validity, deterministic routing, model choice, authorized dispatch, execution, rollback, and truthful completion remain separate metrics.

For release evidence, `rc2-complete-live` runs all required visible, blind, end-to-end, and truthful-completion components as one fail-closed invocation. It requires a clean frozen source commit and a no-write-bit external label package, then rechecks commit, seed, exact model digest, and JSON Schema output mode before completing its manifest.

The current ordinary task files are legacy unsplit assets. The action, truthful-completion, and semantic-routing suites are versioned regression assets. Semantic routing v2 stores only blind inputs, their hash, and an evaluator contract in the repository. A no-tools evaluator process receives only the public behavior/tool taxonomy; readable labels and independent fixtures remain outside the repository and are mounted read-only only after the source candidate is frozen. Blind reports retain label identity and checks without copying expected labels into packaged artifacts.

## Validation and release

Canonical checks:

```bash
python3 -m pytest -q
python3 -m compileall -q mind01 tests
python3 scripts/run_checks.py
python3 -m pip wheel . --no-deps --wheel-dir dist
```

Create a clean source ZIP without runtime databases, traces, receipts, caches, historical outputs, or secrets:

```bash
python3 scripts/build_release.py --output-dir dist
```

## Runtime storage

All runtime state lives under `.mind01/`, including sessions, memory, docs, code index, project knowledge, traces, receipts, patches, dirty-state records, and evaluation runs. This directory is excluded from clean releases.

## Known limitations

- Not a foundation model and not guaranteed to solve arbitrary tasks.
- Not a production multi-tenant platform.
- No complete RBAC, rate-limiting service, distributed lock, signed remote audit log, or hardened container sandbox.
- Host-executed tools can run repository-controlled code.
- Verification quality depends on installed compilers and test tools.
- The project-knowledge graph is intentionally small, not a semantic code intelligence platform.
- Local redaction patterns may miss uncommon secrets.
- Live-model quality must be measured with blind holdouts; dry-run tests prove runtime behavior, not intelligence.
- The v0.11 release gate is blocked until external blind labels and three complete independent live runs exist; this candidate must not be marketed as verified.
- Frozen synthetic proposal labels describe the eventual proposal tool, while the safer runtime may first require `read_file`; label-relative exposure metrics retain that mismatch.
