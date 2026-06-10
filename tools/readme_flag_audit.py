#!/usr/bin/env python3
"""Compare CLI flags with README examples and parameter notes."""

from __future__ import annotations

import argparse
import ast
import json
import re
from pathlib import Path


FLAG_RE = re.compile(r"-{1,2}[A-Za-z0-9-]+")


def cli_flags(init_path: Path) -> set[str]:
    module = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    flags = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Attribute) or node.func.attr != "add_argument":
            continue
        for argument in node.args:
            if isinstance(argument, ast.Constant) and isinstance(argument.value, str):
                flags.add(argument.value)
    return flags


def readme_flags(readme_path: Path) -> set[str]:
    return set(FLAG_RE.findall(readme_path.read_text(encoding="utf-8")))


def build(repo_root: Path) -> dict[str, object]:
    cli = cli_flags(repo_root / "mx_exporter" / "__init__.py")
    readme = readme_flags(repo_root / "README.md")
    return {
        "cli_flag_count": len(cli),
        "readme_flag_count": len(readme),
        "flags_missing_from_readme": sorted(flag for flag in cli - readme if flag.startswith("-")),
        "flags_only_in_readme": sorted(flag for flag in readme - cli if flag.startswith("-")),
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
