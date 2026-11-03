from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
if str(RETURN) not in sys.path:
    sys.path.insert(0, str(RETURN))

import install

install.install()

from bridge.readback import cold_verify


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _hashes(root: Path, label: str) -> dict:
    run_dir = root / "runs" / label
    paths = {
        "world.json": root / "world.json",
        "c12.sqlite": root / "c12.sqlite",
        "c9.sqlite": run_dir / "c9.sqlite",
        "run.json": run_dir / "run.json",
        "s35_receipt.json": run_dir / "s35_receipt.json",
    }
    return {
        name: _sha256(path) if path.exists() else ""
        for name, path in paths.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--world-root", required=True)
    parser.add_argument("--label", required=True)
    args = parser.parse_args()
    root = Path(args.world_root).resolve()
    before = _hashes(root, args.label)
    result = cold_verify(root, args.label)
    after = _hashes(root, args.label)
    result["fresh_process"] = True
    result["pid"] = os.getpid()
    result["store_hashes_before"] = before
    result["store_hashes_after"] = after
    result["store_mutated"] = before != after
    result["ok"] = bool(result.get("ok")) and not result["store_mutated"]
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
