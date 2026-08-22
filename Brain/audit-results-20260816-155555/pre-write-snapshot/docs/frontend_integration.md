# Frontend Integration Guide

This repo does not include or modify a frontend. The existing UI should connect to the local API documented in `docs/api.md`.

## Local Startup

Run the backend API:

```bash
MIND_API_TOKEN=dev-token python3 -m mind01.cli serve-api --workspace . --port 8765 --cors-origin http://localhost:3000
```

Frontend requests should include:

```text
X-Mind-Token: dev-token
```

## Recommended UI Sections

The frontend can be wired around these backend concepts:

- status
- chat/session
- project map
- read/search files
- docs search
- memory list/search
- patch proposals
- receipts
- rollback
- traces
- eval runs

## Mode UX

Expose mode explicitly:

- `read-only` as default
- `propose`
- `write-approved`
- `unsafe`

Do not default to unsafe. For mutation flows, require deliberate user confirmation before sending `yes=true`.

Recommended frontend behavior:

- read-only for normal browsing/chat
- propose for patch proposal and indexing workflows
- write-approved only after review
- unsafe behind an additional warning

## Core Flows

### Health

```http
GET /health
X-Mind-Token: dev-token
```

Use this to show workspace, mode, and auth status.

### Chat

```http
POST /chat
Content-Type: application/json
X-Mind-Token: dev-token

{
  "prompt": "Inspect this repo",
  "mode": "read-only",
  "dry_run": false,
  "trace": true,
  "yes": false,
  "allow_write": false,
  "allow_shell": false
}
```

For write-capable chat:

```json
{
  "mode": "write-approved",
  "allow_write": true,
  "yes": true
}
```

Only send this after explicit user confirmation.

Note: this enables writes only. Without `allow_shell: true`, the agent cannot
run checks, so `completion_status` for a write task will be `unverified` (never
`verified`). Enable `allow_shell` only when the operator accepts host command
execution; see `SECURITY.md` for the shell policy.

### Project Map

```http
GET /project-map
```

Show this as a repo overview.

### Read File

```http
GET /read-file?path=README.md
```

The backend blocks unsafe paths and runtime files.

### Search Code

```http
GET /search-code?q=ToolRegistry&path=mind01
```

### Docs Search

```http
GET /docs/search?q=clock&limit=6
```

Render citations from `citation`, for example:

```text
docs/semiconductor/README.md:L10-L25
```

### Memories

```http
GET /memories?limit=50
GET /memories/search?q=startup&tags=project
```

Memory mutation currently remains primarily CLI/tool-driven. A frontend should not store secrets in memory prompts.

### Patch Proposal

```http
POST /patches/propose
Content-Type: application/json

{
  "kind": "edit",
  "path": "src/app.py",
  "old": "x = 1",
  "new": "x = 2",
  "reason": "small fix",
  "mode": "propose"
}
```

Show the diff:

```http
GET /patches/1
```

Apply only after review:

```http
POST /patches/apply
Content-Type: application/json

{
  "id": 1,
  "mode": "write-approved",
  "yes": true
}
```

Patch apply creates receipts.

### Receipts

```http
GET /receipts
GET /receipts/<receipt_id>
```

Use receipts to show verified write metadata and backup availability.

### Rollback

```http
POST /rollback
Content-Type: application/json

{
  "receipt_id": "...",
  "mode": "write-approved",
  "yes": true,
  "force": false
}
```

If the backend rejects rollback due to current hash mismatch, show that error and ask the user whether they intentionally want force.

### Traces

```http
GET /traces
GET /traces/<trace_id_or_file>
```

Use traces for debugging, not as user-facing proof of production safety.

### Eval Runs

```http
GET /eval-runs
GET /eval-runs/<file>
```

Dry-run evals prove harness behavior only. Live-model evals need Ollama and are not deterministic model-quality guarantees.

## Dirty State Recovery Flow

If a transaction-safe file mutation fails midway (e.g., process crash, disk exhaustion) and the backup cannot be automatically restored, the backend records a dirty mutation state under `.mind01/mutations/dirty/`.

### Checking for Dirty States
The frontend should check the quick `GET /health` or `GET /status` endpoints and look for:
- `"dirty_state_count"`: If `> 0`, display a warning banner in the UI.
- `"receipt_chain_head_present"` / `"trace_chain_head_present"`: Status indicators showing whether tamper-evident chain verification is active.

### Resolving Dirty States
The frontend can list and display dirty states using:
```http
GET /mutations/dirty
GET /mutations/dirty/<dirty_id>
```
To maintain frontend safety, these endpoints return relative paths (e.g., `backup_relative_path` and `target_relative_path` under `.mind01`) and safe metadata (sha256 hashes and sizes) instead of absolute local file system paths or raw contents.

**Recommended Recovery UX**:
1. Present the list of affected files along with `manual_repair_instructions` from the dirty state record.
2. Instruct the user to restore the file from the backup relative path or resolve conflicts manually.
3. Once repaired, delete the corresponding dirty state JSON file from `.mind01/mutations/dirty/` using CLI tools (the endpoints are read-only to prevent unauthorized mutations from the browser).

## Error Handling

The frontend should expect request and trace IDs in structured error payloads:

```json
{
  "error": {
    "code": "bad_request",
    "message": "Human-readable message.",
    "details": {},
    "request_id": "8e66632b462849e69a3c8918094bb502",
    "trace_id": null
  }
}
```

- **`request_id`**: A unique UUID generated for every single API request. Always present. Useful for logging and telemetry.
- **`trace_id`**: A unique trace event identifier. Only present if a trace event actually exists (e.g., for errors occurred during a prompt session/execution). When populated, the frontend can link developers to `GET /traces/<trace_id>` for deep debugging.

Do not display secrets. The backend attempts to avoid token leakage, but UI logs should still avoid dumping headers and raw request bodies.

## Security Notes

- Keep the API bound to localhost.
- Do not expose this API directly to the internet.
- Use a token in local dev when connecting a browser UI.
- Do not use wildcard CORS with auth.
- Never default UI flows to unsafe mode.
- Confirm write, shell, patch apply, and rollback actions explicitly.
