# v3/engine/llm_contract.py
# Two-pass LLM contract: Pass 1 CandidatePacket (LLM → candidates), Pass 2 RenderPacket → RenderOutput.
# Schemas and parsers per specLLM.txt; prompt builders in prompts.py.
# No LLM calls here; code only defines shapes and parses/truncates.

from __future__ import annotations

import json
import re
from typing import Any

from v3.core.derived import DerivedIndices
from v3.core.enums import DOMAIN_NAMES, domain_axis_to_label
from v3.core.state import BackboneState

_RENDER_PACKET_ALLOWED_ROOT_FIELDS = {
    "schema_version",
    "export_rule",
    "domains",
    "dominant_recent_channels",
}
_RENDER_PACKET_ALLOWED_DOMAIN_FIELDS = {
    "felt_register",
    "ordinary_attribution",
    "attribution_confidence",
    "vessel_hint",
    "vessel_status",
    "insulation_mode",
    "cognitive_shelter",
    "insulation_confidence",
    "insulation_status",
    "avoidance_or_deflection",
    "public_private_inner_posture",
    "historical_relation",
    "dominant_channel",
    "charge_band",
    "overt_aim_band",
    "internally_routed_band",
    "charge_relation_to_prior_history",
    "age_phase",
    "vitality_band",
    "fatigue_band",
    "future_horizon",
    "routing_bias",
}

# --- Hard caps (specLLM) ---
EVENT_CANDIDATES_MAX = 6
MAGNET_CANDIDATES_MAX = 4
BRANCH_HYPOTHESES_MAX = 3

# --- Pass 1: CandidatePacket (LLM → code) ---
# Event candidate kind and intensity enums (for validation/truncation).
EVENT_KINDS = frozenset({
    "relationship", "institution", "puncture", "opportunity", "practice",
    "loss", "achievement", "humiliation", "move", "health", "violence", "media",
    "epistemic_rupture", "expectation_event",
})
INTENSITIES = frozenset({"minor", "major", "shock"})
CHANNELS = frozenset({
    "family", "peer", "school", "work", "sect", "state", "media",
    "online", "movement", "neighborhood", "diaspora",
})
MAGNET_TYPES = frozenset({
    "friend", "mentor", "romance", "leader", "teacher", "boss",
    "institution", "scene", "online_cluster",
})
TRAJECTORY_BRANCHES = frozenset({
    "ethical_rebellion", "nihilist_drift", "straight_and_narrow", "conversion",
    "career_track", "organizing", "romance_fixation", "withdrawal",
})
OFFERS = frozenset({
    "belonging", "status", "agency", "escape", "meaning", "care", "curiosity",
})
COSTS = frozenset({
    "binding", "coherence", "reality_anchor", "safety", "reputation", "money", "time",
})
WOUND_HOOKS = frozenset({
    "shame", "fear", "anger", "abandonment", "control", "recognition", "loss",
})
CAPACITY_HOOKS = frozenset({
    "vitality", "aperture", "binding", "coherence", "agency",
    "reality_anchor", "transmutation",
})


def parse_candidate_packet(raw: str | dict[str, Any]) -> dict[str, Any]:
    """
    Parse Pass 1 LLM output into CandidatePacket. Truncates to caps; strips unknown keys.
    Raises ValueError on invalid JSON or missing required structure.
    Handles markdown code fences (```json ... ```) that some models return despite instructions.
    """
    if isinstance(raw, str):
        cleaned = _extract_json_from_raw(raw)
        try:
            obj = json.loads(cleaned)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for CandidatePacket: {e}") from e
    else:
        obj = dict(raw)

    if not isinstance(obj, dict):
        raise ValueError("CandidatePacket must be a JSON object")

    # Unwrap envelope: some models return {"CandidatePacket": {...}} instead of the object directly.
    # Also handle {"candidate_packet": {...}}, {"data": {...}}, etc.
    for _envelope_key in ("CandidatePacket", "candidate_packet", "data", "result", "output"):
        if _envelope_key in obj and isinstance(obj[_envelope_key], dict) and "event_candidates" in obj[_envelope_key]:
            obj = obj[_envelope_key]
            break

    out: dict[str, Any] = {
        "year": int(obj.get("year", 0)),
        "age": int(obj.get("age", 0)),
        "event_candidates": [],
        "magnet_candidates": [],
        "branch_hypotheses": [],
    }

    # Event candidates: truncate to EVENT_CANDIDATES_MAX
    events = obj.get("event_candidates")
    if isinstance(events, list):
        for i, ev in enumerate(events):
            if i >= EVENT_CANDIDATES_MAX:
                break
            if not isinstance(ev, dict):
                continue
            e = _sanitize_event_candidate(ev)
            if e:
                out["event_candidates"].append(e)

    # Magnet candidates: truncate to MAGNET_CANDIDATES_MAX
    magnets = obj.get("magnet_candidates")
    if isinstance(magnets, list):
        for i, mg in enumerate(magnets):
            if i >= MAGNET_CANDIDATES_MAX:
                break
            if not isinstance(mg, dict):
                continue
            m = _sanitize_magnet_candidate(mg)
            if m:
                out["magnet_candidates"].append(m)

    # Branch hypotheses: truncate to BRANCH_HYPOTHESES_MAX
    branches = obj.get("branch_hypotheses")
    if isinstance(branches, list):
        for i, br in enumerate(branches):
            if i >= BRANCH_HYPOTHESES_MAX:
                break
            if not isinstance(br, dict):
                continue
            b = _sanitize_branch_hypothesis(br)
            if b:
                out["branch_hypotheses"].append(b)

    return out


