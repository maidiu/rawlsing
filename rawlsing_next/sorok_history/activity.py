"""T4 independent activity consumption from owner-admitted historical depth.

This module is a world-side consumer. It reads one exact ``physical_depth``
fact from the same ``HistoricalWorld`` target index used by the P4 foreground,
verifies the fact's target/job/parent-event provenance through the existing
owner, and only then calls the existing P2/P3/P4 S46 activity entry point
``run_p4.advance``. It never inspects, narrates, generates history, calls a
model, or writes actor psychology.
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
PROPERTY_SOURCE = "physical_depth"

TARGET_UNKNOWN = "HISTORICAL_TARGET_UNKNOWN"
TARGET_MISMATCH = "HISTORICAL_TARGET_PROVENANCE_MISMATCH"
SCOPE_MISMATCH = "HISTORICAL_SCOPE_MISMATCH"
PARENT_MISSING = "HISTORICAL_PARENT_MISSING"
PLACE_MISMATCH = "HISTORICAL_MATERIAL_NOT_IN_ACTIVITY_PLACE"
DEPTH_MISSING = "HISTORICAL_DEPTH_MISSING"
FACT_MISMATCH = "HISTORICAL_DEPTH_FACT_PROVENANCE_MISMATCH"
JOB_MISSING = "HISTORICAL_DEPTH_JOB_MISSING"
JOB_NOT_ADMITTED = "HISTORICAL_DEPTH_JOB_NOT_ADMITTED"
EVENT_MISMATCH = "HISTORICAL_DEPTH_EVENT_PROVENANCE_MISMATCH"
VALUE_MISMATCH = "HISTORICAL_DEPTH_VALUE_MISMATCH"
WORLD_MISMATCH = "HISTORICAL_MATERIAL_WORLD_MISMATCH"
CALL_SITE_UNAVAILABLE = "P4_ACTIVITY_CALL_SITE_UNAVAILABLE"
CALL_SITE_INVALID = "P4_ACTIVITY_CALL_SITE_INVALID_RESULT"
INVALID_REQUEST = "INVALID_ACTIVITY_REQUEST"

_ADMITTED_JOB_STATUSES = frozenset({"INDEX_READY", "PARTIAL_HELD"})


def _canonical(document: Any) -> str:
    return json.dumps(document, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _digest(document: Any) -> str:
    return sha256(_canonical(document).encode("utf-8")).hexdigest()


class ActivityRefusal(ValueError):
    """A malformed activity request, not a missing world fact."""


@dataclass(frozen=True)
class ActivityReceipt:
    """Immutable T4 receipt: admitted depth provenance -> actual S46 path."""

    schema: str
    grade: str
    status: str
    target_id: str
    target_version: int | None
    predicate: str
    expected: Any
    observed: Any
    property_source: str
    fact_id: str | None
    job_id: str | None
    job_status: str | None
    admission_status: str | None
    fact_parent_event_ref: Mapping[str, Any] | None
    fact_claim_ref: Mapping[str, Any] | None
    property_hash: str | None
    target_hash: str | None
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
            "target_version": self.target_version,
            "predicate": self.predicate,
            "expected": deepcopy(self.expected),
            "observed": deepcopy(self.observed),
            "property_source": self.property_source,
            "fact_id": self.fact_id,
            "job_id": self.job_id,
            "job_status": self.job_status,
            "admission_status": self.admission_status,
            "fact_parent_event_ref": deepcopy(self.fact_parent_event_ref),
            "fact_claim_ref": deepcopy(self.fact_claim_ref),
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


def _material(session: Any) -> int | None:
    try:
        return int(session.world().actor_state.get("A", {}).get("material_remaining"))
    except (TypeError, ValueError, AttributeError):
        return None


def _exact_ref(value: Any) -> Mapping[str, Any] | None:
    if (not isinstance(value, Mapping)
            or set(value) != {"kind", "object_id", "content_hash"}
            or not isinstance(value.get("kind"), str) or not value["kind"]
            or not isinstance(value.get("object_id"), str) or not value["object_id"]
            or not isinstance(value.get("content_hash"), str)
            or len(value["content_hash"]) != 64):
        return None
    return value


def _accepted_fact_ids(job: Mapping[str, Any]) -> set[str]:
    admission = job.get("admission") or {}
    accepted = admission.get("accepted") or []
    return {
        fact_id
        for group in accepted if isinstance(group, Mapping)
        for fact_id in (group.get("fact_ids") or ())
        if isinstance(fact_id, str)
    }


def _receipt(
    *,
    status: str,
    target_id: str,
    target: Mapping[str, Any] | None,
    predicate: str,
    expected: Any,
    observed: Any,
    fact: Mapping[str, Any] | None,
    job: Mapping[str, Any] | None,
    root: str,
    branch: str,
    clock_before: int,
    clock_after: int,
    material_before: int | None,
    material_after: int | None,
    interval: Mapping[str, Any] | None,
    refusal_code: str | None = None,
) -> ActivityReceipt:
    fact = fact or {}
    job = job or {}
    admission = job.get("admission") or {}
    parent_ref = _exact_ref(fact.get("parent_event_ref"))
    claim_ref = _exact_ref(fact.get("claim_ref"))
    return ActivityReceipt(
        schema=ACTIVITY_SCHEMA,
        grade=ACTIVITY_GRADE,
        status=status,
        target_id=target_id,
        target_version=target.get("version") if target is not None else None,
        predicate=predicate,
        expected=deepcopy(expected),
        observed=deepcopy(observed),
        property_source=PROPERTY_SOURCE,
        fact_id=fact.get("id") if isinstance(fact.get("id"), str) else None,
        job_id=job.get("id") if isinstance(job.get("id"), str) else None,
        job_status=job.get("status") if isinstance(job.get("status"), str) else None,
        admission_status=(
            admission.get("status") if isinstance(admission.get("status"), str) else None
        ),
        fact_parent_event_ref=deepcopy(parent_ref),
        fact_claim_ref=deepcopy(claim_ref),
        property_hash=_digest(fact) if fact else None,
        target_hash=_digest(target) if target is not None else None,
        root=root,
        branch=branch,
        clock_before=clock_before,
        clock_after=clock_after,
        material_before=material_before,
        material_after=material_after,
        interval=deepcopy(interval),
        refusal_code=refusal_code,
    )


def _admitted_depth(
    history: Any, target_id: str, predicate: str
) -> tuple[Mapping[str, Any] | None, Mapping[str, Any] | None, str | None]:
    """Return (target, fact, refusal_code) after exact owner provenance checks."""
    target = history.target(target_id)
    if target is None:
        return None, None, TARGET_UNKNOWN
    if (target.get("root"), target.get("branch")) != _scope(history.session):
        return target, None, SCOPE_MISMATCH
    surface = target.get("surface") or {}
    surface_event = history.session.event(surface.get("occurrence_id"))
    if surface_event is None or surface_event.get("hash") != target.get("parent_hash"):
        return target, None, PARENT_MISSING
    depth = target.get("physical_depth") or {}
    fact = depth.get(predicate) if isinstance(depth, Mapping) else None
    if not isinstance(fact, Mapping):
        return target, None, DEPTH_MISSING
    if (fact.get("target_id") != target_id
            or fact.get("predicate") != predicate
            or "value" not in fact):
        return target, fact, FACT_MISMATCH
    fact_id = fact.get("id")
    if not isinstance(fact_id, str) or not fact_id:
        return target, fact, FACT_MISMATCH
    parent_ref = _exact_ref(fact.get("parent_event_ref"))
    if parent_ref is None:
        return target, fact, EVENT_MISMATCH
    parent_event = history.session.event(parent_ref["object_id"])
    if (parent_event is None
            or parent_event.get("hash") != parent_ref["content_hash"]):
        return target, fact, EVENT_MISMATCH
    if (fact.get("parent_hash") != target.get("parent_hash")
            or parent_ref["object_id"] != surface["occurrence_id"]
            or parent_ref["content_hash"] != target.get("parent_hash")):
        return target, fact, EVENT_MISMATCH
    if not isinstance(fact.get("claim_ref"), Mapping):
        return target, fact, FACT_MISMATCH
    job_id = fact.get("job_id")
    if not isinstance(job_id, str) or not job_id:
        return target, fact, JOB_MISSING
    job = history.job(job_id)
    if job is None:
        return target, fact, JOB_MISSING
    if job.get("target_id") != target_id:
        return target, fact, TARGET_MISMATCH
    if (job.get("status") not in _ADMITTED_JOB_STATUSES
            or (job.get("admission") or {}).get("status") not in _ADMITTED_JOB_STATUSES
            or fact_id not in _accepted_fact_ids(job)):
        return target, fact, JOB_NOT_ADMITTED
    return target, fact, None


def advance_independent_activity(
    fanin: Any,
    history: Any,
    *,
    target_id: str,
    predicate: str = "condition",
    expected: Any,
    advance: Callable[[Any], Mapping[str, Any]] | None = None,
) -> ActivityReceipt:
    """Consume one owner-admitted depth fact, then advance the real S46 activity.

    ``physical_depth`` is the only property source. Missing depth is HELD, not
    turned into a physical negative. The owner job, accepted fact, target and
    exact parent event must all agree before ``run_p4.advance`` is reached.
    """
    if not isinstance(target_id, str) or not target_id:
        raise ActivityRefusal(INVALID_REQUEST)
    if not isinstance(predicate, str) or not predicate:
        raise ActivityRefusal(INVALID_REQUEST)
    session = fanin.session
    root, branch = _scope(session)
    clock_before = session.clock()
    material_before = _material(session)
    target, fact, refusal = _admitted_depth(history, target_id, predicate)
    if refusal is not None:
        return _receipt(
            status=HELD, target_id=target_id, target=target,
            predicate=predicate, expected=expected, observed=None,
            fact=fact, job=history.job(fact.get("job_id"))
            if isinstance(fact, Mapping) and isinstance(fact.get("job_id"), str) else None,
            root=root, branch=branch, clock_before=clock_before,
            clock_after=session.clock(), material_before=material_before,
            material_after=_material(session), interval=None,
            refusal_code=refusal,
        )
    observed = fact["value"]
    if observed != expected:
        return _receipt(
            status=HELD, target_id=target_id, target=target,
            predicate=predicate, expected=expected, observed=observed,
            fact=fact, job=history.job(fact["job_id"]), root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=VALUE_MISMATCH,
        )
    world = session.world()
    location = target["surface"]["location"]
    if world.positions.get("A") != location:
        return _receipt(
            status=HELD, target_id=target_id, target=target,
            predicate=predicate, expected=expected, observed=observed,
            fact=fact, job=history.job(fact["job_id"]), root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=PLACE_MISMATCH,
        )
    resource = world.resources.get(location) or {}
    if predicate in resource and resource.get(predicate) != observed:
        return _receipt(
            status=HELD, target_id=target_id, target=target,
            predicate=predicate, expected=expected, observed=observed,
            fact=fact, job=history.job(fact["job_id"]), root=root, branch=branch,
            clock_before=clock_before, clock_after=session.clock(),
            material_before=material_before, material_after=_material(session),
            interval=None, refusal_code=WORLD_MISMATCH,
        )
    call = advance or _default_advance
    interval = call(fanin)
    if not isinstance(interval, Mapping):
        raise ActivityRefusal(CALL_SITE_INVALID)
    return _receipt(
        status=ADVANCED, target_id=target_id, target=target,
        predicate=predicate, expected=expected, observed=observed,
        fact=fact, job=history.job(fact["job_id"]), root=root, branch=branch,
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
    "CALL_SITE_INVALID",
    "CALL_SITE_UNAVAILABLE",
    "DEPTH_MISSING",
    "EVENT_MISMATCH",
    "FACT_MISMATCH",
    "HELD",
    "INVALID_REQUEST",
    "JOB_MISSING",
    "JOB_NOT_ADMITTED",
    "PARENT_MISSING",
    "PLACE_MISMATCH",
    "PROPERTY_SOURCE",
    "SCOPE_MISMATCH",
    "TARGET_MISMATCH",
    "TARGET_UNKNOWN",
    "VALUE_MISMATCH",
    "WORLD_MISMATCH",
    "advance_independent_activity",
    "consume_independent_activity",
    "run_independent_activity",
]
