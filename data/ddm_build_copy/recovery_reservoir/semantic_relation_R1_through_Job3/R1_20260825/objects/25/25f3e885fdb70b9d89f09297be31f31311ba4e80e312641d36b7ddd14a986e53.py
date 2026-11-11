from pathlib import Path
import json,csv,gzip,hashlib,sys
R=Path(__file__).resolve().parents[1]
errs=[];checks=[]
def ck(n,c,d=None):
 checks.append({'check':n,'pass':bool(c),'detail':d});
 if not c:errs.append(n)
s=json.load(open(R/'CURRENT_STATUS_R9.json'))
ck('job3_false',s['job3_authorized'] is False)
ck('r8_dispatch_revoked',s['r8_denominator_66_dispatch_authority'] is False)
ck('packs_poisoned','DO_NOT_EXECUTE' in s['r8_worker_packs_execution_status'])
p=json.load(open(R/'PAIR_CENSUS/PAIR_CENSUS_SUMMARY_R9.json'))
ck('units_3324',p['semantic_unit_count_global']==3324,p['semantic_unit_count_global'])
ck('memberships_4565',p['source_wave_semantic_membership_rows']==4565,p['source_wave_semantic_membership_rows'])
ck('groups_35',p['source_wave_group_count']==35,p['source_wave_group_count'])
ck('pairs_364094',p['all_same_source_wave_unordered_pairs']==364094,p['all_same_source_wave_unordered_pairs'])
# stream count + uniqueness
seen=set();n=0;dupe=0
with gzip.open(R/'PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz','rt',encoding='utf-8',newline='') as f:
 for row in csv.DictReader(f):
  n+=1; pid=row['pair_id']; dupe += pid in seen; seen.add(pid)
ck('pair_file_rows',n==364094,n);ck('pair_id_unique',dupe==0,dupe)
st=json.load(open(R/'REPAIR_STACK_R9.json'))
ck('stack_done_exact',st['done']==[1,7,8],st['done'])
ck('item14_open',14 in st['open'])
ck('item17_open',17 in st['open'])
ck('items9_13_partial',all(x in st['partial'] for x in range(9,14)))
# canary coverage file count = R6 T03-T11 relations 117
with open(R/'PROVENANCE/R6_T03_T11_PAIR_CENSUS_CANARY_COVERAGE_R9.csv',newline='',encoding='utf-8') as f: cr=list(csv.DictReader(f))
ck('r6_t03_t11_relations_117',len(cr)==117,len(cr))
ck('canary_mapping_status_nonblank',all(r['coverage_status'] for r in cr))
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R9.json','w'),indent=2)
print(json.dumps({'status':res['status'],'checks':len(checks),'errors':errs}))
sys.exit(0 if not errs else 1)
