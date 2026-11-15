"""F02 bounded LiTS-I q310/q311 C11 selector closure. No learned workload execution."""
from __future__ import annotations
import hashlib, json, math
from typing import Any, Iterable, Mapping

CONTRACT_ID="PREV3_LITS1_Q310_Q311_C11_SELECTOR_CLOSURE@1.0.0"
SOURCE_SHA256="7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS=29002; SOURCE_VARIABLES=1198
BASE_C11_OBJECT_ID="LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79"
BASE_C11_HASH="e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"
BASE_REPLAY_HASH="6bfe9862abd6f373309ff6f8868f8871948bb9ed397906d880cda6776941a1dd"
D02_FRONTIER_COMMIT="40cb8585f076a66d9884b99022a59bb909606c03"
D02_FRONTIER_GIT_BLOB="5399a3f64642c8d9f8a0644db0adc15d38642971"
F02_COMMISSION_TIP="468fd77d624e6cb73f9c14825d6b75cb433cca36"
NEGATIVE_CEILING="Q310_Q311_OPAQUE_NATIVE_CONDITIONERS__NO_ORDINAL_DIRECTIONAL_STRUCTURAL_POSITION_PSYCHOLOGICAL_OR_CAUSAL_MEANING"
D02_AUTH={
 "i03_query":("urn:rawlsing:pre553:as2b:lits1:authority:i03_query","AS2A-BANKED-1.0.0","6c6d2f5fb5f4165e5de19989bd456ee8c09f42ab175fa4d10572dc2b9403ca0d"),
 "source_semantics":("urn:rawlsing:pre553:as2b:lits1:authority:source_semantics","AS2A-BANKED-1.0.0","5f671f2cf9342820026af287009d1d9220e3f9f29d92134582d77eeebbdcd638"),
 "routing":("urn:rawlsing:pre553:as2b:lits1:authority:routing","AS2A-BANKED-1.0.0","703f629c5d2b66e1ea5fccfddec80130bbb9b2ea5f8f93c4f69ad5797158d89a")}
QUESTION_SPECS={
 "q310":(229,"attitude towards market economy vs. planned economy",{1:"market economy preferable",2:"planned economy preferable under some circumstances",3:"doesn't matter"}),
 "q311":(230,"attitude towards democratic vs. authoritarian gov.",{1:"democracy preferable",2:"authoritarian preferable under some circumstances",3:"doesn't matter"})}
REAL_SOURCE_SCAN={
 "q310":{"counts":{"1":12340,"2":7511,"3":9085,"MISSING":66},"row_semantic_root_sha256":"a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455","selector_roots":{"1":"0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2","2":"0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83","3":"b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d","MISSING":"810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348"}},
 "q311":{"counts":{"1":16582,"2":4548,"3":7826,"MISSING":46},"row_semantic_root_sha256":"af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa","selector_roots":{"1":"bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869","2":"43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f","3":"642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837","MISSING":"847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb"}}}
D02_FRONTIER_INVARIANTS={"expected_compiled_candidate_count":50,"expected_i03_query_execution_count":77,"family_candidate_counts":{"P0":5,"P1":1,"P2":18,"P3":1,"P4":25},"family_query_role_counts":{"P0":5,"P1":3,"P2":36,"P3":8,"P4":25},"maximum_conditioner_arity_K":3,"maximum_target_arity_J":2,"validators":["CONDITIONAL_REVERSAL","DISTRIBUTION_DIFFERS_FROM_BASELINE","JOINT_NOT_PRODUCT_OF_MARGINALS","TARGET_CELL_SUPPORTED"],"pruning_contract":{"kind":"NONE_EXACT_EVALUATE_ALL"},"rng_policy_if_any":"NONE","candidate_scoring_or_ranking_rule_if_any":None,"tie_order_rules":"CANONICAL_CANDIDATE_HASH_ORDER","frontier_frozen_before_empirical_evaluation":True}
SELECTOR_IDS={f"{q.upper()}V{v}":f"urn:rawlsing:prev3:d02:lits2006:{q}:eq:{v}" for q in ("q310","q311") for v in (1,2,3)}

class SelectorClosureError(ValueError): pass

def canon(v:Any)->Any:
 if v is None or isinstance(v,(str,bool,int)): return v
 if isinstance(v,float):
  if not math.isfinite(v) or not v.is_integer(): raise SelectorClosureError("noncanonical float")
  return int(v)
 if isinstance(v,Mapping): return {k:canon(v[k]) for k in sorted(v)}
 if isinstance(v,(list,tuple)): return [canon(x) for x in v]
 if isinstance(v,(set,frozenset)): return sorted((canon(x) for x in v),key=cjson)
 raise SelectorClosureError(f"unsupported identity type {type(v).__name__}")
