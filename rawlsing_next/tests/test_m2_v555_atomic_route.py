from __future__ import annotations

import copy, hashlib, random
from dataclasses import replace

import pytest

from rawlsing_next.m1_temporal_v554_admission_dedup import M1DecisionState, evaluate_m1_temporal_v554_admission_dedup, semantic_hash
from rawlsing_next.m2_v555_atomic_route import (
    CHANNEL_STRUCTURAL_ROLE_ID, M2DecisionState, RECEIVING_CONSTRAINT_KIND,
    ROUTE_AUTHORITY_ID, ROUTE_AUTHORITY_VERSION, ROUTE_RULE_ID, ROUTE_RULE_VERSION,
    ROUTE_SHAPE_ID, ROUTE_SHAPE_VERSION, SEMANTIC_FAMILY,
    evaluate_m2_v555_atomic_route,
)

def _h(x: str) -> str: return hashlib.sha256(x.encode()).hexdigest()
def _ref(kind: str, oid: str) -> dict[str, str]: return {"kind": kind, "object_id": oid, "content_hash": _h(oid)}
def _auth(i: str, v: str, seal: str) -> dict[str, str]: return {"id": i, "version": v, "content_hash": _h(seal)}

def _m1(*, source: str = "u:1", aliases: tuple[str, ...] = ("direct:1",), conditions=()):
    eq = {"focal_structural_proposition_ref":"prop:1","target_use":"STRUCTURAL_MEDIATION_INPUT","v554_rule_id":"V554-RULE-17","v554_rule_version":"1.0.0","v554_rule_hash":_h("rule"),"rule_relevant_structural_semantic_identity_fingerprint":"struct:1","native_scope_identity_fingerprint":"scope:1","rule_relevant_effective_time_semantics_fingerprint":"t:none","originating_structural_empirical_admission_lineage_fingerprint":"adm:1","source_universe_fingerprint":source,"estimand_fingerprint":"estimand:1","measure_and_weight_authority_fingerprint":"measure:1","rule_relevant_source_relation_comparability_authority_fingerprint":"cmp:1","interpretation_critical_semantic_authority_fingerprint":"auth:1"}
    def cand(oid):
        p={"structural_empirical_admission_id":"admission:1","structural_empirical_admission_content_hash":_h("admission:1"),"admission_authority_id":"A","admission_authority_version":"1","admission_authority_hash":_h("a"),"admission_decision_state":"ADMITTED","focal_structural_proposition_ref":"prop:1","structural_semantic_identity_refs":["struct:1"],"native_scope_identity_refs":["scope:1"],"target_use_permission_refs":["perm:1"],"effective_time_or_interval_refs_required_by_target_use":[],"source_universe_refs":[source],"estimand_refs":["estimand:1"],"measure_and_weight_authority_refs":["measure:1"],"applicable_negative_denial_noncomparability_refs":[],"interpretation_critical_authority_refs":["auth:1"],"producer_replay_locator_or_reference_root":"replay:1"}
        return {"basis_kind":"DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION","basis_ref":_ref("DIRECT_STRUCTURAL_EMPIRICAL_ADMISSION",oid),"projection":p,"projection_hash":semantic_hash(p),"equivalence_key":eq,"selected_rule_relevant_basis_semantics":"support:1","v553_families":[],"all_relation_required_support_limit_refs":False}
    cs=[]
    for k in conditions:
        cs.append({"candidate_semantic_key":"c:1","condition_kind_id":k,"predicate_id":f"P-{k}","predicate_version":"1","semantic_owner":"V554","resolution_owner":"V555","binding_producer":"V554","evaluator_owner":"V555","canonical_argument_envelope_fingerprint":f"args:{k}","producer_negative_or_requirement_refs":[f"ref:{k}"]})
    payload={"governed_use_id":"use:1","use_owner":"V554","v554_rule_ref":{"id":"V554-RULE-17","version":"1.0.0","hash":_h("rule")},"signature_id":"V554-SIG-001-NONTEMPORAL-EXACT","target_use":"STRUCTURAL_MEDIATION_INPUT","focal_structural_proposition_ref":"prop:1","originating_admission_refs":["admission:1"],"scr553_decision_state":"V553_NOT_REQUIRED_FOR_THIS_USE","scr553_request_ref":_ref("V553TemporalizationRequest","req:1"),"required_temporal_operations":[],"required_authority_snapshot_refs":["snap:1"],"temporal_completeness":"COMPLETE_FOR_DIRECT_V554","candidates":[cand(x) for x in aliases],"conditions":cs,"authority_bundle_material":{"scr554":"1","rule":"17"},"producer_reference_spine_fingerprint":"spine:1"}
    return evaluate_m1_temporal_v554_admission_dedup(payload)

def _closure(m1, *, source="source:1", channel="channel:1", receiver="receiver:1"):
    f1r={"kind":"F1","object_id":m1.f1["f1_id"],"content_hash":semantic_hash(m1.f1)}
    material={"f1_id":f1r["object_id"],"f1_content_hash":f1r["content_hash"],"source_structural_position_ref":_ref("StructuralPosition",source),"structural_channel_ref":_ref("StructuralChannel",channel),"receiving_structural_position_ref":_ref("StructuralPosition",receiver),"closure_authority_ref":_ref("V554ReferenceClosure","closure-authority:1")}
    return {**material,"closure_content_hash":semantic_hash(material)}

