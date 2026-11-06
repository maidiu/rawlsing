"""Pure source-preserving compression-evidence sidecar.

This module implements the frozen compression API in
``WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/INTEGRATION_CONTRACT.md``.
It validates sourcefree evidence and an actual P2 ``RealizedEvent`` document,
then returns content-addressed metadata.  It has no state writer, no P2 call,
no interval/RNG handler, no psychological rule and no memory/claim authority.

The four declared forms are selection/evidence forms, not new event kinds and
not a licence to multiply imagined witnesses.  An absent actual actor access
returns HELD; an absent source basis, wrong binding, changed source, unsupported
field or malformed receipt refuses before any metadata is emitted.
"""
from __future__ import annotations

import hashlib
from typing import Any, Mapping

from developmental_recursion.contracts import (
    RecursionRefusal,
    canonical,
    detached,
    digest,
)

ENVELOPE_SCHEMA = "SOROK_P3_COMPRESSION_EVIDENCE_ENVELOPE@TEST_ONLY/1"
SPEC_KEYS = {
    "envelope_id",
    "proposal_hash",
    "representation_form",
    "represented_window",
    "recurrence_basis_refs",
    "participation_refs",
    "material_relation_refs",
    "observed",
    "unobserved",
    "selection_basis",
}
WINDOW_KEYS = {"from_clock", "to_clock", "coverage_basis"}
PROPOSAL_KEYS = {
    "event_id",
    "event_time",
    "operation",
    "source_refs",
    "participants",
    "circumstances",
    "interval",
}
IDENTITY_KEYS = {"root", "actor", "branch", "clock", "state_hash"}
REALIZED_KEYS = {
    "operation_id",
    "proposal_hash",
    "before",
    "after",
    "status",
    "objective",
    "accessible",
    "consequences",
    "readset",
    "receipt_ref",
}
SOURCE_KEYS = {
    "hash",
    "grade",
    "root",
    "actor",
    "branch",
    "kind",
    "from_clock",
    "to_clock",
    "data",
}
FORMS = {
    "SINGULAR_OCCURRENCE",
    "REPRESENTATIVE_EPISODE",
    "ACCUMULATED_INTERVAL",
    "RETROSPECTIVE_CRYSTALLIZATION",
}
FORM_SOURCE_KIND = {
    "REPRESENTATIVE_EPISODE": "RECURRING_RELATION",
    "ACCUMULATED_INTERVAL": "BOUNDED_INTERVAL",
    "RETROSPECTIVE_CRYSTALLIZATION": "HISTORICAL_SOURCE",
}
ACTIVE_EVENT_STATUSES = {"REALIZED", "NO_CHANGE", "IMMEDIATE_ONLY"}
INTERVAL_STATUSES = {"REALIZED", "PARTIAL", "NOT_PERFORMED", "UNKNOWN", "REFUSED"}
POSITIVE_INTERVAL_STATUSES = {"REALIZED", "PARTIAL"}
HEX = set("0123456789abcdef")


class CompressionRefusal(RecursionRefusal):
    """Malformed or wrongly bound compression evidence."""


def _fail(message: str) -> None:
    raise CompressionRefusal(message)


def _is_int(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _is_hash(value: Any) -> bool:
    return (
        isinstance(value, str)
        and len(value) == 64
        and all(ch in HEX for ch in value.lower())
    )


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, Mapping):
        _fail(f"{label} must be an object")
    try:
        return detached(value)
    except Exception as exc:
        raise CompressionRefusal(f"{label} must be detached JSON") from exc


def _exact(value: Any, keys: set[str], label: str) -> dict[str, Any]:
    doc = _mapping(value, label)
    if set(doc) != keys:
        _fail(f"{label} has unexpected or missing keys")
    return doc


def _string(value: Any, label: str) -> str:
    if not isinstance(value, str) or not value:
        _fail(f"{label} must be a nonempty string")
    return value


def _strings(value: Any, label: str, *, nonempty: bool = True) -> list[str]:
    if not isinstance(value, list) or (nonempty and not value):
        _fail(f"{label} must be a {'nonempty ' if nonempty else ''}list")
    out: list[str] = []
    for item in value:
        out.append(_string(item, f"{label} item"))
    if len(set(out)) != len(out):
        _fail(f"{label} contains duplicates")
    return out


def _identity(value: Any) -> dict[str, Any]:
    doc = _exact(value, IDENTITY_KEYS, "identity")
    for key in ("root", "actor", "branch", "state_hash"):
        _string(doc[key], f"identity.{key}")
    if not _is_int(doc["clock"]) or doc["clock"] < 0:
        _fail("identity.clock must be a nonnegative integer")
    return doc


