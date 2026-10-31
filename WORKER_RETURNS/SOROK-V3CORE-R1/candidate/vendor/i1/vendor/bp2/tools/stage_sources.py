"""Stage the exact pinned upstream source closures for the BP2 joined producer.

Every staged file is read straight out of the pinned Git object for the exact
commit and path, then hashed. Nothing is re-authored. The resulting
``vendor/source_manifest.json`` records the origin commit, origin path, SHA-256
and Git blob SHA-1 so a later reader can re-verify the closure without trusting
this worker.

Usage:
    python3 tools/stage_sources.py stage
    python3 tools/stage_sources.py verify
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
RETURN = HERE.parent
REPO = next(p for p in RETURN.parents if (p / ".git").exists())
VENDOR = RETURN / "vendor"
MANIFEST = VENDOR / "source_manifest.json"

BP1 = "b4e07ef515e9464c7bc8177e394ac29f4a4af72a"
BP3 = "7faaa0722336231335d974bebc70c1282c79ce3e"
C9R = "6fa2939972ce5a2c0cc4f2b033946b276f1c2934"

BP1_BASE = "WORKER_RETURNS/SOROK-20261020-BP1-HISTORICAL-ACTOR-PRODUCTION-R1"
BP3_BASE = "WORKER_RETURNS/SOROK-20261020-BP3-C8-WRITER-TRUST-R1"
C9R_BASE = (
    "WORKER_RETURNS/SOROK-20261019-C9R-WHOLE-ACTOR-BOUNDARY-AND-CONSUMER-REPAIR-R1"
)

C9R_MODULES = (
    "__init__",
    "canon",
    "identity",
    "events",
    "conditioning",
    "response_rules",
    "target_rules",
    "transaction",
    "pipeline",
    "action_admission",
    "later_action",
    "release_gate",
    "native_custody",
)

# (origin commit, origin path relative to that commit, destination relative to vendor/)
FILES = [
    # ---- BP3: keyed exclusive writer, OUT9 consumer bridge, C9 ingress ----
    (BP3, f"{BP3_BASE}/c8_exclusive_writer.py", "bp3/c8_exclusive_writer.py"),
    (BP3, f"{BP3_BASE}/c9_event_ingress.py", "bp3/c9_event_ingress.py"),
    (BP3, f"{BP3_BASE}/vendor/outbox_prototype.py", "bp3/vendor/outbox_prototype.py"),
    (BP3, f"{BP3_BASE}/vendor/c8o_trusted_outbox.py", "bp3/vendor/c8o_trusted_outbox.py"),
    (BP3, f"{BP3_BASE}/vendor/c8_readonly_consumer.py", "bp3/vendor/c8_readonly_consumer.py"),
    # ---- BP1: two-actor historical production and C9 bridge ----
    *[
        (BP1, f"{BP1_BASE}/candidate/bp1/{name}.py", f"bp1/bp1/{name}.py")
        for name in ("__init__", "canon", "source", "ledger", "composer", "c9_bridge")
    ],
    # ---- G18 lab_sgi1 subset actually imported by BP1 ----
    *[
        (BP1, f"{BP1_BASE}/vendor/g18/candidate/lab_sgi1/{name}.py", f"g18/lab_sgi1/{name}.py")
        for name in ("__init__", "core", "history", "joint", "proposal")
    ],
    # ---- C9R: exact repaired candidate package ----
    *[
        (C9R, f"{C9R_BASE}/candidate/{name}.py", f"c9r/candidate/{name}.py")
        for name in C9R_MODULES
    ],
    # ---- C9R native zero-positive guard (imported by conditioning) ----
    (
        C9R,
        f"{C9R_BASE}/runtime/native/rawlsing_next/v3_psepf_zero_positive_guard.py",
        "native/rawlsing_next/v3_psepf_zero_positive_guard.py",
    ),
]


def _git(args: list[str], *, text: bool = False):
    result = subprocess.run(
        ["git", *args], cwd=str(REPO), capture_output=True, check=True
    )
    return result.stdout.decode("utf8") if text else result.stdout


def stage() -> dict:
    rows = []
    for commit, origin, dest in FILES:
        blob = _git(["show", f"{commit}:{origin}"])
        target = VENDOR / dest
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(blob)
        rows.append(
            {
                "origin_commit": commit,
                "origin_path": origin,
                "staged_path": dest,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "git_blob_sha1": hashlib.sha1(
                    b"blob %d\0" % len(blob) + blob
                ).hexdigest(),
                "size": len(blob),
            }
        )
    manifest = {
        "schema": "BP2_STAGED_SOURCE_MANIFEST@1",
        "repository": "maidiu/rawlsing",
        "origin_commits": {"BP1": BP1, "BP3": BP3, "C9R": C9R},
        "file_count": len(rows),
        "files": rows,
        "closure_note": (
            "Byte-exact copies of the pinned upstream files this candidate "
            "imports. No upstream engine is re-implemented, patched or edited."
        ),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    return manifest


def verify() -> tuple[bool, list[str]]:
    manifest = json.loads(MANIFEST.read_text())
    problems: list[str] = []
    for row in manifest["files"]:
        target = VENDOR / row["staged_path"]
        if not target.exists():
            problems.append("MISSING:" + row["staged_path"])
            continue
        blob = target.read_bytes()
        if hashlib.sha256(blob).hexdigest() != row["sha256"]:
            problems.append("SHA256_DRIFT:" + row["staged_path"])
            continue
        current = _git(["show", f"{row['origin_commit']}:{row['origin_path']}"])
        if current != blob:
            problems.append("ORIGIN_DRIFT:" + row["staged_path"])
    staged = {
        str(p.relative_to(VENDOR))
        for p in VENDOR.rglob("*.py")
        if p.is_file()
    }
    declared = {row["staged_path"] for row in manifest["files"]}
    for extra in sorted(staged - declared):
        problems.append("UNDECLARED_VENDOR_FILE:" + extra)
    return (not problems, problems)


def main(argv: list[str]) -> int:
    if len(argv) != 2 or argv[1] not in {"stage", "verify"}:
        print(__doc__)
        return 2
    if argv[1] == "stage":
        manifest = stage()
        print(f"staged {manifest['file_count']} files -> {MANIFEST}")
        ok, problems = verify()
        print("verify:", "OK" if ok else problems)
        return 0 if ok else 1
    ok, problems = verify()
    print("verify:", "OK" if ok else problems)
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
