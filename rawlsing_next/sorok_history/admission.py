"""Pure, bounded admission for candidate historical dependency groups.

This module is deliberately not a world writer and does not import an owner,
session, provider, or psyche store.  It evaluates a packet already bound by the
existing world/foreground adapter against a structured historical candidate and
returns deterministic accepted groups plus typed held/rejected reasons.

Packet schema (``SOROK_HISTORY_ADMISSION_PACKET@1``)
---------------------------------------------------
``request_id``
    Non-empty string.  It must equal the candidate request ID.
``root`` / ``branch`` / ``time``
    Exact current continuity identifiers and integer clock.
``target_ids``
    Non-empty list of target IDs.  Every target has a ``surface`` entry.
``surface``
    Mapping ``target_id -> {"physical": {predicate: scalar},
    "known_fact_refs": [exact_ref], "unresolved": [dimension]}``.  Physical
    values are the already committed visible material surface.
``known_facts``
    List of exact typed facts:
    ``{"ref": exact_ref, "target_id": str, "predicate": str, "value": JSON,
    "state": "KNOWN"|"KNOWN_NEGATIVE"|"UNKNOWN"}``.  ``UNKNOWN`` is not a
    negative fact.
``world_refs`` / ``actor_refs`` / ``event_refs``
    Exact refs available to the candidate.  No new actor or world owner can be
    created by a candidate.
``authority``
    ``{"ref": exact_ref, "root": str, "branch": str, "valid_from": int,
    "valid_to": int, "allowed_H_classes": [H0..H3]}``.  Root/branch/time must
    match the packet and the authority must be current.  A missing or stale
    authority rejects the candidate.
``chronology``
    ``{"time": int, "window": [start, end], "closed_event_refs": [exact_ref],
    "records": [owner_record]}``.  Candidate times must not exceed the bound
    time and must fall in the window.  ``records`` is optional and owner-supplied;
    each record is keyed by its exact event ``ref`` and carries ``time`` plus
    optional ``closed``, ``targets``, scoped ``condition`` and scoped
    ``custody``.  A condition entry is ``{"target_id", "predicate", "value",
    "valid_from", "valid_to"}``; a custody entry is ``{"target_id",
    "custodian_ref", "valid_from", "valid_to"}``.  Existing parents without an
    owner record, a parent after its child, and a closed owner effect are
    held/rejected rather than certified by model prose.
``causal_closure``
    ``{"closed_event_refs": [exact_ref],
    "closed_owner_effect_refs": [exact_ref],
    "allowed_slack_refs": [exact_ref]}``.  Closed owner effects cannot be
    retroactively changed.  H2 needs a reference in ``allowed_slack_refs`` or
    an existing event ref.
``budgets``
    Optional overrides for structural limits.  Invalid or oversized budgets
    reject the whole candidate.

Candidate schema (``SOROK_HISTORY_ADMISSION_CANDIDATE@1``)
---------------------------------------------------------
The candidate has arrays ``facts``, ``occurrences``, ``links`` and
``dependencies`` plus the bound ``request_id``.

Each fact/occurrence/link has an exact ``ref``, a ``dependency_group`` and an
optional ``asserted_H_class``.  Supported claims include:
- fact: ``target_id``, ``predicate``, ``value``, ``effective_time``,
  ``evidence_class``, ``source_refs``;
- occurrence: ``effective_time``, ``place_ref``, ``actor_refs``,
  ``target_ids``, ``action``, ``effects``, ``causal_parents``, ``source_refs``;
- link: ``subject_ref``, ``relation_type``, ``object_ref``,
  ``parent_event_ref``, ``source_refs``.

A dependency group descriptor is
``{"group_id": str, "parent_refs": [exact_ref],
"parent_groups": [group_id], "asserted_H_class": Hx}``.  Every group is
evaluated atomically: one bad claim holds or rejects the whole group.  Parent
refs and dependency groups are closed over packet refs, candidate occurrences,
and accepted parent groups.  Missing parents, cycles, unknown targets/actors,
surface contradictions, closed-effect rewrites, branch/root/time mismatches,
external-verified claims, actor-state creation, unclassified unknown values,
and budget overflow are typed refusals.

H0 is inert physical material; H1 is a constrained objective episode with exact
parents; H2 is a bounded existing causal-slack/source reference; H3 is
formative and is always held for owner/source issuance.  A claim that presents
actor state, memory, belief, capability, practice, attachment, or another
formative effect while declaring H0-H2 is held as ``H_CLASS_UNDERCALLED``.

The result is::

    {"schema": "SOROK_HISTORY_ADMISSION_RESULT@1",
     "request_id": str, "status": "ACCEPTED"|"PARTIAL_HELD"|"REJECTED"|"HELD",
     "accepted_groups": [...], "held": [...], "rejected": [...],
     "held_groups": [...], "rejected_groups": [...]}

``held`` and ``rejected`` entries carry ``group_id``, ``status``, ``reason``,
``refs`` and ``claim_refs``.  The accepted group carries the exact claim refs
and copied accepted claims for the later owner adapter.  Evaluation never
mutates its inputs and never performs I/O.
"""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from typing import Any, Mapping

