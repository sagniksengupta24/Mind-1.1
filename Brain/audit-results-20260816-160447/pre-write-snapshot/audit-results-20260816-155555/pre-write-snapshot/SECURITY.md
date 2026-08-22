# Security Policy

## Supported status

Mind1.1 v0.11.1.dev0 is a research-grade local development candidate. It is not a verified v0.11.1 release and is not approved for untrusted public deployment or multi-tenant use.

## Trust model

Trusted:

- the local operator
- server startup configuration
- the selected local Ollama installation

Untrusted:

- user prompts
- model output
- repository contents
- tool arguments proposed by the model
- HTTP request bodies

Repository text and retrieved documentation are data, never policy.

## Security invariants

- Clients cannot exceed the server maximum mode or capabilities.
- Model and Ollama endpoint selection are server-controlled.
- Source writes require an elevated mode, server write capability, schema permission, and approval.
- Shell execution requires an elevated mode, server shell capability, schema permission, and approval.
- All file operations remain inside the resolved workspace and reject runtime-storage access.
- Mutations require pre-dispatch traces and produce verified receipts.
- API error responses redact expected secrets and suppress unexpected internal exception text.
- Release artifacts exclude `.mind01` and local databases.
- Constrained decoding never bypasses strict parsing or server policy.
- Safe JSON extraction requires exactly one complete, valid, permitted object and never guesses mutation commands or arguments.
- Mutation tools are hidden outside authorized mutation phases.
- Typed routes are bound to the mode and granted capabilities that produced them; stale routes expose no tools.
- Existing-file proposal and mutation schemas remain hidden until required repository inspection succeeds.
- Diagnostic routing confidence cannot grant authority or widen the visible tool set.
- Semantic model output is limited to closed task/specialist/family candidates;
  final tools are always the intersection of trusted policy sets.
- Low confidence, malformed classifier output, refusal, or timeout can only
  preserve or reduce authority.
- `verified` completion requires runtime-owned deterministic evidence.
- Syntax-only evidence cannot satisfy behavioral requirements.
- Stale, pre-mutation, skipped, mismatched-receipt, and out-of-scope evidence cannot produce verified completion.
- Write capability and shell capability are independent: `--allow-write`
  grants mutation only, never execution.
- Self-verification of a write task requires shell capability; a mutation run
  without shell completes `unverified`, never `verified`.
- A model-claimed `verified` status without current passing evidence is
  downgraded to `unverified` or `failed`, never honored.

## Host-execution warning

Allowlisted commands run on the host. This is not a sandbox. Running Python, pytest, or project build tools can execute malicious repository code. Use a disposable container or VM for untrusted repositories.

### Shell policy for write tasks

`--allow-shell` is the single gate that lets the agent verify its own writes by
running allowlisted commands (`python3`, `pytest`, `ruff`, `mypy`, read-only
`git`). Because those commands execute repository code on the host, they are a
meaningful privilege and are intentionally decoupled from `--allow-write`:

- `--allow-write` alone: edits are applied and receipted, but no command can
  run, so `CompletionAuthority` reports `unverified`. This is the safe default
  for edit-only or review-then-apply workflows.
- `--allow-write --allow-shell`: the agent can also run deterministic checks;
  `verified` becomes reachable and is granted only on current, passing,
  task-relevant evidence.
- `unsafe` mode additionally wraps commands in OS-level sandboxing (`bwrap`)
  and fails closed if `bwrap` is unavailable.

Operators granting `--allow-shell` for unsupervised write runs should treat the
repository as trusted-for-execution, or run inside a disposable container/VM.

## Reporting

Do not include live credentials, private repository content, session databases, traces, or receipt backups in a vulnerability report. Provide a minimal reproduction and affected version.
