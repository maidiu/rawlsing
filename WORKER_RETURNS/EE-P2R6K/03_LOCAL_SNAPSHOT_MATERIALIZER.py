#!/usr/bin/env python3
"""One-shot exact adopted R6L replay plus validated C11 snapshot emission for EE-P2R6K."""
from __future__ import annotations

import argparse
from io import BytesIO
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
from typing import Any

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

SOURCE_NAME = "LITS-2006-data.dta"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS = 29002
SOURCE_VARIABLES = 1198
ADOPTED_RELEASE_ID = "LITS1-I02-F02-SUCCESSOR-7cac43e2ca5b31cb-bf305bf3f169d669"
ADOPTED_RELEASE_HASH = "192926fabd9c9c3d40e43b1d7705ca2bcfe7f8d06e286be26d4b886d436df43f"
ADOPTED_SOURCE_MANIFEST_HASH = "0546be4fa3f55239ee5d208234000066bdc84d832e89bc91d646ee623ed96714"
ADOPTED_CANDIDATE_PROJECTION_HASH = "23912633a23318d22bad0da08027867031320331d8d436d944e9c0b21eb086eb"
ADOPTED_REPLAY_MANIFEST_HASH = "30c168fbdf8425b23cbf2a2b2d2c9ab56f3438851f52e3562510089f1d381a08"
ADOPTED_REPLAY_JSON_SHA256 = "aa3b6026d4dbc3df8b142725704974eaef810e5dbf5b31d14b19c88cf8ecafd5"
R5B_DRIVER_BLOB = "b819fdff50470a71f1c570aa8021e28b361fa986"
AS2B_BLOB = "c51b56779ab9d79126619b7733d41f5253c8150f"
AS2A_LEDGER_BLOB = "c24e0d6acc6f2b823f0fc3fa5fb8a52b7c1cab0c"
AS2A_PACKAGE_BLOB = "174b931e8aa89111086e3d46159b47154bed7f16"
F02_BLOB = "7b45b277164fa90c3da739aab26b516f7a8cb8dc"

EXPECTED_COUNTS = {
    "EmpiricalUniverse": 1,
    "RespondentIdentity": 29002,
    "QuestionVariableBinding": 4,
    "RespondentEvent": 116008,
    "RoutingEligibilityFact": 116008,
    "EmpiricalCoordinateFact": 145010,
    "WeightMeasureFact": 0,
    "AuthoritySnapshot": 10,
    "SourceUniverseRelation": 0,
    "EmpiricalPredicateReplayBinding": 0,
    "ComparatorReplayBinding": 0,
    "DiscoveryBranchReplayBinding": 0,
    "StructuralAdmissionReplayBinding": 0,
    "ReplayManifest": 1,
}
EXPECTED_COVERAGE = {
    "M01": ["EmpiricalUniverse"],
    "M02": ["RespondentIdentity"],
    "M03": ["QuestionVariableBinding"],
    "M04": ["RespondentEvent"],
    "M05": ["QuestionVariableBinding", "RespondentEvent"],
    "M06": ["RespondentEvent.typed_state"],
    "M07": ["RoutingEligibilityFact"],
    "M08": ["EmpiricalCoordinateFact"],
    "M09": ["WeightMeasureFact|TypedAbsence"],
    "M10": ["AuthoritySnapshot"],
    "M11": ["SourceUniverseRelation|DISTINCT_BY_DEFAULT"],
    "M12": ["RoutingEligibilityFact", "EmpiricalPredicateReplayBinding|TypedAbsence"],
    "M13": ["ComparatorReplayBinding|DEFERRED"],
    "M14": ["DiscoveryBranchReplayBinding|DEFERRED"],
    "M15": ["StructuralAdmissionReplayBinding|NOT_APPLICABLE"],
    "M16": ["ReplayManifest"],
    "M17": ["AuthoritySnapshot", "ReplayManifest"],
    "M18": ["ReplayManifest"],
}

