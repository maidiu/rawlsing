"""Normalized, indexed, immutable P3 psychological sidecar storage.

This module is mechanical.  It does not evaluate CAN/ADP rules, choose responses,
issue native science or write the P2 world.  It stores source/rule/actor-bound
records and a durable cross-store operation protocol for the HQ-owned P3Owner.

The base API is the one frozen in INTEGRATION_CONTRACT.md:
PsycheStore, head, query, get_operation, pending, reserve, save_world,
commit_effects, finish and close. ``completed()`` is an additive read-only
listing used by the D01 cold provenance anchor; it does not alter the frozen
protocol.
"""
from __future__ import annotations

from contextlib import contextmanager
import hashlib
import json
import math
import os
from pathlib import Path
import sqlite3
import threading
from typing import Any, Mapping

try:  # Reuse the accepted shared convention when the #704 package is importable.
    from developmental_recursion.contracts import RecursionRefusal, canonical, digest
except ImportError:  # Standalone namespace-package use; ValueError remains convertible.

    class RecursionRefusal(ValueError):
        pass

    def canonical(value: Any) -> str:
        return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False)

    def digest(value: Any) -> str:
        return hashlib.sha256(canonical(value).encode("utf-8")).hexdigest()


SCHEMA = "SOROK_P3_PSYCHE_STORE@1"
PHASE_PREPARED = "PREPARED"
PHASE_WORLD = "WORLD_COMMITTED"
PHASE_PSYCH = "PSYCH_COMMITTED"
PHASE_COMPLETE = "COMPLETE"
PHASES = frozenset({PHASE_PREPARED, PHASE_WORLD, PHASE_PSYCH, PHASE_COMPLETE})
UNRESOLVED_PHASES = (PHASE_PREPARED, PHASE_WORLD, PHASE_PSYCH)
CORE_STATUSES = frozenset(
    {"REALIZED", "IMMEDIATE_ONLY", "NO_CHANGE", "HELD", "REFUSED", "OMITTED"}
)
KINDS = frozenset(
    {
        "MEDIATOR",
        "TENSION",
        "PRACTICE",
        "V3MS_MEDIATOR",
        "V3MS_TENSION",
        "V3MS_PRACTICE",
    }
)
STATE_KEYS = frozenset({"root", "actor", "branch", "clock", "state_hash"})
HEAD_KEYS = frozenset({"hash", "count"})
RECORD_REQUIRED = frozenset(
    {
        "root",
        "actor",
        "branch",
        "project",
        "counterpart",
        "record_id",
        "kind",
        "payload",
        "rule_id",
        "rule_version",
        "rule_hash",
        "registry_hash",
        "source_hash",
        "effective_from",
        "causal_parents",
        "grade",
    }
)
RECORD_OPTIONAL = frozenset({"hash", "operation"})
RULE_KEYS = frozenset({"rule_id", "rule_version", "rule_hash"})
RESULT_KEYS = frozenset(
    {
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
)
MAX_JSON_DEPTH = 100

RECORD_COLUMNS = (
    "seq",
    "record_id",
    "root",
    "actor",
    "branch",
    "project",
    "counterpart",
    "kind",
    "payload_json",
    "rule_id",
    "rule_version_json",
    "rule_hash",
    "registry_hash",
    "source_hash",
    "effective_from",
    "causal_parents_json",
    "grade",
    "hash",
    "record_json",
    "previous_chain",
    "chain_hash",
    "operation_id",
)
RECORD_COLUMNS_SQL = ",".join(RECORD_COLUMNS)
RECORDS_TABLE_DDL = (
    "CREATE TABLE IF NOT EXISTS p3_records ("
    "seq INTEGER PRIMARY KEY AUTOINCREMENT,"
    "record_id TEXT NOT NULL UNIQUE,"
    "root TEXT NOT NULL,"
    "actor TEXT NOT NULL,"
    "branch TEXT NOT NULL,"
    "project TEXT,"
    "counterpart TEXT,"
    "kind TEXT NOT NULL CHECK(kind IN "
    "('MEDIATOR','TENSION','PRACTICE',"
    "'V3MS_MEDIATOR','V3MS_TENSION','V3MS_PRACTICE')),"
    "payload_json TEXT NOT NULL,"
    "rule_id TEXT NOT NULL,"
    "rule_version_json TEXT NOT NULL,"
    "rule_hash TEXT NOT NULL,"
    "registry_hash TEXT NOT NULL,"
    "source_hash TEXT NOT NULL,"
    "effective_from INTEGER NOT NULL,"
    "causal_parents_json TEXT NOT NULL,"
    "grade TEXT NOT NULL,"
    "hash TEXT NOT NULL UNIQUE,"
    "record_json TEXT NOT NULL,"
    "previous_chain TEXT NOT NULL,"
    "chain_hash TEXT NOT NULL UNIQUE,"
    "operation_id TEXT NOT NULL)"
)
RECORDS_SCOPE_INDEX_DDL = (
    "CREATE INDEX IF NOT EXISTS p3_records_scope "
    "ON p3_records(root, actor, branch, project, counterpart, "
    "effective_from, seq)"
)
RECORDS_KIND_INDEX_DDL = (
    "CREATE INDEX IF NOT EXISTS p3_records_kind "
    "ON p3_records(root, actor, branch, kind, effective_from, seq)"
)


def _text(value: Any, code: str) -> str:
    if not isinstance(value, str) or not value or not value.strip():
        raise RecursionRefusal(code)
    return value


def _clock(value: Any, code: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int):
        raise RecursionRefusal(code)
    if value < 0 or value > (1 << 63) - 1:
        raise RecursionRefusal(code)
    return value


def _json_value(value: Any, code: str, depth: int = 0) -> Any:
    if depth > MAX_JSON_DEPTH:
        raise RecursionRefusal(code + ":DEPTH")
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        if not math.isfinite(value):
            raise RecursionRefusal(code + ":NONFINITE")
        return value
    if isinstance(value, Mapping):
        result = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise RecursionRefusal(code + ":NONSTRING_KEY")
            result[key] = _json_value(item, code, depth + 1)
        return result
    if isinstance(value, (list, tuple)):
        return [_json_value(item, code, depth + 1) for item in value]
    raise RecursionRefusal(code + ":NOT_JSON")


def _json_mapping(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping):
        raise RecursionRefusal(code + ":NOT_OBJECT")
    return _json_value(value, code)


def _load_json_text(value: Any, code: str) -> Any:
    try:
        return json.loads(value)
    except (TypeError, ValueError) as exc:
        raise RecursionRefusal(code + ":JSON") from exc


def _detached(value: Any) -> Any:
    return json.loads(canonical(value))


def _state_document(value: Any, code: str) -> dict:
    if not isinstance(value, Mapping) or set(value) != STATE_KEYS:
        raise RecursionRefusal(code + ":SCHEMA")
    root = _text(value["root"], code + ":ROOT")
    actor = _text(value["actor"], code + ":ACTOR")
    branch = _text(value["branch"], code + ":BRANCH")
    clock = _clock(value["clock"], code + ":CLOCK")
    state_hash = _text(value["state_hash"], code + ":STATE_HASH")
    return {
        "root": root,
        "actor": actor,
        "branch": branch,
        "clock": clock,
        "state_hash": state_hash,
    }


def _rule_version(value: Any, code: str) -> str | int:
    if isinstance(value, bool):
        raise RecursionRefusal(code)
    if isinstance(value, int):
        return value
    return _text(value, code)


def _scope_value(value: Any, code: str) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    raise RecursionRefusal(code)


def _head_input(value: Any, code: str) -> dict | str:
    if isinstance(value, str):
        return _text(value, code)
    if isinstance(value, Mapping):
        if set(value) != HEAD_KEYS:
            raise RecursionRefusal(code + ":SCHEMA")
        return {
            "hash": _text(value["hash"], code + ":HASH"),
            "count": _clock(value["count"], code + ":COUNT"),
        }
    raise RecursionRefusal(code)


def _head_matches(value: dict | str, head: Mapping[str, Any]) -> bool:
    if isinstance(value, str):
        return value == head["hash"]
    return value["hash"] == head["hash"] and value["count"] == head["count"]


def _plan_identity(plan: Mapping[str, Any]) -> tuple[str, str, str] | None:
    nested = plan.get("identity")
    top = None
    if any(key in plan for key in ("root", "actor", "branch")):
        top = (plan.get("root"), plan.get("actor"), plan.get("branch"))
        if not all(isinstance(item, str) and item.strip() for item in top):
            raise RecursionRefusal("PLAN_IDENTITY_INVALID")
        top = (top[0], top[1], top[2])
    if nested is not None:
        if not isinstance(nested, Mapping):
            raise RecursionRefusal("PLAN_IDENTITY_INVALID")
        nested_identity = (
            nested.get("root"), nested.get("actor"), nested.get("branch")
        )
        if not all(isinstance(item, str) and item.strip() for item in nested_identity):
            raise RecursionRefusal("PLAN_IDENTITY_INVALID")
        nested_identity = (
            nested_identity[0], nested_identity[1], nested_identity[2]
        )
        if top is not None and top != nested_identity:
            raise RecursionRefusal("PLAN_IDENTITY_CONFLICT")
        return nested_identity
    return top


def _plan_source(plan: Mapping[str, Any]) -> str | None:
    candidates = []
    if "source_hash" in plan:
        candidates.append(_text(plan["source_hash"], "PLAN_SOURCE_HASH_INVALID"))
    if "source" in plan:
        source = plan["source"]
        if isinstance(source, str):
            candidates.append(_text(source, "PLAN_SOURCE_HASH_INVALID"))
        elif isinstance(source, Mapping):
            for key in ("hash", "source_hash"):
                if key in source:
                    candidates.append(_text(source[key], "PLAN_SOURCE_HASH_INVALID"))
            if not candidates:
                raise RecursionRefusal("PLAN_SOURCE_HASH_INVALID")
        else:
            raise RecursionRefusal("PLAN_SOURCE_HASH_INVALID")
    if "source_binding" in plan:
        source = plan["source_binding"]
        if isinstance(source, str):
            candidates.append(_text(source, "PLAN_SOURCE_HASH_INVALID"))
        elif isinstance(source, Mapping):
            for key in ("hash", "source_hash"):
                if key in source:
                    candidates.append(_text(source[key], "PLAN_SOURCE_HASH_INVALID"))
            if not any(key in source for key in ("hash", "source_hash")):
                raise RecursionRefusal("PLAN_SOURCE_HASH_INVALID")
        else:
            raise RecursionRefusal("PLAN_SOURCE_HASH_INVALID")
    if not candidates:
        return None
    if len(set(candidates)) != 1:
        raise RecursionRefusal("PLAN_SOURCE_HASH_CONFLICT")
    return candidates[0]


def _plan_authority(plan: Mapping[str, Any]) -> tuple[str, str]:
    provenance = plan.get("provenance")
    authority_values = []
    grade_values = []
    for source in (plan, provenance):
        if not isinstance(source, Mapping):
            continue
        if "authority" in source:
            authority_values.append(_text(source["authority"], "PLAN_AUTHORITY_INVALID"))
        if "grade" in source:
            grade_values.append(_text(source["grade"], "PLAN_GRADE_INVALID"))
    if not grade_values:
        raise RecursionRefusal("PLAN_AUTHORITY_OR_GRADE_MISSING")
    if len(set(authority_values)) > 1 or len(set(grade_values)) != 1:
        raise RecursionRefusal("PLAN_AUTHORITY_OR_GRADE_CONFLICT")
    grade = grade_values[0]
    explicit_authority = authority_values[0] if authority_values else None

    def is_test_only(value: str) -> bool:
        return value == "SOURCEFREE_TEST_ONLY" or value.startswith("TEST_ONLY")

    if not is_test_only(grade):
        raise RecursionRefusal("PLAN_GRADE_DENIED")
    if explicit_authority is None and grade != "SOURCEFREE_TEST_ONLY":
        raise RecursionRefusal("PLAN_AUTHORITY_OR_GRADE_MISSING")
    if explicit_authority is not None and not explicit_authority.startswith("TEST_ONLY"):
        raise RecursionRefusal("PLAN_AUTHORITY_DENIED")

    for source in (plan, provenance):
        if not isinstance(source, Mapping):
            continue
        for key in (
            "production",
            "native",
            "native_science",
            "source_native",
            "human_validity",
        ):
            value = source.get(key)
            if value is True:
                raise RecursionRefusal("PLAN_PRODUCTION_OR_NATIVE_DENIED")
            if isinstance(value, str) and value.upper() in {
                "TRUE", "PRODUCTION", "ISSUED", "NATIVE", "ACCEPTED"
            }:
                raise RecursionRefusal("PLAN_PRODUCTION_OR_NATIVE_DENIED")
    # Exact frozen SOURCEFREE_TEST_ONLY grade is the existing explicit TEST_ONLY
    # provenance when no conflicting authority is supplied. Legacy
    # TEST_ONLY-prefixed mechanical plans remain supported. The stored plan is
    # not rewritten and no authority field is added to it.
    return "TEST_ONLY", grade


def _plan_rules(plan: Mapping[str, Any]) -> tuple[list[dict], set[str]]:
    rules = plan.get("permitted_rules")
    if not isinstance(rules, (list, tuple)):
        raise RecursionRefusal("PLAN_PERMITTED_RULES_INVALID")
    normalized = []
    keys = set()
    for item in rules:
        if not isinstance(item, Mapping) or set(item) != RULE_KEYS:
            raise RecursionRefusal("PLAN_RULE_DESCRIPTOR_INVALID")
        descriptor = {
            "rule_id": _text(item["rule_id"], "PLAN_RULE_ID_INVALID"),
            "rule_version": _rule_version(
                item["rule_version"], "PLAN_RULE_VERSION_INVALID"
            ),
            "rule_hash": _text(item["rule_hash"], "PLAN_RULE_HASH_INVALID"),
        }
        key = canonical(
            [descriptor["rule_id"], descriptor["rule_version"], descriptor["rule_hash"]]
        )
        if key in keys:
            raise RecursionRefusal("PLAN_DUPLICATE_RULE")
        keys.add(key)
        normalized.append(descriptor)
    return normalized, keys


def _plan_view(
    plan: Any,
    *,
    plan_hash: str,
    binding: tuple[str, str, str],
    registry_hash: str,
    source_hash: str,
) -> dict:
    plan = _json_mapping(plan, "PLAN_INVALID")
    plan_hash = _text(plan_hash, "PLAN_HASH_REQUIRED")
    identity = _plan_identity(plan)
    if identity is None:
        raise RecursionRefusal("PLAN_EXPECTED_IDENTITY_MISSING")
    if identity != binding:
        raise RecursionRefusal("PLAN_IDENTITY_MISMATCH")
    source = _plan_source(plan)
    if source is None:
        raise RecursionRefusal("PLAN_SOURCE_BINDING_MISSING")
    if source != source_hash:
        raise RecursionRefusal("PLAN_SOURCE_MISMATCH")
    authority, grade = _plan_authority(plan)
    rules, keys = _plan_rules(plan)
    return {
        "plan": _detached(plan),
        "plan_hash": plan_hash,
        "authority": authority,
        "grade": grade,
        "rules": rules,
        "rule_keys": keys,
    }


def _record_body(
    record: Any,
    *,
    plan_view: Mapping[str, Any],
    binding: tuple[str, str, str],
    registry_hash: str,
    source_hash: str,
    event_binding: Mapping[str, Any],
) -> dict:
    value = _json_mapping(record, "RECORD_INVALID")
    if set(value) - (RECORD_REQUIRED | RECORD_OPTIONAL):
        raise RecursionRefusal("RECORD_SCHEMA:EXTRA_FIELD")
    if RECORD_REQUIRED - set(value):
        raise RecursionRefusal("RECORD_SCHEMA:MISSING_FIELD")
    operation = value.get("operation", "CREATE")
    if operation != "CREATE":
        raise RecursionRefusal("RECORD_OPERATION_NOT_CREATE")
    root = _text(value["root"], "RECORD_ROOT_INVALID")
    actor = _text(value["actor"], "RECORD_ACTOR_INVALID")
    branch = _text(value["branch"], "RECORD_BRANCH_INVALID")
    if (root, actor, branch) != binding:
        raise RecursionRefusal("RECORD_IDENTITY_MISMATCH")
    project = _scope_value(value["project"], "RECORD_PROJECT_INVALID")
    counterpart = _scope_value(value["counterpart"], "RECORD_COUNTERPART_INVALID")
    record_id = _text(value["record_id"], "RECORD_ID_INVALID")
    kind = _text(value["kind"], "RECORD_KIND_INVALID")
    if kind not in KINDS:
        raise RecursionRefusal("RECORD_KIND_INVALID")
    payload = _json_mapping(value["payload"], "RECORD_PAYLOAD_INVALID")
    rule_id = _text(value["rule_id"], "RECORD_RULE_ID_INVALID")
    rule_version = _rule_version(value["rule_version"], "RECORD_RULE_VERSION_INVALID")
    rule_hash = _text(value["rule_hash"], "RECORD_RULE_HASH_INVALID")
    if canonical([rule_id, rule_version, rule_hash]) not in plan_view["rule_keys"]:
        raise RecursionRefusal("RECORD_RULE_NOT_PERMITTED")
    if _text(value["registry_hash"], "RECORD_REGISTRY_INVALID") != registry_hash:
        raise RecursionRefusal("RECORD_REGISTRY_MISMATCH")
    if _text(value["source_hash"], "RECORD_SOURCE_INVALID") != source_hash:
        raise RecursionRefusal("RECORD_SOURCE_MISMATCH")
    effective_from = _clock(value["effective_from"], "RECORD_EFFECTIVE_FROM_INVALID")
    if effective_from != event_binding["clock"]:
        raise RecursionRefusal("RECORD_EFFECTIVE_TIME_MISMATCH")
    parents = value["causal_parents"]
    if not isinstance(parents, (list, tuple)):
        raise RecursionRefusal("RECORD_CAUSAL_PARENTS_INVALID")
    causal_parents = []
    for parent in parents:
        causal_parents.append(_text(parent, "RECORD_CAUSAL_PARENT_INVALID"))
    if causal_parents and event_binding["event_hash"] not in causal_parents:
        raise RecursionRefusal("RECORD_EVENT_PARENT_MISSING")
    grade = _text(value["grade"], "RECORD_GRADE_INVALID")
    if grade != plan_view["grade"]:
        raise RecursionRefusal("RECORD_GRADE_MISMATCH")
    body = {
        "root": root,
        "actor": actor,
        "branch": branch,
        "project": project,
        "counterpart": counterpart,
        "record_id": record_id,
        "kind": kind,
        "payload": payload,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "rule_hash": rule_hash,
        "registry_hash": registry_hash,
        "source_hash": source_hash,
        "effective_from": effective_from,
        "causal_parents": causal_parents,
        "grade": grade,
    }
    body_hash = digest(body)
    if "hash" in value and value["hash"] != body_hash:
        raise RecursionRefusal("RECORD_HASH_MISMATCH")
    return {**body, "hash": body_hash}


def _event_binding_view(value: Any, binding: tuple[str, str, str]) -> dict:
    event = _json_mapping(value, "EVENT_BINDING_INVALID")
    owner = event.get("owner")
    if not isinstance(owner, Mapping):
        owner = event.get("identity")
    if not isinstance(owner, Mapping):
        owner = {}
    root = event.get("root", owner.get("root"))
    actor = event.get("actor", owner.get("actor"))
    branch = event.get("branch", owner.get("branch"))
    root = _text(root, "EVENT_BINDING_ROOT_INVALID")
    actor = _text(actor, "EVENT_BINDING_ACTOR_INVALID")
    branch = _text(branch, "EVENT_BINDING_BRANCH_INVALID")
    if (root, actor, branch) != binding:
        raise RecursionRefusal("EVENT_BINDING_IDENTITY_MISMATCH")
    event_id = _text(event.get("event_id"), "EVENT_BINDING_EVENT_ID_INVALID")
    event_hash = _text(event.get("event_hash"), "EVENT_BINDING_EVENT_HASH_INVALID")
    clock = _clock(event.get("clock"), "EVENT_BINDING_CLOCK_INVALID")
    normalized = {
        "root": root,
        "actor": actor,
        "branch": branch,
        "event_id": event_id,
        "event_hash": event_hash,
        "clock": clock,
    }
    for key, item in event.items():
        if key not in normalized:
            normalized[key] = _json_value(item, "EVENT_BINDING_INVALID")
    return normalized


def _base_facts(base_result: Any) -> dict:
    base = _json_mapping(base_result, "BASE_RESULT_INVALID")
    event_ids: set[str] = set()
    event_hashes: set[str] = set()
    clocks: set[int] = set()
    identities: set[tuple[str, str, str]] = set()
    for key in ("before", "after"):
        if key in base and isinstance(base[key], Mapping):
            state = _state_document(base[key], "BASE_RESULT_" + key.upper())
            identities.add((state["root"], state["actor"], state["branch"]))
            clocks.add(state["clock"])
    if all(key in base for key in ("root", "actor", "branch")):
        root = _text(base["root"], "BASE_RESULT_ROOT_INVALID")
        actor = _text(base["actor"], "BASE_RESULT_ACTOR_INVALID")
        branch = _text(base["branch"], "BASE_RESULT_BRANCH_INVALID")
        identities.add((root, actor, branch))
    if "clock" in base:
        clocks.add(_clock(base["clock"], "BASE_RESULT_CLOCK_INVALID"))
    event = None
    objective = base.get("objective")
    if isinstance(objective, Mapping) and isinstance(objective.get("event"), Mapping):
        event = objective["event"]
    elif isinstance(base.get("event"), Mapping):
        event = base["event"]
    if event is not None:
        for key in ("e1_event_id", "event_id", "id"):
            if isinstance(event.get(key), str) and event[key].strip():
                event_ids.add(event[key])
        for key in ("e1_event_hash", "event_hash", "hash"):
            if isinstance(event.get(key), str) and event[key].strip():
                event_hashes.add(event[key])
    for key in ("event_id",):
        if isinstance(base.get(key), str) and base[key].strip():
            event_ids.add(base[key])
    for key in ("event_hash",):
        if isinstance(base.get(key), str) and base[key].strip():
            event_hashes.add(base[key])
    receipt_ref = base.get("receipt_ref")
    if isinstance(receipt_ref, str) and receipt_ref.startswith("P2_EVENT:"):
        tail = receipt_ref[len("P2_EVENT:"):]
        if tail.strip():
            event_hashes.add(tail)
    return {
        "event_ids": event_ids,
        "event_hashes": event_hashes,
        "clocks": clocks,
        "identities": identities,
    }


def _validate_base_result(
    base_result: Any,
    *,
    base_before: Mapping[str, Any],
    binding: tuple[str, str, str],
) -> dict:
    base = _json_mapping(base_result, "BASE_RESULT_INVALID")
    before_state = None
    if "before" in base:
        before_state = _state_document(base["before"], "BASE_RESULT_BEFORE")
        if canonical(before_state) != canonical(base_before):
            raise RecursionRefusal("BASE_RESULT_BEFORE_MISMATCH")
    if "after" in base:
        after_state = _state_document(base["after"], "BASE_RESULT_AFTER")
        if (after_state["root"], after_state["actor"], after_state["branch"]) != binding:
            raise RecursionRefusal("BASE_RESULT_AFTER_IDENTITY_MISMATCH")
        if before_state is not None and after_state["clock"] < before_state["clock"]:
            raise RecursionRefusal("BASE_RESULT_CLOCK_REGRESSION")
    if all(key in base for key in ("root", "actor", "branch")):
        identity = (
            _text(base["root"], "BASE_RESULT_ROOT_INVALID"),
            _text(base["actor"], "BASE_RESULT_ACTOR_INVALID"),
            _text(base["branch"], "BASE_RESULT_BRANCH_INVALID"),
        )
        if identity != binding:
            raise RecursionRefusal("BASE_RESULT_IDENTITY_MISMATCH")
    if "clock" in base:
        _clock(base["clock"], "BASE_RESULT_CLOCK_INVALID")
    if "event_id" in base:
        _text(base["event_id"], "BASE_RESULT_EVENT_ID_INVALID")
    if "event_hash" in base:
        _text(base["event_hash"], "BASE_RESULT_EVENT_HASH_INVALID")
    if "receipt_ref" in base:
        _text(base["receipt_ref"], "BASE_RESULT_RECEIPT_INVALID")
    return base


def _validate_result(
    result: Any,
    *,
    operation_id: str,
    proposal_hash: str,
    expected: Mapping[str, Any],
    binding: tuple[str, str, str],
    effects_receipt: Mapping[str, Any] | None,
) -> dict:
    value = _json_mapping(result, "RESULT_INVALID")
    if set(value) != RESULT_KEYS:
        raise RecursionRefusal("RESULT_SCHEMA")
    if _text(value["operation_id"], "RESULT_OPERATION_ID_INVALID") != operation_id:
        raise RecursionRefusal("RESULT_OPERATION_ID_MISMATCH")
    if _text(value["proposal_hash"], "RESULT_PROPOSAL_HASH_INVALID") != proposal_hash:
        raise RecursionRefusal("RESULT_PROPOSAL_HASH_MISMATCH")
    before = _state_document(value["before"], "RESULT_BEFORE")
    if canonical(before) != canonical(expected):
        raise RecursionRefusal("RESULT_BEFORE_MISMATCH")
    after = _state_document(value["after"], "RESULT_AFTER")
    if (after["root"], after["actor"], after["branch"]) != binding:
        raise RecursionRefusal("RESULT_AFTER_IDENTITY_MISMATCH")
    if after["clock"] < before["clock"]:
        raise RecursionRefusal("RESULT_CLOCK_REGRESSION")
    status = _text(value["status"], "RESULT_STATUS_INVALID")
    if status not in CORE_STATUSES:
        raise RecursionRefusal("RESULT_STATUS_INVALID")
    for key in ("objective", "accessible", "consequences"):
        _json_mapping(value[key], "RESULT_" + key.upper() + "_INVALID")
    readset = value["readset"]
    if not isinstance(readset, (list, tuple)):
        raise RecursionRefusal("RESULT_READSET_INVALID")
    for ref in readset:
        _text(ref, "RESULT_READSET_ELEMENT_INVALID")
    _text(value["receipt_ref"], "RESULT_RECEIPT_INVALID")
    if effects_receipt is not None and isinstance(value["consequences"], Mapping):
        consequences = value["consequences"]
        receipt_hash = effects_receipt.get("receipt_hash")
        link_keys = (
            "effects_receipt_hash",
            "psyche_effects_receipt_hash",
            "p3_effects_receipt_hash",
        )
        links = [key for key in link_keys if key in consequences]
        if not links:
            raise RecursionRefusal("RESULT_RECEIPT_LINK_MISSING")
        for key in links:
            if consequences[key] != receipt_hash:
                raise RecursionRefusal("RESULT_RECEIPT_LINK_MISMATCH")
        if "effects_receipt" in consequences:
            if canonical(consequences["effects_receipt"]) != canonical(effects_receipt):
                raise RecursionRefusal("RESULT_RECEIPT_LINK_MISMATCH")
        response = effects_receipt.get("response")
        response_hash = effects_receipt.get("response_hash")
        expected_ref = None
        if isinstance(response_hash, str) and response_hash:
            expected_ref = "P3_PSYCH:" + response_hash
        elif isinstance(response, Mapping):
            embedded = response.get("hash")
            if isinstance(embedded, str) and embedded:
                expected_ref = "P3_PSYCH:" + embedded
        if expected_ref is not None and value["receipt_ref"] != expected_ref:
            raise RecursionRefusal("RESULT_RECEIPT_REF_MISMATCH")
        projection = effects_receipt.get("projection")
        if isinstance(projection, Mapping):
            actor_surface = projection.get("actor")
            if isinstance(actor_surface, Mapping):
                if canonical(value["accessible"]) != canonical(actor_surface):
                    raise RecursionRefusal("RESULT_ACCESSIBLE_RECEIPT_MISMATCH")
                if (
                    "test_only_actor_surface" in consequences
                    and canonical(consequences["test_only_actor_surface"])
                    != canonical(actor_surface)
                ):
                    raise RecursionRefusal("RESULT_ACCESSIBLE_RECEIPT_MISMATCH")
        compression = effects_receipt.get("compression")
        if compression is not None:
            if (
                "test_only_compression_evidence" not in consequences
                or canonical(consequences["test_only_compression_evidence"])
                != canonical(compression)
            ):
                raise RecursionRefusal("RESULT_COMPRESSION_EVIDENCE_MISMATCH")
    return _detached(value)


class PsycheStore:
    """Normalized immutable sidecar state with a durable cross-store protocol."""

    def __init__(
        self,
        path: str | os.PathLike[str],
        *,
        binding: Mapping[str, Any],
        registry_hash: str,
        source_hash: str,
    ):
        binding = _json_mapping(binding, "STORE_BINDING_INVALID")
        if set(binding) != {"root", "actor", "branch"}:
            raise RecursionRefusal("STORE_BINDING_INVALID:SCHEMA")
        self._binding = (
            _text(binding["root"], "STORE_ROOT_INVALID"),
            _text(binding["actor"], "STORE_ACTOR_INVALID"),
            _text(binding["branch"], "STORE_BRANCH_INVALID"),
        )
        self.registry_hash = _text(registry_hash, "STORE_REGISTRY_HASH_INVALID")
        self.source_hash = _text(source_hash, "STORE_SOURCE_HASH_INVALID")
        self.binding = dict(binding)
        raw_path = str(path)
        if not raw_path or not raw_path.strip():
            raise RecursionRefusal("STORE_PATH_REQUIRED")
        self._memory = raw_path == ":memory:"
        if self._memory:
            self.path = ":memory:"
        else:
            path_obj = Path(raw_path).expanduser()
            path_obj.parent.mkdir(parents=True, exist_ok=True)
            self.path = str(path_obj.resolve())
        self._lock = threading.RLock()
        self._closed = False
        self._connection = sqlite3.connect(
            self.path,
            timeout=30.0,
            isolation_level=None,
            check_same_thread=False,
        )
        self._connection.row_factory = sqlite3.Row
        if not self._memory:
            self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute("PRAGMA foreign_keys=ON")
        self._connection.execute("PRAGMA busy_timeout=30000")
        self._counters = {
            "row_reads": 0,
            "row_writes": 0,
            "targeted_queries": 0,
            "full_scans": 0,
            "records_returned": 0,
        }
        with self._lock:
            self._initialize()

    # ------------------------------------------------------------------
    # Public surface

    def head(self) -> dict:
        with self._lock:
            self._ensure_open()
            head = self._read_head()
            return {"hash": head["hash"], "count": head["count"]}

    def query(self, *, project: str | None, counterpart: str | None, as_of: int) -> list[dict]:
        project = _scope_value(project, "QUERY_PROJECT_INVALID")
        counterpart = _scope_value(counterpart, "QUERY_COUNTERPART_INVALID")
        as_of = _clock(as_of, "QUERY_AS_OF_INVALID")
        with self._lock:
            self._ensure_open()
            clauses = [
                "root=?",
                "actor=?",
                "branch=?",
                "effective_from<=?",
            ]
            parameters: list[Any] = [*self._binding, as_of]
            if project is None:
                clauses.append("project IS NULL")
            else:
                clauses.append("project=?")
                parameters.append(project)
            if counterpart is None:
                clauses.append("counterpart IS NULL")
            else:
                clauses.append("counterpart=?")
                parameters.append(counterpart)
            sql = (
                "SELECT record_id, root, actor, branch, project, counterpart, kind,"
                " payload_json, rule_id, rule_version_json, rule_hash, registry_hash,"
                " source_hash, effective_from, causal_parents_json, grade, hash,"
                " record_json, previous_chain, chain_hash, operation_id "
                "FROM p3_records WHERE "
                + " AND ".join(clauses)
                + " ORDER BY effective_from, seq"
            )
            rows = self._connection.execute(sql, tuple(parameters)).fetchall()
            self._counters["row_reads"] += len(rows)
            self._counters["targeted_queries"] += 1
            records = [self._record_from_row(row) for row in rows]
            self._counters["records_returned"] += len(records)
            return _detached(records)

    def get_operation(self, operation_id: str) -> dict | None:
        operation_id = _text(operation_id, "OPERATION_ID_REQUIRED")
        with self._lock:
            self._ensure_open()
            row = self._connection.execute(
                "SELECT * FROM p3_operations WHERE operation_id=?",
                (operation_id,),
            ).fetchone()
            if row is None:
                return None
            self._counters["row_reads"] += 1
            return self._operation_document(row)

    def pending(self) -> list[dict]:
        with self._lock:
            self._ensure_open()
            rows = self._connection.execute(
                "SELECT * FROM p3_operations WHERE phase<>? ORDER BY seq",
                (PHASE_COMPLETE,),
            ).fetchall()
            self._counters["row_reads"] += len(rows)
            return [_detached(self._operation_document(row)) for row in rows]

    def completed(self) -> list[dict]:
        with self._lock:
            self._ensure_open()
            rows = self._connection.execute(
                "SELECT * FROM p3_operations WHERE phase=? ORDER BY seq",
                (PHASE_COMPLETE,),
            ).fetchall()
            self._counters["row_reads"] += len(rows)
            return [_detached(self._operation_document(row)) for row in rows]

    def reserve(
        self,
        operation_id: str,
        *,
        proposal_hash: str,
        expected: Mapping[str, Any],
        plan_hash: str,
        base_before: Mapping[str, Any],
        psyche_before: Mapping[str, Any] | str,
        plan: Mapping[str, Any],
    ) -> dict:
        operation_id = _text(operation_id, "OPERATION_ID_REQUIRED")
        proposal_hash = _text(proposal_hash, "PROPOSAL_HASH_REQUIRED")
        expected_doc = _state_document(expected, "EXPECTED_STATE_INVALID")
        base_before_doc = _state_document(base_before, "BASE_BEFORE_INVALID")
        if (expected_doc["root"], expected_doc["actor"], expected_doc["branch"]) != self._binding:
            raise RecursionRefusal("EXPECTED_STATE_IDENTITY_MISMATCH")
        if (base_before_doc["root"], base_before_doc["actor"], base_before_doc["branch"]) != self._binding:
            raise RecursionRefusal("BASE_BEFORE_IDENTITY_MISMATCH")
        if base_before_doc["clock"] > expected_doc["clock"]:
            raise RecursionRefusal("BASE_BEFORE_CLOCK_AFTER_EXPECTED")
        plan_view = _plan_view(
            plan,
            plan_hash=plan_hash,
            binding=self._binding,
            registry_hash=self.registry_hash,
            source_hash=self.source_hash,
        )
        psyche_ref = _head_input(psyche_before, "PSYCHE_BEFORE_INVALID")
        with self._lock:
            self._ensure_open()
            with self._write():
                existing = self._connection.execute(
                    "SELECT * FROM p3_operations WHERE operation_id=?",
                    (operation_id,),
                ).fetchone()
                if existing is not None:
                    self._counters["row_reads"] += 1
                    op = self._operation_document(existing)
                    same = (
                        op["proposal_hash"] == proposal_hash
                        and canonical(op["expected"]) == canonical(expected_doc)
                        and op["plan_hash"] == plan_view["plan_hash"]
                        and canonical(op["plan"]) == canonical(plan_view["plan"])
                        and canonical(op["base_before"]) == canonical(base_before_doc)
                        and _head_matches(psyche_ref, op["psyche_before"])
                    )
                    if not same:
                        raise RecursionRefusal("OPERATION_REUSE_MISMATCH")
                    return op
                head = self._read_head()
                if not _head_matches(psyche_ref, head):
                    raise RecursionRefusal("STALE_PSYCHE_HEAD")
                self._connection.execute(
                    "INSERT INTO p3_operations("
                    "operation_id, proposal_hash, expected_json, plan_hash, plan_json,"
                    "base_before_json, psyche_before_json, phase, base_result_json,"
                    "base_result_hash, effects_receipt_json, effects_receipt_hash,"
                    "result_json, result_hash) "
                    "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                    (
                        operation_id,
                        proposal_hash,
                        canonical(expected_doc),
                        plan_view["plan_hash"],
                        canonical(plan_view["plan"]),
                        canonical(base_before_doc),
                        canonical(head),
                        PHASE_PREPARED,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                    ),
                )
                self._counters["row_writes"] += 1
                row = self._connection.execute(
                    "SELECT * FROM p3_operations WHERE operation_id=?",
                    (operation_id,),
                ).fetchone()
                self._counters["row_reads"] += 1
                return self._operation_document(row)

    def save_world(self, operation_id: str, base_result: Mapping[str, Any]) -> dict:
        operation_id = _text(operation_id, "OPERATION_ID_REQUIRED")
        with self._lock:
            self._ensure_open()
            with self._write():
                row = self._operation_row(operation_id)
                op = self._operation_document(row)
                base = _validate_base_result(
                    base_result,
                    base_before=op["base_before"],
                    binding=self._binding,
                )
                if op["phase"] != PHASE_PREPARED:
                    if op["base_result"] is None or canonical(op["base_result"]) != canonical(base):
                        raise RecursionRefusal("BASE_RESULT_REUSE_MISMATCH")
                    return op
                self._connection.execute(
                    "UPDATE p3_operations SET phase=?, base_result_json=?, base_result_hash=? "
                    "WHERE operation_id=? AND phase=?",
                    (
                        PHASE_WORLD,
                        canonical(base),
                        digest(base),
                        operation_id,
                        PHASE_PREPARED,
                    ),
                )
                if self._connection.execute("SELECT changes()").fetchone()[0] != 1:
                    raise RecursionRefusal("PHASE_TRANSITION_LOST")
                self._counters["row_writes"] += 1
                return self._operation_document(self._operation_row(operation_id))

    def commit_effects(
        self,
        operation_id: str,
        *,
        records: list[Mapping[str, Any]] | tuple[Mapping[str, Any], ...],
        response: Mapping[str, Any],
        event_binding: Mapping[str, Any],
        compression: Mapping[str, Any] | None = None,
        projection: Mapping[str, Any] | None = None,
    ) -> dict:
        operation_id = _text(operation_id, "OPERATION_ID_REQUIRED")
        response_doc = _json_mapping(response, "RESPONSE_INVALID")
        if not isinstance(records, (list, tuple)):
            raise RecursionRefusal("RECORDS_NOT_A_SEQUENCE")
        event = _event_binding_view(event_binding, self._binding)
        compression_doc = (
            None if compression is None
            else _json_mapping(compression, "COMPRESSION_INVALID")
        )
        projection_doc = (
            None if projection is None
            else _json_mapping(projection, "PROJECTION_INVALID")
        )
        with self._lock:
            self._ensure_open()
            with self._write():
                row = self._operation_row(operation_id)
                op = self._operation_document(row)
                plan_view = _plan_view(
                    op["plan"],
                    plan_hash=op["plan_hash"],
                    binding=self._binding,
                    registry_hash=self.registry_hash,
                    source_hash=self.source_hash,
                )
                normalized = [
                    _record_body(
                        record,
                        plan_view=plan_view,
                        binding=self._binding,
                        registry_hash=self.registry_hash,
                        source_hash=self.source_hash,
                        event_binding=event,
                    )
                    for record in records
                ]
                record_ids = [record["record_id"] for record in normalized]
                if len(set(record_ids)) != len(record_ids):
                    raise RecursionRefusal("DUPLICATE_RECORD_ID")
                request_hash = digest(
                    {
                        "records": normalized,
                        "response": response_doc,
                        "event_binding": event,
                        "compression": compression_doc,
                        "projection": projection_doc,
                    }
                )
                if op["phase"] in (PHASE_PSYCH, PHASE_COMPLETE):
                    receipt = op["effects_receipt"]
                    if receipt is None or receipt.get("request_hash") != request_hash:
                        raise RecursionRefusal("EFFECTS_REPLAY_MISMATCH")
                    return _detached(receipt)
                if op["phase"] != PHASE_WORLD:
                    raise RecursionRefusal("WORLD_NOT_COMMITTED")
                if op["base_result"] is None:
                    raise RecursionRefusal("BASE_RESULT_MISSING")
                facts = _base_facts(op["base_result"])
                if not facts["event_ids"] and not facts["event_hashes"]:
                    raise RecursionRefusal("BASE_RESULT_EVENT_IDENTITY_MISSING")
                if facts["event_ids"] and event["event_id"] not in facts["event_ids"]:
                    raise RecursionRefusal("EVENT_BINDING_EVENT_ID_MISMATCH")
                if facts["event_hashes"] and event["event_hash"] not in facts["event_hashes"]:
                    raise RecursionRefusal("EVENT_BINDING_EVENT_HASH_MISMATCH")
                if not facts["clocks"] or event["clock"] not in facts["clocks"]:
                    raise RecursionRefusal("EVENT_BINDING_CLOCK_MISMATCH")
                if not facts["identities"] or self._binding not in facts["identities"]:
                    raise RecursionRefusal("EVENT_BINDING_OWNER_MISMATCH")
                base_before = _state_document(op["base_result"]["before"], "BASE_RESULT_BEFORE") if "before" in op["base_result"] else None
                if base_before is not None and canonical(base_before) != canonical(op["base_before"]):
                    raise RecursionRefusal("BASE_RESULT_BEFORE_MISMATCH")
                head_before = self._read_head()
                if canonical(head_before) != canonical(op["psyche_before"]):
                    raise RecursionRefusal("STALE_PSYCHE_HEAD")
                for record in normalized:
                    if self._connection.execute(
                        "SELECT 1 FROM p3_records WHERE record_id=? OR hash=? LIMIT 1",
                        (record["record_id"], record["hash"]),
                    ).fetchone() is not None:
                        raise RecursionRefusal("RECORD_ID_OR_HASH_CONFLICT")
                head_hash = head_before["hash"]
                count = head_before["count"]
                for record in normalized:
                    chain = digest(
                        {
                            "previous": head_hash,
                            "record_id": record["record_id"],
                            "record_hash": record["hash"],
                        }
                    )
                    self._connection.execute(
                        "INSERT INTO p3_records("
                        "record_id, root, actor, branch, project, counterpart, kind,"
                        "payload_json, rule_id, rule_version_json, rule_hash,"
                        "registry_hash, source_hash, effective_from, causal_parents_json,"
                        "grade, hash, record_json, previous_chain, chain_hash, operation_id) "
                        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (
                            record["record_id"],
                            record["root"],
                            record["actor"],
                            record["branch"],
                            record["project"],
                            record["counterpart"],
                            record["kind"],
                            canonical(record["payload"]),
                            record["rule_id"],
                            canonical(record["rule_version"]),
                            record["rule_hash"],
                            record["registry_hash"],
                            record["source_hash"],
                            record["effective_from"],
                            canonical(record["causal_parents"]),
                            record["grade"],
                            record["hash"],
                            canonical(record),
                            head_hash,
                            chain,
                            operation_id,
                        ),
                    )
                    self._counters["row_writes"] += 1
                    head_hash = chain
                    count += 1
                head_after = {
                    "hash": head_hash,
                    "count": count,
                }
                if normalized:
                    self._connection.execute(
                        "UPDATE p3_meta SET head_hash=?, record_count=?, "
                        "head_record_id=?, head_record_hash=? WHERE id=1",
                        (
                            head_after["hash"],
                            head_after["count"],
                            normalized[-1]["record_id"],
                            normalized[-1]["hash"],
                        ),
                    )
                    self._counters["row_writes"] += 1
                records_hash = digest(normalized)
                receipt = {
                    "schema": "SOROK_P3_PSYCHE_EFFECTS_RECEIPT@1",
                    "operation_id": operation_id,
                    "phase": PHASE_PSYCH,
                    "root": self._binding[0],
                    "actor": self._binding[1],
                    "branch": self._binding[2],
                    "registry_hash": self.registry_hash,
                    "source_hash": self.source_hash,
                    "proposal_hash": op["proposal_hash"],
                    "plan_hash": op["plan_hash"],
                    "event_binding": event,
                    "psyche_before": head_before,
                    "psyche_after": head_after,
                    "record_ids": record_ids,
                    "record_hashes": [record["hash"] for record in normalized],
                    "records": normalized,
                    "records_hash": records_hash,
                    "response": response_doc,
                    "response_hash": digest(response_doc),
                    "request_hash": request_hash,
                    "authority": plan_view["authority"],
                    "grade": plan_view["grade"],
                    "native_science": "NOT_ISSUED",
                    "production": False,
                }
                if compression_doc is not None:
                    receipt["compression"] = compression_doc
                    receipt["compression_hash"] = digest(compression_doc)
                if projection_doc is not None:
                    receipt["projection"] = projection_doc
                    receipt["projection_hash"] = digest(projection_doc)
                receipt["receipt_hash"] = digest(receipt)
                self._connection.execute(
                    "UPDATE p3_operations SET phase=?, effects_receipt_json=?, "
                    "effects_receipt_hash=? WHERE operation_id=? AND phase=?",
                    (
                        PHASE_PSYCH,
                        canonical(receipt),
                        receipt["receipt_hash"],
                        operation_id,
                        PHASE_WORLD,
                    ),
                )
                if self._connection.execute("SELECT changes()").fetchone()[0] != 1:
                    raise RecursionRefusal("PHASE_TRANSITION_LOST")
                self._counters["row_writes"] += 1
                return _detached(receipt)

    def finish(self, operation_id: str, result: Mapping[str, Any]) -> dict:
        operation_id = _text(operation_id, "OPERATION_ID_REQUIRED")
        with self._lock:
            self._ensure_open()
            with self._write():
                row = self._operation_row(operation_id)
                op = self._operation_document(row)
                result_doc = _validate_result(
                    result,
                    operation_id=operation_id,
                    proposal_hash=op["proposal_hash"],
                    expected=op["expected"],
                    binding=self._binding,
                    effects_receipt=op["effects_receipt"],
                )
                if op["phase"] == PHASE_COMPLETE:
                    if op["result"] is None or canonical(op["result"]) != canonical(result_doc):
                        raise RecursionRefusal("RESULT_REPLAY_MISMATCH")
                    return op
                if op["phase"] != PHASE_PSYCH:
                    raise RecursionRefusal("PSYCH_NOT_COMMITTED")
                self._connection.execute(
                    "UPDATE p3_operations SET phase=?, result_json=?, result_hash=? "
                    "WHERE operation_id=? AND phase=?",
                    (
                        PHASE_COMPLETE,
                        canonical(result_doc),
                        digest(result_doc),
                        operation_id,
                        PHASE_PSYCH,
                    ),
                )
                if self._connection.execute("SELECT changes()").fetchone()[0] != 1:
                    raise RecursionRefusal("PHASE_TRANSITION_LOST")
                self._counters["row_writes"] += 1
                return self._operation_document(self._operation_row(operation_id))

    def verify(self) -> bool:
        """Full integrity scan.  Normal head/query/operation paths never use it."""
        with self._lock:
            self._ensure_open()
            self._counters["full_scans"] += 1
            meta = self._meta_row()
            genesis = self._genesis()
            previous = genesis
            count = 0
            head_record_id = None
            head_record_hash = None
            rows = self._connection.execute(
                "SELECT * FROM p3_records ORDER BY seq"
            ).fetchall()
            self._counters["row_reads"] += len(rows)
            for row in rows:
                record = self._record_from_row(row)
                if row["previous_chain"] != previous:
                    raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_CHAIN")
                chain = digest(
                    {
                        "previous": previous,
                        "record_id": record["record_id"],
                        "record_hash": record["hash"],
                    }
                )
                if row["chain_hash"] != chain:
                    raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_CHAIN_HASH")
                previous = chain
                count += 1
                head_record_id = record["record_id"]
                head_record_hash = record["hash"]
            if (
                meta["record_count"] != count
                or meta["head_hash"] != previous
                or meta["head_record_id"] != head_record_id
                or meta["head_record_hash"] != head_record_hash
            ):
                raise RecursionRefusal("JOURNAL_INTEGRITY:HEAD")
            operations = self._connection.execute(
                "SELECT * FROM p3_operations ORDER BY seq"
            ).fetchall()
            self._counters["row_reads"] += len(operations)
            for row in operations:
                self._operation_document(row)
            return True

    def stats(self) -> dict:
        with self._lock:
            self._ensure_open()
            result = dict(self._counters)
            if not self._memory:
                path = Path(self.path)
                result["db_bytes"] = path.stat().st_size if path.exists() else 0
                wal = Path(self.path + "-wal")
                result["wal_bytes"] = wal.stat().st_size if wal.exists() else 0
            else:
                result["db_bytes"] = 0
                result["wal_bytes"] = 0
            return result

    def close(self) -> None:
        with self._lock:
            if not self._closed:
                self._connection.close()
                self._closed = True

    def __enter__(self) -> "PsycheStore":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()

    # ------------------------------------------------------------------
    # Schema and head

    def _ensure_open(self) -> None:
        if self._closed:
            raise RecursionRefusal("STORE_CLOSED")

    def _genesis(self) -> str:
        return digest(
            {
                "schema": SCHEMA,
                "root": self._binding[0],
                "actor": self._binding[1],
                "branch": self._binding[2],
                "registry_hash": self.registry_hash,
                "source_hash": self.source_hash,
            }
        )

    def _initialize(self) -> None:
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            version = self._connection.execute("PRAGMA user_version").fetchone()[0]
            existing = {
                row["name"]
                for row in self._connection.execute(
                    "SELECT name FROM sqlite_master WHERE type='table' "
                    "AND name IN ('p3_meta','p3_records','p3_operations')"
                )
            }
            if version not in (0, 1, 2):
                raise RecursionRefusal("STORE_SCHEMA_VERSION_UNSUPPORTED")
            if version == 0 and existing:
                raise RecursionRefusal("JOURNAL_INTEGRITY:UNMARKED_SCHEMA")
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS p3_meta ("
                "id INTEGER PRIMARY KEY CHECK(id=1),"
                "schema TEXT NOT NULL,"
                "root TEXT NOT NULL,"
                "actor TEXT NOT NULL,"
                "branch TEXT NOT NULL,"
                "registry_hash TEXT NOT NULL,"
                "source_hash TEXT NOT NULL,"
                "head_hash TEXT NOT NULL,"
                "record_count INTEGER NOT NULL CHECK(record_count>=0),"
                "head_record_id TEXT,"
                "head_record_hash TEXT)"
            )
            self._connection.execute(RECORDS_TABLE_DDL)
            self._migrate_records_kind_schema_if_needed()
            self._connection.execute(RECORDS_SCOPE_INDEX_DDL)
            self._connection.execute(RECORDS_KIND_INDEX_DDL)
            self._connection.execute(
                "CREATE TABLE IF NOT EXISTS p3_operations ("
                "seq INTEGER PRIMARY KEY AUTOINCREMENT,"
                "operation_id TEXT NOT NULL UNIQUE,"
                "proposal_hash TEXT NOT NULL,"
                "expected_json TEXT NOT NULL,"
                "plan_hash TEXT NOT NULL,"
                "plan_json TEXT NOT NULL,"
                "base_before_json TEXT NOT NULL,"
                "psyche_before_json TEXT NOT NULL,"
                "phase TEXT NOT NULL CHECK(phase IN "
                "('PREPARED','WORLD_COMMITTED','PSYCH_COMMITTED','COMPLETE')),"
                "base_result_json TEXT,"
                "base_result_hash TEXT,"
                "effects_receipt_json TEXT,"
                "effects_receipt_hash TEXT,"
                "result_json TEXT,"
                "result_hash TEXT)"
            )
            self._connection.execute(
                "CREATE INDEX IF NOT EXISTS p3_operations_phase "
                "ON p3_operations(phase, seq)"
            )
            self._connection.execute("PRAGMA user_version=2")
            self._connection.execute("COMMIT")
        except BaseException:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise

        row = self._connection.execute("SELECT * FROM p3_meta WHERE id=1").fetchone()
        if row is None:
            has_data = self._connection.execute(
                "SELECT 1 FROM p3_records LIMIT 1"
            ).fetchone() or self._connection.execute(
                "SELECT 1 FROM p3_operations LIMIT 1"
            ).fetchone()
            if has_data is not None:
                raise RecursionRefusal("JOURNAL_INTEGRITY:MISSING_META")
            self._connection.execute(
                "INSERT INTO p3_meta VALUES (1,?,?,?,?,?,?,?,?,?,?)",
                (
                    SCHEMA,
                    self._binding[0],
                    self._binding[1],
                    self._binding[2],
                    self.registry_hash,
                    self.source_hash,
                    self._genesis(),
                    0,
                    None,
                    None,
                ),
            )
            return
        self._validate_meta(row)
        self._read_head()

    def _migrate_records_kind_schema_if_needed(self) -> None:
        row = self._connection.execute(
            "SELECT sql FROM sqlite_master WHERE type='table' AND name='p3_records'"
        ).fetchone()
        if row is None or not row["sql"]:
            return
        sql = row["sql"]
        if "V3MS_MEDIATOR" in sql:
            return
        if "CHECK" not in sql.upper() or "KIND" not in sql.upper():
            return
        self._connection.execute("ALTER TABLE p3_records RENAME TO p3_records_legacy")
        self._connection.execute("DROP INDEX IF EXISTS p3_records_scope")
        self._connection.execute("DROP INDEX IF EXISTS p3_records_kind")
        self._connection.execute(RECORDS_TABLE_DDL)
        self._connection.execute(
            "INSERT INTO p3_records (" + RECORD_COLUMNS_SQL + ") "
            "SELECT " + RECORD_COLUMNS_SQL + " FROM p3_records_legacy"
        )
        self._connection.execute("DROP TABLE p3_records_legacy")
        self._connection.execute(RECORDS_SCOPE_INDEX_DDL)
        self._connection.execute(RECORDS_KIND_INDEX_DDL)

    def _validate_meta(self, row: sqlite3.Row) -> None:
        if row["schema"] != SCHEMA:
            raise RecursionRefusal("STORE_SCHEMA_MISMATCH")
        stored = (row["root"], row["actor"], row["branch"])
        if stored != self._binding:
            raise RecursionRefusal("STORE_REOPEN_BINDING_MISMATCH")
        if row["registry_hash"] != self.registry_hash:
            raise RecursionRefusal("STORE_REOPEN_REGISTRY_MISMATCH")
        if row["source_hash"] != self.source_hash:
            raise RecursionRefusal("STORE_REOPEN_SOURCE_MISMATCH")

    def _meta_row(self) -> sqlite3.Row:
        row = self._connection.execute("SELECT * FROM p3_meta WHERE id=1").fetchone()
        if row is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:META_MISSING")
        self._counters["row_reads"] += 1
        self._validate_meta(row)
        return row

    def _read_head(self) -> dict:
        row = self._meta_row()
        count = int(row["record_count"])
        head_hash = row["head_hash"]
        if count == 0:
            if (
                head_hash != self._genesis()
                or row["head_record_id"] is not None
                or row["head_record_hash"] is not None
            ):
                raise RecursionRefusal("JOURNAL_INTEGRITY:EMPTY_HEAD")
            return {"hash": head_hash, "count": 0}
        if not row["head_record_id"] or not row["head_record_hash"]:
            raise RecursionRefusal("JOURNAL_INTEGRITY:HEAD_POINTER")
        last = self._connection.execute(
            "SELECT record_id, hash, previous_chain, chain_hash "
            "FROM p3_records WHERE record_id=?",
            (row["head_record_id"],),
        ).fetchone()
        self._counters["row_reads"] += 1
        if last is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:HEAD_RECORD_MISSING")
        if (
            last["record_id"] != row["head_record_id"]
            or last["hash"] != row["head_record_hash"]
            or last["chain_hash"] != head_hash
        ):
            raise RecursionRefusal("JOURNAL_INTEGRITY:HEAD_LINK")
        expected = digest(
            {
                "previous": last["previous_chain"],
                "record_id": last["record_id"],
                "record_hash": last["hash"],
            }
        )
        if expected != head_hash:
            raise RecursionRefusal("JOURNAL_INTEGRITY:HEAD_CHAIN")
        return {"hash": head_hash, "count": count}

    # ------------------------------------------------------------------
    # Operations

    def _operation_row(self, operation_id: str) -> sqlite3.Row:
        row = self._connection.execute(
            "SELECT * FROM p3_operations WHERE operation_id=?",
            (operation_id,),
        ).fetchone()
        self._counters["row_reads"] += 1
        if row is None:
            raise RecursionRefusal("OPERATION_NOT_FOUND")
        return row

    def _operation_document(self, row: sqlite3.Row) -> dict:
        phase = row["phase"]
        if phase not in PHASES:
            raise RecursionRefusal("JOURNAL_INTEGRITY:OPERATION_PHASE")
        expected = _state_document(
            _load_json_text(row["expected_json"], "JOURNAL_EXPECTED"),
            "JOURNAL_EXPECTED",
        )
        base_before = _state_document(
            _load_json_text(row["base_before_json"], "JOURNAL_BASE_BEFORE"),
            "JOURNAL_BASE_BEFORE",
        )
        psyche_before = _head_input(
            _load_json_text(row["psyche_before_json"], "JOURNAL_PSYCHE_BEFORE"),
            "JOURNAL_PSYCHE_BEFORE",
        )
        plan = _json_mapping(
            _load_json_text(row["plan_json"], "JOURNAL_PLAN"), "JOURNAL_PLAN"
        )
        plan_view = _plan_view(
            plan,
            plan_hash=row["plan_hash"],
            binding=self._binding,
            registry_hash=self.registry_hash,
            source_hash=self.source_hash,
        )
        plan = plan_view["plan"]
        base_result = None
        if row["base_result_json"] is not None:
            base_result = _json_mapping(
                _load_json_text(row["base_result_json"], "JOURNAL_BASE_RESULT"),
                "JOURNAL_BASE_RESULT",
            )
            if row["base_result_hash"] != digest(base_result):
                raise RecursionRefusal("JOURNAL_INTEGRITY:BASE_RESULT_HASH")
        effects = None
        if row["effects_receipt_json"] is not None:
            effects = _json_mapping(
                _load_json_text(row["effects_receipt_json"], "JOURNAL_EFFECTS"),
                "JOURNAL_EFFECTS",
            )
            receipt_body = {
                key: value for key, value in effects.items() if key != "receipt_hash"
            }
            if row["effects_receipt_hash"] != digest(receipt_body):
                raise RecursionRefusal("JOURNAL_INTEGRITY:EFFECTS_HASH")
            if effects.get("phase") != PHASE_PSYCH:
                raise RecursionRefusal("JOURNAL_INTEGRITY:EFFECTS_PHASE")
            if effects.get("receipt_hash") != digest(receipt_body):
                raise RecursionRefusal("JOURNAL_INTEGRITY:EFFECTS_RECEIPT_HASH")
        result = None
        if row["result_json"] is not None:
            result = _json_mapping(
                _load_json_text(row["result_json"], "JOURNAL_RESULT"),
                "JOURNAL_RESULT",
            )
            if row["result_hash"] != digest(result):
                raise RecursionRefusal("JOURNAL_INTEGRITY:RESULT_HASH")
        if phase in (PHASE_WORLD, PHASE_PSYCH, PHASE_COMPLETE) and base_result is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:BASE_RESULT_MISSING")
        if phase in (PHASE_PSYCH, PHASE_COMPLETE) and effects is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:EFFECTS_MISSING")
        if phase == PHASE_COMPLETE and result is None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RESULT_MISSING")
        if phase == PHASE_PREPARED and (
            base_result is not None or effects is not None or result is not None
        ):
            raise RecursionRefusal("JOURNAL_INTEGRITY:PREPARED_HAS_LATER_PAYLOAD")
        if phase == PHASE_WORLD and (effects is not None or result is not None):
            raise RecursionRefusal("JOURNAL_INTEGRITY:WORLD_HAS_LATER_PAYLOAD")
        if phase == PHASE_PSYCH and result is not None:
            raise RecursionRefusal("JOURNAL_INTEGRITY:PSYCH_HAS_RESULT")
        return {
            "operation_id": row["operation_id"],
            "proposal_hash": row["proposal_hash"],
            "expected": expected,
            "plan_hash": row["plan_hash"],
            "plan": plan,
            "base_before": base_before,
            "psyche_before": psyche_before,
            "phase": phase,
            "base_result": base_result,
            "effects_receipt": effects,
            "result": result,
        }

    @contextmanager
    def _write(self):
        self._connection.execute("BEGIN IMMEDIATE")
        try:
            yield
        except BaseException:
            if self._connection.in_transaction:
                self._connection.execute("ROLLBACK")
            raise
        else:
            self._connection.execute("COMMIT")

    # ------------------------------------------------------------------
    # Record reads and integrity

    def _record_from_json(self, body: str) -> dict:
        try:
            record = json.loads(body)
        except (TypeError, ValueError) as exc:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_JSON") from exc
        if not isinstance(record, Mapping):
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_OBJECT")
        required = RECORD_REQUIRED | {"hash"}
        if set(record) != required:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_SCHEMA")
        body_value = {key: record[key] for key in RECORD_REQUIRED}
        if digest(body_value) != record["hash"]:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_HASH")
        root = _text(record["root"], "JOURNAL_RECORD_ROOT")
        actor = _text(record["actor"], "JOURNAL_RECORD_ACTOR")
        branch = _text(record["branch"], "JOURNAL_RECORD_BRANCH")
        if (root, actor, branch) != self._binding:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_IDENTITY")
        _scope_value(record["project"], "JOURNAL_RECORD_PROJECT")
        _scope_value(record["counterpart"], "JOURNAL_RECORD_COUNTERPART")
        _text(record["record_id"], "JOURNAL_RECORD_ID")
        if record["kind"] not in KINDS:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_KIND")
        _json_mapping(record["payload"], "JOURNAL_RECORD_PAYLOAD")
        _text(record["rule_id"], "JOURNAL_RECORD_RULE_ID")
        _rule_version(record["rule_version"], "JOURNAL_RECORD_RULE_VERSION")
        _text(record["rule_hash"], "JOURNAL_RECORD_RULE_HASH")
        if record["registry_hash"] != self.registry_hash:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_REGISTRY")
        if record["source_hash"] != self.source_hash:
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_SOURCE")
        _clock(record["effective_from"], "JOURNAL_RECORD_EFFECTIVE_FROM")
        parents = record["causal_parents"]
        if not isinstance(parents, (list, tuple)):
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_PARENTS")
        for parent in parents:
            _text(parent, "JOURNAL_INTEGRITY:RECORD_PARENT")
        grade = _text(record["grade"], "JOURNAL_INTEGRITY:RECORD_GRADE")
        if grade != "SOURCEFREE_TEST_ONLY" and not grade.startswith("TEST_ONLY"):
            raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_GRADE_NOT_TEST_ONLY")
        return _detached(record)

    def _record_from_row(self, row: sqlite3.Row) -> dict:
        record = self._record_from_json(row["record_json"])
        checks = {
            "record_id": record["record_id"],
            "root": record["root"],
            "actor": record["actor"],
            "branch": record["branch"],
            "project": record["project"],
            "counterpart": record["counterpart"],
            "kind": record["kind"],
            "payload_json": canonical(record["payload"]),
            "rule_id": record["rule_id"],
            "rule_version_json": canonical(record["rule_version"]),
            "rule_hash": record["rule_hash"],
            "registry_hash": record["registry_hash"],
            "source_hash": record["source_hash"],
            "effective_from": record["effective_from"],
            "causal_parents_json": canonical(record["causal_parents"]),
            "grade": record["grade"],
            "hash": record["hash"],
        }
        for key, expected in checks.items():
            if row[key] != expected:
                raise RecursionRefusal("JOURNAL_INTEGRITY:RECORD_COLUMNS:" + key)
        return record


__all__ = [
    "PHASE_PREPARED",
    "PHASE_WORLD",
    "PHASE_PSYCH",
    "PHASE_COMPLETE",
    "PsycheStore",
    "SCHEMA",
]
