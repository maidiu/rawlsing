"""
Parent Enneagram Type Inference

Heuristic mapping from WVS-derived parent behavior (warmth, authority, material support)
and driver vector to parent Enneagram type. Grounded in Naranjo/Ichazo schema
(ENNEAGRAM_FIXATION_ETIOLOGY_SCHEMA.md): parent character → child formation.

Use infer_parent_type() to get a probability distribution over types 1–9.
Use infer_parent_type_most_likely() for a single best guess.
"""

from typing import Dict, Optional, Literal
import numpy as np


def _get_driver_defaults(driver_vec) -> Dict[str, float]:
    """Extract driver values with safe defaults if driver_vec is None."""
    if driver_vec is None:
        return {
            "authoritarian": 50.0,
            "religiosity": 50.0,
            "family_importance": 50.0,
            "trust": 50.0,
        }
    return {
        "authoritarian": getattr(driver_vec, "authoritarian_vs_egalitarian", 50.0),
        "religiosity": getattr(driver_vec, "religiosity", 50.0),
        "family_importance": getattr(driver_vec, "family_importance", 50.0) or 50.0,
        "trust": getattr(driver_vec, "trust_vs_distrust", 50.0),
    }


def infer_parent_type(
    warmth: float,
    authority: float,
    material_support: float = 50.0,
    gender: Literal["male", "female"] = "male",
    driver_vec=None,
) -> Dict[int, float]:
    """
    Infer parent Enneagram type probabilities from behavior and driver values.

    Heuristic mapping derived from Naranjo/Ichazo parent profiles:
    - Type 1: excessive demands, scant acknowledgment → high authority, low warmth
    - Type 2: over-protective, seductive, need to be needed → high warmth, moderate authority
    - Type 3: distant, disinterested, admiring → low warmth, moderate authority
    - Type 4: melancholic, weak father / intense mother → low warmth (father); variable (mother)
    - Type 5: distant, devouring mother / schizoid → low warmth
    - Type 6: authoritarian, anxious, over-dutiful, over-protective → high authority, moderate-high warmth
    - Type 7: authoritarian father / permissive mother → father: high authority; mother: high warmth, low authority
    - Type 8: tyrannical, unjust, cruel → high authority, low warmth
    - Type 9: over-accommodating, detached, permissive → low authority, variable warmth

    Args:
        warmth: 0–100, parental warmth/affection
        authority: 0–100, parental authority/control
        material_support: 0–100, material provision (optional)
        gender: "male" or "female" (schema distinguishes father vs mother roles)
        driver_vec: Optional DriverVector (authoritarian, religiosity, family_importance, trust)

    Returns:
        Dict mapping type (1–9) to probability. Sums to ~1.0.
    """
    drivers = _get_driver_defaults(driver_vec)
    auth_val = drivers["authoritarian"]
    relig = drivers["religiosity"]
    fam_imp = drivers["family_importance"]
    trust_val = drivers["trust"]

    # Base logits from warmth × authority (0–100)
    # Each type gets a score from -3 to +3 based on fit
    scores = {t: 0.0 for t in range(1, 10)}

    # Type 1: cold, demanding, perfectionistic
    scores[1] += 0.5 * (authority - 50) / 25 - 0.4 * (warmth - 50) / 25
    if auth_val > 65 and relig > 55:
        scores[1] += 0.6

    # Type 2: over-protective, giving, need to be needed
    scores[2] += 0.5 * (warmth - 50) / 25 + 0.2 * (authority - 50) / 25
    if fam_imp > 60:
        scores[2] += 0.3

    # Type 3: distant, disinterested, admiring
    scores[3] += -0.4 * (warmth - 50) / 25 + 0.1 * (authority - 50) / 25
    if gender == "male":
        scores[3] += 0.2

    # Type 4: melancholic, weak father / intense mother
    scores[4] += -0.3 * (warmth - 50) / 25 - 0.2 * (authority - 50) / 25
    if gender == "female":
        scores[4] += 0.15

    # Type 5: distant, schizoid, devouring (mother)
    scores[5] += -0.6 * (warmth - 50) / 25 - 0.2 * (authority - 50) / 25
    if fam_imp < 45:
        scores[5] += 0.3

    # Type 6: anxious, authoritarian, over-dutiful, over-protective
    scores[6] += 0.5 * (authority - 50) / 25 + 0.3 * (warmth - 50) / 25
    if auth_val > 60 and trust_val < 55:
        scores[6] += 0.5

    # Type 7: father authoritarian; mother permissive, indulgent
    if gender == "male":
        scores[7] += 0.3 * (authority - 50) / 25 - 0.2 * (warmth - 50) / 25
    else:
        scores[7] += 0.4 * (warmth - 50) / 25 - 0.4 * (authority - 50) / 25

    # Type 8: tyrannical, unjust, cruel
    scores[8] += 0.6 * (authority - 50) / 25 - 0.5 * (warmth - 50) / 25
    if fam_imp < 45:
        scores[8] += 0.2

    # Type 9: over-accommodating, detached, permissive
    scores[9] += -0.5 * (authority - 50) / 25
    if fam_imp > 55 and gender == "female":
        scores[9] += 0.4

    # Softmax to probabilities
    arr = np.array([scores[t] for t in range(1, 10)])
    arr = np.clip(arr, -10, 10)
    exp_arr = np.exp(arr - np.max(arr))
    probs = exp_arr / exp_arr.sum()

    return {t: float(probs[t - 1]) for t in range(1, 10)}


