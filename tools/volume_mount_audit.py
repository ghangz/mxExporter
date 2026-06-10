#!/usr/bin/env python3
"""Compare static and Helm volume mounts for mx-exporter."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def extract_mounts(text: str) -> list[dict[str, str]]:
    mounts = []
    current_name = None
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if line.startswith('- name: "') and line.endswith('"'):
            current_name = line.split('"')[1]
            continue
        if current_name and line.startswith('mountPath: "') and line.endswith('"'):
            mounts.append({"name": current_name, "path": line.split('"')[1]})
            current_name = None
    return mounts


def build(repo_root: Path) -> dict[str, object]:
    static_text = (repo_root / "deployment" / "mx-exporter" / "mx-exporter-daemonset.yaml").read_text(encoding="utf-8")
    helm_text = (repo_root / "deployment" / "mx-exporter" / "helm" / "mx-exporter" / "templates" / "daemonset.yaml").read_text(encoding="utf-8")
    static_mounts = extract_mounts(static_text)
    helm_mounts = extract_mounts(helm_text)
    static_names = {mount["name"] for mount in static_mounts}
    helm_names = {mount["name"] for mount in helm_mounts}
    return {
        "static_mount_count": len(static_mounts),
        "helm_mount_count": len(helm_mounts),
        "only_in_static": sorted(static_names - helm_names),
        "only_in_helm": sorted(helm_names - static_names),
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