SCHEMA = "SOROK_HISTORY_ADMISSION_PACKET@1"
CANDIDATE_SCHEMA = "SOROK_HISTORY_ADMISSION_CANDIDATE@1"
RESULT_SCHEMA = "SOROK_HISTORY_ADMISSION_RESULT@1"
H_CLASSES = ("H0", "H1", "H2", "H3")
H_RANK = {name: index for index, name in enumerate(H_CLASSES)}
DEFAULT_BUDGETS = {
    "max_groups": 32,
    "max_facts": 128,
    "max_occurrences": 128,
    "max_links": 128,
    "max_dependencies": 128,
    "max_refs": 512,
    "max_depth": 8,
}
HARD_BUDGETS = {
    "max_groups": 128,
    "max_facts": 512,
    "max_occurrences": 512,
    "max_links": 512,
    "max_dependencies": 512,
    "max_refs": 2048,
    "max_depth": 16,
}
_ACTOR_KEYS = frozenset({
    "actor_state", "actor_private", "psyche", "v3_state", "memory", "belief",
    "capability", "capabilities", "practice", "attachment", "first_person",
    "canonical_actor_state", "can011", "can_011", "adp016", "adp_016",
    "adp017", "adp_017", "relationship", "self_model",
})
_ACTOR_TEXT = (
    "ACTOR_STATE", "ACTOR-PRIVATE", "ACTOR_PRIVATE", "PSYCHE", "MEMORY",
    "BELIEF", "CAPABILITY", "PRACTICE", "ATTACHMENT", "FIRST_PERSON",
    "CAN011", "CAN-011", "ADP016", "ADP-016", "ADP017", "ADP-017",
    "TRAUMA", "APPRENTICESHIP", "CONVERSION", "FAMILY_RESTRUCTURING",
    "REPEATED_PRACTICE", "SELF_MODEL", "FORMATIVE", "MAJOR_LIFE",
    "DEVELOPMENTAL", "IDENTITY",
)
_EXTERNAL_EVIDENCE = frozenset({
    "EXTERNAL_VERIFIED", "VERIFIED_EXTERNAL", "SOURCE_VERIFIED",
    "VERIFIED_SOURCE", "EXTERNAL_FACT",
})
_OWNERSHIP_ACTIONS = frozenset({
    "PURCHASE", "BUY", "ACQUIRE", "OWN", "OWNERSHIP", "GIFT", "GIVE",
    "INHERIT", "TRANSFER", "LEND", "BORROW",
})
_OWNERSHIP_PREDICATES = frozenset({"OWNER", "OWNERSHIP", "POSSESSED_BY", "CUSTODY"})
_CLOSED = "closed"
_SUPPORTED_EFFECTS = frozenset({"NO_CHANGE", "PHYSICAL_CONDITION", "CUSTODY"})


class _InputError(ValueError):
    def __init__(self, code: str, refs: Any = ()) -> None:
        super().__init__(code)
        self.code = code
        self.refs = tuple(refs)


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False, allow_nan=False)


def _digest(value: Any) -> str:
    return hashlib.sha256(_canonical(value).encode("utf-8")).hexdigest()


