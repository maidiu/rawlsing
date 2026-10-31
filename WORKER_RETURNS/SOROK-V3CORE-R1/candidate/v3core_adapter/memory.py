"""Material-history memory without a conserved psychological charge.

The historical ``v3.psyche.flow._update_memory`` pattern (lifetime/recent
windows, totals, decayed grooves) is adapted here over recorded material
deltas. No need, wound or meaning is treated as a conserved numerical charge.
"""

from __future__ import annotations

from typing import Any, Iterable

from .contracts import YearRecord
from .provenance import digest


def update_material_memory(
    years: Iterable[YearRecord],
    previous_memory: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Return a transaction-safe material memory document.

    The function is pure: the caller commits the returned document only after
    the year record and projection state have both been accepted.
    """
    years = tuple(years)
    previous = previous_memory if isinstance(previous_memory, dict) else {}
    lifetime_cash = 0.0
    recent_cash = 0.0
    event_counts: dict[str, int] = {}
    source_events: list[str] = []
    for index, year in enumerate(years):
        for delta in year.material_deltas:
            if delta.field == "capacity.money":
                lifetime_cash += delta.delta
                if index >= max(0, len(years) - 5):
                    recent_cash += delta.delta
        for disposition in year.event_dispositions:
            event_counts[disposition.status.value] = event_counts.get(disposition.status.value, 0) + 1
            if disposition.durable_mutation:
                source_events.append(disposition.event_id)
    grooves = dict(previous.get("grooves") or {})
    for key in list(grooves):
        grooves[key] = round(float(grooves.get(key, 0.0)) * 0.985, 6)
    if source_events:
        grooves["material_accounting"] = round(
            float(grooves.get("material_accounting", 0.0)) + 1.0, 6
        )
    payload = {
        "schema": "SOROK_V3CORE_R1_MATERIAL_MEMORY@1",
        "cycles_recorded": len(years),
        "lifetime_cash_delta": round(lifetime_cash, 6),
        "recent_cash_delta": round(recent_cash, 6),
        "event_status_counts": event_counts,
        "durable_source_events": source_events,
        "grooves": grooves,
        "charge_conservation_assumed": False,
        "authority": "TEST_ONLY_MATERIAL_MEMORY_NOT_PSYCHOLOGICAL_CHARGE",
    }
    payload["memory_hash"] = digest(payload)
    return payload
