# v3/engine/run_llm_band.py
# Full LLM band year: Pass 1 (propose events) → score → apply deltas + rupture + magnets → Pass 2 (render).
# Call at band ages so the persona gets LLM-proposed events, ruptures, gifts/disruptions, and narrative.

from __future__ import annotations

import logging
import random
from typing import Any, Callable

logger = logging.getLogger(__name__)

from v3.core.derived import DerivedIndices, compute_all_derived
from v3.core.state import BackboneState
from v3.engine.effects.delta_templates import (
    apply_deltas_to_state,
    build_state_deltas_applied_summary,
    delta_from_event,
    delta_from_magnet,
    merge_deltas,
)
from v3.engine.expectation_events import get_suggested_event_targets
from v3.engine.llm_contract import (
    build_render_packet,
    parse_candidate_packet_with_fallback,
    state_summary_from_backbone,
)
from v3.engine.prompts import build_pass1_prompt, pass1_response_instruction
from v3.engine.scoring import select_candidates
from v3.engine.active_magnets import apply_selected_magnets_to_state
from v3.io.history_fetch import fetch_country_history
from v3.render.phenomenology import render_year

try:
    from v2.country_reference import normalize_country_ref
except Exception:  # pragma: no cover - fallback if v2 package unavailable
    normalize_country_ref = None  # type: ignore


def _llm_yearly_integrity(state: BackboneState) -> dict[str, Any]:
    yearly = getattr(state, "yearly_integrity", None)
    if not isinstance(yearly, dict):
        yearly = {}
        state.yearly_integrity = yearly
    bucket = yearly.get("llm_band")
    if not isinstance(bucket, dict):
        bucket = {}
        yearly["llm_band"] = bucket
    return bucket


def _capture_llm_mutation_snapshot(state: BackboneState) -> dict[str, Any]:
    return {
        "capacity": {k: getattr(state.capacity, k) for k in ("time", "money", "health", "social_support", "skill", "mobility", "risk_tolerance", "legitimacy")},
        "wound": {k: getattr(state.wound_vector, k) for k in ("shame", "fear", "anger", "abandonment", "control", "recognition", "loss")},
        "practice": {k: getattr(state.practice_stack, k) for k in ("study", "care", "organizing", "craft", "spiritual", "risk_training")},
        "domains": {
            name: {comp: getattr(dom, comp) for comp in ("A", "S", "V", "Aim", "latent_aim", "expressed_aim")}
            for name, dom in state.domains.items()
        },
        "alienation": float(getattr(state, "alienation", 0.0) or 0.0),
        "coherence": float(getattr(state.peak_routing, "coherence", 0.0) or 0.0),
        "stability_threshold_inertia": float(getattr(state, "stability_threshold_inertia", 0.0) or 0.0),
    }


def _build_llm_mutation_provenance(
    before: dict[str, Any],
    after: dict[str, Any],
    merged: dict[str, Any],
    selected_events: list[dict[str, Any]],
    selected_magnets: list[dict[str, Any]],
    *,
    selection_mode: str,
) -> list[dict[str, Any]]:
    event_ids = [str(ev.get("id") or "") for ev in selected_events if isinstance(ev, dict) and ev.get("id")]
    magnet_ids = [str(mg.get("id") or "") for mg in selected_magnets if isinstance(mg, dict) and mg.get("id")]
    template_ids = [str(ev.get("kind") or ev.get("label") or "event") for ev in selected_events if isinstance(ev, dict)]
    template_ids.extend(str(mg.get("magnet_type") or mg.get("label") or "magnet") for mg in selected_magnets if isinstance(mg, dict))
    confidence = 1.0 if selection_mode == "scored" else 0.75 if selection_mode == "fallback_first_candidate" else 0.55
    records: list[dict[str, Any]] = []

    def _append(target: str, before_value: Any, after_value: Any, delta: Any) -> None:
        if before_value == after_value:
            return
        records.append(
            {
                "field": target,
                "before": before_value,
                "after": after_value,
                "source": "llm_pass1",
                "event_id": event_ids if event_ids else None,
                "template_id": template_ids if template_ids else None,
                "magnet_id": magnet_ids if magnet_ids else None,
                "confidence": confidence,
                "delta": delta,
            }
        )

    for field_name, delta in (merged.get("capacity_deltas") or {}).items():
        _append(
            f"capacity.{field_name}",
            before.get("capacity", {}).get(field_name),
            after.get("capacity", {}).get(field_name),
            delta,
        )
    for dom_name, comp_deltas in (merged.get("domain_deltas") or {}).items():
        for comp, delta in comp_deltas.items():
            _append(
                f"domains.{dom_name}.{comp}",
                (before.get("domains", {}).get(dom_name) or {}).get(comp),
                (after.get("domains", {}).get(dom_name) or {}).get(comp),
                delta,
            )
    for field_name, delta in (merged.get("practice_deltas") or {}).items():
        _append(
            f"practice_stack.{field_name}",
            before.get("practice", {}).get(field_name),
            after.get("practice", {}).get(field_name),
            delta,
        )
    for field_name, delta in (merged.get("wound_deltas") or {}).items():
        _append(
            f"wound_vector.{field_name}",
            before.get("wound", {}).get(field_name),
            after.get("wound", {}).get(field_name),
            delta,
        )
    _append("alienation", before.get("alienation"), after.get("alienation"), merged.get("alienation_delta"))
    _append("peak_routing.coherence", before.get("coherence"), after.get("coherence"), merged.get("coherence_delta"))
    _append(
        "stability_threshold_inertia",
        before.get("stability_threshold_inertia"),
        after.get("stability_threshold_inertia"),
        merged.get("stability_delta"),
    )
    return records


