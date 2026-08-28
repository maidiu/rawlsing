from copy import deepcopy
import hashlib, json
from pathlib import Path
import pytest
import rawlsing_next.pre553_as3r3_runtime_producer as p
from rawlsing_next.pre553_empirical_objects import Pre553IntegrityError


def h(x): return hashlib.sha256(x.encode()).hexdigest()
def ref(kind, tag): return {"kind":kind,"object_id":f"urn:test:{tag}","content_hash":h(tag)}
def auth(tag): return {"authority_id":f"urn:test:authority:{tag}","authority_version":"1.0.0","authority_content_hash":h("auth:"+tag)}

def pred():
    grammar,hq,cat,hist,mapa=(auth(x) for x in ("grammar","hq","cat-p","hist","map-p"))
    risk,scope,op,qv=(ref(*x) for x in (("RISK","risk"),("SCOPE","scope"),("OP","eq"),("QV","qv")))
    return {"input_schema":p.PREDICATE_INPUT_SCHEMA_ID,"as3_semantic_source_identity":dict(p.FROZEN_AS3_PREDICATE_SOURCES[1]),
      "semantic_derivation":{"source_path":"AS3_CHETIRI_COMMON_MANIFEST_FREEZE_20260827/04_PREDICATE_ATOM_CATALOG.csv","source_git_blob_sha":"577af186fb312ea4e3cca1210c80a5cc2ba82e73","source_row_id":"A1V1","mapping_rule_id":"FIXTURE_EXACT@1","mapping_authority_ref":mapa,"derivation_mode":"EXACT_GOVERNED_NO_HEURISTIC_REWRITE"},
      "authority_roles":{"hq_succession_adoption_ref":hq,"as3_semantic_catalog_authority_ref":cat,"as3r2_historical_provenance_authority_ref":hist,"as3r1_support_rule_authority_ref_if_relevant":None},
      "typed_state":p.AUTHORIZED_PREDICATE_STATE,"authority_snapshot_refs":[grammar,hq,cat,hist,mapa],"dependency_refs":[risk,scope,op,qv],"producer_replay_locator_or_reference_root":ref(p.PRODUCER_REPLAY_ROOT_KIND,"producer"),
      "semantic_fields":{"predicate_ast":{"op":"LEAF","leaf_type":"SURVEY_RESPONSE_EVENT","question":"q","value":1},"grammar_authority_ref":grammar,"coordinate_question_value_refs":[qv],"risk_set_refs":[risk],"scope_refs":[scope],"same_respondent_binding_semantics":"EXACT_SAME_RESPONDENT_ONLY","operator_semantics_refs":[op]}}

def query(condition):
    qa,hq,cat,hist,mapa=(auth(x) for x in ("query","hq","cat-q","hist","map-q"))
    target,risk,uni,scope,measure=(ref(*x) for x in (("TARGET","target"),("RISK","risk"),("UNIVERSE","uni"),("SCOPE","scope-q"),("MEASURE","raw")))
    return {"input_schema":p.QUERY_INPUT_SCHEMA_ID,"as3_semantic_source_identity":dict(p.FROZEN_AS3_QUERY_SOURCES[0]),
      "semantic_derivation":{"source_path":"AS3_CHETIRI_COMMON_MANIFEST_FREEZE_20260827/05_QUERY_TEMPLATE_CATALOG.csv","source_git_blob_sha":"534b57fd90eb63f2d455f49235aac4d240291ad3","source_row_id":"T_Q301_2_RAW","mapping_rule_id":"FIXTURE_EXACT@1","mapping_authority_ref":mapa,"derivation_mode":"EXACT_GOVERNED_NO_HEURISTIC_REWRITE"},
      "authority_roles":{"hq_succession_adoption_ref":hq,"as3_semantic_catalog_authority_ref":cat,"as3r2_historical_provenance_authority_ref":hist,"as3r1_support_rule_authority_ref_if_relevant":None},
      "typed_state":p.AUTHORIZED_QUERY_STATE,"authority_snapshot_refs":[qa,hq,cat,hist,mapa],"dependency_refs":[target,condition,risk,uni,scope,measure],"producer_replay_locator_or_reference_root":ref(p.PRODUCER_REPLAY_ROOT_KIND,"producer"),
      "semantic_fields":{"target_refs":[target],"target_arity_and_topology":{"arity":1,"topology":"SCALAR_SINGULAR"},"condition_predicate_ref":condition,"risk_set_ref":risk,"empirical_universe_refs":[uni],"scope_refs":[scope],"measure_basis_ref":measure,"requested_output_grain":{"measure_kind":"RAW","grain":"TARGET_DISTRIBUTION"},"query_authority_refs":[qa]}}

