#!/usr/bin/env python3
"""I06 Lebanon parity-prep harness. Oracle is never loaded before observations are sealed."""
from __future__ import annotations
import argparse,csv,hashlib,io,json,math
from pathlib import Path

SEED_SCHEMA="I06_LEBANON_CONTROLLER_SEED@1.0.0"; OBS_SCHEMA="I06_CONTROLLER_OBSERVATION@1.0.0"
ORACLE_SCHEMA="I06_FROZEN_L02_PARITY_ORACLE@1.0.0"; RECEIPT_SCHEMA="I06_LEBANON_PARITY_RECEIPT@1.0.0"
AUTH="9bafaf2cb96cc3fb46fef6785d486f08987ab71c"; POLICY="Authority37_Controller_Law_V1"
SOURCE_HASHES={"sav":"a5e83a953f03dd890e076a51da473051f1cfd1ca2e8ab93c2172eeb2517af998","questionnaire":"d72c3afc4529703376dc1133a3d984541c2ceebd1af6cb03a1562f6ce104c2fb","codebook":"328bbbbfa6cb8a78eacad52847b1432a56a81ec9ecfcd4f18754e05532afd4fc"}
Q873={"Q873_1":"socioeconomic_class","Q873_2":"region","Q873_3":"skin_color","Q873_4":"race_or_ethnicity","Q873_5":"nationality","Q873_6":"religion","Q873_7":"gender","Q873_8":"tribe","Q873_9":"age","Q873_10":"sexual_orientation","Q873_11":"disability_status","Q873_12":"migration_status","Q873_13":"none_of_these","Q873_98":"dont_know","Q873_99":"refused"}
PATTERN_FIELDS=["branch_id","pattern_rank","response_pattern","n","weighted_n","unweighted_pct","weighted_pct","support_class"]
BAD_KEYS={"oracle","expected","winner","winners","modal_result","modal_pattern","branch_membership","branch_memberships","branch_support","branch_supports","response_pattern_winner","response_pattern_winners","parity_answer","parity_answers","l02"}
BAD_LITERALS=["c9acd7e9ff887dd3a4a29d91f45688cb9c0705a3","57.460811420389824","47.287269199071936","43.52302383575661","0.06219659150220942","0.02866172519445555","0.1307397230551967","8a642a5cf133843512d84b039af475f70c13b739f3e26908899193ccee886ed9"]

def hbytes(b): return hashlib.sha256(b).hexdigest()
def hfile(p):
 h=hashlib.sha256()
 with Path(p).open("rb") as f:
  for b in iter(lambda:f.read(1<<20),b""): h.update(b)
 return h.hexdigest()
def cjson(x): return (json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False)+"\n").encode()
def load(p): return json.loads(Path(p).read_text())
def write(p,x): Path(p).write_bytes(cjson(x))

def verify(sav,qnr,cb):
 got={"sav":hfile(sav),"questionnaire":hfile(qnr),"codebook":hfile(cb)}
 if got!=SOURCE_HASHES: raise SystemExit(f"SOURCE_HASH_MISMATCH expected={SOURCE_HASHES} got={got}")
 return got

def q873_rows(cb):
 found={}
 with Path(cb).open(encoding="utf-8-sig",newline="") as f:
  for r in csv.DictReader(f):
   n=r.get("var_name","")
   if n in Q873: found[n]={"variable":n,"semantic_name":Q873[n],"question_text":r.get("question_text",""),"sav_variable_label":r.get("sav_variable_label",""),"substantive_value_labels":r.get("substantive_value_labels",""),"special_value_labels":r.get("special_value_labels",""),"note":r.get("note","")}
 order=[f"Q873_{i}" for i in range(1,14)]+["Q873_98","Q873_99"]
 missing=[x for x in order if x not in found]
 if missing: raise SystemExit(f"CODEBOOK_MISSING_Q873_VARIABLES {missing}")
 return [found[x] for x in order]

