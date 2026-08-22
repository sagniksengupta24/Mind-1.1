# `mind01/skills.py`

## File purpose

This planning and skills file is reviewed at snapshot `4d7e2cebd0729579d64267c40dfe65bdb2c660464783ee6540bc1cbffddc7673`. It contains 48 lines.

## Imports and module state

- [mind01/skills.py:1](../../../../mind01/skills.py#L1) imports `__future__` / annotations.
- [mind01/skills.py:3](../../../../mind01/skills.py#L3) imports `dataclasses` / dataclass.

## Symbols

### `mind01.skills.Skill` — lines 7–14

- Source: [mind01/skills.py:7](../../../../mind01/skills.py#L7)
- Type: class
- Signature: `n/a`
- Direct static callees: `dataclass`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.SkillRegistry` — lines 17–31

- Source: [mind01/skills.py:17](../../../../mind01/skills.py#L17)
- Type: class
- Signature: `n/a`
- Direct static callees: `default_skills`, `sorted`, `tuple`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.SkillRegistry.__init__` — lines 18–19

- Source: [mind01/skills.py:18](../../../../mind01/skills.py#L18)
- Type: method
- Signature: `self`
- Direct static callees: `default_skills`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.SkillRegistry.get` — lines 21–22

- Source: [mind01/skills.py:21](../../../../mind01/skills.py#L21)
- Type: method
- Signature: `self, name: str`
- Direct static callees: none resolved
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.SkillRegistry.select` — lines 24–28

- Source: [mind01/skills.py:24](../../../../mind01/skills.py#L24)
- Type: method
- Signature: `self, specialist: str`
- Direct static callees: `tuple`, `values`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.SkillRegistry.names` — lines 30–31

- Source: [mind01/skills.py:30](../../../../mind01/skills.py#L30)
- Type: method
- Signature: `self`
- Direct static callees: `sorted`, `tuple`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

### `mind01.skills.default_skills` — lines 34–48

- Source: [mind01/skills.py:34](../../../../mind01/skills.py#L34)
- Type: function
- Signature: `n/a`
- Direct static callees: `Skill`
- State, failure, security, persistence, and concurrency effects are constrained by the implementation in this line range; unresolved dynamic behavior is not asserted.

## Line-range walkthrough

### Lines 1–1

Imports a dependency used by this module.

### Lines 2–2

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 3–3

Imports a dependency used by this module.

### Lines 4–6

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 7–14

Defines class `Skill` and the behavior of its members.

### Lines 15–16

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 17–31

Defines class `SkillRegistry` and the behavior of its members.

### Lines 32–33

Imports, comments, declarations, or configuration that establish the following implementation context.

### Lines 34–48

Defines `default_skills` and its implementation control flow; direct static calls: Skill.

## Control flow

Control flow follows the functions and conditionals identified above. Static documentation does not claim behavior for reflective calls, subprocess contents, network responses, or model output without direct source evidence.

## Data flow

Inputs and outputs are passed through the symbols listed above; cross-module relationships are indexed in `.project_knowledge/symbol_call_graph.json`.

## Failure modes and security

Exceptions and policy-relevant handling are documented where their source symbols are present. Consult the security analysis and the cited lines before treating any boundary as complete.

## Tests and related files

Tests are mapped by static source relationships in `.project_knowledge/testing/test_map.json`. Internal dependency edges are listed in `.project_knowledge/symbol_call_graph.json`.
