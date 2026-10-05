from __future__ import annotations

import ast
import csv
import hashlib
import inspect
import io
import json
from pathlib import Path
import typing

import pytest

import rawlsing_next.ee_p2x_darwin_stage_backend as backend
from rawlsing_next.pre553_empirical_objects import semantic_hash


PINNED = "3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f"
LEDGER_BLOB = "c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c"
PACKAGE_BLOB = "174b931e8aa89111086e3d46159b47154bed7f16"
BUILDER_BLOB = "c51b56779ab9d79126619b7733d41f5253c8150f"
PART_A_HASH = "9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
LEDGER_SHA256 = "65bdb972c2004d7ea6539b991125d2111e3705aee2d3e76159208d04e4a3fa60"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
BANKED_ROOT = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/banked_as2a"
)
LEDGER_PATH = BANKED_ROOT + "/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
PACKAGE_PATH = BANKED_ROOT + "/04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
BUILDER_PATH = (
    "data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/"
    "R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/"
    "banked_as2b/run_as2b_lits1_mechanical_certification.py"
)
EXPECTED_STAGES = frozenset({
    "S01_CANDIDATE_PREPARATION_BUILD",
    "S02_C11_REACHABILITY",
    "S03_PARITY_ORACLE_GATE",
    "S04_I03_EXECUTION",
    "S05_I05_LEARNED_PRODUCTION",
    "S06_PROVENANCE_AUDIT",
    "S07_COLD_RESEARCH",
    "S08_WARM_REPEATED_RESEARCH",
    "S09_DELETION_REGEN_OR_A_PERSISTENCE",
    "S10_SOURCE_RELEASE_INVALIDATION",
    "S11_SEMANTIC_AUTHORITY_INVALIDATION",
    "S12_STALE_CACHE_OR_PERSISTENT_STATE",
    "S13_CORRUPT_CACHE_OR_PERSISTENT_STATE",
    "S14_INTERRUPTION_RECOVERY",
    "S15_FRESH_PROCESS_REPLAY",
    "S16_TERMINAL_METRIC_VECTOR_COMPLETENESS",
    "S17_FINAL_COMPLETENESS_AND_VERIFICATION",
})


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def git_bytes(path: str) -> bytes:
    return backend._git_bytes(repo_root(), PINNED, path)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def exact_read_banked_authority(builder_bytes: bytes, ledger: Path, package: Path):
    tree = ast.parse(builder_bytes.decode("utf-8"))
    fn = next(
        n for n in tree.body
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        and n.name == "read_banked_authority"
    )
    module = ast.Module(body=[fn], type_ignores=[])
    ast.fix_missing_locations(module)
    ns = {
        "Any": typing.Any,
        "csv": csv,
        "json": json,
        "sha256_file": sha256_file,
        "semantic_hash": semantic_hash,
        "LEDGER": ledger,
        "PACKAGE": package,
        "SLOT_LEDGER_HASH": LEDGER_SHA256,
        "PART_A_HASH": PART_A_HASH,
        "VARIABLES": 1198,
    }
    exec(compile(module, BUILDER_PATH, "exec"), ns)
    return ns["read_banked_authority"]()


def test_exact_pinned_paths_and_git_blobs():
    assert backend.BACKEND_CONTRACT == "RAWLSING_EE_P2X_DARWIN_STAGE_BACKEND@1.0.0"
    assert backend.LITS_BANKED_COMMIT == PINNED
    assert backend.LITS_AS2A == BANKED_ROOT
    assert backend.LITS_LEDGER == LEDGER_PATH
    assert backend.LITS_PACKAGE == PACKAGE_PATH
    assert backend.LITS_SHA == SOURCE_SHA256

    ledger = git_bytes(backend.LITS_LEDGER)
    package = git_bytes(backend.LITS_PACKAGE)
    builder = git_bytes(backend.LITS_BUILDER)

    assert backend._blob(ledger) == LEDGER_BLOB
    assert backend._blob(package) == PACKAGE_BLOB
    assert backend._blob(builder) == BUILDER_BLOB
    assert hashlib.sha256(ledger).hexdigest() == LEDGER_SHA256
    assert semantic_hash(json.loads(package)["projection_material"]) == PART_A_HASH


def test_exact_banked_builder_accepts_deployed_authority_bytes(tmp_path: Path):
    ledger_bytes = git_bytes(LEDGER_PATH)
    package_bytes = git_bytes(PACKAGE_PATH)
    builder_bytes = git_bytes(BUILDER_PATH)
    ledger = tmp_path / Path(LEDGER_PATH).name
    package = tmp_path / Path(PACKAGE_PATH).name
    ledger.write_bytes(ledger_bytes)
    package.write_bytes(package_bytes)

    pkg, rows, slots = exact_read_banked_authority(builder_bytes, ledger, package)

    assert len(rows) == 1198
    assert semantic_hash(pkg["projection_material"]) == PART_A_HASH
    assert slots["country"] == 98
    assert slots["q301_2"] == 194
    assert slots["q301_7"] == 199
    assert slots["tablec"] == 1117
    assert slots["tabled"] == 1118


def test_missing_exact_banked_path_fails_closed():
    missing = LEDGER_PATH.replace("/banked_as2a/", "/banked_as2a_MISSING/")
    with pytest.raises(backend.CourtAuthorityStop, match="immutable path unavailable"):
        git_bytes(missing)


def test_substituted_ledger_bytes_fail_closed(tmp_path: Path):
    builder_bytes = git_bytes(BUILDER_PATH)
    ledger = tmp_path / Path(LEDGER_PATH).name
    package = tmp_path / Path(PACKAGE_PATH).name
    raw = bytearray(git_bytes(LEDGER_PATH))
    raw[-2] = ord("9") if raw[-2] != ord("9") else ord("8")
    ledger.write_bytes(bytes(raw))
    package.write_bytes(git_bytes(PACKAGE_PATH))
    with pytest.raises(RuntimeError, match="slot ledger SHA mismatch"):
        exact_read_banked_authority(builder_bytes, ledger, package)


def test_substituted_package_projection_material_fails_closed(tmp_path: Path):
    builder_bytes = git_bytes(BUILDER_PATH)
    ledger = tmp_path / Path(LEDGER_PATH).name
    package = tmp_path / Path(PACKAGE_PATH).name
    ledger.write_bytes(git_bytes(LEDGER_PATH))
    doc = json.loads(git_bytes(PACKAGE_PATH))
    doc["projection_material"]["__hostile_substitution__"] = True
    package.write_text(json.dumps(doc), encoding="utf-8")
    with pytest.raises(RuntimeError, match="projection authority content hash mismatch"):
        exact_read_banked_authority(builder_bytes, ledger, package)


def test_no_fallback_or_fuzzy_authority_lookup_and_stage_contract_unchanged():
    git_source = inspect.getsource(backend._git_bytes)
    projection_source = inspect.getsource(backend._lits_projection)

    assert "git" in git_source and '"show"' in git_source
    assert "glob(" not in git_source
    assert "rglob(" not in git_source
    assert "_git_bytes(repo, LITS_BANKED_COMMIT, LITS_LEDGER)" in projection_source
    assert "_git_bytes(repo, LITS_BANKED_COMMIT, LITS_PACKAGE)" in projection_source
    assert "glob(" not in projection_source
    assert "rglob(" not in projection_source

    assert backend.READY == EXPECTED_STAGES
    assert frozenset(backend.HANDLERS) == EXPECTED_STAGES
