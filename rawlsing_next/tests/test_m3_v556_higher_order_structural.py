from __future__ import annotations

import copy
import hashlib

import pytest

from rawlsing_next.m2_v555_atomic_route import M2_CONTRACT_ID, M2DecisionState, M2Evaluation, SEMANTIC_FAMILY as V555_FAMILY, semantic_hash
from rawlsing_next.m3_v556_higher_order_structural import (
    M3DecisionState,
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


def _rule(*, order="ORDERED", roles=("CAUSE", "EFFECT"), minc=2, maxc=2, reuse="FORBIDDEN", family="V556_INTERACTION_RELATION"):
    return {
        "authority_id": "V556_TEST_AUTHORITY",
        "authority_version": "1.0.0",
        "authority_content_hash": _h("v556-authority"),
        "rule_id": "V556-TEST-RULE",
        "rule_version": "1.0.0",
        "rule_content_hash": _h("v556-rule"),
        "semantic_family": family,
        "participant_roles": list(roles),
        "participant_order_policy": order,
        "minimum_cardinality": minc,
        "maximum_cardinality_or_unbounded_marker": maxc,
        "multiplicity_policy": "EXACT_OCCURRENCE_INDEX",
        "same_route_reuse_policy": reuse,
        "source_composition_policy": "NONE_BY_DEFAULT",
        "allowed_typed_outcome_states": ["SUPPORTED", "VALID_EMPTY", "DENIED", "NONCOMPARABLE", "CONFLICTING_AUTHORITY"],
        "producer_allowed_uses": ["M3_USE"],
    }


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


def _request(rule, bindings, *, state="SUPPORTED", payload=None, composition=None):
    return {
        "higher_order_semantics_required": True,
        "rule_authority": rule,
        "participant_bindings": bindings,
        "source_composition_authority": composition,
        "governed_result": {"state": state, "semantic_payload": payload if payload is not None else {"relation_kind": "TEST_HIGHER_ORDER"}},
        "intended_use": "M3_USE",
    }


def _eval(upstream, request, *, comp_keys=()):
    return evaluate_m3_v556_higher_order_structural(upstream, request, active_rule_keys=[_rule_key(request["rule_authority"])], active_source_composition_keys=comp_keys)


def test_fewer_than_two_participant_occurrences_fails_closed():
    a = _m2("a"); rule = _rule()
    x = _eval([a], _request(rule, [_bind(a, "CAUSE", 1)]))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and x.v556_object is None


def test_repeated_route_cannot_fake_two_distinct_route_floor_even_when_reuse_permitted():
    a = _m2("a"); rule = _rule(reuse="PERMITTED")
    bindings = [_bind(a, "CAUSE", 1, multiplicity=0), _bind(a, "EFFECT", 2, multiplicity=1)]
    x = _eval([a], _request(rule, bindings))
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET and "two distinct" in x.reason


def test_two_distinct_routes_require_exact_active_v556_authority():
    a, b = _m2("a"), _m2("b"); rule = _rule(); req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)])
    blocked = evaluate_m3_v556_higher_order_structural([a, b], req)
    assert blocked.decision_state is M3DecisionState.UNKNOWN_AUTHORITY and blocked.v556_object is None
    ok = _eval([a, b], req)
    assert ok.decision_state is M3DecisionState.SUPPORTED and ok.v556_object["object_id"].startswith("urn:rawlsing:v556:higher-order:sha256:")


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


def test_actor_persona_render_payload_is_outside_m3_jurisdiction():
    a, b = _m2("a"), _m2("b"); rule = _rule(); req = _request(rule, [_bind(a, "CAUSE", 1), _bind(b, "EFFECT", 2)], payload={"actor_state": "x"})
    x = _eval([a, b], req)
    assert x.decision_state is M3DecisionState.DENIED and x.v556_object is None