def seed_for(sav,qnr,cb):
 hs=verify(sav,qnr,cb)
 s={"schema":SEED_SCHEMA,"authority":{"controller_law":POLICY,"authority37_commit":AUTH},"source":{"family":"ArabBarometer","wave":"VIII","sav_sha256":hs["sav"],"questionnaire_sha256":hs["questionnaire"],"codebook_sha256":hs["codebook"]},"root_request":{"substantive_surface":"Q873","source_universes":[{"scope":"WAVE8_ROUTED"},{"scope":"COUNTRY_EXACT","variable":"COUNTRY","value":10}]},"q873_surface":{"form":"MULTI_SELECT_0_1_TOGGLES","variables":q873_rows(cb),"substantive_denominator_rule":"Q873_1 nonmissing AND Q873_98 != 1 AND Q873_99 != 1","none_exclusivity_rule":"Q873_13=1 excludes every other substantive Q873 selection"},"routing_authority":{"Q873_8":{"asked_only_when_COUNTRY_in":[7,8,9]},"Q873_10":{"asked_only_when_COUNTRY_in":[10,21]},"missing_routed_item_state":"STRUCTURAL_MISSING_NOT_NONSELECTION"},"weight_authority":{"field":"WT","use":"GOVERNED_RELEASED_ANALYSIS_WEIGHT","retain_unweighted_n":True,"no_active_spss_weight_command":True},"coordinate_authority":{"source_coordinates":["COUNTRY","Q1003","Q1012","Q1012A_MUSLIM","Q1012A_CHRISTIAN","Q609","Q1015","Q1016","Q13","Q1001","Q1002","STRATUM","PSU"],"derived_descriptive_coordinates":{"DENOMINATION_COMBINED":"route-preserving union of Q1012A_MUSLIM/Q1012A_CHRISTIAN under Q1012","COUNTRY_INCOME_RANK_QUINTILE":"country-local percentile quintile of Q1015","AGE_BAND":"18-29|30-44|45-59|60+"},"role_ceiling":"POSITIONAL_OR_DEMOGRAPHIC_CONDITIONERS_NEVER_ATTITUDE_NODES"},"controller_policy":{"modal_support_basis":"WT_WHEN_POSITIVE_WEIGHT_AUTHORITY_ELSE_RAW","ties":"RETAIN_MAXIMAL_TIE_AS_MULTIMODAL_UNRESOLVED_SET","candidate_reachability":"EXHAUSTIVE_ALL_LAWFUL_ATOMIC_CATEGORICAL_BOOLEAN_COORDINATE_CONDITIONS","determinicity":{"metric":"NORMALIZED_MUTUAL_INFORMATION_BY_TARGET_ENTROPY","weight_basis":"WT_WHEN_GOVERNED_ELSE_RAW","role":"DESCRIPTIVE_RANK_ONLY_NOT_REACHABILITY"},"branch_roles":["CONFORMER","DEVIANT_EXIT","ALT_CONVERGER","ALT_MINORITY"],"minimum_split_raw_n":50,"minimum_report_raw_n":25,"maximum_depth":4,"retention_rule":"STOP_RECURSION_NEVER_DELETES_RETAINED_SUPPORTED_BRANCH","maximum_target_arity_J":3},"output_contract":{"schema":OBS_SCHEMA,"required_surfaces":["source","semantics","routing","branches","determinicity","response_pattern_census","replay"],"response_pattern_row_fields":PATTERN_FIELDS,"determinicity_fields":["predictor","normalized_mi"]}}
 audit_seed(s); return s

def keys(x):
 if isinstance(x,dict):
  for k,v in x.items(): yield str(k); yield from keys(v)
 elif isinstance(x,list):
  for v in x: yield from keys(v)
def audit_seed(s):
 if s.get("schema")!=SEED_SCHEMA: raise SystemExit("SEED_SCHEMA_MISMATCH")
 bad=sorted({k for k in keys(s) if k.lower() in BAD_KEYS})
 if bad: raise SystemExit(f"SEED_FORBIDDEN_KEYS {bad}")
 text=cjson(s).decode(); leak=[x for x in BAD_LITERALS if x in text]
 if leak: raise SystemExit(f"SEED_ORACLE_LITERAL_LEAK {leak}")

def at(o,path):
 for p in path.split("."):
  if not isinstance(o,dict) or p not in o: raise KeyError(path)
  o=o[p]
 return o
def close(a,b,t):
 try:return math.isclose(float(a),float(b),rel_tol=0,abs_tol=t)
 except:return False
def pattern_bytes(rows):
 s=io.StringIO(newline=""); w=csv.DictWriter(s,fieldnames=PATTERN_FIELDS,lineterminator="\n",extrasaction="ignore"); w.writeheader()
 for r in rows:w.writerow({k:r[k] for k in PATTERN_FIELDS})
 return s.getvalue().encode()
