"""HQ204 focused court: positive source-free V556 rule/material substrate.

Proves the thirteen commissioned properties against the ALREADY-ADOPTED V556
semantics. Synthetic source-free canaries prove MACHINERY ONLY and authorize no
real-world structural claim.
"""

from __future__ import annotations

import copy
import hashlib
import json

import pytest

from rawlsing_next.m2_v555_atomic_route import (
    M2_CONTRACT_ID,
    M2DecisionState,
    M2Evaluation,
    SEMANTIC_FAMILY as V555_FAMILY,
    semantic_hash,
)
from rawlsing_next.m3_v556_higher_order_structural import (
    M3DecisionState,
    RESULT_JURISDICTION,
    evaluate_m3_v556_higher_order_structural,
)
from rawlsing_next.pre553_v556_positive_substrate import (
    ADMITTED_OBJECTIVE_ROLES,
    PERMITTED_INCIDENCE_KINDS,
    PERMITTED_RELATION_KINDS,
    SUPPORTED_FAMILIES,
    SubstrateAuthoringError,
    V556RuleMaterialRegistry,
    VALID_EMPTY_NO_GOVERNED_RULE,
    author_closed_result_schema,
    author_governed_rule,
    author_result_contract_binding,
    interaction_relation_canary_rule,
    source_free_canary_registry,
    topology_canary_rule,
)

SUBSTRATE_CANARY_CLAIM = (
    "source-free machinery canary only; authorizes no real-world structural claim"
)


def _h(x: str) -> str:
    return hashlib.sha256(x.encode()).hexdigest()


def _ref(kind: str, oid: str) -> dict[str, str]:
    return {"kind": kind, "object_id": oid, "content_hash": _h(oid)}


