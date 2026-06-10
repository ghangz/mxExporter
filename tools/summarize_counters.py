#!/usr/bin/env python3
"""Summarize mx-exporter counter CSV files as JSON."""

from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path


def summarize(path: Path) -> dict[str, object]:
    type_counts: Counter[str] = Counter()
    metric_names: list[str] = []
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.reader(handle):
            if not row or not "".join(row).strip() or row[0].lstrip().startswith("#"):
                continue
            if len(row) < 3:
                continue
            metric_type = row[1].strip()
            metric_name = row[2].strip()
            if metric_type and metric_name:
                type_counts[metric_type] += 1
                metric_names.append(metric_name)
    duplicates = sorted(name for name, count in Counter(metric_names).items() if count > 1)
    return {
        "path": str(path),
        "metric_count": len(metric_names),
        "type_counts": dict(sorted(type_counts.items())),
        "duplicate_metric_names": duplicates,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "mx_exporter" / "default-counters.csv",
    )
    parser.add_argument("--output", type=Path, help="write summary JSON to this path")
    args = parser.parse_args()

    if not args.path.is_file():
        parser.error(f"input file does not exist: {args.path}")

    payload = summarize(args.path)
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
