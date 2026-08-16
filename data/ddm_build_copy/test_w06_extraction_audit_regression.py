from __future__ import annotations

import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

import pandas as pd

from data.ddm_build_copy.run_v550_552_extraction_audit import (
    _load_parquet_result,
    _load_v551_v3_run,
)
from data.ddm_build_copy.v550_552_extraction_audit import (
    APPLICABLE_BUT_UNRESOLVED,
    COMPILER_FAILURE,
    NO_APPLICABLE_EVIDENCE,
    OBSERVED_ZERO,
    PROMOTABLE_EVIDENCE,
    V551_CANONICAL_ARTIFACTS,
    V551_COMPILER_VERSION,
    V551_SCHEMA_VERSION,
    build_v550_552_extraction_audit_package,
)
from data.ddm_build_copy.ddm_pipeline_boundary_contract import PIPELINE_BOUNDARY_CONTRACT_VERSION

ADJ_COLS = [
    "candidate_id", "empirical_distribution_id", "directional_applicability_status",
    "adjudication_outcome", "promotable", "schema_version", "compiler_version",
]
ATOM_COLS = [
    "candidate_id", "empirical_distribution_id", "response_intensity_status",
    "v551_signed_side", "v551_signed_intensity", "schema_version", "compiler_version",
]
COV_COLS = [
    "empirical_distribution_id", "applicable_candidate_count", "promotable_candidate_count",
    "nonpromotable_candidate_count", "directional_adjudication_status",
    "candidate_count_conserved", "unweighted_mass_conserved", "weighted_mass_conserved",
    "schema_version", "compiler_version",
]


def empty_adjudication():
    return pd.DataFrame(columns=ADJ_COLS)


def empty_atoms():
    return pd.DataFrame(columns=ATOM_COLS)


def empty_coverage():
    return pd.DataFrame(columns=COV_COLS)


def manifest(*, evidence: str, permission: str, candidates: int, promotable: int, nonpromotable: int, atoms: int, coverage_rows: int, integrity: str = "PASS"):
    return {
        "contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "boundary_contract_version": PIPELINE_BOUNDARY_CONTRACT_VERSION,
        "producer_run_id": "w06-fixture",
        "run_id": "w06-fixture",
        "source": "GSS",
        "wave": "1972",
        "canonical_wave": "1972",
        "country_code": "US",
        "producer_scope_identity": {"source": "GSS", "wave": "1972", "canonical_wave": "1972", "country_code": "US", "shard_id": "", "scope_kind": "country"},
        "schema_version": V551_SCHEMA_VERSION,
        "compiler_version": V551_COMPILER_VERSION,
        "run_integrity_status": integrity,
        "evidence_status": evidence,
        "downstream_permission_status": permission,
        "candidate_count": candidates,
        "promotable_candidate_count": promotable,
        "nonpromotable_candidate_count": nonpromotable,
        "atom_count": atoms,
        "distribution_coverage_rows": coverage_rows,
        "canonical_artifact_names": list(V551_CANONICAL_ARTIFACTS),
        "artifacts": [],
    }


def promotable_adjudication(count: int = 1):
    return pd.DataFrame([
        {
            "candidate_id": f"c{i}", "empirical_distribution_id": f"d{i}",
            "directional_applicability_status": "APPLICABLE_BY_AUTHORITY",
            "adjudication_outcome": "PROMOTABLE", "promotable": True,
            "schema_version": V551_SCHEMA_VERSION, "compiler_version": V551_COMPILER_VERSION,
        }
        for i in range(count)
    ], columns=ADJ_COLS)


def repair_adjudication():
    return pd.DataFrame([{
        "candidate_id": "c-repair", "empirical_distribution_id": "d-repair",
        "directional_applicability_status": "APPLICABLE_BY_AUTHORITY",
        "adjudication_outcome": "NONPROMOTABLE_REPAIRABLE", "promotable": False,
        "schema_version": V551_SCHEMA_VERSION, "compiler_version": V551_COMPILER_VERSION,
    }], columns=ADJ_COLS)


