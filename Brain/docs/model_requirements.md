# Local model requirements

The v0.11 candidate is evaluated only with `qwen2.5-coder:7b` through Ollama. Do not silently substitute another tag or quantization when comparing retained metrics.

The retained environment uses Ollama 0.32.0 and model digest `dae161e27b0e90dd1856c8bb3209201fd6736d8eb66298e75ed87571486f4364`: 7.6B parameters, Q4_K_M, 32,768 context length, and JSON Schema structured-output support. Live reports record the daemon/client version, resolved digest, model details, schema capability, seed, temperature 0.2, top-p 0.9, context size, and timeout.

```bash
ollama serve
ollama pull qwen2.5-coder:7b
ollama list
python -m mind01.eval semantic-live \
  --partition development \
  --model qwen2.5-coder:7b \
  --ollama-url http://127.0.0.1:11434 \
  --seed 1101 \
  --timeout 180 \
  --output evaluation_results/v0.11.0-release/development_runs/run-001.json
```

RC2 complete runs use recorded seeds `11101`, `11102`, and `11103` for every v2 visible partition, the isolated end-to-end fixture suite, and the externally labeled blind partition. The runner fails before evaluation when the resolved digest differs from the value above; an average from mixed model identities is invalid.

If the daemon, exact model, digest lookup, or structured request is unavailable, deterministic work may continue but the live release gate is blocked. JSON-mode fallback remains parser-validated, but its results must be reported separately from JSON Schema runs.

Model quality is a remaining limitation. A 7B local model can emit structurally valid yet semantically wrong actions, repeat an invalid repair, or fail to synthesize valid replacement arguments without inspected source. The runtime bounds and records these failures; it cannot turn the model into a stronger model.
