from __future__ import annotations

import hashlib
import json
import subprocess
import time
import uuid
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable

from .file_safety import FileSafetyError, ensure_write_target_safe, relative_path
from .mutations import MutationError, MutationResult, execute_content_mutation
from .locking import file_lock
from .traces import TraceError, TraceStore, sanitize_args, trace_event_base


class ReceiptError(RuntimeError):
    pass


@dataclass(frozen=True)
class ReceiptContext:
    operation_type: str
    mode: str
    allow_write: bool
    approved: bool
    source: str
    original_receipt_id: str | None = None


class ReceiptStore:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.root = self.workspace / ".mind01" / "receipts"
        self.backups = self.root / "backups"
        self.root.mkdir(parents=True, exist_ok=True)
        self.backups.mkdir(parents=True, exist_ok=True)

    def list(self, limit: int = 50) -> list[dict]:
        receipts = []
        for path in sorted(self.root.glob("*.json"), reverse=True):
            if path.name == "head.json" or path.name.startswith("."):
                continue
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            receipts.append(data)
            if len(receipts) >= limit:
                break
        return receipts

    def get(self, receipt_id: str) -> dict:
        path = self._receipt_path(receipt_id)
        if not path.exists():
            raise ReceiptError(f"Receipt not found: {receipt_id}")
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ReceiptError(f"Could not read receipt: {receipt_id}") from exc
        if not isinstance(data, dict):
            raise ReceiptError(f"Receipt is invalid: {receipt_id}")
        return data

    def render_list(self, limit: int = 50) -> str:
        receipts = self.list(limit=limit)
        if not receipts:
            return "(no receipts)"
        return "\n".join(
            f"{item.get('receipt_id')}: {item.get('operation_type')} "
            f"{item.get('relative_file_path')} {item.get('timestamp')} "
            f"success={item.get('success')}"
            for item in receipts
        )

    def render_show(self, receipt_id: str) -> str:
        return json.dumps(self.get(receipt_id), indent=2, sort_keys=True)

    def rollback(
        self,
        receipt_id: str,
        *,
        mode: str,
        approved: bool,
        force: bool = False,
        source: str = "rollback",
    ) -> dict:
        original = self.get(receipt_id)
        validate_rollback_source(original, receipt_id)
        raw_path = str(original["relative_file_path"])
        try:
            target = ensure_write_target_safe(self.workspace, raw_path)
        except FileSafetyError as exc:
            raise ReceiptError(str(exc)) from exc

        expected_after = str(original["after_sha256"])
        if not target.exists():
            current_after = None
        else:
            current_after = sha256_file(target)
        if current_after != expected_after and not force:
            raise ReceiptError(
                f"Current file hash differs from receipt after_sha256 for {raw_path}; "
                "refusing rollback without --force."
            )

        previous_backup = self._resolve_original_backup(original, receipt_id)
        self._trace_required(
            {
                **trace_event_base(event_type="rollback", mode=mode),
                "tool_name": "rollback",
                "normalized_args": sanitize_args(
                    {"receipt_id": receipt_id, "path": raw_path, "force": force}
                ),
                "policy_decision": "allowed_pre_dispatch",
                "receipt_id": receipt_id,
                "error": None,
            }
        )

        rollback_content: str | None = None
        delete = not bool(original.get("before_exists"))
        if not delete:
            if previous_backup is None:
                raise ReceiptError(
                    f"Receipt {receipt_id} is missing the backup needed for rollback."
                )
            try:
                rollback_content = previous_backup.read_text(encoding="utf-8")
            except UnicodeDecodeError as exc:
                raise ReceiptError("Rollback backup is not UTF-8 text.") from exc
            except OSError as exc:
                raise ReceiptError("Could not read rollback backup.") from exc

        return perform_verified_content_mutation(
            self.workspace,
            raw_path,
            ReceiptContext(
                operation_type="rollback",
                mode=mode,
                allow_write=False,
                approved=approved,
                source=source,
                original_receipt_id=receipt_id,
            ),
            rollback_content,
            delete=delete,
        )

    def write_receipt(self, receipt: dict) -> Path:
        with file_lock(self.root / ".chain.lock"):
            return self._write_receipt_unlocked(receipt)

    def _write_receipt_unlocked(self, receipt: dict) -> Path:
        import os
        receipt_id = str(receipt["receipt_id"])
        path = self._receipt_path(receipt_id)
        if path.exists():
            raise ReceiptError(f"Receipt already exists: {receipt_id}")

        head_path = self.root / "head.json"
        prev_hash = None
        if head_path.exists():
            try:
                head_data = json.loads(head_path.read_text(encoding="utf-8"))
                if not isinstance(head_data, dict) or "receipt_hash" not in head_data:
                    raise ReceiptError("head.json is invalid or corrupted")
                prev_hash = head_data["receipt_hash"]
            except Exception as exc:
                raise ReceiptError(f"head.json exists but is invalid/corrupted: {exc}") from exc

            head_receipt_id = head_data.get("receipt_id")
            if not isinstance(head_receipt_id, str) or not head_receipt_id:
                raise ReceiptError("head.json is missing receipt_id")
            head_receipt_path = self._receipt_path(head_receipt_id)
            if not head_receipt_path.exists():
                raise ReceiptError("head.json references a missing receipt")
            try:
                head_receipt_data = json.loads(head_receipt_path.read_text(encoding="utf-8"))
                if head_receipt_data.get("receipt_hash") != prev_hash:
                    raise ReceiptError("head.json is inconsistent with the latest receipt file")
            except Exception as exc:
                raise ReceiptError(f"Inconsistency detected: {exc}") from exc
        else:
            import sys
            receipt_files = sorted(
                (p for p in self.root.glob("*.json") if p.name != "head.json" and not p.name.startswith(".")),
                key=lambda p: p.name,
            )
            hashed_receipts = []
            for p in receipt_files:
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    if "receipt_hash" in data:
                        hashed_receipts.append(data)
                except Exception:
                    pass
            if hashed_receipts:
                referenced = {item.get("previous_receipt_hash") for item in hashed_receipts if item.get("previous_receipt_hash")}
                tips = [item for item in hashed_receipts if item.get("receipt_hash") not in referenced]
                if len(tips) != 1:
                    raise ReceiptError("Cannot rebuild missing head: receipt chain has zero or multiple tips")
                latest_hashed = tips[0]
                prev_hash = latest_hashed.get("receipt_hash")
                print(
                    f"Warning: head.json was missing; rebuilt head from chain tip {latest_hashed.get('receipt_id')}",
                    file=sys.stderr,
                )
            else:
                prev_hash = None

        receipt["previous_receipt_hash"] = prev_hash
        receipt_hash = hashlib.sha256(canonical_json(receipt)).hexdigest()
        receipt["receipt_hash"] = receipt_hash

        temp_receipt = path.parent / f".{receipt_id}.json.tmp-{uuid.uuid4().hex}"
        try:
            with temp_receipt.open("w", encoding="utf-8") as handle:
                json.dump(receipt, handle, indent=2, sort_keys=True)
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass
            os.replace(temp_receipt, path)
        except Exception as exc:
            if temp_receipt.exists():
                try:
                    temp_receipt.unlink()
                except OSError:
                    pass
            raise ReceiptError(f"Could not write receipt atomically: {receipt_id} - {exc}") from exc

        temp_head = head_path.parent / f".head.json.tmp-{uuid.uuid4().hex}"
        try:
            with temp_head.open("w", encoding="utf-8") as handle:
                json.dump(
                    {"receipt_id": receipt_id, "receipt_hash": receipt_hash},
                    handle,
                    indent=2,
                    sort_keys=True,
                )
                handle.flush()
                try:
                    os.fsync(handle.fileno())
                except OSError:
                    pass
            os.replace(temp_head, head_path)
        except Exception as exc:
            if path.exists():
                try:
                    path.unlink()
                except OSError:
                    pass
            raise ReceiptError(f"Could not write receipt head atomically: {exc}") from exc

        return path

    def _receipt_path(self, receipt_id: str) -> Path:
        if "/" in receipt_id or "\\" in receipt_id or receipt_id.startswith("."):
            raise ReceiptError(f"Invalid receipt id: {receipt_id}")
        return self.root / f"{receipt_id}.json"

    def _resolve_original_backup(self, receipt: dict, receipt_id: str) -> Path | None:
        if not bool(receipt.get("before_exists")):
            return None
        backup = receipt.get("backup_path")
        if not isinstance(backup, str) or not backup:
            raise ReceiptError(f"Receipt {receipt_id} has no backup path.")
        path = (self.workspace / backup).resolve()
        backup_root = self.backups.resolve()
        if backup_root != path and backup_root not in path.parents:
            raise ReceiptError(f"Receipt {receipt_id} backup path is outside receipt storage.")
        if not path.is_file():
            raise ReceiptError(f"Receipt {receipt_id} backup file is missing.")
        return path

    def _trace_required(self, event: dict) -> None:
        try:
            TraceStore(self.workspace).append(event)
        except TraceError as exc:
            raise ReceiptError("Required rollback trace event could not be written.") from exc


