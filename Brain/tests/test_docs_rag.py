from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from mind01.rag import DocStore


def run_docs_rag_tests() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind01-docs-rag-"))
    try:
        docs_dir = tmp / "docs"
        docs_dir.mkdir()
        timing = docs_dir / "timing.md"
        timing.write_text(
            "\n".join(
                [
                    "# Timing",
                    "Setup time is checked before the active clock edge.",
                    "Hold time is checked after the active clock edge.",
                    "Capture margin depends on clock skew and data delay.",
                    "Semiconductor learners should cite exact lines.",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

        store = DocStore(tmp)
        indexed = store.index_path(docs_dir)
        assert indexed >= 1
        hits = store.search("capture margin", limit=3)
        assert hits
        hit = hits[0]
        assert hit.path == "docs/timing.md"
        assert hit.line_start == 1
        assert hit.line_end == 5
        assert hit.citation == "docs/timing.md:L1-L5"
        assert hit.chunk_sha256
        assert hit.file_mtime_ns > 0
        assert hit.stale is False
        assert "Capture margin" in hit.chunk

        timing.write_text(
            timing.read_text(encoding="utf-8") + "New stale line.\n",
            encoding="utf-8",
        )
        stale = store.stale_files()
        assert len(stale) == 1
        assert stale[0].path == "docs/timing.md"
        stale_hits = store.search("capture margin", limit=1)
        assert stale_hits
        assert stale_hits[0].stale is True

        assert store.index_path(docs_dir) >= 1
        store.fts_enabled = False
        fallback_hits = store.search("hold clock", limit=2)
        assert fallback_hits
        assert fallback_hits[0].citation.startswith("docs/timing.md:L")
    finally:
        shutil.rmtree(tmp)


def test_docs_rag_regressions() -> None:
    run_docs_rag_tests()
