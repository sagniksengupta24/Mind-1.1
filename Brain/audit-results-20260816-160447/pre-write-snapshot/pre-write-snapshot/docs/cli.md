# CLI reference additions for semantic routing

Existing `ask`, API, evaluation, knowledge, receipt, trace, and rollback commands remain available. The v0.11 candidate adds the following evaluation paths:

```bash
# Validate ordinary assets, frozen routing partitions, hashes, and blind-label separation.
python -m mind01.eval validate

# Deterministic typed router; no model calls.
python -m mind01.eval run --suite semantic-routing --partition development

# Real constrained action selection; retains per-case raw output and metadata.
python -m mind01.eval semantic-live \
  --partition regression \
  --model qwen2.5-coder:7b \
  --seed 2101 \
  --timeout 180 \
  --output evaluation_results/v0.11.0-release/regression_runs/run-001.json
```

Valid local labeled partitions are `development`, `regression`, `adversarial`, `capability_mode`, and `ambiguity`. The `blind` partition intentionally refuses local live scoring because its expected labels must come from an external evaluator outside the editable repository.

`semantic-live` performs up to two bounded parser repairs and executes no selected tool. Use the agent `ask` command or API for the actual policy/execution lifecycle; do not interpret routing-harness safety zeros as execution evidence.

Lifecycle-aware v2 selection and real disposable-fixture dispatch are separate commands:

```bash
python -m mind01.eval semantic-v2-live \
  --partition lifecycle --seed 11101 \
  --output evaluation_results/v0.11.0-rc2/visible_runs/run_1/lifecycle.json

python -m mind01.eval end-to-end-live \
  --seed 11101 \
  --output evaluation_results/v0.11.0-rc2/end_to_end_runs/run_1.json

python -m mind01.eval rc2-complete-live \
  --run-name run_1 --seed 11101 \
  --external-blind-labels /read-only/mount/labels.json \
  --output-root evaluation_results/v0.11.0-rc2
```

The v2 labeled partitions add `lifecycle`; `end_to_end` is executed through its dedicated command. Blind scoring additionally requires `--external-blind-labels /read-only/mount/labels.json` after candidate freeze. The scorer verifies the external label/provenance hash and frozen input identity and does not copy expected blind labels into its report.

`rc2-complete-live` is the release-evidence entry point. It refuses a dirty tracked source tree or writable blind-label file, executes every visible partition, all disposable end-to-end fixtures, the external blind suite, and truthful-completion regression in one invocation, and marks its manifest complete only after source/model/seed identity is rechecked.

```bash
mind01 --version
python -c "import mind01; print(mind01.__version__)"
```

## Shell policy for write tasks (`ask --allow-write --allow-shell`)

`--allow-write` and `--allow-shell` are independent privileges on `ask` (and the
API `POST /chat` body):

- `--allow-write`: lets the agent apply `edit_file` / `write_file` mutations.
- `--allow-shell`: lets the agent run allowlisted commands (`python3`, `pytest`,
  `ruff`, `mypy`, read-only `git`) via `run_command` / `test_patch`.

**Self-verification of a write task requires `--allow-shell`.** Every mutation
route's plan includes a `verify` step that executes through `run_command`;
`CompletionAuthority` reports a mutation `verified` only with current, passing,
task-relevant evidence, which only command execution can produce. A write task
run with `--allow-write` but without `--allow-shell`:

- cannot run `run_command` or `test_patch` (hidden; they raise `ToolError`), and
- completes with status `unverified` (never `verified`); a model-claimed
  `verified` is downgraded to `unverified` or `failed`.

So the exact command for an unsupervised, self-verifying edit is:

```bash
mind01 ask "<write task>" --workspace . \
  --mode write-approved --allow-write --allow-shell --yes
```

Dropping `--allow-shell` keeps edits possible but forces an honest `unverified`
completion — appropriate for edit-only workflows. `unsafe` mode adds OS-level
sandboxing (`bwrap`) and fails closed without it. See `SECURITY.md` and
`README.md` for the full policy.
