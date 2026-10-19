# v3/engine/striving_objects.py
# StrivingObject spawn/update from proxy_striving_map.yaml (Trace 8).
# Full adoption: all 4 baselines (direct + proxy), multipliers, tag similarity, update_existing, retirement.

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

from v3.core.state import BackboneState, StrivingObject, NEED_AXES

PROXY_STRIVING_AGE_BRACKETS = (3, 7, 11, 14, 17, 24, 35)

# Baseline multipliers (ChatGPT: forbidden/hopeless lower spawn/investment; identity_load higher for forbidden)
SPAWN_MULT = {"entitled": 1.3, "hopeful": 1.0, "forbidden": 0.85, "hopeless": 0.6}
INVEST_MULT = {"entitled": 1.25, "hopeful": 1.0, "forbidden": 0.75, "hopeless": 0.6}
IDENTITY_MULT = {"entitled": 1.15, "hopeful": 1.0, "forbidden": 1.05, "hopeless": 0.9}

# Retirement: when investment and identity_load low, prob retire
RETIRE_INVESTMENT_THRESHOLD = 15
RETIRE_IDENTITY_THRESHOLD = 25
RETIRE_PROB = 0.35


def load_proxy_striving_map() -> dict[str, Any]:
    """Load proxy_striving_map.yaml; return dict with meta and proxies (NeedAxis -> baseline -> age -> list)."""
    if yaml is None:
        logger.warning("generation degradation: yaml not available; proxy_striving_map disabled")
        return {}
    for base in (Path(__file__).resolve().parent.parent, Path(__file__).resolve().parent):
        path = base / "proxy_striving_map.yaml"
        if path.exists():
            break
    else:
        logger.warning("generation degradation: proxy_striving_map.yaml not found; striving map disabled")
        return {}
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        return dict(data) if isinstance(data, dict) else {}
    except Exception as exc:
        logger.warning("generation degradation: proxy_striving_map.yaml failed to load: %s", exc)
        return {}


def _nearest_bracket(age: int) -> int:
    """Return nearest age bracket from PROXY_STRIVING_AGE_BRACKETS."""
    best = PROXY_STRIVING_AGE_BRACKETS[0]
    for b in PROXY_STRIVING_AGE_BRACKETS:
        if abs(age - b) < abs(age - best):
            best = b
    return best


def spawn_budget_for_age(age: int, rng: random.Random | None = None) -> int:
    """Jagged spawn budget: 2 at transition ages, 1 at adjacent, else 0 or 1 with prob."""
    rng = rng or random.Random()
    if age in PROXY_STRIVING_AGE_BRACKETS:
        return 2
    if age in (6, 10, 13, 16, 23, 34):
        return 1
    return 1 if rng.random() < 0.35 else 0


def _is_similar(existing: StrivingObject, cand_tags: list[str], axis: str) -> bool:
    """True if existing object has same axis and >=2 tag overlap (avoid near-duplicate)."""
    if existing.need_axis != axis or not getattr(existing, "active", True):
        return False
    exist_tags = set(getattr(existing, "tags", None) or [])
    cand_set = set(cand_tags or [])
    return len(exist_tags & cand_set) >= 2


def _make_object_from_entry(
    ent: dict[str, Any],
    need_axis: str,
    age: int,
    year: int,
    baseline: str,
    existing_ids: set[str],
    rng: random.Random | None = None,
) -> StrivingObject | None:
    """Build one StrivingObject from YAML entry; apply baseline multipliers. Returns None if id duplicate."""
    rng = rng or random.Random()
    pid = str(ent.get("id", ""))
    if pid in existing_ids:
        return None
    existing_ids.add(pid)
    label = str(ent.get("label", ""))[:200]
    inv_raw = max(0, min(100, int(ent.get("default_investment", 50))))
    id_load_raw = max(0, min(100, int(ent.get("default_identity_load", 50))))
    mult_inv = INVEST_MULT.get(baseline, 1.0)
    mult_id = IDENTITY_MULT.get(baseline, 1.0)
    inv = max(0, min(100, int(inv_raw * mult_inv)))
    id_load = max(0, min(100, int(id_load_raw * mult_id)))
    base_fb = 60 if baseline in ("entitled", "hopeful") else 45
    feasibility_belief = max(10, min(90, base_fb + rng.randint(-10, 10)))
    social_support = max(0, min(100, 55 + rng.randint(-15, 15)))
    tags = [str(x) for x in (ent.get("tags") or []) if isinstance(x, str)][:30]
    costs = [str(x) for x in (ent.get("costs") or []) if isinstance(x, str)][:20]
    secrecy = max(0, min(100, int(ent.get("secrecy", 0))))
    return StrivingObject(
        id=pid,
        label=label,
        need_axis=need_axis,
        started_age=age,
        investment=inv,
        identity_load=id_load,
        feasibility_belief=feasibility_belief,
        social_support=social_support,
        recent_momentum=rng.randint(-10, 10),
        tags=tags,
        secrecy=secrecy,
        costs=costs,
        active=True,
    )


