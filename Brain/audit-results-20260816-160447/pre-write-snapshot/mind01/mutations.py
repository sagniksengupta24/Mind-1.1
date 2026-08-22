from __future__ import annotations

import hashlib
import json
import os
import shutil
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .file_safety import FileSafetyError, ensure_write_target_safe, relative_path


class MutationError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        restored: bool = False,
        dirty_id: str | None = None,
    ) -> None:
        super().__init__(message)
        self.restored = restored
        self.dirty_id = dirty_id


@dataclass(frozen=True)
class FileState:
    exists: bool
    sha256: str | None
    size_bytes: int | None


@dataclass(frozen=True)
class MutationResult:
    receipt_id: str
    operation: str
    target: Path
    relative_path: str
    before: FileState
    intended_after: FileState
    final: FileState
    backup_path: str | None


class DirtyStateStore:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.root = self.workspace / ".mind01" / "mutations" / "dirty"
        self.root.mkdir(parents=True, exist_ok=True)

    def create(
        self,
        *,
        operation: str,
        target: Path,
        before: FileState,
        intended_after: FileState,
        current: FileState,
        backup_path: str | None,
        error: str,
        recovery_status: str,
    ) -> dict:
        dirty_id = make_dirty_id(operation)
        rel = relative_path(self.workspace, target)
        record = {
            "dirty_id": dirty_id,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "operation": operation,
            "target_relative_path": rel,
            "target_absolute_path": str(target),
            "before_sha256": before.sha256,
            "before_size_bytes": before.size_bytes,
            "intended_after_sha256": intended_after.sha256,
            "intended_after_size_bytes": intended_after.size_bytes,
            "current_sha256": current.sha256,
            "current_size_bytes": current.size_bytes,
            "backup_path": backup_path,
            "error": error,
            "recovery_status": recovery_status,
            "manual_repair_instructions": (
                "Inspect the target path, compare current_sha256 with before_sha256 "
                "and intended_after_sha256, then restore from backup_path if appropriate. "
                "Do not assume the mutation succeeded."
            ),
        }
        path = self._path(dirty_id)
        path.write_text(json.dumps(record, indent=2, sort_keys=True), encoding="utf-8")
        return record

    def list(self, limit: int = 50) -> list[dict]:
        records = []
        for path in sorted(self.root.glob("*.json"), reverse=True):
            try:
                records.append(json.loads(path.read_text(encoding="utf-8")))
            except (OSError, json.JSONDecodeError):
                continue
            if len(records) >= limit:
                break
        return records

    def get(self, dirty_id: str) -> dict:
        path = self._path(dirty_id)
        if not path.exists():
            raise MutationError(f"Dirty mutation record not found: {dirty_id}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise MutationError(f"Could not read dirty mutation record: {dirty_id}") from exc
        if not isinstance(data, dict):
            raise MutationError(f"Dirty mutation record is invalid: {dirty_id}")
        return data

    def render_list(self, limit: int = 50) -> str:
        records = self.list(limit=limit)
        if not records:
            return "(no dirty mutations)"
        return "\n".join(
            f"{item.get('dirty_id')}: {item.get('operation')} "
            f"{item.get('target_relative_path')} {item.get('timestamp')} "
            f"recovery={item.get('recovery_status')}"
            for item in records
        )

    def render_show(self, dirty_id: str) -> str:
        return json.dumps(self.get(dirty_id), indent=2, sort_keys=True)

    def _path(self, dirty_id: str) -> Path:
        if "/" in dirty_id or "\\" in dirty_id or dirty_id.startswith("."):
            raise MutationError(f"Invalid dirty mutation id: {dirty_id}")
        return self.root / f"{dirty_id}.json"


def execute_content_mutation(
    *,
    workspace: Path,
    raw_path: str,
    operation: str,
    receipt_id: str,
    content: str | None,
    delete: bool,
    write_success_metadata: Callable[[MutationResult], None],
) -> MutationResult:
    root = workspace.resolve()
    try:
        target = ensure_write_target_safe(root, raw_path)
    except FileSafetyError as exc:
        raise MutationError(str(exc)) from exc

    temp_path: Path | None = None
    replaced = False
    rel = relative_path(root, target)
    before = file_state(target)
    intended = intended_state(content, delete)
    backup_path = create_backup(root, target, receipt_id) if before.exists else None

    try:
        if delete:
            if target.exists():
                target.unlink()
            replaced = True
        else:
            if content is None:
                raise MutationError("Mutation content is required unless delete=true.")
            target.parent.mkdir(parents=True, exist_ok=True)
            temp_path = write_temp_file(target, content)
            verify_state(temp_path, intended, "temporary mutation file")
            os.replace(temp_path, target)
            temp_path = None
            fsync_directory(target.parent)
            replaced = True

        final = file_state(target)
        verify_state_matches(final, intended, rel)
        result = MutationResult(
            receipt_id=receipt_id,
            operation=operation,
            target=target,
            relative_path=rel,
            before=before,
            intended_after=intended,
            final=final,
            backup_path=backup_path,
        )
        write_success_metadata(result)
        return result
    except Exception as exc:
        if temp_path is not None and temp_path.exists():
            try:
                temp_path.unlink()
            except OSError:
                pass
        if not replaced:
            raise MutationError(
                f"Mutation failed before replace for {rel}: {exc}"
            ) from exc
        restored = False
        try:
            restore_previous_state(root, target, before, backup_path)
            verify_state_matches(file_state(target), before, rel)
            restored = True
        except Exception as restore_exc:
            current = file_state(target)
            dirty = DirtyStateStore(root).create(
                operation=operation,
                target=target,
                before=before,
                intended_after=intended,
                current=current,
                backup_path=backup_path,
                error=f"{type(exc).__name__}: {exc}",
                recovery_status=f"restore_failed: {type(restore_exc).__name__}",
            )
            raise MutationError(
                f"Mutation failed after replace for {rel}; restore failed; "
                f"dirty state recorded as {dirty['dirty_id']}.",
                dirty_id=str(dirty["dirty_id"]),
            ) from exc
        if restored:
            raise MutationError(
                f"Mutation failed after replace for {rel}: {exc}; original state restored.",
                restored=True,
            ) from exc
        raise MutationError(f"Mutation failed after replace for {rel}: {exc}") from exc


def create_backup(workspace: Path, target: Path, receipt_id: str) -> str:
    backup_root = workspace / ".mind01" / "receipts" / "backups"
    backup_root.mkdir(parents=True, exist_ok=True)
    rel = relative_path(workspace, target)
    safe_name = rel.replace("/", "__").replace("\\", "__")
    backup_path = backup_root / f"{receipt_id}_{safe_name}.bak"
    try:
        shutil.copy2(target, backup_path)
    except OSError as exc:
        raise MutationError(f"Could not create mutation backup for {rel}") from exc
    return relative_path(workspace, backup_path)


def restore_previous_state(
    workspace: Path,
    target: Path,
    before: FileState,
    backup_path: str | None,
) -> None:
    if before.exists:
        if not backup_path:
            raise MutationError("Cannot restore previous file without backup.")
        backup = (workspace / backup_path).resolve()
        backup_root = (workspace / ".mind01" / "receipts" / "backups").resolve()
        if backup_root != backup and backup_root not in backup.parents:
            raise MutationError("Backup path escapes receipt backup storage.")
        if not backup.is_file():
            raise MutationError("Backup file is missing.")
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(backup, target)
        fsync_directory(target.parent)
        return
    if target.exists():
        if not target.is_file():
            raise MutationError("Cannot restore previous absent state over non-file target.")
        target.unlink()
        fsync_directory(target.parent)


def write_temp_file(target: Path, content: str) -> Path:
    temp_path = target.parent / f".{target.name}.mind-tmp-{uuid.uuid4().hex}"
    try:
        with temp_path.open("w", encoding="utf-8") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
    except OSError as exc:
        raise MutationError("Could not write temporary mutation file.") from exc
    return temp_path


def verify_state(path: Path, expected: FileState, label: str) -> None:
    actual = file_state(path)
    if actual.sha256 != expected.sha256 or actual.size_bytes != expected.size_bytes:
        raise MutationError(f"Verification failed for {label}.")


def verify_state_matches(actual: FileState, expected: FileState, rel_path: str) -> None:
    if actual.exists != expected.exists:
        raise MutationError(f"Final existence verification failed for {rel_path}.")
    if actual.sha256 != expected.sha256 or actual.size_bytes != expected.size_bytes:
        raise MutationError(f"Final hash/size verification failed for {rel_path}.")


def intended_state(content: str | None, delete: bool) -> FileState:
    if delete:
        return FileState(False, None, None)
    if content is None:
        raise MutationError("Mutation content is required.")
    data = content.encode("utf-8")
    return FileState(True, hashlib.sha256(data).hexdigest(), len(data))


def file_state(path: Path) -> FileState:
    if not path.exists():
        return FileState(False, None, None)
    return FileState(True, sha256_file(path), path.stat().st_size)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fsync_directory(path: Path) -> None:
    try:
        fd = os.open(str(path), os.O_RDONLY)
    except OSError:
        return
    try:
        os.fsync(fd)
    except OSError:
        return
    finally:
        os.close(fd)


def make_dirty_id(operation: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    safe_operation = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "_" for ch in operation)
    return f"{stamp}_{time.time_ns()}_{safe_operation}_{uuid.uuid4().hex[:8]}"
