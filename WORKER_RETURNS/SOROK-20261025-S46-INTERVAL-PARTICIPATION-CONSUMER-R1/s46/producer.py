"""Produce actual period-grain workshop participation in the S45 C12 person."""
from __future__ import annotations

from copy import deepcopy
from typing import Any

from .bootstrap import install

install()

from candidate import digest, seal  # noqa: E402
from s41.event import world_prerequisites  # noqa: E402

from .errors import S46Refusal  # noqa: E402
from .model import (
    ACTOR_OWNER,
    ACTOR_OWNER_VERSION,
    MODEL_HASH,
    OWNER_REGISTRY_HASH,
    POLICY_ID,
    POLICY_VERSION,
    SOURCE_RULE_REF,
    WORLD_OWNER,
    WORLD_OWNER_VERSION,
    validate_domain,
)

STATE_SCHEMA = "S46_INTERVAL_PARTICIPATION_STATE@1"
STATE_KIND = "S46_INTERVAL_STATE"
STATE_GRADE = "TEST_ONLY_S46_ACTUAL_INTERVAL_PARTICIPATION_NOT_NATIVE"
STATE_STATUSES = frozenset({
    "REALIZED", "PARTIAL", "NOT_PERFORMED", "UNKNOWN", "REFUSED",
})


def _seal(body: dict) -> dict:
    value = dict(body)
    value["receipt_hash"] = digest(body)
    return value


def _attempt_receipt(domain: dict, segment: tuple[int, int],
                     before: dict, predecessor: str = "") -> dict:
    mode = domain["mode"]
    if mode == "SCHEDULED_ONLY":
        kind = "NOT_ATTEMPTED"
        reason = "SCHEDULE_ONLY_NOT_PARTICIPATION_EVIDENCE"
    elif mode == "DECLINED":
        kind = "DECLINED"
        reason = "ACTOR_ATTEMPT_POLICY_DECLINED"
    elif mode == "CONSTRAINED":
        kind = "CONSTRAINED_ATTEMPT"
        reason = "MATERIALLY_CONSTRAINED_ATTEMPT_NO_CONSENT_CLAIM"
    elif mode == "UNKNOWN":
        kind = "UNKNOWN"
        reason = "SOURCE_OR_OWNER_UNKNOWN_NOT_A_NEGATIVE"
    else:
        kind = "ATTEMPT"
        reason = "RESOURCE_CONSTRAINED_ATTEMPT"
    return _seal({
        "schema": "S46_ACTOR_ATTEMPT_RECEIPT@1",
        "grade": STATE_GRADE,
        "native": False,
        "psychology_claim": False,
        "actor_id": domain["actor_id"],
        "branch_id": domain["branch_id"],
        "scope_id": domain["scope_id"],
        "start": segment[0],
        "end": segment[1],
        "attempt": kind,
        "reason": reason,
        "policy_id": POLICY_ID,
        "policy_version": POLICY_VERSION,
        "model_hash": MODEL_HASH,
        "owner_registry_hash": OWNER_REGISTRY_HASH,
        "source_owner": ACTOR_OWNER,
        "source_owner_version": ACTOR_OWNER_VERSION,
        "source_rule_ref": SOURCE_RULE_REF,
        "inputs": {
            "tool_available": bool(before.get("tool_available")),
            "material_available": bool(before.get("material_available")),
            "free_hours": bool(before.get("free_hours")),
            "actor_present": bool(before.get("actor_present")),
        },
        "predecessor_world_receipt_hash": predecessor,
        "actual_result_claimed": False,
        "consent_or_willingness_claimed": False,
    })


