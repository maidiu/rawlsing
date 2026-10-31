from __future__ import annotations

import copy

from v3.core.state import BackboneState
from v3.psyche.channels import SUBLIMATION_CHANNELS, assign_sublimation_channels
from v3.psyche.gating import route_unexpressed_load


def _make_state() -> BackboneState:
    state = BackboneState()
    for domain in state.domains.values():
        domain.baseline_load = 90.0
        domain.expressed_aim = 10.0
        domain.affect_channel = "quiet_organizing"
    return state


def test_assign_sublimation_channels_picks_valid_channels_for_all_domains() -> None:
    state = BackboneState()
    state.practice_stack.spiritual = 80.0
    assign_sublimation_channels(state)

    assert set(state.domains) == {"empire_occupation", "nation_state", "sect_class_ethnicity", "family_household", "body_self"}
    assert all(domain.affect_channel in SUBLIMATION_CHANNELS for domain in state.domains.values())


def test_route_unexpressed_load_changes_bounded_downstream_traits_and_practice_stack() -> None:
    state = _make_state()
    state.domains["empire_occupation"].affect_channel = "quiet_organizing"
    state.domains["nation_state"].affect_channel = "hyper_competence"
    state.domains["sect_class_ethnicity"].affect_channel = "caretaking_warmth"
    state.domains["family_household"].affect_channel = "piety_ritual"
    state.domains["body_self"].affect_channel = "somatic_irritability"

    before = {
        "organizing": state.practice_stack.organizing,
        "study": state.practice_stack.study,
        "craft": state.practice_stack.craft,
        "care": state.practice_stack.care,
        "spiritual": state.practice_stack.spiritual,
        "coherence": state.peak_routing.coherence,
        "health": state.capacity.health,
        "psychological_aperture": state.psychological_capacity.aperture,
        "anger": state.wound_vector.anger,
    }

    route_unexpressed_load(state)

    assert state.practice_stack.organizing > before["organizing"]
    assert state.practice_stack.study > before["study"]
    assert state.practice_stack.craft > before["craft"]
    assert state.practice_stack.care > before["care"]
    assert state.practice_stack.spiritual > before["spiritual"]
    assert state.peak_routing.coherence >= before["coherence"]
    assert 0.0 <= state.capacity.health <= 100.0
    assert state.psychological_capacity.aperture == before["psychological_aperture"]
    assert 0.0 <= state.wound_vector.anger <= 100.0


def test_route_unexpressed_load_unknown_channel_routes_safely() -> None:
    state = _make_state()
    for domain in state.domains.values():
        domain.baseline_load = 0.0
        domain.expressed_aim = 0.0
        domain.affect_channel = "quiet_organizing"
    state.domains["empire_occupation"].baseline_load = 90.0
    state.domains["empire_occupation"].expressed_aim = 10.0
    state.domains["empire_occupation"].affect_channel = "mystery_channel"
    before = copy.deepcopy(state.practice_stack)

    route_unexpressed_load(state)

    assert state.practice_stack.craft > before.craft
    assert state.practice_stack.organizing == before.organizing
    assert state.practice_stack.spiritual == before.spiritual
    assert state.practice_stack.care == before.care