def parse_candidate_packet_with_fallback(
    raw: str | dict[str, Any],
    year: int | None = None,
    age: int | None = None,
) -> dict[str, Any]:
    """
    Parse Pass 1 output and apply fallback if 0 events and 0 magnets (ml_pass1_fallback_packet).
    Use this in pipelines so deltas always run. Returns packet (with one minimal event if was empty).
    """
    packet = parse_candidate_packet(raw)
    fallback_candidate_packet_if_empty(packet, year=year, age=age)
    return packet


def make_fallback_event(year: int = 0, age: int = 0) -> dict[str, Any]:
    """Minimal event candidate for Pass 1 fallback when LLM returns 0 candidates. One minor practice/relationship so deltas still run."""
    return {
        "id": f"fallback_ev_{year}_{age}",
        "kind": "practice",
        "label": "Routine practice or relationship moment (fallback)",
        "logline": "",
        "intensity": "minor",
        "channels": [],
        "implicated": {"domains": [], "strata_levels": []},
        "magnets": {"offers": [], "costs": []},
        "hooks": {"wound_hooks": [], "capacity_hooks": []},
        "preconditions": [],
        "plausibility_notes": {"why_now": "Fallback when no candidates returned.", "what_makes_it_unlikely": ""},
    }


def fallback_candidate_packet_if_empty(packet: dict[str, Any], year: int | None = None, age: int | None = None) -> bool:
    """
    If packet has 0 event_candidates and 0 magnet_candidates, append one minimal event so select_candidates/deltas run.
    Mutates packet in place. Returns True if fallback was applied.
    """
    events = packet.get("event_candidates")
    magnets = packet.get("magnet_candidates")
    if not isinstance(events, list) or not isinstance(magnets, list):
        return False
    if len(events) > 0 or len(magnets) > 0:
        return False
    y = int(year if year is not None else packet.get("year", 0))
    a = int(age if age is not None else packet.get("age", 0))
    packet["event_candidates"] = [make_fallback_event(y, a)]
    packet["_integrity"] = {
        "status": "degraded",
        "fallback_used": True,
        "fallback_reason": "empty_candidate_packet",
        "reasons": ["empty_candidate_packet"],
        "surface": "candidate_packet",
    }
    return True


def _sanitize_event_candidate(ev: dict[str, Any]) -> dict[str, Any] | None:
    """Extract allowed keys; normalize kind/intensity/channels."""
    kind = (ev.get("kind") or "").strip().lower()
    if kind not in EVENT_KINDS:
        kind = "relationship"  # fallback
    intensity = (ev.get("intensity") or "minor").strip().lower()
    if intensity not in INTENSITIES:
        intensity = "minor"
    channels = ev.get("channels")
    if isinstance(channels, list):
        channels = [c for c in channels if isinstance(c, str) and c.strip().lower() in CHANNELS][:10]
    else:
        channels = []
    magnets = ev.get("magnets") or {}
    if isinstance(magnets, dict):
        offers = [x for x in magnets.get("offers") or [] if isinstance(x, str) and x.strip().lower() in OFFERS][:7]
        costs = [x for x in magnets.get("costs") or [] if isinstance(x, str) and x.strip().lower() in COSTS][:7]
        magnets = {"offers": offers, "costs": costs}
    hooks = ev.get("hooks") or {}
    if isinstance(hooks, dict):
        wound = [x for x in hooks.get("wound_hooks") or [] if isinstance(x, str) and x.strip().lower() in WOUND_HOOKS][:7]
        cap = [x for x in hooks.get("capacity_hooks") or [] if isinstance(x, str) and x.strip().lower() in CAPACITY_HOOKS][:7]
        hooks = {"wound_hooks": wound, "capacity_hooks": cap}
    implicated = ev.get("implicated") or {}
    if isinstance(implicated, dict):
        domains = [d for d in implicated.get("domains") or [] if isinstance(d, str)][:5]
        levels = [int(x) for x in implicated.get("strata_levels") or [] if isinstance(x, (int, float))][:8]
        positions = [str(p).strip() for p in (implicated.get("positions") or []) if isinstance(p, (str, int, float))][:15]
        implicated = {"domains": domains, "strata_levels": levels, "positions": positions}
    else:
        implicated = {"domains": [], "strata_levels": [], "positions": []}
    out: dict[str, Any] = {
        "id": str(ev.get("id", "")).strip() or f"ev_{hash(ev) % 10000}",
        "kind": kind,
        "label": str(ev.get("label", "")).strip()[:200],
        "logline": str(ev.get("logline", "")).strip()[:500],
        "intensity": intensity,
        "channels": channels,
        "implicated": implicated,
        "magnets": magnets,
        "hooks": hooks,
        "preconditions": _list_of_preconditions(ev.get("preconditions")),
        "plausibility_notes": _plausibility_notes(ev.get("plausibility_notes")),
    }
    if kind == "epistemic_rupture":
        r = ev.get("rupture")
        if isinstance(r, dict):
            out["rupture"] = {str(k): v for k, v in r.items() if k and v is not None}
    # Expectation-event targeting: fulfillment/violation + striving_object_id for Gift/Disruption shards
    ex_type = (ev.get("expectation_type") or "").strip().lower()
    if ex_type in ("fulfillment", "violation"):
        out["expectation_type"] = ex_type
    sid = (ev.get("striving_object_id") or "").strip()
    if sid:
        out["striving_object_id"] = sid[:80]
    return out


