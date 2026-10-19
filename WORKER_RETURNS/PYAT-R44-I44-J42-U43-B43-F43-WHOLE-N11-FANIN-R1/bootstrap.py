"""R44 I44 bootstrap: repo root, pinned return paths, executable input materialization.

The five R42/R43 returns are NOT in the R44 startup tree; they live on their own
pushed branches in the same shared Git object store. This module:

* resolves the repository root and this return's directory,
* materializes each pinned return at its canonical ``WORKER_RETURNS/<dir>`` path
  from its exact commit (``git archive``) when absent,
* materializes U43's new candidate module ``rawlsing_next/pre553_issued_workload.py``
  from U43's commit when absent,
* exposes the exact pin table used by every preimage verification.

Nothing here trusts a working-tree copy: ``i44_integration`` verifies every
consumed artifact against its Git blob SHA-1, byte length and SHA-256 at the
pinned commit.
"""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

RETURN_DIR = Path(__file__).resolve().parent


def _repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "rawlsing_next").is_dir() and (candidate / "WORKER_RETURNS").is_dir():
            return candidate
    raise RuntimeError("repo root not found from I44 return")


ROOT = _repo_root()

PINS = {
    "A42": {
        "commit": "843175b0587b54db3df1f461ad9f7f1314894372",
        "dir": "WORKER_RETURNS/PYAT-R42-A42-WHOLE-ESTATE-RETURN-FANIN-AND-N11-CANDIDATE-R1",
        "grade": "UNCHANGED_N11_ASSESSOR",
    },
    "J42": {
        "commit": "f53cb0d2bce52640268c844c398bbd8007d28edc",
        "dir": "WORKER_RETURNS/PYAT-R42-J42-COMPLETE-E41-W41-P41-ACTUAL-JOINT-PREV3-CONSUMER-R1",
        "grade": "SOURCEFREE_TESTONLY_JOINED_RETURN",
    },
    "U43": {
        "commit": "dcf71f1afbfdbe8a084844cea5fffbc73d9d91ef",
        "dir": "WORKER_RETURNS/PYAT-R43-U43-ORIGINAL35-PROSPECTIVE-WORKLOAD-R1",
        "grade": "RETAINED_RESEARCH_FRONTIER_AND_DESCRIPTOR_REPAIR",
    },
    "B43": {
        "commit": "0fa15c1eda1ca36d89b0bbd948b655aa68f17370",
        "dir": "WORKER_RETURNS/PYAT-R43-B43-SELECTED-ROUTE-B-ORIGINAL35-SOURCE-POSITIVE-ENDTOEND-R1",
        "grade": "SOURCE_PENDING_EXECUTABLE_FEEDER",
    },
    "F43": {
        "commit": "c0271e2b8d59018d3cf2af7b366258ea503295a6",
        "dir": "WORKER_RETURNS/PYAT-R43-F43-SOURCE-QUALIFIED-OBJECTIVE-WORLD-R1",
        "grade": "BOUNDED_F5_F6_F7_CANDIDATE",
    },
}

U43_ISSUED_WORKLOAD = {
    "commit": PINS["U43"]["commit"],
    "path": "rawlsing_next/pre553_issued_workload.py",
}

REPO_RELATIVE_RETURN = RETURN_DIR.relative_to(ROOT).as_posix()


def path_for(name: str) -> Path:
    return ROOT / PINS[name]["dir"]


def _git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True)


def commit_exists(commit: str) -> bool:
    return _git("cat-file", "-t", commit).returncode == 0


def materialize(name: str) -> Path:
    pin = PINS[name]
    target = path_for(name)
    if target.is_dir() and any(target.iterdir()):
        return target
    if not commit_exists(pin["commit"]):
        raise RuntimeError(f"PINNED_COMMIT_UNAVAILABLE:{name}:{pin['commit']}")
    target.parent.mkdir(parents=True, exist_ok=True)
    archive = _git("archive", pin["commit"], pin["dir"])
    if archive.returncode != 0:
        raise RuntimeError(f"PINNED_ARCHIVE_FAILED:{name}:{archive.stderr.decode()[:300]}")
    extract = subprocess.run(
        ["tar", "-x", "-C", str(target.parent)],
        input=archive.stdout, capture_output=True,
    )
    if extract.returncode != 0:
        raise RuntimeError(f"PINNED_EXTRACT_FAILED:{name}:{extract.stderr.decode()[:300]}")
    return target


def materialize_u43_module() -> Path:
    target = ROOT / U43_ISSUED_WORKLOAD["path"]
    if target.is_file():
        return target
    archive = _git("show", f"{U43_ISSUED_WORKLOAD['commit']}:{U43_ISSUED_WORKLOAD['path']}")
    if archive.returncode != 0:
        raise RuntimeError("U43_ISSUED_WORKLOAD_UNAVAILABLE")
    target.write_bytes(archive.stdout)
    return target


def ensure_inputs() -> dict[str, Path]:
    paths = {name: materialize(name) for name in PINS}
    materialize_u43_module()
    return paths


def ensure_sys_path() -> None:
    for path in (str(ROOT), str(RETURN_DIR), str(path_for("A42")), str(path_for("B43")),
                 str(path_for("F43")), str(path_for("J42")), str(path_for("U43"))):
        if path not in sys.path:
            sys.path.insert(0, path)


if __name__ == "__main__":
    paths = ensure_inputs()
    print(json.dumps({name: str(path.relative_to(ROOT)) for name, path in paths.items()}, indent=2))
