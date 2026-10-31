from __future__ import annotations

from v3.core.state import BackboneState, Framework
from v3.io.json_codec import state_from_json, state_to_json
from v3.systems.frameworks import enforce_framework_caps


def _make_state() -> BackboneState:
    state = BackboneState(year=2001, age=33)
    state.frameworks = [
        Framework(id=f"fw_{i}", weight=16.0 - i * 4.0, tenure_years=i, failure_mode="test")
        for i in range(8)
    ]
    return state


def test_framework_caps_move_excess_to_dormant() -> None:
    state = _make_state()

    enforce_framework_caps(state)

    assert len([fw for fw in state.frameworks if fw.weight >= 5.0]) <= 3
    assert len(state.frameworks_dormant) == 5
    assert all(entry["reason_dormant"] == "weight_below_5" for entry in state.frameworks_dormant)
    assert {entry["id"] for entry in state.frameworks_dormant} == {f"fw_{i}" for i in range(3, 8)}


def test_framework_dormancy_survives_json_round_trip() -> None:
    state = _make_state()
    enforce_framework_caps(state)

    round_tripped = state_from_json(state_to_json(state))

    assert len([fw for fw in round_tripped.frameworks if fw.weight >= 5.0]) <= 3
    assert len(round_tripped.frameworks_dormant) == 5
    assert round_tripped.frameworks_dormant == state.frameworks_dormant