def spawn_striving_objects_for_age(
    age: int,
    expectation_baseline: dict[str, str],
    existing: list[StrivingObject],
    existing_ids: set[str],
    year: int,
    map_data: dict[str, Any] | None = None,
    max_new: int = 2,
    use_budget_by_age: bool = False,
    use_weighted_axis: bool = False,
    rng: random.Random | None = None,
) -> list[StrivingObject]:
    """
    Return 0--max_new StrivingObjects for this age and baseline.
    Spawns from all 4 baselines (entitled, hopeful, forbidden, hopeless). Uses baseline multipliers.
    Skips candidate if tag-similar to existing or already-spawned. use_budget_by_age: cap by spawn_budget_for_age.
    use_weighted_axis: pick axis by weighted random (entitled/hopeful slightly preferred).
    """
    map_data = map_data or load_proxy_striving_map()
    proxies = map_data.get("proxies") or {}
    if not proxies:
        return []
    rng = rng or random.Random()
    budget = spawn_budget_for_age(age, rng) if use_budget_by_age else max_new
    cap = min(max_new, budget) if use_budget_by_age else max_new
    bracket = _nearest_bracket(age)
    out: list[StrivingObject] = []
    axes_order = list(NEED_AXES)
    if use_weighted_axis:
        weights = []
        for ax in axes_order:
            b = expectation_baseline.get(ax) or "hopeful"
            w = SPAWN_MULT.get(b, 1.0)
            weights.append(w)
        # draw axes with replacement until we have enough candidates to try
        tries_left = 20
        while len(out) < cap and tries_left > 0:
            tries_left -= 1
            ax = rng.choices(axes_order, weights=weights, k=1)[0]
            baseline = expectation_baseline.get(ax) or "hopeful"
            axis_proxies = proxies.get(ax)
            if not isinstance(axis_proxies, dict):
                continue
            by_baseline = axis_proxies.get(baseline)
            if not isinstance(by_baseline, dict):
                continue
            entries = by_baseline.get(bracket) or by_baseline.get(str(bracket)) or []
            if not entries:
                continue
            ent = rng.choice(entries)
            if not isinstance(ent, dict):
                continue
            cand_tags = [str(x) for x in (ent.get("tags") or []) if isinstance(x, str)]
            if any(_is_similar(e, cand_tags, ax) for e in existing + out):
                continue
            if rng.random() > min(1.0, 0.75 * SPAWN_MULT.get(baseline, 1.0)):
                continue
            obj = _make_object_from_entry(ent, ax, age, year, baseline, existing_ids, rng)
            if obj is not None:
                out.append(obj)
        return out
    # Deterministic order (original behavior)
    for need_axis in axes_order:
        if len(out) >= cap:
            break
        baseline = expectation_baseline.get(need_axis) or "hopeful"
        axis_proxies = proxies.get(need_axis)
        if not isinstance(axis_proxies, dict):
            continue
        by_baseline = axis_proxies.get(baseline)
        if not isinstance(by_baseline, dict):
            continue
        entries = by_baseline.get(bracket) or by_baseline.get(str(bracket)) or []
        if not isinstance(entries, list):
            continue
        for ent in entries:
            if len(out) >= cap:
                break
            if not isinstance(ent, dict):
                continue
            cand_tags = [str(x) for x in (ent.get("tags") or []) if isinstance(x, str)]
            if any(_is_similar(e, cand_tags, need_axis) for e in existing + out):
                continue
            obj = _make_object_from_entry(ent, need_axis, age, year, baseline, existing_ids, rng)
            if obj is not None:
                out.append(obj)
    return out


def update_existing_objects(state: BackboneState, config: dict[str, Any], rng: random.Random | None = None) -> None:
    """
    Mutate existing striving objects: momentum decay, investment/identity_load drift, retire when faded.
    Then remove inactive from state.striving_objects to bound list size.
    """
    rng = rng or random.Random()
    striving_cfg = config.get("striving") or {}
    retire_prob = float(striving_cfg.get("retire_prob", RETIRE_PROB))
    for s in state.striving_objects:
        if not getattr(s, "active", True):
            continue
        s.recent_momentum = int(s.recent_momentum * 0.6)
        drift = (s.recent_momentum // 10) + (s.feasibility_belief - 50) // 25 + (s.social_support - 50) // 40
        s.investment = max(0, min(100, s.investment + drift))
        ident_drift = (s.investment - 50) // 35 + (getattr(s, "secrecy", 0) - 50) // 60
        s.identity_load = max(0, min(100, s.identity_load + ident_drift))
        if (
            s.investment < RETIRE_INVESTMENT_THRESHOLD
            and s.identity_load < RETIRE_IDENTITY_THRESHOLD
            and rng.random() < retire_prob
        ):
            s.active = False
        s.clamp_all()
    state.striving_objects = [s for s in state.striving_objects if getattr(s, "active", True)]


def update_striving_step(
    state: BackboneState,
    derived: Any,
    config: dict[str, Any],
) -> None:
    """
    Yearly step: update existing (drift, retire), then spawn 0--max_new from proxy_striving_map.
    Spawns from all baselines. Optionally use budget-by-age and weighted axis selection from config.
    """
    striving_cfg = config.get("striving") or {}
    max_new = int(striving_cfg.get("max_new_per_year", 2))
    max_new = max(0, min(5, max_new))
    use_budget = bool(striving_cfg.get("use_budget_by_age", False))
    use_weighted = bool(striving_cfg.get("use_weighted_axis", False))
    for ax in NEED_AXES:
        state.expectation_baseline.setdefault(ax, "hopeful")
    update_existing_objects(state, config)
    existing = [s for s in state.striving_objects if getattr(s, "active", True)]
    existing_ids = {s.id for s in existing}
    new_objs = spawn_striving_objects_for_age(
        state.age,
        state.expectation_baseline,
        existing,
        existing_ids,
        state.year,
        max_new=max_new,
        use_budget_by_age=use_budget,
        use_weighted_axis=use_weighted,
    )
    for obj in new_objs:
        state.striving_objects.append(obj)
