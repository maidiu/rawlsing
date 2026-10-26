"""Independent reviewer check of the recovered historical V3 machine on its fixture."""
from __future__ import annotations
import hashlib, json, os, sys
from pathlib import Path
ARCHIVE = Path(os.environ["RAD_REVIEW_ARCHIVE"])
S50 = ARCHIVE / "WORKER_RETURNS/SOROK-20261025-S50-HISTORICAL-V3-ACTOR-RECOVERY-R1"
sys.path.insert(0, str(S50))
from s50.bootstrap import install
install()
import v3.psyche.flow as flow
import v3.systems.topology as topology
from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.json_codec import state_to_json, state_from_json
from v3.core.derived import compute_all_derived
from v3.core.config_loader import load_v3config, load_step_order
from v3.engine.yearly_step import run_one_year
from s50.recovery import V3_FIXTURE
identity = json.loads(V3_FIXTURE.read_text())
state = backbone_state_from_identity(identity, year=2000, age=30)
derived = compute_all_derived(state)
config = load_v3config(); order = load_step_order()
def snap():
    return {
        "year": state.year, "age": state.age,
        "loop_topology": state.peak_routing.loop_topology,
        "topology_hysteresis_years": dict(state.peak_routing.topology_hysteresis_years or {}),
        "pressure_flow_history_len": len(state.pressure_flow_history),
        "pressure_flow_memory_grooves_domains": sorted((state.pressure_flow_memory.get("grooves") or {}).keys()),
        "surface_domains": sorted((state.surface_psyche_profile.get("domains") or {}).keys()),
        "analyst_domains": sorted((state.analyst_pressure_account.get("domains") or {}).keys()),
        "domains_with_baseline_load": sorted(k for k,d in state.domains.items() if getattr(d,'baseline_load',0)>0),
        "capacity_money": state.capacity.money,
        "vitality": state.psychological_capacity.vitality,
    }
before = snap()
run_one_year(state, derived, config, order)
after = snap()
js = state_to_json(state)
roundtrip = state_to_json(state_from_json(js)) == js
print(json.dumps({
 "schema":"RA_D_INDEPENDENT_REVIEW_V3_FUNCTIONS@1",
 "fixture_sha256": hashlib.sha256(V3_FIXTURE.read_bytes()).hexdigest(),
 "functions_present": {
   "run_pressure_flow_cycle": callable(flow.run_pressure_flow_cycle),
   "_derive_current_charge": callable(flow._derive_current_charge),
   "_channel_conductance": callable(flow._channel_conductance),
   "_simulate_domain_routes_transactionally": callable(flow._simulate_domain_routes_transactionally),
   "_commit_route_state": callable(flow._commit_route_state),
   "_update_memory": callable(flow._update_memory),
   "update_loop_topology": callable(topology.update_loop_topology),
   "run_one_year": callable(run_one_year),
 },
 "before": before,
 "after": after,
 "roundtrip_exact": roundtrip,
 "notes": {
   "annual_cadence": "run_one_year increments year/age and invokes scheduled annual steps before the post-year pressure-flow cycle.",
   "event_context_consumed": "pressure-flow event_context only counts events_this_year/micro_trace_this_year by type; it does not read event identity, access, or admitted semantic content.",
   "legacy_defaults": "fixture expectation_baseline is all 'hopeful' and psychological capacities are fixture values; not current-person authority."
 }
}, indent=2, sort_keys=True))
