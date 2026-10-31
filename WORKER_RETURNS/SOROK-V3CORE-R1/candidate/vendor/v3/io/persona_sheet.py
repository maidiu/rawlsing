# v3/io/persona_sheet.py
# Wave 4: Emit persona_sheet.json compatible with run_conversation_chat.py --persona-json.
# Builds v2-compatible surface (identity, current_state, bands, voice_profile, backstory, life_snapshot)
# from BackboneState + DerivedIndices + rendered_output; optionally includes backbone/rendered_output.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices
from v3.core.year_record import state_and_derived_from_snapshot
from v3.render.phenomenology import developmental_age_tier, AGE_TIER_0_3, AGE_TIER_4_10

_SURFACE_PSYCH_ALLOWED_ROOT_FIELDS = {
    "schema_version",
    "export_rule",
    "domains",
    "dominant_recent_channels",
}
_SURFACE_PSYCH_ALLOWED_DOMAIN_FIELDS = {
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


def _first_micro_drift_or_repair_from_snapshot(snapshot: Any) -> dict | None:
    """Return first micro trace with kind micro_drift or micro_repair from snapshot, or None."""
    state, _derived, _record = state_and_derived_from_snapshot(snapshot)
    events = state.get("micro_trace_this_year") or state.get("events_this_year") or []
    for ev in events:
        if isinstance(ev, dict) and ev.get("kind") in ("micro_drift", "micro_repair"):
            return ev
    return None


def _ambient_line_from_micro_trace(age: int, cue: str, shaping: str) -> str:
    """One-line ambient year entry; age-sensitive wording (no adult abstractions at low ages)."""
    tier = developmental_age_tier(age)
    if tier == AGE_TIER_0_3:
        # Sensory/attachment only
        return "Felt shift in how things held together."
    if tier == AGE_TIER_4_10:
        # Fairness, concrete; no political
        return f"Things felt a bit more {shaping}."
    return f"{cue} → {shaping}"


def _country_default_labels(code: str) -> dict[str, str]:
    """Country-level fallbacks for religion/ethnicity/language so sheet never shows Unknown. Prefer v2.spec."""
    raw = str(code or "").strip()
    try:
        from v2.country_reference import normalize_country_ref
        from v2.spec import COUNTRY_DEFAULT_LABELS, _DEFAULT_LABEL_FALLBACK
        ref = normalize_country_ref(raw) if raw else {}
        code = str((ref or {}).get("iso3") or (ref or {}).get("iso2") or raw).strip().upper()
        defaults = (COUNTRY_DEFAULT_LABELS or {}).get(code) or _DEFAULT_LABEL_FALLBACK or {}
    except Exception:
        defaults = {}
    if not defaults:
        defaults = {"ethnicity": "—", "language": "—", "religion": "—"}
    # Never return Unknown; replace any that slipped in
    return {k: (v if (v and str(v).strip() != "Unknown") else "—") for k, v in defaults.items()}


def _is_valid_language_label(label: str) -> bool:
    text = (label or "").strip().lower()
    if not text or text in {"—", "-", "unknown", "n/a", "na", "dialect", "dialects"}:
        return False
    invalid_fragments = (
        " or ",
        "other ",
        "mute",
        "language group",
        "varieties",
    )
    return not any(fragment in text for fragment in invalid_fragments)


def _classify_language_integrity(labels: list[str]) -> dict[str, Any]:
    valid = [label for label in labels if _is_valid_language_label(label)]
    invalid = [label for label in labels if not _is_valid_language_label(label)]
    status = "clean" if not invalid else "invalid_labels_found"
    return {
        "status": status,
        "valid_labels": valid,
        "invalid_labels": invalid,
        "invalid_count": len(invalid),
        "valid_count": len(valid),
    }


def _sanitize_surface_psych(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    out: dict[str, Any] = {}
    for key in _SURFACE_PSYCH_ALLOWED_ROOT_FIELDS:
        if key not in value:
            continue
        nested = value[key]
        if key == "domains" and isinstance(nested, dict):
            domains: dict[str, Any] = {}
            for domain_name, domain_value in nested.items():
                if not isinstance(domain_value, dict):
                    continue
                cleaned = {k: v for k, v in domain_value.items() if k in _SURFACE_PSYCH_ALLOWED_DOMAIN_FIELDS}
                if cleaned:
                    domains[str(domain_name)] = cleaned
            out[key] = domains
        else:
            out[key] = nested
    return out


def _derive_job_type(state: BackboneState) -> str:
    """Derive job_type from practice_stack dominance when not in identity. Labels for conversation engine."""
    ps = state.practice_stack
    vals = [
        ("study", "student"),
        ("care", "caregiver"),
        ("organizing", "organizer"),
        ("craft", "craftsperson"),
        ("spiritual", "spiritual_practice"),
        ("risk_training", "risk_engaged"),
    ]
    by_val = [(getattr(ps, k, 0), label) for k, label in vals]
    by_val.sort(key=lambda x: -x[0])
    if by_val and by_val[0][0] >= 40:
        return by_val[0][1]
    if state.age <= 21 and getattr(ps, "study", 0) >= 20:
        return "student"
    return "worker"  # default


def _voice_profile_from_state(
    state: BackboneState,
    derived: DerivedIndices,
    identity_override: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Wire full voice profile from v3 state (v3 → v2 surface). Includes speech_tics, subculture_tags, routines, roles_in_systems, quirks, language_experience so web path populates palimpsest."""
    pr = state.peak_routing
    st = state.style_traits
    ps = state.practice_stack
    wv = state.wound_vector

    scripts: list[str] = []
    if getattr(pr, "loop_topology", None):
        scripts.append(f"loop_{pr.loop_topology}")
    if getattr(pr, "solidarity_boundary", None):
        scripts.append(f"solidarity_{pr.solidarity_boundary}")
    if getattr(pr, "theory_of_change_style", None):
        scripts.append(pr.theory_of_change_style)
    if getattr(st, "playfulness", 50) > 55:
        scripts.append("play_leeway")
    if getattr(st, "conscientiousness", 50) > 55:
        scripts.append("duty_anchor")
    scripts_were_defaulted = not bool(scripts)

    loops: list[str] = []
    for hook in ("shame", "fear", "anger", "control", "recognition"):
        val = getattr(wv, hook, 50)
        if val >= 60:
            loops.append(f"{hook}_sensitive")
        elif val <= 40:
            loops.append(f"{hook}_dampened")
    if getattr(pr, "coherence", 50) >= 60:
        loops.append("coherence_seeking")
    loops_were_defaulted = not bool(loops)

    # Speech tics from style_traits and wound (mannerisms).
    # Thresholds lowered to 52 so personas near the default 50 still get real tics.
    speech_tics: list[str] = []
    if getattr(st, "playfulness", 50) > 52:
        speech_tics.append("laughs_quickly")
    if getattr(st, "impulsivity", 50) > 52:
        speech_tics.append("cuts_in_or_finishes_sentences")
    if getattr(st, "absurdist_humor", 50) > 52:
        speech_tics.append("deadpan_then_smile")
    if getattr(wv, "shame", 50) >= 52:
        speech_tics.append("self_deprecates")
    if getattr(st, "conscientiousness", 50) > 52:
        speech_tics.append("qualifies_with_exactly")
    # Always give the persona at least one concrete mannerism derived from their wound/strategies
    if not speech_tics:
        _wv_vals = {h: getattr(wv, h, 50) for h in ("shame", "fear", "anger", "control", "abandonment")}
        _top_wound = max(_wv_vals, key=lambda h: _wv_vals[h])
        _tic_map = {
            "shame": "trails_off_mid_sentence",
            "fear": "glances_around_before_answering",
            "anger": "short_clipped_answers",
            "control": "corrects_own_phrasing",
            "abandonment": "checks_if_still_listening",
        }
        speech_tics.append(_tic_map.get(_top_wound, "pauses_before_answering"))
    speech_tics_were_defaulted = len(speech_tics) == 1 and speech_tics[0] == "pauses_before_answering"

    # Subculture tags from practice_stack, peak_routing, identity
    subculture_tags: list[str] = []
    if getattr(ps, "study", 0) >= 35:
        subculture_tags.append("student_world")
    if getattr(ps, "care", 0) >= 35:
        subculture_tags.append("caregiver_network")
    if getattr(ps, "organizing", 0) >= 35:
        subculture_tags.append("organizer_culture")
    if getattr(ps, "spiritual", 0) >= 35:
        subculture_tags.append("faith_community")
    if getattr(ps, "craft", 0) >= 35:
        subculture_tags.append("maker_scene")
    topo = getattr(pr, "solidarity_boundary", "") or ""
    if topo:
        subculture_tags.append(f"solidarity_{topo}")
    id_ = identity_override or {}
    loc = (id_.get("locality") or id_.get("region") or "").strip()
    if loc:
        subculture_tags.append(loc.replace(" ", "_").lower()[:40])

    # Routines: practices + wound (rituals that reinforce/undermine)
    routines: list[str] = []
    if getattr(ps, "spiritual", 0) >= 40:
        routines.append("morning_ritual_or_pause")
    if getattr(wv, "shame", 50) >= 55 and getattr(st, "playfulness", 50) > 50:
        routines.append("guilt_after_pleasure")
    if getattr(st, "conscientiousness", 50) > 58:
        routines.append("list_before_sleep")
    if getattr(ps, "organizing", 0) >= 40:
        routines.append("check_in_with_people")
    routines_were_defaulted = not bool(routines)

    # Roles from practice_stack + active_magnets.
    # Thresholds lowered to 20 so any meaningful practice registers.
    roles_in_systems: list[str] = []
    if getattr(ps, "study", 0) >= 20:
        roles_in_systems.append("student")
    if getattr(ps, "care", 0) >= 20:
        roles_in_systems.append("caregiver")
    if getattr(ps, "organizing", 0) >= 20:
        roles_in_systems.append("organizer")
    if getattr(ps, "spiritual", 0) >= 20:
        roles_in_systems.append("practitioner_of_faith")
    if getattr(ps, "craft", 0) >= 20:
        roles_in_systems.append("maker")
    for m in getattr(state, "active_magnets", [])[:8]:
        mt = getattr(m, "magnet_type", "") or (m.get("magnet_type") if isinstance(m, dict) else "")
        if mt and mt not in roles_in_systems:
            roles_in_systems.append(str(mt)[:30])
    roles_were_defaulted = not bool(roles_in_systems)

    # Rupture-derived voice texture: unmetabolized rupture shards are the most
    # character-defining features of a persona and must surface in the voice schema.
    rupture_shards = getattr(state, "rupture_shards", None) or []
    rupture_voice_notes: list[str] = []
    for shard in rupture_shards[:3]:
        status = getattr(shard, "current_status", "") or (shard.get("current_status") if isinstance(shard, dict) else "")
        assumption = getattr(shard, "violated_assumption", "") or (shard.get("violated_assumption") if isinstance(shard, dict) else "")
        mode = getattr(shard, "metabolization_mode", "") or (shard.get("metabolization_mode") if isinstance(shard, dict) else "")
        # Rupture shards store age and year, not origin_year — pull age first, fall back to year
        origin_age = getattr(shard, "age", None) or (shard.get("age") if isinstance(shard, dict) else None)
        origin_year = getattr(shard, "year", None) or (shard.get("year") if isinstance(shard, dict) else None)
        origin = f"age {origin_age}" if origin_age else (str(origin_year) if origin_year else "childhood")
        if assumption and status in ("raw", "narrativized", "sealed"):
            note = f'unresolved since {origin}: "{assumption}"'
            if mode:
                note += f" (metabolized as: {mode})"
            rupture_voice_notes.append(note)

    # Quirks from style_traits and wound.
    # Thresholds lowered to 52; fallback ensures every persona has at least one quirk.
    quirks: list[str] = []
    if getattr(st, "aesthetic_sensitivity", 50) > 52:
        quirks.append("notices_texture_and_light")
    if getattr(st, "novelty_seeking", 50) > 52:
        quirks.append("tries_new_phrases")
    if getattr(wv, "control", 50) >= 52:
        quirks.append("rephrases_until_right")
    if not quirks:
        # Derive a quirk from peak_routing loop topology or strategies
        _topo = getattr(pr, "loop_topology", "") or ""
        _toc = getattr(pr, "theory_of_change_style", "") or ""
        if "self_contained" in _topo or "self_contained" in _toc:
            quirks.append("goes_quiet_when_thinking")
        elif "expanding" in _topo or "expanding" in _toc:
            quirks.append("draws_others_into_the_point")
        else:
            quirks.append("returns_to_same_example_twice")
    quirks_were_defaulted = len(quirks) == 1 and quirks[0] == "returns_to_same_example_twice"

    # Language experience from identity
    language_experience: dict[str, Any] = {}
    language_experience_were_defaulted = True
    if identity_override:
        lang = identity_override.get("primary_language") or identity_override.get("languages")
        if isinstance(lang, list) and lang:
            language_experience["L1"] = str(lang[0])[:60]
            language_experience_were_defaulted = False
        elif isinstance(lang, str) and lang.strip():
            language_experience["L1"] = lang.strip()[:60]
            language_experience_were_defaulted = False
        rel = identity_override.get("current_religion") or identity_override.get("religion") or ""
        if rel:
            language_experience["religion_language"] = str(rel)[:60]

    voice_profile = {
        "identity_scripts": scripts or ["default_self"],
        "moral_loops": loops or ["steady"],
        "speech_tics": speech_tics,
        "subculture_tags": subculture_tags,
        "routines": routines,
        "roles_in_systems": roles_in_systems,
        "quirks": quirks,
        "language_experience": language_experience,
        # Rupture notes feed directly into VOICE_SCHEMA so the conversation engine
        # knows what this person is still carrying and can't talk around.
        "rupture_voice_notes": rupture_voice_notes,
    }
    voice_profile["_provenance"] = {
        "identity_scripts": {
            "fallback_generated": scripts_were_defaulted,
            "source_signals": ["peak_routing.loop_topology", "peak_routing.solidarity_boundary", "peak_routing.theory_of_change_style", "style_traits.playfulness", "style_traits.conscientiousness"],
        },
        "moral_loops": {
            "fallback_generated": loops_were_defaulted,
            "source_signals": ["wound_vector.shame", "wound_vector.fear", "wound_vector.anger", "wound_vector.control", "wound_vector.recognition", "peak_routing.coherence"],
        },
        "speech_tics": {
            "fallback_generated": speech_tics_were_defaulted,
            "source_signals": ["style_traits.playfulness", "style_traits.impulsivity", "style_traits.absurdist_humor", "wound_vector.shame", "style_traits.conscientiousness"],
        },
        "subculture_tags": {
            "fallback_generated": False,
            "source_signals": ["practice_stack", "peak_routing", "identity_override.locality/region"],
        },
        "routines": {
            "fallback_generated": routines_were_defaulted,
            "source_signals": ["practice_stack.spiritual", "wound_vector.shame", "style_traits.conscientiousness", "practice_stack.organizing"],
        },
        "roles_in_systems": {
            "fallback_generated": roles_were_defaulted,
            "source_signals": ["practice_stack", "active_magnets"],
        },
        "quirks": {
            "fallback_generated": quirks_were_defaulted,
            "source_signals": ["style_traits.aesthetic_sensitivity", "style_traits.novelty_seeking", "wound_vector.control", "peak_routing.loop_topology", "peak_routing.theory_of_change_style"],
        },
        "language_experience": {
            "fallback_generated": language_experience_were_defaulted,
            "source_signals": ["identity_override.primary_language", "identity_override.languages", "identity_override.current_religion"],
        },
        "rupture_voice_notes": {
            "fallback_generated": False,
            "source_signals": ["state.rupture_shards"],
        },
    }
    return voice_profile


def _micrograph_from_state(state: BackboneState, rendered: dict[str, Any]) -> dict[str, list[Any]]:
    """Wire caregivers, peers, institutions, key_events, norm_conflicts from active_magnets + rendered_output."""
    caregivers: list[str] = []
    peers: list[str] = []
    institutions: list[str] = []
    for m in getattr(state, "active_magnets", []) or []:
        label = getattr(m, "label", "") or getattr(m, "id", "")
        mt = getattr(m, "magnet_type", "friend")
        if mt in ("mentor", "teacher", "leader"):
            caregivers.append(label or mt)
        elif mt in ("friend", "romance", "scene", "online_cluster"):
            peers.append(label or mt)
        elif mt in ("institution", "boss"):
            institutions.append(label or mt)
    key_events: list[str] = []
    for ev in getattr(state, "events_this_year", []) or []:
        if isinstance(ev, dict) and ev.get("kind"):
            key_events.append(f"{ev.get('kind', '')}: {ev.get('label', ev.get('id', ''))}"[:80])
    narrative = rendered.get("narrative_snapshot") or {}
    if isinstance(narrative, dict) and narrative.get("scene"):
        key_events.insert(0, "(last scene)")
    norm_conflicts: list[str] = []
    for c in getattr(state, "cracks", []) or []:
        if getattr(c, "type", None) and getattr(c, "intensity", 0) >= 30:
            norm_conflicts.append(getattr(c, "type", "crack"))
    return {
        "caregivers": caregivers[:10],
        "peers": peers[:10],
        "institutions": institutions[:10],
        "key_events": key_events[:15],
        "norm_conflicts": norm_conflicts[:8],
    }


# Band boundaries for trajectory (age at end of band): 0-6, 7-12, 13-17, 18-24, 25+
_TRAJECTORY_BANDS = [(0, 6), (7, 12), (13, 17), (18, 24), (25, 999)]


def _one_rupture_line(r: dict) -> str:
    """One rupture as memory: what gave way, at what age, how it sits now."""
    age = r.get("age", 0)
    v = (r.get("violated_assumption") or "").strip()
    status = (r.get("current_status") or "raw").replace("_", " ")
    irr = int(r.get("intrusive_return_rate", 50))
    if not v:
        return ""
    if irr >= 60:
        return f"At {age} something gave way: «{v[:120]}». Still {status}—it comes back often."
    return f"At {age} something gave way: «{v[:120]}». Now {status}."


def _one_metabolization_line(m: dict) -> str:
    """One metabolization as memory: what they've been carrying, since when, how they're processing it."""
    start_age = m.get("start_age", 0)
    v = (m.get("violated_assumption") or "").strip()
    mode = (m.get("mode") or "").replace("_", " ")
    status = (m.get("status") or "raw").replace("_", " ")
    narrators = m.get("narrators") or []
    triggers = m.get("reactivation_triggers") or []
    if not v:
        return ""
    who = f" (through {', '.join(narrators[:3])})" if narrators else ""
    trig = f" Triggers: {', '.join(triggers[:3])}." if triggers else ""
    return f"They've been carrying «{v[:100]}» since {start_age}—{mode}, {status}{who}.{trig}"


def _one_crack_line(c: dict) -> str:
    """One crack as memory: what kind, how deep, when it started."""
    t = (c.get("type") or "wound").replace("_", " ")
    intensity = float(c.get("intensity", 0))
    origin = c.get("origin_year", 0)
    if intensity < 20:
        return ""
    return f"A crack around {t} (from early on, still {intensity:.0f}/100)."


def _one_gift_line(g: dict) -> str:
    """One gift as memory: what they received, when, what need it touched."""
    age = g.get("age", 0)
    label = (g.get("label") or "").strip() or "something good"
    need = (g.get("need_axis") or "").replace("_", " ") or "life"
    return f"At {age} they received a gift: {label[:80]}—touched their {need}."


def _one_disruption_line(d: dict) -> str:
    """One disruption as memory: what hit them, when, whether it was identity-level."""
    age = d.get("age", 0)
    label = (d.get("label") or "").strip() or "something broke"
    malheur = d.get("malheur_risk", False)
    if malheur:
        return f"At {age} a disruption that cut to the bone: {label[:80]}."
    return f"At {age} a disruption: {label[:80]}."


def _trajectory_backstory_from_snapshots(per_year: list[Any]) -> str:
    """
    Build a non-repetitive layered backstory from per-year (state_dict, derived_dict).

    Each band only mentions ruptures/metabolization/gifts/disruptions that are *new* in
    that band — things already mentioned in a prior band are skipped. This prevents the
    same rupture appearing four times (which the LLM treats as boilerplate and de-weights).
    Structural stats (health, agency) are dropped after the first band — they add nothing
    to lived texture. The result reads as a compressed life story, not a ledger.
    """
    if not per_year:
        return ""

    # Seen sets: track already-mentioned items so each only appears once
    seen_rupture_ids: set[str] = set()
    seen_meta_ids: set[str] = set()
    seen_gift_ids: set[str] = set()
    seen_disruption_ids: set[str] = set()

    lines = [
        "LIFE AS PALIMPSEST — what has accumulated in them; who they are *because* of this:"
    ]

    for band_idx, (lo, hi) in enumerate(_TRAJECTORY_BANDS):
        rep_index = min(len(per_year) - 1, max(0, hi - 1))
        s, d, _record = state_and_derived_from_snapshot(per_year[rep_index])
        rep_age = int(s.get("age") or rep_index + 1)
        band_label = f"Ages {lo}–{hi}" if hi < 999 else f"Ages {lo}+"
        parts = [f"{band_label}:"]

        # Ruptures: only those newly acquired in this band
        ruptures = s.get("rupture_shards") or []
        for r in ruptures:
            rid = r.get("id") or r.get("violated_assumption", "")[:40]
            if rid in seen_rupture_ids:
                continue
            seen_rupture_ids.add(rid)
            line = _one_rupture_line(r)
            if line:
                parts.append(line)

        # Metabolization: only new processes
        metas = s.get("metabolization_processes") or []
        for m in metas[:3]:
            mid = m.get("id") or m.get("violated_assumption", "")[:40]
            if mid in seen_meta_ids:
                continue
            seen_meta_ids.add(mid)
            line = _one_metabolization_line(m)
            if line:
                parts.append(line)

        # Gifts: only new
        gifts = s.get("gift_shards") or []
        for g in gifts[:3]:
            gid = g.get("id") or (g.get("label", "")[:30] + str(g.get("age", "")))
            if gid in seen_gift_ids:
                continue
            seen_gift_ids.add(gid)
            line = _one_gift_line(g)
            if line:
                parts.append(line)

        # Disruptions: only new
        disruptions = s.get("disruption_shards") or []
        for disr in disruptions[:3]:
            did = disr.get("id") or (disr.get("label", "")[:30] + str(disr.get("age", "")))
            if did in seen_disruption_ids:
                continue
            seen_disruption_ids.add(did)
            line = _one_disruption_line(disr)
            if line:
                parts.append(line)

        # Structural context: only for the earliest bands (no point repeating numbers each band)
        if band_idx == 0:
            cap = s.get("capacity") or {}
            health = cap.get("health", 50)
            support = cap.get("social_support", 50)
            host = d.get("hostage_index", 0)
            parts.append(f"By then: health {health:.0f}/100, social support {support:.0f}/100, early pressure {host:.0f}.")
        elif band_idx == 1:
            ac = d.get("agency_capacity_AC", 0)
            practice = s.get("practice_stack") or {}
            study = practice.get("study", 0)
            care = practice.get("care", 0)
            organizing = practice.get("organizing", 0)
            active = [k for k, v in [("study", study), ("care", care), ("organizing", organizing)] if v >= 15]
            if active:
                parts.append(f"Agency building ({ac:.0f}/100); practices taking shape: {', '.join(active)}.")

        # Events from the representative year for texture (only if meaningful label)
        events = s.get("events_this_year") or []
        ev_labels = []
        for e in events[:3]:
            if isinstance(e, dict):
                lab = e.get("label") or e.get("kind") or e.get("id")
                if lab and lab not in ("micro_drift", "micro_repair", "no_event"):
                    ev_labels.append(str(lab)[:50])
        if ev_labels:
            parts.append(f"That year: {'; '.join(ev_labels)}.")

        # Only emit the band if it has something to say beyond the label
        if len(parts) > 1:
            lines.append(" ".join(parts))

    return "\n\n".join(lines)


def build_persona_sheet(
    state: BackboneState,
    derived: DerivedIndices,
    identity_override: dict[str, Any] | None = None,
    include_backbone: bool = True,
    trajectory_snapshots: list[Any] | None = None,
    parent_override: dict[str, Any] | None = None,
    generation_integrity: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Build a persona_sheet dict consumable by v2 run_conversation_chat.py --persona-json.
    Maps v3 backbone + derived + rendered_output to identity, current_state (needs, strategies, indices),
    bands, voice_profile, backstory, life_snapshot. If include_backbone, adds backbone and rendered_output keys.
    If trajectory_snapshots is provided (legacy list of (state_dict, derived_dict) tuples or YearRecord dicts per year),
    prepends a layered LIFE TRAJECTORY to backstory. If parent_override (from v2 generate_parent_identities), adds
    "parents" key.
    """
    id_override = identity_override or {}
    age = state.age
    current_year = state.year
    birth_year = current_year - age
    try:
        from v2.country_reference import normalize_country_ref
    except Exception:
        normalize_country_ref = None  # type: ignore
    try:
        from v3.core.generation_integrity import classify_field_provenance
    except Exception:
        classify_field_provenance = None  # type: ignore

    # Identity: v2 expects given_name, family_name, country, region, urban_rural, ses_band, minority_status, religion, gender, age, ethnicity, languages
    # Never emit "Unknown": use country defaults when missing or Unknown (everyone gets an identity).
    country_input = id_override.get("country") or id_override.get("country_code") or ""
    country_ref = normalize_country_ref(id_override.get("country") or id_override.get("country_code") or "") if normalize_country_ref else {}
    defaults = _country_default_labels(country_input) if country_input else _country_default_labels("")
    source_prov = id_override.get("_source_provenance") or {}
    ethnic_prov = source_prov.get("ethnic") or {}
    rel_lang_prov = source_prov.get("religion_language") or {}
    location_prov = source_prov.get("location") or {}
    def _str(v: Any) -> str:
        return (v or "").strip() if isinstance(v, str) else ""
    def _good(s: str) -> bool:
        return bool(s and s != "Unknown" and s != "—")
    religion = _str(id_override.get("religion") or id_override.get("current_religion") or id_override.get("childhood_religion"))
    if not _good(religion):
        religion = defaults.get("religion", "—") or "—"
    ethnicity = _str(id_override.get("ethnicity") or id_override.get("ethnicity_label"))
    if not _good(ethnicity):
        ethnicity = defaults.get("ethnicity", "—") or "—"
    langs = id_override.get("languages")
    if isinstance(langs, list):
        langs = [str(x).strip() for x in langs if x and str(x).strip() and str(x).strip() != "Unknown"]
    else:
        langs = []
    if not langs:
        primary = _str(id_override.get("primary_language"))
        if _good(primary):
            langs = [primary] + list(id_override.get("secondary_languages") or [])
        else:
            langs = [defaults.get("language", "—") or "—"]
    if not langs or (len(langs) == 1 and not _good(langs[0])):
        langs = [defaults.get("language", "—") or "—"]
    # Final clamp: never emit "Unknown" (everyone gets an identity)
    religion = religion if _good(religion) else (defaults.get("religion", "—") or "—")
    ethnicity = ethnicity if _good(ethnicity) else (defaults.get("ethnicity", "—") or "—")
    langs = [x if _good(x) else (defaults.get("language", "—") or "—") for x in langs]
    if not any(_good(x) for x in langs):
        langs = [defaults.get("language", "—") or "—"]
    language_integrity = _classify_language_integrity([str(x).strip() for x in langs if str(x).strip()])
    ses = id_override.get("ses_band") or id_override.get("current_class") or id_override.get("class_origin") or "middle"
    if isinstance(ses, str):
        ses = ses.replace(" ", "_").lower()

    field_provenance = {
        "given_name": {
            "source": "provided" if _good(_str(id_override.get("given_name"))) else "defaulted",
            "fallback_used": not _good(_str(id_override.get("given_name"))),
        },
        "country": {
            "source_family": (country_ref or {}).get("resolved_via") or "unknown",
            "fallback_used": bool(country_ref and country_ref.get("fallback_used")),
            "resolved_via": (country_ref or {}).get("resolved_via"),
            "iso2": (country_ref or {}).get("iso2") or "",
            "iso3": (country_ref or {}).get("iso3") or "",
            "canonical_name": (country_ref or {}).get("canonical_name") or "",
        },
        "ethnicity": {
            "source_family": ethnic_prov.get("source_family") or ("provided" if _good(ethnicity) else "defaulted"),
            "source_method": ethnic_prov.get("source_method") or "",
            "fallback_used": ethnic_prov.get("fallback_used", not _good(ethnicity)),
            "fallback_reason": ethnic_prov.get("fallback_reason") or "",
        },
        "religion": {
            "source_family": rel_lang_prov.get("source_family") or ("provided" if _good(religion) else "defaulted"),
            "source_method": rel_lang_prov.get("source_method") or "",
            "religion_found": rel_lang_prov.get("religion_found", _good(religion)),
            "fallback_used": rel_lang_prov.get("fallback_used", not _good(religion)),
            "fallback_reason": rel_lang_prov.get("fallback_reason") or "",
        },
        "language": {
            "source_family": rel_lang_prov.get("source_family") or ("provided" if any(_good(x) for x in langs) else "defaulted"),
            "source_method": rel_lang_prov.get("source_method") or "",
            "language_found": rel_lang_prov.get("language_found", any(_good(x) for x in langs)),
            "fallback_used": rel_lang_prov.get("fallback_used", not any(_good(x) for x in langs)),
            "fallback_reason": rel_lang_prov.get("fallback_reason") or "",
            "language_integrity": language_integrity,
        },
        "locality": {
            "source_family": location_prov.get("source_family") or ("geonames" if id_override.get("locality") else "missing"),
            "geo_country_code_used": location_prov.get("geo_country_code_used") or "",
            "city_found": location_prov.get("city_found", bool(id_override.get("locality"))),
            "fallback_used": location_prov.get("fallback_used", not bool(id_override.get("locality"))),
            "fallback_reason": location_prov.get("fallback_reason") or "",
        },
        "ses_band": {
            "source_family": "identity_pipeline",
            "fallback_used": ses == "middle",
        },
    }
    if classify_field_provenance is not None:
        field_provenance["field_integrity"] = classify_field_provenance(field_provenance)
    field_provenance["language_integrity"] = language_integrity
    loc_geo = field_provenance["locality"]["geo_country_code_used"]
    country_iso2 = field_provenance["country"]["iso2"]
    if loc_geo and country_iso2 and loc_geo.upper() != country_iso2.upper():
        field_provenance["_coherence_warnings"] = [
            f"locality queried under geo country {loc_geo} but persona country is {country_iso2}"
        ]
    identity = {
        "given_name": id_override.get("given_name", "Persona"),
        "family_name": id_override.get("family_name", ""),
        "country": id_override.get("country") or id_override.get("country_code", "unknown"),
        "region": id_override.get("region", "") or defaults.get("region", ""),
        "locality": id_override.get("locality", "") or id_override.get("region", "") or "",
        "urban_rural": id_override.get("urban_rural") or id_override.get("urbanicity", "city"),
        "ses_band": ses,
        "minority_status": id_override.get("minority_status", "dominant"),
        "religion": religion,
        "gender": id_override.get("gender", "female"),
        "age": age,
        "ethnicity": ethnicity,
        "languages": langs,
        "religiosity_level": float(id_override.get("religiosity_level") or 50.0),
    }

    # current_state: needs (NeedGradients), strategies (StrategyPortfolio), indices (Indices), thought_rails (ThoughtRails)
    # Map v3 capacity + derived to v2 need-like 0–100 values.
    # Note: When using v3 backbone without v2 recursion, many dimensions stay at defaults (0 or 50) because
    # only code-sampled events update state; LLM deltas (v2 simulate_life_course) are not applied.
    c = state.capacity
    pr = state.peak_routing

    # Warmth/bonding: social_support modulated by alienation and abandonment wound.
    # High social_support + high alienation + high abandonment wound → lower felt connection quality.
    _wv = getattr(state, "wound_vector", None)
    _abandonment = float(getattr(_wv, "abandonment", 50) or 50) if _wv else 50.0
    _recognition_wound = float(getattr(_wv, "recognition", 50) or 50) if _wv else 50.0
    _alienation_raw = float(getattr(state, "alienation", 0) or 0)
    _connection_quality = max(0.0, min(100.0,
        c.social_support
        - (_alienation_raw * 0.5)                        # alienation directly degrades felt warmth
        - max(0.0, (_abandonment - 50.0) * 0.5)          # abandonment wound: each point above 50 costs
    ))
    # belonging_group: group membership sense — more vulnerable to abandonment than warmth
    _belonging_quality = max(0.0, min(100.0,
        _connection_quality - max(0.0, (_abandonment - 50.0) * 0.3)
    ))
    # recognition_status: how satisfied is the need to be seen/respected
    _recognition_status = max(0.0, min(100.0,
        80.0 - max(0.0, (_recognition_wound - 50.0) * 1.5)
    ))
    # transcendence_sacred: spiritual need from religiosity, penalized if sacred assumptions were ruptured
    _religiosity = float(id_override.get("religiosity_level") or 50.0)
    _sacred_ruptured = any(
        getattr(rs, "domain", "") in ("sect_class", "sacred", "religion")
        and getattr(rs, "metabolization_mode", "") in ("sealing", "hardening", "mis_aim", "collapse")
        for rs in (getattr(state, "rupture_shards", None) or [])
    )
    _transcendence = max(0.0, min(100.0, _religiosity * (0.4 if _sacred_ruptured else 0.8)))
    # play_pleasure: appetite for pleasure/play — driven by vitality (life energy), modulated by shame
    # (shame suppresses playful expression) and presence of aesthetic/creative magnets.
    _vitality = float(getattr(state.psychological_capacity, "vitality", 50.0) or 50.0)
    _shame = float(getattr(_wv, "shame", 50.0) or 50.0) if _wv else 50.0
    _arts_magnets = [
        m for m in (getattr(state, "active_magnets", None) or [])
        if any(
            kw in str(
                (m.get("label") or m.get("id") or "") if isinstance(m, dict)
                else (getattr(m, "label", None) or getattr(m, "id", None) or "")
            ).lower()
            for kw in ("art", "music", "aesthetic", "creative", "culture")
        )
    ]
    _arts_bonus = min(8.0, len(_arts_magnets) * 3.0)
    _play_pleasure = max(0.0, min(100.0,
        _vitality * 0.6
        + state.style_traits.playfulness * 0.4
        - max(0.0, (_shame - 50.0) * 0.6)
        + _arts_bonus
    ))

    needs = {
        "safety": (c.health + (100 - state.reproduction_constraints.housing_insecurity)) / 2,
        "bodily_comfort": c.health,
        "warmth_bonding": _connection_quality,
        "belonging_group": _belonging_quality,
        "recognition_status": _recognition_status,
        "competence_effectiveness": c.skill,
        "autonomy_agency": derived.agency_capacity_AC,
        "coherence_meaning": pr.coherence,
        "play_pleasure": _play_pleasure,
        "transcendence_sacred": _transcendence,
    }
    # Strategies: proxy from practice_stack and style; floor from derived so we don't get all zeros
    agency_norm = derived.agency_capacity_AC / 100.0
    intensity_norm = getattr(state.intensity_and_capture, "intensity", 50.0) / 100.0
    strategies = {
        "humor_play": max(state.style_traits.absurdist_humor / 100.0 * 50, 50.0 * 0.2 * intensity_norm),
        "aggression_outward": 0.0,
        "aggression_inward": 0.0,
        "compliance_obedience": 0.0,
        "people_pleasing": 0.0,
        "caretaking_rescue": max(state.practice_stack.care / 100.0 * 50, 50.0 * 0.15 * agency_norm),
        "achievement_striving": max(state.practice_stack.study / 100.0 * 50, 50.0 * 0.4 * agency_norm),
        "perfectionism_control": 0.0,
        "piety_ideology": state.practice_stack.spiritual / 100.0 * 30,
        "intimacy_seeking": 0.0,
        "withdrawal_avoidance": 0.0,
        "dissociation_numbing": 0.0,
        "fantasy_immersion": 0.0,
        "substance_use": 0.0,
        "risk_seeking_thrill": max(state.capacity.risk_tolerance / 100.0 * 50, 50.0 * 0.25 * intensity_norm),
        "activism_justice": max(state.practice_stack.organizing / 100.0 * 50, 50.0 * 0.2 * agency_norm),
        "creative_expression": max(state.practice_stack.craft / 100.0 * 50, 50.0 * 0.2 * intensity_norm),
    }
    # Indices: derive from v3 derived/state so they're not all 0
    ic = state.intensity_and_capture
    indices = {
        "permeability_index": round(min(100.0, (getattr(ic, "intensity", 50.0) / 100.0) * 50 + (derived.structural_lucidity_SL or 0) * 0.3), 1),
        "drts": round(derived.agency_capacity_AC * 0.15, 1),
        "iai": round((derived.hostage_index or 0) * 0.2, 1),
        "transgression_threshold": max(0, min(100, 50 + (pr.coherence - 50) * 0.3)),
        "aesthetic_amplification": round(state.style_traits.aesthetic_sensitivity / 100.0 * 30, 1),
        "recursive_madness_threshold": 0.0,
    }
    # Thought rails: label from peak_routing so not all "unknown"
    toc = getattr(pr, "theory_of_change_style", "") or "institution_building"
    loop = getattr(pr, "loop_topology", "") or "self_contained"
    boundary = getattr(pr, "solidarity_boundary", "") or "expanding"
    thought_rails = {
        "authority_schema": toc.replace("_", " ") or "unknown",
        "fairness_schema": boundary.replace("_", " ") or "unknown",
        "self_schema": loop.replace("_", " ") or "unknown",
        "other_groups_schema": {},
    }
    current_state = {
        "needs": needs,
        "strategies": strategies,
        "indices": indices,
        "thought_rails": thought_rails,
    }

    # One band for current age (fix: 22 → 22-29 not 17-21; align with v2 band labels)
    if age <= 3:
        age_band = "0-3"
    elif age <= 11:
        age_band = "4-11"
    elif age <= 16:
        age_band = "12-16"
    elif age <= 21:
        age_band = "17-21"
    elif age <= 29:
        age_band = "22-29"
    elif age <= 45:
        age_band = "30-45"
    else:
        age_band = "46+"
    rendered = state.rendered_output or {}
    micrograph = _micrograph_from_state(state, rendered)
    bands = [
        {
            "age_band": age_band,
            "age_range": str(age),
            "needs": needs,
            "top_strategies": [k for k, v in sorted(strategies.items(), key=lambda x: -x[1])[:5] if v > 0] or ["people_pleasing"],
            "indices": indices,
            "micrograph": micrograph,
        }
    ]

    # Backstory: trajectory summary first (compressed), then only the real LLM scenes at the end.
    # Ordering matters for LLM attention: scenes come last so they're in the high-attention zone.
    # Structural-year annotations ("[no recorded scene]") are dropped entirely — they waste
    # tokens and teach the LLM to treat the backstory as boilerplate.
    narrative = rendered.get("narrative_snapshot") or {}
    scene = narrative.get("scene", "") if isinstance(narrative, dict) else ""
    trajectory_text = _trajectory_backstory_from_snapshots(trajectory_snapshots) if trajectory_snapshots else ""

    # Collect real scenes only — skip structural stubs
    real_scenes: list[str] = []
    for i, snapshot in enumerate(trajectory_snapshots or []):
        snap, _d, _record = state_and_derived_from_snapshot(snapshot)
        ro = snap.get("rendered_output") or {}
        ns = ro.get("narrative_snapshot") or {}
        sc = (ns.get("scene") or "").strip() if isinstance(ns, dict) else ""
        if sc and "[This year had no recorded scene" not in sc and "[Structural year" not in sc:
            real_scenes.append(f"Age {i + 1}:\n{sc}")

    # Structure: trajectory summary → scene memories (most recent = last = highest attention)
    parts_bs: list[str] = []
    if trajectory_text:
        parts_bs.append(trajectory_text)
    if real_scenes:
        parts_bs.append("MEMORIES (specific moments — carry these; let them surface when the conversation touches them):\n\n" + "\n\n".join(real_scenes))
    elif scene:
        parts_bs.append(f"Most recent memory:\n{scene}")

    backstory = "\n\n".join(parts_bs) if parts_bs else ""

    # Prepend v2 parent narratives (older parent to meeting + second parent and fused story to birth) when present
    parent_birth_context = (parent_override or {}).get("parent_birth_context") if parent_override else None
    if parent_birth_context and isinstance(parent_birth_context, str) and parent_birth_context.strip():
        backstory = (
            "STORY YOU WERE BORN INTO (your parents—who they are, how they met, and the world you entered):\n\n"
            + parent_birth_context.strip()
            + "\n\n---\n\n"
            + backstory
        )

    # Voice profile: identity_scripts and moral_loops from state (peak_routing, style_traits, wound_vector)
    voice_profile = id_override.get("voice_profile") if isinstance(id_override.get("voice_profile"), dict) else None
    if not voice_profile:
        voice_profile = _voice_profile_from_state(state, derived, id_override)
    voice_profile_provenance = voice_profile.get("_provenance") if isinstance(voice_profile, dict) else None

    # Life snapshot: job_type from identity_override or derived from state (practice_stack dominance)
    job_type = id_override.get("job_type") or id_override.get("occupation") or _derive_job_type(state)
    life_snapshot = {
        "job_type": str(job_type).strip() or "unknown",
        "current_life_phase": "stable_routine_phase" if derived.hostage_index < 50 else "constrained_phase",
    }

    # Structure layer: baselines, strivings, rupture status (GAP_AND_NEXT_STEPS: surface for conversation/narrative)
    expectation_baseline = dict(getattr(state, "expectation_baseline", None) or {})
    active_strivings = [
        {"label": getattr(s, "label", "")[:120], "need_axis": getattr(s, "need_axis", ""), "investment": round(getattr(s, "investment", 50), 0)}
        for s in (getattr(state, "striving_objects", None) or [])[:15]
        if hasattr(s, "label")
    ]
    procs = getattr(state, "metabolization_processes", None) or []
    active_procs = [p for p in procs if getattr(p, "status", "") in ("raw", "working")]
    pw = getattr(state, "plasticity_window", None) or {}
    rupture_status = {
        "active_metabolization_count": len(active_procs),
        "plasticity_active": int(pw.get("years_left", 0)) > 0,
        "recent_domains": [getattr(p, "domain", "")[:60] for p in active_procs[:5]],
    }

    # Recent gift and disruption shards for narrative/conversation (GAP optional)
    gift_shards = getattr(state, "gift_shards", None) or []
    disruption_shards = getattr(state, "disruption_shards", None) or []
    recent_gifts = [
        {"label": (getattr(g, "label", "") or "")[:120], "need_axis": getattr(g, "need_axis", ""), "year": getattr(g, "year", None), "age": getattr(g, "age", None)}
        for g in gift_shards[-10:]
    ]
    recent_disruptions = [
        {"label": (getattr(d, "label", "") or "")[:120], "need_axis": getattr(d, "need_axis", ""), "year": getattr(d, "year", None), "age": getattr(d, "age", None)}
        for d in disruption_shards[-10:]
    ]

    sheet = {
        "identity": identity,
        "current_state": current_state,
        "bands": bands,
        "voice_profile": voice_profile,
        "backstory": backstory,
        "life_snapshot": life_snapshot,
        "expectation_baseline": expectation_baseline,
        "active_strivings": active_strivings,
        "rupture_status": rupture_status,
        "recent_gifts": recent_gifts,
        "recent_disruptions": recent_disruptions,
    }
    surface_psyche = getattr(state, "surface_psyche_profile", None)
    if isinstance(surface_psyche, dict) and surface_psyche:
        sheet["surface_psyche"] = _sanitize_surface_psych(surface_psyche)
    metadata = dict(sheet.get("metadata") or {})
    metadata["field_provenance"] = field_provenance
    metadata["field_integrity"] = field_provenance.get("field_integrity") if isinstance(field_provenance, dict) else None
    metadata["voice_profile_provenance"] = voice_profile_provenance or {}
    metadata["language_integrity"] = language_integrity
    if generation_integrity is not None:
        metadata["generation_integrity"] = generation_integrity
    sheet["metadata"] = metadata
    if parent_override:
        loc = parent_override.get("location") or {}
        region = loc.get("region") or {}
        city = loc.get("city") or {}
        sheet["parents"] = {
            "father": {
                "age_at_child_birth": parent_override.get("parents", {}).get("father", {}).get("age_at_child_birth"),
                "birth_year": parent_override.get("parents", {}).get("father", {}).get("birth_year"),
            },
            "mother": {
                "age_at_child_birth": parent_override.get("parents", {}).get("mother", {}).get("age_at_child_birth"),
                "birth_year": parent_override.get("parents", {}).get("mother", {}).get("birth_year"),
            },
            "household_location": (region.get("admin1_name") or "") + ", " + (city.get("name") or "" if isinstance(city, dict) else str(city or "")),
            "household_ses": (parent_override.get("ses") or {}).get("class_label"),
        }
    if include_backbone:
        from v3.io.json_codec import state_to_dict
        sheet["backbone"] = state_to_dict(state)
        sheet["rendered_output"] = rendered
    return sheet
