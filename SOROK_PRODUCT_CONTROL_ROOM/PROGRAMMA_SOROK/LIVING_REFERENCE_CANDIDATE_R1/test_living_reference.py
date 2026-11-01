"""Tests for the Sorok-only living reference and orchestration map."""
from __future__ import annotations

import copy
import json
import shutil
import tempfile
import unittest
from pathlib import Path

import living_reference as lr
import verify_source_manifest as vsm


class LivingReferenceTests(unittest.TestCase):
    def test_refresh_and_read_commands_share_state(self):
        state = lr.build_state()
        self.assertEqual(len(state["nodes"]), lr.BASE_NODE_COUNT)
        self.assertEqual(len(state["edges"]), lr.BASE_EDGE_COUNT)
        self.assertEqual(state["source_count"], 144)
        self.assertGreaterEqual(len(state["pyat_boundary"]), 9)
        self.assertEqual(state["pyat_boundary"]["id"], "PYAT_EXTERNAL_BOUNDARY")
        self.assertTrue(all(not n["id"].startswith("PYAT_") for n in state["nodes"] if n["id"] != "PYAT_EXTERNAL_BOUNDARY"))
        nodes, edges = lr._neighbors(state, "S5", 2)
        self.assertTrue(any(n["id"] == "L0_S5_FLOURISHING_AGENCY" for n in nodes))
        self.assertTrue(any(e["from"] == "L1_S5_FLOURISHING" and e["to"] == "S5" for e in edges))
        self.assertIsNotNone(lr._critical_path(state, "L0_PERSON"))

    def test_material_b_path_is_visible_but_not_native(self):
        state = lr.build_state()
        self.assertIn("B-F1CR-R2", {n["id"] for n in state["nodes"]})
        report = lr._neighbors(state, "B-F1CR-R2", 2)
        ids = {n["id"] for n in report[0]}
        self.assertTrue({"B-F1CR-R2", "L4_NAMED_FIRST_CONSUMER"} & ids)
        axes = state["axes"]["B-F1CR-R2"]
        self.assertEqual(axes["human"], "NOT_PROVEN")
        self.assertEqual(axes["authority"], "UNADOPTED")
        self.assertNotEqual(axes["consumer"], "ACTUAL")

    def test_v3_mechanism_is_source_linked_not_adopted(self):
        state = lr.build_state()
        source = next(x for x in state["source_manifest"]["rows"] if x["id"] == "M25")
        self.assertEqual(source["namespace"], "SOROK")
        self.assertEqual(source["source_owner"], "ORIGINAL_V3_SOURCE_OWNER")
        self.assertIn("M25", {n["id"] for n in state["nodes"]})
        self.assertEqual(state["axes"]["M25"]["science"], "MECHANISM_NOT_ISSUED")

    def test_six_product_paths_and_falsifiers_are_specific(self):
        state = lr.build_state()
        for sid in ("S5", "S7", "S11", "S13", "S14", "S15"):
            node_ids = {n["id"] for n in state["nodes"]}
            self.assertIn(sid, node_ids)
            row = lr._load(lr.SEED_REGISTRY)["rows"]
            source = next(x for x in row if x["id"] == sid)
            link = source["product_link"]
            self.assertEqual(link["l2"], sid)
            for key in ("l0", "l1", "l3", "l4", "l5"):
                self.assertIn(link[key], node_ids)
            self.assertTrue(any(g["domain"] == sid for g in state["gaps"]))
            self.assertTrue(source["alternatives"])

    def test_arbitrary_source_has_terminal_or_explicit_gap(self):
        state = lr.build_state()
        for sid in ("E01", "M01", "S16", "CP-A5-R2", "R6"):
            self.assertIn(sid, {n["id"] for n in state["nodes"]})
            source = next((x for x in state["source_manifest"]["rows"] if x["id"] == sid), None)
            if source is not None:
                self.assertTrue(source["path"])
            else:
                self.assertIn(sid, {"R6", "R7"})
        self.assertTrue(lr._critical_path(state, "L0_MATERIAL"))

    def test_positive_candidate_transition_does_not_mass_invalidate(self):
        state = lr.build_state()
        before = copy.deepcopy(state["axes"]["B-F1CR-R2"])
        result = lr._apply_transition(state, {"node_id": "B-F1CR-R2", "dimension": "engineering", "to": "CANDIDATE_UPGRADED", "evidence": {"kind": "SYNTHETIC_DEMO", "note": "sourcefree candidate only"}})
        self.assertEqual(state["axes"]["B-F1CR-R2"]["engineering"], "CANDIDATE_UPGRADED")
        self.assertEqual(state["axes"]["B-F1CR-R2"]["human"], before["human"])
        self.assertEqual(state["axes"]["B-F1CR-R2"]["authority"], before["authority"])
        self.assertEqual(result["invalidated"], [])
        self.assertEqual(state["pyat_boundary"]["status"], "EXTERNAL_OWNER_HELD")

    def test_transition_without_owner_or_reviewer_is_refused(self):
        state = lr.build_state()
        with self.assertRaises(ValueError):
            lr._apply_transition(state, {"node_id": "CP-A5-R2", "dimension": "engineering", "to": "ACCEPTED", "owner_evidence": "", "reviewer_evidence": "r"})
        with self.assertRaises(ValueError):
            lr._apply_transition(state, {"node_id": "CP-A5-R2", "dimension": "human", "to": "A5_GREEN", "owner_evidence": "o", "reviewer_evidence": ""})

    def test_returned_code_pass_does_not_make_human_a5_green(self):
        state = lr.build_state()
        lr._apply_transition(state, {"node_id": "CP-A5-R2", "dimension": "engineering", "to": "CANDIDATE_UPGRADED", "evidence": {"kind": "SYNTHETIC_DEMO", "note": "author-test candidate only"}})
        self.assertNotEqual(state["axes"]["CP-A5-R2"]["human"], "PROVEN")
        self.assertNotEqual(state["axes"]["A5"]["human"], "PROVEN")
        self.assertEqual(state["axes"]["A5"]["authority"], "NOT_ADOPTED")
        result = lr._apply_transition(state, {"node_id": "A5", "dimension": "human", "to": "PROVEN", "evidence": {"kind": "HUMAN_PARTICIPANT", "participant_record_hash": "a" * 64, "consent_record": "c", "protocol": "p", "reviewer_role": "NOT_INDEPENDENT"}})
        self.assertNotEqual(state["axes"]["A5"]["human"], "PROVEN")
        self.assertIn(result["status"], {"SIMULATED_NOT_ADOPTED", "PENDING_MANUAL_VERIFICATION"})

    def test_source_withdrawal_invalidates_sorok_downstream_not_pyat_boundary(self):
        state = lr.build_state()
        unaffected = state["axes"]["M01"]["consumer"]
        lr._apply_transition(state, {"node_id": "B-F1CR-R2", "dimension": "source_recovery", "to": "SOURCE_NOT_FOUND", "evidence": {"kind": "SYNTHETIC_DEMO", "note": "source withdrawal simulation"}})
        self.assertEqual(state["axes"]["M01"]["consumer"], unaffected)
        self.assertEqual(state["pyat_boundary"]["status"], "EXTERNAL_OWNER_HELD")
        self.assertTrue(state["history"][-1]["invalidated"])

    def test_synthetic_intake_is_quarantined_and_cannot_create_operating_gap(self):
        state = lr.build_state()
        old_history = len(state["history"])
        item = lr.intake_candidate(state, {"id": "NEW-RETURN", "branch": "x", "sha": "a" * 40, "new_requirement": "NEW_REQUISITE", "tests": {"passed": 1}})
        self.assertEqual(item["status"], "QUARANTINED_SYNTHETIC_OR_UNVERIFIABLE")
        self.assertFalse(any(g["node"] == "NEW_REQUISITE" for g in state["gaps"]))
        self.assertEqual(len(state["history"]), old_history)
        self.assertEqual(state["history"][0]["history_id"], "H0001")
        self.assertTrue(state["quarantined_intake"])

    def test_snapshot_death_restore_and_forged_source_failure(self):
        state = lr.build_state()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "state.json").write_text(json.dumps(state), encoding="utf-8")
            backup = root / "backup.json"; shutil.copy2(root / "state.json", backup)
            (root / "state.json").unlink()
            self.assertFalse((root / "state.json").exists())
            shutil.copy2(backup, root / "state.json")
            self.assertEqual(json.loads((root / "state.json").read_text())["state_digest"], state["state_digest"])
            manifest = json.loads((root / "source_manifest.json").read_text()) if (root / "source_manifest.json").exists() else json.loads(lr.SOURCE_MANIFEST.read_text())
            manifest["rows"][0]["object_id"] = "f" * 40
            (root / "source_manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
            report = vsm.verify(root, lr.ROOT.parents[2])
            self.assertEqual(report["result"], "FAIL")


if __name__ == "__main__":
    unittest.main()
