"""Independent RX02 sourcefree probes against original V3. Read-only."""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, zipfile
from copy import deepcopy
from pathlib import Path

SRC = Path(os.environ["X02_SOURCE_ROOT"])
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, Stratum, Buffer, BufferCostProfile
from v3.core.derived import compute_hostage_index, compute_all_derived
from v3.psyche.channels import (
    SUBLIMATION_CHANNELS, assign_sublimation_channels, _pick_channel,
)
from v3.psyche.flow import (
    run_pressure_flow_cycle, _derive_current_charge, _domain_charge_ledger,
    _channel_conductance, _update_memory,
)
from v3.psyche.gating import _derive_hostage_index
import v3.psyche.flow as flow

out = {"schema": "RX02_REVIEW_PROBE@1", "source_root": "<X02_SOURCE_ROOT>"}

# A. Source identity: X02 19 files vs local/S50/zip.
x02 = json.loads(subprocess.check_output([
    "git", "-C", os.environ["RX02_RAWLSING_REPO"], "show",
    "b8ccf53f591a9b067a029e3c64ecad2874794d03:SOROK_PRODUCT_CONTROL_ROOM/V3_COURTS/WORKER_RETURNS/X02/source_identity.json"
]))
s50 = json.loads(Path(os.environ["X02_S50_MANIFEST"]).read_text())
s50paths = {r["path"] for r in s50["selected_files_verified"]}
zip_path = Path(os.environ["X02_STAGING_ZIP"])
rows = []
with zipfile.ZipFile(zip_path) as z:
    names = set(z.namelist())
    for r in x02["files"]:
        p = SRC / r["path"]
        local = hashlib.sha256(p.read_bytes()).hexdigest() if p.is_file() else ""
        zn = "Rawlsing_code_bundle_staging/" + r["path"]
        zdata = z.read(zn) if zn in names else b""
        rows.append({
            "path": r["path"], "x02_sha256": r["sha256"], "local_sha256": local,
            "local_exact": local == r["sha256"], "in_s50": r["path"] in s50paths,
            "zip_top_level_exact": bool(zdata) and hashlib.sha256(zdata).hexdigest() == r["sha256"],
        })
out["source_identity"] = {
    "x02_files": len(rows), "local_exact": sum(r["local_exact"] for r in rows),
    "in_s50": sum(r["in_s50"] for r in rows), "not_in_s50": sum(not r["in_s50"] for r in rows),
    "zip_exact": sum(r["zip_top_level_exact"] for r in rows), "rows": rows,
}
s50_ok = 0
for r in s50["selected_files_verified"]:
    p = SRC / r["path"]
    if p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest() == r["sha256"]:
        s50_ok += 1
out["source_identity"]["s50_selected_exact"] = s50_ok
out["source_identity"]["s50_selected_total"] = len(s50["selected_files_verified"])

# B. Charge formula and non-conservation.
s = BackboneState(year=2000, age=30)
for n in DOMAIN_NAMES:
    d = s.domains[n]; d.baseline_load = 80.0; d.expressed_aim = 10.0; d.affect_channel = "quiet_organizing"
s.registers.inner_load = 60.0
for k in ("shame","fear","anger","abandonment","control","recognition","loss"):
    setattr(s.wound_vector, k, 50.0)
current = _derive_current_charge(s, "body_self")
snap = run_pressure_flow_cycle(s, assign_channels=False, compute_pressure=False, apply_gating=False)
item = snap["charge_ledger"]["body_self"]
out["charge"] = {
    "expected_current": round(80.0 * (0.90 + 60.0/500.0) * (0.92 + 50.0/625.0), 3),
    "current": current, "overt": item["overt_aim_charge"],
    "internal": item["internally_routed_charge"], "trace": item["trace_intensity"],
    "conductance": item["channel_conductance"],
    "overt_plus_internal_equals_current": abs(item["current_charge"] - item["overt_aim_charge"] - item["internally_routed_charge"]) < 1e-9,
}
# Groove 100 makes trace > current, not only internal.
s_g = deepcopy(s); s_g.pressure_flow_memory = {"grooves": {n: {"quiet_organizing": 100.0} for n in DOMAIN_NAMES}}
g = _domain_charge_ledger(s_g, s_g.pressure_flow_memory)["body_self"]
out["charge"]["groove_100"] = {"conductance": g["channel_conductance"], "trace": g["trace_intensity"], "current": g["current_charge"], "trace_exceeds_current": g["trace_intensity"] > g["current_charge"]}

# C. Grooves do not select; route history can change selection via wound/practice scalars.
g0, g1 = BackboneState(), BackboneState()
for n in DOMAIN_NAMES:
    for st in (g0, g1):
        d = st.domains[n]; d.A = 20.0; d.S = 20.0; d.V = 80.0
