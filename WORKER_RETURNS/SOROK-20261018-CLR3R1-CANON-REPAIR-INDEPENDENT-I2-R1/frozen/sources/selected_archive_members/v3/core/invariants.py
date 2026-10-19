# v3/core/invariants.py
# Hard invariants from v3config. Fail fast; no silent drift.
# Wave 2.1: state integrity (clamps, list caps). Wave 2.2: architecture (render/events/derived/step order).
# Spec §12: at least 2 cracks, at least 2 frameworks, expressed aim gated.

from __future__ import annotations

import hashlib
import json
from typing import Any

from v3.core.enums import DEFAULT_MAX, DEFAULT_MIN
from v3.core.state import BackboneState, Crack, Framework

# Derived index names; BackboneState must not have these as stored fields (Wave 2.2).
DERIVED_INDEX_NAMES = frozenset({
    "hostage_index",
    "agency_capacity_AC",
    "insulation_score",
    "structural_lucidity_SL",
    "mis_aim_risk",
    "peak_regime",
})

# Spec §12: minimum cracks/frameworks unless explicitly insulated
MIN_CRACKS_DEFAULT = 2
MIN_FRAMEWORKS_DEFAULT = 2
EXPRESSED_AIM_THRESHOLD = 10.0  # treat as "non-empty" above this
COERCION_MAX_FOR_EXPRESSED_AIM = 60.0  # expressed aim allowed if coercion proxy below this
DEFIANCE_ORGANIZING_MIN = 40.0
HOSTAGE_MAX_FOR_DEFIANCE = 50.0
AGENCY_MIN_FOR_DEFIANCE = 40.0
BINDING_MIN_FOR_DEFIANCE = 40.0


# Default limits when config not provided (match v3config)
CRACKS_MAX_TOTAL = 8
CRACKS_MAX_ACTIVE = 3
BUFFERS_MAX_TOTAL = 8
FRAMEWORKS_MAX_ACTIVE = 6


def _get_limits(config: dict[str, Any] | None) -> tuple[int, int, int, int]:
    """(cracks_max_total, cracks_max_active, buffers_max_total, frameworks_max_active)."""
    if not config:
        return CRACKS_MAX_TOTAL, CRACKS_MAX_ACTIVE, BUFFERS_MAX_TOTAL, FRAMEWORKS_MAX_ACTIVE
    stored = config.get("stored_state_schema") or {}
    cracks = stored.get("cracks") or {}
    buffers = stored.get("buffers") or {}
    frameworks = stored.get("frameworks") or {}
    return (
        int(cracks.get("max_total", CRACKS_MAX_TOTAL)),
        int(cracks.get("max_active", CRACKS_MAX_ACTIVE)),
        int(buffers.get("max_total", BUFFERS_MAX_TOTAL)),
        int(frameworks.get("max_active", FRAMEWORKS_MAX_ACTIVE)),
    )


def _collect_numeric_values(obj: Any, prefix: str = "") -> list[tuple[str, float]]:
    """Recursively collect (path, value) for all numeric fields in dataclass-like obj."""
    out: list[tuple[str, float]] = []
    if hasattr(obj, "__dataclass_fields__"):
        for k in obj.__dataclass_fields__:
            v = getattr(obj, k, None)
            path = f"{prefix}.{k}" if prefix else k
            if isinstance(v, (int, float)):
                out.append((path, float(v)))
            elif hasattr(v, "__dataclass_fields__"):
                out.extend(_collect_numeric_values(v, path))
            elif isinstance(v, dict):
                for k2, v2 in v.items():
                    if isinstance(v2, (int, float)):
                        out.append((f"{path}.{k2}", float(v2)))
                    elif hasattr(v2, "__dataclass_fields__"):
                        out.extend(_collect_numeric_values(v2, f"{path}.{k2}"))
            elif isinstance(v, list):
                for i, item in enumerate(v):
                    if hasattr(item, "__dataclass_fields__"):
                        out.extend(_collect_numeric_values(item, f"{path}[{i}]"))
                    elif isinstance(item, (int, float)):
                        out.append((f"{path}[{i}]", float(item)))
    return out


# Numeric fields that are not on the 0-100 scale (excluded from clamp invariant).
CLAMP_EXCLUDE_PATHS = frozenset({"year", "age"})
# Any path whose last component is year/age is excluded (e.g. rupture_shards[0].year, rendered_output.age).
CLAMP_EXCLUDE_LAST_COMPONENT = frozenset({"year", "age"})
CLAMP_EXCLUDE_SUFFIXES = ("origin_year", "start_year", "start_age", "tenure_years", "half_life_years", "plasticity_years_left", "recent_momentum")  # StrivingObject.recent_momentum is -50..+50
# Paths containing these substrings are excluded (e.g. downstream_biases are bias deltas, can be negative).
# acute_delta/chronic_delta on Framework are signed capacity deltas (e.g. coherence=-1.0), not 0-100 values.
CLAMP_EXCLUDE_PATH_SUBSTRINGS = (
    "downstream_biases",
    "acute_delta",
    "chronic_delta",
    "yearly_integrity",
    "initial_state_provenance",
    "provenance",
)


