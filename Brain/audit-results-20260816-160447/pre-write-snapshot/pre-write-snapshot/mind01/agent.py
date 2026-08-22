from __future__ import annotations

import json
import difflib
import hashlib
import re
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Iterable, List, Optional
from pathlib import Path

from .action_parser import (
    ParsedAction,
    ParserFailureCode,
    ResponseMode,
    canonical_response_schema,
    parse_action_output,
)
from .config import AgentConfig
from .completion import CompletionAuthority
from .llm import LLMError, Message, OllamaClient
from .llm_providers import build_llm_client
from .memory_intent import MemoryIntent, detect_memory_intent
from .modes import AgentMode
from .planning import Planner
from .patch_review import review_patch
from .prompts import SYSTEM_PROMPT, build_action_instruction
from .recovery import RecoveryController
from .receipts import ReceiptError, ReceiptStore
from .routing import HierarchicalRouter, RouteDecision, RoutingDecision, ToolFamily
from .semantic_router_v2 import (
    OllamaSemanticClassifier,
    RuleBasedSemanticClassifier,
    SemanticRouterV2,
)
from .security import redact_secrets
from .skills import SkillRegistry
from .state import AgentPhase, AgentState
from .task_contract import (
    EVIDENCE_TAXONOMY,
    EvidenceType,
    TaskContract,
    build_task_contract,
    requirement_ids_for_evidence,
    state_hash,
)
from .tool_exposure import (
    LifecyclePhase,
    StaleRouteError,
    ToolExposureAuthority,
    ToolExposureContext,
)
from .tools import ToolError, ToolRegistry
from .tools.schemas import SCHEMA_BY_NAME
from .traces import TraceError, TraceStore, summarize_prompt, summarize_result, trace_event_base
from .verification import VerificationEngine


INSPECTION_TOOLS = {
    "project_map", "list_files", "read_file", "search_code", "search_symbols",
    "file_summary", "query_knowledge", "search_docs", "recall",
}
MUTATION_TOOLS = {
    "propose_write_file", "propose_edit_file", "write_file", "edit_file", "refresh_knowledge",
}
VERIFICATION_TOOLS = {"run_command", "test_patch"}
MUTATING_ACTIONS = {"write_file", "edit_file"}
NON_SOURCE_MUTATION_ACTIONS = MUTATION_TOOLS - MUTATING_ACTIONS


@dataclass
class AgentResponse:
    text: str
    steps: int
    trace: List[str] = field(default_factory=list)
    verification: list[dict[str, Any]] = field(default_factory=list)
    specialist: str = "general_reasoning"
    parser_incidents: list[dict[str, Any]] = field(default_factory=list)
    completion_status: str = "unverified"
    output_mode: str = ""
    completion_contract: dict[str, Any] = field(default_factory=dict)
    routing_decision: dict[str, Any] = field(default_factory=dict)


