# v0.11 candidate failure analysis

## Deterministic labels

The frozen labeled partitions pass 184/200 complete route checks. Failure taxonomy: `{"mutation_intent": 16}`.

The 16 mutation-intent failures come from contradictory labels in the frozen adversarial generator: repeated attack archetypes are semantically identical but their mutation label changes with absolute case index. The files and hashes are retained unchanged; correcting this requires a new dataset version frozen before future routing changes.

## Development live model

- `development_runs/run-001.json`: 60 cases; first structural validity 0.9666666666666667; terminal parser failure 0.03333333333333333; allowed action 0.9666666666666667.
- `development_runs/run-002.json`: 60 cases; first structural validity 1.0; terminal parser failure 0.0; allowed action 0.9666666666666667.

The initial run's two failures were existing-file proposals with no inspected source. The model repeated empty required `old` and `new` fields through all bounded attempts. The candidate now exposes only `read_file` before the eventual proposal tool. Frozen labels still name the eventual proposal action, so label-relative exact-action and exposure metrics retain that lifecycle mismatch.

## Blind integrity and release blockers

No external blind label package or independently controlled evaluator was provided. In addition, the repository blind-input generator selects prompts from visible labeled archetypes, making their semantic expectations derivable even though expected fields are omitted. Those inputs cannot establish independent blind performance in this development process.

No tool is dispatched by `semantic-live`. Selection and parser safety are measured; zero execution counters are not execution-safety evidence. Host command execution in the real agent remains controlled but is not sandboxed.