def _proposal(value: Any) -> dict[str, Any]:
    doc = _exact(value, PROPOSAL_KEYS, "proposal")
    _string(doc["event_id"], "proposal.event_id")
    _string(doc["operation"], "proposal.operation")
    if not _is_int(doc["event_time"]) or doc["event_time"] < 0:
        _fail("proposal.event_time must be a nonnegative integer")
    _strings(doc["source_refs"], "proposal.source_refs", nonempty=False)
    _strings(doc["participants"], "proposal.participants", nonempty=False)
    doc["circumstances"] = _mapping(doc["circumstances"], "proposal.circumstances")
    interval = doc["interval"]
    if interval is not None:
        interval = _exact(interval, {"mode", "span"}, "proposal.interval")
        _string(interval["mode"], "proposal.interval.mode")
        if not _is_int(interval["span"]) or interval["span"] < 1:
            _fail("proposal.interval.span must be a positive integer")
        doc["interval"] = interval
    return doc


def _source(ref: str, value: Any, identity: Mapping[str, Any]) -> dict[str, Any]:
    doc = _exact(value, SOURCE_KEYS, f"catalog[{ref}]")
    _string(doc["kind"], f"catalog[{ref}].kind")
    if doc["grade"] != "SOURCEFREE_TEST_ONLY":
        _fail(f"catalog[{ref}] is not SOURCEFREE_TEST_ONLY")
    for key in ("root", "actor", "branch"):
        _string(doc[key], f"catalog[{ref}].{key}")
        if doc[key] != identity[key]:
            _fail(f"catalog[{ref}] identity mismatch: {key}")
    if not _is_int(doc["from_clock"]) or not _is_int(doc["to_clock"]):
        _fail(f"catalog[{ref}] clocks must be integers")
    if doc["from_clock"] < 0 or doc["from_clock"] > doc["to_clock"]:
        _fail(f"catalog[{ref}] has invalid clock range")
    if not _is_hash(doc["hash"]):
        _fail(f"catalog[{ref}].hash must be a lowercase 64-hex digest")
    body = {k: v for k, v in doc.items() if k != "hash"}
    if digest(body) != doc["hash"]:
        _fail(f"catalog[{ref}] source hash does not bind its complete document")
    doc["data"] = _mapping(doc["data"], f"catalog[{ref}].data")
    return doc


def _catalog(value: Any, identity: Mapping[str, Any], refs: list[str]) -> dict[str, dict[str, Any]]:
    catalog = _mapping(value, "catalog")
    out: dict[str, dict[str, Any]] = {}
    for ref in refs:
        if ref not in catalog:
            _fail(f"catalog source missing: {ref}")
        out[ref] = _source(ref, catalog[ref], identity)
    return out


def _window(value: Any, identity: Mapping[str, Any], proposal: Mapping[str, Any]) -> dict[str, Any]:
    doc = _exact(value, WINDOW_KEYS, "represented_window")
    if not _is_int(doc["from_clock"]) or not _is_int(doc["to_clock"]):
        _fail("represented_window clocks must be integers")
    if doc["from_clock"] < 0 or doc["from_clock"] > doc["to_clock"]:
        _fail("represented_window has invalid clock range")
    _string(doc["coverage_basis"], "represented_window.coverage_basis")
    return doc


