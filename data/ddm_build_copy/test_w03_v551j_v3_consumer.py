#!/usr/bin/env python3
"""W03-B regressions for the V551 v3 -> V551J consumer boundary."""

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


RUN_ID = "run-w03-b"
SOURCE = "EVS"
WAVE = "2017"
COUNTRY = "DE"


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _pattern_frames() -> tuple[pd.DataFrame, pd.DataFrame]:
    pattern = pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "source_family": SOURCE,
                "canonical_wave": WAVE,
                "country_code": COUNTRY,
                "family_id": "family-1",
                "pattern_id": "pattern-1",
            }
        ]
    )
    items = pd.DataFrame(
        [
            {
                "run_id": RUN_ID,
                "source_family": SOURCE,
                "canonical_wave": WAVE,
                "country_code": COUNTRY,
                "family_id": "family-1",
                "pattern_id": "pattern-1",
                "item_order": 1,
            }
        ]
    )
    return pattern, items


def _adjudication_row(candidate_id: str, outcome: str, reason: str = "") -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "candidate_id": candidate_id,
        "empirical_distribution_id": "dist-1",
        "source": SOURCE,
        "source_family": SOURCE,
        "canonical_wave": WAVE,
        "country_code": COUNTRY,
        "question_id": "q1",
        "var_code": "Q1",
        "response_value_normalized": candidate_id,
        "directional_applicability_status": "APPLICABLE_BY_AUTHORITY",
        "adjudication_outcome": outcome,
        "adjudication_reason": reason,
        "promotable": outcome == "PROMOTABLE",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
    }


def _atom_row(candidate_id: str, *, neutral: bool = False, low_support: bool = False) -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "atom_id": f"atom-{candidate_id}",
        "candidate_id": candidate_id,
        "empirical_distribution_id": "dist-1",
        "source": SOURCE,
        "source_family": SOURCE,
        "canonical_wave": WAVE,
        "country_code": COUNTRY,
        "question_id": "q1",
        "var_code": "Q1",
        "response_value_normalized": candidate_id,
        "response_intensity": 0.5 if neutral else 1.0,
        "v551_signed_side": "neutral" if neutral else "positive",
        "v551_signed_intensity": 0.0 if neutral else 1.0,
        "support_status": "REVIEW_REQUIRED" if low_support else "SUPPORTED",
        "atom_contract_hash": "a" * 64,
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
    }


def _coverage_row(*, applicable: int, promotable: int, nonpromotable: int, status: str) -> dict[str, object]:
    return {
        "run_id": RUN_ID,
        "empirical_distribution_id": "dist-1",
        "source": SOURCE,
        "source_family": SOURCE,
        "canonical_wave": WAVE,
        "country_code": COUNTRY,
        "question_id": "q1",
        "var_code": "Q1",
        "applicable_candidate_count": applicable,
        "promotable_candidate_count": promotable,
        "nonpromotable_candidate_count": nonpromotable,
        "directional_adjudication_status": status,
        "candidate_count_conserved": True,
        "unweighted_mass_conserved": True,
        "weighted_mass_conserved": True,
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
    }


