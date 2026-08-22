# `mind01/cli.py`

## File purpose

This CLI file is reviewed at snapshot `e8f3194c5021c0891063c6afd03b9f96b237cb3fc963d1c76e874a3028cb3040`. It contains 746 lines.

## Imports and module state

- [mind01/cli.py:1](../../../../mind01/cli.py#L1) imports `__future__` / annotations.
- [mind01/cli.py:3](../../../../mind01/cli.py#L3) imports `argparse`.
- [mind01/cli.py:4](../../../../mind01/cli.py#L4) imports `sys`.
- [mind01/cli.py:5](../../../../mind01/cli.py#L5) imports `pathlib` / Path.
- [mind01/cli.py:7](../../../../mind01/cli.py#L7) imports `agent` / Agent.
- [mind01/cli.py:8](../../../../mind01/cli.py#L8) imports `api` / default_api_token.
- [mind01/cli.py:8](../../../../mind01/cli.py#L8) imports `api` / serve_api.
- [mind01/cli.py:9](../../../../mind01/cli.py#L9) imports `code_index` / CodeIndex.
- [mind01/cli.py:9](../../../../mind01/cli.py#L9) imports `code_index` / render_file_summary.
- [mind01/cli.py:9](../../../../mind01/cli.py#L9) imports `code_index` / render_symbol_hits.
- [mind01/cli.py:10](../../../../mind01/cli.py#L10) imports `config` / AgentConfig.
- [mind01/cli.py:11](../../../../mind01/cli.py#L11) imports `doctor` / render_doctor.
- [mind01/cli.py:11](../../../../mind01/cli.py#L11) imports `doctor` / run_doctor.
- [mind01/cli.py:12](../../../../mind01/cli.py#L12) imports `eval` / render_eval_results.
- [mind01/cli.py:12](../../../../mind01/cli.py#L12) imports `eval` / run_eval_file.
- [mind01/cli.py:12](../../../../mind01/cli.py#L12) imports `eval` / save_eval_results.
- [mind01/cli.py:12](../../../../mind01/cli.py#L12) imports `eval` / save_eval_run.
- [mind01/cli.py:13](../../../../mind01/cli.py#L13) imports `file_safety` / FileSafetyError.
- [mind01/cli.py:13](../../../../mind01/cli.py#L13) imports `file_safety` / resolve_workspace_path.
- [mind01/cli.py:14](../../../../mind01/cli.py#L14) imports `llm` / EmbeddingError.
- [mind01/cli.py:14](../../../../mind01/cli.py#L14) imports `llm` / OllamaEmbeddingClient.
- [mind01/cli.py:15](../../../../mind01/cli.py#L15) imports `memory` / MemoryStore.
- [mind01/cli.py:16](../../../../mind01/cli.py#L16) imports `modes` / AgentMode.
- [mind01/cli.py:16](../../../../mind01/cli.py#L16) imports `modes` / mode_choices.
- [mind01/cli.py:16](../../../../mind01/cli.py#L16) imports `modes` / parse_agent_mode.
- [mind01/cli.py:17](../../../../mind01/cli.py#L17) imports `mutations` / DirtyStateStore.
- [mind01/cli.py:17](../../../../mind01/cli.py#L17) imports `mutations` / MutationError.
- [mind01/cli.py:18](../../../../mind01/cli.py#L18) imports `patches` / PatchError.
- [mind01/cli.py:18](../../../../mind01/cli.py#L18) imports `patches` / PatchStore.
- [mind01/cli.py:19](../../../../mind01/cli.py#L19) imports `project_knowledge` / ProjectKnowledgeStore.
- [mind01/cli.py:20](../../../../mind01/cli.py#L20) imports `project_map` / build_project_map.
- [mind01/cli.py:21](../../../../mind01/cli.py#L21) imports `rag` / DocStore.
- [mind01/cli.py:22](../../../../mind01/cli.py#L22) imports `receipts` / ReceiptError.
- [mind01/cli.py:22](../../../../mind01/cli.py#L22) imports `receipts` / ReceiptStore.
- [mind01/cli.py:23](../../../../mind01/cli.py#L23) imports `security` / redact_secrets.
- [mind01/cli.py:24](../../../../mind01/cli.py#L24) imports `tools` / ToolError.
- [mind01/cli.py:25](../../../../mind01/cli.py#L25) imports `traces` / TraceError.
- [mind01/cli.py:25](../../../../mind01/cli.py#L25) imports `traces` / TraceStore.
- [mind01/cli.py:26](../../../../mind01/cli.py#L26) imports `version` / __version__.

## Symbols

### `mind01.cli.main` — lines 29–384

- Source: [mind01/cli.py:29](../../../../mind01/cli.py#L29)
- Type: function
- Signature: `argv: list[str] | None=None`
- Direct static callees: `Agent`, `CodeIndex`, `DirtyStateStore`, `DocStore`, `MemoryStore`, `OllamaEmbeddingClient`, `PatchStore`, `Path`, `ProjectKnowledgeStore`, `ReceiptStore`, `TraceStore`, `all`, `apply`, `ask`, `bool`, `build_config`, `build_parser`, `build_project_map`, `call`, `delete`, `discard`, `dumps`, `expanduser`, `file_summary`, `getattr`, `index_path`, `input`, `list`, `parse_agent_mode`, `parse_args`, `print`, `print_help`, `print_trace`, `query`, `recall`, `refresh`, `relative_to`, `remember`, `render`, `render_doc_hits`, `render_docs_status`, `render_doctor`, `render_eval_results`, `render_file_summary`, `render_list`, `render_memories`, `render_show`, `render_symbol_hits`, `require_cli_mutation_policy`, `require_patch_apply_policy`, `require_rollback_policy`, `resolve`, `resolve_workspace_path`, `rollback`, `run_doctor`, `run_eval_file`, `save_eval_results`, `save_eval_run`, `search`, `search_symbols`, `serve_api`, `show`, `stats`, `strip`, `update`, `verify_receipt_chain`, `verify_trace_chain`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.build_parser` — lines 387–598

- Source: [mind01/cli.py:387](../../../../mind01/cli.py#L387)
- Type: function
- Signature: `n/a`
- Direct static callees: `ArgumentParser`, `add_argument`, `add_common`, `add_parser`, `add_subparsers`, `default_api_token`, `mode_choices`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.add_common` — lines 601–630

- Source: [mind01/cli.py:601](../../../../mind01/cli.py#L601)
- Type: function
- Signature: `parser: argparse.ArgumentParser`
- Direct static callees: `add_argument`, `mode_choices`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.build_config` — lines 633–646

- Source: [mind01/cli.py:633](../../../../mind01/cli.py#L633)
- Type: function
- Signature: `args: argparse.Namespace`
- Direct static callees: `build`, `getattr`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.require_patch_apply_policy` — lines 649–657

- Source: [mind01/cli.py:649](../../../../mind01/cli.py#L649)
- Type: function
- Signature: `args: argparse.Namespace`
- Direct static callees: `ToolError`, `getattr`, `parse_agent_mode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.require_rollback_policy` — lines 660–668

- Source: [mind01/cli.py:660](../../../../mind01/cli.py#L660)
- Type: function
- Signature: `args: argparse.Namespace`
- Direct static callees: `ToolError`, `getattr`, `parse_agent_mode`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.require_cli_mutation_policy` — lines 671–682

- Source: [mind01/cli.py:671](../../../../mind01/cli.py#L671)
- Type: function
- Signature: `args: argparse.Namespace, allowed_modes: set[str], action: str`
- Direct static callees: `ToolError`, `getattr`, `join`, `parse_agent_mode`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.print_trace` — lines 685–691

- Source: [mind01/cli.py:685](../../../../mind01/cli.py#L685)
- Type: function
- Signature: `events: list[str]`
- Direct static callees: `print`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.render_memories` — lines 694–706

- Source: [mind01/cli.py:694](../../../../mind01/cli.py#L694)
- Type: function
- Signature: `memories`
- Direct static callees: `join`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.render_doc_hits` — lines 709–720

- Source: [mind01/cli.py:709](../../../../mind01/cli.py#L709)
- Type: function
- Signature: `hits`
- Direct static callees: `append`, `join`, `redact_secrets`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.render_docs_status` — lines 723–735

- Source: [mind01/cli.py:723](../../../../mind01/cli.py#L723)
- Type: function
- Signature: `store: DocStore`
- Direct static callees: `append`, `extend`, `join`, `len`, `stale_files`, `stats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.cli.resolve_workspace_path` — lines 738–742

- Source: [mind01/cli.py:738](../../../../mind01/cli.py#L738)
- Type: function
- Signature: `workspace: Path, raw_path: str`
- Direct static callees: `ValueError`, `resolve_safe_workspace_path`, `str`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

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

### Lines 27–28

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 29–58

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 59–88

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 89–118

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 119–148

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 149–178

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 179–208

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 209–238

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 239–268

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 269–298

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 299–328

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 329–358

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 359–384

Defines `main` and its implementation control flow; direct static calls: Agent, CodeIndex, DirtyStateStore, DocStore, MemoryStore, OllamaEmbeddingClient, PatchStore, Path, ProjectKnowledgeStore, ReceiptStore, TraceStore, all, apply, ask, bool, build_config, build_parser, build_project_map, call, delete, discard, dumps, expanduser, file_summary, getattr, index_path, input, list, parse_agent_mode, parse_args, print, print_help, print_trace, query, recall, refresh, relative_to, remember, render, render_doc_hits, render_docs_status, render_doctor, render_eval_results, render_file_summary, render_list, render_memories, render_show, render_symbol_hits, require_cli_mutation_policy, require_patch_apply_policy, require_rollback_policy, resolve, resolve_workspace_path, rollback, run_doctor, run_eval_file, save_eval_results, save_eval_run, search, search_symbols, serve_api, show, stats, strip, update, verify_receipt_chain, verify_trace_chain.

### Lines 385–386

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 387–416

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 417–446

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 447–476

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 477–506

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 507–536

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 537–566

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 567–596

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 597–598

Defines `build_parser` and its implementation control flow; direct static calls: ArgumentParser, add_argument, add_common, add_parser, add_subparsers, default_api_token, mode_choices.

### Lines 599–600

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 601–630

Defines `add_common` and its implementation control flow; direct static calls: add_argument, mode_choices.

### Lines 631–632

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 633–646

Defines `build_config` and its implementation control flow; direct static calls: build, getattr.

### Lines 647–648

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 649–657

Defines `require_patch_apply_policy` and its implementation control flow; direct static calls: ToolError, getattr, parse_agent_mode.

### Lines 658–659

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 660–668

Defines `require_rollback_policy` and its implementation control flow; direct static calls: ToolError, getattr, parse_agent_mode.

### Lines 669–670

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 671–682

Defines `require_cli_mutation_policy` and its implementation control flow; direct static calls: ToolError, getattr, join, parse_agent_mode, sorted.

### Lines 683–684

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 685–691

Defines `print_trace` and its implementation control flow; direct static calls: print.

### Lines 692–693

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 694–706

Defines `render_memories` and its implementation control flow; direct static calls: join, list.

### Lines 707–708

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 709–720

Defines `render_doc_hits` and its implementation control flow; direct static calls: append, join, redact_secrets.

### Lines 721–722

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 723–735

Defines `render_docs_status` and its implementation control flow; direct static calls: append, extend, join, len, stale_files, stats.

### Lines 736–737

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 738–742

Defines `resolve_workspace_path` and its implementation control flow; direct static calls: ValueError, resolve_safe_workspace_path, str.

### Lines 743–744

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 745–746

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
