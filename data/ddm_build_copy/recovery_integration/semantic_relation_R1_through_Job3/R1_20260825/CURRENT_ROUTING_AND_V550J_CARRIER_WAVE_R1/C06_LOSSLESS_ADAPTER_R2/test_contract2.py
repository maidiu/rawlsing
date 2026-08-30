from __future__ import annotations

import unittest
from unittest.mock import patch

import compile_contract2 as c2


class Contract2HostileTests(unittest.TestCase):
    def fixture(self):
        catalog = {}
        rows = []
        dispositions = [
            "GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
            "POSITIVE_EXECUTABLE_ROUTING_AUTHORITY",
            "GOVERNED_SCOPED_NONAPPLICABILITY",
            c2.UNRESOLVED,
        ]
        for i, disp in enumerate(dispositions):
            qid = f"q{i}"
            family = "C05F" if i == 3 else f"F{i}"
            catalog[qid] = {"question_implementation_id": qid, "source_family": family, "wave": f"W{i}", "source_variable_code": f"V{i}"}
            rows.append({
                "contract_version": c2.CONTRACT,
                "question_implementation_id": qid,
                "source_family": family,
                "wave": f"W{i}",
                "source_variable_code": f"V{i}",
                "disposition": disp,
                "source_court": "C05_FIXTURE" if i == 3 else "FIXTURE",
                "source_commit": "a" * 40,
                "source_carrier_ref": "fixture://carrier",
                "source_carrier_identity": "sha256:" + "b" * 64,
                "source_row_selector": f"row:{i}",
                "source_row_record_sha256": "c" * 64,
                "unresolved_token_kind": "NOT_EMITTED_AT_ROW_GRAIN" if i == 3 else "",
                "unresolved_token": "",
            })
        counts = {}
        for row in rows:
            counts[row["disposition"]] = counts.get(row["disposition"], 0) + 1
        return catalog, rows, counts

    def test_contract_is_not_old_26_column_schema(self):
        self.assertEqual(c2.CONTRACT, "CURRENT_ROUTING_LEDGER_CONTRACT@2")
        self.assertNotIn("evidence_authority_type", c2.LEDGER_COLUMNS)
        self.assertIn("source_carrier_ref", c2.LEDGER_COLUMNS)
        self.assertIn("source_row_record_sha256", c2.LEDGER_COLUMNS)

    def test_non_unresolved_cannot_carry_taxonomy_token(self):
        with self.assertRaisesRegex(c2.Contract2Error, "non-unresolved"):
            c2.contract_row(
                qid="q", family="F", wave="W", var="V",
                disposition="GOVERNED_GENERAL_OR_UNCONDITIONAL_UNIVERSE",
                court="FIX", commit="a" * 40, carrier_ref="x", carrier_identity="y",
                selector="0", source_row={"x": 1}, token_kind="BLOCKER", token="invented",
            )

    def test_exact_set_and_coordinates_pass(self):
        catalog, rows, counts = self.fixture()
        with patch.object(c2, "EXPECTED_ROWS", 4), patch.object(c2, "EXPECTED_COUNTS", counts):
            receipt = c2.validate_join(rows, catalog)
        self.assertEqual(receipt["missing"], 0)
        self.assertEqual(receipt["duplicates"], 0)
        self.assertEqual(receipt["coordinate_drift"], 0)

    def test_duplicate_id_fails_closed(self):
        catalog, rows, counts = self.fixture()
        rows[-1]["question_implementation_id"] = rows[0]["question_implementation_id"]
        with patch.object(c2, "EXPECTED_ROWS", 4), patch.object(c2, "EXPECTED_COUNTS", counts):
            with self.assertRaisesRegex(c2.Contract2Error, "ID accounting failed"):
                c2.validate_join(rows, catalog)

    def test_coordinate_drift_fails_closed(self):
        catalog, rows, counts = self.fixture()
        rows[0]["wave"] = "COUNTERFEIT_WAVE"
        with patch.object(c2, "EXPECTED_ROWS", 4), patch.object(c2, "EXPECTED_COUNTS", counts):
            with self.assertRaisesRegex(c2.Contract2Error, "identity-coordinate drift"):
                c2.validate_join(rows, catalog)

    def test_disposition_mutation_fails_closed(self):
        catalog, rows, counts = self.fixture()
        rows[0]["disposition"] = c2.UNRESOLVED
        with patch.object(c2, "EXPECTED_ROWS", 4), patch.object(c2, "EXPECTED_COUNTS", counts):
            with self.assertRaisesRegex(c2.Contract2Error, "frozen disposition vector mismatch"):
                c2.validate_join(rows, catalog)

    def test_c05_row_level_blocker_synthesis_fails_closed(self):
        catalog, rows, counts = self.fixture()
        rows[-1]["unresolved_token_kind"] = "UNRESOLVED_BLOCKER_CLASS"
        rows[-1]["unresolved_token"] = "AGGREGATE_COUNT_COUNTERFEIT"
        with patch.object(c2, "EXPECTED_ROWS", 4), patch.object(c2, "EXPECTED_COUNTS", counts):
            with self.assertRaisesRegex(c2.Contract2Error, "C05 row-level blocker synthesis detected"):
                c2.validate_join(rows, catalog)

    def test_exact_production_invariants_are_pinned(self):
        self.assertEqual(c2.EXPECTED_ROWS, 18_276)
        self.assertEqual(c2.EXPECTED_COUNTS[c2.UNRESOLVED], 14_386)
        self.assertEqual(sum(c2.EXPECTED_COUNTS.values()), 18_276)
        self.assertEqual(c2.C02_SHA256, "0197c20dc6d48106d6070d8b1ba390d43815cd36d92e2f03e70cad04a0a1be4d")
        self.assertEqual(c2.C03_CANONICAL_SHA256, "b08b5e4b539cd7936ad24c04a45d8b8e672913f1656482ffc0d3dce5437a095c")
        self.assertEqual(c2.C04_SHA256, "c3148341c5a6315c4b060f665595c93c4aa935dfc171aa5faf4c14628f914f90")
        self.assertEqual(c2.C05_PAIR_SHA256, "1d72efe346cced887b65e396b0f69645e668415e7dd9cbc69b9e69d420498013")


if __name__ == "__main__":
    unittest.main(verbosity=2)
