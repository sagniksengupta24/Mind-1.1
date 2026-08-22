from __future__ import annotations

import hashlib
import json
import re
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Iterable


class EvidenceType(str, Enum):
    SYNTAX = "syntax"
    SOURCE_STRUCTURE = "source_structure"
    IMPORTABILITY = "importability"
    SYMBOL_LOOKUP = "symbol_lookup"
    SIGNATURE = "signature"
    BEHAVIORAL_TEST = "behavioral_test"
    REGRESSION_TEST = "regression_test"
    INTEGRATION_TEST = "integration_test"
    STATIC_ANALYSIS = "static_analysis"
    SECURITY_CHECK = "security_check"
    ARTIFACT = "artifact"
    RECEIPT_INTEGRITY = "receipt_integrity"
    PATCH_REVIEW = "patch_review"
    POLICY = "policy"


@dataclass(frozen=True)
class EvidenceSemantics:
    evidence_type: EvidenceType
    proves: tuple[str, ...]
    does_not_prove: tuple[str, ...]


EVIDENCE_TAXONOMY: dict[EvidenceType, EvidenceSemantics] = {
    EvidenceType.SYNTAX: EvidenceSemantics(
        EvidenceType.SYNTAX,
        ("source parses or compiles under the named tool",),
        ("importability", "symbol presence", "correct behavior", "regression safety"),
    ),
    EvidenceType.SOURCE_STRUCTURE: EvidenceSemantics(
        EvidenceType.SOURCE_STRUCTURE,
        ("limited encoded structural properties hold",),
        ("importability", "correct behavior", "regression safety"),
    ),
    EvidenceType.IMPORTABILITY: EvidenceSemantics(
        EvidenceType.IMPORTABILITY,
        ("the checked module imports in the recorded environment",),
        ("requested symbol presence", "signature correctness", "correct behavior"),
    ),
    EvidenceType.SYMBOL_LOOKUP: EvidenceSemantics(
        EvidenceType.SYMBOL_LOOKUP,
        ("the requested symbol exists in executable source",),
        ("signature correctness", "correct behavior", "regression safety"),
    ),
    EvidenceType.SIGNATURE: EvidenceSemantics(
        EvidenceType.SIGNATURE,
        ("the requested callable signature matches the encoded contract",),
        ("correct behavior", "regression safety"),
    ),
    EvidenceType.BEHAVIORAL_TEST: EvidenceSemantics(
        EvidenceType.BEHAVIORAL_TEST,
        ("the behavior exercised by the named acceptance test passed",),
        ("untested behavior", "general correctness"),
    ),
    EvidenceType.REGRESSION_TEST: EvidenceSemantics(
        EvidenceType.REGRESSION_TEST,
        ("the recorded regression suite passed",),
        ("behavior absent from that suite", "general correctness"),
    ),
    EvidenceType.INTEGRATION_TEST: EvidenceSemantics(
        EvidenceType.INTEGRATION_TEST,
        ("the tested component integration passed",),
        ("untested integrations", "general correctness"),
    ),
    EvidenceType.STATIC_ANALYSIS: EvidenceSemantics(
        EvidenceType.STATIC_ANALYSIS,
        ("the configured static-analysis rules passed",),
        ("runtime behavior", "absence of unencoded defects"),
    ),
    EvidenceType.SECURITY_CHECK: EvidenceSemantics(
        EvidenceType.SECURITY_CHECK,
        ("the configured security checks passed",),
        ("absence of vulnerabilities outside the encoded checks",),
    ),
    EvidenceType.ARTIFACT: EvidenceSemantics(
        EvidenceType.ARTIFACT,
        ("the expected artifact exists with the recorded identity",),
        ("artifact correctness", "correct behavior"),
    ),
    EvidenceType.RECEIPT_INTEGRITY: EvidenceSemantics(
        EvidenceType.RECEIPT_INTEGRITY,
        ("the final file identity matches its mutation receipt",),
        ("source correctness", "correct behavior"),
    ),
    EvidenceType.PATCH_REVIEW: EvidenceSemantics(
        EvidenceType.PATCH_REVIEW,
        ("the configured high-signal patch rules found no blocking issue",),
        ("correct behavior", "absence of all security defects"),
    ),
    EvidenceType.POLICY: EvidenceSemantics(
        EvidenceType.POLICY,
        ("the recorded action satisfied the named policy decision",),
        ("source correctness", "correct behavior"),
    ),
}


