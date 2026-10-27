"""RX04 independent read-only source probes. No source or production writes."""
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

from v3.core.config_loader import get_core_step_ids, get_step_list, load_step_order, load_v3config
from v3.core.derived import compute_all_derived
from v3.core.invariants import backbone_hash
from v3.core.state import BackboneState, MetabolizationProcess
from v3.engine.effects.metabolization_effects import (
    create_rupture_shard_from_event, is_malheur, maybe_inject_rupture_at_band_age,
    update_metabolization_and_plasticity_step,
)
from v3.engine.run_llm_band import run_llm_band_year
from v3.engine.llm_contract import parse_candidate_packet_with_fallback
from v3.io.json_codec import state_to_dict
from v3.io.persona_sheet import build_persona_sheet
from v3.render.phenomenology import render_year

CONFIG = load_v3config()
ORDER = load_step_order()

def fw_hash(s): return backbone_hash(s)

def valid_packet() -> dict:
    return {
        "year": 2024, "age": 8,
        "event_candidates": [{
            "id": "rx04_practice_event", "kind": "practice",
            "label": "A supported workshop", "logline": "attends a workshop",
            "intensity": "minor", "channels": ["school"],
            "implicated": {"domains": ["nation_state"], "strata_levels": [7], "positions": []},
            "magnets": {"offers": ["meaning"], "costs": []},
            "hooks": {"wound_hooks": [], "capacity_hooks": []},
            "preconditions": [], "plausibility_notes": {"why_now": "fixture", "what_makes_it_unlikely": ""},
        }],
        "magnet_candidates": [], "branch_hypotheses": [],
    }

def valid_render() -> dict:
    return {
        "narrative_snapshot": {
            "scene": "At the workshop table, a teacher held the tool steady while the child tried again.",
            "which_strata_fired": [], "which_frameworks_fired": [],
            "what_was_buffered": [], "what_scratched": [],
        },
        "dialogue_snippets": [],
        "consistency_check": {"did_not_resolve": True, "public_vs_private_register_obeyed": True, "latent_vs_expressed_aim_obeyed": True},
        "particularity": {
            "place_anchor": {"value": "the workshop on Mill Street"},
            "object_anchor": {"value": "a worn wooden plane"},
            "schedule_anchor": {"value": "Saturday morning before the bus"},
            "money_anchor": {"value": "two dollars for the bus"},
            "language_anchor": {"value": "the teacher's quiet 'again'"},
            "power_anchor": {"value": "who is allowed to touch the tools"},
            "body_anchor": {"value": "sawdust on the knuckles"},
            "social_risk_anchor": {"value": "being seen as clumsy"},
        },
        "jaggedness": [
            {"and": ["warmth", "cruelty"], "where": "the teacher praised and corrected in one breath"},
            {"and": ["loyalty", "betrayal"], "where": "a peer shared the tool then took it back"},
        ],
        "micro_causality": [{"detail": "the tool slipped", "caused": "the room went quiet"}],
        "person_stubs": [],
    }

