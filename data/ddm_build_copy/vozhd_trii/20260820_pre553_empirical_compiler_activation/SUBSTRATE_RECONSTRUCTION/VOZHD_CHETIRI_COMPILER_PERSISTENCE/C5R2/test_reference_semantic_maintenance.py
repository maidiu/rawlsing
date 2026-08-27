from __future__ import annotations

import json
import unittest

from reference_semantic_maintenance import (
    Candidate,
    DependencyBinding,
    EvidenceBundle,
    ExactRef,
    FamilyPolicyRegistry,
    GenealogyEdge,
    GenealogyType,
    GovernedGenealogyDecision,
    GovernedDecision,
    LifecycleEvent,
    LifecycleType,
    Pre553SemanticMaintenanceOwner,
    Pre553SemanticReleaseExecutor,
    SemanticMaintenanceError,
    build_authoritative_witness,
    make_ref,
    OWNER_CONTRACT,
)


def fixture():
    owner = Pre553SemanticMaintenanceOwner()
    executor = Pre553SemanticReleaseExecutor(owner)
    family_rule = make_ref("SEMANTIC_FAMILY_RULE", "T06_RULE_TEST", {"family": "T06"})
    binding = make_ref("EVIDENCE_BINDING_AUTHORITY", "BINDING_TEST", {"complete": True})
    decision_auth = make_ref("COURT_DECISION_AUTHORITY", "C5R2_TEST", OWNER_CONTRACT)
    evidence = make_ref("SOURCE_EVIDENCE", "DOC-1", {"text": "fixture"})
    owner.register_governance_authority(decision_auth)
    owner.register_family_rule("T06", family_rule)
    bundle = EvidenceBundle("EB-T", (evidence,), "COMPLETE", binding)
    owner.bind_evidence(bundle)
    candidate = Candidate(
        "CAND-T", "T06", ("N", "C"), (("N", "NORM"), ("C", "CONDUCT")),
        {"actor": "R", "target": "RULE", "action_domain": "COMPLY", "modality": "EXPECTED"},
        {"source": "FIX", "wave": "W1"}, family_rule, bundle.ref,
    )
    return owner, executor, candidate, decision_auth


class C5R2PositiveTests(unittest.TestCase):
    def test_authoritative_end_to_end_witness(self):
        witness = build_authoritative_witness()
        self.assertEqual(witness["status"], "C5R2_AUTHORITATIVE_REFERENCE_WITNESS_PASS")
        self.assertTrue(witness["same_semantic_claim_under_recertification"])
        self.assertEqual(witness["current_release_after_rollback"], witness["predecessor_release_ref"])
        self.assertEqual(witness["exact_replay"]["predecessor_authority"], witness["predecessor_authority_ref"])
        self.assertEqual(witness["exact_replay"]["successor_authority"], witness["successor_authority_ref"])


