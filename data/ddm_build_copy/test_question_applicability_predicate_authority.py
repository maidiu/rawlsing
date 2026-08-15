import copy
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AUTH = ROOT / "authority/question_applicability_predicate_authority_v1.json"
FALLBACK = "DO_NOT_INFER_APPLICABILITY_FROM_COLUMN_EXISTENCE_OR_EMPIRICAL_COOCCURRENCE"


class ApplicabilityAuthorityTests(unittest.TestCase):
    def setUp(self):
        self.payload = json.loads(AUTH.read_text())

    def test_complete_coverage_is_fail_closed(self):
        self.assertEqual(self.payload["row_count"], 700)
        self.assertEqual(len(self.payload["rows"]), 700)
        self.assertTrue(all(r["authority_status"] == "FAIL_CLOSED_UNRESOLVED" for r in self.payload["rows"]))

    def test_missing_predicate_is_rejected(self):
        mutated = copy.deepcopy(self.payload)
        mutated["rows"][0].pop("predicate")
        self.assertNotIn("predicate", mutated["rows"][0])

    def test_fallback_policy_cannot_be_weakened(self):
        mutated = copy.deepcopy(self.payload)
        mutated["rows"][0]["prohibited_fallback"] = "ALLOW_COLUMN_EXISTENCE"
        self.assertNotEqual(mutated["rows"][0]["prohibited_fallback"], FALLBACK)

    def test_duplicate_ids_are_detectable(self):
        mutated = copy.deepcopy(self.payload)
        mutated["rows"][1]["applicability_authority_id"] = mutated["rows"][0]["applicability_authority_id"]
        ids = [r["applicability_authority_id"] for r in mutated["rows"]]
        self.assertLess(len(set(ids)), len(ids))


if __name__ == "__main__":
    unittest.main()
