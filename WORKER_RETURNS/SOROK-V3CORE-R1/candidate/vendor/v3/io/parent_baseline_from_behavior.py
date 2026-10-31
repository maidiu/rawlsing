# v3/io/parent_baseline_from_behavior.py
# Infer parent_expectation_baseline and transmission_regime from parent behavior (warmth, authority, material_support).
# Used so v2/server can set identity["parent_expectation_baseline"] and identity["transmission_regime"] before v3 backbone.

from __future__ import annotations

from typing import Any

from v3.core.state import NEED_AXES


def _get(obj: Any, key: str, default: Any = None) -> Any:
    if isinstance(obj, dict):
        return obj.get(key, default)
    return getattr(obj, key, default)


def _float(val: Any, default: float = 50.0) -> float:
    try:
        return max(0.0, min(100.0, float(val)))
    except (TypeError, ValueError):
        return default


def infer_parent_baseline_and_regime(
    parent_identity: dict[str, Any],
) -> tuple[dict[str, str], dict[str, float]]:
    """
    Infer (parent_expectation_baseline, transmission_regime) from parent_identity.
    Expects parent_identity to have:
      - parent_behavior.father, parent_behavior.mother with parental_warmth, parental_authority, parental_material_support (0-100)
    or parents.father / parents.mother with those keys.
    Returns (baseline dict NeedAxis -> entitled|hopeful|forbidden|hopeless, regime dict warmth/coercion/openness/etc 0-100).
    """
    behavior_f = _get(parent_identity, "parent_behavior", {}) or {}
    if isinstance(behavior_f, dict):
        father_b = behavior_f.get("father") or {}
        mother_b = behavior_f.get("mother") or {}
    else:
        father_b = mother_b = {}
    if not father_b and not mother_b:
        parents = _get(parent_identity, "parents") or {}
        father_b = _get(parents, "father") or {}
        mother_b = _get(parents, "mother") or {}
    warmth_f = _float(_get(father_b, "parental_warmth", 50))
    warmth_m = _float(_get(mother_b, "parental_warmth", 50))
    auth_f = _float(_get(father_b, "parental_authority", 50))
    auth_m = _float(_get(mother_b, "parental_authority", 50))
    mat_f = _float(_get(father_b, "parental_material_support", 50))
    mat_m = _float(_get(mother_b, "parental_material_support", 50))
    warmth = (warmth_f + warmth_m) / 2.0
    authority = (auth_f + auth_m) / 2.0
    material = (mat_f + mat_m) / 2.0

    # Heuristics: low warmth -> attachment/belonging forbidden/hopeless; high authority -> autonomy/safety forbidden; low material -> status/competence hopeless
    baseline: dict[str, str] = {}
    for ax in NEED_AXES:
        baseline[ax] = "hopeful"
    if warmth < 40:
        baseline["attachment"] = "forbidden" if warmth < 30 else "hopeful"
        baseline["belonging"] = "hopeless" if warmth < 25 else "forbidden" if warmth < 40 else "hopeful"
    if authority > 60:
        baseline["autonomy"] = "forbidden" if authority > 70 else "hopeful"
        baseline["safety"] = "forbidden" if authority > 65 else "hopeful"
    if material < 35:
        baseline["status"] = "hopeless" if material < 25 else "forbidden"
        baseline["competence"] = "hopeless" if material < 30 else "hopeful"

    # Transmission regime: warmth, coercion (from authority), openness (~ inverse authority), anxiety (high when low warmth), shame, modeling_consistency
    coercion = authority
    openness = 100.0 - authority
    anxiety = 100.0 - warmth
    shame = 50.0
    if warmth < 40 and authority > 55:
        shame = 60.0
    modeling = warmth * 0.5 + (100.0 - authority) * 0.3 + 20.0

    regime: dict[str, float] = {
        "warmth": warmth,
        "coercion": coercion,
        "openness": max(0, min(100, openness)),
        "anxiety": max(0, min(100, anxiety)),
        "shame": max(0, min(100, shame)),
        "modeling_consistency": max(0, min(100, modeling)),
    }
    return baseline, regime
