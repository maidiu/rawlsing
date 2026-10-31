# v3/tests/test_llm_contract.py
# Wave 4: sanity tests for llm_contract (parse CandidatePacket, RenderOutput, state_summary) and prompts.

from __future__ import annotations

import sys
import unittest
from pathlib import Path

_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices, compute_all_derived
from v3.engine.llm_contract import (
    parse_candidate_packet,
    parse_candidate_packet_with_fallback,
    parse_render_output,
    state_summary_from_backbone,
    build_render_packet,
    make_fallback_event,
    fallback_candidate_packet_if_empty,
    EVENT_CANDIDATES_MAX,
    MAGNET_CANDIDATES_MAX,
    BRANCH_HYPOTHESES_MAX,
)
from v3.engine.prompts import build_pass1_prompt, build_pass2_prompt
from v3.engine.validators import validate_render_output


class TestLLMContract(unittest.TestCase):
    def test_parse_candidate_packet_truncates_to_caps(self) -> None:
        raw = {
            "year": 2011,
            "age": 11,
            "event_candidates": [{"id": f"ev_{i}", "kind": "relationship", "label": f"Event {i}", "intensity": "minor"} for i in range(10)],
            "magnet_candidates": [{"id": f"mg_{i}", "magnet_type": "friend", "label": f"Magnet {i}"} for i in range(6)],
            "branch_hypotheses": [{"id": f"br_{i}", "fork": f"Fork {i}"} for i in range(5)],
        }
        out = parse_candidate_packet(raw)
        self.assertEqual(out["year"], 2011)
        self.assertEqual(out["age"], 11)
        self.assertLessEqual(len(out["event_candidates"]), EVENT_CANDIDATES_MAX)
        self.assertLessEqual(len(out["magnet_candidates"]), MAGNET_CANDIDATES_MAX)
        self.assertLessEqual(len(out["branch_hypotheses"]), BRANCH_HYPOTHESES_MAX)

    def test_parse_candidate_packet_from_string(self) -> None:
        s = '{"year": 2020, "age": 20, "event_candidates": [], "magnet_candidates": [], "branch_hypotheses": []}'
        out = parse_candidate_packet(s)
        self.assertEqual(out["year"], 2020)
        self.assertEqual(out["age"], 20)

    def test_fallback_candidate_packet_if_empty_applies_when_both_empty(self) -> None:
        packet = parse_candidate_packet('{"year": 2021, "age": 15, "event_candidates": [], "magnet_candidates": [], "branch_hypotheses": []}')
        self.assertEqual(len(packet["event_candidates"]), 0)
        applied = fallback_candidate_packet_if_empty(packet)
        self.assertTrue(applied)
        self.assertEqual(len(packet["event_candidates"]), 1)
        self.assertIn("_integrity", packet)
        self.assertEqual(packet["_integrity"]["status"], "degraded")
        ev = packet["event_candidates"][0]
        self.assertEqual(ev["kind"], "practice")
        self.assertEqual(ev["intensity"], "minor")
        self.assertIn("fallback_ev_", ev["id"])

    def test_fallback_candidate_packet_if_empty_no_op_when_has_events(self) -> None:
        packet = parse_candidate_packet('{"year": 2022, "age": 18, "event_candidates": [{"id": "e1", "kind": "relationship", "label": "X", "intensity": "minor"}], "magnet_candidates": [], "branch_hypotheses": []}')
        applied = fallback_candidate_packet_if_empty(packet)
        self.assertFalse(applied)
        self.assertEqual(len(packet["event_candidates"]), 1)
        self.assertEqual(packet["event_candidates"][0]["id"], "e1")

    def test_parse_candidate_packet_with_fallback_applies_when_empty(self) -> None:
        packet = parse_candidate_packet_with_fallback(
            '{"year": 2023, "age": 19, "event_candidates": [], "magnet_candidates": [], "branch_hypotheses": []}'
        )
        self.assertEqual(packet["year"], 2023)
        self.assertEqual(len(packet["event_candidates"]), 1)
        self.assertIn("_integrity", packet)
        self.assertEqual(packet["_integrity"]["status"], "degraded")
        self.assertEqual(packet["event_candidates"][0]["kind"], "practice")

    def test_parse_candidate_packet_invalid_json_raises(self) -> None:
        with self.assertRaises(ValueError):
            parse_candidate_packet("not json {")

    def test_parse_candidate_packet_epistemic_rupture_keeps_rupture_block(self) -> None:
        raw = {
            "year": 2022,
            "age": 14,
            "event_candidates": [
                {
                    "id": "ev_rupture_1",
                    "kind": "epistemic_rupture",
                    "label": "Friend betrays in public",
                    "intensity": "major",
                    "rupture": {
                        "opacity": "high",
                        "prediction_error": "high",
                        "violated_assumption": "Friends don't sell you out",
                        "why_incomprehensible_now": "He looked at me and lied.",
                        "who_explains_it_later": "Nobody",
                        "resolution_horizon": "years",
                    },
                    "implicated": {"domains": ["sect_class"], "strata_levels": [6, 7]},
                },
            ],
            "magnet_candidates": [],
            "branch_hypotheses": [],
        }
        out = parse_candidate_packet(raw)
        self.assertEqual(len(out["event_candidates"]), 1)
        ev = out["event_candidates"][0]
        self.assertEqual(ev["kind"], "epistemic_rupture")
        self.assertIn("rupture", ev)
        self.assertEqual(ev["rupture"]["opacity"], "high")
        self.assertEqual(ev["rupture"]["violated_assumption"], "Friends don't sell you out")
        self.assertEqual(ev["rupture"]["resolution_horizon"], "years")
        self.assertEqual(ev["implicated"]["domains"], ["sect_class"])

    def test_parse_render_output_valid(self) -> None:
        raw = {
            "narrative_snapshot": {
                "scene": "A short scene.",
                "which_strata_fired": [6, 7],
                "which_frameworks_fired": ["family_honor"],
                "what_was_buffered": [],
                "what_scratched": [],
            },
            "dialogue_snippets": [{"speaker": "self", "line": "I said something."}],
            "consistency_check": {"did_not_resolve": True, "public_vs_private_register_obeyed": True, "latent_vs_expressed_aim_obeyed": True},
        }
        out = parse_render_output(raw)
        self.assertIn("narrative_snapshot", out)
        self.assertEqual(out["narrative_snapshot"]["scene"], "A short scene.")
        self.assertEqual(out["dialogue_snippets"][0]["speaker"], "self")
        self.assertTrue(out["consistency_check"]["did_not_resolve"])

    def test_parse_render_output_from_string(self) -> None:
        s = '{"narrative_snapshot": {"scene": "x", "which_strata_fired": [], "which_frameworks_fired": [], "what_was_buffered": [], "what_scratched": []}, "dialogue_snippets": [], "consistency_check": {}}'
        out = parse_render_output(s)
        self.assertEqual(out["narrative_snapshot"]["scene"], "x")

    def test_parse_render_output_empty_scene_gets_fallback(self) -> None:
        raw = {"narrative_snapshot": {"scene": "", "which_strata_fired": []}, "dialogue_snippets": [], "consistency_check": {}}
        out = parse_render_output(raw)
        self.assertIn(out["narrative_snapshot"]["scene"], ("[This year had no recorded scene.]",))
        self.assertIn("_integrity", out)
        self.assertEqual(out["_integrity"]["status"], "degraded")

    def test_state_summary_from_backbone(self) -> None:
        state = BackboneState(year=2011, age=11)
        derived = compute_all_derived(state)
        summary = state_summary_from_backbone(state, derived)
        self.assertEqual(summary["year"], 2011)
        self.assertEqual(summary["age"], 11)
        self.assertIn("identity", summary)
        self.assertIn("field", summary)
        self.assertIn("hostage_index", summary["field"])
        self.assertIn("capacity", summary)
        self.assertIn("vitality", summary["capacity"])
        self.assertIn("frameworks_active", summary)
        self.assertIn("active_cracks", summary)
        # last_year_notes only emitted when actual notes are present
        self.assertIn("expectation_baseline", summary)
        self.assertIn("striving_objects", summary)
        self.assertIn("active_magnets", summary)
        self.assertIn("rupture_plasticity", summary)
        self.assertIn("registers", summary)
        self.assertIn("metabolic_style", summary)
        self.assertIn("public_expression_gate", summary["registers"])
        self.assertIn("current", summary["metabolic_style"])
        self.assertIn("registers", summary)
        self.assertIn("metabolic_style", summary)

    def test_state_summary_includes_baseline_strivings_when_present(self) -> None:
        from v3.core.state import StrivingObject, Magnet
        state = BackboneState(year=2015, age=14)
        state.expectation_baseline = {"attachment": "forbidden", "belonging": "hopeful"}
        state.striving_objects.append(
            StrivingObject(id="so_1", label="People-pleasing", need_axis="attachment", started_age=12, investment=60, identity_load=50)
        )
        state.active_magnets.append(Magnet(id="mg_1", label="A mentor", magnet_type="mentor", intensity=60, tenure_years=1))
        derived = compute_all_derived(state)
        summary = state_summary_from_backbone(state, derived)
        self.assertEqual(summary["expectation_baseline"].get("attachment"), "forbidden")
        self.assertEqual(len(summary["striving_objects"]), 1)
        self.assertEqual(summary["striving_objects"][0]["id"], "so_1")
        self.assertEqual(len(summary["active_magnets"]), 1)
        self.assertIn("active_metabolization_count", summary["rupture_plasticity"])

    def test_build_render_packet(self) -> None:
        packet = build_render_packet(
            year=2011,
            age=11,
            selected_events=[{"id": "ev_1", "label": "Friend", "intensity": "major"}],
            selected_magnets=[],
            state_deltas_applied={"capacity": {"agency": 5}, "framework_weights": []},
            constraints={"no_resolution": True},
        )
        self.assertEqual(packet["year"], 2011)
        self.assertEqual(packet["selected"]["events"][0]["label"], "Friend")
        self.assertTrue(packet["constraints"]["no_resolution"])

    def test_build_pass1_prompt_contains_summary(self) -> None:
        summary = {"year": 2011, "age": 11, "identity": {}, "field": {}, "capacity": {}, "wound": {}, "frameworks_active": [], "active_cracks": [], "last_year_notes": {}}
        prompt = build_pass1_prompt(summary)
        self.assertIn("2011", prompt)
        self.assertTrue("state summary" in prompt.lower() or "State summary" in prompt)

    def test_build_pass2_prompt_contains_packet(self) -> None:
        packet = build_render_packet(2011, 11, [], [], {}, {})
        prompt = build_pass2_prompt(packet)
        self.assertIn("2011", prompt)
        self.assertTrue("Render packet" in prompt or "render packet" in prompt)

    def test_parse_render_output_particularity_jaggedness_micro_causality_person_stubs(self) -> None:
        raw = {
            "narrative_snapshot": {"scene": "A scene.", "which_strata_fired": [], "which_frameworks_fired": [], "what_was_buffered": [], "what_scratched": []},
            "dialogue_snippets": [],
            "consistency_check": {},
            "particularity": {
                "place_anchor": {"value": "the old gym on mill street"},
                "object_anchor": {"value": "a cracked leather ball"},
                "schedule_anchor": {"value": "saturday 3pm practice"},
                "money_anchor": {"value": "twenty dollars for the bus"},
                "language_anchor": {"value": "coach's whistle and shouts"},
                "power_anchor": {"value": "who gets to start"},
                "body_anchor": {"value": "skinned knee from the fall"},
                "social_risk_anchor": {"value": "being picked last again"},
            },
            "jaggedness": [
                {"and": ["warmth", "cruelty"], "where": "coach praised then benched him"},
                {"and": ["loyalty", "betrayal"], "where": "teammate promised to pass and didn't"},
            ],
            "micro_causality": [{"detail": "the whistle", "caused": "everyone froze"}],
            "person_stubs": [{"name": "Coach Dale", "role": "coach", "signature": "hands on hips", "moral_edge": "win at any cost", "speech_tic": "again", "status_marker": "authority", "pressure_point": "his son on the bench"}],
        }
        out = parse_render_output(raw)
        self.assertEqual(len(out.get("particularity", {})), 8)
        self.assertIn("place_anchor", out["particularity"])
        self.assertEqual(out["particularity"]["place_anchor"].get("value"), "the old gym on mill street")
        self.assertEqual(len(out.get("jaggedness", [])), 2)
        self.assertEqual(out["jaggedness"][0]["and"], ["warmth", "cruelty"])
        self.assertEqual(len(out.get("micro_causality", [])), 1)
        self.assertEqual(out["micro_causality"][0]["detail"], "the whistle")
        self.assertEqual(len(out.get("person_stubs", [])), 1)
        self.assertEqual(out["person_stubs"][0]["name"], "Coach Dale")

    def test_validate_render_output_accepts_valid(self) -> None:
        parsed = {
            "narrative_snapshot": {"scene": "A scene."},
            "dialogue_snippets": [],
            "consistency_check": {},
            "particularity": {
                "place_anchor": {"value": "the old gym on mill street"},
                "object_anchor": {"value": "a cracked leather ball"},
                "schedule_anchor": {"value": "saturday 3pm practice"},
                "money_anchor": {"value": "twenty dollars for the bus"},
                "language_anchor": {"value": "coach's whistle"},
                "power_anchor": {"value": "who gets to start"},
                "body_anchor": {"value": "skinned knee"},
                "social_risk_anchor": {"value": "being picked last"},
            },
            "jaggedness": [
                {"and": ["warmth", "cruelty"], "where": "here"},
                {"and": ["loyalty", "betrayal"], "where": "there"},
            ],
            "micro_causality": [],
            "person_stubs": [],
        }
        all_ok, failures = validate_render_output(parsed, history=None)
        self.assertTrue(all_ok, failures)
        self.assertEqual(failures, [])

    def test_validate_no_repeats_with_history(self) -> None:
        # History with 2 years of particularity; current has novel anchors => pass
        history = [
            {"particularity": {k: {"value": f"old_{k}_year1"} for k in ("place_anchor", "object_anchor", "schedule_anchor", "money_anchor", "language_anchor", "power_anchor", "body_anchor", "social_risk_anchor")}},
            {"particularity": {k: {"value": f"old_{k}_year2"} for k in ("place_anchor", "object_anchor", "schedule_anchor", "money_anchor", "language_anchor", "power_anchor", "body_anchor", "social_risk_anchor")}},
        ]
        current_novel = {
            "particularity": {
                "place_anchor": {"value": "brand new place"},
                "object_anchor": {"value": "brand new object"},
                "schedule_anchor": {"value": "old_schedule_anchor_year1"},
                "money_anchor": {"value": "old_money_anchor_year1"},
                "language_anchor": {"value": "old_language_anchor_year1"},
                "power_anchor": {"value": "old_power_anchor_year1"},
                "body_anchor": {"value": "old_body_anchor_year1"},
                "social_risk_anchor": {"value": "old_social_risk_anchor_year1"},
            },
            "jaggedness": [{"and": ["a", "b"], "where": "w1"}, {"and": ["c", "d"], "where": "w2"}],
        }
        all_ok, failures = validate_render_output(current_novel, history=history)
        self.assertTrue(all_ok, failures)
        # Current with 0 novel anchors => no_repeats failure (need 2 novel)
        current_repeat = {
            "particularity": {
                "place_anchor": {"value": "old_place_anchor_year1"},
                "object_anchor": {"value": "old_object_anchor_year1"},
                "schedule_anchor": {"value": "old_schedule_anchor_year1"},
                "money_anchor": {"value": "old_money_anchor_year1"},
                "language_anchor": {"value": "old_language_anchor_year1"},
                "power_anchor": {"value": "old_power_anchor_year1"},
                "body_anchor": {"value": "old_body_anchor_year1"},
                "social_risk_anchor": {"value": "old_social_risk_anchor_year1"},
            },
            "jaggedness": [{"and": ["x", "y"], "where": "w1"}, {"and": ["z", "w"], "where": "w2"}],
        }
        all_ok2, failures2 = validate_render_output(current_repeat, history=history)
        self.assertFalse(all_ok2)
        self.assertTrue(any("no_repeats" in f for f in failures2))


if __name__ == "__main__":
    unittest.main()
