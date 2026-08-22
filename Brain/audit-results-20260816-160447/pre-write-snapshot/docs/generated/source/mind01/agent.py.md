# `mind01/agent.py`

## File purpose

This agent runtime file is reviewed at snapshot `e8f55c329c3a3f888a7d0cc4563775cba6cd1f007a2a56954156079b8678cfde`. It contains 1056 lines.

## Imports and module state

- [mind01/agent.py:1](../../../../mind01/agent.py#L1) imports `__future__` / annotations.
- [mind01/agent.py:3](../../../../mind01/agent.py#L3) imports `json`.
- [mind01/agent.py:4](../../../../mind01/agent.py#L4) imports `difflib`.
- [mind01/agent.py:5](../../../../mind01/agent.py#L5) imports `hashlib`.
- [mind01/agent.py:6](../../../../mind01/agent.py#L6) imports `re`.
- [mind01/agent.py:7](../../../../mind01/agent.py#L7) imports `time`.
- [mind01/agent.py:8](../../../../mind01/agent.py#L8) imports `uuid`.
- [mind01/agent.py:9](../../../../mind01/agent.py#L9) imports `dataclasses` / dataclass.
- [mind01/agent.py:9](../../../../mind01/agent.py#L9) imports `dataclasses` / field.
- [mind01/agent.py:10](../../../../mind01/agent.py#L10) imports `typing` / Any.
- [mind01/agent.py:10](../../../../mind01/agent.py#L10) imports `typing` / Iterable.
- [mind01/agent.py:10](../../../../mind01/agent.py#L10) imports `typing` / List.
- [mind01/agent.py:10](../../../../mind01/agent.py#L10) imports `typing` / Optional.
- [mind01/agent.py:11](../../../../mind01/agent.py#L11) imports `pathlib` / Path.
- [mind01/agent.py:13](../../../../mind01/agent.py#L13) imports `action_parser` / ParsedAction.
- [mind01/agent.py:13](../../../../mind01/agent.py#L13) imports `action_parser` / ParserFailureCode.
- [mind01/agent.py:13](../../../../mind01/agent.py#L13) imports `action_parser` / ResponseMode.
- [mind01/agent.py:13](../../../../mind01/agent.py#L13) imports `action_parser` / canonical_response_schema.
- [mind01/agent.py:13](../../../../mind01/agent.py#L13) imports `action_parser` / parse_action_output.
- [mind01/agent.py:20](../../../../mind01/agent.py#L20) imports `config` / AgentConfig.
- [mind01/agent.py:21](../../../../mind01/agent.py#L21) imports `completion` / CompletionAuthority.
- [mind01/agent.py:22](../../../../mind01/agent.py#L22) imports `llm` / LLMError.
- [mind01/agent.py:22](../../../../mind01/agent.py#L22) imports `llm` / Message.
- [mind01/agent.py:22](../../../../mind01/agent.py#L22) imports `llm` / OllamaClient.
- [mind01/agent.py:23](../../../../mind01/agent.py#L23) imports `memory_intent` / MemoryIntent.
- [mind01/agent.py:23](../../../../mind01/agent.py#L23) imports `memory_intent` / detect_memory_intent.
- [mind01/agent.py:24](../../../../mind01/agent.py#L24) imports `modes` / AgentMode.
- [mind01/agent.py:25](../../../../mind01/agent.py#L25) imports `planning` / Planner.
- [mind01/agent.py:26](../../../../mind01/agent.py#L26) imports `patch_review` / review_patch.
- [mind01/agent.py:27](../../../../mind01/agent.py#L27) imports `prompts` / SYSTEM_PROMPT.
- [mind01/agent.py:27](../../../../mind01/agent.py#L27) imports `prompts` / build_action_instruction.
- [mind01/agent.py:28](../../../../mind01/agent.py#L28) imports `recovery` / RecoveryController.
- [mind01/agent.py:29](../../../../mind01/agent.py#L29) imports `receipts` / ReceiptError.
- [mind01/agent.py:29](../../../../mind01/agent.py#L29) imports `receipts` / ReceiptStore.
- [mind01/agent.py:30](../../../../mind01/agent.py#L30) imports `routing` / HierarchicalRouter.
- [mind01/agent.py:30](../../../../mind01/agent.py#L30) imports `routing` / RouteDecision.
- [mind01/agent.py:30](../../../../mind01/agent.py#L30) imports `routing` / RoutingDecision.
- [mind01/agent.py:30](../../../../mind01/agent.py#L30) imports `routing` / ToolFamily.
- [mind01/agent.py:31](../../../../mind01/agent.py#L31) imports `semantic_router_v2` / OllamaSemanticClassifier.
- [mind01/agent.py:31](../../../../mind01/agent.py#L31) imports `semantic_router_v2` / RuleBasedSemanticClassifier.
- [mind01/agent.py:31](../../../../mind01/agent.py#L31) imports `semantic_router_v2` / SemanticRouterV2.
- [mind01/agent.py:36](../../../../mind01/agent.py#L36) imports `security` / redact_secrets.
- [mind01/agent.py:37](../../../../mind01/agent.py#L37) imports `skills` / SkillRegistry.
- [mind01/agent.py:38](../../../../mind01/agent.py#L38) imports `state` / AgentPhase.
- [mind01/agent.py:38](../../../../mind01/agent.py#L38) imports `state` / AgentState.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / EVIDENCE_TAXONOMY.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / EvidenceType.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / TaskContract.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / build_task_contract.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / requirement_ids_for_evidence.
- [mind01/agent.py:39](../../../../mind01/agent.py#L39) imports `task_contract` / state_hash.
- [mind01/agent.py:47](../../../../mind01/agent.py#L47) imports `tool_exposure` / LifecyclePhase.
- [mind01/agent.py:47](../../../../mind01/agent.py#L47) imports `tool_exposure` / StaleRouteError.
- [mind01/agent.py:47](../../../../mind01/agent.py#L47) imports `tool_exposure` / ToolExposureAuthority.
- [mind01/agent.py:47](../../../../mind01/agent.py#L47) imports `tool_exposure` / ToolExposureContext.
- [mind01/agent.py:53](../../../../mind01/agent.py#L53) imports `tools` / ToolError.
- [mind01/agent.py:53](../../../../mind01/agent.py#L53) imports `tools` / ToolRegistry.
- [mind01/agent.py:54](../../../../mind01/agent.py#L54) imports `tools.schemas` / SCHEMA_BY_NAME.
- [mind01/agent.py:55](../../../../mind01/agent.py#L55) imports `traces` / TraceError.
- [mind01/agent.py:55](../../../../mind01/agent.py#L55) imports `traces` / TraceStore.
- [mind01/agent.py:55](../../../../mind01/agent.py#L55) imports `traces` / summarize_prompt.
- [mind01/agent.py:55](../../../../mind01/agent.py#L55) imports `traces` / summarize_result.
- [mind01/agent.py:55](../../../../mind01/agent.py#L55) imports `traces` / trace_event_base.
- [mind01/agent.py:56](../../../../mind01/agent.py#L56) imports `verification` / VerificationEngine.

## Symbols

### `mind01.agent.INSPECTION_TOOLS` — lines 59–62

- Source: [mind01/agent.py:59](../../../../mind01/agent.py#L59)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.MUTATION_TOOLS` — lines 63–65

- Source: [mind01/agent.py:63](../../../../mind01/agent.py#L63)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.VERIFICATION_TOOLS` — lines 66–66

- Source: [mind01/agent.py:66](../../../../mind01/agent.py#L66)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.MUTATING_ACTIONS` — lines 67–67

- Source: [mind01/agent.py:67](../../../../mind01/agent.py#L67)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.NON_SOURCE_MUTATION_ACTIONS` — lines 68–68

- Source: [mind01/agent.py:68](../../../../mind01/agent.py#L68)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.AgentResponse` — lines 72–82

- Source: [mind01/agent.py:72](../../../../mind01/agent.py#L72)
- Type: class
- Signature: `n/a`
- Direct static callees: `field`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent` — lines 85–673

- Source: [mind01/agent.py:85](../../../../mind01/agent.py#L85)
- Type: class
- Signature: `n/a`
- Direct static callees: `AgentResponse`, `AgentState`, `HierarchicalRouter`, `OllamaClient`, `OllamaSemanticClassifier`, `Planner`, `ReceiptStore`, `RecoveryController`, `RuleBasedSemanticClassifier`, `SemanticRouterV2`, `SkillRegistry`, `ToolExposureAuthority`, `ToolRegistry`, `TraceStore`, `VerificationEngine`, `_action_required`, `_attach_verification_summary`, `_build_runtime_context`, `_changed_paths`, `_dry_run_response`, `_handle_memory_intent`, `_model_phase`, `_normalize_history`, `_patch_review_evidence`, `_recall_intent`, `_receipt_id_from_result`, `_receipt_integrity_evidence`, `_remember_intent`, `_requires_grounding`, `_response`, `_review_receipt`, `_runtime_completion_decision`, `_semantic_route`, `_trace_agent_event`, `_trace_final`, `_visible_tools`, `any`, `append`, `bool`, `build`, `build_action_instruction`, `build_generation_only_write_correction`, `build_task_contract`, `call`, `canonical_response_schema`, `chat`, `compact_text`, `detect_memory_intent`, `dumps`, `extend`, `from_dict`, `get`, `get_final_quality_issue`, `int`, `join`, `legacy_decision`, `legacy_view`, `len`, `list`, `mandatory_requirements`, `max`, `monotonic`, `parse_action_output`, `parser_failure`, `preview_model_output`, `range`, `record_error`, `repeated_action`, `rollback`, `route_typed`, `select`, `set`, `should_block_generation_only_write`, `sorted`, `state_hash`, `str`, `strip`, `summarize_prompt`, `summarize_result`, `to_dict`, `tool_error`, `trace_event_base`, `transition`, `update`, `uuid4`, `verify_paths`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent.__init__` — lines 88–133

- Source: [mind01/agent.py:88](../../../../mind01/agent.py#L88)
- Type: method
- Signature: `self, config: AgentConfig, *, initial_messages: Iterable[Message] | None=None, session_id: str | None=None`
- Direct static callees: `HierarchicalRouter`, `OllamaClient`, `OllamaSemanticClassifier`, `Planner`, `RecoveryController`, `RuleBasedSemanticClassifier`, `SemanticRouterV2`, `SkillRegistry`, `ToolExposureAuthority`, `ToolRegistry`, `TraceStore`, `VerificationEngine`, `_normalize_history`, `extend`, `uuid4`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent.ask` — lines 135–525

- Source: [mind01/agent.py:135](../../../../mind01/agent.py#L135)
- Type: method
- Signature: `self, prompt: str`
- Direct static callees: `AgentState`, `ReceiptStore`, `_action_required`, `_attach_verification_summary`, `_build_runtime_context`, `_changed_paths`, `_dry_run_response`, `_handle_memory_intent`, `_model_phase`, `_patch_review_evidence`, `_receipt_id_from_result`, `_receipt_integrity_evidence`, `_requires_grounding`, `_response`, `_review_receipt`, `_runtime_completion_decision`, `_semantic_route`, `_trace_agent_event`, `_trace_final`, `_visible_tools`, `any`, `append`, `bool`, `build`, `build_action_instruction`, `build_generation_only_write_correction`, `build_task_contract`, `call`, `canonical_response_schema`, `chat`, `compact_text`, `dumps`, `extend`, `from_dict`, `get`, `get_final_quality_issue`, `int`, `join`, `len`, `list`, `mandatory_requirements`, `max`, `monotonic`, `parse_action_output`, `parser_failure`, `preview_model_output`, `range`, `record_error`, `repeated_action`, `rollback`, `select`, `set`, `should_block_generation_only_write`, `sorted`, `state_hash`, `str`, `strip`, `summarize_prompt`, `summarize_result`, `to_dict`, `tool_error`, `transition`, `verify_paths`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._response` — lines 527–547

- Source: [mind01/agent.py:527](../../../../mind01/agent.py#L527)
- Type: method
- Signature: `self, text: str, steps: int, trace: list[str], state: AgentState, *, completion_status: str='unverified'`
- Direct static callees: `AgentResponse`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._semantic_route` — lines 549–617

- Source: [mind01/agent.py:549](../../../../mind01/agent.py#L549)
- Type: method
- Signature: `self, prompt: str`
- Direct static callees: `_trace_agent_event`, `legacy_decision`, `legacy_view`, `route_typed`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._dry_run_response` — lines 619–620

- Source: [mind01/agent.py:619](../../../../mind01/agent.py#L619)
- Type: method
- Signature: `self, prompt: str, route: RouteDecision, plan_text: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._handle_memory_intent` — lines 622–630

- Source: [mind01/agent.py:622](../../../../mind01/agent.py#L622)
- Type: method
- Signature: `self, prompt: str, trace: List[str]`
- Direct static callees: `_recall_intent`, `_remember_intent`, `detect_memory_intent`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._remember_intent` — lines 632–641

- Source: [mind01/agent.py:632](../../../../mind01/agent.py#L632)
- Type: method
- Signature: `self, intent: MemoryIntent, trace: List[str]`
- Direct static callees: `AgentState`, `_response`, `append`, `call`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._recall_intent` — lines 643–653

- Source: [mind01/agent.py:643](../../../../mind01/agent.py#L643)
- Type: method
- Signature: `self, intent: MemoryIntent, trace: List[str]`
- Direct static callees: `AgentState`, `_response`, `append`, `call`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._trace_final` — lines 655–664

- Source: [mind01/agent.py:655](../../../../mind01/agent.py#L655)
- Type: method
- Signature: `self, text: str, decision: str, route: RouteDecision`
- Direct static callees: `_trace_agent_event`, `summarize_result`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.Agent._trace_agent_event` — lines 666–673

- Source: [mind01/agent.py:666](../../../../mind01/agent.py#L666)
- Type: method
- Signature: `self, event_type: str, data: dict[str, Any]`
- Direct static callees: `append`, `get`, `trace_event_base`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._normalize_history` — lines 676–689

- Source: [mind01/agent.py:676](../../../../mind01/agent.py#L676)
- Type: function
- Signature: `messages: Iterable[Message], max_messages: int=24, max_chars: int=24000`
- Direct static callees: `append`, `get`, `len`, `list`, `reversed`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._build_runtime_context` — lines 692–709

- Source: [mind01/agent.py:692](../../../../mind01/agent.py#L692)
- Type: function
- Signature: `route: RouteDecision, plan: str, skills: tuple[Any, ...], contract: TaskContract | None=None, semantic_route: RoutingDecision | None=None`
- Direct static callees: `dumps`, `join`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._visible_tools` — lines 712–757

- Source: [mind01/agent.py:712](../../../../mind01/agent.py#L712)
- Type: function
- Signature: `route: RouteDecision, state: AgentState, inspected: bool, *, allow_write: bool=False, allow_shell: bool=False, semantic_route: RoutingDecision | None=None, authority: ToolExposureAuthority | None=None`
- Direct static callees: `ToolExposureAuthority`, `build`, `decide`, `legacy_visible_tools`, `record_error`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._action_required` — lines 760–775

- Source: [mind01/agent.py:760](../../../../mind01/agent.py#L760)
- Type: function
- Signature: `route: RouteDecision, tool_calls: int, state: AgentState, *, semantic_route: RoutingDecision | None=None`
- Direct static callees: `_requires_grounding`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._model_phase` — lines 778–793

- Source: [mind01/agent.py:778](../../../../mind01/agent.py#L778)
- Type: function
- Signature: `route: RouteDecision, state: AgentState, inspected: bool, *, semantic_route: RoutingDecision | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._requires_grounding` — lines 796–807

- Source: [mind01/agent.py:796](../../../../mind01/agent.py#L796)
- Type: function
- Signature: `route: RouteDecision, tool_calls: int, *, semantic_route: RoutingDecision | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._changed_paths` — lines 810–814

- Source: [mind01/agent.py:810](../../../../mind01/agent.py#L810)
- Type: function
- Signature: `action: ParsedAction`
- Direct static callees: `get`, `isinstance`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._runtime_completion_decision` — lines 817–846

- Source: [mind01/agent.py:817](../../../../mind01/agent.py#L817)
- Type: function
- Signature: `action: ParsedAction, state: AgentState`
- Direct static callees: `CompletionAuthority`, `append`, `decide`, `from_dict`, `get`, `items`, `list`, `str`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._runtime_completion_status` — lines 849–852

- Source: [mind01/agent.py:849](../../../../mind01/agent.py#L849)
- Type: function
- Signature: `action: ParsedAction, state: AgentState`
- Direct static callees: `_runtime_completion_decision`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._attach_verification_summary` — lines 855–871

- Source: [mind01/agent.py:855](../../../../mind01/agent.py#L855)
- Type: function
- Signature: `text: str, results: list[dict[str, Any]]`
- Direct static callees: `any`, `append`, `get`, `join`, `rstrip`, `str`, `upper`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.parse_action` — lines 874–875

- Source: [mind01/agent.py:874](../../../../mind01/agent.py#L874)
- Type: function
- Signature: `raw: str`
- Direct static callees: `parse_action_output`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.build_parse_recovery_message` — lines 878–879

- Source: [mind01/agent.py:878](../../../../mind01/agent.py#L878)
- Type: function
- Signature: `raw: str, error: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.build_generation_only_write_correction` — lines 882–886

- Source: [mind01/agent.py:882](../../../../mind01/agent.py#L882)
- Type: function
- Signature: `prompt: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.should_block_generation_only_write` — lines 889–890

- Source: [mind01/agent.py:889](../../../../mind01/agent.py#L889)
- Type: function
- Signature: `prompt: str, action: ParsedAction`
- Direct static callees: `_explicit_mutation_request`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._explicit_mutation_request` — lines 893–895

- Source: [mind01/agent.py:893](../../../../mind01/agent.py#L893)
- Type: function
- Signature: `prompt: str`
- Direct static callees: `bool`, `has_named_workspace_file`, `lower`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.has_named_workspace_file` — lines 898–899

- Source: [mind01/agent.py:898](../../../../mind01/agent.py#L898)
- Type: function
- Signature: `text: str`
- Direct static callees: `bool`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.can_use_plain_text_fallback` — lines 902–904

- Source: [mind01/agent.py:902](../../../../mind01/agent.py#L902)
- Type: function
- Signature: `raw: str, mode: AgentMode`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.get_final_quality_issue` — lines 907–921

- Source: [mind01/agent.py:907](../../../../mind01/agent.py#L907)
- Type: function
- Signature: `text: str, original_prompt: str, mode: AgentMode | None=None`
- Direct static callees: `any`, `len`, `lower`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.is_low_quality_recovery_final` — lines 924–925

- Source: [mind01/agent.py:924](../../../../mind01/agent.py#L924)
- Type: function
- Signature: `text: str, original_prompt: str`
- Direct static callees: `get_final_quality_issue`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.build_preflight_deterministic_answer` — lines 928–929

- Source: [mind01/agent.py:928](../../../../mind01/agent.py#L928)
- Type: function
- Signature: `prompt: str, mode: AgentMode | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.build_deterministic_domain_repair_answer` — lines 932–933

- Source: [mind01/agent.py:932](../../../../mind01/agent.py#L932)
- Type: function
- Signature: `prompt: str, reason: str, mode: AgentMode | None=None`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.deterministic_backend_inspection_repair` — lines 936–937

- Source: [mind01/agent.py:936](../../../../mind01/agent.py#L936)
- Type: function
- Signature: `prompt: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.looks_like_json_container` — lines 940–942

- Source: [mind01/agent.py:940](../../../../mind01/agent.py#L940)
- Type: function
- Signature: `text: str`
- Direct static callees: `endswith`, `startswith`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent.preview_model_output` — lines 945–946

- Source: [mind01/agent.py:945](../../../../mind01/agent.py#L945)
- Type: function
- Signature: `raw: str, limit: int=200`
- Direct static callees: `redact_secrets`, `replace`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._receipt_id_from_result` — lines 949–951

- Source: [mind01/agent.py:949](../../../../mind01/agent.py#L949)
- Type: function
- Signature: `text: str`
- Direct static callees: `group`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._review_receipt` — lines 954–981

- Source: [mind01/agent.py:954](../../../../mind01/agent.py#L954)
- Type: function
- Signature: `workspace: Path, receipt_id: str, expected_paths: list[str] | None=None`
- Direct static callees: `ReceiptStore`, `exists`, `get`, `join`, `read_text`, `review_patch`, `splitlines`, `str`, `to_dicts`, `unified_diff`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._patch_review_evidence` — lines 984–1013

- Source: [mind01/agent.py:984](../../../../mind01/agent.py#L984)
- Type: function
- Signature: `review: list[dict[str, str]], contract: TaskContract | None, mutation_state_hash: str, sequence: int`
- Direct static callees: `any`, `get`, `join`, `list`, `requirement_ids_for_evidence`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.agent._receipt_integrity_evidence` — lines 1016–1056

- Source: [mind01/agent.py:1016](../../../../mind01/agent.py#L1016)
- Type: function
- Signature: `workspace: Path, receipt_id: str, contract: TaskContract | None, mutation_state_hash: str, sequence: int`
- Direct static callees: `ReceiptStore`, `bool`, `get`, `hexdigest`, `is_file`, `list`, `read_bytes`, `requirement_ids_for_evidence`, `resolve`, `sha256`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–4

Imports a dependency used by this module.

### Lines 5–5

Imports a dependency used by this module.

### Lines 6–6

Imports a dependency used by this module.

### Lines 7–7

Imports a dependency used by this module.

### Lines 8–8

Imports a dependency used by this module.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports a dependency used by this module.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 13–19

Imports a dependency used by this module.

### Lines 20–20

Imports a dependency used by this module.

### Lines 21–21

Imports a dependency used by this module.

### Lines 22–22

Imports a dependency used by this module.

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports a dependency used by this module.

### Lines 25–25

Imports a dependency used by this module.

### Lines 26–26

Imports a dependency used by this module.

### Lines 27–27

Imports a dependency used by this module.

### Lines 28–28

Imports a dependency used by this module.

### Lines 29–29

Imports a dependency used by this module.

### Lines 30–30

Imports a dependency used by this module.

### Lines 31–35

Imports a dependency used by this module.

### Lines 36–36

Imports a dependency used by this module.

### Lines 37–37

Imports a dependency used by this module.

### Lines 38–38

Imports a dependency used by this module.

### Lines 39–46

Imports a dependency used by this module.

### Lines 47–52

Imports a dependency used by this module.

### Lines 53–53

Imports a dependency used by this module.

### Lines 54–54

Imports a dependency used by this module.

### Lines 55–55

Imports a dependency used by this module.

### Lines 56–56

Imports a dependency used by this module.

### Lines 57–58

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 59–62

Implements module-level `Assign` behavior or data.

### Lines 63–65

Implements module-level `Assign` behavior or data.

### Lines 66–66

Implements module-level `Assign` behavior or data.

### Lines 67–67

Implements module-level `Assign` behavior or data.

### Lines 68–68

Implements module-level `Assign` behavior or data.

### Lines 69–71

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 72–82

Defines class `AgentResponse` and the behavior of its members.

### Lines 83–84

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 85–114

Defines class `Agent` and the behavior of its members.

### Lines 115–144

Defines class `Agent` and the behavior of its members.

### Lines 145–174

Defines class `Agent` and the behavior of its members.

### Lines 175–204

Defines class `Agent` and the behavior of its members.

### Lines 205–234

Defines class `Agent` and the behavior of its members.

### Lines 235–264

Defines class `Agent` and the behavior of its members.

### Lines 265–294

Defines class `Agent` and the behavior of its members.

### Lines 295–324

Defines class `Agent` and the behavior of its members.

### Lines 325–354

Defines class `Agent` and the behavior of its members.

### Lines 355–384

Defines class `Agent` and the behavior of its members.

### Lines 385–414

Defines class `Agent` and the behavior of its members.

### Lines 415–444

Defines class `Agent` and the behavior of its members.

### Lines 445–474

Defines class `Agent` and the behavior of its members.

### Lines 475–504

Defines class `Agent` and the behavior of its members.

### Lines 505–534

Defines class `Agent` and the behavior of its members.

### Lines 535–564

Defines class `Agent` and the behavior of its members.

### Lines 565–594

Defines class `Agent` and the behavior of its members.

### Lines 595–624

Defines class `Agent` and the behavior of its members.

### Lines 625–654

Defines class `Agent` and the behavior of its members.

### Lines 655–673

Defines class `Agent` and the behavior of its members.

### Lines 674–675

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 676–689

Defines `_normalize_history` and its implementation control flow; direct static calls: append, get, len, list, reversed, str.

### Lines 690–691

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 692–709

Defines `_build_runtime_context` and its implementation control flow; direct static calls: dumps, join, to_dict.

### Lines 710–711

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 712–741

Defines `_visible_tools` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, legacy_visible_tools, record_error.

### Lines 742–757

Defines `_visible_tools` and its implementation control flow; direct static calls: ToolExposureAuthority, build, decide, legacy_visible_tools, record_error.

### Lines 758–759

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 760–775

Defines `_action_required` and its implementation control flow; direct static calls: _requires_grounding.

### Lines 776–777

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 778–793

Defines `_model_phase` and its implementation control flow; direct static calls: none resolved.

### Lines 794–795

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 796–807

Defines `_requires_grounding` and its implementation control flow; direct static calls: none resolved.

### Lines 808–809

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 810–814

Defines `_changed_paths` and its implementation control flow; direct static calls: get, isinstance.

### Lines 815–816

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 817–846

Defines `_runtime_completion_decision` and its implementation control flow; direct static calls: CompletionAuthority, append, decide, from_dict, get, items, list, str, to_dict.

### Lines 847–848

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 849–852

Defines `_runtime_completion_status` and its implementation control flow; direct static calls: _runtime_completion_decision, str.

### Lines 853–854

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 855–871

Defines `_attach_verification_summary` and its implementation control flow; direct static calls: any, append, get, join, rstrip, str, upper.

### Lines 872–873

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 874–875

Defines `parse_action` and its implementation control flow; direct static calls: parse_action_output.

### Lines 876–877

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 878–879

Defines `build_parse_recovery_message` and its implementation control flow; direct static calls: none resolved.

### Lines 880–881

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 882–886

Defines `build_generation_only_write_correction` and its implementation control flow; direct static calls: none resolved.

### Lines 887–888

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 889–890

Defines `should_block_generation_only_write` and its implementation control flow; direct static calls: _explicit_mutation_request.

### Lines 891–892

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 893–895

Defines `_explicit_mutation_request` and its implementation control flow; direct static calls: bool, has_named_workspace_file, lower, search.

### Lines 896–897

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 898–899

Defines `has_named_workspace_file` and its implementation control flow; direct static calls: bool, search.

### Lines 900–901

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 902–904

Defines `can_use_plain_text_fallback` and its implementation control flow; direct static calls: none resolved.

### Lines 905–906

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 907–921

Defines `get_final_quality_issue` and its implementation control flow; direct static calls: any, len, lower, strip.

### Lines 922–923

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 924–925

Defines `is_low_quality_recovery_final` and its implementation control flow; direct static calls: get_final_quality_issue.

### Lines 926–927

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 928–929

Defines `build_preflight_deterministic_answer` and its implementation control flow; direct static calls: none resolved.

### Lines 930–931

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 932–933

Defines `build_deterministic_domain_repair_answer` and its implementation control flow; direct static calls: none resolved.

### Lines 934–935

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 936–937

Defines `deterministic_backend_inspection_repair` and its implementation control flow; direct static calls: none resolved.

### Lines 938–939

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 940–942

Defines `looks_like_json_container` and its implementation control flow; direct static calls: endswith, startswith, strip.

### Lines 943–944

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 945–946

Defines `preview_model_output` and its implementation control flow; direct static calls: redact_secrets, replace, strip.

### Lines 947–948

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 949–951

Defines `_receipt_id_from_result` and its implementation control flow; direct static calls: group, search.

### Lines 952–953

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 954–981

Defines `_review_receipt` and its implementation control flow; direct static calls: ReceiptStore, exists, get, join, read_text, review_patch, splitlines, str, to_dicts, unified_diff.

### Lines 982–983

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 984–1013

Defines `_patch_review_evidence` and its implementation control flow; direct static calls: any, get, join, list, requirement_ids_for_evidence.

### Lines 1014–1015

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1016–1045

Defines `_receipt_integrity_evidence` and its implementation control flow; direct static calls: ReceiptStore, bool, get, hexdigest, is_file, list, read_bytes, requirement_ids_for_evidence, resolve, sha256, str.

### Lines 1046–1056

Defines `_receipt_integrity_evidence` and its implementation control flow; direct static calls: ReceiptStore, bool, get, hexdigest, is_file, list, read_bytes, requirement_ids_for_evidence, resolve, sha256, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
