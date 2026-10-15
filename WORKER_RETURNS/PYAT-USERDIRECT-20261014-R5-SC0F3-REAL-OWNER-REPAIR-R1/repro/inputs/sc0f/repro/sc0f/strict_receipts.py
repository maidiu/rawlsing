"""SC0F strict Draft 2020-12 two-contract receipt builders — full schema conformance.

Emits WorldReceipt (17 required fields) and PossibilityReceipt (20 required fields)
that pass Draft202012Validator against the frozen envelope blob
610ac870fde6cfe63796592b3c6b1e1bf1e37150.  additionalProperties: false throughout.
"""
from __future__ import annotations

import copy
import hashlib
import json
from typing import Any, Mapping


def _sha256(obj: Any) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _ref(kind: str, ident: str, content: Any = None) -> dict[str, str]:
    h = _sha256(content if content is not None else ident)
    return {"kind": kind, "id": ident, "hash": h}


# Valid enum values from the frozen schema
STATUS_CODES = (
    "PRESENT", "OBSERVED_ZERO", "VALID_EMPTY", "MISSING", "UNDERPOWERED",
    "NOT_ASKED", "NONCOMPARABLE", "HELD_AUTHORITY", "NO_CURRENT", "DENIED_USE",
    "UNBOUND_RUNTIME_BINDING", "PROXY_MODELLED", "UNKNOWN_UNOBSERVED_GAP",
    "PARTIAL_DEFERRED", "INTEGRITY_FAILURE",
)
RECOVERABILITY = (
    "NONE_SOURCE_INTRINSIC", "ISSUER_OR_POLICY", "PRODUCER_OR_BINDING",
    "NEW_RELEASE", "DEFERRED", "UNKNOWN",
)
DECISIONS = ("SELECTED", "DEFERRED", "EXCLUDED", "UNRESOLVED")
GRADES = ("SOURCE_OBSERVED", "SOURCE_DERIVED", "MODELLED_AUTHORIZED", "TEST_FIXTURE_ONLY")


def _status(code: str = "PRESENT", scope: str = "world", reason: str = "", recoverability: str = "UNKNOWN") -> dict[str, Any]:
    return {
        "code": code if code in STATUS_CODES else "PRESENT",
        "scope_ref": _ref("SCOPE", scope),
        "reason": reason or "selected",
        "recoverability": recoverability if recoverability in RECOVERABILITY else "UNKNOWN",
    }


