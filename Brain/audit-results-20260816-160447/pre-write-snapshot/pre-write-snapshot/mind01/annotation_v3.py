from __future__ import annotations

import hashlib
import itertools
import json
from dataclasses import dataclass
from typing import Any, Mapping


TASK_CLASSES = {"inspection", "mutation", "verification", "explanation", "planning", "blocked"}
SPECIALISTS = {"general", "repository_inspector", "implementation", "verification", "debugging", "documentation", "security_review"}
RESPONSE_MODES = {"action", "final_answer", "clarification", "blocked"}
RISK_LEVELS = {"low", "medium", "high", "critical"}
PHASES = {"inspection", "proposal", "mutation", "verification", "answer"}
TOOL_FAMILIES = {
    "repository_discovery", "file_inspection", "symbol_inspection", "documentation_retrieval",
    "execution_verification", "mutation_proposal", "targeted_mutation", "file_creation",
    "patch_inspection", "memory_retrieval", "final_response", "clarification", "blocked",
}
TOOLS = {
    "list_files", "project_map", "read_file", "search_code", "index_code", "search_symbols",
    "file_summary", "write_file", "edit_file", "propose_write_file", "propose_edit_file",
    "list_patches", "show_patch", "test_patch", "run_command", "remember", "recall",
    "list_memories", "update_memory", "delete_memory", "search_docs", "refresh_knowledge",
    "query_knowledge",
}
TOOL_FAMILIES_BY_TOOL = {
    "list_files": {"repository_discovery"}, "project_map": {"repository_discovery"},
    "read_file": {"file_inspection"},
    "search_code": {"repository_discovery", "symbol_inspection", "file_inspection"},
    "search_symbols": {"symbol_inspection"}, "file_summary": {"file_inspection"},
    "search_docs": {"documentation_retrieval"},
    "query_knowledge": {"documentation_retrieval", "memory_retrieval"},
    "run_command": {"execution_verification"}, "test_patch": {"execution_verification"},
    "propose_write_file": {"mutation_proposal"}, "propose_edit_file": {"mutation_proposal"},
    "write_file": {"file_creation"}, "edit_file": {"targeted_mutation"},
    "list_patches": {"patch_inspection"}, "show_patch": {"patch_inspection"},
    "recall": {"memory_retrieval"}, "list_memories": {"memory_retrieval"},
    "index_code": {"symbol_inspection"}, "refresh_knowledge": {"documentation_retrieval"},
    "remember": {"memory_retrieval"}, "update_memory": {"memory_retrieval"},
    "delete_memory": {"memory_retrieval"},
}
SIDE_EFFECT_TOOLS = {
    "index_code", "write_file", "edit_file", "propose_write_file", "propose_edit_file",
    "remember", "update_memory", "delete_memory", "refresh_knowledge",
}
LIVE_MUTATION_TOOLS = {"write_file", "edit_file", "remember", "update_memory", "delete_memory"}
SHELL_TOOLS = {"run_command", "test_patch"}
PROPOSAL_TOOLS = {"propose_write_file", "propose_edit_file"}
EXISTING_FILE_OPERATIONS = {"propose_existing", "apply_existing", "replace_existing"}
MUTATION_OPERATIONS = EXISTING_FILE_OPERATIONS | {"propose_new", "create_new"}
REASON_CODES = {
    "repository_inventory", "direct_file_read", "symbol_lookup", "reference_search",
    "dependency_inspection", "documentation_lookup", "direct_explanation", "test_execution",
    "compilation_check", "lint_check", "command_execution", "existing_file_patch_proposal",
    "new_file_patch_proposal", "approved_targeted_edit", "approved_file_creation",
    "approved_full_file_replacement", "mutation_requires_approval", "missing_capability",
    "policy_blocked", "inspect_before_mutate", "patch_review", "patch_test", "proposal_review",
    "memory_lookup", "symbol_index_refresh", "knowledge_refresh", "security_inspection",
    "planning_response", "evidence_comparison", "file_structure_summary", "grounded_explanation",
    "capability_assessment", "clarification_missing_target", "repository_resolves_target",
    "safe_fallback", "no_safe_fallback", "unsupported_capability", "stale_route",
}
LABEL_FIELDS = {
    "task_class", "specialist", "immediate_tool_family", "allowed_immediate_tool_families",
    "allowed_immediate_tools", "terminal_tool_family", "allowed_terminal_tools",
    "required_lifecycle", "allowed_alternative_lifecycles", "response_mode", "reason_code",
    "risk_level", "user_mutation_goal", "immediate_action_side_effect",
    "terminal_mutation_expected", "annotation_confidence", "ambiguities", "rationale_codes",
}