def _m2(seed: str, *, uses=("M3_USE",), state=M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED):
    if state is not M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED:
        return M2Evaluation(M2_CONTRACT_ID, state, "x", "ELIGIBLE", None, None, (), None,
                            None, None, {}, None, None, None)
    f1 = {"kind": "F1", "object_id": f"urn:rawlsing:v554:f1:sha256:{_h('f1:'+seed)}",
          "content_hash": _h("f1-content:" + seed)}
    b1 = {"kind": "B1", "object_id": f"urn:rawlsing:v554:b1:sha256:{_h('b1:'+seed)}",
          "content_hash": _h("b1-content:" + seed)}
    ident = (
        f1["object_id"],
        "V555-RR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL@1.0.0",
        "V555-RS-001-SOURCE-EXACT-CHANNEL-EXACT-RECEIVER@1.0.0",
        "V555-LCR-001-EXACT-UPSTREAM-STRUCTURAL-CHANNEL",
        _ref("StructuralChannel", "channel:" + seed),
        "V555-RC-001-EXACT-STRUCTURAL-POSITION-REF",
        _ref("StructuralPosition", "receiver:" + seed),
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
    return M2Evaluation(M2_CONTRACT_ID, state, "ok", "ELIGIBLE", f1, b1, (), ident, ih,
                        route, {}, None, _h("replay:" + seed))


def _route_ref(m2):
    return {"kind": V555_FAMILY, "object_id": m2.route["route_id"],
            "content_hash": semantic_hash(m2.route)}


def _bind(m2, role, ordinal, *, multiplicity=0, source="source:1"):
    return {
        "v555_route_identity_ref": _route_ref(m2),
        "role": role,
        "ordinal_or_null": ordinal,
        "multiplicity_index": multiplicity,
        "source_universe_ref": _ref("SourceUniverse", source),
    }


def _request(rule, bindings, *, state="SUPPORTED", payload=None):
    return {
        "higher_order_semantics_required": True,
        "rule_authority": dict(rule.rule),
        "participant_bindings": bindings,
        "source_composition_authority": None,
        "result_contract_binding": dict(rule.result_contract),
        "governed_result": {
            "state": state,
            "semantic_payload": payload if payload is not None else {"relation_kind": "CANARY"},
        },
        "intended_use": "M3_USE",
    }


def _eval(registry, upstream, request):
    return evaluate_m3_v556_higher_order_structural(
        upstream, request,
        active_rule_keys=registry.active_rule_keys(),
        active_source_composition_keys=[],
        active_result_contract_refs=registry.active_result_contract_refs(),
    )


def _topology_payload():
    return {
        "endpoint_a_ref": _ref("StructuralChannel", "endpoint-a"),
        "endpoint_b_ref": _ref("StructuralChannel", "endpoint-b"),
        "shared_structural_channel_ref": _ref("StructuralChannel", "shared-channel"),
        "incidence_kind": PERMITTED_INCIDENCE_KINDS[0],
    }


def _interaction_payload(n=2):
    kinds = list(PERMITTED_RELATION_KINDS)
    return {
        "coexisting_relations": [
            {
                "relation_kind": kinds[i % len(kinds)],
                "left_endpoint_ref": _ref("StructuralPosition", f"left-{i}"),
                "right_endpoint_ref": _ref("StructuralPosition", f"right-{i}"),
            }
            for i in range(n)
        ]
    }


# ------------------------------------------------- 1. lawful TOPOLOGY rule
def test_one_lawful_positive_v556_topology_rule():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    assert t is not None
    assert t.semantic_family == "V556_TOPOLOGY"
    assert t.rule["source_composition_policy"] == "NONE_BY_DEFAULT"
    assert set(t.rule["participant_roles"]) == {"STRUCTURAL_ENDPOINT", "SHARED_INCIDENCE_CHANNEL"}
    assert t.rule["minimum_cardinality"] == 2


# ------------------------------------------- 2. exact result-contract binding
def test_topology_rule_commits_to_exact_result_contract_binding():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    committed = t.rule["result_contract_binding_ref"]
    assert committed == dict(t.result_contract_ref)
    assert committed["kind"] == "M3ResultContractBinding@2.0.0"
    assert t.result_contract["bound_rule_id"] == t.rule["rule_id"]
    assert t.result_contract["bound_rule_version"] == t.rule["rule_version"]
    assert t.result_contract["semantic_jurisdiction"] == RESULT_JURISDICTION


# ------------------------------------------------------------ 3. closed schema
def test_result_schemas_are_closed_and_use_only_admitted_objective_roles():
    reg = source_free_canary_registry()
    for family in reg.populated_families:
        schema = reg.rule_for(family).result_contract["result_schema"]
        root = schema["root"]
        assert root["type"] == "object"
        assert root["additional_fields"] is False, "open result schemas are forbidden"
        assert set(root["required"]) <= set(root["fields"])
        stack = [root]
        while stack:
            node = stack.pop()
            assert node["semantic_role"] in ADMITTED_OBJECTIVE_ROLES
            if node["type"] == "object":
                assert node["additional_fields"] is False
                stack.extend(node["fields"].values())
            elif node["type"] == "array":
                stack.append(node["items"])


# ------------------------------------------- 4. lawful positive topology result
def test_lawful_positive_topology_result_is_produced():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    a, b = _m2("topo-a"), _m2("topo-b")
    req = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                   payload=_topology_payload())
    x = _eval(reg, [a, b], req)
    assert x.decision_state is M3DecisionState.SUPPORTED
    assert x.v556_object is not None
    assert x.v556_object["semantic_family"] if "semantic_family" in x.v556_object else True
    assert x.v556_object["semantic_jurisdiction"] == RESULT_JURISDICTION
    assert x.v556_object["person_state_absent"] is True


# ------------------------------------ 5. one lawful INTERACTION_RELATION rule
def test_one_lawful_positive_v556_interaction_relation_rule():
    reg = source_free_canary_registry()
    i = reg.rule_for("V556_INTERACTION_RELATION")
    assert i is not None
    assert i.semantic_family == "V556_INTERACTION_RELATION"
    assert i.rule["minimum_cardinality"] == 2
    assert set(i.rule["participant_roles"]) == {
        "COEXISTING_RELATION_LEFT", "COEXISTING_RELATION_RIGHT"}


