"""AS3R3 Node 4A frozen production predicate inputs.

Static input carrier only.  It does not import the runtime producer and never
calls construct_successor_predicate or any query/discovery constructor.
"""
from __future__ import annotations
import copy, hashlib, json

SOURCE_SHA="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
PART_A_HASH="9dd1e6b7350ebb795e028db86279131f8d319e939a044b74c3c5605ecacf5b06"
START_HEAD="cfc240aa3a64c59509eab97450a7d3603af813cc"
PRODUCER_SHA256="ad7434186e5e72886333f438ed9726cec01a2d2cf740353175da938708a5ef6d"
PRED_SRC_PATH="AS3_CHETIRI_COMMON_MANIFEST_FREEZE_20260827/04_PREDICATE_ATOM_CATALOG.csv"
PRED_SRC_BLOB="577af186fb312ea4e3cca1210c80a5cc2ba82e73"
INPUT_SCHEMA="PRE553_AS3R3_SUCCESSOR_PREDICATE_INPUT@1.0.0"
TYPED_STATE="PREDICATE_RESOLVED_AUTHORIZED"
SAME_RESPONDENT="EXACT_SAME_RESPONDENT_ONLY"
MAPPING_RULE="AS3R3_NODE4A_EXACT_ATOM_TO_GOVERNED_PREDICATE_AST@1.0.0"

def _cj(v): return json.dumps(v,sort_keys=True,separators=(",",":"),ensure_ascii=False)
def _h(v): return hashlib.sha256(_cj(v).encode()).hexdigest()
def _dref(kind,tag,material,prefix="urn:rawlsing:pre553:as2b"):
    h=_h(material); return {"kind":kind,"object_id":f"{prefix}:{tag}:sha256:{h}","content_hash":h}
def _doc_auth(num,filename,title):
    material={"git_commit":"fdef92776e055e1d4a667d8e616d01c44e84b688",
              "path":f"data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/{filename}",
              "authority_number":num,"title":title}
    return {"authority_id":f"urn:rawlsing:governance:authority-{num}:{filename}",
            "authority_version":"git:fdef92776e055e1d4a667d8e616d01c44e84b688",
            "authority_content_hash":_h(material)}
def _as2b_auth(role,kind,families):
    material={"court":"AS2B_LITS1_MECHANICAL_SOURCE_CERTIFICATION_20260827","role":role,"kind":kind,
              "source_sha256":SOURCE_SHA,"part_a_projection_authority_hash":PART_A_HASH,"families":list(families)}
    return {"authority_id":f"urn:rawlsing:pre553:as2b:lits1:authority:{role}",
            "authority_version":"AS2A-BANKED-1.0.0","authority_content_hash":_h(material)}
def _dec(n): return {"$exact_decimal":str(n)}
def _opref(leaf,op):
    material={"commit":START_HEAD,"file_git_blob_sha":"524043996f21110b25a05f0f08bce056e0fa357e",
              "leaf_type":leaf,"operator_semantics":op}
    h=_h(material)
    return {"kind":"PRE553_PREDICATE_OPERATOR_SEMANTICS",
            "object_id":f"rawlsing_next/_pre553_query_predicate.py@{START_HEAD}#{leaf}:{op}:sha256:{h}",
            "content_hash":h}
def _dedupe(refs):
    out=[]; seen=set()
    for r in refs:
        k=(r["kind"],r["object_id"],r["content_hash"])
        if k not in seen: seen.add(k); out.append(r)
    return out

A28=_doc_auth(28,"28_AS3R3_RUNTIME_IDENTITY_SUCCESSION_HQ_ADOPTION.md","AS3R3 RUNTIME-IDENTITY SUCCESSION HQ ADOPTION")
A29=_doc_auth(29,"29_AS3R3_PRODUCER_IDENTITY_FREEZE_AND_INPUT_FREEZE_AUTHORIZATION.md","AS3R3 PRODUCER IDENTITY FREEZE AND INPUT-FREEZE AUTHORIZATION")
A30=_doc_auth(30,"30_AS3R3_TWO_PHASE_PREDICATE_THEN_QUERY_INPUT_AND_MINT_SEQUENCE_CORRECTION.md","AS3R3 TWO-PHASE PREDICATE→QUERY INPUT/MINT SEQUENCE CORRECTION")
AS3R2_AUTH={"authority_id":"urn:rawlsing:pre553:verkhovod:as3r2:discovery-frontier-adoption",
 "authority_version":"git:8e97730bed689b478901ecddd222848802cfd617",
 "authority_content_hash":"08a00dae22e08905b42b650125920653897c6a88b66682699932a31ccb230115"}
