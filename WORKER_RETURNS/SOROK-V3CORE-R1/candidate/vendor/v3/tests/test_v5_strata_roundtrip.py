from __future__ import annotations

from v3.core.state import BackboneState, Stratum
from v3.io.json_codec import state_from_json, state_to_json


def _make_state() -> BackboneState:
    state = BackboneState()
    state.strata_stack = [
        Stratum(
            level=i,
            name=f"stratum_{i}",
            description=f"description_{i}",
            material_relation="exploited" if i % 2 == 0 else "intermediary",
            hegemonic_story=f"story_{i}",
            loyalty_demand=f"obey, organize, and resist #{i}",
            provision_strength=10.0 + i,
            coercion_strength=20.0 + i,
            contradiction_load=30.0 + i,
            visibility_of_complicity=40.0 + i,
            salience=50.0 + i,
        )
        for i in range(9)
    ]
    return state


def test_strata_stack_json_round_trip_preserves_strings_and_numbers() -> None:
    state = _make_state()

    round_tripped = state_from_json(state_to_json(state))

    assert len(round_tripped.strata_stack) == 9
    for i, (before, after) in enumerate(zip(state.strata_stack, round_tripped.strata_stack, strict=True)):
        assert after.level == i
        assert after.name == before.name
        assert after.description == before.description
        assert after.material_relation == before.material_relation
        assert after.hegemonic_story == before.hegemonic_story
        assert after.loyalty_demand == before.loyalty_demand
        assert after.provision_strength == before.provision_strength
        assert after.coercion_strength == before.coercion_strength
        assert after.contradiction_load == before.contradiction_load
        assert after.visibility_of_complicity == before.visibility_of_complicity
        assert after.salience == before.salience