def _validate_spec(
    spec: Any,
    identity: Mapping[str, Any],
    proposal: Mapping[str, Any],
    catalog: Mapping[str, Any],
) -> dict[str, Any]:
    doc = _exact(spec, SPEC_KEYS, "spec")
    _string(doc["envelope_id"], "spec.envelope_id")
    form = _string(doc["representation_form"], "spec.representation_form")
    if form not in FORMS:
        _fail("spec.representation_form is unsupported")
    if not _is_hash(doc["proposal_hash"]):
        _fail("spec.proposal_hash must be a lowercase 64-hex digest")
    if doc["proposal_hash"] != digest(proposal):
        _fail("spec.proposal_hash does not bind the supplied proposal")
    if proposal["event_time"] <= identity["clock"]:
        _fail("present event time must be after the owner clock")
    window = _window(doc["represented_window"], identity, proposal)
    for key in (
        "recurrence_basis_refs",
        "participation_refs",
        "material_relation_refs",
    ):
        doc[key] = _strings(doc[key], f"spec.{key}", nonempty=(key != "recurrence_basis_refs" and key != "material_relation_refs"))
    for key in ("observed", "unobserved"):
        doc[key] = _strings(doc[key], f"spec.{key}", nonempty=False)
    if set(doc["observed"]) & set(doc["unobserved"]):
        _fail("observed and unobserved scopes overlap")
    _string(doc["selection_basis"], "spec.selection_basis")

    if not doc["participation_refs"]:
        _fail("spec requires at least one actor participation source")
    all_refs = []
    for key in (
        "recurrence_basis_refs",
        "participation_refs",
        "material_relation_refs",
    ):
        all_refs.extend(doc[key])
    sources = _catalog(catalog, identity, all_refs)
    for ref, source in sources.items():
        if source["to_clock"] > proposal["event_time"]:
            _fail(f"catalog[{ref}] extends past the present event")

    if form == "SINGULAR_OCCURRENCE":
        if not window["from_clock"] <= proposal["event_time"] <= window["to_clock"]:
            _fail("singular occurrence event is outside represented_window")
    elif form == "REPRESENTATIVE_EPISODE":
        if not doc["recurrence_basis_refs"]:
            _fail("representative episode requires a recurring-relation source")
        recurring = [sources[r] for r in doc["recurrence_basis_refs"]
                     if sources[r]["kind"] == FORM_SOURCE_KIND[form]]
        if not recurring:
            _fail("representative episode has no RECURRING_RELATION source")
        if not any(s["from_clock"] <= window["to_clock"]
                   and s["to_clock"] >= window["from_clock"] for s in recurring):
            _fail("recurring-relation source does not overlap represented_window")
    elif form == "ACCUMULATED_INTERVAL":
        if not doc["recurrence_basis_refs"]:
            _fail("accumulated interval requires a bounded-interval source")
        bounded = [sources[r] for r in doc["recurrence_basis_refs"]
                   if sources[r]["kind"] == FORM_SOURCE_KIND[form]]
        if not bounded:
            _fail("accumulated interval has no BOUNDED_INTERVAL source")
        if not any(s["from_clock"] == window["from_clock"]
                   and s["to_clock"] == window["to_clock"] for s in bounded):
            _fail("bounded-interval source does not exactly bind represented_window")
        if proposal["event_time"] < window["to_clock"]:
            _fail("present event precedes the accumulated interval")
    elif form == "RETROSPECTIVE_CRYSTALLIZATION":
        if not doc["recurrence_basis_refs"]:
            _fail("retrospective crystallization requires a historical source")
        historical = [sources[r] for r in doc["recurrence_basis_refs"]
                      if sources[r]["kind"] == FORM_SOURCE_KIND[form]]
        if not historical:
            _fail("retrospective crystallization has no HISTORICAL_SOURCE source")
        if not any(s["from_clock"] == window["from_clock"]
                   and s["to_clock"] == window["to_clock"] for s in historical):
            _fail("historical source does not exactly bind represented_window")
        if not window["to_clock"] < proposal["event_time"]:
            _fail("retrospective historical source is not fixed before the present event")
    return doc


def preflight(
    spec: Any,
    *,
    identity: Any,
    proposal: Any,
    catalog: Any,
) -> dict[str, Any]:
    """Validate a compression spec without actual-event or side effects."""
    identity_doc = _identity(identity)
    proposal_doc = _proposal(proposal)
    return _validate_spec(spec, identity_doc, proposal_doc, catalog)


