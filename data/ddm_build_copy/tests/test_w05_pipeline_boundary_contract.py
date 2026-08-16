from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    BoundaryContractError,
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    atomic_write_json,
    boundary_state_from_payload,
    inspect_artifact,
    legacy_status_to_state,
    publish_staged_directory,
    validate_machine_output_policy,
    verify_boundary_manifest,
)


def test_legacy_status_is_anchored_not_substring() -> None:
    assert legacy_status_to_state("READY_V550").permits_downstream
    with pytest.raises(BoundaryContractError, match="LEGACY_STATUS_UNKNOWN"):
        legacy_status_to_state("MAYBE_READY_LATER")
    assert not legacy_status_to_state("NOT_READY_V550").permits_downstream


def test_typed_status_rejects_integrity_permission_contradiction() -> None:
    with pytest.raises(BoundaryContractError, match="ALLOW_WITH_NONPASS"):
        boundary_state_from_payload(
            {
                "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
                "run_integrity_status": "FAIL",
                "evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
            }
        )


def test_valid_empty_parquet_is_not_corrupt(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "empty.parquet"
    path.write_bytes(b"placeholder")
    monkeypatch.setattr(pd, "read_parquet", lambda _path: pd.DataFrame(columns=["x"]))
    result = inspect_artifact(path)
    assert result.readable is True
    assert result.row_count == 0
    assert result.valid_empty is True


def test_corrupt_parquet_is_not_reported_as_zero_rows(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    path = tmp_path / "corrupt.parquet"
    path.write_bytes(b"not parquet")

    def boom(_path: Path):
        raise ValueError("corrupt")

    monkeypatch.setattr(pd, "read_parquet", boom)
    result = inspect_artifact(path)
    assert result.readable is False
    assert result.row_count is None
    assert "READ_ERROR" in result.error


def test_strict_manifest_binds_identity_and_producer_file_hash(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.parquet"
    artifact.write_bytes(b"payload")
    monkeypatch.setattr(pd, "read_parquet", lambda _path: pd.DataFrame([{"x": 1}]))
    digest = hashlib.sha256(b"payload").hexdigest()
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
                "run_integrity_status": "PASS",
                "evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
                "producer_run_id": "run-1",
                "source": "GSS",
                "wave": "2010",
                "artifacts": [{"path": "artifact.parquet", "artifact_file_sha256": digest}],
            }
        ),
        encoding="utf-8",
    )
    verified = verify_boundary_manifest(
        manifest, run_id="run-1", source="GSS", wave="2010", required_artifacts=["artifact.parquet"]
    )
    assert verified.state.permits_downstream
    assert verified.verified_artifacts[0].artifact_file_sha256 == digest


def test_strict_manifest_rejects_wrong_hash(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    artifact = tmp_path / "artifact.parquet"
    artifact.write_bytes(b"payload")
    monkeypatch.setattr(pd, "read_parquet", lambda _path: pd.DataFrame([{"x": 1}]))
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
                "run_integrity_status": "PASS",
                "evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
                "producer_run_id": "run-1",
                "artifacts": [{"path": "artifact.parquet", "artifact_file_sha256": "0" * 64}],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(BoundaryContractError, match="SHA256_MISMATCH"):
        verify_boundary_manifest(manifest, run_id="run-1", required_artifacts=["artifact.parquet"])


def test_parquet_policy_fails_closed() -> None:
    validate_machine_output_policy(write_parquet=True, write_csv=False)
    with pytest.raises(BoundaryContractError, match="PARQUET_CANONICAL_OUTPUT_REQUIRED"):
        validate_machine_output_policy(write_parquet=False, write_csv=True)


def test_stale_safe_directory_publication_replaces_old_tree(tmp_path: Path) -> None:
    final = tmp_path / "stage"
    final.mkdir()
    (final / "stale.txt").write_text("old", encoding="utf-8")
    staging = tmp_path / "stage.new"
    staging.mkdir()
    atomic_write_json(staging / "manifest.json", {"current": True})
    publish_staged_directory(staging, final)
    assert not (final / "stale.txt").exists()
    assert json.loads((final / "manifest.json").read_text(encoding="utf-8")) == {"current": True}
