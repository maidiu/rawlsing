"""Source-free, contract-local D02Z tests. No original official byte custody."""
import copy
import json
import pathlib
import unittest

from pre553_documentary_rule_source_contract_candidate import (
    CONTRACT_ID, HELD_OPERATIONS, inspect_source_preimage,
    evaluate_requested_operation
)
ROOT = pathlib.Path(__file__).resolve().parent.parent

class DocumentaryRuleCandidateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.fixture = json.loads((ROOT / "01_DOCUMENTARY_SOURCE_IMMUTABLE_PREIMAGE.json").read_text())
        cls.base = cls.fixture["source_local_input"]

    def test_positive_shape_is_not_issued(self):
        result = inspect_source_preimage(copy.deepcopy(self.base))
        self.assertEqual(result.state, "LOCAL_PREIMAGE_SHAPE_POSITIVE__NOT_ISSUED")
        self.assertEqual(result.proposed_rule_class, "RULE_TEXT_DOCUMENTED")
        self.assertIsNone(result.issued_fact_ref)
        self.assertIsNone(result.source_document_pdf_sha256)
        self.assertFalse(result.permitted_externally_active_uses)

    def test_deterministic_local_replay(self):
        a = inspect_source_preimage(copy.deepcopy(self.base)).to_jsonable()
        b = inspect_source_preimage(copy.deepcopy(self.base)).to_jsonable()
        self.assertEqual(a,b)
        self.assertRegex(a["canonical_input_sha256"], r"^[0-9a-f]{64}$")
        self.assertNotEqual(a["canonical_input_sha256"], a["source_document_pdf_sha256"])

    def test_all_fixture_mutations_and_expected_states(self):
        fixtures = json.loads((ROOT/"03_RULE_TEXT_ORIGINAL_POSITIVE_AND_NEGATIVE_FIXTURES.json").read_text())
        self.assertGreaterEqual(len(fixtures["cases"]), 20)
        for fixture in fixtures["cases"]:
            with self.subTest(fixture=fixture["id"]):
                input_value = copy.deepcopy(self.base)
                for k,v in fixture.get("replace",{}).items():
                    input_value[k] = v
                for k in fixture.get("remove",[]):
                    input_value.pop(k,None)
                op = fixture.get("operation","INSPECT_UNISSUED_DOCUMENTARY_PREIMAGE")
                observed = evaluate_requested_operation(input_value, op)
                self.assertEqual(observed["state"],fixture["expected_state"])
                self.assertIsNone(observed["issued_fact_ref"])
                self.assertEqual(observed["preimage"]["candidate_only"],True)

    def test_production_operations_always_held_or_refused(self):
        for op, expected in HELD_OPERATIONS.items():
            with self.subTest(operation=op):
                res = evaluate_requested_operation(self.base, op)
                self.assertEqual(res["state"],expected)
                self.assertIsNone(res["issued_fact_ref"])

    def test_wrong_type_fails_closed(self):
        for obj in [None, [], "document", 0]:
            with self.subTest(obj=obj):
                self.assertEqual(inspect_source_preimage(obj).state,"REFUSED_LOCAL_PREIMAGE")

    def test_hash_is_local_json_not_original_source(self):
        res = inspect_source_preimage(self.base).to_jsonable()
        self.assertIsNotNone(res["canonical_input_sha256"])
        self.assertIsNone(res["source_document_pdf_sha256"])

if __name__ == "__main__":
    unittest.main()
