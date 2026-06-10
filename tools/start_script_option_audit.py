#!/usr/bin/env python3
"""Compare documented and implemented start_mxexporter.sh options."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


TOKEN_RE = re.compile(r"--[A-Za-z0-9-]+|-[A-Za-z0-9]+")


def parse_documented(text: str) -> set[str]:
    items = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("--") or line.endswith(")") or ":)" in line:
            continue
        definition = line.split(maxsplit=1)[0]
        items.update(TOKEN_RE.findall(definition))
    return items


def parse_implemented(text: str) -> set[str]:
    items = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.endswith(")") or not line.startswith("-"):
            continue
        items.update(TOKEN_RE.findall(line))
    return items


def build(repo_root: Path) -> dict[str, object]:
    script_text = (repo_root / "start_mxexporter.sh").read_text(encoding="utf-8")
    documented = parse_documented(script_text)
    implemented = parse_implemented(script_text)
    return {
        "documented_count": len(documented),
        "implemented_count": len(implemented),
        "undocumented_options": sorted(implemented - documented),
        "stale_documentation": sorted(documented - implemented),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=Path("."))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    text = json.dumps(build(args.repo_root), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
