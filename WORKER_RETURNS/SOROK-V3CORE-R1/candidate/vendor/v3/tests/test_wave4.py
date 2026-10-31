# v3/tests/test_wave4.py
# Wave 4: scoring, delta_templates, persona_sheet (no LLM calls).

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices, compute_all_derived
from v3.engine.scoring import score_event_candidate, score_magnet_candidate, select_candidates
from v3.engine.active_magnets import apply_selected_magnets_to_state
from v3.engine.effects.delta_templates import (
    delta_from_event,
    delta_from_magnet,
    merge_deltas,
    apply_deltas_to_state,
    build_state_deltas_applied_summary,
)
from v3.io.persona_sheet import build_persona_sheet
from v3.tools.distill_memory import distill_persona_sheet_backstory


class TestScoring(unittest.TestCase):
    def test_score_event_returns_0_to_1(self) -> None:
        summary = {"age": 25, "field": {"affordances": {"available_channels": ["family", "peer"]}, "hostage_index": 20}, "capacity": {"vitality": 60, "agency": 50, "coherence": 50}, "wound": {}}
        ev = {"kind": "relationship", "intensity": "minor", "channels": ["family"], "implicated": {}}
        s = score_event_candidate(ev, summary)
        self.assertGreaterEqual(s, 0.0)
        self.assertLessEqual(s, 1.0)

    def test_boundary_fit_discouraged_incentivized(self) -> None:
        base_summary = {"age": 25, "field": {"affordances": {"available_channels": ["family", "peer"]}, "hostage_index": 20}, "capacity": {"vitality": 60, "agency": 50, "coherence": 50}, "wound": {}}
        boundary_map = {
            "autonomy": {"discouraged": ["rebellion", "open defiance"], "permitted": ["compliance"], "incentivized": ["quiet initiative"]},
        }
        summary = {**base_summary, "boundary_map": boundary_map}
        ev_neutral = {"kind": "relationship", "intensity": "minor", "channels": ["family"], "implicated": {}}
        ev_discouraged = {"kind": "relationship", "intensity": "minor", "channels": ["family"], "implicated": {"positions": ["rebellion"]}}
        ev_incentivized = {"kind": "relationship", "intensity": "minor", "channels": ["family"], "implicated": {"positions": ["quiet initiative"]}}
        s_neutral = score_event_candidate(ev_neutral, summary)
        s_discouraged = score_event_candidate(ev_discouraged, summary)
        s_incentivized = score_event_candidate(ev_incentivized, summary)
        self.assertGreater(s_incentivized, s_neutral, "incentivized position should score higher than no position")
        self.assertGreater(s_neutral, s_discouraged, "discouraged position should score lower than no position")
        self.assertLess(s_discouraged, 0.5, "discouraged should be heavily down-weighted")

    def test_select_candidates_respects_limits(self) -> None:
        packet = {
            "year": 2020,
            "age": 20,
            "event_candidates": [
                {"id": "e1", "kind": "relationship", "intensity": "major", "channels": ["peer"]},
                {"id": "e2", "kind": "opportunity", "intensity": "minor", "channels": ["work"]},
                {"id": "e3", "kind": "loss", "intensity": "minor", "channels": ["family"]},
            ],
            "magnet_candidates": [
                {"id": "m1", "magnet_type": "friend", "label": "A friend"},
            ],
            "branch_hypotheses": [],
        }
        summary = {"age": 20, "field": {"affordances": {"available_channels": ["family", "peer", "work"]}, "hostage_index": 15}, "capacity": {"vitality": 60, "agency": 55, "coherence": 50}, "wound": {}}
        events, magnets = select_candidates(packet, summary)
        self.assertLessEqual(len(events), 5)  # ≤2 major + ≤2 minor + ≤1 surprise
        self.assertLessEqual(len(magnets), 2)

    def test_apply_selected_magnets_persists_to_state(self) -> None:
        state = BackboneState(year=2020, age=20)
        self.assertEqual(len(state.active_magnets), 0)
        selected = [
            {"id": "mg_1", "magnet_type": "mentor", "label": "A mentor"},
            {"id": "mg_2", "magnet_type": "friend", "label": "A friend"},
        ]
        apply_selected_magnets_to_state(state, selected, {})
        self.assertEqual(len(state.active_magnets), 2)
        ids = [m.id for m in state.active_magnets]
        self.assertIn("mg_1", ids)
        self.assertIn("mg_2", ids)
        self.assertEqual(state.active_magnets[0].tenure_years, 0)
        # Duplicate id not added
        apply_selected_magnets_to_state(state, [{"id": "mg_1", "magnet_type": "mentor", "label": "Same"}], {})
        self.assertEqual(len(state.active_magnets), 2)