g1.pressure_flow_memory = {"grooves": {n: {"quiet_organizing": 100.0} for n in DOMAIN_NAMES}}
assign_sublimation_channels(g0); assign_sublimation_channels(g1)
out["grooves_do_not_select"] = {
    "same": all(g0.domains[n].affect_channel == g1.domains[n].affect_channel for n in DOMAIN_NAMES),
    "without": {n: g0.domains[n].affect_channel for n in DOMAIN_NAMES},
    "with": {n: g1.domains[n].affect_channel for n in DOMAIN_NAMES},
}
# Route history counterexample: body somatic -> quiet_organizing after anger/spiritual move.
h = BackboneState(year=2000, age=30)
h.practice_stack.spiritual = 50.0
for n in DOMAIN_NAMES:
    d = h.domains[n]; d.A = 50.0; d.S = 50.0; d.V = 50.0; d.baseline_load = 0.0; d.expressed_aim = 0.0
b = h.domains["body_self"]; b.A = 40.0; b.S = 70.0; b.V = 80.0
h.wound_vector.anger = 59.0
for k in ("shame","fear","abandonment","control","recognition","loss"): setattr(h.wound_vector, k, 50.0)
assign_sublimation_channels(h)
before_channels = {n: h.domains[n].affect_channel for n in DOMAIN_NAMES}
for n in DOMAIN_NAMES: h.domains[n].baseline_load = 80.0; h.domains[n].expressed_aim = 0.0
h.domains["body_self"].affect_channel = "somatic_irritability"
run_pressure_flow_cycle(h, assign_channels=False, compute_pressure=False, apply_gating=False)
assign_sublimation_channels(h)
out["route_history_can_change_selection"] = {
    "before": before_channels, "after": {n: h.domains[n].affect_channel for n in DOMAIN_NAMES},
    "body_before": before_channels["body_self"], "body_after": h.domains["body_self"].affect_channel,
    "anger_after": round(h.wound_vector.anger, 3), "spiritual_after": round(h.practice_stack.spiritual, 3),
    "flipped": before_channels["body_self"] != h.domains["body_self"].affect_channel,
}

# D. One winner / tie.
tie = {c: (10.0 if c in ("humor_irony", "hyper_competence", "quiet_organizing") else 0.0) for c in SUBLIMATION_CHANNELS}
out["single_winner"] = {"tie_selected": _pick_channel(tie), "channel_count": len(SUBLIMATION_CHANNELS), "domain_field_is_single_str": isinstance(BackboneState().domains["body_self"].affect_channel, str), "second_field": hasattr(BackboneState().domains["body_self"], "secondary_channel")}

# E. Duplicate hostage.
hs = BackboneState()
hs.reproduction_constraints.dependents = 2.0
hs.reproduction_constraints.housing_insecurity = 20.0
hs.reproduction_constraints.legal_status = 80.0
hs.reproduction_constraints.debt = 20.0
hs.reproduction_constraints.job_insecurity = 30.0
hs.reproduction_constraints.caregiving_load = 20.0
out["hostage_duplicate"] = {"derived": compute_hostage_index(hs), "gating": _derive_hostage_index(hs), "equal": abs(compute_hostage_index(hs) - _derive_hostage_index(hs)) < 1e-9}

# F. Ratchet.
rs = BackboneState(year=2000, age=30)
for n in DOMAIN_NAMES:
    d = rs.domains[n]; d.baseline_load = 80.0; d.expression_rate = 100.0; d.activation_threshold = 0.0; d.affect_channel = "quiet_organizing"
rs.reproduction_constraints.housing_insecurity = 100.0
rs.reproduction_constraints.legal_status = 0.0
rs.reproduction_constraints.dependents = 80.0
rs.reproduction_constraints.debt = 60.0
rs.reproduction_constraints.job_insecurity = 80.0
rs.reproduction_constraints.caregiving_load = 70.0
rates = []
for i in range(3):
    run_pressure_flow_cycle(rs, assign_channels=False, compute_pressure=False, apply_gating=True, route_internal_charge=False)
    rates.append({"cycle": i + 1, "expression_rate": rs.domains["body_self"].expression_rate, "expressed_aim": rs.domains["body_self"].expressed_aim})
out["ratchet"] = {"rates": rates, "reset_assignment_found": False}

# G. Pre-route transaction residue: X02-style and tailored high-hostage/low-energy.
def forced_failure(state):
    before = {n: {"baseline_load": state.domains[n].baseline_load, "affect_channel": state.domains[n].affect_channel, "expression_rate": state.domains[n].expression_rate, "expressed_aim": state.domains[n].expressed_aim} for n in DOMAIN_NAMES}
    orig = flow._update_memory
    def boom(_h, _p=None): raise RuntimeError("forced post-route failure")
    flow._update_memory = boom
    try:
        try: run_pressure_flow_cycle(state)
        except Exception: pass
    finally:
        flow._update_memory = orig
    after = {n: {"baseline_load": state.domains[n].baseline_load, "affect_channel": state.domains[n].affect_channel, "expression_rate": state.domains[n].expression_rate, "expressed_aim": state.domains[n].expressed_aim} for n in DOMAIN_NAMES}
    changed = []
    for n in DOMAIN_NAMES:
        for k in before[n]:
            if before[n][k] != after[n][k]: changed.append(f"{n}.{k}")
    return {"before": before, "after": after, "changed": changed}

