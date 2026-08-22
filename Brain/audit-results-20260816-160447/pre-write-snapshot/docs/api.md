# Mind1.1 Local API — v0.11 development candidate

The API is intended for a trusted local frontend. It is not a public hosted-agent service.

`POST /chat` uses the same canonical JSON action protocol, typed semantic route, phase-scoped tools, parser repair, policy checks, mutation receipts, verification, review, and completion-status authority as the CLI. Its response includes `routing_decision`, `parser_incidents`, `completion_status`, and `output_mode`; clients cannot choose the model, Ollama endpoint, or greater privileges.

## Secure defaults

- Bind: `127.0.0.1`
- Maximum mode: `read-only`
- Write: disabled
- Shell: disabled
- Non-interactive mutation approval: disabled
- Ollama endpoint: server-configured loopback endpoint
- Body limit: 1 MB
- Concurrent requests: 4
- Request timeout: 180 seconds
- Token: `MIND_API_TOKEN` or `--api-token`

A token is mandatory when elevated capabilities are enabled or when binding beyond loopback. Wildcard CORS is rejected when authentication is enabled.

```bash
MIND_API_TOKEN=dev-token python3 -m mind01.cli serve-api \
  --workspace . \
  --mode propose \
  --cors-origin http://localhost:3000
```

Write-capable example:

```bash
MIND_API_TOKEN=dev-token python3 -m mind01.cli serve-api \
  --workspace . \
  --mode write-approved \
  --allow-write \
  --auto-approve
```

`--auto-approve` is intentionally separate from `--allow-write`. Without it, API patch apply and rollback remain disabled.

## Authentication

Send:

```text
X-Mind-Token: <token>
```

## Errors

```json
{
  "error": {
    "code": "bad_request",
    "message": "Requested mode `unsafe` exceeds server maximum `read-only`.",
    "details": {},
    "request_id": "...",
    "trace_id": null
  }
}
```

Unexpected internal exception text is not exposed.

## `POST /chat`

Accepted request fields:

```json
{
  "prompt": "Inspect api.py",
  "session_id": "optional-existing-session",
  "mode": "read-only",
  "max_steps": 6,
  "dry_run": false,
  "trace": true,
  "allow_write": false,
  "allow_shell": false
}
```

Rules:

- `mode` cannot exceed the server maximum.
- `max_steps` cannot exceed the server limit.
- `allow_write` and `allow_shell` cannot exceed server capabilities.
- `model` cannot be changed by a client.
- `ollama_url` cannot be changed by a client.
- An unknown `session_id` is rejected.
- Existing bounded conversation history is restored before execution.

Shell policy: `allow_write` and `allow_shell` are independent. A write task
(`mode: write-approved` + `allow_write`) without `allow_shell` can apply edits
but cannot run `run_command`/`test_patch`, so its `completion_status` is
`unverified` (never `verified`). Self-verification of writes requires
`allow_shell`; see `SECURITY.md` for the full policy.

Response:

```json
{
  "session_id": "...",
  "text": "...",
  "steps": 3,
  "trace": [],
  "specialist": "repository_understanding",
  "verification": [],
  "parser_incidents": [],
  "completion_status": "unverified",
  "completion_contract": {},
  "routing_decision": {
    "schema_version": "1.0",
    "task_class": "inspection",
    "specialist": "repository_inspector",
    "tool_family": "file_inspection",
    "response_mode": "action",
    "reason_code": "direct_file_read"
  },
  "output_mode": "json_schema"
}
```

`routing_decision` is diagnostic and auditable. It never grants authority; the server policy and current capability fingerprint remain authoritative. Unknown route fields, specialists, families, reason codes, and stale capability identities fail closed.

## Read endpoints

- `GET /health` and `/status`: version, mode, auth and audit-head status; does not expose the absolute workspace path
- `GET /project-map`
- `GET /read-file?path=README.md`
- `GET /search-code?q=query&path=.`
- `GET /knowledge` and `/knowledge?q=query&limit=20`
- `GET /docs`
- `GET /docs/search?q=query&limit=6`
- `GET /memories`
- `GET /memories/search`
- `GET /patches` and `/patches/<id>`
- `GET /receipts` and `/receipts/<id>`
- `GET /traces` and `/traces/<id>`
- `GET /eval-runs` and `/eval-runs/<id>`
- `GET /mutations/dirty` and `/mutations/dirty/<id>`
- `GET /sessions` and `/sessions/<id>`

## Runtime-mutation endpoints

### `POST /index`

Requires a server maximum of at least `propose`.

```json
{"path": ".", "mode": "propose"}
```

### `POST /knowledge/refresh`

Requires at least `propose`. Refreshes provenance-aware files, symbols, modules, definitions, and imports.

### `POST /docs/index`

Requires at least `propose`. The embedding endpoint is always the trusted server Ollama endpoint.

### `POST /patches/propose`

Requires at least `propose`. Creates a reviewable proposal; it does not modify source files.

### `POST /patches/apply`

Requires:

- authenticated elevated server
- maximum mode `write-approved` or `unsafe`
- server `--allow-write`
- server `--auto-approve`

The request cannot grant any of these capabilities.

### `POST /rollback`

Uses the same elevated server requirements as patch apply and creates a new rollback receipt.
