#!/usr/bin/env python3
"""W03 shard-grain scope identity regressions."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import _expected_v551_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, verify_exact_identity


def _frame(*country_codes: str, run_id: str = "r1") -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": run_id,
                "source_family": "EVS",
                "canonical_wave": "2017",
                "country_code": country_code,
            }
            for country_code in country_codes
        ]
    )


def _write_manifest(
    tmp_path: Path,
    *,
    country_codes: list[str],
    country_code: str = "",
    shard_id: str = "EVS__2017",
    run_id: str = "r1",
) -> Path:
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "run_id": run_id,
                "source": "EVS",
                "shard_id": shard_id,
                "producer_scope_identity": {
                    "run_id": run_id,
                    "source": "EVS",
                    "wave": "2017",
                    "canonical_wave": "2017",
                    "country_code": country_code,
                    "country_codes": country_codes,
                    "shard_id": shard_id,
                    "scope_kind": "shard" if shard_id else "country",
                },
            }
        ),
        encoding="utf-8",
    )
    return manifest


def test_multi_country_v550j_scope_uses_declared_shard_identity(tmp_path: Path) -> None:
    pattern = _frame("DE", "FR")
    manifest = _write_manifest(tmp_path, country_codes=["DE", "FR"])

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["scope_kind"] == "shard"
    assert scope["shard_id"] == "EVS__2017"
    assert scope["country_code"] == ""
    assert scope["country_codes"] == ["DE", "FR"]


def test_single_country_shard_derives_is_scalar_from_verified_country_list(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["IS"], country_code="")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["scope_kind"] == "shard"
    assert scope["shard_id"] == "EVS__2017"
    assert scope["country_codes"] == ["IS"]
    assert scope["country_code"] == "IS"


def test_single_country_shard_preserves_matching_scalar_country(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["IS"], country_code="IS")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["country_codes"] == ["IS"]
    assert scope["country_code"] == "IS"
    assert scope["shard_id"] == "EVS__2017"


def test_valid_empty_single_country_v550j_scope_keeps_scalar_and_shard_identity(tmp_path: Path) -> None:
    pattern = pd.DataFrame(columns=["run_id", "source_family", "canonical_wave", "country_code"])
    manifest = _write_manifest(tmp_path, country_codes=["IS"], country_code="")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["source"] == "EVS"
    assert scope["wave"] == "2017"
    assert scope["country_codes"] == ["IS"]
    assert scope["country_code"] == "IS"
    assert scope["shard_id"] == "EVS__2017"


def test_observed_frame_country_disagreement_with_producer_country_list_fails_closed(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["DE"])

    with pytest.raises(BoundaryContractError, match="V550J_FRAME_MANIFEST_COUNTRY_SCOPE_MISMATCH"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_single_country_scalar_list_contradiction_fails_closed(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["IS"], country_code="DE")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_COUNTRY_CODE_SCOPE_MISMATCH"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_multi_country_shard_rejects_scalar_country_identity(tmp_path: Path) -> None:
    pattern = _frame("DE", "FR")
    manifest = _write_manifest(tmp_path, country_codes=["DE", "FR"], country_code="DE")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_MULTI_COUNTRY_SCALAR_COUNTRY_FORBIDDEN"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_multi_country_scope_cannot_be_coerced_to_country_without_shard(tmp_path: Path) -> None:
    pattern = _frame("DE", "FR")
    manifest = _write_manifest(tmp_path, country_codes=["DE", "FR"], shard_id="")

    with pytest.raises(BoundaryContractError, match="V551J_MULTI_COUNTRY_SCOPE_REQUIRES_V550J_SHARD_ID"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_wrong_manifest_run_remains_fail_closed(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["IS"], run_id="other")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_RUN_ID_MISMATCH"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_corrected_singleton_scope_matches_existing_downstream_exact_identity_and_mismatches_fail(tmp_path: Path) -> None:
    pattern = _frame("IS")
    manifest = _write_manifest(tmp_path, country_codes=["IS"], country_code="")
    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)
    downstream_payload = {
        "producer_run_id": "r1",
        "source": "EVS",
        "wave": "2017",
        "canonical_wave": "2017",
        "country_code": "IS",
        "shard_id": "EVS__2017",
    }

    resolved = verify_exact_identity(
        downstream_payload,
        run_id=scope["run_id"],
        source=scope["source"],
        wave=scope["wave"],
        country_code=scope["country_code"],
        shard_id=scope["shard_id"],
    )

    assert resolved["country_code"] == "IS"
    assert resolved["shard_id"] == "EVS__2017"

    wrong_country = {**downstream_payload, "country_code": "DE"}
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:country_code"):
        verify_exact_identity(
            wrong_country,
            run_id=scope["run_id"],
            source=scope["source"],
            wave=scope["wave"],
            country_code=scope["country_code"],
            shard_id=scope["shard_id"],
        )

    wrong_shard = {**downstream_payload, "shard_id": "EVS__2017__other"}
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:shard_id"):
        verify_exact_identity(
            wrong_shard,
            run_id=scope["run_id"],
            source=scope["source"],
            wave=scope["wave"],
            country_code=scope["country_code"],
            shard_id=scope["shard_id"],
        )