def _write_bundle(
    root: Path,
    *,
    adjudication: pd.DataFrame,
    atoms: pd.DataFrame,
    coverage: pd.DataFrame,
    producer_integrity: str = "PASS",
    producer_evidence: str = "PRESENT",
    producer_permission: str = "ALLOW",
) -> tuple[Path, Path]:
    root.mkdir(parents=True, exist_ok=True)
    frames = {
        "directional_candidate_adjudication": adjudication,
        "relation_evidence_atoms": atoms,
        "directional_distribution_coverage": coverage,
    }
    artifacts = []
    for name, frame in frames.items():
        path = root / f"{name}.parquet"
        frame.to_parquet(path, index=False)
        artifacts.append(
            {
                "artifact": name,
                "path": path.name,
                "artifact_kind": "canonical",
                "row_count": len(frame),
                "artifact_file_sha256": _sha(path),
                "logical_content_sha256": "b" * 64,
                "schema_version": "v3.0",
            }
        )
    manifest = {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": RUN_ID,
        "run_id": RUN_ID,
        "source": SOURCE,
        "wave": WAVE,
        "canonical_wave": WAVE,
        "country_code": COUNTRY,
        "shard_id": "",
        "schema_version": "v3.0",
        "compiler_version": "v3.0",
        "run_integrity_status": producer_integrity,
        "evidence_status": producer_evidence,
        "downstream_permission_status": producer_permission,
        "candidate_count": len(adjudication),
        "promotable_candidate_count": int(adjudication.get("promotable", pd.Series(dtype=bool)).map(bool).sum()) if not adjudication.empty else 0,
        "atom_count": len(atoms),
        "distribution_coverage_rows": len(coverage),
        "artifacts": artifacts,
        "canonical_artifact_names": list(V551_V3_CANONICAL_ARTIFACTS),
    }
    manifest_path = root / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return manifest_path, root / "relation_evidence_atoms.parquet"


def _verify(manifest_path: Path, atoms_path: Path):
    pattern, items = _pattern_frames()
    scope = _expected_v551_scope(RUN_ID, pattern, items)
    return _verify_v551_v3_bundle(
        run_id=RUN_ID,
        manifest_path=manifest_path,
        atoms_path=atoms_path,
        expected_scope=scope,
    )


def test_complete_v3_bundle_is_allowed_and_preserves_neutral_review_semantics(tmp_path: Path) -> None:
    adjudication = pd.DataFrame([_adjudication_row("c1", "PROMOTABLE")])
    atoms = pd.DataFrame([_atom_row("c1", neutral=True, low_support=True)])
    coverage = pd.DataFrame([_coverage_row(applicable=1, promotable=1, nonpromotable=0, status="COMPLETE")])
    manifest_path, atoms_path = _write_bundle(tmp_path, adjudication=adjudication, atoms=atoms, coverage=coverage)

    bundle = _verify(manifest_path, atoms_path)

    assert bundle["report"]["effective_evidence_status"] == "PRESENT"
    assert bundle["report"]["effective_downstream_permission_status"] == "ALLOW"
    atom = bundle["atoms"].iloc[0]
    assert atom["response_intensity"] == pytest.approx(0.5)
    assert atom["v551_signed_side"] == "neutral"
    assert atom["v551_signed_intensity"] == pytest.approx(0.0)
    assert atom["support_status"] == "REVIEW_REQUIRED"


def test_partial_v3_coverage_demotes_even_if_producer_manifest_says_allow(tmp_path: Path) -> None:
    adjudication = pd.DataFrame(
        [
            _adjudication_row("c1", "PROMOTABLE"),
            _adjudication_row("c2", "NONPROMOTABLE_REPAIRABLE", "missing_projection_authority"),
        ]
    )
    atoms = pd.DataFrame([_atom_row("c1")])
    coverage = pd.DataFrame([_coverage_row(applicable=2, promotable=1, nonpromotable=1, status="PARTIAL_WITH_REPAIR_DEBT")])
    manifest_path, atoms_path = _write_bundle(tmp_path, adjudication=adjudication, atoms=atoms, coverage=coverage)

    bundle = _verify(manifest_path, atoms_path)

    assert bundle["report"]["effective_evidence_status"] == "APPLICABLE_UNRESOLVED"
    assert bundle["report"]["effective_downstream_permission_status"] == "DENY"
    assert bundle["report"]["repair_debt_candidate_count"] == 1
    assert bundle["report"]["repair_debt_reason_counts"] == {"missing_projection_authority": 1}


