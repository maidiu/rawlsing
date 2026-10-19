"""Relational-field mediation helpers for the canonical 9-strata stack.

The absolute horizon is represented as an internal-only projection, not a tenth stratum.
"""

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState, Stratum, clamp


def build_relational_field_projection(strata_stack: list[Stratum]) -> dict[str, Any]:
    """Summarize the existing 9-strata stack and attach an internal-only absolute horizon."""
    levels = [s.level for s in strata_stack]
    names = [s.name for s in strata_stack]
    relations: list[dict[str, Any]] = []
    for prev, cur in zip(strata_stack, strata_stack[1:], strict=False):
        relations.append(
            {
                "from_level": prev.level,
                "to_level": cur.level,
                "from_name": prev.name,
                "to_name": cur.name,
                "contrast": clamp(abs(cur.salience - prev.salience), 0.0, 100.0),
                "direction": "downstream" if cur.level > prev.level else "upstream",
            }
        )
    return {
        "status": "ok" if strata_stack else "blocked",
        "strata_count": len(strata_stack),
        "levels": levels,
        "names": names,
        "relations": relations,
        "absolute_horizon": {
            "status": "internal_only",
            "surface_export_allowed": False,
            "surface_label_allowed": False,
            "stratum_index": None,
            "notes": ["absolute_horizon_is_not_a_stratum"],
        },
    }


def apply_relational_field_to_state(state: BackboneState, relational_field: dict[str, Any] | None) -> None:
    """Attach relational projection to existing state surfaces without mutating strata_stack."""
    if not isinstance(relational_field, dict) or not relational_field:
        return
    summary = build_relational_field_projection(state.strata_stack)
    summary.update(
        {
            "status": str(relational_field.get("status") or summary.get("status") or "blocked"),
            "source": str(relational_field.get("source") or "relational_field_bridge"),
        }
    )
    if isinstance(relational_field.get("absolute_horizon"), dict):
        summary["absolute_horizon"] = dict(relational_field.get("absolute_horizon"))
    if isinstance(relational_field.get("projection"), dict):
        summary["projection"] = dict(relational_field.get("projection"))
    if isinstance(relational_field.get("notes"), list):
        summary["notes"] = [str(note) for note in relational_field.get("notes") if str(note).strip()]

    state.strata_salience["relational_field"] = summary
    state.strata_salience["absolute_horizon"] = summary.get("absolute_horizon", {})
    yearly = getattr(state, "yearly_integrity", None)
    if isinstance(yearly, dict):
        yearly["relational_field"] = {
            "status": summary.get("status", "blocked"),
            "surface_export_allowed": summary.get("absolute_horizon", {}).get("surface_export_allowed", False),
            "strata_count": summary.get("strata_count", 0),
        }
