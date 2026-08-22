# `mind01/api.py`

## File purpose

This API file is reviewed at snapshot `76e82a50e969b0536396b582441a4f9c23c0e699fdfbf89bf5b3ce7844089be9`. It contains 726 lines.

## Imports and module state

- [mind01/api.py:1](../../../../mind01/api.py#L1) imports `__future__` / annotations.
- [mind01/api.py:3](../../../../mind01/api.py#L3) imports `json`.
- [mind01/api.py:4](../../../../mind01/api.py#L4) imports `os`.
- [mind01/api.py:5](../../../../mind01/api.py#L5) imports `threading`.
- [mind01/api.py:6](../../../../mind01/api.py#L6) imports `http.server` / BaseHTTPRequestHandler.
- [mind01/api.py:6](../../../../mind01/api.py#L6) imports `http.server` / ThreadingHTTPServer.
- [mind01/api.py:7](../../../../mind01/api.py#L7) imports `pathlib` / Path.
- [mind01/api.py:8](../../../../mind01/api.py#L8) imports `urllib.parse` / parse_qs.
- [mind01/api.py:8](../../../../mind01/api.py#L8) imports `urllib.parse` / urlparse.
- [mind01/api.py:10](../../../../mind01/api.py#L10) imports `agent` / Agent.
- [mind01/api.py:11](../../../../mind01/api.py#L11) imports `code_index` / CodeIndex.
- [mind01/api.py:11](../../../../mind01/api.py#L11) imports `code_index` / render_file_summary.
- [mind01/api.py:12](../../../../mind01/api.py#L12) imports `config` / AgentConfig.
- [mind01/api.py:13](../../../../mind01/api.py#L13) imports `file_safety` / FileSafetyError.
- [mind01/api.py:13](../../../../mind01/api.py#L13) imports `file_safety` / read_text_file_safe.
- [mind01/api.py:14](../../../../mind01/api.py#L14) imports `llm` / EmbeddingError.
- [mind01/api.py:14](../../../../mind01/api.py#L14) imports `llm` / OllamaEmbeddingClient.
- [mind01/api.py:15](../../../../mind01/api.py#L15) imports `memory` / MemoryStore.
- [mind01/api.py:16](../../../../mind01/api.py#L16) imports `modes` / AgentMode.
- [mind01/api.py:16](../../../../mind01/api.py#L16) imports `modes` / parse_agent_mode.
- [mind01/api.py:17](../../../../mind01/api.py#L17) imports `mutations` / DirtyStateStore.
- [mind01/api.py:17](../../../../mind01/api.py#L17) imports `mutations` / MutationError.
- [mind01/api.py:18](../../../../mind01/api.py#L18) imports `patches` / PatchError.
- [mind01/api.py:18](../../../../mind01/api.py#L18) imports `patches` / PatchStore.
- [mind01/api.py:19](../../../../mind01/api.py#L19) imports `policy` / PolicyViolation.
- [mind01/api.py:19](../../../../mind01/api.py#L19) imports `policy` / ServerPolicy.
- [mind01/api.py:20](../../../../mind01/api.py#L20) imports `project_knowledge` / ProjectKnowledgeStore.
- [mind01/api.py:21](../../../../mind01/api.py#L21) imports `project_map` / build_project_map.
- [mind01/api.py:22](../../../../mind01/api.py#L22) imports `rag` / DocStore.
- [mind01/api.py:23](../../../../mind01/api.py#L23) imports `receipts` / ReceiptError.
- [mind01/api.py:23](../../../../mind01/api.py#L23) imports `receipts` / ReceiptStore.
- [mind01/api.py:24](../../../../mind01/api.py#L24) imports `security` / redact_secrets.
- [mind01/api.py:25](../../../../mind01/api.py#L25) imports `sessions` / SessionStore.
- [mind01/api.py:25](../../../../mind01/api.py#L25) imports `sessions` / message_to_dict.
- [mind01/api.py:25](../../../../mind01/api.py#L25) imports `sessions` / session_to_dict.
- [mind01/api.py:26](../../../../mind01/api.py#L26) imports `tools` / ToolError.
- [mind01/api.py:26](../../../../mind01/api.py#L26) imports `tools` / ToolRegistry.
- [mind01/api.py:27](../../../../mind01/api.py#L27) imports `traces` / TraceError.
- [mind01/api.py:27](../../../../mind01/api.py#L27) imports `traces` / TraceStore.

## Symbols

### `mind01.api.sanitize_backup_relative_path` — lines 30–38

- Source: [mind01/api.py:30](../../../../mind01/api.py#L30)
- Type: function
- Signature: `path_str: str | None`
- Direct static callees: `replace`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.safe_dirty_record` — lines 41–58

- Source: [mind01/api.py:41](../../../../mind01/api.py#L41)
- Type: function
- Signature: `record: dict`
- Direct static callees: `get`, `sanitize_backup_relative_path`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MAX_BODY_BYTES` — lines 61–61

- Source: [mind01/api.py:61](../../../../mind01/api.py#L61)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI` — lines 64–498

- Source: [mind01/api.py:64](../../../../mind01/api.py#L64)
- Type: class
- Signature: `n/a`
- Direct static callees: `Agent`, `BoundedSemaphore`, `CodeIndex`, `DirtyStateStore`, `DocStore`, `MemoryStore`, `OllamaEmbeddingClient`, `PatchStore`, `PolicyViolation`, `ProjectKnowledgeStore`, `ReceiptStore`, `ServerPolicy`, `SessionStore`, `ToolRegistry`, `TraceStore`, `ValueError`, `_dispatch_get`, `_get_detail_payload`, `_get_routes`, `_require_mode`, `_write_get_exception`, `acquire`, `add_message`, `apply`, `ask`, `authorized`, `bool`, `build`, `build_project_map`, `call`, `capabilities_for`, `context_messages`, `create`, `doc_hit_to_dict`, `exists`, `file_summary`, `first`, `get`, `glob`, `handle_get`, `handle_options`, `handle_post`, `handler`, `index_path`, `int`, `isinstance`, `join`, `knowledge_hit_to_dict`, `len`, `list`, `list_eval_runs`, `lower`, `max`, `memory_to_dict`, `message_to_dict`, `min`, `parse_agent_mode`, `parse_qs`, `propose_patch`, `query`, `read_eval_run`, `read_json`, `read_text_file_safe`, `recall`, `redact_secrets`, `refresh`, `release`, `render`, `render_file_summary`, `render_show`, `resolve`, `resolve_mode`, `resolve_steps`, `resolve_workspace_path`, `rollback`, `rstrip`, `safe_dirty_record`, `search`, `search_symbols`, `session_to_dict`, `show`, `sorted`, `stale_doc_to_dict`, `stale_files`, `startswith`, `stats`, `str`, `strip`, `symbol_to_dict`, `to_dict`, `urlparse`, `uuid4`, `validate_ollama_url`, `write_error`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.__init__` — lines 65–103

- Source: [mind01/api.py:65](../../../../mind01/api.py#L65)
- Type: method
- Signature: `self, workspace: Path, model: str, ollama_url: str, mode: str | AgentMode=AgentMode.READ_ONLY, api_token: str='', cors_origin: str='http://localhost:3000', *, allow_write: bool=False, allow_shell: bool=False, auto_approve: bool=False, max_steps: int=12, max_body_bytes: int=MAX_BODY_BYTES, max_concurrent_requests: int=4, request_timeout_seconds: int=180`
- Direct static callees: `BoundedSemaphore`, `ServerPolicy`, `ValueError`, `bool`, `int`, `max`, `min`, `parse_agent_mode`, `resolve`, `validate_ollama_url`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.handler` — lines 105–121

- Source: [mind01/api.py:105](../../../../mind01/api.py#L105)
- Type: method
- Signature: `self`
- Direct static callees: `handle_get`, `handle_options`, `handle_post`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.handle_options` — lines 123–124

- Source: [mind01/api.py:123](../../../../mind01/api.py#L123)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler`
- Direct static callees: `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.handle_get` — lines 126–139

- Source: [mind01/api.py:126](../../../../mind01/api.py#L126)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler`
- Direct static callees: `_dispatch_get`, `_write_get_exception`, `authorized`, `parse_qs`, `urlparse`, `uuid4`, `write_error`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._dispatch_get` — lines 141–147

- Source: [mind01/api.py:141](../../../../mind01/api.py#L141)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler, path: str, query: dict[str, list[str]]`
- Direct static callees: `_get_detail_payload`, `_get_routes`, `get`, `handler`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_routes` — lines 149–170

- Source: [mind01/api.py:149](../../../../mind01/api.py#L149)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_detail_payload` — lines 172–184

- Source: [mind01/api.py:172](../../../../mind01/api.py#L172)
- Type: method
- Signature: `self, path: str, query: dict[str, list[str]]`
- Direct static callees: `handler`, `len`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_health` — lines 186–201

- Source: [mind01/api.py:186](../../../../mind01/api.py#L186)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `bool`, `exists`, `glob`, `len`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_project_map` — lines 203–204

- Source: [mind01/api.py:203](../../../../mind01/api.py#L203)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `build_project_map`, `render`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_read_file` — lines 206–209

- Source: [mind01/api.py:206](../../../../mind01/api.py#L206)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `first`, `read_text_file_safe`, `redact_secrets`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_search_code` — lines 211–216

- Source: [mind01/api.py:211](../../../../mind01/api.py#L211)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `ToolRegistry`, `call`, `first`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_memories` — lines 218–222

- Source: [mind01/api.py:218](../../../../mind01/api.py#L218)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `MemoryStore`, `first`, `int`, `list`, `memory_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_memory_search` — lines 224–230

- Source: [mind01/api.py:224](../../../../mind01/api.py#L224)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `MemoryStore`, `first`, `int`, `memory_to_dict`, `recall`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_patches` — lines 232–233

- Source: [mind01/api.py:232](../../../../mind01/api.py#L232)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `PatchStore`, `list`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_patch` — lines 235–236

- Source: [mind01/api.py:235](../../../../mind01/api.py#L235)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `PatchStore`, `int`, `show`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_receipts` — lines 238–239

- Source: [mind01/api.py:238](../../../../mind01/api.py#L238)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `ReceiptStore`, `first`, `int`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_receipt` — lines 241–242

- Source: [mind01/api.py:241](../../../../mind01/api.py#L241)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `ReceiptStore`, `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_traces` — lines 244–245

- Source: [mind01/api.py:244](../../../../mind01/api.py#L244)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `TraceStore`, `first`, `int`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_trace` — lines 247–248

- Source: [mind01/api.py:247](../../../../mind01/api.py#L247)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `TraceStore`, `render_show`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_dirty_states` — lines 250–252

- Source: [mind01/api.py:250](../../../../mind01/api.py#L250)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `DirtyStateStore`, `first`, `int`, `list`, `safe_dirty_record`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_dirty_state` — lines 254–255

- Source: [mind01/api.py:254](../../../../mind01/api.py#L254)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `DirtyStateStore`, `get`, `safe_dirty_record`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_eval_runs` — lines 257–258

- Source: [mind01/api.py:257](../../../../mind01/api.py#L257)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `list_eval_runs`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_eval_run` — lines 260–261

- Source: [mind01/api.py:260](../../../../mind01/api.py#L260)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `read_eval_run`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_symbols` — lines 263–267

- Source: [mind01/api.py:263](../../../../mind01/api.py#L263)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `CodeIndex`, `first`, `int`, `search_symbols`, `symbol_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_code_index` — lines 269–272

- Source: [mind01/api.py:269](../../../../mind01/api.py#L269)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `CodeIndex`, `stale_files`, `stats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_knowledge` — lines 274–280

- Source: [mind01/api.py:274](../../../../mind01/api.py#L274)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `ProjectKnowledgeStore`, `first`, `int`, `knowledge_hit_to_dict`, `query`, `stats`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_file_summary` — lines 282–284

- Source: [mind01/api.py:282](../../../../mind01/api.py#L282)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `CodeIndex`, `file_summary`, `first`, `render_file_summary`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_docs` — lines 286–288

- Source: [mind01/api.py:286](../../../../mind01/api.py#L286)
- Type: method
- Signature: `self, _query: dict[str, list[str]]`
- Direct static callees: `DocStore`, `stale_doc_to_dict`, `stale_files`, `stats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_docs_search` — lines 290–300

- Source: [mind01/api.py:290](../../../../mind01/api.py#L290)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `DocStore`, `OllamaEmbeddingClient`, `doc_hit_to_dict`, `first`, `int`, `lower`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_sessions` — lines 302–304

- Source: [mind01/api.py:302](../../../../mind01/api.py#L302)
- Type: method
- Signature: `self, query: dict[str, list[str]]`
- Direct static callees: `SessionStore`, `first`, `int`, `list`, `session_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._get_session` — lines 306–311

- Source: [mind01/api.py:306](../../../../mind01/api.py#L306)
- Type: method
- Signature: `self, identifier: str, _query: dict[str, list[str]]`
- Direct static callees: `SessionStore`, `get`, `message_to_dict`, `session_to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._write_get_exception` — lines 313–326

- Source: [mind01/api.py:313](../../../../mind01/api.py#L313)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler, req_id: str, exc: Exception`
- Direct static callees: `isinstance`, `lower`, `str`, `write_error`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.handle_post` — lines 328–486

- Source: [mind01/api.py:328](../../../../mind01/api.py#L328)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler`
- Direct static callees: `Agent`, `CodeIndex`, `DocStore`, `OllamaEmbeddingClient`, `PatchStore`, `PolicyViolation`, `ProjectKnowledgeStore`, `ReceiptStore`, `SessionStore`, `ValueError`, `_require_mode`, `acquire`, `add_message`, `apply`, `ask`, `authorized`, `bool`, `build`, `capabilities_for`, `context_messages`, `create`, `exists`, `get`, `index_path`, `int`, `join`, `len`, `lower`, `min`, `propose_patch`, `read_json`, `redact_secrets`, `refresh`, `release`, `resolve_mode`, `resolve_steps`, `resolve_workspace_path`, `rollback`, `rstrip`, `session_to_dict`, `stats`, `str`, `strip`, `to_dict`, `uuid4`, `write_error`, `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI._require_mode` — lines 488–493

- Source: [mind01/api.py:488](../../../../mind01/api.py#L488)
- Type: method
- Signature: `self, body: dict, allowed: set[AgentMode], action: str`
- Direct static callees: `PolicyViolation`, `get`, `join`, `resolve_mode`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.MindAPI.authorized` — lines 495–498

- Source: [mind01/api.py:495](../../../../mind01/api.py#L495)
- Type: method
- Signature: `self, request: BaseHTTPRequestHandler`
- Direct static callees: `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.serve_api` — lines 501–543

- Source: [mind01/api.py:501](../../../../mind01/api.py#L501)
- Type: function
- Signature: `workspace: Path, host: str, port: int, model: str, ollama_url: str, mode: str | AgentMode=AgentMode.READ_ONLY, api_token: str='', cors_origin: str='http://localhost:3000', *, allow_write: bool=False, allow_shell: bool=False, auto_approve: bool=False, max_steps: int=12, max_body_bytes: int=MAX_BODY_BYTES, max_concurrent_requests: int=4, request_timeout_seconds: int=180`
- Direct static callees: `MindAPI`, `ThreadingHTTPServer`, `ValueError`, `handler`, `print`, `serve_forever`, `server_close`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.read_json` — lines 546–556

- Source: [mind01/api.py:546](../../../../mind01/api.py#L546)
- Type: function
- Signature: `request: BaseHTTPRequestHandler, max_body_bytes: int=MAX_BODY_BYTES`
- Direct static callees: `ValueError`, `decode`, `get`, `int`, `isinstance`, `loads`, `read`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.write_json` — lines 559–573

- Source: [mind01/api.py:559](../../../../mind01/api.py#L559)
- Type: function
- Signature: `request: BaseHTTPRequestHandler, payload: dict, status: int=200, cors_origin: str='http://localhost:3000'`
- Direct static callees: `dumps`, `encode`, `end_headers`, `len`, `send_header`, `send_response`, `str`, `write`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.write_error` — lines 576–595

- Source: [mind01/api.py:576](../../../../mind01/api.py#L576)
- Type: function
- Signature: `request: BaseHTTPRequestHandler, code: str, message: str, status: int, cors_origin: str='http://localhost:3000', details: dict | None=None, request_id: str | None=None, trace_id: str | None=None`
- Direct static callees: `write_json`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.first` — lines 598–602

- Source: [mind01/api.py:598](../../../../mind01/api.py#L598)
- Type: function
- Signature: `query: dict[str, list[str]], key: str, default: str`
- Direct static callees: `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.resolve_workspace_path` — lines 605–609

- Source: [mind01/api.py:605](../../../../mind01/api.py#L605)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `ValueError`, `resolve`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.require_api_mode` — lines 612–619

- Source: [mind01/api.py:612](../../../../mind01/api.py#L612)
- Type: function
- Signature: `body: dict, allowed: set[AgentMode], action: str`
- Direct static callees: `ValueError`, `get`, `join`, `parse_agent_mode`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.propose_patch` — lines 622–631

- Source: [mind01/api.py:622](../../../../mind01/api.py#L622)
- Type: function
- Signature: `workspace: Path, body: dict`
- Direct static callees: `PatchStore`, `ValueError`, `get`, `propose_edit`, `propose_write`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.memory_to_dict` — lines 634–652

- Source: [mind01/api.py:634](../../../../mind01/api.py#L634)
- Type: function
- Signature: `item`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.symbol_to_dict` — lines 655–662

- Source: [mind01/api.py:655](../../../../mind01/api.py#L655)
- Type: function
- Signature: `item`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.knowledge_hit_to_dict` — lines 665–673

- Source: [mind01/api.py:665](../../../../mind01/api.py#L665)
- Type: function
- Signature: `item`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.doc_hit_to_dict` — lines 676–691

- Source: [mind01/api.py:676](../../../../mind01/api.py#L676)
- Type: function
- Signature: `item`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.stale_doc_to_dict` — lines 694–695

- Source: [mind01/api.py:694](../../../../mind01/api.py#L694)
- Type: function
- Signature: `item`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.list_eval_runs` — lines 698–709

- Source: [mind01/api.py:698](../../../../mind01/api.py#L698)
- Type: function
- Signature: `workspace: Path`
- Direct static callees: `append`, `exists`, `get`, `glob`, `loads`, `read_text`, `relative_to`, `sorted`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.read_eval_run` — lines 712–722

- Source: [mind01/api.py:712](../../../../mind01/api.py#L712)
- Type: function
- Signature: `workspace: Path, identifier: str`
- Direct static callees: `ValueError`, `endswith`, `exists`, `loads`, `read_text`, `resolve`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.api.default_api_token` — lines 725–726

- Source: [mind01/api.py:725](../../../../mind01/api.py#L725)
- Type: function
- Signature: `n/a`
- Direct static callees: `get`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports a dependency used by this module.

### Lines 5–5

Imports a dependency used by this module.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–21

Imports a dependency used by this module.

### Lines 22–22

Imports a dependency used by this module.

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports a dependency used by this module.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–26

Imports a dependency used by this module.

### Lines 27–27

Imports a dependency used by this module.

### Lines 28–29

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 30–38

Defines `sanitize_backup_relative_path` and its implementation control flow; direct static calls: replace, startswith.

### Lines 39–40

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 41–58

Defines `safe_dirty_record` and its implementation control flow; direct static calls: get, sanitize_backup_relative_path.

### Lines 59–60

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 61–61

Implements module-level `Assign` behavior or data.

### Lines 62–63

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 64–93

Defines class `MindAPI` and the behavior of its members.

### Lines 94–123

Defines class `MindAPI` and the behavior of its members.

### Lines 124–153

Defines class `MindAPI` and the behavior of its members.

### Lines 154–183

Defines class `MindAPI` and the behavior of its members.

### Lines 184–213

Defines class `MindAPI` and the behavior of its members.

### Lines 214–243

Defines class `MindAPI` and the behavior of its members.

### Lines 244–273

Defines class `MindAPI` and the behavior of its members.

### Lines 274–303

Defines class `MindAPI` and the behavior of its members.

### Lines 304–333

Defines class `MindAPI` and the behavior of its members.

### Lines 334–363

Defines class `MindAPI` and the behavior of its members.

### Lines 364–393

Defines class `MindAPI` and the behavior of its members.

### Lines 394–423

Defines class `MindAPI` and the behavior of its members.

### Lines 424–453

Defines class `MindAPI` and the behavior of its members.

### Lines 454–483

Defines class `MindAPI` and the behavior of its members.

### Lines 484–498

Defines class `MindAPI` and the behavior of its members.

### Lines 499–500

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 501–530

Defines `serve_api` and its implementation control flow; direct static calls: MindAPI, ThreadingHTTPServer, ValueError, handler, print, serve_forever, server_close.

### Lines 531–543

Defines `serve_api` and its implementation control flow; direct static calls: MindAPI, ThreadingHTTPServer, ValueError, handler, print, serve_forever, server_close.

### Lines 544–545

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 546–556

Defines `read_json` and its implementation control flow; direct static calls: ValueError, decode, get, int, isinstance, loads, read.

### Lines 557–558

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 559–573

Defines `write_json` and its implementation control flow; direct static calls: dumps, encode, end_headers, len, send_header, send_response, str, write.

### Lines 574–575

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 576–595

Defines `write_error` and its implementation control flow; direct static calls: write_json.

### Lines 596–597

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 598–602

Defines `first` and its implementation control flow; direct static calls: get.

### Lines 603–604

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 605–609

Defines `resolve_workspace_path` and its implementation control flow; direct static calls: ValueError, resolve.

### Lines 610–611

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 612–619

Defines `require_api_mode` and its implementation control flow; direct static calls: ValueError, get, join, parse_agent_mode, sorted, str.

### Lines 620–621

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 622–631

Defines `propose_patch` and its implementation control flow; direct static calls: PatchStore, ValueError, get, propose_edit, propose_write, str.

### Lines 632–633

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 634–652

Defines `memory_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 653–654

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 655–662

Defines `symbol_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 663–664

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 665–673

Defines `knowledge_hit_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 674–675

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 676–691

Defines `doc_hit_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 692–693

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 694–695

Defines `stale_doc_to_dict` and its implementation control flow; direct static calls: none resolved.

### Lines 696–697

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 698–709

Defines `list_eval_runs` and its implementation control flow; direct static calls: append, exists, get, glob, loads, read_text, relative_to, sorted, str.

### Lines 710–711

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 712–722

Defines `read_eval_run` and its implementation control flow; direct static calls: ValueError, endswith, exists, loads, read_text, resolve, startswith.

### Lines 723–724

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 725–726

Defines `default_api_token` and its implementation control flow; direct static calls: get.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
