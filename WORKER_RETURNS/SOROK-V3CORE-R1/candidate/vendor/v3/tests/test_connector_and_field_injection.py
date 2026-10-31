# v3/tests/test_connector_and_field_injection.py
# v2→v3 connector and Wave 5 field injection.

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.state import BackboneState
from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.field_injection import (
    build_field_raw_from_world_slice,
    build_field_raw_from_driver_vec,
    merge_field_injection,
    get_field_injection,
)


class TestIdentityToBackbone(unittest.TestCase):
    def test_minimal_identity_defaults_to_middle(self) -> None:
        state = backbone_state_from_identity({}, year=1990, age=0)
        self.assertEqual(state.year, 1990)
        self.assertEqual(state.age, 0)
        self.assertGreater(state.capacity.money, 40)
        self.assertLess(state.capacity.money, 70)

    def test_class_origin_working_lowers_money_raises_job_insecurity(self) -> None:
        state = backbone_state_from_identity(
            {"class_origin": "working", "current_class": "working"},
            year=1985,
            age=0,
        )
        self.assertLess(state.capacity.money, 45)
        self.assertGreater(state.reproduction_constraints.job_insecurity, 40)

    def test_elite_raises_money_lowers_job_insecurity(self) -> None:
        state = backbone_state_from_identity(
            {"current_class": "elite"},
            year=1980,
            age=0,
        )
        self.assertGreater(state.capacity.money, 80)
        self.assertLess(state.reproduction_constraints.job_insecurity, 15)

    def test_minority_status_lowers_legitimacy(self) -> None:
        state = backbone_state_from_identity(
            {"minority_status": "minoritized"},
            year=1995,
            age=0,
        )
        self.assertLess(state.capacity.legitimacy, 50)

    def test_religiosity_sets_spiritual(self) -> None:
        state = backbone_state_from_identity(
            {"religiosity_level": 80},
            year=1990,
            age=0,
        )
        self.assertGreater(state.practice_stack.spiritual, 70)

    def test_derive_child_expectation_baseline_when_parent_and_regime_provided(self) -> None:
        identity = {
            "parent_expectation_baseline": {"attachment": "forbidden", "belonging": "hopeful"},
            "transmission_regime": {},
        }
        state = backbone_state_from_identity(identity, year=1995, age=0)
        self.assertIsNotNone(getattr(state, "expectation_baseline", None))
        self.assertIsInstance(state.expectation_baseline, dict)

    def test_child_model_populated_from_parent_baseline_and_regime(self) -> None:
        identity = {
            "parent_expectation_baseline": {"attachment": "forbidden", "safety": "hopeless"},
            "transmission_regime": {"openness": 70, "coercion": 30},
        }
        state = backbone_state_from_identity(identity, year=1995, age=5)
        self.assertIsInstance(getattr(state, "child_model", None), dict)
        cm = state.child_model
        self.assertIn("assumed_rules", cm)
        self.assertIn("taboos", cm)
        self.assertIn("what_counts_as_possible", cm)
        self.assertIsInstance(cm["assumed_rules"], list)
        self.assertGreater(len(cm["assumed_rules"]), 0)
        self.assertIn(cm["what_counts_as_possible"], ("narrow", "medium", "wide"))
        # Forbidden/hopeless axes should produce rules and taboos
        self.assertGreater(len(cm["taboos"]), 0)


class TestFieldInjection(unittest.TestCase):
    def test_world_slice_maps_economy_repression(self) -> None:
        raw = build_field_raw_from_world_slice({
            "gdp_per_capita": 60.0,
            "state_repression": 30.0,
        })
        self.assertEqual(raw.get("economy"), 60.0)
        self.assertEqual(raw.get("repression_baseline"), 30.0)

    def test_driver_vec_maps_legitimacy(self) -> None:
        raw = build_field_raw_from_driver_vec({"trust_vs_distrust": 70.0})
        self.assertEqual(raw.get("legitimacy"), 70.0)

    def test_merge_overrides(self) -> None:
        a = {"economy": 50.0, "morale": 40.0}
        b = {"morale": 60.0}
        m = merge_field_injection(a, b)
        self.assertEqual(m["economy"], 50.0)
        self.assertEqual(m["morale"], 60.0)
        self.assertIn("_integrity", m)
        self.assertEqual(m["_integrity"]["status"], "ok")
        self.assertGreaterEqual(m["_integrity"]["conflict_count"], 1)

    def test_get_field_injection_exposes_integrity(self) -> None:
        out = get_field_injection("XX", 2000, 10)
        self.assertIsInstance(out, dict)
        self.assertIn("_integrity", out)
        self.assertIn(out["_integrity"]["status"], ("ok", "degraded", "failed"))


if __name__ == "__main__":
    unittest.main()