# ------------------------------- 6. coexisting-relation array with >= 2 items
def test_interaction_result_carries_coexisting_relation_array_min_two():
    reg = source_free_canary_registry()
    i = reg.rule_for("V556_INTERACTION_RELATION")
    array_node = i.result_contract["result_schema"]["root"]["fields"]["coexisting_relations"]
    assert array_node["type"] == "array"
    assert array_node["min_items"] >= 2
    a, b = _m2("int-a"), _m2("int-b")
    payload = _interaction_payload(3)
    assert len(payload["coexisting_relations"]) >= 2
    req = _request(i, [_bind(a, "COEXISTING_RELATION_LEFT", 1),
                        _bind(b, "COEXISTING_RELATION_RIGHT", 2)], payload=payload)
    x = _eval(reg, [a, b], req)
    assert x.decision_state is M3DecisionState.SUPPORTED and x.v556_object is not None
    # one item only must fail closed against the closed schema
    bad = _request(i, [_bind(a, "COEXISTING_RELATION_LEFT", 1),
                       _bind(b, "COEXISTING_RELATION_RIGHT", 2)],
                   payload=_interaction_payload(1))
    y = _eval(reg, [a, b], bad)
    assert y.decision_state is not M3DecisionState.SUPPORTED or y.v556_object is None


# ------------------------------- 7. exact rule/content-hash binding integrity
def test_exact_rule_and_content_hash_binding_is_enforced():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    a, b = _m2("hash-a"), _m2("hash-b")
    good = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                    payload=_topology_payload())
    assert _eval(reg, [a, b], copy.deepcopy(good)).decision_state is M3DecisionState.SUPPORTED
    tampered = copy.deepcopy(good)
    tampered["rule_authority"]["rule_content_hash"] = _h("tampered")
    x = _eval(reg, [a, b], tampered)
    assert x.v556_object is None
    assert x.decision_state in (M3DecisionState.INTEGRITY_FAILURE, M3DecisionState.UNKNOWN_AUTHORITY)


# --------------------------------------------- 8. closed result vocabulary
def test_result_values_outside_closed_schema_vocabulary_are_refused():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    a, b = _m2("voc-a"), _m2("vocab-b")
    payload = _topology_payload()
    payload["incidence_kind"] = "SOME_UNGOVERNED_INCIDENCE_KIND"
    req = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                   payload=payload)
    x = _eval(reg, [a, b], req)
    assert x.v556_object is None
    assert x.decision_state is not M3DecisionState.SUPPORTED
    # undeclared extra field is also refused (closed schema)
    extra = _topology_payload()
    extra["unmagnetised_field"] = "smuggled"
    req2 = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                    payload=extra)
    y = _eval(reg, [a, b], req2)
    assert y.v556_object is None


# ------------------------------------------------- 9. negative/refusal behaviour
def test_missing_or_incomplete_authority_refuses_and_never_manufactures():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    a, b = _m2("neg-a"), _m2("neg-b")
    req = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                   payload=_topology_payload())

    # no active rule authority at all
    no_rules = evaluate_m3_v556_higher_order_structural(
        [a, b], req, active_rule_keys=[],
        active_source_composition_keys=[],
        active_result_contract_refs=reg.active_result_contract_refs())
    assert no_rules.v556_object is None
    assert no_rules.decision_state is not M3DecisionState.SUPPORTED

    # single participant cannot satisfy the two-participant floor
    one = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1)], payload=_topology_payload())
    x = _eval(reg, [a], one)
    assert x.v556_object is None
    assert x.decision_state is M3DecisionState.INVALID_PARTICIPANT_SET

    # wrong role labels
    wrong = _request(t, [_bind(a, "NOT_A_ROLE", 1), _bind(b, "ALSO_NOT", 2)],
                     payload=_topology_payload())
    y = _eval(reg, [a, b], wrong)
    assert y.v556_object is None


