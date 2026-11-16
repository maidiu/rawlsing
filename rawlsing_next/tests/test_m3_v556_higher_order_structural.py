from __future__ import annotations

import copy
import hashlib

import pytest

from rawlsing_next.m2_v555_atomic_route import (
    M2_CONTRACT_ID,
    M2DecisionState,
    M2Evaluation,
    SEMANTIC_FAMILY as V555_FAMILY,
    semantic_hash,
)
from rawlsing_next.m3_v556_higher_order_structural import (
    ACTOR_INDEXING_MODES,
    M3_CONTRACT_ID,
    M3DecisionState,
    PERSON_STATE_SEMANTICS,
    RESULT_CONTRACT_BINDING_REF_KIND,
    RESULT_JURISDICTION,
    RESULT_SCHEMA_REF_KIND,
    ZERO_V556_OBJECTS,
    evaluate_m3_v556_higher_order_structural,
)


def _h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def _ref(kind: str, oid: str) -> dict[str, str]:
    return {"kind": kind, "object_id": oid, "content_hash": _h(oid)}


def _m2(seed: str, *, uses=("M3_USE",), state=M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED, handoff=None):
    if state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED:
        return M2Evaluation(M2_CONTRACT_ID, state, "x", "ELIGIBLE", None, None, (), None, None, None, {}, handoff, None)
    f1 = {"kind": "F1", "object_id": f"urn:rawlsing:v554:f1:sha256:{_h('f1:'+seed)}", "content_hash": _h("f1-content:"+seed)}
    b1 = {"kind": "B1", "object_id": f"urn:rawlsing:v554:b1:sha256:{_h('b1:'+seed)}", "content_hash": _h("b1-content:"+seed)}
    ident = (
        f1["object_id"],
        "V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL@1.0.0",
        "V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER@1.0.0",
        "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL",
        _ref("StructuralChannel", "channel:"+seed),
        "V555-RC-001-EXACT-STRUCTURAL-POSITION-REF",
        _ref("StructuralPosition", "receiver:"+seed),
    )
    ih = semantic_hash(list(ident))
    route = {
        "semantic_family": V555_FAMILY,
        "route_id": f"urn:rawlsing:v555:route:sha256:{ih}",
        "canonical_route_identity": ident,
        "canonical_route_identity_hash": ih,
        "exact_v554_f1_ref": f1,
        "exact_v554_b1_ref": b1,
        "inherited_v554_f2_refs": (),
        "producer_allowed_uses": tuple(uses),
        "actor_independent": True,
    }
    return M2Evaluation(M2_CONTRACT_ID, state, "ok", "ELIGIBLE", f1, b1, (), ident, ih, route, {}, handoff, _h("replay:"+seed))


def _route_ref(m2):
    return {"kind": V555_FAMILY, "object_id": m2.route["route_id"], "content_hash": semantic_hash(m2.route)}


def _string(role, allowed="UNBOUNDED"):
    return {
        "type": "string",
        "semantic_role": role,
        "allowed_values_or_unbounded_marker": allowed,
    }


def _object(fields, required, role="OBJECTIVE_GROUPING"):
    return {
        "type": "object",
        "semantic_role": role,
        "fields": fields,
        "required": list(required),
        "additional_fields": False,
    }


def _array(items, *, minimum=0, maximum="UNBOUNDED", role="OBJECTIVE_GROUPING"):
    return {
        "type": "array",
        "semantic_role": role,
        "items": items,
        "min_items": minimum,
        "max_items_or_unbounded_marker": maximum,
    }


def _schema_structural(*, extra_fields=None, required_extra=(), schema_id="HOSTILE_FIXTURE_OBJECTIVE_STRUCTURAL_RESULT"):
    fields = {
        "relation_kind": _string("OBJECTIVE_STRUCTURAL_RELATION"),
    }
    if extra_fields:
        fields.update(extra_fields)
    return {
        "schema_id": schema_id,
        "schema_version": "1.0.0",
        "semantic_class": "OBJECTIVE_STRUCTURAL_RESULT",
        "root": _object(fields, ("relation_kind", *required_extra)),
    }


