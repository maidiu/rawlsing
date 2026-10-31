from __future__ import annotations

import json
from pathlib import Path

from v3.core.derived import compute_all_derived
from v3.core.state import BackboneState
from v3.io.persona_sheet import build_persona_sheet
from v2.run_conversation_chat import load_persona_sheet_with_integrity


def test_v5_v2_chat_prompt_no_raw_v5_leaks(tmp_path: Path) -> None:
    state = BackboneState(year=2026, age=31)
    state.rendered_output = {"narrative_snapshot": {"scene": "A year passed."}, "dialogue_snippets": [], "consistency_check": {}}
    state.surface_psyche_profile = {
        "schema_version": "v516_surface_psyche_profile",
        "domains": {
            "body_self": {
                "felt_register": "contained",
                "analyst_pressure_account": {"secret": True},
                "pressure_flow_history": [{"stage": "hidden"}],
                "raw_v5_bridge": {"status": "green"},
            }
        },
        "analyst_pressure_account": {"top_level": True},
        "pressure_flow_history": [{"stage": "hidden"}],
        "profile_posterior": {"blocked": True},
        "stratum_tension_matrix": {"blocked": True},
        "relation_evidence_atom": {"blocked": True},
    }
    derived = compute_all_derived(state)
    sheet = build_persona_sheet(state, derived, identity_override={"country": "US", "given_name": "Test"})

    persona_path = tmp_path / "persona_sheet.json"
    persona_path.write_text(json.dumps(sheet), encoding="utf-8")

    history, integrity = load_persona_sheet_with_integrity(str(persona_path))
    assert integrity["verdict"] in {"clean", "degraded"}
    surface = history.metadata["surface_psyche"]
    assert "analyst_pressure_account" not in surface
    assert "pressure_flow_history" not in surface
    assert "profile_posterior" not in surface
    assert "stratum_tension_matrix" not in surface
    assert "relation_evidence_atom" not in surface
    assert "analyst_pressure_account" not in surface["domains"]["body_self"]
    assert "raw_v5_bridge" not in surface["domains"]["body_self"]
