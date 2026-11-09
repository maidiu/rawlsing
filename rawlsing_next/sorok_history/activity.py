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
REQUIREMENT_STALE = "HISTORICAL_ACTIVITY_REQUIREMENT_STALE"
REQUIREMENT_CONSUMED = "HISTORICAL_ACTIVITY_REQUIREMENT_CONSUMED"
REQUIREMENT_TARGET_MISSING = "HISTORICAL_ACTIVITY_TARGET_MISSING"
DISPATCHING = "DISPATCHING"
RECOVERED = "HISTORICAL_ACTIVITY_DISPATCH_RECOVERED"
RECOVERY_AMBIGUOUS = "HISTORICAL_ACTIVITY_RECOVERY_AMBIGUOUS"
RECOVERY_UNVERIFIED = "HISTORICAL_ACTIVITY_RECOVERY_UNVERIFIED"

REPAIR_TASK_ID = "S46_ACTUAL_REPAIR"
REPAIR_ACTION_KIND = "REPAIR"
REPAIR_PREDICATE = "condition"
REPAIR_EXPECTED = "serviceable"

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


@dataclass(frozen=True)
class ActivityDispatch:
    """Runtime dispatch result: durable requirement plus adapter receipt."""

    status: str
    requirement: Mapping[str, Any]
    activity: ActivityReceipt | None
    reason: str | None = None

    def __getitem__(self, key: str) -> Any:
        if key in {"status", "requirement", "activity", "reason"}:
            return getattr(self, key)
        raise KeyError(key)

    def as_dict(self) -> dict[str, Any]:
        return {
            "status": self.status,
            "requirement": deepcopy(self.requirement),
            "activity": self.activity.as_dict() if self.activity is not None else None,
            "reason": self.reason,
        }



def _default_advance(fanin: Any, *, dispatch_ref: str | None = None) -> Mapping[str, Any]:
    try:
        from run_p4 import advance
    except ImportError as exc:
        raise ActivityRefusal(CALL_SITE_UNAVAILABLE) from exc
    if dispatch_ref is None:
        return advance(fanin)
    return advance(fanin, dispatch_ref=dispatch_ref)


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
    dispatch_ref: str | None = None,
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
    if dispatch_ref is None:
        interval = call(fanin)
    else:
        interval = call(fanin, dispatch_ref=dispatch_ref)
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



def produce_activity_requirement(
    fanin: Any,
    history: Any,
    *,
    task_id: str = REPAIR_TASK_ID,
    action_kind: str = REPAIR_ACTION_KIND,
    predicate: str = REPAIR_PREDICATE,
    expected: Any = REPAIR_EXPECTED,
) -> Mapping[str, Any]:
    """Resolve the live S46 repair tool and persist its material requirement.

    The target is selected from the committed HistoricalWorld index by the
    world's existing ``world-resource:<location>:tool`` referent, never from a
    caller-supplied target literal. The expected serviceability is the
    sourcefree S46 repair rule for this fixture; a different admitted value
    must fail the adapter's exact-value check.
    """
    session = fanin.session
    world = session.world()
    location = world.positions.get("A")
    if not isinstance(location, str) or not location:
        raise ActivityRefusal("HISTORICAL_ACTIVITY_ACTOR_LOCATION_MISSING")
    referent = f"world-resource:{location}:tool"
    target = history.target_for_referent(referent, location=location)
    if target is None:
        raise ActivityRefusal(REQUIREMENT_TARGET_MISSING)
    surface = target.get("surface") or {}
    parent_ref = _exact_ref({
        "kind": "WORLD_EVENT",
        "object_id": surface.get("occurrence_id"),
        "content_hash": target.get("parent_hash"),
    })
    if parent_ref is None:
        raise ActivityRefusal(PARENT_MISSING)
    root, branch = _scope(session)
    requirement_id = "history-activity:" + _digest({
        "root": root, "branch": branch, "task_id": task_id,
        "action_kind": action_kind, "target_id": target["id"],
        "predicate": predicate,
        "expected": expected, "parent_event_ref": parent_ref,
        "required_at": session.clock(),
    })
    requirement = {
        "schema": "SOROK_HISTORY_ACTIVITY_REQUIREMENT@1",
        "id": requirement_id,
        "task_id": task_id,
        "action_kind": action_kind,
        "target_id": target["id"],
        "target_version": target.get("version"),
        "predicate": predicate,
        "expected": deepcopy(expected),
        "root": root,
        "branch": branch,
        "parent_event_ref": deepcopy(parent_ref),
        "job_id": target.get("job_id"),
        "world_readset": _digest(world.snapshot()),
        "required_at": session.clock(),
        "status": "HELD",
    }
    return history.hold_activity_requirement(requirement)


