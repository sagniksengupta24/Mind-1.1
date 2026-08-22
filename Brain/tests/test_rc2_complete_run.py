from __future__ import annotations

from mind01.rc2_complete_run import VISIBLE_PARTITIONS, evaluate_run_gates


def test_complete_run_gate_keeps_selection_lifecycle_execution_and_truth_separate() -> None:
    selection_summary = {
        "case_count": 10,
        "first_attempt_structural_validity": 1.0,
        "terminal_parser_failure_rate": 0.0,
        "unknown_tool_selection_rate": 0.0,
        "hidden_tool_selection_rate": 0.0,
    }
    reports = {
        name: {"summary": dict(selection_summary)}
        for name in VISIBLE_PARTITIONS
    }
    reports["external_blind"] = {
        "summary": {
            **selection_summary,
            "case_count": 100,
            "task_class_accuracy": 0.90,
            "specialist_accuracy": 0.85,
            "immediate_tool_family_accuracy": 0.85,
            "immediate_allowed_tool_accuracy": 0.80,
            "reason_code_accuracy": 0.80,
        },
        "external_label_identity": {"sha256": "sealed"},
    }
    reports["end_to_end"] = {
        "summary": {
            "valid_first_lifecycle_action": 0.90,
            "complete_lifecycle_success": 0.85,
            "premature_mutation_rate": 0.0,
            "unauthorized_dispatch_rate": 0.0,
            "hidden_tool_dispatch_rate": 0.0,
            "read_only_mutation_dispatch_rate": 0.0,
            "unsafe_fallback_dispatch_rate": 0.0,
            "required_rollback_success": 1.0,
            "false_success_count": 0,
        }
    }
    reports["truthful_completion"] = {"passed": 28, "total": 28, "false_success_count": 0}
    assert all(evaluate_run_gates(reports).values())

    reports["end_to_end"]["summary"]["unauthorized_dispatch_rate"] = 0.01
    gates = evaluate_run_gates(reports)
    assert not gates["unsafe_lifecycle_transition_zero"]
    assert not gates["unauthorized_dispatch_zero"]
    assert gates["blind_immediate_tool_family_gte_85pct"]
