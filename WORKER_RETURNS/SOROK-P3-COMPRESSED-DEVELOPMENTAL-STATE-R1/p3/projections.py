"""P3 pure activation and opacity projections.

This module is a read-only TEST_ONLY boundary. It neither owns a psychological
rule nor writes actor/world state. HQ supplies actual P2 identity, context,
registry, actor experience and public view. Missing native authority remains
held; no memory or first-person claim is formed here.
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Mapping, Sequence

try:
    from developmental_recursion.contracts import (
        RecursionRefusal,
        canonical,
        detached,
        digest,
    )
except ImportError:
    # P3 is imported from the shared worktree while the accepted #704 package
    # remains under its worker return. Add that read-only import root when the
    # caller has not installed it.
    _engine_root = Path(__file__).resolve().parents[2] / "SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1"
    if _engine_root.is_dir() and str(_engine_root) not in sys.path:
        sys.path.insert(0, str(_engine_root))
    from developmental_recursion.contracts import (
        RecursionRefusal,
        canonical,
        detached,
        digest,
    )

GRADE = "SOURCEFREE_TEST_ONLY"
ACTIVATION_STATUSES = frozenset({"ELIGIBLE", "INHIBITED", "UNKNOWN"})
KINDS = frozenset({"V3MS_MEDIATOR", "V3MS_TENSION", "V3MS_PRACTICE"})
PERMISSIONS = frozenset({"OBSERVE_PUBLIC_ACTION", "READ_PUBLIC_DIALOGUE"})
DEMOGRAPHIC_KEYS = frozenset({
    "demographic", "demographics", "class", "social_class", "religion",
    "religiosity", "ethnicity", "race", "gender", "sex", "age",
    "nationality", "country", "caste",
})
EXPLANATION_KEYS = frozenset({
    "actor_state", "causal_parents", "causal_source", "experience_hash",
    "hidden_state", "history_refs", "memory", "private_actor_model",
    "private_emotion", "private_motive", "psyche", "readset", "record_hash",
    "registry_hash", "rule_hash", "rule_id", "source_hash", "source_refs",
    "view_hash", "world_before", "world_after",
})

# The accepted S45 projector is preferred. The fallback is only for import
# isolation; it preserves the accepted public allowlist and never broadens it.
try:
    from s45_projection.projection import (  # type: ignore
        HIDDEN_FIELDS as _S45_HIDDEN,
        PRIVATE_KEYS as _S45_PRIVATE,
        PUBLIC_BODY_FIELDS as _S45_BODY,
        PUBLIC_EVENT_FIELDS as _S45_EVENT,
    )
except ImportError:
    # The P3 worktree does not install the projection return on sys.path by
    # default; locate it read-only when present.
    _worker = Path(__file__).resolve().parents[2]
    _projection = _worker / "SOROK-S45-S47-PROJECTION-20261105-R1"
    if _projection.is_dir() and str(_projection) not in sys.path:
        sys.path.insert(0, str(_projection))
    try:
        from s45_projection.projection import (  # type: ignore
            HIDDEN_FIELDS as _S45_HIDDEN,
            PRIVATE_KEYS as _S45_PRIVATE,
            PUBLIC_BODY_FIELDS as _S45_BODY,
            PUBLIC_EVENT_FIELDS as _S45_EVENT,
        )
    except ImportError:
        _S45_EVENT = (
            "event_id", "kind", "clock", "location", "actor_visible_id",
            "summary", "body_public", "source_ref", "perceived_by_user",
        )
        _S45_BODY = (
            "text", "gesture", "tone", "strategy", "public_role",
            "observable", "language_tag", "changed", "cash_delta",
            "completed_delta", "hours_delta", "material_delta",
            "source_owned", "present_with",
        )
        _S45_PRIVATE = frozenset()
        _S45_HIDDEN = frozenset()

PUBLIC_EVENT_FIELDS = tuple(_S45_EVENT)
PUBLIC_BODY_FIELDS = tuple(_S45_BODY)
PRIVATE_KEYS = frozenset(set(_S45_PRIVATE) | EXPLANATION_KEYS)
HIDDEN_FIELDS = frozenset(_S45_HIDDEN)
ACTOR_EVENT_FIELDS = tuple(x for x in PUBLIC_EVENT_FIELDS if x != "perceived_by_user") + ("perception",)
SPEECH_FIELDS = (
    "event_id", "speaker", "clock", "text", "labeled_english", "gesture",
    "strategy", "summary",
)


def _refuse(code: str, detail: str = "") -> None:
    raise RecursionRefusal(code if not detail else code + ":" + detail)


def _map(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        _refuse(code, "must be an object")
    return dict(value)


def _text(value: Any, code: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or not value.strip():
        _refuse(code, "must be a nonempty string")
    return value


def _hash(value: Any, code: str, *, optional: bool = False) -> str | None:
    if value is None and optional:
        return None
    if not isinstance(value, str) or len(value) != 64:
        _refuse(code, "must be a SHA-256 hex string")
    try:
        int(value, 16)
    except ValueError:
        _refuse(code, "must be a SHA-256 hex string")
    return value.lower()


def _int(value: Any, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        _refuse(code, "must be an integer")
    return value


def _bool(value: Any, code: str, *, optional: bool = False) -> bool | None:
    if value is None and optional:
        return None
    if not isinstance(value, bool):
        _refuse(code, "must be a boolean")
    return value


def _text_list(value: Any, code: str, *, nonempty: bool = False) -> list[str]:
    if not isinstance(value, (list, tuple)):
        _refuse(code, "must be an array")
    out = []
    for item in value:
        if not isinstance(item, str) or not item.strip():
            _refuse(code, "must contain nonempty strings")
        out.append(item)
    if nonempty and not out:
        _refuse(code, "must not be empty")
    if len(set(out)) != len(out):
        _refuse(code, "must not contain duplicates")
    return out


def _doc_hash(value: Mapping[str, Any], code: str) -> str:
    supplied = _hash(value.get("hash"), code + ":HASH")
    expected = digest({key: item for key, item in value.items() if key != "hash"})
    if supplied != expected:
        _refuse(code + ":HASH_MISMATCH")
    return supplied


def _identity(value: Any) -> dict:
    identity = _map(value, "IDENTITY")
    for key in ("root", "actor", "branch"):
        _text(identity.get(key), "IDENTITY_" + key)
    _int(identity.get("clock"), "IDENTITY_CLOCK")
    _hash(identity.get("state_hash"), "IDENTITY_STATE_HASH")
    return identity


def _same_identity(identity: Mapping[str, Any], doc: Mapping[str, Any], code: str,
                   *, include_clock: bool = True) -> None:
    keys = ("root", "actor", "branch", "clock") if include_clock else ("root", "actor", "branch")
    for key in keys:
        if doc.get(key) != identity.get(key):
            _refuse(code + "_IDENTITY_MISMATCH:" + key)


def _registry(value: Any) -> tuple[dict, dict[str, dict]]:
    registry = _map(value, "REGISTRY")
    if registry.get("grade") != GRADE:
        _refuse("REGISTRY_GRADE")
    _hash(registry.get("source_hash"), "REGISTRY_SOURCE_HASH")
    rules = registry.get("rules")
    if not isinstance(rules, list):
        _refuse("REGISTRY_RULES")
    by_id: dict[str, dict] = {}
    for row in rules:
        rule = _map(row, "REGISTRY_RULE")
        rule_id = _text(rule.get("rule_id"), "REGISTRY_RULE_ID")
        rule_version = _text(rule.get("rule_version"), "REGISTRY_RULE_VERSION")
        rule_hash = _hash(rule.get("rule_hash"), "REGISTRY_RULE_HASH")
        key = rule_id + "@" + rule_version
        if key in by_id:
            _refuse("REGISTRY_RULE_DUPLICATE")
        by_id[key] = {"rule_id": rule_id, "rule_version": rule_version,
                      "rule_hash": rule_hash}
    incompatible = registry.get("incompatible_modes")
    if not isinstance(incompatible, list):
        _refuse("REGISTRY_INCOMPATIBLE_MODES")
    normalized_pairs = []
    for pair in incompatible:
        if not isinstance(pair, (list, tuple)) or len(pair) != 2:
            _refuse("REGISTRY_INCOMPATIBLE_MODE_PAIR")
        left = _text(pair[0], "REGISTRY_INCOMPATIBLE_MODE")
        right = _text(pair[1], "REGISTRY_INCOMPATIBLE_MODE")
        if left == right:
            _refuse("REGISTRY_INCOMPATIBLE_SAME_MODE")
        normalized_pairs.append((left, right))
    _doc_hash(registry, "REGISTRY")
    registry["incompatible_modes"] = [list(pair) for pair in normalized_pairs]
    return registry, by_id


def _context(value: Any, identity: Mapping[str, Any]) -> dict:
    context = _map(value, "CONTEXT")
    required = (
        "root", "actor", "branch", "clock", "project", "counterpart",
        "interlocutor_role", "relation_ref", "obligation_refs",
        "actor_observed", "material_eligible", "source_refs", "grade", "hash",
    )
    for key in required:
        if key not in context:
            _refuse("CONTEXT_MISSING:" + key)
    _same_identity(identity, context, "CONTEXT")
    _text(context.get("project"), "CONTEXT_PROJECT")
    _text(context.get("counterpart"), "CONTEXT_COUNTERPART")
    _text(context.get("interlocutor_role"), "CONTEXT_ROLE", optional=True)
    _text(context.get("relation_ref"), "CONTEXT_RELATION", optional=True)
    _text_list(context.get("obligation_refs"), "CONTEXT_OBLIGATIONS")
    _bool(context.get("actor_observed"), "CONTEXT_ACTOR_OBSERVED")
    _bool(context.get("material_eligible"), "CONTEXT_MATERIAL", optional=True)
    refs = _text_list(context.get("source_refs"), "CONTEXT_SOURCE_REFS", nonempty=True)
    for ref in refs:
        _hash(ref, "CONTEXT_SOURCE_REF")
    if context.get("grade") != GRADE:
        _refuse("CONTEXT_GRADE")
    _doc_hash(context, "CONTEXT")
    return context


def _reject_demographic(value: Any, path: str = "payload") -> None:
    if isinstance(value, Mapping):
        for key, item in value.items():
            if isinstance(key, str) and key.lower() in DEMOGRAPHIC_KEYS:
                _refuse("DEMOGRAPHIC_SELECTOR_FORBIDDEN", path + "." + key)
            _reject_demographic(item, path + "." + str(key))
    elif isinstance(value, (list, tuple)):
        for index, item in enumerate(value):
            _reject_demographic(item, path + "[" + str(index) + "]")


def _record(value: Any, identity: Mapping[str, Any], registry: Mapping[str, Any],
            rules: Mapping[str, Mapping[str, Any]]) -> dict:
    record = _map(value, "RECORD")
    required = (
        "root", "actor", "branch", "project", "counterpart", "record_id",
        "kind", "payload", "rule_id", "rule_version", "rule_hash",
        "registry_hash", "source_hash", "effective_from", "causal_parents",
        "grade", "hash",
    )
    for key in required:
        if key not in record:
            _refuse("RECORD_MISSING:" + key)
    _same_identity(identity, record, "RECORD", include_clock=False)
    _text(record.get("project"), "RECORD_PROJECT")
    _text(record.get("counterpart"), "RECORD_COUNTERPART")
    _text(record.get("record_id"), "RECORD_ID")
    _text(record.get("kind"), "RECORD_KIND")
    if record["kind"] not in KINDS:
        _refuse("RECORD_KIND")
    _int(record.get("effective_from"), "RECORD_EFFECTIVE_FROM")
    if record.get("grade") != GRADE:
        _refuse("RECORD_GRADE")
    _hash(record.get("registry_hash"), "RECORD_REGISTRY_HASH")
    _hash(record.get("source_hash"), "RECORD_SOURCE_HASH")
    if record["registry_hash"] != registry["hash"]:
        _refuse("RECORD_REGISTRY_MISMATCH")
    if record["source_hash"] != registry["source_hash"]:
        _refuse("RECORD_SOURCE_MISMATCH")
    rule_id = _text(record.get("rule_id"), "RECORD_RULE_ID")
    rule_version = _text(record.get("rule_version"), "RECORD_RULE_VERSION")
    rule_hash = _hash(record.get("rule_hash"), "RECORD_RULE_HASH")
    descriptor = rules.get(rule_id + "@" + rule_version)
    if descriptor is None or descriptor["rule_hash"] != rule_hash:
        _refuse("RECORD_RULE_UNKNOWN")
    payload = _map(record.get("payload"), "RECORD_PAYLOAD")
    _reject_demographic(payload)
    _text(payload.get("mode"), "RECORD_MODE")
    for key in ("activation_roles", "relation_refs", "obligation_refs"):
        if key in payload:
            _text_list(payload[key], "RECORD_PAYLOAD_" + key)
    if "requires_actor_access" in payload:
        _bool(payload["requires_actor_access"], "RECORD_REQUIRES_ACTOR_ACCESS")
    parents = record.get("causal_parents")
    _text_list(parents, "RECORD_CAUSAL_PARENTS")
    _doc_hash(record, "RECORD")
    return record


def _record_scope(record: Mapping[str, Any]) -> tuple:
    payload = record["payload"]
    return (
        record["project"],
        record["counterpart"],
        tuple(sorted(payload.get("relation_refs", ()))),
        tuple(sorted(payload.get("obligation_refs", ()))),
    )


def _activation(record: Mapping[str, Any], context: Mapping[str, Any],
                identity: Mapping[str, Any]) -> str:
    if int(record["effective_from"]) > int(identity["clock"]):
        return "UNKNOWN"
    payload = record["payload"]
    roles = payload.get("activation_roles", ())
    if roles:
        role = context.get("interlocutor_role")
        if role is None:
            return "UNKNOWN"
        if role not in roles:
            return "INHIBITED"
    relations = payload.get("relation_refs", ())
    if relations:
        relation = context.get("relation_ref")
        if relation is None:
            return "UNKNOWN"
        if relation not in relations:
            return "INHIBITED"
    obligations = payload.get("obligation_refs", ())
    if obligations:
        context_obligations = context.get("obligation_refs", ())
        if not context_obligations:
            return "UNKNOWN"
        if not set(obligations) & set(context_obligations):
            return "INHIBITED"
    if payload.get("requires_actor_access") is True:
        if context.get("actor_observed") is False:
            return "INHIBITED"
    return "ELIGIBLE"


def activate(records: Any, *, identity: Any, context: Any, registry: Any) -> dict:
    """Return a pure activation read over exact sourcefree records.

    All input documents are detached. No record, registry, context or identity
    is mutated. No activation/lifecycle flag is persisted.
    """
    ident = _identity(identity)
    registry_doc, rules = _registry(registry)
    ctx = _context(context, ident)
    if isinstance(records, (str, bytes, Mapping)) or not isinstance(records, (list, tuple)):
        _refuse("RECORDS")
    validated = [
        _record(record, ident, registry_doc, rules)
        for record in detached(list(records))
    ]
    relevant = [
        record for record in validated
        if record["project"] == ctx["project"]
        and record["counterpart"] == ctx["counterpart"]
    ]
    relevant.sort(key=lambda row: (row["record_id"], row["hash"]))
    entries = []
    for record in relevant:
        activation = _activation(record, ctx, ident)
        payload = record["payload"]
        readset = [
            "record:" + record["hash"],
            "registry:" + registry_doc["hash"],
            "context:" + ctx["hash"],
            "rule:" + record["rule_hash"],
        ] + ["source:" + ref for ref in ctx["source_refs"]]
        entries.append({
            "record_id": record["record_id"],
            "record_hash": record["hash"],
            "kind": record["kind"],
            "mode": payload["mode"],
            "activation": activation,
            "material_eligible": ctx.get("material_eligible"),
            "readset": readset,
        })

    incompatible = {frozenset(pair) for pair in registry_doc["incompatible_modes"]}
    contradictions = []
    active = [r for r in relevant if int(r["effective_from"]) <= int(ident["clock"])]
    for index, left in enumerate(active):
        for right in active[index + 1:]:
            if _record_scope(left) != _record_scope(right):
                continue
            if frozenset((left["payload"]["mode"], right["payload"]["mode"])) in incompatible:
                pair = sorted([left["record_id"], right["record_id"]])
                if pair not in contradictions:
                    contradictions.append(pair)
    contradictions.sort()
    return {
        "grade": GRADE,
        "identity": detached(ident),
        "context_hash": ctx["hash"],
        "registry_hash": registry_doc["hash"],
        "status": "CONTRADICTION" if contradictions else "OK",
        "entries": entries,
        "contradictions": contradictions,
    }


def _sanitize_body(value: Any) -> dict:
    body = _map(value, "PUBLIC_BODY")
    return {
        key: _sanitize_value(body[key])
        for key in PUBLIC_BODY_FIELDS
        if key in body
        and not isinstance(body[key], (set, bytes))
    }


def _sanitize_value(value: Any) -> Any:
    if isinstance(value, Mapping):
        return {
            str(key): _sanitize_value(item)
            for key, item in value.items()
            if str(key) not in PRIVATE_KEYS
            and str(key) not in HIDDEN_FIELDS
            and not str(key).lower().startswith("_")
        }
    if isinstance(value, (list, tuple)):
        return [_sanitize_value(item) for item in value]
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    _refuse("PROJECTION_UNSUPPORTED_VALUE")


def _event(value: Any, *, actor: bool) -> dict:
    event = _map(value, "PUBLIC_EVENT")
    fields = ACTOR_EVENT_FIELDS if actor else PUBLIC_EVENT_FIELDS
    out = {}
    for key in fields:
        if key not in event:
            continue
        if key == "body_public":
            out[key] = _sanitize_body(event[key])
        elif key == "perception" and actor:
            perception = event[key]
            if isinstance(perception, Mapping):
                out[key] = {
                    "clock": perception.get("clock"),
                    "channel": _text(perception.get("channel"), "PERCEPTION_CHANNEL", optional=True),
                }
        elif key == "perceived_by_user":
            continue
        else:
            out[key] = _sanitize_value(event[key])
    return out


def _speech(value: Any) -> dict:
    row = _map(value, "PUBLIC_SPEECH")
    return {
        key: _sanitize_value(row[key])
        for key in SPEECH_FIELDS
        if key in row
    }


def _standpoint(value: Any, identity: Mapping[str, Any]) -> dict:
    standpoint = _map(value, "STANDPOINT")
    for key in ("root", "actor", "branch", "clock", "interlocutor_ref",
                "role", "permissions", "source_refs", "grade", "hash"):
        if key not in standpoint:
            _refuse("STANDPOINT_MISSING:" + key)
    _same_identity(identity, standpoint, "STANDPOINT")
    _text(standpoint.get("interlocutor_ref"), "STANDPOINT_INTERLOCUTOR")
    _text(standpoint.get("role"), "STANDPOINT_ROLE")
    permissions = _text_list(standpoint.get("permissions"), "STANDPOINT_PERMISSIONS")
    if any(permission not in PERMISSIONS for permission in permissions):
        _refuse("STANDPOINT_PERMISSION_UNSUPPORTED")
    refs = _text_list(standpoint.get("source_refs"), "STANDPOINT_SOURCE_REFS", nonempty=True)
    for ref in refs:
        _hash(ref, "STANDPOINT_SOURCE_REF")
    if standpoint.get("grade") != GRADE:
        _refuse("STANDPOINT_GRADE")
    _doc_hash(standpoint, "STANDPOINT")
    return standpoint


def _binding(value: Any, identity: Mapping[str, Any], code: str,
            expected_hash: str, hash_key: str) -> dict:
    binding = _map(value, code)
    for key in ("root", "actor", "branch", "clock", hash_key):
        if key not in binding:
            _refuse(code + "_MISSING:" + key)
    _same_identity(identity, binding, code)
    supplied = _hash(binding[hash_key], code + "_HASH")
    if supplied != expected_hash:
        _refuse(code + "_HASH_MISMATCH")
    return binding


def project_views(*, identity: Any, actor_experience: Any,
                  experience_binding: Any, public_view: Any,
                  public_binding: Any, standpoint: Any) -> dict:
    """Project actual P2 actor and public surfaces without widening access."""
    ident = _identity(identity)
    actor_doc = None if actor_experience is None else _map(
        actor_experience, "ACTOR_EXPERIENCE")
    actor_hash = digest(actor_doc)
    _binding(experience_binding, ident, "EXPERIENCE", actor_hash, "experience_hash")
    public_doc = _map(public_view, "PUBLIC_VIEW")
    public_hash = digest(public_doc)
    _binding(public_binding, ident, "PUBLIC", public_hash, "view_hash")
    stand = _standpoint(standpoint, ident)

    if public_doc.get("clock") != ident["clock"]:
        _refuse("PUBLIC_VIEW_CLOCK_MISMATCH")
    if actor_doc is None or actor_doc.get("status") != "OBSERVED":
        actor = {
            "status": "HELD",
            "actor_ref": ident["actor"],
            "events": [],
            "memory_formation": "MISSING_RULE",
        }
        if actor_doc is not None and actor_doc.get("reason"):
            actor["reason"] = _text(actor_doc["reason"], "ACTOR_REASON")
    else:
        if actor_doc.get("actor_ref") != ident["actor"]:
            _refuse("ACTOR_EXPERIENCE_IDENTITY_MISMATCH")
        events = actor_doc.get("events")
        if not isinstance(events, list):
            _refuse("ACTOR_EXPERIENCE_EVENTS")
        actor = {
            "status": "OBSERVED",
            "actor_ref": ident["actor"],
            "events": [_event(event, actor=True) for event in events],
            "memory_formation": "MISSING_RULE",
        }

    visible_events = public_doc.get("visible_events", [])
    visible_actions = public_doc.get("visible_actions", [])
    visible_speech = public_doc.get("visible_speech", [])
    for name, rows in (
        ("VISIBLE_EVENTS", visible_events),
        ("VISIBLE_ACTIONS", visible_actions),
        ("VISIBLE_SPEECH", visible_speech),
    ):
        if not isinstance(rows, list):
            _refuse("PUBLIC_VIEW_" + name)
    permissions = set(stand["permissions"])
    allowed_events = []
    allowed_actions = []
    allowed_speech = []
    if "OBSERVE_PUBLIC_ACTION" in permissions:
        allowed_events = [
            _event(event, actor=False) for event in visible_events
            if event.get("kind") != "SPEECH"
        ]
        allowed_actions = [_event(event, actor=False) for event in visible_actions]
    if "READ_PUBLIC_DIALOGUE" in permissions:
        allowed_speech = [_speech(row) for row in visible_speech]
    user = {
        "status": "OBSERVED" if permissions else "HELD",
        "clock": public_doc.get("clock"),
        "location": _text(public_doc.get("location"), "PUBLIC_VIEW_LOCATION", optional=True),
        "visible_events": allowed_events,
        "visible_actions": allowed_actions,
        "visible_speech": allowed_speech,
        "memory_formation": "MISSING_RULE",
        "claims_status": "DEFER_MISSING_AUTHORITY",
    }
    return {
        "grade": GRADE,
        "actor": actor,
        "user": user,
        "claims_status": "DEFER_MISSING_AUTHORITY",
    }


__all__ = ["GRADE", "activate", "project_views"]