def _world_receipt(domain: dict, segment: tuple[int, int], attempt: dict,
                   before: dict, after: dict, result: dict | None) -> dict:
    actual = result or {}
    confirmed = actual.get("status") == "OK" and bool(actual.get("event_id"))
    status = "CONFIRMED" if confirmed else (
        "NOT_PERFORMED" if attempt["attempt"] in {
            "ATTEMPT", "CONSTRAINED_ATTEMPT",
        } else "UNKNOWN"
    )
    if attempt["attempt"] in {"NOT_ATTEMPTED", "DECLINED"}:
        status = "NOT_PERFORMED"
    body = {
        "schema": "S46_WORLD_PERIOD_RECEIPT@1",
        "grade": STATE_GRADE,
        "native": False,
        "psychology_claim": False,
        "actor_id": domain["actor_id"],
        "branch_id": domain["branch_id"],
        "scope_id": domain["scope_id"],
        "start": segment[0],
        "end": segment[1],
        "status": status,
        "reason": actual.get("code", ""),
        "source_owner": WORLD_OWNER,
        "source_owner_version": WORLD_OWNER_VERSION,
        "source_rule_ref": SOURCE_RULE_REF,
        "model_hash": MODEL_HASH,
        "owner_registry_hash": OWNER_REGISTRY_HASH,
        "actor_attempt_receipt_hash": attempt["receipt_hash"],
        "actual_action_event_id": actual.get("event_id", ""),
        "actual_action_event_hash": (
            actual.get("event_hash", "") or ""
        ),
        "state_before": before,
        "state_after": after,
        "actual_daily_events_invented": 0,
        "welfare_or_consent_inferred": False,
    }
    return _seal(body)


def produce_interval(session, domain: dict) -> dict:
    domain = validate_domain(domain)
    root = session.read_root()
    if domain["branch_id"] != session.branch_id:
        raise S46Refusal("S46_DOMAIN_BRANCH_MISMATCH")
    if domain["actor_id"] != session.world().actor_state.get("A", {}).get("actor_id"):
        raise S46Refusal("S46_DOMAIN_ACTOR_MISMATCH")
    if session.clock() > domain["start"]:
        raise S46Refusal("S46_INTERVAL_STARTS_IN_PAST")
    segments = []
    for segment in domain["segments"]:
        start, end = int(segment[0]), int(segment[1])
        if session.clock() < start:
            world = session.world()
            world.advance(start)
            session.product._checkpoint(session.branch_id, start, world)
        before = world_prerequisites(session)
        before_state = dict(session.world().actor_state.get("A", {}))
        predecessor = segments[-1]["world"]["receipt_hash"] if segments else ""
        attempt = _attempt_receipt(domain, (start, end), before, predecessor)
        actual = None
        if attempt["attempt"] in {"ATTEMPT", "CONSTRAINED_ATTEMPT"}:
            actual = session.product.repair(actor="A")
            if actual and actual.get("status") == "OK" and actual.get("event_id"):
                action = session.event(actual["event_id"])
                if action:
                    actual["event_hash"] = action.get("hash", "")
        after_state = dict(session.world().actor_state.get("A", {}))
        world = _world_receipt(
            domain, (start, end), attempt, before_state, after_state, actual,
        )
        segments.append({
            "start": start,
            "end": end,
            "attempt": attempt,
            "world": world,
            "status": (
                "REALIZED" if world["status"] == "CONFIRMED"
                else "NOT_PERFORMED" if world["status"] == "NOT_PERFORMED"
                else "UNKNOWN"
            ),
        })
        if session.clock() < end:
            world = session.world()
            world.advance(end)
            session.product._checkpoint(session.branch_id, end, world)
    coverage = [[row["start"], row["end"]] for row in segments
                if row["status"] == "REALIZED"]
    if any(row["status"] == "UNKNOWN" for row in segments):
        status = "UNKNOWN"
    elif len(coverage) == len(segments):
        status = "REALIZED"
    elif coverage:
        status = "PARTIAL"
    else:
        status = "NOT_PERFORMED"
    body = {
        "schema": STATE_SCHEMA,
        "grade": STATE_GRADE,
        "native": False,
        "psychology_claim": False,
        "state_id": "S46_STATE_" + digest({
            "domain": domain["domain_hash"],
            "segments": segments,
            "root": root["root_hash"],
        })[:24].upper(),
        "actor_id": domain["actor_id"],
        "branch_id": domain["branch_id"],
        "scope_id": domain["scope_id"],
        "activity_id": domain["activity_id"],
        "domain_id": domain["domain_id"],
        "domain_hash": domain["domain_hash"],
        "model_hash": MODEL_HASH,
        "owner_registry_hash": OWNER_REGISTRY_HASH,
        "actor_owner": ACTOR_OWNER,
        "actor_owner_version": ACTOR_OWNER_VERSION,
        "world_owner": WORLD_OWNER,
        "world_owner_version": WORLD_OWNER_VERSION,
        "source_rule_ref": SOURCE_RULE_REF,
        "root_hash": root["root_hash"],
        "root_id": root["root_id"],
        "start": domain["start"],
        "end": domain["end"],
        "segments": segments,
        "coverage": coverage,
        "status": status,
        "currentness": "CURRENT",
        "superseded_by": "",
        "resolution": "BOUNDED_PERIOD_STATE_NO_DAILY_EVENTS",
        "actual_daily_events_invented": 0,
        "actor_knowledge_inferred": False,
        "psychology_state_written": False,
        "target_proposals": [],
    }
    state = _seal(body)
    episode = session.product._append_episode(
        session.branch_id, "A", STATE_KIND, session.clock(), state,
    )
    session.product._checkpoint(session.branch_id, session.clock(), session.world())
    return {**state, "episode_id": episode["episode_id"]}