@dataclass(frozen=True)
class TaskRequirement:
    id: str
    description: str
    required_evidence: tuple[EvidenceType, ...]
    mandatory: bool = True

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["required_evidence"] = [item.value for item in self.required_evidence]
        return payload


@dataclass(frozen=True)
class TaskContract:
    schema_version: str
    contract_id: str
    normalized_goal: str
    task_type: str
    target_scope: tuple[str, ...]
    forbidden_scope: tuple[str, ...]
    expected_artifacts: tuple[str, ...]
    required_symbols: tuple[str, ...]
    required_signatures: dict[str, tuple[str, ...]]
    behavioral_requirements: tuple[str, ...]
    regression_requirements: tuple[str, ...]
    security_requirements: tuple[str, ...]
    requirements: tuple[TaskRequirement, ...]
    rollback_conditions: tuple[str, ...]
    completion_criteria: tuple[str, ...]
    mutation_required: bool
    baseline_state_hash: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["requirements"] = [item.to_dict() for item in self.requirements]
        payload["required_signatures"] = {
            name: list(arguments) for name, arguments in self.required_signatures.items()
        }
        return payload

    @classmethod
    def from_dict(cls, payload: dict[str, Any]) -> "TaskContract":
        requirements = tuple(
            TaskRequirement(
                id=str(item["id"]),
                description=str(item["description"]),
                required_evidence=tuple(EvidenceType(value) for value in item.get("required_evidence", [])),
                mandatory=bool(item.get("mandatory", True)),
            )
            for item in payload.get("requirements", [])
        )
        return cls(
            schema_version=str(payload.get("schema_version", "1.0")),
            contract_id=str(payload.get("contract_id", "")),
            normalized_goal=str(payload.get("normalized_goal", "")),
            task_type=str(payload.get("task_type", "general")),
            target_scope=tuple(str(item) for item in payload.get("target_scope", [])),
            forbidden_scope=tuple(str(item) for item in payload.get("forbidden_scope", [])),
            expected_artifacts=tuple(str(item) for item in payload.get("expected_artifacts", [])),
            required_symbols=tuple(str(item) for item in payload.get("required_symbols", [])),
            required_signatures={
                str(name): tuple(str(item) for item in arguments)
                for name, arguments in payload.get("required_signatures", {}).items()
            },
            behavioral_requirements=tuple(str(item) for item in payload.get("behavioral_requirements", [])),
            regression_requirements=tuple(str(item) for item in payload.get("regression_requirements", [])),
            security_requirements=tuple(str(item) for item in payload.get("security_requirements", [])),
            requirements=requirements,
            rollback_conditions=tuple(str(item) for item in payload.get("rollback_conditions", [])),
            completion_criteria=tuple(str(item) for item in payload.get("completion_criteria", [])),
            mutation_required=bool(payload.get("mutation_required", False)),
            baseline_state_hash=str(payload.get("baseline_state_hash", "")),
            metadata=dict(payload.get("metadata", {})),
        )

    def sha256(self) -> str:
        serialized = json.dumps(self.to_dict(), sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def mandatory_requirements(self) -> tuple[TaskRequirement, ...]:
        return tuple(item for item in self.requirements if item.mandatory)


_FILE_RE = re.compile(
    r"(?:^|\s|[`'\"])([\w./-]+\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md))(?:\s|$|[`'\",.:])",
    re.IGNORECASE,
)

# "in eval_suites/: dummy_a_1.py and dummy_b_1.py" — the colon after a
# directory splits the token, so the plain _FILE_RE loses the directory prefix
# and the resulting contract scope does not match the written path.  Glue the
# directory onto every listed file before extraction.
_DIRECTORY_FILE_LIST_RE = re.compile(
    r"\b([\w./-]+)/:\s*"
    r"([\w./-]+\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md)"
    r"(?:\s+and\s+[\w./-]+\.(?:py|js|jsx|ts|tsx|c|cc|cpp|h|hpp|v|sv|json|toml|ya?ml|md))*)",
    re.IGNORECASE,
)


def _expand_directory_file_lists(normalized: str) -> str:
    """Prefix every file in a `dir/: a.py and b.py` list with the directory."""

    def _replace(match: re.Match[str]) -> str:
        directory = match.group(1).rstrip("/")
        files = re.split(r"\s+and\s+", match.group(2), flags=re.IGNORECASE)
        glued = " and ".join(
            f"{directory}/{name}" if "/" not in name else name for name in files
        )
        return f"{directory}: {glued}"

    return _DIRECTORY_FILE_LIST_RE.sub(_replace, normalized)
_CALLABLE_PATTERNS = (
    re.compile(r"\b(?:def|function)\s+([A-Za-z_]\w*)\s*(?:\(([^)]*)\))?", re.IGNORECASE),
    re.compile(
        r"\b(?:implement|add)\s+(?:the\s+)?(?:function|method|callable)\s+"
        r"([A-Za-z_]\w*)\s*(?:\(([^)]*)\))?",
        re.IGNORECASE,
    ),
    re.compile(
        r"\b(?:implement|add)\s+(?:the\s+)?([A-Za-z_]\w*)\s*\(([^)]*)\)",
        re.IGNORECASE,
    ),
)


def build_task_contract(
    goal: str,
    *,
    mutation_required: bool,
    specialist: str = "general_reasoning",
    baseline_state_hash: str = "",
) -> TaskContract:
    """Build a conservative contract from general task signals.

    Missing requirements reduce the chance of verification; they never grant it. The
    builder intentionally does not contain benchmark phrases or expected answers.
    """

    normalized = " ".join(goal.strip().split())
    expanded = _expand_directory_file_lists(normalized)
    lowered = normalized.lower()
    target_scope = tuple(dict.fromkeys(match.group(1) for match in _FILE_RE.finditer(expanded)))
    symbols: list[str] = []
    signatures: dict[str, tuple[str, ...]] = {}
    for pattern in _CALLABLE_PATTERNS:
        for match in pattern.finditer(normalized):
            symbol = match.group(1)
            if symbol not in symbols:
                symbols.append(symbol)
            raw_args = match.group(2)
            if raw_args is not None:
                arguments = tuple(
                    part.strip().split(":", 1)[0].split("=", 1)[0].strip()
                    for part in raw_args.split(",")
                    if part.strip()
                )
                signatures[symbol] = arguments

    syntax_only = bool(
        re.search(r"\b(syntax error|syntax repair|compilation error|compile error|make .* compile)\b", lowered)
    )
    behavioral = not syntax_only and bool(
        re.search(
            r"\b(implement|fix|repair|bug|feature|behavior|behaviour|return|calculate|convert|normalize|parse|validate|endpoint|migration|refactor)\b",
            lowered,
        )
    )
    security = bool(re.search(r"\b(security|auth|authorization|token|secret|permission|ssrf|injection|traversal)\b", lowered))
    task_type = "read_only"
    if mutation_required:
        task_type = "implement_function" if symbols else "behavioral_mutation" if behavioral else "scoped_mutation"

    requirements: list[TaskRequirement] = []
    if mutation_required:
        requirements.append(
            TaskRequirement("R-SCOPE", "Only authorized target scope changed", (EvidenceType.PATCH_REVIEW,))
        )
        requirements.append(
            TaskRequirement("R-RECEIPT", "Final workspace state matches mutation receipts", (EvidenceType.RECEIPT_INTEGRITY,))
        )
    python_target = any(path.lower().endswith(".py") for path in target_scope) or "python" in lowered
    if mutation_required and python_target:
        requirements.extend(
            [
                TaskRequirement("R-SYNTAX", "Changed Python source is syntactically valid", (EvidenceType.SYNTAX,)),
                TaskRequirement("R-STRUCTURE", "Changed Python definitions are executable source", (EvidenceType.SOURCE_STRUCTURE,)),
                TaskRequirement("R-IMPORT", "Changed Python source is importable", (EvidenceType.IMPORTABILITY,)),
            ]
        )
    for index, symbol in enumerate(symbols, start=1):
        requirements.append(
            TaskRequirement(f"R-SYMBOL-{index}", f"Required symbol {symbol} exists in executable source", (EvidenceType.SYMBOL_LOOKUP,))
        )
        if symbol in signatures:
            requirements.append(
                TaskRequirement(f"R-SIGNATURE-{index}", f"Required symbol {symbol} has the requested signature", (EvidenceType.SIGNATURE,))
            )
    if mutation_required and behavioral:
        requirements.append(
            TaskRequirement("R-BEHAVIOR", "Requested behavior passes independent acceptance", (EvidenceType.BEHAVIORAL_TEST,))
        )
        requirements.append(
            TaskRequirement("R-REGRESSION", "Existing behavior passes regression checks", (EvidenceType.REGRESSION_TEST,))
        )
    if mutation_required and security:
        requirements.append(
            TaskRequirement("R-SECURITY", "Security-sensitive requirements pass configured checks", (EvidenceType.SECURITY_CHECK,))
        )
    if mutation_required and not requirements:
        requirements.append(
            TaskRequirement("R-ARTIFACT", "Requested artifact exists with recorded identity", (EvidenceType.ARTIFACT,))
        )

    forbidden_scope = (".git", ".mind01")
    identity = json.dumps(
        {
            "goal": normalized,
            "mutation_required": mutation_required,
            "specialist": specialist,
            "baseline_state_hash": baseline_state_hash,
            "target_scope": target_scope,
            "symbols": symbols,
            "signatures": signatures,
        },
        sort_keys=True,
        separators=(",", ":"),
    )
    return TaskContract(
        schema_version="1.0",
        contract_id=f"contract-{hashlib.sha256(identity.encode('utf-8')).hexdigest()[:24]}",
        normalized_goal=normalized,
        task_type=task_type,
        target_scope=target_scope,
        forbidden_scope=forbidden_scope,
        expected_artifacts=target_scope,
        required_symbols=tuple(symbols),
        required_signatures=signatures,
        behavioral_requirements=(normalized,) if mutation_required and behavioral else (),
        regression_requirements=("Preserve existing project behavior",) if mutation_required and behavioral else (),
        security_requirements=("Pass configured security checks",) if mutation_required and security else (),
        requirements=tuple(requirements),
        rollback_conditions=(
            "blocking verification failure",
            "blocking patch-review finding",
            "unauthorized mutation",
            "receipt or final-state mismatch",
        ),
        completion_criteria=("Every mandatory requirement has current, passing, task-relevant evidence",),
        mutation_required=mutation_required,
        baseline_state_hash=baseline_state_hash,
        metadata={"specialist": specialist},
    )


def requirement_ids_for_evidence(
    contract: TaskContract | None,
    evidence_type: EvidenceType | str,
) -> tuple[str, ...]:
    if contract is None:
        return ()
    kind = evidence_type if isinstance(evidence_type, EvidenceType) else EvidenceType(evidence_type)
    return tuple(
        requirement.id for requirement in contract.requirements if kind in requirement.required_evidence
    )


def state_hash(workspace: Path, paths: Iterable[str]) -> str:
    digest = hashlib.sha256()
    root = workspace.resolve()
    for relative in sorted(set(paths)):
        target = (root / relative).resolve()
        digest.update(relative.encode("utf-8", errors="replace"))
        if target.exists() and target.is_file() and (target == root or root in target.parents):
            digest.update(target.read_bytes())
        else:
            digest.update(b"<missing>")
    return digest.hexdigest()
