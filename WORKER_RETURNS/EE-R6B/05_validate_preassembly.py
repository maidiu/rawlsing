from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
HERE=Path(__file__).resolve().parent
M="01_FINAL_PREASSEMBLY_MANIFEST.json"; R="02_READY_14_EXECUTION_ORACLE_PROFILES.json"; S="03_EE_R6A_FOUR_CELL_SPLICE_CONTRACT.json"; O="04_EXECUTION_MEASUREMENT_ORDER_RESET_LAW.json"
class ValidationError(ValueError): pass
def fail(x): raise ValidationError(x)
def load(p): return json.loads(Path(p).read_text())
def cbytes(x): return json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()
def hobj(x): return hashlib.sha256(cbytes(x)).hexdigest()
PINS={"EE-W1":"1637b53abf90cac8a57857aaa5571dbb4278dfa9","EE-W4":"b74b7cf0b8cb3f7e5fae80094a7db7d26ce20457","EE-R2E":"7f7f716ae9cd26bbb1fe5adc7a5ff1024955e285","EE-W5":"4cbd4c0bba8b6fd9809209d9fd61d730b8a40747","EE-R3B":"1dc316b4a388949c1736aa65a20c8d43cfb2c8ba","EE-R3E":"dd218b1182b29259a19837c89222cbc47024b2ec","EE-R3F":"9082b85d0963c6505e2b9dc9b417cfb881b8cb1b","EE-R4B":"e5012ff2d9116e65850402b4432899de4937ed5e","EE-R5B":"02d32036db49c70ff137f1730d0ff95b571040d3"}
OWNERS={"A":["0b96b8de9aac774566f872cf0630ebd4ddeb70e6","rawlsing_next/pre553_r5_source_backed_adapter.py","d4915e7e6755ba1850756aebff72f982f73a332b",[]],"B":["0b96b8de9aac774566f872cf0630ebd4ddeb70e6","rawlsing_next/pre553_source_backed_c11_facade.py","7c509c2098d0030f253344eb3f682471378812a8",[]],"C":["0b96b8de9aac774566f872cf0630ebd4ddeb70e6","rawlsing_next/pre553_route_c_accelerators.py","abfdc91a71ef5e18c4a8a6bf62fa65750d8d9889",["CACC1_LITS1_SEMANTIC_EXECUTION_BUNDLE","CACC2_FRONTIER_ATOMIC_PREDICATE_RISK_MASK_BANK"]]}
SRC={"WVS7":["EEU_WVS7_WAVE7_EXACT_SOURCE","2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d",185163494],"LiTS-I":["EEU_LITS_I_2006_EXACT_SOURCE","7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09",139531180]}
ORDER=["WVS7::OP001","WVS7::OP002","WVS7::OP003","WVS7::OP004","WVS7::OP005","WVS7::OP006","WVS7::OP020","WVS7::OP021","WVS7::OP022","LiTS-I::OP001","LiTS-I::OP002","LiTS-I::OP003","LiTS-I::OP004","LiTS-I::OP005","LiTS-I::OP006","LiTS-I::OP020","LiTS-I::OP021","LiTS-I::OP022"]
PENDING=ORDER[2:6]; READY=[x for x in ORDER if x not in PENDING]
LIFE={"WVS7::OP020":["WORKER_RETURNS/EE-R3E/profiles/WVS7_OP020.json","388674dd8759a2b4b14ac5a1238828ef8d1204db"],"WVS7::OP021":["WORKER_RETURNS/EE-R3E/profiles/WVS7_OP021.json","20d4c2685715570f4f1ce88052026cadb166de5f"],"WVS7::OP022":["WORKER_RETURNS/EE-R3E/profiles/WVS7_OP022.json","a9e89cde8b62c3ae7f76383f4d8757ea9cb963e1"],"LiTS-I::OP020":["WORKER_RETURNS/EE-R3E/profiles/LITS_OP020.json","9e3cc4ab92e4a72fe509691393f4ec5721ddc165"],"LiTS-I::OP021":["WORKER_RETURNS/EE-R3E/profiles/LITS_OP021.json","64a4a43bf8787f0ea2b849cdab346a3e968349af"],"LiTS-I::OP022":["WORKER_RETURNS/EE-R3E/profiles/LITS_OP022.json","10fa0c9980267112cd88a094a6b6eb80e40aa831"]}
QIDS=["question_impl.phase0.041c03bbacabe4e8d802","question_impl.phase0.075b1650737d99679b9c"]; PAIR="5636b4d8cb5249f876dd1bd14e41d96cf903a7b52ae0dfeab9bc76d2152f2406"
MAT="BEFORE_ANY_CANDIDATE_INVOCATION__RUN_THE_PINNED_CANDIDATE_INDEPENDENT_REFERENCE_PROCEDURE_ON_THE_EXACT_SOURCE_AND_AUTHORITY_INPUTS__CANONICALIZE_THE_REFERENCE_RESULT_WITH_THE_PINNED_EE_W4_CANONICAL_JSON_FUNCTION__SET_ORACLE.semantic_output_sha256_TO_ITS_SHA256__THE_SAME_HASH_IS_USED_FOR_A_B_C"
MET=["wall_ns","cpu_user_ns","cpu_system_ns","peak_rss_bytes","scratch_bytes_before","scratch_bytes_after","peak_scratch_bytes_observed","peak_scratch_file_count_observed","max_single_temp_object_bytes_observed","durable_bytes_before","durable_bytes_after","durable_bytes_created_delta","source_open_count","source_decode_count","bytes_read","bytes_written","temporary_spill_bytes_reported","cache_index_bytes_created","rewritten_bytes","semantic_oracle_status","identity_oracle_status"]
def validate_preassembly(root=HERE):
 m=load(root/M); r=load(root/R); s=load(root/S); o=load(root/O)
 if m.get("schema")!="RAWLSING_EE_R6B_FINAL_ABC_PREASSEMBLY_MANIFEST@1.0.0" or m.get("commission_tip")!="5ec735fe02fc0659613ec888ec32f5b2ee74accd": fail("manifest identity")
 if m.get("canonical_hq",{}).get("semantic_pre_main_tip")!="1dcd2a79dd6d4208738f655ab7fe4e71c219e354" or m.get("binding_authority_commits")!=PINS: fail("authority pins")
 for c,(commit,path,blob,acc) in OWNERS.items():
  x=m.get("candidates",{}).get(c,{})
  if [x.get("implementation_owner_commit"),x.get("path"),x.get("blob"),x.get("accelerators")]!=[commit,path,blob,acc]: fail("owner/config "+c)
 x=m.get("binding_artifacts",{}).get("EE-R5B",{})
 if [x.get("bridge_blob"),x.get("physical_cells_ready"),x.get("physical_cells_total"),x.get("proved_physical_gaps")]!=["d169be112f454732df161620743ea6332866255e",27,27,0]: fail("R5B")
 for f,(uid,sha,n) in SRC.items():
  x=m.get("universes",{}).get(f,{})
  if [x.get("universe_id"),x.get("sha256"),x.get("bytes")]!=[uid,sha,n]: fail("source "+f)
 f=m.get("selection_floor",{})
 if [f.get("total_cells"),f.get("ready_count"),f.get("pending_count"),f.get("ready_cells"),f.get("pending_cells"),f.get("final_cell_order")]!=[18,14,4,READY,PENDING,ORDER]: fail("floor")
 for k in ["abc_execution_performed","ranking_performed","surrogate_performance_numbers_generated","workload_redesigned","harness_redesigned","candidate_redesigned","storage_architecture_redesigned","main_modified","semantic_pre_main_modified"]:
  if m.get("boundaries",{}).get(k) is not False: fail("boundary "+k)
 if r.get("schema")!="RAWLSING_EE_R6B_READY_14_EXECUTION_ORACLE_PROFILES@1.0.0" or r.get("profile_count")!=14 or r.get("ready_cell_ids")!=READY: fail("ready index")
 ps=r.get("profiles",[])
 if len(ps)!=14 or [p.get("cell_id") for p in ps]!=READY or len(set(READY))!=14: fail("ready profiles")
 if r.get("shared_reference_oracle_materialization",{}).get("law")!=MAT: fail("materialization law")
 bs=r.get("shared_binding_sets",{})
 if [bs.get("WVS7_BASE",{}).get("source_identity",{}).get("sha256"),bs.get("LITS_BASE",{}).get("source_identity",{}).get("sha256")]!=[SRC["WVS7"][1],SRC["LiTS-I"][1]]: fail("shared source")
 for p in ps:
  cid=p["cell_id"]; fam,op=cid.split("::")
  if p.get("status")!="READY" or p.get("universe_id")!=SRC[fam][0] or p.get("operation_id")!="EEW1-"+op: fail("cell "+cid)
  if any(k in p for k in ["candidate_id","candidate_overrides","candidate_exclusions","candidate_specific_request","candidate_specific_oracle"]): fail("candidate-specific "+cid)
  if cid in LIFE:
   path,blob=LIFE[cid]; u=p.get("upstream_profile",{})
   if p.get("profile_mode")!="EXACT_IMMUTABLE_UPSTREAM_W4_PROFILE" or u!={"authority_commit":PINS["EE-R3E"],"path":path,"git_blob":blob}: fail("life "+cid)
   if p.get("step_order_mode")!="USE_UPSTREAM_STEPS_BYTE_FOR_BYTE__DO_NOT_INSERT_DELETE_REORDER_OR_REWRITE_STEPS": fail("life order "+cid)
  else:
   if [p.get("profile_mode"),p.get("phase"),p.get("action"),p.get("repetitions")]!=["REFERENCE_ORACLE_EXECUTION_PROFILE","cold","EXECUTE",1]: fail("query mode "+cid)
   if p.get("binding_set_id") not in bs or not p.get("reference_oracle",{}).get("laws"): fail("query authority "+cid)
 if s.get("schema")!="RAWLSING_EE_R6B_R6A_FOUR_CELL_SPLICE_CONTRACT@1.0.0" or s.get("slot_count")!=4 or s.get("frozen_pair",{}).get("qids")!=QIDS or s.get("frozen_pair",{}).get("newline_stream_sha256")!=PAIR: fail("splice header")
 ss=s.get("slots",[])
 if [x.get("slot_id") for x in ss]!=PENDING: fail("splice ids")
 for i,x in enumerate(ss,3):
  if [x.get("final_cell_order_ordinal_one_based"),x.get("universe_id"),x.get("source_sha256"),x.get("frozen_qids"),x.get("frozen_pair_newline_stream_sha256"),x.get("operation_id")]!=[i,SRC["WVS7"][0],SRC["WVS7"][1],QIDS,PAIR,f"EEW1-OP00{i}"]: fail("splice slot")
 if o.get("schema")!="RAWLSING_EE_R6B_EXECUTION_MEASUREMENT_ORDER_RESET_LAW@1.0.0" or o.get("candidate_execution_order")!=["A","B","C"] or o.get("final_selection_cell_order")!=ORDER: fail("order")
 if o.get("measurement",{}).get("aggregation_key")!=["candidate_id","universe_id","operation_id","phase"] or o.get("measurement",{}).get("telemetry_fields")!=MET: fail("measurement")
 return {"status":"PASS","ready_cells":14,"pending_splice_slots":4,"candidate_count":3,"physical_cells_ready":27,"abc_run":False,"ranking":False}