def _schema_actor_position(*, position_values=("EMPLOYEE_OF",), schema_id="HOSTILE_FIXTURE_OBJECTIVE_ACTOR_POSITION"):
    return {
        "schema_id": schema_id,
        "schema_version": "1.0.0",
        "semantic_class": "OBJECTIVE_ACTOR_POSITION",
        "root": _object(
            {
                "actor_ref": _string("OBJECTIVE_ACTOR_INDEX"),
                "institution_ref": _string("OBJECTIVE_INSTITUTION"),
                "position_kind": _string("OBJECTIVE_POSITION", list(position_values)),
            },
            ("actor_ref", "institution_ref", "position_kind"),
        ),
    }


def _schema_actor_opportunity():
    return {
        "schema_id": "HOSTILE_FIXTURE_OBJECTIVE_ACTOR_OPPORTUNITY",
        "schema_version": "1.0.0",
        "semantic_class": "OBJECTIVE_ACTOR_OPPORTUNITY",
        "root": _object(
            {
                "actor_ref": _string("OBJECTIVE_ACTOR_INDEX"),
                "opportunity_ref": _string("OBJECTIVE_OPPORTUNITY"),
                "availability_state": _string("OBJECTIVE_STATUS", ["AVAILABLE", "UNAVAILABLE"]),
            },
            ("actor_ref", "opportunity_ref", "availability_state"),
        ),
    }


def _schema_ref(schema):
    return {
        "kind": RESULT_SCHEMA_REF_KIND,
        "object_id": f"{schema['schema_id']}@{schema['schema_version']}",
        "content_hash": semantic_hash(schema),
    }


def _binding(
    *,
    rule_id,
    rule_version,
    schema,
    actor_mode="NO_ACTOR_INDEX",
    authorization_state="AUTHORIZED_CURRENT",
    tag="base",
):
    assert actor_mode in ACTOR_INDEXING_MODES
    schema_ref = _schema_ref(schema)
    owner_ref = _ref("M3_RESULT_SEMANTIC_OWNER", f"owner:{tag}")
    owner_current_ref = _ref("M3_RESULT_OWNER_CURRENT_SELECTION", f"owner-current:{tag}")
    material = {
        "contract_id": M3_CONTRACT_ID,
        "binding_id": f"M3-RESULT-BINDING-{tag}",
        "binding_version": "1.0.0",
        "authorization_state": authorization_state,
        "bound_rule_id": rule_id,
        "bound_rule_version": rule_version,
        "result_schema_ref": schema_ref,
        "result_semantic_owner_ref": owner_ref,
        "result_semantic_owner_current_selection_ref": owner_current_ref,
        "semantic_jurisdiction": RESULT_JURISDICTION,
        "actor_indexing_mode": actor_mode,
        "person_state_semantics": PERSON_STATE_SEMANTICS,
        "result_schema": schema,
    }
    binding_hash = semantic_hash(material)
    binding = {
        key: value for key, value in material.items() if key != "contract_id"
    }
    binding["binding_content_hash"] = binding_hash
    binding_ref = {
        "kind": RESULT_CONTRACT_BINDING_REF_KIND,
        "object_id": f"{binding['binding_id']}@{binding['binding_version']}",
        "content_hash": binding_hash,
    }
    return binding, binding_ref


class _Rule(dict):
    result_contract: dict
    result_contract_ref: dict


