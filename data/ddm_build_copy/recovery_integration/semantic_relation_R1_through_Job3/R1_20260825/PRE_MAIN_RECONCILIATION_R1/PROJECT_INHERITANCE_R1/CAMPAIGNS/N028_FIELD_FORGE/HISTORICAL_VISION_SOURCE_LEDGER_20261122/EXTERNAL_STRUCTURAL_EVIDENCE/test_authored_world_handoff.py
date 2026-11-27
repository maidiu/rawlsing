"""Actual native reads + exact R36 gate body, with narrow dependency fixtures.

FF_R36_MODULE points at the unmodified incumbent material_conjunction.py.
The test does NOT run ConstitutiveRuntime, its ledger, or the full SOROK package.
"""
import copy
import hashlib
import importlib.util
import os
from pathlib import Path
import sys
import types
import unittest

from native_priority_readers import NativePack
from authored_world_handoff import select_world_evidence, prepare_authored_history, verify_handoff

R36_BLOB = "b03a35e3efc04473d64a0b6f8d301b8cac5b8646"


def load_incumbent():
    path = Path(os.environ["FF_R36_MODULE"])
    data = path.read_bytes()
    if hashlib.sha1(f"blob {len(data)}\0".encode() + data).hexdigest() != R36_BLOB:
        raise ValueError("not exact R36 gate blob")
    package = types.ModuleType("r36_gate_fixture")
    package.__path__ = []
    deps = types.ModuleType("r36_gate_fixture.types")
    deps.GRADE, deps.copy = "SOURCEFREE_RESEARCH_PROVISIONAL", copy.deepcopy
    organism = types.ModuleType("r36_gate_fixture.organism")
    organism.ACTIONS = {"EAT": {}}
    for module in (package, deps, organism):
        sys.modules[module.__name__] = module
    spec = importlib.util.spec_from_file_location("r36_gate_fixture.material_conjunction", path)
    gate = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(gate)
    return gate


class HandoffTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pack = NativePack(os.environ["FF_PRIORITY_PACK"])
        cls.gate = load_incumbent()
        cls.evidence = select_world_evidence(cls.pack, [
            {"source": "FINDEX", "keys": {"codewb": "IND", "year": 2021,
                "group": "all", "group2": "all"}, "reference_year": None},
            {"source": "JOIN", "keys": {"Country Code": "IND", "Year of survey": 2019,
                "Subsample": "All"}, "reference_year": None},
        ])

    def packet(self, value="admitted", extra=False):
        pos = [] if value is None else [{"id": "p1", "actor": "mother", "field": "ration_access",
            "value": value, "effective_from": 1, "effective_until": 1}]
        if extra:
            pos.append(dict(pos[0], id="p2", value="excluded"))
        return prepare_authored_history(self.evidence, scenario_id="fictional-ration-test",
            rationale="Explore material access independently of published resource margins; no actual ration policy inferred.",
            positions=pos, rules=[{"id": "r1", "operation": "EAT", "location": "home",
                "effective_from": 1, "effective_until": 1,
                "all_of": [{"kind": "RECORDED_POSITION", "field": "ration_access", "equals": "admitted"}]}])

    def evaluate(self, packet):
        world = {"clock": 1, "sites": {"home": {}}, "positioned_material_records": [],
                 "institutional_access_rules": []}
        self.gate.admit_authored_structural_history(world, {"mother"}, packet["authored_structural_history"])
        return world, self.gate.evaluate_material_conjunction(world, "mother", "home", "EAT")

    def test_actual_native_values_and_separate_years(self):
        a, b = self.evidence["observations"]
        self.assertAlmostEqual(a["rows"][0]["values"]["save_any_t_d"], .235477, places=5)
        self.assertEqual(a["keys"]["year"], 2021)
        self.assertEqual(b["keys"]["Year of survey"], 2019)
        self.assertEqual(set(self.pack.cache), {"FINDEX", "JOIN"})

    def test_same_evidence_different_rule_outcome(self):
        a, b = self.packet(), self.packet("excluded")
        self.assertEqual(a["evidence"], b["evidence"])
        wa, x = self.evaluate(a)
        wb, y = self.evaluate(b)
        self.assertEqual((x["decision"], y["decision"]), ("PERMITTED_BY_ALL_RULES", "BLOCKED"))
        self.assertFalse(wa["structural_history_origin"]["native_structural_authority"])
        self.assertFalse(wb["structural_history_origin"]["native_structural_authority"])
        self.assertEqual(x["readset"], [a["authored_structural_history"]["source_ref"]])
        self.assertTrue(verify_handoff(a))

    def test_unknown_conflict_expiry(self):
        for packet in (self.packet(None), self.packet(extra=True)):
            world, result = self.evaluate(packet)
            self.assertEqual(result["decision"], "UNRESOLVED")
            world["clock"] = 2
            self.assertEqual(self.gate.evaluate_material_conjunction(world, "mother", "home", "EAT")["decision"], "NO_ADDITIONAL_RULE")

    def test_changed_evidence_not_automatic_rule_change(self):
        a = self.packet()
        other = select_world_evidence(self.pack, [{"source": "FINDEX", "keys": {"codewb": "LBN", "year": 2021,
            "group": "all", "group2": "all"}, "reference_year": None}])
        b = prepare_authored_history(other, **a["fictional_choice"])
        self.assertNotEqual(a["content_hash"], b["content_hash"])
        self.assertEqual(self.evaluate(a)[1]["decision"], self.evaluate(b)[1]["decision"])
        self.assertEqual(a["fictional_choice"], b["fictional_choice"])

    def test_tamper_and_no_native_rule_authority(self):
        p = self.packet()
        p["authored_structural_history"]["positions"][0]["value"] = "excluded"
        self.assertFalse(verify_handoff(p))
        p = self.packet()
        choices = p["fictional_choice"]
        choices["rules"][0]["source_ref"] = "native"
        with self.assertRaises(ValueError): prepare_authored_history(self.evidence, **choices)

    def test_incumbent_rejects_unknown_actor_before_mutation(self):
        p = self.packet()
        world = {"clock": 1, "sites": {"home": {}}, "positioned_material_records": [],
                 "institutional_access_rules": []}
        before = copy.deepcopy(world)
        with self.assertRaisesRegex(ValueError, "STRUCTURAL_HISTORY_INVALID_POSITION"):
            self.gate.admit_authored_structural_history(world, {"other"}, p["authored_structural_history"])
        self.assertEqual(world, before)


if __name__ == "__main__":
    unittest.main()
