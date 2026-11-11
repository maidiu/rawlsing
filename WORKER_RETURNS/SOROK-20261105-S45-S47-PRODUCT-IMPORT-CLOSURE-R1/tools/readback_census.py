#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

EXCLUDED = ("READBACK.json",)


def included(path: Path, root: Path) -> bool:
    if not path.is_file():
        return False
    rel = path.relative_to(root)
    if "__pycache__" in rel.parts:
        return False
    if str(rel) in EXCLUDED:
        return False
    return True


def census(root: Path) -> dict:
    root = root.resolve()
    rows = []
    for path in sorted(root.rglob("*")):
        if not included(path, root):
            continue
        rows.append({
            "path": str(path.relative_to(root)),
            "bytes": path.stat().st_size,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    return {
        "schema": "SOROK_S45_S47_PUBLICATION_CENSUS@1",
        "root": str(root),
        "definition": (
            "all regular files under root, excluding READBACK.json and any path "
            "containing a __pycache__ component; .local-logs is outside this root"
        ),
        "excluded": list(EXCLUDED) + ["**/__pycache__/**"],
        "file_count": len(rows),
        "total_bytes": sum(row["bytes"] for row in rows),
        "files": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
    )
    parser.add_argument("--files", action="store_true")
    args = parser.parse_args()
    report = census(args.root)
    if not args.files:
        report.pop("files", None)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