def _req(m1, **kw):
    r={"route_authority_ref":_auth(ROUTE_AUTHORITY_ID,ROUTE_AUTHORITY_VERSION,"registry"),"route_rule_ref":_auth(ROUTE_RULE_ID,ROUTE_RULE_VERSION,"rule"),"route_shape_ref":_auth(ROUTE_SHAPE_ID,ROUTE_SHAPE_VERSION,"shape"),"f1_reference_closure":_closure(m1),"channel_structural_role_id":CHANNEL_STRUCTURAL_ROLE_ID,"receiving_constraint_kind":RECEIVING_CONSTRAINT_KIND,"producer_allowed_uses":["STRUCTURAL_MEDIATION_INPUT"],"v556_higher_order_semantics_required":None,"v557_publication_authority":None}
    r.update(kw); return r

def _pub(use="STRUCTURAL_MEDIATION_INPUT"):
    return {"authority_id":"PUB","authority_version":"1","authority_hash":_h("pub"),"producer":"V555","publisher":"V557","decision":"AUTHORIZED","intended_use":use,"allowed_object_families":[SEMANTIC_FAMILY]}

def test_positive_route_is_exact_seven_field_actor_independent_route():
    m=_m1(); x=evaluate_m2_v555_atomic_route(m,_req(m)); assert x.decision_state is M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED
    assert len(x.canonical_route_identity)==7 and x.canonical_route_identity[0]==m.f1["f1_id"]
    assert x.canonical_route_identity[1:4]==(f"{ROUTE_RULE_ID}@{ROUTE_RULE_VERSION}",f"{ROUTE_SHAPE_ID}@{ROUTE_SHAPE_VERSION}",CHANNEL_STRUCTURAL_ROLE_ID)
    assert [z["role"] for z in x.route["ordered_structure"]]==["SOURCE","MEDIATION_LOCUS","RECEIVER"] and x.route["actor_independent"] is True

def test_b1_and_f2_are_not_route_identity_and_route_born_registry_is_valid_empty():
    m=_m1(conditions=("K01","K02")); x=evaluate_m2_v555_atomic_route(m,_req(m)); s=repr(x.canonical_route_identity)
    assert m.b1["b1_id"] not in s and all(z["f2_id"] not in s for z in m.f2)
    assert [z["object_id"] for z in x.inherited_v554_f2_refs]==sorted(z["f2_id"] for z in m.f2)
    assert x.route_born_predicate_registry["state"]=="VALID_EMPTY" and x.route_born_predicate_registry["registered_predicate_count"]==0

def test_deferred_f2_does_not_block_structural_route_or_assert_satisfaction():
    m=_m1(conditions=("K01","K02","K03")); x=evaluate_m2_v555_atomic_route(m,_req(m)); assert x.decision_state is M2DecisionState.ROUTE_CANDIDATE_AUTHORIZED
    assert all(z["disposition"]=="DEFERRED" for z in m.f2) and "satisfied" not in repr(x.route).lower()

@pytest.mark.parametrize("mutation",["missing","mismatch","false"])
def test_exact_b1_is_required_for_positive_route(mutation):
    m=_m1()
    if mutation=="missing": m=replace(m,b1=None)
    elif mutation=="mismatch":
        b=copy.deepcopy(m.b1); b["material"]["f1_id_or_null"]="urn:wrong"; m=replace(m,b1=b)
    else:
        b=copy.deepcopy(m.b1); b["allowed_v555_structural_use"]=False; m=replace(m,b1=b)
    assert evaluate_m2_v555_atomic_route(m,_req(_m1())).decision_state is M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE

@pytest.mark.parametrize("state,expected",[(M1DecisionState.VALID_EMPTY,M2DecisionState.VALID_EMPTY),(M1DecisionState.INTEGRITY_FAILURE,M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE),(M1DecisionState.INELIGIBLE_UNKNOWN_OR_CONFLICTING_REQUIRED_AUTHORITY,M2DecisionState.ROUTE_STATIC_AUTHORITY_MISSING),(M1DecisionState.INELIGIBLE_EXPLICIT_DENIAL,M2DecisionState.V554_STRUCTURAL_USE_DENIED)])
def test_upstream_nonpositive_states_never_create_route(state,expected):
    good=_m1(); m=replace(good,decision_state=state,support_count=0,f1=None,b1=None,f2=())
    x=evaluate_m2_v555_atomic_route(m,{}); assert x.decision_state is expected and x.route is None

@pytest.mark.parametrize("raw",[{"StructuralEmpiricalAdmission":"x"},{"V553":"x"},{"legacy_seed":"x"}])
def test_raw_or_legacy_bypass_is_rejected(raw):
    assert evaluate_m2_v555_atomic_route(raw,{}).decision_state is M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE

