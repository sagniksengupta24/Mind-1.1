# v0.11 Semantic Routing Reliability — candidate release notes

Status: **FAILED/BLOCKED release gate**. The code is versioned `0.11.0.dev0`; no stable `v0.11.0` tag is authorized.

RC3 annotation later processed 120 independently authored blind cases, accepted 117, and rejected 3. Its sealer correctly failed because selection happened before annotation and no reserve existed. The old input hash is retained as superseded evidence. The evaluation-only RC3.1 process is documented in [rc3_1_evaluation.md](rc3_1_evaluation.md); it does not authorize a release or runtime tuning.

RC3.1 subsequently sealed a corrected 120-case set and completed its public-only live execution. Structural validity was 100% with zero terminal parser failures, unsafe actions, and unauthorized mutations, but task-class accuracy was 70%, immediate-family accuracy 49.17%, allowed-tool accuracy 53.33%, and all five frozen semantic gates failed. The computed decision remains `HOLD`; no stable tag is authorized.

The candidate adds strict typed intent, hierarchical deterministic routing, capability-bound route identities, finite reason codes, ambiguity handling, centralized phase-scoped tool exposure, and real-Ollama semantic action evidence. v0.10 canonical parsing, bounded repair, mutation receipts, verification, rollback, and runtime completion authority remain in force.

The first complete 60-case development run retained two terminal parser failures. Both attempted an existing-file proposal without source content and repeated empty required `old`/`new` values through the bounded repair budget. The architectural correction now exposes only `read_file` until exact-file inspection succeeds. No parser weakening or frozen-label change was made.

Release blocking issues:

- no independently controlled external blind labels or evaluator were supplied;
- the repository blind inputs were generated from visible archetypes, so they cannot establish independent blind performance even though readable expected fields are absent;
- three complete independent live runs, including blind evaluation, do not exist;
- the frozen adversarial set contains 16 contradictory mutation-intent labels across repeated archetypes; those failures are retained rather than relabeled;
- the live semantic harness selects but does not execute tools, so execution-safety results require separate evidence.

The release report and manifest under `evaluation_results/v0.11.0-release/` are failure evidence, not certification. A future candidate needs an independently authored/sealed blind package, corrected newly versioned datasets created before further tuning, candidate freeze, and three complete live runs. Do not start or claim v0.12 from this failed gate.
