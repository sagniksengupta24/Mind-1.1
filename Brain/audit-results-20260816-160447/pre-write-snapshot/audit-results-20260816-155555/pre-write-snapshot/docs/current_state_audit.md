# Mind1.1 pre-transformation audit

Audit timestamp: `2026-07-15T22:38:22Z`

This document records the v0.9.1 checkout before the production-grade transformation directive was implemented. It separates directly observed source and deterministic results from historical or unavailable live-model evidence.

## Repository identity and provenance

- Working directory: `/home/mind/Desktop/Archive/Brain`
- Declared package version: `0.9.1`
- Git top level: unavailable; this directory and its parents are not a Git repository.
- Branches, tags, commits, and tree hashes: unavailable.
- Existing evaluation reports record `git_commit: null`.
- The checkout therefore has no immutable association between source, packages, and reported metrics.

## Deterministic baseline

Commands were run with the already installed `.venv-linux` environment before architectural edits:

| Command | Exit | Result |
|---|---:|---|
| `.venv-linux/bin/python -m pytest -q` | 0 | `71 passed in 2.65s` |
| `.venv-linux/bin/python -m compileall -q mind01 tests scripts` | 0 | passed |
| `.venv-linux/bin/python -m mind01.eval validate` | 0 | 20 ordinary tasks; 50 action cases |
| `.venv-linux/bin/python -m mind01.eval run --suite regression --mock-model` | 0 | 25/25; `metrics_source=mock_model` |
| `.venv-linux/bin/python scripts/run_checks.py` | 0 | tests, compileall, asset validation, mock regression, dry-run and package checks passed |

The mock and dry-run results prove harness behavior only. They are not evidence of model intelligence or live coding ability.

## Environment

- Python: `3.14.4`
- Platform: `Linux-7.0.0-27-generic-x86_64-with-glibc2.43`
- Ollama client: `0.32.0`; the daemon was not reachable from the restricted execution environment.
- Docker: not found.
- Icarus Verilog, Verilator, Yosys, SymbiYosys, and Z3: not found.
- Action suite SHA-256: `468281e4aabfe2ee460c98df0dade69ef88548a563ca830a899f130a4b1413f5`
- System prompt SHA-256: `df00449f8f55fe0b06ec4f79af0db86be57335138ca30a4f6373bfde8bb32a36`
- Tool schema SHA-256: `60122985311e517b13d7cffc8a42e25ed04eb7f41411f5cf468e8c450dbd752c`
- Preserved wheel SHA-256: `1ba7cec908f2f90072e9b0f9d021dc6a4f21b498a8f30afd68f229c3ea9d82f7`

## Current runtime inventory

The runtime is a local-first Ollama-backed engineering-agent control plane, not a foundation model.

- Model protocol: one schema-version `1.0` JSON object.
- Response modes: `ACTION_REQUIRED`, `FINAL_ALLOWED`, `REPAIR_REQUIRED`.
- Operating modes: `read-only`, `propose`, `write-approved`, `unsafe`.
- Registered tools: 23 inspection, memory, knowledge, proposal, mutation, patch, and command tools.
- Parser: typed failures, bounded excerpts and hashes, strict arguments, hidden-tool rejection, size/depth limits, and at most two repairs.
- Tool exposure: route-, phase-, mode-, write-capability-, and shell-capability-scoped.
- Persistence: SQLite stores, receipts, backups, traces, hash chains, and local locks.
- Verification: JSON parsing, Python executable-structure and compilation, optional project pytest, C/C++ syntax, HDL syntax when available, and an optional JavaScript test hook.
- Mutation safety: transactional replace, hash/size validation, receipts, patch review, and rollback on blocking verification/review.

## Evidence and evaluation inventory

- Ordinary evaluations: 20 tasks across ten JSON files. They are not consistently schema-versioned and have no declared development/regression/blind split.
- Action evaluation: one versioned 50-case suite with five categories.
- Real mutation evaluation: three isolated precondition-failing fixtures.
- Preserved deterministic reports: v0.9.0 baseline and v0.9.1 deterministic verification.
- Retained live action reports: none.
- Retained live mutation reports: none.
- Historical claims of 100% structural validity, 62% tool-family match, and 2/3 mutation success are not independently auditable from this checkout.

## Risk-ranked findings

### Critical

1. **Completion can overstate proof.** `Agent._runtime_completion_status` can promote a mutation to `verified` when any verification passes, including syntax-only checks, without satisfying a task-level acceptance contract.
2. **No source/report provenance.** There is no Git history and all retained reports lack commit identity.
3. **Host execution is not isolated.** Python, pytest, compilers, and build tools can execute repository-controlled code on the host.

### High

1. `Agent`, `completion.py`, and `SelfCorrectionController` implement overlapping lifecycle and status decisions.
2. Verification results do not state precisely which requirement they prove or what they leave unproven.
3. Task requirements are not captured in a typed pre-mutation acceptance contract.
4. Stale or pre-mutation evidence is not structurally rejected by the completion path.
5. Live action and mutation reports referenced by handoff claims are absent.

### Medium

1. Ordinary evaluation files lack a validated versioned schema and true blind split.
2. Semantic tool-family selection is historically reported at only 62%.
3. The real coding suite has only three fixtures.
4. `evals/README.md` references missing files and absolute paths from another machine.
5. API response documentation omits several current response fields.
6. Bytecode and historical build artifacts are present in the working directory, although release tooling excludes them.

### Release blockers

- No Git commit/tree identity.
- No retained real-model evidence.
- No sandbox runtime.
- No open-source redistribution license.
- No signed release manifest or externally anchored audit evidence.

## v0.10 implementation boundary

The first coherent release will address truthful completion and reproducible deterministic evidence only:

1. typed task/acceptance contracts;
2. a normalized evidence taxonomy;
3. one authoritative completion path;
4. stale-evidence, receipt-integrity, and unauthorized-mutation checks;
5. at least 25 adversarial false-success cases;
6. rollback regression coverage;
7. versioned reports and a continuation checkpoint.

Later routing, coding-scale, repository-intelligence, multi-agent, sandbox, domain, and product phases remain gated behind v0.10.