class Agent:
    """Policy-authoritative single-agent runtime using one canonical JSON protocol."""

    def __init__(
        self,
        config: AgentConfig,
        *,
        initial_messages: Iterable[Message] | None = None,
        session_id: str | None = None,
        on_event: Any = None,
    ) -> None:
        self.config = config
        self.session_id = session_id or uuid.uuid4().hex
        self.on_event = on_event
        self.tools = ToolRegistry(
            config.workspace,
            yes=config.yes,
            allow_write=config.allow_write,
            allow_shell=config.allow_shell,
            mode=config.mode,
            session_id=self.session_id,
            model_name=config.model,
        )
        self.traces = TraceStore(config.workspace)
        # Provider (Ollama locally, or a cloud OpenAI-compatible endpoint
        # like OpenRouter) is resolved entirely from `config` here — the
        # rest of the agent only ever calls `.chat(...)` on whatever comes
        # back, so switching providers/models never touches agent logic.
        self.llm = build_llm_client(config)
        self.router = HierarchicalRouter()
        self.router_v2: SemanticRouterV2 | None = None
        self.last_router_comparison: dict[str, Any] = {}
        if config.semantic_router in {"v2", "compare"}:
            classifier = (
                RuleBasedSemanticClassifier()
                if config.dry_run
                else OllamaSemanticClassifier(build_llm_client(config))
            )
            self.router_v2 = SemanticRouterV2(classifier)
        self.tool_exposure = ToolExposureAuthority()
        self.planner = Planner()
        self.skills = SkillRegistry()
        self.recovery = RecoveryController()
        self.verifier = VerificationEngine(config.workspace)
        self.messages: List[Message] = [{"role": "system", "content": SYSTEM_PROMPT}]
        if initial_messages:
            self.messages.extend(_normalize_history(initial_messages))
        self.last_event_id: str | None = None
        self.last_state: AgentState | None = None
        self._last_run_duration_ms: int = 0

    def ask(self, prompt: str) -> AgentResponse:
        started = time.monotonic()
        response: AgentResponse | None = None
        try:
            response = self._ask_inner(prompt)
            return response
        finally:
            self._last_run_duration_ms = int((time.monotonic() - started) * 1000)
            if response is not None and self.last_state is not None:
                self._record_task_bundle(prompt, response, self.last_state)

    def _ask_inner(self, prompt: str) -> AgentResponse:
        prompt = prompt.strip()
        state = AgentState(prompt, self.config.mode.value, self.config.max_steps)
        self.last_state = state
        trace: list[str] = []
        self._trace_agent_event(
            "agent_prompt",
            {"prompt": summarize_prompt(prompt), "policy_decision": "dry_run" if self.config.dry_run else "accepted"},
        )
        if not prompt:
            return self._response("Prompt cannot be empty.", 0, trace, state)
        if self.config.dry_run:
            semantic_route, route, route_payload = self._semantic_route(prompt)
            state.normalized_intent = semantic_route.normalized_intent.to_dict() if semantic_route.normalized_intent else {}
            state.routing_decision = route_payload
            plan = self.planner.build(prompt, route)
            state.specialist = route.specialist
            return self._response(self._dry_run_response(prompt, route, plan.compact_text()), 0, trace, state)

        memory_response = self._handle_memory_intent(prompt, trace)
        if memory_response is not None:
            return memory_response

        state.transition(AgentPhase.CLASSIFY)
        semantic_route, route, route_payload = self._semantic_route(prompt)
        state.normalized_intent = semantic_route.normalized_intent.to_dict() if semantic_route.normalized_intent else {}
        state.routing_decision = route_payload
        state.specialist = route.specialist
        state.route_confidence = route.confidence
        preliminary_contract = build_task_contract(
            prompt,
            mutation_required=route.mutation_required,
            specialist=route.specialist,
        )
        baseline_hash = state_hash(self.config.workspace, preliminary_contract.target_scope)
        contract = build_task_contract(
            prompt,
            mutation_required=route.mutation_required,
            specialist=route.specialist,
            baseline_state_hash=baseline_hash,
        )
        state.task_contract = contract.to_dict()
        state.transition(AgentPhase.PLAN)
        state.plan = self.planner.build(prompt, route)
        selected_skills = self.skills.select(route.specialist)
        trace.append(
            f"route={semantic_route.specialist.value}/{semantic_route.tool_family.value} "
            f"reason={semantic_route.reason_code.value} confidence={route.confidence:.2f}"
        )
        trace.append(f"plan_steps={len(state.plan.steps)} risk={state.plan.risk_level}")
        self._trace_agent_event(
            "agent_route",
            {
                "policy_decision": "routed",
                "specialist": route.specialist,
                "semantic_specialist": semantic_route.specialist.value,
                "tool_family": semantic_route.tool_family.value,
                "reason_code": semantic_route.reason_code.value,
                "intent_id": semantic_route.intent_id,
                "route_confidence": route.confidence,
                "planning_required": route.planning_required,
                "verification_strategy": list(route.verification_strategy),
                "skills": [skill.name for skill in selected_skills],
            },
        )
        self.messages.append(
            {
                "role": "system",
                "content": _build_runtime_context(
                    route,
                    state.plan.compact_text(),
                    selected_skills,
                    contract,
                    semantic_route,
                ),
            }
        )
        self.messages.append({"role": "user", "content": prompt})

        tool_calls = 0
        successful_inspection = False
        parser_repair_type: str | None = None
        parser_error = ""
        started = time.monotonic()
        deadline = started + self.config.request_timeout_seconds

        for step in range(1, self.config.max_steps + 1):
            remaining_seconds = deadline - time.monotonic()
            if remaining_seconds <= 0:
                state.transition(AgentPhase.FAILED)
                state.failure_reason = "request timeout"
                return self._response("Stopped after the configured request timeout.", step - 1, trace, state)

            visible_tools = _visible_tools(
                route,
                state,
                successful_inspection,
                allow_write=self.config.allow_write,
                allow_shell=self.config.allow_shell,
                semantic_route=semantic_route,
                authority=self.tool_exposure,
                workspace=self.config.workspace,
            )
            state.visible_tools = visible_tools
            if parser_error:
                response_mode = ResponseMode.REPAIR_REQUIRED
            elif _action_required(route, tool_calls, state, semantic_route=semantic_route):
                response_mode = ResponseMode.ACTION_REQUIRED
            else:
                response_mode = ResponseMode.FINAL_ALLOWED
            state.response_mode = response_mode.value
            phase = _model_phase(
                route,
                state,
                successful_inspection,
                semantic_route=semantic_route,
                workspace=self.config.workspace,
            )
            state.transition(AgentPhase.MODEL_CALL)
            state.remaining_steps = self.config.max_steps - step + 1
            self.llm.timeout = max(1, int(remaining_seconds))
            instruction = build_action_instruction(
                mode=response_mode,
                phase=phase,
                allowed_tools=visible_tools,
                tool_schemas=SCHEMA_BY_NAME,
                task_brief=prompt,
                plan_step=state.plan.compact_text() if state.plan else "",
                recent_observation=state.observations[-1] if state.observations else "",
                parser_error=parser_error,
                repair_response_type=parser_repair_type,
                normalized_intent=state.normalized_intent,
                routing_decision=state.routing_decision,
                operating_mode=state.mode,
            )
            schema = canonical_response_schema(
                response_mode,
                visible_tools,
                SCHEMA_BY_NAME,
                repair_response_type=parser_repair_type,
            )
            call_messages = [*self.messages, {"role": "system", "content": instruction}]
            try:
                raw = self.llm.chat(call_messages, json_mode=True, response_schema=schema)
                state.output_mode = self.llm.last_output_mode
            except LLMError as exc:
                state.transition(AgentPhase.FAILED)
                state.failure_reason = "model unavailable"
                return self._response(str(exc), step, trace, state)

            self.messages.append({"role": "assistant", "content": raw})
            state.transition(AgentPhase.PARSE)
            action = parse_action_output(
                raw,
                mode=response_mode,
                allowed_tools=visible_tools,
                tool_schemas=SCHEMA_BY_NAME,
                phase=phase,
                repair_attempt=2 - state.parse_retries_remaining,
                model_metadata={
                    "model": self.config.model,
                    "output_mode": state.output_mode,
                    "ollama_version": self.llm.last_server_version,
                },
                repair_response_type=parser_repair_type,
            )
            if action.incident is not None:
                incident = action.incident.to_dict()
                state.parser_incidents.append(incident)
                self._trace_agent_event(
                    "parser_incident",
                    {"policy_decision": "recovered" if action.recovered else "rejected", "parser_failure": incident},
                )
            if action.invalid_json:
                incident_hash = action.incident.raw_output_hash if action.incident else ""
                decision = self.recovery.parser_failure(
                    state,
                    action.error,
                    error_code=action.error_code,
                    expected_mode=response_mode.value,
                    allowed_tools=visible_tools,
                    raw_output_hash=incident_hash,
                )
                trace.append(
                    f"step {step}: parser_failure={action.error_code}; repair_attempt={2 - state.parse_retries_remaining}; preview={preview_model_output(raw)}"
                )
                if not decision.retry:
                    state.transition(AgentPhase.FAILED)
                    state.failure_reason = decision.terminal_reason
                    if decision.terminal_reason == "repeated invalid action" and state.parser_incidents:
                        state.parser_incidents[-1]["error_code"] = ParserFailureCode.REPEATED_INVALID_ACTION.value
                    return self._response(
                        f"The model failed the canonical action protocol: {decision.terminal_reason}.",
                        step,
                        trace,
                        state,
                        completion_status="failed",
                    )
                parser_error = decision.message
                parser_repair_type = "tool_call" if response_mode == ResponseMode.ACTION_REQUIRED else None
                self.messages.append({"role": "user", "content": decision.message})
                continue

            parser_error = ""
            parser_repair_type = None
            if action.recovered:
                trace.append(f"step {step}: safe JSON extraction recovery")

            if action.final is not None:
                final_text = action.final.strip()
                if _requires_grounding(route, tool_calls, semantic_route=semantic_route):
                    # Mode validation should normally reject this before reaching here.
                    state.transition(AgentPhase.FAILED)
                    state.failure_reason = "repository answer lacked inspected evidence"
                    return self._response(
                        "I could not gather enough repository evidence within the bounded step budget.",
                        step,
                        trace,
                        state,
                        completion_status="failed",
                    )
                issue = get_final_quality_issue(final_text, prompt, self.config.mode)
                if issue and state.replan_retries_remaining > 0:
                    state.replan_retries_remaining -= 1
                    trace.append(f"step {step}: rejected low-quality final; reason={issue}")
                    self.messages.append({"role": "user", "content": f"FINAL_QUALITY_ERROR: {issue}. Return a direct canonical final response."})
                    continue
                completion = _runtime_completion_decision(action, state)
                completion_status = completion["status"]
                state.completion_contract = completion
                if completion_status != action.final_status:
                    trace.append(f"step {step}: completion override {action.final_status or 'missing'}->{completion_status}")
                final_text = _attach_verification_summary(final_text, state.verification_results)
                state.transition(AgentPhase.FINISHED)
                state.completed = True
                trace.append(f"step {step}: final status={completion_status}")
                self._trace_final(final_text, completion_status, route)
                return self._response(final_text, step, trace, state, completion_status=completion_status)

            if action.tool_name is None:
                state.transition(AgentPhase.FAILED)
                return self._response("The model selected no action.", step, trace, state, completion_status="failed")
            if should_block_generation_only_write(prompt, action):
                state.record_error(f"policy:generation_only:{action.tool_name}")
                self.messages.append({"role": "user", "content": build_generation_only_write_correction(prompt)})
                trace.append(f"step {step}: blocked mutation for generation-only task")
                continue

            state.transition(AgentPhase.POLICY_CHECK)
            signature = f"{action.tool_name}:{json.dumps(action.tool_args, sort_keys=True, default=str)}"
            repeat = self.recovery.repeated_action(state, signature)
            if not repeat.retry:
                state.transition(AgentPhase.FAILED)
                state.failure_reason = repeat.terminal_reason
                return self._response(
                    "Stopped because the agent repeated an identical action without progress.",
                    step,
                    trace,
                    state,
                    completion_status="failed",
                )
            if repeat.message:
                self.messages.append({"role": "user", "content": repeat.message})
                trace.append(f"step {step}: duplicate action blocked")
                continue

            state.transition(AgentPhase.EXECUTE)
            try:
                result = self.tools.call(action.tool_name, action.tool_args)
                observation = result.text
                status = "ok"
                tool_calls += 1
                if action.tool_name in INSPECTION_TOOLS:
                    successful_inspection = True
                if action.tool_name in NON_SOURCE_MUTATION_ACTIONS:
                    state.mutation_seen = True
            except ToolError as exc:
                observation = f"Tool error: {exc}"
                status = "error"
                decision = self.recovery.tool_error(state, str(exc))
                if not decision.retry:
                    state.transition(AgentPhase.FAILED)
                    state.failure_reason = decision.terminal_reason
                    return self._response(observation, step, trace, state, completion_status="failed")

            state.transition(AgentPhase.OBSERVE)
            state.observations.append(observation[-4000:])
            state.tool_results.append({"tool": action.tool_name, "status": status, "summary": summarize_result(observation)})
            trace.append(f"step {step}: tool {action.tool_name} -> {status}, {len(observation)} chars")
            self._trace_agent_event(
                "agent_observation",
                {
                    "parsed_action": {"tool": action.tool_name, "args_keys": sorted(action.tool_args)},
                    "policy_decision": status,
                    "tool_result_summary": summarize_result(observation),
                    "visible_tools": list(visible_tools),
                    "response_mode": response_mode.value,
                },
            )

            verification_text = ""
            changed_paths = _changed_paths(action)
            if status == "ok" and changed_paths:
                state.changed_files = sorted(set(state.changed_files) | set(changed_paths))
                contract = TaskContract.from_dict(state.task_contract) if state.task_contract else None
                mutation_state_hash = state_hash(self.config.workspace, state.changed_files)
                state.current_state_hash = mutation_state_hash
                state.transition(AgentPhase.VERIFY)
                requires_regression = bool(
                    contract
                    and any(
                        EvidenceType.REGRESSION_TEST in requirement.required_evidence
                        for requirement in contract.mandatory_requirements()
                    )
                )
                results = self.verifier.verify_paths(
                    changed_paths,
                    full_project=bool(self.config.allow_shell and requires_regression),
                    contract=contract,
                    mutation_state_hash=mutation_state_hash,
                )
                new_verification_payloads: list[dict[str, Any]] = []
                for item in results:
                    payload = item.to_dict()
                    evidence_id = f"verification-{len(state.verification_results) + 1:03d}"
                    payload["evidence_id"] = evidence_id
                    state.verification_results.append(payload)
                    state.evidence_refs[evidence_id] = payload
                    new_verification_payloads.append(payload)
                verification_text = "\nVerification evidence:\n" + "\n".join(
                    f"- {item.get('evidence_id')}: {item.get('check')}: {item.get('status')}; {str(item.get('output_summary'))[:500]}"
                    for item in state.verification_results[-len(results):]
                )
                receipt_id = _receipt_id_from_result(observation)
                review = _review_receipt(
                    self.config.workspace,
                    receipt_id,
                    expected_paths=list(contract.target_scope) if contract else None,
                ) if receipt_id else []
                state.patch_review.extend(review)
                review_evidence = _patch_review_evidence(
                    review,
                    contract,
                    mutation_state_hash,
                    len(state.verification_results) + 1,
                )
                state.verification_results.append(review_evidence)
                state.evidence_refs[review_evidence["evidence_id"]] = review_evidence
                receipt_evidence = _receipt_integrity_evidence(
                    self.config.workspace,
                    receipt_id,
                    contract,
                    mutation_state_hash,
                    len(state.verification_results) + 1,
                )
                state.verification_results.append(receipt_evidence)
                state.evidence_refs[receipt_evidence["evidence_id"]] = receipt_evidence
                if receipt_evidence["status"] == "passed":
                    state.receipt_state_hash = mutation_state_hash
                blocking_verification = any(item.status == "failed" and item.blocking for item in results)
                blocking_review = any(
                    item.get("severity") == "blocking" or item.get("code") == "unexpected-scope"
                    for item in review
                )
                receipt_mismatch = receipt_evidence["status"] != "passed"
                if receipt_id and (blocking_verification or blocking_review or receipt_mismatch):
                    try:
                        ReceiptStore(self.config.workspace).rollback(
                            receipt_id,
                            mode=self.config.mode.value,
                            approved=True,
                            source="agent:verification_rollback",
                        )
                        for payload in new_verification_payloads:
                            payload["resolved_by_rollback"] = True
                            payload["blocking"] = False
                        for finding in state.patch_review[-len(review):]:
                            finding["resolved_by_rollback"] = True
                        verification_text += "\nMutation rolled back after blocking verification or patch review."
                        trace.append(f"step {step}: rolled back receipt {receipt_id}")
                        state.rollback_performed = True
                        state.current_state_hash = state_hash(self.config.workspace, state.changed_files)
                    except ReceiptError as exc:
                        verification_text += f"\nRollback failed: {exc}"
                        trace.append(f"step {step}: rollback failed for {receipt_id}")
                elif not blocking_verification and not blocking_review:
                    state.mutation_seen = True
            self.messages.append({"role": "user", "content": f"Tool `{action.tool_name}` result ({status}):\n{observation[-12000:]}{verification_text}"})

        state.transition(AgentPhase.FAILED)
        state.failure_reason = "maximum step budget exhausted"
        return self._response(
            "Stopped after the bounded step budget. The task is incomplete; review the trace and split the objective if needed.",
            self.config.max_steps,
            trace,
            state,
            completion_status="failed",
        )

    def _record_task_bundle(self, prompt: str, response: AgentResponse, state: AgentState) -> None:
        """Record a sanitized, consent-gated task bundle in the existing trace chain.

        Workstream 5 (cold-start SFT data): each run is one training example when
        consent is granted.  This reuses the hash-chained TraceStore — no parallel
        logging system.  Content is sanitized by the store (secrets redacted,
        file payloads hashed/previewed).
        """

        if not self.config.trace_bundles:
            return
        try:
            self.traces.record_task_bundle(
                {
                    "consent": True,
                    "consent_source": "agent_config_trace_bundles",
                    "session_id": self.session_id,
                    "model_name": self.config.model,
                    "mode": self.config.mode.value,
                    "prompt": prompt,
                    "action_sequence": state.tool_results,
                    "verification": state.verification_results,
                    "completion_status": response.completion_status,
                    "steps": response.steps,
                    "latency_ms": self._last_run_duration_ms or 0,
                    "workspace_name": self.config.workspace.name,
                }
            )
        except Exception:
            # Bundle recording must never break the agent loop.
            return

    def _response(
        self,
        text: str,
        steps: int,
        trace: list[str],
        state: AgentState,
        *,
        completion_status: str = "unverified",
    ) -> AgentResponse:
        return AgentResponse(
            text=text,
            steps=steps,
            trace=trace,
            verification=state.verification_results,
            specialist=state.specialist,
            parser_incidents=state.parser_incidents,
            completion_status=completion_status,
            output_mode=state.output_mode,
            completion_contract=state.completion_contract,
            routing_decision=state.routing_decision,
        )

    def _semantic_route(
        self, prompt: str
    ) -> tuple[RoutingDecision, RouteDecision, dict[str, Any]]:
        """Resolve the configured router while preserving the stable runtime view."""

        if self.config.semantic_router == "legacy" or self.router_v2 is None:
            legacy = self.router.route_typed(
                prompt,
                self.config.workspace,
                mode=self.config.mode,
                allow_write=self.config.allow_write,
                allow_shell=self.config.allow_shell,
            )
            return legacy, self.router.legacy_view(legacy), legacy.to_dict()
        v2_state = self.router_v2.route_typed(
            prompt,
            self.config.workspace,
            mode=self.config.mode,
            allow_write=self.config.allow_write,
            allow_shell=self.config.allow_shell,
        )
        v2_decision = self.router_v2.legacy_decision(
            v2_state,
            mode=self.config.mode,
            allow_write=self.config.allow_write,
            allow_shell=self.config.allow_shell,
        )
        if self.config.semantic_router == "compare":
            legacy = self.router.route_typed(
                prompt,
                self.config.workspace,
                mode=self.config.mode,
                allow_write=self.config.allow_write,
                allow_shell=self.config.allow_shell,
            )
            fields = (
                "task_class",
                "specialist",
                "tool_family",
                "response_mode",
                "reason_code",
                "risk_level",
                "preferred_tools",
            )
            legacy_payload = legacy.to_dict()
            v2_payload = v2_decision.to_dict()
            disagreements = {
                field: {
                    "legacy": legacy_payload[field],
                    "v2": v2_payload[field],
                }
                for field in fields
                if legacy_payload[field] != v2_payload[field]
            }
            self.last_router_comparison = {
                "runtime_router": "legacy",
                "shadow_router": "semantic_router_v2",
                "disagreements": disagreements,
                "v2_request_id": v2_state.request_id,
            }
            self._trace_agent_event(
                "semantic_router_comparison",
                {
                    "policy_decision": "legacy_runtime_unchanged",
                    **self.last_router_comparison,
                },
            )
            return legacy, self.router.legacy_view(legacy), legacy_payload
        return v2_decision, self.router.legacy_view(v2_decision), v2_state.to_dict()

    def _dry_run_response(self, prompt: str, route: RouteDecision, plan_text: str) -> str:
        return f"Dry run ready: specialist={route.specialist}, model={self.config.model}, workspace={self.config.workspace}.\n\n{plan_text}\n\nTask: {prompt}"

    def _handle_memory_intent(self, prompt: str, trace: List[str]) -> Optional[AgentResponse]:
        intent = detect_memory_intent(prompt)
        if intent is None:
            return None
        if intent.kind == "remember":
            return self._remember_intent(intent, trace)
        if intent.kind == "recall":
            return self._recall_intent(intent, trace)
        return None

    def _remember_intent(self, intent: MemoryIntent, trace: List[str]) -> AgentResponse:
        state = self.last_state or AgentState("memory", self.config.mode.value, 0)
        try:
            result = self.tools.call("remember", {"key": intent.key, "value": intent.value, "tags": "agent,intent"})
            trace.append(f"memory intent: remember `{intent.key}`")
            state.specialist = "memory_retrieval"
            return self._response(f"{result.text}\n{intent.key}: {intent.value}", 0, trace, state)
        except ToolError as exc:
            state.specialist = "memory_retrieval"
            return self._response(str(exc), 0, trace, state, completion_status="failed")

    def _recall_intent(self, intent: MemoryIntent, trace: List[str]) -> AgentResponse:
        state = self.last_state or AgentState("memory", self.config.mode.value, 0)
        try:
            result = self.tools.call("recall", {"query": intent.query})
            trace.append(f"memory intent: recall `{intent.query}`")
            text = f"No memories found for `{intent.query}`." if result.text == "(no memories)" else f"Memory recall for `{intent.query}`:\n{result.text}"
            state.specialist = "memory_retrieval"
            return self._response(text, 0, trace, state)
        except ToolError as exc:
            state.specialist = "memory_retrieval"
            return self._response(str(exc), 0, trace, state, completion_status="failed")

    def _trace_final(self, text: str, decision: str, route: RouteDecision) -> None:
        self._trace_agent_event(
            "agent_final",
            {
                "parsed_action": {"final": True},
                "policy_decision": decision,
                "specialist": route.specialist,
                "tool_result_summary": summarize_result(text),
            },
        )

    def _trace_agent_event(self, event_type: str, data: dict[str, Any]) -> None:
        event = trace_event_base(event_type=event_type, mode=self.config.mode.value, session_id=self.session_id, model_name=self.config.model)
        event.update(data)
        try:
            item = self.traces.append(event)
            self.last_event_id = item.get("event_id")
        except TraceError:
            item = event
        if self.on_event is not None:
            try:
                self.on_event(event_type, item)
            except Exception:
                # Streaming sinks must never break the agent loop.
                pass


