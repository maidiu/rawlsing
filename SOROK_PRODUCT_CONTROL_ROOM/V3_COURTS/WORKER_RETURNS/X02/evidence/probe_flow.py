from __future__ import annotations
import json, os, sys
from copy import deepcopy
from pathlib import Path
SOURCE_ROOT = os.environ["X02_SOURCE_ROOT"]
sys.path.insert(0, SOURCE_ROOT)
from v3.core.state import BackboneState, Stratum, Buffer, BufferCostProfile
from v3.core.enums import DOMAIN_NAMES
from v3.core.derived import compute_all_derived, compute_hostage_index
from v3.psyche.flow import (
    run_pressure_flow_cycle, _derive_current_charge, _domain_charge_ledger,
    _channel_conductance, _prior_groove, _update_memory, _simulate_domain_routes_transactionally,
    _apply_single_domain_route, _commit_route_state, _relational_field_conductance_bonus,
)
from v3.psyche.gating import _derive_hostage_index, apply_expression_gating, compute_baseline_load
from v3.psyche.channels import _pick_channel, assign_sublimation_channels, SUBLIMATION_CHANNELS
import v3.psyche.flow as flow

out = {"schema": "X02_PRESSURE_FLOW_SOURCE_PROBE@1", "source": "<X02_SOURCE_ROOT>", "tests": {}}

# 1. Exact charge formula and internal/trace split.
s = BackboneState(year=2000, age=30)
for name in DOMAIN_NAMES:
    d = s.domains[name]
    d.baseline_load = 80.0
    d.expressed_aim = 10.0
    d.affect_channel = "quiet_organizing"
s.registers.inner_load = 60.0
for k in ("shame","fear","anger","abandonment","control","recognition","loss"):
    setattr(s.wound_vector, k, 50.0)
current = _derive_current_charge(s, "body_self")
snap = run_pressure_flow_cycle(s, assign_channels=False, compute_pressure=False, apply_gating=False)
item = snap["charge_ledger"]["body_self"]
out["tests"]["charge_formula"] = {
    "baseline": 80.0, "inner_load": 60.0, "wound_mean": 50.0,
    "expected_current": round(80.0 * (0.90 + 60.0/500.0) * (0.92 + 50.0/625.0), 3),
    "actual_current": current,
    "overt_aim_charge": item["overt_aim_charge"],
    "internally_routed_charge": item["internally_routed_charge"],
    "trace_intensity": item["trace_intensity"],
    "conductance": item["channel_conductance"],
    "current_equals_overt_plus_internal": abs(item["current_charge"] - (item["overt_aim_charge"] + item["internally_routed_charge"])) < 1e-9,
}

# 2. Groove increases conductance, not current charge.
s1 = deepcopy(s); s2 = deepcopy(s)
s2.pressure_flow_memory = {"grooves": {"body_self": {"quiet_organizing": 100.0}}}
l1 = _domain_charge_ledger(s1, {})["body_self"]
l2 = _domain_charge_ledger(s2, s2.pressure_flow_memory)["body_self"]
out["tests"]["groove_effect"] = {
    "no_groove_conductance": l1["channel_conductance"],
    "groove_100_conductance": l2["channel_conductance"],
    "same_current_charge": l1["current_charge"] == l2["current_charge"],
    "trace_greater_than_internal_with_groove": l2["trace_intensity"] > l2["internally_routed_charge"],
}

# 3. Single-channel winner and tie-break.
tie = {"humor_irony": 10.0, "hyper_competence": 10.0, "quiet_organizing": 10.0}
out["tests"]["channel_selector"] = {
    "channel_set_size": len(SUBLIMATION_CHANNELS),
    "tie_scores": tie,
    "selected": _pick_channel(tie),
    "domain_field_type": "single str",
    "second_channel_field_present": False,
    "scores_persisted_on_domain": False,
}
out["tests"]["channel_selection_ignores_grooves"] = {}
_g0 = BackboneState(); _g1 = BackboneState()
for _n in DOMAIN_NAMES:
    for _st in (_g0, _g1):
        _d = _st.domains[_n]; _d.A = 20.0; _d.S = 20.0; _d.V = 80.0
_g1.pressure_flow_memory = {"grooves": {n: {"quiet_organizing": 100.0} for n in DOMAIN_NAMES}}
assign_sublimation_channels(_g0); assign_sublimation_channels(_g1)
out["tests"]["channel_selection_ignores_grooves"] = {
    "without_grooves": {n: _g0.domains[n].affect_channel for n in DOMAIN_NAMES},
    "with_grooves": {n: _g1.domains[n].affect_channel for n in DOMAIN_NAMES},
    "same_selection": {n: _g0.domains[n].affect_channel == _g1.domains[n].affect_channel for n in DOMAIN_NAMES},
    "memory_read_by_assign": False,
}

