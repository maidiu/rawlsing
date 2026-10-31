# v3/psyche/gating.py
# Expression gating — ensures structural load does not default to constant expression.
# Implements the "go along to get along" / "load ≠ expression" policy.

from __future__ import annotations

from v3.core.enums import DOMAIN_NAMES, domain_axis_to_label
from v3.core.state import BackboneState

DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS = {
    "empire_occupation": {
        0: 0.35,
        1: 0.35,
        2: 0.15,
        4: 0.05,
        5: 0.05,
        8: 0.05,
    },
    "nation_state": {
        1: 0.10,
        2: 0.45,
        3: 0.15,
        4: 0.10,
        5: 0.10,
        6: 0.05,
        8: 0.05,
    },
    "sect_class_ethnicity": {
        0: 0.05,
        1: 0.05,
        2: 0.10,
        3: 0.10,
        4: 0.45,
        5: 0.05,
        6: 0.10,
        7: 0.05,
        8: 0.05,
    },
    "family_household": {
        2: 0.05,
        3: 0.05,
        4: 0.10,
        5: 0.05,
        6: 0.20,
        7: 0.40,
        8: 0.15,
    },
    "body_self": {
        0: 0.05,
        1: 0.05,
        2: 0.10,
        3: 0.05,
        4: 0.10,
        6: 0.10,
        7: 0.15,
        8: 0.40,
    },
}


def _derive_hostage_index(state: BackboneState) -> float:
    """Derive hostage_index from reproduction_constraints: 0=free, 100=trapped."""
    rc = state.reproduction_constraints
    score = 0.0
    score += rc.housing_insecurity * 0.35     # insecure housing = heavily trapped
    score += (100.0 - rc.legal_status) * 0.25   # precarious legal status = trapped
    score += rc.dependents * 0.60              # dependents = heavily trapped
    score += rc.debt * 0.30                    # debt = trapped
    score += rc.job_insecurity * 0.30          # job insecurity = trapped
    score += rc.caregiving_load * 0.35         # caregiving load = trapped
    return max(0.0, min(100.0, score))


def _viscerality_weight(label: str) -> float:
    if label == "target":
        return 1.0
    if label == "proximate":
        return 0.8
    if label == "identified":
        return 0.65
    return 0.35


def _awareness_weight(label: str) -> float:
    if label == "structural":
        return 1.0
    if label == "partial":
        return 0.8
    if label == "distorted":
        return 0.55
    return 0.35


def _build_strata_by_level(strata: list[object]) -> dict[int, object]:
    strata_by_level: dict[int, object] = {}
    fallback_strata: list[tuple[int, object]] = []
    for index, stratum in enumerate(strata):
        level = getattr(stratum, "level", None)
        if isinstance(level, int):
            strata_by_level[level] = stratum
        else:
            fallback_strata.append((index, stratum))
    for index, stratum in fallback_strata:
        strata_by_level.setdefault(index, stratum)
    return strata_by_level


def _stratum_latent_pressure(stratum: object, domain: object) -> float:
    awareness = domain_axis_to_label("A", float(getattr(domain, "A", 0.0) or 0.0))
    viscerality = domain_axis_to_label("V", float(getattr(domain, "V", 0.0) or 0.0))
    provision_strength = float(getattr(stratum, "provision_strength", 0.0) or 0.0)
    provision_deprivation = max(0.0, min(100.0, 100.0 - provision_strength))
    pressure = 0.0
    pressure += float(getattr(stratum, "coercion_strength", 0.0) or 0.0) * _viscerality_weight(viscerality)
    pressure += float(getattr(stratum, "contradiction_load", 0.0) or 0.0) * _awareness_weight(awareness)
    pressure += float(getattr(stratum, "visibility_of_complicity", 0.0) or 0.0) * 0.25
    pressure += float(getattr(stratum, "salience", 0.0) or 0.0) * 0.10
    pressure += provision_deprivation * 0.20
    return pressure


