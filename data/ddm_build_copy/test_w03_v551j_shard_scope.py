#!/usr/bin/env python3
"""W03 shard-grain scope identity regressions."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import _expected_v551_scope
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError, verify_exact_identity


def _frame(*country_codes: str) -> pd.DataFrame:
    return pd.DataFrame(
        [
            {
                "run_id": "r1",
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
) -> Path:
    manifest = tmp_path / "v550j_manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "run_id": "r1",
                "source": "EVS",
                "shard_id": shard_id,
                "producer_scope_identity": {
                    "run_id": "r1",
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


def test_single_country_shard_derives_scalar_country_from_exact_country_list(tmp_path: Path) -> None:
    pattern = _frame("DE")
    manifest = _write_manifest(tmp_path, country_codes=["DE"], country_code="")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["scope_kind"] == "shard"
    assert scope["shard_id"] == "EVS__2017"
    assert scope["country_codes"] == ["DE"]
    assert scope["country_code"] == "DE"


def test_single_country_shard_preserves_matching_scalar_country(tmp_path: Path) -> None:
    pattern = _frame("DE")
    manifest = _write_manifest(tmp_path, country_codes=["DE"], country_code="DE")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["country_codes"] == ["DE"]
    assert scope["country_code"] == "DE"
    assert scope["shard_id"] == "EVS__2017"


def test_valid_empty_single_country_v550j_scope_keeps_scalar_and_shard_identity(tmp_path: Path) -> None:
    pattern = pd.DataFrame(columns=["run_id", "source_family", "canonical_wave", "country_code"])
    manifest = _write_manifest(tmp_path, country_codes=["DE"], country_code="")

    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)

    assert scope["source"] == "EVS"
    assert scope["wave"] == "2017"
    assert scope["country_codes"] == ["DE"]
    assert scope["country_code"] == "DE"
    assert scope["shard_id"] == "EVS__2017"


def test_single_country_scalar_list_contradiction_fails_closed(tmp_path: Path) -> None:
    pattern = _frame("DE")
    manifest = _write_manifest(tmp_path, country_codes=["DE"], country_code="FR")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_COUNTRY_CODE_SCOPE_MISMATCH"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_multi_country_shard_rejects_scalar_country_identity(tmp_path: Path) -> None:
    pattern = _frame("DE", "FR")
    manifest = _write_manifest(tmp_path, country_codes=["DE", "FR"], country_code="DE")

    with pytest.raises(BoundaryContractError, match="V550J_MANIFEST_MULTI_COUNTRY_SCALAR_COUNTRY_FORBIDDEN"):
        _expected_v551_scope("r1", pattern, pattern.copy(), manifest)


def test_corrected_singleton_scope_remains_coherent_with_downstream_exact_identity(tmp_path: Path) -> None:
    pattern = _frame("DE")
    manifest = _write_manifest(tmp_path, country_codes=["DE"], country_code="")
    scope = _expected_v551_scope("r1", pattern, pattern.copy(), manifest)
    downstream_payload = {
        "producer_run_id": "r1",
        "source": "EVS",
        "wave": "2017",
        "canonical_wave": "2017",
        "country_code": "DE",
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

    assert resolved["country_code"] == "DE"
    assert resolved["shard_id"] == "EVS__2017"

    mismatched_payload = {**downstream_payload, "country_code": "FR"}
    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:country_code"):
        verify_exact_identity(
            mismatched_payload,
            run_id=scope["run_id"],
            source=scope["source"],
            wave=scope["wave"],
            country_code=scope["country_code"],
            shard_id=scope["shard_id"],
        )
