# v3/engine/yearly_step.py — Run one year: execute steps in v3_yearly_step_order, compute derived after each scheduled step.

from __future__ import annotations

from typing import Any

from v3.core.state import BackboneState
from v3.core.derived import DerivedIndices, compute_all_derived
from v3.core.config_loader import get_step_list, get_execution, get_derived_schedule


def run_one_year(
    state: BackboneState,
    derived: DerivedIndices,
    v3config: dict[str, Any],
    step_order: dict[str, Any],
) -> None:
    """Execute all steps in order; recompute derived after steps that declare derived_compute; clamp after each step if config says so."""
    steps = get_step_list(step_order)
    execution = get_execution(step_order)
    derived_schedule = get_derived_schedule(step_order)
    clamp_after_each = execution.get("clamp_after_each_step", True)
    state.micro_trace_this_year = []
    state.yearly_integrity = {}
    # Spec §12: ensure min cracks/frameworks before steps (repair so invariants hold)
    inv_cfg = (v3config or {}).get("invariants") or {}
    if inv_cfg.get("repair_min_counts", True):
        from v3.core.invariants import ensure_min_cracks, ensure_min_frameworks
        ensure_min_cracks(state, v3config)
        ensure_min_frameworks(state, v3config)

    for step_spec in steps:
        step_id = step_spec.get("id")
        if not step_id:
            continue
        _run_step(step_id, state, derived, v3config)
        if step_id == "frameworks_update":
            try:
                from v3.systems.frameworks import enforce_framework_caps
                from v3.core.invariants import ensure_min_frameworks
                enforce_framework_caps(state)
                ensure_min_frameworks(state, v3config)
            except Exception:
                pass
        if clamp_after_each:
            state.clamp_all()
        # Flush generation diagnostics into rendered output for engine audit trail
        diags = getattr(state, "generation_diagnostics", None) or []
        if diags:
            ro = getattr(state, "rendered_output", None) or {}
            if isinstance(ro, dict):
                existing = ro.get("engine_diagnostics") or []
                ro["engine_diagnostics"] = existing + list(diags)
            state.rendered_output = ro
        _compute_derived_after_step(step_id, step_spec, state, derived, derived_schedule)
    state.year += 1
    state.age += 1
    # Apply awareness puncture counters per domain after events processed for the year
    try:
        from v3.engine.event_engine import apply_puncture_counters
        apply_puncture_counters(state)
    except Exception:
        pass
    # V515b.2 PressureFlow: one membrane-owned post-year psyche cycle.
    # Do not reintroduce direct calls to assign_sublimation_channels / compute_baseline_load /
    # apply_expression_gating / route_unexpressed_load here; flow.py owns ordering, audit, history,
    # diagnostics, and analyst/surface separation.
    try:
        from v3.psyche.flow import run_pressure_flow_cycle
        run_pressure_flow_cycle(state)
        state.clamp_all()
    except Exception as exc:
        pressure_flow_diag = None
        if isinstance(state.yearly_integrity, dict):
            pressure_flow_diag = state.yearly_integrity.get("pressure_flow")
        if pressure_flow_diag is None:
            pressure_flow_diag = {
                "stage": "pressure_flow",
                "status": "error",
                "fallback_used": False,
                "fallback_reason": "pressure_flow_cycle_failed",
                "fields_impacted": [
                    "pressure_flow_history",
                    "pressure_flow_memory",
                    "surface_psyche_profile",
                    "analyst_pressure_account",
                ],
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            }
            if hasattr(state, "generation_diagnostics"):
                state.generation_diagnostics.append(pressure_flow_diag)
            state.yearly_integrity["pressure_flow"] = pressure_flow_diag
        if not bool((v3config or {}).get("allow_pressure_flow_failure", False)):
            raise
    # Optional: assert backbone invariants after year (incl. expressed_aim gated)
    if inv_cfg.get("assert_after_year", False):
        from v3.core.invariants import assert_backbone_invariants
        assert_backbone_invariants(state, v3config, derived=derived, check_expressed_aim_gated=True)