@dataclass(frozen=True)
class PolicyConstraints:
    case_id: str
    mutation_execution_permitted: bool
    proposal_permitted: bool
    prior_inspection_required: bool
    target_exists: bool
    target_unique: bool
    repository_resolvable: bool
    shell_permitted: bool
    route_stale: bool
    must_block: bool
    clarification_required: bool
    final_answer_required: bool
    required_response_mode: str
    required_task_class: str | None
    required_immediate_family: str | None
    required_reason_code: str | None
    required_immediate_tools: tuple[str, ...] | None
    required_terminal_family: str | None
    required_terminal_tools: tuple[str, ...] | None
    required_lifecycle: tuple[tuple[str, tuple[str, ...]], ...] | None
    required_immediate_side_effect: bool | None
    required_terminal_mutation_expected: bool | None
    user_mutation_goal: bool
    forbidden_response_modes: tuple[str, ...]
    forbidden_tools: tuple[str, ...]
    required_first_phase: str | None
    rationale_codes: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "case_id": self.case_id,
            "hard_constraints": {
                "mutation_execution_permitted": self.mutation_execution_permitted,
                "proposal_permitted": self.proposal_permitted,
                "prior_inspection_required": self.prior_inspection_required,
                "target_exists": self.target_exists,
                "target_unique": self.target_unique,
                "repository_resolvable": self.repository_resolvable,
                "shell_permitted": self.shell_permitted,
                "route_stale": self.route_stale,
                "must_block": self.must_block,
                "clarification_required": self.clarification_required,
                "final_answer_required": self.final_answer_required,
                "required_response_mode": self.required_response_mode,
                "required_task_class": self.required_task_class,
                "required_immediate_family": self.required_immediate_family,
                "required_reason_code": self.required_reason_code,
                "required_immediate_tools": (
                    list(self.required_immediate_tools)
                    if self.required_immediate_tools is not None
                    else None
                ),
                "required_terminal_family": self.required_terminal_family,
                "required_terminal_tools": (
                    list(self.required_terminal_tools)
                    if self.required_terminal_tools is not None
                    else None
                ),
                "required_lifecycle": (
                    [
                        {"phase": phase, "allowed_tools": list(tools)}
                        for phase, tools in self.required_lifecycle
                    ]
                    if self.required_lifecycle is not None
                    else None
                ),
                "required_immediate_side_effect": self.required_immediate_side_effect,
                "required_terminal_mutation_expected": self.required_terminal_mutation_expected,
                "user_mutation_goal": self.user_mutation_goal,
            },
            "forbidden_response_modes": list(self.forbidden_response_modes),
            "forbidden_tools": list(self.forbidden_tools),
            "required_first_phase": self.required_first_phase,
            "rationale_codes": list(self.rationale_codes),
        }


