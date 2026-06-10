#!/usr/bin/env python3
"""Inventory Grafana dashboards shipped with mx-exporter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def inventory(root: Path) -> dict[str, object]:
    dashboards = []
    for path in sorted((root / "deployment" / "grafana-dashboard").glob("*.json")):
        try:
            data = json.loads(path.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError as exc:
            raise RuntimeError(f"Failed to parse JSON file {path}: {exc}") from exc
        panels = data.get("panels", [])
        dashboards.append(
            {
                "path": path.relative_to(root).as_posix(),
                "title": data.get("title", ""),
                "uid": data.get("uid", ""),
                "panel_count": len(panels),
            }
        )
    return {"dashboard_count": len(dashboards), "dashboards": dashboards}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    text = json.dumps(inventory(args.root), indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
