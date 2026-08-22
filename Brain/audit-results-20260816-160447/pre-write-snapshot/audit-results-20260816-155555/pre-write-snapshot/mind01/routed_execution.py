from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from .intent import Capability, ExpectedOutputMode
from .modes import AgentMode, parse_agent_mode
from .pre_validate import PreValidationError
from .receipts import ReceiptStore, record_blocked_mutation
from .routing import HierarchicalRouter, RoutingDecision, ToolFamily
from .tool_exposure import (
    LifecyclePhase,
    StaleRouteError,
    ToolExposureAuthority,
    ToolExposureContext,
    ToolExposureDecision,
)
from .tools.registry import ToolRegistry
from .tools.schemas import SCHEMA_BY_NAME
from .tools.verify_tools import ToolError, ToolResult


DISCOVERY_TOOLS = {"list_files", "project_map", "search_code", "search_symbols"}
INSPECTION_TOOLS = DISCOVERY_TOOLS | {"read_file", "file_summary", "search_docs", "query_knowledge", "recall"}
RECEIPT_RE = re.compile(r"\(receipt ([a-zA-Z0-9_-]+)\)")


class DispatchAuthorizationError(ToolError):
    """Raised before a hidden, stale, or lifecycle-invalid action reaches a tool."""


@dataclass(frozen=True)
class RoutedStep:
    route: RoutingDecision
    exposure: ToolExposureDecision
    context: ToolExposureContext
    generation: int


@dataclass(frozen=True)
class DispatchEvidence:
    route_intent_id: str
    route_family: str
    context_fingerprint: str
    visible_tools: tuple[str, ...]
    selected_tool: str
    dispatched: bool
    execution_success: bool
    observation: str
    rolled_back: bool
    rollback_receipt_id: str | None
    dispatched_args: dict[str, object]
    argument_grounding: str | None


