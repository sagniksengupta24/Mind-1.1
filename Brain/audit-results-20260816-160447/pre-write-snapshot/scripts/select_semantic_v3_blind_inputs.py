"""Compatibility entry point for the repaired post-annotation selector.

The RC3 selector chose 120 inputs before annotation and is intentionally no
longer available. RC3.1 selects only after all candidate and reserve
annotations have reached a terminal state.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from rc3_1_pipeline import select_final


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Select exactly 120 accepted RC3.1 cases after frozen annotation"
    )
    parser.add_argument("--candidates", required=True)
    parser.add_argument("--old-inputs", required=True)
    parser.add_argument("--old-report", required=True)
    parser.add_argument("--old-labels", required=True)
    parser.add_argument("--reserve-inputs", required=True)
    parser.add_argument("--reserve-report", required=True)
    parser.add_argument("--reserve-labels", required=True)
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    result = select_final(
        candidates_path=Path(args.candidates),
        old_inputs_path=Path(args.old_inputs),
        old_report_path=Path(args.old_report),
        old_labels_path=Path(args.old_labels),
        reserve_inputs_path=Path(args.reserve_inputs),
        reserve_report_path=Path(args.reserve_report),
        reserve_labels_path=Path(args.reserve_labels),
        output_dir=Path(args.output_dir),
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
