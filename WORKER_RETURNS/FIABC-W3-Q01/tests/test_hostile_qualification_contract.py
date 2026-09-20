from __future__ import annotations

import json
from pathlib import Path
import unittest

from qualification_contract import QualificationFailure, VALIDATORS


FIXTURE_PATH = Path(__file__).resolve().parents[1] / "02_HOSTILE_FIXTURES.json"


class Wave3HostileQualificationContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.document = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
        cls.fixtures = cls.document["fixtures"]

    def test_fixture_schema_and_unique_ids(self):
        self.assertEqual(self.document["schema"], "FIABC_W3_Q01_HOSTILE_FIXTURES@1.0.0")
        self.assertEqual(self.document["base_sha"], "56697a27e94eb9603dfa412a15ab8f1feb819b0c")
        ids = [fixture["id"] for fixture in self.fixtures]
        self.assertEqual(len(ids), len(set(ids)))
        self.assertTrue(ids)

    def test_all_required_validator_families_present(self):
        present = {fixture["validator"] for fixture in self.fixtures}
        self.assertEqual(present, set(VALIDATORS))

    def test_positive_controls_pass(self):
        positives = [fixture for fixture in self.fixtures if fixture["expected_result"] == "PASS"]
        self.assertGreaterEqual(len(positives), len(VALIDATORS))
        for fixture in positives:
            with self.subTest(fixture=fixture["id"]):
                VALIDATORS[fixture["validator"]](fixture["payload"])

    def test_negative_fixtures_reject_with_exact_code(self):
        negatives = [fixture for fixture in self.fixtures if fixture["expected_result"] == "REJECT"]
        self.assertGreaterEqual(len(negatives), 20)
        for fixture in negatives:
            with self.subTest(fixture=fixture["id"]):
                with self.assertRaises(QualificationFailure) as caught:
                    VALIDATORS[fixture["validator"]](fixture["payload"])
                self.assertEqual(caught.exception.code, fixture["expected_code"])

    def test_mission_minimum_risks_have_explicit_negative_fixture(self):
        required = {
            "Q01-DIAG-001", "Q01-DIAG-002", "Q01-NEFF-001",
            "Q01-CANDC-001", "Q01-CANDC-002", "Q01-CANDC-003",
            "Q01-CANDC-004", "Q01-CANDC-005", "Q01-PKG-001",
            "Q01-PKG-002", "Q01-ORACLE-001", "Q01-ORACLE-002",
            "Q01-METRIC-001", "Q01-METRIC-002", "Q01-METRIC-003",
            "Q01-METRIC-004", "Q01-METRIC-005", "Q01-PREFLIGHT-001",
            "Q01-TERM-001", "Q01-TERM-002"
        }
        present = {fixture["id"] for fixture in self.fixtures}
        self.assertTrue(required.issubset(present), sorted(required - present))


if __name__ == "__main__":
    unittest.main()
