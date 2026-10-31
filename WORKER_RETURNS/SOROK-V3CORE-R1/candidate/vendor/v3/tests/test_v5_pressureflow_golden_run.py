from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from v3.core.derived import compute_all_derived
from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.engine.llm_contract import build_render_packet
from v3.io.json_codec import state_from_json, state_to_json
from v3.io.persona_sheet import build_persona_sheet
from v3.psyche.flow import run_pressure_flow_cycle


def _make_golden_state() -> BackboneState:
    state = BackboneState(year=2001, age=32)

    state.rendered_output = {
        "narrative_snapshot": {"scene": "The year settled into a tense but ordinary rhythm."},
        "dialogue_snippets": [],
        "consistency_check": {},
    }

    for name in DOMAIN_NAMES:
        domain = state.domains[name]
        domain.A = 25.0
        domain.S = 50.0
        domain.V = 70.0
        domain.baseline_load = 82.0
        domain.expressed_aim = 8.0
        domain.affect_channel = "quiet_organizing"

    state.domains["body_self"].affect_channel = "somatic_irritability"
    state.domains["body_self"].baseline_load = 92.0
    state.domains["family_household"].affect_channel = "caretaking_warmth"

    state.practice_stack.organizing = 78.0
    state.practice_stack.care = 68.0
    state.practice_stack.study = 55.0
    state.practice_stack.spiritual = 24.0
    state.capacity.health = 72.0
    state.capacity.social_support = 65.0
    state.psychological_capacity.vitality = 64.0
    state.psychological_capacity.aperture = 58.0
    state.psychological_capacity.agency = 61.0
    state.collective_infrastructure.network_density = 74.0
    state.registers.inner_load = 56.0
    return state


def _write_sidecars(base_dir: Path, state: BackboneState, derived: object, sheet: dict[str, object]) -> Path:
    base_dir.mkdir(parents=True, exist_ok=True)
    persona_path = base_dir / "persona_sheet.json"
    state_path = base_dir / "state_final.json"
    derived_path = base_dir / "derived_final.json"

    persona_path.write_text(json.dumps(sheet, indent=2, sort_keys=True), encoding="utf-8")
    state_path.write_text(state_to_json(state), encoding="utf-8")
    derived_path.write_text(json.dumps(getattr(derived, "__dict__", {}), indent=2, sort_keys=True), encoding="utf-8")
    return persona_path


def _forbidden_present(value: object, forbidden: set[str]) -> bool:
    if isinstance(value, dict):
        for key, nested in value.items():
            if key in forbidden:
                return True
            if _forbidden_present(nested, forbidden):
                return True
    elif isinstance(value, list):
        for item in value:
            if _forbidden_present(item, forbidden):
                return True
    return False


def test_pressureflow_golden_run_evidence_bundle_stays_offline_and_leak_free(tmp_path: Path) -> None:
    state = _make_golden_state()

    run_pressure_flow_cycle(
        state,
        assign_channels=False,
        compute_pressure=False,
        apply_gating=False,
        route_internal_charge=False,
    )

    round_tripped = state_from_json(state_to_json(state))
    assert round_tripped.pressure_flow_history
    assert round_tripped.surface_psyche_profile["schema_version"] == "v516_surface_psyche_profile"

    derived = compute_all_derived(state)
    sheet = build_persona_sheet(
        state,
        derived,
        identity_override={
            "given_name": "Amina",
            "family_name": "Test",
            "country": "US",
            "primary_language": "English",
            "languages": ["English", "Spanish"],
            "religion": "Catholic",
            "ethnicity": "Latina",
            "ses_band": "middle",
            "locality": "Brooklyn",
            "region": "NY",
        },
    )

    assert "surface_psyche" in sheet
    assert sheet["surface_psyche"]["schema_version"] == "v516_surface_psyche_profile"
    assert "vitality_profile" not in sheet["surface_psyche"]
    assert not _forbidden_present(
        sheet["surface_psyche"],
        {
            "analyst_pressure_account",
            "pressure_flow_history",
            "per_domain_trace_delta",
            "raw_strata_pressure",
            "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS",
        },
    )

    persona_path = _write_sidecars(tmp_path, state, derived, sheet)

    from v2.run_conversation_chat import load_persona_sheet_with_integrity
    from v2.conversation_engine import prepare_conversation_turn

    history, integrity = load_persona_sheet_with_integrity(str(persona_path))
    assert integrity["verdict"] == "clean"
    assert history.metadata["surface_psyche"]["schema_version"] == "v516_surface_psyche_profile"

    render_packet = build_render_packet(
        state.year,
        state.age,
        [],
        [],
        {},
        {},
        identity_override=sheet["identity"],
        persona_context={"structural_lucidity": derived.structural_lucidity_SL},
        surface_psyche=sheet["surface_psyche"],
    )
    assert "surface_psyche" in render_packet
    assert "vitality_profile" not in render_packet["surface_psyche"]
    assert not _forbidden_present(
        render_packet["surface_psyche"],
        {
            "analyst_pressure_account",
            "pressure_flow_history",
            "per_domain_trace_delta",
            "raw_strata_pressure",
            "DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS",
        },
    )

    with patch("v3.io.history_fetch.fetch_country_history", return_value="Offline history backdrop."):
        out = prepare_conversation_turn(
            history,
            "Tell me what the year felt like.",
            integrity_report=integrity,
            chat_relation_mode="generated_persona",
        )

    assert "SURFACE PSYCHE" in out["prompt"]
    assert "v516_surface_psyche_profile" in out["prompt"]
    assert "vitality_profile" not in out["prompt"]
    assert "analyst_pressure_account" not in out["prompt"]
    assert "pressure_flow_history" not in out["prompt"]
    assert "future_horizon_years" not in out["prompt"]
    assert "recovery_cost" not in out["prompt"]
    assert "conductance_multiplier" not in out["prompt"]
    assert "structural_lucidity" in out["prompt"]
    assert out["integrity_status"] == "clean"
    assert out["voice_schema_status"] == "clean"
