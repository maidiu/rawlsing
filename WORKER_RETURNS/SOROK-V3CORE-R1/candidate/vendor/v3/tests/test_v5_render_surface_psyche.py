from __future__ import annotations

import json

from v3.core.derived import compute_all_derived
from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.engine.llm_contract import build_render_packet
from v3.engine.prompts import PASS2_SYSTEM
from v3.engine.run_llm_band import run_llm_band_year


def _state_for_low_awareness() -> BackboneState:
    state = BackboneState(year=2001, age=16)
    for name in DOMAIN_NAMES:
        domain = state.domains[name]
        domain.A = 10.0
        domain.S = 45.0
        domain.V = 65.0
        domain.baseline_load = 55.0
        domain.expressed_aim = 5.0
        domain.affect_channel = "quiet_organizing"
    state.surface_psyche_profile = {
        "schema_version": "v516_surface_psyche_profile",
        "domains": {name: {"felt_register": "contained"} for name in DOMAIN_NAMES},
    }
    return state


def test_low_awareness_gating_uses_unknown_without_unbound_local_error() -> None:
    state = _state_for_low_awareness()
    derived = compute_all_derived(state)
    prompts: list[tuple[str, str]] = []

    def llm_callback(stage_label: str, prompt: str) -> str:
        prompts.append((stage_label, prompt))
        if "pass1" in stage_label:
            return json.dumps(
                {
                    "year": state.year,
                    "age": state.age,
                    "event_candidates": [
                        {
                            "id": "ev_1",
                            "kind": "practice",
                            "label": "Rehearsal after school",
                            "logline": "A low-stakes practice candidate.",
                            "intensity": "minor",
                            "channels": ["school"],
                            "implicated": {"domains": ["body_self"], "strata_levels": [8]},
                            "magnets": [],
                            "hooks": {"wound_hooks": ["recognition"], "capacity_hooks": ["agency"]},
                            "plausibility_notes": {"why_now": "routine practice", "what_makes_it_unlikely": "none"},
                        }
                    ],
                    "magnet_candidates": [],
                    "branch_hypotheses": [],
                }
            )
        return json.dumps(
            {
                "narrative_snapshot": {
                    "scene": "A short scene.",
                    "which_strata_fired": [],
                    "which_frameworks_fired": [],
                    "what_was_buffered": [],
                    "what_scratched": [],
                },
                "dialogue_snippets": [],
                "consistency_check": {"did_not_resolve": True, "public_vs_private_register_obeyed": True},
            }
        )

    run_llm_band_year(
        state,
        derived,
        {},
        llm_callback=llm_callback,
        previous_scene="",
    )

    pass2_prompts = [prompt for stage, prompt in prompts if "pass2" in stage]
    assert pass2_prompts
    assert "unknown" in pass2_prompts[0]
    assert state.yearly_integrity["llm_band"]["status"] == "applied"
    assert state.yearly_integrity["llm_band"]["render_pass"] == "pass2"


def test_build_render_packet_includes_sanitized_surface_psyche() -> None:
    packet = build_render_packet(
        2001,
        16,
        [],
        [],
        {},
        {},
        surface_psyche={
            "schema_version": "v516_surface_psyche_profile",
            "domains": {
                "body_self": {
                    "felt_register": "contained",
                    "analyst_pressure_account": {"secret": True},
                    "pressure_flow_history": [{"stage": "hidden"}],
                    "nested": {
                        "per_domain_trace_delta": {"body_self": {"capacity.health": -1.0}},
                        "raw_strata_pressure": 88.0,
                        "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS": {"body_self": {8: 1.0}},
                    },
                }
            },
            "analyst_pressure_account": {"top_level": True},
            "pressure_flow_history": [{"stage": "hidden"}],
            "per_domain_trace_delta": {"body_self": {"capacity.health": -1.0}},
            "raw_strata_pressure": 88.0,
            "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS": {"body_self": {8: 1.0}},
        },
    )

    surface = packet["surface_psyche"]
    assert "vitality_profile" not in surface
    assert "analyst_pressure_account" not in surface
    assert "pressure_flow_history" not in surface
    assert "per_domain_trace_delta" not in surface
    assert "raw_strata_pressure" not in surface
    assert "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS" not in surface
    assert "analyst_pressure_account" not in surface["domains"]["body_self"]
    assert "pressure_flow_history" not in surface["domains"]["body_self"]
    assert "nested" not in surface["domains"]["body_self"]


def test_pass2_system_does_not_instruct_persona_to_speak_analyst_account() -> None:
    assert "analyst_pressure_account" not in PASS2_SYSTEM
    assert "route_account" not in PASS2_SYSTEM
