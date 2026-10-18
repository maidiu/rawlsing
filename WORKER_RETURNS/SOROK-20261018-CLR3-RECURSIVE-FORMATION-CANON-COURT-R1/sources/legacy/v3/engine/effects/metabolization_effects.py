# v3/engine/effects/metabolization_effects.py
# Rupture templates load, metabolization delta computation, malheur detection (specLLM).

from __future__ import annotations

import logging
import random
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

from v3.core.state import BackboneState, MetabolizationProcess, NarrationSupport, RuptureShard
import re

# Age brackets for template lookup
RUPTURE_AGE_BRACKETS = (3, 7, 11, 14, 17, 24, 35)

# Cluster deltas: psychological capacity keys -> delta (baseline per year in window)
CLUSTER_DELTAS: dict[str, dict[str, int]] = {
    "hardening_protection": {"vitality": 2, "aperture": -3, "coherence": 1, "binding": 2, "reality_anchor": 1},
    "sensitivity_exposure": {"vitality": -1, "aperture": 4, "coherence": -2, "binding": -1},
    "meaning_rebinding": {"vitality": 0, "aperture": 2, "coherence": 3, "binding": 2, "transmutation": 1},
    "cynicism_sealing": {"vitality": -2, "aperture": -4, "coherence": 2, "reality_anchor": -1},
    "justice_engagement": {"vitality": -1, "aperture": 3, "binding": 4, "agency": 2},
}

MODE_SCALARS: dict[str, float] = {
    "assimilation": 0.7,
    "accommodation": 1.0,
    "sealing": 0.9,
    "collapse": 1.2,
    "transmutation": 1.1,
    "mis_aim": 0.85,
}

MODE_OVERRIDES: dict[str, dict[str, int]] = {
    "collapse": {"coherence": -3, "aperture": -2},
    "transmutation": {"transmutation": 3, "aperture": 2},
}

MALHEUR_MULTIPLIER = 1.35


def _clamp_val(value: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, value))


def load_rupture_templates() -> list[dict[str, Any]]:
    """Load rupture_templates.yaml; return list of template dicts. Empty list if file or yaml missing."""
    if yaml is None:
        logger.warning("generation degradation: yaml not available; rupture_templates disabled")
        return []
    path = Path(__file__).resolve().parent / "rupture_templates.yaml"
    if not path.exists():
        logger.warning("generation degradation: rupture_templates.yaml not found; templates disabled")
        return []
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if isinstance(data, dict) and isinstance(data.get("templates"), list):
            return data["templates"]
        logger.warning("generation degradation: rupture_templates.yaml has unexpected structure")
        return []
    except Exception as exc:
        logger.warning("generation degradation: rupture_templates.yaml failed to load: %s", exc)
        return []


def _sample_from_priors(priors: dict[str, float], rng: random.Random | None = None) -> str:
    """Sample a key from weighted priors dict. Returns random key if priors empty."""
    if not priors:
        return "meaning_rebinding"
    rng = rng or random.Random()
    total = sum(priors.values())
    if total <= 0:
        return rng.choice(list(priors.keys()))
    r = rng.random() * total
    cumulative = 0.0
    for key, weight in priors.items():
        cumulative += weight
        if r <= cumulative:
            return key
    return list(priors.keys())[-1]


def _sample_mode_from_priors_and_support(
    mode_priors: dict[str, float],
    narration_support: NarrationSupport | None,
    rng: random.Random | None = None,
) -> str:
    """
    Sample metabolization mode from template mode_priors, weighted by NarrationSupport (specLLM: drives mode selection).
    Low warmth / high coercion → boost sealing, collapse. High warmth/accuracy → boost accommodation, transmutation.
    """
    if not mode_priors:
        return "accommodation"
    rng = rng or random.Random()
    warmth = narration_support.warmth if narration_support else 50
    coercion = narration_support.coercion if narration_support else 50
    accuracy = narration_support.accuracy if narration_support else 50
    # Weights: low support favours sealing/collapse; high support favours accommodation/transmutation
    support_factor = (warmth * 0.4 + accuracy * 0.3 - coercion * 0.3) / 100.0  # roughly -0.4 to 0.4
    adjusted: dict[str, float] = {}
    for mode, w in mode_priors.items():
        m = (mode or "").strip().lower()
        if support_factor < -0.15 and m in ("sealing", "collapse"):
            adjusted[m] = w * (1.2 - support_factor)
        elif support_factor < -0.15 and m in ("accommodation", "transmutation"):
            adjusted[m] = w * (0.85 + support_factor)
        elif support_factor > 0.15 and m in ("accommodation", "transmutation"):
            adjusted[m] = w * (1.0 + support_factor * 0.5)
        elif support_factor > 0.15 and m in ("sealing", "collapse"):
            adjusted[m] = w * (1.0 - support_factor * 0.5)
        else:
            adjusted[m] = max(0.01, w)
    return _sample_from_priors(adjusted, rng)


