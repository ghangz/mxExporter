#!/usr/bin/env python3
"""Summarize key mx-exporter Helm values without external YAML dependencies."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def summarize(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace")
    return {
        "path": str(path),
        "repositories": re.findall(r"repository:\s*['\"]?([^'\"\s]+)", text),
        "tags": re.findall(r"tag:\s*['\"]?([^'\"\s]+)", text),
        "service_types": re.findall(r"type:\s*['\"]?([^'\"\s]+)", text),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "values",
        nargs="?",
        type=Path,
        default=Path("deployment/mx-exporter/helm/mx-exporter/values.yaml"),
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    text = json.dumps(summarize(args.values), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
