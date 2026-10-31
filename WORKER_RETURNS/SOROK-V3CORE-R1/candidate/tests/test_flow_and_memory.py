from __future__ import annotations

from conftest import projection, year_input

from v3.core.invariants import backbone_hash
from v3core_adapter.contracts import Status
from v3core_adapter.flow_quarantine import run_conserved_charge_flow_probe
from v3core_adapter.memory import update_material_memory
from v3core_adapter.scheduler import run_year


def test_conserved_charge_flow_is_held_by_default() -> None:
    proj = projection()
    before = backbone_hash(proj.state)
    probe = run_conserved_charge_flow_probe(proj.state)
    assert probe.status == Status.HELD_CONSERVED_CHARGE_MODEL
    assert probe.live_state_mutated is False
    assert backbone_hash(proj.state) == before


def test_conserved_charge_flow_probe_is_test_only_and_nonmutating() -> None:
    proj = projection()
    before = backbone_hash(proj.state)
    probe = run_conserved_charge_flow_probe(proj.state, explicitly_enabled=True)
    assert probe.status == Status.APPLIED_TEST_ONLY_SOURCEFREE
    assert probe.live_state_mutated is False
    assert probe.reason == "test_only_conserved_charge_model_not_science"
    assert probe.snapshot["charge_ledger"]
    assert backbone_hash(proj.state) == before


def test_material_memory_tracks_source_deltas_not_conserved_charge() -> None:
    proj = projection()
    run_year(proj, year_input(prior=proj.prior_snapshot))
    memory = update_material_memory(proj.years)
    assert memory["cycles_recorded"] == 1
    assert memory["lifetime_cash_delta"] == 2.0
    assert memory["recent_cash_delta"] == 2.0
    assert memory["charge_conservation_assumed"] is False
    assert memory["durable_source_events"] == ["EV_MARKET_WORK"]
    assert len(memory["memory_hash"]) == 64