def build_world_receipt(
    *,
    request_id: str,
    selection: Mapping[str, Any],
    values_read_refs: list[dict[str, str]],
    state_code: str = "PRESENT",
) -> dict[str, Any]:
    """Build a strict Draft 2020-12 WorldReceipt (17 required fields)."""
    world = selection["world"]
    demand = selection.get("demand", {})
    axes = world.get("time_axes", {})
    ceiling = world.get("permission_ceiling", {})

    clock = {
        "observation_effective": {
            "valid_from": axes.get("observation_valid"),
            "valid_to": None,
            "evidence_ref": _ref("EVIDENCE", "observation"),
        },
        "publication_knowledge": {
            "published_at": axes.get("published"),
            "knowledge_as_of": axes.get("as_of"),
        },
        "actor_event": {
            "scene_at": axes.get("actor_event"),
            "caller_owns_time": True,
        },
        "request_currentness": {
            "asked_at": axes.get("requested"),
            "policy_ref": _ref("POLICY", "request-currentness"),
        },
        "mode": world.get("clock_mode", "KNOWLEDGE_AS_OF"),
    }

    # Selection records
    selection_records = []
    for key in sorted(world.get("values", {})):
        selection_records.append({
            "demand_key": key,
            "decision": "SELECTED",
            "object_ref": _ref("WORLD_OBJECT", key),
            "native_scope_ref": _ref("NATIVE_SCOPE", world.get("native_unit", "RESPONDENT")),
            "status": _status("PRESENT", key, "value present"),
            "use_atoms": list(ceiling.get("use_atoms", [])),
            "dependency_refs": [_ref("WORLD_OBJECT", key)],
            "selection_record_ref": _ref("SELECTION_RECORD", f"sel:{key}"),
        })
    for key in sorted(world.get("routes", {})):
        selection_records.append({
            "demand_key": key,
            "decision": "SELECTED",
            "object_ref": _ref("WORLD_OBJECT", key),
            "native_scope_ref": _ref("NATIVE_SCOPE", world.get("native_unit", "RESPONDENT")),
            "status": _status("PRESENT", key, "route present"),
            "use_atoms": list(ceiling.get("use_atoms", [])),
            "dependency_refs": [_ref("WORLD_OBJECT", key)],
            "selection_record_ref": _ref("SELECTION_RECORD", f"sel:{key}"),
        })
    for neg in world.get("negative_states", []):
        scope = neg.get("scope", "")
        code = neg.get("state", "MISSING")
        if code == "DENIED":
            code = "DENIED_USE"
        if code not in STATUS_CODES:
            code = "MISSING"
        selection_records.append({
            "demand_key": scope,
            "decision": "SELECTED",
            "object_ref": _ref("WORLD_OBJECT", scope),
            "native_scope_ref": _ref("NATIVE_SCOPE", world.get("native_unit", "RESPONDENT")),
            "status": _status(code, scope, f"negative {code}"),
            "use_atoms": list(ceiling.get("use_atoms", [])),
            "dependency_refs": [],
            "selection_record_ref": _ref("SELECTION_RECORD", f"neg:{scope}"),
        })

    # Payloads
    payloads = []
    for key in sorted(world.get("values", {})):
        payloads.append({
            "object_ref": _ref("WORLD_OBJECT", key),
            "object_family": "OTHER_PRODUCER_OWNED",
            "payload_ref": _ref("PAYLOAD", key),
            "native_dimensions": {"unit": world.get("native_unit", "RESPONDENT")},
            "participant_roles": [],
            "f2_prerequisites": {
                "route_refs": [], "f1_refs": [], "motif_ref": _ref("MOTIF", "none"),
                "predicate_refs": [], "actor_history_requirement_refs": [],
                "unbound_requirement_refs": [],
            },
            "public_rule_refs": [],
            "contradiction_group_ref": _ref("CONTRADICTION", "none"),
            "grade": "TEST_FIXTURE_ONLY",
        })
    for key in sorted(world.get("routes", {})):
        payloads.append({
            "object_ref": _ref("WORLD_OBJECT", key),
            "object_family": "ROUTE",
            "payload_ref": _ref("PAYLOAD", key),
            "native_dimensions": {"unit": world.get("native_unit", "RESPONDENT")},
            "participant_roles": [
                {"ordinal": p.get("ordinal", 0), "role": p.get("role", ""), "participant_ref": _ref("PARTICIPANT", p.get("ref", ""))}
                for p in world.get("nary", {}).get("participants", [])
            ],
            "f2_prerequisites": {
                "route_refs": [_ref("ROUTE", r) for r in world.get("f2", {}).get("v555_routes", [])],
                "f1_refs": [_ref("F1", r) for r in world.get("f2", {}).get("f1_refs", [])],
                "motif_ref": _ref("MOTIF", world.get("f2", {}).get("motif", "")),
                "predicate_refs": [_ref("PREDICATE", world.get("f2", {}).get("predicate_ref", ""))],
                "actor_history_requirement_refs": [],
                "unbound_requirement_refs": [_ref("UNBOUND", world.get("f2_requirement_ref", ""))],
            },
            "public_rule_refs": [_ref("RULE", world.get("routes", {}).get(key, {}).get("rule_ref", ""))],
            "contradiction_group_ref": _ref("CONTRADICTION", "none"),
            "grade": "TEST_FIXTURE_ONLY",
        })

    # Native scopes
    native_scopes = [{
        "native_unit_ref": _ref("NATIVE_UNIT", world.get("native_unit", "RESPONDENT")),
        "native_geography_ref": _ref("GEOGRAPHY", "fixture-municipality"),
        "version_ref": _ref("VERSION", world.get("source_release_ref", "")),
        "original_stratum_refs": [_ref("STRATUM", s) for s in world.get("native_strata", [])],
        "absolute_horizon_refs": [_ref("AH", world.get("absolute_horizon", ""))],
    }]

    # Dependency closure
    dep_edges = []
    dep_refs = []
    for key in sorted(world.get("values", {})):
        dep_refs.append(_ref("WORLD_OBJECT", key))
        dep_edges.append({"from": _ref("DEMAND", "root"), "to": _ref("WORLD_OBJECT", key), "role": "SELECTED_VALUE"})
    for key in sorted(world.get("routes", {})):
        dep_refs.append(_ref("WORLD_OBJECT", key))
        dep_edges.append({"from": _ref("DEMAND", "root"), "to": _ref("WORLD_OBJECT", key), "role": "SELECTED_ROUTE"})
    dependency_closure = {
        "closure_ref": _ref("CLOSURE", "closure"),
        "edges": dep_edges,
        "is_demand_complete": True,
        "negative_dependencies": [],
        "dereference_capability_ref": _ref("DEREFERENCE", "lossless"),
    }

    # Generated criteria echo (H3)
    gce = world.get("generated_binding_echo", {})
    generated_criteria_echo = [{
        "tag": "GENERATED_RUNTIME_FACT_REF",
        "caller_fact_ref": {"kind": "GENERATED_RUNTIME_FACT_REF", "id": gce.get("caller_fact", ""), "hash": _sha256(gce.get("caller_fact", ""))},
        "kind": "FILTER_ONLY",
        "effective_at": axes.get("actor_event", ""),
        "binding_fingerprint": _sha256(gce),
    }]

    # Refresh (H2)
    refresh = {
        "repository_predictable_boundaries": ["H2_GENERATED_BINDING_REFRESH", "H2_PUBLICATION_BOUNDARY_REFRESH"],
        "binding_fingerprint": _sha256({"bg": selection.get("binding_generation", 0)}),
        "requery_on_binding_change": True,
        "successor_only": True,
    }

    # Issuer and use
    issuer_and_use = {
        "issuer_refs": [_ref("ISSUER", world.get("authority_ref", ""))],
        "source_allowed_use_atoms": list(ceiling.get("use_atoms", [])),
        "requested_use_atoms": list(ceiling.get("use_atoms", [])),
        "effective_use_atoms": list(ceiling.get("use_atoms", [])),
        "model_use_ref": _ref("MODEL_USE", "TEST_ONLY"),
    }

    return {
        "contract": "GENERIC_WORLD_SELECTION@1.0.0",
        "request_id": request_id,
        "receipt_ref": _ref("WORLD_RECEIPT", request_id),
        "snapshot_ref": _ref("SNAPSHOT", selection.get("selection_digest", "")),
        "demand_ref": _ref("DEMAND", json.dumps(demand, sort_keys=True)),
        "repository_refs": [_ref("REPOSITORY", world.get("source_ref", ""))],
        "native_scopes": native_scopes,
        "clock": clock,
        "selection": selection_records,
        "payloads": payloads,
        "dependency_closure": dependency_closure,
        "generated_criteria_echo": generated_criteria_echo,
        "refresh": refresh,
        "issuer_and_use": issuer_and_use,
        "grade": "TEST_FIXTURE_ONLY",
        "state": _status(state_code, "world", "selected world"),
        "values_read_refs": values_read_refs,
    }


