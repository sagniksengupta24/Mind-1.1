from __future__ import annotations

import difflib
import json
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .file_safety import (
    FileSafetyError,
    ensure_text_file_safe,
    ensure_write_target_safe,
    resolve_workspace_path,
)
from .receipts import ReceiptContext, ReceiptError, perform_verified_content_mutation
from .traces import TraceError, TraceStore, sanitize_args, trace_event_base


class PatchError(RuntimeError):
    pass


@dataclass
class PatchProposal:
    id: int
    kind: str
    path: str
    content: str | None = None
    old: str | None = None
    new: str | None = None
    reason: str = ""
    created_at: int = 0

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PatchProposal":
        return cls(
            id=int(data["id"]),
            kind=str(data["kind"]),
            path=str(data["path"]),
            content=data.get("content"),
            old=data.get("old"),
            new=data.get("new"),
            reason=str(data.get("reason", "")),
            created_at=int(data.get("created_at", 0)),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "kind": self.kind,
            "path": self.path,
            "content": self.content,
            "old": self.old,
            "new": self.new,
            "reason": self.reason,
            "created_at": self.created_at,
        }


class PatchStore:
    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace.resolve()
        self.path = self.workspace / ".mind01" / "patches.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def propose_write(self, path: str, content: str, reason: str = "") -> PatchProposal:
        self._resolve_write(path)
        proposal = self._new("write", path, reason)
        proposal.content = content
        self._append(proposal)
        return proposal

    def propose_edit(
        self, path: str, old: str, new: str, reason: str = ""
    ) -> PatchProposal:
        target = self._resolve_existing_text(path)
        current = target.read_text(encoding="utf-8")
        if old not in current:
            raise PatchError("Old text is not present in current file.")
        proposal = self._new("edit", path, reason)
        proposal.old = old
        proposal.new = new
        self._append(proposal)
        return proposal

    def list(self) -> list[PatchProposal]:
        return [PatchProposal.from_dict(item) for item in self._read()]

    def get(self, patch_id: int) -> PatchProposal:
        for proposal in self.list():
            if proposal.id == patch_id:
                return proposal
        raise PatchError(f"Patch proposal not found: {patch_id}")

    def show(self, patch_id: int) -> str:
        proposal = self.get(patch_id)
        target = self._resolve(proposal.path)
        current = ""
        if target.exists():
            self._ensure_text(target, proposal.path)
            current = target.read_text(encoding="utf-8", errors="ignore")
        if proposal.kind == "write":
            updated = proposal.content or ""
        elif proposal.kind == "edit":
            if proposal.old is None or proposal.new is None:
                raise PatchError("Edit proposal is missing old/new text.")
            if proposal.old not in current:
                raise PatchError("Old text is not present in current file.")
            updated = current.replace(proposal.old, proposal.new, 1)
        else:
            raise PatchError(f"Unknown proposal kind: {proposal.kind}")

        diff = difflib.unified_diff(
            current.splitlines(),
            updated.splitlines(),
            fromfile=f"a/{proposal.path}",
            tofile=f"b/{proposal.path}",
            lineterm="",
        )
        header = f"patch {proposal.id}: {proposal.kind} {proposal.path}\nreason: {proposal.reason}\n"
        return header + "\n".join(diff)

    def apply(
        self,
        patch_id: int,
        mode: str = "write-approved",
        allow_write: bool = False,
        approved: bool = False,
        source: str = "patch_apply",
    ) -> str:
        proposal = self.get(patch_id)
        target = self._resolve_write(proposal.path)
        updated_text = ""
        if proposal.kind == "edit":
            if proposal.old is None or proposal.new is None:
                raise PatchError("Edit proposal is missing old/new text.")
            self._ensure_text(target, proposal.path)
            current = target.read_text(encoding="utf-8")
            if proposal.old not in current:
                raise PatchError("Old text is not present in current file.")
            updated_text = current.replace(proposal.old, proposal.new, 1)
        elif proposal.kind == "write":
            updated_text = proposal.content or ""
        elif proposal.kind != "write":
            raise PatchError(f"Unknown proposal kind: {proposal.kind}")
        self._trace_required(
            {
                **trace_event_base(event_type="patch_apply", mode=mode),
                "tool_name": "patch_apply",
                "normalized_args": sanitize_args(
                    {"id": patch_id, "path": proposal.path, "kind": proposal.kind}
                ),
                "policy_decision": "allowed_pre_dispatch",
                "receipt_id": None,
                "error": None,
            }
        )

        try:
            receipt = perform_verified_content_mutation(
                self.workspace,
                proposal.path,
                ReceiptContext(
                    operation_type="patch_apply",
                    mode=mode,
                    allow_write=allow_write,
                    approved=approved,
                    source=source,
                ),
                updated_text,
            )
        except ReceiptError as exc:
            raise PatchError(str(exc)) from exc
        self._remove(patch_id)
        return (
            f"Applied patch {patch_id} to {proposal.path}. "
            f"Receipt {receipt['receipt_id']}."
        )

    def discard(self, patch_id: int) -> str:
        self.get(patch_id)
        self._remove(patch_id)
        return f"Discarded patch {patch_id}."

    def render_list(self) -> str:
        proposals = self.list()
        if not proposals:
            return "(no pending patches)"
        return "\n".join(
            f"{item.id}: {item.kind} {item.path} - {item.reason}" for item in proposals
        )

    def _new(self, kind: str, path: str, reason: str) -> PatchProposal:
        proposals = self.list()
        next_id = max((item.id for item in proposals), default=0) + 1
        return PatchProposal(
            id=next_id,
            kind=kind,
            path=path,
            reason=reason,
            created_at=int(time.time()),
        )

    def _append(self, proposal: PatchProposal) -> None:
        items = self._read()
        items.append(proposal.to_dict())
        self._write(items)

    def _remove(self, patch_id: int) -> None:
        items = [item for item in self._read() if int(item["id"]) != patch_id]
        self._write(items)

    def _read(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        return json.loads(self.path.read_text(encoding="utf-8"))

    def _write(self, items: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(items, indent=2), encoding="utf-8")

    def _resolve(self, raw_path: str) -> Path:
        try:
            return resolve_workspace_path(self.workspace, raw_path)
        except FileSafetyError as exc:
            raise PatchError(str(exc)) from exc

    def _resolve_write(self, raw_path: str) -> Path:
        try:
            return ensure_write_target_safe(self.workspace, raw_path)
        except FileSafetyError as exc:
            raise PatchError(str(exc)) from exc

    def _resolve_existing_text(self, raw_path: str) -> Path:
        target = self._resolve(raw_path)
        self._ensure_text(target, raw_path)
        return target

    def _ensure_text(self, path: Path, raw_path: str) -> None:
        try:
            ensure_text_file_safe(self.workspace, path, raw_path)
        except FileSafetyError as exc:
            raise PatchError(str(exc)) from exc

    def _trace_required(self, event: dict[str, Any]) -> None:
        try:
            TraceStore(self.workspace).append(event)
        except TraceError as exc:
            raise PatchError("Required patch apply trace event could not be written.") from exc
