#!/usr/bin/env python3
"""Audit mx-exporter port defaults across code and deployment files."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CLI_RE = re.compile(r'parser\.add_argument\("-p".*default=(\d+)')
SCRIPT_RE = re.compile(r"HOST_PORT=(\d+)")
YAML_PORT_RE = re.compile(r"(?:port|containerPort):\s*(\d+)")


def build(repo_root: Path) -> dict[str, object]:
    cli_text = (repo_root / "mx_exporter" / "__init__.py").read_text(encoding="utf-8")
    script_text = (repo_root / "start_mxexporter.sh").read_text(encoding="utf-8")
    static_text = (repo_root / "deployment" / "mx-exporter" / "mx-exporter-daemonset.yaml").read_text(encoding="utf-8")

    cli_default = int(CLI_RE.search(cli_text).group(1))
    script_default = int(SCRIPT_RE.search(script_text).group(1))
    static_ports = sorted({int(value) for value in YAML_PORT_RE.findall(static_text)})
    aligned = script_default == cli_default and all(port == cli_default for port in static_ports)
    return {
        "cli_default_port": cli_default,
        "script_default_port": script_default,
        "static_ports": static_ports,
        "aligned": aligned,
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
