from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import Enum

from .intent import Capability, ExpectedOutputMode
from .modes import AgentMode, parse_agent_mode
from .routing import RoutingDecision, ToolFamily
from .tools.schemas import SCHEMA_BY_NAME


class LifecyclePhase(str, Enum):
    INSPECTION = "inspection"
    PROPOSAL = "proposal"
    MUTATION = "mutation"
    VERIFICATION = "verification"
    ANSWER = "answer"


class StaleRouteError(ValueError):
    pass


@dataclass(frozen=True)
class ToolExposureContext:
    phase: LifecyclePhase
    mode: AgentMode
    granted_capabilities: tuple[Capability, ...]
    prior_inspection: bool
    mutation_seen: bool = False
    discovery_seen: bool = False
    discovery_scope: tuple[str, ...] = ()
    target_exists: bool | None = None

    @classmethod
    def build(
        cls,
        *,
        phase: LifecyclePhase | str,
        mode: AgentMode | str,
        allow_write: bool,
        allow_shell: bool,
        prior_inspection: bool,
        mutation_seen: bool = False,
        discovery_seen: bool = False,
        discovery_scope: tuple[str, ...] = (),
        target_exists: bool | None = None,
    ) -> "ToolExposureContext":
        normalized_mode = parse_agent_mode(mode)
        capabilities = [Capability.WORKSPACE_READ]
        if normalized_mode in {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            capabilities.append(Capability.RUNTIME_STATE)
        if allow_write and normalized_mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            capabilities.append(Capability.WORKSPACE_WRITE)
        if allow_shell and normalized_mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            capabilities.append(Capability.SHELL)
        return cls(
            phase=phase if isinstance(phase, LifecyclePhase) else LifecyclePhase(phase),
            mode=normalized_mode,
            granted_capabilities=tuple(capabilities),
            prior_inspection=prior_inspection,
            mutation_seen=mutation_seen,
            discovery_seen=discovery_seen,
            discovery_scope=tuple(sorted(set(discovery_scope))),
            target_exists=target_exists,
        )

    def fingerprint(self) -> str:
        payload = json.dumps(
            {
                "mode": self.mode.value,
                "capabilities": sorted(item.value for item in self.granted_capabilities),
                "phase": self.phase.value,
                "prior_inspection": self.prior_inspection,
                "mutation_seen": self.mutation_seen,
                "discovery_seen": self.discovery_seen,
                "discovery_scope": list(self.discovery_scope),
            },
            sort_keys=True,
            separators=(",", ":"),
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class ToolExposureDecision:
    visible_tools: tuple[str, ...]
    excluded_tools: dict[str, str]
    route_intent_id: str
    context_fingerprint: str


class ToolExposureAuthority:
    """The sole policy-aware function that turns a typed route into visible tools."""

    _INSPECTION_FALLBACKS = ("read_file", "search_code")
    _EXACT_TARGET_INSPECTION = ("read_file",)
    _POST_MUTATION = ("read_file", "search_code", "run_command", "test_patch")

    def decide(
        self,
        route: RoutingDecision,
        context: ToolExposureContext,
    ) -> ToolExposureDecision:
        if not route.is_current_for(context.granted_capabilities, context.mode.value):
            raise StaleRouteError("routing decision was produced under different capabilities or mode")
        if route.response_mode != ExpectedOutputMode.ACTION:
            return ToolExposureDecision((), {}, route.intent_id, context.fingerprint())

        candidates: tuple[str, ...]
        if context.mutation_seen and context.phase == LifecyclePhase.VERIFICATION:
            # Mutation is complete: expose only post-mutation tools so the agent
            # verifies and finishes instead of mutating further.
            candidates = self._POST_MUTATION
        elif context.discovery_seen and route.tool_family in {
            ToolFamily.REPOSITORY_DISCOVERY,
            ToolFamily.SYMBOL_INSPECTION,
        }:
            candidates = self._EXACT_TARGET_INSPECTION
        elif (
            route.requires_prior_inspection
            and not context.prior_inspection
            and context.target_exists is not False
        ):
            # A mutation whose target file does not exist is a new-file
            # creation: there is no source text to inspect first, so the
            # prior-inspection gate must not hide the write tools forever.
            candidates = self._EXACT_TARGET_INSPECTION
        elif route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
            if context.phase == LifecyclePhase.INSPECTION and not context.prior_inspection:
                candidates = self._INSPECTION_FALLBACKS
            else:
                candidates = (*route.preferred_tools, *route.fallback_tools)
        else:
            candidates = (*route.preferred_tools, *route.fallback_tools)

        visible: list[str] = []
        excluded: dict[str, str] = {}
        for name in dict.fromkeys(candidates):
            reason = self._exclusion_reason(name, route, context)
            if reason:
                excluded[name] = reason
            else:
                visible.append(name)
        return ToolExposureDecision(
            visible_tools=tuple(visible),
            excluded_tools=excluded,
            route_intent_id=route.intent_id,
            context_fingerprint=context.fingerprint(),
        )

    def legacy_visible_tools(
        self,
        *,
        permitted_tools: tuple[str, ...],
        mutation_required: bool,
        planning_required: bool,
        specialist: str,
        mode: AgentMode | str,
        inspected: bool,
        mutation_seen: bool,
        allow_write: bool,
        allow_shell: bool,
    ) -> tuple[str, ...]:
        """Compatibility projection for v0.10 callers; policy filtering remains centralized here."""

        permitted = set(permitted_tools)
        if mutation_seen:
            scoped = {"read_file", "search_code", "run_command", "test_patch"} & permitted
        elif mutation_required and inspected:
            scoped = {
                "read_file", "search_code", "propose_write_file", "propose_edit_file",
                "write_file", "edit_file", "refresh_knowledge",
            } & permitted
        elif mutation_required:
            scoped = {"project_map", "list_files", "read_file", "search_code"} & permitted
        elif planning_required:
            scoped = {"project_map", "list_files", "read_file", "search_code", "search_symbols", "file_summary"} & permitted
        elif specialist in {"testing_verification", "python_verification", "cpp_verification", "verilog_verification"}:
            scoped = {"project_map", "list_files", "read_file", "search_code", "search_symbols", "file_summary", "run_command", "test_patch"} & permitted
        elif specialist == "documentation_rag":
            scoped = {"search_docs", "read_file"} & permitted
        elif specialist == "memory_retrieval":
            scoped = {"recall", "query_knowledge"} & permitted
        else:
            scoped = set()
        normalized_mode = parse_agent_mode(mode)
        visible = []
        for name in sorted(scoped):
            schema = SCHEMA_BY_NAME[name]
            if normalized_mode.value not in schema.allowed_modes:
                continue
            if schema.can_write and not allow_write:
                continue
            if schema.can_run_shell and not allow_shell:
                continue
            visible.append(name)
        return tuple(visible)

    @staticmethod
    def _exclusion_reason(
        name: str,
        route: RoutingDecision,
        context: ToolExposureContext,
    ) -> str:
        schema = SCHEMA_BY_NAME.get(name)
        if schema is None:
            return "unknown_tool"
        if context.mode.value not in schema.allowed_modes:
            return "mode_mismatch"
        capabilities = set(context.granted_capabilities)
        if schema.can_write and Capability.WORKSPACE_WRITE not in capabilities:
            return "missing_workspace_write"
        if schema.can_run_shell and Capability.SHELL not in capabilities:
            return "missing_shell"
        if schema.mutates_runtime and Capability.RUNTIME_STATE not in capabilities:
            return "missing_runtime_state"
        if schema.can_write and context.phase != LifecyclePhase.MUTATION:
            return "write_tool_outside_mutation_phase"
        if route.tool_family == ToolFamily.MUTATION_PROPOSAL and schema.can_write:
            return "live_apply_hidden_in_propose_route"
        if route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION} and name.startswith("propose_"):
            return "proposal_hidden_in_live_apply_route"
        return ""
