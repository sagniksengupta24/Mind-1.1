# `mind01/semantic_router_v2.py`

## File purpose

This semantic routing file is reviewed at snapshot `f7f9e3774643b248a18af5dd8a31611743d3a8ee2017169dc25b69b9dd7117d9`. It contains 2210 lines.

## Imports and module state

- [mind01/semantic_router_v2.py:9](../../../../mind01/semantic_router_v2.py#L9) imports `__future__` / annotations.
- [mind01/semantic_router_v2.py:11](../../../../mind01/semantic_router_v2.py#L11) imports `hashlib`.
- [mind01/semantic_router_v2.py:12](../../../../mind01/semantic_router_v2.py#L12) imports `json`.
- [mind01/semantic_router_v2.py:13](../../../../mind01/semantic_router_v2.py#L13) imports `re`.
- [mind01/semantic_router_v2.py:14](../../../../mind01/semantic_router_v2.py#L14) imports `time`.
- [mind01/semantic_router_v2.py:15](../../../../mind01/semantic_router_v2.py#L15) imports `dataclasses` / dataclass.
- [mind01/semantic_router_v2.py:15](../../../../mind01/semantic_router_v2.py#L15) imports `dataclasses` / field.
- [mind01/semantic_router_v2.py:15](../../../../mind01/semantic_router_v2.py#L15) imports `dataclasses` / replace.
- [mind01/semantic_router_v2.py:16](../../../../mind01/semantic_router_v2.py#L16) imports `enum` / Enum.
- [mind01/semantic_router_v2.py:17](../../../../mind01/semantic_router_v2.py#L17) imports `pathlib` / Path.
- [mind01/semantic_router_v2.py:18](../../../../mind01/semantic_router_v2.py#L18) imports `typing` / Any.
- [mind01/semantic_router_v2.py:18](../../../../mind01/semantic_router_v2.py#L18) imports `typing` / Mapping.
- [mind01/semantic_router_v2.py:18](../../../../mind01/semantic_router_v2.py#L18) imports `typing` / Protocol.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / Ambiguity.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / AmbiguityLevel.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / Capability.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / ExpectedOutputMode.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / InterpretationIncidentCode.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / NormalizedIntent.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / RiskLevel.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / TargetKind.
- [mind01/semantic_router_v2.py:20](../../../../mind01/semantic_router_v2.py#L20) imports `intent` / TaskClass.
- [mind01/semantic_router_v2.py:31](../../../../mind01/semantic_router_v2.py#L31) imports `llm` / LLMError.
- [mind01/semantic_router_v2.py:31](../../../../mind01/semantic_router_v2.py#L31) imports `llm` / Message.
- [mind01/semantic_router_v2.py:31](../../../../mind01/semantic_router_v2.py#L31) imports `llm` / OllamaClient.
- [mind01/semantic_router_v2.py:32](../../../../mind01/semantic_router_v2.py#L32) imports `modes` / AgentMode.
- [mind01/semantic_router_v2.py:32](../../../../mind01/semantic_router_v2.py#L32) imports `modes` / parse_agent_mode.
- [mind01/semantic_router_v2.py:33](../../../../mind01/semantic_router_v2.py#L33) imports `routing` / ReasonCode.
- [mind01/semantic_router_v2.py:33](../../../../mind01/semantic_router_v2.py#L33) imports `routing` / RoutingDecision.
- [mind01/semantic_router_v2.py:33](../../../../mind01/semantic_router_v2.py#L33) imports `routing` / Specialist.
- [mind01/semantic_router_v2.py:33](../../../../mind01/semantic_router_v2.py#L33) imports `routing` / ToolFamily.
- [mind01/semantic_router_v2.py:33](../../../../mind01/semantic_router_v2.py#L33) imports `routing` / _capability_fingerprint.
- [mind01/semantic_router_v2.py:40](../../../../mind01/semantic_router_v2.py#L40) imports `tool_exposure` / LifecyclePhase.
- [mind01/semantic_router_v2.py:41](../../../../mind01/semantic_router_v2.py#L41) imports `tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `mind01.semantic_router_v2.SCHEMA_VERSION` — lines 44–44

- Source: [mind01/semantic_router_v2.py:44](../../../../mind01/semantic_router_v2.py#L44)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.ROUTER_VERSION` — lines 45–45

- Source: [mind01/semantic_router_v2.py:45](../../../../mind01/semantic_router_v2.py#L45)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.MAX_ROUTING_OUTPUT_BYTES` — lines 46–46

- Source: [mind01/semantic_router_v2.py:46](../../../../mind01/semantic_router_v2.py#L46)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.MUTATION_TOOLS` — lines 47–51

- Source: [mind01/semantic_router_v2.py:47](../../../../mind01/semantic_router_v2.py#L47)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.LIVE_WRITE_TOOLS` — lines 52–54

- Source: [mind01/semantic_router_v2.py:52](../../../../mind01/semantic_router_v2.py#L52)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SHELL_TOOLS` — lines 55–57

- Source: [mind01/semantic_router_v2.py:55](../../../../mind01/semantic_router_v2.py#L55)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.DecisionSource` — lines 60–66

- Source: [mind01/semantic_router_v2.py:60](../../../../mind01/semantic_router_v2.py#L60)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.ConstraintSeverity` — lines 69–74

- Source: [mind01/semantic_router_v2.py:69](../../../../mind01/semantic_router_v2.py#L69)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.FirstLifecycleStep` — lines 77–84

- Source: [mind01/semantic_router_v2.py:77](../../../../mind01/semantic_router_v2.py#L77)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.DecisionTraceEntry` — lines 88–102

- Source: [mind01/semantic_router_v2.py:88](../../../../mind01/semantic_router_v2.py#L88)
- Type: class
- Signature: `n/a`
- Direct static callees: `_json_safe`, `dataclass`, `dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.DecisionTraceEntry.to_dict` — lines 95–102

- Source: [mind01/semantic_router_v2.py:95](../../../../mind01/semantic_router_v2.py#L95)
- Type: method
- Signature: `self`
- Direct static callees: `_json_safe`, `dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.HardConstraint` — lines 106–122

- Source: [mind01/semantic_router_v2.py:106](../../../../mind01/semantic_router_v2.py#L106)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.HardConstraint.to_dict` — lines 114–122

- Source: [mind01/semantic_router_v2.py:114](../../../../mind01/semantic_router_v2.py#L114)
- Type: method
- Signature: `self`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.NormalizedRequest` — lines 126–182

- Source: [mind01/semantic_router_v2.py:126](../../../../mind01/semantic_router_v2.py#L126)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`, `len`, `list`, `public_features`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.NormalizedRequest.public_features` — lines 150–169

- Source: [mind01/semantic_router_v2.py:150](../../../../mind01/semantic_router_v2.py#L150)
- Type: method
- Signature: `self`
- Direct static callees: `len`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.NormalizedRequest.to_dict` — lines 171–182

- Source: [mind01/semantic_router_v2.py:171](../../../../mind01/semantic_router_v2.py#L171)
- Type: method
- Signature: `self`
- Direct static callees: `list`, `public_features`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.AlternativeTask` — lines 186–188

- Source: [mind01/semantic_router_v2.py:186](../../../../mind01/semantic_router_v2.py#L186)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.TaskPrediction` — lines 192–197

- Source: [mind01/semantic_router_v2.py:192](../../../../mind01/semantic_router_v2.py#L192)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RouteSelectionPrediction` — lines 201–208

- Source: [mind01/semantic_router_v2.py:201](../../../../mind01/semantic_router_v2.py#L201)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.ModelCallStats` — lines 212–230

- Source: [mind01/semantic_router_v2.py:212](../../../../mind01/semantic_router_v2.py#L212)
- Type: class
- Signature: `n/a`
- Direct static callees: `round`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.ModelCallStats.to_dict` — lines 221–230

- Source: [mind01/semantic_router_v2.py:221](../../../../mind01/semantic_router_v2.py#L221)
- Type: method
- Signature: `self`
- Direct static callees: `round`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticClassifier` — lines 233–246

- Source: [mind01/semantic_router_v2.py:233](../../../../mind01/semantic_router_v2.py#L233)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticClassifier.predict_task` — lines 237–238

- Source: [mind01/semantic_router_v2.py:237](../../../../mind01/semantic_router_v2.py#L237)
- Type: method
- Signature: `self, request: NormalizedRequest`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticClassifier.select_route` — lines 240–246

- Source: [mind01/semantic_router_v2.py:240](../../../../mind01/semantic_router_v2.py#L240)
- Type: method
- Signature: `self, request: NormalizedRequest, task_class: TaskClass, candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RouterThresholds` — lines 250–254

- Source: [mind01/semantic_router_v2.py:250](../../../../mind01/semantic_router_v2.py#L250)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SolverResult` — lines 258–270

- Source: [mind01/semantic_router_v2.py:258](../../../../mind01/semantic_router_v2.py#L258)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`, `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SolverResult.to_dict` — lines 264–270

- Source: [mind01/semantic_router_v2.py:264](../../../../mind01/semantic_router_v2.py#L264)
- Type: method
- Signature: `self`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouteState` — lines 274–339

- Source: [mind01/semantic_router_v2.py:274](../../../../mind01/semantic_router_v2.py#L274)
- Type: class
- Signature: `n/a`
- Direct static callees: `ValueError`, `dataclass`, `dict`, `list`, `set`, `sorted`, `startswith`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouteState.__post_init__` — lines 298–313

- Source: [mind01/semantic_router_v2.py:298](../../../../mind01/semantic_router_v2.py#L298)
- Type: method
- Signature: `self`
- Direct static callees: `ValueError`, `set`, `sorted`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouteState.to_dict` — lines 315–339

- Source: [mind01/semantic_router_v2.py:315](../../../../mind01/semantic_router_v2.py#L315)
- Type: method
- Signature: `self`
- Direct static callees: `dict`, `list`, `to_dict`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.TASK_SPECIALISTS` — lines 344–374

- Source: [mind01/semantic_router_v2.py:344](../../../../mind01/semantic_router_v2.py#L344)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.TASK_SPECIALIST_FAMILIES` — lines 376–436

- Source: [mind01/semantic_router_v2.py:376](../../../../mind01/semantic_router_v2.py#L376)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.FAMILY_TOOLS` — lines 438–458

- Source: [mind01/semantic_router_v2.py:438](../../../../mind01/semantic_router_v2.py#L438)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SPECIALIST_TOOLS` — lines 460–499

- Source: [mind01/semantic_router_v2.py:460](../../../../mind01/semantic_router_v2.py#L460)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.TASK_TOOLS` — lines 501–521

- Source: [mind01/semantic_router_v2.py:501](../../../../mind01/semantic_router_v2.py#L501)
- Type: constant
- Signature: `n/a`
- Direct static callees: `frozenset`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RuleBasedSemanticClassifier` — lines 524–637

- Source: [mind01/semantic_router_v2.py:524](../../../../mind01/semantic_router_v2.py#L524)
- Type: class
- Signature: `n/a`
- Direct static callees: `ModelCallStats`, `RouteSelectionPrediction`, `TaskPrediction`, `casefold`, `iter`, `next`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RuleBasedSemanticClassifier.__init__` — lines 527–529

- Source: [mind01/semantic_router_v2.py:527](../../../../mind01/semantic_router_v2.py#L527)
- Type: method
- Signature: `self`
- Direct static callees: `ModelCallStats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RuleBasedSemanticClassifier.reset_route_stats` — lines 531–532

- Source: [mind01/semantic_router_v2.py:531](../../../../mind01/semantic_router_v2.py#L531)
- Type: method
- Signature: `self`
- Direct static callees: `ModelCallStats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RuleBasedSemanticClassifier.predict_task` — lines 534–568

- Source: [mind01/semantic_router_v2.py:534](../../../../mind01/semantic_router_v2.py#L534)
- Type: method
- Signature: `self, request: NormalizedRequest`
- Direct static callees: `TaskPrediction`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.RuleBasedSemanticClassifier.select_route` — lines 570–637

- Source: [mind01/semantic_router_v2.py:570](../../../../mind01/semantic_router_v2.py#L570)
- Type: method
- Signature: `self, request: NormalizedRequest, task_class: TaskClass, candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `RouteSelectionPrediction`, `casefold`, `iter`, `next`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier` — lines 640–763

- Source: [mind01/semantic_router_v2.py:640](../../../../mind01/semantic_router_v2.py#L640)
- Type: class
- Signature: `n/a`
- Direct static callees: `ModelCallStats`, `_call`, `append`, `chat`, `clear`, `dumps`, `items`, `len`, `parse_route_selection`, `parser`, `perf_counter`, `public_features`, `route_selection_schema`, `str`, `sum`, `task_prediction_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier.__init__` — lines 643–648

- Source: [mind01/semantic_router_v2.py:643](../../../../mind01/semantic_router_v2.py#L643)
- Type: method
- Signature: `self, client: OllamaClient`
- Direct static callees: `ModelCallStats`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier.reset_route_stats` — lines 650–653

- Source: [mind01/semantic_router_v2.py:650](../../../../mind01/semantic_router_v2.py#L650)
- Type: method
- Signature: `self`
- Direct static callees: `ModelCallStats`, `clear`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier.predict_task` — lines 655–683

- Source: [mind01/semantic_router_v2.py:655](../../../../mind01/semantic_router_v2.py#L655)
- Type: method
- Signature: `self, request: NormalizedRequest`
- Direct static callees: `_call`, `dumps`, `public_features`, `task_prediction_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier.select_route` — lines 685–725

- Source: [mind01/semantic_router_v2.py:685](../../../../mind01/semantic_router_v2.py#L685)
- Type: method
- Signature: `self, request: NormalizedRequest, task_class: TaskClass, candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `_call`, `dumps`, `items`, `parse_route_selection`, `public_features`, `route_selection_schema`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.OllamaSemanticClassifier._call` — lines 727–763

- Source: [mind01/semantic_router_v2.py:727](../../../../mind01/semantic_router_v2.py#L727)
- Type: method
- Signature: `self, messages: list[Message], schema: dict[str, Any], parser: Any`
- Direct static callees: `append`, `chat`, `len`, `parser`, `perf_counter`, `str`, `sum`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.FAMILY_PURPOSE` — lines 766–768

- Source: [mind01/semantic_router_v2.py:766](../../../../mind01/semantic_router_v2.py#L766)
- Type: constant
- Signature: `n/a`
- Direct static callees: `replace`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SPECIALIST_PURPOSE` — lines 769–777

- Source: [mind01/semantic_router_v2.py:769](../../../../mind01/semantic_router_v2.py#L769)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.FAMILY_BOUNDARY` — lines 778–792

- Source: [mind01/semantic_router_v2.py:778](../../../../mind01/semantic_router_v2.py#L778)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.FAMILY_LIFECYCLE` — lines 793–807

- Source: [mind01/semantic_router_v2.py:793](../../../../mind01/semantic_router_v2.py#L793)
- Type: constant
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouterV2` — lines 810–1285

- Source: [mind01/semantic_router_v2.py:810](../../../../mind01/semantic_router_v2.py#L810)
- Type: class
- Signature: `n/a`
- Direct static callees: `Ambiguity`, `DecisionTraceEntry`, `ModelCallStats`, `NormalizedIntent`, `RouterThresholds`, `RoutingDecision`, `RuleBasedSemanticClassifier`, `SemanticRouteState`, `TaskPrediction`, `_capability_fingerprint`, `append`, `callable`, `derive_reason_code`, `evaluate_policy`, `extend`, `float`, `fromkeys`, `get`, `getattr`, `granted_capabilities`, `isinstance`, `items`, `len`, `list`, `min`, `normalize_request`, `parse_agent_mode`, `perf_counter`, `predict_task`, `reduce_candidates`, `replace`, `reset_stats`, `resolve_first_step_tools`, `resolve_lifecycle`, `resolve_response_mode`, `resolve_risk`, `resolve_terminal_tools`, `round`, `route_identity`, `safe_selection`, `select_route`, `set`, `solve_constraints`, `terminal_family_for_response`, `to_dict`, `tuple`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouterV2.__init__` — lines 811–820

- Source: [mind01/semantic_router_v2.py:811](../../../../mind01/semantic_router_v2.py#L811)
- Type: method
- Signature: `self, classifier: SemanticClassifier | None=None, *, thresholds: RouterThresholds | None=None, model_identity: str='deterministic-fixture-classifier'`
- Direct static callees: `RouterThresholds`, `RuleBasedSemanticClassifier`, `getattr`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouterV2.route_typed` — lines 822–1181

- Source: [mind01/semantic_router_v2.py:822](../../../../mind01/semantic_router_v2.py#L822)
- Type: method
- Signature: `self, prompt: str, workspace: Path, *, mode: str | AgentMode=AgentMode.READ_ONLY, allow_write: bool=False, allow_shell: bool=False, allow_network: bool=False, prior_inspection: bool=False`
- Direct static callees: `DecisionTraceEntry`, `ModelCallStats`, `SemanticRouteState`, `TaskPrediction`, `append`, `callable`, `derive_reason_code`, `evaluate_policy`, `extend`, `float`, `get`, `getattr`, `items`, `len`, `list`, `min`, `normalize_request`, `parse_agent_mode`, `perf_counter`, `predict_task`, `reduce_candidates`, `replace`, `reset_stats`, `resolve_first_step_tools`, `resolve_lifecycle`, `resolve_response_mode`, `resolve_risk`, `resolve_terminal_tools`, `round`, `route_identity`, `safe_selection`, `select_route`, `solve_constraints`, `terminal_family_for_response`, `to_dict`, `tuple`, `type`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.SemanticRouterV2.legacy_decision` — lines 1183–1285

- Source: [mind01/semantic_router_v2.py:1183](../../../../mind01/semantic_router_v2.py#L1183)
- Type: method
- Signature: `self, state: SemanticRouteState, *, mode: str | AgentMode, allow_write: bool, allow_shell: bool, allow_network: bool=False`
- Direct static callees: `Ambiguity`, `NormalizedIntent`, `RoutingDecision`, `_capability_fingerprint`, `append`, `fromkeys`, `granted_capabilities`, `isinstance`, `items`, `parse_agent_mode`, `replace`, `set`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2._PATH_RE` — lines 1288–1291

- Source: [mind01/semantic_router_v2.py:1288](../../../../mind01/semantic_router_v2.py#L1288)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.normalize_request` — lines 1294–1455

- Source: [mind01/semantic_router_v2.py:1294](../../../../mind01/semantic_router_v2.py#L1294)
- Type: function
- Signature: `prompt: str, workspace: Path`
- Direct static callees: `NormalizedRequest`, `ValueError`, `any`, `bool`, `casefold`, `finditer`, `fromkeys`, `group`, `join`, `len`, `search`, `split`, `startswith`, `strip`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.evaluate_policy` — lines 1458–1532

- Source: [mind01/semantic_router_v2.py:1458](../../../../mind01/semantic_router_v2.py#L1458)
- Type: function
- Signature: `request: NormalizedRequest, mode: AgentMode, *, allow_write: bool, allow_shell: bool, allow_network: bool`
- Direct static callees: `HardConstraint`, `add`, `append`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.resolve_response_mode` — lines 1535–1549

- Source: [mind01/semantic_router_v2.py:1535](../../../../mind01/semantic_router_v2.py#L1535)
- Type: function
- Signature: `request: NormalizedRequest, constraints: tuple[HardConstraint, ...], mode: AgentMode`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.resolve_risk` — lines 1552–1566

- Source: [mind01/semantic_router_v2.py:1552](../../../../mind01/semantic_router_v2.py#L1552)
- Type: function
- Signature: `request: NormalizedRequest, constraints: tuple[HardConstraint, ...]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.reduce_candidates` — lines 1569–1610

- Source: [mind01/semantic_router_v2.py:1569](../../../../mind01/semantic_router_v2.py#L1569)
- Type: function
- Signature: `task_class: TaskClass, request: NormalizedRequest, response_mode: ExpectedOutputMode`
- Direct static callees: `append`, `extend`, `fromkeys`, `list`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.safe_selection` — lines 1613–1648

- Source: [mind01/semantic_router_v2.py:1613](../../../../mind01/semantic_router_v2.py#L1613)
- Type: function
- Signature: `task_class: TaskClass, request: NormalizedRequest, candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `RouteSelectionPrediction`, `iter`, `next`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.terminal_family_for_response` — lines 1651–1664

- Source: [mind01/semantic_router_v2.py:1651](../../../../mind01/semantic_router_v2.py#L1651)
- Type: function
- Signature: `family: ToolFamily, response_mode: ExpectedOutputMode, request: NormalizedRequest`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.resolve_terminal_tools` — lines 1667–1732

- Source: [mind01/semantic_router_v2.py:1667](../../../../mind01/semantic_router_v2.py#L1667)
- Type: function
- Signature: `task_class: TaskClass, specialist: Specialist, family: ToolFamily, response_mode: ExpectedOutputMode, request: NormalizedRequest, mode: AgentMode, *, allow_write: bool, allow_shell: bool, allow_network: bool`
- Direct static callees: `append`, `casefold`, `frozenset`, `items`, `search`, `set`, `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.resolve_lifecycle` — lines 1735–1757

- Source: [mind01/semantic_router_v2.py:1735](../../../../mind01/semantic_router_v2.py#L1735)
- Type: function
- Signature: `response_mode: ExpectedOutputMode, task_class: TaskClass, family: ToolFamily, request: NormalizedRequest, terminal_tools: tuple[str, ...]`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.resolve_first_step_tools` — lines 1760–1793

- Source: [mind01/semantic_router_v2.py:1760](../../../../mind01/semantic_router_v2.py#L1760)
- Type: function
- Signature: `lifecycle: FirstLifecycleStep, terminal_tools: tuple[str, ...], specialist: Specialist, request: NormalizedRequest, mode: AgentMode, *, allow_write: bool, allow_shell: bool`
- Direct static callees: `append`, `fromkeys`, `get`, `set`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.derive_reason_code` — lines 1796–1872

- Source: [mind01/semantic_router_v2.py:1796](../../../../mind01/semantic_router_v2.py#L1796)
- Type: function
- Signature: `task_class: TaskClass, response_mode: ExpectedOutputMode, specialist: Specialist, family: ToolFamily, lifecycle: FirstLifecycleStep, request: NormalizedRequest, constraints: tuple[HardConstraint, ...]`
- Direct static callees: `casefold`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.solve_constraints` — lines 1875–1977

- Source: [mind01/semantic_router_v2.py:1875](../../../../mind01/semantic_router_v2.py#L1875)
- Type: function
- Signature: `fields: dict[str, Any], request: NormalizedRequest, constraints: tuple[HardConstraint, ...], candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `SolverResult`, `append`, `derive_reason_code`, `dict`, `float`, `len`, `max`, `min`, `round`, `tuple`, `update`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.task_prediction_schema` — lines 1980–2005

- Source: [mind01/semantic_router_v2.py:1980](../../../../mind01/semantic_router_v2.py#L1980)
- Type: function
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.route_selection_schema` — lines 2008–2052

- Source: [mind01/semantic_router_v2.py:2008](../../../../mind01/semantic_router_v2.py#L2008)
- Type: function
- Signature: `candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `append`, `items`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.parse_task_prediction` — lines 2055–2084

- Source: [mind01/semantic_router_v2.py:2055](../../../../mind01/semantic_router_v2.py#L2055)
- Type: function
- Signature: `raw: str`
- Direct static callees: `AlternativeTask`, `TaskClass`, `TaskPrediction`, `ValueError`, `_confidence`, `_exact_fields`, `append`, `isinstance`, `len`, `strict_json_object`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.parse_route_selection` — lines 2087–2124

- Source: [mind01/semantic_router_v2.py:2087](../../../../mind01/semantic_router_v2.py#L2087)
- Type: function
- Signature: `raw: str, candidates: Mapping[Specialist, tuple[ToolFamily, ...]]`
- Direct static callees: `RouteSelectionPrediction`, `Specialist`, `ToolFamily`, `ValueError`, `_confidence`, `_exact_fields`, `isinstance`, `len`, `strict_json_object`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.strict_json_object` — lines 2127–2147

- Source: [mind01/semantic_router_v2.py:2127](../../../../mind01/semantic_router_v2.py#L2127)
- Type: function
- Signature: `raw: str`
- Direct static callees: `ValueError`, `encode`, `isinstance`, `len`, `loads`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.granted_capabilities` — lines 2150–2166

- Source: [mind01/semantic_router_v2.py:2150](../../../../mind01/semantic_router_v2.py#L2150)
- Type: function
- Signature: `mode: AgentMode, *, allow_write: bool, allow_shell: bool, allow_network: bool`
- Direct static callees: `append`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2.route_identity` — lines 2169–2182

- Source: [mind01/semantic_router_v2.py:2169](../../../../mind01/semantic_router_v2.py#L2169)
- Type: function
- Signature: `prompt: str, mode: AgentMode, allow_write: bool, allow_shell: bool`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `join`, `sha256`, `split`, `strip`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2._confidence` — lines 2185–2191

- Source: [mind01/semantic_router_v2.py:2185](../../../../mind01/semantic_router_v2.py#L2185)
- Type: function
- Signature: `value: Any`
- Direct static callees: `ValueError`, `float`, `isinstance`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2._exact_fields` — lines 2194–2200

- Source: [mind01/semantic_router_v2.py:2194](../../../../mind01/semantic_router_v2.py#L2194)
- Type: function
- Signature: `payload: Mapping[str, Any], required: set[str]`
- Direct static callees: `ValueError`, `join`, `set`, `sorted`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.semantic_router_v2._json_safe` — lines 2203–2210

- Source: [mind01/semantic_router_v2.py:2203](../../../../mind01/semantic_router_v2.py#L2203)
- Type: function
- Signature: `value: Any`
- Direct static callees: `_json_safe`, `isinstance`, `items`, `str`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–7

Implements module-level `Expr` behavior or data.

### Lines 8–8

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 9–9

Imports a dependency used by this module.

### Lines 10–10

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–11

Imports a dependency used by this module.

### Lines 12–12

Imports a dependency used by this module.

### Lines 13–13

Imports a dependency used by this module.

### Lines 14–14

Imports a dependency used by this module.

### Lines 15–15

Imports a dependency used by this module.

### Lines 16–16

Imports a dependency used by this module.

### Lines 17–17

Imports a dependency used by this module.

### Lines 18–18

Imports a dependency used by this module.

### Lines 19–19

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 20–30

Imports a dependency used by this module.

### Lines 31–31

Imports a dependency used by this module.

### Lines 32–32

Imports a dependency used by this module.

### Lines 33–39

Imports a dependency used by this module.

### Lines 40–40

Imports a dependency used by this module.

### Lines 41–41

Imports a dependency used by this module.

### Lines 42–43

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 44–44

Implements module-level `Assign` behavior or data.

### Lines 45–45

Implements module-level `Assign` behavior or data.

### Lines 46–46

Implements module-level `Assign` behavior or data.

### Lines 47–51

Implements module-level `Assign` behavior or data.

### Lines 52–54

Implements module-level `Assign` behavior or data.

### Lines 55–57

Implements module-level `Assign` behavior or data.

### Lines 58–59

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 60–66

Defines class `DecisionSource` and the behavior of its members.

### Lines 67–68

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 69–74

Defines class `ConstraintSeverity` and the behavior of its members.

### Lines 75–76

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 77–84

Defines class `FirstLifecycleStep` and the behavior of its members.

### Lines 85–87

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 88–102

Defines class `DecisionTraceEntry` and the behavior of its members.

### Lines 103–105

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 106–122

Defines class `HardConstraint` and the behavior of its members.

### Lines 123–125

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 126–155

Defines class `NormalizedRequest` and the behavior of its members.

### Lines 156–182

Defines class `NormalizedRequest` and the behavior of its members.

### Lines 183–185

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 186–188

Defines class `AlternativeTask` and the behavior of its members.

### Lines 189–191

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 192–197

Defines class `TaskPrediction` and the behavior of its members.

### Lines 198–200

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 201–208

Defines class `RouteSelectionPrediction` and the behavior of its members.

### Lines 209–211

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 212–230

Defines class `ModelCallStats` and the behavior of its members.

### Lines 231–232

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 233–246

Defines class `SemanticClassifier` and the behavior of its members.

### Lines 247–249

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 250–254

Defines class `RouterThresholds` and the behavior of its members.

### Lines 255–257

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 258–270

Defines class `SolverResult` and the behavior of its members.

### Lines 271–273

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 274–303

Defines class `SemanticRouteState` and the behavior of its members.

### Lines 304–333

Defines class `SemanticRouteState` and the behavior of its members.

### Lines 334–339

Defines class `SemanticRouteState` and the behavior of its members.

### Lines 340–343

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 344–373

Implements module-level `AnnAssign` behavior or data.

### Lines 374–374

Implements module-level `AnnAssign` behavior or data.

### Lines 375–375

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 376–405

Implements module-level `AnnAssign` behavior or data.

### Lines 406–435

Implements module-level `AnnAssign` behavior or data.

### Lines 436–436

Implements module-level `AnnAssign` behavior or data.

### Lines 437–437

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 438–458

Implements module-level `AnnAssign` behavior or data.

### Lines 459–459

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 460–489

Implements module-level `AnnAssign` behavior or data.

### Lines 490–499

Implements module-level `AnnAssign` behavior or data.

### Lines 500–500

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 501–521

Implements module-level `AnnAssign` behavior or data.

### Lines 522–523

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 524–553

Defines class `RuleBasedSemanticClassifier` and the behavior of its members.

### Lines 554–583

Defines class `RuleBasedSemanticClassifier` and the behavior of its members.

### Lines 584–613

Defines class `RuleBasedSemanticClassifier` and the behavior of its members.

### Lines 614–637

Defines class `RuleBasedSemanticClassifier` and the behavior of its members.

### Lines 638–639

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 640–669

Defines class `OllamaSemanticClassifier` and the behavior of its members.

### Lines 670–699

Defines class `OllamaSemanticClassifier` and the behavior of its members.

### Lines 700–729

Defines class `OllamaSemanticClassifier` and the behavior of its members.

### Lines 730–759

Defines class `OllamaSemanticClassifier` and the behavior of its members.

### Lines 760–763

Defines class `OllamaSemanticClassifier` and the behavior of its members.

### Lines 764–765

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 766–768

Implements module-level `AnnAssign` behavior or data.

### Lines 769–777

Implements module-level `AnnAssign` behavior or data.

### Lines 778–792

Implements module-level `AnnAssign` behavior or data.

### Lines 793–807

Implements module-level `AnnAssign` behavior or data.

### Lines 808–809

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 810–839

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 840–869

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 870–899

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 900–929

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 930–959

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 960–989

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 990–1019

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1020–1049

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1050–1079

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1080–1109

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1110–1139

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1140–1169

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1170–1199

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1200–1229

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1230–1259

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1260–1285

Defines class `SemanticRouterV2` and the behavior of its members.

### Lines 1286–1287

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1288–1291

Implements module-level `Assign` behavior or data.

### Lines 1292–1293

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1294–1323

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1324–1353

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1354–1383

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1384–1413

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1414–1443

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1444–1455

Defines `normalize_request` and its implementation control flow; direct static calls: NormalizedRequest, ValueError, any, bool, casefold, finditer, fromkeys, group, join, len, search, split, startswith, strip, tuple.

### Lines 1456–1457

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1458–1487

Defines `evaluate_policy` and its implementation control flow; direct static calls: HardConstraint, add, append, tuple.

### Lines 1488–1517

Defines `evaluate_policy` and its implementation control flow; direct static calls: HardConstraint, add, append, tuple.

### Lines 1518–1532

Defines `evaluate_policy` and its implementation control flow; direct static calls: HardConstraint, add, append, tuple.

### Lines 1533–1534

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1535–1549

Defines `resolve_response_mode` and its implementation control flow; direct static calls: none resolved.

### Lines 1550–1551

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1552–1566

Defines `resolve_risk` and its implementation control flow; direct static calls: none resolved.

### Lines 1567–1568

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1569–1598

Defines `reduce_candidates` and its implementation control flow; direct static calls: append, extend, fromkeys, list, tuple.

### Lines 1599–1610

Defines `reduce_candidates` and its implementation control flow; direct static calls: append, extend, fromkeys, list, tuple.

### Lines 1611–1612

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1613–1642

Defines `safe_selection` and its implementation control flow; direct static calls: RouteSelectionPrediction, iter, next.

### Lines 1643–1648

Defines `safe_selection` and its implementation control flow; direct static calls: RouteSelectionPrediction, iter, next.

### Lines 1649–1650

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1651–1664

Defines `terminal_family_for_response` and its implementation control flow; direct static calls: none resolved.

### Lines 1665–1666

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1667–1696

Defines `resolve_terminal_tools` and its implementation control flow; direct static calls: append, casefold, frozenset, items, search, set, sorted, tuple.

### Lines 1697–1726

Defines `resolve_terminal_tools` and its implementation control flow; direct static calls: append, casefold, frozenset, items, search, set, sorted, tuple.

### Lines 1727–1732

Defines `resolve_terminal_tools` and its implementation control flow; direct static calls: append, casefold, frozenset, items, search, set, sorted, tuple.

### Lines 1733–1734

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1735–1757

Defines `resolve_lifecycle` and its implementation control flow; direct static calls: none resolved.

### Lines 1758–1759

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1760–1789

Defines `resolve_first_step_tools` and its implementation control flow; direct static calls: append, fromkeys, get, set, tuple.

### Lines 1790–1793

Defines `resolve_first_step_tools` and its implementation control flow; direct static calls: append, fromkeys, get, set, tuple.

### Lines 1794–1795

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1796–1825

Defines `derive_reason_code` and its implementation control flow; direct static calls: casefold, search.

### Lines 1826–1855

Defines `derive_reason_code` and its implementation control flow; direct static calls: casefold, search.

### Lines 1856–1872

Defines `derive_reason_code` and its implementation control flow; direct static calls: casefold, search.

### Lines 1873–1874

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1875–1904

Defines `solve_constraints` and its implementation control flow; direct static calls: SolverResult, append, derive_reason_code, dict, float, len, max, min, round, tuple, update.

### Lines 1905–1934

Defines `solve_constraints` and its implementation control flow; direct static calls: SolverResult, append, derive_reason_code, dict, float, len, max, min, round, tuple, update.

### Lines 1935–1964

Defines `solve_constraints` and its implementation control flow; direct static calls: SolverResult, append, derive_reason_code, dict, float, len, max, min, round, tuple, update.

### Lines 1965–1977

Defines `solve_constraints` and its implementation control flow; direct static calls: SolverResult, append, derive_reason_code, dict, float, len, max, min, round, tuple, update.

### Lines 1978–1979

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 1980–2005

Defines `task_prediction_schema` and its implementation control flow; direct static calls: none resolved.

### Lines 2006–2007

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2008–2037

Defines `route_selection_schema` and its implementation control flow; direct static calls: append, items.

### Lines 2038–2052

Defines `route_selection_schema` and its implementation control flow; direct static calls: append, items.

### Lines 2053–2054

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2055–2084

Defines `parse_task_prediction` and its implementation control flow; direct static calls: AlternativeTask, TaskClass, TaskPrediction, ValueError, _confidence, _exact_fields, append, isinstance, len, strict_json_object, tuple.

### Lines 2085–2086

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2087–2116

Defines `parse_route_selection` and its implementation control flow; direct static calls: RouteSelectionPrediction, Specialist, ToolFamily, ValueError, _confidence, _exact_fields, isinstance, len, strict_json_object.

### Lines 2117–2124

Defines `parse_route_selection` and its implementation control flow; direct static calls: RouteSelectionPrediction, Specialist, ToolFamily, ValueError, _confidence, _exact_fields, isinstance, len, strict_json_object.

### Lines 2125–2126

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2127–2147

Defines `strict_json_object` and its implementation control flow; direct static calls: ValueError, encode, isinstance, len, loads.

### Lines 2148–2149

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2150–2166

Defines `granted_capabilities` and its implementation control flow; direct static calls: append, tuple.

### Lines 2167–2168

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2169–2182

Defines `route_identity` and its implementation control flow; direct static calls: dumps, encode, hexdigest, join, sha256, split, strip.

### Lines 2183–2184

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2185–2191

Defines `_confidence` and its implementation control flow; direct static calls: ValueError, float, isinstance.

### Lines 2192–2193

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2194–2200

Defines `_exact_fields` and its implementation control flow; direct static calls: ValueError, join, set, sorted.

### Lines 2201–2202

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 2203–2210

Defines `_json_safe` and its implementation control flow; direct static calls: _json_safe, isinstance, items, str.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
