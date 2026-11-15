#!/usr/bin/env python3
import os, sys, json, hashlib, pandas as pd

ROOT=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
PARENT=os.environ.get("RAWLSING_T06_PARENT_DIR","/mnt/data/rawlsing_exec/parents")
OLD=os.environ.get("RAWLSING_T06_R1_CSV","/mnt/data/rawlsing_exec/T06_NORM_STATED_CONDUCT_RECALL_PAIRS.csv")
checks=[]; errors=[]

def check(name, cond, detail=""):
    checks.append({"name":name,"pass":bool(cond),"detail":str(detail)})
    if not cond: errors.append(f"{name}: {detail}")

reg=pd.read_csv(os.path.join(PARENT,'CANONICAL_IMPLEMENTATION_REGISTRY.csv'),low_memory=False)
r6=pd.read_csv(os.path.join(PARENT,'INTER_QUESTION_RELATION_AUTHORITY_R2.csv'),low_memory=False)
st=pd.read_csv(os.path.join(ROOT,'NARROWING','T06_STATED_INTENDED_RECONSTRUCTION_R2.csv'))
rl=pd.read_csv(os.path.join(ROOT,'NARROWING','T06_REALIZED_BEHAVIOR_PAIR_DISPOSITION_R2.csv'))
na=pd.read_csv(os.path.join(ROOT,'NARROWING','T06_NORM_SHORE_ACCOUNTING_R2.csv'))
ea=pd.read_csv(os.path.join(ROOT,'NARROWING','T06_ENDPOINT_SHORE_ACCOUNTING_R2.csv'))
pk=pd.read_csv(os.path.join(ROOT,'NARROWING','T06_CANONICAL_REVIEW_PACKETS_R2.csv'))
old=pd.read_csv(OLD)

check("canonical_registry_18276",len(reg)==18276,len(reg))
accepted=reg['o04__central_s2b_disposition'].fillna('').eq('ACCEPT_ENDPOINT').sum()
check("o04_accepted_endpoints_2113",accepted==2113,accepted)

u=reg[reg['sem__audit_unit_id'].notna() & reg['sem__audit_unit_id'].astype(str).ne('')].drop_duplicates('sem__audit_unit_id')
norm594=u['sem__canonical_role'].fillna('').eq('NORMATIVE_OR_POLICY_STANCE').sum()
check("r10g_unique_normative_units_594",norm594==594,norm594)

t06=r6[r6['relation_type'].eq('NORM_EXPECTED_CONDUCT')]
check("sealed_r6_t06_count_2",len(t06)==2,len(t06))
check("sealed_r6_t06_all_cross_object",(t06['edge_construction_class']=='CROSS_OBJECT_GOVERNED_ALIGNMENT').all(),
      t06['edge_construction_class'].value_counts().to_dict())

check("r1_saved_csv_rows_313",len(old)==313,len(old))
known_true=old['known'].fillna(False).astype(bool).sum()
check("r1_saved_csv_known_true_zero",known_true==0,known_true)
canary_ids={'p2xsafe__b78b1f88ee7fe5a2','p2xsafe__4363881d3493db4a','p2xsafe__7995f1c9863f16e7','p2xsafe__c1c46e11bba5613d'}
old_ids=set(old['norm'].astype(str))|set(old['conduct'].astype(str))
check("r1_saved_csv_contains_no_sealed_canary_member",not bool(canary_ids & old_ids),sorted(canary_ids & old_ids))

check("r2_stated_rows_11",len(st)==11,len(st))
check("r2_stated_canaries_2",(st['disposition']=='KNOWN_R6_ACCEPTED_T06_CANARY').sum()==2,
      (st['disposition']=='KNOWN_R6_ACCEPTED_T06_CANARY').sum())
sealed_ids=set(t06['relation_authority_id'])
recovered=set(st.loc[st['disposition']=='KNOWN_R6_ACCEPTED_T06_CANARY','existing_relation_authority_id'].dropna().astype(str))
check("r2_stated_recovers_exact_sealed_t06_ids",recovered==sealed_ids,{"recovered":sorted(recovered),"sealed":sorted(sealed_ids)})

check("r2_realized_rows_39",len(rl)==39,len(rl))
check("r2_realized_no_empty_dispositions",rl['disposition'].fillna('').str.len().gt(0).all())
check("r2_realized_reviews_6",rl['disposition'].str.startswith('EMIT_BRIDGE_REVIEW_CANDIDATE').sum()==6,
      rl['disposition'].str.startswith('EMIT_BRIDGE_REVIEW_CANDIDATE').sum())
check("r2_realized_t07_blocks_16",(rl['disposition']=='BLOCK_PENDING_T07_TARGET_HIERARCHY_AUTHORITY').sum()==16,
      (rl['disposition']=='BLOCK_PENDING_T07_TARGET_HIERARCHY_AUTHORITY').sum())
check("r2_realized_no_authority_accept_verdicts",not rl['disposition'].str.match(r'^(ACCEPT|AUTHORITY_)').any())

check("norm_shore_accounting_nonempty",len(na)>0,len(na))
check("norm_shore_no_empty_dispositions",na['accounting_disposition'].fillna('').str.len().gt(0).all())
check("endpoint_shore_2113",len(ea)==2113,len(ea))
check("endpoint_shore_no_empty_dispositions",ea['accounting_disposition'].fillna('').str.len().gt(0).all())
check("packet_count_7",len(pk)==7,len(pk))
check("packet_has_lits_t05_cross_rule",((pk['packet_id']=='T06R2-P02-LITSIII-CORRUPTION-REPORT') & pk['rule_hypotheses'].str.contains('T05')).any())
check("packet_has_evs_t07_dependency",((pk['packet_id']=='T06R2-P06-EVS1990-VOLUNTARY-DUTY') & pk['rule_hypotheses'].str.contains('T07')).any())

status=json.load(open(os.path.join(ROOT,'CURRENT_STATUS_R2.json')))
check("job3_not_authorized",status.get('job3_authorized') is False)
check("811_not_complete",status.get('o12_r2_811_complete_authority') is False)
check("next_is_t07",status.get('t06',{}).get('next_dependency')=='T07 target hierarchy')

result={"validator":"validate_t06_checkpoint_r2.py","checks":len(checks),"errors":len(errors),"status":"PASS" if not errors else "FAIL",
        "details":checks,"error_messages":errors}
out=os.path.join(ROOT,'VALIDATION','VALIDATION_RESULT_R2.json')
json.dump(result,open(out,'w'),indent=2)
print(json.dumps({"status":result["status"],"checks":len(checks),"errors":len(errors)},indent=2))
if errors:
    for e in errors: print("ERROR",e)
    sys.exit(1)