def _nonempty(value: Any, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise _InputError("INVALID_" + name.upper())
    return value


def _exact_ref(value: Any, name: str = "REF") -> dict[str, str]:
    if not isinstance(value, Mapping):
        raise _InputError("INVALID_" + name.upper())
    if set(value) != {"kind", "object_id", "content_hash"}:
        raise _InputError("INVALID_" + name.upper())
    kind = _nonempty(value.get("kind"), name + "_KIND")
    object_id = _nonempty(value.get("object_id"), name + "_OBJECT_ID")
    content_hash = value.get("content_hash")
    if (not isinstance(content_hash, str) or len(content_hash) != 64
            or any(ch not in "0123456789abcdef" for ch in content_hash)):
        raise _InputError("INVALID_" + name.upper())
    return {"kind": kind, "object_id": object_id, "content_hash": content_hash}


def _ref_key(value: Any, name: str = "REF") -> str:
    ref = _exact_ref(value, name)
    return ref["kind"] + "|" + ref["object_id"] + "|" + ref["content_hash"]


def _refs(value: Any, name: str) -> list[dict[str, str]]:
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise _InputError("INVALID_" + name.upper())
    return [_exact_ref(item, name) for item in value]


def _ref_set(value: Any, name: str) -> set[str]:
    return {_ref_key(item, name) for item in _refs(value, name)}


def _array(candidate: Mapping[str, Any], name: str) -> list[Any]:
    value = candidate.get(name)
    if value is None:
        return []
    if not isinstance(value, (list, tuple)):
        raise _InputError("INVALID_" + name.upper())
    return list(value)


def _claim_ref(claim: Mapping[str, Any], name: str) -> dict[str, str]:
    value = claim.get("ref", claim.get("claim_ref"))
    return _exact_ref(value, name)


def _h_class(value: Any, default: str = "H0") -> str:
    result = value if value is not None else default
    if result not in H_RANK:
        raise _InputError("INVALID_H_CLASS")
    return str(result)


def _actor_impact(value: Any) -> bool:
    if isinstance(value, Mapping):
        for key, item in value.items():
            normalized = str(key).lower()
            if normalized in {k.lower() for k in _ACTOR_KEYS} and item not in (None, False, "", (), [], {}):
                return True
            if isinstance(item, (Mapping, list, tuple)) and _actor_impact(item):
                return True
        return False
    if isinstance(value, (list, tuple)):
        return any(_actor_impact(item) for item in value)
    if isinstance(value, str):
        upper = value.upper()
        return any(token in upper for token in _ACTOR_TEXT)
    return False


def _budgets(packet: Mapping[str, Any]) -> dict[str, int]:
    supplied = packet.get("budgets") or {}
    if not isinstance(supplied, Mapping):
        raise _InputError("INVALID_BUDGETS")
    result = dict(DEFAULT_BUDGETS)
    for name, hard in HARD_BUDGETS.items():
        value = supplied.get(name, result[name])
        if type(value) is not int or value < 1 or value > hard:
            raise _InputError("INVALID_BUDGETS")
        result[name] = value
    return result


def _known_state(value: Any) -> str:
    state = str(value or "KNOWN").upper()
    if state not in {"KNOWN", "KNOWN_NEGATIVE", "UNKNOWN"}:
        raise _InputError("INVALID_KNOWN_FACT_STATE")
    return state


def _prepare_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(packet, Mapping):
        raise _InputError("INVALID_PACKET")
    request_id = _nonempty(packet.get("request_id"), "REQUEST_ID")
    root = _nonempty(packet.get("root"), "ROOT")
    branch = _nonempty(packet.get("branch"), "BRANCH")
    time = packet.get("time")
    if type(time) is not int:
        raise _InputError("INVALID_TIME")
    target_ids = packet.get("target_ids")
    if (not isinstance(target_ids, (list, tuple)) or not target_ids
            or any(not isinstance(item, str) or not item for item in target_ids)
            or len(set(target_ids)) != len(target_ids)):
        raise _InputError("INVALID_TARGET_IDS")
    surface = packet.get("surface")
    if not isinstance(surface, Mapping):
        raise _InputError("INVALID_SURFACE")
    surfaces = {}
    for target_id in target_ids:
        row = surface.get(target_id)
        if not isinstance(row, Mapping):
            raise _InputError("MISSING_SURFACE")
        physical = row.get("physical", {})
        if not isinstance(physical, Mapping) or any(
                not isinstance(key, str) or not key
                or type(value) not in (str, int, bool) for key, value in physical.items()):
            raise _InputError("INVALID_SURFACE")
        known_refs = _ref_set(row.get("known_fact_refs", []), "SURFACE_KNOWN_REF")
        unresolved = row.get("unresolved", [])
        if not isinstance(unresolved, (list, tuple)) or any(
                not isinstance(item, str) or not item for item in unresolved):
            raise _InputError("INVALID_SURFACE")
        surfaces[target_id] = {
            "physical": dict(physical), "known_refs": known_refs,
            "unresolved": list(unresolved),
        }
    known_facts = []
    known_refs = set()
    for item in packet.get("known_facts") or []:
        if not isinstance(item, Mapping):
            raise _InputError("INVALID_KNOWN_FACT")
        ref = _exact_ref(item.get("ref"), "KNOWN_FACT_REF")
        target_id = _nonempty(item.get("target_id"), "KNOWN_TARGET")
        if target_id not in target_ids:
            raise _InputError("UNKNOWN_KNOWN_FACT_TARGET")
        predicate = _nonempty(item.get("predicate"), "KNOWN_PREDICATE")
        known_refs.add(_ref_key(ref, "KNOWN_FACT_REF"))
        known_facts.append({
            "ref": ref, "target_id": target_id, "predicate": predicate,
            "value": item.get("value"), "state": _known_state(item.get("state")),
        })
    world_refs = _ref_set(packet.get("world_refs", []), "WORLD_REF")
    actor_refs = _ref_set(packet.get("actor_refs", []), "ACTOR_REF")
    event_refs = _ref_set(packet.get("event_refs", []), "EVENT_REF")
    chronology = packet.get("chronology") or {}
    if not isinstance(chronology, Mapping):
        raise _InputError("INVALID_CHRONOLOGY")
    chronology_time = chronology.get("time", time)
    if chronology_time != time:
        raise _InputError("CHRONOLOGY_TIME_MISMATCH")
    window = chronology.get("window", [0, time])
    if (not isinstance(window, (list, tuple)) or len(window) != 2
            or any(type(item) is not int for item in window)
            or window[0] > window[1] or time < window[0] or time > window[1]):
        raise _InputError("INVALID_CHRONOLOGY")
    records = chronology.get("records", chronology.get("events", []))
    if not isinstance(records, (list, tuple)):
        raise _InputError("INVALID_CHRONOLOGY")
    chronology_records = {}
    record_conditions = []
    record_custody = []
    record_times = {}
    record_refs = set()
    record_closed = set()
    for item in records:
        if not isinstance(item, Mapping):
            raise _InputError("INVALID_CHRONOLOGY")
        ref = _exact_ref(item.get("ref"), "CHRONOLOGY_REF")
        key = _ref_key(ref, "CHRONOLOGY_REF")
        if key in chronology_records:
            raise _InputError("DUPLICATE_CHRONOLOGY_REF")
        record_time = item.get("time")
        if (type(record_time) is not int or record_time < window[0]
                or record_time > time):
            raise _InputError("INVALID_CHRONOLOGY")
        closed = item.get("closed", False)
        if type(closed) is not bool:
            raise _InputError("INVALID_CHRONOLOGY")
        targets = item.get("targets", [])
        if (not isinstance(targets, (list, tuple))
                or any(target not in target_ids for target in targets)):
            raise _InputError("INVALID_CHRONOLOGY")
        conditions = item.get("condition", item.get("conditions", []))
        if not isinstance(conditions, (list, tuple)):
            raise _InputError("INVALID_CHRONOLOGY")
        for condition in conditions:
            if not isinstance(condition, Mapping):
                raise _InputError("INVALID_CHRONOLOGY")
            target = condition.get("target_id")
            predicate = condition.get("predicate")
            start = condition.get("valid_from")
            end = condition.get("valid_to")
            if (target not in target_ids or not isinstance(predicate, str)
                    or not predicate or type(start) is not int or type(end) is not int
                    or not (start <= end and window[0] <= start and end <= time)):
                raise _InputError("INVALID_CHRONOLOGY")
            record_conditions.append({
                "target_id": target, "predicate": predicate,
                "value": condition.get("value"), "valid_from": start,
                "valid_to": end, "event_ref": ref,
            })
        custody = item.get("custody", [])
        if not isinstance(custody, (list, tuple)):
            raise _InputError("INVALID_CHRONOLOGY")
        for entry in custody:
            if not isinstance(entry, Mapping):
                raise _InputError("INVALID_CHRONOLOGY")
            target = entry.get("target_id")
            custodian = _exact_ref(entry.get("custodian_ref"), "CUSTODIAN_REF")
            start = entry.get("valid_from")
            end = entry.get("valid_to")
            if (target not in target_ids or type(start) is not int or type(end) is not int
                    or not (start <= end and window[0] <= start and end <= time)):
                raise _InputError("INVALID_CHRONOLOGY")
            record_custody.append({
                "target_id": target, "custodian_ref": custodian,
                "custodian_key": _ref_key(custodian, "CUSTODIAN_REF"),
                "valid_from": start, "valid_to": end, "event_ref": ref,
            })
        chronology_records[key] = {
            "ref": ref, "time": record_time, "closed": closed,
            "targets": list(targets),
        }
        record_times[key] = record_time
        record_refs.add(key)
        if closed:
            record_closed.add(key)
    closed_events = _ref_set(chronology.get("closed_event_refs", []), "CLOSED_EVENT_REF")
    closure = packet.get("causal_closure") or {}
    if not isinstance(closure, Mapping):
        raise _InputError("INVALID_CAUSAL_CLOSURE")
    closed_effects = _ref_set(closure.get("closed_owner_effect_refs", []), "CLOSED_EFFECT_REF")
    slack_refs = _ref_set(closure.get("allowed_slack_refs", []), "SLACK_REF")
    closure_events = _ref_set(closure.get("closed_event_refs", []), "CLOSED_EVENT_REF")
    closed_all = closed_events | closed_effects | closure_events | record_closed
    all_event_refs = event_refs | record_refs
    authority = packet.get("authority")
    if not isinstance(authority, Mapping):
        raise _InputError("AUTHORITY_REQUIRED")
    authority_ref = _exact_ref(authority.get("ref"), "AUTHORITY_REF")
    allowed_h = authority.get("allowed_H_classes")
    if (not isinstance(allowed_h, (list, tuple)) or not allowed_h
            or any(item not in H_RANK for item in allowed_h)):
        raise _InputError("INVALID_AUTHORITY")
    for field, wanted in (("root", root), ("branch", branch)):
        if field in authority and authority[field] != wanted:
            raise _InputError("AUTHORITY_SCOPE_MISMATCH")
    valid_from = authority.get("valid_from", 0)
    valid_to = authority.get("valid_to", time)
    if type(valid_from) is not int or type(valid_to) is not int or not (valid_from <= time <= valid_to):
        raise _InputError("AUTHORITY_NOT_CURRENT")
    budgets = _budgets(packet)
    packet_refs = known_refs | world_refs | actor_refs | all_event_refs | closed_all | slack_refs
    packet_refs |= record_refs
    for entry in record_custody:
        packet_refs.add(entry["custodian_key"])
    packet_refs.add(_ref_key(authority_ref, "AUTHORITY_REF"))
    for row in surfaces.values():
        packet_refs |= row["known_refs"]
    return {
        "request_id": request_id, "root": root, "branch": branch, "time": time,
        "window": (window[0], window[1]), "target_ids": set(target_ids),
        "surfaces": surfaces, "known_facts": known_facts,
        "known_refs": known_refs, "world_refs": world_refs,
        "actor_refs": actor_refs, "event_refs": all_event_refs,
        "closed_refs": closed_all, "slack_refs": slack_refs,
        "chronology_records": chronology_records, "record_times": record_times,
        "record_conditions": record_conditions, "record_custody": record_custody,
        "authority_ref": authority_ref, "allowed_H": set(allowed_h),
        "packet_refs": packet_refs, "budgets": budgets,
    }


def _prepare_candidate(candidate: Mapping[str, Any], ctx: Mapping[str, Any]) -> dict[str, Any]:
    if not isinstance(candidate, Mapping):
        raise _InputError("INVALID_CANDIDATE")
    request_id = _nonempty(candidate.get("request_id"), "REQUEST_ID")
    if request_id != ctx["request_id"]:
        raise _InputError("REQUEST_ID_MISMATCH")
    if "root" in candidate and candidate["root"] != ctx["root"]:
        raise _InputError("CANDIDATE_ROOT_MISMATCH")
    if "branch" in candidate and candidate["branch"] != ctx["branch"]:
        raise _InputError("CANDIDATE_BRANCH_MISMATCH")
    arrays = {name: _array(candidate, name) for name in
              ("facts", "occurrences", "links", "dependencies")}
    budgets = ctx["budgets"]
    for name, limit in (("facts", "max_facts"), ("occurrences", "max_occurrences"),
                        ("links", "max_links"), ("dependencies", "max_dependencies")):
        if len(arrays[name]) > budgets[limit]:
            raise _InputError("BUDGET_EXCEEDED")
    claims = []
    groups: dict[str, dict[str, Any]] = {}
    all_claim_refs = set()
    for kind in ("facts", "occurrences", "links"):
        for item in arrays[kind]:
            if not isinstance(item, Mapping):
                raise _InputError("INVALID_" + kind.upper())
            ref = _claim_ref(item, kind.upper())
            ref_key = _ref_key(ref, kind.upper())
            if ref_key in all_claim_refs:
                raise _InputError("DUPLICATE_CLAIM_REF")
            all_claim_refs.add(ref_key)
            group_id = item.get("dependency_group", item.get("group_id", "default"))
            if not isinstance(group_id, str) or not group_id:
                raise _InputError("INVALID_DEPENDENCY_GROUP")
            h = _h_class(item.get("asserted_H_class", item.get("h_class")))
            if ("root" in item and item["root"] != ctx["root"]) or (
                    "branch" in item and item["branch"] != ctx["branch"]):
                raise _InputError("CANDIDATE_SCOPE_MISMATCH")
            claim = {"kind": kind, "ref": ref, "ref_key": ref_key,
                     "group_id": group_id, "h_class": h,
                     "body": deepcopy(dict(item))}
            claims.append(claim)
            groups.setdefault(group_id, {"group_id": group_id, "claims": [],
                                         "parent_refs": [], "parent_groups": [],
                                         "asserted_H_class": h})
            groups[group_id]["claims"].append(claim)
    for item in arrays["dependencies"]:
        if not isinstance(item, Mapping):
            raise _InputError("INVALID_DEPENDENCY_GROUP")
        if set(item) == {"kind", "object_id", "content_hash"}:
            group_id = "default"
            groups.setdefault(group_id, {"group_id": group_id, "claims": [],
                                         "parent_refs": [], "parent_groups": [],
                                         "asserted_H_class": "H0"})
            groups[group_id]["parent_refs"].append(_exact_ref(item, "DEPENDENCY_REF"))
            continue
        group_id = item.get("group_id", item.get("group", item.get("id")))
        if not isinstance(group_id, str) or not group_id:
            raise _InputError("INVALID_DEPENDENCY_GROUP")
        group = groups.setdefault(group_id, {"group_id": group_id, "claims": [],
                                             "parent_refs": [], "parent_groups": [],
                                             "asserted_H_class": _h_class(item.get("asserted_H_class"), "H0")})
        group["parent_refs"].extend(_refs(item.get("parent_refs", []), "DEPENDENCY_REF"))
        parent_groups = item.get("parent_groups", [])
        if (not isinstance(parent_groups, (list, tuple))
                or any(not isinstance(parent, str) or not parent for parent in parent_groups)):
            raise _InputError("INVALID_DEPENDENCY_GROUP")
        group["parent_groups"].extend(parent_groups)
        group["asserted_H_class"] = max(
            (group["asserted_H_class"], _h_class(item.get("asserted_H_class"), "H0")),
            key=lambda value: H_RANK[value])
    for group in groups.values():
        if not group["claims"]:
            raise _InputError("EMPTY_DEPENDENCY_GROUP")
        group["h_class"] = max(
            [group["asserted_H_class"]] + [claim["h_class"] for claim in group["claims"]],
            key=lambda value: H_RANK[value])
    if not groups:
        raise _InputError("NO_GROUPS")
    if len(groups) > budgets["max_groups"]:
        raise _InputError("BUDGET_EXCEEDED")
    depth_cache = {}
    def group_depth(group_id, stack=()):
        if group_id in depth_cache:
            return depth_cache[group_id]
        if group_id in stack:
            raise _InputError("DEPENDENCY_CYCLE")
        parents = tuple(groups[group_id]["parent_groups"])
        value = 1 + max((group_depth(parent, stack + (group_id,))
                         for parent in parents if parent in groups), default=0)
        depth_cache[group_id] = value
        return value
    if any(group_depth(group_id) > budgets["max_depth"] for group_id in groups):
        raise _InputError("BUDGET_EXCEEDED")
    refs = set(all_claim_refs)
    for group in groups.values():
        refs.update(_ref_key(ref, "DEPENDENCY_REF") for ref in group["parent_refs"])
    if len(refs) > budgets["max_refs"]:
        raise _InputError("BUDGET_EXCEEDED")
    return {"request_id": request_id, "groups": groups, "claims": claims,
            "claim_refs": all_claim_refs, "dependencies": arrays["dependencies"]}


def _known_fact_conflict(ctx: Mapping[str, Any], target_id: str, predicate: str,
                         value: Any) -> bool:
    for known in ctx["known_facts"]:
        if (known["target_id"] == target_id and known["predicate"] == predicate
                and known["state"] == "KNOWN"):
            return known["value"] != value
    return False


def _surface_conflict(ctx: Mapping[str, Any], target_id: str, predicate: str,
                      value: Any) -> bool:
    surface = ctx["surfaces"].get(target_id, {}).get("physical", {})
    return predicate in surface and surface[predicate] != value


def _known_negative(ctx: Mapping[str, Any], target_id: str, predicate: str,
                    value: Any) -> bool:
    for known in ctx["known_facts"]:
        if (known["target_id"] == target_id and known["predicate"] == predicate
                and known["state"] == "KNOWN_NEGATIVE"
                and known["value"] != value):
            return True
    return False


def _known_owner_conflict(ctx: Mapping[str, Any], target_id: str,
                          claim: Mapping[str, Any]) -> bool:
    action = str(claim.get("action") or claim.get("relation_type") or "").upper()
    if action not in _OWNERSHIP_ACTIONS and not any(
            str(key).upper() in _OWNERSHIP_PREDICATES for key in claim
            if key in {"predicate", "relation_type"}):
        return False
    value = claim.get("value", claim.get("object_ref", claim.get("owner_ref")))
    for known in ctx["known_facts"]:
        if known["target_id"] != target_id:
            continue
        if str(known["predicate"]).upper() not in _OWNERSHIP_PREDICATES:
            continue
        if known["state"] == "KNOWN_NEGATIVE":
            return True
        if known["state"] == "KNOWN" and known["value"] != value:
            return True
    return False


def _source_refs_ok(ctx: Mapping[str, Any], refs: Any) -> bool:
    return all(_ref_key(ref, "SOURCE_REF") in ctx["packet_refs"]
               for ref in _refs(refs, "SOURCE_REF"))


def _validate_fact(ctx: Mapping[str, Any], claim: Mapping[str, Any],
                   occurrence_refs: set[str]) -> str | None:
    body = claim["body"]
    target_id = body.get("target_id")
    if target_id not in ctx["target_ids"]:
        return "UNKNOWN_TARGET"
    predicate = body.get("predicate")
    if not isinstance(predicate, str) or not predicate:
        return "INVALID_FACT"
    value = body.get("value")
    if value is None or (isinstance(value, str) and value.upper() in {
            "UNKNOWN", "UNRESOLVED", "UNKNOWN_UNRESOLVED"}):
        return "UNKNOWN_NOT_FACT"
    evidence = str(body.get("evidence_class", "GENERAL_PRIOR")).upper()
    if evidence in _EXTERNAL_EVIDENCE:
        return "EXTERNAL_FACT_NOT_ADMITTED"
    if _known_fact_conflict(ctx, target_id, predicate, value):
        return "KNOWN_FACT_CONFLICT"
    if _surface_conflict(ctx, target_id, predicate, value):
        return "SURFACE_CONTRADICTION"
    if _known_negative(ctx, target_id, predicate, value):
        return "KNOWN_NEGATIVE_CONFLICT"
    if _known_owner_conflict(ctx, target_id, body):
        return "OWNERSHIP_CONFLICT"
    effective_time = body.get("effective_time")
    if effective_time is not None:
        if type(effective_time) is not int:
            return "INVALID_EFFECTIVE_TIME"
        if effective_time > ctx["time"] or not (ctx["window"][0] <= effective_time <= ctx["window"][1]):
            return "FUTURE_FACT"
    if not _source_refs_ok(ctx, body.get("source_refs", [])):
        return "EXTERNAL_REF_NOT_ADMITTED"
    if claim["h_class"] != "H3" and _actor_impact(body):
        return "H_CLASS_UNDERCALLED"
    return None


def _active_condition(ctx: Mapping[str, Any], target_id: str, predicate: str,
                      when: int) -> Mapping[str, Any] | None:
    for row in ctx["record_conditions"]:
        if (row["target_id"] == target_id and row["predicate"] == predicate
                and row["valid_from"] <= when <= row["valid_to"]):
            return row
    return None


def _active_custody(ctx: Mapping[str, Any], target_id: str,
                    when: int) -> Mapping[str, Any] | None:
    for row in ctx["record_custody"]:
        if (row["target_id"] == target_id
                and row["valid_from"] <= when <= row["valid_to"]):
            return row
    return None


def _validate_effects(ctx: Mapping[str, Any], body: Mapping[str, Any],
                      targets: list[str], when: int) -> str | None:
    effects = body.get("effects", [])
    if not isinstance(effects, (list, tuple)):
        return "INVALID_EFFECT"
    for effect in effects:
        if not isinstance(effect, Mapping):
            return "INVALID_EFFECT"
        kind = str(effect.get("kind", "")).upper()
        if kind == "NO_CHANGE":
            continue
        if kind == "PHYSICAL_CONDITION":
            target = effect.get("target_id")
            predicate = effect.get("predicate")
            if (target not in targets or not isinstance(predicate, str)
                    or not predicate or "value" not in effect):
                return "INVALID_EFFECT"
            active = _active_condition(ctx, target, predicate, when)
            if active is None:
                return "OWNER_MATERIAL_REQUIRED"
            if active["value"] != effect["value"]:
                return "IMPOSSIBLE_STATE_TRANSITION"
            continue
        if kind == "CUSTODY":
            target = effect.get("target_id")
            if target not in targets:
                return "INVALID_EFFECT"
            try:
                custodian_key = _ref_key(effect.get("custodian_ref"), "CUSTODIAN_REF")
            except _InputError:
                return "INVALID_EFFECT"
            active = _active_custody(ctx, target, when)
            if active is None:
                return "OWNER_MATERIAL_REQUIRED"
            if active["custodian_key"] != custodian_key:
                return "CONTRADICTORY_CUSTODY"
            continue
        return "UNSUPPORTED_EFFECT"
    return None


def _validate_occurrence(ctx: Mapping[str, Any], claim: Mapping[str, Any],
                         occurrence_refs: set[str],
                         occurrence_times: Mapping[str, int]) -> str | None:
    body = claim["body"]
    effective_time = body.get("effective_time", body.get("time"))
    if type(effective_time) is not int or effective_time > ctx["time"] or not (
            ctx["window"][0] <= effective_time <= ctx["window"][1]):
        return "FUTURE_FACT"
    targets = body.get("target_ids", [])
    if (not isinstance(targets, (list, tuple))
            or any(target not in ctx["target_ids"] for target in targets)):
        return "UNKNOWN_TARGET"
    place = body.get("place_ref")
    if place is not None and _ref_key(place, "PLACE_REF") not in ctx["packet_refs"]:
        return "EXTERNAL_REF_NOT_ADMITTED"
    actors = body.get("actor_refs", [])
    if any(_ref_key(ref, "ACTOR_REF") not in ctx["actor_refs"] for ref in _refs(actors, "ACTOR_REF")):
        return "UNKNOWN_ACTOR"
    parents = _refs(body.get("causal_parents", body.get("parent_refs", [])), "PARENT_REF")
    for parent in parents:
        key = _ref_key(parent, "PARENT_REF")
        if key not in ctx["packet_refs"] and key not in occurrence_refs:
            return "MISSING_PARENT"
        if key in ctx["closed_refs"]:
            return "CLOSED_OWNER_EFFECT"
        if key in occurrence_refs:
            parent_time = occurrence_times.get(key)
            if parent_time is None:
                return "OWNER_MATERIAL_REQUIRED"
        else:
            parent_time = ctx["record_times"].get(key)
            if parent_time is None:
                return "OWNER_MATERIAL_REQUIRED"
        if parent_time > effective_time:
            return "PARENT_AFTER_CHILD"
    if not _source_refs_ok(ctx, body.get("source_refs", [])):
        return "EXTERNAL_REF_NOT_ADMITTED"
    action = str(body.get("action", "")).upper()
    if action in _OWNERSHIP_ACTIONS and any(
            _known_owner_conflict(ctx, target, body) for target in targets):
        return "OWNERSHIP_CONFLICT"
    if claim["h_class"] != "H3" and _actor_impact(body.get("effects", body)):
        return "H_CLASS_UNDERCALLED"
    return _validate_effects(ctx, body, targets, effective_time)


def _validate_link(ctx: Mapping[str, Any], claim: Mapping[str, Any],
                   occurrence_refs: set[str]) -> str | None:
    body = claim["body"]
    for name in ("subject_ref", "object_ref"):
        try:
            key = _ref_key(body.get(name), name.upper())
        except _InputError:
            return "INVALID_LINK_REF"
        if key not in ctx["packet_refs"] and key not in occurrence_refs:
            return "MISSING_PARENT"
    parent = body.get("parent_event_ref")
    if parent is None:
        return "MISSING_PARENT"
    parent_key = _ref_key(parent, "PARENT_EVENT_REF")
    if parent_key not in ctx["event_refs"] and parent_key not in occurrence_refs:
        return "MISSING_PARENT"
    if parent_key in ctx["closed_refs"]:
        return "CLOSED_OWNER_EFFECT"
    if not _source_refs_ok(ctx, body.get("source_refs", [])):
        return "EXTERNAL_REF_NOT_ADMITTED"
    if claim["h_class"] != "H3" and _actor_impact(body):
        return "H_CLASS_UNDERCALLED"
    return None


def _group_error(code: str, group: Mapping[str, Any]) -> str:
    if code in {"H3_HELD", "H_CLASS_NOT_ALLOWED", "H2_SOURCE_REF_REQUIRED",
                "UNKNOWN_NOT_FACT", "H_CLASS_UNDERCALLED",
                "OWNER_MATERIAL_REQUIRED", "UNSUPPORTED_EFFECT"}:
        return "HELD"
    return "REJECTED"


def _result(request_id: Any, status: str, accepted: list[dict[str, Any]],
            held: list[dict[str, Any]], rejected: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema": RESULT_SCHEMA, "request_id": request_id, "status": status,
        "accepted_groups": accepted,
        "held": held, "rejected": rejected,
        "held_groups": held, "rejected_groups": rejected,
        "result_digest": _digest({"accepted": accepted, "held": held,
                                  "rejected": rejected}),
    }


def _own_occurrence_refs(group: Mapping[str, Any]) -> set[str]:
    return {claim["ref_key"] for claim in group["claims"] if claim["kind"] == "occurrences"}


def _visible_occurrence_refs(group: Mapping[str, Any],
                             accepted_occurrences: Mapping[str, set[str]]) -> set[str]:
    visible = _own_occurrence_refs(group)
    for parent in group["parent_groups"]:
        visible |= accepted_occurrences.get(parent, set())
    return visible


def _occurrence_cycle(group: Mapping[str, Any]) -> bool:
    own = _own_occurrence_refs(group)
    edges = {}
    for claim in group["claims"]:
        if claim["kind"] != "occurrences":
            continue
        body = claim["body"]
        parents = _refs(body.get("causal_parents", body.get("parent_refs", [])), "PARENT_REF")
        edges[claim["ref_key"]] = {_ref_key(parent, "PARENT_REF") for parent in parents
                                   if _ref_key(parent, "PARENT_REF") in own}
    visiting = set()
    done = set()
    def visit(node):
        if node in visiting:
            return True
        if node in done:
            return False
        visiting.add(node)
        if any(visit(child) for child in edges.get(node, ())):
            return True
        visiting.remove(node)
        done.add(node)
        return False
    return any(visit(node) for node in edges)


def _evaluate_group(ctx: Mapping[str, Any], candidate: Mapping[str, Any],
                    group: Mapping[str, Any], occurrence_refs: set[str],
                    occurrence_times: Mapping[str, int],
                    accepted_parents: set[str]) -> tuple[str, str | None, list[dict[str, str]]]:
    refs = [claim["ref"] for claim in group["claims"]]
    refs.extend(group["parent_refs"])
    for parent_group in group["parent_groups"]:
        if parent_group not in candidate["groups"]:
            return "REJECTED", "MISSING_PARENT_GROUP", refs
        if parent_group not in accepted_parents:
            return "HELD", "PARENT_GROUP_HELD", refs
    for ref in group["parent_refs"]:
        key = _ref_key(ref, "DEPENDENCY_REF")
        if key not in ctx["packet_refs"] and key not in occurrence_refs:
            return "REJECTED", "MISSING_PARENT", refs
        if key in ctx["closed_refs"]:
            return "REJECTED", "CLOSED_OWNER_EFFECT", refs
    h_class = group["h_class"]
    if h_class == "H3":
        return "HELD", "H3_HELD", refs
    if h_class not in ctx["allowed_H"]:
        return "HELD", "H_CLASS_NOT_ALLOWED", refs
    if h_class == "H2":
        group_refs = {_ref_key(ref, "DEPENDENCY_REF") for ref in group["parent_refs"]}
        if not (group_refs & ctx["slack_refs"] or group_refs & ctx["event_refs"]):
            return "HELD", "H2_SOURCE_REF_REQUIRED", refs
    if _occurrence_cycle(group):
        return "REJECTED", "DEPENDENCY_CYCLE", refs
    issues = []
    local_facts = {}
    for claim in group["claims"]:
        if claim["kind"] == "facts":
            body = claim["body"]
            key = (body.get("target_id"), body.get("predicate"))
            if key in local_facts and local_facts[key] != body.get("value"):
                issue = "KNOWN_FACT_CONFLICT"
            else:
                issue = _validate_fact(ctx, claim, occurrence_refs)
                if issue is None:
                    local_facts[key] = body.get("value")
        elif claim["kind"] == "occurrences":
            issue = _validate_occurrence(ctx, claim, occurrence_refs, occurrence_times)
        else:
            issue = _validate_link(ctx, claim, occurrence_refs)
        if issue:
            issues.append((_group_error(issue, group), issue, claim["ref"]))
    if issues:
        status = "HELD" if all(item[0] == "HELD" for item in issues) else "REJECTED"
        return status, issues[0][1], [item[2] for item in issues]
    return "ACCEPTED", None, refs


def evaluate(packet: dict, candidate: dict) -> dict:
    """Evaluate candidate dependency groups without any world or model effect."""
    try:
        ctx = _prepare_packet(packet)
    except _InputError as exc:
        return _result(None, "REJECTED", [], [], [
            {"group_id": None, "status": "REJECTED", "reason": exc.code,
             "refs": [], "claim_refs": []}])
    try:
        prepared = _prepare_candidate(candidate, ctx)
    except _InputError as exc:
        return _result(ctx["request_id"], "REJECTED", [], [], [
            {"group_id": None, "status": "REJECTED", "reason": exc.code,
             "refs": [], "claim_refs": []}])
    groups = prepared["groups"]
    accepted: list[dict[str, Any]] = []
    held: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    accepted_parents: set[str] = set()
    accepted_occurrences: dict[str, set[str]] = {}
    occurrence_times = {
        claim["ref_key"]: claim["body"].get("effective_time", claim["body"].get("time"))
        for claim in prepared["claims"] if claim["kind"] == "occurrences"
    }
    pending = set(groups)
    while pending:
        progressed = False
        for group_id in sorted(pending):
            group = groups[group_id]
            parents = set(group["parent_groups"])
            if parents & pending:
                continue
            progressed = True
            pending.remove(group_id)
            visible_occurrences = _visible_occurrence_refs(group, accepted_occurrences)
            try:
                status, reason, refs = _evaluate_group(
                    ctx, prepared, group, visible_occurrences, occurrence_times,
                    accepted_parents)
            except _InputError as exc:
                status, reason, refs = "REJECTED", exc.code, [claim["ref"] for claim in group["claims"]]
            record = {
                "group_id": group_id, "status": status, "reason": reason,
                "asserted_H_class": group["h_class"],
                "refs": sorted(refs, key=_ref_key),
                "claim_refs": sorted((claim["ref_key"] for claim in group["claims"])),
            }
            if status == "ACCEPTED":
                record["claims"] = deepcopy([
                    {**claim["body"], "kind": claim["kind"], "ref": claim["ref"]}
                    for claim in group["claims"]])
                record["parent_refs"] = deepcopy(group["parent_refs"])
                record["parent_groups"] = list(group["parent_groups"])
                accepted.append(record)
                accepted_parents.add(group_id)
                accepted_occurrences[group_id] = _visible_occurrence_refs(
                    group, accepted_occurrences)
                for claim in group["claims"]:
                    if claim["kind"] == "facts":
                        body = claim["body"]
                        ctx["known_facts"].append({
                            "ref": claim["ref"], "target_id": body.get("target_id"),
                            "predicate": body.get("predicate"),
                            "value": body.get("value"), "state": "KNOWN",
                        })
            elif status == "HELD":
                record["reason"] = reason or "HELD"
                held.append(record)
            else:
                record["reason"] = reason or "REJECTED"
                rejected.append(record)
        if not progressed:
            for group_id in sorted(pending):
                group = groups[group_id]
                rejected.append({
                    "group_id": group_id, "status": "REJECTED",
                    "reason": "DEPENDENCY_CYCLE",
                    "asserted_H_class": group["h_class"],
                    "refs": sorted([claim["ref"] for claim in group["claims"]],
                                   key=_ref_key),
                    "claim_refs": sorted(claim["ref_key"] for claim in group["claims"]),
                })
            pending.clear()
    accepted.sort(key=lambda row: row["group_id"])
    held.sort(key=lambda row: row["group_id"])
    rejected.sort(key=lambda row: row["group_id"])
    if accepted and not held and not rejected:
        status = "ACCEPTED"
    elif accepted:
        status = "PARTIAL_HELD"
    elif held and not rejected:
        status = "HELD"
    else:
        status = "REJECTED"
    return _result(ctx["request_id"], status, accepted, held, rejected)


__all__ = ["evaluate", "SCHEMA", "CANDIDATE_SCHEMA", "RESULT_SCHEMA",
           "H_CLASSES", "DEFAULT_BUDGETS", "HARD_BUDGETS"]
