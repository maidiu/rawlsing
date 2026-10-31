from __future__ import annotations

from v3.core.state import BackboneState, Stratum
from v3.io.json_codec import state_from_json, state_to_json
from v3.psyche.channels import assign_sublimation_channels, seed_wound_vector_from_identity
from v3.psyche.gating import apply_expression_gating, compute_baseline_load, route_unexpressed_load


def _make_state(high: bool) -> BackboneState:
    state = BackboneState()
    for domain in state.domains.values():
        domain.A = 80.0
        domain.V = 80.0
    strength = 80.0 if high else 10.0
    contradiction = 60.0 if high else 5.0
    state.strata_stack = [
        Stratum(level=i, name=f"stratum_{i}", coercion_strength=strength, contradiction_load=contradiction, visibility_of_complicity=50.0, salience=50.0)
        for i in range(5)
    ]
    return state


def test_baseline_load_varies_by_position() -> None:
    high = _make_state(True)
    low = _make_state(False)
    compute_baseline_load(high)
    compute_baseline_load(low)

    assert high.domains["empire_occupation"].baseline_load > low.domains["empire_occupation"].baseline_load
    assert high.domains["nation_state"].baseline_load > low.domains["nation_state"].baseline_load


def test_expression_gated_by_hostage_and_fatigue() -> None:
    state = BackboneState()
    domain = state.domains["empire_occupation"]
    domain.baseline_load = 100.0
    domain.expression_rate = 100.0
    domain.activation_threshold = 40.0
    state.psychological_capacity.vitality = 80.0
    state.registers.inner_load = 20.0

    apply_expression_gating(state)
    assert domain.expressed_aim == 100.0

    state.reproduction_constraints.housing_insecurity = 100.0
    state.reproduction_constraints.legal_status = 0.0
    state.reproduction_constraints.dependents = 80.0
    state.reproduction_constraints.debt = 60.0
    state.reproduction_constraints.job_insecurity = 80.0
    state.reproduction_constraints.caregiving_load = 70.0
    apply_expression_gating(state)
    assert domain.expressed_aim == 0.0
    assert domain.expression_rate < 100.0


def test_unexpressed_load_routed_to_channels() -> None:
    state = BackboneState()
    domain = state.domains["empire_occupation"]
    domain.baseline_load = 90.0
    domain.expressed_aim = 10.0
    domain.affect_channel = "quiet_organizing"

    before = state.practice_stack.organizing
    route_unexpressed_load(state)

    assert state.practice_stack.organizing > before


def test_sublimation_channels_seed_from_identity_and_wounds() -> None:
    state = BackboneState()
    seed_wound_vector_from_identity(
        state,
        {
            "class_origin": "working",
            "current_class": "working",
            "minority_status": "minoritized",
            "religiosity_level": 85,
        },
        age=16,
    )
    state.practice_stack.spiritual = 85.0
    assign_sublimation_channels(state)

    assert state.domains["family_household"].affect_channel in {"caretaking_warmth", "piety_ritual", "withdrawal_numbness"}
    assert state.domains["sect_class_ethnicity"].affect_channel in {"piety_ritual", "caretaking_warmth", "withdrawal_numbness"}

    state2 = BackboneState()
    seed_wound_vector_from_identity(
        state2,
        {
            "class_origin": "elite",
            "current_class": "elite",
            "minority_status": "dominant",
            "religiosity_level": 10,
        },
        age=42,
    )
    state2.practice_stack.spiritual = 10.0
    assign_sublimation_channels(state2)

    assert state2.domains["nation_state"].affect_channel in {"quiet_organizing", "micro_authoritarianism", "conspiracy_symbolic", "humor_irony", "hyper_competence"}
    assert state.domains["nation_state"].affect_channel != state2.domains["nation_state"].affect_channel


def test_domain_activation_fields_round_trip_json() -> None:
    state = BackboneState()
    domain = state.domains["nation_state"]
    domain.baseline_load = 77.5
    domain.expression_rate = 44.0
    domain.activation_threshold = 66.0
    domain.affect_channel = "humor_irony"

    round_tripped = state_from_json(state_to_json(state))
    rt_domain = round_tripped.domains["nation_state"]

    assert rt_domain.baseline_load == 77.5
    assert rt_domain.expression_rate == 44.0
    assert rt_domain.activation_threshold == 66.0
    assert rt_domain.affect_channel == "humor_irony"