def derive_policy_constraints(case: Mapping[str, Any]) -> PolicyConstraints:
    facts = case.get("public_facts")
    if not isinstance(facts, Mapping):
        raise ValueError("case requires public_facts")
    capabilities = case.get("capabilities")
    if not isinstance(capabilities, Mapping):
        raise ValueError("case requires capabilities")
    mode = str(case.get("agent_mode", ""))
    operation = str(facts.get("requested_operation", "inspect"))
    target_state = str(facts.get("target_state", "exists_unique"))
    route_state = str(facts.get("route_state", "none"))
    unsafe = bool(facts.get("unsafe_operation", False) or facts.get("prompt_injection", False))
    unsupported = bool(facts.get("unsupported_operation", False))
    self_contained = bool(facts.get("self_contained", False))
    repository_resolvable = bool(facts.get("repository_resolvable", False))
    target_exists = target_state in {"exists_unique", "exists_multiple"}
    target_unique = target_state == "exists_unique"
    route_stale = route_state in {"stale_mode", "stale_capabilities"}
    mutation_goal = operation in MUTATION_OPERATIONS
    write_capability = bool(capabilities.get("workspace_write", False))
    shell_capability = bool(capabilities.get("shell", False))
    write_mode = mode in {"write_approved", "unsafe"}
    proposal_permitted = mode in {"propose", "write_approved", "unsafe"} and not route_stale and not unsafe
    mutation_execution_permitted = write_mode and write_capability and not route_stale and not unsafe
    shell_permitted = write_mode and shell_capability and not route_stale and not unsafe
    prior_inspection_required = operation in EXISTING_FILE_OPERATIONS and target_exists
    clarification_required = (
        operation in MUTATION_OPERATIONS
        and target_state in {"unspecified", "exists_multiple"}
        and not repository_resolvable
        and not unsafe
        and not route_stale
    )
    missing_required_capability = (
        (operation in {"apply_existing", "replace_existing", "create_new"} and not mutation_execution_permitted)
        or (operation in {"run_tests", "compile", "shell"} and not shell_permitted)
    )
    must_block = unsafe or route_stale or (missing_required_capability and not clarification_required)
    final_answer_required = unsupported or self_contained
    required_response_mode = "action"
    required_task_class = None
    required_immediate_family = None
    required_reason_code = None
    required_immediate_tools: tuple[str, ...] | None = None
    required_terminal_family: str | None = None
    required_terminal_tools: tuple[str, ...] | None = None
    required_lifecycle: tuple[tuple[str, tuple[str, ...]], ...] | None = None
    required_immediate_side_effect: bool | None = None
    required_terminal_mutation_expected: bool | None = None
    if must_block:
        required_response_mode = "blocked"
        required_task_class = "blocked"
        required_immediate_family = "blocked"
        if route_stale:
            required_reason_code = "stale_route"
        elif unsafe:
            required_reason_code = "policy_blocked"
        else:
            required_reason_code = (
                "mutation_requires_approval"
                if mutation_goal and mode == "read_only"
                else "missing_capability"
            )
    elif clarification_required:
        required_response_mode = "clarification"
        required_task_class = "blocked"
        required_immediate_family = "clarification"
        required_reason_code = "clarification_missing_target"
    elif final_answer_required:
        required_response_mode = "final_answer"
        required_task_class = "explanation"
        required_immediate_family = "final_response"
        required_reason_code = "unsupported_capability" if unsupported else "direct_explanation"
    else:
        operation_contracts: dict[str, dict[str, Any]] = {
            "propose_existing": {
                "task_class": "planning",
                "immediate_family": "file_inspection",
                "immediate_tools": ("read_file",),
                "terminal_family": "mutation_proposal",
                "terminal_tools": ("propose_edit_file",),
                "lifecycle": (
                    ("inspection", ("read_file",)),
                    ("proposal", ("propose_edit_file",)),
                ),
                "reason_code": "existing_file_patch_proposal",
                "immediate_side_effect": False,
                "terminal_mutation_expected": True,
            },
            "propose_new": {
                "task_class": "planning",
                "immediate_family": "mutation_proposal",
                "immediate_tools": ("propose_write_file",),
                "terminal_family": None,
                "terminal_tools": (),
                "lifecycle": (("proposal", ("propose_write_file",)),),
                "reason_code": "new_file_patch_proposal",
                "immediate_side_effect": True,
                "terminal_mutation_expected": True,
            },
            "apply_existing": {
                "task_class": "mutation",
                "immediate_family": "file_inspection",
                "immediate_tools": ("read_file",),
                "terminal_family": "targeted_mutation",
                "terminal_tools": ("edit_file",),
                "lifecycle": (
                    ("inspection", ("read_file",)),
                    ("mutation", ("edit_file",)),
                ),
                "reason_code": "approved_targeted_edit",
                "immediate_side_effect": False,
                "terminal_mutation_expected": True,
            },
            "replace_existing": {
                "task_class": "mutation",
                "immediate_family": "file_inspection",
                "immediate_tools": ("read_file",),
                "terminal_family": "file_creation",
                "terminal_tools": ("write_file",),
                "lifecycle": (
                    ("inspection", ("read_file",)),
                    ("mutation", ("write_file",)),
                ),
                "reason_code": "approved_full_file_replacement",
                "immediate_side_effect": False,
                "terminal_mutation_expected": True,
            },
            "create_new": {
                "task_class": "mutation",
                "immediate_family": "file_creation",
                "immediate_tools": ("write_file",),
                "terminal_family": None,
                "terminal_tools": (),
                "lifecycle": (("mutation", ("write_file",)),),
                "reason_code": "approved_file_creation",
                "immediate_side_effect": True,
                "terminal_mutation_expected": True,
            },
            "run_tests": {
                "task_class": "verification",
                "immediate_family": "execution_verification",
                "immediate_tools": ("run_command",),
                "terminal_family": None,
                "terminal_tools": (),
                "lifecycle": (("verification", ("run_command",)),),
                "reason_code": "test_execution",
                "immediate_side_effect": False,
                "terminal_mutation_expected": False,
            },
            "compile": {
                "task_class": "verification",
                "immediate_family": "execution_verification",
                "immediate_tools": ("run_command",),
                "terminal_family": None,
                "terminal_tools": (),
                "lifecycle": (("verification", ("run_command",)),),
                "reason_code": "compilation_check",
                "immediate_side_effect": False,
                "terminal_mutation_expected": False,
            },
            "shell": {
                "task_class": "verification",
                "immediate_family": "execution_verification",
                "immediate_tools": ("run_command",),
                "terminal_family": None,
                "terminal_tools": (),
                "lifecycle": (("verification", ("run_command",)),),
                "reason_code": "command_execution",
                "immediate_side_effect": False,
                "terminal_mutation_expected": False,
            },
        }
        contract = operation_contracts.get(operation)
        if contract is not None:
            required_task_class = contract["task_class"]
            required_immediate_family = contract["immediate_family"]
            required_immediate_tools = contract["immediate_tools"]
            required_terminal_family = contract["terminal_family"]
            required_terminal_tools = contract["terminal_tools"]
            required_lifecycle = contract["lifecycle"]
            required_reason_code = contract["reason_code"]
            required_immediate_side_effect = contract["immediate_side_effect"]
            required_terminal_mutation_expected = contract["terminal_mutation_expected"]
        elif operation == "inspect":
            required_task_class = "inspection"
    forbidden_tools: set[str] = set()
    if not mutation_execution_permitted:
        forbidden_tools |= LIVE_MUTATION_TOOLS
    if not proposal_permitted:
        forbidden_tools |= PROPOSAL_TOOLS
    if not shell_permitted:
        forbidden_tools |= SHELL_TOOLS
    if mode == "read_only":
        forbidden_tools |= SIDE_EFFECT_TOOLS
    if must_block or clarification_required or final_answer_required:
        forbidden_tools |= TOOLS
    forbidden_modes = []
    if must_block:
        forbidden_modes.extend(["action", "final_answer", "clarification"])
    elif clarification_required:
        forbidden_modes.extend(["action", "final_answer", "blocked"])
    elif final_answer_required:
        forbidden_modes.extend(["action", "clarification", "blocked"])
    rationale = []
    if route_stale:
        rationale.append("stale_route_fails_closed")
    if unsafe:
        rationale.append("unsafe_operation_blocked")
    if prior_inspection_required:
        rationale.append("existing_target_requires_inspection")
    if missing_required_capability:
        rationale.append("required_capability_unavailable")
    if clarification_required:
        rationale.append("target_not_uniquely_bounded")
    if final_answer_required:
        rationale.append("no_tool_required_or_supported")
    required_first_phase = "inspection" if prior_inspection_required and not must_block and not clarification_required else None
    return PolicyConstraints(
        case_id=str(case.get("case_id", "")),
        mutation_execution_permitted=mutation_execution_permitted,
        proposal_permitted=proposal_permitted,
        prior_inspection_required=prior_inspection_required,
        target_exists=target_exists,
        target_unique=target_unique,
        repository_resolvable=repository_resolvable,
        shell_permitted=shell_permitted,
        route_stale=route_stale,
        must_block=must_block,
        clarification_required=clarification_required,
        final_answer_required=final_answer_required,
        required_response_mode=required_response_mode,
        required_task_class=required_task_class,
        required_immediate_family=required_immediate_family,
        required_reason_code=required_reason_code,
        required_immediate_tools=required_immediate_tools,
        required_terminal_family=required_terminal_family,
        required_terminal_tools=required_terminal_tools,
        required_lifecycle=required_lifecycle,
        required_immediate_side_effect=required_immediate_side_effect,
        required_terminal_mutation_expected=required_terminal_mutation_expected,
        user_mutation_goal=mutation_goal,
        forbidden_response_modes=tuple(sorted(set(forbidden_modes))),
        forbidden_tools=tuple(sorted(forbidden_tools)),
        required_first_phase=required_first_phase,
        rationale_codes=tuple(rationale),
    )


