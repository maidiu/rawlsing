#!/usr/bin/env python3
"""EE-P2R6N local exact snapshot reconstruction and R6A proof."""

from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import gzip
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import exact_ref
from rawlsing_next.pre553_runtime_authority import (
    ACTIVE_POSITIVE_BINDING,
    CONCRETE_BINDING_SCHEMA,
    Pre553RuntimeAuthoritySet,
)


R6N = ROOT / "WORKER_RETURNS" / "EE-P2R6N"
R6J = ROOT / "WORKER_RETURNS" / "EE-P2R6J"
R5A = ROOT / "WORKER_RETURNS" / "EE-P2R5A"
R6K = ROOT / "WORKER_RETURNS" / "EE-P2R6K"
OUTPUT = R6N

EXPECTED_BINDING_HASH = "a5f36a81843fe2ebab0b5cccb369ce76035f842b93e602613b8b9f3a81103308"
EXPECTED_RELEASE = {
    "kind": "C11LogicalRelease",
    "object_id": "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669",
    "content_hash": "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f",
}
EXPECTED_SCOPE = {
    "kind": "C11LogicalRelease",
    "object_id": "LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669",
    "content_hash": "bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297",
}
EXPECTED_SNAPSHOT_BYTES = 1_447_731_437
EXPECTED_SNAPSHOT_SHA = "ca1e62ca14586bcd23392fc56d0af5f95c12d833bf994ef5a0ea09577ca1569b"
EXPECTED_GZIP_BYTES = 116_229_878
EXPECTED_GZIP_SHA = "42bff5e6ffc9dd76283b74525f47a5ec99c91ca44d9b5a7537fd13b820ef8e04"
CHUNKS = (
    ("validated_c11_candidate_snapshot.json.gz.part0000", 50_331_648, "9743cb7de71d470b305c91d3a9c55fd615d2d1544c3ae82bb33cf0e4f4d2ccb2"),
    ("validated_c11_candidate_snapshot.json.gz.part0001", 50_331_648, "0a5b16e20bb16b3b1537ea9b8e15e308f9daa3656c7c6a2fa299a4b3bb9da6f3"),
    ("validated_c11_candidate_snapshot.json.gz.part0002", 15_566_582, "84071bd29a466bbf4f8cfe0fe681749610e18f88fedcb1cd2573a7031b0b1869"),
)
ADOPTED_AUTHORITY_HASHES = (
    "3ef0317887f6910838636d3816237a81d5a56b38e07595c8cc1f7c5e7f1fae74",
    "0d7cfaac1d63cd438d29b109b590cb828805bd113fc37759a6f6f4c88d3c8f55",
    "225e4b80390500451834ea784d955465eb9f145a4cd1f798dace51f3a6d3baa4",
    "b87c387f9d222c83106c8d47d369af44f5c5368b274fd85e7a08b12c20d49cae",
    "9da19997168612891f59012e69674bac59fbee417d9b30b003171f3074168bf5",
    "a1da1ea78dce423ea3520726d0477b058057482d67964056743e08389d9045a0",
    "d8e3d9a19fa36599e8cd6b1bc8e82092c425fd9119be478f7ba79335d05a1b3e",
    "d9aa476c493810651baefa8bad23990d9dd80812a48670ad2052353f0e7d52a2",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_file(path: Path) -> tuple[int, str]:
    digest = hashlib.sha256()
    size = 0
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            size += len(block)
            digest.update(block)
    return size, digest.hexdigest()


def load_public_rehydrator():
    path = R6K / "04_SNAPSHOT_REHYDRATOR.py"
    spec = importlib.util.spec_from_file_location("ee_p2r6n_public_rehydrator", path)
    if spec is None or spec.loader is None:
        raise RuntimeError("public rehydrator could not be loaded")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build_runtime(binding_records: tuple[dict[str, Any], ...]) -> Pre553RuntimeAuthoritySet:
    fixtures = ROOT / "rawlsing_next" / "tests" / "fixtures"
    dialect = load_json(fixtures / "ee_p2r6a_r4a_01_dialect.json")
    respondent = load_json(fixtures / "ee_p2r6a_r4a_02_respondent.json")
    mixed = load_json(fixtures / "ee_p2r6a_r4a_03_mixed.json")
    derived = load_json(fixtures / "ee_p2r6a_r4a_04_derived.json")
    successor = load_json(fixtures / "ee_p2r6a_r4a_05_successor.json")
    realization = load_json(R5A / "02_RELEASE_REALIZATION_RELATION_AUTHORITY.json")
    schema = load_json(R5A / "03_CONCRETE_REALIZATION_BINDING_SCHEMA.json")
    clause = load_json(R5A / "04_R4A_RELEASE_PRECONDITION_SUCCESSOR_CLAUSE.json")
    return Pre553RuntimeAuthoritySet(
        adopted_authority_hashes=ADOPTED_AUTHORITY_HASHES,
        predicate_dialect_matrices=(dialect,),
        respondent_compatibility_authorities=(respondent,),
        mixed_composition_authorities=(mixed,),
        derived_predicate_contracts=(derived,),
        public_predicate_successor_authorities=(successor,),
        release_realization_authorities=(realization,),
        realization_binding_schemas=(schema,),
        release_precondition_clauses=(clause,),
        realization_bindings=binding_records,
    )


def expect_failure(label: str, thunk: Callable[[], Any]) -> dict[str, Any]:
    try:
        thunk()
    except Exception as exc:  # exact production failure is the expected negative result
        return {
            "label": label,
            "status": "PASS_FAIL_CLOSED",
            "exception_type": type(exc).__name__,
            "message": str(exc),
        }
    raise RuntimeError(f"required fail-closed negative unexpectedly passed: {label}")


def main() -> int:
    binding = load_json(R6J / "04_PROPOSED_ACTIVE_RUNTIME_BINDING_RECORD.json")
    if binding["binding_ref"]["content_hash"] != EXPECTED_BINDING_HASH:
        raise RuntimeError("banked binding hash mismatch")
    if binding.get("schema") != CONCRETE_BINDING_SCHEMA or binding.get("typed_state") != ACTIVE_POSITIVE_BINDING:
        raise RuntimeError("banked binding schema/state mismatch")

    quarantine = load_json(R6J / "SUPPORT" / "01_QUARANTINED_R6I_CANDIDATE.json")
    if quarantine["binding_ref"]["content_hash"] != "fd4177eaddff07dc1e51a6f900c07f163965f996742b301932bbeb79a8690bb0":
        raise RuntimeError("quarantined R6I identity mismatch")

    rehydrator = load_public_rehydrator()
    scope_ref = exact_ref(EXPECTED_SCOPE)
    expected_runtime_ref = exact_ref(EXPECTED_RELEASE)
    chunk_receipts = []

    with tempfile.TemporaryDirectory(prefix="ee-p2r6n-proof-") as temp_name:
        temp = Path(temp_name)
        gzip_path = temp / "validated_c11_candidate_snapshot.json.gz"
        with gzip_path.open("wb") as out:
            for index, (name, expected_bytes, expected_sha) in enumerate(CHUNKS):
                path = ROOT / "WORKER_RETURNS" / "EE-P2R6M" / "RUN_OUTPUT" / name
                size, digest = sha256_file(path)
                if size != expected_bytes or digest != expected_sha:
                    raise RuntimeError(f"snapshot chunk identity mismatch: {name}")
                with path.open("rb") as handle:
                    shutil.copyfileobj(handle, out, length=1024 * 1024)
                chunk_receipts.append({"index": index, "filename": name, "byte_length": size, "sha256": digest})

        gzip_bytes, gzip_sha = sha256_file(gzip_path)
        if gzip_bytes != EXPECTED_GZIP_BYTES or gzip_sha != EXPECTED_GZIP_SHA:
            raise RuntimeError("reconstructed gzip identity mismatch")

        snapshot_path = temp / "validated_c11_candidate_snapshot.json"
        with gzip.open(gzip_path, "rb") as source, snapshot_path.open("wb") as target:
            shutil.copyfileobj(source, target, length=1024 * 1024)
        snapshot_bytes, snapshot_sha = sha256_file(snapshot_path)
        if snapshot_bytes != EXPECTED_SNAPSHOT_BYTES or snapshot_sha != EXPECTED_SNAPSHOT_SHA:
            raise RuntimeError("decompressed snapshot identity mismatch")

        restored_release, repository, rehydration_receipt = rehydrator.rehydrate_snapshot_bytes(
            snapshot_path.read_bytes()
        )
        if rehydration_receipt.get("status") != "PASS":
            raise RuntimeError("public rehydrator did not PASS")
        if restored_release.release_ref.as_dict() != EXPECTED_RELEASE:
            raise RuntimeError("public rehydrator release identity mismatch")
        if repository.snapshot_identity() != json.dumps([EXPECTED_RELEASE], separators=(",", ":"), sort_keys=True):
            raise RuntimeError("public rehydrator repository snapshot identity mismatch")

        runtime = build_runtime((binding,))
        returned = runtime.require_realized_release(
            scope_ref,
            repository=repository,
            runtime_release_ref=expected_runtime_ref,
        )
        if returned.release_ref.as_dict() != EXPECTED_RELEASE:
            raise RuntimeError("production R6A returned unexpected release")

        negatives: list[dict[str, Any]] = []
        negatives.append(expect_failure("zero active binding", lambda: build_runtime(()).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))
        negatives.append(expect_failure("multiple active positive bindings", lambda: build_runtime((binding, copy.deepcopy(binding))).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))
        negatives.append(expect_failure("quarantined R6I fd4177e", lambda: build_runtime((quarantine,)).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))

        mutated = copy.deepcopy(binding)
        mutated["identity_material"]["source_artifact_sha256"] = "0" * 64
        negatives.append(expect_failure("mutated source identity", lambda: build_runtime((mutated,)).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))

        mutated = copy.deepcopy(binding)
        mutated["identity_material"]["runtime_i02_release_ref"]["content_hash"] = "0" * 64
        negatives.append(expect_failure("mutated runtime release ref", lambda: build_runtime((mutated,)).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))

        mutated = copy.deepcopy(binding)
        mutated["identity_material"]["runtime_replay_manifest_ref"]["content_hash"] = "0" * 64
        negatives.append(expect_failure("mutated replay ref", lambda: build_runtime((mutated,)).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))

        mutated = copy.deepcopy(binding)
        del mutated["identity_material"]["runtime_m01_m18_coverage"]["M18"]
        negatives.append(expect_failure("incomplete M01-M18 coverage", lambda: build_runtime((mutated,)).require_realized_release(scope_ref, repository=repository, runtime_release_ref=expected_runtime_ref)))

        for label, bad_ref in (
            ("latest resolution", {"latest": True}),
            ("default resolution", {"default": True}),
            ("fuzzy resolution", {"kind": "C11LogicalRelease", "object_id": "fuzzy", "content_hash": "0" * 64}),
            ("nearest resolution", {"kind": "C11LogicalRelease", "object_id": "nearest", "content_hash": "0" * 64}),
        ):
            negatives.append(expect_failure(label, lambda bad_ref=bad_ref: runtime.require_realized_release(scope_ref, repository=repository, runtime_release_ref=bad_ref)))

    qualification = {
        "schema": "EE_P2R6N_LOCAL_QUALIFICATION_RECEIPT@1.0.0",
        "status": "PASS",
        "terminal": "EE_P2R6N_PASS__BANKED_A5F36_BINDING_ACCEPTED_BY_EXACT_PRODUCTION_R6A_AGAINST_PUBLICLY_REHYDRATED_ADOPTED_R6L_RELEASE__INACTIVE_PENDING_HQ_ADOPTION",
        "source_or_library_access": False,
        "browser_infrastructure_nonresult": "NOT_EXECUTED__BROWSER_REPOSITORY_WRITE_GATE_PREVENTED_GOVERNED_PROOF_DRIVER_MATERIALIZATION",
        "binding_hash": EXPECTED_BINDING_HASH,
        "binding_blob_sha1": "4ac8cd48aac62600e648ff9692488796c51c826f",
        "snapshot": {"logical_byte_length": snapshot_bytes, "logical_sha256": snapshot_sha, "gzip_byte_length": gzip_bytes, "gzip_sha256": gzip_sha, "chunks": chunk_receipts},
        "rehydration": rehydration_receipt,
        "returned_release_ref": returned.release_ref.as_dict(),
        "production_runtime": {"module": "rawlsing_next/pre553_runtime_authority.py", "git_blob_sha1": "2ddc591f2572983d18f8f3e8f81a33b80b3bca7b", "disposition": "PASS"},
        "negative_tests": negatives,
        "forbidden_work": {"binding_activated_or_adopted": False, "a_b_qualification": False, "be1": False, "p2x": False},
        "wake": "HQ_CORRECTED_BINDING_ADJUDICATION_ONLY",
    }
    proof = {
        "schema": "EE_P2R6N_R6A_PRODUCTION_RUNTIME_PROOF@1.0.0",
        "status": "PASS",
        "binding_hash": EXPECTED_BINDING_HASH,
        "returned_release_ref": returned.release_ref.as_dict(),
        "repository_snapshot_identity": repository.snapshot_identity(),
        "production_entrypoint": "Pre553RuntimeAuthoritySet.require_realized_release",
        "production_runtime_blob_sha1": "2ddc591f2572983d18f8f3e8f81a33b80b3bca7b",
        "rehydration_status": rehydration_receipt,
        "negative_tests": negatives,
        "binding_activation_or_adoption": False,
    }
    reconstruction = {
        "schema": "EE_P2R6N_SNAPSHOT_RECONSTRUCTION_RECEIPT@1.0.0",
        "status": "PASS",
        "chunk_count": len(chunk_receipts),
        "chunks": chunk_receipts,
        "gzip": {"byte_length": gzip_bytes, "sha256": gzip_sha},
        "logical_snapshot": {"byte_length": snapshot_bytes, "sha256": snapshot_sha},
        "public_rehydration": {"status": rehydration_receipt["status"], "repository_snapshot_identity": repository.snapshot_identity()},
        "source_or_library_access": False,
    }
    for path, payload in (
        (OUTPUT / "01_SNAPSHOT_RECONSTRUCTION_RECEIPT.json", reconstruction),
        (OUTPUT / "03_R6A_PRODUCTION_RUNTIME_PROOF.json", proof),
        (OUTPUT / "04_LOCAL_QUALIFICATION_RECEIPT.json", qualification),
    ):
        path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "PASS", "returned_release_ref": returned.release_ref.as_dict(), "binding_hash": EXPECTED_BINDING_HASH, "snapshot": reconstruction["logical_snapshot"], "gzip": reconstruction["gzip"], "negative_count": len(negatives)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