def _requirement_stale_receipt(
    fanin: Any,
    history: Any,
    requirement: Mapping[str, Any],
    reason: str,
) -> ActivityReceipt:
    session = fanin.session
    root, branch = _scope(session)
    target = history.target(requirement.get("target_id"))
    fact = (target or {}).get("physical_depth", {}).get(requirement.get("predicate"))
    job = history.job(requirement.get("job_id")) if requirement.get("job_id") else None
    return _receipt(
        status=HELD, target_id=str(requirement.get("target_id")),
        target=target, predicate=str(requirement.get("predicate")),
        expected=requirement.get("expected"), observed=None,
        fact=fact, job=job, root=root, branch=branch,
        clock_before=session.clock(), clock_after=session.clock(),
        material_before=_material(session), material_after=_material(session),
        interval=None, refusal_code=reason,
    )


def _recoverable_interval(session: Any, requirement: Mapping[str, Any]):
    required_at = requirement.get("required_at")
    requirement_id = requirement.get("id")
    if type(required_at) is not int or not isinstance(requirement_id, str):
        return None, RECOVERY_UNVERIFIED
    actor_id = session.world().actor_state.get("A", {}).get("actor_id")
    matches = []
    for row in session.read_interval_states():
        domain = row.get("domain") or {}
        if (domain.get("mode") != "ACTUAL"
                or domain.get("start") != required_at
                or domain.get("activity_requirement_ref") != requirement_id
                or row.get("root_hash") != requirement.get("root")
                or row.get("branch_id") != requirement.get("branch")
                or row.get("actor_id") != actor_id
                or row.get("status") not in {"PARTIAL", "REALIZED"}):
            continue
        matches.append(row)
    if not matches:
        return None, None
    if len(matches) != 1:
        return None, RECOVERY_AMBIGUOUS
    return matches[0], None


def _recovered_receipt(fanin: Any, history: Any, requirement: Mapping[str, Any],
                       interval: Mapping[str, Any]) -> ActivityReceipt | None:
    target, fact, refusal = _admitted_depth(
        history, requirement.get("target_id"), requirement.get("predicate")
    )
    if refusal is not None or fact is None or fact.get("value") != requirement.get("expected"):
        return None
    session = fanin.session
    job = history.job(fact.get("job_id"))
    material_before = None
    try:
        segments = interval.get("segments") or []
        material_before = int(
            segments[0]["world"]["state_before"]["material_remaining"]
        ) if segments else None
    except (KeyError, TypeError, ValueError, IndexError):
        pass
    root, branch = _scope(session)
    return _receipt(
        status=ADVANCED, target_id=str(requirement.get("target_id")),
        target=target, predicate=str(requirement.get("predicate")),
        expected=requirement.get("expected"),
        observed=fact.get("value"), fact=fact, job=job,
        root=root, branch=branch, clock_before=int(requirement["required_at"]),
        clock_after=session.clock(), material_before=material_before,
        material_after=_material(session), interval=interval,
    )


