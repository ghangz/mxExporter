#!/usr/bin/env python3
"""Lint mx-exporter counter CSV files."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


VALID_TYPES = {"Gauge", "Counter", "Summary", "Histogram", "Info"}


def lint_counter_file(path: Path) -> list[str]:
    errors: list[str] = []
    seen_ids: set[str] = set()

    with path.open(newline="", encoding="utf-8") as handle:
        for line_no, row in enumerate(csv.reader(handle), start=1):
            if not row or not "".join(row).strip() or row[0].lstrip().startswith("#"):
                continue
            if len(row) < 4:
                errors.append(f"{line_no}: expected at least 4 columns, got {len(row)}")
                continue

            metric_id = row[0].strip()
            metric_type = row[1].strip()
            metric_name = row[2].strip()
            if metric_id in seen_ids:
                errors.append(f"{line_no}: duplicate metric id {metric_id!r}")
            seen_ids.add(metric_id)

            if metric_type not in VALID_TYPES:
                errors.append(f"{line_no}: invalid metric type {metric_type!r}")
            if not metric_name:
                errors.append(f"{line_no}: empty prometheus metric name")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Lint mx-exporter counter CSV files.")
    parser.add_argument(
        "path",
        nargs="?",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "mx_exporter" / "default-counters.csv",
    )
    args = parser.parse_args()

    errors = lint_counter_file(args.path)
    if errors:
        print(f"Counter lint failed for {args.path}:", file=sys.stderr)
        for error in errors:
            print(f"  {error}", file=sys.stderr)
        return 1

    print(f"Counter lint passed for {args.path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
