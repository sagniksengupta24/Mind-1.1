from __future__ import annotations

from copy import deepcopy

from mind01.annotation_v3 import annotation_schema, derive_policy_constraints, validate_annotation


def case(*, mode: str = "propose", write: bool = False, operation: str = "propose_existing") -> dict:
    return {
        "case_id": "calibration-test",
        "agent_mode": mode,
        "capabilities": {"workspace_read": True, "workspace_write": write, "shell": False, "network": False},
        "public_facts": {
            "requested_operation": operation,
            "target_state": "exists_unique",
            "route_state": "none",
            "unsafe_operation": False,
            "prompt_injection": False,
            "unsupported_operation": False,
            "self_contained": False,
            "repository_resolvable": False,
        },
    }


def valid_proposal_label() -> dict:
    return {
        "task_class": "planning",
        "specialist": "implementation",
        "immediate_tool_family": "file_inspection",
        "allowed_immediate_tool_families": ["file_inspection"],
        "allowed_immediate_tools": ["read_file"],
        "terminal_tool_family": "mutation_proposal",
        "allowed_terminal_tools": ["propose_edit_file"],
        "required_lifecycle": [
            {"phase": "inspection", "allowed_tools": ["read_file"]},
            {"phase": "proposal", "allowed_tools": ["propose_edit_file"]},
        ],
        "allowed_alternative_lifecycles": [],
        "response_mode": "action",
        "reason_code": "existing_file_patch_proposal",
        "risk_level": "medium",
        "user_mutation_goal": True,
        "immediate_action_side_effect": False,
        "terminal_mutation_expected": True,
        "annotation_confidence": 0.95,
        "ambiguities": [],
        "rationale_codes": ["existing_target_requires_inspection", "proposal_only"],
    }


def test_policy_derivation_blocks_read_only_live_mutation() -> None:
    constraints = derive_policy_constraints(case(mode="read_only", operation="apply_existing"))
    assert constraints.must_block
    assert not constraints.mutation_execution_permitted
    assert "edit_file" in constraints.forbidden_tools


def test_valid_existing_file_proposal_passes_consistency() -> None:
    item = case()
    assert validate_annotation(item, valid_proposal_label()) == []


def test_consistency_rejects_missing_inspection_and_live_write_in_propose_mode() -> None:
    item = case()
    label = deepcopy(valid_proposal_label())
    label["allowed_immediate_tools"] = ["edit_file"]
    label["allowed_immediate_tool_families"] = ["targeted_mutation"]
    label["immediate_tool_family"] = "targeted_mutation"
    label["required_lifecycle"] = [{"phase": "mutation", "allowed_tools": ["edit_file"]}]
    label["immediate_action_side_effect"] = True
    errors = validate_annotation(item, label)
    assert "mandatory prior inspection is omitted" in errors
    assert "annotation includes a deterministically forbidden tool" in errors


def test_consistency_rejects_action_when_constraints_require_blocking() -> None:
    item = case(mode="read_only", operation="apply_existing")
    errors = validate_annotation(item, valid_proposal_label())
    assert "blocking constraint requires blocked response" in errors
    assert "annotation uses a deterministically forbidden response mode" in errors


def test_public_operation_contract_binds_policy_defined_semantics() -> None:
    expected = {
        "propose_existing": ("planning", "file_inspection", ("read_file",), "mutation_proposal"),
        "propose_new": ("planning", "mutation_proposal", ("propose_write_file",), None),
        "apply_existing": ("mutation", "file_inspection", ("read_file",), "targeted_mutation"),
        "replace_existing": ("mutation", "file_inspection", ("read_file",), "file_creation"),
        "create_new": ("mutation", "file_creation", ("write_file",), None),
        "run_tests": ("verification", "execution_verification", ("run_command",), None),
        "compile": ("verification", "execution_verification", ("run_command",), None),
        "shell": ("verification", "execution_verification", ("run_command",), None),
    }
    for operation, required in expected.items():
        item = case(
            mode="propose" if operation.startswith("propose") else "write_approved",
            write=operation in {"apply_existing", "replace_existing", "create_new"},
            operation=operation,
        )
        if operation == "propose_new" or operation == "create_new":
            item["public_facts"]["target_state"] = "missing"
        if operation in {"run_tests", "compile", "shell"}:
            item["capabilities"]["shell"] = True
        constraints = derive_policy_constraints(item)
        assert (
            constraints.required_task_class,
            constraints.required_immediate_family,
            constraints.required_immediate_tools,
            constraints.required_terminal_family,
        ) == required
        assert constraints.required_lifecycle is not None
        assert constraints.required_immediate_side_effect is not None
        assert constraints.required_terminal_mutation_expected is not None


def test_consistency_rejects_invented_cross_phase_semantics() -> None:
    item = case(mode="write_approved", operation="run_tests")
    item["capabilities"]["shell"] = True
    label = deepcopy(valid_proposal_label())
    label.update({
        "task_class": "verification",
        "immediate_tool_family": "execution_verification",
        "allowed_immediate_tool_families": ["execution_verification"],
        "allowed_immediate_tools": ["run_command"],
        "terminal_tool_family": None,
        "allowed_terminal_tools": [],
        "required_lifecycle": [
            {"phase": "proposal", "allowed_tools": ["propose_edit_file"]},
            {"phase": "verification", "allowed_tools": ["run_command"]},
        ],
        "reason_code": "test_execution",
        "user_mutation_goal": False,
        "terminal_mutation_expected": True,
    })
    errors = validate_annotation(item, label)
    assert "annotation contradicts the deterministically required lifecycle" in errors
    assert "annotation contradicts the deterministic terminal-mutation value" in errors


def test_dynamic_schema_seals_deterministic_operation_fields() -> None:
    constraints = derive_policy_constraints(case())
    properties = annotation_schema(constraints)["properties"]
    assert properties["task_class"] == {"enum": ["planning"]}
    assert properties["allowed_immediate_tools"]["enum"] == [["read_file"]]
    assert properties["terminal_tool_family"] == {"enum": ["mutation_proposal"]}
    assert properties["required_lifecycle"]["enum"] == [[
        {"phase": "inspection", "allowed_tools": ["read_file"]},
        {"phase": "proposal", "allowed_tools": ["propose_edit_file"]},
    ]]


def test_dynamic_schema_excludes_reason_contradicting_public_fixture_facts() -> None:
    item = case(mode="read_only", operation="inspect")
    properties = annotation_schema(derive_policy_constraints(item))["properties"]
    assert "repository_resolves_target" not in properties["reason_code"]["enum"]

    item["public_facts"]["repository_resolvable"] = True
    properties = annotation_schema(derive_policy_constraints(item))["properties"]
    assert "repository_resolves_target" in properties["reason_code"]["enum"]