def infer_parent_type_most_likely(
    warmth: float,
    authority: float,
    material_support: float = 50.0,
    gender: Literal["male", "female"] = "male",
    driver_vec=None,
) -> int:
    """
    Return the most likely parent Enneagram type (1–9).
    """
    probs = infer_parent_type(warmth, authority, material_support, gender, driver_vec)
    return max(probs.items(), key=lambda x: x[1])[0]


def get_parent_type_effects_for_child(
    father_type: Optional[int],
    mother_type: Optional[int],
    trust_vs_distrust: Optional[float] = None,
) -> Dict[int, float]:
    """
    Return type probability adjustments for child based on parent types.

    See PARENT_CHILD_TYPE_SCHEMA.md Section 8: Identification (I), Reaction (R), Complementary (C).
    - I: parent type X → boost child type X
    - R: parent type X → boost child type Y (opposite/compensatory strategy)
    - C: parent pair (e.g. 1+9) → boost child type that fills gap

    When trust_vs_distrust < 45, reaction paths are weighted more (schema: low trust → more R).

    Returns:
        Dict mapping child type (1–9) to additive adjustment (e.g. +0.1).
    """
    effects = {t: 0.0 for t in range(1, 10)}

    if father_type is None and mother_type is None:
        return effects

    # Bias toward reaction when trust is low (unreliable authority → rebel/compensate)
    r_weight = 0.35 if (trust_vs_distrust is not None and trust_vs_distrust < 45) else 0.25

    # Father effects (Identification)
    if father_type == 1:
        effects[1] += 0.15  # I: Demanding father → Type 1
        effects[7] += 0.10 * r_weight  # R: Child escapes into pleasure (1→7)
    elif father_type == 2:
        effects[2] += 0.12  # I: Domineering father → Type 2
    elif father_type == 3:
        effects[3] += 0.12  # I: Distant father → Type 3
    elif father_type == 4:
        effects[4] += 0.08  # I/C: Weak father (with Type 4 mother) → Type 4
    elif father_type == 5:
        effects[5] += 0.10  # I: Distant father → Type 5
    elif father_type == 6:
        effects[6] += 0.15  # I: Authoritarian father → Type 6
        effects[6] += 0.05 * r_weight  # R: Rebel against authority (also 6)
    elif father_type == 7:
        effects[7] += 0.12  # R: Authoritarian father → Type 7 (escape)
    elif father_type == 8:
        effects[4] += 0.08  # R: Sadistic father → Type 4
        effects[8] += 0.08  # I: Identification with aggressor
        effects[2] += 0.10 * r_weight  # R: Domineering father → child serves (8→2)
    elif father_type == 9:
        effects[9] += 0.08  # I: Accommodating father

    # Mother effects (Identification)
    if mother_type == 1:
        effects[1] += 0.15  # I: Cold mother → Type 1
        effects[7] += 0.08 * r_weight  # R: Child escapes (1→7)
    elif mother_type == 2:
        effects[2] += 0.10  # I: Over-protective mother → Type 2
    elif mother_type == 5:
        effects[5] += 0.15  # R: Devouring mother → child withdraws (5)
    elif mother_type == 6:
        effects[6] += 0.12  # I: Over-protective, anxious mother → Type 6
    elif mother_type == 7:
        effects[7] += 0.12  # I: Permissive mother → Type 7
    elif mother_type == 8:
        effects[8] += 0.15  # I/R: Tyrannical mother → Type 8
    elif mother_type == 9:
        effects[9] += 0.15  # I: Detached mother → Type 9
    elif mother_type == 4:
        effects[4] += 0.12  # I: Melancholic mother → Type 4

    # Complementary: 1+9 pair → Type 1 child (fills "responsible one" gap)
    if (father_type == 1 and mother_type == 9) or (father_type == 9 and mother_type == 1):
        effects[1] += 0.12  # C: Demanding + accommodating → child becomes responsible one

    return effects
