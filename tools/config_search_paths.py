#!/usr/bin/env python3
"""Export the default counter-config search paths used by mx-exporter."""

from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path


def build(repo_root: Path) -> dict[str, object]:
    init_path = repo_root / "mx_exporter" / "__init__.py"
    module = ast.parse(init_path.read_text(encoding="utf-8"), filename=str(init_path))
    for node in ast.walk(module):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "default_config_files":
                    values = [ast.unparse(value) for value in node.value.elts]
                    return {"path_count": len(values), "paths": values}
    raise ValueError("default_config_files not found")


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
