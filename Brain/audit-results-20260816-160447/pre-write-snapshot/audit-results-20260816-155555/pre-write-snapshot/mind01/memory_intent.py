from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class MemoryIntent:
    kind: str
    key: str = ""
    value: str = ""
    query: str = ""


REMEMBER_RE = re.compile(
    r"\b(?:remember|save|store)\b(?:\s+this)?(?:\s+(?P<key>[^:\n]{1,80}))?:\s*(?P<value>.+)",
    re.IGNORECASE | re.DOTALL,
)
RECALL_RE = re.compile(
    r"\b(?:recall|retrieve)\b\s+(?P<query>[^.\n]+)",
    re.IGNORECASE,
)


def detect_memory_intent(prompt: str) -> Optional[MemoryIntent]:
    remember = REMEMBER_RE.search(prompt)
    if remember:
        key = normalize_key(remember.group("key") or "memory")
        value = clean_remember_value(remember.group("value"))
        if value:
            return MemoryIntent(kind="remember", key=key, value=value)

    lowered = prompt.lower()
    if "what do you remember" in lowered:
        return MemoryIntent(kind="recall", query="memory")

    recall = RECALL_RE.search(prompt)
    if recall:
        query = clean_recall_query(recall.group("query"))
        if query:
            return MemoryIntent(kind="recall", query=query)

    return None


def normalize_key(raw: str) -> str:
    key = raw.strip().strip(" .")
    if key.lower().startswith("the "):
        key = key[4:]
    if key.lower().startswith("a "):
        key = key[2:]
    if not key:
        return "memory"
    return key[:80]


def clean_remember_value(raw: str) -> str:
    value = raw.strip()
    for marker in [" Then ", "\nThen ", " then "]:
        if marker in value:
            value = value.split(marker, 1)[0]
    return value.strip().strip('"').strip("'").strip()


def clean_recall_query(raw: str) -> str:
    query = raw.strip().strip(" .")
    for marker in [" and ", " using ", " in "]:
        if marker in query:
            query = query.split(marker, 1)[0]
    if query.lower().startswith("the "):
        query = query[4:]
    return query.strip()[:120]