x02_style = BackboneState(year=2000, age=30)
x02_style.strata_stack = [Stratum(level=i, name=f"s{i}", provision_strength=20.0, coercion_strength=80.0, contradiction_load=60.0, visibility_of_complicity=50.0, salience=50.0) for i in range(5)]
for n in DOMAIN_NAMES: x02_style.domains[n].A = 80.0; x02_style.domains[n].V = 80.0
tail = BackboneState(year=2000, age=30)
tail.strata_stack = [Stratum(level=i, name=f"s{i}", provision_strength=20.0, coercion_strength=80.0, contradiction_load=60.0, visibility_of_complicity=50.0, salience=50.0) for i in range(5)]
for n in DOMAIN_NAMES:
    d = tail.domains[n]; d.A = 80.0; d.V = 80.0; d.baseline_load = 100.0; d.expression_rate = 100.0; d.activation_threshold = 10.0; d.expressed_aim = 0.0; d.affect_channel = "compartmentalization"
tail.psychological_capacity.vitality = 10.0; tail.registers.inner_load = 100.0
tail.reproduction_constraints.housing_insecurity = 100.0; tail.reproduction_constraints.legal_status = 0.0; tail.reproduction_constraints.dependents = 80.0; tail.reproduction_constraints.debt = 60.0; tail.reproduction_constraints.job_insecurity = 80.0; tail.reproduction_constraints.caregiving_load = 70.0
out["transaction"] = {"x02_style": forced_failure(x02_style), "tailored": forced_failure(tail)}

# H. Categorical trace omission.
cs = BackboneState(year=2000, age=30)
for n in DOMAIN_NAMES:
    d = cs.domains[n]; d.baseline_load = 80.0; d.expressed_aim = 0.0; d.affect_channel = "conspiracy_symbolic"
ledger = _domain_charge_ledger(cs, {})
working, per_domain, aggregate = flow._simulate_domain_routes_transactionally(cs, ledger)
out["categorical_trace"] = {"theory_before": cs.peak_routing.theory_of_change_style, "theory_after_working": working.peak_routing.theory_of_change_style, "aggregate_has_theory": any("theory_of_change_style" in k for k in aggregate), "aggregate": aggregate, "per_domain_keys": sorted({k for v in per_domain.values() for k in v})}

# I. Buffer route and metadata.
def buf_state(strength):
    st = deepcopy(s); st.buffers = [Buffer(type="craft", strength=strength, cost_profile=BufferCostProfile(0,0,0,0))]; return st
b0, b100 = buf_state(0.0), buf_state(100.0)
l0 = _domain_charge_ledger(b0, {})["body_self"]; l100 = _domain_charge_ledger(b100, {})["body_self"]
out["buffer"] = {"current_equal": l0["current_charge"] == l100["current_charge"], "conductance_equal": l0["channel_conductance"] == l100["channel_conductance"], "trace_equal": l0["trace_intensity"] == l100["trace_intensity"], "insulation_mode_0": l0["insulation_mode"], "insulation_mode_100": l100["insulation_mode"], "insulation_confidence_0": l0["insulation_confidence"], "insulation_confidence_100": l100["insulation_confidence"]}

# J. Event semantics.
def sem_state(label, **extra):
    st = BackboneState(year=2000, age=30)
    for n in DOMAIN_NAMES:
        d = st.domains[n]; d.baseline_load = 70.0; d.expressed_aim = 10.0; d.affect_channel = "quiet_organizing"
    st.events_this_year = [{"type": "job_loss", "label": label, **extra}]
    return st
sa, sb = sem_state("loss A"), sem_state("loss B", id="different-id", semantic_value="different")
ra = run_pressure_flow_cycle(sa, assign_channels=False, compute_pressure=False, apply_gating=False)
rb = run_pressure_flow_cycle(sb, assign_channels=False, compute_pressure=False, apply_gating=False)
out["event_semantics"] = {"same_charge_ledger": ra["charge_ledger"] == rb["charge_ledger"], "same_trace_delta": ra["trace_delta"] == rb["trace_delta"], "same_memory": sa.pressure_flow_memory == sb.pressure_flow_memory, "history_event_context_a": sa.pressure_flow_history[-1].get("event_context"), "history_event_context_b": sb.pressure_flow_history[-1].get("event_context")}

print(json.dumps(out, indent=2, sort_keys=True))