def validate_r6a_splice_payload(path,root=HERE):
 validate_preassembly(root); c=load(root/S); p=load(path); ss=p.get("slots",[])
 if p.get("schema")!=c.get("r6a_payload_schema") or len(ss)!=4 or [x.get("slot_id") for x in ss]!=PENDING: fail("R6A payload header")
 cs={x["slot_id"]:x for x in c["slots"]}
 req={"slot_id","universe_id","operation_id","source_sha256","frozen_qids","frozen_pair_newline_stream_sha256","source_coordinate_binding","routing_applicability_binding","risk_set_binding","denominator_binding","response_semantic_binding","reference_oracle","oracle_authority_refs","oracle_materialization","profile_content_sha256"}
 for x in ss:
  e=cs[x["slot_id"]]
  if set(x)!=req or [x["universe_id"],x["operation_id"],x["source_sha256"],x["frozen_qids"],x["frozen_pair_newline_stream_sha256"]] != [e["universe_id"],e["operation_id"],e["source_sha256"],QIDS,PAIR]: fail("R6A slot identity")
  if any(not isinstance(x[k],dict) or not x[k] for k in ["source_coordinate_binding","routing_applicability_binding","risk_set_binding","denominator_binding","response_semantic_binding"]): fail("R6A binding")
  if x["reference_oracle"].get("laws")!=e["required_oracle_laws"] or not x["reference_oracle"].get("kind") or not x["oracle_authority_refs"]: fail("R6A oracle")
  if x["oracle_materialization"].get("law")!=MAT or x["oracle_materialization"].get("candidate_outputs_may_not_define_or_modify_oracle") is not True: fail("R6A materialization")
  y=dict(x); claimed=y.pop("profile_content_sha256")
  if not isinstance(claimed,str) or len(claimed)!=64 or hobj(y)!=claimed: fail("R6A content hash")
 return {"status":"PASS","spliced_ready_cells":18,"pending_splice_slots":0,"abc_run":False,"ranking":False}
if __name__=="__main__":
 a=argparse.ArgumentParser(); a.add_argument("--root",default=str(HERE)); a.add_argument("--r6a-splice"); n=a.parse_args()
 try: out=validate_r6a_splice_payload(Path(n.r6a_splice),Path(n.root)) if n.r6a_splice else validate_preassembly(Path(n.root))
 except ValidationError as e: print("FAIL:",e); raise SystemExit(1)
 print(json.dumps(out,sort_keys=True))
