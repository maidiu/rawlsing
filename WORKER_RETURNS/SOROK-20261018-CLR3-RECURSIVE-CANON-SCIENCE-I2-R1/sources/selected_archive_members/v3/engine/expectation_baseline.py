# v3/engine/expectation_baseline.py
# Expectation baseline derivation from need_axis_rules.yaml (Trace 8).
# Score per axis in [-2..+2]; map to entitled|hopeful|forbidden|hopeless.

from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore[assignment]

from v3.core.state import NEED_AXES, BASELINE_STATES

# Score -> baseline category
SCORE_TO_BASELINE: dict[int, str] = {
    2: "entitled",
    1: "entitled",
    0: "hopeful",
    -1: "forbidden",
    -2: "hopeless",
}
PARENT_CATEGORY_TO_SCORE: dict[str, int] = {
    "entitled": 1,
    "hopeful": 0,
    "forbidden": -1,
    "hopeless": -2,
}


def _strip_yaml_fences(text: str) -> str:
    """Remove ALL markdown code fences so YAML can be parsed."""
    import re
    text = re.sub(r'^```\w*\n?', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n?```\s*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n```\w*\n', '\n', text)
    return text.strip()


def load_need_axis_rules() -> dict[str, Any]:
    """Load need_axis_rules.yaml; return dict with meta, global_modifiers, axis_rules. Empty dict if missing."""
    if yaml is None:
        logger.warning("generation degradation: yaml not available; need_axis_rules disabled")
        return {}
    for base in (Path(__file__).resolve().parent.parent, Path(__file__).resolve().parent):
        path = base / "need_axis_rules.yaml"
        if path.exists():
            break
    else:
        logger.warning("generation degradation: need_axis_rules.yaml not found; baseline rules disabled")
        return {}
    try:
        raw = path.read_text(encoding="utf-8")
        raw = _strip_yaml_fences(raw)
        data = yaml.safe_load(raw)
        return dict(data) if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("generation degradation: need_axis_rules.yaml failed to load: %s", exc)
        return {}


def _apply_global_modifiers(
    scores: dict[str, int],
    rules: dict[str, Any],
    regime: dict[str, Any],
) -> None:
    """Apply global_modifiers from rules when regime conditions match. Mutates scores."""
    for mod in rules.get("global_modifiers") or []:
        if not isinstance(mod, dict):
            continue
        when = mod.get("when") or {}
        apply_spec = mod.get("apply") or {}
        if not when or not apply_spec:
            continue
        match = True
        for k, v in when.items():
            if k.endswith("_gte") and isinstance(v, (int, float)):
                key = k[:-4]
                if regime.get(key, 0) < v:
                    match = False
                    break
            elif k.endswith("_lt") and isinstance(v, (int, float)):
                key = k[:-3]
                if regime.get(key, 0) >= v:
                    match = False
                    break
        if not match:
            continue
        if "all_axes" in apply_spec:
            delta = int(apply_spec["all_axes"])
            for ax in NEED_AXES:
                if ax in scores:
                    scores[ax] = max(-2, min(2, scores[ax] + delta))
        axes_delta = apply_spec.get("axes")
        if isinstance(axes_delta, dict):
            for ax, delta in axes_delta.items():
                if ax in scores:
                    scores[ax] = max(-2, min(2, scores[ax] + int(delta)))


def derive_child_expectation_baseline(
    parent_baseline: dict[str, str] | None = None,
    transmission_regime: dict[str, Any] | None = None,
    environment: dict[str, Any] | None = None,
    rules: dict[str, Any] | None = None,
) -> dict[str, str]:
    """
    Derive expectation_baseline[NeedAxis] from parent + regime + environment.
    parent_baseline: NeedAxis -> entitled|hopeful|forbidden|hopeless (primary caregiver).
    transmission_regime: warmth, coercion, anxiety, shame, modeling_consistency, openness (0-100).
    environment: external_threat, economic_precarity, institutional_reliability, status_competition, collective_solidarity (0-100).
    Returns dict[NeedAxis, baseline].
    """
    regime = dict(transmission_regime or {})
    env = dict(environment or {})
    # Merge regime + env for rule conditions
    for k, v in env.items():
        regime.setdefault(k, v)
    rules = rules or load_need_axis_rules()
    meta = rules.get("meta") or {}
    parent_to_score = meta.get("parent_category_to_score") or PARENT_CATEGORY_TO_SCORE
    score_min = int(meta.get("score_min", -2))
    score_max = int(meta.get("score_max", 2))

    scores: dict[str, int] = {}
    for ax in NEED_AXES:
        parent_cat = (parent_baseline or {}).get(ax) or "hopeful"
        scores[ax] = parent_to_score.get(parent_cat, 0)
        scores[ax] = max(score_min, min(score_max, scores[ax]))

    _apply_global_modifiers(scores, rules, regime)

    out: dict[str, str] = {}
    for ax in NEED_AXES:
        s = scores.get(ax, 0)
        out[ax] = SCORE_TO_BASELINE.get(s, "hopeful")
    return out
