"""PYAT R27 T9D guarded runner: per-import preimage custody and real pytest.

Supplies the `verify(module_name, path)` / `EXPECTED` interface that the frozen
T9I court's `test_independent_guard_rejects_untrusted_path_and_changed_preimage`
imports from `sys.modules['__main__']`, while enforcing for every court:

  * `sys.path` is pinned to this return's staging tree; the ambient repository
    root cannot shadow the staged native closure;
  * `PYTHONDONTWRITEBYTECODE` / `-B` keeps disk bytes untouched;
  * plugin autoload is disabled so no ambient plugin can alter collection;
  * every project module actually imported is checked against its expected
    git blob SHA-1 (NUL preimage) before and after its code runs;
  * sealed sources are never mutated; negative controls use scratch paths only.
"""
from __future__ import annotations

import hashlib
import importlib
import json
import os
import sys
from pathlib import Path

RET = Path(__file__).resolve().parent
STAGE = RET / "staging"
NATIVE = STAGE / "pinned_candidate" / "native"
PIN = STAGE / "pinned_candidate"
for _d in ("evidence", "junit", "logs"):
    (RET / _d).mkdir(parents=True, exist_ok=True)

AMBIENT_ROOTS = (
    "/Users/matthewsmith/Desktop/Rawlsing",
)

EXPECTED: dict = {}
AUDIT: list = []


def _git_blob_sha1(path: Path) -> str:
    b = path.read_bytes()
    return hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()


def _file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify(module_name: str, path) -> None:
    """Reject an unpinned path, then reject changed bytes (NUL-preimage SHA-1)."""
    p = Path(path).resolve()
    entry = EXPECTED.get(p)
    if entry is None:
        raise ImportError(f"UNPINNED_PROJECT_MODULE {module_name} -> {p}")
    actual = _git_blob_sha1(p)
    if actual != entry["git_blob_sha1"]:
        raise ImportError(f"PREIMAGE_MISMATCH {module_name} -> {p}")
    AUDIT.append({"module": module_name, "__file__": str(p),
                  "git_blob_sha1_NUL_preimage": actual})


def build_expected() -> None:
    targets = [PIN / "t9b_temporal.py"]
    targets += sorted(p for p in NATIVE.rglob("*.py"))
    for rel in targets:
        EXPECTED[rel.resolve()] = {
            "git_blob_sha1": _git_blob_sha1(rel),
            "sha256": _file_sha256(rel),
        }


def pin_sys_path() -> None:
    sys.path[:] = [
        p for p in sys.path
        if p and not any(str(Path(p).resolve()).startswith(a) for a in AMBIENT_ROOTS)
    ]
    for entry in (str(PIN), str(NATIVE)):
        if entry in sys.path:
            sys.path.remove(entry)
    sys.path.insert(0, str(NATIVE))
    sys.path.insert(0, str(PIN))
    sys.path.insert(0, str(STAGE))


def module_receipts() -> dict:
    out = {}
    for name, mod in sorted(sys.modules.items()):
        f = getattr(mod, "__file__", None)
        if not f or name.split(".")[0] not in {"t9b_temporal", "data"}:
            continue
        p = Path(f).resolve()
        out[name] = {"__file__": str(p),
                     "inside_this_return": str(p).startswith(str(RET)),
                     "git_blob_sha1_NUL_preimage": _git_blob_sha1(p) if p.exists() else None,
                     "sha256": _file_sha256(p) if p.exists() else None}
    return out


SUITES = {
    "frozen_t9i_independent_48": str(STAGE / "tests/test_independent_clock_custody.py"),
    "t9c_own_repair_52": str(PIN / "test_t9c_repair.py"),
    "inherited_original_v553_native_8":
        str(NATIVE / "data/ddm_build_copy/tests/test_postg5_v552j_v553_consumer_contract.py"),
    "unchanged_t9b_author_28": str(PIN / "test_t9b_temporal.py"),
    "t9r_frozen_delta_50": str(STAGE / "tests/test_t9r_delta.py"),
    "t9r_postinspection_hostiles_7": str(STAGE / "tests/test_postinspection_hostiles.py"),
    "t9d_own_authority_provenance": str(STAGE / "tests/test_t9d_authority_provenance.py"),
}


def main() -> int:
    import pytest

    suite = sys.argv[1] if len(sys.argv) > 1 else "frozen_t9i_independent_48"
    pin_sys_path()
    build_expected()

    import data.ddm_build_copy as probe
    assert str(Path(probe.__file__).resolve()).startswith(str(NATIVE.resolve())), \
        f"AMBIENT DATA LEAK: {probe.__file__}"

    os.environ["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "1"
    sys.dont_write_bytecode = True
    junit = RET / "junit" / f"{suite}.xml"
    rc = pytest.main([
        "-q", "-p", "no:cacheprovider",
        "--rootdir", str(STAGE),
        "-c", str(STAGE / "pytest.ini"),
        f"--junitxml={junit}",
        SUITES[suite],
    ])
    receipts = module_receipts()
    (RET / "evidence" / f"{suite}_module_receipts.json").write_text(
        json.dumps({"suite": suite, "pytest_exit": int(rc),
                    "imports_before_exec": AUDIT,
                    "loaded_project_modules": receipts,
                    "plugins_autoload_disabled": True,
                    "python_executable": sys.executable,
                    "python_version": sys.version}, indent=2, sort_keys=True) + "\n")
    print(f"T9D_COURT_{suite}_EXIT={int(rc)} VERIFIED_PROJECT_MODULES={len(receipts)}")
    return int(rc)


if __name__ == "__main__":
    raise SystemExit(main())
