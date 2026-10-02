#!/usr/bin/env python3
"""Read-only integrity verification of this documentary delivery; never accesses sources."""
import hashlib
import json
from pathlib import Path

def verify(root):
    root = root.resolve()
    manifest = json.loads((root / "MANIFEST.json").read_text())
    seen = set()
    for entry in manifest["files"]:
        rel = Path(entry["path"])
        if rel.is_absolute() or ".." in rel.parts or str(rel) in seen:
            raise ValueError("unsafe or duplicate manifest path")
        seen.add(str(rel))
        path = (root / rel).resolve()
        if root not in path.parents:
            raise ValueError("path escapes packet")
        data = path.read_bytes()
        blob = hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()
        if hashlib.sha256(data).hexdigest() != entry["sha256"] or blob != entry["git_blob_sha1"]:
            raise ValueError("integrity mismatch: " + str(rel))
        if path.suffix == ".json":
            json.loads(data)
    required = {"HQ_START_HERE.md", "README.md", "FIRST_TASKS.json", "DELIVERY.json",
                "ACTIVATION_RUNBOOK.md", "scripts/verify_packet.py"}
    if not required <= seen:
        raise ValueError("required packet files missing")
    plan = json.loads((root / "FIRST_TASKS.json").read_text())
    done = set()
    for task in plan["tasks"]:
        if task["id"] in done or not set(task["depends_on"]) <= done:
            raise ValueError("duplicate task or invalid dependency order")
        done.add(task["id"])
    return len(seen)

if __name__ == "__main__":
    try:
        count = verify(Path(__file__).resolve().parents[1])
    except (ValueError, KeyError, OSError) as exc:
        raise SystemExit("FAIL: " + str(exc))
    print(f"PASS: {count} delivery files verified; activation and runtime qualification remain separate")

