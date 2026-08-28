"""Static contract and fail-closed validators for the AS3R3 bounded producer."""
from __future__ import annotations
from collections.abc import Iterable, Mapping, Sequence
from typing import Any
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef, Pre553IntegrityError, authority_ref, exact_ref

AS3R3_RUNTIME_PRODUCER_CONTRACT_ID="PRE553_AS3R3_BOUNDED_RUNTIME_OBJECT_PRODUCER@1.0.0"
PREDICATE_INPUT_SCHEMA_ID="PRE553_AS3R3_SUCCESSOR_PREDICATE_INPUT@1.0.0"
QUERY_INPUT_SCHEMA_ID="PRE553_AS3R3_SUCCESSOR_QUERY_INPUT@1.0.0"
FUTURE_INPUT_BUNDLE_SCHEMA_ID="PRE553_AS3R3_SUCCESSOR_RUNTIME_INPUT_BUNDLE@1.0.0"
TERRAIN_CLAIM_SCHEMA_ID="PRE553_AS3R3_FROZEN_TERRAIN_COMPATIBILITY_CLAIM@1.0.0"
AUTHORIZED_PREDICATE_STATE="PREDICATE_RESOLVED_AUTHORIZED"
AUTHORIZED_QUERY_STATE="QUERY_AUTHORIZED_RESOLVABLE"
PRODUCER_REPLAY_ROOT_KIND="AS3R3_RUNTIME_OBJECT_PRODUCER"
PRED_SRC_PATH="AS3_CHETIRI_COMMON_MANIFEST_FREEZE_20260827/04_PREDICATE_ATOM_CATALOG.csv"
QUERY_SRC_PATH="AS3_CHETIRI_COMMON_MANIFEST_FREEZE_20260827/05_QUERY_TEMPLATE_CATALOG.csv"
PRED_SRC_BLOB="577af186fb312ea4e3cca1210c80a5cc2ba82e73"
QUERY_SRC_BLOB="534b57fd90eb63f2d455f49235aac4d240291ad3"
DERIVATION_MODE="EXACT_GOVERNED_NO_HEURISTIC_REWRITE"

