#!/usr/bin/env python3
import os, json, pandas as pd, sys
ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
errors=[]; checks=[]
def ck(name,cond,detail=""):
    checks.append({"name":name,"pass":bool(cond),"detail":str(detail)})
    if not cond: errors.append(f"{name}: {detail}")

r6=pd.read_csv(os.path.join(ROOT,'PROVENANCE','SEALED_R6_T07_CANARY_RECOVERY_R3.csv'))
p2=pd.read_csv(os.path.join(ROOT,'NARROWING','T07_P2_TARGET_RELATION_DISPOSITION_R3.csv'))
proxy=pd.read_csv(os.path.join(ROOT,'AUDIT','O11_T07_65_PROXY_GROUP_DISPOSITION_R3.csv'))
src=pd.read_csv(os.path.join(ROOT,'NARROWING','T07_R14_SOURCE_NATIVE_MULTI_TARGET_SCAN_R3.csv'))
pk=pd.read_csv(os.path.join(ROOT,'NARROWING','T07_CANONICAL_REVIEW_PACKETS_R3.csv'))
dep=pd.read_csv(os.path.join(ROOT,'NARROWING','T07_T06_DEPENDENCY_LEDGER_R3.csv'))
status=json.load(open(os.path.join(ROOT,'CURRENT_STATUS_R3.json')))

ck("r6_t07_canaries_6",len(r6)==6,len(r6))
ck("r6_all_recovered",(r6.t07_recovery_status=='RECOVERED_SEALED_R6_T07_CANARY').all())
ck("p2_target_rows_79",len(p2)==79,len(p2))
ck("p2_explicit_nested_3",(p2.original_relation_type=='NESTED_TARGET_RELATION_NOT_EQUIVALENT').sum()==3,
   (p2.original_relation_type=='NESTED_TARGET_RELATION_NOT_EQUIVALENT').sum())
ck("p2_coordinate_76",(p2.original_relation_type=='TARGET_RELATION_COORDINATE_ONLY').sum()==76,
   (p2.original_relation_type=='TARGET_RELATION_COORDINATE_ONLY').sum())
ck("p2_no_empty_dispositions",p2.t07_disposition.fillna('').str.len().gt(0).all())
ck("p2_no_unclassified",not p2.t07_disposition.str.startswith('BLOCK_UNCLASSIFIED').any())
ck("proxy_groups_65",len(proxy)==65,len(proxy))
ck("proxy_all_dispositioned",proxy.t07_disposition.fillna('').str.len().gt(0).all())
ck("proxy_review_8",(proxy.t07_narrowing_status=='REVIEW_EMITTED').sum()==8,
   (proxy.t07_narrowing_status=='REVIEW_EMITTED').sum())
ck("proxy_canary_1",(proxy.t07_narrowing_status=='EXISTING_GOVERNED_CANARY').sum()==1,
   (proxy.t07_narrowing_status=='EXISTING_GOVERNED_CANARY').sum())
ck("proxy_exclusion_56",(proxy.t07_narrowing_status=='TERMINAL_PROXY_EXCLUSION').sum()==56,
   (proxy.t07_narrowing_status=='TERMINAL_PROXY_EXCLUSION').sum())
ck("r14_exact_multi_target_objects_180",len(src)==180,len(src))
ck("r14_scan_all_dispositioned",src.t07_disposition.fillna('').str.len().gt(0).all())
ck("packet_count_15",len(pk)==15,len(pk))
ck("unresolved_packet_count_11",pk.status.str.startswith('UNRESOLVED').sum()==11,
   pk.status.str.startswith('UNRESOLVED').sum())
ck("no_novel_accept_verdicts",not pk[pk.status.str.startswith('UNRESOLVED')].status.str.contains('ACCEPT|AUTHORITY',case=False,regex=True).any())
ck("t06_dependency_one",len(dep)==1,len(dep))
ck("t06_dependency_remains_blocked",dep.r3_status.str.contains('REMAINS_BLOCKED').all())
ck("mandatory_evs_packet_present",(pk.packet_id=='T07R3-P05-EVS1990-VOLUNTARY-WORK').any())
ck("p2_police_packet_present",(pk.packet_id=='T07R3-P01-P2-POLICE-STATION').any())
ck("p2_parties_packet_present",(pk.packet_id=='T07R3-P02-P2-OPPOSITION-PARTIES').any())
ck("job3_not_authorized",status.get('job3_authorized') is False)
ck("811_not_complete",status.get('o12_r2_811_complete_authority') is False)
ck("workers_zero",status.get('workers_launched') is False)
ck("next_is_t08",status.get('t07',{}).get('next_dependency')=='T08 institution class')
ck("repair_9_partial",9 in status.get('repair_stack',{}).get('partial',[]))

result={"validator":"validate_t07_checkpoint_r3.py","status":"PASS" if not errors else "FAIL",
        "checks":len(checks),"errors":len(errors),"details":checks,"error_messages":errors}
os.makedirs(os.path.join(ROOT,'VALIDATION'),exist_ok=True)
json.dump(result,open(os.path.join(ROOT,'VALIDATION','VALIDATION_RESULT_R3.json'),'w'),indent=2)
print(json.dumps({"status":result["status"],"checks":len(checks),"errors":len(errors)},indent=2))
if errors:
    for e in errors: print("ERROR",e)
    sys.exit(1)