def cjson(v): return json.dumps(canon(v),sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def sh(v): return hashlib.sha256(cjson(v).encode()).hexdigest()
def cset(vs):
 d={cjson(v):canon(v) for v in vs}; return [d[k] for k in sorted(d)]
def ref(kind,ns,material):
 h=sh(material); return {"kind":kind,"object_id":f"urn:rawlsing:prev3:f02:{ns}:sha256:{h}","content_hash":h}
def oldauth(k):
 a=D02_AUTH[k]; return {"authority_id":a[0],"authority_version":a[1],"authority_content_hash":a[2]}
def auth(name,kind,ops,parent):
 material={"contract":CONTRACT_ID,"commission_tip":F02_COMMISSION_TIP,"name":name,"kind":kind,"operations":sorted(ops),"source_sha256":SOURCE_SHA256,"base_c11_hash":BASE_C11_HASH,"questions":["q310","q311"],"native_values":[1,2,3],"negative_ceiling":NEGATIVE_CEILING,"parent":oldauth(parent)}
 h=sh(material); r={"authority_id":f"urn:rawlsing:prev3:f02:lits1:{name}","authority_version":"1.0.0","authority_content_hash":h}
 return r,{"authority_ref":r,"authority_kind":kind,"decision_state":"ALLOW","governed_operations":sorted(ops),"scope":{"source_sha256":SOURCE_SHA256,"questions":["q310","q311"],"native_values":[1,2,3],"use":"D02_SELECTOR_PREIMAGE_RESOLUTION_ONLY"},"parent_authority_refs":[oldauth(parent)],"negative_ceiling":NEGATIVE_CEILING}
def authority_package():
 specs={"source_semantics":("source-semantics","SOURCE_SEMANTICS_TOPOLOGY",("QUESTION_NATIVE_BIND","RESPONSE_SLOT_BIND","RESPONSE_VALUE_STATE_BIND"),"source_semantics"),"routing":("routing","ROUTING_RISK_SET",("SOURCE_CELL_STATE_PRESERVATION","SELECTOR_APPLICABILITY"),"routing"),"predicate_grammar":("predicate-grammar","PREDICATE_GRAMMAR",("survey_response_EQ",),"i03_query"),"replay":("replay","REPLAY_PROTOCOL",("F02_C11_SELECTOR_REPLAY",),"i03_query")}
 refs={}; snaps={}
 for k,s in specs.items(): refs[k],snaps[k]=auth(*s)
 return {"refs":refs,"snapshots":snaps}
def qref(q,a):
 row,text,labels=QUESTION_SPECS[q]; return ref("QUESTION_NATIVE",f"lits1-{q}-question",{"source_sha256":SOURCE_SHA256,"physical_var_name":q,"ledger_row_index":row,"question_text":text,"native_domain":[1,2,3],"labels":labels,"semantic_lane":"STRUCTURAL_CONTEXT__TOPOLOGY","directionality":"PRESERVED_NON_DIRECTIONAL__NO_SIGN","authority_ref":a,"negative_ceiling":NEGATIVE_CEILING})
def vref(q,v,qr,a): return ref("RESPONSE_VALUE_STATE",f"lits1-{q}-{'missing' if v is None else v}",{"question_ref":qr,"raw_native_value":v,"response_state":"MISSING" if v is None else "SUBSTANTIVE_RESPONSE","authority_ref":a,"negative_ceiling":NEGATIVE_CEILING})
def predicate(q,v,release,qr,vr,auths):
 ast={"op":"LEAF","leaf_type":"SURVEY_RESPONSE_EVENT","operation":"survey_response_EQ","question_ref":qr,"response_value_ref":vr,"source_native_value":v,"release_ref":release}
 opref=ref("PREDICATE_OPERATOR_SEMANTICS","survey-response-eq",{"operator":"survey_response_EQ","semantics":"TRUE_IFF_SAME_ROW_GOVERNED_EVENT_HAS_EXACT_NATIVE_VALUE","missing_is_false":True,"no_ordering_or_distance":True})
 replay=ref("F02_SELECTOR_REPLAY_ROOT",f"{q}-{v}",{"question":q,"value":v,"release_ref":release,"source_root":REAL_SOURCE_SCAN[q]["selector_roots"][str(v)],"replay_authority_ref":auths["replay"]})
 sem={"predicate_ast":ast,"predicate_hash":sh(ast),"grammar_authority_ref":auths["predicate_grammar"],"coordinate_question_value_refs":cset([qr,vr]),"risk_set_refs":[],"scope_refs":cset([release]),"same_respondent_binding_semantics":"EXACT_SOURCE_ROW_REPLAY_WITHIN_SAME_LITS1_RELEASE","operator_semantics_refs":cset([opref])}
 ars=sorted([auths["predicate_grammar"],auths["source_semantics"],auths["routing"]],key=lambda x:(x["authority_id"],x["authority_version"],x["authority_content_hash"]))
 deps=sorted([qr,vr,release],key=lambda x:(x["kind"],x["object_id"],x["content_hash"]))
 proj={"schema_id":"EmpiricalPredicate","schema_version":"1.0.0","typed_state":"PREDICATE_RESOLVED_AUTHORIZED","authority_snapshot_refs":ars,"dependency_refs":deps,"producer_replay_locator_or_reference_root":replay,"semantic_fields":canon(sem)}
 h=sh(proj); return {"kind":"EmpiricalPredicate@1.0.0","object_id":f"urn:rawlsing:pre553:EmpiricalPredicate:sha256:{h}","content_hash":h},proj

def build_selector_closure():
 ap=authority_package(); ar=ap["refs"]; qs={}
 for q in ("q310","q311"):
  qr=qref(q,ar["source_semantics"]); vals={str(v):vref(q,v,qr,ar["source_semantics"]) for v in (1,2,3)}; vals["MISSING"]=vref(q,None,qr,ar["source_semantics"])
  slot=ref("RESPONSE_SLOT",f"lits1-{q}-slot",{"question_ref":qr,"value_state_refs":vals,"missingness_law":"MISSING_NEVER_SELECTOR_1_2_3","authority_ref":ar["source_semantics"]})
  route=ref("ROUTING_BINDING",f"lits1-{q}-routing",{"question_ref":qr,"authority_ref":ar["routing"],"law":"PHYSICAL_SLOT_PRESENT_ALL_ROWS__CELL_MISSINGNESS_PRESERVED"})
  qs[q]={"question_ref":qr,"value_state_refs":vals,"slot_ref":slot,"routing_ref":route,"real_source_scan":REAL_SOURCE_SCAN[q],"directionality":"PRESERVED_NON_DIRECTIONAL__NO_SIGN","negative_ceiling":NEGATIVE_CEILING}
 base={"kind":"C11LogicalRelease","object_id":BASE_C11_OBJECT_ID,"content_hash":BASE_C11_HASH}
 mat={"schema":"F02_LITS1_C11_COMPOSITE_RELEASE@1.0.0","contract":CONTRACT_ID,"source":{"sha256":SOURCE_SHA256,"rows":SOURCE_ROWS,"variables":SOURCE_VARIABLES},"base_release_ref":base,"base_replay_hash":BASE_REPLAY_HASH,"member_law":"BASE_MEMBERS_UNCHANGED_UNION_Q310_Q311_GOVERNED_EXTENSION","questions":qs,"authority_snapshots":ap["snapshots"],"forbidden":["BASE_C11_MUTATION","CATEGORY_RECODE","DIRECTIONAL_INTERPRETATION","POST_RESULT_FRONTIER_MUTATION","LEARNED_WORKLOAD_EXECUTION"]}
 rh=sh(mat); release={"kind":"C11LogicalRelease","object_id":f"LITS1-F02-C11-{SOURCE_SHA256[:16]}-{rh[:16]}","content_hash":rh}
 sels={}
 for q in ("q310","q311"):
  for v in (1,2,3):
   atom=f"{q.upper()}V{v}"; pr,pp=predicate(q,v,release,qs[q]["question_ref"],qs[q]["value_state_refs"][str(v)],ar); sid=SELECTOR_IDS[atom]
   sels[sid]={"atom_id":atom,"physical_var_name":q,"source_native_value":v,"operation":"survey_response_EQ","predicate_ref":pr,"predicate_projection":pp,"selector_support_count":REAL_SOURCE_SCAN[q]["counts"][str(v)],"selector_membership_root_sha256":REAL_SOURCE_SCAN[q]["selector_roots"][str(v)]}
 rmat={"schema":"F02_LITS1_C11_SELECTOR_REPLAY@1.0.0","source_sha256":SOURCE_SHA256,"base_c11_hash":BASE_C11_HASH,"new_release_ref":release,"question_row_roots":{q:REAL_SOURCE_SCAN[q]["row_semantic_root_sha256"] for q in ("q310","q311")},"selector_refs":{s:sels[s]["predicate_ref"] for s in sorted(sels)},"replay_authority_ref":ar["replay"],"order":"SOURCE_ROW_ORDINAL_ASC__Q310_THEN_Q311__SELECTOR_ID_LEXICAL"}
 rrh=sh(rmat); replay={"kind":"ReplayReceipt@1.0.0","object_id":f"urn:rawlsing:prev3:f02:lits1-c11-selector-replay:sha256:{rrh}","content_hash":rrh}
 return {"contract":CONTRACT_ID,"source":mat["source"],"base_release_ref":base,"new_release_ref":release,"release_material_hash":rh,"replay_ref":replay,"replay_material_hash":rrh,"authorities":ap,"questions":qs,"selectors":sels}

def build_frontier_readoption(closure,invariants=None):
 exp=canon(D02_FRONTIER_INVARIANTS); got=canon(D02_FRONTIER_INVARIANTS if invariants is None else invariants)
 if got!=exp: raise SelectorClosureError("D02 frontier mutation forbidden")
 sels=closure.get("selectors",{})
 if set(sels)!=set(SELECTOR_IDS.values()): raise SelectorClosureError("exact six-selector closure required")
 mat={"schema":"F02_D02_LEARNED_FRONTIER_READOPTION@1.0.0","d02_frontier_source":{"commit":D02_FRONTIER_COMMIT,"git_blob_sha1":D02_FRONTIER_GIT_BLOB,"artifact_bytes_mutated":False},"new_release_ref":closure["new_release_ref"],"selector_preimage_substitutions":{s:sels[s]["predicate_ref"] for s in sorted(sels)},"frozen_invariants":exp,"allowed_mutation":"SELECTOR_PREIMAGE_SUBSTITUTION_ONLY","workload_execution":"NOT_EXECUTED","post_result_mutation":"FORBIDDEN"}
 return {**mat,"readoption_hash_sha256":sh(mat)}
def verify_real_source_summary(s):
 if canon(s)!=canon(REAL_SOURCE_SCAN): raise SelectorClosureError("real q310/q311 source replay summary mismatch")
 if any(sum(REAL_SOURCE_SCAN[q]["counts"].values())!=SOURCE_ROWS for q in ("q310","q311")): raise SelectorClosureError("source count mismatch")
def typed_native_value(v):
 if v is None or (isinstance(v,float) and math.isnan(v)): return "MISSING",None
 if isinstance(v,bool): raise SelectorClosureError("boolean response forbidden")
 if isinstance(v,float):
  if not v.is_integer(): raise SelectorClosureError("nonintegral response")
  v=int(v)
 if v not in (1,2,3): raise SelectorClosureError("outside governed native domain")
 return "SUBSTANTIVE_RESPONSE",int(v)
def scan_records(records:Iterable[Mapping[str,Any]]):
 rows=list(records)
 if len(rows)!=SOURCE_ROWS: raise SelectorClosureError(f"expected {SOURCE_ROWS} exact source rows")
 if [r.get("row_ordinal") for r in rows]!=list(range(SOURCE_ROWS)): raise SelectorClosureError("invalid row replay coordinates")
 out={}
 for q in ("q310","q311"):
  total=hashlib.sha256(); hs={k:hashlib.sha256() for k in ("1","2","3","MISSING")}; counts={k:0 for k in hs}
  for r in rows:
   st,v=typed_native_value(r[q]); k="MISSING" if st=="MISSING" else str(v); b=(cjson({"row_ordinal":r["row_ordinal"],"response_state":st,"raw_native_value":v})+"\n").encode(); total.update(b); hs[k].update(b); counts[k]+=1
  out[q]={"counts":counts,"row_semantic_root_sha256":total.hexdigest(),"selector_roots":{k:hs[k].hexdigest() for k in hs}}
 return out

__all__=["SOURCE_SHA256","SOURCE_ROWS","BASE_C11_HASH","D02_FRONTIER_INVARIANTS","REAL_SOURCE_SCAN","SELECTOR_IDS","SelectorClosureError","build_selector_closure","build_frontier_readoption","verify_real_source_summary","typed_native_value","scan_records"]