def atom(*, signed: float, side: str = "positive", raw_status: str = "OBSERVED_NUMERIC"):
    return pd.DataFrame([{
        "candidate_id": "c0", "empirical_distribution_id": "d0",
        "response_intensity_status": raw_status, "v551_signed_side": side,
        "v551_signed_intensity": signed, "schema_version": V551_SCHEMA_VERSION,
        "compiler_version": V551_COMPILER_VERSION,
    }], columns=ATOM_COLS)


def coverage(*, promotable: int, nonpromotable: int, status: str):
    return pd.DataFrame([{
        "empirical_distribution_id": "d0", "applicable_candidate_count": promotable + nonpromotable,
        "promotable_candidate_count": promotable, "nonpromotable_candidate_count": nonpromotable,
        "directional_adjudication_status": status, "candidate_count_conserved": True,
        "unweighted_mass_conserved": True, "weighted_mass_conserved": True,
        "schema_version": V551_SCHEMA_VERSION, "compiler_version": V551_COMPILER_VERSION,
    }], columns=COV_COLS)


class Fixtures:
    @staticmethod
    def row(manifest_payload, adjudication, atoms, coverage_frame, loads=None):
        package = build_v550_552_extraction_audit_package(
            run_id="w06-fixture", source="GSS", wave="1972", canonical_wave="1972", country_code="US",
            v551_outputs={
                "directional_candidate_adjudication": adjudication,
                "relation_evidence_atoms": atoms,
                "directional_distribution_coverage": coverage_frame,
            },
            v551_manifest=manifest_payload,
            artifact_load_diagnostics=pd.DataFrame(loads or []),
        )
        return package["readiness_report"].iloc[0]


