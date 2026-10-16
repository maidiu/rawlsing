#!/usr/bin/env python3
"""OC7 independent staging of the OC6 candidate under review + its author controls."""
import hashlib
import json
import os
import subprocess
import sys

REPO = os.environ["OC7_REPO"]
OUT = os.environ["OC7_STAGE"]

# (commit, repo_path, staged_name, expected_git_blob_sha1, expected_sha256)
OC6 = [
    (
        "c6cb15d7417595c359571e4525dd0f0fd6c59d1f",
        "WORKER_RETURNS/SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1/repro/custody_protocol.py",
        "custody_protocol.OC6_REPAIRED.py",
        "4c185c18dbee57603038e97886da8fc4aa834082",
        "ca85b844994e5ce6fd9e7a21c0f210d08b6d5e7519c63ac09d7dd8a9516fd90b",
    ),
    (
        "c6cb15d7417595c359571e4525dd0f0fd6c59d1f",
        "WORKER_RETURNS/SOROK-R3-HQ313-OC6-NATIVE-INPUT-CONTRACT-REPAIR-R1/tests/test_oc6_input_contract_controls.py",
        "test_oc6_author_controls.py",
        None,
        None,
    ),
]


def git_blob_sha1(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\x00" + data).hexdigest()


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    ledger, failures = [], []
    for commit, path, staged, eblob, esha in OC6:
        data = subprocess.run(
            ["git", "-C", REPO, "cat-file", "blob", f"{commit}:{path}"],
            check=True, capture_output=True,
        ).stdout
        blob = git_blob_sha1(data)
        store = subprocess.run(
            ["git", "-C", REPO, "rev-parse", f"{commit}:{path}"],
            check=True, capture_output=True, text=True,
        ).stdout.strip()
        sha = hashlib.sha256(data).hexdigest()
        ok = blob == store
        if eblob:
            ok = ok and blob == eblob and sha == esha
        if not ok:
            failures.append(staged)
        with open(os.path.join(OUT, staged), "wb") as fh:
            fh.write(data)
        ledger.append({
            "kind": "git_blob", "commit": commit, "repo_path": path,
            "staged": staged, "bytes": len(data),
            "computed_git_blob_sha1": blob, "git_store_blob_sha1": store,
            "declared_git_blob_sha1": eblob, "computed_sha256": sha,
            "declared_sha256": esha, "all_match": ok,
        })
        print(f"{'OK  ' if ok else 'FAIL'} {staged:38s} blob={blob} bytes={len(data)} sha256={sha[:16]}...")

    with open(os.path.join(OUT, "_stage_oc6_ledger.json"), "w") as fh:
        json.dump({"ledger": ledger, "failures": failures}, fh, indent=2)
    if failures:
        print("FAILURES:", failures)
        return 1
    print("OC6 CANDIDATE STAGED + VERIFIED")
    return 0


if __name__ == "__main__":
    sys.exit(main())
