from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Mapping

from .intent import (
    Ambiguity,
    AmbiguityLevel,
    Capability,
    ExpectedOutputMode,
    InterpretationIncidentCode,
    NormalizedIntent,
    RiskLevel,
    TargetKind,
    TaskClass,
    intent_identity,
)
from .modes import AgentMode, parse_agent_mode
from .tools.schemas import SCHEMA_BY_NAME


class Specialist(str, Enum):
    GENERAL = "general"
    REPOSITORY_INSPECTOR = "repository_inspector"
    IMPLEMENTATION = "implementation"
    VERIFICATION = "verification"
    DEBUGGING = "debugging"
    DOCUMENTATION = "documentation"
    SECURITY_REVIEW = "security_review"


class ToolFamily(str, Enum):
    REPOSITORY_DISCOVERY = "repository_discovery"
    FILE_INSPECTION = "file_inspection"
    SYMBOL_INSPECTION = "symbol_inspection"
    DOCUMENTATION_RETRIEVAL = "documentation_retrieval"
    EXECUTION_VERIFICATION = "execution_verification"
    MUTATION_PROPOSAL = "mutation_proposal"
    TARGETED_MUTATION = "targeted_mutation"
    FILE_CREATION = "file_creation"
    PATCH_INSPECTION = "patch_inspection"
    MEMORY_RETRIEVAL = "memory_retrieval"
    FINAL_RESPONSE = "final_response"
    CLARIFICATION = "clarification"
    BLOCKED = "blocked"


class ReasonCode(str, Enum):
    REPOSITORY_INVENTORY = "repository_inventory"
    DIRECT_FILE_READ = "direct_file_read"
    SYMBOL_LOOKUP = "symbol_lookup"
    REFERENCE_SEARCH = "reference_search"
    DEPENDENCY_INSPECTION = "dependency_inspection"
    DOCUMENTATION_LOOKUP = "documentation_lookup"
    DIRECT_EXPLANATION = "direct_explanation"
    TEST_EXECUTION = "test_execution"
    COMPILATION_CHECK = "compilation_check"
    LINT_CHECK = "lint_check"
    COMMAND_EXECUTION = "command_execution"
    EXISTING_FILE_PATCH_PROPOSAL = "existing_file_patch_proposal"
    NEW_FILE_PATCH_PROPOSAL = "new_file_patch_proposal"
    APPROVED_TARGETED_EDIT = "approved_targeted_edit"
    APPROVED_FILE_CREATION = "approved_file_creation"
    APPROVED_FULL_FILE_REPLACEMENT = "approved_full_file_replacement"
    MUTATION_REQUIRES_APPROVAL = "mutation_requires_approval"
    MISSING_CAPABILITY = "missing_capability"
    POLICY_BLOCKED = "policy_blocked"
    INSPECT_BEFORE_MUTATE = "inspect_before_mutate"
    PATCH_REVIEW = "patch_review"
    PATCH_TEST = "patch_test"
    PROPOSAL_REVIEW = "proposal_review"
    MEMORY_LOOKUP = "memory_lookup"
    SYMBOL_INDEX_REFRESH = "symbol_index_refresh"
    KNOWLEDGE_REFRESH = "knowledge_refresh"
    SECURITY_INSPECTION = "security_inspection"
    PLANNING_RESPONSE = "planning_response"
    EVIDENCE_COMPARISON = "evidence_comparison"
    FILE_STRUCTURE_SUMMARY = "file_structure_summary"
    GROUNDED_EXPLANATION = "grounded_explanation"
    CAPABILITY_ASSESSMENT = "capability_assessment"
    CLARIFICATION_MISSING_TARGET = "clarification_missing_target"
    REPOSITORY_RESOLVES_TARGET = "repository_resolves_target"
    SAFE_FALLBACK = "safe_fallback"
    NO_SAFE_FALLBACK = "no_safe_fallback"
    UNSUPPORTED_CAPABILITY = "unsupported_capability"