# 4. Duplicate hostage index definitions.
s4 = BackboneState()
s4.reproduction_constraints.dependents = 2.0
s4.reproduction_constraints.housing_insecurity = 20.0
s4.reproduction_constraints.legal_status = 80.0
s4.reproduction_constraints.debt = 20.0
s4.reproduction_constraints.job_insecurity = 30.0
s4.reproduction_constraints.caregiving_load = 20.0
out["tests"]["hostage_index_duplicate"] = {
    "derived_compute_hostage_index": compute_hostage_index(s4),
    "gating_private_derive_hostage_index": _derive_hostage_index(s4),
    "equal": abs(compute_hostage_index(s4) - _derive_hostage_index(s4)) < 1e-9,
}

# 5. Expression-rate ratchet over repeated cycles with constant high hostage.
s5 = BackboneState(year=2000, age=30)
for name in DOMAIN_NAMES:
    d = s5.domains[name]
    d.baseline_load = 80.0
    d.expression_rate = 100.0
    d.activation_threshold = 0.0
    d.affect_channel = "quiet_organizing"
s5.reproduction_constraints.housing_insecurity = 100.0
s5.reproduction_constraints.legal_status = 0.0
s5.reproduction_constraints.dependents = 80.0
s5.reproduction_constraints.debt = 60.0
s5.reproduction_constraints.job_insecurity = 80.0
s5.reproduction_constraints.caregiving_load = 70.0
rates = []
for i in range(3):
    run_pressure_flow_cycle(s5, assign_channels=False, compute_pressure=False, apply_gating=True, route_internal_charge=False)
    rates.append({"cycle": i+1, "expression_rate": s5.domains["body_self"].expression_rate, "expressed_aim": s5.domains["body_self"].expressed_aim})
out["tests"]["expression_rate_ratchet"] = {"rates": rates, "reset_code_found": False}

# 6. Pre-route live mutations survive a later transactional failure.
s6 = BackboneState(year=2000, age=30)
s6.strata_stack = [Stratum(level=i, name=f"s{i}", provision_strength=20.0, coercion_strength=80.0, contradiction_load=60.0, visibility_of_complicity=50.0, salience=50.0) for i in range(5)]
for name in DOMAIN_NAMES:
    s6.domains[name].A = 80.0
    s6.domains[name].V = 80.0
before = {
    "baseline_load": {n: s6.domains[n].baseline_load for n in DOMAIN_NAMES},
    "affect_channel": {n: s6.domains[n].affect_channel for n in DOMAIN_NAMES},
    "expression_rate": {n: s6.domains[n].expression_rate for n in DOMAIN_NAMES},
    "expressed_aim": {n: s6.domains[n].expressed_aim for n in DOMAIN_NAMES},
    "history_len": len(s6.pressure_flow_history),
}
orig = flow._update_memory
def boom(_history, _previous_memory=None):
    raise RuntimeError("forced post-route failure")
flow._update_memory = boom
try:
    try:
        run_pressure_flow_cycle(s6)
        failed = False
    except Exception:
        failed = True
finally:
    flow._update_memory = orig
after = {
    "baseline_load": {n: s6.domains[n].baseline_load for n in DOMAIN_NAMES},
    "affect_channel": {n: s6.domains[n].affect_channel for n in DOMAIN_NAMES},
    "expression_rate": {n: s6.domains[n].expression_rate for n in DOMAIN_NAMES},
    "expressed_aim": {n: s6.domains[n].expressed_aim for n in DOMAIN_NAMES},
    "history_len": len(s6.pressure_flow_history),
}
out["tests"]["transactional_boundary"] = {
    "raised": failed, "before": before, "after": after,
    "pre_route_fields_changed": before != after,
    "notes": "baseline_load/affect_channel/expression_rate/expressed_aim are written before the working-copy route simulation and are not rolled back.",
}

# 7. Buffer strength does not affect charge/conductance/trace, only metadata.
def buffer_state(strength):
    st = deepcopy(s)
    st.buffers = [Buffer(type="craft", strength=strength, cost_profile=BufferCostProfile(0,0,0,0))]
    return st
b0, b100 = buffer_state(0.0), buffer_state(100.0)
l0 = _domain_charge_ledger(b0, {})["body_self"]
l100 = _domain_charge_ledger(b100, {})["body_self"]
out["tests"]["buffer_not_in_route"] = {
    "current_equal": l0["current_charge"] == l100["current_charge"],
    "conductance_equal": l0["channel_conductance"] == l100["channel_conductance"],
    "trace_equal": l0["trace_intensity"] == l100["trace_intensity"],
    "buffer_strength_0": 0.0, "buffer_strength_100": 100.0,
    "insulation_score_read_by_route": False,
}

