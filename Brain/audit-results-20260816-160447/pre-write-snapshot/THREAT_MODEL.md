# Threat Model

## Primary assets

- workspace source files
- local credentials and environment variables
- session and memory databases
- mutation backups
- trace and receipt integrity
- host execution environment

## Main threats and controls

| Threat | Control | Residual risk |
|---|---|---|
| Client privilege escalation | ServerPolicy caps mode, write, shell, approval and steps | Single-token auth has no roles |
| SSRF through model endpoint | Client model/URL changes rejected; loopback allowlist | Trusted startup config can still be wrong |
| Path traversal/symlink escape | Resolved workspace checks and write-target safety | Platform filesystem edge cases require continued testing |
| Malformed model actions | Canonical JSON parser, typed failures, response modes, size/depth limits, bounded repair | Model can still choose a structurally valid but semantically poor action |
| Semantic misrouting | Typed intent/route, finite reason codes, capability fingerprint, phase-scoped exposure, frozen evaluation partitions | Deterministic rules and a 7B model can still misclassify novel requests |
| Tool-schema expansion through prompt injection | One exposure authority derives the visible subset from server mode, capabilities, lifecycle, and route; stale routes fail closed | A permitted read tool can still return malicious repository text |
| Proposal used as execution | Proposal and live-apply families are distinct; live write tools are hidden in propose mode | A poor proposal can still be accepted later by an operator |
| Infinite action loops | Step budget, duplicate-action and repeated-error detection | Complex tasks may stop early |
| Audit-chain race | Cross-thread/process lock and atomic head replacement | Network/distributed filesystems are not supported |
| Session leakage | Session-keyed queries and bounded restoration | No user identity layer beyond API token |
| Malicious repository command | Allowlist, sanitized env, timeout, output cap | Host commands still execute repository code |
| Secret leakage | Redaction and bounded traces | Pattern-based redaction is incomplete |
| Poisoned project memory | File hashes and provenance; changed files replace facts | Semantic truth is not formally proven |

## Out of scope for the v0.11 candidate

- hostile public internet deployment
- multi-tenant isolation
- signed remote attestation
- kernel/container escape resistance
- distributed execution
- claiming semantic verification without an independently controlled blind evaluator and three retained live runs