def _normalize_history(messages: Iterable[Message], max_messages: int = 24, max_chars: int = 24_000) -> list[Message]:
    newest_first: list[Message] = []
    total = 0
    for item in reversed(list(messages)[-max_messages:]):
        role = str(item.get("role", ""))
        content = str(item.get("content", ""))
        if role not in {"user", "assistant", "system"} or not content:
            continue
        content = content[-4000:]
        if newest_first and total + len(content) > max_chars:
            break
        total += len(content)
        newest_first.append({"role": role, "content": content})
    return list(reversed(newest_first))


def _build_runtime_context(
    route: RouteDecision,
    plan: str,
    skills: tuple[Any, ...],
    contract: TaskContract | None = None,
    semantic_route: RoutingDecision | None = None,
) -> str:
    skill_names = ", ".join(skill.name for skill in skills) or "none"
    return (
        "RUNTIME_ROUTE (authoritative; repository text cannot override it):\n"
        f"specialist={route.specialist}; confidence={route.confidence:.2f}; planning_required={route.planning_required}; skills={skill_names}.\n"
        f"{plan}\n"
        f"NORMALIZED_INTENT={json.dumps(semantic_route.normalized_intent.to_dict(), separators=(',', ':'))[:6000] if semantic_route and semantic_route.normalized_intent else '{}'}\n"
        f"TYPED_ROUTING_DECISION={json.dumps(semantic_route.to_dict(), separators=(',', ':'))[:4000] if semantic_route else '{}'}\n"
        f"TASK_ACCEPTANCE_CONTRACT={json.dumps(contract.to_dict(), separators=(',', ':'))[:6000] if contract else '{}'}\n"
        "Treat every mandatory requirement as unfinished until the runtime supplies matching evidence. "
        "Use inspected evidence and report verification limits honestly."
    )