VENDOR = HERE / "SUPPORT" / "R5B"
DRIVER_PATH = VENDOR / "03_LOCAL_I02_SUCCESSOR_RELEASE_DRIVER.py"
SUPPORT = VENDOR / "SUPPORT"
AS2B = SUPPORT / "FROZEN_BASE" / "AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827" / "run_as2b_lits1_mechanical_certification.py"
AS2A_LEDGER = SUPPORT / "FROZEN_BASE" / "AS2A_LITS1_SHARED_CERTIFICATION_20260827" / "01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv"
AS2A_PACKAGE = SUPPORT / "FROZEN_BASE" / "AS2A_LITS1_SHARED_CERTIFICATION_20260827" / "04_SOURCE_SPECIFIC_PROJECTION_AUTHORITY_PACKAGE.json"
F02 = SUPPORT / "FROZEN_F02" / "prev3_lits1_selector_closure.py"

GIT_SAFE_THRESHOLD = 90 * 1024 * 1024
TRANSPORT_CHUNK_SIZE = 48 * 1024 * 1024
LOCAL_PASS_TERMINAL = "EE_P2R6K_LOCAL_SNAPSHOT_MATERIALIZATION_PASS__ADOPTED_R6L_IDENTITIES_EXACT__VALIDATED_C11_SNAPSHOT_EMITTED"


class LocalMaterializationError(RuntimeError):
    pass


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def git_blob_sha1(path: Path) -> str:
    payload = path.read_bytes()
    h = hashlib.sha1()
    h.update(f"blob {len(payload)}\0".encode("ascii"))
    h.update(payload)
    return h.hexdigest()


def load_local_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise LocalMaterializationError(f"cannot load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n", encoding="utf-8")


def verify_vendored_r5b() -> dict[str, str]:
    expected = {
        DRIVER_PATH: R5B_DRIVER_BLOB,
        AS2B: AS2B_BLOB,
        AS2A_LEDGER: AS2A_LEDGER_BLOB,
        AS2A_PACKAGE: AS2A_PACKAGE_BLOB,
        F02: F02_BLOB,
    }
    observed = {}
    for path, blob in expected.items():
        if not path.is_file():
            raise LocalMaterializationError(f"vendored exact R5B support missing: {path}")
        got = git_blob_sha1(path)
        if got != blob:
            raise LocalMaterializationError(f"vendored R5B blob mismatch: {path}: {got} != {blob}")
        observed[str(path.relative_to(HERE))] = got
    return observed


def load_exact_r5b_driver():
    driver = load_local_module("ee_p2r6k_exact_r5b_driver", DRIVER_PATH)
    driver.HERE = VENDOR
    driver.SUPPORT = SUPPORT
    driver.AS2B = AS2B
    driver.AS2A_LEDGER = AS2A_LEDGER
    driver.AS2A_PACKAGE = AS2A_PACKAGE
    driver.F02 = F02
    driver.FROZEN_GIT_BLOBS = {
        AS2B: AS2B_BLOB,
        AS2A_LEDGER: AS2A_LEDGER_BLOB,
        AS2A_PACKAGE: AS2A_PACKAGE_BLOB,
        F02: F02_BLOB,
    }
    return driver


def deterministic_gzip(data: bytes) -> bytes:
    buffer = BytesIO()
    with gzip.GzipFile(filename="", mode="wb", compresslevel=9, fileobj=buffer, mtime=0) as handle:
        handle.write(data)
    return buffer.getvalue()