def get_template_for_age(templates: list[dict[str, Any]], age: int) -> dict[str, Any] | None:
    """Return first template that has severity_prior for age or nearest bracket; or None."""
    if not templates:
        return None
    best = None
    best_dist = 999
    for t in templates:
        prior = t.get("severity_prior") or {}
        if not isinstance(prior, dict):
            continue
        brackets = [b for b in RUPTURE_AGE_BRACKETS if b in prior]
        if not brackets:
            continue
        dist = min(abs(age - b) for b in brackets)
        if dist < best_dist:
            best_dist = dist
            best = t
    return best


def create_rupture_shard_from_event(
    state: BackboneState,
    ev: dict[str, Any],
    shard_id: str | None = None,
) -> RuptureShard:
    """
    When an epistemic_rupture event is selected, create a RuptureShard and append to state.
    Optionally create a MetabolizationProcess and set plasticity_window (1–3 years).
    ev must have kind "epistemic_rupture" and a "rupture" sub-dict (from parse_candidate_packet).
    """
    r = ev.get("rupture") or {}
    impl = ev.get("implicated") or {}
    domains = impl.get("domains") if isinstance(impl, dict) else []
    domain = (domains[0] if domains else "") or "unknown"
    violated = str(r.get("violated_assumption", "")).strip() or ev.get("label", "rupture")[:200]
    opacity = str(r.get("opacity", "medium")).strip().lower()
    if opacity not in ("low", "medium", "high"):
        opacity = "medium"
    pred_err = str(r.get("prediction_error", "medium")).strip().lower()
    if pred_err not in ("low", "medium", "high"):
        pred_err = "medium"
    sid = shard_id or f"rs_{state.year}_{state.age}_{len(state.rupture_shards)}"
    shard = RuptureShard(
        id=sid,
        year=state.year,
        age=state.age,
        violated_assumption=violated[:500],
        domain=domain[:80],
        opacity=opacity,
        prediction_error=pred_err,
        current_status="raw",
        intrusive_return_rate=60 if pred_err == "high" or opacity == "high" else 40,
        meaning_attempts=[],
    )
    state.rupture_shards.append(shard)
    # One MetabolizationProcess per rupture; severity from intensity or "major"; cluster from template
    intensity = str(ev.get("intensity", "major")).strip().lower()
    severity = "major" if intensity in ("major", "shock") else "micro"
    templates = load_rupture_templates()
    tpl = get_template_for_age(templates, state.age)
    cluster_candidates = tpl.get("cluster_candidates", ["meaning_rebinding"]) if tpl else ["meaning_rebinding"]
    cluster = str(cluster_candidates[0])[:60] if cluster_candidates else "meaning_rebinding"
    mode_priors = (tpl.get("mode_priors") or {}) if tpl else {}
    mode = _sample_mode_from_priors_and_support(mode_priors, state.narration_support) if mode_priors else "accommodation"
    proc = MetabolizationProcess(
        id=f"mp_{sid}",
        start_year=state.year,
        start_age=state.age,
        domain=domain[:80],
        violated_assumption=violated[:500],
        severity=severity,
        opacity=opacity,
        prediction_error=pred_err,
        mode=mode,
        status="raw",
        cluster=cluster,
        plasticity_years_left=min(3, max(1, 2 + (1 if opacity == "high" else 0))),
        intrusive_return_rate=shard.intrusive_return_rate,
        narrators=[],
        provisional_frame=None,
        downstream_biases={},
        reactivation_triggers=[],
    )
    state.metabolization_processes.append(proc)
    state.plasticity_window = {
        "years_left": proc.plasticity_years_left,
        "framework_switch_sensitivity": 15,
        "magnet_susceptibility": 10,
        "crack_rewrite_probability": 10,
    }
    return shard