def _list_of_preconditions(val: Any) -> list[dict[str, str]]:
    out = []
    if isinstance(val, list):
        for p in val[:5]:
            if isinstance(p, dict) and "if" in p and "then" in p:
                out.append({"if": str(p["if"])[:300], "then": str(p["then"])[:300]})
    return out


def _plausibility_notes(val: Any) -> dict[str, str]:
    if not isinstance(val, dict):
        return {}
    return {
        "why_now": str(val.get("why_now", ""))[:400],
        "what_makes_it_unlikely": str(val.get("what_makes_it_unlikely", ""))[:400],
    }


def _sanitize_magnet_candidate(mg: dict[str, Any]) -> dict[str, Any] | None:
    magnet_type = (mg.get("magnet_type") or "friend").strip().lower()
    if magnet_type not in MAGNET_TYPES:
        magnet_type = "friend"
    _raw_stickiness = mg.get("stickiness") or "medium"
    # LLM sometimes returns stickiness as a number (0-100); convert to low/medium/high
    if isinstance(_raw_stickiness, (int, float)):
        stickiness = "high" if _raw_stickiness >= 66 else "low" if _raw_stickiness < 33 else "medium"
    else:
        stickiness = str(_raw_stickiness).strip().lower()
    if stickiness not in {"low", "medium", "high"}:
        stickiness = "medium"
    offers = [x for x in mg.get("offers") or [] if isinstance(x, str) and x.strip().lower() in OFFERS][:7]
    costs = [x for x in mg.get("costs") or [] if isinstance(x, str) and x.strip().lower() in COSTS][:7]
    compatibility = mg.get("compatibility") or {}
    if isinstance(compatibility, dict):
        compatibility = {
            "attractors": [str(x) for x in (compatibility.get("attractors") or []) if x][:5],
            "repulsors": [str(x) for x in (compatibility.get("repulsors") or []) if x][:5],
        }
    trajectory_branches = []
    for tb in (mg.get("trajectory_branches") or [])[:5]:
        if isinstance(tb, dict) and tb.get("branch_id") and tb.get("label"):
            label = str(tb.get("label", "")).strip().lower()
            if label in TRAJECTORY_BRANCHES:
                trajectory_branches.append({
                    "branch_id": str(tb["branch_id"]),
                    "label": label,
                    "when": str(tb.get("when", ""))[:200],
                    "notes": str(tb.get("notes", ""))[:300],
                })
    implicated = mg.get("implicated") or {}
    if isinstance(implicated, dict):
        implicated = {
            "domains": [d for d in implicated.get("domains") or [] if isinstance(d, str)][:5],
            "strata_levels": [int(x) for x in implicated.get("strata_levels") or [] if isinstance(x, (int, float))][:8],
        }
    return {
        "id": str(mg.get("id", "")).strip() or f"mg_{hash(mg) % 10000}",
        "magnet_type": magnet_type,
        "label": str(mg.get("label", "")).strip()[:200],
        "who": str(mg.get("who", "")).strip()[:200],
        "entry_point": str(mg.get("entry_point", "")).strip()[:300],
        "stickiness": stickiness,
        "offers": offers,
        "costs": costs,
        "compatibility": compatibility,
        "trajectory_branches": trajectory_branches,
        "implicated": implicated,
    }