def _validate_segment(session, state: dict, segment: dict) -> None:
    if segment.get("status") not in {"REALIZED", "NOT_PERFORMED", "UNKNOWN"}:
        raise S46Refusal("S46_SEGMENT_STATUS_INVALID")
    attempt = segment.get("attempt") or {}
    world = segment.get("world") or {}
    if attempt.get("source_owner") != ACTOR_OWNER:
        raise S46Refusal("S46_ATTEMPT_OWNER_MISMATCH")
    if world.get("source_owner") != WORLD_OWNER:
        raise S46Refusal("S46_WORLD_OWNER_MISMATCH")
    if attempt.get("source_owner_version") != ACTOR_OWNER_VERSION:
        raise S46Refusal("S46_ATTEMPT_OWNER_VERSION_MISMATCH")
    if world.get("source_owner_version") != WORLD_OWNER_VERSION:
        raise S46Refusal("S46_WORLD_OWNER_VERSION_MISMATCH")
    for row in (attempt, world):
        if row.get("model_hash") != MODEL_HASH:
            raise S46Refusal("S46_SEGMENT_MODEL_MISMATCH")
        if row.get("owner_registry_hash") != OWNER_REGISTRY_HASH:
            raise S46Refusal("S46_SEGMENT_OWNER_REGISTRY_MISMATCH")
        if row.get("source_rule_ref") != SOURCE_RULE_REF:
            raise S46Refusal("S46_SEGMENT_SOURCE_RULE_MISMATCH")
    if attempt.get("actor_id") != state["actor_id"] or world.get("actor_id") != state["actor_id"]:
        raise S46Refusal("S46_SEGMENT_ACTOR_MISMATCH")
    if world.get("actor_attempt_receipt_hash") != attempt.get("receipt_hash"):
        raise S46Refusal("S46_ATTEMPT_WORLD_BINDING_MISMATCH")
    if (segment.get("start"), segment.get("end")) != (
        world.get("start"), world.get("end")
    ):
        raise S46Refusal("S46_SEGMENT_TIME_MISMATCH")
    action_id = world.get("actual_action_event_id", "")
    if segment["status"] == "REALIZED":
        if world.get("status") != "CONFIRMED" or not action_id:
            raise S46Refusal("S46_REALIZED_WITHOUT_ACTION")
        action = session.event(action_id)
        if (
            not action
            or action.get("hash") != world.get("actual_action_event_hash")
        ):
            raise S46Refusal("S46_ACTION_EVENT_MISMATCH")
        if action.get("actor_id") != "A" or action.get("kind") not in {
            "INSPECT", "REPAIR",
        }:
            raise S46Refusal("S46_ACTION_EVENT_INVALID")
    elif action_id:
        raise S46Refusal("S46_NONREALIZED_HAS_ACTION")
    if not attempt.get("receipt_hash") or not world.get("receipt_hash"):
        raise S46Refusal("S46_SEGMENT_RECEIPT_MISSING")
    attempt_body = {k: v for k, v in attempt.items() if k != "receipt_hash"}
    world_body = {k: v for k, v in world.items() if k != "receipt_hash"}
    if attempt.get("receipt_hash") != digest(attempt_body):
        raise S46Refusal("S46_ATTEMPT_RECEIPT_HASH_MISMATCH")
    if world.get("receipt_hash") != digest(world_body):
        raise S46Refusal("S46_WORLD_RECEIPT_HASH_MISMATCH")


