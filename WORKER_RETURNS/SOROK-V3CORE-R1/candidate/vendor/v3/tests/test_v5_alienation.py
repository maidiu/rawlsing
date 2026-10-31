from __future__ import annotations

from v3.core.derived import DerivedIndices
from v3.core.state import BackboneState
from v3.engine.alienation import derive_alienation


def _make_state(
    *,
    a: float,
    s: float,
    v: float,
    buffer_type: str,
    inner_load: float,
    coherence: float,
    spiritual: float,
) -> BackboneState:
    state = BackboneState()
    for domain in state.domains.values():
        domain.A = a
        domain.S = s
        domain.V = v
        domain.buffer_type = buffer_type
    state.registers.inner_load = inner_load
    state.peak_routing.coherence = coherence
    state.practice_stack.spiritual = spiritual
    return state


def test_derive_alienation_changes_with_av_and_buffers() -> None:
    state_structural = _make_state(
        a=80.0,
        s=80.0,
        v=80.0,
        buffer_type="not_my_concern",
        inner_load=20.0,
        coherence=80.0,
        spiritual=70.0,
    )
    state_distant = _make_state(
        a=10.0,
        s=10.0,
        v=10.0,
        buffer_type="guilt",
        inner_load=80.0,
        coherence=20.0,
        spiritual=10.0,
    )

    derive_alienation(state_structural, DerivedIndices(), {})
    derive_alienation(state_distant, DerivedIndices(), {})

    assert state_structural.alienation_vector.distant_others < state_distant.alienation_vector.distant_others
    assert state_structural.alienation_vector.near_others < state_distant.alienation_vector.near_others
    assert state_structural.alienation_vector.moral_totality < state_distant.alienation_vector.moral_totality
    assert state_structural.alienation != state_distant.alienation


def test_derive_alienation_keeps_scalar_synced_to_vector() -> None:
    state = _make_state(
        a=30.0,
        s=20.0,
        v=40.0,
        buffer_type="liberal_utopian_blur",
        inner_load=65.0,
        coherence=45.0,
        spiritual=25.0,
    )

    derive_alienation(state, DerivedIndices(), {})

    expected = (
        state.alienation_vector.distant_others
        + state.alienation_vector.near_others
        + state.alienation_vector.self
        + state.alienation_vector.moral_totality
    ) / 4.0
    assert state.alienation == expected
