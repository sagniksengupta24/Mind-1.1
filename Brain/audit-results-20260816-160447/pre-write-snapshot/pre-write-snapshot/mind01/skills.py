from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Skill:
    name: str
    description: str
    specialists: tuple[str, ...]
    permitted_tools: tuple[str, ...]
    procedure: tuple[str, ...]
    verification: tuple[str, ...]
    failure_conditions: tuple[str, ...]


class SkillRegistry:
    def __init__(self) -> None:
        self._skills = {skill.name: skill for skill in default_skills()}

    def get(self, name: str) -> Skill:
        return self._skills[name]

    def select(self, specialist: str) -> tuple[Skill, ...]:
        selected = tuple(skill for skill in self._skills.values() if specialist in skill.specialists)
        if selected:
            return selected
        return (self._skills["repository_analysis"],) if specialist == "repository_understanding" else ()

    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._skills))


def default_skills() -> tuple[Skill, ...]:
    read = ("project_map", "list_files", "read_file", "search_code", "search_symbols", "file_summary")
    edit = read + ("propose_write_file", "propose_edit_file", "write_file", "edit_file")
    return (
        Skill("repository_analysis", "Map and explain a repository from inspected evidence.", ("repository_understanding",), read, ("map", "locate", "read", "synthesize"), ("evidence coverage",), ("answering before inspection",)),
        Skill("safe_code_edit", "Perform minimal, policy-compliant repository edits.", ("code_modification",), edit, ("inspect", "plan", "edit", "verify"), ("file-type checks", "tests"), ("unplanned mutation", "unverified success claim")),
        Skill("add_feature", "Implement a bounded feature from explicit acceptance criteria.", ("code_modification",), edit + ("run_command",), ("inspect contracts", "plan", "implement", "test"), ("targeted tests", "project checks"), ("unclear acceptance criteria", "unverified behavior")),
        Skill("refactor_code", "Improve structure without changing externally observable behavior.", ("code_modification",), edit + ("run_command",), ("capture behavior", "refactor", "compare", "test"), ("regression tests",), ("behavior drift",)),
        Skill("write_tests", "Add focused behavioral tests for a validated requirement or bug.", ("testing_verification", "debugging"), edit + ("run_command",), ("identify invariant", "write test", "run targeted suite"), ("targeted tests",), ("test does not exercise behavior",)),
        Skill("debug_failing_test", "Reproduce, localize, fix, and retest a failure.", ("debugging",), edit + ("run_command",), ("reproduce", "localize", "fix", "targeted retest"), ("targeted tests",), ("cannot reproduce",)),
        Skill("python_verification", "Validate Python changes with syntax and tests.", ("python_verification", "testing_verification"), read + ("run_command",), ("discover", "compile", "test"), ("compileall", "pytest"), ("tool unavailable",)),
        Skill("api_security_review", "Review trust boundaries and authorization invariants.", ("security_review",), read + ("run_command",), ("map entry points", "trace data flow", "test invariants"), ("security regression tests",), ("insufficient evidence",)),
        Skill("verilog_verification", "Inspect and verify RTL/testbench code.", ("verilog_verification",), edit + ("run_command", "search_docs"), ("classify block", "inspect", "edit", "compile/simulate"), ("iverilog/verilator",), ("tool unavailable",)),
        Skill("documentation_retrieval", "Retrieve indexed documentation with provenance.", ("documentation_rag",), ("search_docs", "read_file"), ("search", "check freshness", "answer with source"), ("freshness",), ("stale source",)),
    )
