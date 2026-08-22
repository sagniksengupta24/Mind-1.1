from __future__ import annotations

import difflib
import hashlib
import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, field
from enum import Enum
from pathlib import Path
from typing import Callable, Iterable, Sequence

from .completion import CompletionContract, VerificationEvidence, build_completion_contract
from .patch_review import review_patch
from .sandbox import SandboxConfig, SandboxedExecutor, SandboxError


class FailureCategory(str, Enum):
    SYNTAX_ERROR = "syntax_error"
    COMPILATION_ERROR = "compilation_error"
    FAILING_TEST = "failing_test"
    IMPORT_ERROR = "import_error"
    TYPE_ERROR = "type_error"
    LINT_ERROR = "lint_error"
    RUNTIME_EXCEPTION = "runtime_exception"
    TIMEOUT = "timeout"
    PERMISSION_DENIAL = "permission_denial"
    POLICY_VIOLATION = "policy_violation"
    ENVIRONMENT_DEPENDENCY_MISSING = "environment_dependency_missing"
    PARSER_FAILURE = "parser_failure"
    NO_PROGRESS_FAILURE = "no_progress_failure"
    UNRELATED_REGRESSION = "unrelated_regression"
    UNVERIFIABLE_RESULT = "unverifiable_result"


@dataclass(frozen=True)
class VerificationFailure:
    category: FailureCategory
    check_name: str
    output_summary: str
    exit_code: int | None = None

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["category"] = self.category.value
        return payload


@dataclass(frozen=True)
class RepairPlan:
    category: FailureCategory
    summary: str
    target_files: list[str]


@dataclass(frozen=True)
class RepairAttempt:
    index: int
    plan: RepairPlan
    files_changed: list[str]
    verification: list[VerificationEvidence]
    patch_review: list[dict[str, str]]
    rolled_back: bool = False
    rollback_files: list[str] = field(default_factory=list)
    no_progress: bool = False

    def to_dict(self) -> dict[str, object]:
        payload = asdict(self)
        payload["plan"]["category"] = self.plan.category.value
        payload["verification"] = [item.to_dict() for item in self.verification]
        return payload


@dataclass
class CorrectionState:
    objective: str
    repair_budget: int
    attempts: list[RepairAttempt] = field(default_factory=list)
    failure_history: list[VerificationFailure] = field(default_factory=list)
    patch_hashes: dict[str, int] = field(default_factory=dict)
    failure_hashes: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class CorrectionOutcome:
    contract: CompletionContract
    attempts: list[RepairAttempt]
    stopped_reason: str

    def to_dict(self) -> dict[str, object]:
        return {
            "contract": self.contract.to_dict(),
            "attempts": [attempt.to_dict() for attempt in self.attempts],
            "stopped_reason": self.stopped_reason,
        }


RepairExecutor = Callable[[Path, CorrectionState], str | None]


class WorkspaceSnapshot:
    def __init__(self, workspace: Path, files: dict[str, bytes]) -> None:
        self.workspace = workspace
        self.files = files

    @classmethod
    def capture(cls, workspace: Path) -> "WorkspaceSnapshot":
        root = workspace.resolve()
        files: dict[str, bytes] = {}
        for path in sorted(root.rglob("*")):
            if not path.is_file() or should_skip_snapshot_path(path, root):
                continue
            files[path.relative_to(root).as_posix()] = path.read_bytes()
        return cls(root, files)

    def changed_files(self, other: "WorkspaceSnapshot") -> list[str]:
        names = set(self.files) | set(other.files)
        return sorted(name for name in names if self.files.get(name) != other.files.get(name))

    def diff(self, other: "WorkspaceSnapshot") -> str:
        chunks: list[str] = []
        for name in self.changed_files(other):
            before = decode_for_diff(self.files.get(name, b""))
            after = decode_for_diff(other.files.get(name, b""))
            chunks.extend(
                difflib.unified_diff(
                    before.splitlines(keepends=True),
                    after.splitlines(keepends=True),
                    fromfile=f"a/{name}",
                    tofile=f"b/{name}",
                )
            )
        return "".join(chunks)

    def restore(self) -> list[str]:
        current = WorkspaceSnapshot.capture(self.workspace)
        changed = self.changed_files(current)
        for name in sorted(current.files):
            if name not in self.files:
                (self.workspace / name).unlink(missing_ok=True)
        for name, content in self.files.items():
            target = self.workspace / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
        remove_empty_dirs(self.workspace)
        return changed


def should_skip_snapshot_path(path: Path, root: Path) -> bool:
    rel_parts = path.relative_to(root).parts
    return any(part in {".git", ".mind01", "__pycache__", ".pytest_cache"} for part in rel_parts) or path.suffix in {".pyc", ".pyo", ".sqlite3", ".db"}