def assert_all_numeric_clamped(
    state: BackboneState,
    lo: float = DEFAULT_MIN,
    hi: float = DEFAULT_MAX,
) -> None:
    """Raise AssertionError if any numeric field in state is outside [lo, hi]. year and age are excluded."""
    for path, val in _collect_numeric_values(state):
        if path in CLAMP_EXCLUDE_PATHS:
            continue
        # rupture_shards[].year, metabolization_processes[].start_year, etc. are calendar years
        last = path.split(".")[-1].split("[")[0]
        if last in CLAMP_EXCLUDE_LAST_COMPONENT:
            continue
        if path.startswith("rendered_output."):
            continue  # rendered_output holds year (calendar), age, and narrative payload; not 0-100 indices
        if any(path.endswith(s) for s in CLAMP_EXCLUDE_SUFFIXES):
            continue
        if any(sub in path for sub in CLAMP_EXCLUDE_PATH_SUBSTRINGS):
            continue  # e.g. metabolization_processes[].downstream_biases: bias deltas, not 0-100
        if val < lo or val > hi:
            raise AssertionError(
                f"invariant all_numeric_fields_clamped_0_100: {path}={val} outside [{lo}, {hi}]"
            )
    # alienation
    if state.alienation < lo or state.alienation > hi:
        raise AssertionError(
            f"invariant alienation clamped: alienation={state.alienation} outside [{lo}, {hi}]"
        )