def perform_verified_file_mutation(
    workspace: Path,
    raw_path: str,
    context: ReceiptContext,
    mutator: Callable[[Path], None],
    after_must_exist: bool = True,
) -> dict:
    raise ReceiptError(
        "Callback-based file mutations are disabled; use transaction-safe content mutations."
    )


def perform_verified_content_mutation(
    workspace: Path,
    raw_path: str,
    context: ReceiptContext,
    content: str | None,
    *,
    delete: bool = False,
) -> dict:
    store = ReceiptStore(workspace)
    try:
        target = ensure_write_target_safe(workspace, raw_path)
    except FileSafetyError as exc:
        raise ReceiptError(str(exc)) from exc

    receipt_id = make_receipt_id(context.operation_type)
    before_status = git_status_summary(workspace)
    rel_path = relative_path(workspace, target)

    receipt = {
        "receipt_id": receipt_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation_type": context.operation_type,
        "original_receipt_id": context.original_receipt_id,
        "workspace": str(workspace.resolve()),
        "relative_file_path": rel_path,
        "absolute_file_path": str(target),
        "mode": context.mode,
        "allow_write": context.allow_write,
        "approved": context.approved,
        "approval_yes_status": context.approved,
        "before_exists": None,
        "before_sha256": None,
        "after_exists": None,
        "after_sha256": None,
        "before_size_bytes": None,
        "after_size_bytes": None,
        "backup_path": None,
        "git_status_before": before_status,
        "git_status_after": "",
        "tool_name": context.source,
        "success": False,
        "error": None,
    }

    def write_success_metadata(result: MutationResult) -> None:
        receipt["before_exists"] = result.before.exists
        receipt["before_sha256"] = result.before.sha256
        receipt["before_size_bytes"] = result.before.size_bytes
        receipt["after_exists"] = result.final.exists
        receipt["after_sha256"] = result.final.sha256
        receipt["after_size_bytes"] = result.final.size_bytes
        receipt["backup_path"] = result.backup_path
        receipt["git_status_after"] = git_status_summary(workspace)
        receipt["success"] = True
        store.write_receipt(receipt)

    try:
        execute_content_mutation(
            workspace=workspace,
            raw_path=raw_path,
            operation=context.operation_type,
            receipt_id=receipt_id,
            content=content,
            delete=delete,
            write_success_metadata=write_success_metadata,
        )
    except MutationError as exc:
        receipt["success"] = False
        receipt["error"] = str(exc)
        raise ReceiptError(str(exc)) from exc

    return receipt