class C5R2HostileTests(unittest.TestCase):
    def _accepted_authority(self):
        owner, executor, candidate, decision_auth = fixture()
        owner.nominate(candidate)
        decision = owner.adjudicate(GovernedDecision("ADJ-T", candidate.ref, "ACCEPT", decision_auth, "TEST_ACCEPT"))
        authority = owner.create_authority(authority_id="A-T", authority_version="1.0.0", decision=decision)
        return owner, executor, candidate, decision_auth, decision, authority

    def test_nomination_is_not_authority(self):
        owner, _, candidate, _ = fixture()
        owner.nominate(candidate)
        self.assertEqual(len(owner.authorities), 0)

    def test_ambiguous_split_fails_closed(self):
        owner, _, _, decision_auth, decision, authority = self._accepted_authority()
        child1 = authority
        gd = GovernedGenealogyDecision("GD-AMB", GenealogyType.SPLIT, (authority.ref,), (child1.ref,), decision_auth, "AMBIGUOUS", "PARTITION_NOT_GOVERNED")
        with self.assertRaises(SemanticMaintenanceError):
            owner.adjudicate_genealogy(gd)

    def test_split_member_conservation(self):
        owner, _, candidate, decision_auth, decision, authority = self._accepted_authority()
        c1 = Candidate("C1", "T06", ("N", "X"), (("N", "NORM"), ("X", "CONDUCT")), dict(candidate.constitutive_payload), dict(candidate.scope), candidate.family_rule_ref, candidate.evidence_bundle_ref)
        owner.nominate(c1)
        d1 = owner.adjudicate(GovernedDecision("D1", c1.ref, "ACCEPT", decision_auth, "SPLIT_CHILD"))
        a1 = owner.create_authority(authority_id="A1", authority_version="1.0.0", decision=d1)
        gd = owner.adjudicate_genealogy(GovernedGenealogyDecision("GD-LOSS", GenealogyType.SPLIT, (authority.ref,), (a1.ref,), decision_auth, "RESOLVED", "TEST_SPLIT"))
        edge = GenealogyEdge("G-LOSS", GenealogyType.SPLIT, (authority.ref,), (a1.ref,), authority.members, (("N",),), gd.ref)
        with self.assertRaises(SemanticMaintenanceError):
            owner.append_genealogy(edge)

    def test_ungoverned_variant_exclusion_fails_closed(self):
        owner, _, _, _, _, authority = self._accepted_authority()
        bad = ExactRef("SEMANTIC_GENEALOGY_DECISION", "X", "0" * 64)
        edge = GenealogyEdge("G-V", GenealogyType.VARIANT, (authority.ref,), (authority.ref,), authority.members, (authority.members,), bad)
        with self.assertRaises(SemanticMaintenanceError):
            owner.append_genealogy(edge)

    def test_blocked_reopening_is_not_truth(self):
        owner, _, candidate, decision_auth = fixture()
        owner.nominate(candidate)
        blocked = owner.adjudicate(GovernedDecision("ADJ-B", candidate.ref, "BLOCKED", decision_auth, "MISSING_EVIDENCE"))
        self.assertEqual(len(owner.authorities), 0)
        reopen = owner.record_lifecycle(LifecycleEvent("EV-RB", LifecycleType.REOPENS_BLOCKED, blocked.ref, None, "T06|FIX|W1", decision_auth, "new evidence permits readjudication only"))
        self.assertEqual(reopen.event_type, LifecycleType.REOPENS_BLOCKED)
        self.assertEqual(len(owner.authorities), 0)
        with self.assertRaises(SemanticMaintenanceError):
            owner.create_authority(authority_id="A-B", authority_version="1.0.0", decision=blocked)

    def test_newest_is_not_current(self):
        owner, _, candidate, decision_auth, decision, a1 = self._accepted_authority()
        c2 = Candidate("C2", candidate.family, candidate.members, candidate.member_roles, dict(candidate.constitutive_payload), dict(candidate.scope), candidate.family_rule_ref, candidate.evidence_bundle_ref)
        owner.nominate(c2)
        d2 = owner.adjudicate(GovernedDecision("D2", c2.ref, "ACCEPT", decision_auth, "RECERT"))
        a2 = owner.create_authority(authority_id="A2", authority_version="99.0.0", decision=d2, predecessor_authority_ref=a1.ref)
        self.assertIsNone(owner.current_exact("J"))
        owner.select_current(event_id="SEL1", authority_ref=a1.ref, jurisdiction_key="J", decision_authority_ref=decision_auth)
        self.assertEqual(owner.current_exact("J").ref, a1.ref)
        self.assertNotEqual(owner.current_exact("J").ref, a2.ref)

    def test_correction_vs_recertification_identity(self):
        owner, _, candidate, decision_auth, decision, a1 = self._accepted_authority()
        same = Candidate("CS", candidate.family, candidate.members, candidate.member_roles, dict(candidate.constitutive_payload), dict(candidate.scope), candidate.family_rule_ref, candidate.evidence_bundle_ref)
        owner.nominate(same)
        ds = owner.adjudicate(GovernedDecision("DS", same.ref, "ACCEPT", decision_auth, "RECERT"))
        a2 = owner.create_authority(authority_id="A2", authority_version="1.0.0", decision=ds, predecessor_authority_ref=a1.ref)
        self.assertEqual(a1.semantic_claim_id, a2.semantic_claim_id)
        recert = owner.record_lifecycle(LifecycleEvent("L-REC", LifecycleType.RECERTIFIES, a2.ref, a1.ref, "J-ID", decision_auth, "same claim/new authority"))
        self.assertEqual(recert.event_type, LifecycleType.RECERTIFIES)
        reaffirm = owner.record_lifecycle(LifecycleEvent("L-REAFF", LifecycleType.SURVIVES_SAME_ID, a2.ref, a2.ref, "J-ID", decision_auth, "reaffirmation/no authority replacement"))
        self.assertEqual(reaffirm.event_type, LifecycleType.SURVIVES_SAME_ID)
        changed_payload = dict(candidate.constitutive_payload); changed_payload["action_domain"] = "REFUSE"
        changed = Candidate("CC", candidate.family, candidate.members, candidate.member_roles, changed_payload, dict(candidate.scope), candidate.family_rule_ref, candidate.evidence_bundle_ref)
        owner.nominate(changed)
        dc = owner.adjudicate(GovernedDecision("DC", changed.ref, "ACCEPT", decision_auth, "CORRECTION"))
        a3 = owner.create_authority(authority_id="A3", authority_version="1.0.0", decision=dc, predecessor_authority_ref=a2.ref)
        self.assertNotEqual(a2.semantic_claim_id, a3.semantic_claim_id)
        correct = owner.record_lifecycle(LifecycleEvent("L-COR", LifecycleType.CORRECTS, a3.ref, a2.ref, "J-ID", decision_auth, "constitutive change"))
        self.assertEqual(correct.event_type, LifecycleType.CORRECTS)

    def test_rollback_does_not_rewrite_history(self):
        witness = build_authoritative_witness()
        self.assertEqual(witness["current_release_after_rollback"], witness["predecessor_release_ref"])
        self.assertIn("successor_release", witness["exact_replay"])

    def test_governed_split_merge_variant_exclusion_execute(self):
        owner, _, base_candidate, decision_auth = fixture()
        t10_rule = make_ref("SEMANTIC_FAMILY_RULE", "T10_RULE_TEST", {"family": "T10"})
        owner.register_family_rule("T10", t10_rule)
        def mk(cid, aid, members):
            c = Candidate(cid, "T10", tuple(members), tuple((m, "CELL") for m in members), {"target_condition_matrix": {"members": list(members)}}, {"source": "FIX", "wave": "W1"}, t10_rule, base_candidate.evidence_bundle_ref)
            owner.nominate(c)
            d = owner.adjudicate(GovernedDecision("D-"+cid, c.ref, "ACCEPT", decision_auth, "GENEALOGY_FIXTURE"))
            return owner.create_authority(authority_id=aid, authority_version="1.0.0", decision=d)
        parent = mk("P4", "AP", ("A","B","C","D"))
        left = mk("L2", "AL", ("A","B"))
        right = mk("R2", "AR", ("C","D"))
        merged = mk("M4", "AM", ("A","B","C","D"))
        split_d = owner.adjudicate_genealogy(GovernedGenealogyDecision("GD-S", GenealogyType.SPLIT, (parent.ref,), (left.ref,right.ref), decision_auth, "RESOLVED", "EXACT_PARTITION"))
        split_e = owner.append_genealogy(GenealogyEdge("G-S", GenealogyType.SPLIT, (parent.ref,), (left.ref,right.ref), parent.members, (left.members,right.members), split_d.ref))
        self.assertEqual(split_e.edge_type, GenealogyType.SPLIT)
        merge_d = owner.adjudicate_genealogy(GovernedGenealogyDecision("GD-M", GenealogyType.MERGE, (left.ref,right.ref), (merged.ref,), decision_auth, "RESOLVED", "EXACT_UNION"))
        merge_e = owner.append_genealogy(GenealogyEdge("G-M", GenealogyType.MERGE, (left.ref,right.ref), (merged.ref,), tuple(sorted(set(left.members+right.members))), (merged.members,), merge_d.ref))
        self.assertEqual(merge_e.edge_type, GenealogyType.MERGE)
        variant_d = owner.adjudicate_genealogy(GovernedGenealogyDecision("GD-V", GenealogyType.VARIANT, (parent.ref,), (merged.ref,), decision_auth, "RESOLVED", "GOVERNED_VARIANT"))
        variant_e = owner.append_genealogy(GenealogyEdge("G-VP", GenealogyType.VARIANT, (parent.ref,), (merged.ref,), parent.members, (merged.members,), variant_d.ref))
        self.assertEqual(variant_e.edge_type, GenealogyType.VARIANT)
        excl_d = owner.adjudicate_genealogy(GovernedGenealogyDecision("GD-X", GenealogyType.EXCLUSION, (parent.ref,), (), decision_auth, "RESOLVED", "GOVERNED_EXCLUSION"))
        excl_e = owner.append_genealogy(GenealogyEdge("G-X", GenealogyType.EXCLUSION, (parent.ref,), (), parent.members, (), excl_d.ref))
        self.assertEqual(excl_e.edge_type, GenealogyType.EXCLUSION)

    def test_dependency_traversal_does_not_infer_lifecycle(self):
        owner, _, _, _, _, authority = self._accepted_authority()
        owner.bind_descendants(DependencyBinding("DEP-T", authority.ref, (make_ref("I04_ADMISSION", "I04-T", {"a": authority.ref.as_dict()}),)))
        with self.assertRaises(SemanticMaintenanceError):
            owner.revalidate_descendants(receipt_id="RV-T", authority_ref=authority.ref, triggering_event=None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
