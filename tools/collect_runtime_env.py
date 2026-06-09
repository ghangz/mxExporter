#!/usr/bin/env python3
"""Collect mx-exporter runtime diagnostics as JSON."""

from __future__ import annotations

import argparse
import ctypes.util
import json
import os
import platform
import sys
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path


def package_version(name: str) -> dict[str, str | bool]:
    try:
        return {"installed": True, "version": version(name)}
    except PackageNotFoundError:
        return {"installed": False}


def path_exists(path: str | None) -> bool:
    return bool(path and Path(path).exists())


def collect() -> dict:
    maca_path = os.environ.get("MACA_PATH")
    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "python": sys.version,
            "executable": sys.executable,
        },
        "environment": {
            "MACA_PATH": maca_path,
            "LD_LIBRARY_PATH": os.environ.get("LD_LIBRARY_PATH"),
            "PATH": os.environ.get("PATH"),
        },
        "paths": {
            "maca_path_exists": path_exists(maca_path),
            "dev_dri_exists": Path("/dev/dri").exists(),
            "default_counters_exists": Path(__file__).resolve().parents[1]
            .joinpath("mx_exporter", "default-counters.csv")
            .exists(),
        },
        "libraries": {
            "mxsml": ctypes.util.find_library("mxsml"),
        },
        "python_packages": {
            "prometheus_client": package_version("prometheus_client"),
            "grpcio": package_version("grpcio"),
            "protobuf": package_version("protobuf"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect mx-exporter runtime diagnostics.")
    parser.add_argument("--output", type=Path, help="Optional JSON output path.")
    parser.add_argument("--pretty", action="store_true")
    args = parser.parse_args()

    text = json.dumps(collect(), indent=2 if args.pretty else None, sort_keys=True)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
