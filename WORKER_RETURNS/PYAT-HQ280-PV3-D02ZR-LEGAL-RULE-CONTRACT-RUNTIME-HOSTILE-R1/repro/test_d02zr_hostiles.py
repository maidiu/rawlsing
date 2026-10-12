"""D02ZR independent hostile tests for the D02Z documentary-rule candidate.

These tests are authored by the independent reviewer, not by D02Z. They attack
source identity, statutory wording, historical-version dates, issuer claims,
local JSON hashes masquerading as original document custody, and attempts to
manufacture N5/N6/N9 operative states.
"""
from __future__ import annotations

import json
from hashlib import sha256
import unittest

from pre553_documentary_rule_source_contract_candidate import (
    EXACT_FIELDS,
    MUST_BE_NULL,
    HELD_OPERATIONS,
    inspect_source_preimage,
    evaluate_requested_operation,
)


def _valid_input() -> dict:
    """A shape-valid input: all EXACT_FIELDS correct, all MUST_BE_NULL None."""
    return {**EXACT_FIELDS, **{k: None for k in MUST_BE_NULL}}


class D02ZRIndependentHostiles(unittest.TestCase):
    """Independent hostile tests. None of these were authored by D02Z."""

    def test_wrong_clause_id_refused(self):
        """PART_I_SECTION_7 must not be substituted with another clause."""
        value = _valid_input()
        value["clause_id"] = "PART_II_SECTION_15"
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:clause_id", result.reasons)

    def test_wrong_legal_document_id_refused(self):
        """ACT_591_2000 must not be substituted."""
        value = _valid_input()
        value["legal_document_id"] = "ACT_591_1992_ORIGINAL"
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:legal_document_id", result.reasons)

    def test_wrong_parent_wording_refused(self):
        """Qualifying ancestor roles must be exactly PARENT, GRANDPARENT."""
        value = _valid_input()
        value["qualifying_ancestor_roles"] = ["PARENT", "GRANDPARENT", "GREAT_GRANDPARENT"]
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:qualifying_ancestor_roles", result.reasons)

    def test_wrong_grandparent_wording_refused(self):
        value = _valid_input()
        value["qualifying_ancestor_roles"] = ["PARENT", "GREAT_GRANDPARENT"]
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:qualifying_ancestor_roles", result.reasons)

    def test_wrong_time_boundary_refused(self):
        """Birth cohort date must be exactly 1993-01-07."""
        value = _valid_input()
        value["birth_cohort_date"] = "1993-01-08"
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:birth_cohort_date", result.reasons)

    def test_wrong_assent_date_refused(self):
        value = _valid_input()
        value["assent_date"] = "2000-12-30"
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:assent_date", result.reasons)

    def test_wrong_source_url_refused(self):
        value = _valid_input()
        value["source_url"] = "https://example.com/not-the-official-source.pdf"
        result = inspect_source_preimage(value)
        self.assertIn("CLAUSE_OR_SOURCE_SEMANTIC_MISMATCH:source_url", result.reasons)

    def test_unsigned_issuer_metadata_refused(self):
        """A non-null producer_issuer_ref is an unproved authority claim."""
        value = _valid_input()
        value["producer_issuer_ref"] = "urn:forged:issuer"
        result = inspect_source_preimage(value)
        self.assertIn("FORBIDDEN_UNPROVED_AUTHORITY_OR_OUTCOME:producer_issuer_ref", result.reasons)

    def test_issued_fact_ref_masquerade_refused(self):
        """A non-null issued_fact_ref claims an issued fact that does not exist."""
        value = _valid_input()
        value["issued_fact_ref"] = "urn:forged:fact"
        result = inspect_source_preimage(value)
        # issued_fact_ref is not in EXACT_FIELDS or MUST_BE_NULL, so it is an extra key
        self.assertIn("UNAUTHORIZED_EXTRA_KEYS:issued_fact_ref", result.reasons)

    def test_local_sha256_is_not_pdf_custody(self):
        """A local input SHA-256 must never be treated as custody of the original PDF."""
        value = _valid_input()
        result = inspect_source_preimage(value)
        self.assertIsNone(result.source_document_pdf_sha256)
        self.assertIsNone(result.issued_fact_ref)
        self.assertIsNone(result.competent_issuer_ref)
        self.assertEqual(result.permitted_externally_active_uses, ())
        self.assertTrue(result.candidate_only)

    def test_local_sha256_is_not_original_document_identity(self):
        """The canonical_input_sha256 is a local JSON hash, not original document custody."""
        value = _valid_input()
        result = inspect_source_preimage(value)
        # The hash is computed from the local JSON input, not from a government PDF
        blob = json.dumps(value, sort_keys=True, ensure_ascii=False,
                          separators=(",", ":"), allow_nan=False)
        local_hash = sha256(blob.encode("utf-8")).hexdigest()
        self.assertEqual(result.canonical_input_sha256, local_hash)
        self.assertIsNone(result.source_document_pdf_sha256)

    def test_altered_json_identity_changes_hash(self):
        """Altering any field changes the canonical hash (local JSON identity)."""
        value1 = _valid_input()
        value2 = _valid_input()
        value2["clause_id"] = "PART_I_SECTION_8"
        result1 = inspect_source_preimage(value1)
        result2 = inspect_source_preimage(value2)
        self.assertNotEqual(result1.canonical_input_sha256, result2.canonical_input_sha256)

    def test_operative_state_assertion_refused(self):
        """Attempting to assert a current/operative state is refused."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "ASSERT_OPERATIVE_CURRENT_STATE")
        self.assertEqual(result["state"], "REFUSED_UNKNOWN_OPERATION")
        self.assertIsNone(result["issued_fact_ref"])

    def test_n9_current_refused(self):
        """SERVE_N9_CURRENT is HELD — no issued rule source root or selected world."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "SERVE_N9_CURRENT")
        self.assertEqual(result["state"],
                         "HELD_NO_CURRENT_LEGAL_VERSION_OR_SELECTED_WORLD")
        self.assertIsNone(result["issued_fact_ref"])

    def test_n9_historical_refused(self):
        """SERVE_N9_HISTORICAL is HELD — no issued rule source root or N9 consumer."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "SERVE_N9_HISTORICAL")
        self.assertEqual(result["state"],
                         "HELD_NO_ISSUED_RULE_SOURCE_ROOT_OR_N9_CONSUMER")

    def test_g0b_refused(self):
        """G0B_OR_ACTOR_V3 is REFUSED — no model or actor use grant."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "G0B_OR_ACTOR_V3")
        self.assertEqual(result["state"], "REFUSED_NO_MODEL_OR_ACTOR_USE_GRANT")

    def test_empirical_fact_refused(self):
        """EMIT_EMPIRICAL_FACT is REFUSED — wrong empirical object family."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "EMIT_EMPIRICAL_FACT")
        self.assertEqual(result["state"], "REFUSED_WRONG_EMPIRICAL_OBJECT_FAMILY")

    def test_causal_assertion_refused(self):
        """ASSERT_CAUSAL_MECHANISM is REFUSED — no causal mechanism authority."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "ASSERT_CAUSAL_MECHANISM")
        self.assertEqual(result["state"], "REFUSED_NO_CAUSAL_MECHANISM_AUTHORITY")

    def test_enforcement_assertion_refused(self):
        """ASSERT_ENFORCEMENT is REFUSED — no official administrative observation."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "ASSERT_ENFORCEMENT")
        self.assertEqual(result["state"],
                         "REFUSED_NO_OFFICIAL_ADMINISTRATIVE_OBSERVATION")

    def test_person_citizenship_assertion_refused(self):
        """INTERPRET_PERSON_CITIZENSHIP is REFUSED — no person case facts."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "INTERPRET_PERSON_CITIZENSHIP")
        self.assertEqual(result["state"],
                         "REFUSED_NO_PERSON_CASE_FACTS_OR_LEGAL_ADJUDICATION")

    def test_rule_text_documented_held(self):
        """ISSUE_RULE_TEXT_DOCUMENTED is HELD — no competent issuer."""
        value = _valid_input()
        result = evaluate_requested_operation(value, "ISSUE_RULE_TEXT_DOCUMENTED")
        self.assertEqual(result["state"],
                         "HELD_COMPETENT_ORIGINAL_SOURCE_ISSUER_AND_PRODUCER_ADOPTION")

    def test_omitted_required_key_refused(self):
        """Omitting a required key refuses."""
        value = _valid_input()
        del value["jurisdiction"]
        result = inspect_source_preimage(value)
        self.assertIn("MISSING_REQUIRED_KEYS:jurisdiction", result.reasons)

    def test_extra_key_refused(self):
        """Adding an unauthorized extra key refuses."""
        value = _valid_input()
        value["unexpected_key"] = "x"
        result = inspect_source_preimage(value)
        self.assertIn("UNAUTHORIZED_EXTRA_KEYS:unexpected_key", result.reasons)

    def test_non_dict_refused(self):
        """A non-dict input refuses."""
        result = inspect_source_preimage("not a dict")
        self.assertEqual(result.state, "REFUSED_LOCAL_PREIMAGE")

    def test_as_enacted_text_is_not_person_outcome(self):
        """An as-enacted textual description is not a person-level outcome."""
        value = _valid_input()
        result = inspect_source_preimage(value)
        self.assertIsNone(result.issued_fact_ref)
        self.assertIsNone(result.competent_issuer_ref)
        # The documentary_assertion field explicitly states this
        self.assertEqual(value["documentary_assertion"],
                         "SOURCE_TEXT_PREIMAGE_CANDIDATE_ONLY")

    def test_original_pdf_byte_custody_not_custodied(self):
        """original_pdf_byte_custody is NOT_CUSTODIED — no PDF bytes are held."""
        value = _valid_input()
        result = inspect_source_preimage(value)
        self.assertEqual(value["original_pdf_byte_custody"], "NOT_CUSTODIED")
        self.assertIsNone(result.source_document_pdf_sha256)

    def test_35_fixture_cases_all_execute(self):
        """Independently execute all 35 D02Z fixture cases per the documented protocol."""
        import copy
        import os
        here = os.path.dirname(os.path.abspath(__file__))
        candidates = [
            os.path.join(here, "..",
                         "03_RULE_TEXT_ORIGINAL_POSITIVE_AND_NEGATIVE_FIXTURES.json"),
            os.path.join(here, "..", "..",
                         "PYAT-HQ280-PV3-D02Z-NATIVE-LEGAL-RULE-PRODUCER-CONTRACT-R1",
                         "03_RULE_TEXT_ORIGINAL_POSITIVE_AND_NEGATIVE_FIXTURES.json"),
            os.path.join(here, "..", "..",
                         "PYAT-HQ280-PV3-D02Z-NATIVE-LEGAL-RULE-PRODUCER-CONTRACT-R1",
                         "repro",
                         "03_RULE_TEXT_ORIGINAL_POSITIVE_AND_NEGATIVE_FIXTURES.json"),
        ]
        base_candidates = [
            os.path.join(here, "..",
                         "01_DOCUMENTARY_SOURCE_IMMUTABLE_PREIMAGE.json"),
            os.path.join(here, "..", "..",
                         "PYAT-HQ280-PV3-D02Z-NATIVE-LEGAL-RULE-PRODUCER-CONTRACT-R1",
                         "01_DOCUMENTARY_SOURCE_IMMUTABLE_PREIMAGE.json"),
        ]
        fixture_path = next(p for p in candidates if os.path.isfile(p))
        base_path = next(p for p in base_candidates if os.path.isfile(p))
        with open(fixture_path) as f:
            fixtures = json.load(f)
        with open(base_path) as f:
            base = json.load(f)["source_local_input"]
        self.assertEqual(fixtures.get("case_count"), 35)
        self.assertEqual(len(fixtures["cases"]), 35)
        for case in fixtures["cases"]:
            with self.subTest(fixture=case["id"]):
                input_value = copy.deepcopy(base)
                for k, v in case.get("replace", {}).items():
                    input_value[k] = v
                for k in case.get("remove", []):
                    input_value.pop(k, None)
                op = case.get("operation", "INSPECT_UNISSUED_DOCUMENTARY_PREIMAGE")
                observed = evaluate_requested_operation(input_value, op)
                self.assertEqual(observed["state"], case["expected_state"])
                self.assertIsNone(observed["issued_fact_ref"])
                self.assertTrue(observed["preimage"]["candidate_only"])


if __name__ == "__main__":
    unittest.main()