def _rule(
    *,
    order="ORDERED",
    roles=("CAUSE", "EFFECT"),
    minc=2,
    maxc=2,
    reuse="FORBIDDEN",
    family="V556_INTERACTION_RELATION",
    schema=None,
    actor_mode="NO_ACTOR_INDEX",
    authorization_state="AUTHORIZED_CURRENT",
    tag="base",
):
    rule_id = f"V556-TEST-RULE-{tag}"
    rule_version = "2.0.0"
    schema = schema or _schema_structural(schema_id=f"TEST_STRUCTURAL_{tag}")
    result_contract, result_ref = _binding(
        rule_id=rule_id,
        rule_version=rule_version,
        schema=schema,
        actor_mode=actor_mode,
        authorization_state=authorization_state,
        tag=tag,
    )
    body_material = {
        "contract_id": M3_CONTRACT_ID,
        "rule_id": rule_id,
        "rule_version": rule_version,
        "semantic_family": family,
        "participant_roles": list(roles),
        "participant_order_policy": order,
        "minimum_cardinality": minc,
        "maximum_cardinality_or_unbounded_marker": maxc,
        "multiplicity_policy": "EXACT_OCCURRENCE_INDEX",
        "same_route_reuse_policy": reuse,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": sorted({"SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "CONFLICTING_AUTHORITY"}),
        "producer_allowed_uses": ["M3_USE"],
        "result_contract_binding_ref": result_ref,
    }
    rule = _Rule(
        authority_id="V556_TEST_AUTHORITY",
        authority_version="2.0.0",
        authority_content_hash=_h(f"v556-authority:{tag}"),
        rule_id=rule_id,
        rule_version=rule_version,
        rule_content_hash=semantic_hash(body_material),
        semantic_family=family,
        participant_roles=list(roles),
        participant_order_policy=order,
        minimum_cardinality=minc,
        maximum_cardinality_or_unbounded_marker=maxc,
        multiplicity_policy="EXACT_OCCURRENCE_INDEX",
        same_route_reuse_policy=reuse,
        source_composition_policy="NONE_BY_DEFAULT",
        allowed_typed_outcome_states=["SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "CONFLICTING_AUTHORITY"],
        producer_allowed_uses=["M3_USE"],
        result_contract_binding_ref=result_ref,
    )
    rule.result_contract = result_contract
    rule.result_contract_ref = result_ref
    return rule


def _rule_key(rule):
    return tuple(rule[k] for k in ("authority_id", "authority_version", "authority_content_hash", "rule_id", "rule_version", "rule_content_hash"))


def _bind(m2, role, ordinal, *, multiplicity=0, source="source:1"):
    return {
        "v555_route_identity_ref": _route_ref(m2),
        "role": role,
        "ordinal_or_null": ordinal,
        "multiplicity_index": multiplicity,
        "source_universe_ref": _ref("SourceUniverse", source),
    }


def _request(rule, bindings, *, state="SUPPORTED", payload=None, composition=None, result_contract=None):
    return {
        "higher_order_semantics_required": True,
        "rule_authority": rule,
        "participant_bindings": bindings,
        "source_composition_authority": composition,
        "result_contract_binding": result_contract if result_contract is not None else rule.result_contract,
        "governed_result": {
            "state": state,
            "semantic_payload": payload if payload is not None else {"relation_kind": "TEST_HIGHER_ORDER"},
        },
        "intended_use": "M3_USE",
    }


def _eval(upstream, request, *, comp_keys=(), result_refs=None):
    rule = request["rule_authority"]
    if result_refs is None:
        result_refs = [rule.result_contract_ref]
    return evaluate_m3_v556_higher_order_structural(
        upstream,
        request,
        active_rule_keys=[_rule_key(rule)],
        active_source_composition_keys=comp_keys,
        active_result_contract_refs=result_refs,
    )


def test_fewer_than_two_participant_occurrences_fails_closed():
    a = _m2("a"); rule = _rule()
    x = _eval([a], _request(rule, [_bind(a, "CAUSE", 1)]))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and x.v556_object is None


def test_repeated_route_cannot_fake_two_distinct_route_floor_even_when_reuse_permitted():
    a = _m2("a"); rule = _rule(reuse="PERMITTED")
    bindings = [_bind(a, "CAUSE", 1, multiplicity=0), _bind(a, "EFFECT", 2, multiplicity=1)]
    x = _eval([a], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and "two distinct" in x.reason


def test_two_distinct_routes_require_exact_active_v556_and_result_contract_authority():
    a, b = _m2("a"), _m2("b"); rule = _rule(); req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)])
    blocked = evaluate_m3_v556_higher_order_structural(
        [a, b], req, active_result_contract_refs=[rule.result_contract_ref]
    )
    assert blocked.decision_state is M3DecisionState.UNKNOWN_AUTHORITY and blocked.v556_object is None
    missing_result = evaluate_m3_v556_higher_order_structural(
        [a, b], req, active_rule_keys=[_rule_key(rule)]
    )
    assert missing_result.decision_state is M3DecisionState.INTEGRITY_FAILURE and missing_result.v556_object is None
    ok = _eval([a, b], req)
    assert ok.decision_state is M3DecisionState.SUPPORTED
    assert ok.v556_object["object_id"].startswith("urn:rawlsing:v556:higher-order:sha256:")
    assert ok.v556_object["result_schema_ref"] == rule.result_contract["result_schema_ref"]
    assert ok.v556_object["semantic_jurisdiction"] == RESULT_JURISDICTION
    assert ok.v556_object["person_state_absent"] is True


