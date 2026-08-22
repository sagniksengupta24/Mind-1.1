from __future__ import annotations

import shutil
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from mind01.receipts import ReceiptStore, verify_receipt_chain
from mind01.traces import TraceStore, verify_trace_chain


def test_concurrent_trace_chain_writers() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-trace-concurrency-"))
    try:
        def append(index: int) -> str:
            return TraceStore(tmp).append({"event_type": "concurrent", "mode": "read-only", "index": index})["event_id"]

        with ThreadPoolExecutor(max_workers=10) as pool:
            ids = list(pool.map(append, range(50)))
        assert len(set(ids)) == 50
        result = verify_trace_chain(tmp)
        assert result["status"] == "valid"
        assert result["verified_count"] == 50
    finally:
        shutil.rmtree(tmp)


def test_concurrent_receipt_chain_writers() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-receipt-concurrency-"))
    try:
        def append(index: int) -> str:
            receipt_id = f"R{index:04d}"
            ReceiptStore(tmp).write_receipt(
                {
                    "receipt_id": receipt_id,
                    "timestamp": index,
                    "operation_type": "test",
                    "relative_file_path": f"file-{index}.txt",
                    "success": True,
                }
            )
            return receipt_id

        with ThreadPoolExecutor(max_workers=10) as pool:
            ids = list(pool.map(append, range(30)))
        assert len(set(ids)) == 30
        result = verify_receipt_chain(tmp)
        assert result["status"] == "valid"
        assert result["verified_count"] == 30
    finally:
        shutil.rmtree(tmp)
