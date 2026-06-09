#!/usr/bin/env python3
"""Audit Kubernetes and Helm manifests for mx-exporter image references."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


IMAGE_RE = re.compile(r"^\s*image:\s*['\"]?([^'\"\s]+)", re.MULTILINE)


def collect_images(root: Path) -> list[dict[str, str]]:
    images: list[dict[str, str]] = []
    for path in sorted((root / "deployment").rglob("*")):
        if path.suffix not in {".yaml", ".yml"}:
            continue
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in IMAGE_RE.finditer(text):
            images.append({"path": path.relative_to(root).as_posix(), "image": match.group(1)})
    return images


def audit(root: Path) -> dict[str, object]:
    images = collect_images(root)
    exporter_images = sorted({item["image"] for item in images if "exporter" in item["path"].lower()})
    return {
        "image_count": len(images),
        "images": images,
        "mx_exporter_images": exporter_images,
        "mx_exporter_image_count": len(exporter_images),
        "mx_exporter_image_consistent": len(exporter_images) <= 1,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--strict", action="store_true", help="return non-zero when mx-exporter images differ")
    parser.add_argument("--output", type=Path, help="write audit JSON to this path")
    args = parser.parse_args()

    payload = audit(args.root)
    text = json.dumps(payload, indent=2, ensure_ascii=False)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 1 if args.strict and not payload["mx_exporter_image_consistent"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