@pytest.mark.parametrize("mutator", ["role", "order", "cardinality", "multiplicity"])
def test_role_order_cardinality_and_multiplicity_mismatches_fail_closed(mutator):
    a, b, c = _m2("a"), _m2("b"), _m2("c"); rule = _rule(); bindings = [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)]
    upstream = [a, b]
    if mutator == "role": bindings[1]["role"] = "UNKNOWN_ROLE"
    elif mutator == "order": bindings[1]["ordinal_or_null"] = 1
    elif mutator == "cardinality": bindings.append(_bind(c, "EFFECT", 3)); upstream.append(c)
    else: bindings[0]["multiplicity_index"] = 2
    x = _eval(upstream, _request(rule, bindings))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and x.v556_object is None


def test_same_route_reuse_without_exact_permission_fails_closed():
    a, b = _m2("a"), _m2("b"); rule = _rule(order="UNORDERED", roles=("NODE",), minc=3, maxc="UNBOUNDED", reuse="FORBIDDEN")
    bindings = [_bind(a, "NODE", None, multiplicity=0), _bind(a, "NODE", None, multiplicity=1), _bind(b, "NODE", None)]
    x = _eval([a, b], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and "reuse" in x.reason


def test_exact_permitted_reuse_is_occurrence_metadata_not_new_route_identity():
    a, b = _m2("a"), _m2("b"); rule = _rule(order="UNORDERED", roles=("NODE",), minc=3, maxc="UNBOUNDED", reuse="PERMITTED")
    bindings = [_bind(a, "NODE", None, multiplicity=0), _bind(a, "NODE", None, multiplicity=1), _bind(b, "NODE", None)]
    x = _eval([a, b], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.SUPPORTED
    refs = [z["v555_route_identity_ref"]["object_id"] for z in x.canonical_participant_bindings]
    assert refs.count(a.route["route_id"]) == 2 and len(set(refs)) == 2


def _composition(bindings, decision="AUTHORIZED"):
    return {
        "authority_id": "COMPOSE",
        "authority_version": "1.0.0",
        "authority_content_hash": _h("compose"),
        "operation_id": "COMPOSE-ROUTES",
        "covered_source_universe_refs": [x["source_universe_ref"] for x in bindings],
        "covered_participant_bindings": [{k: x[k] for k in ("v555_route_identity_ref", "role", "ordinal_or_null", "multiplicity_index")} for x in bindings],
        "compatibility_scope": "EXACT_PARTICIPANTS",
        "decision": decision,
    }


def _comp_key(c):
    return tuple(c[k] for k in ("authority_id", "authority_version", "authority_content_hash", "operation_id"))


def test_cross_source_composition_is_none_by_default_and_adjacency_never_authorizes_it():
    a, b = _m2("a"), _m2("b"); rule = _rule(); bindings = [_bind(a, "CAUSE", 1, source="source:a"), _bind(b, "EFFECT", 2, source="source:b")]
    x = _eval([a, b], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.UNKNOWN_AUTHORITY and x.v556_object is None
    comp = _composition(bindings)
    ok = _eval([a, b], _request(rule, bindings, composition=comp), comp_keys=[_comp_key(comp)])
    assert ok.decision_state is M3DecisionState.SUPPORTED


def test_b1_f2_raw_v554_material_cannot_substitute_for_v555_route_identity():
    a, b = _m2("a"), _m2("b"); rule = _rule(); bindings = [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)]
    dirty = copy.deepcopy(bindings); dirty[0]["B1"] = a.exact_v554_b1_ref
    x = _eval([a, b], _request(rule, dirty))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET
    raw = evaluate_m3_v556_higher_order_structural([{"F1": "raw"}], {"higher_order_semantics_required": False})
    assert raw.decision_state is M3DecisionState.UNRESOLVABLE_PARTICIPANT


def test_route_reid_or_reconstruction_is_rejected_even_when_visible_labels_match():
    a, b = _m2("a"), _m2("b"); rule = _rule(); bindings = [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)]
    bindings[0]["v555_route_identity_ref"]["object_id"] = "urn:rawlsing:v555:route:sha256:" + _h("re-id")
    x = _eval([a, b], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.UNRESOLVABLE_PARTICIPANT and x.v556_object is None


def test_valid_empty_or_zero_upstream_never_creates_filler_v556_object():
    empty = _m2("empty", state=M2DecisionState.VALID_EMPTY)
    x = evaluate_m3_v556_higher_order_structural([empty], {"higher_order_semantics_required": False})
    assert x.decision_state is None and x.behavior == ZERO_V556_OBJECTS and x.v556_object is None


def test_governed_valid_empty_preserves_typed_state_without_positive_object():
    a, b = _m2("a"), _m2("b"); rule = _rule(); req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], state="VALID_EMPTY", payload=None)
    x = _eval([a, b], req)
    assert x.decision_state is M3DecisionState.VALID_EMPTY and x.v556_object is None


