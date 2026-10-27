"""X03 sourcefree read-only probe. No source or production writes."""
from __future__ import annotations
import copy, json, os, random, subprocess, sys, types
from pathlib import Path

SOURCE = Path(os.environ["RAWLSING_STAGING_ROOT"])
if str(SOURCE) not in sys.path:
    sys.path.insert(0, str(SOURCE))

_RUBY = "require 'yaml'; require 'json'; print JSON.generate(YAML.safe_load(STDIN.read, [], [], true))"
def _conv(obj):
    if isinstance(obj, dict):
        return {(int(k) if isinstance(k, str) and k.isdigit() else k): _conv(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_conv(v) for v in obj]
    return obj
def safe_load(value):
    if hasattr(value, "read"):
        value = value.read()
    p = subprocess.run(["ruby", "-e", _RUBY], input=value, capture_output=True, text=True)
    if p.returncode != 0:
        raise ValueError("YAML_PARSE_FAILED: " + p.stderr.strip()[:300])
    return _conv(json.loads(p.stdout))
_m = sys.modules.get("yaml") or types.ModuleType("yaml")
_m.safe_load = safe_load
sys.modules["yaml"] = _m

from v3.core.config_loader import load_step_order, load_v3config
from v3.core.derived import compute_all_derived
from v3.core.invariants import ensure_min_cracks, ensure_min_frameworks
from v3.core.state import BackboneState, Crack, Framework, MetabolizationProcess, NarrationSupport, StrivingObject
from v3.engine.effects.metabolization_effects import (
    _analyze_narrative_for_support_quality,
    create_rupture_shard_from_event,
    is_malheur,
    maybe_inject_rupture_at_band_age,
    update_metabolization_and_plasticity_step,
    update_wound_vector_from_rupture,
)
from v3.engine.striving_objects import spawn_striving_objects_for_age, update_existing_objects, update_striving_step
from v3.io.identity_to_backbone import backbone_state_from_identity
from v3.io.seed_frameworks import seed_cracks_from_identity, seed_frameworks_from_identity
from v3.systems.boundary import update_solidarity_boundary
from v3.systems.cracks import update_cracks
from v3.systems.domains import update_domains
from v3.systems.frameworks import enforce_framework_caps, update_framework_weights
from v3.systems.practices import update_practice_stack
from v3.systems.stability_inertia import stability_inertia_dissipation
from v3.systems.topology import update_loop_topology

CONFIG = load_v3config()
STEP_ORDER = load_step_order()

def fw(f: Framework) -> dict:
    return {
        "id": f.id, "weight": round(f.weight, 3), "tenure_years": f.tenure_years,
        "half_life_years": f.half_life_years,
        "phase": "chronic" if f.half_life_years > 0 and f.tenure_years >= f.half_life_years else "acute",
        "failure_mode": f.failure_mode, "enemy_requirement": f.enemy_requirement,
        "institutional_affinities": list(f.institutional_affinities),
        "acute_delta": dict(f.acute_delta), "chronic_delta": dict(f.chronic_delta),
    }

def crack(c: Crack) -> dict:
    return {"type": c.type, "intensity": round(c.intensity, 3), "latent_pressure": round(c.latent_pressure, 3), "active": c.active, "origin_year": c.origin_year}

def proc(p: MetabolizationProcess) -> dict:
    return {
        "id": p.id, "severity": p.severity, "mode": p.mode, "status": p.status, "cluster": p.cluster,
        "plasticity_years_left": p.plasticity_years_left,
        "intrusive_return_rate": p.intrusive_return_rate, "intrusive_return_rate_prev": p.intrusive_return_rate_prev,
        "narrators": list(p.narrators), "provisional_frame": p.provisional_frame,
        "downstream_biases": dict(p.downstream_biases), "sealed_candidate_years": p.sealed_candidate_years,
        "post_plasticity_years": p.post_plasticity_years, "reactivation_triggers": list(p.reactivation_triggers),
    }

def shard(s) -> dict:
    return {"id": s.id, "current_status": s.current_status, "severity_does_not_exist": True, "intrusive_return_rate": s.intrusive_return_rate, "meaning_attempts": list(s.meaning_attempts), "domain": s.domain, "violated_assumption": s.violated_assumption}

def strive(s: StrivingObject) -> dict:
    return {"id": s.id, "label": s.label, "need_axis": s.need_axis, "started_age": s.started_age, "investment": s.investment, "identity_load": s.identity_load, "feasibility_belief": s.feasibility_belief, "social_support": s.social_support, "recent_momentum": s.recent_momentum, "active": s.active}

CHILD = {
    "given_name": "Child", "class_origin": "working", "current_class": "working",
    "ses_band": "working", "minority_status": "minoritized", "religiosity_level": 80,
    "religion": "Islam", "urbanicity": "city", "region": "Test",
}
ADULT = {
    "given_name": "Adult", "class_origin": "middle", "current_class": "middle",
    "ses_band": "middle", "minority_status": "dominant", "religiosity_level": 50,
    "religion": "None", "urbanicity": "city", "region": "Test",
}

out: dict = {}

# --- M09 cracks ---
st = BackboneState(year=2000, age=30)
ensure_min_cracks(st, CONFIG)
out["cracks"] = {
    "default_ensure_min": {
        "count": len(st.cracks), "cracks": [crack(c) for c in st.cracks],
        "placeholder_counts": st.yearly_integrity.get("placeholder_counts"),
        "placeholder_repair": st.yearly_integrity.get("placeholder_repair"),
    },
    "child_seed": [crack(c) for c in seed_cracks_from_identity(CHILD, year=2000, age=8)],
    "adult_seed": [crack(c) for c in seed_cracks_from_identity(ADULT, year=2000, age=40)],
}
st = BackboneState(year=2000, age=30)
st.cracks = [Crack(type="latent_test", intensity=80.0, latent_pressure=70.0, active=False, origin_year=1990)]
update_cracks(st, compute_all_derived(st), CONFIG)
out["cracks"]["no_event_update_record"] = crack(st.cracks[0])
st.cracks = [Crack(type="test", intensity=10.0, latent_pressure=5.0, active=True, origin_year=1990)]
st.events_this_year = [{"crack_deltas": [{"intensity": 10.0, "latent_pressure": 10.0}]}]
update_cracks(st, compute_all_derived(st), CONFIG)
out["cracks"]["event_delta_update_record"] = crack(st.cracks[0])
out["cracks"]["config_rules_declared"] = CONFIG.get("cracks_rules")

# --- M11 frameworks ---
child_fw = seed_frameworks_from_identity(CHILD, year=2000, age=8)
adult_fw = seed_frameworks_from_identity(ADULT, year=2000, age=40)
st = BackboneState(year=2000, age=40)
st.frameworks = copy.deepcopy(adult_fw)
before = {k: round(getattr(st.psychological_capacity, k), 6) for k in ("vitality", "aperture", "coherence", "binding", "transmutation")}
st.events_this_year = []
update_framework_weights(st, compute_all_derived(st), CONFIG)
after = {k: round(getattr(st.psychological_capacity, k), 6) for k in ("vitality", "aperture", "coherence", "binding", "transmutation")}
out["frameworks"] = {
    "child_seed": [fw(f) for f in child_fw],
    "adult_seed": [fw(f) for f in adult_fw],
    "adult_operator_empty_event_year": {
        "before_psych": before, "after_psych": after,
        "frameworks_after": [fw(f) for f in st.frameworks],
    },
}

# explicit acute -> chronic switch on a synthetic framework
st = BackboneState(year=2000, age=30)
st.frameworks = [Framework(id="switch", weight=100.0, half_life_years=2, tenure_years=0, acute_delta={"binding": 5.0}, chronic_delta={"binding": -5.0})]
switch = []
for i in range(3):
    update_framework_weights(st, compute_all_derived(st), CONFIG)
    switch.append({"after_year": i + 1, "tenure_years": st.frameworks[0].tenure_years, "binding": round(st.psychological_capacity.binding, 6)})
out["frameworks"]["synthetic_acute_then_chronic"] = switch

st = BackboneState(year=2000, age=40)
st.frameworks = [Framework(id="fragile", weight=4.0), Framework(id="stable", weight=20.0)]
enforce_framework_caps(st)
out["frameworks"]["dormancy_after_weight4"] = {
    "active": [fw(f) for f in st.frameworks],
    "dormant": list(st.frameworks_dormant),
}

# --- M13 practices ---
child_ps = backbone_state_from_identity(CHILD, year=2000, age=8)
adult_ps = backbone_state_from_identity(ADULT, year=2000, age=40)
out["practices"] = {
    "child_seed": {k: round(getattr(child_ps.practice_stack, k), 3) for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")},
    "adult_seed": {k: round(getattr(adult_ps.practice_stack, k), 3) for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")},
}
st = BackboneState(year=2000, age=30)
st.practice_stack.organizing = 40.0
st.practice_stack.craft = 50.0
st.events_this_year = []
update_practice_stack(st, compute_all_derived(st), CONFIG)
out["practices"]["empty_event_year"] = {"organizing": st.practice_stack.organizing, "craft": st.practice_stack.craft}
st.events_this_year = [{"practice_deltas": {"organizing": 10.0, "craft": -5.0}}]
update_practice_stack(st, compute_all_derived(st), CONFIG)
out["practices"]["event_delta_year"] = {"organizing": st.practice_stack.organizing, "craft": st.practice_stack.craft}

# domains step ignores frameworks/practices (same events, different carriers)
def build_domain_probe(fw_weight: float, practice_val: float) -> dict:
    s = BackboneState(year=2000, age=30)
    s.frameworks = [Framework(id="f", weight=fw_weight, acute_delta={"coherence": 6}, chronic_delta={"coherence": -6})]
    s.practice_stack.organizing = practice_val
    s.domains["empire_occupation"].A = 20.0
    s.events_this_year = [{"domain_deltas": {"empire_occupation": {"A": 8.0, "V": 5.0}}}]
    update_domains(s, compute_all_derived(s), CONFIG)
    d = s.domains["empire_occupation"]
    return {"A": d.A, "S": d.S, "V": d.V, "Aim": d.Aim, "latent_aim": d.latent_aim, "expressed_aim": d.expressed_aim}
out["domains_ignore_frameworks_practices"] = {
    "low_framework_low_practice": build_domain_probe(5.0, 5.0),
    "high_framework_high_practice": build_domain_probe(95.0, 95.0),
}

# --- M14 topology/boundary ---
st = BackboneState(year=2000, age=30)
st.collective_infrastructure.network_density = 60.0
st.practice_stack.organizing = 60.0
st.peak_routing.solidarity_boundary = "in_group"
st.peak_routing.loop_topology = "self_contained"
d = compute_all_derived(st)
topo = []
for year in range(2):
    update_loop_topology(st, d, CONFIG)
    topo.append({"after_call": year + 1, "loop": st.peak_routing.loop_topology, "counters": dict(st.peak_routing.topology_hysteresis_years)})
st.peak_routing.solidarity_boundary = "universal"
st.collective_infrastructure.repression_pressure = 0.0
st.events_this_year = [{"solidarity_boundary": "none"}]
d = compute_all_derived(st)
update_solidarity_boundary(st, d, CONFIG)
boundary_blocked = st.peak_routing.solidarity_boundary
st.collective_infrastructure.repression_pressure = 75.0
d = compute_all_derived(st)
update_solidarity_boundary(st, d, CONFIG)
boundary_allowed = st.peak_routing.solidarity_boundary
out["topology_boundary"] = {
    "topology_calls": topo,
    "boundary_reversal_blocked_without_condition": boundary_blocked,
    "boundary_reversal_allowed_repression75": boundary_allowed,
    "config_hysteresis": CONFIG.get("hysteresis"),
}

# --- M16 strivings ---
striving_runs = []
for i in range(5):
    s = BackboneState(year=2000, age=14)
    s.expectation_baseline = {ax: "hopeful" for ax in ("attachment", "safety", "belonging", "status", "competence", "autonomy", "meaning", "justice", "beauty_play", "eros_intimacy")}
    update_striving_step(s, compute_all_derived(s), CONFIG)
    striving_runs.append([strive(x) for x in s.striving_objects])
s = BackboneState(year=2000, age=14)
s.expectation_baseline = {}
update_striving_step(s, compute_all_derived(s), CONFIG)
seeded_spawn = spawn_striving_objects_for_age(
    14, {ax: "hopeful" for ax in ("attachment", "safety", "belonging", "status", "competence", "autonomy", "meaning", "justice", "beauty_play", "eros_intimacy")}, [], set(), 2000,
    max_new=2, use_budget_by_age=True, use_weighted_axis=True, rng=random.Random(7),
)
out["striving"] = {
    "config": CONFIG.get("striving"),
    "five_unseeded_update_striving_step_runs": striving_runs,
    "seeded_spawn_rng7": [strive(x) for x in seeded_spawn],
    "missing_baseline_axes_after_step": sorted(s.expectation_baseline.items()),
}
st = BackboneState(year=2000, age=40)
st.striving_objects = [StrivingObject(id="s1", investment=10, identity_load=20, feasibility_belief=10, social_support=10, recent_momentum=0)]
update_existing_objects(st, CONFIG, rng=random.Random(0))
out["striving"]["retire_example_seed0"] = [strive(x) for x in st.striving_objects]
retire_scan = []
for seed in range(6):
    s = BackboneState(year=2000, age=40)
    s.striving_objects = [StrivingObject(id="s1", investment=10, identity_load=20, feasibility_belief=10, social_support=10, recent_momentum=0)]
    update_existing_objects(s, CONFIG, rng=random.Random(seed))
    retire_scan.append({"seed": seed, "remaining": [strive(x) for x in s.striving_objects]})
out["striving"]["retire_seed_scan"] = retire_scan

# --- M18 rupture creation + M19 process ---
st = BackboneState(year=2020, age=14)
st.narration_support = NarrationSupport(availability=50, accuracy=50, warmth=50, coercion=50)
wound_before = {k: getattr(st.wound_vector, k) for k in ("abandonment", "fear", "shame", "loss")}
ev = {
    "kind": "epistemic_rupture", "id": "ev_malheur", "label": "Rupture",
    "intensity": "malheur",
    "rupture": {"violated_assumption": "Caregivers return", "opacity": "high", "prediction_error": "high"},
    "implicated": {"domains": ["family_household"]},
}
sh = create_rupture_shard_from_event(st, ev)
p0 = st.metabolization_processes[0]
creation_shard = shard(sh)
creation_process = proc(p0)
wound_after_create = {k: getattr(st.wound_vector, k) for k in ("abandonment", "fear", "shame", "loss")}
is_malheur_at_update = is_malheur(p0.severity, narration_availability=50)
update_wound_vector_from_rupture(st, "malheur", "family_household", "high")
wound_after_direct_malheur = {k: getattr(st.wound_vector, k) for k in ("abandonment", "fear", "shame", "loss")}
transitions = []
for i in range(3):
    update_metabolization_and_plasticity_step(st, compute_all_derived(st), CONFIG)
    transitions.append({"year": i + 1, "status": p0.status, "plasticity_years_left": p0.plasticity_years_left, "narrators": list(p0.narrators), "irr": p0.intrusive_return_rate, "irr_prev": p0.intrusive_return_rate_prev, "downstream_biases": dict(p0.downstream_biases), "narration_support": {"availability": st.narration_support.availability, "accuracy": st.narration_support.accuracy, "warmth": st.narration_support.warmth, "coercion": st.narration_support.coercion}})
out["rupture_metabolization"] = {
    "shard": creation_shard,
    "process_at_creation": creation_process,
    "is_malheur_with_process_severity_at_yearly_update": is_malheur_at_update,
    "wound_before": wound_before,
    "wound_after_create_only": wound_after_create,
    "wound_after_direct_malheur_update": wound_after_direct_malheur,
    "three_update_years": transitions,
    "status_enum": __import__("v3.core.state", fromlist=["METABOLIZATION_STATUS"]).METABOLIZATION_STATUS,
}
# two ruptures overwrite plasticity window
st2 = BackboneState(year=2020, age=14)
ev_high = {"kind": "epistemic_rupture", "intensity": "major", "rupture": {"opacity": "high", "prediction_error": "high"}, "implicated": {"domains": ["sect_class"]}, "label": "A"}
ev_low = {"kind": "epistemic_rupture", "intensity": "minor", "rupture": {"opacity": "low", "prediction_error": "low"}, "implicated": {"domains": ["nation"]}, "label": "B"}
create_rupture_shard_from_event(st2, ev_high)
first_window = dict(st2.plasticity_window)
create_rupture_shard_from_event(st2, ev_low)
out["rupture_metabolization"]["second_rupture_overwrites_window"] = {"first": first_window, "after_second": dict(st2.plasticity_window), "processes": [proc(p) for p in st2.metabolization_processes]}

# maybe_inject age-band behavior
inj = []
for seed in range(20):
    s = BackboneState(year=2020, age=14)
    random.seed(seed)
    maybe_inject_rupture_at_band_age(s)
    if s.metabolization_processes:
        p = s.metabolization_processes[0]
        inj.append({"seed": seed, "shard_status": s.rupture_shards[0].current_status, "process_severity": p.severity, "process_status": p.status, "process_mode": p.mode, "wound": {k: getattr(s.wound_vector, k) for k in ("abandonment", "fear", "shame", "loss")}})
out["rupture_metabolization"]["maybe_inject_age14_seeds0to19"] = {"injected_count": len(inj), "injected": inj}

# --- stability inertia ---
st = BackboneState(year=2020, age=14)
st.metabolization_processes = [MetabolizationProcess(id="mp", status="raw", intrusive_return_rate=50, intrusive_return_rate_prev=50)]
st.stability_threshold_inertia = 20.0
st.narration_support = NarrationSupport(availability=80, accuracy=80, warmth=80, coercion=10)
d = compute_all_derived(st)
stability_inertia_dissipation(st, d, CONFIG)
raw_drain = st.stability_threshold_inertia
st2 = copy.deepcopy(st)
st2.stability_threshold_inertia = 20.0
st2.metabolization_processes[0].status = "integrated"
stability_inertia_dissipation(st2, compute_all_derived(st2), CONFIG)
out["stability_inertia"] = {
    "raw_process_inertia_20_after": raw_drain,
    "manually_integrated_inertia_20_after": st2.stability_threshold_inertia,
    "source_generated_statuses": [p.status for p in st.metabolization_processes],
}

# --- narrative text -> NarrationSupport -> capacity ---
texts = {
    "neutral": "A year passed.",
    "warm": "A parent held them and said I love you. Care, support, comfort and understanding.",
    "coercive": "You must obey. Punishment, control, force and discipline.",
}
scores = {k: _analyze_narrative_for_support_quality({"narrative_snapshot": {"scene": v}}) for k, v in texts.items()}
def metab_with_rendered(scene: str) -> dict:
    s = BackboneState(year=2020, age=14)
    s.metabolization_processes = [MetabolizationProcess(id="mp", status="raw", cluster="sensitivity_exposure", mode="accommodation", severity="major", plasticity_years_left=2)]
    s.rendered_output = {"narrative_snapshot": {"scene": scene}}
    update_metabolization_and_plasticity_step(s, compute_all_derived(s), CONFIG)
    return {"narration_support": {"availability": s.narration_support.availability, "accuracy": s.narration_support.accuracy, "warmth": s.narration_support.warmth, "coercion": s.narration_support.coercion}, "psych": {k: round(getattr(s.psychological_capacity, k), 6) for k in ("vitality", "aperture", "coherence", "binding", "transmutation")}}
out["narrative_support"] = {"scores": scores, "neutral_metab": metab_with_rendered(texts["neutral"]), "warm_metab": metab_with_rendered(texts["warm"]), "coercive_metab": metab_with_rendered(texts["coercive"])}

print(json.dumps(out, indent=2, sort_keys=True))
