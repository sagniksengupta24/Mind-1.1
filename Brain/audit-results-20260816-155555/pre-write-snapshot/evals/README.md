# Mind1.1 evaluation assets

This directory contains the ordinary local evaluation tasks used by the CLI harness. These files currently cover repository analysis, coding, documentation retrieval, memory, safety, semiconductor topics, and Indian-language explanations.

The ordinary files are legacy v0.9 assets: they do not yet have a fully validated dataset schema or development/regression/blind split. They must not be described as a blind model-quality benchmark.

Versioned deterministic suites live inside the package:

- `mind01/eval_suites/action_reliability_v1.json`: 50 model-action cases.
- `mind01/eval_suites/truthful_completion_v1.json`: 25 adversarial false-success cases plus positive evidence-mapping controls.
- `mind01/eval_suites/real_mutation/manifest.json`: three isolated real-mutation fixtures.
- `mind01/eval_suites/semantic_routing_v1/`: frozen routing development, regression, adversarial, capability/mode, ambiguity, and unlabeled blind-input partitions (260 inputs total).

Validate all assets:

```bash
python -m mind01.eval validate
```

Run deterministic plumbing and completion regressions:

```bash
python -m mind01.eval run --suite regression --mock-model
python -m mind01.eval run --suite truthful-completion
python -m mind01.eval run --suite semantic-routing --partition development
```

The first command is explicitly mocked and proves protocol plumbing only. The truthful-completion suite exercises deterministic completion authority; it is not a live-model benchmark.

Live semantic action selection requires Ollama and retains raw output, hashes, parser incidents, model identity/digest, latency, tokens, route fields, visible tools, and per-case choices:

```bash
python -m mind01.eval semantic-live \
  --partition development \
  --model qwen2.5-coder:7b \
  --seed 1101 \
  --output evaluation_results/v0.11.0-release/development_runs/run-001.json
```

This harness does not execute selected tools; its execution-safety fields are therefore zero-by-construction and are not proof of real execution safety. Development tuning, frozen regression, adversarial, capability/mode, ambiguity, and externally evaluated blind results must be reported separately. Blind expected labels must be mounted outside the editable repository after candidate freeze. Three complete independent live runs are required for the v0.11 gate.