def test_replay_is_deterministic_for_exact_governed_inputs():
    a, b = _m2("a"), _m2("b"); rule = _rule(); req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)])
    x = _eval([a, b], copy.deepcopy(req)); y = _eval([a, b], copy.deepcopy(req))
    assert x == y and x.replay_key_hash == y.replay_key_hash


def test_m3_does_not_disturb_lawful_direct_v555_v557_path_when_not_required():
    handoff = {"handoff_id": "direct:1", "route": "V555_TO_V557_DIRECT"}
    a = _m2("a", handoff=handoff)
    x = evaluate_m3_v556_higher_order_structural([a], {"higher_order_semantics_required": False})
    assert x.behavior == ZERO_V556_OBJECTS and x.v556_object is None and x.passthrough_v555_v557_handoffs == (handoff,)


@pytest.mark.parametrize(
    "payload",
    [
        {"psychometric_type": 4, "motivation": "approval"},
        {"subject_ref": "urn:audit:subject:1", "preference": "deference", "psychological_trait": "submissive"},
        {"relation_kind": "TEST_HIGHER_ORDER", "attributes": {"drive": "approval", "temperament": "submissive"}},
        {"relation_kind": "TEST_HIGHER_ORDER", "semantic_class": "psychological_trait", "value": "submissive"},
        {"p_type": 4, "goal": "approval"},
    ],
)
def test_hostile_person_semantic_aliases_fail_closed_by_schema_not_key_blacklist(payload):
    a, b = _m2("a"), _m2("b")
    schema = _schema_structural(
        extra_fields={
            "semantic_class": _string("OBJECTIVE_TEXT_LABEL", ["STRUCTURAL_RELATION"]),
            "value": _string("OBJECTIVE_TEXT_LABEL"),
        }
    )
    rule = _rule(schema=schema, tag="hostile-structural")
    x = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload))
    assert x.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING
    assert x.v556_object is None


def test_lawful_non_actor_structural_positive_control():
    a, b = _m2("a"), _m2("b")
    schema = _schema_structural(
        extra_fields={
            "condition_ref": _string("OBJECTIVE_CONSTRAINT"),
            "constraint_ref": _string("OBJECTIVE_CONSTRAINT"),
        },
        required_extra=("condition_ref", "constraint_ref"),
    )
    rule = _rule(schema=schema, tag="h06")
    payload = {
        "relation_kind": "TEST_HIGHER_ORDER",
        "condition_ref": "urn:audit:condition:1",
        "constraint_ref": "urn:audit:constraint:1",
    }
    x = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload))
    assert x.decision_state is M3DecisionState.SUPPORTED
    assert x.v556_object["actor_indexing_mode"] == "NO_ACTOR_INDEX"


def test_lawful_objective_actor_indexed_position_positive_control_preserves_actor_identifier():
    a, b = _m2("a"), _m2("b")
    rule = _rule(schema=_schema_actor_position(), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="h07")
    payload = {
        "actor_ref": "urn:audit:actor:1",
        "institution_ref": "urn:audit:institution:1",
        "position_kind": "EMPLOYEE_OF",
    }
    x = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload))
    assert x.decision_state is M3DecisionState.SUPPORTED
    assert x.v556_object["actor_indexing_mode"] == "OBJECTIVE_ACTOR_INDEXED"
    assert x.v556_object["semantic_payload"]["actor_ref"] == "urn:audit:actor:1"
    assert x.v556_object["person_state_absent"] is True


