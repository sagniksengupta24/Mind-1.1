from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

from .agent import Agent
from .api import default_api_token, serve_api
from .code_index import CodeIndex, render_file_summary, render_symbol_hits
from .config import AgentConfig
from .doctor import render_doctor, run_doctor, run_doctor_eval
from .eval import render_eval_results, run_eval_file, save_eval_results, save_eval_run
from .file_safety import FileSafetyError, resolve_workspace_path as resolve_safe_workspace_path
from .llm import EmbeddingError, OllamaEmbeddingClient
from .memory import MemoryStore
from .modes import AgentMode, mode_choices, parse_agent_mode
from .mutations import DirtyStateStore, MutationError
from .patches import PatchError, PatchStore
from .project_knowledge import ProjectKnowledgeStore
from .project_map import build_project_map
from .rag import DocStore
from .receipts import ReceiptError, ReceiptStore
from .security import redact_secrets
from .tools import ToolError
from .traces import TraceError, TraceStore
from .version import __version__


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "ask":
        config = build_config(args)
        agent = Agent(config)
        response = agent.ask(args.prompt)
        if args.trace:
            print_trace(response.trace)
        print(response.text)
        return 0

    if args.command == "doctor":
        if getattr(args, "eval", False):
            config = build_config(args)
            return run_doctor_eval(config)
        config = build_config(args)
        checks = run_doctor(
            config.model,
            config.ollama_url,
            provider=config.provider,
            api_key=config.api_key,
            base_url=config.base_url,
        )
        print(render_doctor(checks))
        return 0 if all(check.ok for check in checks) else 2

    if args.command == "serve-api":
        workspace = Path(args.workspace).expanduser().resolve()
        serve_api(
            workspace,
            args.host,
            args.port,
            args.model,
            args.ollama_url,
            mode=args.mode,
            api_token=args.api_token,
            cors_origin=args.cors_origin,
            allow_write=args.allow_write,
            allow_shell=args.allow_shell,
            auto_approve=args.auto_approve,
            max_steps=args.max_steps,
            max_body_bytes=args.max_body_bytes,
            max_concurrent_requests=args.max_concurrent_requests,
            request_timeout_seconds=args.request_timeout_seconds,
        )
        return 0

    if args.command == "chat":
        config = build_config(args)
        agent = Agent(config)
        print("Mind1.1 chat. Type /exit to quit.")
        while True:
            try:
                prompt = input("> ").strip()
            except EOFError:
                print()
                return 0
            if prompt in {"/exit", "/quit"}:
                return 0
            if not prompt:
                continue
            response = agent.ask(prompt)
            if args.trace:
                print_trace(response.trace)
            print(response.text)

    if args.command == "index-docs":
        workspace = Path(args.workspace).expanduser().resolve()
        store = DocStore(workspace)
        embedder = None
        if args.embed:
            embedder = OllamaEmbeddingClient(args.ollama_url, args.embedding_model)
        try:
            require_cli_mutation_policy(args, {"propose", "write-approved", "unsafe"}, "index-docs")
            count = store.index_path(
                resolve_workspace_path(workspace, args.path),
                embedder=embedder,
                embedding_model=args.embedding_model if args.embed else "",
            )
        except (EmbeddingError, ToolError, ValueError) as exc:
            print(f"index error: {exc}", file=sys.stderr)
            return 2
        stats = store.stats()
        suffix = f" Embedded chunks: {stats['embedded_chunks']}." if args.embed else ""
        print(f"Indexed {count} chunks. Total chunks: {stats['chunks']}.{suffix}")
        return 0

    if args.command == "docs-status":
        workspace = Path(args.workspace).expanduser().resolve()
        store = DocStore(workspace)
        print(render_docs_status(store))
        return 0

    if args.command == "search-docs":
        workspace = Path(args.workspace).expanduser().resolve()
        store = DocStore(workspace)
        embedder = None
        if args.embed:
            embedder = OllamaEmbeddingClient(args.ollama_url, args.embedding_model)
        try:
            hits = store.search(
                args.query,
                args.limit,
                embedder=embedder,
                embedding_model=args.embedding_model if args.embed else "",
            )
        except EmbeddingError as exc:
            print(f"embedding error: {exc}", file=sys.stderr)
            return 2
        print(render_doc_hits(hits))
        return 0

    if args.command == "map":
        workspace = Path(args.workspace).expanduser().resolve()
        print(build_project_map(workspace, args.path).render())
        return 0

    if args.command == "index-code":
        workspace = Path(args.workspace).expanduser().resolve()
        index = CodeIndex(workspace)
        try:
            require_cli_mutation_policy(args, {"propose", "write-approved", "unsafe"}, "index-code")
            count = index.index_path(resolve_workspace_path(workspace, args.path))
        except (ToolError, ValueError) as exc:
            print(f"index error: {exc}", file=sys.stderr)
            return 2
        files, symbols = index.stats()
        print(f"Indexed {count} files. Current index: {files} files, {symbols} symbols.")
        return 0

    if args.command == "symbols":
        workspace = Path(args.workspace).expanduser().resolve()
        index = CodeIndex(workspace)
        print(render_symbol_hits(index.search_symbols(args.query, args.limit)))
        return 0

    if args.command == "file-summary":
        workspace = Path(args.workspace).expanduser().resolve()
        index = CodeIndex(workspace)
        try:
            print(render_file_summary(index.file_summary(args.path)))
        except ValueError as exc:
            print(f"index error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "knowledge":
        workspace = Path(args.workspace).expanduser().resolve()
        store = ProjectKnowledgeStore(workspace)
        try:
            if args.knowledge_command == "refresh":
                require_cli_mutation_policy(
                    args, {"propose", "write-approved", "unsafe"}, "knowledge refresh"
                )
                counts = store.refresh(args.path)
                print({**counts, **store.stats()})
            elif args.knowledge_command == "query":
                hits = store.query(args.query, args.limit)
                if not hits:
                    print("(no project knowledge matches)")
                else:
                    for hit in hits:
                        print(
                            f"{hit.entity_type} {hit.name} path={hit.path or '-'} "
                            f"provenance={hit.provenance or '-'} id={hit.entity_id}"
                        )
            elif args.knowledge_command == "status":
                print(store.stats())
            else:
                parser.print_help()
                return 1
        except (ToolError, ValueError) as exc:
            print(f"knowledge error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "eval":
        config = build_config(args)
        results = run_eval_file(
            config,
            Path(args.eval_file),
            args.task_timeout,
            args.repair_attempts,
        )
        print(render_eval_results(results))
        saved_run = save_eval_run(config.workspace, Path(args.eval_file), results, config=config)
        print(f"\nSaved eval run: {saved_run.relative_to(config.workspace)}")
        if args.output:
            output = Path(args.output).expanduser().resolve()
            save_eval_results(Path(args.eval_file), output, results, config=config)
            print(f"\nWrote eval trace: {output}")
        return 0

    if args.command == "remember":
        workspace = Path(args.workspace).expanduser().resolve()
        store = MemoryStore(workspace)
        try:
            require_cli_mutation_policy(args, {"write-approved", "unsafe"}, "remember")
            print(store.remember(args.key, args.value, args.tags, args.source, args.importance))
        except (ToolError, ValueError) as exc:
            print(f"memory error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "memory":
        workspace = Path(args.workspace).expanduser().resolve()
        store = MemoryStore(workspace)
        try:
            if args.memory_command == "list":
                print(render_memories(store.list(args.limit, getattr(args, "tags", ""))))
            elif args.memory_command in {"recall", "search"}:
                print(render_memories(store.recall(args.query, args.limit, getattr(args, "tags", ""))))
            elif args.memory_command == "add":
                require_cli_mutation_policy(args, {"write-approved", "unsafe"}, "memory add")
                print(
                    store.remember(
                        args.key,
                        args.value,
                        args.tags,
                        args.source,
                        args.importance,
                    )
                )
            elif args.memory_command == "update":
                require_cli_mutation_policy(args, {"write-approved", "unsafe"}, "memory update")
                print(store.update(args.id, args.value, args.tags, args.source, args.importance))
            elif args.memory_command == "delete":
                require_cli_mutation_policy(args, {"write-approved", "unsafe"}, "memory delete")
                print(store.delete(args.id))
            else:
                parser.print_help()
                return 1
        except (ToolError, ValueError) as exc:
            print(f"memory error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "patch":
        workspace = Path(args.workspace).expanduser().resolve()
        store = PatchStore(workspace)
        try:
            if args.patch_command == "list":
                print(store.render_list())
            elif args.patch_command == "show":
                print(store.show(args.id))
            elif args.patch_command == "apply":
                require_patch_apply_policy(args)
                mode = parse_agent_mode(getattr(args, "mode", AgentMode.READ_ONLY.value))
                print(
                    store.apply(
                        args.id,
                        mode=mode.value,
                        allow_write=False,
                        approved=bool(args.yes),
                        source="cli:patch apply",
                    )
                )
            elif args.patch_command == "discard":
                require_cli_mutation_policy(args, {"write-approved", "unsafe"}, "patch discard")
                print(store.discard(args.id))
            elif args.patch_command == "test":
                config = build_config(args)
                agent = Agent(config)
                result = agent.tools.call(
                    "test_patch",
                    {"id": args.id, "command": args.command_to_run},
                )
                print(result.text)
            else:
                parser.print_help()
                return 1
        except (PatchError, ToolError, ValueError) as exc:
            print(f"patch error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "receipts":
        workspace = Path(args.workspace).expanduser().resolve()
        store = ReceiptStore(workspace)
        try:
            if args.receipts_command == "list":
                print(store.render_list(args.limit))
            elif args.receipts_command == "show":
                print(store.render_show(args.receipt_id))
            elif args.receipts_command == "verify-chain":
                import json
                from .receipts import verify_receipt_chain
                res = verify_receipt_chain(workspace)
                print(json.dumps(res, indent=2, sort_keys=True))
                if res["status"] == "invalid":
                    return 2
                return 0
            else:
                parser.print_help()
                return 1
        except ReceiptError as exc:
            print(f"receipt error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "rollback":
        workspace = Path(args.workspace).expanduser().resolve()
        store = ReceiptStore(workspace)
        try:
            require_rollback_policy(args)
            mode = parse_agent_mode(getattr(args, "mode", AgentMode.READ_ONLY.value))
            receipt = store.rollback(
                args.receipt_id,
                mode=mode.value,
                approved=bool(args.yes),
                force=bool(args.force),
                source="cli:rollback",
            )
        except (ReceiptError, ToolError, ValueError) as exc:
            print(f"rollback error: {exc}", file=sys.stderr)
            return 2
        print(
            f"Rolled back {receipt['relative_file_path']}. "
            f"Receipt {receipt['receipt_id']}."
        )
        return 0

    if args.command == "traces":
        workspace = Path(args.workspace).expanduser().resolve()
        store = TraceStore(workspace)
        try:
            if args.traces_command == "list":
                print(store.render_list(args.limit))
            elif args.traces_command == "show":
                print(store.render_show(args.identifier))
            elif args.traces_command == "verify-chain":
                import json
                from .traces import verify_trace_chain
                res = verify_trace_chain(workspace)
                print(json.dumps(res, indent=2, sort_keys=True))
                if res["status"] == "invalid":
                    return 2
                return 0
            else:
                parser.print_help()
                return 1
        except TraceError as exc:
            print(f"trace error: {exc}", file=sys.stderr)
            return 2
        return 0

    if args.command == "mutations":
        workspace = Path(args.workspace).expanduser().resolve()
        store = DirtyStateStore(workspace)
        try:
            if args.mutations_command == "dirty-list":
                print(store.render_list(args.limit))
            elif args.mutations_command == "dirty-show":
                print(store.render_show(args.dirty_id))
            else:
                parser.print_help()
                return 1
        except MutationError as exc:
            print(f"mutation error: {exc}", file=sys.stderr)
            return 2
        return 0

    parser.print_help()
    return 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="mind01")
    parser.add_argument("--version", action="version", version=f"mind01 {__version__}")
    sub = parser.add_subparsers(dest="command")

    ask = sub.add_parser("ask", help="Run one prompt")
    add_common(ask)
    ask.add_argument("prompt")

    doctor = sub.add_parser("doctor", help="Check local runtime and model setup")
    add_common(doctor)
    doctor.add_argument("--eval", action="store_true", help="Run the full evaluation suite")

    api = sub.add_parser("serve-api", help="Run local HTTP API for a frontend")
    api.add_argument("--workspace", default=".")
    api.add_argument("--host", default="127.0.0.1")
    api.add_argument("--port", type=int, default=8765)
    api.add_argument("--model", default="qwen2.5-coder:7b")
    api.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    api.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    api.add_argument("--api-token", default=default_api_token())
    api.add_argument("--cors-origin", default="http://localhost:3000")
    api.add_argument("--allow-write", action="store_true", help="Server maximum: permit source mutations in elevated modes")
    api.add_argument("--allow-shell", action="store_true", help="Server maximum: permit allowlisted host command execution")
    api.add_argument("--auto-approve", action="store_true", help="Permit authenticated non-interactive API mutations")
    api.add_argument("--max-steps", type=int, default=12, help="Hard server step limit per chat request")
    api.add_argument("--max-body-bytes", type=int, default=1_000_000)
    api.add_argument("--max-concurrent-requests", type=int, default=4)
    api.add_argument("--request-timeout-seconds", type=int, default=180)

    chat = sub.add_parser("chat", help="Run interactive chat")
    add_common(chat)

    index_docs = sub.add_parser("index-docs", help="Index docs for RAG search")
    index_docs.add_argument("path")
    index_docs.add_argument("--workspace", default=".")
    index_docs.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    index_docs.add_argument("--embed", action="store_true", help="Store Ollama embeddings for semantic search")
    index_docs.add_argument("--embedding-model", default="nomic-embed-text")
    index_docs.add_argument("--ollama-url", default="http://127.0.0.1:11434")

    docs_status = sub.add_parser("docs-status", help="Show doc index freshness")
    docs_status.add_argument("--workspace", default=".")

    search_docs = sub.add_parser("search-docs", help="Search indexed docs")
    search_docs.add_argument("query")
    search_docs.add_argument("--workspace", default=".")
    search_docs.add_argument("--limit", type=int, default=6)
    search_docs.add_argument("--embed", action="store_true", help="Use stored embeddings for semantic search")
    search_docs.add_argument("--embedding-model", default="nomic-embed-text")
    search_docs.add_argument("--ollama-url", default="http://127.0.0.1:11434")

    project_map = sub.add_parser("map", help="Print a compact project map")
    project_map.add_argument("--workspace", default=".")
    project_map.add_argument("--path", default=".")

    index_code = sub.add_parser("index-code", help="Index code symbols")
    index_code.add_argument("--workspace", default=".")
    index_code.add_argument("--path", default=".")
    index_code.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)

    symbols = sub.add_parser("symbols", help="Search indexed code symbols")
    symbols.add_argument("query")
    symbols.add_argument("--workspace", default=".")
    symbols.add_argument("--limit", type=int, default=20)

    file_summary = sub.add_parser("file-summary", help="Show indexed imports and symbols for a file")
    file_summary.add_argument("path")
    file_summary.add_argument("--workspace", default=".")

    knowledge = sub.add_parser("knowledge", help="Manage provenance-aware project knowledge")
    knowledge.add_argument("--workspace", default=".")
    knowledge_sub = knowledge.add_subparsers(dest="knowledge_command")
    knowledge_refresh = knowledge_sub.add_parser("refresh", help="Refresh project entities and relations")
    knowledge_refresh.add_argument("--path", default=".")
    knowledge_refresh.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    knowledge_refresh.add_argument("--workspace", default=argparse.SUPPRESS)
    knowledge_query = knowledge_sub.add_parser("query", help="Query project entities")
    knowledge_query.add_argument("query")
    knowledge_query.add_argument("--limit", type=int, default=20)
    knowledge_query.add_argument("--workspace", default=argparse.SUPPRESS)
    knowledge_status = knowledge_sub.add_parser("status", help="Show project knowledge statistics")
    knowledge_status.add_argument("--workspace", default=argparse.SUPPRESS)

    eval_cmd = sub.add_parser("eval", help="Run a small JSON eval file")
    add_common(eval_cmd)
    eval_cmd.add_argument("eval_file")
    eval_cmd.add_argument(
        "--task-timeout",
        type=int,
        default=120,
        help="Seconds before one eval task is marked timed out; use 0 to disable",
    )
    eval_cmd.add_argument(
        "--repair-attempts",
        type=int,
        default=1,
        help="Extra correction attempts when an eval answer misses expected criteria",
    )
    eval_cmd.add_argument("--output", help="Write structured eval results to JSON")

    remember = sub.add_parser("remember", help="Store a memory")
    remember.add_argument("key")
    remember.add_argument("value")
    remember.add_argument("--tags", default="")
    remember.add_argument("--source", default="cli")
    remember.add_argument("--importance", type=int, default=1)
    remember.add_argument("--workspace", default=".")
    remember.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)

    memory = sub.add_parser("memory", help="Manage saved memories")
    memory.add_argument("--workspace", default=".")
    memory_sub = memory.add_subparsers(dest="memory_command")
    memory_add = memory_sub.add_parser("add", help="Add a tagged memory")
    memory_add.add_argument("key")
    memory_add.add_argument("value")
    memory_add.add_argument("--tags", default="")
    memory_add.add_argument("--source", default="cli")
    memory_add.add_argument("--importance", type=int, default=1)
    memory_add.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    memory_add.add_argument("--workspace", default=argparse.SUPPRESS)
    memory_list = memory_sub.add_parser("list", help="List recent memories")
    memory_list.add_argument("--limit", type=int, default=50)
    memory_list.add_argument("--tags", default="")
    memory_list.add_argument("--workspace", default=argparse.SUPPRESS)
    memory_recall = memory_sub.add_parser("recall", help="Search saved memories")
    memory_recall.add_argument("query")
    memory_recall.add_argument("--limit", type=int, default=8)
    memory_recall.add_argument("--tags", default="")
    memory_recall.add_argument("--workspace", default=argparse.SUPPRESS)
    memory_search = memory_sub.add_parser("search", help="Search saved memories")
    memory_search.add_argument("query")
    memory_search.add_argument("--limit", type=int, default=8)
    memory_search.add_argument("--tags", default="")
    memory_search.add_argument("--workspace", default=argparse.SUPPRESS)
    memory_update = memory_sub.add_parser("update", help="Update a memory by id")
    memory_update.add_argument("id", type=int)
    memory_update.add_argument("value")
    memory_update.add_argument("--tags")
    memory_update.add_argument("--source")
    memory_update.add_argument("--importance", type=int)
    memory_update.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    memory_update.add_argument("--workspace", default=argparse.SUPPRESS)
    memory_delete = memory_sub.add_parser("delete", help="Delete a memory by id")
    memory_delete.add_argument("id", type=int)
    memory_delete.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    memory_delete.add_argument("--workspace", default=argparse.SUPPRESS)

    patch = sub.add_parser("patch", help="Manage pending patch proposals")
    patch.add_argument("--workspace", default=".")
    patch_sub = patch.add_subparsers(dest="patch_command")
    patch_list = patch_sub.add_parser("list", help="List pending patches")
    patch_list.add_argument("--workspace", default=argparse.SUPPRESS)
    patch_show = patch_sub.add_parser("show", help="Show a patch diff")
    patch_show.add_argument("id", type=int)
    patch_show.add_argument("--workspace", default=argparse.SUPPRESS)
    patch_apply = patch_sub.add_parser("apply", help="Apply a patch")
    patch_apply.add_argument("id", type=int)
    patch_apply.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    patch_apply.add_argument("--yes", action="store_true", help="Apply without an interactive approval prompt")
    patch_apply.add_argument("--workspace", default=argparse.SUPPRESS)
    patch_discard = patch_sub.add_parser("discard", help="Discard a patch")
    patch_discard.add_argument("id", type=int)
    patch_discard.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    patch_discard.add_argument("--workspace", default=argparse.SUPPRESS)
    patch_test = patch_sub.add_parser("test", help="Test a patch in a temporary copy")
    patch_test.add_argument("id", type=int)
    patch_test.add_argument("--command-to-run", default="python3 -B tests/smoke_test.py")
    add_common(patch_test)

    receipts = sub.add_parser("receipts", help="Inspect verified write receipts")
    receipts.add_argument("--workspace", default=".")
    receipts_sub = receipts.add_subparsers(dest="receipts_command")
    receipts_list = receipts_sub.add_parser("list", help="List recent receipts")
    receipts_list.add_argument("--limit", type=int, default=50)
    receipts_list.add_argument("--workspace", default=argparse.SUPPRESS)
    receipts_show = receipts_sub.add_parser("show", help="Show one receipt JSON")
    receipts_show.add_argument("receipt_id")
    receipts_show.add_argument("--workspace", default=argparse.SUPPRESS)
    receipts_verify = receipts_sub.add_parser("verify-chain", help="Verify receipt chain integrity")
    receipts_verify.add_argument("--workspace", default=argparse.SUPPRESS)

    rollback = sub.add_parser("rollback", help="Rollback a successful write receipt")
    rollback.add_argument("receipt_id")
    rollback.add_argument("--workspace", default=".")
    rollback.add_argument("--mode", choices=mode_choices(), default=AgentMode.READ_ONLY.value)
    rollback.add_argument("--yes", action="store_true", help="Confirm rollback after review")
    rollback.add_argument("--force", action="store_true", help="Rollback even if current hash differs")

    traces = sub.add_parser("traces", help="Inspect persistent JSONL traces")
    traces.add_argument("--workspace", default=".")
    traces_sub = traces.add_subparsers(dest="traces_command")
    traces_list = traces_sub.add_parser("list", help="List trace files")
    traces_list.add_argument("--limit", type=int, default=20)
    traces_list.add_argument("--workspace", default=argparse.SUPPRESS)
    traces_show = traces_sub.add_parser("show", help="Show one trace file or event")
    traces_show.add_argument("identifier")
    traces_show.add_argument("--workspace", default=argparse.SUPPRESS)
    traces_verify = traces_sub.add_parser("verify-chain", help="Verify trace chain integrity")
    traces_verify.add_argument("--workspace", default=argparse.SUPPRESS)

    mutations = sub.add_parser("mutations", help="Inspect mutation transaction state")
    mutations.add_argument("--workspace", default=".")
    mutations_sub = mutations.add_subparsers(dest="mutations_command")
    dirty_list = mutations_sub.add_parser("dirty-list", help="List dirty mutation records")
    dirty_list.add_argument("--limit", type=int, default=50)
    dirty_list.add_argument("--workspace", default=argparse.SUPPRESS)
    dirty_show = mutations_sub.add_parser("dirty-show", help="Show one dirty mutation record")
    dirty_show.add_argument("dirty_id")
    dirty_show.add_argument("--workspace", default=argparse.SUPPRESS)

    return parser


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--model", default=os.environ.get("LLM_MODEL", "qwen2.5-coder:7b"))
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434")
    parser.add_argument(
        "--provider",
        choices=("ollama", "openrouter", "openai_compatible", "openai"),
        default=None,
        help=(
            "Where inference runs. 'ollama' (default) uses your local server. "
            "'openrouter' or 'openai_compatible' call a cloud, OpenAI-compatible "
            "API instead — no local model download/run. Falls back to $LLM_PROVIDER, "
            "then 'ollama'."
        ),
    )
    parser.add_argument(
        "--api-key",
        default=None,
        help="Cloud provider API key. Falls back to $OPENROUTER_API_KEY / $LLM_API_KEY.",
    )
    parser.add_argument(
        "--base-url",
        default=None,
        help=(
            "Cloud provider base URL (e.g. https://openrouter.ai/api/v1). "
            "Defaults to OpenRouter's URL when --provider openrouter is used. "
            "Falls back to $LLM_BASE_URL."
        ),
    )
    parser.add_argument(
        "--fallback-models",
        default=None,
        help=(
            "Comma-separated model IDs to try in order if --model fails "
            "(rate limit, 5xx, model unavailable). Falls back to $LLM_FALLBACK_MODELS."
        ),
    )
    parser.add_argument("--max-steps", type=int, default=8)
    parser.add_argument("--yes", action="store_true", help="Auto-approve edits/commands")
    parser.add_argument("--dry-run", action="store_true", help="Skip model calls")
    parser.add_argument("--trace", action="store_true", help="Show tool loop events")
    parser.add_argument(
        "--mode",
        choices=mode_choices(),
        default=AgentMode.READ_ONLY.value,
        help="Tool execution mode",
    )
    parser.add_argument(
        "--allow-write",
        action="store_true",
        help="Allow source file writes from write_file/edit_file tools",
    )
    parser.add_argument(
        "--allow-shell",
        action="store_true",
        help="Allow allowlisted command execution from run_command tool",
    )
    parser.add_argument(
        "--semantic-router",
        choices=("legacy", "v2", "compare"),
        default="legacy",
        help="Semantic router activation: legacy, opt-in v2, or shadow comparison",
    )


def build_config(args: argparse.Namespace) -> AgentConfig:
    fallback_models_arg = getattr(args, "fallback_models", None)
    fallback_models = (
        tuple(item.strip() for item in fallback_models_arg.split(",") if item.strip())
        if fallback_models_arg
        else None
    )
    return AgentConfig.build(
        workspace=args.workspace,
        model=args.model,
        ollama_url=args.ollama_url,
        max_steps=args.max_steps,
        yes=args.yes,
        dry_run=args.dry_run,
        trace=getattr(args, "trace", False),
        allow_write=getattr(args, "allow_write", False),
        allow_shell=getattr(args, "allow_shell", False),
        mode=getattr(args, "mode", AgentMode.READ_ONLY.value),
        semantic_router=getattr(args, "semantic_router", "legacy"),
        provider=getattr(args, "provider", None),
        api_key=getattr(args, "api_key", None),
        base_url=getattr(args, "base_url", None),
        fallback_models=fallback_models,
    )


def require_patch_apply_policy(args: argparse.Namespace) -> None:
    mode = parse_agent_mode(getattr(args, "mode", AgentMode.READ_ONLY.value))
    if mode not in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
        raise ToolError(
            f"patch apply is not allowed in mode `{mode.value}`. "
            "Use `--mode write-approved --yes` after reviewing the patch."
        )
    if not getattr(args, "yes", False):
        raise ToolError("patch apply requires `--yes` after review in write-approved mode.")


def require_rollback_policy(args: argparse.Namespace) -> None:
    mode = parse_agent_mode(getattr(args, "mode", AgentMode.READ_ONLY.value))
    if mode not in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
        raise ToolError(
            f"rollback is not allowed in mode `{mode.value}`. "
            "Use `--mode write-approved --yes` after reviewing the receipt."
        )
    if not getattr(args, "yes", False):
        raise ToolError("rollback requires `--yes` after reviewing the receipt.")


def require_cli_mutation_policy(
    args: argparse.Namespace,
    allowed_modes: set[str],
    action: str,
) -> None:
    mode = parse_agent_mode(getattr(args, "mode", AgentMode.READ_ONLY.value))
    if mode.value not in allowed_modes:
        allowed = ", ".join(sorted(allowed_modes))
        raise ToolError(
            f"{action} mutates Mind runtime state and is not allowed in "
            f"mode `{mode.value}`. Allowed modes: {allowed}."
        )


def print_trace(events: list[str]) -> None:
    if not events:
        return
    print("[trace]")
    for event in events:
        print(f"- {event}")
    print("[/trace]")


def render_memories(memories) -> str:  # type: ignore[no-untyped-def]
    items = list(memories)
    if not items:
        return "(no memories)"
    return "\n\n".join(
        (
            f"{item.id}: {item.key} [{item.tags}] source={item.source} "
            f"importance={item.importance} use_count={item.use_count} "
            f"created_at={item.created_at} updated_at={item.updated_at} "
            f"score={item.score:.1f}\n{item.value}"
        )
        for item in items
    )


def render_doc_hits(hits) -> str:  # type: ignore[no-untyped-def]
    if not hits:
        return "(no docs found; run `index-docs` first)"
    rendered = []
    for hit in hits:
        vector = f" vector={hit.vector_score:.3f}" if hit.vector_score else ""
        stale = " stale=true" if hit.stale else ""
        rendered.append(
            f"{hit.citation} score={hit.score}{vector}{stale}\n"
            f"{redact_secrets(hit.chunk[:1200])}"
        )
    return "\n\n".join(rendered)


def render_docs_status(store: DocStore) -> str:
    stats = store.stats()
    stale = store.stale_files()
    lines = [
        f"files={stats['files']}",
        f"chunks={stats['chunks']}",
        f"embedded_chunks={stats['embedded_chunks']}",
        f"stale_files={len(stale)}",
    ]
    if stale:
        lines.append("")
        lines.extend(f"{item.path}: {item.reason}" for item in stale)
    return "\n".join(lines)


def resolve_workspace_path(workspace: Path, raw_path: str) -> Path:
    try:
        return resolve_safe_workspace_path(workspace, raw_path)
    except FileSafetyError as exc:
        raise ValueError(str(exc)) from exc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
