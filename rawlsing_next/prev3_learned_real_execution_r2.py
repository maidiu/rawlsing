"""G02 real execution of the F02-resealed D02 learned-world frontier.

Receipt-producing runner only. It compiles the frozen D02/F02 frontier before
opening source bytes, executes all 50 candidates / 77 query roles against the
exact LiTS-I carrier, and emits deterministic PRE-V3 learned empirical receipts.
It does not mint structural, causal, population, person, V3, ranking, scoring,
or architecture-selection truth.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Mapping, Sequence

CONTRACT_ID = "PREV3_LEARNED_WORLD_POSITIVE_WORKLOAD_REAL_EXECUTION_AND_REPLAY_R2@1.0.0"
SOURCE_SHA256 = "7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09"
SOURCE_ROWS = 29002
SOURCE_VARIABLES = 1198
D02_AUTHORITY_COMMIT = "40cb8585f076a66d9884b99022a59bb909606c03"
D02_FRONTIER_GIT_BLOB = "5399a3f64642c8d9f8a0644db0adc15d38642971"
F02_RETURN_COMMIT = "482bb884a99e31ba77e904d0df39fffc872cbed3"
F02_RELEASE_REF = {"kind":"C11LogicalRelease","object_id":"LITS1-F02-C11-7cac43e2ca5b31cb-bf305bf3f169d669","content_hash":"bf305bf3f169d66954be4f39cc602880fddea6083b5bee9c0212938355cd5297"}
F02_REPLAY_HASH = "89bb3e9140ae0e0fcc9a3e205fd6b60ae721153d88a4730dd66f4fc16e238b1f"
F02_FRONTIER_READOPTION_HASH = "07c6175b1d3828f8dc8763c51f3eb44a3cba6812bb128d4f0b84ffc5096cb851"
BASE_C11_REF = {"kind":"C11LogicalRelease","object_id":"LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79","content_hash":"e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26"}
EMPIRICAL_UNIVERSE_REF = {"kind":"EmpiricalUniverse@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalUniverse:sha256:83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080","content_hash":"83af05f5891e8accc18eeb99e5a1fd99242a509d9a38276004675c0e26be8080"}
RISK_SET_REF = {"kind":"RISK_SET","object_id":"urn:rawlsing:pre553:as2b:lits1-q301-bounded:sha256:31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45","content_hash":"31f7ec452d8d75eebf7963d1ce1715b38f5329a31c757d9088819c99f5d4db45"}
MEASURE_BASIS_REF = {"kind":"AS3_QUERY_MEASURE_BASIS","object_id":"urn:rawlsing:pre553:as3:measure-raw:sha256:25e90c83f1f226ce7eb6a337018635b28427ae90446f3e4d825a1788c43336ec","content_hash":"25e90c83f1f226ce7eb6a337018635b28427ae90446f3e4d825a1788c43336ec"}
ATOM_REFS = {
 "A000":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0","content_hash":"ac3fcb4e32a41f9972004b2c31da61e9b32ba69568a795d2c1e584c9bed21be0"},
 "A1V1":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:082157ea8f31fe0d209c6241552116108e3e3917f7ddb7a49fa365ad5362aeeb","content_hash":"082157ea8f31fe0d209c6241552116108e3e3917f7ddb7a49fa365ad5362aeeb"},
 "A1V5":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:9ba962d35fc630686b7538ae22dbabe2f5b51fe8c7b3473beab901214b1db43c","content_hash":"9ba962d35fc630686b7538ae22dbabe2f5b51fe8c7b3473beab901214b1db43c"},
 "Q310V1":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a","content_hash":"c9a0c8106d457bba7e3f3f5abb7ee7fb98482bd86af629d860e4a904ad58456a"},
 "Q310V2":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df","content_hash":"78dbd1a899fe43ac2e2ca6985ea0eccb086989fa2c4315fa518524e7ba94a6df"},
 "Q310V3":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca","content_hash":"c4d2dd827326b6ff29f3c02382c36fa33c47c6227bfbf8c8053c11e1089923ca"},
 "Q311V1":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8","content_hash":"69dc59f79014a7c17190ca658e193a004e167c322c7f713f4540882fb980feb8"},
 "Q311V2":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849","content_hash":"f63d6121776500912342ab377178a15fcf6fabf7071864f4f413d95babb43849"},
 "Q311V3":{"kind":"EmpiricalPredicate@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalPredicate:sha256:a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d","content_hash":"a6494153b4defeb13e1658b73eead7c5df6e25847708c770dad5f42142492c7d"},
}
QUERY_REFS = {
 "T_Q301_2_RAW":{"kind":"EmpiricalQuerySpec@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44","content_hash":"8a7bf5bbb1c2d8d6328dc5507416931a9c12e2c76668e0fc47af8add254c5d44"},
 "T_Q301_7_RAW":{"kind":"EmpiricalQuerySpec@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7","content_hash":"deb71e653592d8bdb246f8c4d53359e290708d3875e38433f518b307f520c6f7"},
 "T_Q301_2_Q301_7_RAW":{"kind":"EmpiricalQuerySpec@1.0.0","object_id":"urn:rawlsing:pre553:EmpiricalQuerySpec:sha256:ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053","content_hash":"ef8b19744ec3c06e352f7accf75efbc216ffc454905da09948763a2c54fdc053"},
}
NEGATIVE_CEILING = "PREV3_LEARNED_EMPIRICAL_ONLY__NO_STRUCTURAL_ADMISSION__NO_CAUSAL_PROMOTION__NO_POPULATION_GENERALIZATION__NO_PERSON_STATE__NO_V3"
EXPECTED_F02_SCAN = {
 "q310":{"counts":{"1":12340,"2":7511,"3":9085,"MISSING":66},"row_semantic_root_sha256":"a979c15c93502b77979041ffd8451c602f63a7fcbb145106d68a78414be92455","selector_roots":{"1":"0a62f6f0e3d78b429022b95c2594a3fcbf053b8af588f0ceb304ac3dafe700d2","2":"0bad1e397f5b74b6136ba82e8d81fc608d1df7124e6ff043048cc5cd91ef9c83","3":"b477bf705a93bb672d9ae670a1daa38013c2aa2841d0c506f722ab1bbdbb2f3d","MISSING":"810a81a5663c05dcd0e2f4c2c972f66dc16e7446c87054bb412242632dc57348"}},
 "q311":{"counts":{"1":16582,"2":4548,"3":7826,"MISSING":46},"row_semantic_root_sha256":"af193e948fd2199bb784f476475d6dd4c6b96698a01e1804e5a6ce69b93c49aa","selector_roots":{"1":"bffb9d2e9da447a27aaf7c8f889a07d5c47389a58ad933d3ea9867f83e127869","2":"43ffb4ef1de60354b9c943135fd0f31ee54d31edbcd3bb6abf147e5bff1dce1f","3":"642a70ba00a4f7292d96267647068c3bfc83f5efc75451ce00a7df4cd2d62837","MISSING":"847c4e89a7336a5cb5ac6d73953b87091640231ba7cd5c5376e37044a12a03fb"}},
}
LANE_EXPECTATIONS = {
 "P0":{"rule_id":"D02_P0_REAL_POSITIVE_CONTROL","candidate_count":5,"query_role_count":5},
 "P1":{"rule_id":"D02_P1_JOINT_DEPENDENCE","candidate_count":1,"query_role_count":3},
 "P2":{"rule_id":"D02_P2_HIGHER_ORDER_K3","candidate_count":18,"query_role_count":36},
 "P3":{"rule_id":"D02_P3_CONDITIONAL_REVERSAL","candidate_count":1,"query_role_count":8},
 "P4":{"rule_id":"D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS","candidate_count":25,"query_role_count":25},
}

class G02ExecutionError(RuntimeError): pass

def canon(v:Any)->Any:
 if v is None or isinstance(v,(str,bool,int)): return v
 if isinstance(v,Fraction): return {"$exact_fraction":[v.numerator,v.denominator]}
 if isinstance(v,float):
  if not math.isfinite(v): raise G02ExecutionError("non-finite numeric material")
  if v.is_integer(): return int(v)
  raise G02ExecutionError("binary float forbidden in identity material")
 if isinstance(v,Mapping): return {str(k):canon(v[k]) for k in sorted(v,key=str)}
 if isinstance(v,(list,tuple)): return [canon(x) for x in v]
 if isinstance(v,(set,frozenset)): return sorted((canon(x) for x in v),key=cjson)
 if hasattr(v,"item"): return canon(v.item())
 raise G02ExecutionError(f"unsupported canonical type {type(v).__name__}")
def cjson(v): return json.dumps(canon(v),sort_keys=True,separators=(",",":"),ensure_ascii=False,allow_nan=False)
def sh(v): return hashlib.sha256(cjson(v).encode()).hexdigest()
def file_sha256(path):
 h=hashlib.sha256()
 with Path(path).open("rb") as f:
  for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def exact_decimal(n): return {"$exact_decimal":str(n)}
def _condition(*atoms): return {"op":"AND" if len(atoms)>1 else "ATOM","atom_ids":list(atoms),"atom_refs":[ATOM_REFS[a] for a in atoms],"same_respondent_binding":"EXACT_SOURCE_ROW_WITHIN_F02_COMPOSITE_RELEASE"}
def _role(role,q,atoms): return {"role":role,"query_template_id":q,"query_template_ref":QUERY_REFS[q],"condition":_condition(*atoms)}

def compile_frontier():
 candidates=[]
 for cell in range(1,6):
  candidates.append({"lane":"P0","rule_id":"D02_P0_REAL_POSITIVE_CONTROL","family":"BOUNDED_K_WAY_RESPONSE_CONFIGURATION","form":"BASE_QUERY","parameters":{"target_cell":exact_decimal(cell)},"validation":{"kind":"TARGET_CELL_SUPPORTED","target_cell":exact_decimal(cell)},"query_roles":[_role("BASE","T_Q301_2_RAW",["A000"])]})
 candidates.append({"lane":"P1","rule_id":"D02_P1_JOINT_DEPENDENCE","family":"PAIR_RESPONSE_COTRAVEL","form":"JOINT_DEPENDENCE","parameters":{},"validation":{"kind":"JOINT_NOT_PRODUCT_OF_MARGINALS"},"query_roles":[_role("JOINT","T_Q301_2_Q301_7_RAW",["A000"]),_role("MARGINAL_0","T_Q301_2_RAW",["A000"]),_role("MARGINAL_1","T_Q301_7_RAW",["A000"])]})
 for q2 in (1,5):
  for q310 in (1,2,3):
   for q311 in (1,2,3):
    atoms=[f"A1V{q2}",f"Q310V{q310}",f"Q311V{q311}"]
    candidates.append({"lane":"P2","rule_id":"D02_P2_HIGHER_ORDER_K3","family":"BOUNDED_K_WAY_RESPONSE_CONFIGURATION","form":"AND_CARTESIAN_GROUPS","parameters":{"q301_2":q2,"q310":q310,"q311":q311},"validation":{"kind":"DISTRIBUTION_DIFFERS_FROM_BASELINE"},"query_roles":[_role("CONDITION","T_Q301_7_RAW",atoms),_role("BASELINE","T_Q301_7_RAW",["A000"])]})
 p3=[_role("POOLED_POS","T_Q301_7_RAW",["A1V5"]),_role("POOLED_NEG","T_Q301_7_RAW",["A1V1"])]
 for q310 in (1,2,3): p3 += [_role(f"STRATUM:Q310V{q310}:POS","T_Q301_7_RAW",[f"Q310V{q310}","A1V5"]),_role(f"STRATUM:Q310V{q310}:NEG","T_Q301_7_RAW",[f"Q310V{q310}","A1V1"])]
 candidates.append({"lane":"P3","rule_id":"D02_P3_CONDITIONAL_REVERSAL","family":"CONDITIONAL_REVERSAL_OR_SIMPSON","form":"REVERSAL_GRID","parameters":{"stratum_atom_ids":["Q310V1","Q310V2","Q310V3"]},"validation":{"kind":"CONDITIONAL_REVERSAL","target_cell":exact_decimal(5)},"query_roles":p3})
 for q2 in range(1,6):
  for q7 in range(1,6):
   tc=[exact_decimal(q2),exact_decimal(q7)]
   candidates.append({"lane":"P4","rule_id":"D02_P4_MINORITY_NONMODAL_COMPLETE_JOINT_CELLS","family":"MINORITY_OR_NONMODAL_DEPARTURE","form":"BASE_QUERY","parameters":{"target_cell":tc},"validation":{"kind":"TARGET_CELL_SUPPORTED","target_cell":tc},"query_roles":[_role("BASE","T_Q301_2_Q301_7_RAW",["A000"])]})
 if len(candidates)!=50 or sum(len(c["query_roles"]) for c in candidates)!=77: raise G02ExecutionError("frozen frontier count mismatch")
 keyed=[]
 for c in candidates:
  material={"contract":CONTRACT_ID,"d02_frontier_blob":D02_FRONTIER_GIT_BLOB,"f02_frontier_readoption_hash":F02_FRONTIER_READOPTION_HASH,"candidate_semantics":c}
  h=sh(material); keyed.append({**c,"execution_candidate_id":f"urn:rawlsing:prev3:g02:execution-candidate:sha256:{h}","execution_candidate_hash":h})
 keyed=sorted(keyed,key=lambda x:x["execution_candidate_hash"])
 mat={"schema":"G02_F02_RESEALED_D02_PREEXECUTION_FRONTIER_SEAL@1.0.0","d02_authority_commit":D02_AUTHORITY_COMMIT,"d02_frontier_git_blob":D02_FRONTIER_GIT_BLOB,"f02_return_commit":F02_RETURN_COMMIT,"f02_frontier_readoption_hash":F02_FRONTIER_READOPTION_HASH,"f02_release_ref":F02_RELEASE_REF,"candidate_count":50,"query_role_count":77,"candidate_execution_keys":[c["execution_candidate_hash"] for c in keyed],"lane_expectations":LANE_EXPECTATIONS,"invariants":{"maximum_conditioner_arity_K":3,"maximum_target_arity_J":2,"pruning_contract":{"kind":"NONE_EXACT_EVALUATE_ALL"},"rng_policy":"NONE","score_or_top_k":"FORBIDDEN","post_data_frontier_mutation":"FORBIDDEN","selector_substitution_after_execution_start":"FORBIDDEN","order":"CANONICAL_G02_EXECUTION_CANDIDATE_HASH_ORDER_OVER_F02_RESEALED_FROZEN_MEMBERSHIP"},"authority_note":"EXECUTION_KEYS_ARE_G02_RECEIPT_KEYS__NOT_A_CLAIM_TO_RECOVER_OR_REPLACE_PRE553_CANONICAL_CANDIDATE_OBJECT_IDENTITIES"}
 return {"frontier":keyed,"preexecution_frontier_seal":mat,"preexecution_frontier_seal_hash":sh(mat)}

def _typed_native(v):
 if v is None: return "MISSING",None
 try:
  if math.isnan(v): return "MISSING",None
 except (TypeError,ValueError): pass
 if hasattr(v,"item"): v=v.item()
 if isinstance(v,float):
  if not v.is_integer(): raise G02ExecutionError("nonintegral q310/q311")
  v=int(v)
 if v not in (1,2,3): raise G02ExecutionError(f"q310/q311 outside governed domain: {v!r}")
 return "SUBSTANTIVE_RESPONSE",int(v)
def scan_f02_selectors(records):
 if len(records)!=SOURCE_ROWS: raise G02ExecutionError(f"expected {SOURCE_ROWS} exact source rows")
 out={}
 for q in ("q310","q311"):
  total=hashlib.sha256(); hs={k:hashlib.sha256() for k in ("1","2","3","MISSING")}; counts={k:0 for k in hs}
  for i,row in enumerate(records):
   state,value=_typed_native(row[q]); key="MISSING" if state=="MISSING" else str(value); b=(cjson({"row_ordinal":i,"response_state":state,"raw_native_value":value})+"\n").encode(); total.update(b); hs[key].update(b); counts[key]+=1
  out[q]={"counts":counts,"row_semantic_root_sha256":total.hexdigest(),"selector_roots":{k:hs[k].hexdigest() for k in hs}}
 return out
def _value(row,name):
 v=row[name]
 if v is None: return None
 try:
  if math.isnan(v): return None
 except (TypeError,ValueError): pass
 if hasattr(v,"item"): v=v.item()
 if isinstance(v,float):
  if not v.is_integer(): raise G02ExecutionError(f"nonintegral response {name}")
  return int(v)
 if isinstance(v,int) and not isinstance(v,bool): return v
 raise G02ExecutionError(f"unexpected response {name}={v!r}")
def _matches(row,atom):
 if atom=="A000": return True
 if atom=="A1V1": return _value(row,"q301_2")==1
 if atom=="A1V5": return _value(row,"q301_2")==5
 if atom.startswith("Q310V"): return _value(row,"q310")==int(atom[-1])
 if atom.startswith("Q311V"): return _value(row,"q311")==int(atom[-1])
 raise G02ExecutionError(f"unknown frozen atom {atom}")
def _query(records,q,atoms):
 selected=[r for r in records if all(_matches(r,a) for a in atoms)]; den=len(selected)
 if q=="T_Q301_2_RAW": cells={str(v):sum(_value(r,"q301_2")==v for r in selected) for v in range(1,6)}; topology="SCALAR_Q301_2_NATIVE_1_5"
 elif q=="T_Q301_7_RAW": cells={str(v):sum(_value(r,"q301_7")==v for r in selected) for v in range(1,6)}; topology="SCALAR_Q301_7_NATIVE_1_5"
 elif q=="T_Q301_2_Q301_7_RAW": cells={f"{a},{b}":sum(_value(r,"q301_2")==a and _value(r,"q301_7")==b for r in selected) for a in range(1,6) for b in range(1,6)}; topology="JOINT_Q301_2_X_Q301_7_NATIVE_5X5"
 else: raise G02ExecutionError(f"unknown query template {q}")
 result={"typed_state":"QUERY_RESULT_AVAILABLE","query_template_id":q,"query_template_ref":QUERY_REFS[q],"condition_atom_ids":list(atoms),"condition_atom_refs":[ATOM_REFS[a] for a in atoms],"raw_denominator_support":den,"raw_complete_cell_support":sum(cells.values()),"complete_cell_counts":cells,"target_topology":topology,"measure_kind":"RAW","empirical_universe_ref":EMPIRICAL_UNIVERSE_REF,"risk_set_ref":RISK_SET_REF,"measure_basis_ref":MEASURE_BASIS_REF,"release_ref":F02_RELEASE_REF,"negative_ceiling":NEGATIVE_CEILING}
 return {**result,"query_result_hash":sh(result)}
def _frac_cell(r,key):
 den=int(r["raw_denominator_support"]); return None if den==0 else Fraction(int(r["complete_cell_counts"].get(key,0)),den)
def _validate(candidate,roles):
 v=candidate["validation"]; kind=v["kind"]; details={}
 if kind=="TARGET_CELL_SUPPORTED":
  tc=v["target_cell"]; r=next(iter(roles.values())); key=f"{tc[0]['$exact_decimal']},{tc[1]['$exact_decimal']}" if isinstance(tc,list) else tc["$exact_decimal"]; n=int(r["complete_cell_counts"].get(key,0)); supported=int(r["raw_denominator_support"])>0 and n>0; details={"target_cell":tc,"target_support":n,"raw_denominator_support":int(r["raw_denominator_support"])}
 elif kind=="JOINT_NOT_PRODUCT_OF_MARGINALS":
  j,m0,m1=roles["JOINT"],roles["MARGINAL_0"],roles["MARGINAL_1"]; jd,d0,d1=int(j["raw_denominator_support"]),int(m0["raw_denominator_support"]),int(m1["raw_denominator_support"]); supported=False; witness=None
  for a in range(1,6):
   for b in range(1,6):
    obs=int(j["complete_cell_counts"][f"{a},{b}"]); c0=int(m0["complete_cell_counts"][str(a)]); c1=int(m1["complete_cell_counts"][str(b)])
    if obs*d0*d1!=jd*c0*c1: supported=True; witness={"cell":[a,b],"joint_count":obs,"joint_denominator":jd,"marginal_0_count":c0,"marginal_0_denominator":d0,"marginal_1_count":c1,"marginal_1_denominator":d1}; break
   if supported: break
  details={"first_exact_dependence_witness":witness}
 elif kind=="DISTRIBUTION_DIFFERS_FROM_BASELINE":
  c,b=roles["CONDITION"],roles["BASELINE"]; cd,bd=int(c["raw_denominator_support"]),int(b["raw_denominator_support"]); supported=False; witness=None
  if cd>0 and bd>0:
   for x in range(1,6):
    cc,bc=int(c["complete_cell_counts"][str(x)]),int(b["complete_cell_counts"][str(x)])
    if cc*bd!=bc*cd: supported=True; witness={"cell":x,"condition_count":cc,"condition_denominator":cd,"baseline_count":bc,"baseline_denominator":bd}; break
  details={"first_exact_distribution_difference_witness":witness}
 elif kind=="CONDITIONAL_REVERSAL":
  target=v["target_cell"]["$exact_decimal"]; pp,pn=_frac_cell(roles["POOLED_POS"],target),_frac_cell(roles["POOLED_NEG"],target); sign=lambda x:1 if x>0 else (-1 if x<0 else 0); supported=False; pooled_sign=0; signs=[]; rates={}
  if pp is not None and pn is not None:
   pooled_sign=sign(pp-pn); rates.update({"POOLED_POS":pp,"POOLED_NEG":pn})
   for s in (1,2,3):
    pr,nr=_frac_cell(roles[f"STRATUM:Q310V{s}:POS"],target),_frac_cell(roles[f"STRATUM:Q310V{s}:NEG"],target); rates[f"Q310V{s}_POS"]=pr; rates[f"Q310V{s}_NEG"]=nr; signs.append(0 if pr is None or nr is None else sign(pr-nr))
   supported=pooled_sign!=0 and bool(signs) and all(x!=0 and x==signs[0] for x in signs) and signs[0]==-pooled_sign
  details={"target_cell":v["target_cell"],"pooled_sign":pooled_sign,"stratum_signs":signs,"exact_rates":rates}
 else: raise G02ExecutionError(f"unknown validator {kind}")
 return ("EVALUATED_SUPPORTED" if supported else "EVALUATED_VALID_EMPTY"),canon(details)

def execute_records(records,compiled):
 if len(records)!=SOURCE_ROWS: raise G02ExecutionError(f"production execution requires {SOURCE_ROWS} rows")
 scan=scan_f02_selectors(records)
 if canon(scan)!=canon(EXPECTED_F02_SCAN): raise G02ExecutionError("F02 q310/q311 selector replay mismatch")
 role_receipts=[]; candidate_receipts=[]
 for candidate in compiled["frontier"]:
  role_map={}; hashes=[]
  for role in candidate["query_roles"]:
   result=_query(records,role["query_template_id"],role["condition"]["atom_ids"]); material={"schema":"G02_LEARNED_QUERY_ROLE_EXECUTION_RECEIPT@1.0.0","contract":CONTRACT_ID,"execution_candidate_hash":candidate["execution_candidate_hash"],"role":role["role"],"frozen_role_semantics":role,"result":result,"authority":{"d02_authority_commit":D02_AUTHORITY_COMMIT,"f02_return_commit":F02_RETURN_COMMIT,"f02_frontier_readoption_hash":F02_FRONTIER_READOPTION_HASH}}; rh=sh(material); receipt={**material,"receipt_id":f"urn:rawlsing:prev3:g02:query-role-receipt:sha256:{rh}","receipt_hash":rh}; role_receipts.append(receipt); hashes.append(rh); role_map[role["role"]]=result
  state,details=_validate(candidate,role_map); cmat={"schema":"G02_LEARNED_CANDIDATE_TERMINAL_RECEIPT@1.0.0","contract":CONTRACT_ID,"execution_candidate_id":candidate["execution_candidate_id"],"execution_candidate_hash":candidate["execution_candidate_hash"],"lane":candidate["lane"],"rule_id":candidate["rule_id"],"family":candidate["family"],"form":candidate["form"],"parameters":candidate["parameters"],"validation":candidate["validation"],"terminal_state":state,"validation_details":details,"query_role_receipt_hashes":hashes,"negative_ceiling":NEGATIVE_CEILING}; ch=sh(cmat); candidate_receipts.append({**cmat,"receipt_id":f"urn:rawlsing:prev3:g02:candidate-receipt:sha256:{ch}","receipt_hash":ch})
 if len(candidate_receipts)!=50 or len(role_receipts)!=77: raise G02ExecutionError("postexecution count mismatch")
 byhash={c["execution_candidate_hash"]:c for c in compiled["frontier"]}; lanes={}
 for lane,exp in LANE_EXPECTATIONS.items():
  cs=[c for c in candidate_receipts if c["lane"]==lane]; rs=[r for r in role_receipts if byhash[r["execution_candidate_hash"]]["lane"]==lane]
  if len(cs)!=exp["candidate_count"] or len(rs)!=exp["query_role_count"]: raise G02ExecutionError(f"{lane} lane accounting mismatch")
  lanes[lane]={"candidate_count":len(cs),"query_role_count":len(rs),"supported_candidates":sum(c["terminal_state"]=="EVALUATED_SUPPORTED" for c in cs),"valid_empty_candidates":sum(c["terminal_state"]=="EVALUATED_VALID_EMPTY" for c in cs),"other_terminal_candidates":sum(c["terminal_state"] not in {"EVALUATED_SUPPORTED","EVALUATED_VALID_EMPTY"} for c in cs)}
 if lanes["P0"]["supported_candidates"]<1: raise G02ExecutionError("required P0 positive control absent")
 semantic={"schema":"G02_PREV3_LEARNED_REAL_EXECUTION_RESULT@1.0.0","contract":CONTRACT_ID,"status":"PASS__FULL_FROZEN_FRONTIER_EXECUTED","source":{"sha256":SOURCE_SHA256,"rows":SOURCE_ROWS,"variables":SOURCE_VARIABLES},"logical_execution_surface":{"base_c11_ref":BASE_C11_REF,"f02_release_ref":F02_RELEASE_REF,"f02_replay_hash":F02_REPLAY_HASH,"f02_frontier_readoption_hash":F02_FRONTIER_READOPTION_HASH,"ephemeral_transport_note":"EXACT_SOURCE_BYTES_USED_ONLY_TO_REPLAY_ACCEPTED_LOGICAL_RELEASE_MEMBERS__NO_NEW_SOURCE_SEMANTICS"},"preexecution_frontier_seal_hash":compiled["preexecution_frontier_seal_hash"],"candidate_count":50,"query_role_execution_count":77,"candidate_terminal_counts":{"EVALUATED_SUPPORTED":sum(c["terminal_state"]=="EVALUATED_SUPPORTED" for c in candidate_receipts),"EVALUATED_VALID_EMPTY":sum(c["terminal_state"]=="EVALUATED_VALID_EMPTY" for c in candidate_receipts)},"p0_positive_control_supported_count":lanes["P0"]["supported_candidates"],"lane_accounting":lanes,"f02_selector_source_replay":scan,"candidate_receipts":candidate_receipts,"query_role_receipts":role_receipts,"frontier_mutation_count":0,"selector_substitution_after_execution_start_count":0,"pruned_candidate_count":0,"ranked_candidate_count":0,"structural_admission_count":0,"causal_promotion_count":0,"population_generalization_count":0,"person_state_count":0,"v3_state_count":0,"negative_ceiling":NEGATIVE_CEILING}
 return {**semantic,"semantic_replay_hash":sh(semantic)}

def load_carrier(path):
 p=Path(path); observed=file_sha256(p)
 if observed!=SOURCE_SHA256: raise G02ExecutionError(f"source SHA mismatch: {observed}")
 import pandas as pd
 frame=pd.read_stata(p,columns=["q301_2","q301_7","q310","q311"],convert_categoricals=False)
 if len(frame)!=SOURCE_ROWS: raise G02ExecutionError("source row denominator mismatch")
 return frame.to_dict(orient="records")
def execute_carrier(path):
 compiled=compile_frontier(); records=load_carrier(path); return execute_records(records,compiled)
def main(argv=None):
 ap=argparse.ArgumentParser(); ap.add_argument("--source",required=True); ap.add_argument("--output",required=True); args=ap.parse_args(argv); result=execute_carrier(args.source); Path(args.output).write_text(json.dumps(canon(result),indent=2,sort_keys=True,ensure_ascii=False)+"\n",encoding="utf-8"); return 0
if __name__=="__main__": raise SystemExit(main())

__all__=["CONTRACT_ID","SOURCE_SHA256","SOURCE_ROWS","F02_RELEASE_REF","F02_FRONTIER_READOPTION_HASH","EXPECTED_F02_SCAN","LANE_EXPECTATIONS","NEGATIVE_CEILING","G02ExecutionError","compile_frontier","scan_f02_selectors","execute_records","execute_carrier","file_sha256","canon","cjson","sh"]