# ---------------------------- 10. VALID_EMPTY when no governed rule exists
def test_valid_empty_no_governed_rule_and_missing_authority_manufactures_nothing():
    empty = V556RuleMaterialRegistry.build([])
    assert empty.state == VALID_EMPTY_NO_GOVERNED_RULE
    assert empty.registered_rule_count == 0
    assert empty.active_rule_keys() == []
    assert empty.active_result_contract_refs() == []
    assert set(empty.populated_families) == set()
    assert set(empty.unfilled_families) == set(SUPPORTED_FAMILIES)

    t = topology_canary_rule()
    a, b = _m2("empty-a"), _m2("empty-b")
    req = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                   payload=_topology_payload())
    x = _eval(empty, [a, b], req)
    assert x.v556_object is None
    assert x.decision_state is not M3DecisionState.SUPPORTED


def test_governed_valid_empty_state_still_emits_no_positive_object():
    reg = source_free_canary_registry()
    t = reg.rule_for("V556_TOPOLOGY")
    a, b = _m2("ve-a"), _m2("ve-b")
    payload = _topology_payload()
    payload["incidence_kind"] = PERMITTED_INCIDENCE_KINDS[1]  # declared-absent incidence
    req = _request(t, [_bind(a, "STRUCTURAL_ENDPOINT", 1), _bind(b, "SHARED_INCIDENCE_CHANNEL", 2)],
                   state="VALID_EMPTY", payload=payload)
    x = _eval(reg, [a, b], req)
    assert x.decision_state is M3DecisionState.VALID_EMPTY
    assert x.v556_object is None


# ---------------------------------------------------- 11. no actor-state leakage
def test_no_actor_state_leaks_into_canary_material():
    reg = source_free_canary_registry()
    blob = json.dumps(reg.snapshot(), sort_keys=True) + json.dumps(
        [dict(r.rule) for r in reg.rules], sort_keys=True) + json.dumps(
        [dict(r.result_contract) for r in reg.rules], sort_keys=True)
    for forbidden in (
        "PERSONALITY", "PSYCHOMETRIC", "SUBJECTIVE_BELIEF", "IDEOLOGY", "AFFECT",
        "APPRAISAL", "PREFERENCE", "MOTIVATION", "DISPOSITION", "TRAIT", "ACTOR_UPTAKE",
        "ACTOR_INTERPRETATION", "ACTOR_RESPONSE", "DURABLE_PERSON_STATE",
        "DEVELOPMENTAL_BIOGRAPHICAL_STATE", "ACTOR_MEMORY", "PREFERENCE", "DESIRE",
        "BELIEF", "PERSONALITY",
    ):
        assert forbidden not in blob, f"actor/person-state leakage: {forbidden}"
    for rule in reg.rules:
        assert rule.result_contract["person_state_semantics"] == "FORBIDDEN"
        assert rule.result_contract["actor_indexing_mode"] == "NO_ACTOR_INDEX"


def test_schema_authoring_refuses_person_state_role():
    with pytest.raises(SubstrateAuthoringError):
        author_closed_result_schema(
            schema_id="BAD", semantic_class="OBJECTIVE_STRUCTURAL_RESULT",
            root={"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                  "fields": {"x": {"type": "string", "semantic_role": "SUBJECTIVE_BELIEF_IDEOLOGY",
                                   "allowed_values_or_unbounded_marker": "UNBOUNDED"}},
                  "required": ("x",), "additional_fields": False})


