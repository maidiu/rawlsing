#!/usr/bin/env python3
"""Hostile fail-closed regressions for the W03-B V551 producer boundary."""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pandas as pd
import pytest

from data.ddm_build_copy.compile_v551j_joint_evidence_packets import (
    _clear_v551j_stage_outputs,
    _verify_v551_v3_bundle,
    _write_v551_typed_stop,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import BoundaryContractError
from data.ddm_build_copy.ddm_v551j_io import ensure_output_dirs


SCOPE = {
    "run_id": "run-w03-b",
    "source": "EVS",
    "wave": "2017",
    "country_code": "DE",
    "country_codes": ["DE"],
    "shard_id": "",
}


def test_missing_v551_manifest_fails_closed(tmp_path: Path) -> None:
    with pytest.raises(BoundaryContractError, match="V551_MANIFEST_MISSING"):
        _verify_v551_v3_bundle(
            run_id=SCOPE["run_id"],
            manifest_path=tmp_path / "missing-manifest.json",
            atoms_path=tmp_path / "relation_evidence_atoms.parquet",
            expected_scope=SCOPE,
        )


def test_malformed_v551_manifest_fails_closed(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text("{not-json", encoding="utf-8")
    with pytest.raises(BoundaryContractError, match="V551_MANIFEST_UNREADABLE"):
        _verify_v551_v3_bundle(
            run_id=SCOPE["run_id"],
            manifest_path=manifest,
            atoms_path=tmp_path / "relation_evidence_atoms.parquet",
            expected_scope=SCOPE,
        )


def test_wrong_v551_contract_version_fails_before_artifact_use(tmp_path: Path) -> None:
    manifest = tmp_path / "manifest.json"
    manifest.write_text(
        json.dumps(
            {
                "contract_version": "wrong-boundary-contract",
                "schema_version": "v3.0",
                "compiler_version": "v3.0",
                "producer_run_id": SCOPE["run_id"],
                "run_id": SCOPE["run_id"],
                "source": SCOPE["source"],
                "wave": SCOPE["wave"],
                "canonical_wave": SCOPE["wave"],
                "country_code": SCOPE["country_code"],
                "run_integrity_status": "PASS",
                "evidence_status": "PRESENT",
                "downstream_permission_status": "ALLOW",
                "artifacts": [],
                "canonical_artifact_names": [],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(BoundaryContractError, match="V551_CONTRACT_VERSION_MISMATCH"):
        _verify_v551_v3_bundle(
            run_id=SCOPE["run_id"],
            manifest_path=manifest,
            atoms_path=tmp_path / "relation_evidence_atoms.parquet",
            expected_scope=SCOPE,
        )


def test_unresolved_v551_state_publishes_only_typed_state_not_packets(tmp_path: Path) -> None:
    output_dirs = ensure_output_dirs(tmp_path / "v551j", SCOPE["run_id"])
    stale = output_dirs["packets"] / "v551j_packet_candidate_trace.parquet"
    stale.write_bytes(b"stale-complete-looking-packet")
    _clear_v551j_stage_outputs(output_dirs)
    args = SimpleNamespace(run_id=SCOPE["run_id"], strict=True)
    bundle = {
        "report": {
            "effective_evidence_status": "APPLICABLE_UNRESOLVED",
            "effective_downstream_permission_status": "DENY",
            "effective_state_detail": "KNOWN_V551_REPAIR_DEBT_OR_INCOMPLETE_COVERAGE",
            "candidate_count": 2,
            "promotable_candidate_count": 1,
            "repair_debt_candidate_count": 1,
            "repair_debt_reason_counts": {"missing_projection_authority": 1},
            "producer_manifest_sha256": "a" * 64,
        },
        "atoms": pd.DataFrame([{"candidate_id": "c1"}]),
        "adjudication": pd.DataFrame([{"candidate_id": "c1"}, {"candidate_id": "c2"}]),
        "coverage": pd.DataFrame([{"empirical_distribution_id": "d1"}]),
    }

    exit_code = _write_v551_typed_stop(
        args=args,
        output_dirs=output_dirs,
        bundle=bundle,
        required_paths={},
        required_input_hashes={},
        started=0.0,
    )

    assert exit_code == 1
    assert list(output_dirs["packets"].iterdir()) == []
    assert not stale.exists()
    readiness = json.loads((output_dirs["manifest"] / "v551j_readiness_report.json").read_text(encoding="utf-8"))
    manifest = json.loads((output_dirs["manifest"] / "manifest.json").read_text(encoding="utf-8"))
    assert readiness["evidence_status"] == "APPLICABLE_UNRESOLVED"
    assert readiness["downstream_permission_status"] == "DENY"
    assert readiness["ready_for_v552j_joint_evidence"] is False
    assert manifest["output_artifacts"] == {}


def test_not_applicable_v551_state_is_typed_skip_without_packets(tmp_path: Path) -> None:
    output_dirs = ensure_output_dirs(tmp_path / "v551j", SCOPE["run_id"])
    _clear_v551j_stage_outputs(output_dirs)
    args = SimpleNamespace(run_id=SCOPE["run_id"], strict=True)
    bundle = {
        "report": {
            "effective_evidence_status": "NOT_APPLICABLE",
            "effective_downstream_permission_status": "NOT_APPLICABLE",
            "effective_state_detail": "NO_APPLICABLE_DIRECTIONAL_EVIDENCE",
            "candidate_count": 0,
            "promotable_candidate_count": 0,
            "repair_debt_candidate_count": 0,
            "repair_debt_reason_counts": {},
            "producer_manifest_sha256": "b" * 64,
        },
        "atoms": pd.DataFrame(),
        "adjudication": pd.DataFrame(),
        "coverage": pd.DataFrame(),
    }

    exit_code = _write_v551_typed_stop(
        args=args,
        output_dirs=output_dirs,
        bundle=bundle,
        required_paths={},
        required_input_hashes={},
        started=0.0,
    )

    assert exit_code == 0
    assert list(output_dirs["packets"].iterdir()) == []
    readiness = json.loads((output_dirs["manifest"] / "v551j_readiness_report.json").read_text(encoding="utf-8"))
    assert readiness["evidence_status"] == "NOT_APPLICABLE"
    assert readiness["downstream_permission_status"] == "NOT_APPLICABLE"
    assert readiness["ready_for_v552j_joint_evidence"] is False