def test_different_f1_same_visible_channel_receiver_stays_different_route():
    a,b=_m1(source="u:a"),_m1(source="u:b"); xa,xb=evaluate_m2_v555_atomic_route(a,_req(a)),evaluate_m2_v555_atomic_route(b,_req(b))
    assert a.f1["f1_id"]!=b.f1["f1_id"] and xa.canonical_route_identity!=xb.canonical_route_identity

def test_duplicate_physical_aliases_do_not_multiply_or_change_route():
    a,b=_m1(aliases=("direct:a",)),_m1(aliases=("direct:b","direct:a")); assert a.f1["f1_id"]==b.f1["f1_id"]
    assert evaluate_m2_v555_atomic_route(a,_req(a)).canonical_route_identity==evaluate_m2_v555_atomic_route(b,_req(b)).canonical_route_identity

@pytest.mark.parametrize("field,value,expected",[("route_rule_ref",None,M2DecisionState.ROUTE_STATIC_AUTHORITY_MISSING),("route_rule_ref",{"id":ROUTE_RULE_ID,"version":"latest","content_hash":_h("x")},M2DecisionState.NO_GOVERNED_ROUTE_AUTHORITY),("route_shape_ref",{"id":"V555-RS-FUZZY","version":ROUTE_SHAPE_VERSION,"content_hash":_h("x")},M2DecisionState.NO_GOVERNED_ROUTE_AUTHORITY)])
def test_missing_latest_or_fuzzy_route_authority_fails_closed(field,value,expected):
    m=_m1(); r=_req(m); r[field]=value; assert evaluate_m2_v555_atomic_route(m,r).decision_state is expected

def test_reference_closure_must_bind_exact_f1_and_exact_seal():
    m=_m1(); r=_req(m); r["f1_reference_closure"]["f1_id"]="wrong"; assert evaluate_m2_v555_atomic_route(m,r).decision_state is M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE
    r=_req(m); del r["f1_reference_closure"]["structural_channel_ref"]; assert evaluate_m2_v555_atomic_route(m,r).decision_state is M2DecisionState.ROUTE_IDENTITY_UNRESOLVED
    r=_req(m); r["f1_reference_closure"]["closure_content_hash"]=_h("wrong"); assert evaluate_m2_v555_atomic_route(m,r).decision_state is M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE

@pytest.mark.parametrize("key,value",[("actor_state",{}),("persona",{}),("additional_hops",[1]),("B1_as_identity","x"),("F2_as_identity","x")])
def test_forbidden_actor_multihop_or_eighth_identity_fields_are_rejected(key,value):
    m=_m1(); r=_req(m); r[key]=value; assert evaluate_m2_v555_atomic_route(m,r).decision_state is M2DecisionState.CONSTRUCTION_FAILURE__NOT_STRUCTURAL_NEGATIVE

def test_source_reference_is_local_replay_material_not_eighth_tuple_field():
    m=_m1(); a,b=_req(m),_req(m); a["f1_reference_closure"]=_closure(m,source="s:a"); b["f1_reference_closure"]=_closure(m,source="s:b")
    xa,xb=evaluate_m2_v555_atomic_route(m,a),evaluate_m2_v555_atomic_route(m,b); assert xa.canonical_route_identity==xb.canonical_route_identity and xa.replay_key_hash!=xb.replay_key_hash

def test_replay_is_deterministic_and_ignores_external_rng_file_noise(tmp_path):
    m=_m1(); r=_req(m); before=random.getstate(); (tmp_path/"latest").write_text("a"); a=evaluate_m2_v555_atomic_route(m,copy.deepcopy(r)); random.random(); (tmp_path/"latest").write_text("b"); b=evaluate_m2_v555_atomic_route(m,copy.deepcopy(r))
    assert a==b and before!=random.getstate()

def test_permission_ceiling_is_replay_material_but_not_route_identity():
    m=_m1(); a,b=_req(m),_req(m); b["producer_allowed_uses"]=["STRUCTURAL_MEDIATION_INPUT","SECONDARY"]
    xa,xb=evaluate_m2_v555_atomic_route(m,a),evaluate_m2_v555_atomic_route(m,b); assert xa.canonical_route_identity==xb.canonical_route_identity and xa.replay_key_hash!=xb.replay_key_hash

def test_direct_v555_v557_requires_independent_permission_and_no_v556_transform():
    m=_m1(); r=_req(m,v556_higher_order_semantics_required=False,v557_publication_authority=_pub()); x=evaluate_m2_v555_atomic_route(m,r); assert x.direct_v557_handoff and x.direct_v557_handoff["route"]=="V555_TO_V557_DIRECT"
    r=_req(m,v556_higher_order_semantics_required=True,v557_publication_authority=_pub()); x=evaluate_m2_v555_atomic_route(m,r); assert x.route is not None and x.direct_v557_handoff is None
    r=_req(m,v556_higher_order_semantics_required=False,v557_publication_authority=_pub("NOT_ALLOWED")); assert evaluate_m2_v555_atomic_route(m,r).direct_v557_handoff is None