def assert_cracks_limits(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Raise AssertionError if len(cracks) > max_total or active_cracks > max_active."""
    max_total, max_active, _, _ = _get_limits(config)
    n = len(state.cracks)
    if n > max_total:
        raise AssertionError(
            f"invariant len(cracks) <= cracks.max_total: len(cracks)={n} > {max_total}"
        )
    active = sum(1 for c in state.cracks if getattr(c, "active", False))
    if active > max_active:
        raise AssertionError(
            f"invariant active_cracks_count <= cracks.max_active: active={active} > {max_active}"
        )


def assert_buffers_limits(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Raise AssertionError if len(buffers) > max_total."""
    _, _, max_buffers, _ = _get_limits(config)
    n = len(state.buffers)
    if n > max_buffers:
        raise AssertionError(
            f"invariant len(buffers) <= buffers.max_total: len(buffers)={n} > {max_buffers}"
        )


def assert_frameworks_limits(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Raise AssertionError if more than max_active frameworks have weight > 0 (or count all if no threshold)."""
    _, _, _, max_active = _get_limits(config)
    # Count frameworks with non-zero weight as "active"
    active = sum(1 for f in state.frameworks if getattr(f, "weight", 0) > 0)
    if active > max_active:
        raise AssertionError(
            f"invariant frameworks active <= max_active: active={active} > {max_active}"
        )


def _get_min_cracks_frameworks(config: dict[str, Any] | None) -> tuple[int, int]:
    """(min_cracks, min_frameworks) from config or spec defaults."""
    if not config:
        return MIN_CRACKS_DEFAULT, MIN_FRAMEWORKS_DEFAULT
    inv = config.get("invariants") or {}
    return (
        int(inv.get("min_cracks", MIN_CRACKS_DEFAULT)),
        int(inv.get("min_frameworks", MIN_FRAMEWORKS_DEFAULT)),
    )


def assert_min_cracks(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Spec §12: at least min_cracks (default 2) unless explicitly insulated."""
    min_cracks, _ = _get_min_cracks_frameworks(config)
    if getattr(state, "insulated", False):
        return
    n = len(state.cracks)
    if n < min_cracks:
        raise AssertionError(
            f"invariant min_cracks: len(cracks)={n} < {min_cracks} (insulated={getattr(state, 'insulated', False)})"
        )


def assert_min_frameworks(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Spec §12: at least min_frameworks (default 2) with weight above threshold, or explicit mono-framework insulation."""
    _, min_frameworks = _get_min_cracks_frameworks(config)
    if getattr(state, "mono_framework_insulation", False):
        return
    active = sum(1 for f in state.frameworks if getattr(f, "weight", 0) > 0)
    if active < min_frameworks:
        raise AssertionError(
            f"invariant min_frameworks: frameworks with weight>0 = {active} < {min_frameworks}"
        )


def assert_expressed_aim_gated(
    state: BackboneState,
    config: dict[str, Any] | None = None,
    derived: Any = None,
) -> None:
    """Spec §12: expressed aim non-empty in public only if coercion below threshold OR defiance channel + low hostage + high agency/binding."""
    if derived is None:
        return
    coercion_proxy = 50.0
    if isinstance(getattr(state.field, "raw", None), dict):
        coercion_proxy = float(state.field.raw.get("repression_baseline", 50))
    organizing = getattr(state.practice_stack, "organizing", 0) or 0
    hostage = getattr(derived, "hostage_index", 50) or 50
    agency = getattr(state.psychological_capacity, "agency", None) or getattr(state.capacity, "legitimacy", 50) or 50
    binding = getattr(state.psychological_capacity, "binding", None) or getattr(state.capacity, "social_support", 50) or 50

    for _domain_name, d in state.domains.items():
        expressed = getattr(d, "expressed_aim", 0) or 0
        if expressed <= EXPRESSED_AIM_THRESHOLD:
            continue
        allowed = (
            coercion_proxy < COERCION_MAX_FOR_EXPRESSED_AIM
            or (
                organizing >= DEFIANCE_ORGANIZING_MIN
                and hostage <= HOSTAGE_MAX_FOR_DEFIANCE
                and agency >= AGENCY_MIN_FOR_DEFIANCE
                and binding >= BINDING_MIN_FOR_DEFIANCE
            )
        )
        if not allowed:
            raise AssertionError(
                f"invariant expressed_aim_gated: domain has expressed_aim={expressed} but coercion={coercion_proxy:.0f} and defiance/hostage/agency/binding do not allow"
            )


def ensure_min_cracks(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Ensure at least min_cracks exist; append placeholder cracks if below (for seeds that start with 0)."""
    min_cracks, _ = _get_min_cracks_frameworks(config)
    added = 0
    while len(state.cracks) < min_cracks:
        state.cracks.append(Crack(type="placeholder", intensity=5.0, latent_pressure=5.0, active=True, origin_year=state.year))
        added += 1
    if added:
        yearly = getattr(state, "yearly_integrity", None)
        if isinstance(yearly, dict):
            placeholder_counts = yearly.setdefault("placeholder_counts", {})
            if isinstance(placeholder_counts, dict):
                placeholder_counts["cracks"] = int(placeholder_counts.get("cracks", 0)) + added
            repair = yearly.setdefault("placeholder_repair", {"status": "degraded", "reasons": [], "added": 0})
            reasons = list(repair.get("reasons") or [])
            reasons.append("placeholder_cracks_required")
            repair["status"] = "degraded"
            repair["reasons"] = list(dict.fromkeys(reasons))
            repair["added"] = int(repair.get("added", 0)) + added


def ensure_min_frameworks(
    state: BackboneState,
    config: dict[str, Any] | None = None,
) -> None:
    """Ensure at least min_frameworks have weight > 0; append placeholder framework if below."""
    _, min_frameworks = _get_min_cracks_frameworks(config)
    active = sum(1 for f in state.frameworks if getattr(f, "weight", 0) > 0)
    added = 0
    while active < min_frameworks:
        state.frameworks.append(Framework(id=f"placeholder_{len(state.frameworks)}", weight=5.0))
        active += 1
        added += 1
    if added:
        yearly = getattr(state, "yearly_integrity", None)
        if isinstance(yearly, dict):
            placeholder_counts = yearly.setdefault("placeholder_counts", {})
            if isinstance(placeholder_counts, dict):
                placeholder_counts["frameworks"] = int(placeholder_counts.get("frameworks", 0)) + added
            repair = yearly.setdefault("placeholder_repair", {"status": "degraded", "reasons": [], "added": 0})
            reasons = list(repair.get("reasons") or [])
            reasons.append("placeholder_frameworks_required")
            repair["status"] = "degraded"
            repair["reasons"] = list(dict.fromkeys(reasons))
            repair["added"] = int(repair.get("added", 0)) + added


def assert_backbone_invariants(
    state: BackboneState,
    config: dict[str, Any] | None = None,
    derived: Any = None,
    check_clamp: bool = True,
    check_cracks: bool = True,
    check_buffers: bool = True,
    check_frameworks: bool = True,
    check_min_cracks: bool = True,
    check_min_frameworks: bool = True,
    check_expressed_aim_gated: bool = True,
    repair_min_counts: bool = False,
) -> None:
    """Run all hard invariants. Raise on first failure. If repair_min_counts, ensure min cracks/frameworks before asserting."""
    if repair_min_counts:
        ensure_min_cracks(state, config)
        ensure_min_frameworks(state, config)
    if check_clamp:
        assert_all_numeric_clamped(state)
    if check_cracks:
        assert_cracks_limits(state, config)
    if check_buffers:
        assert_buffers_limits(state, config)
    if check_frameworks:
        assert_frameworks_limits(state, config)
    if check_min_cracks:
        assert_min_cracks(state, config)
    if check_min_frameworks:
        assert_min_frameworks(state, config)
    if check_expressed_aim_gated and derived is not None:
        assert_expressed_aim_gated(state, config, derived)


# --- Wave 2.2: Architecture integrity ---

def backbone_hash(state: BackboneState) -> str:
    """Hash of backbone state excluding rendered_output (for render non-mutation test)."""
    from v3.io.json_codec import state_to_dict
    d = state_to_dict(state)
    d.pop("rendered_output", None)
    return hashlib.sha256(json.dumps(d, sort_keys=True).encode()).hexdigest()


def assert_no_derived_fields_in_backbone() -> None:
    """BackboneState must not have stored fields named like derived indices (no persistence of derived)."""
    backbone_fields = set(BackboneState.__dataclass_fields__)
    overlap = backbone_fields & DERIVED_INDEX_NAMES
    if overlap:
        raise AssertionError(
            f"invariant derived_indices_not_stored: BackboneState must not have fields {overlap}; "
            "derived indices are computed only, not persisted."
        )