def _assert_adopted(candidate: Any, release: Any, r5b_output: Path) -> None:
    from rawlsing_next.pre553_c11_ingest import record_counts_for_candidate

    if release.release_ref.object_id != ADOPTED_RELEASE_ID:
        raise LocalMaterializationError("adopted R6L release id mismatch")
    if release.semantic_release_hash != ADOPTED_RELEASE_HASH:
        raise LocalMaterializationError("adopted R6L semantic release hash mismatch")
    if release.source_artifact_ref.content_hash != SOURCE_SHA256:
        raise LocalMaterializationError("adopted R6L source artifact hash mismatch")
    if release.source_release_manifest_hash != ADOPTED_SOURCE_MANIFEST_HASH:
        raise LocalMaterializationError("adopted R6L source manifest hash mismatch")
    if candidate.source_release_manifest.content_hash != ADOPTED_SOURCE_MANIFEST_HASH:
        raise LocalMaterializationError("candidate source manifest hash mismatch")
    if candidate.candidate_replay_manifest.semantic_projection_hash != ADOPTED_CANDIDATE_PROJECTION_HASH:
        raise LocalMaterializationError("adopted R6L candidate projection hash mismatch")
    if release.replay_manifest.content_hash != ADOPTED_REPLAY_MANIFEST_HASH:
        raise LocalMaterializationError("adopted R6L ReplayManifest hash mismatch")
    if dict(record_counts_for_candidate(candidate)) != EXPECTED_COUNTS:
        raise LocalMaterializationError("adopted R6L record counts mismatch")
    coverage = {key: list(value) for key, value in release.m01_m18_coverage.items()}
    if coverage != EXPECTED_COVERAGE:
        raise LocalMaterializationError("adopted R6L M01-M18 coverage mismatch")
    replay_json = r5b_output / "successor_release_replay_manifest.json"
    if sha256_file(replay_json) != ADOPTED_REPLAY_JSON_SHA256:
        raise LocalMaterializationError("adopted R6L ReplayManifest JSON byte identity mismatch")


def _emit_transport(snapshot_bytes: bytes, output_dir: Path) -> dict[str, Any]:
    compressed = deterministic_gzip(snapshot_bytes)
    compressed_sha = hashlib.sha256(compressed).hexdigest()
    base = "validated_c11_candidate_snapshot.json.gz"
    chunks = []
    if len(compressed) <= GIT_SAFE_THRESHOLD:
        path = output_dir / base
        path.write_bytes(compressed)
        chunks.append({
            "index": 0,
            "filename": path.name,
            "byte_length": len(compressed),
            "sha256": compressed_sha,
        })
        mode = "SINGLE_DETERMINISTIC_GZIP"
    else:
        mode = "DETERMINISTIC_GZIP_FIXED_SIZE_TRANSPORT_CHUNKS"
        for index, offset in enumerate(range(0, len(compressed), TRANSPORT_CHUNK_SIZE)):
            payload = compressed[offset:offset + TRANSPORT_CHUNK_SIZE]
            path = output_dir / f"{base}.part{index:04d}"
            path.write_bytes(payload)
            chunks.append({
                "index": index,
                "filename": path.name,
                "byte_length": len(payload),
                "sha256": hashlib.sha256(payload).hexdigest(),
            })
    return {
        "schema": "EE_P2R6K_SNAPSHOT_TRANSPORT_MANIFEST@1.0.0",
        "semantic_snapshot_partitioned": False,
        "transport_mode": mode,
        "canonical_snapshot": {
            "filename": "validated_c11_candidate_snapshot.json",
            "byte_length": len(snapshot_bytes),
            "sha256": hashlib.sha256(snapshot_bytes).hexdigest(),
        },
        "compression": {
            "format": "gzip",
            "compresslevel": 9,
            "mtime": 0,
            "compressed_byte_length": len(compressed),
            "compressed_sha256": compressed_sha,
        },
        "chunk_policy": {
            "git_safe_threshold_bytes": GIT_SAFE_THRESHOLD,
            "fixed_chunk_size_bytes": TRANSPORT_CHUNK_SIZE,
            "chunks": chunks,
            "reconstruction": "concatenate chunks in ascending index when chunked, then gunzip once to recover the single canonical semantic snapshot",
        },
    }


