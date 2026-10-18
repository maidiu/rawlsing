# v3/io/json_codec.py
# Serialize / deserialize BackboneState to JSON. Clamp on load.

from __future__ import annotations

import json
from typing import Any

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import (
    AlienationVector,
    AppetiteProfile,
    BackboneState,
    BoundaryMapEntry,
    Buffer,
    BufferCostProfile,
    CalibrationRegime,
    Capacity,
    CollectiveInfrastructure,
    Crack,
    DisruptionShard,
    DomainState,
    GiftShard,
    MacroField,
    Framework,
    IntensityAndCapture,
    Magnet,
    MetabolizationProcess,
    NarrationSupport,
    PeakRouting,
    PracticeStack,
    PsychologicalCapacity,
    Registers,
    ReproductionConstraints,
    RuptureShard,
    Stratum,
    StrivingObject,
    StyleTraits,
    WoundVector,
    clamp,
)


def _state_to_dict(obj: Any) -> Any:
    if hasattr(obj, "__dataclass_fields__"):
        return {k: _state_to_dict(getattr(obj, k)) for k in obj.__dataclass_fields__}
    if isinstance(obj, dict):
        return {k: _state_to_dict(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_state_to_dict(v) for v in obj]
    return obj


def _dict_to_domain_state(d: dict[str, Any]) -> DomainState:
    return DomainState(
        A=clamp(float(d.get("A", 0))),
        S=clamp(float(d.get("S", 0))),
        V=clamp(float(d.get("V", 0))),
        Aim=clamp(float(d.get("Aim", 0))),
        latent_aim=clamp(float(d.get("latent_aim", 0))),
        expressed_aim=clamp(float(d.get("expressed_aim", 0))),
        baseline_load=clamp(float(d.get("baseline_load", 0))),
        expression_rate=clamp(float(d.get("expression_rate", 50))),
        activation_threshold=clamp(float(d.get("activation_threshold", 80))),
        affect_channel=str(d.get("affect_channel", "compartmentalization")),
        buffer_type=str(d.get("buffer_type", "")),
        puncture_counter=int(d.get("puncture_counter", 0)),
        puncture_years_since_last=int(d.get("puncture_years_since_last", 0)),
    )


def _dict_to_magnet(d: dict[str, Any]) -> Magnet:
    return Magnet(
        id=str(d.get("id", ""))[:80],
        magnet_type=str(d.get("magnet_type", "friend"))[:40],
        label=str(d.get("label", ""))[:200],
        intensity=clamp(float(d.get("intensity", 50))),
        tenure_years=max(0, int(d.get("tenure_years", 0))),
    )


def _dict_to_alienation_vector(d: dict[str, Any] | None, scalar_alienation: float = 0.0) -> AlienationVector:
    """Build AlienationVector from dict; if missing use scalar for all dimensions."""
    if d and isinstance(d, dict):
        return AlienationVector(
            distant_others=clamp(float(d.get("distant_others", scalar_alienation))),
            near_others=clamp(float(d.get("near_others", scalar_alienation))),
            self=clamp(float(d.get("self", scalar_alienation))),
            moral_totality=clamp(float(d.get("moral_totality", scalar_alienation))),
        )
    return AlienationVector(distant_others=scalar_alienation, near_others=scalar_alienation, self=scalar_alienation, moral_totality=scalar_alienation)


def _dict_to_registers(d: dict[str, Any]) -> Registers:
    return Registers(
        public_expression_gate=clamp(float(d.get("public_expression_gate", 50))),
        private_expression_gate=clamp(float(d.get("private_expression_gate", 50))),
        inner_load=clamp(float(d.get("inner_load", 50))),
    )


def _dict_to_crack(d: dict[str, Any]) -> Crack:
    return Crack(
        type=str(d.get("type", "shame_core")),
        intensity=clamp(float(d.get("intensity", 0))),
        latent_pressure=clamp(float(d.get("latent_pressure", 0))),
        active=bool(d.get("active", False)),
        origin_year=int(d.get("origin_year", 0)),
    )


def _dict_to_buffer_cost(d: dict[str, Any]) -> BufferCostProfile:
    return BufferCostProfile(
        time_cost=clamp(float(d.get("time_cost", 0))),
        money_cost=clamp(float(d.get("money_cost", 0))),
        relational_cost=clamp(float(d.get("relational_cost", 0))),
        truth_cost=clamp(float(d.get("truth_cost", 0))),
    )


def _dict_to_buffer(d: dict[str, Any]) -> Buffer:
    cp = d.get("cost_profile")
    return Buffer(
        type=str(d.get("type", "craft")),
        strength=clamp(float(d.get("strength", 0))),
        cost_profile=_dict_to_buffer_cost(cp) if isinstance(cp, dict) else BufferCostProfile(),
    )


def _dict_to_framework(d: dict[str, Any]) -> Framework:
    acute = d.get("acute_delta")
    chronic = d.get("chronic_delta")
    return Framework(
        id=str(d.get("id", "")),
        weight=clamp(float(d.get("weight", 0))),
        acute_delta=dict(acute) if isinstance(acute, dict) else {},
        chronic_delta=dict(chronic) if isinstance(chronic, dict) else {},
        half_life_years=int(d.get("half_life_years", 0)),
        failure_mode=str(d.get("failure_mode", "")),
        enemy_requirement=clamp(float(d.get("enemy_requirement", 0))),
        institutional_affinities=[str(x) for x in (d.get("institutional_affinities") or []) if x],
        tenure_years=int(d.get("tenure_years", 0)),
    )


def _dict_to_appetite(d: dict[str, Any]) -> AppetiteProfile:
    return AppetiteProfile(
        status=clamp(float(d.get("status", 0))),
        control=clamp(float(d.get("control", 0))),
        sensuality=clamp(float(d.get("sensuality", 0))),
        care=clamp(float(d.get("care", 0))),
    )


def _dict_to_peak_routing(d: dict[str, Any]) -> PeakRouting:
    ap = d.get("appetite_profile")
    thy = d.get("topology_hysteresis_years")
    if isinstance(thy, dict):
        thy = {str(k): int(v) for k, v in thy.items() if isinstance(v, (int, float))}
    else:
        thy = {}
    return PeakRouting(
        loop_topology=str(d.get("loop_topology", "self_contained")),
        solidarity_boundary=str(d.get("solidarity_boundary", "in_group")),
        harm_constraint=clamp(float(d.get("harm_constraint", 50))),
        rage_metabolization=clamp(float(d.get("rage_metabolization", 50))),
        theory_of_change_style=str(d.get("theory_of_change_style", "institution_building")),
        coherence=clamp(float(d.get("coherence", 50))),
        impunity_access=clamp(float(d.get("impunity_access", 0))),
        appetite_profile=_dict_to_appetite(ap) if isinstance(ap, dict) else AppetiteProfile(),
        topology_hysteresis_years=thy,
    )


def _dict_to_psychological_capacity(d: dict[str, Any]) -> PsychologicalCapacity:
    return PsychologicalCapacity(
        vitality=clamp(float(d.get("vitality", 50))),
        aperture=clamp(float(d.get("aperture", 50))),
        reality_anchor=clamp(float(d.get("reality_anchor", 50))),
        binding=clamp(float(d.get("binding", 50))),
        coherence=clamp(float(d.get("coherence", 50))),
        agency=clamp(float(d.get("agency", 50))),
        transmutation=clamp(float(d.get("transmutation", 50))),
    )


def _dict_to_wound_vector(d: dict[str, Any]) -> WoundVector:
    channels = d.get("default_coping_channels")
    if isinstance(channels, list):
        channels = [str(x) for x in channels[:20] if isinstance(x, str)]
    else:
        channels = ["withdraw", "intellectualize"]
    return WoundVector(
        shame=clamp(float(d.get("shame", 50))),
        fear=clamp(float(d.get("fear", 50))),
        anger=clamp(float(d.get("anger", 50))),
        abandonment=clamp(float(d.get("abandonment", 50))),
        control=clamp(float(d.get("control", 50))),
        recognition=clamp(float(d.get("recognition", 50))),
        loss=clamp(float(d.get("loss", 50))),
        default_coping_channels=channels,
    )


def _dict_to_intensity_capture(d: dict[str, Any]) -> IntensityAndCapture:
    return IntensityAndCapture(
        intensity=clamp(float(d.get("intensity", 50))),
        craft_talent=clamp(float(d.get("craft_talent", 0))),
        opportunity_access=clamp(float(d.get("opportunity_access", 0))),
        attention_field_exposure=clamp(float(d.get("attention_field_exposure", 0))),
        capture_pressure=clamp(float(d.get("capture_pressure", 0))),
    )


def _dict_to_style_traits(d: dict[str, Any]) -> StyleTraits:
    return StyleTraits(
        playfulness=clamp(float(d.get("playfulness", 50))),
        novelty_seeking=clamp(float(d.get("novelty_seeking", 50))),
        conscientiousness=clamp(float(d.get("conscientiousness", 50))),
        social_energy=clamp(float(d.get("social_energy", 50))),
        absurdist_humor=clamp(float(d.get("absurdist_humor", 50))),
        aesthetic_sensitivity=clamp(float(d.get("aesthetic_sensitivity", 50))),
        impulsivity=clamp(float(d.get("impulsivity", 50))),
    )


def _dict_to_stratum(d: dict[str, Any]) -> Stratum:
    return Stratum(
        level=int(d.get("level", 0)),
        name=str(d.get("name", ""))[:80],
        description=str(d.get("description", ""))[:200],
        material_relation=str(d.get("material_relation", "intermediary"))[:80],
        hegemonic_story=str(d.get("hegemonic_story", ""))[:500],
        loyalty_demand=str(d.get("loyalty_demand", ""))[:500],
        provision_strength=clamp(float(d.get("provision_strength", d.get("provision", 50)))),
        coercion_strength=clamp(float(d.get("coercion_strength", d.get("coercion", 50)))),
        contradiction_load=clamp(float(d.get("contradiction_load", d.get("contradiction", 50)))),
        visibility_of_complicity=clamp(float(d.get("visibility_of_complicity", 50))),
        salience=clamp(float(d.get("salience", 50))),
    )


def _dict_to_calibration_regime(d: dict[str, Any] | None) -> CalibrationRegime | None:
    if not d or not isinstance(d, dict):
        return None
    penalties = d.get("outlier_penalties")
    incentives = d.get("outlier_incentives")
    if not isinstance(penalties, list):
        penalties = []
    if not isinstance(incentives, list):
        incentives = []
    return CalibrationRegime(
        norm_center=str(d.get("norm_center", "middle"))[:200],
        uniqueness_norm=clamp(float(d.get("uniqueness_norm", 50))),
        outlier_penalties=[x for x in penalties if isinstance(x, dict)][:50],
        outlier_incentives=[x for x in incentives if isinstance(x, dict)][:50],
        dream_window=str(d.get("dream_window", ""))[:500],
    )


def _dict_to_boundary_map_entry(d: dict[str, Any]) -> BoundaryMapEntry:
    return BoundaryMapEntry(
        discouraged=[str(x) for x in (d.get("discouraged") or []) if isinstance(x, str)][:50],
        permitted=[str(x) for x in (d.get("permitted") or []) if isinstance(x, str)][:50],
        incentivized=[str(x) for x in (d.get("incentivized") or []) if isinstance(x, str)][:50],
        trigger_conditions=[x for x in (d.get("trigger_conditions") or []) if isinstance(x, dict)][:20],
    )


def _dict_to_striving_object(d: dict[str, Any]) -> StrivingObject:
    tags = d.get("tags")
    if isinstance(tags, list):
        tags = [str(x) for x in tags[:30] if isinstance(x, str)]
    else:
        tags = []
    costs = d.get("costs")
    if isinstance(costs, list):
        costs = [str(x) for x in costs[:20] if isinstance(x, str)]
    else:
        costs = []
    return StrivingObject(
        id=str(d.get("id", ""))[:80],
        label=str(d.get("label", ""))[:200],
        need_axis=str(d.get("need_axis", ""))[:80],
        started_age=int(d.get("started_age", 0)),
        investment=max(0, min(100, int(d.get("investment", 50)))),
        identity_load=max(0, min(100, int(d.get("identity_load", 50)))),
        feasibility_belief=max(0, min(100, int(d.get("feasibility_belief", 50)))),
        social_support=max(0, min(100, int(d.get("social_support", 50)))),
        recent_momentum=max(-50, min(50, int(d.get("recent_momentum", 0)))),
        tags=tags,
        secrecy=max(0, min(100, int(d.get("secrecy", 0)))),
        costs=costs,
        active=bool(d.get("active", True)),
    )


def _dict_to_gift_shard(d: dict[str, Any]) -> GiftShard:
    return GiftShard(
        id=str(d.get("id", ""))[:80],
        year=int(d.get("year", 0)),
        age=int(d.get("age", 0)),
        need_axis=str(d.get("need_axis", ""))[:80],
        striving_object_id=str(d.get("striving_object_id", ""))[:80],
        label=str(d.get("label", ""))[:200],
        valence=str(d.get("valence", "positive"))[:20],
        prediction_error=str(d.get("prediction_error", "medium"))[:20],
        opacity=str(d.get("opacity", "low"))[:20],
    )


def _dict_to_disruption_shard(d: dict[str, Any]) -> DisruptionShard:
    return DisruptionShard(
        id=str(d.get("id", ""))[:80],
        year=int(d.get("year", 0)),
        age=int(d.get("age", 0)),
        need_axis=str(d.get("need_axis", ""))[:80],
        striving_object_id=str(d.get("striving_object_id", ""))[:80],
        label=str(d.get("label", ""))[:200],
        valence=str(d.get("valence", "negative"))[:20],
        prediction_error=str(d.get("prediction_error", "medium"))[:20],
        opacity=str(d.get("opacity", "medium"))[:20],
        malheur_risk=bool(d.get("malheur_risk", False)),
    )


def _dict_to_rupture_shard(d: dict[str, Any]) -> RuptureShard:
    meaning = d.get("meaning_attempts")
    if isinstance(meaning, list):
        meaning = [str(x) for x in meaning[:50] if isinstance(x, str)]
    else:
        meaning = []
    return RuptureShard(
        id=str(d.get("id", ""))[:80],
        year=int(d.get("year", 0)),
        age=int(d.get("age", 0)),
        violated_assumption=str(d.get("violated_assumption", ""))[:500],
        domain=str(d.get("domain", ""))[:80],
        opacity=str(d.get("opacity", "medium"))[:20],
        prediction_error=str(d.get("prediction_error", "medium"))[:20],
        current_status=str(d.get("current_status", "raw"))[:30],
        intrusive_return_rate=max(0, min(100, int(d.get("intrusive_return_rate", 50)))),
        meaning_attempts=meaning,
    )


def _dict_to_narration_support(d: dict[str, Any] | None) -> NarrationSupport | None:
    """Deserialize NarrationSupport; return None if d is not a dict."""
    if not d or not isinstance(d, dict):
        return None
    return NarrationSupport(
        availability=max(0, min(100, int(d.get("availability", 50)))),
        accuracy=max(0, min(100, int(d.get("accuracy", 50)))),
        warmth=max(0, min(100, int(d.get("warmth", 50)))),
        coercion=max(0, min(100, int(d.get("coercion", 50)))),
    )


def _dict_to_metabolization_process(d: dict[str, Any]) -> MetabolizationProcess:
    narrators = d.get("narrators")
    if isinstance(narrators, list):
        narrators = [str(x) for x in narrators[:20] if isinstance(x, str)]
    else:
        narrators = []
    triggers = d.get("reactivation_triggers")
    if isinstance(triggers, list):
        triggers = [str(x) for x in triggers[:30] if isinstance(x, str)]
    else:
        triggers = []
    biases = d.get("downstream_biases")
    if isinstance(biases, dict):
        biases = {str(k): v for k, v in list(biases.items())[:50]}
    else:
        biases = {}
    return MetabolizationProcess(
        id=str(d.get("id", ""))[:80],
        start_year=int(d.get("start_year", 0)),
        start_age=int(d.get("start_age", 0)),
        domain=str(d.get("domain", ""))[:80],
        violated_assumption=str(d.get("violated_assumption", ""))[:500],
        severity=str(d.get("severity", "major"))[:20],
        opacity=str(d.get("opacity", "medium"))[:20],
        prediction_error=str(d.get("prediction_error", "medium"))[:20],
        mode=str(d.get("mode", "accommodation"))[:30],
        status=str(d.get("status", "raw"))[:30],
        cluster=str(d.get("cluster", ""))[:60],
        plasticity_years_left=max(0, int(d.get("plasticity_years_left", 0))),
        intrusive_return_rate=max(0, min(100, int(d.get("intrusive_return_rate", 50)))),
        intrusive_return_rate_prev=max(0, min(100, int(d.get("intrusive_return_rate_prev", 50)))),
        narrators=narrators,
        provisional_frame=str(d["provisional_frame"])[:80] if d.get("provisional_frame") else None,
        downstream_biases=biases,
        reactivation_triggers=triggers,
        sealed_candidate_years=max(0, int(d.get("sealed_candidate_years", 0))),
        post_plasticity_years=max(0, int(d.get("post_plasticity_years", 0))),
        start_plasticity_years=max(0, int(d.get("start_plasticity_years", 0))),
    )


def state_to_dict(state: BackboneState) -> dict[str, Any]:
    """Serialize BackboneState to a JSON-serializable dict (for hashing/comparison)."""
    return _state_to_dict(state)


def state_to_json(state: BackboneState, indent: int | None = 2) -> str:
    """Serialize BackboneState to JSON string."""
    d = _state_to_dict(state)
    return json.dumps(d, indent=indent)


def _derive_psychological_from_material(cap: Capacity, pr_dict: dict, intensity: float = 50.0) -> PsychologicalCapacity:
    """Derive psychological capacity from material + peak_routing when not stored (e.g. old JSON)."""
    return PsychologicalCapacity(
        vitality=(cap.health + cap.social_support) / 2.0,
        aperture=intensity,
        reality_anchor=(cap.health + 50) / 2.0,
        binding=cap.social_support,
        coherence=float(pr_dict.get("coherence", 50)),
        agency=50.0,  # AC not available at load; step will not overwrite psychological_capacity
        transmutation=float(pr_dict.get("rage_metabolization", 50)),
    )


def state_from_dict(d: dict[str, Any]) -> BackboneState:
    """Deserialize BackboneState from dict (e.g. json.load). Clamps numerics."""
    cap = d.get("capacity") or {}
    cap_obj = Capacity(
        time=clamp(float(cap.get("time", 50))),
        money=clamp(float(cap.get("money", 50))),
        health=clamp(float(cap.get("health", 50))),
        social_support=clamp(float(cap.get("social_support", 50))),
        skill=clamp(float(cap.get("skill", 50))),
        mobility=clamp(float(cap.get("mobility", 50))),
        risk_tolerance=clamp(float(cap.get("risk_tolerance", 50))),
        legitimacy=clamp(float(cap.get("legitimacy", 50))),
    )
    pr = d.get("peak_routing") or {}
    psych = d.get("psychological_capacity")
    if isinstance(psych, dict):
        psych_cap = _dict_to_psychological_capacity(psych)
    else:
        ic = d.get("intensity_and_capture") or {}
        psych_cap = _derive_psychological_from_material(
            cap_obj,
            pr if isinstance(pr, dict) else {},
            intensity=clamp(float(ic.get("intensity", 50))),
        )
    cal = d.get("calibration_regime")
    calibration_regime = _dict_to_calibration_regime(cal) if cal else None
    bmap_raw = d.get("boundary_map")
    if isinstance(bmap_raw, dict):
        boundary_map = {str(k): _dict_to_boundary_map_entry(v) for k, v in bmap_raw.items() if isinstance(v, dict)}
    else:
        boundary_map = {}
    av = _dict_to_alienation_vector(
        d.get("alienation_vector") if isinstance(d.get("alienation_vector"), dict) else None,
        clamp(float(d.get("alienation", 0))),
    )
    state = BackboneState(
        year=int(d.get("year", 0)),
        age=int(d.get("age", 0)),
        field=MacroField(
            raw=((d.get("field") or {}).get("raw") if isinstance(d.get("field"), dict) and isinstance((d.get("field") or {}).get("raw"), dict) else (d.get("field") if isinstance(d.get("field"), dict) else {})),
            provenance=((d.get("field") or {}).get("provenance") if isinstance(d.get("field"), dict) and isinstance((d.get("field") or {}).get("provenance"), dict) else {}),
        ),
        calibration_regime=calibration_regime,
        boundary_map=boundary_map,
        strata_salience=d.get("strata_salience") if isinstance(d.get("strata_salience"), dict) else {},
        strata_stack=[_dict_to_stratum(x) for x in (d.get("strata_stack") or []) if isinstance(x, dict)],
        events_this_year=list(d.get("events_this_year") or []),
        micro_trace_this_year=list(d.get("micro_trace_this_year") or []),
        capacity=cap_obj,
        psychological_capacity=psych_cap,
        reproduction_constraints=ReproductionConstraints(
            dependents=clamp(float((d.get("reproduction_constraints") or {}).get("dependents", 0))),
            housing_insecurity=clamp(float((d.get("reproduction_constraints") or {}).get("housing_insecurity", 0))),
            # Field is "legal_status" (100 = secure) in the dataclass; old snapshots may store
            # "legal_insecurity" (0 = secure) — handle both, converting insecurity → status.
            legal_status=clamp(
                float((d.get("reproduction_constraints") or {}).get("legal_status", 0))
                or (100.0 - clamp(float((d.get("reproduction_constraints") or {}).get("legal_insecurity", 0))))
            ),
            debt=clamp(float((d.get("reproduction_constraints") or {}).get("debt", 0))),
            job_insecurity=clamp(float((d.get("reproduction_constraints") or {}).get("job_insecurity", 0))),
            caregiving_load=clamp(float((d.get("reproduction_constraints") or {}).get("caregiving_load", 0))),
        ),
        domains={},
        alienation=clamp(av.aggregate()),
        alienation_vector=av,
        wound_vector=_dict_to_wound_vector(d.get("wound_vector") or {}),
        cracks=[_dict_to_crack(x) for x in (d.get("cracks") or []) if isinstance(x, dict)],
        buffers=[_dict_to_buffer(x) for x in (d.get("buffers") or []) if isinstance(x, dict)],
        frameworks=[_dict_to_framework(x) for x in (d.get("frameworks") or []) if isinstance(x, dict)],
        frameworks_dormant=[dict(x) for x in (d.get("frameworks_dormant") or []) if isinstance(x, dict)],
        collective_infrastructure=CollectiveInfrastructure(
            network_density=clamp(float((d.get("collective_infrastructure") or {}).get("network_density", 0))),
            org_discipline=clamp(float((d.get("collective_infrastructure") or {}).get("org_discipline", 0))),
            resource_pool=clamp(float((d.get("collective_infrastructure") or {}).get("resource_pool", 0))),
            repression_pressure=clamp(float((d.get("collective_infrastructure") or {}).get("repression_pressure", 0))),
            elite_splits=clamp(float((d.get("collective_infrastructure") or {}).get("elite_splits", 0))),
        ),
        practice_stack=PracticeStack(
            study=clamp(float((d.get("practice_stack") or {}).get("study", 0))),
            care=clamp(float((d.get("practice_stack") or {}).get("care", 0))),
            organizing=clamp(float((d.get("practice_stack") or {}).get("organizing", 0))),
            craft=clamp(float((d.get("practice_stack") or {}).get("craft", 0))),
            spiritual=clamp(float((d.get("practice_stack") or {}).get("spiritual", 0))),
            risk_training=clamp(float((d.get("practice_stack") or {}).get("risk_training", 0))),
        ),
        peak_routing=_dict_to_peak_routing(d.get("peak_routing") or {}),
        intensity_and_capture=_dict_to_intensity_capture(d.get("intensity_and_capture") or {}),
        style_traits=_dict_to_style_traits(d.get("style_traits") or {}),
        rendered_output=d.get("rendered_output") if isinstance(d.get("rendered_output"), dict) else None,
        rupture_shards=[_dict_to_rupture_shard(x) for x in (d.get("rupture_shards") or []) if isinstance(x, dict)],
        metabolization_processes=[_dict_to_metabolization_process(x) for x in (d.get("metabolization_processes") or []) if isinstance(x, dict)],
        initial_state_provenance=dict(d.get("initial_state_provenance") or {}) if isinstance(d.get("initial_state_provenance"), dict) else {},
        yearly_integrity=dict(d.get("yearly_integrity") or {}) if isinstance(d.get("yearly_integrity"), dict) else {},
        pressure_flow_history=[dict(x) for x in (d.get("pressure_flow_history") or []) if isinstance(x, dict)],
        pressure_flow_memory=dict(d.get("pressure_flow_memory") or {}) if isinstance(d.get("pressure_flow_memory"), dict) else {},
        surface_psyche_profile=dict(d.get("surface_psyche_profile") or {}) if isinstance(d.get("surface_psyche_profile"), dict) else {},
        analyst_pressure_account=dict(d.get("analyst_pressure_account") or {}) if isinstance(d.get("analyst_pressure_account"), dict) else {},
        plasticity_window=dict(d.get("plasticity_window") or {}) if isinstance(d.get("plasticity_window"), dict) else {},
        narration_support=_dict_to_narration_support(d.get("narration_support")) if d.get("narration_support") else None,
        metabolic_style=dict(d.get("metabolic_style") or {}) if isinstance(d.get("metabolic_style"), dict) else {},
        expectation_baseline=dict(d.get("expectation_baseline") or {}) if isinstance(d.get("expectation_baseline"), dict) else {},
        striving_objects=[_dict_to_striving_object(x) for x in (d.get("striving_objects") or []) if isinstance(x, dict)],
        gift_shards=[_dict_to_gift_shard(x) for x in (d.get("gift_shards") or []) if isinstance(x, dict)],
        disruption_shards=[_dict_to_disruption_shard(x) for x in (d.get("disruption_shards") or []) if isinstance(x, dict)],
        registers=_dict_to_registers(d.get("registers") or {}),
        child_model=dict(d.get("child_model") or {}) if isinstance(d.get("child_model"), dict) else {},
        active_magnets=[_dict_to_magnet(x) for x in (d.get("active_magnets") or []) if isinstance(x, dict)],
        v5_runtime_input_bundle=dict(d.get("v5_runtime_input_bundle") or {}) if isinstance(d.get("v5_runtime_input_bundle"), dict) else {},
        v5_runtime_input_refs=(
            [str(d.get("v5_runtime_input_refs")).strip()]
            if isinstance(d.get("v5_runtime_input_refs"), (str, bytes, bytearray)) and str(d.get("v5_runtime_input_refs")).strip()
            else [str(x).strip() for x in (d.get("v5_runtime_input_refs") or []) if str(x).strip()]
        ),
        v5_bridge_status=str(d.get("v5_bridge_status", "not_attached") or "not_attached"),
        autonomy_drive=clamp(float(d.get("autonomy_drive", 50)), 0.0, 100.0),
        safety_drive=clamp(float(d.get("safety_drive", 50)), 0.0, 100.0),
        autonomy_condition=clamp(float(d.get("autonomy_condition", 50)), 0.0, 100.0),
        safety_condition=clamp(float(d.get("safety_condition", 50)), 0.0, 100.0),
        stability_threshold_inertia=clamp(float(d.get("stability_threshold_inertia", 0)), 0.0, 100.0),
        stability_delta_applied_this_year=bool(d.get("stability_delta_applied_this_year", False)),
    )
    doms = d.get("domains")
    if isinstance(doms, dict):
        for name in DOMAIN_NAMES:
            if name in doms and isinstance(doms[name], dict):
                state.domains[name] = _dict_to_domain_state(doms[name])
    for name in DOMAIN_NAMES:
        if name not in state.domains:
            state.domains[name] = DomainState()
    state.alienation = state.alienation_vector.aggregate()
    return state


def state_from_json(s: str) -> BackboneState:
    """Deserialize BackboneState from JSON string."""
    return state_from_dict(json.loads(s))