_P=(
("A000","7b10ea72bfa44e77c84973fc2160b21aa0ce6827d12e6bcba13724a02fb43e7e"),("A1V1","442e99e0a7df1e4e32593a743b3512d55bb70bcc95ea092baef6c5b8660dbe3d"),("A1V2","e024f84b162ea19c2ac6f415e083b5afb1c4e0159082474d7b47eeb74cca4601"),("A1V3","2c870e179d624c7a25b377fd48912bf3068eddef4d3384aa078f1ee510130653"),("A1V4","5380f555056fbc055b6a01b1e986b6fe2e2df80aabc4f7c2fa34084644054efe"),("A1V5","b0c25dcdcb92663079cb11f305ac1c90effae0a5bac85041c84ee3e3717bd659"),("A1SSUB","0b81b5e8599c0d5b3482c87a1a7bb7b7ca59948de7b24ea5ff35d16fe28e18fc"),("A1SSPS","1eabaa9100f952e0188b3add7e6eaf064e02536c547e30afd5f7ea48bd8ceef7"),("A1SMIS","9e866f518d3ffd26704387d6fd601e2fa80bbf353f629bd4e55854f6a8211645"),("A1RAPP","2cc073de0e3035399c21e827e4299edeb6af23d2b324800cbd2ad03105eb8f15"),("A2V1","773fc0d01f808c279de3ff17109b92d99d94aaf8d6e2cbcb760ba48df9d56d58"),("A2V2","90bd592ba47c39017b43879629a08c57efbf3d47ffc7f2abd5447a149d6cfffa"),("A2V3","5beeb086201138e422dd3e1109b1ec26fd9c8822f68c792016b46ab01311b85c"),("A2V4","869f76ba4508bfe9cf466f120bfea7d88cf015d636a3fc364eb6f7b6aa69d6e3"),("A2V5","5128a104a40fb311ff139b9c5ba7828974e70e9c7b6b903a95abff6acb005c4c"),("A2SSUB","65d66c58a2c837702a8ac064f879a85f4431ec7e9f8c000290c5f750f96800d6"),("A2SSPS","d7e73c19e4030d46a34e79cd55252fb40f8293286d4ef69a661bf3e4a16331c8"),("A2SMIS","e2ee4a009f6bc7611584b647d099587a5e7e8e19d1a79159b74f56314539602b"),("A2RAPP","fc4cdaa96888716a3f2ff6e023c0f574f7a0b092549ba80739738335eb5054f1"))
_Q=(("T_Q301_2_RAW","fe90741a61a3b89bd24f9d08b374459ccac931b59a14f16237e3db6ad3974479"),("T_Q301_7_RAW","72c61c7dc621b2ffa43e3c0cfe56639c04df3f7e5eaa3aa32dddb642987e75f4"),("T_Q301_2_Q301_7_RAW","d55fb8f6cc47e83c570d13b4aba171b77c221b6d18637d909dc54a7b44255367"))
def _sources(rows,family): return tuple({"as3_id":i,"object_id":f"urn:rawlsing:pre553:as3:{family}-{i.lower()}:sha256:{h}","content_hash":h} for i,h in rows)
FROZEN_AS3_PREDICATE_SOURCES=_sources(_P,"atom")
FROZEN_AS3_QUERY_SOURCES=_sources(_Q,"query")
FROZEN_TERRAIN_EXPECTATIONS:Mapping[str,Any]={
"accepted_as3":"da36f2457513acf2ce734f3509236ef6d2dceec5","predicate_count":19,"query_count":3,
"predicate_semantic_catalog_hash":"8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293","query_semantic_catalog_hash":"f76ddf2b8a99e6a05884d503aa7a5da8fbf1fb3b07fbcd4cc93597457defa423",
"risk_partition_count":1,"measure_partition":"RAW_ONLY","topology_partition_count":2,"risk_measure_topology_identity_hash":"ed3b76242a588a5e2d4dacbb76f17ceef6185cd27a4080a2e8fb436056abfabf","K":18,"J":2,"recursive_depth":18,"candidate_count":82,
"candidate_semantic_frontier_hash":"ec85fc2c6460a8a014ae90c54e5847f883c495708c32898ea44bfc0ef78c54e6","candidate_ordering_law":"CANONICAL_CANDIDATE_HASH_ORDER","completion_law":"NONE_EXACT_EVALUATE_ALL","rng":"NONE","minimum_raw_denominator":0,
"support_rule_id":"PRE553_PRODUCTION_I05_NO_ADDITIONAL_MINIMUM_RAW_DENOMINATOR@1.0.0","support_rule_hash":"6df2664f4a9cd8fe5d334b954aed4db1b97de4937b4d03e5ce63bcc322baab4c","common_I03_git_blob_sha":"3194ccbd4aede70f587bce32c7d0b70c54a17f4c","typed_nonpositive_learned_preV3_target_git_blob_sha":"8527efc27dc23ebba4e7a212a1d6c152c18f720a","common_measurement_law_git_blob_sha":"7c13a3e100e84154c86efa90b0257dc63c0485d0","route_B_common_candidate_terrain_git_blob_sha":"93b7e23650b3544669ee15e424f42c4ea807ade1","route_C_accelerator_spec_git_blob_sha":"34d2d21e51cff0995301e04bfef994b97c6cc5d8","route_C_invalidation_spec_git_blob_sha":"4fda5eb6ae5c6b215bfeb3a42b111bf6f8880f8a","route_A_common_candidate_terrain_git_blob_sha":"030b2b98fa2fb38be51cb38bc52d6401fd304d04"}
COMMON=frozenset("input_schema as3_semantic_source_identity semantic_derivation authority_roles typed_state authority_snapshot_refs dependency_refs producer_replay_locator_or_reference_root semantic_fields".split())
PFIELDS=frozenset("predicate_ast grammar_authority_ref coordinate_question_value_refs risk_set_refs scope_refs same_respondent_binding_semantics operator_semantics_refs".split())
QFIELDS=frozenset("target_refs target_arity_and_topology condition_predicate_ref risk_set_ref empirical_universe_refs scope_refs measure_basis_ref requested_output_grain query_authority_refs".split())
ROLES=frozenset("hq_succession_adoption_ref as3_semantic_catalog_authority_ref as3r2_historical_provenance_authority_ref as3r1_support_rule_authority_ref_if_relevant".split())
DERIVE=frozenset("source_path source_git_blob_sha source_row_id mapping_rule_id mapping_authority_ref derivation_mode".split())

def mapping(v,n):
    if not isinstance(v,Mapping): raise Pre553IntegrityError(f"{n} must be a mapping")
    return v
def sequence(v,n,empty=False):
    if isinstance(v,(str,bytes,bytearray)) or not isinstance(v,Sequence) or (not v and not empty): raise Pre553IntegrityError(f"{n} must be a sequence")
    return v