def test_same_input_and_set_reorder_are_deterministic():
    a=pred(); b=deepcopy(a); x,y=ref("SCOPE","x"),ref("SCOPE","y"); a["semantic_fields"]["scope_refs"] += [x,y]; a["dependency_refs"] += [x,y]; b["semantic_fields"]["scope_refs"] += [y,x]; b["dependency_refs"] += [y,x]
    assert p.construct_successor_predicate(a).content_hash == p.construct_successor_predicate(b).content_hash

def test_behavior_capable_field_and_predicate_ast_change_identity():
    a=pred(); b=deepcopy(a); b["semantic_fields"]["same_respondent_binding_semantics"]="OTHER_EXPLICIT"; assert p.construct_successor_predicate(a).content_hash != p.construct_successor_predicate(b).content_hash
    c=deepcopy(a); c["semantic_fields"]["predicate_ast"]["value"]=2; assert p.construct_successor_predicate(a).content_hash != p.construct_successor_predicate(c).content_hash

def test_missing_authority_and_unauthorized_state_fail_closed():
    a=pred(); a["authority_snapshot_refs"]=[]
    with pytest.raises(Pre553IntegrityError): p.validate_successor_predicate_input(a)
    b=pred(); b["typed_state"]="PREDICATE_UNRESOLVED"
    with pytest.raises(Pre553IntegrityError): p.validate_successor_predicate_input(b)

def test_malformed_or_incomplete_dependency_closure_fails_closed():
    a=pred(); a["dependency_refs"]=a["dependency_refs"][:-1]
    with pytest.raises(Pre553IntegrityError): p.validate_successor_predicate_input(a)
    b=pred(); b["dependency_refs"][0]["content_hash"]="bad"
    with pytest.raises(Pre553IntegrityError): p.validate_successor_predicate_input(b)

def test_query_determinism_semantic_change_and_state_guard():
    pr=p.construct_successor_predicate(pred()); a=query(pr.ref.as_dict()); q1=p.construct_successor_query(a,successor_predicate_refs=[pr.ref]); q2=p.construct_successor_query(a,successor_predicate_refs=[pr.ref]); assert q1.content_hash==q2.content_hash
    b=deepcopy(a); b["semantic_fields"]["requested_output_grain"]["grain"]="OTHER"; assert p.construct_successor_query(b,successor_predicate_refs=[pr.ref]).content_hash != q1.content_hash
    c=deepcopy(a); c["typed_state"]="QUERY_UNAUTHORIZED"
    with pytest.raises(Pre553IntegrityError): p.validate_successor_query_input(c,successor_predicate_refs=[pr.ref])

def test_query_condition_must_be_supplied_successor_predicate():
    pr=p.construct_successor_predicate(pred()); a=query(pr.ref.as_dict())
    with pytest.raises(Pre553IntegrityError): p.validate_successor_query_input(a,successor_predicate_refs=[ref("EmpiricalPredicate@1.0.0","other")])

def test_no_old_hash_target_fitting_fields():
    a=pred(); a["expected_runtime_hash"]="0"*64
    with pytest.raises(Pre553IntegrityError): p.construct_successor_predicate(a)
    schema=json.loads((Path(__file__).parents[1]/"pre553_as3r3_runtime_producer_input.schema.json").read_text()); text=json.dumps(schema,sort_keys=True)
    assert "expected_runtime_hash" not in text and "old_as3r2_runtime_ref" not in text

def test_replay_root_and_exact_frozen_mapping_are_required():
    a=pred(); a["producer_replay_locator_or_reference_root"]["kind"]="OTHER"
    with pytest.raises(Pre553IntegrityError): p.construct_successor_predicate(a)
    b=pred(); b["semantic_derivation"]["source_git_blob_sha"]="0"*40
    with pytest.raises(Pre553IntegrityError): p.construct_successor_predicate(b)

def test_frozen_terrain_checker_rejects_drift_without_i05():
    claim={"schema":p.TERRAIN_CLAIM_SCHEMA_ID,**p.FROZEN_TERRAIN_EXPECTATIONS}; p.validate_frozen_terrain_claim(claim); claim["candidate_count"]=81
    with pytest.raises(Pre553IntegrityError): p.validate_frozen_terrain_claim(claim)

def test_future_bundle_requires_exact_19_plus_3_but_does_not_mint():
    claim={"schema":p.TERRAIN_CLAIM_SCHEMA_ID,**p.FROZEN_TERRAIN_EXPECTATIONS}
    with pytest.raises(Pre553IntegrityError): p.validate_future_input_bundle({"schema":p.FUTURE_INPUT_BUNDLE_SCHEMA_ID,"predicate_inputs":[pred()],"query_inputs":[],"terrain_claim":claim})

def test_no_final_production_catalog_or_object_globals():
    assert not hasattr(p,"FINAL_SUCCESSOR_RUNTIME_CATALOG") and not hasattr(p,"AS3R3_SUCCESSOR_RUNTIME_OBJECTS")
    assert all(not isinstance(v,(p.EmpiricalPredicate,p.EmpiricalQuerySpec)) for v in vars(p).values())
