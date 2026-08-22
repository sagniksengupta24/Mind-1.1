from __future__ import annotations

import shutil
import tempfile
from pathlib import Path

from mind01.project_knowledge import ProjectKnowledgeStore
from mind01.tools import ToolRegistry


def test_project_knowledge_tracks_provenance_and_invalidates_changed_file() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="mind-knowledge-"))
    try:
        source = tmp / "demo.py"
        source.write_text("import json\n\ndef add(a, b):\n    return a + b\n", encoding="utf-8")
        store = ProjectKnowledgeStore(tmp)
        counts = store.refresh(".")
        assert counts["files"] == 1
        assert counts["symbols"] == 1
        add_hits = store.query("add")
        assert len(add_hits) == 1
        assert add_hits[0].provenance == "demo.py:L3"
        assert any(item["predicate"] == "defines" for item in store.relations_for(add_hits[0].entity_id))

        source.write_text("import math\n\ndef subtract(a, b):\n    return a - b\n", encoding="utf-8")
        store.refresh(".")
        assert store.query("add") == []
        subtract = store.query("subtract")
        assert subtract and subtract[0].provenance == "demo.py:L3"

        tools = ToolRegistry(tmp, mode="propose", yes=True)
        assert "Refreshed project knowledge" in tools.call("refresh_knowledge", {"path": "."}).text
        assert "subtract" in tools.call("query_knowledge", {"query": "subtract"}).text
    finally:
        shutil.rmtree(tmp)
