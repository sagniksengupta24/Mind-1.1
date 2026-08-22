from __future__ import annotations

import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mind01.sessions import SessionStore


def test_session_context_is_bounded_and_separated() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-session-context-"))
    try:
        store = SessionStore(tmp)
        first = store.create("first")
        second = store.create("second")
        for index in range(30):
            store.add_message(first.id, "user", f"turn-{index} " + ("x" * 500))
            store.add_message(first.id, "assistant", f"answer-{index}")
        store.add_message(second.id, "user", "private-second-session")

        context = store.context_messages(first.id, max_messages=8, max_chars=3000)
        joined = "\n".join(item["content"] for item in context)
        assert "Earlier session summary" in joined
        assert "turn-29" in joined
        assert "private-second-session" not in joined
        assert len(joined) < 8000
    finally:
        shutil.rmtree(tmp)


def test_session_sqlite_concurrent_writes() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-session-concurrency-"))
    try:
        store = SessionStore(tmp)
        session = store.create("concurrent")

        def write(index: int) -> None:
            SessionStore(tmp).add_message(session.id, "user", f"message-{index}")

        with ThreadPoolExecutor(max_workers=8) as pool:
            list(pool.map(write, range(40)))
        _session, messages = store.get(session.id)
        assert len(messages) == 40
        assert {message.content for message in messages} == {f"message-{index}" for index in range(40)}
    finally:
        shutil.rmtree(tmp)