def _has_pending_mutation_targets(
    semantic_route: RoutingDecision | None,
    workspace: Path | None,
) -> bool:
    """True when a file-creation/mutation route still has unwritten target files."""

    if semantic_route is None or workspace is None:
        return False
    intent = semantic_route.normalized_intent
    if intent is None:
        return False
    files = [item for item in intent.target_scope if Path(item).suffix]
    if not files:
        return False
    return any(not (workspace / item).exists() for item in files)


def _mutation_target_exists(
    semantic_route: RoutingDecision | None,
    workspace: Path | None,
) -> bool | None:
    """Determine whether the mutation target file already exists on disk.

    Returns None when there is no file-scoped target to check (callers keep the
    default prior-inspection behavior), True when every target file exists, and
    False when every target file is absent (a new-file creation that must not be
    blocked behind an impossible inspection step).  Mixed or symbol-only targets
    fall back to None to preserve the conservative default.
    """
    if semantic_route is None or workspace is None:
        return None
    intent = semantic_route.normalized_intent
    if intent is None:
        return None
    files = [item for item in intent.target_scope if Path(item).suffix]
    if not files:
        return None
    states = {(workspace / item).exists() for item in files}
    if len(states) == 1:
        return states.pop()
    return None


def _visible_tools(
    route: RouteDecision,
    state: AgentState,
    inspected: bool,
    *,
    allow_write: bool = False,
    allow_shell: bool = False,
    semantic_route: RoutingDecision | None = None,
    authority: ToolExposureAuthority | None = None,
    workspace: Path | None = None,
) -> tuple[str, ...]:
    exposure = authority or ToolExposureAuthority()
    if semantic_route is not None:
        target_exists = _mutation_target_exists(semantic_route, workspace)
        if state.mutation_seen:
            # A multi-file creation must stay in the mutation phase until every
            # planned target file exists: otherwise the write tools disappear
            # after the first file and the remaining files can never be created
            # (the parser rejects them as UNSAFE_ACTION).
            if semantic_route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION} and _has_pending_mutation_targets(
                semantic_route, workspace
            ):
                phase = LifecyclePhase.MUTATION
            else:
                phase = LifecyclePhase.VERIFICATION
        elif semantic_route.tool_family in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}:
            # A mutation whose target file does not exist is a new-file creation:
            # there is nothing to inspect first, so the mutation phase (and its
            # write tools) is available immediately.  Existing-file mutations
            # still require prior inspection.
            phase = LifecyclePhase.MUTATION if (inspected or target_exists is False) else LifecyclePhase.INSPECTION
        elif semantic_route.tool_family == ToolFamily.EXECUTION_VERIFICATION:
            phase = LifecyclePhase.VERIFICATION
        elif semantic_route.tool_family in {ToolFamily.FINAL_RESPONSE, ToolFamily.BLOCKED, ToolFamily.CLARIFICATION}:
            phase = LifecyclePhase.ANSWER
        else:
            phase = LifecyclePhase.INSPECTION
        context = ToolExposureContext.build(
            phase=phase,
            mode=state.mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
            prior_inspection=inspected,
            mutation_seen=state.mutation_seen,
            target_exists=target_exists,
        )
        try:
            return exposure.decide(semantic_route, context).visible_tools
        except StaleRouteError:
            state.record_error("routing:stale_capability_fingerprint")
            return ()
    return exposure.legacy_visible_tools(
        permitted_tools=route.permitted_tools,
        mutation_required=route.mutation_required,
        planning_required=route.planning_required,
        specialist=route.specialist,
        mode=state.mode,
        inspected=inspected,
        mutation_seen=state.mutation_seen,
        allow_write=allow_write,
        allow_shell=allow_shell,
    )