def step_one_year(
    state: BackboneState,
    v3config: dict[str, Any],
    step_order: dict[str, Any],
    derived: DerivedIndices,
) -> DerivedIndices:
    """Run one year; return updated derived (state mutated in place). Convenience for tests and callers that want return value."""
    run_one_year(state, derived, v3config, step_order)
    return derived


def _run_step(
    step_id: str,
    state: BackboneState,
    derived: DerivedIndices,
    config: dict,
) -> None:
    """Dispatch to the correct step implementation."""
    from v3.systems import field, reproduction, capacity, buffers, frameworks, domains
    from v3.systems import cracks, alienation, practices, infrastructure, health_drift, autonomy_safety, stability_inertia
    from v3.systems import topology, boundary, coherence, attention, signal, style
    from v3.engine import active_magnets, event_engine, striving_objects
    from v3.render import phenomenology

    from v3.engine.effects.metabolization_effects import update_metabolization_and_plasticity_step
    runners = {
        "field_update": field.update_field,
        "autonomy_safety_micro_drift": autonomy_safety.autonomy_safety_micro_drift,
        "event_sampling": event_engine.sample_events,
        "reproduction_constraints_update": reproduction.update_reproduction_constraints,
        "capacity_update": capacity.update_capacity,
        "health_drift_update": health_drift.update_health_drift,
        "buffers_update": buffers.update_buffers,
        "frameworks_update": frameworks.update_framework_weights,
        "domains_update": domains.update_domains,
        "cracks_and_alienation_update": _run_cracks_and_alienation,
        "plasticity_and_metabolization_update": update_metabolization_and_plasticity_step,
        "stability_inertia_dissipation": stability_inertia.stability_inertia_dissipation,
        "practice_and_infrastructure_update": _run_practice_and_infrastructure,
        "topology_and_boundary_update": _run_topology_and_boundary,
        "attention_and_capture_update": attention.update_attention_and_capture,
        "strategy_and_signal_effects": signal.apply_signal_effects,
        "style_trait_drift": style.update_style_traits,
        "render_layer": phenomenology.render_year,
        "striving_update": striving_objects.update_striving_step,
        "active_magnets_update": active_magnets.update_active_magnets_step,
    }
    fn = runners.get(step_id)
    if fn is not None:
        fn(state, derived, config)


def _run_cracks_and_alienation(state: BackboneState, derived: DerivedIndices, config: dict) -> None:
    from v3.systems import cracks, alienation
    cracks.update_cracks(state, derived, config)
    alienation.update_alienation(state, derived, config)


def _run_practice_and_infrastructure(state: BackboneState, derived: DerivedIndices, config: dict) -> None:
    from v3.systems import practices, infrastructure
    practices.update_practice_stack(state, derived, config)
    infrastructure.update_collective_infrastructure(state, derived, config)


def _run_topology_and_boundary(state: BackboneState, derived: DerivedIndices, config: dict) -> None:
    from v3.systems import topology, boundary, coherence
    topology.update_loop_topology(state, derived, config)
    boundary.update_solidarity_boundary(state, derived, config)
    coherence.update_coherence(state, derived, config)


def _compute_derived_after_step(
    step_id: str,
    step_spec: dict,
    state: BackboneState,
    derived: DerivedIndices,
    derived_schedule: dict[str, dict[str, Any]],
) -> None:
    """Recompute derived indices scheduled for this step and validate against step-local declarations."""
    compute_after = [name for name, spec in derived_schedule.items() if (spec or {}).get("compute_after_step") == step_id]
    declared = [str(x) for x in (step_spec.get("derived_compute") or [])]
    if set(compute_after) != set(declared):
        raise AssertionError(
            f"derived schedule mismatch for step {step_id!r}: step-local={declared} schedule={compute_after}"
        )
    if not compute_after:
        return
    new_derived = compute_all_derived(state)
    for field_name in compute_after:
        _copy_derived_field(field_name, new_derived, derived)


def _copy_derived_field(field_name: str, src: DerivedIndices, dst: DerivedIndices) -> None:
    if field_name == "metabolic_style":
        dst.metabolic_style_current = src.metabolic_style_current
        dst.metabolic_style_trend = src.metabolic_style_trend
        return
    if hasattr(dst, field_name) and hasattr(src, field_name):
        setattr(dst, field_name, getattr(src, field_name))