def remove_empty_dirs(root: Path) -> None:
    for path in sorted(root.rglob("*"), key=lambda item: len(item.parts), reverse=True):
        if path.is_dir() and not should_skip_snapshot_path(path, root):
            try:
                path.rmdir()
            except OSError:
                pass


def decode_for_diff(content: bytes) -> str:
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return "<binary content>\n"


def classify_failure(output: str, *, exit_code: int | None = None, timed_out: bool = False) -> FailureCategory:
    text = output.lower()
    if timed_out or "timed out" in text or "timeout" in text:
        return FailureCategory.TIMEOUT
    if "permission denied" in text or "operation not permitted" in text:
        return FailureCategory.PERMISSION_DENIAL
    if "policy" in text and "denied" in text:
        return FailureCategory.POLICY_VIOLATION
    if "syntaxerror" in text or "syntax error" in text or "invalid syntax" in text:
        return FailureCategory.SYNTAX_ERROR
    if "modulenotfounderror" in text or "importerror" in text or "no module named" in text:
        return FailureCategory.IMPORT_ERROR
    if "typeerror" in text or "mypy" in text:
        return FailureCategory.TYPE_ERROR
    if "assertionerror" in text or " failed" in text or "failures" in text or "pytest" in text:
        return FailureCategory.FAILING_TEST
    if "lint" in text or "ruff" in text or "flake8" in text:
        return FailureCategory.LINT_ERROR
    if "compile" in text or "compilation" in text or "gcc" in text or "clang" in text:
        return FailureCategory.COMPILATION_ERROR
    if "not found" in text or "is not installed" in text:
        return FailureCategory.ENVIRONMENT_DEPENDENCY_MISSING
    if exit_code not in (None, 0):
        return FailureCategory.RUNTIME_EXCEPTION
    return FailureCategory.UNVERIFIABLE_RESULT


def repair_plan_for_failure(failure: VerificationFailure, changed_files: list[str]) -> RepairPlan:
    if failure.category == FailureCategory.SYNTAX_ERROR:
        summary = "Inspect exact syntax location and repair the malformed file."
    elif failure.category == FailureCategory.FAILING_TEST:
        summary = "Inspect failing test output and repair the targeted behavior."
    elif failure.category == FailureCategory.ENVIRONMENT_DEPENDENCY_MISSING:
        summary = "Report blocked unless dependency installation is permitted."
    elif failure.category == FailureCategory.POLICY_VIOLATION:
        summary = "Stop; never bypass capability policy."
    elif failure.category == FailureCategory.TIMEOUT:
        summary = "Reduce scope and run a cheaper targeted check."
    else:
        summary = "Replan from deterministic verification evidence."
    return RepairPlan(failure.category, summary, changed_files)


def run_command_verification(workspace: Path, command: Sequence[str], *, timeout_seconds: int = 60, name: str = "command") -> VerificationEvidence:
    start = time.perf_counter()
    try:
        config = SandboxConfig(
            workspace=workspace,
            timeout_seconds=timeout_seconds,
            max_output_bytes=4000,
            allow_network=False,
        )
        executor = SandboxedExecutor(workspace, config)
        res = executor.execute(list(command), cwd=workspace, timeout_seconds=timeout_seconds)
        if res.timed_out:
            return VerificationEvidence(
                name=name,
                command=list(command),
                status="failed",
                exit_code=None,
                duration_seconds=round(time.perf_counter() - start, 3),
                output_summary=(res.output or "timed out")[-4000:],
                selected_reason="acceptance contract",
            )
        output = (res.output or "")[-4000:]
        return VerificationEvidence(
            name=name,
            command=list(command),
            status="passed" if res.returncode == 0 else "failed",
            exit_code=res.returncode,
            duration_seconds=round(time.perf_counter() - start, 3),
            output_summary=output,
            selected_reason="acceptance contract",
        )
    except SandboxError as exc:
        return VerificationEvidence(
            name=name,
            command=list(command),
            status="failed",
            exit_code=None,
            duration_seconds=round(time.perf_counter() - start, 3),
            output_summary=str(exc),
            selected_reason="acceptance contract",
        )
    except OSError as exc:
        return VerificationEvidence(
            name=name,
            command=list(command),
            status="unavailable",
            exit_code=None,
            duration_seconds=round(time.perf_counter() - start, 3),
            output_summary=str(exc),
            selected_reason="acceptance contract",
        )