def run_once(source: Path, output_dir: Path) -> dict[str, Any]:
    if source.name != SOURCE_NAME:
        raise LocalMaterializationError(f"authorized source filename must be exactly {SOURCE_NAME}")
    if sha256_file(source) != SOURCE_SHA256:
        raise LocalMaterializationError("authorized LiTS-I source SHA-256 mismatch")

    vendored = verify_vendored_r5b()
    driver = load_exact_r5b_driver()
    captured: dict[str, Any] = {}
    original_ingest = driver.ingest_c11_source_release

    def capture_ingest(candidate, repository):
        result = original_ingest(candidate, repository)
        if not result.accepted or result.release_ref is None:
            raise LocalMaterializationError("exact R5B/R6L replay did not produce accepted successor")
        captured["candidate"] = candidate
        captured["release"] = repository.resolve_release_exact(result.release_ref)
        return result

    driver.ingest_c11_source_release = capture_ingest
    r5b_output = output_dir / "R5B_REPLAY"
    r5b_output.mkdir(parents=True, exist_ok=True)
    prior_argv = list(sys.argv)
    try:
        sys.argv = [str(DRIVER_PATH), "--source", str(source), "--output-dir", str(r5b_output)]
        rc = driver.main()
    finally:
        sys.argv = prior_argv
        driver.ingest_c11_source_release = original_ingest
    if rc != 0 or set(captured) != {"candidate", "release"}:
        raise LocalMaterializationError("exact R5B/R6L replay failed before snapshot capture")

    candidate = captured["candidate"]
    release = captured["release"]
    _assert_adopted(candidate, release, r5b_output)

    codec = load_local_module("ee_p2r6k_codec_local", HERE / "02_C11_VALIDATED_SNAPSHOT_CODEC.py")
    rehydrator = load_local_module("ee_p2r6k_rehydrator_local", HERE / "04_SNAPSHOT_REHYDRATOR.py")
    snapshot_bytes = codec.serialize_snapshot_bytes(candidate, release)

    snapshot_path = output_dir / "validated_c11_candidate_snapshot.json"
    snapshot_path.write_bytes(snapshot_bytes)

    restored_release, restored_repository, rehydration_receipt = rehydrator.rehydrate_snapshot_bytes(snapshot_bytes)
    if restored_release.release_ref != release.release_ref:
        raise LocalMaterializationError("snapshot public rehydration release ref mismatch")
    if restored_repository.resolve_release_exact(release.release_ref).semantic_release_hash != ADOPTED_RELEASE_HASH:
        raise LocalMaterializationError("snapshot repository exact resolution mismatch")

    transport = _emit_transport(snapshot_bytes, output_dir)
    transport["vendored_r5b_git_blobs"] = vendored
    transport["adopted_r6l_identity_check"] = {
        "source_sha256": SOURCE_SHA256,
        "release_ref": release.release_ref.as_dict(),
        "source_release_manifest_hash": release.source_release_manifest_hash,
        "candidate_projection_hash": candidate.candidate_replay_manifest.semantic_projection_hash,
        "replay_manifest_ref": release.replay_manifest.ref.as_dict(),
        "record_counts": EXPECTED_COUNTS,
        "m01_m18_coverage": EXPECTED_COVERAGE,
        "status": "EXACT_MATCH",
    }
    write_json(output_dir / "snapshot_transport_manifest.json", transport)
    write_json(output_dir / "snapshot_rehydration_receipt.json", rehydration_receipt)

    local_receipt = {
        "schema": "EE_P2R6K_LOCAL_SNAPSHOT_MATERIALIZATION_RECEIPT@1.0.0",
        "status": "PASS",
        "terminal": LOCAL_PASS_TERMINAL,
        "operation": "EXACT_ADOPTED_R6L_REPLAY_AND_VALIDATED_C11_SNAPSHOT_EMISSION_ONLY",
        "source": {"name": SOURCE_NAME, "sha256": SOURCE_SHA256},
        "adopted_release_ref": release.release_ref.as_dict(),
        "snapshot": transport["canonical_snapshot"],
        "transport_mode": transport["transport_mode"],
        "rehydration": rehydration_receipt,
        "forbidden_work": {
            "benchmark": False,
            "p2x": False,
            "be1": False,
            "a_b_qualification": False,
            "binding_activation_or_adoption": False,
            "selector_or_candidate_semantic_mutation": False,
        },
    }
    write_json(output_dir / "local_snapshot_materialization_receipt.json", local_receipt)
    return local_receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True, type=Path)
    parser.add_argument("--output-dir", required=True, type=Path)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    receipt = run_once(args.source, args.output_dir)
    print(json.dumps({
        "status": receipt["status"],
        "terminal": receipt["terminal"],
        "adopted_release_ref": receipt["adopted_release_ref"],
        "snapshot": receipt["snapshot"],
        "transport_mode": receipt["transport_mode"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
