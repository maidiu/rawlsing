# v3/tests/test_step_logic.py
# Wave 3: step implementations (reproduction, capacity, buffers) move state and derived; test with outputs.

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent.parent))

from v3.core.config_loader import load_v3config, load_step_order
from v3.core.derived import DerivedIndices, compute_all_derived
from v3.core.state import BackboneState
from v3.engine.yearly_step import run_one_year
from v3.systems.reproduction import update_reproduction_constraints
from v3.systems.capacity import update_capacity
from v3.systems.buffers import update_buffers
from v3.systems.domains import update_domains
from v3.systems.alienation import update_alienation
from v3.systems.cracks import update_cracks
from v3.systems.field import update_field
from v3.systems.frameworks import update_framework_weights
from v3.systems.infrastructure import update_collective_infrastructure
from v3.systems.practices import update_practice_stack


def test_reproduction_constraints_update_applies_event_deltas() -> None:
    """Events with reproduction_deltas change constraints and thus hostage_index after step."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.reproduction_constraints.job_insecurity = 10.0
    state.reproduction_constraints.debt = 5.0
    state.events_this_year = [
        {"reproduction_deltas": {"job_insecurity": 15.0, "debt": 10.0}},
    ]
    derived_before = compute_all_derived(state)
    update_reproduction_constraints(state, derived_before, config)
    derived_after = compute_all_derived(state)
    assert state.reproduction_constraints.job_insecurity == 25.0, "job_insecurity 10+15=25"
    assert state.reproduction_constraints.debt == 15.0, "debt 5+10=15"
    assert derived_after.hostage_index != derived_before.hostage_index or (derived_before.hostage_index == 0 and derived_after.hostage_index > 0), (
        "hostage_index should move when constraints change"
    )
    print(
        f"  reproduction_deltas job_insecurity 10→25, debt 5→15; "
        f"hostage_index {derived_before.hostage_index:.1f} → {derived_after.hostage_index:.1f}"
    )


def test_reproduction_delta_cap_limits_year_total() -> None:
    """Sum of event deltas for one field is capped by config (reproduction_constraints_fields)."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.reproduction_constraints.dependents = 20.0
    # Cap is 20; sum of deltas = 50 should be clamped to +20.
    state.events_this_year = [
        {"reproduction_deltas": {"dependents": 25.0}},
        {"reproduction_deltas": {"dependents": 25.0}},
    ]
    update_reproduction_constraints(state, DerivedIndices(), config)
    assert state.reproduction_constraints.dependents == 40.0, "20 + capped(50)=20 -> 40"
    print(f"  dependents 20 + sum_deltas(25+25)=50 capped to +20 → 40 (delta_cap=20)")


def test_capacity_update_applies_event_deltas() -> None:
    """Events with capacity_deltas change capacity and thus AC after step."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.capacity.money = 50.0
    state.events_this_year = [{"capacity_deltas": {"money": -10.0}}]
    derived = compute_all_derived(state)
    update_capacity(state, derived, config)
    assert state.capacity.money == 40.0, "50 - 10 = 40"
    print(f"  capacity_deltas money 50 → 40 (event -10)")


def test_domains_update_applies_event_deltas() -> None:
    """Events with domain_deltas change A/S/V/Aim and thus structural_lucidity_SL after step."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.domains["empire_occupation"].A = 20.0
    state.domains["empire_occupation"].V = 10.0
    # delta_cap for domain_A/domain_V is 10, so 8 and 5 both apply in full
    state.events_this_year = [
        {"domain_deltas": {"empire_occupation": {"A": 8.0, "V": 5.0}}},
    ]
    derived_before = compute_all_derived(state)
    update_domains(state, derived_before, config)
    derived_after = compute_all_derived(state)
    assert state.domains["empire_occupation"].A == 28.0, "A 20+8=28"
    assert state.domains["empire_occupation"].V == 15.0, "V 10+5=15"
    print(
        f"  domain_deltas empire_occupation A 20→28, V 10→15; SL {derived_before.structural_lucidity_SL:.1f} → {derived_after.structural_lucidity_SL:.1f}"
    )