class RoutedExecutionSession:
    """Policy-bound dispatch for disposable or normal workspaces.

    The registry is deliberately behind this class. A route, its exposure
    fingerprint, the current mode/capabilities, and lifecycle state must all be
    current before a selected action can reach ``ToolRegistry.call``.
    """

    def __init__(
        self,
        workspace: Path,
        *,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        allow_write: bool = False,
        allow_shell: bool = False,
        allow_network: bool = False,
        registry: ToolRegistry | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.router = HierarchicalRouter()
        self.authority = ToolExposureAuthority()
        self.mode = parse_agent_mode(mode)
        self.allow_write = allow_write
        self.allow_shell = allow_shell
        self.allow_network = allow_network
        self.prior_inspection = False
        self.discovery_seen = False
        self.discovered_files: set[str] = set()
        self.mutation_seen = False
        self.generation = 0
        self.evidence: list[DispatchEvidence] = []
        self._registry = registry or self._new_registry()

    def route(self, prompt: str) -> RoutedStep:
        route = self.router.route_typed(
            prompt,
            self.workspace,
            mode=self.mode,
            allow_write=self.allow_write,
            allow_shell=self.allow_shell,
            allow_network=self.allow_network,
            prior_inspection=self.prior_inspection,
        )
        context = self._context(route)
        exposure = self.authority.decide(route, context)
        return RoutedStep(route, exposure, context, self.generation)

    def reconfigure(
        self,
        *,
        mode: str | AgentMode | None = None,
        allow_write: bool | None = None,
        allow_shell: bool | None = None,
        allow_network: bool | None = None,
    ) -> None:
        if mode is not None:
            self.mode = parse_agent_mode(mode)
        if allow_write is not None:
            self.allow_write = allow_write
        if allow_shell is not None:
            self.allow_shell = allow_shell
        if allow_network is not None:
            self.allow_network = allow_network
        self.generation += 1
        self._registry = self._new_registry()

    def dispatch(
        self,
        step: RoutedStep,
        tool: str,
        args: dict[str, object],
        *,
        verify: Callable[[Path], bool] | None = None,
    ) -> DispatchEvidence:
        self._authorize(step, tool)
        dispatched_args, argument_grounding = self._ground_existing_file_argument(step, tool, args)
        try:
            result = self._registry.call(tool, dispatched_args)
        except PreValidationError as exc:
            # A deterministic pre-validation check (e.g. Python syntax) rejected
            # the mutation before it reached the filesystem. Report it like any
            # other failed write: evidence with rollback semantics, so the
            # workspace is provably unchanged and the attempt is auditable.
            return self._blocked_evidence(step, tool, dispatched_args, argument_grounding, exc)
        rolled_back = False
        rollback_receipt_id: str | None = None
        execution_success = True
        if SCHEMA_BY_NAME[tool].can_write and verify is not None and not verify(self.workspace):
            receipt_id = _receipt_id(result)
            rollback = ReceiptStore(self.workspace).rollback(
                receipt_id,
                mode=self.mode.value,
                approved=True,
                source="routed_post_write_verification",
            )
            rolled_back = True
            rollback_receipt_id = str(rollback["receipt_id"])
            execution_success = False
        elif tool in DISCOVERY_TOOLS:
            self.discovery_seen = _useful_discovery(result.text)
            self.discovered_files = self._discovered_file_paths(tool, result.text) if self.discovery_seen else set()
        elif tool in INSPECTION_TOOLS:
            self.prior_inspection = True
            self.discovery_seen = False
            self.discovered_files.clear()
        if SCHEMA_BY_NAME[tool].can_write:
            self.mutation_seen = not rolled_back
        evidence = DispatchEvidence(
            route_intent_id=step.route.intent_id,
            route_family=step.route.tool_family.value,
            context_fingerprint=step.exposure.context_fingerprint,
            visible_tools=step.exposure.visible_tools,
            selected_tool=tool,
            dispatched=True,
            execution_success=execution_success,
            observation=result.text,
            rolled_back=rolled_back,
            rollback_receipt_id=rollback_receipt_id,
            dispatched_args=dispatched_args,
            argument_grounding=argument_grounding,
        )
        self.evidence.append(evidence)
        return evidence

    def _authorize(self, step: RoutedStep, tool: str) -> None:
        if step.generation != self.generation:
            raise StaleRouteError("route generation is stale after mode or capability change")
        current = self._context(step.route)
        if not step.route.is_current_for(current.granted_capabilities, current.mode.value):
            raise StaleRouteError("route capability fingerprint is stale")
        if step.exposure.route_intent_id != step.route.intent_id:
            raise DispatchAuthorizationError("exposure does not belong to the selected route")
        if step.exposure.context_fingerprint != current.fingerprint():
            raise StaleRouteError("exposure context fingerprint is stale")
        if tool not in step.exposure.visible_tools:
            raise DispatchAuthorizationError(f"tool `{tool}` was not exposed for this lifecycle step")
        if tool not in SCHEMA_BY_NAME:
            raise DispatchAuthorizationError(f"unknown tool `{tool}`")
        schema = SCHEMA_BY_NAME[tool]
        capabilities = set(current.granted_capabilities)
        if schema.can_write and Capability.WORKSPACE_WRITE not in capabilities:
            raise DispatchAuthorizationError("workspace write capability is absent")
        if schema.can_run_shell and Capability.SHELL not in capabilities:
            raise DispatchAuthorizationError("shell capability is absent")
        if schema.can_write and not self.prior_inspection and step.route.requires_prior_inspection:
            raise DispatchAuthorizationError("required prior inspection is incomplete")

    def _ground_existing_file_argument(
        self,
        step: RoutedStep,
        tool: str,
        args: dict[str, object],
    ) -> tuple[dict[str, object], str | None]:
        """Ground a missing existing-file path to one explicit routed target.

        This never broadens target scope and never redirects a valid path. It
        only repairs a nonexistent path for tools that operate on an existing
        file when the typed route names exactly one existing workspace file.
        Creation tools are deliberately excluded.
        """

        if tool not in {"read_file", "file_summary", "edit_file", "propose_edit_file"} or not isinstance(args.get("path"), str):
            return dict(args), None
        supplied = str(args["path"])
        try:
            if self._registry.resolve_path(supplied).is_file():
                return dict(args), None
        except ToolError:
            pass
        intent = step.route.normalized_intent
        if intent is None:
            return dict(args), None
        existing: list[str] = []
        for target in intent.target_scope:
            try:
                resolved = self._registry.resolve_path(target)
            except ToolError:
                continue
            if resolved.is_file():
                existing.append(str(resolved.relative_to(self.workspace)))
        candidates = tuple(dict.fromkeys(existing))
        grounding_source = "routed"
        if len(candidates) != 1:
            candidates = tuple(sorted(self.discovered_files))
            grounding_source = "discovered"
        if len(candidates) != 1:
            return dict(args), None
        grounded = dict(args)
        grounded["path"] = candidates[0]
        return grounded, f"nonexistent existing-file path `{supplied}` grounded to sole {grounding_source} file `{candidates[0]}`"

    def _discovered_file_paths(self, tool: str, observation: str) -> set[str]:
        candidates: list[str] = []
        if tool in {"search_code", "search_symbols"}:
            for line in observation.splitlines():
                match = re.match(r"^(.+?):\d+:", line)
                if match:
                    candidates.append(match.group(1))
        elif tool == "list_files":
            candidates.extend(line.strip() for line in observation.splitlines())
        discovered: set[str] = set()
        for raw_path in candidates:
            try:
                path = self._registry.resolve_path(raw_path)
            except ToolError:
                continue
            if path.is_file():
                discovered.add(str(path.relative_to(self.workspace)))
        return discovered

    def _context(self, route: RoutingDecision) -> ToolExposureContext:
        return ToolExposureContext.build(
            phase=self._phase(route),
            mode=self.mode,
            allow_write=self.allow_write,
            allow_shell=self.allow_shell,
            prior_inspection=self.prior_inspection,
            mutation_seen=self.mutation_seen,
            discovery_seen=self.discovery_seen,
            discovery_scope=tuple(sorted(self.discovered_files)),
        )

    def _phase(self, route: RoutingDecision) -> LifecyclePhase:
        if self.mutation_seen:
            return LifecyclePhase.VERIFICATION
        if route.response_mode != ExpectedOutputMode.ACTION:
            return LifecyclePhase.ANSWER
        if route.requires_prior_inspection and not self.prior_inspection:
            return LifecyclePhase.INSPECTION
        if route.tool_family == ToolFamily.MUTATION_PROPOSAL:
            return LifecyclePhase.PROPOSAL
        if route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
            return LifecyclePhase.MUTATION
        if route.tool_family == ToolFamily.EXECUTION_VERIFICATION:
            return LifecyclePhase.VERIFICATION
        return LifecyclePhase.INSPECTION

    def _new_registry(self) -> ToolRegistry:
        return ToolRegistry(
            self.workspace,
            yes=True,
            allow_write=self.allow_write,
            allow_shell=self.allow_shell,
            mode=self.mode,
        )

    def _blocked_evidence(
        self,
        step: RoutedStep,
        tool: str,
        dispatched_args: dict[str, object],
        argument_grounding: str | None,
        exc: PreValidationError,
    ) -> DispatchEvidence:
        receipt = record_blocked_mutation(
            self.workspace,
            operation_type=tool,
            path=str(dispatched_args.get("path", "")),
            reason=str(exc),
            source="routed_pre_validation",
            mode=self.mode.value,
        )
        if SCHEMA_BY_NAME[tool].can_write:
            self.mutation_seen = False
        evidence = DispatchEvidence(
            route_intent_id=step.route.intent_id,
            route_family=step.route.tool_family.value,
            context_fingerprint=step.exposure.context_fingerprint,
            visible_tools=step.exposure.visible_tools,
            selected_tool=tool,
            dispatched=True,
            execution_success=False,
            observation=str(exc),
            rolled_back=True,
            rollback_receipt_id=receipt["receipt_id"],
            dispatched_args=dispatched_args,
            argument_grounding=argument_grounding,
        )
        self.evidence.append(evidence)
        return evidence


def _receipt_id(result: ToolResult) -> str:
    match = RECEIPT_RE.search(result.text)
    if match is None:
        raise DispatchAuthorizationError("write result did not include a mutation receipt")
    return match.group(1)


def _useful_discovery(observation: str) -> bool:
    return observation.strip().lower() not in {"", "(no matches)", "(no files)", "(no symbols)"}
