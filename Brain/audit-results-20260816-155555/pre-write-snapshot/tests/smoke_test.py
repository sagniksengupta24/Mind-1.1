from __future__ import annotations

import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from mind01.agent import Agent, parse_action
from mind01.config import AgentConfig
from mind01.doctor import Check, extract_model_names, render_doctor
from mind01.eval import render_eval_results, run_eval_file, save_eval_results
from mind01.rag import DocStore
from mind01.security import redact_secrets
from mind01.sessions import SessionStore
from mind01.tools import ToolError, ToolRegistry, parse_allowed_command
from mind01.tools.registry import ToolRegistry as PackageToolRegistry
from mind01.tools.schemas import SCHEMA_BY_NAME, TOOL_SCHEMAS, render_tool_docs, validate_tool_args
from mind01.tools.shell_tools import parse_allowed_command as package_parse_allowed_command
from test_api import run_api_tests
from test_action_parser import run_action_parser_tests
from test_docs_rag import run_docs_rag_tests
from test_evals import run_eval_suite_tests
from test_file_safety import run_file_safety_tests
from test_integration_audit import run_integration_audit_tests
from test_memory import run_memory_tests
from test_modes import run_mode_tests
from test_mutation_transactions import run_mutation_transaction_tests
from test_receipts import run_receipt_tests
from test_rollback import run_rollback_tests
from test_shell_safety import run_shell_safety_tests
from test_traces import run_trace_tests
from test_audit_chains import run_audit_chain_tests
from test_agent_fallback import run_agent_fallback_tests


