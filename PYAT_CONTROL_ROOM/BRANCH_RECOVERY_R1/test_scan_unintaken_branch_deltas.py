#!/usr/bin/env python3
"""Sourcefree negative/positive tests for Pyat no-stranding change detection."""
import importlib.util
from pathlib import Path
import unittest

DIR = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("branch_delta", DIR / "scan_unintaken_branch_deltas.py")
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)

A = "a" * 40
B = "b" * 40
C = "c" * 40

class PyatDeltaTests(unittest.TestCase):
    def test_all_2831_baseline_heads_accounted_no_claim_of_review(self):
        old, counts = MOD.baseline()
        self.assertEqual(len(old), 2831)
        self.assertEqual(counts["PYAT_DIRECT"], 840)
        self.assertEqual(counts["PRE_PYAT_FOUNDATION_OR_SHARED"], 1110)
        self.assertEqual(counts["SHARED_BOUNDARY_REFERENCE_ONLY"], 5)
        self.assertEqual(counts["UNCLASSIFIED_SCREEN_NOT_CLOSED"], 587)
        self.assertEqual(counts["SOROK_OUTSIDE_MISSION"], 289)

    def test_new_pyat_branch_without_custody_is_flagged(self):
        flagged, stats = MOD.scan({}, {"agent/pyat-new-work": A}, {"entries": []})
        self.assertEqual(len(flagged), 1)
        self.assertEqual(flagged[0]["kind"], "NEW_REF")

    def test_existing_head_move_without_updated_custody_is_flagged(self):
        name = "agent/vozhd-dva-w3-adp-004-v556-interaction"
        flagged, stats = MOD.scan({name: A}, {name: B}, {"entries": [{"branch": name, "observed_head_sha": A}]})
        self.assertEqual(flagged[0]["kind"], "MOVED_HEAD")

    def test_exact_new_head_intaken_is_not_flagged(self):
        name = "agent/pyat-reviewed-return"
        flagged, stats = MOD.scan({name: A}, {name: B}, {"entries": [{"branch": name, "observed_head_sha": B}]})
        self.assertEqual(flagged, [])
        self.assertEqual(stats["REGISTERED_AT_THIS_SHA"], 1)

    def test_sorok_only_is_not_mistaken_for_pyat(self):
        flagged, stats = MOD.scan({}, {"agent/sorok-actor-work": B}, {"entries": []})
        self.assertEqual(flagged, [])
        self.assertEqual(stats["SOROK_SEPARATE_NO_PYAT_INTAKE"], 1)

    def test_pyat_sorok_shared_boundary_still_flagged(self):
        flagged, stats = MOD.scan({}, {"agent/reviewer-pyat-sorok-bridge": B}, {"entries": []})
        self.assertEqual(flagged[0]["cohort"], "SHARED_BOUNDARY_REFERENCE_ONLY")

    def test_unknown_old_branch_is_not_silently_dropped(self):
        flagged, stats = MOD.scan({"unclassified-legacy": A}, {"unclassified-legacy": B}, {"entries": []})
        self.assertEqual(flagged[0]["cohort"], "UNCLASSIFIED_SCREEN_NOT_CLOSED")

    def test_unchanged_branches_do_not_reopen(self):
        flagged, stats = MOD.scan({"agent/pyat-old": A}, {"agent/pyat-old": A}, {"entries": []})
        self.assertEqual(flagged, [])
        self.assertEqual(stats["UNCHANGED"], 1)

    def test_invalid_duplicate_current_census_fails_closed(self):
        with self.assertRaises(ValueError):
            MOD.normalize([{"name":"x","sha":A},{"name":"x","sha":B}])

if __name__ == "__main__":
    unittest.main()