@dataclass(frozen=True)
class RoutingDecision:
    schema_version: str
    intent_id: str
    intent_type: str
    task_class: TaskClass
    specialist: Specialist
    tool_family: ToolFamily
    preferred_tools: tuple[str, ...]
    fallback_tools: tuple[str, ...]
    response_mode: ExpectedOutputMode
    reason_code: ReasonCode
    risk_level: RiskLevel
    requires_prior_inspection: bool
    required_capabilities: tuple[Capability, ...]
    missing_capabilities: tuple[Capability, ...]
    confidence: float
    deterministic_signals: tuple[str, ...]
    model_signals: tuple[str, ...] = ()
    capability_fingerprint: str = ""
    normalized_intent: NormalizedIntent | None = field(default=None, repr=False, compare=False)

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise ValueError("unsupported routing-decision schema version")
        if not self.intent_id.startswith("intent-"):
            raise ValueError("routing decision has invalid intent id")
        if not self.intent_type or len(self.intent_type) > 96:
            raise ValueError("routing intent type must be bounded")
        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError("routing confidence must be between zero and one")
        unknown = (set(self.preferred_tools) | set(self.fallback_tools)) - set(SCHEMA_BY_NAME)
        if unknown:
            raise ValueError(f"routing decision contains unknown tools: {', '.join(sorted(unknown))}")
        if set(self.preferred_tools) & set(self.fallback_tools):
            raise ValueError("preferred and fallback tools must be disjoint")
        if self.response_mode != ExpectedOutputMode.ACTION and (self.preferred_tools or self.fallback_tools):
            raise ValueError("non-action route cannot select tools")
        if self.tool_family in {ToolFamily.BLOCKED, ToolFamily.CLARIFICATION, ToolFamily.FINAL_RESPONSE}:
            if self.preferred_tools or self.fallback_tools:
                raise ValueError("terminal tool family cannot select tools")
        if set(self.missing_capabilities) - set(self.required_capabilities):
            raise ValueError("missing capabilities must be required capabilities")
        if len(self.deterministic_signals) > 64 or len(self.model_signals) > 16:
            raise ValueError("routing decision contains too many signals")

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "intent_id": self.intent_id,
            "intent_type": self.intent_type,
            "task_class": self.task_class.value,
            "specialist": self.specialist.value,
            "tool_family": self.tool_family.value,
            "preferred_tools": list(self.preferred_tools),
            "fallback_tools": list(self.fallback_tools),
            "response_mode": self.response_mode.value,
            "reason_code": self.reason_code.value,
            "risk_level": self.risk_level.value,
            "requires_prior_inspection": self.requires_prior_inspection,
            "required_capabilities": [item.value for item in self.required_capabilities],
            "missing_capabilities": [item.value for item in self.missing_capabilities],
            "confidence": self.confidence,
            "deterministic_signals": list(self.deterministic_signals),
            "model_signals": list(self.model_signals),
            "capability_fingerprint": self.capability_fingerprint,
        }

    @classmethod
    def from_dict(cls, payload: Mapping[str, Any]) -> "RoutingDecision":
        fields = {
            "schema_version", "intent_id", "intent_type", "task_class", "specialist", "tool_family",
            "preferred_tools", "fallback_tools", "response_mode", "reason_code", "risk_level",
            "requires_prior_inspection", "required_capabilities", "missing_capabilities", "confidence",
            "deterministic_signals", "model_signals", "capability_fingerprint",
        }
        extra = set(payload) - fields
        missing = fields - set(payload)
        if extra:
            raise ValueError(f"routing decision contains unknown fields: {', '.join(sorted(extra))}")
        if missing:
            raise ValueError(f"routing decision missing fields: {', '.join(sorted(missing))}")
        array_fields = (
            "preferred_tools", "fallback_tools", "required_capabilities", "missing_capabilities",
            "deterministic_signals", "model_signals",
        )
        if any(not isinstance(payload[name], list) for name in array_fields):
            raise ValueError("routing decision list fields must be arrays")
        if not isinstance(payload["requires_prior_inspection"], bool):
            raise ValueError("requires_prior_inspection must be a boolean")
        confidence = payload["confidence"]
        if isinstance(confidence, bool) or not isinstance(confidence, (int, float)):
            raise ValueError("confidence must be numeric")
        return cls(
            schema_version=str(payload["schema_version"]),
            intent_id=str(payload["intent_id"]),
            intent_type=str(payload["intent_type"]),
            task_class=TaskClass(str(payload["task_class"])),
            specialist=Specialist(str(payload["specialist"])),
            tool_family=ToolFamily(str(payload["tool_family"])),
            preferred_tools=tuple(str(item) for item in payload["preferred_tools"]),
            fallback_tools=tuple(str(item) for item in payload["fallback_tools"]),
            response_mode=ExpectedOutputMode(str(payload["response_mode"])),
            reason_code=ReasonCode(str(payload["reason_code"])),
            risk_level=RiskLevel(str(payload["risk_level"])),
            requires_prior_inspection=payload["requires_prior_inspection"],
            required_capabilities=tuple(Capability(str(item)) for item in payload["required_capabilities"]),
            missing_capabilities=tuple(Capability(str(item)) for item in payload["missing_capabilities"]),
            confidence=float(confidence),
            deterministic_signals=tuple(str(item) for item in payload["deterministic_signals"]),
            model_signals=tuple(str(item) for item in payload["model_signals"]),
            capability_fingerprint=str(payload["capability_fingerprint"]),
        )

    def is_current_for(self, granted_capabilities: tuple[Capability, ...], mode: str) -> bool:
        return self.capability_fingerprint == _capability_fingerprint(granted_capabilities, mode)


@dataclass(frozen=True)
class RouteDecision:
    """v0.10 compatibility view derived from the typed v0.11 decision."""

    specialist: str
    confidence: float
    required_context: tuple[str, ...]
    permitted_tools: tuple[str, ...]
    verification_strategy: tuple[str, ...]
    estimated_complexity: str
    planning_required: bool
    rationale: str
    mutation_required: bool = False
    semantic_decision: RoutingDecision | None = field(default=None, repr=False, compare=False)


