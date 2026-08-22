from __future__ import annotations

import tempfile
from pathlib import Path

from mind01.cli import main


def test_cli_project_knowledge_round_trip(capsys) -> None:
    with tempfile.TemporaryDirectory(prefix="mind-cli-knowledge-") as directory:
        root = Path(directory)
        (root / "sample.py").write_text("def sample():\n    return 1\n", encoding="utf-8")
        assert main(["knowledge", "refresh", "--workspace", str(root), "--mode", "propose"]) == 0
        assert "entities" in capsys.readouterr().out
        assert main(["knowledge", "query", "sample", "--workspace", str(root)]) == 0
        assert "sample" in capsys.readouterr().out
