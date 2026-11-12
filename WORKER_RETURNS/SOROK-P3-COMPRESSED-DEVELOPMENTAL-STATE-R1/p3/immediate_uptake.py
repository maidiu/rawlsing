"""D03 sourcefree immediate speech uptake over actual C04 child receipts.

This module is a read-only adapter. It consumes the actual public child uptake
from ``parent_speech.read_child_uptake`` plus the actual parent utterance
receipt, activates the existing sourcefree P3 mediator records with the existing
``projections.activate`` machinery, and returns allowed immediate response
candidates under the existing P3 response rule descriptor.

It does not write a record, target, memory, world or psyche state. Durable
formation remains MISSING_RULE. The parent's hidden reason, decision internals,
cash/period material and portal/user view are never read into the child
readset. The sourcefree vertical project/counterpart is a P3 organization scope,
not the registered parent identity; the actual parent speaker is a separate
speech scope.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RecursionRefusal,
    detached,
    digest,
)
from developmental_recursion.parent_speech import read_child_uptake
from developmental_recursion.supporting_actor import read_supporting_actor

from . import p3_owner, projections, test_rules

GRADE = "SOURCEFREE_S2_ONLY"
P3_GRADE = test_rules.GRADE
UTTERANCE_GRADE = "SOURCEFREE_S2_ONLY"
SCHEMA = "SOROK_D03_IMMEDIATE_UPTAKE@1"
SOURCE_SCHEMA = "SOROK_D03_SOURCE_CLOSURE@1"
UTTERANCE_RECEIPT_SCHEMA = "SOROK_PARENT_UTTERANCE_RECEIPT@1"
CHILD_UPTAKE_SCHEMA = "SOROK_CHILD_SPEECH_UPTAKE@1"
IMMEDIATE_RULE = test_rules.rule_descriptors()[1]
_WORKER_RETURNS = Path(__file__).resolve().parents[2]


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code)
    return detached(value)


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    return value


def _hash(value: Any, code: str) -> str:
    if not isinstance(value, str) or len(value) != 64:
        _refuse(code)
    try:
        int(value, 16)
    except ValueError:
        _refuse(code)
    return value.lower()


def _source_label(path: Path) -> str:
    path = Path(path).resolve()
    try:
        return str(path.relative_to(_WORKER_RETURNS))
    except ValueError:
        return str(path)


def _identity(value: Any) -> dict:
    document = value.document() if hasattr(value, "document") else value
    document = _mapping(document, "D03_IDENTITY_SCHEMA")
    for key in ("root", "actor", "branch"):
        _text(document.get(key), "D03_IDENTITY_" + key.upper())
    clock = document.get("clock")
    if isinstance(clock, bool) or not isinstance(clock, int):
        _refuse("D03_IDENTITY_CLOCK")
    _hash(document.get("state_hash"), "D03_IDENTITY_STATE_HASH")
    return document


def _check_expected(snapshot: Mapping[str, Any], expected: Any) -> None:
    if expected is None:
        return
    document = _identity(expected)
    for key in ("root", "actor", "branch"):
        if document.get(key) != snapshot.get(key):
            _refuse("D03_FOREIGN_STATE:" + key)
    if document.get("clock") != snapshot.get("clock"):
        _refuse("D03_STALE_CLOCK")
    if document.get("state_hash") != snapshot.get("state_hash"):
        _refuse("D03_STALE_STATE")


def _check_session_alignment(base_owner: Any, session: Any,
                             snapshot: Mapping[str, Any]) -> None:
    current = base_owner.snapshot()
    for key in ("root", "actor", "branch", "clock"):
        if getattr(current, key) != snapshot.get(key):
            _refuse("D03_STALE_BASE_SESSION:" + key)
    root = session.read_root()
    if root.get("root_hash") != snapshot["root"]:
        _refuse("D03_STALE_SESSION_ROOT")
    if session.branch_id != snapshot["branch"]:
        _refuse("D03_STALE_SESSION_BRANCH")
    if session.clock() != snapshot["clock"]:
        _refuse("D03_STALE_SESSION_CLOCK")


def _plan_scope(plan: Any, owner: Any, snapshot: Mapping[str, Any]) -> dict:
    value = _mapping(plan, "D03_ACQUIRED_PLAN")
    for key in ("actor_observed", "material_eligible", "eligible",
                "eligible_modes", "record_hashes"):
        if key in value:
            _refuse("D03_PLAN_OVERRIDE_FORBIDDEN:" + key)
    for key in ("root", "actor", "branch"):
        if value.get(key) != snapshot.get(key):
            _refuse("D03_ACQUIRED_PLAN_IDENTITY:" + key)
    for key in ("source_hash", "registry_hash", "grade", "project",
                "counterpart", "event_id"):
        _text(value.get(key), "D03_ACQUIRED_PLAN_" + key.upper())
    if value.get("source_hash") != owner.source_hash:
        _refuse("D03_ACQUIRED_PLAN_SOURCE")
    if value.get("registry_hash") != owner.registry.get("hash"):
        _refuse("D03_ACQUIRED_PLAN_REGISTRY")
    if value.get("grade") != P3_GRADE:
        _refuse("D03_ACQUIRED_PLAN_GRADE")
    if not value.get("hash"):
        _refuse("D03_ACQUIRED_PLAN_HASH_MISSING")
    _hash(value.get("hash"), "D03_ACQUIRED_PLAN_HASH")
    if digest({key: item for key, item in value.items()
               if key != "hash"}) != value["hash"]:
        _refuse("D03_ACQUIRED_PLAN_HASH_MISMATCH")
    if value.get("permitted_rules") != test_rules.rule_descriptors():
        _refuse("D03_ACQUIRED_PLAN_RULES")
    selectors = {}
    for key in ("activation_roles", "relation_refs", "obligation_refs"):
        items = value.get(key, [])
        if not isinstance(items, list) or any(
                not isinstance(item, str) or not item for item in items):
            _refuse("D03_ACQUIRED_PLAN_SELECTORS:" + key)
        selectors[key] = list(items)
    role = value.get("interlocutor_role")
    if role is not None:
        _text(role, "D03_ACQUIRED_PLAN_ROLE")
    relation = value.get("relation_ref")
    if relation is not None:
        _text(relation, "D03_ACQUIRED_PLAN_RELATION")
    elif len(selectors["relation_refs"]) == 1:
        relation = selectors["relation_refs"][0]
    return {
        "project": value["project"],
        "counterpart": value["counterpart"],
        "interlocutor_role": role,
        "relation_ref": relation,
        "obligation_refs": selectors["obligation_refs"],
        "activation_roles": selectors["activation_roles"],
        "relation_refs": selectors["relation_refs"],
        "plan_hash": value.get("hash"),
    }


def _module_source(module: Any, expected: Path, code: str) -> Path:
    value = getattr(module, "__file__", None)
    if not isinstance(value, str) or not value.strip():
        _refuse(code)
    path = Path(value).resolve()
    if path != expected.resolve():
        _refuse(code)
    return path


def _selected_source_files() -> list[tuple[str, Path]]:
    """D03 reader closure: P3 owner pins + the actual speech/projection readers.

    The C04 writer's decision/activity modules are not read by this adapter;
    only the child uptake/public receipt, the C01 speaker registration, the S45
    event projection and the P3 activation/rule/plan-scope code are selected.
    """
    rows: list[tuple[str, Path]] = []
    for row in p3_owner._code_pins().get("files", []):
        path = Path(row["path"]).resolve()
        rows.append((_source_label(path), path))
    from developmental_recursion import parent_speech
    from s45_projection import projection
    expected_parent = (
        _WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
        / "developmental_recursion" / "parent_speech.py")
    expected_supporting = (
        _WORKER_RETURNS / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
        / "developmental_recursion" / "supporting_actor.py")
    expected_projection = (
        _WORKER_RETURNS / "SOROK-S45-S47-PROJECTION-20261105-R1"
        / "s45_projection" / "projection.py")
    parent_path = _module_source(
        parent_speech, expected_parent, "D03_PARENT_SPEECH_SOURCE_IDENTITY")
    from developmental_recursion import supporting_actor
    supporting_path = _module_source(
        supporting_actor, expected_supporting,
        "D03_SUPPORTING_SOURCE_IDENTITY")
    projection_path = _module_source(
        projection, expected_projection, "D03_PROJECTION_SOURCE_IDENTITY")
    own_path = Path(__file__).resolve()
    p3_init = Path(__file__).with_name("__init__.py").resolve()
    rows.extend([
        (_source_label(own_path), own_path),
        (_source_label(p3_init), p3_init),
        (_source_label(parent_path), parent_path),
        (_source_label(supporting_path), supporting_path),
        (_source_label(projection_path), projection_path),
    ])
    unique: dict[str, Path] = {}
    for label, path in rows:
        unique[label] = path
    return sorted(unique.items(), key=lambda row: row[0])


def _source_closure(files: Any = None) -> dict:
    rows = _selected_source_files() if files is None else list(files)
    result = []
    for label, path in rows:
        label = _text(str(label), "D03_SOURCE_LABEL")
        path = Path(path).expanduser().resolve()
        if not path.is_file():
            _refuse("D03_SOURCE_MISSING:" + label)
        result.append({
            "path": label,
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        })
    result.sort(key=lambda row: row["path"])
    if len({row["path"] for row in result}) != len(result):
        _refuse("D03_SOURCE_DUPLICATE")
    return {"schema": SOURCE_SCHEMA, "files": result,
            "hash": digest(result)}


def source_closure() -> dict:
    """Return the exact selected D03 reader closure; no authority."""
    return _source_closure()


def _expected_closure_hash(value: Any) -> str:
    if isinstance(value, str):
        return _hash(value, "D03_EXPECTED_SOURCE_CLOSURE")
    document = _mapping(value, "D03_EXPECTED_SOURCE_CLOSURE")
    return _hash(document.get("hash"), "D03_EXPECTED_SOURCE_CLOSURE:HASH")


def _speaker_scope(session: Any, snapshot: Mapping[str, Any],
                   child_id: str, event_id: str, receipt: Mapping[str, Any],
                   uptake: Mapping[str, Any],
                   expected_speaker_actor_id: str | None = None) -> dict:
    body = _mapping(receipt, "D03_UTTERANCE_RECEIPT")
    if body.get("schema") != UTTERANCE_RECEIPT_SCHEMA:
        _refuse("D03_UTTERANCE_RECEIPT_SCHEMA")
    if body.get("grade") != UTTERANCE_GRADE:
        _refuse("D03_UTTERANCE_RECEIPT_GRADE")
    if body.get("hidden_reason") not in (None, "NOT_READ"):
        _refuse("D03_PRIVATE_INPUT")
    if body.get("status") not in ("ADMITTED", "REPLAY"):
        _refuse("D03_UTTERANCE_RECEIPT_STATUS")
    if body.get("event_id") != event_id:
        _refuse("D03_UTTERANCE_EVENT_MISMATCH")
    if body.get("child_actor_id") != child_id:
        _refuse("D03_UTTERANCE_CHILD_MISMATCH")
    if body.get("child_perception_channel") != "speech":
        _refuse("D03_UTTERANCE_NOT_CHILD_SPEECH")
    if body.get("hidden_reason") not in (None, "NOT_READ"):
        _refuse("D03_PRIVATE_INPUT")
    if body.get("private_state") not in (None, "SELF_ONLY_HIDDEN_REASON"):
        _refuse("D03_PRIVATE_INPUT")
    event_hash = _hash(body.get("event_hash"), "D03_UTTERANCE_EVENT_HASH")
    raw = session.event(event_id)
    if not isinstance(raw, Mapping):
        _refuse("D03_UTTERANCE_EVENT_SEVERED")
    if raw.get("hash") != event_hash:
        _refuse("D03_UTTERANCE_EVENT_SEVERED")
    if raw.get("kind") != "SPEECH":
        _refuse("D03_UTTERANCE_NOT_SPEECH")
    speaker_id = _text(body.get("actor_id"), "D03_SPEAKER_ID")
    alias = _text(body.get("alias"), "D03_SPEAKER_ALIAS")
    if (expected_speaker_actor_id is not None
            and speaker_id != expected_speaker_actor_id):
        _refuse("D03_SPEAKER_EXPECTED_MISMATCH")
    if body.get("event_authored_by") != alias:
        _refuse("D03_SPEAKER_EVENT_MISMATCH")
    if alias == snapshot.get("actor"):
        _refuse("D03_SPEAKER_IS_FOCAL")
    registration = read_supporting_actor(session, speaker_id)
    if registration.get("alias") != alias:
        _refuse("D03_SPEAKER_REGISTRATION_MISMATCH")
    if registration.get("role") != "parent":
        _refuse("D03_SPEAKER_ROLE")
    if raw.get("actor_id") != alias:
        _refuse("D03_SPEAKER_EVENT_MISMATCH")
    event = uptake.get("event")
    if not isinstance(event, Mapping):
        _refuse("D03_CHILD_UPTAKE_EVENT")
    if event.get("actor_visible_id") != alias:
        _refuse("D03_SPEAKER_UPTAKE_MISMATCH")
    public = event.get("body_public")
    if not isinstance(public, Mapping):
        _refuse("D03_CHILD_UPTAKE_PUBLIC_BODY")
    text = _text(public.get("text"), "D03_CHILD_UPTAKE_TEXT")
    if text != body.get("text"):
        _refuse("D03_UTTERANCE_TEXT_MISMATCH")
    return {
        "schema": "SOROK_D03_SPEECH_SCOPE@1",
        "status": "PERCEIVED",
        "source": "C04_ACTUAL_CHILD_SPEECH_UPTAKE",
        "speaker_actor_id": speaker_id,
        "alias": alias,
        "role": registration.get("role"),
        "event_id": event_id,
        "event_hash": event_hash,
        "text": text,
        "child_actor_id": child_id,
        "child_alias": uptake.get("child_alias"),
        "receipt": detached(uptake.get("receipt")),
        "expected_speaker_actor_id": expected_speaker_actor_id,
        "expected_speaker_bound": expected_speaker_actor_id is not None,
        "hidden_reason": "NOT_READ",
        "parent_decision": "NOT_READ",
        "period_context": "NOT_READ",
        "cash": "NOT_READ",
        "portal_user_view": "NOT_READ",
    }


def _held_output(snapshot: Mapping[str, Any], closure: Mapping[str, Any],
                 event_id: str, uptake: Mapping[str, Any],
                 head_before: Mapping[str, Any]) -> dict:
    response = {
        "status": "HELD_NOT_PERCEIVED",
        "rule": dict(IMMEDIATE_RULE),
        "streams": [],
        "contradictions": [],
        "eligible_modes": [],
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "memory_formation": "MISSING_RULE",
        "first_person_claims": [],
    }
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "status": "HELD_NOT_PERCEIVED",
        "identity": detached(snapshot),
        "speech_scope": {
            "schema": "SOROK_D03_SPEECH_SCOPE@1",
            "status": uptake.get("status"),
            "event_id": "NOT_READ",
            "text": "NOT_READ",
            "hidden_reason": "NOT_READ",
            "parent_decision": "NOT_READ",
            "period_context": "NOT_READ",
            "cash": "NOT_READ",
            "portal_user_view": "NOT_READ",
            "source": "C04_ACTUAL_CHILD_UPTAKE",
        },
        "prior_organization_scope": None,
        "activation_context": None,
        "immediate_response": response,
        "durable_formation": {
            "status": "MISSING_RULE",
            "written": False,
            "records": [],
            "target_candidate": None,
            "reason": "NO_D03_DURABLE_OWNER",
            "native_rule": "MISSING_RULE",
            "memory_formation": "MISSING_RULE",
        },
        "source_closure": detached(closure),
        "read_boundary": {
            "speech": "C04_ACTUAL_CHILD_UPTAKE_NOT_TEXT_WHEN_UNPERCEIVED",
            "parent_private_state": "NOT_READ",
            "parent_decision": "NOT_READ",
            "period_context": "NOT_READ",
            "cash": "NOT_READ",
            "portal_user_view": "NOT_READ",
            "psyche_store": "NOT_READ",
            "store_write": "NOT_WRITTEN",
        },
        "store_head": {
            "before": detached(head_before), "after": detached(head_before)},
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "memory_formation": "MISSING_RULE",
    }
    body["readset"] = {
        "identity": {
            "root": snapshot["root"], "actor": snapshot["actor"],
            "branch": snapshot["branch"], "clock": snapshot["clock"],
            "state_hash": snapshot["state_hash"],
        },
        "status": "HELD_NOT_PERCEIVED",
        "speech_event_id": "NOT_READ",
        "source_closure": {"hash": closure["hash"]},
        "store_head": detached(head_before),
    }
    body["hash"] = digest(body)
    return detached(body)


def build_immediate_uptake(
    owner: Any, *, speech_event_id: str, child_id: str,
    utterance_receipt: Any, plan: Any, expected: Any = None,
    expected_source_closure: Any = None,
    expected_speaker_actor_id: str | None = None,
) -> dict:
    """Consume actual C04 speech uptake and existing P3 prior organization."""
    if not hasattr(owner, "snapshot") or not hasattr(owner, "base_owner"):
        _refuse("D03_P3_OWNER_UNAVAILABLE")
    snapshot = _identity(owner.snapshot())
    if child_id != snapshot["actor"]:
        _refuse("D03_CHILD_NOT_FOCAL")
    _check_expected(snapshot, expected)
    store = getattr(owner, "store", None)
    if store is not None and hasattr(store, "pending") and store.pending():
        _refuse("D03_PENDING_OPERATION")
    base = owner.base_owner
    session = getattr(getattr(base, "fanin", None), "session", None)
    if session is None:
        _refuse("D03_ACTUAL_SESSION_UNAVAILABLE")
    _check_session_alignment(base, session, snapshot)
    closure = source_closure()
    if expected_source_closure is not None:
        if _expected_closure_hash(expected_source_closure) != closure["hash"]:
            _refuse("D03_SOURCE_CLOSURE_CHANGED")
    head_before = store.head() if store is not None else None
    uptake = read_child_uptake(session, child_id, speech_event_id)
    if uptake.get("schema") != CHILD_UPTAKE_SCHEMA:
        _refuse("D03_CHILD_UPTAKE_SCHEMA")
    if uptake.get("status") != "PERCEIVED":
        return _held_output(
            snapshot, closure, speech_event_id, uptake, head_before or {})

    speech = _speaker_scope(
        session, snapshot, child_id, speech_event_id, utterance_receipt, uptake,
        expected_speaker_actor_id)
    scope = _plan_scope(plan, owner, snapshot)
    records = store.query(
        project=scope["project"], counterpart=scope["counterpart"],
        as_of=snapshot["clock"],
    )
    context = {
        "root": snapshot["root"], "actor": snapshot["actor"],
        "branch": snapshot["branch"], "clock": snapshot["clock"],
        "project": scope["project"], "counterpart": scope["counterpart"],
        "interlocutor_role": scope.get("interlocutor_role"),
        "relation_ref": scope.get("relation_ref"),
        "obligation_refs": list(scope.get("obligation_refs") or []),
        "actor_observed": True,
        "material_eligible": None,
        "source_refs": [owner.source_hash],
        "grade": P3_GRADE,
    }
    context["hash"] = digest(context)
    activation = projections.activate(
        records, identity=snapshot, context=context, registry=owner.registry)
    head_after = store.head()
    if head_before != head_after:
        _refuse("D03_STORE_MUTATED")
    entries = activation.get("entries") if isinstance(
        activation.get("entries"), list) else []
    eligible = [row for row in entries
                if row.get("activation") == "ELIGIBLE"]
    withheld = [row for row in entries
                if row.get("activation") != "ELIGIBLE"]
    contradictions = detached(activation.get("contradictions") or [])
    eligible_ids = {row.get("record_id") for row in eligible}
    active = [
        pair for pair in contradictions
        if isinstance(pair, (list, tuple)) and len(pair) == 2
        and set(pair) <= eligible_ids
    ]
    streams = []
    for row in eligible:
        mode = row.get("mode")
        streams.append({
            "mode": mode,
            "record_id": row.get("record_id"),
            "record_hash": row.get("record_hash"),
            "candidate_activity": str(mode) + ":" + scope["counterpart"],
            "material_eligible": None,
            "native_action_performed": False,
        })
    if not records:
        status = "NO_PRIOR_ORGANIZATION"
        streams = [{
            "mode": "inspect_alone",
            "candidate_activity": "inspect_alone:" + scope["counterpart"],
            "material_eligible": None,
            "native_action_performed": False,
        }]
    elif active:
        status = "CONTRADICTION"
    elif eligible:
        status = "COMPUTED_TEST_ONLY_IMMEDIATE"
    else:
        status = "HELD_NO_ELIGIBLE_ORGANIZATION"
    response = {
        "status": status,
        "event_ref": speech["event_hash"],
        "rule": dict(IMMEDIATE_RULE),
        "rule_scope": (
            "EXISTING_P3_RESPONSE_RULE_ACTIVATED_BY_ACTUAL_C04_SPEECH_UPTAKE"),
        "streams": streams,
        "contradictions": active,
        "eligible_modes": sorted({row.get("mode") for row in eligible}),
        "withheld_record_hashes": [
            row.get("record_hash") for row in withheld],
        "material_feasibility": "NOT_EVALUATED_WORLD_PROPOSAL_SEPARATE",
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "memory_formation": "MISSING_RULE",
        "first_person_claims": [],
    }
    prior_scope = {
        "schema": "SOROK_D03_PRIOR_ORGANIZATION_SCOPE@1",
        "project": scope["project"], "counterpart": scope["counterpart"],
        "plan_hash": scope.get("plan_hash"),
        "plan_event_id": plan.get("event_id") if isinstance(plan, Mapping) else None,
        "plan_phase": plan.get("phase") if isinstance(plan, Mapping) else None,
        "activation_roles": list(scope.get("activation_roles") or []),
        "relation_ref": scope.get("relation_ref"),
        "obligation_refs": list(scope.get("obligation_refs") or []),
        "scope_kind": "SOURCEFREE_P3_PLAN_SCOPE_NOT_PARENT_IDENTITY",
    }
    activation_context = {
        "hash": context["hash"],
        "actor_observed": True,
        "actor_observed_basis": "ACTUAL_C04_CHILD_SPEECH_RECEIPT",
        "material_eligible": None,
        "material_eligible_basis": (
            "NOT_EVALUATED_WORLD_PROPOSAL_SEPARATE"),
    }
    durable = {
        "status": "MISSING_RULE",
        "written": False,
        "records": [],
        "target_candidate": None,
        "reason": "NO_D03_DURABLE_OWNER",
        "native_rule": "MISSING_RULE",
        "memory_formation": "MISSING_RULE",
    }
    body = {
        "schema": SCHEMA,
        "grade": GRADE,
        "status": status,
        "identity": detached(snapshot),
        "speech_scope": speech,
        "prior_organization_scope": prior_scope,
        "activation_context": activation_context,
        "immediate_response": response,
        "durable_formation": durable,
        "source_closure": detached(closure),
        "read_boundary": {
            "speech": "C04_ACTUAL_CHILD_SPEECH_UPTAKE_PUBLIC_ONLY",
            "parent_private_state": "NOT_READ",
            "parent_decision": "NOT_READ",
            "period_context": "NOT_READ",
            "cash": "NOT_READ",
            "portal_user_view": "NOT_READ",
            "world_material": "NOT_READ",
            "psyche_store": "P3_ACQUIRED_RECORDS_ACTIVATION_READ",
            "store_write": "NOT_WRITTEN",
        },
        "store_head": {"before": detached(head_before),
                       "after": detached(head_after)},
        "native_rule": "MISSING_RULE",
        "native_action": "NOT_ISSUED_BY_D03_RULE",
        "memory_formation": "MISSING_RULE",
    }
    readset = {
        "identity": {
            "root": snapshot["root"], "actor": snapshot["actor"],
            "branch": snapshot["branch"], "clock": snapshot["clock"],
            "state_hash": snapshot["state_hash"],
        },
        "source_closure": {"hash": closure["hash"]},
        "source_hash": owner.source_hash,
        "registry_hash": owner.registry.get("hash"),
        "speech_scope": {
            "event_id": speech["event_id"],
            "event_hash": speech["event_hash"],
            "text": speech["text"],
            "speaker_actor_id": speech["speaker_actor_id"],
            "alias": speech["alias"],
            "role": speech["role"],
            "child_receipt": detached(speech["receipt"]),
        },
        "prior_organization_scope": {
            "project": prior_scope["project"],
            "counterpart": prior_scope["counterpart"],
            "plan_hash": prior_scope["plan_hash"],
            "scope_kind": prior_scope["scope_kind"],
        },
        "activation_context_hash": context["hash"],
        "eligible_modes": response["eligible_modes"],
        "eligible_record_hashes": [
            row.get("record_hash") for row in eligible],
        "withheld_record_hashes": response["withheld_record_hashes"],
        "contradictions": active,
        "status": status,
        "store_head": detached(head_before),
    }
    body["readset"] = readset
    body["hash"] = digest(body)
    return detached(body)


__all__ = [
    "build_immediate_uptake",
    "source_closure",
    "SCHEMA",
    "GRADE",
    "IMMEDIATE_RULE",
]