def _sanitize_branch_hypothesis(br: dict[str, Any]) -> dict[str, Any] | None:
    if not br.get("id") or not br.get("fork"):
        return None
    return {
        "id": str(br["id"]).strip(),
        "fork": str(br["fork"])[:300],
        "if_path_A": str(br.get("if_path_A", ""))[:300],
        "if_path_B": str(br.get("if_path_B", ""))[:300],
        "state_sensitivity": str(br.get("state_sensitivity", ""))[:200],
    }


# --- Pass 2: RenderPacket (code → LLM), RenderOutput (LLM → code) ---

def _extract_json_from_raw(raw: str) -> str:
    """Strip markdown code fences so we can parse JSON when the LLM wraps it in ```json ... ```."""
    s = raw.strip()
    if s.startswith("```"):
        # Find first newline after opening fence, then closing fence
        first = s.find("\n")
        if first != -1:
            s = s[first + 1 :]
        if s.endswith("```"):
            s = s[: -3].strip()
        elif "```" in s:
            s = s.split("```")[0].strip()
    return s


def parse_render_output(raw: str | dict[str, Any]) -> dict[str, Any]:
    """
    Parse Pass 2 LLM output into RenderOutput. Strips unknown keys.
    Tolerates JSON wrapped in markdown code fences. Raises ValueError on invalid JSON.
    """
    if isinstance(raw, str):
        to_parse = _extract_json_from_raw(raw)
        try:
            obj = json.loads(to_parse)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON for RenderOutput: {e}") from e
    else:
        obj = dict(raw)

    if not isinstance(obj, dict):
        raise ValueError("RenderOutput must be a JSON object")

    narrative = obj.get("narrative_snapshot") or {}
    # Normalize: LLM sometimes returns narrative_snapshot as a plain string
    if isinstance(narrative, str):
        narrative = {"scene": narrative}
    scene_fallback_used = False
    if isinstance(narrative, dict):
        raw_strata = narrative.get("which_strata_fired") or []
        raw_fw = narrative.get("which_frameworks_fired") or []
        raw_buf = narrative.get("what_was_buffered") or []
        raw_scr = narrative.get("what_scratched") or []
        scene_val = narrative.get("scene")
        scene = ("" if scene_val is None else str(scene_val))[:5000].strip()
        if not scene and isinstance(raw, str):
            m = re.search(r'"scene"\s*:\s*"((?:[^"\\]|\\.)*)"', raw, re.DOTALL)
            if m:
                scene = m.group(1).encode().decode("unicode_escape")[:5000].strip()
        if not scene:
            scene = "[This year had no recorded scene.]"
            scene_fallback_used = True
        narrative = {
            "scene": scene,
            "which_strata_fired": [int(x) for x in raw_strata if isinstance(x, (int, float))][:20],
            "which_frameworks_fired": [str(x) for x in raw_fw if isinstance(x, str)][:20],
            "what_was_buffered": [str(x) for x in raw_buf if isinstance(x, str)][:10],
            "what_scratched": [str(x) for x in raw_scr if isinstance(x, str)][:10],
        }
        if scene_fallback_used:
            narrative["_scene_fallback"] = "pass2_empty_scene"
            narrative["_integrity"] = {"status": "degraded", "reason": "pass2_empty_scene_fallback"}
    dialogue = obj.get("dialogue_snippets")
    if isinstance(dialogue, list):
        dialogue = [
            {"speaker": str(s.get("speaker", "other"))[:50], "line": str(s.get("line", ""))[:500]}
            for s in dialogue[:20] if isinstance(s, dict)
        ]
    else:
        dialogue = []
    consistency = obj.get("consistency_check") or {}
    if isinstance(consistency, dict):
        consistency = {
            "did_not_resolve": bool(consistency.get("did_not_resolve", True)),
            "public_vs_private_register_obeyed": bool(consistency.get("public_vs_private_register_obeyed", True)),
            "latent_vs_expressed_aim_obeyed": bool(consistency.get("latent_vs_expressed_aim_obeyed", True)),
        }

    # Particularity block (specLLM): 8 anchors; each can be dict with name/micro_detail etc. or string
    raw_particularity = obj.get("particularity") or obj.get("particularity_block") or {}
    if isinstance(raw_particularity, dict):
        anchor_keys = ("place_anchor", "object_anchor", "schedule_anchor", "money_anchor", "language_anchor", "power_anchor", "body_anchor", "social_risk_anchor")
        particularity = {}
        for k in anchor_keys:
            v = raw_particularity.get(k)
            if isinstance(v, dict):
                particularity[k] = {str(kk): str(vv)[:500] for kk, vv in v.items() if isinstance(vv, (str, int, float))}
            elif isinstance(v, str):
                particularity[k] = {"value": v[:500]}
            else:
                particularity[k] = {}
    else:
        particularity = {}

    # Jaggedness: 2 contradictions per scene; list of {and: [str, str], where: str}
    raw_jaggedness = obj.get("jaggedness") or []
    jaggedness = []
    if isinstance(raw_jaggedness, list):
        for j in raw_jaggedness[:5]:
            if isinstance(j, dict):
                and_pair = j.get("and")
                if isinstance(and_pair, list) and len(and_pair) >= 2:
                    jaggedness.append({
                        "and": [str(and_pair[0])[:80], str(and_pair[1])[:80]],
                        "where": str(j.get("where", ""))[:200],
                    })
    jaggedness = jaggedness[:5]

    # Micro_causality: list of {detail: str, caused: str}
    raw_micro = obj.get("micro_causality") or []
    micro_causality = []
    if isinstance(raw_micro, list):
        for m in raw_micro[:5]:
            if isinstance(m, dict) and (m.get("detail") or m.get("caused")):
                micro_causality.append({
                    "detail": str(m.get("detail", ""))[:300],
                    "caused": str(m.get("caused", ""))[:300],
                })
    micro_causality = micro_causality[:5]

    # Person_stubs: 0–2 new; name, role, signature, moral_edge, speech_tic, status_marker, pressure_point
    raw_stubs = obj.get("person_stubs") or obj.get("person_stub") or []
    if isinstance(raw_stubs, dict):
        raw_stubs = [raw_stubs]
    person_stubs = []
    if isinstance(raw_stubs, list):
        for s in raw_stubs[:5]:
            if isinstance(s, dict):
                person_stubs.append({
                    "name": str(s.get("name", ""))[:80],
                    "role": str(s.get("role", ""))[:80],
                    "signature": str(s.get("signature", ""))[:200],
                    "moral_edge": str(s.get("moral_edge", ""))[:200],
                    "speech_tic": str(s.get("speech_tic", ""))[:200],
                    "status_marker": str(s.get("status_marker", ""))[:100],
                    "pressure_point": str(s.get("pressure_point", ""))[:200],
                })
    person_stubs = person_stubs[:5]

    out = {
        "narrative_snapshot": narrative,
        "dialogue_snippets": dialogue,
        "consistency_check": consistency,
        "particularity": particularity,
        "jaggedness": jaggedness,
        "micro_causality": micro_causality,
        "person_stubs": person_stubs,
    }
    if scene_fallback_used:
        out["_integrity"] = {
            "status": "degraded",
            "fallback_used": True,
            "fallback_reason": "empty_scene_fallback",
            "reasons": ["empty_scene_fallback"],
            "surface": "render_output",
        }
    return out