def _set_llm_band_status(state: BackboneState, **payload: Any) -> dict[str, Any]:
    bucket = _llm_yearly_integrity(state)
    bucket.update(payload)
    return bucket


def run_llm_band_year(
    state: BackboneState,
    derived: DerivedIndices,
    config: dict[str, Any],
    *,
    identity_override: dict[str, Any] | None = None,
    llm_callback: Callable[[str, str], str],
    rng: random.Random | None = None,
    previous_scene: str | None = None,
) -> DerivedIndices:
    """
    Run full Pass 1 → select → apply deltas (incl. rupture + gift/disruption) → apply magnets →
    re-derive → Pass 2 (render). Uses state as-is (after run_one_year for this year).
    Returns updated derived.
    """
    rng = rng or random.Random()
    identity_override = identity_override or {}

    # Pass 1 input
    state_summary = state_summary_from_backbone(state, derived, identity_override)
    suggested = get_suggested_event_targets(state_summary)

    # Fetch historical backdrop for this country + year (cached per country+decade).
    # Injected into Pass 1 so proposed events are grounded in real conditions.
    _country_ref = normalize_country_ref(
        identity_override.get("country")
        or identity_override.get("country_code")
        or ""
    ) if normalize_country_ref else {}
    _country_for_history = (_country_ref.get("canonical_name") or "").strip()
    if not _country_for_history:
        _country_for_history = (
            identity_override.get("country")
            or identity_override.get("country_code")
            or ""
        )
    _historical_backdrop: str | None = None
    if _country_for_history:
        try:
            _historical_backdrop = fetch_country_history(_country_for_history, state.year)
            if _country_ref.get("fallback_used"):
                logger.debug(
                    "history normalization fallback used for %r -> %r",
                    identity_override.get("country") or identity_override.get("country_code"),
                    _country_for_history,
                )
        except Exception as _he:
            logger.debug("history_fetch failed for %r year=%s: %s", _country_for_history, state.year, _he)

    prompt = build_pass1_prompt(
        state_summary,
        suggested_event_targets=suggested,
        historical_backdrop=_historical_backdrop,
    ) + pass1_response_instruction()

    # Stage label used by server-side logging (ignored by simple callbacks).
    stage_label = f"llm_band_pass1_age_{state.age}"
    raw = llm_callback(stage_label, prompt)
    if not raw or not raw.strip():
        _set_llm_band_status(
            state,
            status="empty_response",
            selection_mode="none",
            derived_unchanged=True,
            source="llm_pass1",
            integrity_level="degraded",
        )
        return derived

    try:
        packet = parse_candidate_packet_with_fallback(raw, year=state.year, age=state.age)
    except Exception:
        _set_llm_band_status(
            state,
            status="parse_failed",
            selection_mode="none",
            derived_unchanged=True,
            source="llm_pass1",
            integrity_level="degraded",
        )
        return derived
    events = packet.get("event_candidates") or []
    magnets = packet.get("magnet_candidates") or []
    if not events and not magnets:
        _set_llm_band_status(
            state,
            status="no_candidates",
            selection_mode="none",
            derived_unchanged=True,
            source="llm_pass1",
            integrity_level="degraded",
        )
        return derived

    selected_events, selected_magnets = select_candidates(packet, state_summary, rng=rng)
    selection_mode = "scored"
    # If scoring discarded everything but we have candidates, take the first event so
    # Pass 2 always has something concrete to render rather than silently bailing out.
    if not selected_events and not selected_magnets:
        fallback_events = packet.get("event_candidates") or []
        fallback_magnets = packet.get("magnet_candidates") or []
        if fallback_events:
            selected_events = [fallback_events[0]]
            selection_mode = "fallback_first_candidate"
        elif fallback_magnets:
            selected_magnets = [fallback_magnets[0]]
            selection_mode = "fallback_first_candidate"
        else:
            _set_llm_band_status(
                state,
                status="scoring_bypass_no_fallback",
                selection_mode="none",
                derived_unchanged=True,
                source="llm_pass1",
                integrity_level="degraded",
            )
            return derived

    before_snapshot = _capture_llm_mutation_snapshot(state)
    try:
        deltas_list = [delta_from_event(ev, config) for ev in selected_events]
        deltas_list.extend([delta_from_magnet(mg, config) for mg in selected_magnets])
        merged = merge_deltas(deltas_list)
        apply_deltas_to_state(state, merged, config, selected_events=selected_events)
        apply_selected_magnets_to_state(state, selected_magnets, config)
        state.clamp_all()
        derived = compute_all_derived(state)
        after_snapshot = _capture_llm_mutation_snapshot(state)
        mutation_provenance = _build_llm_mutation_provenance(
            before_snapshot,
            after_snapshot,
            merged,
            selected_events,
            selected_magnets,
            selection_mode=selection_mode,
        )

        state_deltas_applied = build_state_deltas_applied_summary(merged)

        # Build persona_context for Pass 2: wound pattern, structural lucidity, strata position,
        # and rupture notes — all the information that makes the scene render from inside this person.
        _wv = getattr(state, "wound_vector", None) or {}
        def _wval(name: str) -> float:
            if isinstance(_wv, dict):
                return float(_wv.get(name, 50.0) or 50.0)
            return float(getattr(_wv, name, 50.0) or 50.0)

        _wound_names = ["shame", "fear", "anger", "abandonment", "control", "recognition", "loss"]
        _wound_pattern = {w: round(_wval(w), 1) for w in _wound_names if _wval(w) > 55.0}

        _sl = derived.structural_lucidity_SL if derived else 50.0
        if _sl < 5:
            _sl_label = "none — sees only personal causation, character, luck; cannot hold structural patterns"
        elif _sl < 20:
            _sl_label = "minimal — glimpses patterns but cannot sustain structural analysis; personal causation dominates"
        elif _sl < 40:
            _sl_label = "partial — aware of some structural forces, still mostly personal framing"
        elif _sl < 65:
            _sl_label = "moderate — can sometimes name structural forces"
        else:
            _sl_label = "high — able to name structural forces and locate self within them"

        _ses = str(identity_override.get("ses_band") or identity_override.get("class_origin") or "").replace("_", " ")
        _minority = str(identity_override.get("minority_status") or "")
        _country_name = str(identity_override.get("country") or identity_override.get("country_code") or "")
        _ethnicity = str(identity_override.get("ethnicity") or identity_override.get("ethnicity_label") or "")
        _strata_parts: list[str] = []
        if _ses:
            _strata_parts.append(_ses + " class")
        if "minorit" in _minority.lower():
            _strata_parts.append((_ethnicity + "-ethnic minority") if _ethnicity else "ethnic minority")
        if _country_name:
            _strata_parts.append("in " + _country_name)
        _strata_position = ", ".join(_strata_parts)

        _rupture_shards = getattr(state, "rupture_shards", None) or []
        _rupture_notes: list[str] = []
        for rs in _rupture_shards[:5]:
            if isinstance(rs, dict):
                assumption = rs.get("violated_assumption") or ""
                status = str(rs.get("current_status") or "")
                rs_age = rs.get("age") or ""
            else:
                assumption = getattr(rs, "violated_assumption", "") or ""
                status = str(getattr(rs, "current_status", "") or "")
                rs_age = getattr(rs, "age", None) or ""
            if not assumption:
                continue
            entry = f'"{assumption}"'
            if rs_age:
                entry = f"since age {rs_age}: {entry}"
            if "raw" in status.lower():
                entry += " [still raw]"
            _rupture_notes.append(entry)

        _persona_context: dict[str, Any] = {
            "structural_lucidity": _sl_label,
        }
        if _wound_pattern:
            _persona_context["wound_pattern"] = _wound_pattern
        if _strata_position:
            _persona_context["strata_position"] = _strata_position
        if _rupture_notes:
            _persona_context["rupture_notes"] = _rupture_notes

        # Build awareness gating from domain awareness states
        _awareness_gating: dict[str, str] = {}
        for _dname, _dstate in state.domains.items():
            _av = float(getattr(_dstate, "A", 0))
            _a_label = "unknown"
            if _av >= 75:
                _a_label = "structural"
            elif _av >= 50:
                _a_label = "partial"
            elif _av >= 25:
                _a_label = "distorted"
            if _a_label in ("distorted", "unknown"):
                _awareness_gating[_dname] = f"{_a_label} — structural thinking about this domain not available to them"
            elif _a_label == "partial":
                _awareness_gating[_dname] = f"{_a_label} — they sense contradictions but cannot name structural forces"

        render_packet = build_render_packet(
            state.year,
            state.age,
            selected_events,
            selected_magnets,
            state_deltas_applied,
            {},
            identity_override=identity_override,
            persona_context=_persona_context,
            previous_scene=previous_scene,
            awareness_gating=_awareness_gating,
            surface_psyche=getattr(state, "surface_psyche_profile", None),
        )
        render_year(state, derived, config, render_packet=render_packet, llm_callback=llm_callback)
        # Check render output integrity — pass2 placeholder scenes degrade the verdict
        rendered = getattr(state, "rendered_output", None) or {}
        render_integrity = rendered.get("_integrity") if isinstance(rendered, dict) else None
        narr = rendered.get("narrative_snapshot") if isinstance(rendered, dict) else {}
        scene_fallback = isinstance(narr, dict) and narr.get("pass2_scene_fallback")
        render_status = "applied"
        render_integrity_level = "degraded" if selection_mode == "fallback_first_candidate" else "clean"
        if scene_fallback or (isinstance(render_integrity, dict) and render_integrity.get("status") == "degraded"):
            render_status = "pass2_scene_fallback"
            render_integrity_level = "degraded"
        _set_llm_band_status(
            state,
            status=render_status,
            selection_mode=selection_mode,
            source="llm_pass1",
            derived_unchanged=False,
            candidate_counts={"events": len(events), "magnets": len(magnets)},
            selected_counts={"events": len(selected_events), "magnets": len(selected_magnets)},
            selected_event_ids=[ev.get("id") for ev in selected_events if isinstance(ev, dict) and ev.get("id")],
            selected_magnet_ids=[mg.get("id") for mg in selected_magnets if isinstance(mg, dict) and mg.get("id")],
            mutation_summary=state_deltas_applied,
            mutation_provenance=mutation_provenance,
            render_pass="pass2",
            render_integrity=render_integrity,
            integrity_level=render_integrity_level,
        )
    except Exception as _pass2_exc:
        logger.warning(
            "run_llm_band_year (age=%s): exception in delta/render block: %s",
            state.age,
            _pass2_exc,
            exc_info=True,
        )
        derived = compute_all_derived(state)
        _set_llm_band_status(
            state,
            status="mutation_or_render_failed",
            selection_mode=selection_mode,
            source="llm_pass1",
            derived_unchanged=False,
            integrity_level="degraded",
            error=_pass2_exc.__class__.__name__,
            error_message=str(_pass2_exc),
            candidate_counts={"events": len(events), "magnets": len(magnets)},
            selected_counts={"events": len(selected_events), "magnets": len(selected_magnets)},
            selected_event_ids=[ev.get("id") for ev in selected_events if isinstance(ev, dict) and ev.get("id")],
            selected_magnet_ids=[mg.get("id") for mg in selected_magnets if isinstance(mg, dict) and mg.get("id")],
            render_pass="pass2",
        )

    return derived