def validate_annotation(
    case: Mapping[str, Any],
    label: Mapping[str, Any],
    constraints: PolicyConstraints | None = None,
) -> list[str]:
    errors: list[str] = []
    constraints = constraints or derive_policy_constraints(case)
    if set(label) != LABEL_FIELDS:
        missing = sorted(LABEL_FIELDS - set(label))
        extra = sorted(set(label) - LABEL_FIELDS)
        return [f"annotation fields mismatch; missing={missing}; extra={extra}"]
    _enum(errors, label, "task_class", TASK_CLASSES)
    _enum(errors, label, "specialist", SPECIALISTS)
    _enum(errors, label, "immediate_tool_family", TOOL_FAMILIES)
    _enum(errors, label, "response_mode", RESPONSE_MODES)
    _enum(errors, label, "reason_code", REASON_CODES)
    _enum(errors, label, "risk_level", RISK_LEVELS)
    immediate_tools = _string_set(errors, label.get("allowed_immediate_tools"), TOOLS, "allowed_immediate_tools")
    immediate_families = _string_set(errors, label.get("allowed_immediate_tool_families"), TOOL_FAMILIES, "allowed_immediate_tool_families")
    terminal_tools = _string_set(errors, label.get("allowed_terminal_tools"), TOOLS, "allowed_terminal_tools")
    terminal_family = label.get("terminal_tool_family")
    if terminal_family is not None and terminal_family not in TOOL_FAMILIES:
        errors.append("terminal_tool_family is invalid")
    for field in ("user_mutation_goal", "immediate_action_side_effect", "terminal_mutation_expected"):
        if not isinstance(label.get(field), bool):
            errors.append(f"{field} must be boolean")
    confidence = label.get("annotation_confidence")
    if not isinstance(confidence, (int, float)) or isinstance(confidence, bool) or not 0 <= float(confidence) <= 1:
        errors.append("annotation_confidence must be between 0 and 1")
    for field in ("ambiguities", "rationale_codes"):
        value = label.get(field)
        if not isinstance(value, list) or any(not isinstance(item, str) or not item for item in value):
            errors.append(f"{field} must be an array of non-empty strings")
    lifecycle = _validate_lifecycle(errors, label.get("required_lifecycle"), "required_lifecycle")
    alternatives = label.get("allowed_alternative_lifecycles")
    if not isinstance(alternatives, list):
        errors.append("allowed_alternative_lifecycles must be an array")
        alternatives = []
    else:
        for index, alternative in enumerate(alternatives):
            _validate_lifecycle(errors, alternative, f"allowed_alternative_lifecycles[{index}]")

    response_mode = label.get("response_mode")
    task_class = label.get("task_class")
    if task_class == "blocked" and response_mode not in {"blocked", "clarification"}:
        errors.append("blocked task class requires blocked or clarification response mode")
    if response_mode == "blocked" and task_class != "blocked":
        errors.append("blocked response mode requires blocked task class")
    if response_mode in {"final_answer", "clarification", "blocked"}:
        if immediate_tools or terminal_tools or lifecycle or alternatives:
            errors.append("non-action response cannot specify tools or lifecycles")
    if response_mode == "clarification" and label.get("immediate_tool_family") != "clarification":
        errors.append("clarification response requires clarification family")
    if response_mode == "blocked" and label.get("immediate_tool_family") != "blocked":
        errors.append("blocked response requires blocked family")
    if response_mode == "final_answer" and label.get("immediate_tool_family") != "final_response":
        errors.append("final answer requires final_response family")
    if response_mode == "action":
        if not immediate_tools or not lifecycle:
            errors.append("action response requires immediate tools and lifecycle")
        elif not immediate_tools.intersection(set(lifecycle[0].get("allowed_tools", []))):
            errors.append("first lifecycle step must include an allowed immediate tool")
    if label.get("immediate_tool_family") not in immediate_families:
        errors.append("primary immediate family must be included in allowed immediate families")
    if immediate_tools:
        if any(not TOOL_FAMILIES_BY_TOOL.get(tool, set()).intersection(immediate_families) for tool in immediate_tools):
            errors.append("allowed immediate tools conflict with allowed immediate families")
    if bool(immediate_tools & SIDE_EFFECT_TOOLS) != bool(label.get("immediate_action_side_effect")):
        errors.append("immediate side-effect field conflicts with tool semantics")
    if terminal_family is None and terminal_tools:
        errors.append("terminal tools require a terminal family")
    if terminal_family is not None:
        if not terminal_tools:
            errors.append("terminal family requires terminal tools")
        elif any(terminal_family not in TOOL_FAMILIES_BY_TOOL.get(tool, set()) for tool in terminal_tools):
            errors.append("terminal family conflicts with terminal tools")
    if label.get("terminal_mutation_expected") and not label.get("user_mutation_goal"):
        errors.append("terminal mutation expectation requires a user mutation goal")
    if not label.get("terminal_mutation_expected") and terminal_tools & (LIVE_MUTATION_TOOLS | PROPOSAL_TOOLS):
        errors.append("terminal mutation tools require terminal mutation expectation")
    if immediate_tools & set(constraints.forbidden_tools) or terminal_tools & set(constraints.forbidden_tools):
        errors.append("annotation includes a deterministically forbidden tool")
    if response_mode in constraints.forbidden_response_modes:
        errors.append("annotation uses a deterministically forbidden response mode")
    if response_mode != constraints.required_response_mode:
        errors.append("annotation contradicts the deterministically required response mode")
    if constraints.required_task_class and task_class != constraints.required_task_class:
        errors.append("annotation contradicts the deterministically required task class")
    if constraints.required_immediate_family and label.get("immediate_tool_family") != constraints.required_immediate_family:
        errors.append("annotation contradicts the deterministically required immediate family")
    if constraints.required_reason_code and label.get("reason_code") != constraints.required_reason_code:
        errors.append("annotation contradicts the deterministically required reason code")
    if (
        constraints.required_immediate_tools is not None
        and immediate_tools != set(constraints.required_immediate_tools)
    ):
        errors.append("annotation contradicts the deterministically required immediate tools")
    if constraints.required_terminal_tools is not None:
        if terminal_family != constraints.required_terminal_family:
            errors.append("annotation contradicts the deterministically required terminal family")
        if terminal_tools != set(constraints.required_terminal_tools):
            errors.append("annotation contradicts the deterministically required terminal tools")
    if constraints.required_lifecycle is not None:
        required_lifecycle = _lifecycle_payload(constraints.required_lifecycle)
        if lifecycle != required_lifecycle or alternatives:
            errors.append("annotation contradicts the deterministically required lifecycle")
    if (
        constraints.required_immediate_side_effect is not None
        and label.get("immediate_action_side_effect")
        is not constraints.required_immediate_side_effect
    ):
        errors.append("annotation contradicts the deterministic immediate side-effect value")
    if (
        constraints.required_terminal_mutation_expected is not None
        and label.get("terminal_mutation_expected")
        is not constraints.required_terminal_mutation_expected
    ):
        errors.append("annotation contradicts the deterministic terminal-mutation value")
    facts = case.get("public_facts", {})
    if label.get("reason_code") == "repository_resolves_target" and not bool(facts.get("repository_resolvable", False)):
        errors.append("repository-resolvable reason contradicts public fixture facts")
    if label.get("user_mutation_goal") != constraints.user_mutation_goal:
        errors.append("user mutation goal contradicts public operation facts")
    if constraints.must_block and response_mode != "blocked":
        errors.append("blocking constraint requires blocked response")
    if constraints.clarification_required and response_mode != "clarification":
        errors.append("unbounded target requires clarification")
    if constraints.final_answer_required and response_mode != "final_answer":
        errors.append("self-contained or unsupported task requires final answer")
    if constraints.prior_inspection_required and response_mode == "action":
        if not lifecycle or lifecycle[0].get("phase") != "inspection":
            errors.append("mandatory prior inspection is omitted")
        if immediate_tools & (LIVE_MUTATION_TOOLS | PROPOSAL_TOOLS):
            errors.append("mutation/proposal cannot be the immediate action before inspection")
    if not constraints.mutation_execution_permitted and (immediate_tools | terminal_tools) & LIVE_MUTATION_TOOLS:
        errors.append("live mutation is forbidden by mode or capability")
    if not constraints.proposal_permitted and (immediate_tools | terminal_tools) & PROPOSAL_TOOLS:
        errors.append("proposal is forbidden by mode")
    if not constraints.shell_permitted and (immediate_tools | terminal_tools) & SHELL_TOOLS:
        errors.append("shell action is forbidden by capability")
    if (constraints.route_stale or "unsafe_operation_blocked" in constraints.rationale_codes) and label.get("risk_level") not in {"high", "critical"}:
        errors.append("stale or critical policy case must be high or critical risk")
    if isinstance(confidence, (int, float)) and float(confidence) < 0.75:
        errors.append("annotation confidence is below acceptance threshold")
    return sorted(set(errors))


