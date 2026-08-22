from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path

from mind01 import __version__
from mind01.config import AgentConfig
from mind01.eval import (
    category_summary,
    main as eval_main,
    render_eval_results,
    run_eval_file,
    save_eval_run,
)


def run_eval_suite_tests() -> None:
    repo = Path(__file__).resolve().parents[1]
    expected = {
        "coding.json",
        "safety.json",
        "docs_rag.json",
        "memory.json",
        "indic_languages.json",
        "semiconductor.json",
        "repo_analysis.json",
        "full_suite.json",
    }
    eval_files = sorted((repo / "evals" / name) for name in expected)
    assert all(path.exists() for path in eval_files)
    for path in eval_files:
        data = json.loads(path.read_text(encoding="utf-8"))
        assert isinstance(data.get("tasks"), list), path

    tmp = Path(tempfile.mkdtemp(prefix="mind01-evals-"))
    try:
        config = AgentConfig.build(
            workspace=str(tmp),
            model="qwen2.5-coder:7b",
            ollama_url="http://127.0.0.1:11434",
            max_steps=1,
            yes=True,
            dry_run=True,
        )
        results = run_eval_file(config, repo / "evals" / "full_suite.json", task_timeout=5)
        assert results
        assert all(result.passed for result in results)
        summary = category_summary(results)
        assert summary["coding"]["passed"] == 1
        rendered = render_eval_results(results)
        assert "categories:" in rendered
        assert "coding: 1/1" in rendered
        output = save_eval_run(tmp, repo / "evals" / "full_suite.json", results, config=config)
        assert output.exists()
        payload = json.loads(output.read_text(encoding="utf-8"))
        assert payload["summary"]["passed"] == len(results)
        assert payload["summary"]["categories"]["semiconductor"]["passed"] == 1
        assert payload["metadata"]["mind_version"] == __version__
        assert payload["metadata"]["model"] == config.model
        assert "false_success_count" in payload["summary"]

        invalid = tmp / "invalid_eval.json"
        invalid.write_text('{"tasks":[{"name":"bad"}]}', encoding="utf-8")
        try:
            run_eval_file(config, invalid, task_timeout=5)
            raise AssertionError("invalid eval file did not fail clearly")
        except ValueError as exc:
            assert "missing required `prompt`" in str(exc)
    finally:
        shutil.rmtree(tmp)


def test_eval_suite_regressions() -> None:
    run_eval_suite_tests()


def test_eval_validate_and_run_output_are_separately_scoped(
    tmp_path: Path,
    capsys,
) -> None:
    assert eval_main(["validate"]) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["truthful_completion_cases"] == 28
    assert validated["semantic_routing"]["total_cases"] == 260
    assert validated["semantic_routing"]["blind_labels_present"] is False

    output = tmp_path / "truthful-completion.json"
    assert eval_main(["run", "--suite", "truthful-completion", "--output", str(output)]) == 0
    rendered = json.loads(capsys.readouterr().out)
    retained = json.loads(output.read_text(encoding="utf-8"))
    assert retained == rendered
    assert retained["false_success_count"] == 0

    semantic_output = tmp_path / "semantic-development.json"
    assert eval_main(
        [
            "run",
            "--suite",
            "semantic-routing",
            "--partition",
            "development",
            "--output",
            str(semantic_output),
        ]
    ) == 0
    capsys.readouterr()
    semantic = json.loads(semantic_output.read_text(encoding="utf-8"))
    assert semantic["passed"] == semantic["total"] == 60
    assert semantic["metrics_source"] == "deterministic_router"

    assert eval_main(["run", "--suite", "semantic-routing"]) == 1
    full_semantic = json.loads(capsys.readouterr().out)
    assert full_semantic["failure_taxonomy"] == {"mutation_intent": 14}