def fake_band(state, packet=None, raw_override=None, render_override=None, raise_on_pass2=False):
    calls = []
    def cb(stage, prompt):
        calls.append(stage)
        if "pass1" in stage:
            if raw_override is not None:
                return raw_override
            return json.dumps(packet or valid_packet())
        if raise_on_pass2:
            raise RuntimeError("RX04 pass2 transport failure after state mutation")
        if render_override is not None:
            return render_override
        return json.dumps(valid_render())
    derived = compute_all_derived(state)
    before_events = copy.deepcopy(state.events_this_year)
    before_hash = fw_hash(state)
    before_practice = {k: getattr(state.practice_stack, k) for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")}
    result = run_llm_band_year(state, derived, CONFIG, identity_override={}, llm_callback=cb)
    after_events = copy.deepcopy(state.events_this_year)
    after_practice = {k: getattr(state.practice_stack, k) for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")}
    return {
        "calls": calls,
        "events_before": before_events,
        "events_after": after_events,
        "events_unchanged": before_events == after_events,
        "backbone_hash_before": before_hash,
        "backbone_hash_after": fw_hash(state),
        "backbone_changed": before_hash != fw_hash(state),
        "practice_before": before_practice,
        "practice_after": after_practice,
        "llm_band": copy.deepcopy((state.yearly_integrity or {}).get("llm_band")),
        "selected_event_ids": list((state.yearly_integrity or {}).get("llm_band", {}).get("selected_event_ids", []) or []),
    }

out: dict = {}
out["scheduler"] = {
    "core_count": len(get_core_step_ids(ORDER)),
    "step_count": len(get_step_list(ORDER)),
    "core": get_core_step_ids(ORDER),
    "steps": [x.get("id") for x in get_step_list(ORDER)],
}

st = BackboneState(year=2024, age=8)
st.registers.inner_load = 10.0
before = {"inner_load": st.registers.inner_load, "metabolic_style": copy.deepcopy(st.metabolic_style)}
d = compute_all_derived(st)
out["derived_writes"] = {
    "before": before,
    "after": {"inner_load": st.registers.inner_load, "metabolic_style": copy.deepcopy(st.metabolic_style)},
}

out["band_normal"] = fake_band(BackboneState(year=2024, age=8))
out["band_empty_response"] = fake_band(BackboneState(year=2024, age=8), raw_override="")
out["band_parse_failure"] = fake_band(BackboneState(year=2024, age=8), raw_override="not json")
empty_packet = {"year": 2024, "age": 8, "event_candidates": [], "magnet_candidates": [], "branch_hypotheses": []}
out["band_empty_packet"] = fake_band(BackboneState(year=2024, age=8), packet=empty_packet)
out["band_pass2_failure_after_mutation"] = fake_band(BackboneState(year=2024, age=8), raise_on_pass2=True)

# Rendered output -> narration_support -> psychological capacity, the X03/X05 overlap.
def metab_feedback(scene: str) -> dict:
    s = BackboneState(year=2020, age=14)
    s.metabolization_processes = [MetabolizationProcess(
        id="mp_rx04", status="raw", cluster="sensitivity_exposure",
        mode="accommodation", severity="major", plasticity_years_left=1,
        intrusive_return_rate=60, intrusive_return_rate_prev=50,
    )]
    s.rendered_output = {"narrative_snapshot": {"scene": scene}}
    update_metabolization_and_plasticity_step(s, compute_all_derived(s), CONFIG)
    return {
        "narration_support": (
            {"availability": s.narration_support.availability,
             "accuracy": s.narration_support.accuracy,
             "warmth": s.narration_support.warmth,
             "coercion": s.narration_support.coercion}
            if s.narration_support else None
        ),
        "psych": {k: getattr(s.psychological_capacity, k) for k in ("vitality", "aperture", "coherence", "binding", "transmutation")},
    }
out["rendered_output_feedback"] = {
    "neutral": metab_feedback("A year passed."),
    "warm": metab_feedback("A parent held them and said I love you with care and support."),
    "coercive": metab_feedback("You must obey. Punishment, control and force."),
}

st = BackboneState(year=2000, age=3)
st.rendered_output = {"narrative_snapshot": {"scene": "Age 3: health declined."}}
d = compute_all_derived(st)
snap = state_to_dict(st)
sheet = build_persona_sheet(st, d, identity_override={"country": "US"}, trajectory_snapshots=[snap])
out["annotation_as_memory"] = {
    "backstory_contains_annotation": "Age 3: health declined." in (sheet.get("backstory") or ""),
    "backstory_excerpt": (sheet.get("backstory") or "")[-500:],
}
st.rendered_output = {"narrative_snapshot": {"scene": "[Structural year: no LLM scene rendered]"}}
d = compute_all_derived(st)
sheet = build_persona_sheet(st, d, identity_override={"country": "US"}, trajectory_snapshots=[state_to_dict(st)])
out["marker_as_most_recent"] = {
    "backstory_contains_marker": "[Structural year" in (sheet.get("backstory") or ""),
    "backstory_excerpt": (sheet.get("backstory") or "")[-500:],
}

st = BackboneState(year=2020, age=14)
ev = {"kind": "epistemic_rupture", "intensity": "malheur", "label": "R", "rupture": {"opacity": "high", "prediction_error": "high", "violated_assumption": "Caregivers return"}, "implicated": {"domains": ["family_household"]}}
sh = create_rupture_shard_from_event(st, ev)
proc = st.metabolization_processes[0]
out["rupture_severity"] = {
    "shard_status": sh.current_status,
    "process_severity": proc.severity,
    "process_status": proc.status,
    "is_malheur_with_process_severity": is_malheur(proc.severity, narration_availability=50),
}

st = BackboneState(year=2020, age=3)
st.events_this_year = []
random.seed(1)
maybe_inject_rupture_at_band_age(st)
out["age_injection_seed1_age3"] = {
    "shard_count": len(st.rupture_shards),
    "process_count": len(st.metabolization_processes),
    "events_this_year": st.events_this_year,
    "shard": ({k: getattr(st.rupture_shards[0], k) for k in ("year", "age", "current_status", "domain", "violated_assumption")} if st.rupture_shards else None),
    "wound": {k: getattr(st.wound_vector, k) for k in ("abandonment", "fear", "shame")},
    "process": ({k: getattr(st.metabolization_processes[0], k) for k in ("severity", "status", "mode", "plasticity_years_left")} if st.metabolization_processes else None),
}

# Render direct nonmutation.
st = BackboneState(year=2024, age=8)
d = compute_all_derived(st)
h0 = fw_hash(st)
render_year(st, d, CONFIG)
out["render_direct_nonmutation"] = {"hash_before": h0, "hash_after": fw_hash(st), "unchanged": h0 == fw_hash(st)}

print(json.dumps(out, indent=2, sort_keys=True, default=str))
