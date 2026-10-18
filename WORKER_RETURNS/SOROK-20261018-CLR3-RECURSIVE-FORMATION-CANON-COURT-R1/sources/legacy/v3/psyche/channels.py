"""Sublimation channel seeding and assignment.

Phase 3 uses a small fixed channel set so suppressed load can route into
regularized outlets instead of disappearing or becoming constant overt rage.
"""

from __future__ import annotations

from typing import Any

from v3.core.enums import DOMAIN_NAMES
from v3.core.state import BackboneState, clamp

SUBLIMATION_CHANNELS = (
    "humor_irony",
    "hyper_competence",
    "caretaking_warmth",
    "piety_ritual",
    "aesthetic_intensification",
    "withdrawal_numbness",
    "micro_authoritarianism",
    "conspiracy_symbolic",
    "quiet_organizing",
    "somatic_irritability",
)

_CHANNEL_PRIORITY = {name: idx for idx, name in enumerate(SUBLIMATION_CHANNELS)}


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def seed_wound_vector_from_identity(state: BackboneState, identity: Any, age: int | None = None) -> None:
    """Seed wound sensitivities from structural identity so channel assignment is differentiated."""
    wv = state.wound_vector
    class_origin = str(_get(identity, "class_origin") or _get(identity, "current_class") or "middle").strip().lower()
    current_class = str(_get(identity, "current_class") or class_origin or "middle").strip().lower()
    minority = str(_get(identity, "minority_status") or "dominant").strip().lower()
    religiosity = _get(identity, "religiosity_level")
    age_value = int(age if age is not None else (_get(identity, "age") or 0) or 0)

    # Start from a neutral baseline and then layer structural position.
    wv.shame = 50.0
    wv.fear = 50.0
    wv.anger = 50.0
    wv.abandonment = 50.0
    wv.control = 50.0
    wv.recognition = 50.0
    wv.loss = 50.0

    class_wounds = {
        "underclass": {"fear": 14.0, "abandonment": 12.0, "loss": 12.0, "shame": 8.0},
        "working": {"fear": 10.0, "abandonment": 9.0, "loss": 8.0, "shame": 6.0},
        "lower_middle": {"fear": 6.0, "abandonment": 5.0, "loss": 5.0, "control": 4.0},
        "middle": {"control": 3.0, "recognition": 3.0, "loss": 2.0},
        "upper_middle": {"control": 8.0, "recognition": 7.0, "shame": -2.0},
        "elite": {"control": 12.0, "recognition": 10.0, "fear": -4.0, "abandonment": -3.0},
    }
    for field_name, delta in class_wounds.get(current_class, class_wounds.get(class_origin, {})).items():
        setattr(wv, field_name, getattr(wv, field_name) + delta)

    if "minorit" in minority:
        wv.shame += 12.0
        wv.fear += 10.0
        wv.abandonment += 8.0
        wv.anger += 6.0
        wv.recognition += 2.0
    else:
        wv.control += 6.0
        wv.recognition += 5.0

    if isinstance(religiosity, (int, float)):
        rel = float(religiosity)
        if rel >= 70.0:
            wv.shame += 6.0
            wv.fear += 4.0
            wv.control += 3.0
            wv.recognition += 4.0
            wv.abandonment -= 2.0
        elif rel <= 30.0:
            wv.anger += 4.0
            wv.loss += 2.0

    if age_value < 18:
        wv.abandonment += 8.0
        wv.fear += 5.0
        wv.loss += 4.0
    elif age_value >= 40:
        wv.loss += 4.0
        wv.control += 2.0

    wv.clamp_all()


def _add(scores: dict[str, float], channel: str, delta: float) -> None:
    if channel in scores:
        scores[channel] += delta


