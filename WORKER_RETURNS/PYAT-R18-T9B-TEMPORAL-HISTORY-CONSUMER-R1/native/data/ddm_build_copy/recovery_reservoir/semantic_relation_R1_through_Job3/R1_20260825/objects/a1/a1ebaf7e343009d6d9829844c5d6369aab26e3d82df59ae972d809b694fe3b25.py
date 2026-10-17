import pandas as pd, json, pathlib, hashlib, sys
root=pathlib.Path(__file__).resolve().parents[1]
ret=root/'RETURN'
required=['T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv','T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv','T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv','T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv','T06_SOURCE_COVERAGE_DEFECTS.csv','T06_SOURCE_FIRST_BLOCKERS.csv','T06_WAVE_COMPLETENESS_ATTESTATION.csv','WORKER_REPORT.md','VALIDATION.json']
errs=[]
for f in required:
    if not (ret/f).exists(): errs.append(f'missing {f}')
a=pd.read_csv(ret/'T06_SOURCE_FIRST_POSITIVE_RELATION_AUTHORITY.csv')
i=pd.read_csv(ret/'T06_SOURCE_FIRST_IMPLEMENTATION_ACCOUNTING.csv',low_memory=False)
x=pd.read_csv(ret/'T06_SOURCE_FIRST_CROSSWALK_REVIEW.csv')
r=pd.read_csv(ret/'T06_SOURCE_FIRST_UPSTREAM_REPAIRS.csv')
c=pd.read_csv(ret/'T06_SOURCE_COVERAGE_DEFECTS.csv')
b=pd.read_csv(ret/'T06_SOURCE_FIRST_BLOCKERS.csv')
w=pd.read_csv(ret/'T06_WAVE_COMPLETENESS_ATTESTATION.csv')
v=json.load(open(ret/'VALIDATION.json'))
exp={('LiTS','2006'):1198,('GSS','1984'):675,('EVS','2017'):474,('Arab Barometer','V'):359,('GSS','1972'):216,('South Asia','W2'):73}
i['wave']=i['wave'].astype(str); w['wave']=w['wave'].astype(str); a['wave']=a['wave'].astype(str)
if len(i)!=2995: errs.append(f'accounting rows {len(i)} !=2995')
if i.question_implementation_id.nunique()!=2995: errs.append('implementation IDs not unique')
for k,n in exp.items():
    z=len(i[(i.source_family==k[0])&(i.wave==k[1])])
    if z!=n: errs.append(f'{k} {z}!={n}')
if len(w)!=6: errs.append(f'attestation rows {len(w)} !=6')
if len(a)!=7: errs.append(f'positive relations {len(a)} !=7')
base=['index','central_relation_id','authority_class','rule_id','relation_type','source_family','wave','active_source_wave_set_json','member_semantic_unit_ids_json','member_implementation_ids_json','role_assignments_json','common_proposition_or_target','actor_scope','target_scope','action_domain','position_or_routing_condition','central_basis','confidence','worker_origin','worker_relation_id','grain_note','r16f_freeze_status','r16f_freeze_basis']
if list(a.columns[:len(base)])!=base: errs.append('R16F successor base column contract/order mismatch')
allids=set(i.question_implementation_id)
allowed={'RR_NORM','RR_STATED_OR_INTENDED_CONDUCT','RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT'}
for _,row in a.iterrows():
    mids=set(json.loads(row.member_implementation_ids_json))
    if not mids<=allids: errs.append(f'unbound positive {row.worker_relation_id}')
    for ra in json.loads(row.role_assignments_json):
        if ra['relation_role'] not in allowed: errs.append(f'bad role {ra["relation_role"]}')
if not x.disposition.isin(['POSITIVE_T06','BLOCKED_SOURCE_AMBIGUITY','NOT_T06_SOURCE_PROVEN_MISMATCH']).all(): errs.append('invalid disposition')
if not (i.loc[i.source_first_classification=='NORM_SHORE','norm_to_conduct_search_status']=='COMPLETE').all(): errs.append('norm search incomplete')
if not (i.loc[i.source_first_classification=='CONDUCT_SHORE','conduct_to_norm_search_status']=='COMPLETE').all(): errs.append('conduct search incomplete')
zero=w[w.positive_T06_count==0]
if not zero.hostile_QA_result.eq('PASS').all(): errs.append('zero-wave hostile QA fail')
if not zero.zero_T06_wave_supportable.eq('YES').all(): errs.append('zero-wave supportability fail')
if len(c)!=0: errs.append('unexpected coverage defects')
if v.get('status')!='PASS': errs.append('embedded VALIDATION not PASS')
if not a.r16f_freeze_status.eq('NOT_FROZEN_WORKER_RETURN').all(): errs.append('freeze claim detected')
print(json.dumps({'status':'PASS' if not errs else 'FAIL','errors':errs,'counts':{'positive_relations':len(a),'accounting_rows':len(i),'crosswalk_rows':len(x),'repairs':len(r),'coverage_defects':len(c),'blockers':len(b)}},indent=2))
sys.exit(0 if not errs else 1)
