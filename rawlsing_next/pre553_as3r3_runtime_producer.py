"""Bounded AS3R3 successor runtime-object producer.

Authority 28 permits new executable identities only after this producer exists.
No final 19+3 production inputs/objects or AS3R2 target hashes live here.
SEMANTIC_SUCCESSION != IDENTITY_RECOVERY.
"""
from __future__ import annotations
from collections.abc import Iterable, Mapping
from typing import Any
from rawlsing_next.pre553_empirical_objects import AuthorityRef, EmpiricalPredicate, EmpiricalQuerySpec, ExactRef, Pre553IntegrityError, authority_ref, exact_ref, make_empirical_predicate
from rawlsing_next.pre553_as3r3_runtime_producer_contract import *
from rawlsing_next.pre553_as3r3_runtime_producer_contract import PFIELDS,QFIELDS,PRED_SRC_PATH,PRED_SRC_BLOB,QUERY_SRC_PATH,QUERY_SRC_BLOB,common,roles,derivation,keys,refs,sequence,need_auth,need_dep,source,mapping,require_frozen_source


def validate_successor_predicate_input(record: Mapping[str,Any]) -> None:
    s,a,d,_,f=common(record,PREDICATE_INPUT_SCHEMA_ID,AUTHORIZED_PREDICATE_STATE,"predicate input")
    require_frozen_source(s,True)
    roles(record["authority_roles"],a,"predicate input"); derivation(record["semantic_derivation"],s,a,PRED_SRC_PATH,PRED_SRC_BLOB,"predicate input"); keys(f,PFIELDS,"predicate input.semantic_fields")
    grammar=authority_ref(f["grammar_authority_ref"],"grammar_authority_ref"); qv=refs(f["coordinate_question_value_refs"],"coordinate_question_value_refs",True); risk=refs(f["risk_set_refs"],"risk_set_refs"); scope=refs(f["scope_refs"],"scope_refs"); ops=refs(f["operator_semantics_refs"],"operator_semantics_refs",True)
    if f["same_respondent_binding_semantics"] in (None,""): raise Pre553IntegrityError("same_respondent_binding_semantics must be explicit")
    need_auth(a,(grammar,),"predicate input"); need_dep(d,(*qv,*risk,*scope,*ops),"predicate input")
    if not isinstance(f["predicate_ast"],Mapping): raise Pre553IntegrityError("predicate_ast must be a mapping")

def construct_successor_predicate(record: Mapping[str,Any]) -> EmpiricalPredicate:
    validate_successor_predicate_input(record); _,a,d,root,f=common(record,PREDICATE_INPUT_SCHEMA_ID,AUTHORIZED_PREDICATE_STATE,"predicate input")
    return make_empirical_predicate(predicate_ast=f["predicate_ast"],typed_state=AUTHORIZED_PREDICATE_STATE,authority_snapshot_refs=a,dependency_refs=d,producer_replay_locator_or_reference_root=root,grammar_authority_ref=authority_ref(f["grammar_authority_ref"],"grammar_authority_ref"),coordinate_question_value_refs=refs(f["coordinate_question_value_refs"],"coordinate_question_value_refs",True),risk_set_refs=refs(f["risk_set_refs"],"risk_set_refs"),scope_refs=refs(f["scope_refs"],"scope_refs"),same_respondent_binding_semantics=f["same_respondent_binding_semantics"],operator_semantics_refs=refs(f["operator_semantics_refs"],"operator_semantics_refs",True))


def _validate_query(record: Mapping[str,Any], condition_keys: set[str]|None):
    s,a,d,root,f=common(record,QUERY_INPUT_SCHEMA_ID,AUTHORIZED_QUERY_STATE,"query input")
    require_frozen_source(s,False)
    roles(record["authority_roles"],a,"query input"); derivation(record["semantic_derivation"],s,a,QUERY_SRC_PATH,QUERY_SRC_BLOB,"query input"); keys(f,QFIELDS,"query input.semantic_fields")
    targets=refs(f["target_refs"],"target_refs"); condition=exact_ref(f["condition_predicate_ref"],"condition_predicate_ref"); risk=exact_ref(f["risk_set_ref"],"risk_set_ref"); universes=refs(f["empirical_universe_refs"],"empirical_universe_refs"); scopes=refs(f["scope_refs"],"scope_refs"); measure=exact_ref(f["measure_basis_ref"],"measure_basis_ref"); qa=tuple(authority_ref(x,"query_authority_refs") for x in sequence(f["query_authority_refs"],"query_authority_refs"))
    if not isinstance(f["target_arity_and_topology"],Mapping) or not isinstance(f["requested_output_grain"],Mapping): raise Pre553IntegrityError("query topology/output grain must be explicit mappings")
    if condition_keys is not None and condition.key not in condition_keys: raise Pre553IntegrityError("query condition_predicate_ref must resolve to supplied successor predicate refs")
    need_auth(a,qa,"query input"); need_dep(d,(*targets,condition,risk,*universes,*scopes,measure),"query input")
    return s,a,d,root,f

