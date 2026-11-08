"""Exact-cut provenance and current-owner ABI records.

The R157 package and its 35 declared source configurations are imported from
one pinned candidate commit.  This module records and verifies the exact Git
blob identity of every imported file, and records the ABI/hash of the current
installed C11 consumer that receives the releases.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import inspect
import json
from pathlib import Path
import subprocess
from typing import Any, Iterable, Mapping

ROOT = Path(__file__).resolve().parents[2]

R157_CANDIDATE = "1384612bfed8d801140e00ace353779338599da3"
R157_REVIEW_CUT = "d81bc2c67baf933461ae6cfca468f24779cc7e44"
R157_PLAN_SEAL = "4c0c619eac747afee1d8e65e1418bf2d472da4c3"
R157_FACADE_BLOB = "8a761119e4a8d68eb291fc4edfadb52e027f8284"
R157_FACADE_SHA256 = "03b88d258d21c403542756db7316923aa392871442d99294de904b1744da1d01"

IMPORTED_PATHS = (
    "rawlsing_next/source_configuration",
    "source_pre553_validation",
    "SOURCE_PRE553_PLAN",
    "rawlsing_next/pre553_source_read_admission.py",
)
# The four R157 test modules are retained as focused harness inputs but are not
# package/config provenance: two environment-dependent R154 tests are skipped
# when the R154 runtime is absent, and the historical owner-mapping hash check
# is split into (a) exact R157 mapping provenance and (b) current-owner ABI.
TEST_HARNESS_EDITS = {
    "rawlsing_next/tests/test_source_configuration_foundation.py": (
        "owner-mapping test records the exact R157 facade hash and verifies the "
        "current facade hash through the current owner/ABI ledger"
    ),
    "rawlsing_next/tests/test_source_configuration_p3.py": (
        "two R154 loader tests skip when the R154 runtime/store is absent from "
        "this branch; the all-35 current-consumer proof is the focused suite"
    ),
}

CURRENT_CONSUMER_FILES = (
    "rawlsing_next/pre553_source_backed_c11_facade.py",
    "rawlsing_next/pre553_c11_ingest.py",
    "rawlsing_next/pre553_c11_repository.py",
    "rawlsing_next/pre553_c11_integrity.py",
    "rawlsing_next/pre553_empirical_objects.py",
    "rawlsing_next/pre553_empirical_authority.py",
    "rawlsing_next/pre553_source_local_universe_admission.py",
    "rawlsing_next/pre553_empirical_query.py",
    "rawlsing_next/pre553_source_native_preimage_adapter.py",
    "rawlsing_next/pre553_physical_decoder.py",
)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(
        ("git", "-C", str(ROOT), *args),
        check=True, capture_output=True, text=True,
    ).stdout


def _git_blob(path: Path) -> str:
    relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
    return _git("rev-parse", f"{R157_CANDIDATE}:{relative}").strip()


def _iter_imported_files() -> Iterable[Path]:
    for relative in IMPORTED_PATHS:
        target = ROOT / relative
        if target.is_file():
            yield target
            continue
        if not target.is_dir():
            raise FileNotFoundError(f"imported path absent: {relative}")
        for path in sorted(target.rglob("*")):
            if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc":
                yield path


def imported_cut_manifest(*, include_sha256: bool = True) -> dict[str, Any]:
    """Return the exact blob identity of every file imported from the R157 cut.

    ``git_blob`` is the authoritative Git object id at ``R157_CANDIDATE``.
    ``working_blob`` is the current index/working-tree object id and must match.
    """
    entries: list[dict[str, Any]] = []
    for path in _iter_imported_files():
        relative = path.resolve().relative_to(ROOT.resolve()).as_posix()
        entry = {
            "path": relative,
            "bytes": path.stat().st_size,
            "git_blob": _git_blob(path),
            "working_blob": _git("hash-object", str(path)).strip(),
        }
        if include_sha256:
            entry["sha256"] = _sha256(path)
        entries.append(entry)
    material = json.dumps(
        [{"path": x["path"], "git_blob": x["git_blob"], "bytes": x["bytes"]} for x in entries],
        sort_keys=True, separators=(",", ":"),
    ).encode("utf-8")
    return {
        "schema": "PYAT_777_UNIVERSAL_SOURCE_TO_C11_IMPORT_PROVENANCE@1.0.0",
        "r157_candidate": R157_CANDIDATE,
        "r157_review_cut": R157_REVIEW_CUT,
        "r157_plan_seal": R157_PLAN_SEAL,
        "imported_paths": list(IMPORTED_PATHS),
        "file_count": len(entries),
        "tree_identity_sha256": hashlib.sha256(material).hexdigest(),
        "files": entries,
    }


def verify_imported_cut(manifest: Mapping[str, Any] | None = None) -> dict[str, Any]:
    """Verify every imported file still equals its R157-cut Git blob."""
    document = dict(manifest or imported_cut_manifest(include_sha256=False))
    failures = []
    for entry in document["files"]:
        path = ROOT / entry["path"]
        if not path.is_file():
            failures.append(f"missing:{entry['path']}")
            continue
        if _git("hash-object", str(path)).strip() != entry["git_blob"]:
            failures.append(f"blob_drift:{entry['path']}")
        if path.stat().st_size != entry["bytes"]:
            failures.append(f"bytes_drift:{entry['path']}")
    return {
        "ok": not failures,
        "failures": failures,
        "file_count": document["file_count"],
        "tree_identity_sha256": document["tree_identity_sha256"],
        "r157_candidate": document["r157_candidate"],
    }


def _signature(callable_object: Any) -> str | None:
    try:
        return str(inspect.signature(callable_object))
    except (TypeError, ValueError):
        return None


def current_owner_abi() -> dict[str, Any]:
    """Record the current installed C11 receive seam and its exact bytes."""
    from rawlsing_next import pre553_c11_ingest as ingest
    from rawlsing_next import pre553_c11_repository as repository
    from rawlsing_next import pre553_source_backed_c11_facade as facade

    owners = []
    for relative in CURRENT_CONSUMER_FILES:
        path = ROOT / relative
        owners.append({
            "path": relative,
            "sha256": _sha256(path),
            "git_blob": _git("hash-object", str(path)).strip(),
            "bytes": path.stat().st_size,
        })
    return {
        "schema": "PYAT_777_UNIVERSAL_SOURCE_TO_C11_OWNER_ABI@1.0.0",
        "r157_candidate": R157_CANDIDATE,
        "r157_review_cut": R157_REVIEW_CUT,
        "r157_facade_sha256_at_cut": R157_FACADE_SHA256,
        "current_consumer": {
            "facade": {
                "module": facade.__name__,
                "class": "GovernedC11Projection",
                "candidate_builder": _signature(facade.project_c11_candidate_from_physical_cells),
                "stream_validator": _signature(facade.build_validated_source_backed_c11_release_from_stream),
                "incidence_validator": _signature(facade.build_validated_source_backed_c11_release),
                "repository_builder": _signature(facade.build_source_backed_c11_repository),
            },
            "ingest": {
                "module": ingest.__name__,
                "validator": _signature(ingest.validate_c11_source_release),
                "atomic_ingest": _signature(ingest.ingest_c11_source_release),
                "candidate_type": "C11SourceReleaseCandidate",
                "result_type": "C11IngestResult",
            },
            "repository": {
                "module": repository.__name__,
                "class": "C11Repository",
                "resolve_release_exact": _signature(repository.C11Repository.resolve_release_exact),
            },
        },
        "receive_seam": [
            "rawlsing_next.source_configuration.factory.build_governed_c11_projection",
            "rawlsing_next.pre553_source_backed_c11_facade.project_c11_candidate_from_physical_cells",
            "rawlsing_next.pre553_c11_ingest.validate_c11_source_release",
            "rawlsing_next.pre553_c11_ingest.ingest_c11_source_release",
            "rawlsing_next.pre553_c11_repository.C11Repository",
        ],
        "owner_files": owners,
        "no_new_engine": True,
        "no_replacement_c11_i03_batch": True,
        "native_source_package_required": False,
    }