def annotation_schema(constraints: PolicyConstraints | None = None) -> dict[str, Any]:
    lifecycle = {
        "type": "object", "additionalProperties": False,
        "required": ["phase", "allowed_tools"],
        "properties": {
            "phase": {"enum": sorted(PHASES)},
            "allowed_tools": {"type": "array", "uniqueItems": True, "items": {"enum": sorted(TOOLS)}},
        },
    }
    schema = {
        "type": "object", "additionalProperties": False, "required": sorted(LABEL_FIELDS),
        "properties": {
            "task_class": {"enum": sorted(TASK_CLASSES)},
            "specialist": {"enum": sorted(SPECIALISTS)},
            "immediate_tool_family": {"enum": sorted(TOOL_FAMILIES)},
            "allowed_immediate_tool_families": {"type": "array", "uniqueItems": True, "items": {"enum": sorted(TOOL_FAMILIES)}},
            "allowed_immediate_tools": {"type": "array", "uniqueItems": True, "items": {"enum": sorted(TOOLS)}},
            "terminal_tool_family": {"enum": [*sorted(TOOL_FAMILIES), None]},
            "allowed_terminal_tools": {"type": "array", "uniqueItems": True, "items": {"enum": sorted(TOOLS)}},
            "required_lifecycle": {"type": "array", "items": lifecycle},
            "allowed_alternative_lifecycles": {"type": "array", "items": {"type": "array", "items": lifecycle}},
            "response_mode": {"enum": sorted(RESPONSE_MODES)},
            "reason_code": {"enum": sorted(REASON_CODES)},
            "risk_level": {"enum": sorted(RISK_LEVELS)},
            "user_mutation_goal": {"type": "boolean"},
            "immediate_action_side_effect": {"type": "boolean"},
            "terminal_mutation_expected": {"type": "boolean"},
            "annotation_confidence": {"type": "number", "minimum": 0, "maximum": 1},
            "ambiguities": {"type": "array", "items": {"type": "string", "minLength": 1, "maxLength": 120}},
            "rationale_codes": {"type": "array", "items": {"type": "string", "minLength": 1, "maxLength": 120}},
        },
    }
    if constraints is None:
        return schema
    properties = schema["properties"]
    properties["response_mode"] = {"enum": [constraints.required_response_mode]}
    properties["user_mutation_goal"] = {"enum": [constraints.user_mutation_goal]}
    if constraints.required_task_class:
        properties["task_class"] = {"enum": [constraints.required_task_class]}
    if constraints.required_immediate_family:
        properties["immediate_tool_family"] = {"enum": [constraints.required_immediate_family]}
        properties["allowed_immediate_tool_families"] = {
            "type": "array", "enum": [[constraints.required_immediate_family]],
        }
    if constraints.required_reason_code:
        properties["reason_code"] = {"enum": [constraints.required_reason_code]}
    elif not constraints.repository_resolvable:
        properties["reason_code"] = {
            "enum": sorted(REASON_CODES - {"repository_resolves_target"})
        }
    permitted_tools = sorted(TOOLS - set(constraints.forbidden_tools))
    properties["allowed_immediate_tools"]["items"] = {"enum": permitted_tools}
    properties["allowed_terminal_tools"]["items"] = {"enum": permitted_tools}
    if constraints.required_immediate_tools is not None:
        properties["allowed_immediate_tools"] = {
            "type": "array", "enum": [list(constraints.required_immediate_tools)],
        }
    if constraints.required_terminal_tools is not None:
        properties["terminal_tool_family"] = {"enum": [constraints.required_terminal_family]}
        properties["allowed_terminal_tools"] = {
            "type": "array", "enum": [list(constraints.required_terminal_tools)],
        }
    if constraints.required_lifecycle is not None:
        properties["required_lifecycle"] = {
            "type": "array", "enum": [_lifecycle_payload(constraints.required_lifecycle)],
        }
        properties["allowed_alternative_lifecycles"] = {"type": "array", "maxItems": 0}
    if constraints.required_immediate_side_effect is not None:
        properties["immediate_action_side_effect"] = {
            "enum": [constraints.required_immediate_side_effect]
        }
    if constraints.required_terminal_mutation_expected is not None:
        properties["terminal_mutation_expected"] = {
            "enum": [constraints.required_terminal_mutation_expected]
        }
    if constraints.required_response_mode != "action":
        properties["allowed_immediate_tools"]["maxItems"] = 0
        properties["allowed_terminal_tools"]["maxItems"] = 0
        properties["required_lifecycle"]["maxItems"] = 0
        properties["allowed_alternative_lifecycles"]["maxItems"] = 0
        properties["terminal_tool_family"] = {"enum": [None]}
        properties["immediate_action_side_effect"] = {"enum": [False]}
        properties["terminal_mutation_expected"] = {"enum": [False]}
    else:
        properties["allowed_immediate_tools"]["minItems"] = 1
        properties["required_lifecycle"]["minItems"] = 1
    return schema


