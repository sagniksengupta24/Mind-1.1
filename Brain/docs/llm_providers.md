# LLM provider adapter

Mind1.1 talks to exactly one seam for model calls: `Agent.llm`, an
object with a `chat(messages, json_mode, response_schema) -> str` method.
Historically that object was always an `OllamaClient` (`mind01/llm.py`),
hardcoded at construction time in `Agent.__init__`.

`mind01/llm_providers.py` adds a second implementation of that same
surface, `OpenAICompatibleClient`, for any cloud, OpenAI-compatible
`/chat/completions` endpoint — OpenRouter by default, or any other provider
(Together, Groq, Fireworks, a self-hosted vLLM/TGI server, ...) via
`base_url`/`api_key`. Inference runs on the provider's GPUs; nothing is
downloaded or run locally. This lets the agent use 30B-70B+ open-weight
models (DeepSeek, Qwen, Llama, ...) without owning the hardware for them.

`Agent` and `OllamaSemanticClassifier` do not know which implementation
they got — `build_llm_client(config)` is the only place that branches on
provider:

```text
AgentConfig (provider, model, api_key, base_url, fallback_models, ...)
        |
        v
build_llm_client(config)  --  the only provider branch point
        |
        +--> OllamaClient            (provider = "ollama", default)
        +--> OpenAICompatibleClient  (provider = "openrouter" | "openai_compatible")
        |
        v
Agent.llm.chat(...)  /  OllamaSemanticClassifier(client).predict_task(...)
```

## Configuring a provider

Nothing here is required — the default (`provider=ollama`) is byte-for-byte
the previous local-only behavior. To use a cloud provider, set env vars
(see `.env.example`) or pass the equivalent CLI flags:

| Env var                | CLI flag             | Meaning                                                        |
|-------------------------|-----------------------|------------------------------------------------------------------|
| `LLM_PROVIDER`          | `--provider`          | `ollama` (default) \| `openrouter` \| `openai_compatible`        |
| `LLM_MODEL`             | `--model`             | Model ID as the provider names it                                 |
| `OPENROUTER_API_KEY`    | `--api-key`           | Used automatically when provider is `openrouter`                  |
| `LLM_API_KEY`           | `--api-key`           | Used for `openai_compatible`, or as a fallback for any provider   |
| `LLM_BASE_URL`          | `--base-url`          | Required for `openai_compatible`; defaults to OpenRouter's URL for `openrouter` |
| `LLM_FALLBACK_MODELS`   | `--fallback-models`   | Comma-separated model IDs tried in order on retryable failure     |
| `LLM_SITE_URL`          | —                      | Optional `HTTP-Referer` sent to OpenRouter for attribution         |
| `LLM_APP_NAME`          | —                      | Optional `X-Title` sent to OpenRouter for attribution              |

Example (OpenRouter, free model, two free fallbacks):

```bash
export LLM_PROVIDER=openrouter
export LLM_MODEL="deepseek/deepseek-chat-v3.1:free"
export OPENROUTER_API_KEY="sk-or-v1-..."
export LLM_FALLBACK_MODELS="qwen/qwen3-235b-a22b:free,meta-llama/llama-3.3-70b-instruct:free"

mind01 ask --workspace . "Summarize this repo's routing design."
```

Or via CLI flags only, no env vars:

```bash
mind01 ask --workspace . --provider openrouter \
  --model "deepseek/deepseek-chat-v3.1:free" \
  --api-key "$OPENROUTER_API_KEY" \
  --fallback-models "qwen/qwen3-235b-a22b:free,meta-llama/llama-3.3-70b-instruct:free" \
  "Summarize this repo's routing design."
```

`serve-api` picks up the same env vars automatically (it builds
`AgentConfig` the same way per request); no extra flags were added there.

## What the adapter does

- **Structured JSON output.** `Agent` always calls `chat(..., json_mode=True,
  response_schema=<schema>)` — it has no unconstrained-prose path. The
  cloud client mirrors `OllamaClient`'s behavior exactly: it starts
  conservative (`response_format: json_object`, broadly supported), and
  only enables `response_format: json_schema` once a live call proves the
  model/deployment accepts it. If a `json_schema` attempt gets a `400`/`422`,
  it's retried once as `json_object` in the same call and that capability is
  remembered for the rest of the session — never falls through to
  unconstrained text.
- **Error handling.** Every HTTP failure becomes an `LLMError` (the same
  exception type `Agent` already catches) with a `status_code` and a
  provider-message-derived, bounded description — auth failures, missing
  model, rate limiting, and payment-required are distinguished so the
  agent's failure message is actionable.
- **Retries.** `429`/`5xx` responses are retried with exponential backoff
  (`max_retries`, default 2) before raising.
- **Fallback models.** `chat()` tries `model`, then each entry in
  `fallback_models` in order, on any retryable failure. Auth errors
  (`401`/`403`) are never retried against a different model, since they
  won't improve.
- **Streaming.** `chat_stream()` yields content deltas from the endpoint's
  SSE stream. Not currently wired into `Agent` (which does one blocking
  call per step), but available for a UI/CLI that wants token-by-token
  output.
- **Tool/function calling.** `chat_with_tools()` sends OpenAI-style `tools`
  and returns the raw assistant `message` (which may contain `tool_calls`)
  unopinionated — `Agent`'s own action protocol is a JSON-schema-constrained
  single response rather than native tool calls, so this method isn't
  wired into the loop, but it's there for callers/extensions that want
  native function calling from a tool-calling-capable model.

## Adding another provider

Any strictly OpenAI-compatible endpoint needs zero new code — set
`LLM_PROVIDER=openai_compatible` and point `LLM_BASE_URL`/`LLM_API_KEY` at
it. A provider with a genuinely different wire format gets its own class
next to `OpenAICompatibleClient` in `llm_providers.py`, implementing the
same `chat(messages, json_mode, response_schema) -> str` surface (plus the
`.timeout` / `.last_output_mode` / `.last_server_version` /
`.last_response_metadata` attributes `Agent` reads), and one more branch
in `build_llm_client()`. No other module changes.

## Known scope boundary

`mind01/doctor.py`'s `run_doctor()` is provider-aware: for
`provider=ollama` it does the original local reachability/model-pull
checks. For a cloud provider it checks that an API key and base URL are
configured, but does **not** make a live request to the provider (to
avoid spending a paid or rate-limited call just for a health check) — an
auth or connectivity problem will surface as a clear `LLMError` on the
first real `ask`/`chat` call instead.
