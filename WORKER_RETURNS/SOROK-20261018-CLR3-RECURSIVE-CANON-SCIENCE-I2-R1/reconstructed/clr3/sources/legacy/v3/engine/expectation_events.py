# v3/engine/expectation_events.py
# Expectation event templates (fulfillment/violation) and Gift/Disruption shard creation from selected events.

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

from v3.core.state import BackboneState, GiftShard, DisruptionShard


def load_expectation_event_templates() -> list[dict[str, Any]]:
    """Load expectation_event_templates.yaml; return list of template dicts. Empty if missing."""
    if yaml is None:
        logger.warning("generation degradation: yaml not available; expectation_event_templates disabled")
        return []
    for base in (Path(__file__).resolve().parent.parent, Path(__file__).resolve().parent):
        path = base / "expectation_event_templates.yaml"
        if path.exists():
            break
    else:
        logger.warning("generation degradation: expectation_event_templates.yaml not found; templates disabled")
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict):
            templates = data.get("templates")
            if isinstance(templates, list):
                return [t for t in templates if isinstance(t, dict)]
        logger.warning("generation degradation: expectation_event_templates.yaml has unexpected structure")
        return []
    except Exception as exc:
        logger.warning("generation degradation: expectation_event_templates.yaml failed to load: %s", exc)
        return []


def get_suggested_event_targets_for_summary(
    state_summary: dict,
    max_per_axis: int = 2,
    age: int | None = None,
) -> list[dict[str, Any]]:
    """
    Return suggested event targets from templates that match active strivings.
    Used to constrain/suggest Pass 1 event proposals: LLM sees these and can
    propose events that match (expectation_type + striving_object_id).
    """
    templates = load_expectation_event_templates()
    if not templates:
        return []
    strivings = state_summary.get("striving_objects") or []
    if not strivings:
        return []
    # need_axis -> list of striving ids (use first for suggestion)
    axis_to_ids: dict[str, list[str]] = {}
    for s in strivings:
        if isinstance(s, dict):
            aid = (s.get("need_axis") or "").strip()
            sid = (s.get("id") or "").strip()
        else:
            aid = (getattr(s, "need_axis", None) or "").strip()
            sid = (getattr(s, "id", None) or "").strip()
        if aid and sid:
            axis_to_ids.setdefault(aid, []).append(sid)
    out: list[dict[str, Any]] = []
    seen_axis_type: set[tuple[str, str]] = set()
    for t in templates:
        if not isinstance(t, dict):
            continue
        axis = (t.get("need_axis") or "").strip()
        typ = (t.get("type") or "").strip().lower()
        if typ not in ("fulfillment", "violation") or axis not in axis_to_ids:
            continue
        key = (axis, typ)
        if key in seen_axis_type:
            continue
        ids_for_axis = axis_to_ids[axis]
        if len([k for k in seen_axis_type if k[0] == axis]) >= max_per_axis * 2:
            continue
        seen_axis_type.add(key)
        out.append({
            "template_id": t.get("id", ""),
            "need_axis": axis,
            "expectation_type": typ,
            "targets": t.get("targets") or [],
            "striving_object_ids": ids_for_axis[:3],
            "notes": (t.get("notes") or "")[:200],
        })
    return out[:20]


# Alias for callers that use the shorter name
get_suggested_event_targets = get_suggested_event_targets_for_summary


def apply_gift_disruption_shards_from_events(
    state: BackboneState,
    selected_events: list[dict[str, Any]],
) -> None:
    """
    For each selected event with expectation_type (fulfillment|violation) and striving_object_id
    that matches an active striving, create GiftShard or DisruptionShard and append to state.
    """
    striving_ids = {s.id for s in (getattr(state, "striving_objects", None) or []) if getattr(s, "active", True)}
    for ev in selected_events:
        ex_type = (ev.get("expectation_type") or "").strip().lower()
        if ex_type not in ("fulfillment", "violation"):
            continue
        sid = (ev.get("striving_object_id") or "").strip()
        if not sid or sid not in striving_ids:
            continue
        # Find striving for need_axis and label
        need_axis = ""
        label = str(ev.get("label", ""))[:200] or "event"
        for s in state.striving_objects:
            if s.id == sid:
                need_axis = getattr(s, "need_axis", "") or ""
                break
        if ex_type == "fulfillment":
            shard_id = f"gs_{state.year}_{state.age}_{len(state.gift_shards)}"
            state.gift_shards.append(
                GiftShard(
                    id=shard_id,
                    year=state.year,
                    age=state.age,
                    need_axis=need_axis,
                    striving_object_id=sid,
                    label=label,
                    valence="positive",
                    prediction_error="medium",
                    opacity="low",
                )
            )
        else:
            # Malheur path: when violation targets a striving with high identity_load, mark malheur_risk
            identity_load = 50
            for s in state.striving_objects:
                if s.id == sid:
                    identity_load = getattr(s, "identity_load", 50)
                    break
            MALHEUR_IDENTITY_LOAD_THRESHOLD = 60
            malheur_risk = identity_load >= MALHEUR_IDENTITY_LOAD_THRESHOLD
            shard_id = f"ds_{state.year}_{state.age}_{len(state.disruption_shards)}"
            state.disruption_shards.append(
                DisruptionShard(
                    id=shard_id,
                    year=state.year,
                    age=state.age,
                    need_axis=need_axis,
                    striving_object_id=sid,
                    label=label,
                    valence="negative",
                    prediction_error="high" if malheur_risk else "medium",
                    opacity="high" if malheur_risk else "medium",
                    malheur_risk=malheur_risk,
                )
            )