def validate_successor_query_input(record: Mapping[str,Any], *, successor_predicate_refs: Iterable[ExactRef|Mapping[str,Any]]) -> None:
    _validate_query(record,{exact_ref(x,"successor_predicate_refs").key for x in successor_predicate_refs})

def construct_successor_query(record: Mapping[str,Any], *, successor_predicate_refs: Iterable[ExactRef|Mapping[str,Any]]) -> EmpiricalQuerySpec:
    _,a,d,root,f=_validate_query(record,{exact_ref(x,"successor_predicate_refs").key for x in successor_predicate_refs})
    return EmpiricalQuerySpec(typed_state=AUTHORIZED_QUERY_STATE,authority_snapshot_refs=a,dependency_refs=d,producer_replay_locator_or_reference_root=root,target_refs=refs(f["target_refs"],"target_refs"),target_arity_and_topology=f["target_arity_and_topology"],condition_predicate_ref=exact_ref(f["condition_predicate_ref"],"condition_predicate_ref"),risk_set_ref=exact_ref(f["risk_set_ref"],"risk_set_ref"),empirical_universe_refs=refs(f["empirical_universe_refs"],"empirical_universe_refs"),scope_refs=refs(f["scope_refs"],"scope_refs"),measure_basis_ref=exact_ref(f["measure_basis_ref"],"measure_basis_ref"),requested_output_grain=f["requested_output_grain"],query_authority_refs=tuple(authority_ref(x,"query_authority_refs") for x in sequence(f["query_authority_refs"],"query_authority_refs")))


def _observed(inputs,predicate):
    out={}
    for raw in inputs:
        rec=mapping(raw,"predicate input" if predicate else "query input")
        validate_successor_predicate_input(rec) if predicate else _validate_query(rec,None)
        sid,oid,h=source(rec["as3_semantic_source_identity"])
        if sid in out: raise Pre553IntegrityError(f"duplicate AS3 semantic source id: {sid}")
        out[sid]=(oid,h)
    return out

def validate_future_input_bundle(bundle: Mapping[str,Any]) -> None:
    """Validate a later complete input freeze without constructing any object."""
    bundle=mapping(bundle,"future input bundle"); keys(bundle,frozenset({"schema","predicate_inputs","query_inputs","terrain_claim"}),"future input bundle")
    if bundle["schema"]!=FUTURE_INPUT_BUNDLE_SCHEMA_ID: raise Pre553IntegrityError("future input bundle schema mismatch")
    ps=sequence(bundle["predicate_inputs"],"predicate_inputs"); qs=sequence(bundle["query_inputs"],"query_inputs")
    if len(ps)!=19 or len(qs)!=3: raise Pre553IntegrityError("future AS3R3 input bundle must contain exactly 19 predicates and 3 queries")
    ep={x["as3_id"]:(x["object_id"],x["content_hash"]) for x in FROZEN_AS3_PREDICATE_SOURCES}; eq={x["as3_id"]:(x["object_id"],x["content_hash"]) for x in FROZEN_AS3_QUERY_SOURCES}
    if _observed(ps,True)!=ep: raise Pre553IntegrityError("future predicate inputs do not match exact frozen 19-row AS3 semantic source set")
    if _observed(qs,False)!=eq: raise Pre553IntegrityError("future query inputs do not match exact frozen 3-row AS3 semantic source set")
    validate_frozen_terrain_claim(bundle["terrain_claim"])

__all__=["AS3R3_RUNTIME_PRODUCER_CONTRACT_ID","PREDICATE_INPUT_SCHEMA_ID","QUERY_INPUT_SCHEMA_ID","FUTURE_INPUT_BUNDLE_SCHEMA_ID","TERRAIN_CLAIM_SCHEMA_ID","AUTHORIZED_PREDICATE_STATE","AUTHORIZED_QUERY_STATE","PRODUCER_REPLAY_ROOT_KIND","FROZEN_AS3_PREDICATE_SOURCES","FROZEN_AS3_QUERY_SOURCES","FROZEN_TERRAIN_EXPECTATIONS","validate_successor_predicate_input","construct_successor_predicate","validate_successor_query_input","construct_successor_query","validate_frozen_terrain_claim","validate_future_input_bundle"]