def annotation_agreement(left: Mapping[str, Any], right: Mapping[str, Any]) -> dict[str, bool]:
    return {
        "task_class": left.get("task_class") == right.get("task_class"),
        "specialist": left.get("specialist") == right.get("specialist"),
        "immediate_family": set(left.get("allowed_immediate_tool_families", [])) == set(right.get("allowed_immediate_tool_families", [])),
        "allowed_tool_set": set(left.get("allowed_immediate_tools", [])) == set(right.get("allowed_immediate_tools", [])),
        "lifecycle": _lifecycle_signature(left) == _lifecycle_signature(right),
        "response_mode": left.get("response_mode") == right.get("response_mode"),
        "reason_code": left.get("reason_code") == right.get("reason_code"),
        "risk_level": left.get("risk_level") == right.get("risk_level"),
        "mutation_fields": all(left.get(field) == right.get(field) for field in (
            "user_mutation_goal", "immediate_action_side_effect", "terminal_mutation_expected"
        )),
    }


def semantic_label_projection(label: Mapping[str, Any]) -> dict[str, Any]:
    return {key: label[key] for key in sorted(LABEL_FIELDS - {"annotation_confidence", "ambiguities", "rationale_codes"})}


def label_sha256(labels: list[Mapping[str, Any]]) -> str:
    payload = json.dumps(labels, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _enum(errors: list[str], label: Mapping[str, Any], field: str, values: set[str]) -> None:
    if label.get(field) not in values:
        errors.append(f"{field} is invalid")


def _string_set(errors: list[str], value: Any, allowed: set[str], field: str) -> set[str]:
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        errors.append(f"{field} must be an array of strings")
        return set()
    if len(value) != len(set(value)):
        errors.append(f"{field} contains duplicates")
    result = set(value)
    if not result.issubset(allowed):
        errors.append(f"{field} contains unknown values")
    return result


def _validate_lifecycle(errors: list[str], value: Any, field: str) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(f"{field} must be an array")
        return []
    result: list[dict[str, Any]] = []
    for index, step in enumerate(value):
        if not isinstance(step, Mapping) or set(step) != {"phase", "allowed_tools"}:
            errors.append(f"{field}[{index}] is malformed")
            continue
        if step.get("phase") not in PHASES:
            errors.append(f"{field}[{index}] has invalid phase")
        _string_set(errors, step.get("allowed_tools"), TOOLS, f"{field}[{index}].allowed_tools")
        result.append(dict(step))
    return result


def _lifecycle_payload(
    lifecycle: tuple[tuple[str, tuple[str, ...]], ...],
) -> list[dict[str, Any]]:
    return [
        {"phase": phase, "allowed_tools": list(tools)}
        for phase, tools in lifecycle
    ]


def _lifecycle_signature(label: Mapping[str, Any]) -> str:
    lifecycles = [label.get("required_lifecycle", []), *label.get("allowed_alternative_lifecycles", [])]
    expanded: set[tuple[tuple[str, str], ...]] = set()
    for lifecycle in lifecycles:
        if not lifecycle:
            expanded.add(())
            continue
        choices = [
            [(str(step.get("phase")), str(tool)) for tool in sorted(step.get("allowed_tools", []))]
            for step in lifecycle
        ]
        expanded.update(tuple(sequence) for sequence in itertools.product(*choices))
    payload = {
        "valid_sequences": sorted(expanded),
        "terminal_family": label.get("terminal_tool_family"),
        "terminal_tools": sorted(label.get("allowed_terminal_tools", [])),
    }
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
