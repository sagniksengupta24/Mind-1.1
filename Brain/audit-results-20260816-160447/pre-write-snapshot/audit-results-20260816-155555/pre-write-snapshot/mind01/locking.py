from __future__ import annotations

import contextlib
import os
import threading
from pathlib import Path
from typing import Iterator


_PROCESS_LOCKS: dict[str, threading.RLock] = {}
_PROCESS_GUARD = threading.Lock()


@contextlib.contextmanager
def file_lock(path: Path) -> Iterator[None]:
    """Cross-thread and, on POSIX, cross-process exclusive lock."""
    path.parent.mkdir(parents=True, exist_ok=True)
    key = str(path.resolve())
    with _PROCESS_GUARD:
        lock = _PROCESS_LOCKS.setdefault(key, threading.RLock())
    with lock:
        handle = path.open("a+b")
        try:
            if os.name == "posix":
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            if os.name == "posix":
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            handle.close()