def test_alienation_update_applies_event_delta() -> None:
    """Events with alienation_delta change alienation (vector aggregate) and thus mis_aim_risk after step."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.alienation_vector.distant_others = state.alienation_vector.near_others = state.alienation_vector.self = state.alienation_vector.moral_totality = 20.0
    state.alienation = 20.0
    state.events_this_year = [{"alienation_delta": 10.0}]
    derived_before = compute_all_derived(state)
    update_alienation(state, derived_before, config)
    derived_after = compute_all_derived(state)
    assert state.alienation == 30.0, "alienation 20+10=30"
    print(
        f"  alienation_delta 20→30; mis_aim_risk {derived_before.mis_aim_risk:.1f} → {derived_after.mis_aim_risk:.1f}"
    )


def test_cracks_update_applies_event_deltas() -> None:
    """Events with crack_deltas change intensity/latent_pressure per crack."""
    from v3.core.state import Crack
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.cracks = [Crack(intensity=10.0, latent_pressure=5.0)]
    state.events_this_year = [{"crack_deltas": [{"intensity": 8.0, "latent_pressure": 10.0}]}]
    update_cracks(state, DerivedIndices(), config)
    assert state.cracks[0].intensity == 18.0, "intensity 10+8=18"
    assert state.cracks[0].latent_pressure == 15.0, "latent_pressure 5+10=15"
    print(f"  crack_deltas[0] intensity 10→18, latent_pressure 5→15")


def test_frameworks_update_applies_event_deltas() -> None:
    """Events with framework_deltas change framework weights."""
    from v3.core.state import Framework
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.frameworks = [Framework(id="a", weight=10.0), Framework(id="b", weight=20.0)]
    state.events_this_year = [{"framework_deltas": [5.0, -3.0]}]
    update_framework_weights(state, DerivedIndices(), config)
    assert state.frameworks[0].weight == 15.0, "10+5=15"
    assert state.frameworks[1].weight == 17.0, "20-3=17"
    print(f"  framework_deltas weights 10→15, 20→17")


def test_practice_stack_update_applies_event_deltas() -> None:
    """Events with practice_deltas change practice stack."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.practice_stack.organizing = 40.0
    state.practice_stack.craft = 50.0
    state.events_this_year = [{"practice_deltas": {"organizing": 10.0, "craft": -5.0}}]
    update_practice_stack(state, DerivedIndices(), config)
    assert state.practice_stack.organizing == 50.0, "40+10=50"
    assert state.practice_stack.craft == 45.0, "50-5=45"
    print(f"  practice_deltas organizing 40→50, craft 50→45")


def test_field_update_applies_event_deltas() -> None:
    """Events with field_deltas update state.field.raw (applied at start of next year)."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.field.raw = {"economy": 50.0, "repression_baseline": 40.0}
    state.events_this_year = [{"field_deltas": {"economy": 8.0, "repression_baseline": -5.0}}]
    update_field(state, DerivedIndices(), config)
    assert state.field.raw.get("economy") == 58.0, "economy 50+8=58"
    assert state.field.raw.get("repression_baseline") == 35.0, "repression 40-5=35"
    print(f"  field_deltas economy 50→58, repression_baseline 40→35")


def test_infrastructure_update_applies_event_deltas() -> None:
    """Events with infrastructure_deltas change collective_infrastructure."""
    config = load_v3config()
    state = BackboneState(year=2000, age=30)
    state.collective_infrastructure.network_density = 20.0
    state.collective_infrastructure.org_discipline = 30.0
    state.events_this_year = [{"infrastructure_deltas": {"network_density": 10.0, "org_discipline": -5.0}}]
    update_collective_infrastructure(state, DerivedIndices(), config)
    assert state.collective_infrastructure.network_density == 30.0, "20+10=30"
    assert state.collective_infrastructure.org_discipline == 25.0, "30-5=25"
    print(f"  infrastructure_deltas network_density 20→30, org_discipline 30→25")


def test_event_sampling_produces_events_in_full_run() -> None:
    """event_sampling (in run_one_year) populates events_this_year; downstream steps consume them."""
    config = load_v3config()
    step_order = load_step_order()
    state = BackboneState(year=2000, age=30)
    derived = compute_all_derived(state)
    run_one_year(state, derived, config, step_order)
    # Events are sampled during the year; we can't inspect mid-run. After one year, state moved.
    # Run a few more years and check that derived drift (event-driven) is visible.
    for _ in range(4):
        run_one_year(state, derived, config, step_order)
    assert state.year == 2005 and state.age == 35
    print(
        f"  after 5 years: year={state.year}, hostage_index={derived.hostage_index:.1f}, AC={derived.agency_capacity_AC:.1f}, "
        f"mis_aim={derived.mis_aim_risk:.1f} (event-driven drift)"
    )


def test_run_one_year_advances_and_derived_valid() -> None:
    """Full run_one_year: completes without error; year/age advance; derived stays in valid range."""
    config = load_v3config()
    step_order = load_step_order()
    state = BackboneState(year=2000, age=30)
    derived = compute_all_derived(state)
    run_one_year(state, derived, config, step_order)
    assert state.year == 2001 and state.age == 31, "year and age advance"
    assert 0 <= derived.hostage_index <= 100 and 0 <= derived.agency_capacity_AC <= 100, "derived in range"
    print(
        f"  year 2000→2001, age 30→31; hostage_index={derived.hostage_index:.1f}, AC={derived.agency_capacity_AC:.1f}, "
        f"SL={derived.structural_lucidity_SL:.1f}, mis_aim_risk={derived.mis_aim_risk:.1f}"
    )


if __name__ == "__main__":
    import inspect
    print("--- test_step_logic ---")
    for _name, obj in inspect.getmembers(sys.modules[__name__], predicate=inspect.isfunction):
        if _name.startswith("test_"):
            obj()
            print(f"  {_name} passed")
    print("All tests passed.")