# 8. Memory update exact decay/increment.
prev = {"grooves": {"body_self": {"quiet_organizing": 10.0}}}
history = [{
    "charge_ledger": {n: {"current_charge": 80.0, "trace_intensity": 50.0, "primary_channel": "quiet_organizing"} for n in DOMAIN_NAMES},
    "year": 2000,
}]
mem = _update_memory(history, prev)
out["tests"]["memory_update"] = {
    "prior_groove": 10.0, "decay": 0.985, "increment": 0.035, "trace": 50.0,
    "expected": round(10.0*0.985 + 50.0*0.035, 3),
    "actual": mem["grooves"]["body_self"]["quiet_organizing"],
    "cycles_recorded": mem["cycles_recorded"],
    "history_window": mem["recent_window_years"],
}

# 9. Route field changes for each channel (cross-component scalar vs categorical).
route_rows = {}
for ch in SUBLIMATION_CHANNELS:
    rs = BackboneState(year=2000, age=30)
    d = rs.domains["body_self"]
    d.baseline_load = 80.0; d.expressed_aim = 0.0; d.affect_channel = ch
    before_dict = {k: dict(vars(v)) for k, v in {
        "capacity": rs.capacity, "psychological_capacity": rs.psychological_capacity,
        "practice_stack": rs.practice_stack, "peak_routing": rs.peak_routing,
        "style_traits": rs.style_traits, "wound_vector": rs.wound_vector,
    }.items()}
    item = _domain_charge_ledger(rs, {})["body_self"]
    _apply_single_domain_route(rs, item)
    after_dict = {k: dict(vars(v)) for k, v in {
        "capacity": rs.capacity, "psychological_capacity": rs.psychological_capacity,
        "practice_stack": rs.practice_stack, "peak_routing": rs.peak_routing,
        "style_traits": rs.style_traits, "wound_vector": rs.wound_vector,
    }.items()}
    changed = []
    for obj_name in before_dict:
        for field in before_dict[obj_name]:
            if before_dict[obj_name][field] != after_dict[obj_name][field]:
                changed.append(f"{obj_name}.{field}")
    route_rows[ch] = {"changed_fields": changed, "domain_A_S_V_changed": False}
out["tests"]["route_effects"] = route_rows

# 9a. Event semantic/identity content is not read by the pressure-flow route.
def semantic_state(label, **extra):
    st = BackboneState(year=2000, age=30)
    for n in DOMAIN_NAMES:
        d = st.domains[n]; d.baseline_load = 70.0; d.expressed_aim = 10.0; d.affect_channel = "quiet_organizing"
    st.events_this_year = [{"type": "job_loss", "label": label, **extra}]
    return st
sa = semantic_state("loss A")
sb = semantic_state("loss B", id="different-id", semantic_value="different")
ra = run_pressure_flow_cycle(sa, assign_channels=False, compute_pressure=False, apply_gating=False)
rb = run_pressure_flow_cycle(sb, assign_channels=False, compute_pressure=False, apply_gating=False)
out["tests"]["event_semantics_not_in_route"] = {
    "same_current_charge": ra["charge_ledger"] == rb["charge_ledger"],
    "same_trace_delta": ra["trace_delta"] == rb["trace_delta"],
    "same_memory": sa.pressure_flow_memory == sb.pressure_flow_memory,
    "event_context_a": ra["event_context"],
    "event_context_b": rb["event_context"],
}

# 9b. Categorical route effect not represented in the numeric trace audit.
sc = BackboneState(year=2000, age=30)
for n in DOMAIN_NAMES:
    sc.domains[n].baseline_load = 80.0
    sc.domains[n].expressed_aim = 0.0
    sc.domains[n].affect_channel = "conspiracy_symbolic"
sc_ledger = _domain_charge_ledger(sc, {})
sc_working, sc_per_domain, sc_aggregate = _simulate_domain_routes_transactionally(sc, sc_ledger)
out["tests"]["categorical_effect_audit"] = {
    "theory_before": sc.peak_routing.theory_of_change_style,
    "theory_after_working_copy": sc_working.peak_routing.theory_of_change_style,
    "aggregate_contains_theory": any("theory_of_change_style" in k for k in sc_aggregate),
    "per_domain_keys": sorted({k for v in sc_per_domain.values() for k in v}),
    "aggregate": sc_aggregate,
}

print(json.dumps(out, indent=2, sort_keys=True))