def record_blocked_mutation(
    workspace: Path,
    *,
    operation_type: str,
    path: str = "",
    reason: str = "",
    source: str = "pre_validation",
    mode: str = "write-approved",
) -> dict:
    """Record a mutation that was rejected before it touched the filesystem.

    The attempt is written into the normal receipt chain with ``success``
    False, so blocked attempts stay auditable without claiming a write ever
    occurred. Because ``validate_rollback_source`` requires ``success is
    True``, such a receipt can never be rolled back — there is nothing to
    roll back.
    """
    store = ReceiptStore(workspace)
    receipt_id = make_receipt_id(operation_type)
    receipt = {
        "receipt_id": receipt_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "operation_type": f"{operation_type}_blocked",
        "workspace": str(workspace.resolve()),
        "relative_file_path": path,
        "mode": mode,
        "tool_name": source,
        "success": False,
        "error": reason,
    }
    store.write_receipt(receipt)
    return receipt


def validate_rollback_source(receipt: dict, receipt_id: str) -> None:
    if receipt.get("success") is not True:
        raise ReceiptError(f"Receipt is not a successful write receipt: {receipt_id}")
    operation = receipt.get("operation_type")
    if operation not in {"write_file", "edit_file", "patch_apply"}:
        raise ReceiptError(
            f"Receipt {receipt_id} cannot be rolled back because operation "
            f"`{operation}` is not rollback-supported."
        )
    if not isinstance(receipt.get("relative_file_path"), str):
        raise ReceiptError(f"Receipt {receipt_id} is missing relative_file_path.")
    if not isinstance(receipt.get("after_sha256"), str) or not receipt.get("after_sha256"):
        raise ReceiptError(f"Receipt {receipt_id} is missing after_sha256.")