class SelfCorrectionController:
    def __init__(self, workspace: Path, *, repair_budget: int = 2) -> None:
        self.workspace = workspace.resolve()
        self.repair_budget = max(0, repair_budget)

    def run(
        self,
        *,
        objective: str,
        repair_executors: Sequence[RepairExecutor],
        verification_commands: Sequence[Sequence[str]],
        expected_paths: list[str] | None = None,
    ) -> CorrectionOutcome:
        state = CorrectionState(objective=objective, repair_budget=self.repair_budget)
        last_verification: list[VerificationEvidence] = []
        last_review: list[dict[str, str]] = []
        last_changed: list[str] = []
        stopped_reason = "repair budget exhausted"
        max_attempts = min(len(repair_executors), self.repair_budget + 1)
        if max_attempts == 0:
            contract = build_completion_contract(objective=objective, requested_status="blocked", remaining_uncertainty=["no repair executor available"])
            return CorrectionOutcome(contract, [], "no repair executor available")

        for index in range(max_attempts):
            before = WorkspaceSnapshot.capture(self.workspace)
            executor = repair_executors[index]
            note = executor(self.workspace, state) or "repair attempted"
            after = WorkspaceSnapshot.capture(self.workspace)
            changed = before.changed_files(after)
            diff = before.diff(after)
            review = review_patch(diff_text=diff, changed_files=changed, expected_paths=expected_paths).to_dicts()
            verification = [
                run_command_verification(self.workspace, command, name=f"acceptance-{n}")
                for n, command in enumerate(verification_commands, start=1)
            ]
            last_verification = verification
            last_review = review
            last_changed = changed

            failure = first_failure(verification)
            if failure:
                state.failure_history.append(failure)
            plan = repair_plan_for_failure(failure or VerificationFailure(FailureCategory.UNVERIFIABLE_RESULT, "none", note), changed)
            patch_hash = sha256_text(diff)
            failure_hash = sha256_text((failure.output_summary if failure else "passed") + (failure.category.value if failure else ""))
            state.patch_hashes[patch_hash] = state.patch_hashes.get(patch_hash, 0) + 1
            state.failure_hashes[failure_hash] = state.failure_hashes.get(failure_hash, 0) + 1
            no_progress = bool(failure and (state.patch_hashes[patch_hash] > 1 or state.failure_hashes[failure_hash] > 1))
            blocking_review = any(item.get("severity") == "blocking" for item in review)
            policy_or_regression = bool(failure and failure.category in {FailureCategory.POLICY_VIOLATION, FailureCategory.UNRELATED_REGRESSION})
            rolled_back = False
            rollback_files: list[str] = []
            if failure or blocking_review or policy_or_regression:
                rollback_files = before.restore()
                rolled_back = True
            attempt = RepairAttempt(
                index=index + 1,
                plan=plan,
                files_changed=changed,
                verification=verification,
                patch_review=review,
                rolled_back=rolled_back,
                rollback_files=rollback_files,
                no_progress=no_progress,
            )
            state.attempts.append(attempt)
            if all(item.passed for item in verification) and not blocking_review:
                contract = build_completion_contract(
                    objective=objective,
                    requested_status="verified",
                    plan_summary=[note, "Run independent acceptance checks", "Review final patch"],
                    files_changed=changed,
                    verification=verification,
                    repair_attempts=index,
                    rollback_available=True,
                    patch_review=review,
                )
                return CorrectionOutcome(contract, state.attempts, "verified")
            if rolled_back:
                last_changed = []
            if no_progress:
                stopped_reason = "no-progress failure"
                break
            if failure and failure.category == FailureCategory.POLICY_VIOLATION:
                stopped_reason = "policy violation"
                break

        failure_category = state.failure_history[-1].category.value if state.failure_history else ""
        if stopped_reason == "no-progress failure":
            status = "failed"
            uncertainty = ["repeated identical patch or verification failure"]
        else:
            status = "failed" if last_verification else "unverified"
            uncertainty = [stopped_reason]
        contract = build_completion_contract(
            objective=objective,
            requested_status=status,
            plan_summary=["Execute bounded repair loop", "Stop when deterministic evidence does not pass"],
            files_changed=last_changed,
            verification=last_verification,
            repair_attempts=max(0, len(state.attempts) - 1),
            rollback_available=True,
            remaining_uncertainty=uncertainty,
            patch_review=last_review,
            failure_category=failure_category,
        )
        return CorrectionOutcome(contract, state.attempts, stopped_reason)


def first_failure(verification: Iterable[VerificationEvidence]) -> VerificationFailure | None:
    for item in verification:
        if item.status != "passed" or item.exit_code not in (0, None):
            return VerificationFailure(
                classify_failure(item.output_summary, exit_code=item.exit_code),
                item.name,
                item.output_summary,
                item.exit_code,
            )
    return None


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest()