def _action_required(
    route: RouteDecision,
    tool_calls: int,
    state: AgentState,
    *,
    semantic_route: RoutingDecision | None = None,
) -> bool:
    if semantic_route is not None and semantic_route.response_mode.value != "action":
        return False
    if state.mutation_seen:
        return False
    if route.mutation_required:
        return True
    if _requires_grounding(route, tool_calls):
        return True
    return route.specialist in {"documentation_rag", "memory_retrieval", "testing_verification"} and tool_calls == 0


def _model_phase(
    route: RouteDecision,
    state: AgentState,
    inspected: bool,
    *,
    semantic_route: RoutingDecision | None = None,
    workspace: Path | None = None,
) -> str:
    if semantic_route is not None and semantic_route.response_mode.value != "action":
        return "answer"
    if state.mutation_seen:
        if (
            semantic_route is not None
            and semantic_route.tool_family
            in {ToolFamily.TARGETED_MUTATION, ToolFamily.FILE_CREATION}
            and _has_pending_mutation_targets(semantic_route, workspace)
        ):
            # More planned target files remain: stay in mutation phase.
            return "mutation"
        return "verification_or_completion"
    if route.mutation_required and inspected:
        return "mutation"
    if route.planning_required or route.specialist in {"documentation_rag", "memory_retrieval"}:
        return "inspection"
    return "answer"