def _realized(value: Any, identity: Mapping[str, Any], proposal: Mapping[str, Any]) -> dict[str, Any]:
    doc = _exact(value, REALIZED_KEYS, "realized")
    _string(doc["operation_id"], "realized.operation_id")
    if not _is_hash(doc["proposal_hash"]):
        _fail("realized.proposal_hash must be a lowercase 64-hex digest")
    if doc["proposal_hash"] != digest(proposal):
        _fail("realized.proposal_hash does not bind the supplied proposal")
    before = _identity(doc["before"])
    after = _identity(doc["after"])
    if before != identity:
        _fail("realized.before does not equal supplied identity")
    if any(after[k] != before[k] for k in ("root", "actor", "branch")):
        _fail("realized.after identity changed")
    if after["clock"] < before["clock"]:
        _fail("realized.after clock moved backwards")
    _string(doc["status"], "realized.status")
    _strings(doc["readset"], "realized.readset", nonempty=False)
    _string(doc["receipt_ref"], "realized.receipt_ref")
    doc["before"] = before
    doc["after"] = after
    doc["objective"] = _mapping(doc["objective"], "realized.objective")
    doc["consequences"] = _mapping(doc["consequences"], "realized.consequences")
    doc["accessible"] = _mapping(doc["accessible"], "realized.accessible")

    event = doc["objective"].get("event")
    if event is None:
        return doc
    event = _mapping(event, "realized.objective.event")
    event_ref = _string(event.get("e1_event_id"), "actual event e1_event_id")
    event_hash = _string(event.get("e1_event_hash"), "actual event e1_event_hash")
    if not _is_hash(event_hash):
        _fail("actual event e1_event_hash must be a lowercase 64-hex digest")
    if event.get("actor_id") != identity["actor"]:
        _fail("actual event actor does not bind identity")
    if "branch_id" in event and event["branch_id"] != identity["branch"]:
        _fail("actual event branch does not bind identity")
    if event_hash not in doc["readset"] or doc["receipt_ref"] != "P2_EVENT:" + event_hash:
        _fail("actual event hash is not bound to readset/receipt")
    action_ref = event.get("action_event_id")
    action_hash = event.get("action_event_hash")
    if action_ref is not None or action_hash is not None:
        _string(action_ref, "actual action_event_id")
        _string(action_hash, "actual action_event_hash")
        if not _is_hash(action_hash):
            _fail("actual action_event_hash must be a lowercase 64-hex digest")
        doc["actual_action_ref"] = action_ref
        doc["actual_action_hash"] = action_hash
    else:
        doc["actual_action_ref"] = None
        doc["actual_action_hash"] = None
    doc["objective"]["event"] = event
    doc["actual_event_ref"] = event_ref
    doc["actual_event_hash"] = event_hash
    return doc


def _perception_refs(accessible: Mapping[str, Any], action_ref: str,
                     actor: str) -> list[dict[str, Any]]:
    status = accessible.get("status")
    if status != "OBSERVED":
        return []
    actor_ref = accessible.get("actor_ref")
    if actor_ref is None:
        return []
    if actor_ref != actor:
        _fail("actor-accessible projection binds a different actor")
    refs: list[dict[str, Any]] = []
    events = accessible.get("events")
    if isinstance(events, list):
        for event in events:
            if not isinstance(event, Mapping):
                _fail("accessible event is malformed")
            if event.get("perceived_by_user"):
                _fail("actor-accessible projection contains user-view marker")
            perception = event.get("perception")
            if not isinstance(perception, Mapping):
                continue
            clock = perception.get("clock")
            channel = perception.get("channel")
            if not _is_int(clock) or not isinstance(channel, str) or not channel:
                _fail("actor perception receipt is malformed")
            event_id = event.get("event_id")
            refs.append({
                "event_id": _string(event_id, "accessible event_id") if event_id else None,
                "clock": clock,
                "channel": channel,
                "ref": digest({"event_id": event_id, "clock": clock, "channel": channel}),
            })
    else:
        event_ids = accessible.get("event_ids")
        perceptions = accessible.get("perceptions")
        if isinstance(event_ids, list) and isinstance(perceptions, list):
            if len(event_ids) != len(perceptions):
                _fail("accessible event_ids/perceptions length mismatch")
            for event_id, perception in zip(event_ids, perceptions):
                _string(event_id, "accessible event_id")
                if not isinstance(perception, Mapping):
                    _fail("accessible perception is malformed")
                if perception.get("perceived_by_user"):
                    _fail("actor-accessible projection contains user-view marker")
                clock = perception.get("clock")
                channel = perception.get("channel")
                if not _is_int(clock) or not isinstance(channel, str) or not channel:
                    _fail("actor perception receipt is malformed")
                refs.append({
                    "event_id": event_id,
                    "clock": clock,
                    "channel": channel,
                    "ref": digest({"event_id": event_id, "clock": clock, "channel": channel}),
                })
    if refs and not any(ref["event_id"] == action_ref for ref in refs):
        return []
    return refs


def _interval(value: Any) -> dict[str, Any] | None:
    if value is None:
        return None
    doc = _mapping(value, "actual interval")
    status = _string(doc.get("status"), "actual interval status")
    if status not in INTERVAL_STATUSES:
        _fail("actual interval status is unsupported")
    receipt_hash = doc.get("receipt_hash")
    if not _is_hash(receipt_hash):
        _fail("actual interval receipt_hash is missing or malformed")
    return doc