def wound_vector_from_domain(domain: str) -> str:
    """Map rupture domain to primary wound dimension."""
    d = (domain or "").lower()
    if "family" in d or "household" in d:
        return "abandonment"
    if "body" in d or "sexual" in d:
        return "shame"
    if "school" in d or "peer" in d or "status" in d:
        return "shame"
    if "nation" in d or "state" in d or "police" in d or "violence" in d:
        return "fear"
    if "sect" in d or "class" in d or "ethnic" in d:
        return "recognition"
    if "eco" in d or "eviction" in d or "housing" in d:
        return "fear"
    if "loss" in d or "death" in d or "grief" in d:
        return "loss"
    if "religion" in d or "faith" in d or "sacred" in d:
        return "control"
    return "abandonment"


def update_wound_vector_from_rupture(state: BackboneState, severity: str, domain: str, opacity: str) -> None:
    """
    Update wound_vector sensitivities after injecting a rupture shard.
    Ruptures raise the primary wound dimension and related secondaries
    proportional to severity (micro=+4, major=+8, malheur=+15) and opacity.
    """
    wv = getattr(state, "wound_vector", None)
    if wv is None:
        return
    base = {"micro": 4, "major": 8, "malheur": 15}.get(severity, 8)
    if opacity == "high":
        base = int(base * 1.3)
    elif opacity == "low":
        base = int(base * 0.7)
    primary = wound_vector_from_domain(domain)
    secondary_map = {
        "abandonment": "fear",
        "shame": "control",
        "fear": "abandonment",
        "recognition": "anger",
        "loss": "abandonment",
        "control": "fear",
        "anger": "shame",
    }
    secondary = secondary_map.get(primary, "fear")

    def _bump(attr: str, delta: int) -> None:
        current = getattr(wv, attr, 50.0)
        setattr(wv, attr, min(100.0, max(0.0, current + delta)))

    _bump(primary, base)
    _bump(secondary, base // 3)


def maybe_inject_rupture_at_band_age(state) -> None:
    """
    Inject epistemic ruptures across childhood and adult life.
    """
    RUPTURE_BAND_AGES = {3: 0.60, 7: 0.70, 11: 0.65, 14: 0.60, 17: 0.55, 24: 0.45, 30: 0.30}
    if state.age not in RUPTURE_BAND_AGES:
        return
    if random.random() >= RUPTURE_BAND_AGES[state.age]:
        return
    templates = load_rupture_templates()
    if not templates:
        return

    age = state.age
    eligible = []
    for t in templates:
        prior = t.get("severity_prior") or {}
        if not isinstance(prior, dict):
            continue
        brackets = [int(k) for k in prior.keys() if str(k).isdigit()]
        if not brackets:
            continue
        if age in brackets:
            eligible.append((t, 3))
        else:
            dist = min(abs(age - b) for b in brackets)
            if dist <= 7:
                eligible.append((t, 1))

    if not eligible:
        return

    templates_w, weights = zip(*eligible)
    tpl = random.choices(templates_w, weights=weights, k=1)[0]
    prior = tpl.get("severity_prior") or {}
    brackets = sorted(int(k) for k in prior.keys() if str(k).isdigit())
    nearest = min(brackets, key=lambda b: abs(age - b))
    severity = prior.get(str(nearest), prior.get(nearest, "major"))

    if severity == "malheur":
        opacity = random.choices(["medium", "high"], weights=[0.35, 0.65])[0]
    elif severity == "major":
        opacity = random.choices(["low", "medium", "high"], weights=[0.25, 0.55, 0.20])[0]
    else:
        opacity = random.choices(["low", "medium"], weights=[0.60, 0.40])[0]

    domain = tpl.get("domain", "family_household")
    ev = {
        "kind": "epistemic_rupture",
        "label": tpl.get("label", "rupture")[:200],
        "rupture": {
            "violated_assumption": (tpl.get("violated_assumption") or tpl.get("label", ""))[:500],
            "opacity": opacity,
            "prediction_error": "high" if severity == "malheur" else ("medium" if severity == "major" else "low"),
        },
        "implicated": {"domains": [domain]},
        "intensity": severity,
    }
    create_rupture_shard_from_event(state, ev)
    update_wound_vector_from_rupture(state, severity, domain, opacity)


def is_malheur(
    severity: str,
    *,
    status_shock: bool = False,
    isolation_spike: bool = False,
    narration_availability: int = 50,
) -> bool:
    """
    Malheur = (severity == malheur) OR (high severity + status loss + isolation + no reliable narrators).
    specLLM: world-destroying affliction that strips protective meanings and social location.
    """
    sev = (severity or "").strip().lower()
    if sev == "malheur":
        return True
    if sev != "major":
        return False
    return (
        status_shock
        and isolation_spike
        and narration_availability < 40
    )


def compute_metabolization_delta(
    cluster: str,
    mode: str,
    severity: str,
    narration_support: NarrationSupport | None,
    is_malheur_flag: bool,
) -> tuple[dict[str, int], dict[str, int]]:
    """
    Returns (capacity_delta, bias_delta) for psychological capacity and downstream_biases.
    cluster/mode/severity from MetabolizationProcess; narration_support derived; is_malheur_flag from is_malheur().
    """
    base = dict(CLUSTER_DELTAS.get(cluster, {}))
    sev = (severity or "major").strip().lower()
    severity_scalar = {"micro": 0.55, "major": 1.0, "malheur": 1.25}.get(sev, 1.0)
    mode_scalar = MODE_SCALARS.get((mode or "accommodation").strip().lower(), 1.0)
    scalar = severity_scalar * mode_scalar

    delta: dict[str, int] = {k: int(round(v * scalar)) for k, v in base.items()}
    for k, v in MODE_OVERRIDES.get(mode.strip().lower(), {}).items():
        delta[k] = delta.get(k, 0) + int(round(v * severity_scalar))

    if is_malheur_flag:
        for k in ("vitality", "coherence"):
            delta[k] = int(round(delta.get(k, 0) * MALHEUR_MULTIPLIER))
        if narration_support and narration_support.availability < 40:
            delta["aperture"] = delta.get("aperture", 0) - 4

    # NarrationSupport modulates delta magnitude for all clusters (specLLM: drives mode selection and reconfiguration)
    if narration_support:
        support_quality = (
            narration_support.availability * 0.25
            + narration_support.warmth * 0.25
            + narration_support.accuracy * 0.25
            - narration_support.coercion * 0.25
        ) / 100.0  # roughly -0.25 to 0.25
        # Low support → slightly amplify negative capacity effects for hardening/cynicism; reduce for meaning/justice
        if cluster in ("hardening_protection", "cynicism_sealing") and support_quality < 0:
            for k in list(delta.keys()):
                if delta.get(k, 0) < 0:
                    delta[k] = int(round(delta[k] * (1.0 - support_quality * 0.3)))
        elif cluster in ("sensitivity_exposure", "justice_engagement") and support_quality > 0.1:
            for k in list(delta.keys()):
                delta[k] = int(round(delta.get(k, 0) * (1.0 + min(0.2, support_quality * 0.5))))

    # Clamp deltas to sane range
    max_abs = 18
    for k in list(delta.keys()):
        delta[k] = int(_clamp_val(float(delta[k]), -max_abs, max_abs))

    bias: dict[str, int] = {}
    if cluster == "meaning_rebinding" and narration_support:
        support_quality = int(round(
            0.45 * narration_support.warmth
            + 0.45 * narration_support.accuracy
            - 0.35 * narration_support.coercion
        ))
        support_quality = int(_clamp_val(support_quality, 0, 100))
        bias_key = "meaning_rebinding_integrative" if support_quality >= 60 else "meaning_rebinding_authoritarian"
    else:
        bias_key = cluster
    bias = dict(BIAS_DELTAS.get(bias_key, {}))
    for k, v in MODE_BIAS_TWEAKS.get(mode.strip().lower(), {}).items():
        bias[k] = bias.get(k, 0) + v
    for k in list(bias.keys()):
        bias[k] = int(_clamp_val(bias[k], -20, 20))

    return delta, bias


# Stub bias deltas (downstream_biases keys -> delta)
BIAS_DELTAS: dict[str, dict[str, int]] = {
    "hardening_protection": {"betrayal_expectancy": 2, "reality_tolerance": -1},
    "sensitivity_exposure": {"betrayal_expectancy": 1, "justice_sensitivity": 2},
    "meaning_rebinding": {"meaning_rebinding_integrative": 2},
    "meaning_rebinding_integrative": {"meaning_rebinding_integrative": 2},
    "meaning_rebinding_authoritarian": {"meaning_rebinding_authoritarian": 2},
    "cynicism_sealing": {"reality_tolerance": -2, "scapegoat_tendency": 1},
    "justice_engagement": {"justice_sensitivity": 3, "attachment_guarding": -1},
}

MODE_BIAS_TWEAKS: dict[str, dict[str, int]] = {
    "collapse": {"reality_tolerance": -1, "attachment_guarding": 2},
    "sealing": {"scapegoat_tendency": 1},
    "transmutation": {"meaning_rebinding_integrative": 1},
}


def _analyze_narrative_for_support_quality(rendered_output: dict[str, Any]) -> tuple[int, int, int]:
    """
    Analyze rendered narrative for accuracy, warmth, coercion quality (0-100).
    Uses narrative_snapshot.scene and dialogue_snippets when present (specLLM: NarrationSupport from narrative content).
    Returns (accuracy, warmth, coercion). Warmth and coercion are mutually damped so high coercion pulls warmth down.
    """
    combined = ""
    if isinstance(rendered_output, dict):
        snap = rendered_output.get("narrative_snapshot") or {}
        scene = str(snap.get("scene", "") if isinstance(snap, dict) else "")
        combined = scene
        snippets = rendered_output.get("dialogue_snippets")
        if isinstance(snippets, list) and snippets:
            for s in snippets[:10]:
                if isinstance(s, dict) and s.get("text"):
                    combined += " " + str(s.get("text", ""))
                elif isinstance(s, str):
                    combined += " " + s
        if not combined.strip():
            combined = str(rendered_output.get("scene", ""))

    if not combined.strip():
        return 50, 50, 50

    text_lower = combined.lower()

    # Accuracy: detail/specificity vs vague/generic (capped)
    detail_words = ["specific", "exactly", "precisely", "clearly", "definitely", "actually", "really", "truly"]
    vague_words = ["maybe", "perhaps", "somehow", "kind of", "sort of", "somewhere", "sometime"]
    detail_score = min(12, sum(1 for w in detail_words if w in text_lower) * 3)
    vague_penalty = min(10, sum(1 for w in vague_words if w in text_lower) * 2)
    accuracy = max(25, min(95, 50 + detail_score - vague_penalty))

    # Warmth: supportive/caring language (capped so dialogue doesn't blow up score)
    warmth_words = [
        "love", "care", "support", "encourage", "gentle", "kind", "nurture", "comfort",
        "understanding", "empathy", "warmth", "affection", "tender", "compassion",
        "help", "guide", "protect", "embrace", "cherish", "bond", "connection"
    ]
    warmth_patterns = [
        r"i love you", r"you are loved", r"take care of", r"look after",
        r"support you", r"help you", r"understand you", r"with you"
    ]
    warmth_raw = sum(1 for w in warmth_words if w in text_lower) * 4
    for pat in warmth_patterns:
        if re.search(pat, text_lower):
            warmth_raw += 10
    warmth_raw = max(0, min(90, warmth_raw))

    # Coercion: pressure/control/authority (capped)
    coercion_words = [
        "must", "should", "have to", "need to", "ought to", "required", "forced",
        "pressure", "control", "manipulate", "dominate", "command", "demand",
        "insist", "threaten", "punish", "discipline", "obey", "comply", "submit",
        "authority", "power", "rule", "enforce"
    ]
    coercion_patterns = [
        r"you must", r"you have to", r"you need to", r"or else", r"punishment",
        r"consequence", r"discipline", r"obey me", r"listen to me", r"do as i say"
    ]
    coercion_raw = sum(1 for w in coercion_words if w in text_lower) * 4
    for pat in coercion_patterns:
        if re.search(pat, text_lower):
            coercion_raw += 8
    coercion_raw = max(0, min(95, coercion_raw))

    # Mutual damping: high coercion reduces effective warmth (tense/conflict scenes)
    coercion = max(20, min(90, coercion_raw))
    if coercion_raw > 55 and warmth_raw > 50:
        warmth = max(25, int(warmth_raw - (coercion_raw - 50) * 0.4))
    else:
        warmth = max(20, min(90, warmth_raw))

    return accuracy, warmth, coercion


def update_metabolization_and_plasticity_step(
    state: BackboneState,
    derived: Any,
    config: dict[str, Any],
) -> None:
    """
    Optional wiring: plasticity window decrement; derive NarrationSupport from narrators;
    apply reconfiguration cluster deltas to psychological_capacity and downstream_biases.
    """
    from v3.core.state import PsychologicalCapacity

    # Decrement plasticity
    pw = state.plasticity_window or {}
    years_left = int(pw.get("years_left", 0))
    if years_left > 0:
        state.plasticity_window = dict(pw, years_left=years_left - 1)
    for proc in state.metabolization_processes:
        if proc.plasticity_years_left > 0:
            proc.plasticity_years_left -= 1

    # Derive NarrationSupport from active processes' narrators + rendered narrative content
    all_narrators: list[str] = []
    for proc in state.metabolization_processes:
        if proc.status in ("raw", "working") and proc.narrators:
            all_narrators.extend(proc.narrators)
    availability = min(100, 40 + 10 * len(set(all_narrators))) if all_narrators else 50

    # Analyze last year's rendered narrative for accuracy/warmth/coercion quality (50,50,50 when no scene)
    accuracy, warmth, coercion = _analyze_narrative_for_support_quality(state.rendered_output or {})

    state.narration_support = NarrationSupport(
        availability=availability,
        accuracy=accuracy,
        warmth=warmth,
        coercion=coercion,
    )
    state.narration_support.clamp_all()

    # Apply cluster deltas for each active process
    psych = state.psychological_capacity
    for proc in state.metabolization_processes:
        if proc.status not in ("raw", "working"):
            continue
        cluster = (proc.cluster or "meaning_rebinding").strip() or "meaning_rebinding"
        is_malheur_flag = is_malheur(
            proc.severity,
            narration_availability=state.narration_support.availability if state.narration_support else 50,
        )
        cap_delta, bias_delta = compute_metabolization_delta(
            cluster, proc.mode, proc.severity, state.narration_support, is_malheur_flag
        )
        for k, v in cap_delta.items():
            if hasattr(psych, k):
                cur = getattr(psych, k, 50)
                setattr(psych, k, _clamp_val(cur + v, 0, 100))
        for k, v in bias_delta.items():
            proc.downstream_biases[k] = proc.downstream_biases.get(k, 0) + v

    if state.psychological_capacity is not None:
        state.psychological_capacity.clamp_all()
    # Update plasticity_window sensitivities from years_left and psychological capacity
    yl = int((state.plasticity_window or {}).get("years_left", 0))
    pc = state.psychological_capacity
    if pc:
        # Higher aperture = more magnet susceptibility
        magnet_susceptibility = 5 + int(pc.aperture * 0.3)
        # Higher transmutation + binding = more framework switch sensitivity
        framework_switch_sensitivity = 5 + int((pc.transmutation + pc.binding) * 0.2) + min(10, yl)
        # Lower coherence = higher crack rewrite probability
        crack_rewrite_probability = max(5, 25 - int(pc.coherence * 0.4))
    else:
        magnet_susceptibility = 10
        framework_switch_sensitivity = 10 + min(15, yl * 2)
        crack_rewrite_probability = 10

    state.plasticity_window = dict(state.plasticity_window or {},
        framework_switch_sensitivity=framework_switch_sensitivity,
        magnet_susceptibility=magnet_susceptibility,
        crack_rewrite_probability=crack_rewrite_probability)