def projection(o):
 return {k:o.get(k) for k in ["schema","source","semantics","routing","branches","determinicity","response_pattern_census"]}|{"replay":{k:(o.get("replay") or {}).get(k) for k in ["seed_sha256","controller_authority_ref","controller_policy_ref"]}}

def compare_obs(o,q):
 C=[]
 def ex(n,p,e):
  try:g=at(o,p); ok=g==e
  except KeyError:g="<MISSING>";ok=False
  C.append({"check":n,"kind":"EXACT","observed":g,"expected":e,"pass":ok})
 def fl(n,p,e,t):
  try:g=at(o,p);ok=close(g,e,t)
  except KeyError:g="<MISSING>";ok=False
  C.append({"check":n,"kind":"FLOAT_ABS","observed":g,"expected":e,"tolerance":t,"pass":ok})
 ex("observation_schema","schema",OBS_SCHEMA); ex("sav_sha256","source.sav_sha256",q["source"]["sav_sha256"]); ex("questionnaire_sha256","source.questionnaire_sha256",q["source"]["questionnaire_sha256"]); ex("codebook_sha256","source.codebook_sha256",q["source"]["codebook_sha256"]); ex("weight_field","source.weight_field","WT")
 for k,e in q["semantics"].items(): ex(f"semantics.{k}",f"semantics.{k}",e)
 for k,e in q["routing"]["exact"].items(): ex(f"routing.{k}",f"routing.{k}",e)
 for k,e in q["routing"]["float"].items(): fl(f"routing.{k}",f"routing.{k}",e,q["tolerances"]["weighted_or_pct_abs"])
 for b,s in q["branches"].items():
  for k,e in s.get("exact",{}).items(): ex(f"branches.{b}.{k}",f"branches.{b}.{k}",e)
  for k,e in s.get("float",{}).items(): fl(f"branches.{b}.{k}",f"branches.{b}.{k}",e,q["tolerances"]["weighted_or_pct_abs"])
 d=o.get("determinicity",{})
 for t,ers in q["determinicity"].items():
  gr=d.get(t,[]); C.append({"check":f"determinicity.{t}.length","kind":"EXACT","observed":len(gr),"expected":len(ers),"pass":len(gr)==len(ers)})
  for i,e in enumerate(ers):
   g=gr[i] if i<len(gr) else {}; C.append({"check":f"determinicity.{t}[{i}].predictor","kind":"EXACT","observed":g.get("predictor","<MISSING>"),"expected":e["predictor"],"pass":g.get("predictor")==e["predictor"]}); v=g.get("normalized_mi","<MISSING>"); C.append({"check":f"determinicity.{t}[{i}].normalized_mi","kind":"FLOAT_ABS","observed":v,"expected":e["normalized_mi"],"tolerance":q["tolerances"]["normalized_mi_abs"],"pass":close(v,e["normalized_mi"],q["tolerances"]["normalized_mi_abs"])})
 rows=o.get("response_pattern_census")
 if not isinstance(rows,list): C.append({"check":"response_pattern_census.present","kind":"EXACT","observed":type(rows).__name__,"expected":"list","pass":False})
 else:
  C.append({"check":"response_pattern_census.row_count","kind":"EXACT","observed":len(rows),"expected":q["response_pattern_census"]["data_rows"],"pass":len(rows)==q["response_pattern_census"]["data_rows"]})
  try: ph=hbytes(pattern_bytes(rows))
  except Exception as e: ph=f"<SERIALIZATION_ERROR:{e}>"
  C.append({"check":"response_pattern_census.sha256","kind":"EXACT","observed":ph,"expected":q["response_pattern_census"]["canonical_monolithic_sha256"],"pass":ph==q["response_pattern_census"]["canonical_monolithic_sha256"]})
 return C

def prepare(a):
 s=seed_for(Path(a.sav),Path(a.questionnaire),Path(a.codebook)); write(a.seed_out,s)
 if cjson(s)!=cjson(seed_for(Path(a.sav),Path(a.questionnaire),Path(a.codebook))): raise SystemExit("SEED_REPLAY_NONDETERMINISTIC")
 print(json.dumps({"status":"PASS","seed_sha256":hfile(a.seed_out),"seed_out":a.seed_out},sort_keys=True))
