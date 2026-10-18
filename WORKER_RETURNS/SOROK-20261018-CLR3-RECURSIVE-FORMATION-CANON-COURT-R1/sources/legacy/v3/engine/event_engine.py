# v3/engine/event_engine.py — sample 0–3 events per year conditioned on state/field.
# Events carry payloads for downstream steps (reproduction_deltas, capacity_deltas, etc.). No mutation of domains/peak_routing.

from __future__ import annotations

import sys
from pathlib import Path
from typing import Any

# Allow running as script: python3 v3/engine/event_engine.py (from repo root)
_root = Path(__file__).resolve().parent.parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices

MAX_EVENTS_PER_YEAR_DEFAULT = 3


def _pseudo_seed(state: BackboneState, year: int, slot: int) -> int:
    """Deterministic seed from state and year so runs are reproducible."""
    h = year * 1000 + slot * 37
    h += int(state.capacity.money) * 7 + int(state.capacity.time) * 11
    h += int(state.reproduction_constraints.job_insecurity) * 13
    h += int(state.alienation) * 17
    return h & 0x7FFFFFFF


def _one_event(state: BackboneState, derived: DerivedIndices, year: int, slot: int) -> dict[str, Any]:
    """Build one event with small deltas; type varies by slot so we get a mix over 0–3 events."""
    seed = _pseudo_seed(state, year, slot)
    kind = seed % 13  # event flavors
    event: dict[str, Any] = {
        "id": f"event_{year}_{slot}_{seed & 0xFFFF:04x}",
        "label": "",
        "source": "pseudo_random_mechanical",
        "conditioning_inputs": {
            "year": year,
            "slot": slot,
            "seed": seed,
            "capacity_money": round(float(state.capacity.money), 3),
            "capacity_time": round(float(state.capacity.time), 3),
            "job_insecurity": round(float(state.reproduction_constraints.job_insecurity), 3),
            "alienation": round(float(state.alienation), 3),
            "stability_threshold": round(float(getattr(derived, "stability_threshold", 0.0) or 0.0), 3),
            "insulation_score": round(float(getattr(derived, "insulation_score", 0.0) or 0.0), 3),
        },
    }

    # Small magnitudes so caps are respected and state moves gradually
    if kind == 0:
        event["reproduction_deltas"] = {
            "job_insecurity": (seed % 7) - 2,
            "debt": (seed % 5) - 1,
        }
    elif kind == 1:
        event["capacity_deltas"] = {
            "money": -((seed % 5) + 1),
            "time": (seed % 3) - 1,
        }
    elif kind == 2:
        event["alienation_delta"] = (seed % 5) - 1
    elif kind == 3 and state.domains:
        domain = DOMAIN_NAMES[(seed // 10) % len(DOMAIN_NAMES)]
        if domain in state.domains:
            event["domain_deltas"] = {
                domain: {"A": (seed % 5) - 2, "V": (seed % 4) - 1},
            }
    elif kind == 4 and state.cracks:
        n = len(state.cracks)
        event["crack_deltas"] = [
            {"intensity": (seed % 5) - 1, "latent_pressure": (seed % 4)} if i == (seed % n) else {}
            for i in range(n)
        ]
    elif kind == 5 and state.frameworks:
        n = len(state.frameworks)
        event["framework_deltas"] = [(seed % 5) - 2 if i == (seed % n) else 0 for i in range(n)]
    elif kind == 6:
        event["practice_deltas"] = {
            "organizing": (seed % 5) - 1,
            "craft": (seed % 4) - 1,
        }
    elif kind == 7:
        event["field_deltas"] = {
            "economy": (seed % 5) - 2,
            "repression_baseline": (seed % 4) - 1,
        }
    elif kind == 8:
        event["infrastructure_deltas"] = {
            "network_density": (seed % 5) - 1,
            "org_discipline": (seed % 4) - 1,
        }
    elif kind == 9:
        event["coherence_delta"] = (seed % 5) - 2
    elif kind == 10:
        event["loop_topology"] = ("reciprocal", "extractive", "self_contained")[(seed // 3) % 3]
    elif kind == 11:
        event["solidarity_boundary"] = ("none", "transactional", "in_group", "expanding", "universal")[(seed // 5) % 5]
    elif kind == 12:
        event["style_trait_deltas"] = {
            "playfulness": (seed % 5) - 2,
            "social_energy": (seed % 4) - 1,
        }

    label_lookup = {
        0: "reproduction pressure",
        1: "capacity squeeze",
        2: "alienation shift",
        3: "domain disturbance",
        4: "crack pressure",
        5: "framework tug",
        6: "practice nudge",
        7: "field pressure",
        8: "infrastructure drift",
        9: "coherence movement",
        10: "topology hint",
        11: "boundary hint",
        12: "style drift",
    }
    event["label"] = f"{label_lookup.get(kind, 'mechanical event')} (slot {slot + 1})"
    event["kind_label"] = label_lookup.get(kind, "mechanical event")
    return event


def sample_events(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Sample 0–max_events_per_year events; write to state.events_this_year. Does not mutate domains or peak_routing."""
    execution = config.get("execution") or {}
    max_events = int(execution.get("max_events_per_year", MAX_EVENTS_PER_YEAR_DEFAULT))
    max_events = max(0, min(10, max_events))

    # Deterministic count: some years 0, some 1–3, so state drifts over time
    year = state.year
    count_seed = (year * 31 + int(state.capacity.money) + int(state.alienation)) & 0x7FFFFFFF
    n_events = count_seed % (max_events + 1)

    events: list[dict[str, Any]] = []
    for slot in range(n_events):
        ev = _one_event(state, derived, year, slot)
        if ev:
            events.append(ev)
    state.events_this_year = events
    yearly = getattr(state, "yearly_integrity", None)
    if isinstance(yearly, dict):
        yearly["event_sampling"] = {
            "status": "ok",
            "source": "pseudo_random_mechanical",
            "event_count": len(events),
            "conditioning_year": year,
        }


def apply_puncture_counters(state: BackboneState, years_since_last_puncture: dict[str, int] | None = None) -> None:
    """Apply awareness puncture counters and transitions per domain.
    
    Called once per year. For each event this year with puncture_happened=True
    in a given domain, increment the domain's puncture_counter.
    At thresholds: 1→distorted, 2→partial, 3→structural.
    Regression: stored per-domain; 5 years no puncture → partial→distorted; 8 years→structural→partial.
    """
    from v3.core.enums import DOMAIN_NAMES
    for name in DOMAIN_NAMES:
        if name not in state.domains:
            continue
        domain = state.domains[name]
        # Count punctures this year
        fresh_punctures = 0
        for ev in (state.events_this_year or []):
            if isinstance(ev, dict):
                puncture = ev.get("puncture") or {}
                domains_hit = ev.get("implicated_domains") or []
                if name in domains_hit and puncture.get("happened"):
                    fresh_punctures += 1
        domain.puncture_counter += fresh_punctures
        # Awareness transitions (upward)
        counter = domain.puncture_counter
        current_awareness = domain.A
        if current_awareness < 25 and counter >= 1:
            domain.A = 30.0
        elif current_awareness < 50 and counter >= 2:
            domain.A = 55.0
        elif current_awareness < 75 and counter >= 3:
            domain.A = 80.0
        # Regression — persisted on domain
        if fresh_punctures == 0:
            domain.puncture_years_since_last += 1
        else:
            domain.puncture_years_since_last = 0
        yrs = domain.puncture_years_since_last
        if yrs >= 8 and current_awareness >= 75:
            domain.A = 65.0  # structural → partial
        elif yrs >= 5 and current_awareness >= 50 and domain.puncture_counter < 3:
            domain.A = 40.0  # partial → distorted if never reached structural


if __name__ == "__main__":
    from v3.core.derived import compute_all_derived
    from v3.core.config_loader import load_v3config
    state = BackboneState(year=2000, age=30)
    derived = compute_all_derived(state)
    config = load_v3config()
    sample_events(state, derived, config)
    print(f"year={state.year}  events={len(state.events_this_year)}")
    for i, ev in enumerate(state.events_this_year):
        print(f"  event {i}: {list(ev.keys())}")
