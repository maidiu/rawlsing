# v3/tests/test_metabolization_effects.py
# Trace 7: rupture templates, create_rupture_shard_from_event, is_malheur, compute_metabolization_delta.

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.state import BackboneState, NarrationSupport
from v3.engine.effects.metabolization_effects import (
    create_rupture_shard_from_event,
    is_malheur,
    load_rupture_templates,
    get_template_for_age,
    compute_metabolization_delta,
)


class TestMetabolizationEffects(unittest.TestCase):
    def test_load_rupture_templates_returns_list(self) -> None:
        templates = load_rupture_templates()
        self.assertIsInstance(templates, list)
        if templates:
            t = templates[0]
            self.assertIn("id", t)
            self.assertIn("cluster_candidates", t)
            self.assertIn("mode_priors", t)
            self.assertIn("severity_prior", t)

    def test_get_template_for_age(self) -> None:
        templates = load_rupture_templates()
        if not templates:
            self.skipTest("no rupture_templates.yaml or yaml missing")
        t = get_template_for_age(templates, 14)
        self.assertIsNotNone(t)
        self.assertIn("severity_prior", t)

    def test_is_malheur_severity(self) -> None:
        self.assertTrue(is_malheur("malheur"))
        self.assertFalse(is_malheur("major"))
        self.assertFalse(is_malheur("micro"))

    def test_is_malheur_major_plus_conditions(self) -> None:
        self.assertTrue(
            is_malheur("major", status_shock=True, isolation_spike=True, narration_availability=30)
        )
        self.assertFalse(
            is_malheur("major", status_shock=True, isolation_spike=True, narration_availability=50)
        )

    def test_create_rupture_shard_from_event(self) -> None:
        state = BackboneState(year=2022, age=14)
        ev = {
            "kind": "epistemic_rupture",
            "id": "ev_1",
            "label": "Friend betrays in public",
            "intensity": "major",
            "rupture": {
                "opacity": "high",
                "prediction_error": "high",
                "violated_assumption": "Friends don't sell you out",
            },
            "implicated": {"domains": ["sect_class"], "strata_levels": [6, 7]},
        }
        shard = create_rupture_shard_from_event(state, ev)
        self.assertEqual(shard.year, 2022)
        self.assertEqual(shard.age, 14)
        self.assertEqual(shard.violated_assumption, "Friends don't sell you out")
        self.assertEqual(shard.domain, "sect_class")
        self.assertEqual(shard.opacity, "high")
        self.assertEqual(len(state.rupture_shards), 1)
        self.assertEqual(len(state.metabolization_processes), 1)
        self.assertGreater(state.plasticity_window.get("years_left", 0), 0)

    def test_compute_metabolization_delta_returns_tuples(self) -> None:
        cap_delta, bias_delta = compute_metabolization_delta(
            "meaning_rebinding",
            "accommodation",
            "major",
            NarrationSupport(availability=60, accuracy=50, warmth=50, coercion=20),
            is_malheur_flag=False,
        )
        self.assertIsInstance(cap_delta, dict)
        self.assertIsInstance(bias_delta, dict)


if __name__ == "__main__":
    unittest.main()