class TestW06ExtractionAuditV551V3(unittest.TestCase):
    def test_no_applicable_evidence_is_valid_zero_promotable(self):
        row = Fixtures.row(
            manifest(evidence="NOT_APPLICABLE", permission="NOT_APPLICABLE", candidates=0, promotable=0, nonpromotable=0, atoms=0, coverage_rows=0),
            empty_adjudication(), empty_atoms(), empty_coverage(),
        )
        self.assertEqual(row["run_integrity_status"], "PASS")
        self.assertEqual(row["evidence_status"], "NOT_APPLICABLE")
        self.assertEqual(row["overall_status"], NO_APPLICABLE_EVIDENCE)
        self.assertEqual(int(row["promotable_count"]), 0)
        self.assertEqual(int(row["observed_zero_atom_count"]), 0)

    def test_applicable_unresolved_is_repair_debt_not_failure_or_zero(self):
        row = Fixtures.row(
            manifest(evidence="APPLICABLE_UNRESOLVED", permission="DENY", candidates=1, promotable=0, nonpromotable=1, atoms=0, coverage_rows=1),
            repair_adjudication(), empty_atoms(), coverage(promotable=0, nonpromotable=1, status="NO_PROMOTABLE"),
        )
        self.assertEqual(row["run_integrity_status"], "PASS")
        self.assertEqual(row["overall_status"], APPLICABLE_BUT_UNRESOLVED)
        self.assertEqual(int(row["directionally_applicable_count"]), 1)
        self.assertEqual(int(row["repair_debt_count"]), 1)
        self.assertEqual(int(row["observed_zero_atom_count"]), 0)

    def test_observed_zero_is_independent_of_present_evidence_status(self):
        row = Fixtures.row(
            manifest(evidence="PRESENT", permission="ALLOW", candidates=1, promotable=1, nonpromotable=0, atoms=1, coverage_rows=1),
            promotable_adjudication(), atom(signed=0.0, side="neutral", raw_status="MISSING"), coverage(promotable=1, nonpromotable=0, status="COMPLETE"),
        )
        self.assertEqual(row["evidence_status"], "PRESENT")
        self.assertEqual(row["overall_status"], OBSERVED_ZERO)
        self.assertEqual(int(row["observed_zero_atom_count"]), 1)
        self.assertEqual(int(row["raw_missing_observed_zero_atom_count"]), 1)
        self.assertEqual(row["downstream_permission_status"], "ALLOW")

    def test_nonzero_promotable_evidence_is_not_observed_zero(self):
        row = Fixtures.row(
            manifest(evidence="PRESENT", permission="ALLOW", candidates=1, promotable=1, nonpromotable=0, atoms=1, coverage_rows=1),
            promotable_adjudication(), atom(signed=0.7), coverage(promotable=1, nonpromotable=0, status="COMPLETE"),
        )
        self.assertEqual(row["overall_status"], PROMOTABLE_EVIDENCE)
        self.assertEqual(int(row["observed_zero_atom_count"]), 0)

    def test_partial_repair_debt_survives_even_when_some_evidence_is_allowed(self):
        adjud = pd.concat([promotable_adjudication(), repair_adjudication()], ignore_index=True)
        cov = coverage(promotable=1, nonpromotable=1, status="PARTIAL_WITH_REPAIR_DEBT")
        row = Fixtures.row(
            manifest(evidence="PRESENT", permission="ALLOW", candidates=2, promotable=1, nonpromotable=1, atoms=1, coverage_rows=1),
            adjud, atom(signed=0.5), cov,
        )
        self.assertEqual(row["run_integrity_status"], "PASS")
        self.assertEqual(int(row["promotable_count"]), 1)
        self.assertEqual(int(row["repair_debt_count"]), 1)
        self.assertEqual(row["coverage_status"], "PARTIAL_WITH_REPAIR_DEBT")

    def test_compiler_failure_is_not_inferred_from_zero_atoms(self):
        row = Fixtures.row(
            manifest(evidence="APPLICABLE_UNRESOLVED", permission="DENY", candidates=1, promotable=0, nonpromotable=1, atoms=0, coverage_rows=1, integrity="FAIL"),
            repair_adjudication(), empty_atoms(), coverage(promotable=0, nonpromotable=1, status="NO_PROMOTABLE"),
        )
        self.assertEqual(row["run_integrity_status"], "FAIL")
        self.assertEqual(row["overall_status"], COMPILER_FAILURE)

    def test_missing_v551_manifest_is_compiler_failure_not_valid_empty(self):
        row = Fixtures.row({}, empty_adjudication(), empty_atoms(), empty_coverage())
        self.assertEqual(row["run_integrity_status"], "FAIL")
        self.assertEqual(row["overall_status"], COMPILER_FAILURE)
        self.assertEqual(row["evidence_status"], "")

    def test_artifact_read_failure_overrides_producer_pass_without_erasing_evidence(self):
        row = Fixtures.row(
            manifest(evidence="PRESENT", permission="ALLOW", candidates=1, promotable=1, nonpromotable=0, atoms=1, coverage_rows=1),
            promotable_adjudication(), atom(signed=0.4), coverage(promotable=1, nonpromotable=0, status="COMPLETE"),
            loads=[{"stage": "v551", "artifact_name": "relation_evidence_atoms", "load_status": "HASH_MISMATCH"}],
        )
        self.assertEqual(row["producer_run_integrity_status"], "PASS")
        self.assertEqual(row["evidence_status"], "PRESENT")
        self.assertEqual(row["run_integrity_status"], "FAIL")
        self.assertEqual(row["downstream_permission_status"], "DENY")
        self.assertEqual(row["overall_status"], COMPILER_FAILURE)

    def test_manifest_count_mismatch_is_integrity_failure(self):
        bad = manifest(evidence="PRESENT", permission="ALLOW", candidates=1, promotable=1, nonpromotable=0, atoms=1, coverage_rows=1)
        bad["atom_count"] = 99
        row = Fixtures.row(bad, promotable_adjudication(), atom(signed=0.4), coverage(promotable=1, nonpromotable=0, status="COMPLETE"))
        self.assertEqual(row["audit_contract_status"], "FAIL")
        self.assertEqual(row["run_integrity_status"], "FAIL")

    def test_retired_alias_outcome_is_rejected(self):
        adjud = promotable_adjudication()
        adjud.loc[:, "adjudication_outcome"] = "CERTIFIED"
        row = Fixtures.row(
            manifest(evidence="PRESENT", permission="ALLOW", candidates=1, promotable=1, nonpromotable=0, atoms=1, coverage_rows=1),
            adjud, atom(signed=0.4), coverage(promotable=1, nonpromotable=0, status="COMPLETE"),
        )
        self.assertEqual(row["audit_contract_status"], "FAIL")
        self.assertEqual(row["run_integrity_status"], "FAIL")


