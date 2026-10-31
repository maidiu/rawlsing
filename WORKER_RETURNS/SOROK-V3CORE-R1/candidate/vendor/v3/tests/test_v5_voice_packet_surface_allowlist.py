from __future__ import annotations

import json

from v3.engine.llm_contract import build_render_packet
from v3.engine.prompts import build_pass2_prompt


def test_v5_voice_packet_surface_allowlist_blocks_raw_v5_fields() -> None:
    packet = build_render_packet(
        2004,
        21,
        [],
        [],
        {},
        {},
        surface_psyche={
            "schema_version": "v516_surface_psyche_profile",
            "export_rule": "mediated_surface_only_not_persona_voice_permission",
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
        },
    )

    surface = packet["surface_psyche"]
    assert surface["schema_version"] == "v516_surface_psyche_profile"
    assert surface["export_rule"] == "mediated_surface_only_not_persona_voice_permission"
    assert "analyst_pressure_account" not in surface
    assert "pressure_flow_history" not in surface
    assert "profile_posterior" not in surface
    assert "stratum_tension_matrix" not in surface
    assert "relation_evidence_atom" not in surface
    assert "analyst_pressure_account" not in surface["domains"]["body_self"]
    assert "raw_v5_bridge" not in surface["domains"]["body_self"]

    prompt = build_pass2_prompt(packet)
    assert "analyst_pressure_account" not in prompt
    assert "pressure_flow_history" not in prompt
    assert "profile_posterior" not in prompt
    assert "stratum_tension_matrix" not in prompt
    assert "relation_evidence_atom" not in prompt
    assert '"felt_register": "contained"' in prompt