class KeywordEmbedder:
    def embed(self, text: str) -> list[float]:
        lowered = text.lower()
        return [
            1.0 if word in lowered else 0.0
            for word in ("clock", "timing", "reset", "python")
        ]


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-test-"))
    try:
        (tmp / "src").mkdir()
        (tmp / "src" / "demo.py").write_text("def add(a, b):\n    return a + b\n")

        parsed = parse_action(
            '<action_json>{"tool":"read_file","args":{"path":"src/demo.py"}}</action_json>'
        )
        assert parsed.tool_name == "read_file"
        assert parsed.tool_args["path"] == "src/demo.py"
        malformed = parse_action('{"tool":{"name":"read_file","args":{"path":"src/demo.py"}}}')
        assert malformed.invalid_json

        assert PackageToolRegistry is ToolRegistry
        assert package_parse_allowed_command is parse_allowed_command

        tools = ToolRegistry(tmp, yes=True)
        expected_tools = {
            "list_files",
            "project_map",
            "read_file",
            "search_code",
            "index_code",
            "search_symbols",
            "file_summary",
            "write_file",
            "edit_file",
            "propose_write_file",
            "propose_edit_file",
            "list_patches",
            "show_patch",
            "test_patch",
            "run_command",
            "remember",
            "recall",
            "list_memories",
            "update_memory",
            "delete_memory",
            "search_docs",
            "refresh_knowledge",
            "query_knowledge",
        }
        assert set(tools.registered_tools()) == expected_tools
        schema_names = [schema.name for schema in TOOL_SCHEMAS]
        assert sorted(schema_names) == sorted(expected_tools)
        assert len(schema_names) == len(set(schema_names))
        assert set(SCHEMA_BY_NAME) == expected_tools
        assert "not_registered" not in SCHEMA_BY_NAME
        docs_text = render_tool_docs()
        for tool_name in expected_tools:
            assert f"- {tool_name}:" in docs_text

        normalized = validate_tool_args("list_files", {})
        assert normalized == {"path": "."}
        normalized_limit = validate_tool_args("search_symbols", {"query": "add", "limit": 3})
        assert normalized_limit["limit"] == 3
        validate_tool_args("read_file", {"path": "src/demo.py"})
        validate_tool_args("search_docs", {"query": "clock", "embed": "true"})
        try:
            validate_tool_args("read_file", {})
            raise AssertionError("missing required arg was not rejected by schema")
        except ValueError as exc:
            assert "Missing required arg" in str(exc)
        try:
            validate_tool_args("read_file", {"path": "src/demo.py", "extra": "no"})
            raise AssertionError("unknown arg was not rejected by schema")
        except ValueError as exc:
            assert "Unknown arg" in str(exc)
        try:
            validate_tool_args("read_file", {"path": 123})
            raise AssertionError("wrong arg type was not rejected by schema")
        except ValueError as exc:
            assert "must be a string" in str(exc)
        try:
            validate_tool_args("search_symbols", {"query": "add", "limit": "many"})
            raise AssertionError("wrong integer arg type was not rejected by schema")
        except ValueError as exc:
            assert "must be an integer" in str(exc)
        try:
            validate_tool_args("search_docs", {"query": "clock", "embed": "maybe"})
            raise AssertionError("invalid enum value was not rejected by schema")
        except ValueError as exc:
            assert "Invalid value" in str(exc)
        try:
            validate_tool_args("not_registered", {})
            raise AssertionError("unknown tool was not rejected by schema")
        except ValueError as exc:
            assert "Unknown tool" in str(exc)

        assert SCHEMA_BY_NAME["write_file"].safety_level == "write"
        assert SCHEMA_BY_NAME["write_file"].approval_required
        assert SCHEMA_BY_NAME["write_file"].can_write
        assert not SCHEMA_BY_NAME["write_file"].can_run_shell
        assert SCHEMA_BY_NAME["run_command"].safety_level == "shell"
        assert SCHEMA_BY_NAME["run_command"].approval_required
        assert SCHEMA_BY_NAME["run_command"].can_run_shell
        assert not SCHEMA_BY_NAME["run_command"].can_write
        assert SCHEMA_BY_NAME["run_command"].output_summary
        run_api_tests()
        run_action_parser_tests()
        run_docs_rag_tests()
        run_eval_suite_tests()
        run_memory_tests()
        run_mode_tests()
        run_mutation_transaction_tests()
        run_file_safety_tests()
        run_integration_audit_tests()
        run_shell_safety_tests()
        run_receipt_tests()
        run_rollback_tests()
        run_trace_tests()
        run_audit_chain_tests()
        run_agent_fallback_tests()
        listed = tools.call("list_files", {"path": "."}).text
        assert "src/demo.py" in listed
        project = tools.call("project_map", {"path": "."}).text
        assert "total_files" in project
        read = tools.call("read_file", {"path": "src/demo.py"}).text
        assert "def add" in read
        (tmp / "src" / "secret.py").write_text("api_key = 'super-secret-value'\n")
        secret_read = tools.call("read_file", {"path": "src/secret.py"}).text
        assert "super-secret-value" not in secret_read
        assert "[REDACTED]" in secret_read
        search = tools.call("search_code", {"query": "return", "path": "."}).text
        assert "src/demo.py:2" in search
        try:
            tools.call("read_file", {})
            raise AssertionError("missing tool arg was not rejected")
        except ToolError as exc:
            assert "Missing required arg" in str(exc)
        code_tools = ToolRegistry(tmp, yes=True, mode="propose")
        indexed = code_tools.call("index_code", {"path": "."}).text
        assert "Indexed" in indexed
        symbols = code_tools.call("search_symbols", {"query": "add"}).text
        assert "function add" in symbols
        summary = code_tools.call("file_summary", {"path": "src/demo.py"}).text
        assert "def add(a, b)" in summary
        propose_tools = ToolRegistry(tmp, yes=True, mode="propose")
        proposal = propose_tools.call(
            "propose_edit_file",
            {
                "path": "src/demo.py",
                "old": "return a + b",
                "new": "return int(a) + int(b)",
                "reason": "coerce inputs",
            },
        ).text
        assert "Proposed patch 1" in proposal
        patch_list = propose_tools.call("list_patches", {}).text
        assert "coerce inputs" in patch_list
        patch_show = propose_tools.call("show_patch", {"id": 1}).text
        assert "+    return int(a) + int(b)" in patch_show
        patch_test_tools = ToolRegistry(
            tmp,
            yes=True,
            allow_shell=True,
            mode="write-approved",
        )
        patch_test = patch_test_tools.call(
            "test_patch",
            {"id": 1, "command": "python3 --version"},
        ).text
        assert "PASS patch 1" in patch_test
        (tmp / "src" / "demo.py").write_text("def add(a, b):\n    return a - b\n")
        assert "src/demo.py" in code_tools.code_index.stale_files()

        try:
            tools.call("write_file", {"path": "src/blocked.py", "content": "x = 1\n"})
            raise AssertionError("write_file was not blocked in read-only mode")
        except ToolError as exc:
            assert "read-only" in str(exc)

        write_tools = ToolRegistry(
            tmp,
            yes=True,
            allow_write=True,
            mode="write-approved",
        )
        wrote = write_tools.call(
            "write_file", {"path": "src/allowed.py", "content": "x = 1\n"}
        ).text
        assert "Wrote src/allowed.py" in wrote
        assert (tmp / "src" / "allowed.py").read_text() == "x = 1\n"

        memory_tools = ToolRegistry(tmp, yes=True, mode="write-approved")
        memory_tools.call("remember", {"key": "language", "value": "Prefer Hindi explanations"})
        recall = memory_tools.call("recall", {"query": "Hindi"}).text
        assert "Prefer Hindi" in recall
        listed_memories = memory_tools.call("list_memories", {"limit": 5}).text
        assert "language" in listed_memories
        memory_tools.call("update_memory", {"id": 1, "value": "Prefer Bengali explanations"})
        updated_recall = memory_tools.call("recall", {"query": "Bengali"}).text
        assert "Prefer Bengali" in updated_recall
        memory_tools.call("delete_memory", {"id": 1})
        deleted_recall = memory_tools.call("recall", {"query": "Bengali"}).text
        assert deleted_recall == "(no memories)"

        docs_dir = tmp / "docs"
        docs_dir.mkdir()
        (docs_dir / "vlsi.md").write_text("Setup time is checked before clock edge.")
        docs = DocStore(tmp)
        assert docs.index_path(docs_dir) >= 1
        assert docs.search("clock")
        assert docs.stale_files() == []
        (docs_dir / "vlsi.md").write_text(
            "Setup time is checked before clock edge. Hold time is checked after it."
        )
        stale_docs = docs.stale_files()
        assert len(stale_docs) == 1
        assert stale_docs[0].path == "docs/vlsi.md"
        assert stale_docs[0].reason == "changed"
        assert docs.index_path(docs_dir) >= 1
        assert docs.stale_files() == []
        assert docs.index_path(docs_dir, embedder=KeywordEmbedder(), embedding_model="test-embed") >= 1
        stats = docs.stats()
        assert stats["embedded_chunks"] >= 1
        assert stats["stale_files"] == 0
        embedded_hits = docs.search(
            "clock timing",
            embedder=KeywordEmbedder(),
            embedding_model="test-embed",
        )
        assert embedded_hits
        assert embedded_hits[0].vector_score > 0.0
        docs_result = tools.call("search_docs", {"query": "clock"}).text
        assert "score=" in docs_result
        assert redact_secrets("token=abc123") == "token=[REDACTED]"

        try:
            tools.call("run_command", {"command": "rm -rf /"})
            raise AssertionError("dangerous command was not blocked")
        except ToolError:
            pass
        try:
            tools.call("run_command", {"command": "python3 --version"})
            raise AssertionError("run_command was not blocked without allow_shell")
        except ToolError as exc:
            assert "read-only" in str(exc)
        try:
            parse_allowed_command("python3 -c 'print(1)'")
            raise AssertionError("inline Python was not blocked")
        except ToolError:
            pass
        try:
            parse_allowed_command("python3 --version; rm -rf /")
            raise AssertionError("shell operator was not blocked")
        except ToolError:
            pass
        try:
            parse_allowed_command("python3 --version; echo hi")
            raise AssertionError("attached shell operator was not blocked")
        except ToolError:
            pass
        shell_tools = ToolRegistry(
            tmp,
            yes=True,
            allow_shell=True,
            mode="write-approved",
        )
        version = shell_tools.call("run_command", {"command": "python3 --version"}).text
        assert "exit_code=0" in version

        config = AgentConfig.build(
            workspace=str(tmp),
            model="qwen2.5-coder:7b",
            ollama_url="http://127.0.0.1:11434",
            max_steps=1,
            yes=True,
            dry_run=True,
        )
        response = Agent(config).ask("List files")
        assert "Dry run ready" in response.text

        memory_config = AgentConfig.build(
            workspace=str(tmp),
            model="qwen2.5-coder:7b",
            ollama_url="http://127.0.0.1:11434",
            max_steps=1,
            yes=True,
            dry_run=False,
            mode="write-approved",
        )
        memory_agent = Agent(memory_config)
        remembered = memory_agent.ask(
            "Remember this startup direction: Mind1.1 focuses on code, "
            "Indian languages, semiconductor workflows, memory, and reasoning. "
            "Then confirm the saved direction."
        )
        assert "startup direction" in remembered.text
        recalled = memory_agent.ask(
            "Recall the startup direction and summarize it in one sentence."
        )
        assert "code" in recalled.text
        assert "semiconductor" in recalled.text
        assert "memory" in recalled.text

        sessions = SessionStore(tmp)
        session = sessions.create("Smoke session")
        sessions.add_message(session.id, "user", "hello")
        sessions.add_message(session.id, "assistant", "hi", "trace")
        loaded_session, messages = sessions.get(session.id)
        assert loaded_session.title == "Smoke session"
        assert len(messages) == 2
        assert messages[1].trace == "trace"

        eval_file = tmp / "eval.json"
        eval_file.write_text(
            '{"tasks":[{"name":"dry","prompt":"hello","expected_contains":["Dry run ready"]}]}'
        )
        results = run_eval_file(config, eval_file, task_timeout=5)
        assert results[0].passed
        assert results[0].steps == 0
        assert results[0].attempts == 1
        assert results[0].duration_ms >= 0
        assert "passed: 1/1" in render_eval_results(results)
        assert "attempts: 1" in render_eval_results(results)
        eval_output = tmp / "eval-output.json"
        save_eval_results(eval_file, eval_output, results)
        assert '"passed": 1' in eval_output.read_text(encoding="utf-8")

        names = extract_model_names({"models": [{"name": "qwen2.5-coder:7b"}]})
        assert "qwen2.5-coder:7b" in names
        rendered = render_doctor([Check("example", False, "missing", "fix it")])
        assert "missing example" in rendered
    finally:
        shutil.rmtree(tmp)

    print("smoke tests passed")


if __name__ == "__main__":
    main()
