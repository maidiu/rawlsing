#!/usr/bin/env python3
"""Reconstruct candidate identities and produce an independent normalized manifest."""
from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
RETURN = Path(__file__).resolve().parents[1]
EVID = RETURN / "evidence"
CANDIDATE = "efd12b1d46f1ccf90de14b292f600078f11ec7e0"
STARTUP = "6d95a78bf6b7bcf70022e303a151255e65edc38a"
AUTHOR_RETURN = "WORKER_RETURNS/PYAT-R56-R00E-GATE-IMPLEMENTATION-R1"


def git(*args):
    return subprocess.check_output(["git", "-c", "gc.auto=0", *args],
                                   cwd=str(ROOT), text=True).strip()


def sha256(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def blob(path):
    return git("rev-parse", f"{CANDIDATE}:{path}")


def main():
    changed = [line for line in git("diff", "--name-only", f"{STARTUP}..{CANDIDATE}").splitlines() if line]
    candidate_files = []
    for path in changed:
        file_path = ROOT / path
        candidate_files.append({
            "path": path,
            "git_blob_sha1": blob(path),
            "sha256": sha256(path),
            "bytes": file_path.stat().st_size,
        })
    sums_path = ROOT / AUTHOR_RETURN / "evidence/SHA256SUMS.txt"
    sums_entries = []
    if sums_path.exists():
        for line in sums_path.read_text().splitlines():
            parts = line.split("  ", 1)
            if len(parts) == 2:
                sums_entries.append({"sha256": parts[0], "path": parts[1]})
    stale = []
    missing_paths = []
    for entry in sums_entries:
        path = entry["path"]
        if path.startswith("../../"):
            path = path[6:]
        if path.startswith("WORKER_RETURNS/"):
            actual = ROOT / path
        elif path.startswith(("CROSS_HQ_CONTROL_ROOM/", "tests/", "WORKER_RETURNS/")):
            actual = ROOT / path
        else:
            actual = ROOT / AUTHOR_RETURN / path
        if not actual.exists():
            missing_paths.append(entry["path"])
        elif hashlib.sha256(actual.read_bytes()).hexdigest() != entry["sha256"]:
            stale.append({"path": entry["path"], "recorded": entry["sha256"],
                          "actual": hashlib.sha256(actual.read_bytes()).hexdigest()})
    author_manifest = ROOT / AUTHOR_RETURN / "manifest.json"
    normalized = {
        "schema": "R56_R00V_NORMALIZED_MANIFEST@1",
        "candidate_commit": CANDIDATE,
        "startup_commit": STARTUP,
        "author_manifest_json": "ABSENT" if not author_manifest.exists() else str(author_manifest.relative_to(ROOT)),
        "candidate_file_count": len(candidate_files),
        "candidate_files": candidate_files,
        "author_sha256sums": {
            "path": str(sums_path.relative_to(ROOT)) if sums_path.exists() else "ABSENT",
            "entries": len(sums_entries),
            "duplicate_paths": sorted({entry["path"] for entry in sums_entries
                                       if sum(1 for e in sums_entries if e["path"] == entry["path"]) > 1}),
            "missing_paths": missing_paths,
            "stale_entries": stale,
        },
        "reviewer_files": [
            {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
             "bytes": path.stat().st_size}
            for path in sorted((ROOT / "tests/universal_execution_oracle").rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts
        ] + [
            {"path": str(path.relative_to(ROOT)), "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
             "bytes": path.stat().st_size}
            for path in sorted(RETURN.rglob("*"))
            if path.is_file() and "__pycache__" not in path.parts and path.name != "normalized_manifest.json"
        ],
        "note": "Author manifest.json is absent. Candidate identities are reconstructed from Git and author SHA256SUMS; reviewer files are normalized separately.",
    }
    (EVID / "candidate_manifest_reconstruction.json").write_text(
        json.dumps(normalized, indent=2, sort_keys=True) + "\n", encoding="utf8")
    print(json.dumps({"candidate_files": len(candidate_files),
                      "author_manifest": "ABSENT" if not author_manifest.exists() else "PRESENT",
                      "sums_entries": len(sums_entries),
                      "missing": len(missing_paths), "stale": len(stale)}, indent=1))


if __name__ == "__main__":
    main()