def keys(v,k,n):
    if set(v)!=k: raise Pre553IntegrityError(f"{n} keys mismatch; missing={sorted(k-set(v))!r} extra={sorted(set(v)-k)!r}")
def auths(v): return tuple(authority_ref(x,"authority_snapshot_refs") for x in sequence(v,"authority_snapshot_refs"))
def refs(v,n,empty=False): return tuple(exact_ref(x,n) for x in sequence(v,n,empty))
def akeys(v): return {x.key for x in v}
def rkeys(v): return {x.key for x in v}
def source(v,n="as3_semantic_source_identity"):
    v=mapping(v,n); keys(v,frozenset({"as3_id","object_id","content_hash"}),n); out=(v["as3_id"],v["object_id"],v["content_hash"])
    if not all(isinstance(x,str) and x for x in out) or len(out[2])!=64 or any(c not in "0123456789abcdef" for c in out[2]): raise Pre553IntegrityError(f"{n} malformed")
    return out
def roles(v,a,n):
    v=mapping(v,f"{n}.authority_roles"); keys(v,ROLES,f"{n}.authority_roles"); have=akeys(a)
    for k in ROLES:
        x=v[k]
        if x is None:
            if k!="as3r1_support_rule_authority_ref_if_relevant": raise Pre553IntegrityError(f"{n}.{k} may not be null")
        elif authority_ref(x,k).key not in have: raise Pre553IntegrityError(f"{n}.{k} outside authority_snapshot_refs")
def derivation(v,s,a,path,blob,n):
    v=mapping(v,f"{n}.semantic_derivation"); keys(v,DERIVE,f"{n}.semantic_derivation")
    if (v["source_path"],v["source_git_blob_sha"],v["source_row_id"],v["derivation_mode"])!=(path,blob,s[0],DERIVATION_MODE): raise Pre553IntegrityError(f"{n} semantic derivation is not exact governed frozen mapping")
    if not isinstance(v["mapping_rule_id"],str) or not v["mapping_rule_id"].strip() or authority_ref(v["mapping_authority_ref"],"mapping_authority_ref").key not in akeys(a): raise Pre553IntegrityError(f"{n} mapping rule/authority is missing or outside closure")
def common(record,schema,state,n):
    record=mapping(record,n); keys(record,COMMON,n)
    if record["input_schema"]!=schema or record["typed_state"]!=state: raise Pre553IntegrityError(f"{n} schema or HQ-authorized typed state mismatch")
    a=auths(record["authority_snapshot_refs"]); d=refs(record["dependency_refs"],"dependency_refs"); root=exact_ref(record["producer_replay_locator_or_reference_root"],"producer_replay_locator_or_reference_root")
    if root.kind!=PRODUCER_REPLAY_ROOT_KIND: raise Pre553IntegrityError("producer replay root must identify the already-existing AS3R3 producer")
    return source(record["as3_semantic_source_identity"]),a,d,root,mapping(record["semantic_fields"],f"{n}.semantic_fields")
def need_auth(have,required,n):
    missing=[x.key for x in required if x.key not in akeys(have)]
    if missing: raise Pre553IntegrityError(f"{n} authority closure missing exact refs: {sorted(missing)!r}")
def need_dep(have,required,n):
    missing=[x.key for x in required if x.key not in rkeys(have)]
    if missing: raise Pre553IntegrityError(f"{n} dependency closure missing exact refs: {sorted(missing)!r}")

def require_frozen_source(s, predicate):
    allowed=FROZEN_AS3_PREDICATE_SOURCES if predicate else FROZEN_AS3_QUERY_SOURCES
    if not any((x["as3_id"],x["object_id"],x["content_hash"])==s for x in allowed): raise Pre553IntegrityError("semantic source identity is outside the exact frozen AS3 catalog")

def validate_frozen_terrain_claim(claim):
    claim=mapping(claim,"terrain claim"); keys(claim,frozenset({"schema",*FROZEN_TERRAIN_EXPECTATIONS}),"terrain claim")
    if claim["schema"]!=TERRAIN_CLAIM_SCHEMA_ID: raise Pre553IntegrityError("terrain claim schema mismatch")
    for k,v in FROZEN_TERRAIN_EXPECTATIONS.items():
        if claim[k]!=v: raise Pre553IntegrityError(f"frozen terrain mismatch for {k}: expected {v!r}, observed {claim[k]!r}")