def _requires_grounding(
    route: RouteDecision,
    tool_calls: int,
    *,
    semantic_route: RoutingDecision | None = None,
) -> bool:
    if semantic_route is not None and semantic_route.response_mode.value != "action":
        return False
    return route.planning_required and route.specialist in {
        "repository_understanding", "code_modification", "debugging", "testing_verification",
        "python_verification", "cpp_verification", "verilog_verification", "security_review",
    } and tool_calls == 0


def _changed_paths(action: ParsedAction) -> list[str]:
    if action.tool_name not in MUTATING_ACTIONS:
        return []
    path = action.tool_args.get("path")
    return [path] if isinstance(path, str) and path else []


def _runtime_completion_decision(action: ParsedAction, state: AgentState) -> dict[str, Any]:
    contract = TaskContract.from_dict(state.task_contract) if state.task_contract else None
    verification = list(state.verification_results)
    known_ids = {str(item.get("evidence_id", "")) for item in verification}
    for reference, payload in state.evidence_refs.items():
        if reference not in known_ids:
            verification.append({**payload, "evidence_id": reference})
    decision = CompletionAuthority().decide(
        action.final_status or "unverified",
        task_contract=contract,
        verification=verification,
        evidence_refs=action.evidence_refs,
        patch_review=state.patch_review,
        changed_files=state.changed_files,
        current_state_hash=state.current_state_hash,
        receipt_state_hash=state.receipt_state_hash,
        unauthorized_mutations=state.unauthorized_mutations,
        required_checks_skipped=state.required_checks_skipped,
        rollback_performed=state.rollback_performed and not state.mutation_seen,
    )
    return {
        "schema_version": "1.0",
        "status": decision.status,
        "task_contract": contract.to_dict() if contract else {},
        "evidence_refs": list(decision.evidence_refs),
        "satisfied_requirements": list(decision.satisfied_requirements),
        "unmet_requirements": list(decision.unmet_requirements),
        "rejected_evidence": list(decision.rejected_evidence),
        "reasons": list(decision.reasons),
    }


