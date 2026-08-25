from pathlib import Path
import json,csv,sys
R=Path(__file__).resolve().parents[1];e=[];c=[]
def ck(n,x,d=None):c.append({'check':n,'pass':bool(x),'detail':d});e.append(n) if not x else None
s=json.load(open(R/'CURRENT_STATUS_R9A.json'));ck('job3_false',s['job3_authorized'] is False);ck('r8_poison','DO_NOT_EXECUTE' in s['r8_worker_packs'])
a=json.load(open(R/'AUDIT/R9A_CANARY_COVERAGE_CORRECTION.json'));ck('117_total',a['r6_t03_t11_total_relations']==117);ck('98_pair',a['pair_census_addressable_relations']==98);ck('19_nonpair',a['nonpair_or_nonrelational_lane_relations']==19);ck('210_members',a['nonpair_member_implementation_count']==210,a['nonpair_member_implementation_count']);ck('210_found',a['nonpair_registry_rows_found']==210,a['nonpair_registry_rows_found']);ck('rules',a['nonpair_rule_counts']=={'COMPLEMENTARY_ROLE_CONVERGENCE':11,'TARGET_CONDITION_MATRIX':8},a['nonpair_rule_counts'])
rows=list(csv.DictReader(open(R/'AUDIT/R6_T03_T11_NONPAIR_CANARY_GAP_LEDGER_R9A.csv')));ck('19_rows',len(rows)==19,len(rows));ck('zero_sem',all(int(r['rows_with_sem_audit_unit'])==0 for r in rows));ck('all_registry',all(int(r['registry_rows_found'])==int(r['member_implementation_count']) for r in rows))
res={'status':'PASS' if not e else 'FAIL','check_count':len(c),'errors':e,'checks':c};json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9A.json','w'),indent=2);print(json.dumps({'status':res['status'],'checks':len(c),'errors':e}));sys.exit(0 if not e else 1)