class TestDeltaTemplates(unittest.TestCase):
    def test_delta_from_event_returns_bounded_dict(self) -> None:
        config = {"delta_caps": {"capacity_fields": 20, "domain_A": 10, "alienation": 15, "coherence": 10, "practice_fields": 15}}
        ev = {"kind": "relationship", "intensity": "major", "magnets": {"offers": ["agency"], "costs": []}, "implicated": {}}
        d = delta_from_event(ev, config)
        self.assertIn("capacity_deltas", d)
        self.assertIn("alienation_delta", d)
        for k, v in (d.get("capacity_deltas") or {}).items():
            self.assertLessEqual(abs(v), 20)

    def test_merge_deltas_and_apply(self) -> None:
        state = BackboneState(year=2020, age=25)
        config = {"delta_caps": {"capacity_fields": 20, "domain_A": 10, "domain_S": 10, "domain_V": 10, "alienation": 15, "coherence": 10, "practice_fields": 15}}
        d1 = delta_from_event({"kind": "opportunity", "intensity": "minor", "magnets": {}, "implicated": {}}, config)
        d2 = delta_from_magnet({"magnet_type": "mentor", "label": "Mentor"}, config)
        merged = merge_deltas([d1, d2])
        apply_deltas_to_state(state, merged, config, selected_events=[])
        state.clamp_all()
        self.assertGreaterEqual(state.capacity.skill, 0)
        self.assertLessEqual(state.capacity.skill, 100)

    def test_apply_deltas_with_epistemic_rupture_creates_shard_and_process(self) -> None:
        state = BackboneState(year=2022, age=14)
        config = {"delta_caps": {"capacity_fields": 20, "domain_A": 10, "domain_S": 10, "domain_V": 10, "alienation": 15, "coherence": 10, "practice_fields": 15}}
        merged = {"capacity_deltas": {}, "domain_deltas": {}, "alienation_delta": 0, "coherence_delta": 0, "practice_deltas": {}}
        rupture_ev = {
            "kind": "epistemic_rupture",
            "id": "ev_rupture",
            "label": "Betrayal",
            "intensity": "major",
            "rupture": {"violated_assumption": "Friends don't sell you out", "opacity": "medium", "prediction_error": "high"},
            "implicated": {"domains": ["sect_class"]},
        }
        apply_deltas_to_state(state, merged, config, selected_events=[rupture_ev])
        self.assertEqual(len(state.rupture_shards), 1)
        self.assertEqual(len(state.metabolization_processes), 1)
        self.assertGreater(state.plasticity_window.get("years_left", 0), 0)

    def test_apply_deltas_with_expectation_fulfillment_creates_gift_shard(self) -> None:
        from v3.core.state import StrivingObject
        state = BackboneState(year=2023, age=15)
        state.striving_objects.append(
            StrivingObject(id="so_belong", label="Peer cluster", need_axis="belonging", started_age=14, investment=60, identity_load=50, active=True)
        )
        config = {"delta_caps": {"capacity_fields": 20, "domain_A": 10, "domain_S": 10, "domain_V": 10, "alienation": 15, "coherence": 10, "practice_fields": 15}}
        merged = {"capacity_deltas": {}, "domain_deltas": {}, "alienation_delta": 0, "coherence_delta": 0, "practice_deltas": {}}
        fulfillment_ev = {
            "kind": "relationship",
            "id": "ev_chosen",
            "label": "Chosen by a friend",
            "expectation_type": "fulfillment",
            "striving_object_id": "so_belong",
        }
        apply_deltas_to_state(state, merged, config, selected_events=[fulfillment_ev])
        self.assertEqual(len(state.gift_shards), 1)
        self.assertEqual(state.gift_shards[0].striving_object_id, "so_belong")
        self.assertEqual(state.gift_shards[0].need_axis, "belonging")

    def test_apply_deltas_with_violation_high_identity_load_sets_malheur_risk(self) -> None:
        from v3.core.state import StrivingObject
        state = BackboneState(year=2024, age=16)
        state.striving_objects.append(
            StrivingObject(id="so_status", label="High achiever", need_axis="status", started_age=14, investment=70, identity_load=65, active=True)
        )
        config = {"delta_caps": {"capacity_fields": 20, "domain_A": 10, "domain_S": 10, "domain_V": 10, "alienation": 15, "coherence": 10, "practice_fields": 15}}
        merged = {"capacity_deltas": {}, "domain_deltas": {}, "alienation_delta": 0, "coherence_delta": 0, "practice_deltas": {}}
        violation_ev = {
            "kind": "humiliation",
            "id": "ev_public_fail",
            "label": "Public failure at competition",
            "expectation_type": "violation",
            "striving_object_id": "so_status",
        }
        apply_deltas_to_state(state, merged, config, selected_events=[violation_ev])
        self.assertEqual(len(state.disruption_shards), 1)
        self.assertTrue(state.disruption_shards[0].malheur_risk)
        self.assertEqual(state.disruption_shards[0].opacity, "high")
        self.assertEqual(state.disruption_shards[0].prediction_error, "high")

    def test_get_suggested_event_targets_returns_targets_for_active_strivings(self) -> None:
        from v3.engine.expectation_events import get_suggested_event_targets_for_summary
        summary = {
            "year": 2024,
            "age": 14,
            "striving_objects": [
                {"id": "so_bel", "need_axis": "belonging", "label": "Peer cluster"},
                {"id": "so_meaning", "need_axis": "meaning", "label": "Interpretive key"},
            ],
        }
        suggested = get_suggested_event_targets_for_summary(summary)
        self.assertIsInstance(suggested, list)
        axes = {s["need_axis"] for s in suggested}
        self.assertIn("belonging", axes)
        self.assertIn("meaning", axes)
        for s in suggested:
            self.assertIn(s["expectation_type"], ("fulfillment", "violation"))
            self.assertIsInstance(s.get("striving_object_ids"), list)


