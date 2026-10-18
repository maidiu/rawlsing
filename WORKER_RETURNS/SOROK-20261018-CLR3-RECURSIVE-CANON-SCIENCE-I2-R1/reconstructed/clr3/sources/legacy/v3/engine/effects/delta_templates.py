# v3/engine/effects/delta_templates.py
# Wave 4: Event/magnet kind + intensity → delta templates (capacity, domains, frameworks, cracks);
# bounded application per v3config delta_caps. LLM provides semantic class; code maps to deltas.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.enums import DOMAIN_NAMES


def _cap_delta(delta: float, cap: float) -> float:
    return max(-cap, min(cap, delta))


def delta_from_event(
    event: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    """
    Map one selected event (kind, intensity, offers/costs, hooks) to a delta dict.
    Keys: capacity_deltas, domain_deltas, framework_deltas, crack_deltas, alienation_delta,
    practice_deltas, coherence_delta. All bounded by v3config delta_caps.
    """
    caps = config.get("delta_caps") or {}
    cap_capacity = float(caps.get("capacity_fields", 20))
    cap_domain = float(caps.get("domain_A", 10))  # use same for A/S/V
    cap_framework = float(caps.get("frameworks_weights", 15))
    cap_crack = 15.0  # typical intensify range
    cap_alienation = float(caps.get("alienation", 15))
    cap_practice = float(caps.get("practice_fields", 15))
    cap_coherence = float(caps.get("coherence", 10))

    kind = (event.get("kind") or "relationship").strip().lower()
    intensity = (event.get("intensity") or "minor").strip().lower()
    mult = 1.0 if intensity == "minor" else (1.5 if intensity == "major" else 2.0)

    magnets = event.get("magnets") or {}
    offers = set((magnets.get("offers") or []))
    costs = set((magnets.get("costs") or []))

    out: dict[str, Any] = {
        "capacity_deltas": {},
        "domain_deltas": {},
        "framework_deltas": [],
        "crack_deltas": [],
        "alienation_delta": 0.0,
        "practice_deltas": {},
        "coherence_delta": 0.0,
        "stability_delta": 0.0,
        "wound_deltas": {},
    }
    # Trauma kinds: add stability_delta (inertia spike); minor +3, major +5, shock +8
    trauma_kinds = ("puncture", "humiliation", "violence", "epistemic_rupture")
    if kind in trauma_kinds:
        stab = 5
        if intensity == "minor":
            stab = 3
        elif intensity == "shock":
            stab = 8
        out["stability_delta"] = float(stab)

    # Capacity: map offers/costs to v3 capacity fields (time, money, health, social_support, skill, mobility, risk_tolerance, legitimacy)
    if "agency" in offers:
        out["capacity_deltas"]["skill"] = _cap_delta(4 * mult, cap_capacity)
        out["capacity_deltas"]["social_support"] = _cap_delta(2 * mult, cap_capacity)
    if "agency" in costs:
        out["capacity_deltas"]["skill"] = out["capacity_deltas"].get("skill", 0) - _cap_delta(2 * mult, cap_capacity)
    if "binding" in costs or "care" in offers:
        out["capacity_deltas"]["social_support"] = out["capacity_deltas"].get("social_support", 0) + _cap_delta(3 * mult, cap_capacity)
    if "time" in costs:
        out["capacity_deltas"]["time"] = _cap_delta(-3 * mult, cap_capacity)
    if "money" in costs:
        out["capacity_deltas"]["money"] = _cap_delta(-5 * mult, cap_capacity)
    if "reality_anchor" in costs:
        out["capacity_deltas"]["health"] = out["capacity_deltas"].get("health", 0) - _cap_delta(2 * mult, cap_capacity)
    if "coherence" in costs:
        out["coherence_delta"] = _cap_delta(-2 * mult, cap_coherence)
    if "meaning" in offers:
        out["coherence_delta"] = out["coherence_delta"] + _cap_delta(2 * mult, cap_coherence)
    if "escape" in offers:
        out["alienation_delta"] = _cap_delta(2 * mult, cap_alienation)

    # Kind-specific
    if kind in ("puncture", "humiliation", "loss"):
        out["capacity_deltas"]["health"] = out["capacity_deltas"].get("health", 0) - _cap_delta(4 * mult, cap_capacity)
        out["alienation_delta"] = out["alienation_delta"] + _cap_delta(3 * mult, cap_alienation)
    elif kind == "opportunity":
        out["capacity_deltas"]["skill"] = out["capacity_deltas"].get("skill", 0) + _cap_delta(3 * mult, cap_capacity)
        out["capacity_deltas"]["money"] = out["capacity_deltas"].get("money", 0) + _cap_delta(2 * mult, cap_capacity)
    elif kind == "relationship":
        out["capacity_deltas"]["social_support"] = out["capacity_deltas"].get("social_support", 0) + _cap_delta(3 * mult, cap_capacity)
    elif kind == "practice":
        out["practice_deltas"]["organizing"] = _cap_delta(2 * mult, cap_practice)
        out["practice_deltas"]["craft"] = _cap_delta(2 * mult, cap_practice)
    elif kind == "epistemic_rupture":
        out["coherence_delta"] = out["coherence_delta"] + _cap_delta(-4 * mult, cap_coherence)
        out["capacity_deltas"]["health"] = out["capacity_deltas"].get("health", 0) - _cap_delta(2 * mult, cap_capacity)
        out["alienation_delta"] = out["alienation_delta"] + _cap_delta(2 * mult, cap_alienation)
    elif kind == "expectation_event":
        ex_type = (event.get("expectation_type") or "").strip().lower()
        if ex_type == "fulfillment":
            out["coherence_delta"] = out["coherence_delta"] + _cap_delta(2 * mult, cap_coherence)
            out["capacity_deltas"]["social_support"] = out["capacity_deltas"].get("social_support", 0) + _cap_delta(2 * mult, cap_capacity)
        elif ex_type == "violation":
            out["coherence_delta"] = out["coherence_delta"] + _cap_delta(-2 * mult, cap_coherence)
            out["alienation_delta"] = out["alienation_delta"] + _cap_delta(2 * mult, cap_alienation)

    # Domain: implicated domains get small A/V nudge
    implicated = event.get("implicated") or {}
    domains = implicated.get("domains") or []
    for d in domains:
        if d in DOMAIN_NAMES:
            out["domain_deltas"][d] = {
                "A": _cap_delta(1 * mult, cap_domain),
                "V": _cap_delta(1 * mult, cap_domain),
            }
    if not out["domain_deltas"] and kind in ("institution", "puncture"):
        # Default to nation_state if no domain specified
        out["domain_deltas"]["nation_state"] = {"A": _cap_delta(1 * mult, cap_domain), "V": _cap_delta(2 * mult, cap_domain)}

    # Wound sensitization: wound_hooks activate corresponding wound_vector fields.
    # Each hook adds to sensitivity (higher = more sensitized to that wound domain).
    # Caps: 2*mult per hook per event (minor=2, major=3, shock=4), ceiling 5 per field per event.
    # Abandonment-hook events also erode social_support (betrayal/loss of trust costs connection).
    _WOUND_FIELD_NAMES = frozenset({"shame", "fear", "anger", "abandonment", "control", "recognition", "loss"})
    cap_wound = 5.0
    wound_hooks = (event.get("hooks") or {}).get("wound_hooks") or []
    wound_deltas: dict[str, float] = {}
    for _hook in wound_hooks:
        _hook_name = str(_hook).strip().lower()
        if _hook_name in _WOUND_FIELD_NAMES:
            wound_deltas[_hook_name] = _cap_delta(
                wound_deltas.get(_hook_name, 0) + 2.0 * mult, cap_wound
            )
    # Abandonment hook → social trust erodes (person feels left or betrayed by someone they depended on)
    if "abandonment" in wound_deltas:
        out["capacity_deltas"]["social_support"] = (
            out["capacity_deltas"].get("social_support", 0) - _cap_delta(3.0 * mult, cap_capacity)
        )

    # Wound healing: positive event offers and relationship kinds reduce wound sensitivity.
    # Healing fires independently of hook activation — a relationship event can both soothe
    # abandonment (healing) and activate it (if hook fires), with the net sum determining direction.
    # Rates: -1.5*mult for primary healing offers, -1.0*mult for secondary.
    if kind == "relationship" or "care" in offers or "binding" in offers:
        wound_deltas["abandonment"] = wound_deltas.get("abandonment", 0) - _cap_delta(1.5 * mult, cap_wound)
        wound_deltas["fear"] = wound_deltas.get("fear", 0) - _cap_delta(1.0 * mult, cap_wound)
    if "meaning" in offers or kind == "practice":
        wound_deltas["shame"] = wound_deltas.get("shame", 0) - _cap_delta(1.0 * mult, cap_wound)
        wound_deltas["loss"] = wound_deltas.get("loss", 0) - _cap_delta(1.0 * mult, cap_wound)
    if "agency" in offers:
        wound_deltas["control"] = wound_deltas.get("control", 0) - _cap_delta(1.5 * mult, cap_wound)

    out["wound_deltas"] = wound_deltas

    return out


def delta_from_magnet(
    magnet: dict[str, Any],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Map one selected magnet to deltas (e.g. social_support, coherence, practice)."""
    caps = config.get("delta_caps") or {}
    cap_capacity = float(caps.get("capacity_fields", 20))
    cap_coherence = float(caps.get("coherence", 10))
    cap_practice = float(caps.get("practice_fields", 15))
    mult = 1.0

    out: dict[str, Any] = {
        "capacity_deltas": {"social_support": _cap_delta(3 * mult, cap_capacity)},
        "domain_deltas": {},
        "framework_deltas": [],
        "crack_deltas": [],
        "alienation_delta": 0.0,
        "practice_deltas": {},
        "coherence_delta": 0.0,
    }
    magnet_type = (magnet.get("magnet_type") or "friend").strip().lower()
    _label = str(magnet.get("label") or "").lower()
    _arts_label = any(kw in _label for kw in (
        "art", "music", "craft", "creative", "culture", "aesthetic",
        "film", "theater", "theatre", "dance", "poetry", "studio",
    ))
    _care_label = any(kw in _label for kw in (
        "famil", "parent", "sibling", "child", "partner", "spouse", "caregiv",
    ))
    _risk_label = any(kw in _label for kw in (
        "activist", "protest", "militia", "soldier", "militar", "guerrilla",
        "campaign", "resistance", "underground",
    ))
    if magnet_type == "mentor":
        out["capacity_deltas"]["skill"] = _cap_delta(4 * mult, cap_capacity)
        out["coherence_delta"] = _cap_delta(2 * mult, cap_coherence)
        # Mentor presence drives practice: all mentors → study; arts-labeled mentors → craft too
        out["practice_deltas"]["study"] = _cap_delta(2 * mult, cap_practice)
        if _arts_label:
            out["practice_deltas"]["craft"] = _cap_delta(3 * mult, cap_practice)
    elif magnet_type == "teacher":
        out["practice_deltas"]["study"] = _cap_delta(2 * mult, cap_practice)
    elif magnet_type == "scene":
        # Scene magnets in arts contexts drive craft practice
        if _arts_label:
            out["practice_deltas"]["craft"] = _cap_delta(2 * mult, cap_practice)
    elif magnet_type == "romance":
        # Romance magnets drive care practice (intimacy, emotional attunement)
        out["practice_deltas"]["care"] = _cap_delta(2 * mult, cap_practice)
    elif magnet_type == "leader":
        # Leader magnets in activist/conflict contexts drive risk_training
        if _risk_label:
            out["practice_deltas"]["risk_training"] = _cap_delta(2 * mult, cap_practice)
    elif magnet_type == "institution":
        out["capacity_deltas"]["social_support"] = out["capacity_deltas"].get("social_support", 0) + _cap_delta(2 * mult, cap_capacity)
    # Family/caretaking labels on any magnet type add care practice (beyond romance, handled above)
    if _care_label and magnet_type != "romance":
        out["practice_deltas"]["care"] = out["practice_deltas"].get("care", 0) + _cap_delta(2 * mult, cap_practice)
    return out


def merge_deltas(deltas_list: list[dict[str, Any]]) -> dict[str, Any]:
    """Merge multiple delta dicts into one (sum capacity/alienation/coherence; merge domain/framework/crack lists)."""
    merged: dict[str, Any] = {
        "capacity_deltas": {},
        "domain_deltas": {},
        "framework_deltas": [],
        "crack_deltas": [],
        "alienation_delta": 0.0,
        "practice_deltas": {},
        "coherence_delta": 0.0,
        "stability_delta": 0.0,
        "wound_deltas": {},
    }
    for d in deltas_list:
        for k, v in (d.get("capacity_deltas") or {}).items():
            merged["capacity_deltas"][k] = merged["capacity_deltas"].get(k, 0) + v
        for dom, dv in (d.get("domain_deltas") or {}).items():
            if dom not in merged["domain_deltas"]:
                merged["domain_deltas"][dom] = {"A": 0, "S": 0, "V": 0, "Aim": 0}
            for comp, delta in dv.items():
                if comp in merged["domain_deltas"][dom]:
                    merged["domain_deltas"][dom][comp] = merged["domain_deltas"][dom].get(comp, 0) + delta
        merged["alienation_delta"] += d.get("alienation_delta") or 0
        merged["coherence_delta"] += d.get("coherence_delta") or 0
        merged["stability_delta"] += d.get("stability_delta") or 0
        for k, v in (d.get("practice_deltas") or {}).items():
            merged["practice_deltas"][k] = merged["practice_deltas"].get(k, 0) + v
        for k, v in (d.get("wound_deltas") or {}).items():
            merged["wound_deltas"][k] = merged["wound_deltas"].get(k, 0) + v
    return merged


def apply_deltas_to_state(
    state: BackboneState,
    deltas: dict[str, Any],
    config: dict[str, Any],
    selected_events: list[dict[str, Any]] | None = None,
) -> None:
    """
    Apply merged delta dict to state. Respects v3config delta_caps; clamps after each block.
    For each selected event with kind epistemic_rupture, creates RuptureShard + MetabolizationProcess
    and sets plasticity_window. Mutates state in place.
    """
    caps = config.get("delta_caps") or {}
    cap_capacity = float(caps.get("capacity_fields", 20))
    cap_domain_A = float(caps.get("domain_A", 10))
    cap_domain_S = float(caps.get("domain_S", 10))
    cap_domain_V = float(caps.get("domain_V", 10))
    cap_alienation = float(caps.get("alienation", 15))
    cap_coherence = float(caps.get("coherence", 10))
    cap_practice = float(caps.get("practice_fields", 15))
    cap_stability = float(caps.get("stability", 10))

    # Stability-threshold inertia: apply merged stability_delta
    stab_delta = _cap_delta(deltas.get("stability_delta") or 0, cap_stability)
    if stab_delta != 0:
        state.stability_threshold_inertia = max(0.0, min(100.0, getattr(state, "stability_threshold_inertia", 0) + stab_delta))
        state.stability_delta_applied_this_year = True

    # Capacity
    for key, delta in (deltas.get("capacity_deltas") or {}).items():
        if hasattr(state.capacity, key):
            current = getattr(state.capacity, key)
            setattr(state.capacity, key, max(0, min(100, current + _cap_delta(delta, cap_capacity))))
    state.capacity.clamp_all()

    # Wound sensitization: wound_hooks → wound_vector field increments
    # Annual cap prevents runaway accumulation from a single bad year.
    cap_wound = float(caps.get("wound_fields", 8))
    wv = state.wound_vector
    for key, delta in (deltas.get("wound_deltas") or {}).items():
        if hasattr(wv, key):
            cur = float(getattr(wv, key))
            setattr(wv, key, max(0.0, min(100.0, cur + _cap_delta(delta, cap_wound))))
    state.wound_vector.clamp_all()

    # Domains
    for dom_name, comp_deltas in (deltas.get("domain_deltas") or {}).items():
        if dom_name not in state.domains:
            continue
        dom = state.domains[dom_name]
        for comp, delta in comp_deltas.items():
            if comp == "A":
                dom.A = max(0, min(100, dom.A + _cap_delta(delta, cap_domain_A)))
            elif comp == "S":
                dom.S = max(0, min(100, dom.S + _cap_delta(delta, cap_domain_S)))
            elif comp == "V":
                dom.V = max(0, min(100, dom.V + _cap_delta(delta, cap_domain_V)))
            elif comp == "Aim":
                dom.Aim = max(0, min(100, dom.Aim + _cap_delta(delta, cap_domain_A)))
        dom.clamp_all()

    # Alienation (vector + scalar in sync; delta shifts aggregate, all dimensions set to new aggregate)
    capped_al = _cap_delta(deltas.get("alienation_delta") or 0, cap_alienation)
    new_agg = max(0, min(100, state.alienation_vector.aggregate() + capped_al))
    v = state.alienation_vector
    v.structural = v.affective = v.institutional = new_agg
    state.alienation = new_agg

    # Coherence
    state.peak_routing.coherence = max(0, min(100, state.peak_routing.coherence + _cap_delta(deltas.get("coherence_delta") or 0, cap_coherence)))

    # Practice stack
    for key, delta in (deltas.get("practice_deltas") or {}).items():
        if hasattr(state.practice_stack, key):
            current = getattr(state.practice_stack, key)
            setattr(state.practice_stack, key, max(0, min(100, current + _cap_delta(delta, cap_practice))))
    state.practice_stack.clamp_all()

    events = selected_events or []
    # Reactivation bump: trauma events that match existing processes' triggers add to inertia
    trauma_kinds = ("puncture", "humiliation", "violence", "epistemic_rupture")
    for ev in events:
        kind = (ev.get("kind") or "").strip().lower()
        if kind not in trauma_kinds:
            continue
        # Event's stability_delta magnitude (same mapping as delta_from_event)
        intensity = (ev.get("intensity") or "major").strip().lower()
        ev_stab = 5
        if intensity == "minor":
            ev_stab = 3
        elif intensity == "shock":
            ev_stab = 8
        for proc in getattr(state, "metabolization_processes", []) or []:
            triggers = getattr(proc, "reactivation_triggers", []) or []
            domain = (ev.get("implicated") or {}).get("domains") or []
            dom_str = str(domain[0]).lower() if domain else ""
            kind_match = kind in [t.lower() for t in triggers]
            dom_match = dom_str and any(dom_str in str(t).lower() for t in triggers)
            if kind_match or dom_match:
                bump = 0.5 * min(cap_stability, abs(ev_stab))
                state.stability_threshold_inertia = max(0.0, min(100.0, state.stability_threshold_inertia + bump))
                break  # one bump per event (first matching process)
    for ev in events:
        if (ev.get("kind") or "").strip().lower() == "epistemic_rupture":
            from v3.engine.effects.metabolization_effects import create_rupture_shard_from_event
            create_rupture_shard_from_event(state, ev)
    # Expectation events: fulfillment/violation + striving_object_id -> GiftShard/DisruptionShard
    if events:
        from v3.engine.expectation_events import apply_gift_disruption_shards_from_events
        apply_gift_disruption_shards_from_events(state, events)

    state.clamp_all()


def build_state_deltas_applied_summary(
    deltas: dict[str, Any],
) -> dict[str, Any]:
    """Build a summary of applied deltas for RenderPacket (Pass 2 input)."""
    return {
        "capacity": deltas.get("capacity_deltas") or {},
        "domain_deltas": deltas.get("domain_deltas") or {},
        "alienation_delta": deltas.get("alienation_delta") or 0,
        "coherence_delta": deltas.get("coherence_delta") or 0,
        "practice_deltas": deltas.get("practice_deltas") or {},
        "wound_deltas": deltas.get("wound_deltas") or {},
    }
