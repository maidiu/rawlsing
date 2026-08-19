#!/usr/bin/env python3
"""Metamorphic tests for the D13B replay protocol and hostile fixtures."""
from __future__ import annotations
import unittest
from collections import Counter
from replay_proof_protocol import compare_datasets, evaluate_query, failure_codes, shuffled_physical_copy
from hostile_fixtures import load_fixtures

def fxmap():
    return {f["fixture_id"]:f for f in load_fixtures()}

def unary_marginal(ds, question):
    return Counter(
        (e.get("response_state","SUBSTANTIVE"), str(e.get("value")))
        for e in ds.get("events",[]) if e.get("question_id")==question
    )

class ReplayProofTests(unittest.TestCase):
    def test_all_26_hostile_fixtures(self):
        fixtures=load_fixtures()
        self.assertEqual(26,len(fixtures))
        for i,fx in enumerate(fixtures):
            good=compare_datasets(fx["source"],shuffled_physical_copy(fx["good_replay"],seed=500+i))
            hostile=compare_datasets(fx["source"],fx["hostile_replay"])
            self.assertEqual(fx["expected_good_state"],good["overall_state"],fx["fixture_id"])
            self.assertEqual(fx["expected_hostile_state"],hostile["overall_state"],fx["fixture_id"])
            available=set(failure_codes(hostile))|set(hostile.get("source_blockers",[]))|set(hostile.get("replay_blockers",[]))
            self.assertTrue(set(fx["expected_failure_or_blocked_states"]).issubset(available),fx["fixture_id"])

    def test_same_unary_marginals_do_not_prove_joint_incidence(self):
        f=fxmap()["F24"]
        self.assertEqual(unary_marginal(f["source"],"X"),unary_marginal(f["hostile_replay"],"X"))
        self.assertEqual(unary_marginal(f["source"],"Y"),unary_marginal(f["hostile_replay"],"Y"))
        s=evaluate_query(f["source"],f["source"]["queries"][0])
        h=evaluate_query(f["hostile_replay"],f["hostile_replay"]["queries"][0])
        self.assertNotEqual(s["raw_counts"],h["raw_counts"])

    def test_xor_unary_marginals_can_stay_equal(self):
        f=fxmap()["F11"]
        for q in ("A","B","Y"):
            self.assertEqual(unary_marginal(f["source"],q),unary_marginal(f["hostile_replay"],q))
        s=evaluate_query(f["source"],f["source"]["queries"][1])
        h=evaluate_query(f["hostile_replay"],f["hostile_replay"]["queries"][1])
        self.assertNotEqual(s["raw_counts"],h["raw_counts"])

    def test_branch_count_is_not_branch_membership(self):
        f=fxmap()["F22"]
        self.assertEqual(len(f["source"]["branches"][0]["members"]),len(f["hostile_replay"]["branches"][0]["members"]))
        self.assertNotEqual(f["source"]["branches"][0]["members"],f["hostile_replay"]["branches"][0]["members"])

    def test_raw_equality_does_not_prove_weighted_equality(self):
        f=fxmap()["F16"]
        s=evaluate_query(f["source"],f["source"]["queries"][0])
        h=evaluate_query(f["hostile_replay"],f["hostile_replay"]["queries"][0])
        self.assertEqual(s["raw_counts"],h["raw_counts"])
        self.assertNotEqual(s["weighted_counts"],h["weighted_counts"])

    def test_same_displayed_distribution_not_same_fact(self):
        f=fxmap()["F26"]
        qa=evaluate_query(f["source"],f["source"]["queries"][0])
        qb=evaluate_query(f["source"],f["source"]["queries"][1])
        self.assertEqual(qa["raw_counts"],qb["raw_counts"])
        self.assertNotEqual(qa["condition_ast_hash"],qb["condition_ast_hash"])
        self.assertNotEqual(qa["risk_member_keys"],qb["risk_member_keys"])

if __name__=="__main__":
    unittest.main(verbosity=2)
