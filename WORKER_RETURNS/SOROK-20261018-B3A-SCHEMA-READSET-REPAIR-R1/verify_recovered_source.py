"""Exact sourcefile provenance gate for B3A independently scoped repair.

All copied files are original sourcefree research only; accepted engineering
scope does not issue native C8/C9 or developmental Rule A/T.
"""
import hashlib
import json
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = Path(os.environ["B3A_ORIGIN_SOURCE_ROOT"]).resolve()
EXACT_ROOT = "16f15a125ba54cdf17f5d41be2d851bbcd2240d7"
REPAIRED_INTEGRATION_BLOB = "d3a324bb93c17fdaf12670dd153aeb138d9c426a"

COPIED_ROOT = {
    "00_RETURN.md", "README.md", "run_repair.py",
    "test_schema_repair.py", "test_atomic.py", "test_projected_atomic.py",
    "atomic_worker.py", "candidate_version.json", "original_candidate_version.json",
    "repair_manifest.json", "input_manifest.json",
}
COPIED_DIRS = ("candidate", "frozen_review", "frozen_x3")


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def check():
    if not SRC.is_dir():
        raise RuntimeError("B3A_PINNED_ORIGIN_MISSING")
    paths = sorted(COPIED_ROOT | {
        path.relative_to(ROOT).as_posix()
        for folder in COPIED_DIRS
        for path in (ROOT / folder).rglob("*") if path.is_file() and
        not any(x in path.parts for x in ("__pycache__", ".runtime", "evidence"))
    })
    if len(paths) < 35:
        raise RuntimeError("B3A_RECOVERY_SOURCE_COUNT_BELOW_EXPECTED:" + str(len(paths)))
    for relative in paths:
        a = (ROOT / relative).read_bytes()
        b = (SRC / relative).read_bytes()
        if a != b:
            raise RuntimeError("B3A_SOURCE_CHANGED_OR_WRONG_ORIGIN:" + relative)
    actual = blob((ROOT / "candidate/integration.py").read_bytes())
    if actual != REPAIRED_INTEGRATION_BLOB:
        raise RuntimeError("B3A_INDEPENDENT_ACCEPTED_CODE_SHA_CHANGED")
    return {
        "status": "BYTE_EXACT_SOURCEFREE_REPAIR_RECOVERED",
        "original_commit": EXACT_ROOT,
        "accepted_repair_blob": REPAIRED_INTEGRATION_BLOB,
        "copied_files": len(paths),
        "source_sha": {x: blob((ROOT / x).read_bytes()) for x in paths},
        "native_scientific_issuance": "NO_GRANT",
        "repaired_scope": "SQLITE_ATOMIC_READSET_AND_SCHEMA_ONLY",
    }


if __name__ == "__main__":
    print(json.dumps(check(), sort_keys=True))