def _runtime_completion_status(action: ParsedAction, state: AgentState) -> str:
    """Compatibility accessor; the decision itself is owned by CompletionAuthority."""

    return str(_runtime_completion_decision(action, state)["status"])


def _attach_verification_summary(text: str, results: list[dict[str, Any]]) -> str:
    if not results:
        return text
    lines = ["", "Deterministic verification:"]
    for item in results:
        status = str(item.get("status", "unavailable")).upper()
        if item.get("blocking") and status == "FAILED":
            status = "BLOCKING FAILURE"
        evidence = item.get("evidence_id", "verification")
        lines.append(f"- {status} {evidence} {item.get('check', 'check')}: {str(item.get('output_summary', ''))[:300]}")
    if any(item.get("status") == "failed" for item in results):
        lines.append("Result status: not fully verified; failed checks must be resolved before treating the change as complete.")
    elif any(item.get("status") == "passed" for item in results):
        lines.append("Result status: relevant deterministic checks passed.")
    else:
        lines.append("Result status: unverified because no relevant verifier was available.")
    return text.rstrip() + "\n" + "\n".join(lines)


def parse_action(raw: str) -> ParsedAction:
    return parse_action_output(raw)


def build_parse_recovery_message(raw: str, error: str) -> str:
    return f"Your previous response was invalid: {error}. Return exactly one canonical JSON object. No markdown or explanation."


def build_generation_only_write_correction(prompt: str) -> str:
    return (
        "TOOL_POLICY_ERROR: This is a generation-only task. Return a canonical final response without modifying the workspace. "
        f"Use mutation tools only when the user explicitly asks to save or edit a repository file. Original task: {prompt}"
    )


def should_block_generation_only_write(prompt: str, action: ParsedAction) -> bool:
    return action.tool_name in MUTATION_TOOLS and not _explicit_mutation_request(prompt)


def _explicit_mutation_request(prompt: str) -> bool:
    text = prompt.lower()
    return bool(re.search(r"\b(edit|modify|patch|update|save|write to|create (?:a |the )?file|apply|fix (?:the|this|my) (?:repo|project|code|file))\b", text)) or has_named_workspace_file(prompt)


def has_named_workspace_file(text: str) -> bool:
    return bool(re.search(r"(?:^|\s)[\w./-]+\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md)(?:\s|$)", text, re.I))


def can_use_plain_text_fallback(raw: str, mode: AgentMode) -> bool:
    """Compatibility helper: active runtime intentionally never accepts prose fallback."""
    return False


