"""Frozen TEST_ONLY B1-derived predicates; never a native rule registration.

The imported B1 mode_for is real recovered code, not a child/caretaker fixture
selected by this module. Historical sources and current actual P2 participation
are separate inputs. Response transactions are not claims of enacted P2 action.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

from developmental_recursion.contracts import RecursionRefusal, detached, digest

GRADE = "SOURCEFREE_TEST_ONLY"
B1_SHA256 = "478b989730f49a5def41a367b6f53e4aae9c80961f7f466fe669c7dbd92201a3"
B1_PATH = (Path(__file__).resolve().parents[2] /
           "SOROK-P3-E1-DEVELOPMENTAL-ABI-RECONNAISSANCE-R1/probe/vendor/B1/bfirst.py")


def _require(ok, code):
    if not ok:
        raise RecursionRefusal(code)


def _sealed(body):
    return dict(detached(body), hash=digest(body))


def _valid(body):
    return isinstance(body, dict) and body.get("hash") == digest(
        {k: v for k, v in body.items() if k != "hash"})


_FORMATION = _sealed({
    "rule_id": "TEST_ONLY_P3_B1_SCOPED_MEDIATOR_CREATE", "rule_version": "1",
    "grade": GRADE, "source": B1_SHA256,
    "predicate": "actual actor-experienced P2 event + independently bound prior "
                 "compare_plans_in_task participation; preserve B1 mode_for outcome",
    "target": "V3MS_MEDIATOR", "operation": "CREATE",
    "native_rule": "MISSING_RULE", "numeric_policy": "NONE",
})
_RESPONSE = _sealed({
    "rule_id": "TEST_ONLY_P3_B1_SCOPED_RESPONSE", "rule_version": "1",
    "grade": GRADE, "source": B1_SHA256,
    "predicate": "later actual actor experience reads exact same-scope committed "
                 "mediators; preserve all context-eligible streams",
    "fallback": "B1 inspect_alone only when there are no prior same-scope records",
    "native_rule": "MISSING_RULE", "material_effect": "NONE",
})


def rule_descriptors():
    return [{"rule_id": r["rule_id"], "rule_version": r["rule_version"],
             "rule_hash": r["hash"]} for r in (_FORMATION, _RESPONSE)]


def make_registry(source_hash):
    _require(isinstance(source_hash, str) and len(source_hash) == 64,
             "P3_RULE_SOURCE_REQUIRED")
    return _sealed({"schema": "P3_FROZEN_TEST_ONLY_RULE_REGISTRY@1",
                    "grade": GRADE, "source_hash": source_hash,
                    "rules": rule_descriptors(),
                    "incompatible_modes": [["joint_check", "private_check"]]})


def production_guard():
    # No code path mutates or populates the genuine production registry.
    return {"status": "DENY_ZERO_EFFECT", "reason": "ZERO_POSITIVE_REGISTRY",
            "effects": [], "native_rule": "MISSING_RULE"}


def _check_sources(registry, source_hash):
    _require(B1_PATH.is_file() and hashlib.sha256(B1_PATH.read_bytes()).hexdigest()
             == B1_SHA256, "P3_B1_SOURCE_SEVERED")
    _require(registry == make_registry(source_hash), "P3_FROZEN_RULE_REGISTRY_MISMATCH")


def _mode_for(history, event, counterpart):
    # A distinct module object keeps this sourcefree import out of native owners.
    spec = importlib.util.spec_from_file_location("_p3_recovered_b1", B1_PATH)
    module = importlib.util.module_from_spec(spec)
    import sys
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
        return module.mode_for({"history": history}, event, counterpart)
    finally:
        sys.modules.pop(spec.name, None)


def validate_history(history, *, identity, source_hash):
    _require(isinstance(history, (list, tuple)), "P3_HISTORY_SCHEMA")
    known = set()
    result = []
    for h in history:
        _require(_valid(h), "P3_HISTORY_HASH")
        _require(all(h.get(k) == identity[k] for k in ("root", "actor", "branch")),
                 "P3_HISTORY_IDENTITY")
        _require(h.get("grade") == GRADE and h.get("source_hash") == source_hash,
                 "P3_HISTORY_SOURCE")
        _require(type(h.get("time")) is int and h["time"] < identity["clock"],
                 "P3_HISTORY_CLOCK")
        _require(all(isinstance(h.get(k), str) and h[k]
                     for k in ("episode_id", "project", "counterpart", "activity", "outcome")),
                 "P3_HISTORY_FIELDS")
        _require(isinstance(h.get("parent_refs"), list)
                 and all(ref in known for ref in h["parent_refs"]), "P3_HISTORY_LINEAGE")
        _require(h["hash"] not in known, "P3_DUPLICATE_HISTORY")
        known.add(h["hash"])
        result.append(detached(h))
    return result


def validate_plan(plan, *, identity, proposal, source_hash, registry):
    _check_sources(registry, source_hash)
    _require(_valid(plan), "P3_PLAN_HASH")
    _require(all(plan.get(k) == identity[k] for k in ("root", "actor", "branch")),
             "P3_PLAN_IDENTITY")
    _require(plan.get("grade") == GRADE and plan.get("source_hash") == source_hash
             and plan.get("registry_hash") == registry["hash"], "P3_PLAN_SOURCE")
    _require(plan.get("proposal_hash") == digest(proposal)
             and plan.get("event_id") == proposal["event_id"], "P3_PLAN_PROPOSAL")
    _require(plan.get("permitted_rules") == rule_descriptors(), "P3_PLAN_RULE_VERSION")
    _require(plan.get("phase") in ("FORMATION", "RECRUIT", "STABILITY"), "P3_PLAN_PHASE")
    _require(all(isinstance(plan.get(k), str) and plan[k]
                 for k in ("project", "counterpart")), "P3_PLAN_SCOPE")
    for key in ("activation_roles", "relation_refs", "obligation_refs"):
        _require(isinstance(plan.get(key), list)
                 and all(isinstance(x, str) and x for x in plan[key]), "P3_PLAN_SELECTORS")
    return detached(plan)


def evaluate_event(*, identity, proposal, realized, history, records, plan,
                   source_hash, registry, activation=None):
    """Compute one sourcefree response/effect against actual admitted P2 output.

    Validation of the plan is also invoked before effects by the P3 owner. Here
    it is repeated to bind this computation to the exact source and event.
    Material eligibility is read, never written. No ADP016/017 state is emitted.
    """
    plan = validate_plan(plan, identity=identity, proposal=proposal,
                         source_hash=source_hash, registry=registry)
    history = validate_history(history, identity=identity, source_hash=source_hash)
    event = realized.get("objective", {}).get("event", {})
    _require(realized.get("after") == identity and identity["clock"] == proposal["event_time"],
             "P3_REALIZED_STATE_BINDING")
    _require(event.get("actor_id") == identity["actor"]
             and event.get("branch_id") == identity["branch"]
             and event.get("event_time") == proposal["event_time"], "P3_ACTUAL_EVENT_BINDING")
    event_hash = event.get("e1_event_hash")
    _require(isinstance(event_hash, str) and len(event_hash) == 64, "P3_ACTUAL_EVENT_HASH")
    experience = realized.get("accessible", {})
    observed_ids = [x.get("event_id") for x in experience.get("events", [])]
    accessed = (experience.get("status") == "OBSERVED"
                and experience.get("actor_ref") == identity["actor"]
                and event.get("action_event_id") in observed_ids
                and event.get("performed") is True)
    if not accessed:
        return {"records": [], "response": {"grade": GRADE, "status": "HELD",
                "reason": "ACTOR_PARTICIPATION_UNAVAILABLE", "streams": []},
                "readset": [event_hash], "memory_formation": "MISSING_RULE"}
    relevant = []
    for record in records:
        _require(_valid(record), "P3_RECRUITED_RECORD_HASH")
        _require(all(record.get(k) == identity[k] for k in ("root", "actor", "branch")),
                 "P3_RECRUITED_RECORD_IDENTITY")
        _require(record.get("source_hash") == source_hash
                 and record.get("registry_hash") == registry["hash"], "P3_RECRUITED_RECORD_SOURCE")
        _require(record.get("effective_from", proposal["event_time"]) < proposal["event_time"],
                 "P3_RECRUITED_RECORD_TIME")
        _require({k: record.get(k) for k in ("rule_id", "rule_version", "rule_hash")}
                 == rule_descriptors()[0] and record.get("kind") == "V3MS_MEDIATOR"
                 and record.get("grade") == GRADE, "P3_RECRUITED_RECORD_RULE")
        if record.get("project") == plan["project"] and record.get("counterpart") == plan["counterpart"]:
            relevant.append(record)
    material = realized.get("consequences", {}).get("immediate_response", {}).get(
        "objective_material_eligible")
    _require(material is None or type(material) is bool, "P3_MATERIAL_RECEIPT_SCHEMA")
    new_records, streams, parents = [], [], [event_hash]
    if plan["phase"] == "FORMATION":
        modes = _mode_for(history, {"project": plan["project"], "time": proposal["event_time"]},
                          plan["counterpart"])
        for h, mode in modes:
            body = {k: identity[k] for k in ("root", "actor", "branch")}
            body.update(record_id=digest([identity["root"], identity["actor"],
                        identity["branch"], event_hash, h["hash"], _FORMATION["hash"]]),
                        kind="V3MS_MEDIATOR", project=plan["project"], counterpart=plan["counterpart"],
                        payload={"mode": mode, "origin_access": "NOT_GRANTED_AS_MEMORY",
                                 "activation_roles": plan["activation_roles"],
                                 "relation_refs": plan["relation_refs"],
                                 "obligation_refs": plan["obligation_refs"],
                                 "requires_actor_access": True},
                        rule_id=_FORMATION["rule_id"], rule_version="1",
                        rule_hash=_FORMATION["hash"], registry_hash=registry["hash"],
                        source_hash=source_hash, effective_from=proposal["event_time"],
                        causal_parents=[event_hash, h["hash"]], grade=GRADE)
            new_records.append(_sealed(body))
            parents.append(h["hash"])
            streams.append({"mode": "compare_current_plan", "history_ref": h["hash"],
                            "candidate_activity": "compare_current_plan:" + plan["counterpart"],
                            "material_eligible": material, "native_action_performed": False})
    elif relevant:
        # Actual pure activation is supplied by p3.projections, never inferred
        # here from a role/demographic label or from narrative impressions.
        _require(isinstance(activation, dict), "P3_ACTIVATION_READER_REQUIRED")
        _require(activation.get("identity") == identity
                 and activation.get("registry_hash") == registry["hash"],
                 "P3_ACTIVATION_IDENTITY")
        entries = {e["record_id"]: e for e in activation.get("entries", [])}
        for record in relevant:
            entry = entries.get(record["record_id"])
            _require(entry is not None and entry.get("record_hash") == record["hash"],
                     "P3_ACTIVATION_RECORD_BINDING")
            _require(entry.get("activation") in ("ELIGIBLE", "INHIBITED", "UNKNOWN"),
                     "P3_ACTIVATION_STATUS")
            parents.append(record["hash"])
            if entry.get("activation") == "ELIGIBLE":
                mode = record["payload"]["mode"]
                streams.append({"mode": mode, "record_id": record["record_id"],
                                "record_hash": record["hash"],
                                "candidate_activity": mode + ":" + plan["counterpart"],
                                "material_eligible": material, "native_action_performed": False})
    else:
        streams.append({"mode": "inspect_alone",
                        "candidate_activity": "inspect_alone:" + plan["counterpart"],
                        "material_eligible": material, "native_action_performed": False})
    response = {"grade": GRADE, "status": "COMPUTED_TEST_ONLY_RESPONSE",
                "event_ref": event_hash, "rule": rule_descriptors()[1],
                "streams": streams, "contradictions": (activation or {}).get("contradictions", []),
                "native_rule": "MISSING_RULE", "native_action": "NOT_ISSUED_BY_P3_RULE",
                "memory_formation": "MISSING_RULE", "first_person_claims": []}
    return {"records": new_records, "response": _sealed(response),
            "readset": list(dict.fromkeys([*parents, registry["hash"], B1_SHA256])),
            "memory_formation": "MISSING_RULE"}