def _held_envelope(
    spec: Mapping[str, Any],
    identity: Mapping[str, Any],
    *,
    reason: str,
    actual_event_ref: str | None = None,
    actual_event_hash: str | None = None,
    actual_action_ref: str | None = None,
    actual_action_hash: str | None = None,
    actual_interval: Mapping[str, Any] | None = None,
    source_hashes: Mapping[str, str] | None = None,
    native_status: str | None = None,
) -> dict[str, Any]:
    number = {
        "schema": ENVELOPE_SCHEMA,
        "status": "HELD",
        "held_reason": reason,
        "envelope_id": spec["envelope_id"],
        "spec_hash": digest(spec),
        "sourcefree_grade": "SOURCEFREE_TEST_ONLY",
        "identity": detached(identity),
        "proposal_hash": spec["proposal_hash"],
        "representation_form": spec["representation_form"],
        "represented_window": spec["represented_window"],
        "source_ref_hashes": detached(source_hashes or {}),
        "actual_event_ref": actual_event_ref,
        "actual_event_hash": actual_event_hash,
        "actual_action_ref": actual_action_ref,
        "actual_action_hash": actual_action_hash,
        "native_status": native_status,
        "actual_interval_ref": None,
        "actual_interval_hash": None,
        "actual_interval_status": None,
        "actor_access": "HELD",
        "perception_refs": [],
        "observed": spec["observed"],
        "unobserved": spec["unobserved"],
        "selection_basis": spec["selection_basis"],
        "psychological_effects": [],
        "no_psychological_effects": True,
        "no_state_mutation": True,
        "memory_or_claim_issued": False,
        "adp016_017_authorized": False,
    }
    if actual_interval is not None:
        number["actual_interval_ref"] = actual_interval.get("receipt_hash")
        number["actual_interval_hash"] = digest(actual_interval)
        number["actual_interval_status"] = actual_interval.get("status")
    return _seal(number)


def _bound_envelope(
    spec: Mapping[str, Any],
    identity: Mapping[str, Any],
    *,
    actual_event_ref: str,
    actual_event_hash: str,
    actual_action_ref: str,
    actual_action_hash: str,
    actual_interval: Mapping[str, Any] | None,
    perception_refs: list[dict[str, Any]],
    source_hashes: Mapping[str, str],
    native_status: str,
) -> dict[str, Any]:
    number = {
        "schema": ENVELOPE_SCHEMA,
        "status": "BOUND",
        "held_reason": None,
        "envelope_id": spec["envelope_id"],
        "spec_hash": digest(spec),
        "sourcefree_grade": "SOURCEFREE_TEST_ONLY",
        "identity": detached(identity),
        "proposal_hash": spec["proposal_hash"],
        "representation_form": spec["representation_form"],
        "represented_window": spec["represented_window"],
        "source_ref_hashes": detached(source_hashes),
        "actual_event_ref": actual_event_ref,
        "actual_event_hash": actual_event_hash,
        "actual_action_ref": actual_action_ref,
        "actual_action_hash": actual_action_hash,
        "native_status": native_status,
        "actual_interval_ref": actual_interval.get("receipt_hash") if actual_interval else None,
        "actual_interval_hash": digest(actual_interval) if actual_interval else None,
        "actual_interval_status": actual_interval.get("status") if actual_interval else None,
        "actor_access": "OBSERVED",
        "perception_refs": detached(perception_refs),
        "observed": spec["observed"],
        "unobserved": spec["unobserved"],
        "selection_basis": spec["selection_basis"],
        "psychological_effects": [],
        "no_psychological_effects": True,
        "no_state_mutation": True,
        "memory_or_claim_issued": False,
        "adp016_017_authorized": False,
    }
    return _seal(number)


def _seal(number: dict[str, Any]) -> dict[str, Any]:
    body = {k: v for k, v in number.items() if k != "envelope_hash"}
    body["envelope_hash"] = digest(body)
    return body