SOURCE_AUTH=_as2b_auth("source_semantics","SOURCE_SEMANTICS_TOPOLOGY",("EmpiricalUniverse@1.0.0","RespondentEvent@1.0.0"))
ROUTING_AUTH=_as2b_auth("routing","ROUTING_RISK_SET",("RoutingEligibilityFact@1.0.0",))
GRAMMAR_AUTH=_as2b_auth("i03_query","PREDICATE_GRAMMAR",("EmpiricalPredicate@1.0.0","EmpiricalQuerySpec@1.0.0","EmpiricalFact@1.0.0"))
AUTHORITIES=[A28,A29,A30,AS3R2_AUTH,GRAMMAR_AUTH,SOURCE_AUTH,ROUTING_AUTH]
ROLES={"hq_succession_adoption_ref":A28,"as3_semantic_catalog_authority_ref":AS3R2_AUTH,
 "as3r2_historical_provenance_authority_ref":AS3R2_AUTH,"as3r1_support_rule_authority_ref_if_relevant":None}
PRODUCER_ROOT={"kind":"AS3R3_RUNTIME_OBJECT_PRODUCER",
 "object_id":f"urn:rawlsing:pre553:as3r3:runtime-producer:git:{START_HEAD}:file-sha256:{PRODUCER_SHA256}",
 "content_hash":PRODUCER_SHA256}
CATALOG_REF={"kind":"AS3_PREDICATE_CATALOG","object_id":"urn:rawlsing:pre553:as3:predicate-catalog:sha256:8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293","content_hash":"8c559917640242e017b03e206d5a0a950cb2973c36a90e0be43d3c0fe7cc9293"}
GRAMMAR_REF={"kind":"PRE553_I05_CANDIDATE_GRAMMAR","object_id":"urn:rawlsing:pre553:i05:grammar:sha256:85d314d8222d96328b3e0449495ea3946d02cecaf3f2ccd3b249270a3fca2b66","content_hash":"85d314d8222d96328b3e0449495ea3946d02cecaf3f2ccd3b249270a3fca2b66"}
RISK_REF={"kind":"RISK_SET","object_id":"urn:rawlsing:pre553:as2b:lits1-q301-bounded:sha256:31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45","content_hash":"31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45"}
UNIVERSE_REF={"kind":"EmpiricalUniverse@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080","content_hash":"83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080"}
RELEASE_REF={"kind":"C11LogicalRelease","object_id":"LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79","content_hash":"e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"}
QREFS={
 "q301_2":_dref("QUESTION_NATIVE","lits1-q301_2",{"source_sha256":SOURCE_SHA,"slot":194,"name":"q301_2"}),
 "q301_7":_dref("QUESTION_NATIVE","lits1-q301_7",{"source_sha256":SOURCE_SHA,"slot":199,"name":"q301_7"})}
ATOM_HASHES={
"A000":"7b10ea72bfa44e77c84973fc2160b21aa0ce6827d12e6bcba13724a02fb43e7e",
"A1V1":"442e99e0a7df1e4e32593a743b3512d55bb70bcc95ea092baef6c5b8660dbe3d","A1V2":"e024f84b162ea19c2ac6f415e083b5afb1c4e0159082474d7b47eeb74cca4601","A1V3":"2c870e179d624c7a25b377fd48912bf3068eddef4d3384aa078f1ee510130653","A1V4":"5380f555056fbc055b6a01b1e986b6fe2e2df80aabc4f7c2fa34084644054efe","A1V5":"b0c25dcdcb92663079cb11f305ac1c90effae0a5bac85041c84ee3e3717bd659",
"A1SSUB":"0b81b5e8599c0d5b3482c87a1a7bb7b7ca59948de7b24ea5ff35d16fe28e18fc","A1SSPS":"1eabaa9100f952e0188b3add7e6eaf064e02536c547e30afd5f7ea48bd8ceef7","A1SMIS":"9e866f518d3ffd26704387d6fd601e2fa80bbf353f629bd4e55854f6a8211645","A1RAPP":"2cc073de0e3035399c21e827e4299edeb6af23d2b324800cbd2ad03105eb8f15",
"A2V1":"773fc0d01f808c279de3ff17109b92d99d94aaf8d6e2cbcb760ba48df9d56d58","A2V2":"90bd592ba47c39017b43879629a08c57efbf3d47ffc7f2abd5447a149d6cfffa","A2V3":"5beeb086201138e422dd3e1109b1ec26fd9c8822f68c792016b46ab01311b85c","A2V4":"869f76ba4508bfe9cf466f120bfea7d88cf015d636a3fc364eb6f7b6aa69d6e3","A2V5":"5128a104a40fb311ff139b9c5ba7828974e70e9c7b6b903a95abff6acb005c4c",
"A2SSUB":"65d66c58a2c837702a8ac064f879a85f4431ec7e9f8c000290c5f750f96800d6","A2SSPS":"d7e73c19e4030d46a34e79cd55252fb40f8293286d4ef69a661bf3e4a16331c8","A2SMIS":"e2ee4a009f6bc7611584b647d099587a5e7e8e19d1a79159b74f56314539602b","A2RAPP":"fc4cdaa96888716a3f2ff6e023c0f574f7a0b092549ba80739738335eb5054f1"}

