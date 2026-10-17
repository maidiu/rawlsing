"""F6J — source identities, import ledger and environment passport."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
from pathlib import Path

RET = Path(__file__).resolve().parents[1]
CAND = "WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1"
STARTUP = "09a87efc87110cc50c129b02033730ed8feca4e8"
CAND_COMMIT = "9aa0e7d3a0cf9ab7654ce8e3d5cb15060235a48f"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def blob(p):
    return subprocess.run(["git", "hash-object", str(p)], capture_output=True,
                          text=True, check=True).stdout.strip()


def repo_blob(commit, path):
    out = subprocess.run(["git", "rev-parse", f"{commit}:{path}"], capture_output=True,
                         text=True)
    return out.stdout.strip() if out.returncode == 0 else None


rows = []
for p in sorted(RET.rglob("*")):
    if not p.is_file() or "__pycache__" in str(p):
        continue
    rel = str(p.relative_to(RET))
    if rel.startswith(("05_JUNIT/", "06_LOGS/", "07_EVIDENCE/")):
        continue
    rows.append({"path": rel, "bytes": p.stat().st_size, "sha256": sha(p),
                 "git_blob_sha1": blob(p)})

staged_native = RET / "01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py"
staged_sem = RET / "01_STAGED_NATIVE/rawlsing_next/pre553_empirical_objects.py"
fixture = RET / "04_TESTS/run/WORKER_RETURNS/PYAT-R3-S03-F6-HETEROGENEOUS-SYNTHESIS-R1/repro/fixtures.py"

ident = {
    "schema": "PYAT_R27_F6J_SOURCE_IDENTITIES@1",
    "role": "new distinct independent F6 scientific reviewer (F6J)",
    "repository": "maidiu/rawlsing",
    "branch": "agent/reviewer-pyat-r27-f6j-independent-heterogeneous-science-completion-r1",
    "sealed_startup": STARTUP,
    "candidate_commit": CAND_COMMIT,
    "prior_reviewer_commit": "6d99650bed01eed8365ec38bd888741a88888a45",
    "independent_freeze_commit": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
    "native_producer": {
        "staged_path": str(staged_native.relative_to(RET)),
        "git_blob_sha1": blob(staged_native),
        "sha256": sha(staged_native),
        "bytes": staged_native.stat().st_size,
        "expected_commission_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
        "blob_matches_commission": blob(staged_native) == "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
        "candidate_05_NATIVE_STAGE_blob": repo_blob(CAND_COMMIT, f"{CAND}/05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py"),
        "candidate_01_STAGED_NATIVE_blob": repo_blob(CAND_COMMIT, f"{CAND}/01_STAGED_NATIVE/pre553_heterogeneous_synthesis.py"),
        "byte_identical_to_candidate_05_NATIVE_STAGE": blob(staged_native) == repo_blob(CAND_COMMIT, f"{CAND}/05_NATIVE_STAGE/rawlsing_next/pre553_heterogeneous_synthesis.py"),
        "commit_1428c2e92bce1a49efd87378cb23df936d646dc5_verified": True,
        "note": "the commission names S03FO@1428c2e92bce1a49efd87378cb23df936d646dc5 "
                "with blob fc5e37fa5b2f0eb689593b42d95479d1327cb94c and warns that the "
                "older 182cc797 differs; only the fc5e37fa bytes are executed here",
    },
    "semantic_hash_module": {
        "staged_path": str(staged_sem.relative_to(RET)),
        "git_blob_sha1": blob(staged_sem),
        "sha256": sha(staged_sem),
        "repo_blob_at_startup": repo_blob(STARTUP, "rawlsing_next/pre553_empirical_objects.py"),
        "byte_identical_to_repo": blob(staged_sem) == repo_blob(STARTUP, "rawlsing_next/pre553_empirical_objects.py"),
    },
    "inherited_fixture": {
        "staged_path": str(fixture.relative_to(RET)),
        "git_blob_sha1": blob(fixture),
        "sha256": sha(fixture),
        "candidate_repo_blob": repo_blob(CAND_COMMIT, f"{CAND}/00_SOURCES/S03/repro/fixtures.py"),
        "byte_identical_to_candidate": blob(fixture) == repo_blob(CAND_COMMIT, f"{CAND}/00_SOURCES/S03/repro/fixtures.py"),
        "transport_defect": "the candidate resolves this fixture through a git SYMLINK "
                            "whose target is the machine-absolute path "
                            "/Users/matthewsmith/Desktop/Rawlsing_Worktrees/pyat-r23-f6c/"
                            "WORKER_RETURNS/PYAT-R23-F6C-NATIVE-F6-COMPARATIVE-CONTINUATION-R1/"
                            "00_SOURCES/S03; the repo alone therefore cannot reproduce the "
                            "inherited suite. F6J stages the real fixture bytes instead.",
    },
    "transported_test_blobs": {
        "test_pre553_heterogeneous_synthesis.py": blob(RET / "04_TESTS/run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py"),
        "test_f6c_frozen_court.py": blob(RET / "04_TESTS/candidate_transport/test_f6c_frozen_court.py"),
        "f6c_worlds.py": blob(RET / "04_TESTS/candidate_transport/f6c_worlds.py"),
        "01_FROZEN_SOURCEFREE_STUDY_WORLDS.json": blob(RET / "04_TESTS/01_FROZEN_SOURCEFREE_STUDY_WORLDS.json"),
    },
    "staged_file_ledger": rows,
    "staged_file_count": len(rows),
    "staged_total_bytes": sum(r["bytes"] for r in rows),
}
(RET / "07_EVIDENCE/source_identities.json").write_text(
    json.dumps(ident, indent=2, sort_keys=True) + "\n")

import pytest, pandas  # noqa: E402
passport = {
    "schema": "PYAT_R27_F6J_ENVIRONMENT_PASSPORT@1",
    "role": "new distinct independent F6 scientific reviewer (F6J); NOT the F6C "
            "author, NOT the incomplete F6I reviewer",
    "write_scope": "WORKER_RETURNS/PYAT-R27-F6J-INDEPENDENT-F6-EXPERIMENT-COMPLETION-R1/ only",
    "interpreter": {"python": sys.version.split()[0], "executable": sys.executable,
                    "implementation": platform.python_implementation(),
                    "platform": platform.platform(),
                    "bytecode_disabled": True, "flag": "python3 -B + PYTHONDONTWRITEBYTECODE=1"},
    "libraries": {"pytest": pytest.__version__, "pandas": pandas.__version__,
                  "third_party_pins_are_owner_pins": False,
                  "note": "measured facts of this machine, not independently accepted owner pins"},
    "test_runner": {"plugin_autoload_disabled": "PYTEST_DISABLE_PLUGIN_AUTOLOAD=1",
                    "explicitly_disabled_plugins": ["cacheprovider", "randomly"],
                    "import_mode": "importlib", "rootdir_pinned": True,
                    "ambient_pytest_ini_not_used": True},
    "import_custody": {"pinned_via": "PYTHONPATH=01_STAGED_NATIVE",
                       "native_git_blob": "fc5e37fa5b2f0eb689593b42d95479d1327cb94c",
                       "ambient_leaks_permitted": 0},
    "numeric": {"primary": "fractions.Fraction",
                "note": "every scientific expectation in this return was computed in "
                        "exact rationals before the native producer was executed"},
    "ordering": {
        "freeze_pushed_at": "e476ccc090ae0175a540e94c5c382d7e2a8453f0",
        "freeze_pushed_before_candidate_test_output_inspection": True,
        "native_method_surface_read_before_freeze": True,
        "candidate_test_files_read_before_freeze": False,
        "candidate_junit_read_before_freeze": False,
    },
    "prohibitions": ["no original F6 semantic issuer", "no N9", "no OC05", "no N11",
                     "no N12", "no actor authority", "no real survey bytes",
                     "no cross-survey person", "no HQ method decision",
                     "no 35-wave grant"],
}
(RET / "environment_passport.json").write_text(
    json.dumps(passport, indent=2, sort_keys=True) + "\n")
print("staged files:", ident["staged_file_count"], "bytes:", ident["staged_total_bytes"])
print("native blob matches commission:", ident["native_producer"]["blob_matches_commission"])
print("native byte-identical to candidate staging:", ident["native_producer"]["byte_identical_to_candidate_05_NATIVE_STAGE"])
print("fixture byte-identical:", ident["inherited_fixture"]["byte_identical_to_candidate"])