def test_lawful_objective_actor_opportunity_passes_but_uptake_laundering_fails():
    a, b = _m2("a"), _m2("b")
    rule = _rule(schema=_schema_actor_opportunity(), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="h08")
    base = {
        "actor_ref": "urn:audit:actor:1",
        "opportunity_ref": "urn:audit:opportunity:1",
        "availability_state": "AVAILABLE",
    }
    ok = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=base))
    assert ok.decision_state is M3DecisionState.SUPPORTED
    bad = dict(base); bad["uptake"] = "accepted"
    rejected = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=bad))
    assert rejected.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING
    assert rejected.v556_object is None


def test_nested_arrays_are_schema_walked_recursively_and_unknown_person_alias_is_rejected():
    a, b = _m2("a"), _m2("b")
    item = _object(
        {
            "actor_ref": _string("OBJECTIVE_ACTOR_INDEX"),
            "status": _string("OBJECTIVE_STATUS", ["OPEN", "CLOSED"]),
        },
        ("actor_ref", "status"),
    )
    schema = _schema_structural(
        extra_fields={"routes": _array(item, minimum=1)},
        required_extra=("routes",),
        schema_id="NESTED_OBJECTIVE_ROUTES",
    )
    rule = _rule(schema=schema, actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="nested")
    base = {"relation_kind": "TEST_HIGHER_ORDER", "routes": [{"actor_ref": "urn:a:1", "status": "OPEN"}]}
    assert _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=base)).decision_state is M3DecisionState.SUPPORTED
    bad = copy.deepcopy(base); bad["routes"][0]["motivation"] = "approval"
    rejected = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=bad))
    assert rejected.decision_state is M3DecisionState.RESULT_SCHEMA_NONCONFORMING


def test_missing_or_unresolvable_exact_result_binding_fails_closed_without_default_schema():
    a, b = _m2("a"), _m2("b"); rule = _rule(tag="missing-binding")
    req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)])
    missing = dict(req); missing.pop("result_contract_binding")
    x = _eval([a, b], missing)
    assert x.decision_state is M3DecisionState.UNKNOWN_AUTHORITY and x.v556_object is None
    inactive = evaluate_m3_v556_higher_order_structural(
        [a, b], req, active_rule_keys=[_rule_key(rule)], active_result_contract_refs=[]
    )
    assert inactive.decision_state is M3DecisionState.INTEGRITY_FAILURE and inactive.v556_object is None


def test_schema_ref_hash_mismatch_is_integrity_failure_not_fallback():
    a, b = _m2("a"), _m2("b"); rule = _rule(tag="bad-schema-ref")
    binding = copy.deepcopy(rule.result_contract)
    binding["result_schema_ref"]["content_hash"] = "0" * 64
    req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], result_contract=binding)
    x = _eval([a, b], req)
    assert x.decision_state is M3DecisionState.INTEGRITY_FAILURE and x.v556_object is None


def test_stale_result_contract_is_typed_noncurrent_and_never_positive():
    a, b = _m2("a"), _m2("b")
    rule = _rule(authorization_state="STALE", tag="stale")
    x = _eval([a, b], _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)]))
    assert x.decision_state is M3DecisionState.RESULT_CONTRACT_NOT_CURRENT
    assert x.v556_object is None


def test_result_contract_identity_is_committed_to_replay_and_rule_identity():
    a, b = _m2("a"), _m2("b")
    payload = {
        "actor_ref": "urn:audit:actor:1",
        "institution_ref": "urn:audit:institution:1",
        "position_kind": "EMPLOYEE_OF",
    }
    narrow = _rule(schema=_schema_actor_position(position_values=("EMPLOYEE_OF",), schema_id="ACTOR_POSITION_NARROW"), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="identity-a")
    broad = _rule(schema=_schema_actor_position(position_values=("EMPLOYEE_OF", "MEMBER_OF"), schema_id="ACTOR_POSITION_BROAD"), actor_mode="OBJECTIVE_ACTOR_INDEXED", tag="identity-b")
    xa = _eval([a, b], _request(narrow, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload))
    xb = _eval([a, b], _request(broad, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload=payload))
    assert xa.decision_state is xb.decision_state is M3DecisionState.SUPPORTED
    assert xa.replay_key_hash != xb.replay_key_hash
    assert xa.v556_object["object_id"] != xb.v556_object["object_id"]
    assert narrow["rule_content_hash"] != broad["rule_content_hash"]