class TestW06V551V3ArtifactLoader(unittest.TestCase):
    def test_valid_empty_parquet_is_distinct_from_read_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "empty.parquet"
            path.write_bytes(b"fixture")
            digest = hashlib.sha256(b"fixture").hexdigest()
            frame = pd.DataFrame(columns=["schema_version", "compiler_version"])
            with mock.patch("data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet", return_value=frame):
                result = _load_parquet_result(
                    path, label="fixture", expected_sha256=digest, expected_row_count=0,
                    expected_schema_version=V551_SCHEMA_VERSION, expected_compiler_version=V551_COMPILER_VERSION,
                )
        self.assertEqual(result.load_status, "VALID_EMPTY")

    def test_corrupt_parquet_is_read_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.parquet"
            path.write_bytes(b"bad")
            with mock.patch("data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet", side_effect=ValueError("corrupt")):
                result = _load_parquet_result(path, label="fixture")
        self.assertEqual(result.load_status, "READ_ERROR")

    def test_hash_mismatch_fails_before_semantic_read(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.parquet"
            path.write_bytes(b"actual")
            with mock.patch("data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet") as read:
                result = _load_parquet_result(path, label="fixture", expected_sha256="0" * 64)
        self.assertEqual(result.load_status, "HASH_MISMATCH")
        read.assert_not_called()

    def test_loader_consumes_only_manifest_declared_v3_canonical_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            run_dir = Path(tmp) / "w06-fixture"
            run_dir.mkdir()
            frames = {
                "directional_candidate_adjudication": empty_adjudication(),
                "relation_evidence_atoms": empty_atoms(),
                "directional_distribution_coverage": empty_coverage(),
            }
            declarations = []
            for name, frame in frames.items():
                path = run_dir / f"{name}.parquet"
                frame.to_pickle(path)
                declarations.append({
                    "artifact": name, "path": path.name, "artifact_kind": "canonical",
                    "row_count": 0, "artifact_file_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                    "logical_content_sha256": "1" * 64, "schema_version": V551_SCHEMA_VERSION,
                })
            payload = manifest(evidence="NOT_APPLICABLE", permission="NOT_APPLICABLE", candidates=0, promotable=0, nonpromotable=0, atoms=0, coverage_rows=0)
            payload["artifacts"] = declarations
            (run_dir / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
            with mock.patch("data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet", side_effect=lambda p: pd.read_pickle(p)):
                loaded_manifest, outputs, diagnostics = _load_v551_v3_run(
                    run_dir, run_id="w06-fixture", source="GSS", canonical_wave="1972", country_code="US"
                )
        self.assertEqual(loaded_manifest["schema_version"], V551_SCHEMA_VERSION)
        self.assertEqual(set(outputs), set(V551_CANONICAL_ARTIFACTS))
        self.assertTrue(all(row["load_status"] in {"LOADED", "VALID_EMPTY"} for row in diagnostics))


if __name__ == "__main__":
    unittest.main()