def validate_interval_state(session, state: dict) -> dict:
    """Validate a supplied state against the actual C12 person/event records."""
    if not isinstance(state, dict) or state.get("schema") != STATE_SCHEMA:
        raise S46Refusal("S46_STATE_SCHEMA_MISMATCH")
    if state.get("root_hash") != session.read_root()["root_hash"]:
        raise S46Refusal("S46_STATE_ROOT_MISMATCH")
    if state.get("branch_id") != session.branch_id:
        raise S46Refusal("S46_STATE_BRANCH_MISMATCH")
    if state.get("model_hash") != MODEL_HASH:
        raise S46Refusal("S46_STATE_MODEL_MISMATCH")
    if state.get("owner_registry_hash") != OWNER_REGISTRY_HASH:
        raise S46Refusal("S46_STATE_OWNER_REGISTRY_MISMATCH")
    if state.get("actor_owner") != ACTOR_OWNER or state.get("world_owner") != WORLD_OWNER:
        raise S46Refusal("S46_STATE_OWNER_MISMATCH")
    if state.get("actor_owner_version") != ACTOR_OWNER_VERSION:
        raise S46Refusal("S46_STATE_ACTOR_VERSION_MISMATCH")
    if state.get("world_owner_version") != WORLD_OWNER_VERSION:
        raise S46Refusal("S46_STATE_WORLD_VERSION_MISMATCH")
    if state.get("source_rule_ref") != SOURCE_RULE_REF:
        raise S46Refusal("S46_STATE_SOURCE_RULE_MISMATCH")
    body = {k: v for k, v in state.items()
            if k not in {"receipt_hash", "episode_id", "clock"}}
    if state.get("receipt_hash") != digest(body):
        raise S46Refusal("S46_STATE_HASH_MISMATCH")
    segments = state.get("segments") or []
    expected_state_id = "S46_STATE_" + digest({
        "domain": state.get("domain_hash", ""),
        "segments": segments,
        "root": state.get("root_hash", ""),
    })[:24].upper()
    if state.get("state_id") != expected_state_id:
        raise S46Refusal("S46_STATE_ID_MISMATCH")
    if not segments:
        raise S46Refusal("S46_SEGMENTS_MISSING")
    for segment in segments:
        _validate_segment(session, state, segment)
    coverage = [[row["start"], row["end"]] for row in segments
                if row.get("status") == "REALIZED"]
    if state.get("coverage") != coverage:
        raise S46Refusal("S46_COVERAGE_MISMATCH")
    if any(row.get("status") == "UNKNOWN" for row in segments):
        expected = "UNKNOWN"
    else:
        expected = (
            "REALIZED" if coverage and len(coverage) == len(segments)
            else "PARTIAL" if coverage
            else "NOT_PERFORMED"
        )
    if state.get("status") != expected:
        raise S46Refusal("S46_STATE_STATUS_MISMATCH")
    return dict(state)


def read_interval_states(session) -> list[dict]:
    rows = []
    for row in session.product.store.episodes(session.branch_id):
        if row.get("kind") != STATE_KIND:
            continue
        state = dict(row.get("body") or {})
        state = validate_interval_state(session, state)
        if state.get("actor_id") != session.world().actor_state.get("A", {}).get("actor_id"):
            raise S46Refusal("S46_STATE_ACTOR_MISMATCH")
        state["episode_id"] = row.get("episode_id", "")
        state["clock"] = row.get("clock", 0)
        rows.append(state)
    if rows:
        latest_scope = rows[-1].get("scope_id")
        for index, row in enumerate(rows):
            later = [
                other for other in rows[index + 1:]
                if other.get("scope_id") == latest_scope
            ]
            if later and row.get("scope_id") == latest_scope:
                row["currentness"] = "SUPERSEDED"
                row["superseded_by"] = later[-1].get("state_id", "")
            else:
                row["currentness"] = "CURRENT"
                row["superseded_by"] = ""
    return rows


__all__ = [
    "STATE_SCHEMA", "STATE_KIND", "STATE_GRADE", "STATE_STATUSES",
    "produce_interval", "read_interval_states", "validate_interval_state",
]
