import pandas as pd, json, sys
from pathlib import Path
root=Path(sys.argv[1] if len(sys.argv)>1 else Path(__file__).resolve().parent)
errs=[]
def load(n):
 p=root/n
 if not p.exists(): errs.append('MISSING '+n); return pd.DataFrame()
 return pd.read_csv(p,dtype=str).fillna('')
r=load('S16_WAVE_RELATION_CLASS_CAPABILITY_ATLAS_T15_SUCCESSOR.csv')
q=load('S16_WAVE_REQUIREMENT_CAPABILITY_ATLAS_T15_SUCCESSOR.csv')
i=load('S16_WAVE_DERIVED_INDICATOR_CAPABILITY_ATLAS_T15_SUCCESSOR.csv')
t6=load('S16_STRICT_T06_POSITIVE_WITNESS_REPLAY.csv')
t15=load('S16_T15_POSITIVE_WITNESS_REPLAY.csv')
b6=load('S16_T06_BLOCKED_TERRAIN_REPLAY.csv')
b15=load('S16_T15_BLOCKED_TERRAIN_REPLAY.csv')
checks={}
def ck(name,val): checks[name]=bool(val); errs.append(name) if not val else None
ck('relation_rows_525',len(r)==525)
ck('requirement_rows_595',len(q)==595)
ck('indicator_rows_595',len(i)==595)
ck('waves_35',r[['source_family','wave']].drop_duplicates().shape[0]==35 if len(r) else False)
ck('relation_unique',r[['source_family','wave','rule_id']].drop_duplicates().shape[0]==525 if len(r) else False)
ck('every_wave_15',r.groupby(['source_family','wave']).size().eq(15).all() if len(r) else False)
ck('every_wave_17_req',q.groupby(['source_family','wave']).size().eq(17).all() if len(q) else False)
ck('t06_64',len(t6)==64)
ck('t15_188',len(t15)==188)
ck('t06_blocks_111',len(b6)==111)
ck('t15_blocks_139',len(b15)==139)
ck('t14_recall_only',(r[r.rule_id=='S14-T14'].candidate_generation_posture=='RECALL_ONLY').all() if len(r) else False)
ck('t15_35',len(r[r.rule_id=='S14-T15'])==35)
ck('je17_35',len(q[q.requirement_id=='JE-17_NORM_PRACTICAL_REALIZATION'])==35)
ck('no_absence_claim',(r.absence_claim_licensed=='NO').all() if len(r) else False)
ck('no_search_from_blocked',not r[r.capability_status.isin(['SEMANTIC_ONLY_NONCOMPOSABLE','ROUTING_BLOCKED','NOT_OBSERVED'])].candidate_generation_posture.eq('ALLOW_BOUNDED_O12_SEARCH').any() if len(r) else False)
# State ceilings
sp=root/'CURRENT_STATE_O11_T15_SUCCESSOR.json'
if sp.exists():
 s=json.loads(sp.read_text());
 ck('state_no_job3',s.get('job3_candidates_created')==0 and s.get('job3_relation_acceptance_created') is False)
 ck('state_no_indicator_values',s.get('indicator_values_created')==0)
else: errs.append('MISSING state'); checks['state_present']=False
out={'status':'PASS' if not errs else 'FAIL','errors':errs,'checks':checks,'counts':{'relation_status':r.capability_status.value_counts().to_dict() if len(r) else {},'requirement_status':q.capability_status.value_counts().to_dict() if len(q) else {}}}
print(json.dumps(out,indent=2,sort_keys=True))
sys.exit(0 if not errs else 1)
