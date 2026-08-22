from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import PurePosixPath


@dataclass(frozen=True)
class PatchFinding:
    severity: str
    code: str
    message: str
    path: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)


@dataclass(frozen=True)
class PatchReviewResult:
    findings: list[PatchFinding]

    @property
    def blocking(self) -> bool:
        return any(item.severity == "blocking" for item in self.findings)

    def to_dicts(self) -> list[dict[str, str]]:
        return [item.to_dict() for item in self.findings]


def review_patch(
    *,
    diff_text: str,
    changed_files: list[str],
    expected_paths: list[str] | None = None,
    protected_paths: list[str] | None = None,
) -> PatchReviewResult:
    findings: list[PatchFinding] = []
    protected = [normalise_path(path) for path in protected_paths or [".mind01", ".git"]]
    expected = [normalise_path(path) for path in expected_paths or []]
    changed = [normalise_path(path) for path in changed_files]

    for path in changed:
        if any(path == protected_path or path.startswith(protected_path + "/") for protected_path in protected):
            findings.append(PatchFinding("blocking", "protected-file", "protected runtime or VCS path was modified", path))
        if any(part in {"__pycache__", ".pytest_cache"} for part in PurePosixPath(path).parts) or path.endswith((".pyc", ".sqlite3", ".db")):
            findings.append(PatchFinding("blocking", "generated-runtime-data", "generated runtime data was modified", path))
        if expected and not any(path == item or path.startswith(item.rstrip("/") + "/") for item in expected):
            findings.append(PatchFinding("warning", "unexpected-scope", "changed file is outside the expected scope", path))

    if re.search(r"^--- a/tests/.+\n\+\+\+ /dev/null", diff_text, re.MULTILINE):
        findings.append(PatchFinding("blocking", "tests-deleted", "test file deletion cannot be accepted as verification"))

    removed_assertions = [line for line in diff_text.splitlines() if line.startswith("-") and re.search(r"\b(assert|pytest\.raises|expect\(|should|must)\b", line)]
    added_assertions = [line for line in diff_text.splitlines() if line.startswith("+") and re.search(r"\b(assert|pytest\.raises|expect\()\b", line)]
    if removed_assertions and len(added_assertions) < len(removed_assertions):
        findings.append(PatchFinding("blocking", "assertions-weakened", "assertions appear to have been removed or weakened"))

    added_lines = [line[1:].strip() for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++")]
    for line in added_lines:
        lowered = line.lower()
        if re.search(r"except\s+(exception|baseexception)?\s*:\s*(pass)?$", lowered) or lowered in {"except:", "except: pass"}:
            findings.append(PatchFinding("blocking", "broad-exception-swallow", "broad exception swallowing was introduced"))
        if "chmod" in lowered and ("777" in lowered or "+w" in lowered):
            findings.append(PatchFinding("blocking", "unsafe-permission-expansion", "unsafe permission expansion was introduced"))
        if re.search(r"\b(api[_-]?key|secret|password|token)\b\s*=\s*['\"]", lowered):
            findings.append(PatchFinding("blocking", "secret-inserted", "possible hardcoded secret was inserted"))
        if re.search(r"(^|\s)(print|console\.log)\(", line):
            findings.append(PatchFinding("warning", "debug-print", "debug print/log statement remains"))

    changed_line_count = sum(1 for line in diff_text.splitlines() if line[:1] in {"+", "-"} and not line.startswith(("+++", "---")))
    if changed_line_count > 500:
        findings.append(PatchFinding("warning", "large-rewrite", "large rewrite detected; review for unrelated churn"))
    if not findings:
        findings.append(PatchFinding("info", "review-clean", "patch review found no high-signal issues"))
    return PatchReviewResult(findings)


def normalise_path(path: str) -> str:
    return path.replace("\\", "/").strip("/")