def _seed_wound_scores(scores: dict[str, float], state: BackboneState) -> None:
    wv = state.wound_vector
    shame = float(getattr(wv, "shame", 50.0) or 50.0)
    fear = float(getattr(wv, "fear", 50.0) or 50.0)
    anger = float(getattr(wv, "anger", 50.0) or 50.0)
    abandonment = float(getattr(wv, "abandonment", 50.0) or 50.0)
    control = float(getattr(wv, "control", 50.0) or 50.0)
    recognition = float(getattr(wv, "recognition", 50.0) or 50.0)
    loss = float(getattr(wv, "loss", 50.0) or 50.0)
    religiosity = float(getattr(state.practice_stack, "spiritual", 50.0) or 50.0)

    if shame >= 60.0:
        _add(scores, "caretaking_warmth", (shame - 50.0) * 0.24)
        _add(scores, "hyper_competence", (shame - 50.0) * 0.22)
        _add(scores, "aesthetic_intensification", (shame - 50.0) * 0.12)
        _add(scores, "humor_irony", (shame - 50.0) * 0.08)
        _add(scores, "withdrawal_numbness", (shame - 50.0) * 0.10)
    if fear >= 60.0:
        _add(scores, "withdrawal_numbness", (fear - 50.0) * 0.25)
        _add(scores, "piety_ritual", (fear - 50.0) * 0.20)
        _add(scores, "somatic_irritability", (fear - 50.0) * 0.08)
    if anger >= 60.0:
        _add(scores, "quiet_organizing", (anger - 50.0) * 0.24)
        _add(scores, "micro_authoritarianism", (anger - 50.0) * 0.20)
        _add(scores, "humor_irony", (anger - 50.0) * 0.08)
        _add(scores, "somatic_irritability", (anger - 50.0) * 0.08)
    if abandonment >= 60.0:
        _add(scores, "caretaking_warmth", (abandonment - 50.0) * 0.18)
        _add(scores, "withdrawal_numbness", (abandonment - 50.0) * 0.18)
        _add(scores, "piety_ritual", (abandonment - 50.0) * 0.10)
    if control >= 60.0:
        _add(scores, "micro_authoritarianism", (control - 50.0) * 0.25)
        _add(scores, "hyper_competence", (control - 50.0) * 0.20)
        _add(scores, "conspiracy_symbolic", (control - 50.0) * 0.10)
    if recognition >= 60.0:
        _add(scores, "hyper_competence", (recognition - 50.0) * 0.22)
        _add(scores, "aesthetic_intensification", (recognition - 50.0) * 0.18)
        _add(scores, "humor_irony", (recognition - 50.0) * 0.08)
    if loss >= 60.0:
        _add(scores, "withdrawal_numbness", (loss - 50.0) * 0.24)
        _add(scores, "piety_ritual", (loss - 50.0) * 0.18)
        _add(scores, "quiet_organizing", (loss - 50.0) * 0.08)
    if religiosity >= 60.0:
        _add(scores, "piety_ritual", (religiosity - 50.0) * 0.25)
        _add(scores, "caretaking_warmth", (religiosity - 50.0) * 0.10)
    elif religiosity <= 30.0:
        _add(scores, "humor_irony", 4.0)
        _add(scores, "aesthetic_intensification", 2.0)


def _seed_domain_scores(scores: dict[str, float], domain_name: str, domain: Any) -> None:
    a_val = float(getattr(domain, "A", 50.0) or 50.0)
    s_val = float(getattr(domain, "S", 50.0) or 50.0)
    v_val = float(getattr(domain, "V", 50.0) or 50.0)
    buffer_type = str(getattr(domain, "buffer_type", "") or "")

    if domain_name in ("empire_occupation", "nation_state"):
        _add(scores, "quiet_organizing", max(0.0, (70.0 - a_val) * 0.10))
        _add(scores, "conspiracy_symbolic", max(0.0, (80.0 - s_val) * 0.08))
        _add(scores, "micro_authoritarianism", max(0.0, (60.0 - v_val) * 0.06))
        _add(scores, "humor_irony", max(0.0, (a_val - 40.0) * 0.04))
    elif domain_name == "sect_class_ethnicity":
        _add(scores, "piety_ritual", max(0.0, (70.0 - s_val) * 0.12))
        _add(scores, "caretaking_warmth", max(0.0, (s_val - 40.0) * 0.06))
        _add(scores, "quiet_organizing", max(0.0, (70.0 - v_val) * 0.06))
        _add(scores, "withdrawal_numbness", max(0.0, (60.0 - a_val) * 0.05))
    elif domain_name == "family_household":
        _add(scores, "caretaking_warmth", max(0.0, (70.0 - s_val) * 0.10))
        _add(scores, "micro_authoritarianism", max(0.0, (70.0 - v_val) * 0.06))
        _add(scores, "withdrawal_numbness", max(0.0, (60.0 - a_val) * 0.05))
        _add(scores, "humor_irony", max(0.0, (a_val - 50.0) * 0.04))
    elif domain_name == "body_self":
        _add(scores, "somatic_irritability", max(0.0, (v_val - 70.0) * 0.12))
        _add(scores, "withdrawal_numbness", max(0.0, (80.0 - s_val) * 0.06))
        _add(scores, "aesthetic_intensification", max(0.0, (a_val - 40.0) * 0.05))
        _add(scores, "hyper_competence", max(0.0, (70.0 - v_val) * 0.04))

    if buffer_type in ("guilt", "colonial_justification", "resignation"):
        _add(scores, "caretaking_warmth", 4.0)
        _add(scores, "piety_ritual", 3.0)
        _add(scores, "withdrawal_numbness", 2.0)
    elif buffer_type in ("not_my_concern", "liberal_utopian_blur"):
        _add(scores, "humor_irony", 3.0)
        _add(scores, "hyper_competence", 2.0)
        _add(scores, "aesthetic_intensification", 1.0)


def _pick_channel(scores: dict[str, float]) -> str:
    return max(SUBLIMATION_CHANNELS, key=lambda name: (scores.get(name, 0.0), -_CHANNEL_PRIORITY[name]))


def assign_sublimation_channels(state: BackboneState) -> BackboneState:
    """Assign a primary sublimation channel per domain from wound profile and structural position."""
    for domain_name, domain in state.domains.items():
        scores = {name: 0.0 for name in SUBLIMATION_CHANNELS}
        _seed_wound_scores(scores, state)
        _seed_domain_scores(scores, domain_name, domain)
        domain.affect_channel = _pick_channel(scores)
    return state
