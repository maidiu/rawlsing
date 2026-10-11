"""HQ280 PV3 D02 source-free court on the exact existing D07 objective-consumer owner.

Run from repository root:
  PYTHONPATH=. python WORKER_RETURNS/PYAT-HQ280-PV3-D02-OBJECTIVE-PRODUCT-CANDIDATE-R1/repro/test_d02_sourcefree_objective_policy.py

All inputs are synthetic; a positive OC02 policy receipt is not original-source
authentication, Field Forge admission, N9 CURRENT, EE14 G0b, or actor/V3.
"""
import hashlib
import unittest
from dataclasses import replace

from rawlsing_next import objective_consumer_bounded_evidence as o

def ref(kind, identifier):
    return o.ExactRef(kind, f"d02-fixture:{identifier}", hashlib.sha256(f"{kind}/{identifier}".encode()).hexdigest())

def present(name, *, ceiling=o.ClaimCeiling.STRUCTURAL_RELATION, tier=o.EvidenceTier.PARTIAL_AUTHORITY, required=True, source="FAMILY_A"):
    return o.PolicyInput(name, required, True, o.EvidenceKind.EMPIRICAL, tier, ceiling,
                         ref("FIXTURE_PRODUCER", f"{source}:{name}"),
                         (ref("FIXTURE_AUTHORITY", f"{source}:{name}"),))

def missing(name, *, required=True, reason="EXTERNAL_INSTITUTION_SOURCE_NOT_QUALIFIED"):
    return o.PolicyInput(name, required, False, o.EvidenceKind.EMPIRICAL, o.EvidenceTier.UNAVAILABLE,
                         o.ClaimCeiling.SUPPORTED_COMPONENT_ONLY, omission_reason=reason)

