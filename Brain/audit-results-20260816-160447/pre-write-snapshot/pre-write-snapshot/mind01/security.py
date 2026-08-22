from __future__ import annotations

import re


SECRET_PATTERNS = [
    re.compile(r"(?i)(api[_-]?key|secret|token|password)\s*[:=]\s*['\"]?([^\s'\";,]+)"),
    re.compile(r"sk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----", re.DOTALL),
]


def redact_secrets(text: str) -> str:
    redacted = text
    for pattern in SECRET_PATTERNS:
        if pattern.groups >= 2:
            redacted = pattern.sub(lambda match: f"{match.group(1)}=[REDACTED]", redacted)
        else:
            redacted = pattern.sub("[REDACTED_SECRET]", redacted)
    return redacted
