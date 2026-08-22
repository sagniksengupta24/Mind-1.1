# `mind01/routing.py`

## File purpose

This semantic routing file is reviewed at snapshot `9a2e38e9bdb3bbc0174a9db5e30ee96be84068a8c6d533a7fe2b3b4d1a8ca64d`. It contains 727 lines.

## Imports and module state

- [mind01/routing.py:1](../../../../mind01/routing.py#L1) imports `__future__` / annotations.
- [mind01/routing.py:3](../../../../mind01/routing.py#L3) imports `hashlib`.
- [mind01/routing.py:4](../../../../mind01/routing.py#L4) imports `json`.
- [mind01/routing.py:5](../../../../mind01/routing.py#L5) imports `re`.
- [mind01/routing.py:6](../../../../mind01/routing.py#L6) imports `dataclasses` / dataclass.
- [mind01/routing.py:6](../../../../mind01/routing.py#L6) imports `dataclasses` / field.
- [mind01/routing.py:7](../../../../mind01/routing.py#L7) imports `enum` / Enum.
- [mind01/routing.py:8](../../../../mind01/routing.py#L8) imports `pathlib` / Path.
- [mind01/routing.py:9](../../../../mind01/routing.py#L9) imports `typing` / Any.
- [mind01/routing.py:9](../../../../mind01/routing.py#L9) imports `typing` / Mapping.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / Ambiguity.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / AmbiguityLevel.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / Capability.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / ExpectedOutputMode.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / InterpretationIncidentCode.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / NormalizedIntent.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / RiskLevel.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / TargetKind.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / TaskClass.
- [mind01/routing.py:11](../../../../mind01/routing.py#L11) imports `intent` / intent_identity.
- [mind01/routing.py:23](../../../../mind01/routing.py#L23) imports `modes` / AgentMode.
- [mind01/routing.py:23](../../../../mind01/routing.py#L23) imports `modes` / parse_agent_mode.
- [mind01/routing.py:24](../../../../mind01/routing.py#L24) imports `tools.schemas` / SCHEMA_BY_NAME.

## Symbols

### `mind01.routing.Specialist` — lines 27–34

- Source: [mind01/routing.py:27](../../../../mind01/routing.py#L27)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.ToolFamily` — lines 37–50

- Source: [mind01/routing.py:37](../../../../mind01/routing.py#L37)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.ReasonCode` — lines 53–90

- Source: [mind01/routing.py:53](../../../../mind01/routing.py#L53)
- Type: class
- Signature: `n/a`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RoutingDecision` — lines 94–208

- Source: [mind01/routing.py:94](../../../../mind01/routing.py#L94)
- Type: class
- Signature: `n/a`
- Direct static callees: `Capability`, `ExpectedOutputMode`, `ReasonCode`, `RiskLevel`, `Specialist`, `TaskClass`, `ToolFamily`, `ValueError`, `_capability_fingerprint`, `any`, `cls`, `dataclass`, `field`, `float`, `isinstance`, `join`, `len`, `list`, `set`, `sorted`, `startswith`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RoutingDecision.__post_init__` — lines 115–137

- Source: [mind01/routing.py:115](../../../../mind01/routing.py#L115)
- Type: method
- Signature: `self`
- Direct static callees: `ValueError`, `join`, `len`, `set`, `sorted`, `startswith`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RoutingDecision.to_dict` — lines 139–159

- Source: [mind01/routing.py:139](../../../../mind01/routing.py#L139)
- Type: method
- Signature: `self`
- Direct static callees: `list`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RoutingDecision.from_dict` — lines 162–205

- Source: [mind01/routing.py:162](../../../../mind01/routing.py#L162)
- Type: method
- Signature: `cls, payload: Mapping[str, Any]`
- Direct static callees: `Capability`, `ExpectedOutputMode`, `ReasonCode`, `RiskLevel`, `Specialist`, `TaskClass`, `ToolFamily`, `ValueError`, `any`, `cls`, `float`, `isinstance`, `join`, `set`, `sorted`, `str`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RoutingDecision.is_current_for` — lines 207–208

- Source: [mind01/routing.py:207](../../../../mind01/routing.py#L207)
- Type: method
- Signature: `self, granted_capabilities: tuple[Capability, ...], mode: str`
- Direct static callees: `_capability_fingerprint`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.RouteDecision` — lines 212–224

- Source: [mind01/routing.py:212](../../../../mind01/routing.py#L212)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`, `field`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._FILE_RE` — lines 227–230

- Source: [mind01/routing.py:227](../../../../mind01/routing.py#L227)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._SYMBOL_RE` — lines 231–231

- Source: [mind01/routing.py:231](../../../../mind01/routing.py#L231)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._REVERSE_SYMBOL_RE` — lines 232–232

- Source: [mind01/routing.py:232](../../../../mind01/routing.py#L232)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._MUTATION_RE` — lines 233–233

- Source: [mind01/routing.py:233](../../../../mind01/routing.py#L233)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._VERIFICATION_RE` — lines 234–234

- Source: [mind01/routing.py:234](../../../../mind01/routing.py#L234)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._INSPECTION_RE` — lines 235–235

- Source: [mind01/routing.py:235](../../../../mind01/routing.py#L235)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._POLICY_ATTACK_RE` — lines 236–239

- Source: [mind01/routing.py:236](../../../../mind01/routing.py#L236)
- Type: constant
- Signature: `n/a`
- Direct static callees: `compile`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter` — lines 242–718

- Source: [mind01/routing.py:242](../../../../mind01/routing.py#L242)
- Type: class
- Signature: `n/a`
- Direct static callees: `Ambiguity`, `NormalizedIntent`, `Path`, `RouteDecision`, `RoutingDecision`, `ValueError`, `_capability_fingerprint`, `_confidence`, `_granted_capabilities`, `_legacy`, `_legacy_verification`, `_select_route`, `append`, `bool`, `extend`, `finditer`, `fromkeys`, `group`, `intent_identity`, `interpret`, `join`, `len`, `lower`, `match`, `max`, `min`, `parse_agent_mode`, `round`, `route_typed`, `search`, `set`, `split`, `strip`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter.route` — lines 245–259

- Source: [mind01/routing.py:245](../../../../mind01/routing.py#L245)
- Type: method
- Signature: `self, prompt: str, workspace: Path`
- Direct static callees: `_legacy`, `route_typed`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter.legacy_view` — lines 261–262

- Source: [mind01/routing.py:261](../../../../mind01/routing.py#L261)
- Type: method
- Signature: `self, decision: RoutingDecision`
- Direct static callees: `_legacy`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter.route_typed` — lines 264–321

- Source: [mind01/routing.py:264](../../../../mind01/routing.py#L264)
- Type: method
- Signature: `self, prompt: str, workspace: Path, *, mode: str | AgentMode=AgentMode.READ_ONLY, allow_write: bool=False, allow_shell: bool=False, allow_network: bool=False, prior_inspection: bool=False`
- Direct static callees: `RoutingDecision`, `_capability_fingerprint`, `_confidence`, `_granted_capabilities`, `_select_route`, `interpret`, `parse_agent_mode`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter.interpret` — lines 323–539

- Source: [mind01/routing.py:323](../../../../mind01/routing.py#L323)
- Type: method
- Signature: `self, prompt: str, *, mode: AgentMode, granted_capabilities: tuple[Capability, ...], prior_inspection: bool`
- Direct static callees: `Ambiguity`, `NormalizedIntent`, `ValueError`, `append`, `bool`, `extend`, `finditer`, `fromkeys`, `group`, `intent_identity`, `join`, `len`, `lower`, `match`, `search`, `split`, `strip`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter._select_route` — lines 541–625

- Source: [mind01/routing.py:541](../../../../mind01/routing.py#L541)
- Type: method
- Signature: `self, intent: NormalizedIntent, mode: AgentMode`
- Direct static callees: `lower`, `match`, `search`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter._legacy` — lines 627–674

- Source: [mind01/routing.py:627](../../../../mind01/routing.py#L627)
- Type: method
- Signature: `self, decision: RoutingDecision`
- Direct static callees: `Path`, `RouteDecision`, `_legacy_verification`, `bool`, `fromkeys`, `lower`, `search`, `set`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter._legacy_verification` — lines 677–688

- Source: [mind01/routing.py:677](../../../../mind01/routing.py#L677)
- Type: method
- Signature: `specialist: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter._granted_capabilities` — lines 691–707

- Source: [mind01/routing.py:691](../../../../mind01/routing.py#L691)
- Type: method
- Signature: `mode: AgentMode, *, allow_write: bool, allow_shell: bool, allow_network: bool`
- Direct static callees: `append`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing.HierarchicalRouter._confidence` — lines 710–718

- Source: [mind01/routing.py:710](../../../../mind01/routing.py#L710)
- Type: method
- Signature: `intent: NormalizedIntent, reason: ReasonCode`
- Direct static callees: `max`, `min`, `round`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.routing._capability_fingerprint` — lines 721–727

- Source: [mind01/routing.py:721](../../../../mind01/routing.py#L721)
- Type: function
- Signature: `capabilities: tuple[Capability, ...], mode: str`
- Direct static callees: `dumps`, `encode`, `hexdigest`, `sha256`, `sorted`
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

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 11–22

Imports a dependency used by this module.

### Lines 23–23

Imports a dependency used by this module.

### Lines 24–24

Imports a dependency used by this module.

### Lines 25–26

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 27–34

Defines class `Specialist` and the behavior of its members.

### Lines 35–36

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 37–50

Defines class `ToolFamily` and the behavior of its members.

### Lines 51–52

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 53–82

Defines class `ReasonCode` and the behavior of its members.

### Lines 83–90

Defines class `ReasonCode` and the behavior of its members.

### Lines 91–93

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 94–123

Defines class `RoutingDecision` and the behavior of its members.

### Lines 124–153

Defines class `RoutingDecision` and the behavior of its members.

### Lines 154–183

Defines class `RoutingDecision` and the behavior of its members.

### Lines 184–208

Defines class `RoutingDecision` and the behavior of its members.

### Lines 209–211

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 212–224

Defines class `RouteDecision` and the behavior of its members.

### Lines 225–226

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 227–230

Implements module-level `Assign` behavior or data.

### Lines 231–231

Implements module-level `Assign` behavior or data.

### Lines 232–232

Implements module-level `Assign` behavior or data.

### Lines 233–233

Implements module-level `Assign` behavior or data.

### Lines 234–234

Implements module-level `Assign` behavior or data.

### Lines 235–235

Implements module-level `Assign` behavior or data.

### Lines 236–239

Implements module-level `Assign` behavior or data.

### Lines 240–241

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 242–271

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 272–301

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 302–331

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 332–361

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 362–391

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 392–421

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 422–451

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 452–481

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 482–511

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 512–541

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 542–571

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 572–601

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 602–631

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 632–661

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 662–691

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 692–718

Defines class `HierarchicalRouter` and the behavior of its members.

### Lines 719–720

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 721–727

Defines `_capability_fingerprint` and its implementation control flow; direct static calls: dumps, encode, hexdigest, sha256, sorted.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