def build_possibility_receipt(
    *,
    receipt_id: str,
    world_snapshot_ref: dict[str, str],
    possibility: Mapping[str, Any],
    values_read_refs: list[dict[str, str]],
    empirical_evidence: Mapping[str, Any] | None = None,
    state_code: str = "PRESENT",
) -> dict[str, Any]:
    """Build a strict Draft 2020-12 PossibilityReceipt (20 required fields)."""
    emp = possibility
    chain = emp.get("ordered_condition_chain", [])
    support = dict(emp.get("support", {}))
    if empirical_evidence and empirical_evidence.get("support"):
        support.update(empirical_evidence["support"])

    ordered_steps = []
    for row in chain:
        ordered_steps.append({
            "step_index": row.get("index", 0),
            "parent_receipt_ref": _ref("POSSIBILITY_RECEIPT", f"parent:{row.get('index', 0)}") if row.get("index", 0) > 0 else None,
            "new_binding": {
                "binding_ref": _ref("BINDING", row.get("ref", "")),
                "origin": "SOURCE_FACT",
                "subject_fact_ref": _ref("SUBJECT_FACT", row.get("ref", "")),
                "coordinate_ref": _ref("COORDINATE", row.get("ref", "")),
                "comparability_authority_ref": _ref("COMPARABILITY", "fixture"),
                "universe_ref": _ref("SOURCE_UNIVERSE", emp.get("universe", "")),
                "release_ref": _ref("RELEASE", emp.get("release", "")),
            },
            "empirical_query_ref": _ref("EMPIRICAL_QUERY", row.get("ref", "")),
            "cumulative_binding_refs": [_ref("BINDING", r.get("ref", "")) for r in chain if r.get("index", 0) <= row.get("index", 0)],
            "retained_binding_refs": [_ref("BINDING", r.get("ref", "")) for r in chain if r.get("index", 0) <= row.get("index", 0)],
            "dropped_binding_refs": [],
            "denominator_ref": _ref("DENOMINATOR", emp.get("risk_set", "")),
            "support": {
                "raw_numerator": row.get("n"),
                "raw_denominator": support.get("denominator", row.get("n")),
                "weight_ref": _ref("WEIGHT", emp.get("weight", "")),
                "risk_set_ref": _ref("RISK_SET", emp.get("risk_set", "")),
                "sampling_design_ref": _ref("SAMPLING_DESIGN", emp.get("weight", "")),
            },
            "result_state": _status("PRESENT", row.get("ref", ""), "step computed"),
            "uncertainty_ref": _ref("UNCERTAINTY", emp.get("uncertainty", "")),
            "evidence_ref": _ref("EVIDENCE", row.get("ref", "")),
        })

    options = []
    cells = emp.get("cells", [])
    if not cells and support.get("target_yes") is not None:
        # Derive options from support block when cells are absent
        cells = [
            {"value": "YES", "n": support.get("target_yes")},
            {"value": "NO", "n": support.get("target_no")},
        ]
    for c in cells:
        options.append({
            "value_ref": _ref("VALUE", c.get("value", "")),
            "support_state": _status("PRESENT", c.get("value", ""), f"cell {c.get('value')}"),
        })

    alternatives = {
        "minority_refs": [_ref("MINORITY", emp.get("minority", ""))] if emp.get("minority") else [],
        "counterpattern_refs": [],
        "contradiction_refs": [_ref("CONTRADICTION", a.get("id", "")) for a in emp.get("contradictory_alternatives", [])],
        "unknown_refs": [],
    }

    model_and_use = {
        "model_rule_ref": _ref("MODEL_RULE", "EXACT_CONDITIONAL_WITH_GOVERNED_WALKBACK"),
        "model_authority_ref": _ref("MODEL_AUTHORITY", emp.get("model_use", "TEST_ONLY")),
        "use_grant_ref": _ref("USE_GRANT", "fixture-only"),
        "estimand_ref": _ref("ESTIMAND", emp.get("target", "")),
        "nonresponse_ref": _ref("NONRESPONSE", emp.get("routing", "")),
        "uncertainty_ref": _ref("UNCERTAINTY", emp.get("uncertainty", "")),
    }

    return {
        "contract": "GENERIC_ORDERED_POSSIBILITY@1.0.0",
        "receipt_ref": _ref("POSSIBILITY_RECEIPT", receipt_id),
        "world_snapshot_ref": world_snapshot_ref,
        "world_binding_requirement": "N10E_ALONE",
        "target_ref": _ref("TARGET", emp.get("target", "")),
        "direction": "FORWARD_CONDITIONAL" if emp.get("direction", "").startswith("FORWARD") else "REVERSE_CONDITIONAL",
        "source_universe_ref": _ref("SOURCE_UNIVERSE", emp.get("universe", "")),
        "release_ref": _ref("RELEASE", emp.get("release", "")),
        "same_respondent_joint_ref": _ref("SAME_RESPONDENT_JOINT", emp.get("sampling_unit", "")),
        "sampling_unit_ref": _ref("SAMPLING_UNIT", emp.get("sampling_unit", "")),
        "response_routing_ref": _ref("RESPONSE_ROUTING", emp.get("routing", "")),
        "options": options,
        "ordered_steps": ordered_steps,
        "model_and_use": model_and_use,
        "composition_mode": "EXACT_SOURCE_JOINT",
        "alternatives": alternatives,
        "epistemic_grade": "TEST_FIXTURE_ONLY",
        "state": _status(state_code, "possibility", "computed possibility"),
        "values_read_refs": values_read_refs,
        "replay_ref": _ref("REPLAY", emp.get("replay_digest", receipt_id)),
    }
