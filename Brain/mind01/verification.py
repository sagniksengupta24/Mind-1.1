from __future__ import annotations

import ast
import json
import re
import shutil
import subprocess
import sys
import time
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Sequence

from .task_contract import (
    EVIDENCE_TAXONOMY,
    EvidenceType,
    TaskContract,
    requirement_ids_for_evidence,
)
from .sandbox import SandboxConfig, SandboxedExecutor, SandboxError


@dataclass(frozen=True)
class VerificationResult:
    check: str
    status: str
    duration_ms: int
    output_summary: str
    failure_category: str = ""
    confidence: float = 0.0
    blocking: bool = False
    evidence_type: str = EvidenceType.ARTIFACT.value
    requirement_ids: tuple[str, ...] = ()
    proven_properties: tuple[str, ...] = ()
    unproven_properties: tuple[str, ...] = ()
    state_hash: str = ""
    observed_after_mutation: bool = True
    command: tuple[str, ...] = ()
    skipped: bool = False
    source: str = "verification_engine"

    def to_dict(self) -> dict:
        return asdict(self)


class VerificationEngine:
    def __init__(self, workspace: Path, timeout_seconds: int = 60, output_limit: int = 4000) -> None:
        self.workspace = workspace.resolve()
        self.timeout_seconds = timeout_seconds
        self.output_limit = output_limit

    def verify_paths(
        self,
        paths: Sequence[str],
        full_project: bool = False,
        *,
        contract: TaskContract | None = None,
        mutation_state_hash: str = "",
    ) -> list[VerificationResult]:
        suffixes = {Path(path).suffix.lower() for path in paths}
        results: list[VerificationResult] = []
        for path in paths:
            target = (self.workspace / path).resolve()
            if self.workspace != target and self.workspace not in target.parents:
                results.append(VerificationResult("workspace-boundary", "failed", 0, f"Path escapes workspace: {path}", "policy", 1.0, True))
                continue
            if target.suffix.lower() == ".json" and target.exists():
                results.append(self._parse_json(target))
        if suffixes & {".py"}:
            for path in paths:
                target = (self.workspace / path).resolve()
                if target.suffix.lower() == ".py" and target.exists():
                    results.append(self._python_executable_structure(target))
            results.append(self._run((sys.executable, "-m", "compileall", "-q", *paths), "python-compile", blocking=True))
            if contract is not None:
                results.extend(self._python_symbol_contract(paths, contract))
                if any(
                    EvidenceType.IMPORTABILITY in requirement.required_evidence
                    for requirement in contract.mandatory_requirements()
                ):
                    if full_project:
                        results.extend(self._python_imports(paths))
                    else:
                        results.append(
                            VerificationResult(
                                "python-import",
                                "unavailable",
                                0,
                                "Import verification requires authorized project execution.",
                                "authorization_required",
                                0.0,
                                False,
                                evidence_type=EvidenceType.IMPORTABILITY.value,
                                skipped=True,
                            )
                        )
            if full_project and (self.workspace / "tests").exists():
                results.append(self._run((sys.executable, "-m", "pytest", "-q"), "pytest", blocking=True))
        if suffixes & {".v", ".sv"}:
            tool = shutil.which("iverilog")
            if tool:
                results.append(self._run((tool, "-g2012", "-tnull", *paths), "iverilog-syntax", blocking=True))
            else:
                results.append(VerificationResult("iverilog-syntax", "unavailable", 0, "iverilog is not installed", "tool_unavailable", 0.0, False))
        if suffixes & {".c", ".cc", ".cpp"}:
            compiler = shutil.which("clang++") or shutil.which("g++")
            if compiler:
                results.append(self._run((compiler, "-fsyntax-only", "-Wall", "-Wextra", *paths), "cpp-syntax", blocking=True))
            else:
                results.append(VerificationResult("cpp-syntax", "unavailable", 0, "C++ compiler is not installed", "tool_unavailable", 0.0, False))
        if suffixes & {".js", ".jsx", ".ts", ".tsx"} and full_project:
            package = self.workspace / "package.json"
            if package.exists() and shutil.which("npm"):
                results.append(self._run(("npm", "test", "--", "--runInBand"), "javascript-tests", blocking=False))
        if not results:
            results.append(VerificationResult("file-type-verifier", "unavailable", 0, "No deterministic verifier selected for these paths", "no_adapter", 0.0, False))
        return [self._classify_evidence(item, contract, mutation_state_hash) for item in results]

    def _parse_json(self, path: Path) -> VerificationResult:
        start = time.perf_counter()
        try:
            json.loads(path.read_text(encoding="utf-8"))
            return VerificationResult("json-parse", "passed", int((time.perf_counter() - start) * 1000), str(path.relative_to(self.workspace)), confidence=1.0)
        except Exception as exc:
            return VerificationResult("json-parse", "failed", int((time.perf_counter() - start) * 1000), str(exc)[: self.output_limit], "syntax", 1.0, True)

    def _python_executable_structure(self, path: Path) -> VerificationResult:
        start = time.perf_counter()
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        except (OSError, UnicodeDecodeError, SyntaxError) as exc:
            return VerificationResult(
                "python-executable-structure",
                "failed",
                int((time.perf_counter() - start) * 1000),
                str(exc)[: self.output_limit],
                "syntax",
                1.0,
                True,
            )
        trapped: list[int] = []
        definition_pattern = re.compile(r"(?m)^\s*(?:async\s+def|def|class)\s+[A-Za-z_]\w*\s*(?:\(|:)")
        for node in ast.walk(tree):
            if isinstance(node, ast.Constant) and isinstance(node.value, str) and definition_pattern.search(node.value):
                trapped.append(getattr(node, "lineno", 0))
        if trapped:
            return VerificationResult(
                "python-executable-structure",
                "failed",
                int((time.perf_counter() - start) * 1000),
                f"Possible function/class definition trapped in a string literal at line(s): {', '.join(map(str, trapped))}",
                "non_executable_source",
                0.98,
                True,
            )
        return VerificationResult(
            "python-executable-structure",
            "passed",
            int((time.perf_counter() - start) * 1000),
            str(path.relative_to(self.workspace)),
            confidence=0.95,
        )

    def _python_symbol_contract(self, paths: Sequence[str], contract: TaskContract) -> list[VerificationResult]:
        if not contract.required_symbols:
            return []
        started = time.perf_counter()
        definitions: dict[str, ast.FunctionDef | ast.AsyncFunctionDef | ast.ClassDef] = {}
        for relative in paths:
            target = (self.workspace / relative).resolve()
            if target.suffix.lower() != ".py" or not target.exists():
                continue
            try:
                tree = ast.parse(target.read_text(encoding="utf-8"), filename=str(target))
            except (OSError, UnicodeDecodeError, SyntaxError):
                continue
            for node in tree.body:
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    definitions[node.name] = node
        results: list[VerificationResult] = []
        for symbol in contract.required_symbols:
            node = definitions.get(symbol)
            found = node is not None
            results.append(
                VerificationResult(
                    check=f"python-symbol:{symbol}",
                    status="passed" if found else "failed",
                    duration_ms=int((time.perf_counter() - started) * 1000),
                    output_summary=f"Executable top-level symbol `{symbol}` {'found' if found else 'not found'}.",
                    failure_category="" if found else "missing_symbol",
                    confidence=0.99,
                    blocking=not found,
                    evidence_type=EvidenceType.SYMBOL_LOOKUP.value,
                )
            )
            expected = contract.required_signatures.get(symbol)
            if expected is not None:
                actual: tuple[str, ...] = ()
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    actual = tuple(argument.arg for argument in [*node.args.posonlyargs, *node.args.args])
                signature_ok = found and actual == expected
                results.append(
                    VerificationResult(
                        check=f"python-signature:{symbol}",
                        status="passed" if signature_ok else "failed",
                        duration_ms=int((time.perf_counter() - started) * 1000),
                        output_summary=f"Expected {symbol}{expected}; observed {symbol}{actual}.",
                        failure_category="" if signature_ok else "wrong_signature",
                        confidence=0.99,
                        blocking=not signature_ok,
                        evidence_type=EvidenceType.SIGNATURE.value,
                    )
                )
        return results

    def _python_imports(self, paths: Sequence[str]) -> list[VerificationResult]:
        results: list[VerificationResult] = []
        for relative in paths:
            target = (self.workspace / relative).resolve()
            if target.suffix.lower() != ".py" or not target.exists():
                continue
            script = (
                "import importlib.util, pathlib; "
                f"p=pathlib.Path({str(target)!r}); "
                "s=importlib.util.spec_from_file_location('_mind_verify_module', p); "
                "m=importlib.util.module_from_spec(s); s.loader.exec_module(m)"
            )
            results.append(
                self._run(
                    (sys.executable, "-c", script),
                    f"python-import:{relative}",
                    blocking=True,
                )
            )
        return results

    def _classify_evidence(
        self,
        result: VerificationResult,
        contract: TaskContract | None,
        mutation_state_hash: str,
    ) -> VerificationResult:
        kind = _evidence_type_for_check(result.check, result.evidence_type)
        semantics = EVIDENCE_TAXONOMY[kind]
        return replace(
            result,
            evidence_type=kind.value,
            requirement_ids=requirement_ids_for_evidence(contract, kind),
            proven_properties=result.proven_properties or semantics.proves,
            unproven_properties=result.unproven_properties or semantics.does_not_prove,
            state_hash=mutation_state_hash or result.state_hash,
        )

    def _run(self, argv: tuple[str, ...], name: str, blocking: bool) -> VerificationResult:
        start = time.perf_counter()
        try:
            config = SandboxConfig(
                workspace=self.workspace,
                timeout_seconds=self.timeout_seconds,
                max_output_bytes=self.output_limit,
                allow_network=False,
            )
            executor = SandboxedExecutor(self.workspace, config)
            res = executor.execute(list(argv), cwd=self.workspace, timeout_seconds=self.timeout_seconds)
            if res.timed_out:
                output = (res.output or "")[-self.output_limit:]
                return VerificationResult(name, "failed", int((time.perf_counter() - start) * 1000), output or "timed out", "timeout", 0.9, blocking, command=argv)
            output = (res.output or "")[-self.output_limit:]
            status = "passed" if res.returncode == 0 else "failed"
            return VerificationResult(name, status, int((time.perf_counter() - start) * 1000), output, "command_failed" if res.returncode else "", 0.95, blocking and res.returncode != 0, command=argv)
        except SandboxError as exc:
            return VerificationResult(name, "unavailable", int((time.perf_counter() - start) * 1000), str(exc), "sandbox_error", 0.0, False, command=argv)
        except OSError as exc:
            return VerificationResult(name, "unavailable", int((time.perf_counter() - start) * 1000), str(exc), "tool_unavailable", 0.0, False, command=argv)


def _evidence_type_for_check(check: str, declared: str) -> EvidenceType:
    if declared and declared != EvidenceType.ARTIFACT.value:
        return EvidenceType(declared)
    if check == "python-executable-structure":
        return EvidenceType.SOURCE_STRUCTURE
    if check.startswith("python-symbol:"):
        return EvidenceType.SYMBOL_LOOKUP
    if check.startswith("python-signature:"):
        return EvidenceType.SIGNATURE
    if check.startswith("python-import:") or check == "python-import":
        return EvidenceType.IMPORTABILITY
    if check in {"python-compile", "json-parse", "cpp-syntax", "iverilog-syntax"}:
        return EvidenceType.SYNTAX
    if check == "pytest" or check == "javascript-tests":
        return EvidenceType.REGRESSION_TEST
    if check == "workspace-boundary":
        return EvidenceType.POLICY
    return EvidenceType.ARTIFACT