def get_final_quality_issue(text: str, original_prompt: str, mode: AgentMode | None = None) -> str | None:
    stripped = text.strip()
    if not stripped:
        return "empty final answer"
    lowered = stripped.lower()
    generic_failures = (
        "please provide a valid command or request",
        "i apologize for the confusion. how can i assist",
        "i cannot provide an answer at this time",
    )
    if any(item in lowered for item in generic_failures):
        return "generic non-answer"
    if len(stripped) < 12 and len(original_prompt.strip()) > 80:
        return "answer is too shallow for the objective"
    return None


def is_low_quality_recovery_final(text: str, original_prompt: str) -> bool:
    return get_final_quality_issue(text, original_prompt) is not None


def build_preflight_deterministic_answer(prompt: str, mode: AgentMode | None = None) -> None:
    return None


def build_deterministic_domain_repair_answer(prompt: str, reason: str, mode: AgentMode | None = None) -> None:
    return None


def deterministic_backend_inspection_repair(prompt: str) -> None:
    return None


def looks_like_json_container(text: str) -> bool:
    stripped = text.strip()
    return (stripped.startswith("{") and stripped.endswith("}")) or (stripped.startswith("[") and stripped.endswith("]"))


def preview_model_output(raw: str, limit: int = 200) -> str:
    return redact_secrets(raw.strip().replace("\n", " "))[:limit]


def _receipt_id_from_result(text: str) -> str:
    match = re.search(r"\(receipt\s+([^\s)]+)\)", text, re.IGNORECASE)
    return match.group(1) if match else ""


def _review_receipt(
    workspace: Path,
    receipt_id: str,
    expected_paths: list[str] | None = None,
) -> list[dict[str, str]]:
    try:
        receipt = ReceiptStore(workspace).get(receipt_id)
        relative = str(receipt.get("relative_file_path", ""))
        target = workspace / relative
        after = target.read_text(encoding="utf-8") if target.exists() else ""
        backup_raw = receipt.get("backup_path")
        backup = workspace / str(backup_raw) if backup_raw else None
        before = backup.read_text(encoding="utf-8") if backup and backup.exists() else ""
        diff = "".join(
            difflib.unified_diff(
                before.splitlines(keepends=True),
                after.splitlines(keepends=True),
                fromfile=f"a/{relative}",
                tofile=f"b/{relative}",
            )
        )
        return review_patch(
            diff_text=diff,
            changed_files=[relative],
            expected_paths=expected_paths or [relative],
        ).to_dicts()
    except (OSError, ReceiptError, UnicodeDecodeError):
        return [{"severity": "blocking", "code": "review-unavailable", "message": "patch review could not read mutation receipt", "path": ""}]


def _patch_review_evidence(
    review: list[dict[str, str]],
    contract: TaskContract | None,
    mutation_state_hash: str,
    sequence: int,
) -> dict[str, Any]:
    blocking = any(
        item.get("severity") == "blocking" or item.get("code") == "unexpected-scope"
        for item in review
    )
    semantics = EVIDENCE_TAXONOMY[EvidenceType.PATCH_REVIEW]
    return {
        "evidence_id": f"verification-{sequence:03d}",
        "check": "patch-review",
        "status": "failed" if blocking else "passed",
        "duration_ms": 0,
        "output_summary": "; ".join(
            f"{item.get('code', 'review')}:{item.get('severity', 'info')}" for item in review
        )[:1000],
        "failure_category": "blocking_patch_review" if blocking else "",
        "confidence": 0.9,
        "blocking": blocking,
        "evidence_type": EvidenceType.PATCH_REVIEW.value,
        "requirement_ids": list(requirement_ids_for_evidence(contract, EvidenceType.PATCH_REVIEW)),
        "proven_properties": list(semantics.proves),
        "unproven_properties": list(semantics.does_not_prove),
        "state_hash": mutation_state_hash,
        "observed_after_mutation": True,
        "source": "patch_review",
    }


def _receipt_integrity_evidence(
    workspace: Path,
    receipt_id: str,
    contract: TaskContract | None,
    mutation_state_hash: str,
    sequence: int,
) -> dict[str, Any]:
    passed = False
    summary = "Mutation receipt is missing."
    try:
        receipt = ReceiptStore(workspace).get(receipt_id) if receipt_id else {}
        relative = str(receipt.get("relative_file_path", ""))
        target = (workspace / relative).resolve()
        current = hashlib.sha256(target.read_bytes()).hexdigest() if target.is_file() else None
        expected = receipt.get("after_sha256")
        passed = bool(receipt.get("success") is True and expected and current == expected)
        summary = (
            f"Receipt {receipt_id} matches {relative}."
            if passed
            else f"Receipt {receipt_id or '<missing>'} does not match final file state."
        )
    except (ReceiptError, OSError, ValueError):
        passed = False
    semantics = EVIDENCE_TAXONOMY[EvidenceType.RECEIPT_INTEGRITY]
    return {
        "evidence_id": f"verification-{sequence:03d}",
        "check": "receipt-integrity",
        "status": "passed" if passed else "failed",
        "duration_ms": 0,
        "output_summary": summary,
        "failure_category": "" if passed else "receipt_mismatch",
        "confidence": 1.0,
        "blocking": not passed,
        "evidence_type": EvidenceType.RECEIPT_INTEGRITY.value,
        "requirement_ids": list(requirement_ids_for_evidence(contract, EvidenceType.RECEIPT_INTEGRITY)),
        "proven_properties": list(semantics.proves),
        "unproven_properties": list(semantics.does_not_prove),
        "state_hash": mutation_state_hash,
        "observed_after_mutation": True,
        "source": "receipt_store",
    }
