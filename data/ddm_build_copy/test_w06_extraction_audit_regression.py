from __future__ import annotations
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import pandas as pd
from data.ddm_build_copy.run_v550_552_extraction_audit import _load_parquet_result
from data.ddm_build_copy.v550_552_extraction_audit import APPLICABLE_BUT_UNRESOLVED, NO_APPLICABLE_EVIDENCE, OBSERVED_ZERO, FAIL, PASS, build_v550_552_extraction_audit_package

class W06ExtractionFixtures:

    @staticmethod
    def package(*, manifest=None, adjudication=None, atoms=None, coverage=None, loads=None):
        v551 = {'directional_candidate_adjudication': adjudication if adjudication is not None else pd.DataFrame(), 'relation_evidence_atoms': atoms if atoms is not None else pd.DataFrame(), 'directional_distribution_coverage': coverage if coverage is not None else pd.DataFrame()}
        return build_v550_552_extraction_audit_package(run_id='w06-fixture', source='GSS', wave='1972', canonical_wave='1972', country_code='US', v551_outputs=v551, v551_manifest=manifest or {}, artifact_load_diagnostics=pd.DataFrame(loads or []))['readiness_report'].iloc[0]

    @classmethod
    def valid_zero_promotable(cls):
        return cls.package(manifest={'run_integrity_status': 'PASS'}, atoms=pd.DataFrame())

    @classmethod
    def compiler_failure(cls):
        return cls.package(manifest={'run_integrity_status': 'PASS'}, loads=[{'stage': 'v551', 'artifact_name': 'relation_evidence_atoms', 'load_status': 'READ_ERROR'}])

    @classmethod
    def no_applicable_evidence(cls):
        return cls.package(manifest={'run_integrity_status': 'PASS', 'evidence_status': 'NO_APPLICABLE_EVIDENCE'}, adjudication=pd.DataFrame([{'terminal_outcome': 'NOT_APPLICABLE'}]))

    @classmethod
    def applicable_but_unresolved(cls):
        return cls.package(manifest={'run_integrity_status': 'PASS'}, adjudication=pd.DataFrame([{'terminal_outcome': 'NONPROMOTABLE_REPAIRABLE'}]))

    @classmethod
    def observed_zero(cls):
        return cls.package(manifest={'run_integrity_status': 'PASS'}, adjudication=pd.DataFrame([{'terminal_outcome': 'PROMOTABLE'}]), atoms=pd.DataFrame([{'evidence_status': 'OBSERVED_ZERO', 'signed_intensity': 0.0}]))

class TestW06ExtractionAuditTypedStates(unittest.TestCase):

    def test_valid_zero_promotable_is_not_compiler_failure(self):
        row = W06ExtractionFixtures.valid_zero_promotable()
        self.assertEqual(row['run_integrity_status'], PASS)
        self.assertEqual(int(row['promotable_count']), 0)
        self.assertTrue(str(row['overall_status']).startswith('valid_zero_promotable'))
        self.assertNotEqual(row['overall_status'], 'compiler_failure')

    def test_compiler_failure_is_integrity_failure_even_with_zero_atoms(self):
        row = W06ExtractionFixtures.compiler_failure()
        self.assertEqual(row['run_integrity_status'], FAIL)
        self.assertEqual(row['overall_status'], 'compiler_failure')

    def test_no_applicable_evidence_is_distinct_from_unresolved(self):
        row = W06ExtractionFixtures.no_applicable_evidence()
        self.assertEqual(row['evidence_status'], NO_APPLICABLE_EVIDENCE)
        self.assertEqual(int(row['directionally_applicable_count']), 0)
        self.assertEqual(int(row['not_applicable_count']), 1)

    def test_applicable_but_unresolved_keeps_candidate_in_denominator(self):
        row = W06ExtractionFixtures.applicable_but_unresolved()
        self.assertEqual(row['evidence_status'], APPLICABLE_BUT_UNRESOLVED)
        self.assertEqual(int(row['directionally_applicable_count']), 1)
        self.assertEqual(int(row['nonpromotable_count']), 1)
        self.assertEqual(int(row['promotable_count']), 0)

    def test_observed_zero_is_evidence_not_absence(self):
        row = W06ExtractionFixtures.observed_zero()
        self.assertEqual(row['evidence_status'], OBSERVED_ZERO)
        self.assertEqual(int(row['promotable_count']), 1)
        self.assertEqual(row['overall_status'], 'valid_observed_zero')

    def test_legacy_empty_atoms_do_not_certify_or_fail_integrity(self):
        row = W06ExtractionFixtures.package(atoms=pd.DataFrame())
        self.assertEqual(row['run_integrity_status'], 'UNKNOWN')
        self.assertEqual(int(row['promotable_count']), 0)
        self.assertEqual(row['overall_status'], 'integrity_unknown')

    def test_explicit_manifest_permission_is_preserved(self):
        row = W06ExtractionFixtures.package(manifest={'run_integrity_status': 'PASS', 'evidence_status': 'NO_APPLICABLE_EVIDENCE', 'downstream_permission_status': 'ALLOWED'})
        self.assertEqual(row['downstream_permission_status'], 'ALLOWED')

class TestW06ArtifactLoadIntegrity(unittest.TestCase):

    def test_valid_empty_parquet_is_not_read_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'empty.parquet'
            path.touch()
            with mock.patch('data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet', return_value=pd.DataFrame(columns=['x'])):
                result = _load_parquet_result(path, label='fixture')
        self.assertEqual(result.load_status, 'VALID_EMPTY')
        self.assertEqual(len(result.frame), 0)

    def test_unreadable_parquet_is_not_valid_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'corrupt.parquet'
            path.write_bytes(b'not parquet')
            with mock.patch('data.ddm_build_copy.run_v550_552_extraction_audit.pd.read_parquet', side_effect=ValueError('corrupt')):
                result = _load_parquet_result(path, label='fixture')
        self.assertEqual(result.load_status, 'READ_ERROR')
        self.assertEqual(result.error, 'ValueError')

    def test_missing_parquet_is_distinct_from_read_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = _load_parquet_result(Path(tmp) / 'missing.parquet', label='fixture')
        self.assertEqual(result.load_status, 'MISSING')
if __name__ == '__main__':
    unittest.main()
