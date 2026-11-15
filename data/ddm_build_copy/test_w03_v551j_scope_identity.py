#!/usr/bin/env python3
"""W03-B exact producer-scope and declared-path regressions."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import (
    V551_V3_CANONICAL_ARTIFACTS,
    _expected_v551_scope,
    _verify_v551_v3_bundle,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import (
    PIPELINE_BOUNDARY_CONTRACT_VERSION,
    BoundaryContractError,
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_v550j_pattern_and_item_scope_must_be_singular() -> None:
    pattern = pd.DataFrame([
        {"run_id": "r1", "source_family": "EVS", "canonical_wave": "2017", "country_code": "DE"}
    ])
    items = pd.DataFrame([
        {"run_id": "r1", "source_family": "WVS", "canonical_wave": "2017", "country_code": "DE"}
    ])
    with pytest.raises(RuntimeError, match="V551J_V550J_SCOPE_NOT_SINGULAR:source"):
        _expected_v551_scope("r1", pattern, items)


def test_v550j_pattern_run_must_match_requested_run() -> None:
    pattern = pd.DataFrame([
        {"run_id": "other", "source_family": "EVS", "canonical_wave": "2017", "country_code": "DE"}
    ])
    items = pd.DataFrame([
        {"run_id": "other", "source_family": "EVS", "canonical_wave": "2017", "country_code": "DE"}
    ])
    with pytest.raises(RuntimeError, match="V551J_V550J_RUN_IDENTITY_MISMATCH"):
        _expected_v551_scope("r1", pattern, items)


def test_supplied_atoms_must_be_exact_producer_declared_file(tmp_path: Path) -> None:
    scope = {"run_id": "r1", "source": "EVS", "wave": "2017", "country_code": "DE", "country_codes": ["DE"], "shard_id": ""}
    adjudication = pd.DataFrame([
        {
            "run_id": "r1",
            "candidate_id": "c1",
            "empirical_distribution_id": "d1",
            "source": "EVS",
            "source_family": "EVS",
            "canonical_wave": "2017",
            "country_code": "DE",
            "question_id": "q1",
            "var_code": "Q1",
            "response_value_normalized": "1",
            "directional_applicability_status": "APPLICABLE_BY_AUTHORITY",
            "adjudication_outcome": "PROMOTABLE",
            "adjudication_reason": "",
            "promotable": True,
            "schema_version": "v3.0",
            "compiler_version": "v3.0",
        }
    ])
    atoms = pd.DataFrame([
        {
            "run_id": "r1",
            "atom_id": "a1",
            "candidate_id": "c1",
            "empirical_distribution_id": "d1",
            "source": "EVS",
            "source_family": "EVS",
            "canonical_wave": "2017",
            "country_code": "DE",
            "question_id": "q1",
            "var_code": "Q1",
            "response_value_normalized": "1",
            "response_intensity": 1.0,
            "v551_signed_side": "positive",
            "v551_signed_intensity": 1.0,
            "support_status": "SUPPORTED",
            "atom_contract_hash": "a" * 64,
            "schema_version": "v3.0",
            "compiler_version": "v3.0",
        }
    ])
    coverage = pd.DataFrame([
        {
            "run_id": "r1",
            "empirical_distribution_id": "d1",
            "source": "EVS",
            "source_family": "EVS",
            "canonical_wave": "2017",
            "country_code": "DE",
            "question_id": "q1",
            "var_code": "Q1",
            "applicable_candidate_count": 1,
            "promotable_candidate_count": 1,
            "nonpromotable_candidate_count": 0,
            "directional_adjudication_status": "COMPLETE",
            "candidate_count_conserved": True,
            "unweighted_mass_conserved": True,
            "weighted_mass_conserved": True,
            "schema_version": "v3.0",
            "compiler_version": "v3.0",
        }
    ])
    artifacts = []
    for name, frame in {
        "directional_candidate_adjudication": adjudication,
        "relation_evidence_atoms": atoms,
        "directional_distribution_coverage": coverage,
    }.items():
        path = tmp_path / f"{name}.parquet"
        frame.to_parquet(path, index=False)
        artifacts.append({
            "artifact": name,
            "path": path.name,
            "artifact_kind": "canonical",
            "row_count": len(frame),
            "artifact_file_sha256": _sha(path),
            "logical_content_sha256": "b" * 64,
            "schema_version": "v3.0",
        })
    manifest = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": "r1",
        "run_id": "r1",
        "source": "EVS",
        "wave": "2017",
        "canonical_wave": "2017",
        "country_code": "DE",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
        "run_integrity_status": "PASS",
        "evidence_status": "PRESENT",
        "downstream_permission_status": "ALLOW",
        "artifacts": artifacts,
        "canonical_artifact_names": list(V551_V3_CANONICAL_ARTIFACTS),
    }
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
    wrong_atoms = tmp_path / "copied_atoms.parquet"
    atoms.to_parquet(wrong_atoms, index=False)

    with pytest.raises(BoundaryContractError, match="V551_ATOMS_PATH_NOT_PRODUCER_DECLARED"):
        _verify_v551_v3_bundle(
            run_id="r1",
            manifest_path=manifest_path,
            atoms_path=wrong_atoms,
            expected_scope=scope,
        )
