from __future__ import annotations

import json
import shutil
import tempfile
from pathlib import Path
import uuid

from mind01.receipts import ReceiptStore, verify_receipt_chain
from mind01.traces import TraceStore, verify_trace_chain
from mind01.mutations import DirtyStateStore, FileState
from mind01.api import MindAPI
from test_api import request_json


def run_audit_chain_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-audit-"))
    try:
        # 1. Empty State Verification
        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "empty"
        assert res_r["verified_count"] == 0
        assert res_r["legacy_count"] == 0

        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "empty"
        assert res_t["verified_count"] == 0
        assert res_t["legacy_count"] == 0

        # Create stores
        r_store = ReceiptStore(tmp)
        t_store = TraceStore(tmp)

        # 2. Receipt Chain Hashing & Verification
        r1 = {
            "receipt_id": "r1",
            "operation_type": "write_file",
            "relative_file_path": "a.txt",
            "success": True,
        }
        r_store.write_receipt(r1)

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "valid"
        assert res_r["verified_count"] == 1
        assert res_r["legacy_count"] == 0

        # Verify head.json exists
        head_path = r_store.root / "head.json"
        assert head_path.exists()
        head_data = json.loads(head_path.read_text(encoding="utf-8"))
        assert head_data["receipt_id"] == "r1"

        # Create second receipt
        r2 = {
            "receipt_id": "r2",
            "operation_type": "edit_file",
            "relative_file_path": "a.txt",
            "success": True,
        }
        r_store.write_receipt(r2)

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "valid"
        assert res_r["verified_count"] == 2
        assert res_r["legacy_count"] == 0

        # Verify head.json updated
        head_data = json.loads(head_path.read_text(encoding="utf-8"))
        assert head_data["receipt_id"] == "r2"

        # Read back receipts to check hashes
        receipt2_data = r_store.get("r2")
        assert receipt2_data["previous_receipt_hash"] is not None
        assert receipt2_data["receipt_hash"] == head_data["receipt_hash"]

        # 3. Tampering: Receipt Body Tamper Detected
        path_r1 = r_store.root / "r1.json"
        data_r1 = json.loads(path_r1.read_text(encoding="utf-8"))
        data_r1["relative_file_path"] = "tampered.txt"
        path_r1.write_text(json.dumps(data_r1, indent=2, sort_keys=True), encoding="utf-8")

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "invalid"
        assert "Hash mismatch" in res_r["message"]

        # Restore r1
        data_r1["relative_file_path"] = "a.txt"
        path_r1.write_text(json.dumps(data_r1, indent=2, sort_keys=True), encoding="utf-8")
        assert verify_receipt_chain(tmp)["status"] == "valid"

        # 4. Tampering: Receipt head.json Tamper Detected
        head_data["receipt_hash"] = "incorrecthash123"
        head_path.write_text(json.dumps(head_data, indent=2, sort_keys=True), encoding="utf-8")

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "invalid"
        assert "head.json points to hash" in res_r["message"]

        # Restore head.json
        head_data["receipt_hash"] = receipt2_data["receipt_hash"]
        head_path.write_text(json.dumps(head_data, indent=2, sort_keys=True), encoding="utf-8")
        assert verify_receipt_chain(tmp)["status"] == "valid"

        # Delete head.json and check it fails
        head_path.unlink()
        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "invalid"
        assert "head.json is missing but verified receipts exist" in res_r["message"]

        # 5. Legacy Receipt Records Verification
        # Let's clean receipts first
        shutil.rmtree(r_store.root)
        r_store.root.mkdir(parents=True, exist_ok=True)
        r_store.backups.mkdir(parents=True, exist_ok=True)

        # Write manual legacy receipts (no receipt_hash)
        legacy_receipt = {
            "receipt_id": "legacy1",
            "operation_type": "write_file",
            "relative_file_path": "legacy.txt",
            "success": True,
        }
        legacy_path = r_store.root / "legacy1.json"
        legacy_path.write_text(json.dumps(legacy_receipt, indent=2, sort_keys=True), encoding="utf-8")

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "valid_with_legacy"
        assert res_r["verified_count"] == 0
        assert res_r["legacy_count"] == 1

        # Now write a new receipt on top of the legacy receipt. It should start the chain.
        new_receipt = {
            "receipt_id": "new1",
            "operation_type": "edit_file",
            "relative_file_path": "legacy.txt",
            "success": True,
        }
        r_store.write_receipt(new_receipt)

        res_r = verify_receipt_chain(tmp)
        assert res_r["status"] == "valid_with_legacy"
        assert res_r["verified_count"] == 1
        assert res_r["legacy_count"] == 1

        # 6. Trace Chain Hashing & Verification
        t_store.append({"event_type": "test_event1", "mode": "read-only"})
        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "valid"
        assert res_t["verified_count"] == 1
        assert res_t["legacy_count"] == 0

        t_store.append({"event_type": "test_event2", "mode": "read-only"})
        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "valid"
        assert res_t["verified_count"] == 2
        assert res_t["legacy_count"] == 0

        # Retrieve daily trace files
        trace_files = list(t_store.root.glob("*.jsonl"))
        assert len(trace_files) == 1
        original_lines = trace_files[0].read_text(encoding="utf-8").splitlines()
        assert len(original_lines) == 2

        # 7. Tampering: Trace Event Tamper Detected
        # Modify the first event in the trace line
        line1_data = json.loads(original_lines[0])
        line1_data["event_type"] = "tampered_event"
        new_lines = [
            json.dumps(line1_data, sort_keys=True),
            original_lines[1],
        ]
        trace_files[0].write_text("\n".join(new_lines) + "\n", encoding="utf-8")

        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "invalid"
        assert "Hash mismatch" in res_t["message"]

        # Restore trace files
        trace_files[0].write_text("\n".join(original_lines) + "\n", encoding="utf-8")
        assert verify_trace_chain(tmp)["status"] == "valid"

        # 8. Tampering: Trace head.json Tamper Detected
        t_head_path = t_store.root / "head.json"
        assert t_head_path.exists()
        t_head_data = json.loads(t_head_path.read_text(encoding="utf-8"))
        t_head_data["event_hash"] = "incorrecttracehash"
        t_head_path.write_text(json.dumps(t_head_data, indent=2, sort_keys=True), encoding="utf-8")

        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "invalid"
        assert "head.json points to event hash" in res_t["message"]

        # Delete trace head.json
        t_head_path.unlink()
        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "invalid"
        assert "head.json is missing but verified trace events exist" in res_t["message"]

        # 9. Legacy Trace Records Verification
        shutil.rmtree(t_store.root)
        t_store.root.mkdir(parents=True, exist_ok=True)

        # Write manual legacy trace event (no event_hash)
        legacy_event = {"event_type": "legacy_trace", "mode": "read-only"}
        trace_file = t_store.root / "20200101.jsonl"
        trace_file.write_text(json.dumps(legacy_event, sort_keys=True) + "\n", encoding="utf-8")

        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "valid_with_legacy"
        assert res_t["verified_count"] == 0
        assert res_t["legacy_count"] == 1

        # Append new event, which starts the chain
        t_store.append({"event_type": "new_trace", "mode": "read-only"})
        res_t = verify_trace_chain(tmp)
        assert res_t["status"] == "valid_with_legacy"
        assert res_t["verified_count"] == 1
        assert res_t["legacy_count"] == 1

        # 10. API Tests - Dirty State Endpoints (Excluding absolute paths & contents)
        api = MindAPI(tmp, "model", "http://127.0.0.1:11434", api_token="test-token")
        m_store = DirtyStateStore(tmp)

        # Create mock dirty state
        before_state = FileState(True, "before_hash", 100)
        intended_after = FileState(True, "intended_hash", 120)
        current_state = FileState(True, "current_hash", 110)

        dirty_record = m_store.create(
            operation="edit_file",
            target=tmp / "src" / "demo.py",
            before=before_state,
            intended_after=intended_after,
            current=current_state,
            backup_path=".mind01/receipts/backups/test.bak",
            error="API Test Error",
            recovery_status="restore_failed",
        )

        status, dirty_list = request_json(api, "GET", "/mutations/dirty", token="test-token")
        assert status == 200
        assert "dirty_states" in dirty_list
        assert len(dirty_list["dirty_states"]) == 1

        record = dirty_list["dirty_states"][0]
        assert record["dirty_id"] == dirty_record["dirty_id"]
        assert record["operation"] == "edit_file"
        assert record["target_relative_path"] == "src/demo.py"
        assert record["backup_relative_path"] == ".mind01/receipts/backups/test.bak"
        assert record["error"] == "API Test Error"
        # Ensure absolute path is NOT returned
        assert "target_absolute_path" not in record
        assert "backup_path" not in record

        # Show dirty state by ID
        status, dirty_show = request_json(api, "GET", f"/mutations/dirty/{dirty_record['dirty_id']}", token="test-token")
        assert status == 200
        assert "dirty_state" in dirty_show
        record = dirty_show["dirty_state"]
        assert record["dirty_id"] == dirty_record["dirty_id"]
        assert record["target_relative_path"] == "src/demo.py"
        assert record["backup_relative_path"] == ".mind01/receipts/backups/test.bak"
        assert "target_absolute_path" not in record
        assert "backup_path" not in record

        # 10.5 Write time checks for corrupted and inconsistent head.json files
        r_store_test = ReceiptStore(tmp)
        r_store_test.write_receipt({"receipt_id": "r_01_valid", "operation_type": "write", "success": True})

        test_head_path = r_store_test.root / "head.json"
        test_head_path.write_text("corrupted json", encoding="utf-8")
        from mind01.receipts import ReceiptError
        try:
            r_store_test.write_receipt({"receipt_id": "r_02_invalid1", "operation_type": "write", "success": True})
            raise AssertionError("Should have failed writing with corrupted head.json")
        except ReceiptError as exc:
            assert "head.json exists but is invalid/corrupted" in str(exc)

        test_head_path.write_text(json.dumps({"receipt_id": "r_01_valid", "receipt_hash": "wronghash"}, indent=2), encoding="utf-8")
        try:
            r_store_test.write_receipt({"receipt_id": "r_02_invalid2", "operation_type": "write", "success": True})
            raise AssertionError("Should have failed writing with inconsistent head.json")
        except ReceiptError as exc:
            assert "head.json is inconsistent with the latest receipt file" in str(exc)

        receipt_data = r_store_test.get("r_01_valid")
        test_head_path.write_text(
            json.dumps({"receipt_id": "r_01_valid", "receipt_hash": receipt_data["receipt_hash"]}, indent=2),
            encoding="utf-8"
        )

        # Rebuild check when head.json is missing
        test_head_path.unlink()
        import sys
        from io import StringIO
        old_stderr = sys.stderr
        sys.stderr = StringIO()
        try:
            r_store_test.write_receipt({"receipt_id": "r_02_rebuild_child", "operation_type": "write", "success": True})
            warning = sys.stderr.getvalue()
            assert "Warning: head.json was missing; rebuilt head" in warning
        finally:
            sys.stderr = old_stderr

        child_data = r_store_test.get("r_02_rebuild_child")
        assert child_data["previous_receipt_hash"] == receipt_data["receipt_hash"]
        assert test_head_path.exists()

        from mind01.traces import TraceError
        t_store_test = TraceStore(tmp)
        valid_evt = t_store_test.append({"event_type": "trace_valid", "mode": "read-only"})
        t_test_head_path = t_store_test.root / "head.json"

        t_test_head_path.write_text("corrupted json", encoding="utf-8")
        try:
            t_store_test.append({"event_type": "trace_invalid1", "mode": "read-only"})
            raise AssertionError("Should have failed trace append with corrupted head.json")
        except TraceError as exc:
            assert "head.json exists but is invalid/corrupted" in str(exc)

        t_test_head_path.write_text(json.dumps({"event_id": valid_evt["event_id"], "event_hash": "wronghash"}, indent=2), encoding="utf-8")
        try:
            t_store_test.append({"event_type": "trace_invalid2", "mode": "read-only"})
            raise AssertionError("Should have failed trace append with inconsistent head.json")
        except TraceError as exc:
            assert "head.json is inconsistent with the latest trace event in logs" in str(exc)

        # Restore trace head.json to valid state
        t_test_head_path.write_text(
            json.dumps({"event_id": valid_evt["event_id"], "event_hash": valid_evt["event_hash"]}, indent=2),
            encoding="utf-8"
        )

        # 11. API Tests - Health/Status Cheap Check (No Secrets)
        # Re-create receipt head.json so we can test head present statuses
        r_store.write_receipt({"receipt_id": "r3", "operation_type": "write", "success": True})

        status, health = request_json(api, "GET", "/health", token="test-token")
        assert status == 200
        assert health["ok"] is True
        from mind01 import __version__
        assert health["version"] == __version__
        assert health["default_mode"] == "read-only"
        assert health["auth_enabled"] is True
        assert health["dirty_state_count"] == 1
        assert health["receipt_chain_head_present"] is True
        assert health["trace_chain_head_present"] is True
        assert "test-token" not in json.dumps(health)

        # 12. API Tests - Structured Error request_id & trace_id Separation
        status, unauthorized = request_json(api, "GET", "/health", token="wrong-token")
        assert status == 401
        assert "error" in unauthorized
        assert unauthorized["error"]["code"] == "unauthorized"
        assert unauthorized["error"]["request_id"] != ""
        assert unauthorized["error"]["trace_id"] is None

        # Check bad route
        status, not_found = request_json(api, "GET", "/non-existent", token="test-token")
        assert status == 404
        assert not_found["error"]["code"] == "not_found"
        assert not_found["error"]["request_id"] != ""
        assert not_found["error"]["trace_id"] is None

        # 13. Phase 16.1: Atomic Receipt Write Behavior Failure Cleanup
        atomic_workspace = tmp / "atomic_test"
        r_store_atomic = ReceiptStore(atomic_workspace)
        import os
        from typing import Any
        original_replace = os.replace
        def mock_replace(src: Any, dst: Any, *args: Any, **kwargs: Any) -> Any:
            if str(dst).endswith("head.json"):
                raise OSError("Mock head.json write failure")
            return original_replace(src, dst, *args, **kwargs)
        os.replace = mock_replace  # type: ignore[assignment]

        try:
            r_store_atomic.write_receipt({"receipt_id": "r_atomic_fail", "operation_type": "write", "success": True})
            raise AssertionError("Should have failed to write receipt head")
        except ReceiptError as exc:
            assert "Could not write receipt head atomically" in str(exc)
            assert not (r_store_atomic.root / "r_atomic_fail.json").exists()
        finally:
            os.replace = original_replace

        # 14. Phase 16.1: Dirty Backup Path Sanitization
        dirty_store_test = DirtyStateStore(tmp)

        # Absolute backup path
        record_abs = dirty_store_test.create(
            operation="edit_file",
            target=tmp / "demo.py",
            before=FileState(exists=True, sha256="abc", size_bytes=10),
            intended_after=FileState(exists=True, sha256="def", size_bytes=12),
            current=FileState(exists=True, sha256="abc", size_bytes=10),
            backup_path="/absolute/path/to/backup.bak",
            error="API Test Error",
            recovery_status="failed",
        )
        status, res_abs = request_json(api, "GET", f"/mutations/dirty/{record_abs['dirty_id']}", token="test-token")
        assert status == 200
        assert res_abs["dirty_state"]["backup_relative_path"] is None

        # Directory traversal backup path
        record_trav = dirty_store_test.create(
            operation="edit_file",
            target=tmp / "demo.py",
            before=FileState(exists=True, sha256="abc", size_bytes=10),
            intended_after=FileState(exists=True, sha256="def", size_bytes=12),
            current=FileState(exists=True, sha256="abc", size_bytes=10),
            backup_path=".mind01/receipts/backups/../../traversal.bak",
            error="API Test Error",
            recovery_status="failed",
        )
        status, res_trav = request_json(api, "GET", f"/mutations/dirty/{record_trav['dirty_id']}", token="test-token")
        assert status == 200
        assert res_trav["dirty_state"]["backup_relative_path"] is None

        # Safe relative backup path
        record_safe = dirty_store_test.create(
            operation="edit_file",
            target=tmp / "demo.py",
            before=FileState(exists=True, sha256="abc", size_bytes=10),
            intended_after=FileState(exists=True, sha256="def", size_bytes=12),
            current=FileState(exists=True, sha256="abc", size_bytes=10),
            backup_path=".mind01/receipts/backups/safe.bak",
            error="API Test Error",
            recovery_status="failed",
        )
        status, res_safe = request_json(api, "GET", f"/mutations/dirty/{record_safe['dirty_id']}", token="test-token")
        assert status == 200
        assert res_safe["dirty_state"]["backup_relative_path"] == ".mind01/receipts/backups/safe.bak"

        # 15. Phase 16.1: Invalid Dirty ID structured error with request_id
        status, res_err = request_json(api, "GET", "/mutations/dirty/non-existent-id-12345", token="test-token")
        assert status == 404
        assert "error" in res_err
        assert res_err["error"]["code"] == "not_found"
        assert res_err["error"]["request_id"] != ""
        assert res_err["error"]["trace_id"] is None

    finally:
        shutil.rmtree(tmp)


if __name__ == "__main__":
    run_audit_chain_tests()


def test_audit_chain_regressions() -> None:
    run_audit_chain_tests()
