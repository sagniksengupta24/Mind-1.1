from __future__ import annotations

import argparse
import json
from pathlib import Path

from rc3_1_pipeline import seal_package


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Fail-closed RC3.1 blind sealer; final selection must already contain 120 accepted cases"
    )
    parser.add_argument("--selection-dir", required=True)
    parser.add_argument("--contamination-report", required=True)
    parser.add_argument("--evaluator-identity", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = seal_package(
        Path(args.selection_dir),
        Path(args.contamination_report),
        Path(args.evaluator_identity),
        Path(args.output_dir),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