# --- State summary from backbone (Pass 1 input) ---
# specLLM StateSummaryForCandidates uses psychological capacity; v3 stores material only.
# We map material + derived + peak_routing to proxy psychological fields for the summary.

def state_summary_from_backbone(
    state: BackboneState,
    derived: DerivedIndices,
    identity_override: dict[str, Any] | None = None,
    last_year_notes: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build StateSummaryForCandidates (Pass 1 input) from BackboneState + DerivedIndices.
    identity_override can provide identity.country, identity.region, identity.ses_band.
    Psychological capacity fields are proxied from material + derived (v3 has no psychological vector yet).
    """
    c = state.capacity
    pr = state.peak_routing
    ic = state.intensity_and_capture
    # Real psychological capacity from backbone — PsychologicalCapacity fields updated by
    # metabolization_effects and health_drift over the life course.
    pc = state.psychological_capacity
    vitality = float(getattr(pc, "vitality", 50.0))
    aperture = float(getattr(pc, "aperture", 50.0))
    reality_anchor = float(getattr(pc, "reality_anchor", 50.0))
    binding = float(getattr(pc, "binding", 50.0))
    coherence = float(getattr(pc, "coherence", 50.0))
    agency = derived.agency_capacity_AC  # AC 0-100; more sensitive than raw pc.agency
    transmutation = float(getattr(pc, "transmutation", 50.0))

    def _id_real(v: Any) -> str:
        """Strip placeholder values so the LLM gets real identity data only."""
        s = str(v).strip() if v is not None else ""
        return "" if s in ("", "—", "Unknown", "unknown", "None") else s

    raw_id = dict(identity_override or {})
    identity: dict[str, Any] = {}
    for _k, _v in raw_id.items():
        if isinstance(_v, str):
            cleaned = _id_real(_v)
            identity[_k] = cleaned if cleaned else _v  # keep original for non-string fields
        else:
            identity[_k] = _v
    if not _id_real(identity.get("country", "")):
        identity["country"] = "unknown"
    if not _id_real(identity.get("region", "")):
        identity["region"] = "unknown"
    if not _id_real(identity.get("ses_band", "")):
        identity["ses_band"] = "unknown"

    # Salient strata: from strata_salience if present; else minimal placeholder
    salient_strata = []
    if state.strata_salience and isinstance(state.strata_salience, dict):
        for level, info in list(state.strata_salience.items())[:5]:
            if isinstance(info, dict):
                salient_strata.append({
                    "level": int(level) if isinstance(level, (int, float)) else 0,
                    "name": str(info.get("name", level))[:80],
                    "coercion": float(info.get("coercion", 50)),
                    "provision": float(info.get("provision", 50)),
                    "contradiction": float(info.get("contradiction", 50)),
                })
    if not salient_strata:
        salient_strata = [{"level": 7, "name": "family", "coercion": 50, "provision": 50, "contradiction": 50}]

    # Available channels: default set; narrow by calibration_regime outlier_penalties when present
    available = ["family", "peer", "school", "work", "media", "neighborhood"]
    unlikely = ["movement", "diaspora", "online"]
    if state.field and getattr(state.field, "raw", None):
        # Could derive from field.raw / repression / economy
        pass
    cal = getattr(state, "calibration_regime", None)
    if cal is not None:
        # Outlier penalties that mention political/activism/state → movement, state less available
        for p in (getattr(cal, "outlier_penalties", None) or [])[:20]:
            if isinstance(p, dict):
                topic = (p.get("topic") or p.get("behavior") or "").lower()
                if any(x in topic for x in ("political", "activism", "protest", "state")):
                    if "movement" not in unlikely:
                        unlikely = list(unlikely) + ["movement"]
                    if "state" not in unlikely:
                        unlikely = list(unlikely) + ["state"]
                    break

    # Filter out placeholder scaffolding — sending "placeholder_0" to the LLM produces
    # generic events because the model has no ideological content to hook into.
    frameworks_active = [
        {"id": f.id, "weight": round(f.weight, 1)}
        for f in state.frameworks
        if getattr(f, "weight", 0) > 0 and not str(getattr(f, "id", "")).startswith("placeholder")
    ][:10]
    active_cracks = []
    for cr in state.cracks:
        if getattr(cr, "active", False):
            cr_type = getattr(cr, "type", "unknown") or "unknown"
            if cr_type == "placeholder":
                continue  # never send structural scaffolding to LLM
            active_cracks.append({
                "domain": cr_type[:80],
                "tension": cr_type.replace("_", " "),
                "strength": round(getattr(cr, "intensity", 0), 1),
            })
    active_cracks = active_cracks[:8]

    wv = getattr(state, "wound_vector", None)
    if wv is not None and hasattr(wv, "to_sensitivities_dict"):
        wound = {
            **wv.to_sensitivities_dict(),
            "default_channels": list(getattr(wv, "default_coping_channels", None) or ["withdraw", "intellectualize"]),
        }
    else:
        wound = {
            "shame": 50.0, "fear": 50.0, "anger": 50.0, "recognition": 50.0,
            "control": 50.0, "abandonment": 50.0, "loss": 50.0,
            "default_channels": ["withdraw", "intellectualize"],
        }

    # Calibration regime (spec §5): norm_center, uniqueness_norm, penalties/incentives, dream_window
    calibration_summary: dict[str, Any] = {}
    if cal is not None:
        calibration_summary = {
            "norm_center": getattr(cal, "norm_center", "middle"),
            "uniqueness_norm": round(getattr(cal, "uniqueness_norm", 50), 1),
            "outlier_penalties": (getattr(cal, "outlier_penalties", None) or [])[:15],
            "outlier_incentives": (getattr(cal, "outlier_incentives", None) or [])[:15],
            "dream_window": (getattr(cal, "dream_window", None) or "")[:300],
        }

    # Boundary map per domain (spec §5): discouraged / permitted / incentivized, trigger_conditions
    boundary_map_summary: dict[str, Any] = {}
    bmap = getattr(state, "boundary_map", None) or {}
    if isinstance(bmap, dict):
        for domain_key, entry in list(bmap.items())[:12]:
            if hasattr(entry, "discouraged"):
                boundary_map_summary[str(domain_key)[:80]] = {
                    "discouraged": list(getattr(entry, "discouraged", None) or [])[:20],
                    "permitted": list(getattr(entry, "permitted", None) or [])[:20],
                    "incentivized": list(getattr(entry, "incentivized", None) or [])[:20],
                    "trigger_conditions": list(getattr(entry, "trigger_conditions", None) or [])[:5],
                }

    summary = {
        "year": state.year,
        "age": state.age,
        "identity": identity,
        "field": {
            "salient_strata": salient_strata,
            "hostage_index": round(derived.hostage_index, 2),
            "affordances": {
                "available_channels": available,
                "unlikely_channels": unlikely,
            },
        },
        "capacity": {
            "vitality": round(vitality, 1),
            "aperture": round(aperture, 1),
            "reality_anchor": round(reality_anchor, 1),
            "binding": round(binding, 1),
            "coherence": round(coherence, 1),
            "agency": round(agency, 1),
            "transmutation": round(transmutation, 1),
        },
        "wound": wound,
        "frameworks_active": frameworks_active,
        "active_cracks": active_cracks,
    }
    # PracticeStack summary — what the persona is actively doing, shaping their daily texture
    ps_raw = getattr(state, "practice_stack", None)
    if ps_raw is not None:
        ps_dict = {
            k: round(getattr(ps_raw, k, 0), 0)
            for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")
            if getattr(ps_raw, k, 0) >= 10
        }
        if ps_dict:
            summary["practices"] = ps_dict
    # Only include last_year_notes if actual notes are present (not empty stub)
    if last_year_notes and (last_year_notes.get("events") or last_year_notes.get("what_shifted")):
        summary["last_year_notes"] = last_year_notes
    if calibration_summary:
        summary["calibration_regime"] = calibration_summary
    if boundary_map_summary:
        summary["boundary_map"] = boundary_map_summary

    # Domain A/S/V as structured labels (Aim latent/expressed deferred — not yet populated by runtime)
    domain_axes: dict[str, dict[str, Any]] = {}
    for name in DOMAIN_NAMES:
        if name in state.domains:
            d = state.domains[name]
            domain_axes[name] = {
                "A": domain_axis_to_label("A", getattr(d, "A", 50)),
                "S": domain_axis_to_label("S", getattr(d, "S", 50)),
                "V": domain_axis_to_label("V", getattr(d, "V", 50)),
            }
    if domain_axes:
        summary["domain_axes"] = domain_axes

    # Child model (specLLM): assumed_rules, taboos, what_counts_as_possible — for rupture validation
    child_model = getattr(state, "child_model", None)
    if isinstance(child_model, dict) and child_model:
        summary["child_model"] = {
            "assumed_rules": list(child_model.get("assumed_rules") or [])[:15],
            "taboos": list(child_model.get("taboos") or [])[:10],
            "what_counts_as_possible": str(child_model.get("what_counts_as_possible") or "medium").strip().lower()[:20],
        }
    else:
        # Default: age-appropriate assumed_rules; what_counts_as_possible from aperture
        aperture_val = round(aperture, 0)
        what_possible = "narrow" if aperture_val < 40 else ("wide" if aperture_val >= 60 else "medium")
        summary["child_model"] = {
            "assumed_rules": [
                "Adults are mostly fair",
                "Friends don't betray you in public",
                "Violence happens elsewhere",
                "Teachers can't be cruel on purpose",
                "Home is safe",
            ][:15],
            "taboos": ["sex", "police", "money shame"][:10],
            "what_counts_as_possible": what_possible,
        }

    # Expectation baseline + striving (GAP_AND_NEXT_STEPS: get into flow)
    eb = getattr(state, "expectation_baseline", None)
    if isinstance(eb, dict) and eb:
        summary["expectation_baseline"] = dict(eb)
    else:
        summary["expectation_baseline"] = {}

    striving = getattr(state, "striving_objects", None) or []
    summary["striving_objects"] = [
        {"id": getattr(s, "id", "")[:80], "label": getattr(s, "label", "")[:120], "need_axis": getattr(s, "need_axis", ""), "investment": round(getattr(s, "investment", 50), 0)}
        for s in striving[:12] if hasattr(s, "id")
    ]

    # Active magnets (who/what pulls on this person)
    magnets = getattr(state, "active_magnets", None) or []
    summary["active_magnets"] = [
        {"id": getattr(m, "id", "")[:80], "label": getattr(m, "label", "")[:120], "magnet_type": getattr(m, "magnet_type", "friend")}
        for m in magnets[:10] if hasattr(m, "id")
    ]

    # Rupture/plasticity context (open process, plasticity window)
    procs = getattr(state, "metabolization_processes", None) or []
    active_procs = [p for p in procs if getattr(p, "status", "") in ("raw", "working")]
    pw = getattr(state, "plasticity_window", None) or {}
    summary["rupture_plasticity"] = {
        "active_metabolization_count": len(active_procs),
        "plasticity_years_left": int(pw.get("years_left", 0)),
        "recent_rupture_domains": [getattr(p, "domain", "")[:60] for p in active_procs[:3]],
        "magnet_susceptibility": int(pw.get("magnet_susceptibility", 10)),
        "framework_switch_sensitivity": int(pw.get("framework_switch_sensitivity", 10)),
        "crack_rewrite_probability": int(pw.get("crack_rewrite_probability", 10)),
    }

    # Registers (public/private expression gate, inner_load) — so LLM can respect expressed aim gated
    reg = getattr(state, "registers", None)
    if reg is not None:
        summary["registers"] = {
            "public_expression_gate": round(getattr(reg, "public_expression_gate", 50), 1),
            "private_expression_gate": round(getattr(reg, "private_expression_gate", 50), 1),
            "inner_load": round(getattr(reg, "inner_load", 50), 1),
        }
    else:
        summary["registers"] = {"public_expression_gate": 50, "private_expression_gate": 50, "inner_load": 50}

    # Metabolic style (current, trend) — so LLM can respect compartmentalizing vs transmuting etc.
    ms = getattr(state, "metabolic_style", None) or {}
    if isinstance(ms, dict):
        summary["metabolic_style"] = {
            "current": str(ms.get("current", "transmuting"))[:40],
            "trend": str(ms.get("trend", "stabilizing"))[:40],
        }
    else:
        summary["metabolic_style"] = {"current": "transmuting", "trend": "stabilizing"}

    return summary


def build_render_packet(
    year: int,
    age: int,
    selected_events: list[dict[str, Any]],
    selected_magnets: list[dict[str, Any]],
    state_deltas_applied: dict[str, Any],
    constraints: dict[str, Any],
    identity_override: dict[str, Any] | None = None,
    persona_context: dict[str, Any] | None = None,
    previous_scene: str | None = None,
    awareness_gating: dict[str, str] | None = None,
    surface_psyche: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build RenderPacket (Pass 2 input) from code-side selection and applied deltas.
    When identity_override is provided, include locality, country, religion, gender, ethnicity,
    ses_band, minority_status, and all_languages so the rendered scene is about THIS person in
    THIS place with THIS structural position (not a generic character).
    persona_context carries wound_pattern, structural_lucidity, strata_position, rupture_notes.
    previous_scene carries last year's rendered scene for narrative continuity.
    awareness_gating carries per-domain constraints on what the persona can perceive.
    """
    out: dict[str, Any] = {
        "year": year,
        "age": age,
        "selected": {
            "events": selected_events,
            "magnets": selected_magnets,
        },
        "state_deltas_applied": state_deltas_applied,
    }
    if constraints and isinstance(constraints, dict) and any(v for v in constraints.values() if v):
        out["constraints"] = constraints
    if previous_scene and previous_scene.strip() and "[This year had no recorded scene]" not in previous_scene:
        out["previous_scene"] = previous_scene[:1500]
    if identity_override:
        def _real(v: Any) -> str:
            """Return the string value only if it's a real value — not a placeholder."""
            s = str(v).strip() if v is not None else ""
            return "" if s in ("", "—", "Unknown", "unknown", "None") else s

        langs = identity_override.get("languages")
        if isinstance(langs, list):
            lang0 = next((_real(x) for x in langs if _real(x)), "")
            all_langs = [_real(x) for x in langs if _real(x)]
        else:
            lang0 = _real(identity_override.get("primary_language") or "")
            all_langs = [lang0] if lang0 else []

        out["identity"] = {
            "given_name": _real(identity_override.get("given_name")),
            "family_name": _real(identity_override.get("family_name")),
            "locality": _real(identity_override.get("locality")) or _real(identity_override.get("region")),
            "region": _real(identity_override.get("region")),
            "country": _real(identity_override.get("country")) or _real(identity_override.get("country_code")),
            "religion": _real(identity_override.get("current_religion")) or _real(identity_override.get("religion")),
            "gender": _real(identity_override.get("gender")),
            "ethnicity": _real(identity_override.get("ethnicity_label")) or _real(identity_override.get("ethnicity")),
            "primary_language": lang0,
            "all_languages": all_langs,
            "ses_band": _real(identity_override.get("ses_band") or identity_override.get("class_origin") or ""),
            "minority_status": _real(identity_override.get("minority_status") or ""),
        }
        # Drop keys that are still empty so the LLM sees only real data
        out["identity"] = {k: v for k, v in out["identity"].items() if v}
        # Drop all_languages if it only repeats primary_language
        if out["identity"].get("all_languages") == [out["identity"].get("primary_language")]:
            out["identity"].pop("all_languages", None)

    if persona_context:
        out["persona_context"] = {k: v for k, v in persona_context.items() if v}

    if awareness_gating and isinstance(awareness_gating, dict):
        out["awareness_gating"] = {k: v for k, v in awareness_gating.items() if v}

    if surface_psyche is not None:
        out["surface_psyche"] = _sanitize_render_packet_surface_psyche(surface_psyche)

    return out


def _sanitize_render_packet_surface_psyche(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    sanitized: dict[str, Any] = {}
    for key in _RENDER_PACKET_ALLOWED_ROOT_FIELDS:
        if key not in value:
            continue
        nested = value[key]
        if key == "domains" and isinstance(nested, dict):
            domains: dict[str, Any] = {}
            for domain_name, domain_value in nested.items():
                if not isinstance(domain_value, dict):
                    continue
                cleaned = {k: v for k, v in domain_value.items() if k in _RENDER_PACKET_ALLOWED_DOMAIN_FIELDS}
                if cleaned:
                    domains[str(domain_name)] = cleaned
            sanitized[key] = domains
        else:
            sanitized[key] = nested
    return sanitized
