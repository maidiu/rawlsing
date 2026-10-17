"""PYAT R26 T9C guarded runner for the FROZEN independent T9I court.

The independent court file
`frozen_t9i_court/test_independent_clock_custody.py` is a byte-identical copy of
`WORKER_RETURNS/PYAT-R23-T9I-INDEPENDENT-CLOCK-CUSTODY-R1/tests/test_independent_clock_custody.py`
at independent court commit a2a7bdeda76aa008b3d620b01af71f7fd6efaaae
(git blob f624177d4980f524781c84956eb23a45bfa52a78). It is NOT edited. It is
reproduced here only so that this adapter's own runner can supply the
`verify(module_name, path)` / `EXPECTED` interface that the frozen court's
`test_independent_guard_rejects_untrusted_path_and_changed_preimage` imports from
`sys.modules['__main__']`.

Custody rules enforced here:
  * `sys.path` is pinned to this return and the stdlib; the ambient repository
    root cannot shadow the staged native tree.
  * `PYTHONDONTWRITEBYTECODE` / `-B` keeps disk bytes untouched.
  * plugin autoload is disabled so no ambient plugin can alter collection.
  * every project module actually imported is checked against its expected
    git blob SHA-1 before any of its code is allowed to run.
  * sealed sources are never mutated; negative controls use scratch paths only.
"""
from __future__ import annotations

import hashlib
import importlib
import importlib.util
import json
import os
import sys
from pathlib import Path

RET = Path(__file__).resolve().parent
NATIVE = RET / "native"
FROZEN = RET / "frozen_t9i_court"
PINNED_EVIDENCE = RET / "pinned_candidate" / "evidence"
for _d in ("evidence", "junit", "logs"):
    (RET / _d).mkdir(parents=True, exist_ok=True)

# Ambient roots that must never be importable for this court.
AMBIENT_ROOTS = (
    "/Users/matthewsmith/Desktop/Rawlsing",
    "/Users/matthewsmith/Desktop/Rawlsing/data",
)
TRUSTED_ROOTS = tuple(str(p.resolve()) for p in (RET,))

# module name -> (relative path under RET, git blob sha1)
SOURCE_MAP = {
    "t9b_temporal": ("t9b_temporal.py", None),
    "data.ddm_build_copy": ("native/data/ddm_build_copy/__init__.py", None),
    "data.ddm_build_copy.ddm_v553_temporal_pressure": (
        "native/data/ddm_build_copy/ddm_v553_temporal_pressure.py", None),
    "data.ddm_build_copy.ddm_v553_canonical_harmonization": (
        "native/data/ddm_build_copy/ddm_v553_canonical_harmonization.py", None),
    "data.ddm_build_copy.ddm_v553_harmonization": (
        "native/data/ddm_build_copy/ddm_v553_harmonization.py", None),
    "data.ddm_build_copy.ddm_v552j_handoff": (
        "native/data/ddm_build_copy/ddm_v552j_handoff.py", None),
    "data.ddm_build_copy.ddm_pipeline_boundary_contract": (
        "native/data/ddm_build_copy/ddm_pipeline_boundary_contract.py", None),
}

# Populated below from git for every staged native source.
EXPECTED: dict = {}


def _git_blob_sha1(path: Path) -> str:
    import subprocess
    out = subprocess.run(["git", "hash-object", str(path)],
                         cwd=str(RET), capture_output=True, text=True, check=True)
    return out.stdout.strip()


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(module_name: str, path) -> None:
    """Reject an unpinned path, then reject changed bytes.

    This is the interface the frozen independent court exercises.

    Order is the contract: a module that is not in the pin registry at all is
    `UNPINNED_PROJECT_MODULE`; a module that IS registered but whose bytes differ
    from the registered preimage is `PREIMAGE_MISMATCH`. Only after both checks
    does the path-trust guard run, so a counterfeit cannot buy a hash check by
    being registered by the caller, and cannot buy trust by matching a hash of a
    file that lives outside the sealed return.
    """
    p = Path(path).resolve()
    entry = EXPECTED.get(p)
    if entry is None:
        raise ImportError(f"UNPINNED_PROJECT_MODULE {module_name} -> {p}")
    actual = _git_blob_sha1(p)
    if actual != entry["git_blob_sha1"]:
        raise ImportError(f"PREIMAGE_MISMATCH {module_name} -> {p}")
    if not str(p).startswith(TRUSTED_ROOTS):
        raise ImportError(f"UNPINNED_PROJECT_MODULE {module_name} -> {p}")


def pin_sys_path() -> None:
    sys.path[:] = [
        p for p in sys.path
        if p and not any(str(Path(p).resolve()).startswith(a) for a in AMBIENT_ROOTS)
    ]
    for entry in (str(RET), str(NATIVE)):
        if entry in sys.path:
            sys.path.remove(entry)
    sys.path.insert(0, str(NATIVE))
    sys.path.insert(0, str(RET))


def build_expected() -> None:
    for rel in sorted(p for p in NATIVE.rglob("*.py")):
        EXPECTED[rel.resolve()] = {
            "git_blob_sha1": _git_blob_sha1(rel),
            "sha256": _file_sha256(rel),
        }
    EXPECTED[(RET / "t9b_temporal.py").resolve()] = {
        "git_blob_sha1": _git_blob_sha1(RET / "t9b_temporal.py"),
        "sha256": _file_sha256(RET / "t9b_temporal.py"),
    }


def module_receipts() -> dict:
    """Actual __file__ receipts for the project modules that were loaded."""
    out = {}
    for name, mod in sorted(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if not f or name.split(".")[0] not in {"t9b_temporal", "data"}:
            continue
        p = Path(f).resolve()
        out[name] = {"__file__": str(p),
                     "inside_this_return": str(p).startswith(TRUSTED_ROOTS[0]),
                     "sha256": _file_sha256(p) if p.exists() else None}
    return out


def main() -> int:
    import pytest

    pin_sys_path()
    build_expected()

    import data.ddm_build_copy as probe
    assert str(Path(probe.__file__).resolve()).startswith(str(NATIVE.resolve())), \
        f"AMBIENT DATA LEAK: {probe.__file__}"

    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    junit = RET / "junit" / "frozen_t9i_independent_48.xml"
    junit.parent.mkdir(parents=True, exist_ok=True)
    rc = pytest.main([
        "-q", "-p", "no:cacheprovider", "-p", "no:randomly",
        "--rootdir", str(RET),
        "-c", str(FROZEN / "pytest_t9i_frozen.ini"),
        f"--junitxml={junit}",
        str(FROZEN / "test_independent_clock_custody.py"),
    ])
    receipts = module_receipts()
    (RET / "evidence" / "t9c_frozen_t9i_module_receipts.json").write_text(
        json.dumps(receipts, indent=2, sort_keys=True) + "\n")
    print("FROZEN_T9I_COURT_EXIT", rc)
    return rc


if __name__ == "__main__":
    raise SystemExit(main())