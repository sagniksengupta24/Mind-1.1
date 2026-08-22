from __future__ import annotations

import json
import shutil
import tempfile
import urllib.error
from io import BytesIO
from pathlib import Path
from unittest.mock import patch

from mind01.action_parser import ResponseMode, canonical_response_schema, parse_action_output
from mind01.agent import _runtime_completion_status, _visible_tools
from mind01.agent import Agent
from mind01.config import AgentConfig
from mind01.eval import run_mock_protocol_regression
from mind01.eval_harness import _fixture_acceptance, aggregate_parser_report, build_action_report
from mind01.eval_schema import load_action_suite
from mind01.llm import OllamaClient
from mind01.llm import LLMError
from mind01.modes import AgentMode
from mind01.routing import HierarchicalRouter
from mind01.state import AgentState
from mind01.tools.schemas import SCHEMA_BY_NAME
from mind01.verification import VerificationEngine
from mind01.completion import VerificationEvidence, normalize_completion_status


class FakeResponse:
    def __init__(self, payload: dict) -> None:
        self.payload = payload

    def __enter__(self):  # type: ignore[no-untyped-def]
        return self

    def __exit__(self, *args):  # type: ignore[no-untyped-def]
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode()


def test_action_suite_is_versioned_and_has_fifty_cases() -> None:
    suite = load_action_suite()
    assert suite.benchmark_version == "action-reliability-v1"
    assert len(suite.cases) == 50
    assert len({case.id for case in suite.cases}) == 50


def test_every_visible_schema_matches_runtime_validation() -> None:
    suite = load_action_suite()
    for case in suite.cases:
        schema = canonical_response_schema(case.mode, case.allowed_tools, SCHEMA_BY_NAME, repair_response_type=case.repair_response_type)
        assert schema
        assert set(case.allowed_tools).issubset(SCHEMA_BY_NAME)


def test_mock_protocol_regression_is_explicitly_mocked() -> None:
    result = run_mock_protocol_regression()
    assert result["metrics_source"] == "mock_model"
    assert result["passed"] == result["total"] == 25


def test_inspection_phase_hides_mutation_tools() -> None:
    route = HierarchicalRouter().route("Modify agent.py to add a retry", Path("."))
    state = AgentState("x", AgentMode.WRITE_APPROVED.value, 4)
    initial = _visible_tools(route, state, False)
    assert "read_file" in initial
    assert "write_file" not in initial
    mutation = _visible_tools(route, state, True, allow_write=True)
    assert "write_file" in mutation


def test_server_route_still_limits_visible_tools() -> None:
    route = HierarchicalRouter().route("Explain agent.py", Path("."))
    state = AgentState("x", AgentMode.UNSAFE.value, 4)
    assert "write_file" not in _visible_tools(route, state, True)


def test_runtime_downgrades_verified_without_evidence() -> None:
    parsed = parse_action_output(json.dumps({"schema_version":"1.0","response_type":"final","status":"verified","summary":"done","evidence_refs":[]}))
    state = AgentState("x", "read-only", 1)
    assert _runtime_completion_status(parsed, state) == "unverified"


def test_runtime_accepts_verified_with_referenced_evidence() -> None:
    parsed = parse_action_output(json.dumps({"schema_version":"1.0","response_type":"final","status":"verified","summary":"done","evidence_refs":["verification-001"]}))
    state = AgentState("x", "write-approved", 1)
    state.evidence_refs["verification-001"] = {"status":"passed"}
    state.verification_results.append({"status":"passed"})
    assert _runtime_completion_status(parsed, state) == "verified"


def test_ollama_json_schema_capability_detection_supported() -> None:
    client = OllamaClient("http://127.0.0.1:11434", "model")
    with patch("urllib.request.urlopen", return_value=FakeResponse({"version":"0.5.7"})):
        assert client.supports_json_schema()
    assert client.last_server_version == "0.5.7"


def test_ollama_json_schema_capability_detection_fallback() -> None:
    client = OllamaClient("http://127.0.0.1:11434", "model")
    with patch("urllib.request.urlopen", side_effect=OSError("offline")):
        assert not client.supports_json_schema()


def test_ollama_missing_model_404_is_reported_as_missing_model() -> None:
    client = OllamaClient("http://127.0.0.1:11434", "qwen2.5-coder:7b")
    error = urllib.error.HTTPError(
        "http://127.0.0.1:11434/api/chat",
        404,
        "Not Found",
        {},
        BytesIO(b'{"error":"model \'qwen2.5-coder:7b\' not found"}'),
    )
    with patch.object(client, "supports_json_schema", return_value=True):
        with patch("urllib.request.urlopen", side_effect=error):
            try:
                client.chat([{"role": "user", "content": "hello"}], response_schema={"type": "object"})
            except LLMError as exc:
                assert exc.status_code == 404
                assert "ollama pull qwen2.5-coder:7b" in str(exc)
                assert "structured request" not in str(exc)
            else:
                raise AssertionError("Expected missing-model LLMError")