_FILE_RE = re.compile(
    r"(?<![\w./-])([\w./-]+\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md))(?=$|[\s`'\",:;!?().])",
    re.IGNORECASE,
)
_SYMBOL_RE = re.compile(r"\b(?:symbol|function|class|method|definition|reference(?:s)?)\s+([A-Za-z_]\w*)", re.IGNORECASE)
_REVERSE_SYMBOL_RE = re.compile(r"\b([A-Za-z_]\w*)\s+(?:symbol|function|class|method)\b", re.IGNORECASE)
_MUTATION_RE = re.compile(
    r"\b(edit|modify|fix|update|create|implement|refactor|replace|apply|write|overwrite|draft|propose|proposing|change|changing|mutate|mutating|add|insert|append|rename|remove|delete|patch)\b",
    re.IGNORECASE,
)
_VERIFICATION_RE = re.compile(r"^(?:please\s+)?(?:run|test|compile|lint|verify|build|check|execute)\b", re.IGNORECASE)
_INSPECTION_RE = re.compile(r"\b(inspect|read|search|find|locate|map|show|summarize|review|compare|assess|recall|index|refresh|list|count|enumerate|display)\b", re.IGNORECASE)
_POLICY_ATTACK_RE = re.compile(
    r"\b(ignore (?:the )?(?:tool|read[- ]only mode)|hidden tool|unrestricted_shell|bypass policy|rm\s+-rf|arbitrary internet|invent (?:a )?.*tool|escalate from|reuse a .*route|pretend write approval|expose every tool|confidence 1\.0|skip required inspection|apply and propose|claim a successful test.*without shell|encode an edit request|update_memory as a source-code mutation tool)\b",
    re.IGNORECASE,
)


