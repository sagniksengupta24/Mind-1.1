"""Comprehensive secret detection and redaction for Mind1.1 runtime.

Redacts API keys, cloud provider tokens, JWTs, private keys, high-entropy secrets,
and concatenated/multi-line key assignments across all runtime outbound data paths.
"""

from __future__ import annotations

import math
import re
from typing import Any, Dict, List, Union


# Explicit Known Secret Patterns
AWS_ACCESS_KEY_PATTERN = re.compile(r"\b(AKIA|ASIA|ABIA|ACCA)[0-9A-Z]{16}\b")
AWS_SECRET_KEY_PATTERN = re.compile(
    r"(?i)(?:aws_secret_access_key|aws_secret_key|secret_key|aws_session_token)\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{30,80})['\"]?"
)
JWT_PATTERN = re.compile(
    r"\beyJ[A-Za-z0-9_-]{10,}\.eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]+\b"
)
GCP_API_KEY_PATTERN = re.compile(r"\bAIza[0-9A-Za-z_-]{30,40}\b")
GCP_SERVICE_ACCOUNT_PATTERN = re.compile(
    r'(?i)"private_key"\s*:\s*"-----BEGIN [A-Z ]*PRIVATE KEY-----[^"]+"'
)
AZURE_SECRET_PATTERN = re.compile(
    r"(?i)(?:AccountKey|SharedAccessSignature|azure_secret)\s*[:=]\s*['\"]?([A-Za-z0-9/+=]{32,100})['\"]?"
)
DEVELOPER_TOKENS_PATTERN = re.compile(
    r"\b((?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9_]{36,255}|github_pat_[A-Za-z0-9_]{82}|hf_[A-Za-z0-9]{34,}|xox[baprs]-[0-9A-Za-z-]{20,}|sk-ant-api[0-9]{2}-[A-Za-z0-9_-]{40,}|sk-ant-[A-Za-z0-9_-]{20,}|sk-[A-Za-z0-9_-]{20,}|openrouter-[A-Za-z0-9_-]{20,})\b"
)
PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.DOTALL,
)
PGP_PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN PGP PRIVATE KEY BLOCK-----.*?-----END PGP PRIVATE KEY BLOCK-----",
    re.DOTALL,
)
SPLIT_CONCAT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password)\s*=\s*['\"]([a-zA-Z0-9_\-]{6,})['\"]\s*\+\s*['\"]([a-zA-Z0-9_\-]{6,})['\"]"
)
MULTILINE_CONCAT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|secret|token|password)\s*=\s*\(\s*['\"]([a-zA-Z0-9_\-]{6,})['\"]\s*[\r\n]+\s*['\"]([a-zA-Z0-9_\-]{6,})['\"]\s*\)"
)
GENERIC_ASSIGNMENT_PATTERN = re.compile(
    r"(?i)\b(api[_-]?key|secret[_-]?key|secret|token|access[_-]?token|auth[_-]?token|bearer|client[_-]?secret|password|passwd|private[_-]?key)\b\s*[:=]\s*(?:['\"]([^\r\n'\"]+)['\"]|([^\s;,\"'{}]+))"
)


PRESERVED_HASH_KEYS = {
    "sha256",
    "event_hash",
    "previous_event_hash",
    "receipt_hash",
    "previous_receipt_hash",
    "receipt_id",
    "signature",
    "state_hash",
    "current_state_hash",
    "baseline_state_hash",
    "before_sha256",
    "after_sha256",
    "intended_after_sha256",
}


def _shannon_entropy(token: str) -> float:
    """Calculate Shannon entropy for a given token."""
    if not token:
        return 0.0
    length = len(token)
    counts: Dict[str, int] = {}
    for char in token:
        counts[char] = counts.get(char, 0) + 1
    return -sum((count / length) * math.log2(count / length) for count in counts.values())


def _is_high_entropy_secret(token: str) -> bool:
    """Detect if a standalone alphanumeric token resembles a random cryptographic secret."""
    if "[REDACTED" in token:
        return False
    if len(token) < 28 or len(token) > 120:
        return False
    # Avoid typical code identifiers or file paths
    if "/" in token or "\\" in token or "." in token or ":" in token:
        return False
    # Check if pure hex (sha256 or uuid hashes are common and preserved)
    if all(c in "0123456789abcdefABCDEF" for c in token) and len(token) in (32, 64):
        return False

    # Check if mostly alphanumeric / base64 characters
    valid_chars = set("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_+/=")
    if not set(token).issubset(valid_chars):
        return False

    entropy = _shannon_entropy(token)
    has_upper = any(c.isupper() for c in token)
    has_lower = any(c.islower() for c in token)
    has_digit = any(c.isdigit() for c in token)

    classes = sum([has_upper, has_lower, has_digit])
    if classes >= 2 and entropy >= 3.8:
        return True

    return False


def redact_secrets(text: str) -> str:
    """Redact all sensitive credentials from text across all runtime outbound channels."""
    if not text:
        return text

    redacted = text

    # 1. Private Keys
    redacted = PRIVATE_KEY_PATTERN.sub("[REDACTED_PRIVATE_KEY]", redacted)
    redacted = PGP_PRIVATE_KEY_PATTERN.sub("[REDACTED_PRIVATE_KEY]", redacted)
    redacted = GCP_SERVICE_ACCOUNT_PATTERN.sub('"private_key": "[REDACTED_PRIVATE_KEY]"', redacted)

    # 2. AWS Keys
    redacted = AWS_ACCESS_KEY_PATTERN.sub(r"\1[REDACTED_AWS_KEY]", redacted)
    redacted = AWS_SECRET_KEY_PATTERN.sub(r"aws_secret_key=[REDACTED_AWS_SECRET]", redacted)

    # 3. JWTs
    redacted = JWT_PATTERN.sub("[REDACTED_JWT]", redacted)

    # 4. Cloud API Keys (GCP, Azure)
    redacted = GCP_API_KEY_PATTERN.sub("[REDACTED_GCP_KEY]", redacted)
    redacted = AZURE_SECRET_PATTERN.sub(r"AccountKey=[REDACTED_AZURE_SECRET]", redacted)

    # 5. Developer and AI Provider Tokens
    redacted = DEVELOPER_TOKENS_PATTERN.sub("[REDACTED_TOKEN]", redacted)

    # 6. Split / Concatenated Secrets
    redacted = SPLIT_CONCAT_PATTERN.sub(r"\1=[REDACTED_CONCATENATED_SECRET]", redacted)
    redacted = MULTILINE_CONCAT_PATTERN.sub(r"\1=([REDACTED_CONCATENATED_SECRET])", redacted)

    # 7. Generic Key-Value Assignments
    redacted = GENERIC_ASSIGNMENT_PATTERN.sub(r"\1=[REDACTED]", redacted)

    # 8. High-Entropy Standalone Strings
    words = redacted.split()
    modified = False
    new_words = []
    for word in words:
        stripped = word.strip("'\",;()[]{}")
        if _is_high_entropy_secret(stripped):
            new_words.append(word.replace(stripped, "[REDACTED_HIGH_ENTROPY_SECRET]"))
            modified = True
        else:
            new_words.append(word)

    if modified:
        redacted = " ".join(new_words)

    return redacted


def redact_structure(data: Any, parent_key: str = "") -> Any:
    """Recursively sanitize nested dictionaries, lists, and objects."""
    if parent_key in PRESERVED_HASH_KEYS:
        return data
    if isinstance(data, str):
        return redact_secrets(data)
    elif isinstance(data, dict):
        return {k: redact_structure(v, parent_key=k) for k, v in data.items()}
    elif isinstance(data, (list, tuple)):
        sanitized = [redact_structure(item, parent_key=parent_key) for item in data]
        return type(data)(sanitized)
    return data