def compute_baseline_load(state: BackboneState) -> None:
    """Compute per-domain load from latent structural pressure in the current strata."""
    strata = list(getattr(state, "strata_stack", []) or [])
    strata_by_level = _build_strata_by_level(strata)
    for name in DOMAIN_NAMES:
        domain = state.domains.get(name)
        if domain is None:
            continue
        domain.baseline_load = 0.0

    for name in DOMAIN_NAMES:
        domain = state.domains.get(name)
        if domain is None:
            continue
        load = 0.0
        for level, weight in DOMAIN_STRATA_LATENT_PRESSURE_WEIGHTS[name].items():
            stratum = strata_by_level.get(level)
            if stratum is None:
                continue
            load += weight * _stratum_latent_pressure(stratum, domain)
        if getattr(domain, "buffer_type", "") in ("guilt", "colonial_justification"):
            load += 6.0
        elif getattr(domain, "buffer_type", "") in ("not_my_concern", "liberal_utopian_blur"):
            load += 3.0
        domain.baseline_load = max(0.0, min(100.0, round(load, 1)))
        # Keep the historical field present for downstream consumers and docs.
        domain.expression_rate = max(0.0, min(100.0, float(getattr(domain, "expression_rate", 50.0) or 50.0)))
        domain.activation_threshold = max(0.0, min(100.0, float(getattr(domain, "activation_threshold", 80.0) or 80.0)))


def apply_expression_gating(state: BackboneState) -> None:
    """Gate expressed_aim per domain based on hostage_index, coercion, and energy.

    High hostage → expression suppressed (survival first)
    High coercion → avoid overt defiance
    Low energy → everything suppressed (fatigue matters)
    """
    hostage = _derive_hostage_index(state)
    vitality = float(getattr(state.psychological_capacity, "vitality", 50.0) or 50.0)
    inner_load = float(getattr(state.registers, "inner_load", 50.0) or 50.0)
    energy = vitality * 0.5 + (100.0 - inner_load) * 0.5

    for _name, domain in state.domains.items():
        load = float(getattr(domain, "baseline_load", 0.0) or 0.0)
        if load <= 0.0:
            continue

        rate = float(getattr(domain, "expression_rate", 50.0) or 50.0)

        # Hostage brake: survival suppresses display
        if hostage > 70:
            rate *= 0.3
        elif hostage > 50:
            rate *= 0.6

        # Fatigue brake: low energy suppresses everything
        if energy < 30:
            rate *= 0.5
        elif energy < 50:
            rate *= 0.75

        domain.expression_rate = max(0.0, min(100.0, rate))
        expressed = load * (rate / 100.0)
        if expressed > float(getattr(domain, "activation_threshold", 80.0) or 80.0):
            domain.expressed_aim = max(0.0, min(100.0, expressed))
        else:
            domain.expressed_aim = 0.0


def route_unexpressed_load(state: BackboneState) -> None:
    """Route residual load into common sublimation channels."""
    for _name, domain in state.domains.items():
        unexpressed = float(getattr(domain, "baseline_load", 0.0) or 0.0) - float(getattr(domain, "expressed_aim", 0.0) or 0.0)
        if unexpressed <= 0.0:
            continue

        ch = str(getattr(domain, "affect_channel", "compartmentalization") or "compartmentalization")
        if ch == "humor_irony":
            state.style_traits.absurdist_humor += unexpressed * 0.10
        elif ch == "hyper_competence":
            state.practice_stack.study += unexpressed * 0.05
            state.practice_stack.craft += unexpressed * 0.05
            state.intensity_and_capture.craft_talent += unexpressed * 0.02
        elif ch == "caretaking_warmth":
            state.practice_stack.care += unexpressed * 0.08
            state.practice_stack.spiritual += unexpressed * 0.01
        elif ch == "piety_ritual":
            state.practice_stack.spiritual += unexpressed * 0.08
            state.peak_routing.coherence += unexpressed * 0.02
        elif ch == "aesthetic_intensification":
            state.style_traits.aesthetic_sensitivity += unexpressed * 0.07
            state.practice_stack.craft += unexpressed * 0.03
        elif ch == "withdrawal_numbness":
            state.practice_stack.risk_training -= unexpressed * 0.05
        elif ch == "micro_authoritarianism":
            state.style_traits.conscientiousness += unexpressed * 0.04
            state.peak_routing.coherence += unexpressed * 0.01
        elif ch == "conspiracy_symbolic":
            state.psychological_capacity.reality_anchor -= unexpressed * 0.03
            state.peak_routing.theory_of_change_style = "witness_exposure"
        elif ch == "quiet_organizing":
            state.practice_stack.organizing += unexpressed * 0.08
            state.peak_routing.coherence += unexpressed * 0.02
        elif ch == "somatic_irritability":
            state.capacity.health -= unexpressed * 0.02
            state.wound_vector.anger += unexpressed * 0.05
        else:
            state.practice_stack.craft += unexpressed * 0.02

    state.capacity.clamp_all()
    state.psychological_capacity.clamp_all()
    state.practice_stack.clamp_all()
    state.peak_routing.clamp_all()
    state.style_traits.clamp_all()
    state.wound_vector.clamp_all()
