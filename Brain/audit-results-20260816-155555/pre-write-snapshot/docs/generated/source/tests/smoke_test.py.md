# `tests/smoke_test.py`

## File purpose

This testing file is reviewed at snapshot `98edb527bae59c3d22a6c2becd7dc7a36f305fb821729ec4c31e4dcd9a87968f`. It contains 379 lines.

## Imports and module state

- [tests/smoke_test.py:1](../../../../tests/smoke_test.py#L1) imports `__future__` / annotations.
- [tests/smoke_test.py:3](../../../../tests/smoke_test.py#L3) imports `shutil`.
- [tests/smoke_test.py:4](../../../../tests/smoke_test.py#L4) imports `sys`.
- [tests/smoke_test.py:5](../../../../tests/smoke_test.py#L5) imports `tempfile`.
- [tests/smoke_test.py:6](../../../../tests/smoke_test.py#L6) imports `pathlib` / Path.
- [tests/smoke_test.py:10](../../../../tests/smoke_test.py#L10) imports `mind01.agent` / Agent.
- [tests/smoke_test.py:10](../../../../tests/smoke_test.py#L10) imports `mind01.agent` / parse_action.
- [tests/smoke_test.py:11](../../../../tests/smoke_test.py#L11) imports `mind01.config` / AgentConfig.
- [tests/smoke_test.py:12](../../../../tests/smoke_test.py#L12) imports `mind01.doctor` / Check.
- [tests/smoke_test.py:12](../../../../tests/smoke_test.py#L12) imports `mind01.doctor` / extract_model_names.
- [tests/smoke_test.py:12](../../../../tests/smoke_test.py#L12) imports `mind01.doctor` / render_doctor.
- [tests/smoke_test.py:13](../../../../tests/smoke_test.py#L13) imports `mind01.eval` / render_eval_results.
- [tests/smoke_test.py:13](../../../../tests/smoke_test.py#L13) imports `mind01.eval` / run_eval_file.
- [tests/smoke_test.py:13](../../../../tests/smoke_test.py#L13) imports `mind01.eval` / save_eval_results.
- [tests/smoke_test.py:14](../../../../tests/smoke_test.py#L14) imports `mind01.rag` / DocStore.
- [tests/smoke_test.py:15](../../../../tests/smoke_test.py#L15) imports `mind01.security` / redact_secrets.
- [tests/smoke_test.py:16](../../../../tests/smoke_test.py#L16) imports `mind01.sessions` / SessionStore.
- [tests/smoke_test.py:17](../../../../tests/smoke_test.py#L17) imports `mind01.tools` / ToolError.
- [tests/smoke_test.py:17](../../../../tests/smoke_test.py#L17) imports `mind01.tools` / ToolRegistry.
- [tests/smoke_test.py:17](../../../../tests/smoke_test.py#L17) imports `mind01.tools` / parse_allowed_command.
- [tests/smoke_test.py:18](../../../../tests/smoke_test.py#L18) imports `mind01.tools.registry` / ToolRegistry.
- [tests/smoke_test.py:19](../../../../tests/smoke_test.py#L19) imports `mind01.tools.schemas` / SCHEMA_BY_NAME.
- [tests/smoke_test.py:19](../../../../tests/smoke_test.py#L19) imports `mind01.tools.schemas` / TOOL_SCHEMAS.
- [tests/smoke_test.py:19](../../../../tests/smoke_test.py#L19) imports `mind01.tools.schemas` / render_tool_docs.
- [tests/smoke_test.py:19](../../../../tests/smoke_test.py#L19) imports `mind01.tools.schemas` / validate_tool_args.
- [tests/smoke_test.py:20](../../../../tests/smoke_test.py#L20) imports `mind01.tools.shell_tools` / parse_allowed_command.
- [tests/smoke_test.py:21](../../../../tests/smoke_test.py#L21) imports `test_api` / run_api_tests.
- [tests/smoke_test.py:22](../../../../tests/smoke_test.py#L22) imports `test_action_parser` / run_action_parser_tests.
- [tests/smoke_test.py:23](../../../../tests/smoke_test.py#L23) imports `test_docs_rag` / run_docs_rag_tests.
- [tests/smoke_test.py:24](../../../../tests/smoke_test.py#L24) imports `test_evals` / run_eval_suite_tests.
- [tests/smoke_test.py:25](../../../../tests/smoke_test.py#L25) imports `test_file_safety` / run_file_safety_tests.
- [tests/smoke_test.py:26](../../../../tests/smoke_test.py#L26) imports `test_integration_audit` / run_integration_audit_tests.
- [tests/smoke_test.py:27](../../../../tests/smoke_test.py#L27) imports `test_memory` / run_memory_tests.
- [tests/smoke_test.py:28](../../../../tests/smoke_test.py#L28) imports `test_modes` / run_mode_tests.
- [tests/smoke_test.py:29](../../../../tests/smoke_test.py#L29) imports `test_mutation_transactions` / run_mutation_transaction_tests.
- [tests/smoke_test.py:30](../../../../tests/smoke_test.py#L30) imports `test_receipts` / run_receipt_tests.
- [tests/smoke_test.py:31](../../../../tests/smoke_test.py#L31) imports `test_rollback` / run_rollback_tests.
- [tests/smoke_test.py:32](../../../../tests/smoke_test.py#L32) imports `test_shell_safety` / run_shell_safety_tests.
- [tests/smoke_test.py:33](../../../../tests/smoke_test.py#L33) imports `test_traces` / run_trace_tests.
- [tests/smoke_test.py:34](../../../../tests/smoke_test.py#L34) imports `test_audit_chains` / run_audit_chain_tests.
- [tests/smoke_test.py:35](../../../../tests/smoke_test.py#L35) imports `test_agent_fallback` / run_agent_fallback_tests.

## Symbols

### `tests.smoke_test.KeywordEmbedder` — lines 38–44

- Source: [tests/smoke_test.py:38](../../../../tests/smoke_test.py#L38)
- Type: class
- Signature: `n/a`
- Direct static callees: `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.smoke_test.KeywordEmbedder.embed` — lines 39–44

- Source: [tests/smoke_test.py:39](../../../../tests/smoke_test.py#L39)
- Type: method
- Signature: `self, text: str`
- Direct static callees: `lower`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `tests.smoke_test.main` — lines 47–375

- Source: [tests/smoke_test.py:47](../../../../tests/smoke_test.py#L47)
- Type: function
- Signature: `n/a`
- Direct static callees: `Agent`, `AssertionError`, `Check`, `DocStore`, `KeywordEmbedder`, `Path`, `SessionStore`, `ToolRegistry`, `add_message`, `ask`, `build`, `call`, `create`, `extract_model_names`, `get`, `index_path`, `len`, `mkdir`, `mkdtemp`, `parse_action`, `parse_allowed_command`, `print`, `read_text`, `redact_secrets`, `registered_tools`, `render_doctor`, `render_eval_results`, `render_tool_docs`, `rmtree`, `run_action_parser_tests`, `run_agent_fallback_tests`, `run_api_tests`, `run_audit_chain_tests`, `run_docs_rag_tests`, `run_eval_file`, `run_eval_suite_tests`, `run_file_safety_tests`, `run_integration_audit_tests`, `run_memory_tests`, `run_mode_tests`, `run_mutation_transaction_tests`, `run_receipt_tests`, `run_rollback_tests`, `run_shell_safety_tests`, `run_trace_tests`, `save_eval_results`, `search`, `set`, `sorted`, `stale_files`, `stats`, `str`, `validate_tool_args`, `write_text`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 8–8

Implements module-level `Expr` behavior or data.

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

### Lines 28–28

Imports a dependency used by this module.

### Lines 29–29

Imports a dependency used by this module.

### Lines 30–30

Imports a dependency used by this module.

### Lines 31–31

Imports a dependency used by this module.

### Lines 32–32

Imports a dependency used by this module.

### Lines 33–33

Imports a dependency used by this module.

### Lines 34–34

Imports a dependency used by this module.

### Lines 35–35

Imports a dependency used by this module.

### Lines 36–37

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 38–44

Defines class `KeywordEmbedder` and the behavior of its members.

### Lines 45–46

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 47–76

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 77–106

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 107–136

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 137–166

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 167–196

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 197–226

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 227–256

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 257–286

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 287–316

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 317–346

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 347–375

Defines `main` and its implementation control flow; direct static calls: Agent, AssertionError, Check, DocStore, KeywordEmbedder, Path, SessionStore, ToolRegistry, add_message, ask, build, call, create, extract_model_names, get, index_path, len, mkdir, mkdtemp, parse_action, parse_allowed_command, print, read_text, redact_secrets, registered_tools, render_doctor, render_eval_results, render_tool_docs, rmtree, run_action_parser_tests, run_agent_fallback_tests, run_api_tests, run_audit_chain_tests, run_docs_rag_tests, run_eval_file, run_eval_suite_tests, run_file_safety_tests, run_integration_audit_tests, run_memory_tests, run_mode_tests, run_mutation_transaction_tests, run_receipt_tests, run_rollback_tests, run_shell_safety_tests, run_trace_tests, save_eval_results, search, set, sorted, stale_files, stats, str, validate_tool_args, write_text.

### Lines 376–377

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 378–379

Implements module-level `If` behavior or data.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
