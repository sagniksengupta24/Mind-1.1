# CLI reference

Snapshot: `3f71bd56823bbde35e70d9c57dbb858f0d1e8894` / `2026-07-30T16:25:16.739118+00:00`.

## Source-confirmed entry points

- `mind01.cli` — [mind01/cli.py:1](../../mind01/cli.py#L1)
- `mind01.cli.main` — [mind01/cli.py:29](../../mind01/cli.py#L29)
- `mind01.cli.build_parser` — [mind01/cli.py:387](../../mind01/cli.py#L387)
- `mind01.cli.add_common` — [mind01/cli.py:601](../../mind01/cli.py#L601)
- `mind01.cli.build_config` — [mind01/cli.py:633](../../mind01/cli.py#L633)
- `mind01.cli.require_patch_apply_policy` — [mind01/cli.py:649](../../mind01/cli.py#L649)
- `mind01.cli.require_rollback_policy` — [mind01/cli.py:660](../../mind01/cli.py#L660)
- `mind01.cli.require_cli_mutation_policy` — [mind01/cli.py:671](../../mind01/cli.py#L671)
- `mind01.cli.print_trace` — [mind01/cli.py:685](../../mind01/cli.py#L685)
- `mind01.cli.render_memories` — [mind01/cli.py:694](../../mind01/cli.py#L694)
- `mind01.cli.render_doc_hits` — [mind01/cli.py:709](../../mind01/cli.py#L709)
- `mind01.cli.render_docs_status` — [mind01/cli.py:723](../../mind01/cli.py#L723)
- `mind01.cli.resolve_workspace_path` — [mind01/cli.py:738](../../mind01/cli.py#L738)
- `mind01.llm.OllamaClient` — [mind01/llm.py:25](../../mind01/llm.py#L25)
- `mind01.llm.OllamaClient.model_metadata` — [mind01/llm.py:38](../../mind01/llm.py#L38)
- `mind01.llm.OllamaClient.supports_json_schema` — [mind01/llm.py:80](../../mind01/llm.py#L80)
- `mind01.llm.OllamaClient.chat` — [mind01/llm.py:96](../../mind01/llm.py#L96)
- `mind01.llm.OllamaClient._chat_payload` — [mind01/llm.py:137](../../mind01/llm.py#L137)
- `mind01.llm.OllamaEmbeddingClient` — [mind01/llm.py:196](../../mind01/llm.py#L196)
- `mind01.llm.OllamaEmbeddingClient.embed` — [mind01/llm.py:201](../../mind01/llm.py#L201)
- `mind01.llm.OllamaEmbeddingClient._embed_new` — [mind01/llm.py:218](../../mind01/llm.py#L218)
- `mind01.llm.OllamaEmbeddingClient._embed_legacy` — [mind01/llm.py:229](../../mind01/llm.py#L229)
- `mind01.llm.OllamaEmbeddingClient._post` — [mind01/llm.py:236](../../mind01/llm.py#L236)
- `tests.test_action_reliability.test_runtime_accepts_verified_with_referenced_evidence` — [tests/test_action_reliability.py:85](../../tests/test_action_reliability.py#L85)
- `tests.test_cli_knowledge` — [tests/test_cli_knowledge.py:1](../../tests/test_cli_knowledge.py#L1)
- `tests.test_cli_knowledge.test_cli_project_knowledge_round_trip` — [tests/test_cli_knowledge.py:9](../../tests/test_cli_knowledge.py#L9)
- `tests.test_file_safety.run_cli_quietly` — [tests/test_file_safety.py:93](../../tests/test_file_safety.py#L93)
- `tests.test_memory.run_cli_capture` — [tests/test_memory.py:122](../../tests/test_memory.py#L122)
- `tests.test_memory.run_cli_code` — [tests/test_memory.py:131](../../tests/test_memory.py#L131)
- `tests.test_mutation_transactions.test_dirty_cli_commands` — [tests/test_mutation_transactions.py:217](../../tests/test_mutation_transactions.py#L217)
- `tests.test_mutation_transactions.run_cli_capture` — [tests/test_mutation_transactions.py:243](../../tests/test_mutation_transactions.py#L243)
- `tests.test_receipts.run_cli_capture` — [tests/test_receipts.py:115](../../tests/test_receipts.py#L115)
- `tests.test_rollback.run_cli_capture` — [tests/test_rollback.py:144](../../tests/test_rollback.py#L144)
- `tests.test_rollback.run_cli_capture_code` — [tests/test_rollback.py:150](../../tests/test_rollback.py#L150)
- `tests.test_semantic_benchmark_v2.test_forbidden_marker_guard_covers_frozen_data_references` — [tests/test_semantic_benchmark_v2.py:52](../../tests/test_semantic_benchmark_v2.py#L52)
- `tests.test_semantic_router_v2.QueuedClient` — [tests/test_semantic_router_v2.py:377](../../tests/test_semantic_router_v2.py#L377)
- `tests.test_semantic_router_v2.QueuedClient.__init__` — [tests/test_semantic_router_v2.py:380](../../tests/test_semantic_router_v2.py#L380)
- `tests.test_semantic_router_v2.QueuedClient.chat` — [tests/test_semantic_router_v2.py:383](../../tests/test_semantic_router_v2.py#L383)
- `tests.test_traces.run_cli_capture` — [tests/test_traces.py:105](../../tests/test_traces.py#L105)
- `tests.test_version.test_cli_version` — [tests/test_version.py:17](../../tests/test_version.py#L17)

## Scope and confidence

Statements in this generated page are source-indexed navigation. Runtime-only, model-dependent, external-process, and documentation-only behavior is not presented as source-confirmed.

## Related evidence

- [Architecture](../../.project_knowledge/architecture/system_overview.md)
- [Symbol index](../../.project_knowledge/symbols.md)
- [Source companions](source/)
