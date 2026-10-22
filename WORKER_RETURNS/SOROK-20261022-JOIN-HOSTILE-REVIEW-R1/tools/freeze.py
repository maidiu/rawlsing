import hashlib
import json
import os
import subprocess
from pathlib import Path

RETURN = Path(__file__).resolve().parents[1]
REPO = RETURN.parents[1]
DEFAULT_CANDIDATE = REPO / "WORKER_RETURNS" / "SOROK-20261022-SAME-PERSON-JOIN-R1"
CANDIDATE = Path(
    os.environ.get("SOROK_JOIN_CANDIDATE_ROOT", str(DEFAULT_CANDIDATE))
).resolve()
CANDIDATE_COMMIT = "13dfd6bad54ec19b4bdf31159e54fb6052d5440d"


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def git_blob(path):
    return subprocess.run(
        ["git", "hash-object", str(path)],
        cwd=REPO,
        check=True,
        text=True,
        capture_output=True,
    ).stdout.strip()


def main():
    test_paths = [
        "tests/conftest.py",
        "tests/support.py",
        "tests/test_join_v_positive.py",
        "tests/test_join_v_hostile.py",
    ]
    candidate_paths = [
        "joined/session.py",
        "tests/test_join.py",
        "SOURCE_MANIFEST.json",
        "RESUME_CHECKPOINT.md",
    ]
    manifest = json.loads((CANDIDATE / "SOURCE_MANIFEST.json").read_text())
    rows = manifest["files"]
    missing = []
    mismatches = []
    checked = 0
    for row in rows:
        path = CANDIDATE / row["path"]
        if not path.exists():
            missing.append(row["path"])
            continue
        if git_blob(path) != row["git_blob"]:
            mismatches.append(row["path"])
            continue
        checked += 1

    document = {
        "schema": "SOROK_JOIN_V_FROZEN_ORACLES@1",
        "candidate_commit": CANDIDATE_COMMIT,
        "candidate_root": str(CANDIDATE),
        "candidate_files_sha256": {
            path: sha256(CANDIDATE / path) for path in candidate_paths
        },
        "test_files_sha256": {
            path: sha256(RETURN / path) for path in test_paths
        },
        "source_manifest": {
            "rows": len(rows),
            "verified": checked,
            "missing": missing,
            "mismatches": mismatches,
        },
    }
    path = RETURN / "FROZEN_ORACLES.json"
    path.write_text(json.dumps(document, indent=2, sort_keys=True) + "\n")
    print(json.dumps(document["source_manifest"], sort_keys=True))
    print(str(path))


if __name__ == "__main__":
    main()
