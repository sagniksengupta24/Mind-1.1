# Mind1.1 v0.10.0-baseline-for-v0.11 release evidence

Release gate: **PASSED**

## Identity

- Commit: `ff8f5a387d8be31059f074f36d7cac16f455eda7`
- Tree: `c5b2d710cc45552812dffb19fe5bc1eb2ad911f2`
- Branch: `v0.11/semantic-routing`
- Dirty before verification: `False`
- Source SHA-256: `7897fa8ac6d240db455c44194201b1c2ab404893953a998abad89a01ae3fcc5b`
- Wheel SHA-256: `1d21b4a576f267ec885a97a88321ee8ffba815c72b5fce97e25f2b3b356d0559`
- Suite SHA-256: `e23669c37968436aecf88c9076e974dc629917100bd30490de8e1ab8373f5565`

## Deterministic results

- Canonical commands passed: `True`
- Truthful-completion cases: `28/28`
- False successes: `0`
- Verified controls with complete evidence mapping: `3/3`

## Evidence categories not run

- Live model: `not_run`
- Hidden coding: `not_run`
- Sandbox security: `not_run`
- Performance: `not_run`

## Known limitations

- No live-model benchmark was run for v0.10.0.
- Historical 62% semantic tool-family and 2/3 mutation reports are not retained locally.
- Host execution is controlled but not sandboxed.
- Authentication remains a single local token.
- Ordinary evaluation datasets are not yet versioned or split.
- No open-source redistribution license has been selected.
- Release evidence is hash-addressed but not externally signed.