def test_ollama_schema_rejection_falls_back_only_for_400_or_422() -> None:
    client = OllamaClient("http://127.0.0.1:11434", "model")
    with patch.object(client, "supports_json_schema", return_value=True):
        with patch.object(
            client,
            "_chat_payload",
            side_effect=[LLMError("bad schema", status_code=400), "fallback"],
        ) as request:
            assert client.chat([], response_schema={"type": "object"}) == "fallback"
    assert request.call_count == 2
    assert request.call_args_list[1].args[0]["format"] == "json"
    assert client.last_output_mode == "json_fallback"


def test_real_mutation_templates_fail_preconditions() -> None:
    source = Path(__file__).resolve().parents[1] / "mind01" / "eval_suites" / "real_mutation"
    with tempfile.TemporaryDirectory(prefix="mind-fixture-test-") as directory:
        root = Path(directory)
        syntax = root / "syntax"
        shutil.copytree(source / "syntax", syntax)
        (syntax / "broken.py.fixture").rename(syntax / "broken.py")
        assert not _fixture_acceptance(syntax, "compileall")[0]
        failing = root / "failing"
        shutil.copytree(source / "failing_test", failing)
        (failing / "test_calc.py.fixture").rename(failing / "test_calc.py")
        assert not _fixture_acceptance(failing, "pytest")[0]
        feature = root / "feature"
        shutil.copytree(source / "feature", feature)
        assert not _fixture_acceptance(feature, "hidden_feature")[0]


def test_invalid_syntax_is_not_shipped_as_python_source() -> None:
    fixture = Path(__file__).resolve().parents[1] / "mind01" / "eval_suites" / "real_mutation" / "syntax"
    assert (fixture / "broken.py.fixture").exists()
    assert not (fixture / "broken.py").exists()


def test_parser_report_aggregates_without_raw_output(tmp_path: Path) -> None:
    run = tmp_path / "run"
    run.mkdir()
    report = {
        "results": [
            {
                "first_attempt_valid": False,
                "terminal_parser_failure": False,
                "parser_failures": [{"error_code":"MALFORMED_JSON","phase":"inspection","model_metadata":{"model":"m"},"recovered":False}],
            }
        ]
    }
    (run / "report.json").write_text(json.dumps(report), encoding="utf-8")
    payload = aggregate_parser_report(run)
    assert payload["frequency_by_category"] == {"MALFORMED_JSON": 1}
    assert (run / "parser_report.json").exists()


def test_python_verifier_rejects_definitions_trapped_in_strings(tmp_path: Path) -> None:
    (tmp_path / "module.py").write_text('"""\ndef hidden():\n    return 1\n"""\n', encoding="utf-8")
    results = VerificationEngine(tmp_path).verify_paths(["module.py"])
    structure = next(item for item in results if item.check == "python-executable-structure")
    assert structure.status == "failed"
    assert structure.blocking
    assert structure.failure_category == "non_executable_source"


def test_completion_overrides_failed_when_acceptance_proves_success() -> None:
    evidence = VerificationEvidence("acceptance", ["pytest"], "passed", 0, 0.1)
    status, uncertainty = normalize_completion_status("failed", verification=[evidence])
    assert status == "verified"
    assert not uncertainty


def test_non_executable_mutation_is_rolled_back_then_repaired(tmp_path: Path) -> None:
    target = tmp_path / "module.py"
    target.write_text("value = 0\n", encoding="utf-8")
    config = AgentConfig.build(
        str(tmp_path), "model", "http://127.0.0.1:11434", 5, True, False,
        allow_write=True, mode=AgentMode.WRITE_APPROVED,
    )
    agent = Agent(config)
    replies = [
        json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"read_file","arguments":{"path":"module.py"}}),
        json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"write_file","arguments":{"path":"module.py","content":"\"\"\"\ndef feature():\n    return 1\n\"\"\"\n"}}),
        json.dumps({"schema_version":"1.0","response_type":"tool_call","tool":"write_file","arguments":{"path":"module.py","content":"def feature():\n    return 1\n"}}),
        json.dumps({"schema_version":"1.0","response_type":"final","status":"verified","summary":"Implemented executable feature.","evidence_refs":["verification-003"]}),
    ]
    with patch.object(agent.llm, "chat", side_effect=replies):
        response = agent.ask("Modify module.py to add an executable feature")
    assert target.read_text(encoding="utf-8").startswith("def feature")
    assert any("rolled back receipt" in item for item in response.trace)
    assert response.completion_status == "partially_verified"
    assert "R-BEHAVIOR" in response.completion_contract["unmet_requirements"]
    assert "R-REGRESSION" in response.completion_contract["unmet_requirements"]
    assert "R-IMPORT" in response.completion_contract["unmet_requirements"]