class ObjectiveSourcefreeOwnerCourt(unittest.TestCase):
    def test_01_oc01_source_local_positive_not_structural(self):
        x = present("AFRO_REPORTED_ATTITUDE", ceiling=o.ClaimCeiling.SOURCE_LOCAL_STATISTIC,
                    tier=o.EvidenceTier.SOURCE_LOCAL_CERTIFIED)
        r = o.evaluate_oc01_pre553_source_local(operation_id="D02_SYNTH_OC01", inputs=(x,),
                                                requested_claim_ceiling=o.ClaimCeiling.SOURCE_LOCAL_STATISTIC)
        self.assertEqual(r.state, o.DecisionState.SUPPORTED_OBJECTIVE_RESULT)
        self.assertEqual(r.requested_claim_ceiling, o.ClaimCeiling.SOURCE_LOCAL_STATISTIC)

    def test_02_context_cannot_become_structural(self):
        x = present("AFRO_GT2_CONTEXT", ceiling=o.ClaimCeiling.SOURCE_LOCAL_STATISTIC)
        r = o.evaluate_oc02_structural_admission(operation_id="D02_CONTEXT", inputs=(x,))
        self.assertEqual(r.state, o.DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE)
        self.assertIn("CLAIM_CEILING_NOT_AUTHORIZED:AFRO_GT2_CONTEXT", r.refusal_reasons)

    def test_03_lits_reported_opinion_not_institution(self):
        x = present("LITS_SUBJECTIVE", ceiling=o.ClaimCeiling.SUPPORTED_COMPONENT_ONLY)
        r = o.evaluate_oc02_structural_admission(operation_id="D02_LITS", inputs=(x,))
        self.assertFalse(r.positive_completion)

    def test_04_prequalified_sourcefree_fixture_local_policy_positive(self):
        x = present("HYPOTHETICAL_EXTERNAL_STRUCTURE")
        r = o.evaluate_oc02_structural_admission(operation_id="D02_FIXTURE_POSITIVE", inputs=(x,))
        self.assertEqual(r.state, o.DecisionState.SUPPORTED_OBJECTIVE_RESULT)
        self.assertEqual(r.consumer_seam, "rawlsing_next.pre553_structural_admission")
        self.assertTrue(r.positive_completion)

    def test_05_required_source_absent_typed(self):
        r = o.evaluate_oc02_structural_admission(operation_id="D02_ABSENT", inputs=(missing("INSTITUTION"),))
        self.assertEqual(r.state, o.DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION)
        self.assertEqual(r.missing_required_input_ids, ("INSTITUTION",))
        self.assertFalse(r.positive_completion)

    def test_06_context_plus_missing_required_refusal(self):
        r = o.evaluate_oc02_structural_admission(operation_id="D02_MIXED", inputs=(
            present("CONTEXT", ceiling=o.ClaimCeiling.SOURCE_LOCAL_STATISTIC), missing("INSTITUTION")))
        self.assertEqual(r.state, o.DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE)

    def test_07_partial_optional_not_full(self):
        r = o.evaluate_current_consumer(policy_id=o.OC02, operation_id="D02_PARTIAL", inputs=(
            present("HYPOTHETICAL_STRUCTURE"), missing("OPTIONAL", required=False)),
            requested_claim_ceiling=o.ClaimCeiling.STRUCTURAL_RELATION, partial_allowed=True)
        self.assertEqual(r.state, o.DecisionState.PARTIAL_OBJECTIVE_RESULT)
        self.assertEqual(r.omitted_optional_input_ids, ("OPTIONAL",))

    def test_08_strict_optional_loss_refusal(self):
        r = o.evaluate_oc02_structural_admission(operation_id="D02_STRICT", inputs=(
            present("HYPOTHETICAL_STRUCTURE"), missing("OPTIONAL", required=False)))
        self.assertEqual(r.state, o.DecisionState.REFUSED_REQUIRED_OBJECTIVE_EVIDENCE)

    def test_09_nonemp_model_not_external_evidence(self):
        x = o.PolicyInput("PRIOR", True, True, o.EvidenceKind.NON_EMPIRICAL_MODEL,
                          o.EvidenceTier.PARTIAL_AUTHORITY, o.ClaimCeiling.STRUCTURAL_RELATION,
                          ref("MODEL", "prior"), (ref("AUTH", "prior"),),
                          model_prior_version="test-only-1", model_prior_authority_ref=ref("MODEL_AUTH", "prior"))
        r = o.evaluate_oc02_structural_admission(operation_id="D02_PRIOR", inputs=(x,))
        self.assertEqual(r.state, o.DecisionState.ALL_UNAVAILABLE__NOT_POSITIVE_COMPLETION)
        self.assertEqual(r.non_empirical_input_ids, ("PRIOR",))

    def test_10_unwarranted_substitution_refused(self):
        with self.assertRaises(o.RelationAuthorityRequired):
            replace(present("SUB"), substitution=True)

    def test_11_missing_with_positive_ref_refused(self):
        with self.assertRaises(o.MissingAsValueError):
            replace(missing("NOT_SOURCE"), producer_ref=ref("PRODUCER", "fake"))

    def test_12_renormalization_refused(self):
        with self.assertRaises(o.RenormalizationForbidden):
            o.evaluate_oc02_structural_admission(operation_id="D02_RENORM", inputs=(present("X"),),
                                                  renormalization_requested=True)

    def test_13_order_invariance_but_authority_matters(self):
        x, y = present("X"), present("Y")
        a = o.evaluate_oc02_structural_admission(operation_id="D02_HASH", inputs=(x, y))
        b = o.evaluate_oc02_structural_admission(operation_id="D02_HASH", inputs=(y, x))
        c = o.evaluate_oc02_structural_admission(operation_id="D02_HASH", inputs=(
            x, replace(y, authority_refs=(ref("AUTH", "altered"),))))
        self.assertEqual(a.receipt_hash, b.receipt_hash)
        self.assertNotEqual(a.receipt_hash, c.receipt_hash)

    def test_14_population_mismatch_owner_acceptance_is_gap_not_pass(self):
        x, y = present("A", source="FAMILY_A"), present("B", source="FAMILY_B")
        r = o.evaluate_oc02_structural_admission(operation_id="D02_GAP_MISMATCH", inputs=(x, y))
        self.assertTrue(r.positive_completion)  # demonstrates omitted population verification
        self.assertEqual(len(r.selected_producer_refs), 2)

    def test_15_forged_source_label_owner_acceptance_is_gap_not_pass(self):
        r = o.evaluate_oc02_structural_admission(operation_id="D02_GAP_FABRICATED", inputs=(
            present("FAKE_INSTITUTION", source="NO_ORIGINAL_SOURCE"),))
        self.assertTrue(r.positive_completion)  # does NOT authenticate its alleged producer

    def test_16_fake_n9_current_not_applicable(self):
        with self.assertRaises(o.NotYetApplicableConsumer):
            o.evaluate_current_consumer(policy_id=o.OC05, operation_id="D02_CURRENT", inputs=(present("X"),),
                                        requested_claim_ceiling=o.ClaimCeiling.STRUCTURAL_RELATION, partial_allowed=False)

    def test_17_objective_fact_not_relation(self):
        r = o.evaluate_oc02_structural_admission(operation_id="D02_FACT_ONLY", inputs=(
            present("FACT", ceiling=o.ClaimCeiling.OBJECTIVE_FACT),))
        self.assertFalse(r.positive_completion)

    def test_18_duplicate_input_rejected(self):
        with self.assertRaises(o.PolicyError):
            o.evaluate_oc02_structural_admission(operation_id="D02_DUP", inputs=(present("X"),present("X")))

if __name__ == "__main__":
    unittest.main(verbosity=2)
