#!/usr/bin/env python3
"""W03-B V550J producer-surface binding regressions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import (
    V550J_PRODUCER_COMPILER_VERSION,
    V550J_PRODUCER_SCHEMA_VERSION,
    _verify_v550j_producer_surface,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    BoundaryContractError,
)


RUN_ID = "r1"
SOURCE = "EVS"
WAVE = "2017"
COUNTRY = "DE"
SHARD = "EVS__2017"
TABLE_NAMES = (
    "joint_response_pattern_index",
    "joint_response_pattern_item_index",
    "joint_pattern_relation_signature",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _frame(*, empty: bool = False) -> pd.DataFrame:
    columns = ["run_id", "source_family", "canonical_wave", "country_code"]
    if empty:
        return pd.DataFrame(columns=columns)
    return pd.DataFrame(
        [{"run_id": RUN_ID, "source_family": SOURCE, "canonical_wave": WAVE, "country_code": COUNTRY}]
    )


def _scope() -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "source": SOURCE,
        "wave": WAVE,
        "canonical_wave": WAVE,
        "country_code": "",
        "country_codes": [COUNTRY],
        "shard_id": SHARD,
        "scope_kind": "shard",
    }


def _write_surface(
    root: Path,
    *,
    empty: bool = False,
    evidence_status: str = "PRESENT",
    downstream_permission_status: str = "ALLOW",
    run_integrity_status: str = "PASS",
    contract_version: str = PIPELINE_BOUNDARY_CONTRACT_VERSION,
    schema_version: str = V550J_PRODUCER_SCHEMA_VERSION,
    compiler_version: str = V550J_PRODUCER_COMPILER_VERSION,
) -> tuple[Path, Path, dict[str, tuple[Path, pd.DataFrame]]]:
    root.mkdir(parents=True, exist_ok=True)
    frames: dict[str, tuple[Path, pd.DataFrame]] = {}
    tables = {}
    for table_name in TABLE_NAMES:
        path = root / f"{table_name}.parquet"
        frame = _frame(empty=empty)
        frame.to_parquet(path, index=False)
        frames[table_name] = (path, frame)
        tables[table_name] = {
            "table_name": table_name,
            "rows": len(frame),
            "columns": len(frame.columns),
            "parquet_path": str(path),
            "artifact_kind": "canonical",
            "artifact_file_sha256": _sha(path),
            "schema_version": schema_version,
            "compiler_version": compiler_version,
        }
    payload = {
        "contract_version": contract_version,
        "boundary_contract_version": contract_version,
        "producer_run_id": RUN_ID,
        "run_id": RUN_ID,
        "source": SOURCE,
        "wave": WAVE,
        "canonical_wave": WAVE,
        "country_code": "",
        "country_codes": [COUNTRY],
        "shard_id": SHARD,
        "producer_scope_identity": _scope(),
        "schema_version": schema_version,
        "compiler_version": compiler_version,
        "run_integrity_status": run_integrity_status,
        "evidence_status": evidence_status,
        "downstream_permission_status": downstream_permission_status,
        "producer_state_detail": "fixture",
    }
    manifest_payload = {
        **payload,
        "tables": tables,
        "canonical_artifact_names": list(TABLE_NAMES),
        "validation_status": "not_applicable",
    }
    readiness_payload = {**payload, "readiness_status": "validated_for_internal_analysis"}
    manifest = root / "v550j_manifest.json"
    readiness = root / "v550j_readiness.json"
    manifest.write_text(json.dumps(manifest_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    readiness.write_text(json.dumps(readiness_payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest, readiness, frames


def _verify(manifest: Path, readiness: Path, frames: dict[str, tuple[Path, pd.DataFrame]]):
    return _verify_v550j_producer_surface(
        run_id=RUN_ID,
        manifest_path=manifest,
        readiness_path=readiness,
        expected_scope={
            "source": SOURCE,
            "wave": WAVE,
            "country_codes": [COUNTRY],
            "country_code": "",
            "shard_id": SHARD,
        },
        table_inputs=frames,
    )


def test_v550j_declared_serialized_hash_version_and_typed_state_pass(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)

    report = _verify(manifest, readiness, frames)

    assert report["producer_artifact_hash_contract_status"] == "PRODUCER_DECLARED_ARTIFACT_FILE_SHA256_VERIFIED"
    assert report["producer_contract_version"] == PIPELINE_BOUNDARY_CONTRACT_VERSION
    assert report["producer_schema_version"] == V550J_PRODUCER_SCHEMA_VERSION
    assert report["producer_compiler_version"] == V550J_PRODUCER_COMPILER_VERSION
    assert report["producer_run_integrity_status"] == "PASS"
    assert report["producer_evidence_status"] == "PRESENT"
    assert report["producer_downstream_permission_status"] == "ALLOW"
    assert report["tables"]["joint_response_pattern_index"]["hash_status"] == "MATCHED_PRODUCER_DECLARATION"


def test_v550j_tampered_serialized_bytes_fail_before_row_semantics(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    path, already_loaded_frame = frames["joint_response_pattern_index"]
    path.write_bytes(path.read_bytes() + b"tamper")

    with pytest.raises(BoundaryContractError, match="V550J_TABLE_ARTIFACT_FILE_SHA256_MISMATCH"):
        _verify(manifest, readiness, frames)

    assert len(already_loaded_frame) == 1


def test_v550j_missing_producer_hash_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["tables"]["joint_response_pattern_index"].pop("artifact_file_sha256")
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_TABLE_ARTIFACT_FILE_SHA256_MISSING_OR_INVALID"):
        _verify(manifest, readiness, frames)


def test_v550j_legacy_missing_contract_is_not_accepted(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload.pop("contract_version")
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_CONTRACT_VERSION_MISMATCH"):
        _verify(manifest, readiness, frames)


def test_v550j_unsupported_compiler_version_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["compiler_version"] = "unknown-v550j-producer"
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_COMPILER_VERSION_MISMATCH"):
        _verify(manifest, readiness, frames)


def test_v550j_missing_typed_state_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(readiness.read_text(encoding="utf-8"))
    payload.pop("run_integrity_status")
    readiness.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="RUN_INTEGRITY_STATUS_INVALID"):
        _verify(manifest, readiness, frames)


def test_v550j_unknown_evidence_status_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    for path in (manifest, readiness):
        payload = json.loads(path.read_text(encoding="utf-8"))
        payload["evidence_status"] = "UNKNOWN_PRODUCER_STATE"
        path.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="EVIDENCE_STATUS_INVALID"):
        _verify(manifest, readiness, frames)


def test_v550j_nonpass_run_integrity_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(
        tmp_path,
        evidence_status="APPLICABLE_UNRESOLVED",
        downstream_permission_status="DENY",
        run_integrity_status="FAIL",
    )

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_RUN_INTEGRITY_NOT_PASS"):
        _verify(manifest, readiness, frames)


def test_v550j_wrong_producer_run_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["producer_run_id"] = "other-run"
    payload["run_id"] = "other-run"
    payload["producer_scope_identity"]["run_id"] = "other-run"
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_RUN_ID_MISMATCH"):
        _verify(manifest, readiness, frames)


def test_v550j_wrong_declared_path_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(manifest.read_text(encoding="utf-8"))
    payload["tables"]["joint_response_pattern_index"]["parquet_path"] = str(tmp_path / "wrong.parquet")
    manifest.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_TABLE_PATH_MISMATCH"):
        _verify(manifest, readiness, frames)


def test_v550j_wrong_scope_fails_closed(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(tmp_path)
    payload = json.loads(readiness.read_text(encoding="utf-8"))
    payload["producer_scope_identity"]["shard_id"] = "EVS__WRONG"
    readiness.write_text(json.dumps(payload), encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V550J_READINESS_SHARD_ID_MISMATCH"):
        _verify(manifest, readiness, frames)


def test_v550j_valid_empty_is_integrity_valid_and_not_downstream(tmp_path: Path) -> None:
    manifest, readiness, frames = _write_surface(
        tmp_path,
        empty=True,
        evidence_status="VALID_EMPTY",
        downstream_permission_status="NOT_APPLICABLE",
    )

    report = _verify(manifest, readiness, frames)

    assert report["producer_run_integrity_status"] == "PASS"
    assert report["producer_evidence_status"] == "VALID_EMPTY"
    assert report["producer_downstream_permission_status"] == "NOT_APPLICABLE"
    assert all(item["row_count"] == 0 for item in report["tables"].values())
