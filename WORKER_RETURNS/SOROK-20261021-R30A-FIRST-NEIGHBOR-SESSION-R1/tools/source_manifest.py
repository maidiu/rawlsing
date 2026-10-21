#!/usr/bin/env python3
"""Write the exact R29P vendor and live-module source manifest."""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = next(p for p in ROOT.parents if (p / ".git").exists())
VENDOR = ROOT / "vendor" / "r29p"
R29P_REF = "001b506fa26ae879ff5b6e57138fc2696e12b538"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git_blob(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def main():
    files = {}
    for path in sorted(VENDOR.rglob("*")):
        if path.is_file() and "__pycache__" not in path.parts:
            files[str(path.relative_to(VENDOR))] = sha256(path)
    live = {}
    for relative in ("rawlsing_next/m6_actor_safe_expression.py",
                     "rawlsing_next/v3_psepf_zero_positive_guard.py"):
        path = REPO / relative
        live[relative] = {"blob": git_blob(path), "sha256": sha256(path)}
    payload = {
        "schema": "R30A_SOURCE_MANIFEST@1",
        "r29p_source_ref": R29P_REF,
        "r29p_return": "WORKER_RETURNS/SOROK-20261021-R29P-ACTOR-C12-USER-PRODUCT-R1",
        "vendor_root": "vendor/r29p",
        "vendor_file_count": len(files),
        "vendor_files": files,
        "live_module_pins": live,
        "note": "R29P code is copied read-only into this return for executable custody. "
                "The original R29P branch/head remains untouched.",
    }
    (ROOT / "evidence" / "source_manifest.json").parent.mkdir(parents=True, exist_ok=True)
    (ROOT / "evidence" / "source_manifest.json").write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({"vendor_files": len(files), "live": live}, indent=1))


if __name__ == "__main__":
    main()
