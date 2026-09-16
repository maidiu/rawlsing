#!/usr/bin/env python3
import csv,hashlib,json,pathlib
H=pathlib.Path(__file__).resolve().parent
J=lambda n:json.loads((H/n).read_text())
sl=lambda xs:hashlib.sha256("".join(x+"\n" for x in xs).encode()).hexdigest()
cs=lambda x:hashlib.sha256(json.dumps(x,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode()).hexdigest()
with (H/"01_36_QID_DISPOSITION_REGISTRY.csv").open(newline="") as f:R=list(csv.DictReader(f))
S,P,O=J("02_QID_BOUND_RESPONSE_SEMANTICS.json"),J("03_SELECTED_PROVING_PAIR.json"),J("04_OP003_OP006_WVS7_PREMISE_ORACLE_PACKAGE.json")
q=[r["qid"] for r in R];assert len(q)==36 and q==sorted(q) and len(set(q))==36 and sl(q)=="07977dcfb77ca88882985be5f90d27a39d3bc61f030e32e258c1cd5775e19a38"
assert all(r["disposition"]==S["court_disposition"] and r["eligible_for_pair"]=="True" for r in R)
C=S["object_columns"];A=[dict(zip(C,x)) for x in S["objects"]];B={x["qid"]:x for x in A};assert set(B)==set(q)
for x in A:
 assert x["qid"]=="question_impl.phase0."+hashlib.sha256(("WVS\x1fW7\x1f"+x["source_variable_code"]).encode()).hexdigest()[:20]
 assert S["response_profile_sha256"][x["response_profile"]]==cs(S["response_profiles"][x["response_profile"]])
 assert S["topology_profile_sha256"][x["topology_profile"]]==cs(S["topology_profiles"][x["topology_profile"]])
 pre={"qid":x["qid"],"source_variable_code":x["source_variable_code"],"b03_native_status":x["b03_native_status"],"response_profile":x["response_profile"],"response_profile_sha256":S["response_profile_sha256"][x["response_profile"]],"topology_profile":x["topology_profile"],"topology_profile_sha256":S["topology_profile_sha256"][x["topology_profile"]],"directional_certification_status":x["directional_certification_status"],"court_disposition":S["court_disposition"],"authority_docs":S["response_profile_document_refs"][x["response_profile"]]}
 assert x["semantic_object_sha256"]==cs(pre)
 if x["source_variable_code"] in ("Q294A","Q294B"): assert x["directional_certification_status"]=="NOT_CERTIFIED" and S["topology_profiles"][x["topology_profile"]]["split_sample"] is True
first=q[:2];assert first==["question_impl.phase0.03ea3430fb4f08a1f0da","question_impl.phase0.068ef710ac1c269b8adf"] and P["pair"]==first and P["pair_lf_stream_sha256"]==sl(first)
assert P["qid0"]["source_variable_code"]=="Q291G5" and P["qid1"]["source_variable_code"]=="Q291P5"
assert P["qid0"]["semantic_object_sha256"]==B[first[0]]["semantic_object_sha256"] and P["qid1"]["semantic_object_sha256"]==B[first[1]]["semantic_object_sha256"]
assert O["pair_ref"]["pair"]==first and O["respondent_and_joint_topology"]["coadministered"] is True and O["candidate_neutrality"]["candidate_performance_inspected"] is False
assert O["response_semantics"]["qid0_semantic_object_sha256"]==B[first[0]]["semantic_object_sha256"] and O["response_semantics"]["qid1_semantic_object_sha256"]==B[first[1]]["semantic_object_sha256"]
print("EE_R6A_REPLAY_PASS")