def bind(
    spec: Any,
    *,
    identity: Any,
    proposal: Any,
    catalog: Any,
    realized: Any,
) -> dict[str, Any]:
    """Bind validated compression metadata to one actual P2 event.

    Returns BOUND metadata only when the actor's actual accessible projection
    contains the present native event.  Returns HELD metadata when that actor
    access is unavailable.  Wrong identity/proposal/source/event bindings are
    refusals.  This function never mutates P2 world, actor or psychological state.
    """
    identity_doc = _identity(identity)
    proposal_doc = _proposal(proposal)
    spec_doc = _validate_spec(spec, identity_doc, proposal_doc, catalog)
    realized_doc = _realized(realized, identity_doc, proposal_doc)

    all_refs = (
        spec_doc["recurrence_basis_refs"]
        + spec_doc["participation_refs"]
        + spec_doc["material_relation_refs"]
    )
    sources = _catalog(catalog, identity_doc, all_refs)
    source_hashes = {ref: sources[ref]["hash"] for ref in sorted(set(all_refs))}

    actual_event_ref = realized_doc.get("actual_event_ref")
    actual_event_hash = realized_doc.get("actual_event_hash")
    actual_action_ref = realized_doc.get("actual_action_ref")
    actual_action_hash = realized_doc.get("actual_action_hash")
    interval = _interval(realized_doc["objective"].get("interval"))
    consequence_interval = _interval(realized_doc["consequences"].get("interval"))
    if interval != consequence_interval:
        _fail("objective/consequence interval receipts differ")

    if realized_doc["status"] not in ACTIVE_EVENT_STATUSES:
        return _held_envelope(
            spec_doc, identity_doc,
            reason="ACTUAL_EVENT_NOT_AVAILABLE",
            actual_event_ref=actual_event_ref,
            actual_event_hash=actual_event_hash,
            actual_action_ref=actual_action_ref,
            actual_action_hash=actual_action_hash,
            actual_interval=interval,
            source_hashes=source_hashes,
            native_status=realized_doc["status"],
        )
    if not actual_event_ref or not actual_event_hash:
        return _held_envelope(
            spec_doc, identity_doc,
            reason="ACTUAL_EVENT_UNAVAILABLE",
            actual_interval=interval,
            source_hashes=source_hashes,
            native_status=realized_doc["status"],
        )
    if not actual_action_ref or not actual_action_hash:
        return _held_envelope(
            spec_doc, identity_doc,
            reason="ACTUAL_ACTION_BINDING_UNAVAILABLE",
            actual_event_ref=actual_event_ref,
            actual_event_hash=actual_event_hash,
            actual_action_ref=actual_action_ref,
            actual_action_hash=actual_action_hash,
            actual_interval=interval,
            source_hashes=source_hashes,
            native_status=realized_doc["status"],
        )
    accessible = realized_doc["accessible"]
    if accessible.get("actor_ref") not in (None, identity_doc["actor"]):
        _fail("realized actor access binds a different actor")
    if accessible.get("status") != "OBSERVED" or accessible.get("actor_ref") is None:
        return _held_envelope(
            spec_doc, identity_doc,
            reason="ACTOR_ACCESS_UNAVAILABLE",
            actual_event_ref=actual_event_ref,
            actual_event_hash=actual_event_hash,
            actual_action_ref=actual_action_ref,
            actual_action_hash=actual_action_hash,
            actual_interval=interval,
            source_hashes=source_hashes,
            native_status=realized_doc["status"],
        )
    perception_refs = _perception_refs(accessible, actual_action_ref, identity_doc["actor"])
    if not perception_refs:
        return _held_envelope(
            spec_doc, identity_doc,
            reason="ACTOR_PERCEPTION_UNAVAILABLE_FOR_PRESENT_EVENT",
            actual_event_ref=actual_event_ref,
            actual_event_hash=actual_event_hash,
            actual_action_ref=actual_action_ref,
            actual_action_hash=actual_action_hash,
            actual_interval=interval,
            source_hashes=source_hashes,
            native_status=realized_doc["status"],
        )
    if spec_doc["representation_form"] == "ACCUMULATED_INTERVAL":
        if interval is None or interval.get("status") not in POSITIVE_INTERVAL_STATUSES:
            return _held_envelope(
                spec_doc, identity_doc,
                reason="ACTUAL_INTERVAL_UNAVAILABLE",
                actual_event_ref=actual_event_ref,
                actual_event_hash=actual_event_hash,
                actual_action_ref=actual_action_ref,
                actual_action_hash=actual_action_hash,
                actual_interval=interval,
                source_hashes=source_hashes,
                native_status=realized_doc["status"],
            )
    return _bound_envelope(
        spec_doc, identity_doc,
        actual_event_ref=actual_event_ref,
        actual_event_hash=actual_event_hash,
        actual_action_ref=actual_action_ref,
        actual_action_hash=actual_action_hash,
        actual_interval=interval,
        perception_refs=perception_refs,
        source_hashes=source_hashes,
        native_status=realized_doc["status"],
    )


__all__ = ["CompressionRefusal", "preflight", "bind", "FORMS", "FORM_SOURCE_KIND"]
