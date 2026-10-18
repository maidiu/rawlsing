# v3/systems/domains.py — update domain A/S/V/Aim from events + insulation; apply delta caps.
# Structural lucidity (SL) is derived after this step from domain lucidity formula.

from __future__ import annotations

from typing import Any

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, clamp
from v3.core.derived import DerivedIndices

DOMAIN_FIELDS = ("A", "S", "V", "Aim")
DEFAULT_DELTA_CAP = 10


def _get_delta_cap(config: dict[str, Any], field: str) -> float:
    """Per-component annual delta cap (v3config delta_caps.domain_A, domain_S, etc.)."""
    caps = config.get("delta_caps") or {}
    key = f"domain_{field}"
    return float(caps.get(key, DEFAULT_DELTA_CAP))


def _apply_deltas(state: BackboneState, config: dict[str, Any]) -> None:
    """Apply event-driven deltas to each domain's A/S/V/Aim. Cap per component; clamp after."""
    for domain_name in DOMAIN_NAMES:
        if domain_name not in state.domains:
            continue
        d = state.domains[domain_name]
        deltas = {f: 0.0 for f in DOMAIN_FIELDS}
        for ev in state.events_this_year:
            if not isinstance(ev, dict):
                continue
            dd = ev.get("domain_deltas")
            if not isinstance(dd, dict) or domain_name not in dd:
                continue
            domain_ev = dd[domain_name]
            if not isinstance(domain_ev, dict):
                continue
            for f in DOMAIN_FIELDS:
                if f in domain_ev and isinstance(domain_ev[f], (int, float)):
                    deltas[f] += float(domain_ev[f])
        for f in DOMAIN_FIELDS:
            cap = _get_delta_cap(config, f)
            delta = max(-cap, min(cap, deltas[f]))
            current = getattr(d, f)
            setattr(d, f, clamp(current + delta))
        d.clamp_all()


def update_domains(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
) -> None:
    """Update domain A/S/V/Aim from events; apply annual delta caps. SL recomputed after this step."""
    _apply_deltas(state, config)
