"""Stage the exact pinned BP2 and BP4 return closures into this return.

Every staged byte is read from the pinned Git object and hashed. Nothing is
re-authored, patched or re-derived. ``vendor/source_manifest.json`` records the
origin commit, origin path, SHA-256, Git blob SHA-1 and size so an independent
reader can re-verify the closure without trusting this worker.

Local-only runtime roots (``evidence/runtime/``) are deliberately excluded: they
contain a random TEST_ONLY key and path-bound SQLite/journal state, not source.

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

BP2_COMMIT = "5065e2e6934e9d5bca800cbf88c79e461bcf2393"
BP4_COMMIT = "d868e82c7c83def2df18295244d93af9706e647f"
BP2_BASE = "WORKER_RETURNS/SOROK-20261020-BP2-JOINED-ACTOR-EVENT-RULE-ACTION-R1"
BP4_BASE = "WORKER_RETURNS/SOROK-20261020-BP4-C10-C12-A0-A3-CONSUMER-R1"
EXCLUDED_PREFIXES = {
    BP2_COMMIT: (f"{BP2_BASE}/evidence/runtime/",),
    BP4_COMMIT: (f"{BP4_BASE}/evidence/runtime/",),
}


def _git(args: list[str], *, text: bool = False):
    completed = subprocess.run(["git", *args], cwd=str(REPO),
                               capture_output=True, check=True)
    return completed.stdout.decode("utf8") if text else completed.stdout


def _files(commit: str, base: str) -> list[str]:
    out = _git(["ls-tree", "-r", "--name-only", commit, base], text=True)
    excluded = EXCLUDED_PREFIXES.get(commit, ())
    rows = []
    for path in out.splitlines():
        if not path or path.endswith("/"):
            continue
        if any(path.startswith(prefix) for prefix in excluded):
            continue
        if "/__pycache__/" in path or path.endswith(".pyc"):
            continue
        rows.append(path)
    return sorted(rows)


def stage() -> dict:
    rows = []
    for commit, base, prefix in (
        (BP2_COMMIT, BP2_BASE, "bp2"),
        (BP4_COMMIT, BP4_BASE, "bp4"),
    ):
        for origin in _files(commit, base):
            blob = _git(["show", f"{commit}:{origin}"])
            relative = origin[len(base) + 1:]
            destination = VENDOR / prefix / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(blob)
            rows.append({
                "origin_commit": commit,
                "origin_path": origin,
                "staged_path": f"{prefix}/{relative}",
                "sha256": hashlib.sha256(blob).hexdigest(),
                "git_blob_sha1": hashlib.sha1(b"blob %d\0" % len(blob) + blob).hexdigest(),
                "size": len(blob),
            })
    manifest = {
        "schema": "BP2P4J_STAGED_SOURCE_MANIFEST@1",
        "repository": "maidiu/rawlsing",
        "origin_commits": {"BP2": BP2_COMMIT, "BP4": BP4_COMMIT},
        "file_count": len(rows),
        "files": rows,
        "closure_note": (
            "Byte-exact copies of the two pinned upstream returns. No upstream "
            "engine, test or semantic document is re-implemented or edited. "
            "Local runtime roots containing random TEST_ONLY keys are excluded."),
    }
    MANIFEST.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                        encoding="utf8")
    return manifest


def verify() -> tuple[bool, list[str]]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf8"))
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
        origin = _git(["show", f"{row['origin_commit']}:{row['origin_path']}"])
        if origin != blob:
            problems.append("ORIGIN_DRIFT:" + row["staged_path"])
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
