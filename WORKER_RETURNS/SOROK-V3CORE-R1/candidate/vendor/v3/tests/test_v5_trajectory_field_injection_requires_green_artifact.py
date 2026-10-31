from __future__ import annotations

from v3.core.derived import DerivedIndices
from v3.core.state import BackboneState
from v3.io.field_injection import build_field_injection_from_harmonization
from v3.systems.field import update_field


def test_v5_trajectory_field_injection_requires_green_artifact() -> None:
    blocked_injection = build_field_injection_from_harmonization(
        v5_field_bridge={
            "status": "blocked",
            "field": {"economy": 77.0, "morale": 63.0},
            "refs": ["trajectory://blocked"],
            "notes": ["blocked artifact"],
        }
    )
    assert blocked_injection["_integrity"]["status"] == "blocked"
    assert "economy" not in blocked_injection
    assert "morale" not in blocked_injection

    blocked_state = BackboneState(year=2026, age=20)
    blocked_state.field.raw = {"economy": 11.0, "morale": 19.0}
    update_field(blocked_state, DerivedIndices(), {"field_injection": blocked_injection})
    assert blocked_state.field.raw["economy"] == 11.0
    assert blocked_state.field.raw["morale"] == 19.0
    assert blocked_state.yearly_integrity["field_injection"]["status"] == "blocked"

    green_injection = build_field_injection_from_harmonization(
        v5_field_bridge={
            "status": "green",
            "field": {"economy": 77.0, "morale": 63.0, "legitimacy": 58.0},
            "refs": ["trajectory://green"],
            "notes": ["green artifact"],
        }
    )
    assert green_injection["_integrity"]["status"] == "ok"
    assert green_injection["economy"] == 77.0
    assert green_injection["morale"] == 63.0

    green_state = BackboneState(year=2026, age=20)
    update_field(green_state, DerivedIndices(), {"field_injection": green_injection})
    assert green_state.field.raw["economy"] == 77.0
    assert green_state.field.raw["morale"] == 63.0
    assert green_state.field.raw["legitimacy"] == 58.0
    assert green_state.yearly_integrity["field_injection"]["status"] == "ok"
    assert green_state.field.provenance["fields"]["economy"]["source"] == "field_injection"
    assert green_state.field.provenance["fields"]["economy"]["source_detail"]["source"] == "v5_field_bridge"