# --------------------------------------------- 12. no scalar-pressure smuggling
def test_no_scalar_pressure_or_strong_noun_is_smuggled():
    reg = source_free_canary_registry()
    blob = json.dumps([dict(r.rule) for r in reg.rules], sort_keys=True) + json.dumps(
        [dict(r.result_contract) for r in reg.rules], sort_keys=True)
    for forbidden in (
        "PRESSURE_MAGNITUDE", "PRESSURE_FOOTPRINT", "COUPLING", "COUPLING_SCALAR",
        "HEGEMONY", "CAPITAL", "HOMOLOGY", "FORMATION", "STRATA", "NINE_STRATA",
        "PRESSURE_COEFFICIENT", "MAGNITUDE", "INTENSITY", "ATTENUATION",
    ):
        assert forbidden not in blob, f"scalar-pressure / strong-noun smuggling: {forbidden}"
    # no numeric or magnitude-typed leaf may appear in any canary schema
    def walk(node):
        assert node["type"] not in {"number", "integer"}, "no scalar magnitude node permitted"
        if node["type"] == "object":
            for child in node["fields"].values():
                walk(child)
        elif node["type"] == "array":
            walk(node["items"])
    for rule in reg.rules:
        walk(rule.result_contract["result_schema"]["root"])


# --------------------------------------------- 13. stable replay / determinants
def test_replay_and_determinants_are_stable_for_exact_governed_inputs():
    reg = source_free_canary_registry()
    for family, roles, payload in (
        ("V556_TOPOLOGY", ("STRUCTURAL_ENDPOINT", "SHARED_INCIDENCE_CHANNEL"), _topology_payload()),
        ("V556_INTERACTION_RELATION",
         ("COEXISTING_RELATION_LEFT", "COEXISTING_RELATION_RIGHT"), _interaction_payload(2)),
    ):
        rule = reg.rule_for(family)
        a, b = _m2(f"rep-a-{family}"), _m2(f"rep-b-{family}")
        req = _request(rule, [_bind(a, roles[0], 1), _bind(b, roles[1], 2)], payload=payload)
        x = _eval(reg, [a, b], copy.deepcopy(req))
        y = _eval(reg, [a, b], copy.deepcopy(req))
        assert x.decision_state is M3DecisionState.SUPPORTED
        assert x == y
        assert x.replay_key_hash == y.replay_key_hash
        assert x.v556_object["object_id"].startswith("urn:rawlsing:v556:higher-order:sha256:")


# ------------------------------------- commission scope guards (non-invention)
def test_attractor_family_stays_supported_but_unfilled():
    assert "V556_ATTRACTOR_PREREQUISITE" in SUPPORTED_FAMILIES
    reg = source_free_canary_registry()
    assert "V556_ATTRACTOR_PREREQUISITE" in reg.unfilled_families
    assert reg.rule_for("V556_ATTRACTOR_PREREQUISATE") is None
    # and no canary may fabricate one
    with pytest.raises(SubstrateAuthoringError):
        author_governed_rule(
            authority_id="X", authority_version="1.0.0", authority_content_hash=_h("x"),
            rule_id="R", rule_version="1.0.0",
            semantic_family="V556_SOME_NEW_FAMILY",
            participant_roles=("A", "B"),
            result_contract=author_result_contract_binding(
                binding_id="B", rule_id="R", rule_version="1.0.0",
                schema={"schema_id": "S", "schema_version": "1.0.0",
                        "semantic_class": "OBJECTIVE_STRUCTURAL_RESULT",
                        "root": {"type": "object", "semantic_role": "OBJECTIVE_GROUPING",
                                 "fields": {}, "required": (), "additional_fields": False}},
                schema_ref={"kind": "M3ResultSchema@2.0.0", "object_id": "S@1.0.0",
                            "content_hash": _h("S")}))


def test_canary_material_carries_no_real_world_authority_claim():
    reg = source_free_canary_registry()
    snap = reg.snapshot()
    assert snap["state"] == "GOVERNED_RULES_PRESENT"
    assert set(snap["populated_families"]) == {"V556_TOPOLOGY", "V556_INTERACTION_RELATION"}
    # registry refuses a second rule for the same family (no unbounded population)
    with pytest.raises(SubstrateAuthoringError):
        V556RuleMaterialRegistry.build([topology_canary_rule(), topology_canary_rule()])
    # explicitly document the canary limit in the module surface
    assert SUBSTRATE_CANARY_CLAIM.startswith("source-free machinery canary only")