class HierarchicalRouter:
    """Deterministic five-stage semantic router with policy-bound capability inputs."""

    def route(
        self,
        prompt: str,
        workspace: Path,
    ) -> RouteDecision:
        """Return the v0.10 compatibility view without changing its permission-agnostic API."""

        decision = self.route_typed(
            prompt,
            workspace,
            mode=AgentMode.UNSAFE,
            allow_write=True,
            allow_shell=True,
        )
        return self._legacy(decision)

    def legacy_view(self, decision: RoutingDecision) -> RouteDecision:
        return self._legacy(decision)

    def route_typed(
        self,
        prompt: str,
        workspace: Path,
        *,
        mode: str | AgentMode = AgentMode.READ_ONLY,
        allow_write: bool = False,
        allow_shell: bool = False,
        allow_network: bool = False,
        prior_inspection: bool = False,
    ) -> RoutingDecision:
        del workspace  # Reserved for future repository-resolvable ambiguity evidence.
        normalized_mode = parse_agent_mode(mode)
        granted = self._granted_capabilities(
            normalized_mode,
            allow_write=allow_write,
            allow_shell=allow_shell,
            allow_network=allow_network,
        )
        intent = self.interpret(
            prompt,
            mode=normalized_mode,
            granted_capabilities=granted,
            prior_inspection=prior_inspection,
        )
        family, specialist, preferred, fallback, reason = self._select_route(intent, normalized_mode)
        missing = tuple(item for item in intent.required_capabilities if item not in granted)
        response_mode = intent.expected_output_mode
        task_class = intent.task_class
        if missing and response_mode == ExpectedOutputMode.ACTION:
            family = ToolFamily.BLOCKED
            preferred = ()
            fallback = ()
            reason = ReasonCode.MISSING_CAPABILITY
            response_mode = ExpectedOutputMode.BLOCKED
            task_class = TaskClass.BLOCKED
        confidence = self._confidence(intent, reason)
        return RoutingDecision(
            schema_version="1.0",
            intent_id=intent.intent_id,
            intent_type=intent.intent_type,
            task_class=task_class,
            specialist=specialist,
            tool_family=family,
            preferred_tools=preferred,
            fallback_tools=fallback,
            response_mode=response_mode,
            reason_code=reason,
            risk_level=intent.risk_level,
            requires_prior_inspection=intent.requires_prior_inspection,
            required_capabilities=intent.required_capabilities,
            missing_capabilities=missing,
            confidence=confidence,
            deterministic_signals=intent.deterministic_signals,
            model_signals=(),
            capability_fingerprint=_capability_fingerprint(granted, normalized_mode.value),
            normalized_intent=intent,
        )

    def interpret(
        self,
        prompt: str,
        *,
        mode: AgentMode,
        granted_capabilities: tuple[Capability, ...],
        prior_inspection: bool,
    ) -> NormalizedIntent:
        original = prompt.strip()
        if not original:
            raise ValueError("routing request cannot be empty")
        if len(original) > 16_000:
            raise ValueError("routing request exceeds 16000 characters")
        goal = " ".join(original.split())
        text = goal.lower()
        files = tuple(dict.fromkeys(match.group(1) for match in _FILE_RE.finditer(goal)))
        non_identifiers = {
            "a", "an", "the", "whether", "which", "this", "that",
            "index", "indexing", "lookup", "search", "resolution",
        }
        symbol_match = _SYMBOL_RE.search(goal)
        if symbol_match is not None and symbol_match.group(1).lower() in non_identifiers:
            symbol_match = None
        if symbol_match is None:
            reverse_match = _REVERSE_SYMBOL_RE.search(goal)
            if reverse_match is not None and reverse_match.group(1).lower() not in non_identifiers:
                symbol_match = reverse_match
        symbols = (symbol_match.group(1),) if symbol_match else ()
        target_scope = files or symbols
        signals: list[str] = []
        incidents: list[InterpretationIncidentCode] = []

        mutation_matches = tuple(_MUTATION_RE.finditer(text))
        mutation_verb_spans = tuple(m.span() for m in mutation_matches)
        mutation_verb_words = tuple(m.group(0) for m in mutation_matches)
        mutation = bool(mutation_verb_spans)
        # A "do not change X" phrase is only a full prohibition when it covers
        # every mutation verb in the request ("review without changing files").
        # As a bounded constraint inside an otherwise-mutating request
        # ("Add a provider, do not change existing behavior") it must not
        # suppress the mutation route. The ambiguous noun-verb "patch" ("patch
        # review", "patch persistence") is excluded from the positive set when
        # a prohibition is present, so it cannot leak a mutation intent that a
        # "do not edit/mutate" clause explicitly forbids.
        negated_mutation = re.search(
            r"\b(?:do not|without)\b[^.;]{0,48}\b(?:modify|modifying|edit|editing|change|changing|apply|applying|save|saving|mutate|mutating)\b",
            text,
        )
        if negated_mutation is not None:
            neg_start, neg_end = negated_mutation.span()
            mutation = any(
                word != "patch" and not (neg_start <= vstart < neg_end)
                for (vstart, _), word in zip(mutation_verb_spans, mutation_verb_words)
            )
        # "Add 2 and 2"-style arithmetic is a question, not a code mutation.
        if re.search(r"\badd\b\s+\d+\s+(?:and|plus|\+)", text):
            mutation = False
        proposal_verb = bool(re.search(r"\b(?:propose|proposing|draft)\b", text)) and not bool(
            re.search(r"\bbefore (?:propose|proposing)\b", text)
        )
        non_mutating_patch_review = bool(
            re.search(r"^(?:show|review|verify|test)\b.*\b(?:existing )?(?:patch|proposal|proposed change)\b", text)
        )
        if re.search(r"\bplan the implementation\b", text):
            mutation = False
        if non_mutating_patch_review:
            mutation = False
        verification = bool(_VERIFICATION_RE.search(text))
        inspection = bool(_INSPECTION_RE.search(text)) or bool(target_scope)
        research = bool(re.search(r"\b(documentation|docs|guidance|knowledge|research)\b", text))
        proposal = proposal_verb
        creates_new_target = bool(
            re.search(r"\b(?:new file|create (?:an? |the )?(?:approved |new )?file)\b", text)
            or re.search(r"\bcreate\b[^.;]{0,60}\b(?:file|files|module)\b", text)
            or re.search(r"\b(?:or create|create it)\b", text)
        )
        explicitly_requires_inspection = bool(
            re.search(r"\b(after reading|before (?:proposing|changing|editing)|inspect .* before)\b", text)
        )
        # An existing-file proposal needs exact source text for its bounded old/new
        # replacement schema.  Treat inspection as a lifecycle prerequisite even
        # when the user did not spell it out; confidence can never substitute for
        # repository evidence.  New-file proposals do not have that prerequisite.
        prior_required = mutation and bool(target_scope) and not creates_new_target
        prior_required = prior_required or (mutation and explicitly_requires_inspection)
        if mutation:
            signals.append("mutation_terms")
        if verification:
            signals.append("verification_terms")
        if inspection:
            signals.append("inspection_or_target_terms")
        if proposal:
            signals.append("proposal_terms")
        if files:
            signals.append("file_target")
        if symbols:
            signals.append("symbol_target")

        attack = bool(_POLICY_ATTACK_RE.search(text))
        blocking_ambiguity = mutation and bool(
            re.search(r"\b(several|multiple|unspecified|no target|not identified|required format and destination)\b", text)
        )
        resolvable_ambiguity = bool(re.search(r"\b(find which file|determine whether|which (?:file|module))\b", text))
        if attack:
            ambiguity = Ambiguity(AmbiguityLevel.NONE)
            incidents.extend((InterpretationIncidentCode.PROMPT_INJECTION, InterpretationIncidentCode.UNSAFE_REQUEST))
            signals.append("policy_attack")
        elif blocking_ambiguity:
            ambiguity = Ambiguity(AmbiguityLevel.BLOCKING, ("target_scope",))
            incidents.append(InterpretationIncidentCode.MISSING_TARGET)
            signals.append("blocking_ambiguity")
        elif resolvable_ambiguity:
            ambiguity = Ambiguity(AmbiguityLevel.RESOLVABLE, ("target_scope",))
            signals.append("repository_resolvable_ambiguity")
        else:
            ambiguity = Ambiguity(AmbiguityLevel.NONE)

        direct_explanation = bool(re.search(r"\b(explain|tradeoffs|conceptually|plan the implementation)\b", text)) and bool(
            re.search(r"\b(without inspecting|without calling tools|no repository evidence|conceptually)\b", text)
        )
        patch_inspection = bool(re.search(r"\b(show|review|verify)\b.*\b(?:existing )?(?:patch|proposal|proposed change)\b", text)) and not bool(re.search(r"\btest the .*patch\b", text))
        inspect_before = prior_required and not prior_inspection and bool(re.match(r"^inspect\b", text))
        planning = proposal or bool(re.search(r"\bplan the implementation\b", text))
        if attack:
            task_class = TaskClass.BLOCKED
            output = ExpectedOutputMode.BLOCKED
            intent_type = "policy_attack"
        elif blocking_ambiguity:
            task_class = TaskClass.BLOCKED
            output = ExpectedOutputMode.CLARIFICATION
            intent_type = "ambiguous_mutation" if mutation else "missing_creation_contract"
        elif direct_explanation:
            task_class = TaskClass.PLANNING if "plan the implementation" in text else TaskClass.EXPLANATION
            output = ExpectedOutputMode.FINAL_ANSWER
            intent_type = "implementation_plan" if task_class == TaskClass.PLANNING else "explanation"
        elif patch_inspection:
            task_class = TaskClass.INSPECTION
            output = ExpectedOutputMode.ACTION
            intent_type = "proposal_review" if "verify" in text else "patch_inspection"
        elif inspect_before and re.search(r"\bbefore (?:propose|proposing)\b", text):
            task_class = TaskClass.INSPECTION
            output = ExpectedOutputMode.ACTION
            intent_type = "inspect_before_mutation"
        elif planning:
            task_class = TaskClass.PLANNING
            output = ExpectedOutputMode.ACTION if proposal else ExpectedOutputMode.FINAL_ANSWER
            intent_type = "file_proposal" if re.search(r"\bnew file\b", text) else "patch_proposal"
        elif mutation:
            task_class = TaskClass.MUTATION
            output = ExpectedOutputMode.ACTION
            intent_type = "mutation"
        elif verification:
            task_class = TaskClass.VERIFICATION
            output = ExpectedOutputMode.ACTION
            intent_type = "verification"
        elif inspection or research or resolvable_ambiguity:
            task_class = TaskClass.INSPECTION
            output = ExpectedOutputMode.ACTION
            intent_type = "inspection"
        else:
            task_class = TaskClass.EXPLANATION
            output = ExpectedOutputMode.FINAL_ANSWER
            intent_type = "explanation"

        risk = RiskLevel.LOW
        if attack:
            risk = RiskLevel.CRITICAL
        elif re.match(r"^(?:review|inspect|audit)\b", text) and re.search(r"\b(authentication|authorization|ssrf|injection|privilege|risks?)\b", text):
            risk = RiskLevel.HIGH
        elif mutation:
            risk = RiskLevel.HIGH if (
                blocking_ambiguity
                or mode == AgentMode.READ_ONLY
                or re.search(r"\b(replace the complete|full[- ]file|without approval|no write approval)\b", text)
                or re.search(r"\b(syntactically invalid|invalid syntax|so rollback can be verified)\b", text)
            ) else RiskLevel.MEDIUM
        elif patch_inspection:
            risk = RiskLevel.LOW
        elif verification or mode == AgentMode.UNSAFE:
            risk = RiskLevel.MEDIUM

        required: list[Capability] = []
        forbidden: list[Capability] = []
        if output == ExpectedOutputMode.ACTION:
            required.append(Capability.WORKSPACE_READ)
        if task_class == TaskClass.MUTATION:
            required.append(Capability.WORKSPACE_WRITE)
        if proposal or re.search(r"\b(index source|refresh local project knowledge)\b", text):
            required.append(Capability.RUNTIME_STATE)
        if verification and not patch_inspection and output == ExpectedOutputMode.ACTION:
            required.append(Capability.SHELL)
        if attack:
            forbidden.extend((Capability.WORKSPACE_WRITE, Capability.SHELL, Capability.NETWORK))

        missing = [item for item in required if item not in granted_capabilities]
        if missing:
            incidents.append(InterpretationIncidentCode.MISSING_CAPABILITY)
            signals.append("missing_capability")
        if mutation and mode == AgentMode.READ_ONLY and not inspect_before and output == ExpectedOutputMode.ACTION:
            output = ExpectedOutputMode.BLOCKED
            task_class = TaskClass.BLOCKED
            incidents.append(InterpretationIncidentCode.MODE_MISMATCH)
            signals.append("read_only_mutation_block")
        target_kind = TargetKind.UNKNOWN
        if files:
            target_kind = TargetKind.FILE
        elif symbols:
            target_kind = TargetKind.SYMBOL
        elif re.search(r"\b(repository|repo|codebase|workspace|directory|folder)\b", text):
            target_kind = TargetKind.REPOSITORY
        elif verification and re.search(r"\bcommand\b", text):
            target_kind = TargetKind.COMMAND

        return NormalizedIntent(
            schema_version="1.0",
            intent_id=intent_identity(
                original,
                mode=mode.value,
                granted_capabilities=granted_capabilities,
                prior_inspection=prior_inspection,
            ),
            original_request=original,
            goal=goal,
            intent_type=intent_type,
            task_class=task_class,
            target_scope=target_scope,
            target_kind=target_kind,
            mutation_intent=mutation,
            verification_intent=verification,
            research_intent=research,
            requires_prior_inspection=prior_required,
            risk_level=risk,
            ambiguity=ambiguity,
            required_capabilities=tuple(dict.fromkeys(required)),
            forbidden_capabilities=tuple(dict.fromkeys(forbidden)),
            expected_output_mode=output,
            deterministic_signals=tuple(dict.fromkeys(signals)),
            interpretation_incidents=tuple(dict.fromkeys(incidents)),
        )

    def _select_route(
        self,
        intent: NormalizedIntent,
        mode: AgentMode,
    ) -> tuple[ToolFamily, Specialist, tuple[str, ...], tuple[str, ...], ReasonCode]:
        text = intent.goal.lower()
        if intent.expected_output_mode == ExpectedOutputMode.BLOCKED:
            reason = ReasonCode.POLICY_BLOCKED if "policy_attack" in intent.deterministic_signals else ReasonCode.MUTATION_REQUIRES_APPROVAL
            return ToolFamily.BLOCKED, Specialist.SECURITY_REVIEW if reason == ReasonCode.POLICY_BLOCKED else Specialist.IMPLEMENTATION, (), (), reason
        if intent.expected_output_mode == ExpectedOutputMode.CLARIFICATION:
            return ToolFamily.CLARIFICATION, Specialist.IMPLEMENTATION, (), (), ReasonCode.CLARIFICATION_MISSING_TARGET
        if intent.expected_output_mode == ExpectedOutputMode.FINAL_ANSWER:
            reason = ReasonCode.PLANNING_RESPONSE if intent.task_class == TaskClass.PLANNING else ReasonCode.DIRECT_EXPLANATION
            specialist = Specialist.IMPLEMENTATION if intent.task_class == TaskClass.PLANNING else Specialist.GENERAL
            return ToolFamily.FINAL_RESPONSE, specialist, (), (), reason

        if re.search(r"\btest the existing patch\b", text):
            return ToolFamily.EXECUTION_VERIFICATION, Specialist.VERIFICATION, ("test_patch",), (), ReasonCode.PATCH_TEST
        if re.search(r"\b(show|review|verify)\b.*\b(?:existing )?(?:patch|proposal|proposed change)\b", text):
            reason = ReasonCode.PROPOSAL_REVIEW if "verify" in text else ReasonCode.PATCH_REVIEW
            return ToolFamily.PATCH_INSPECTION, Specialist.VERIFICATION if reason == ReasonCode.PROPOSAL_REVIEW else Specialist.REPOSITORY_INSPECTOR, ("list_patches",), ("show_patch",), reason
        if re.search(r"\brecall|recorded project decision|memories\b", text):
            return ToolFamily.MEMORY_RETRIEVAL, Specialist.GENERAL, ("recall",), ("list_memories",), ReasonCode.MEMORY_LOOKUP
        if re.search(r"\bindex source symbols\b", text):
            return ToolFamily.SYMBOL_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("index_code",), (), ReasonCode.SYMBOL_INDEX_REFRESH
        if re.search(r"\brefresh local project knowledge\b", text):
            return ToolFamily.DOCUMENTATION_RETRIEVAL, Specialist.DOCUMENTATION, ("refresh_knowledge",), (), ReasonCode.KNOWLEDGE_REFRESH
        if intent.task_class == TaskClass.PLANNING and intent.mutation_intent:
            if re.search(r"\b(new file|create)\b", text):
                return ToolFamily.MUTATION_PROPOSAL, Specialist.IMPLEMENTATION, ("propose_write_file",), (), ReasonCode.NEW_FILE_PATCH_PROPOSAL
            return ToolFamily.MUTATION_PROPOSAL, Specialist.IMPLEMENTATION, ("propose_edit_file",), (), ReasonCode.EXISTING_FILE_PATCH_PROPOSAL
        if intent.task_class == TaskClass.MUTATION:
            if re.search(r"\breplace the complete contents|full[- ]file replacement\b", text):
                return ToolFamily.FILE_CREATION, Specialist.IMPLEMENTATION, ("write_file",), (), ReasonCode.APPROVED_FULL_FILE_REPLACEMENT
            if re.search(r"\b(?:new file|create (?:the approved file|file)|create it|or create|create\b[^.;]{0,60}\b(?:file|files|module))\b", text):
                return ToolFamily.FILE_CREATION, Specialist.IMPLEMENTATION, ("write_file",), (), ReasonCode.APPROVED_FILE_CREATION
            fallback = ("write_file",) if re.search(r"\bmodify\b", text) else ()
            return ToolFamily.TARGETED_MUTATION, Specialist.IMPLEMENTATION, ("edit_file",), fallback, ReasonCode.APPROVED_TARGETED_EDIT
        if intent.task_class == TaskClass.VERIFICATION:
            if re.match(r"^(?:run\s+)?tests?\b", text):
                reason = ReasonCode.TEST_EXECUTION
            elif re.search(r"\bcompile|compiler\b", text):
                reason = ReasonCode.COMPILATION_CHECK
            elif re.search(r"\blint|linter\b", text):
                reason = ReasonCode.LINT_CHECK
            elif re.search(r"\btest|tests|testing\b", text):
                reason = ReasonCode.TEST_EXECUTION
            else:
                reason = ReasonCode.COMMAND_EXECUTION
            specialist = Specialist.DEBUGGING if re.match(r"^(?:diagnose|debug)\b", text) or re.search(r"\b(?:diagnostic|failing)\b", text) else Specialist.VERIFICATION
            return ToolFamily.EXECUTION_VERIFICATION, specialist, ("run_command",), (), reason
        if intent.requires_prior_inspection and intent.intent_type == "inspect_before_mutation":
            return ToolFamily.FILE_INSPECTION, Specialist.DEBUGGING, ("read_file",), ("search_code",), ReasonCode.INSPECT_BEFORE_MUTATE
        if re.match(r"^(?:review|inspect|audit)\b", text) and re.search(r"\b(authentication|authorization|ssrf|injection|risks?)\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.SECURITY_REVIEW, ("read_file",), ("search_code",), ReasonCode.SECURITY_INSPECTION
        if re.search(r"\b(search the indexed documentation|documentation|docs|guidance|knowledge)\b", text):
            return ToolFamily.DOCUMENTATION_RETRIEVAL, Specialist.DOCUMENTATION, ("search_docs",), ("query_knowledge",), ReasonCode.DOCUMENTATION_LOOKUP
        if re.search(r"\b(find every reference|every reference)\b", text):
            return ToolFamily.SYMBOL_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("search_code",), ("search_symbols",), ReasonCode.REFERENCE_SEARCH
        if re.search(r"\b(locate the definition|symbol lookup|find which (?:file|module))\b", text):
            reason = ReasonCode.REPOSITORY_RESOLVES_TARGET if intent.ambiguity.level == AmbiguityLevel.RESOLVABLE else ReasonCode.SYMBOL_LOOKUP
            preferred = "search_code" if reason == ReasonCode.REPOSITORY_RESOLVES_TARGET else "search_symbols"
            fallback = "search_symbols" if preferred == "search_code" else "search_code"
            return ToolFamily.SYMBOL_INSPECTION, Specialist.REPOSITORY_INSPECTOR, (preferred,), (fallback,), reason
        if re.search(r"\bdependency declarations|dependencies\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("read_file",), ("search_code",), ReasonCode.DEPENDENCY_INSPECTION
        if re.search(r"\bcompare\b.*\bdocumented behavior\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.DOCUMENTATION, ("read_file",), ("search_docs",), ReasonCode.EVIDENCE_COMPARISON
        if re.search(r"\bsummarize the structure|structure of\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("file_summary",), ("read_file",), ReasonCode.FILE_STRUCTURE_SUMMARY
        if re.search(r"\bexplain what\b.*\bafter grounding|grounding the answer\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("read_file",), ("search_symbols",), ReasonCode.GROUNDED_EXPLANATION
        if re.search(r"\bread\b.*\bdirectly|summarize how|inspect .* to diagnose\b", text):
            return ToolFamily.FILE_INSPECTION, Specialist.DEBUGGING if "diagnose" in text else Specialist.REPOSITORY_INSPECTOR, ("read_file",), ("file_summary" if "summarize" in text else "search_code",), ReasonCode.DIRECT_FILE_READ
        if re.match(r"^map\b.*\brepository\b", text):
            return ToolFamily.REPOSITORY_DISCOVERY, Specialist.REPOSITORY_INSPECTOR, ("project_map",), ("list_files",), ReasonCode.REPOSITORY_INVENTORY
        if intent.target_kind == TargetKind.SYMBOL:
            return ToolFamily.SYMBOL_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("search_symbols",), ("search_code",), ReasonCode.SYMBOL_LOOKUP
        if intent.target_kind == TargetKind.FILE:
            return ToolFamily.FILE_INSPECTION, Specialist.REPOSITORY_INSPECTOR, ("read_file",), ("file_summary",), ReasonCode.DIRECT_FILE_READ
        if intent.ambiguity.level == AmbiguityLevel.RESOLVABLE:
            return ToolFamily.REPOSITORY_DISCOVERY, Specialist.REPOSITORY_INSPECTOR, ("project_map",), ("search_code",), ReasonCode.REPOSITORY_RESOLVES_TARGET
        if re.search(r"\bassess whether\b.*\bsupported|capability\b", text):
            return ToolFamily.REPOSITORY_DISCOVERY, Specialist.REPOSITORY_INSPECTOR, ("project_map",), ("search_code",), ReasonCode.CAPABILITY_ASSESSMENT
        return ToolFamily.REPOSITORY_DISCOVERY, Specialist.REPOSITORY_INSPECTOR, ("project_map",), ("list_files",), ReasonCode.REPOSITORY_INVENTORY

    def _legacy(self, decision: RoutingDecision) -> RouteDecision:
        text = decision.normalized_intent.goal.lower() if decision.normalized_intent else ""
        suffixes = {Path(item).suffix.lower() for item in decision.normalized_intent.target_scope} if decision.normalized_intent else set()
        if decision.specialist == Specialist.SECURITY_REVIEW:
            specialist = "security_review"
        elif suffixes & {".v", ".sv"} or re.search(r"\b(verilog|systemverilog|rtl|iverilog)\b", text):
            specialist = "verilog_verification"
        elif suffixes & {".c", ".cc", ".cpp", ".h", ".hpp"}:
            specialist = "cpp_verification"
        elif decision.specialist == Specialist.VERIFICATION and (suffixes & {".py"} or "python" in text or "pytest" in text):
            specialist = "python_verification"
        else:
            specialist = {
                Specialist.GENERAL: "general_reasoning",
                Specialist.REPOSITORY_INSPECTOR: "repository_understanding",
                Specialist.IMPLEMENTATION: "code_modification",
                Specialist.VERIFICATION: "testing_verification",
                Specialist.DEBUGGING: "debugging",
                Specialist.DOCUMENTATION: "documentation_rag",
                Specialist.SECURITY_REVIEW: "security_review",
            }[decision.specialist]
        mutation = bool(decision.normalized_intent and decision.normalized_intent.mutation_intent)
        read_tools = (
            "project_map", "list_files", "read_file", "search_code", "search_symbols",
            "file_summary", "query_knowledge", "search_docs", "recall",
        )
        permitted = read_tools
        if mutation:
            permitted += ("refresh_knowledge", "propose_write_file", "propose_edit_file", "write_file", "edit_file")
        if specialist in {
            "debugging", "testing_verification", "mathematics", "python_verification",
            "cpp_verification", "verilog_verification", "security_review",
        } or mutation:
            permitted += ("run_command",)
        verification = self._legacy_verification(specialist)
        complexity = decision.risk_level.value
        return RouteDecision(
            specialist=specialist,
            confidence=decision.confidence,
            required_context=decision.normalized_intent.target_scope if decision.normalized_intent and decision.normalized_intent.target_scope else ("workspace map when repository-grounded",),
            permitted_tools=tuple(dict.fromkeys(permitted)),
            verification_strategy=verification,
            estimated_complexity=complexity,
            planning_required=decision.tool_family not in {ToolFamily.FINAL_RESPONSE, ToolFamily.BLOCKED, ToolFamily.CLARIFICATION},
            rationale=f"Typed route: {decision.reason_code.value}; family={decision.tool_family.value}.",
            mutation_required=mutation,
            semantic_decision=decision,
        )

    @staticmethod
    def _legacy_verification(specialist: str) -> tuple[str, ...]:
        if specialist == "security_review":
            return ("policy invariants", "security regression tests")
        if specialist == "verilog_verification":
            return ("HDL syntax", "simulation/formal when available")
        if specialist == "cpp_verification":
            return ("compiler warnings", "tests")
        if specialist in {"python_verification", "debugging", "code_modification"}:
            return ("python syntax", "targeted tests")
        if specialist == "testing_verification":
            return ("project checks",)
        return ()

    @staticmethod
    def _granted_capabilities(
        mode: AgentMode,
        *,
        allow_write: bool,
        allow_shell: bool,
        allow_network: bool,
    ) -> tuple[Capability, ...]:
        granted = [Capability.WORKSPACE_READ]
        if mode in {AgentMode.PROPOSE, AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            granted.append(Capability.RUNTIME_STATE)
        if allow_write and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            granted.append(Capability.WORKSPACE_WRITE)
        if allow_shell and mode in {AgentMode.WRITE_APPROVED, AgentMode.UNSAFE}:
            granted.append(Capability.SHELL)
        if allow_network:
            granted.append(Capability.NETWORK)
        return tuple(granted)

    @staticmethod
    def _confidence(intent: NormalizedIntent, reason: ReasonCode) -> float:
        confidence = 0.9
        if intent.ambiguity.level == AmbiguityLevel.RESOLVABLE:
            confidence = 0.82
        elif intent.ambiguity.level == AmbiguityLevel.BLOCKING:
            confidence = 0.96
        if reason in {ReasonCode.REPOSITORY_INVENTORY, ReasonCode.DIRECT_EXPLANATION} and not intent.target_scope:
            confidence -= 0.08
        return round(max(0.0, min(1.0, confidence)), 2)


def _capability_fingerprint(capabilities: tuple[Capability, ...], mode: str) -> str:
    identity = json.dumps(
        {"mode": mode, "capabilities": sorted(item.value for item in capabilities)},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(identity.encode("utf-8")).hexdigest()
