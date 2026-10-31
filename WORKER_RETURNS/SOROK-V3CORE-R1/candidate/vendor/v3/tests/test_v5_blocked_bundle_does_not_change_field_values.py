from __future__ import annotations

from v3.core.state import BackboneState, Stratum
from v3.io.json_codec import state_to_dict
from v3.io.v5_bridge import attach_v5_runtime_input_bundle


def _make_state() -> BackboneState:
    state = BackboneState(year=2024, age=39)
    state.capacity.time = 12.5
    state.capacity.money = 44.0
    state.capacity.health = 88.0
    state.psychological_capacity.agency = 67.0
    state.reproduction_constraints.debt = 21.0
    state.practice_stack.organizing = 9.0
    state.strata_stack = [
        Stratum(level=1, name="household", provision_strength=35.0, coercion_strength=18.0, contradiction_load=22.0),
        Stratum(level=2, name="community", provision_strength=61.0, coercion_strength=24.0, contradiction_load=11.0),
    ]
    state.autonomy_drive = 57.5
    state.safety_drive = 66.5
    return state


def test_v5_blocked_bundle_does_not_change_field_values() -> None:
    state = _make_state()
    before = state_to_dict(state)

    attach_v5_runtime_input_bundle(
        state,
        {
            "status": "blocked",
            "payload": {"reason": "missing statistical authority"},
            "notes": ["blocked branch"],
        },
        refs=["bundle://v5/blocker"],
        notes=["blocked branch", "no runtime mutation"],
    )

    after = state_to_dict(state)

    for key, value in before.items():
        if key in {"v5_runtime_input_bundle", "v5_runtime_input_refs", "v5_bridge_status"}:
            continue
        assert after[key] == value, key

    assert state.v5_bridge_status == "blocked"
    assert state.v5_runtime_input_refs == ["bundle://v5/blocker"]
    assert state.v5_runtime_input_bundle["status"] == "blocked"
    assert state.v5_runtime_input_bundle["payload"] == {"reason": "missing statistical authority"}
    assert state.v5_runtime_input_bundle["refs"] == ["bundle://v5/blocker"]
    assert state.v5_runtime_input_bundle["notes"] == ["blocked branch", "no runtime mutation"]