def make_receipt_id(operation_type: str) -> str:
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S")
    return f"{stamp}_{time.time_ns()}_{operation_type}_{uuid.uuid4().hex[:8]}"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_status_summary(workspace: Path) -> str:
    try:
        completed = subprocess.run(
            ["git", "status", "--short"],
            cwd=workspace,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            timeout=5,
        )
    except (OSError, subprocess.TimeoutExpired):
        return ""
    if completed.returncode != 0:
        return ""
    return completed.stdout[:20000]


def canonical_json(data: dict) -> bytes:
    cleaned = {
        k: v for k, v in data.items()
        if k not in ("receipt_hash", "event_hash")
    }
    return json.dumps(
        cleaned,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    ).encode("utf-8")


def verify_receipt_chain(workspace: Path) -> dict:
    store = ReceiptStore(workspace)
    receipt_files = sorted(
        (path for path in store.root.glob("*.json") if path.name != "head.json" and not path.name.startswith(".")),
        key=lambda path: path.name,
    )
    head_path = store.root / "head.json"
    if not receipt_files:
        if head_path.exists():
            return {"status": "invalid", "message": "head.json exists but no receipts found", "verified_count": 0, "legacy_count": 0}
        return {"status": "empty", "message": "No receipts found.", "verified_count": 0, "legacy_count": 0}

    legacy_count = 0
    hashed: dict[str, dict] = {}
    for path in receipt_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "invalid", "message": f"Could not read receipt file {path.name}: {exc}", "verified_count": 0, "legacy_count": legacy_count}
        if "receipt_hash" not in data:
            legacy_count += 1
            continue
        stored_hash = data.get("receipt_hash")
        expected_hash = hashlib.sha256(canonical_json(data)).hexdigest()
        if stored_hash != expected_hash:
            return {
                "status": "invalid",
                "message": f"Hash mismatch in receipt {data.get('receipt_id')}. Stored: {stored_hash}, Computed: {expected_hash}",
                "verified_count": 0,
                "legacy_count": legacy_count,
            }
        if stored_hash in hashed:
            return {"status": "invalid", "message": "Duplicate receipt hash detected.", "verified_count": 0, "legacy_count": legacy_count}
        hashed[str(stored_hash)] = data

    if not hashed:
        if head_path.exists():
            return {"status": "invalid", "message": "head.json exists but no verified receipts found", "verified_count": 0, "legacy_count": legacy_count}
        return {"status": "valid_with_legacy", "message": "Only legacy receipts exist, no chain head.", "verified_count": 0, "legacy_count": legacy_count}
    if not head_path.exists():
        return {"status": "invalid", "message": "head.json is missing but verified receipts exist", "verified_count": 0, "legacy_count": legacy_count}
    try:
        head_data = json.loads(head_path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {"status": "invalid", "message": f"Could not read head.json: {exc}", "verified_count": 0, "legacy_count": legacy_count}
    head_hash = head_data.get("receipt_hash")
    if head_hash not in hashed:
        return {
            "status": "invalid",
            "message": f"head.json points to hash {head_hash}, but that receipt is missing from the chain",
            "verified_count": 0,
            "legacy_count": legacy_count,
        }

    visited: set[str] = set()
    current: str | None = str(head_hash)
    while current is not None:
        if current in visited:
            return {"status": "invalid", "message": "Cycle detected in receipt chain.", "verified_count": len(visited), "legacy_count": legacy_count}
        data = hashed.get(current)
        if data is None:
            return {
                "status": "invalid",
                "message": f"Link mismatch in receipt chain. Missing previous hash: {current}",
                "verified_count": len(visited),
                "legacy_count": legacy_count,
            }
        visited.add(current)
        previous = data.get("previous_receipt_hash")
        current = str(previous) if previous is not None else None

    if len(visited) != len(hashed):
        return {
            "status": "invalid",
            "message": "Receipt chain contains disconnected or forked verified records.",
            "verified_count": len(visited),
            "legacy_count": legacy_count,
        }
    status = "valid" if legacy_count == 0 else "valid_with_legacy"
    return {
        "status": status,
        "message": "Receipt chain is healthy.",
        "verified_count": len(visited),
        "legacy_count": legacy_count,
    }