def _event(q,n):
    es=_dref("EVENT_SELECTOR",f"{q}-scalar",{"question":q,"topology":"SCALAR_SINGULAR"})
    vr=_dref("VALUE_REF",f"{q}-values",{"question":q,"values":[_dec(n)]})
    op=_opref("SURVEY_RESPONSE_EVENT","EQ")
    return {"op":"LEAF","leaf_type":"SURVEY_RESPONSE_EVENT","question_semantic_ref":QREFS[q],
      "component_or_event_selector_ref":es,"response_value_or_state_ref":vr,
      "response_topology_authority_ref":SOURCE_AUTH,"response_semantic_authority_ref":SOURCE_AUTH,
      "operator":"EQ","exact_values":[_dec(n)],"exact_value":_dec(n)},[QREFS[q],es,vr],[op]
def _state(q,state):
    sr=_dref("TYPED_STATE",f"{q}-{state}",{"question":q,"state":state})
    op=_opref("TYPED_RESPONSE_STATE","STATE_EQ")
    return {"op":"LEAF","leaf_type":"TYPED_RESPONSE_STATE","question_semantic_ref":QREFS[q],
      "typed_state_ref":sr,"state_semantic_authority_ref":SOURCE_AUTH,"typed_state":state},[QREFS[q],sr],[op]
def _routing(q):
    rr=_dref("ROUTING_STATE",f"{q}-eligible",{"question":q,"state":"ELIGIBLE_APPLICABLE"})
    op=_opref("ROUTING_APPLICABILITY_STATE","EXACT_STATE_MATCH")
    return {"op":"LEAF","leaf_type":"ROUTING_APPLICABILITY_STATE","question_semantic_ref":QREFS[q],
      "routing_or_applicability_state_ref":rr,"routing_authority_ref":ROUTING_AUTH,
      "routing_state":"ELIGIBLE_APPLICABLE"},[QREFS[q],rr],[op]
def _ast(atom):
    if atom=="A000": return _routing("q301_2")
    if atom.endswith("RAPP"): return _routing("q301_2" if atom.startswith("A1") else "q301_7")
    if atom.endswith("SSUB"): return _state("q301_2" if atom.startswith("A1") else "q301_7","SUBSTANTIVE_RESPONSE")
    if atom.endswith("SSPS"): return _state("q301_2" if atom.startswith("A1") else "q301_7","SOURCE_SPECIFIC_SPECIAL")
    if atom.endswith("SMIS"): return _state("q301_2" if atom.startswith("A1") else "q301_7","MISSING")
    return _event("q301_2" if atom.startswith("A1") else "q301_7",int(atom[-1]))

def _record(atom):
    h=ATOM_HASHES[atom]; ast,qv,ops=_ast(atom)
    src={"as3_id":atom,"object_id":f"urn:rawlsing:pre553:as3:atom-{atom.lower()}:sha256:{h}","content_hash":h}
    deps=_dedupe([CATALOG_REF,GRAMMAR_REF,*qv,RISK_REF,UNIVERSE_REF,RELEASE_REF,*ops])
    return {"input_schema":INPUT_SCHEMA,"as3_semantic_source_identity":src,
      "semantic_derivation":{"source_path":PRED_SRC_PATH,"source_git_blob_sha":PRED_SRC_BLOB,
        "source_row_id":atom,"mapping_rule_id":MAPPING_RULE,"mapping_authority_ref":A28,
        "derivation_mode":"EXACT_GOVERNED_NO_HEURISTIC_REWRITE"},
      "authority_roles":ROLES,"typed_state":TYPED_STATE,"authority_snapshot_refs":AUTHORITIES,
      "dependency_refs":deps,"producer_replay_locator_or_reference_root":PRODUCER_ROOT,
      "semantic_fields":{"predicate_ast":ast,"grammar_authority_ref":GRAMMAR_AUTH,
        "coordinate_question_value_refs":qv,"risk_set_refs":[RISK_REF],
        "scope_refs":[UNIVERSE_REF,RELEASE_REF],"same_respondent_binding_semantics":SAME_RESPONDENT,
        "operator_semantics_refs":ops}}

PREDICATE_INPUTS=tuple(_record(atom) for atom in ATOM_HASHES)
assert len(PREDICATE_INPUTS)==19 and len({x["as3_semantic_source_identity"]["as3_id"] for x in PREDICATE_INPUTS})==19
def load_predicate_inputs(): return copy.deepcopy(PREDICATE_INPUTS)