def dispatch_activity_requirement(
    fanin: Any,
    history: Any,
    requirement: Mapping[str, Any] | str,
    *,
    advance: Callable[[Any], Mapping[str, Any]] | None = None,
) -> ActivityDispatch:
    """Dispatch one durable requirement through the T4 adapter.

    The requirement must already be owner-persisted. A consumed requirement is
    never re-dispatched. A stale requirement (target version, job or parent
    event changed) is held before the adapter can authorize work.
    """
    requirement_id = (
        requirement if isinstance(requirement, str)
        else requirement.get("id") if isinstance(requirement, Mapping)
        else None
    )
    if not isinstance(requirement_id, str) or not requirement_id:
        raise ActivityRefusal(INVALID_REQUEST)
    stored = history.activity_requirement(requirement_id)
    if stored is None:
        raise ActivityRefusal("ACTIVITY_REQUIREMENT_NOT_RECORDED")
    if stored.get("status") == "CONSUMED":
        return ActivityDispatch(
            status=HELD, requirement=stored, activity=None,
            reason=REQUIREMENT_CONSUMED,
        )
    if stored.get("status") == DISPATCHING:
        interval, ambiguity = _recoverable_interval(fanin.session, stored)
        if ambiguity is not None:
            receipt = _requirement_stale_receipt(
                fanin, history, stored, ambiguity
            )
            saved = history.mark_activity_requirement(
                requirement_id, "HELD", receipt=receipt.as_dict()
            )
            return ActivityDispatch(HELD, saved, receipt, ambiguity)
        if interval is not None:
            receipt = _recovered_receipt(fanin, history, stored, interval)
            if receipt is None:
                held = _requirement_stale_receipt(
                    fanin, history, stored, RECOVERY_UNVERIFIED
                )
                saved = history.mark_activity_requirement(
                    requirement_id, "HELD", receipt=held.as_dict()
                )
                return ActivityDispatch(HELD, saved, held, RECOVERY_UNVERIFIED)
            saved = history.mark_activity_requirement(
                requirement_id, "CONSUMED", receipt=receipt.as_dict()
            )
            return ActivityDispatch(
                ADVANCED, saved, receipt, RECOVERED
            )
        stored = history.mark_activity_requirement(requirement_id, "HELD")
    target = history.target(stored.get("target_id"))
    session = fanin.session
    root, branch = _scope(session)
    parent = _exact_ref(stored.get("parent_event_ref"))
    if (target is None
            or (stored.get("root"), stored.get("branch")) != (root, branch)
            or target.get("parent_hash") != (parent or {}).get("content_hash")):
        receipt = _requirement_stale_receipt(fanin, history, stored, REQUIREMENT_STALE)
        history.mark_activity_requirement(
            requirement_id, "HELD", receipt=receipt.as_dict()
        )
        return ActivityDispatch(HELD, history.activity_requirement(requirement_id),
                                receipt, REQUIREMENT_STALE)
    history.mark_activity_requirement(
        requirement_id, DISPATCHING,
        receipt={"stage": "BEFORE_INTERVAL", "required_at": stored.get("required_at")},
    )
    receipt = advance_independent_activity(
        fanin, history,
        target_id=stored["target_id"], predicate=stored["predicate"],
        expected=stored["expected"], advance=advance,
        dispatch_ref=requirement_id,
    )
    status = "CONSUMED" if receipt.advanced else "HELD"
    saved = history.mark_activity_requirement(
        requirement_id, status, receipt=receipt.as_dict()
    )
    return ActivityDispatch(receipt.status, saved, receipt, receipt.refusal_code)


def resume_activity_requirements(
    fanin: Any,
    history: Any,
    *,
    advance: Callable[[Any], Mapping[str, Any]] | None = None,
) -> tuple[ActivityDispatch, ...]:
    """Resume every held dispatch requirement through the same normal adapter."""
    return tuple(
        dispatch_activity_requirement(fanin, history, requirement, advance=advance)
        for requirement in history.activity_requirements()
        if requirement.get("status") in {"HELD", DISPATCHING}
    )


consume_independent_activity = advance_independent_activity
run_independent_activity = advance_independent_activity


__all__ = [
    "ACTIVITY_GRADE",
    "ACTIVITY_SCHEMA",
    "ADVANCED",
    "ActivityDispatch",
    "ActivityReceipt",
    "ActivityRefusal",
    "CALL_SITE_INVALID",
    "CALL_SITE_UNAVAILABLE",
    "DEPTH_MISSING",
    "DISPATCHING",
    "EVENT_MISMATCH",
    "FACT_MISMATCH",
    "HELD",
    "INVALID_REQUEST",
    "JOB_MISSING",
    "JOB_NOT_ADMITTED",
    "PARENT_MISSING",
    "PLACE_MISMATCH",
    "PROPERTY_SOURCE",
    "REPAIR_ACTION_KIND",
    "REPAIR_EXPECTED",
    "REPAIR_PREDICATE",
    "REPAIR_TASK_ID",
    "REQUIREMENT_CONSUMED",
    "REQUIREMENT_STALE",
    "RECOVERED",
    "RECOVERY_AMBIGUOUS",
    "RECOVERY_UNVERIFIED",
    "REQUIREMENT_TARGET_MISSING",
    "SCOPE_MISMATCH",
    "TARGET_MISMATCH",
    "TARGET_UNKNOWN",
    "VALUE_MISMATCH",
    "WORLD_MISMATCH",
    "advance_independent_activity",
    "consume_independent_activity",
    "dispatch_activity_requirement",
    "produce_activity_requirement",
    "resume_activity_requirements",
    "run_independent_activity",
]
