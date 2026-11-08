"""T4 independent activity consumption from the HistoricalWorld index.

This module is a world-side consumer.  It resolves one exact material
property from the same committed ``HistoricalWorld`` target index used by the
P4 foreground, refuses meaningfully when that property is unknown or absent,
and only then calls the existing P2/P3/P4 S46 activity producer.  It does not
inspect, narrate, generate history, create a model request, or write actor
psychology.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass
from hashlib import sha256
import json
from typing import Any, Callable, Mapping


ACTIVITY_SCHEMA = "SOROK_HISTORY_INDEPENDENT_ACTIVITY@1"
ACTIVITY_GRADE = "SOURCEFREE_TEST_ONLY"
HELD = "HELD"
ADVANCED = "ADVANCED"

PROPERTY_MISSING = "HISTORICAL_MATERIAL_PROPERTY_MISSING"
PARENT_MISSING = "HISTORICAL_PARENT_MISSING"
PROPERTY_UNAVAILABLE = "HISTORICAL_MATERIAL_PROPERTY_UNAVAILABLE"
TARGET_UNKNOWN = "HISTORICAL_TARGET_UNKNOWN"
SCOPE_MISMATCH = "HISTORICAL_SCOPE_MISMATCH"
PLACE_MISMATCH = "HISTORICAL_MATERIAL_NOT_IN_ACTIVITY_PLACE"
WORLD_MISMATCH = "HISTORICAL_MATERIAL_WORLD_MISMATCH"
CALL_SITE_UNAVAILABLE = "P4_ACTIVITY_CALL_SITE_UNAVAILABLE"
INVALID_REQUEST = "INVALID_ACTIVITY_REQUEST"


def _canonical(document: Any) -> str:
    return json.dumps(document, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _digest(document: Any) -> str:
    return sha256(_canonical(document).encode("utf-8")).hexdigest()


class ActivityRefusal(ValueError):
    """A malformed activity request, not a missing world fact."""


@dataclass(frozen=True)
class ActivityReceipt:
    """Immutable T4 receipt: exact material gate -> actual S46 path."""

    schema: str
    grade: str
    status: str
    target_id: str
    predicate: str
    expected: Any
    observed: Any
    property_source: str | None
    property_hash: str | None
    target_hash: str
    root: str
    branch: str
    clock_before: int
    clock_after: int
    material_before: int | None
    material_after: int | None
    interval: Mapping[str, Any] | None
    refusal_code: str | None = None
    user_visible: bool = False
    writes_authority: bool = False
    psychology_claim: bool = False

    @property
    def advanced(self) -> bool:
        return self.status == ADVANCED

    @property
    def held(self) -> bool:
        return self.status == HELD

    def as_dict(self) -> dict[str, Any]:
        return {
            "schema": self.schema,
            "grade": self.grade,
            "status": self.status,
            "target_id": self.target_id,
            "predicate": self.predicate,
            "expected": self.expected,
            "observed": self.observed,
            "property_source": self.property_source,
            "property_hash": self.property_hash,
            "target_hash": self.target_hash,
            "root": self.root,
            "branch": self.branch,
            "clock_before": self.clock_before,
            "clock_after": self.clock_after,
            "material_before": self.material_before,
            "material_after": self.material_after,
            "interval": deepcopy(self.interval),
            "refusal_code": self.refusal_code,
            "user_visible": self.user_visible,
            "writes_authority": self.writes_authority,
            "psychology_claim": self.psychology_claim,
        }


def _default_advance(fanin: Any) -> Mapping[str, Any]:
    try:
        from run_p4 import advance
    except ImportError as exc:
        raise ActivityRefusal(CALL_SITE_UNAVAILABLE) from exc
    return advance(fanin)


def _scope(session: Any) -> tuple[str, str]:
    return session.read_root()["root_hash"], session.branch_id


def _property_from_target(target: Mapping[str, Any], predicate: str) -> tuple[Any, str | None, str | None]:
    surface = target.get("surface") or {}
    physical = surface.get("physical") or {}
    if predicate in physical:
        value = physical[predicate]
        return value, "surface.physical", None
    depth = target.get("physical_depth") or {}
    if predicate in depth:
        row = depth[predicate]
        if isinstance(row, Mapping) and "value" in row:
            return row["value"], "physical_depth", row.get("id")
    return None, None, None


def _material(session: Any) -> int | None:
    try:
        return int(session.world().actor_state.get("A", {}).get("material_remaining"))
    except (TypeError, ValueError, AttributeError):
        return None


def _receipt(
    *,
    status: str,
    target_id: str,
    predicate: str,
    expected: Any,
    observed: Any,
    property_source: str | None,
    property_hash: str | None,
    target: Mapping[str, Any] | None,
    root: str,
    branch: str,
    clock_before: int,
    clock_after: int,
    material_before: int | None,
    material_after: int | None,
    interval: Mapping[str, Any] | None,
    refusal_code: str | None = None,
) -> ActivityReceipt:
    return ActivityReceipt(
        schema=ACTIVITY_SCHEMA,
        grade=ACTIVITY_GRADE,
        status=status,
        target_id=target_id,
        predicate=predicate,
        expected=deepcopy(expected),
        observed=deepcopy(observed),
        property_source=property_source,
        property_hash=property_hash,
        target_hash=_digest(target) if target is not None else _digest({"target_id": target_id}),
        root=root,
        branch=branch,
        clock_before=clock_before,
        clock_after=clock_after,
        material_before=material_before,
        material_after=material_after,
        interval=deepcopy(interval),
        refusal_code=refusal_code,
    )


def advance_independent_activity(
    fanin: Any,
    history: Any,
    *,
    target_id: str,
    predicate: str = "tool_available",
    expected: Any = True,
    advance: Callable[[Any], Mapping[str, Any]] | None = None,
) -> ActivityReceipt:
    """Resolve one committed material property and advance the real S46 activity.

    The property is read from the same ``HistoricalWorld`` target index as the
    committed P4 surface.  Missing/unknown is held, not converted into a
    physical negative.  A present property must agree with the world resource
    at the activity place before the existing ``run_p4.advance`` call site is
    reached.
    """
    if not isinstance(target_id, str) or not target_id:
        raise ActivityRefusal(INVALID_REQUEST)
    if not isinstance(predicate, str) or not predicate:
        raise ActivityRefusal(INVALID_REQUEST)
    session = fanin.session
    root, branch = _scope(session)
    clock_before = session.clock()
    material_before = _material(session)
    target = history.target(target_id)
    if target is None:
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=None, property_source=None,
            property_hash=None, target=None, root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=TARGET_UNKNOWN,
        )
    if (target.get("root"), target.get("branch")) != (root, branch):
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=None, property_source=None,
            property_hash=None, target=target, root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=SCOPE_MISMATCH,
        )
    surface = target.get("surface") or {}
    location = surface.get("location")
    parent = session.event(surface.get("occurrence_id"))
    if parent is None or parent.get("hash") != target.get("parent_hash"):
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=None, property_source=None,
            property_hash=None, target=target, root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=PARENT_MISSING,
        )
    world = session.world()
    actor_place = world.positions.get("A")
    if not location or actor_place != location:
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=None, property_source=None,
            property_hash=None, target=target, root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=PLACE_MISMATCH,
        )
    observed, source, fact_id = _property_from_target(target, predicate)
    if source is None:
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=None, property_source=None,
            property_hash=None, target=target, root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=PROPERTY_MISSING,
        )
    property_hash = _digest({
        "target_id": target_id, "predicate": predicate,
        "value": observed, "source": source, "fact_id": fact_id,
    })
    if observed != expected:
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=observed, property_source=source,
            property_hash=property_hash, target=target, root=root,
            branch=branch, clock_before=clock_before,
            clock_after=session.clock(), material_before=material_before,
            material_after=_material(session), interval=None,
            refusal_code=PROPERTY_UNAVAILABLE,
        )
    resource = world.resources.get(location) or {}
    if predicate in resource and resource.get(predicate) != observed:
        return _receipt(
            status=HELD, target_id=target_id, predicate=predicate,
            expected=expected, observed=observed, property_source=source,
            property_hash=property_hash, target=target, root=root,
            branch=branch, clock_before=clock_before,
            clock_after=session.clock(), material_before=material_before,
            material_after=_material(session), interval=None,
            refusal_code=WORLD_MISMATCH,
        )
    call = advance or _default_advance
    interval = call(fanin)
    if not isinstance(interval, Mapping):
        raise ActivityRefusal("P4_ACTIVITY_CALL_SITE_INVALID_RESULT")
    return _receipt(
        status=ADVANCED, target_id=target_id, predicate=predicate,
        expected=expected, observed=observed, property_source=source,
        property_hash=property_hash, target=target, root=root, branch=branch,
        clock_before=clock_before, clock_after=session.clock(),
        material_before=material_before, material_after=_material(session),
        interval=interval,
    )


consume_independent_activity = advance_independent_activity
run_independent_activity = advance_independent_activity


__all__ = [
    "ACTIVITY_GRADE",
    "ACTIVITY_SCHEMA",
    "ADVANCED",
    "ActivityReceipt",
    "ActivityRefusal",
    "CALL_SITE_UNAVAILABLE",
    "HELD",
    "INVALID_REQUEST",
    "PARENT_MISSING",
    "PLACE_MISMATCH",
    "PROPERTY_MISSING",
    "PROPERTY_UNAVAILABLE",
    "SCOPE_MISMATCH",
    "TARGET_UNKNOWN",
    "WORLD_MISMATCH",
    "advance_independent_activity",
    "consume_independent_activity",
    "run_independent_activity",
]