class TestPersonaSheet(unittest.TestCase):
    def test_build_persona_sheet_has_v2_surface(self) -> None:
        state = BackboneState(year=2026, age=43)
        state.rendered_output = {"narrative_snapshot": {"scene": "A year passed."}, "dialogue_snippets": [], "consistency_check": {}}
        derived = compute_all_derived(state)
        sheet = build_persona_sheet(state, derived, identity_override={"country": "US", "given_name": "Test"})
        self.assertIn("identity", sheet)
        self.assertEqual(sheet["identity"]["age"], 43)
        self.assertIn("current_state", sheet)
        self.assertIn("needs", sheet["current_state"])
        self.assertIn("strategies", sheet["current_state"])
        self.assertIn("indices", sheet["current_state"])
        self.assertIn("bands", sheet)
        self.assertIn("backstory", sheet)
        self.assertIn("A year passed.", sheet["backstory"])
        self.assertIn("expectation_baseline", sheet)
        self.assertIn("active_strivings", sheet)
        self.assertIn("rupture_status", sheet)
        self.assertIn("recent_gifts", sheet)
        self.assertIn("recent_disruptions", sheet)
        self.assertIsInstance(sheet["recent_gifts"], list)
        self.assertIsInstance(sheet["recent_disruptions"], list)
        self.assertIn("voice_profile_provenance", sheet["metadata"])
        self.assertIn("language_integrity", sheet["metadata"])

    def test_build_persona_sheet_flags_invalid_language_labels(self) -> None:
        state = BackboneState(year=2026, age=29)
        state.rendered_output = {"narrative_snapshot": {"scene": "A year passed."}, "dialogue_snippets": [], "consistency_check": {}}
        derived = compute_all_derived(state)
        sheet = build_persona_sheet(
            state,
            derived,
            identity_override={
                "country": "US",
                "given_name": "Test",
                "languages": ["English", "or mute"],
            },
        )
        self.assertEqual(sheet["metadata"]["language_integrity"]["status"], "invalid_labels_found")
        self.assertIn("fallback_generated", sheet["metadata"]["voice_profile_provenance"]["speech_tics"])

    def test_distillation_manifest_written_for_preprocessed_fallback(self) -> None:
        sheet = {
            "identity": {"given_name": "Test", "family_name": "Person", "age": 29, "country": "US"},
            "backstory": "Age 1:\nsmall memory\n\nAge 2:\nsmall memory again",
        }
        result = distill_persona_sheet_backstory(sheet, openai_key="test", model="gpt-4o", dry_run=False)
        self.assertIn("distillation_manifest", result)
        self.assertEqual(result["distillation_manifest"]["status"], "preprocessed_fallback")
        self.assertGreater(result["distillation_manifest"]["input_chars"], 0)

    def test_persona_sheet_with_backbone_includes_raw_state(self) -> None:
        state = BackboneState(year=2026, age=30)
        derived = compute_all_derived(state)
        sheet = build_persona_sheet(state, derived, include_backbone=True)
        self.assertIn("backbone", sheet)
        self.assertIn("rendered_output", sheet)


if __name__ == "__main__":
    unittest.main()