def audit(a): s=load(a.seed);audit_seed(s);print(json.dumps({"status":"PASS","seed_sha256":hfile(a.seed)},sort_keys=True))
def compare(a):
 s=load(a.seed);audit_seed(s);ss=hfile(a.seed); ob=Path(a.observation).read_bytes(); oh=hbytes(ob); o=json.loads(ob); r=None;rh=None;eq=None;ps=hbytes(cjson(projection(o)))
 if a.replay_observation: rb=Path(a.replay_observation).read_bytes();rh=hbytes(rb);r=json.loads(rb);eq=cjson(projection(o))==cjson(projection(r))
 C=[]
 for label,x in [("",o),("replay_run.",r)] if r is not None else [("",o)]:
  rr=(x.get("replay") or {}); specs=[("seed_sha256",ss),("controller_authority_ref",AUTH),("controller_policy_ref",POLICY)]
  for k,e in specs:C.append({"check":f"{label}replay.{k}" if not label else f"{label}{k}","kind":"EXACT","observed":rr.get(k,"<MISSING>"),"expected":e,"pass":rr.get(k)==e})
 # Oracle is deliberately opened only after seed/observations and bindings are sealed above.
 qs=hfile(a.oracle); q=load(a.oracle)
 if q.get("schema")!=ORACLE_SCHEMA: raise SystemExit("ORACLE_SCHEMA_MISMATCH")
 C+=compare_obs(o,q); C.append({"check":"deterministic_replay.parity_projection_equal" if r else "deterministic_replay.second_observation_present","kind":"EXACT","observed":eq if r else False,"expected":True,"pass":eq is True if r else False})
 receipt={"schema":RECEIPT_SCHEMA,"status":"PASS" if all(x["pass"] for x in C) else "FAIL","anti_leak_phase_order":"OBSERVATION_SEALED_BEFORE_ORACLE_LOAD","seed_sha256_before_oracle_load":ss,"observation_sha256_before_oracle_load":oh,"observation_parity_projection_sha256_before_oracle_load":ps,"replay_observation_sha256_before_oracle_load":rh,"oracle_sha256_loaded_after_observation_seal":qs,"checks":C};write(a.receipt,receipt);print(json.dumps({"status":receipt["status"],"receipt":a.receipt,"failed":[x["check"] for x in C if not x["pass"]]},sort_keys=True));
 if receipt["status"]!="PASS":raise SystemExit(2)
def selftest(a):
 got=verify(a.sav,a.questionnaire,a.codebook); s1=seed_for(a.sav,a.questionnaire,a.codebook);s2=seed_for(a.sav,a.questionnaire,a.codebook); cm=cjson(s1)==cjson(load(a.seed)); inj=False;bad=json.loads(json.dumps(s1));bad["expected"]={"leaked":True}
 try:audit_seed(bad)
 except SystemExit:inj=True
 q=load(a.oracle); checks={"source_hash_verification":"PASS","seed_deterministic_replay":"PASS" if cjson(s1)==cjson(s2) else "FAIL","committed_seed_matches_regeneration":"PASS" if cm else "FAIL","anti_leak_injection_rejected":"PASS" if inj else "FAIL","oracle_schema":"PASS" if q.get("schema")==ORACLE_SCHEMA else "FAIL","oracle_source_hash_binding":"PASS" if all(q["source"][k+"_sha256"]==v for k,v in got.items()) else "FAIL","comparator_rejects_incomplete_observation":"PASS" if any(not x["pass"] for x in compare_obs({"schema":OBS_SCHEMA},q)) else "FAIL","production_controller_execution":"NOT_RUN_PREP_ONLY"}; ok=all(v=="PASS" for k,v in checks.items() if k!="production_controller_execution"); print(json.dumps({"status":"PASS" if ok else "FAIL","checks":checks},sort_keys=True));
 if not ok:raise SystemExit(2)
def main():
 p=argparse.ArgumentParser();sp=p.add_subparsers(dest="cmd",required=True)
 x=sp.add_parser("prepare");[x.add_argument("--"+k,required=True) for k in ["sav","questionnaire","codebook","seed-out"]];x.set_defaults(fn=prepare)
 x=sp.add_parser("audit-seed");x.add_argument("--seed",required=True);x.set_defaults(fn=audit)
 x=sp.add_parser("compare");[x.add_argument("--"+k,required=True) for k in ["seed","observation","oracle","receipt"]];x.add_argument("--replay-observation");x.set_defaults(fn=compare)
 x=sp.add_parser("selftest");[x.add_argument("--"+k,required=True,type=Path if k in ["sav","questionnaire","codebook"] else str) for k in ["sav","questionnaire","codebook","seed","oracle"]];x.set_defaults(fn=selftest)
 a=p.parse_args();a.fn(a)
if __name__=="__main__":main()