def test_missing_promotable_atom_is_unexplained_integrity_failure(tmp_path: Path) -> None:
    adjudication = pd.DataFrame([_adjudication_row("c1", "PROMOTABLE")])
    atoms = pd.DataFrame(columns=list(_atom_row("c1").keys()))
    coverage = pd.DataFrame([_coverage_row(applicable=1, promotable=1, nonpromotable=0, status="COMPLETE")])
    manifest_path, atoms_path = _write_bundle(tmp_path, adjudication=adjudication, atoms=atoms, coverage=coverage)

    with pytest.raises(BoundaryContractError, match="V551_UNEXPLAINED_MISSING_PROMOTABLE_ATOM"):
        _verify(manifest_path, atoms_path)


def test_wrong_declared_artifact_hash_fails_closed(tmp_path: Path) -> None:
    adjudication = pd.DataFrame([_adjudication_row("c1", "PROMOTABLE")])
    atoms = pd.DataFrame([_atom_row("c1")])
    coverage = pd.DataFrame([_coverage_row(applicable=1, promotable=1, nonpromotable=0, status="COMPLETE")])
    manifest_path, atoms_path = _write_bundle(tmp_path, adjudication=adjudication, atoms=atoms, coverage=coverage)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    for artifact in manifest["artifacts"]:
        if artifact["artifact"] == "relation_evidence_atoms":
            artifact["artifact_file_sha256"] = "0" * 64
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="V551_ARTIFACT_FILE_SHA256_MISMATCH"):
        _verify(manifest_path, atoms_path)


def test_fail_integrity_manifest_fails_closed(tmp_path: Path) -> None:
    adjudication = pd.DataFrame([_adjudication_row("c1", "PROMOTABLE")])
    atoms = pd.DataFrame([_atom_row("c1")])
    coverage = pd.DataFrame([_coverage_row(applicable=1, promotable=1, nonpromotable=0, status="COMPLETE")])
    manifest_path, atoms_path = _write_bundle(
        tmp_path,
        adjudication=adjudication,
        atoms=atoms,
        coverage=coverage,
        producer_integrity="FAIL",
        producer_evidence="APPLICABLE_UNRESOLVED",
        producer_permission="DENY",
    )

    with pytest.raises(BoundaryContractError, match="V551_RUN_INTEGRITY_NOT_PASS"):
        _verify(manifest_path, atoms_path)


def test_wrong_run_scope_identity_fails_closed(tmp_path: Path) -> None:
    adjudication = pd.DataFrame([_adjudication_row("c1", "PROMOTABLE")])
    atoms = pd.DataFrame([_atom_row("c1")])
    coverage = pd.DataFrame([_coverage_row(applicable=1, promotable=1, nonpromotable=0, status="COMPLETE")])
    manifest_path, atoms_path = _write_bundle(tmp_path, adjudication=adjudication, atoms=atoms, coverage=coverage)
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["producer_run_id"] = "other-run"
    manifest["run_id"] = "other-run"
    manifest_path.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    with pytest.raises(BoundaryContractError, match="IDENTITY_MISMATCH:run_id"):
        _verify(manifest_path, atoms_path)


def test_empty_v3_bundle_is_typed_not_applicable(tmp_path: Path) -> None:
    adjudication = pd.DataFrame(columns=list(_adjudication_row("c1", "PROMOTABLE").keys()))
    atoms = pd.DataFrame(columns=list(_atom_row("c1").keys()))
    coverage = pd.DataFrame(columns=list(_coverage_row(applicable=0, promotable=0, nonpromotable=0, status="COMPLETE").keys()))
    manifest_path, atoms_path = _write_bundle(
        tmp_path,
        adjudication=adjudication,
        atoms=atoms,
        coverage=coverage,
        producer_evidence="NOT_APPLICABLE",
        producer_permission="NOT_APPLICABLE",
    )

    bundle = _verify(manifest_path, atoms_path)

    assert bundle["report"]["effective_evidence_status"] == "NOT_APPLICABLE"
    assert bundle["report"]["effective_downstream_permission_status"] == "NOT_APPLICABLE"
    assert bundle["report"]["candidate_count"] == 0
    assert bundle["report"]["atom_count"] == 0
