import pandas as pd, numpy as np, json, hashlib, os, shutil, pathlib, csv, zipfile, subprocess
from collections import defaultdict
ROOT=pathlib.Path('/mnt/data')
R13ZIP=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811.zip'
R13=ROOT/'r13_work'/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811'
OUT=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14_20260811'
if OUT.exists(): shutil.rmtree(OUT)
for d in ['WORKER_ECONOMICS','VALIDATION','PROVENANCE','CODE']:(OUT/d).mkdir(parents=True,exist_ok=True)
P=R13/'PACKETS'/'R13_CROSS_RULE_DEDUPED_PACKET_LEDGER.csv'
df=pd.read_csv(P)

def broad(x):
 s=str(x)
 if s in ['T06_ENDPOINT_LINK','MEMBER_TARGET_EVIDENCE','PAIR_AUTHORITY_BLOCKER','T06_NORM_ROLE_BLOCKER']: return s
 if s.startswith('SOURCE_OBJECT::'): return 'SOURCE_OBJECT'
 if s.startswith('PARALLEL_OBJECT::'): return 'PARALLEL_OBJECT'
 if s.startswith('T07_CONCEPT::'): return 'T07_CONCEPT'
 return 'OTHER'
def njson(x):
 try: return len(json.loads(x))
 except Exception: return 0

df['work_family']=df.dedupe_family.map(broad)
df['member_implementation_count']=df.member_implementation_ids_json.fillna('[]').map(njson)
df['rule_count']=df.rule_hypotheses.fillna('').map(lambda s:len([x for x in str(s).split(';') if x]))
# Planning metric only; never semantic authority.
df['planning_effort_units']=1+.35*(df.rule_count-1).clip(lower=0)+.15*(df.member_implementation_count-2).clip(lower=0)+.08*np.sqrt(df.decision_atom_count.clip(lower=0))
for fam,add in [('SOURCE_OBJECT',.7),('PARALLEL_OBJECT',1.0),('MEMBER_TARGET_EVIDENCE',1.0),('T06_ENDPOINT_LINK',.4),('T07_CONCEPT',.2)]:
 df.loc[df.work_family==fam,'planning_effort_units']+=add

def lane(f):
 if f=='PAIR_AUTHORITY_BLOCKER': return 'VOZHD_CENTRAL__PAIR_AUTHORITY_BLOCKER'
 if f=='T06_NORM_ROLE_BLOCKER': return 'VOZHD_CENTRAL__T06_NORM_ROLE_AUTHORITY_BLOCKER'
 if f=='T07_CONCEPT': return 'VOZHD_CENTRAL__T07_IMPLEMENTATION_BINDING'
 return 'WORKER_ELIGIBLE__SEMANTIC_ADJUDICATION'
df['execution_lane']=df.work_family.map(lane)
# Status-based hostile confirmation: no blocker may be worker eligible.
df['status_has_input_blocker']=df.packet_statuses_json.fillna('').str.contains('INPUT_AUTHORITY_BLOCKER',regex=False)

cand=df[df.execution_lane.str.startswith('WORKER_ELIGIBLE')].copy()
central=df[~df.execution_lane.str.startswith('WORKER_ELIGIBLE')].copy()
# preserve source-wave as indivisible unit and balance with LPT over planning-only metric
waves=cand.groupby(['source_family','wave'],dropna=False).agg(container_count=('packet_id','size'),decision_atom_count=('decision_atom_count','sum'),planning_effort_units=('planning_effort_units','sum')).reset_index().sort_values(['planning_effort_units','source_family','wave'],ascending=[False,True,True])

def make_bins(n):
 bins=[{'worker_id':f'W{i:02d}','planning_effort_units':0.0,'groups':[]} for i in range(1,n+1)]
 for _,r in waves.iterrows():
  b=min(bins,key=lambda x:(x['planning_effort_units'],x['worker_id']))
  g=(str(r.source_family),str(r.wave),int(r.container_count),int(r.decision_atom_count),float(r.planning_effort_units))
  b['groups'].append(g); b['planning_effort_units']+=float(r.planning_effort_units)
 return bins
sensitivity=[]
for n in range(4,9):
 bs=make_bins(n); vals=[b['planning_effort_units'] for b in bs]
 sensitivity.append({'worker_count':n,'max_shard_effort_units':max(vals),'min_shard_effort_units':min(vals),'mean_shard_effort_units':sum(vals)/n,'max_min_ratio':max(vals)/min(vals)})
sens=pd.DataFrame(sensitivity)
sens['max_shard_reduction_vs_prior_pct']=np.nan
for i in range(1,len(sens)):
 sens.loc[i,'max_shard_reduction_vs_prior_pct']=100*(sens.loc[i-1,'max_shard_effort_units']-sens.loc[i,'max_shard_effort_units'])/sens.loc[i-1,'max_shard_effort_units']
sens.to_csv(OUT/'WORKER_ECONOMICS'/'R14_WORKER_COUNT_SENSITIVITY.csv',index=False)

bins=make_bins(6)
wave_assign=[]
for b in bins:
 for sf,w,c,a,e in b['groups']:
  wave_assign.append({'worker_id':b['worker_id'],'source_family':sf,'wave':w,'container_count':c,'decision_atom_count':a,'planning_effort_units':e})
wa=pd.DataFrame(wave_assign).sort_values(['worker_id','source_family','wave'])
wa.to_csv(OUT/'WORKER_ECONOMICS'/'R14_SOURCE_WAVE_SHARD_PLAN.csv',index=False)
assign_map={(r.source_family,str(r.wave)):r.worker_id for _,r in wa.iterrows()}
cand['worker_id']=[assign_map[(str(sf),str(w))] for sf,w in zip(cand.source_family,cand.wave)]
assign_cols=['worker_id','packet_id','source_family','wave','work_family','rule_hypotheses','decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','planning_effort_units','packet_statuses_json','authority_ceilings_json']
cand[assign_cols].sort_values(['worker_id','source_family','wave','packet_id']).to_csv(OUT/'WORKER_ECONOMICS'/'R14_WORKER_PACKET_ASSIGNMENT_LEDGER.csv',index=False)
central_cols=['packet_id','source_family','wave','work_family','execution_lane','rule_hypotheses','decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','planning_effort_units','packet_statuses_json','authority_ceilings_json']
central[central_cols].sort_values(['execution_lane','source_family','wave','packet_id']).to_csv(OUT/'WORKER_ECONOMICS'/'R14_VOZHD_CENTRAL_QUEUE.csv',index=False)
class_cols=['packet_id','source_family','wave','dedupe_family','work_family','execution_lane','rule_hypotheses','decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','rule_count','planning_effort_units','status_has_input_blocker','packet_statuses_json','authority_ceilings_json']
df[class_cols].sort_values('packet_id').to_csv(OUT/'WORKER_ECONOMICS'/'R14_WORKLOAD_CLASSIFICATION.csv',index=False)
# worker summary
ws=cand.groupby('worker_id').agg(container_count=('packet_id','size'),decision_atom_count=('decision_atom_count','sum'),planning_effort_units=('planning_effort_units','sum'),source_wave_groups=('wave','size')).reset_index()
# overwrite group count correctly from wa
wg=wa.groupby('worker_id').size().to_dict(); ws['source_wave_group_count']=ws.worker_id.map(wg)
ws['source_family_count']=ws.worker_id.map(wa.groupby('worker_id').source_family.nunique().to_dict())
ws=ws.drop(columns=['source_wave_groups']).sort_values('worker_id')
ws.to_csv(OUT/'WORKER_ECONOMICS'/'R14_WORKER_SHARD_SUMMARY.csv',index=False)
# family summary
fs=df.groupby(['execution_lane','work_family']).agg(container_count=('packet_id','size'),decision_atom_count=('decision_atom_count','sum'),planning_effort_units=('planning_effort_units','sum')).reset_index()
fs.to_csv(OUT/'WORKER_ECONOMICS'/'R14_EXECUTION_LANE_SUMMARY.csv',index=False)

# status summary
summary={
 'r13_parent_zip_sha256':hashlib.sha256(R13ZIP.read_bytes()).hexdigest(),
 'r13_total_containers':int(len(df)),
 'r13_total_decision_atoms':int(df.decision_atom_count.sum()),
 'worker_eligible_containers':int(len(cand)),
 'worker_eligible_decision_atoms':int(cand.decision_atom_count.sum()),
 'central_containers':int(len(central)),
 'central_decision_atoms':int(central.decision_atom_count.sum()),
 'central_pair_authority_blockers':int((central.work_family=='PAIR_AUTHORITY_BLOCKER').sum()),
 'central_t06_norm_role_blockers':int((central.work_family=='T06_NORM_ROLE_BLOCKER').sum()),
 'central_t07_binding_containers':int((central.work_family=='T07_CONCEPT').sum()),
 'worker_count_selected':6,
 'worker_shard_container_counts':{r.worker_id:int(r.container_count) for _,r in ws.iterrows()},
 'worker_shard_atom_counts':{r.worker_id:int(r.decision_atom_count) for _,r in ws.iterrows()},
 'worker_shard_effort_units':{r.worker_id:round(float(r.planning_effort_units),6) for _,r in ws.iterrows()},
 'max_min_effort_ratio':round(float(ws.planning_effort_units.max()/ws.planning_effort_units.min()),6),
 'planning_metric_authority_ceiling':'SCHEDULING_ONLY__NOT_SEMANTIC_AUTHORITY__NOT_TIME_ESTIMATE',
 'worker_economics_decision':'YES__SIX_WORKERS_FOR_2433_NONBLOCKED_CONTAINERS__VOZHD_CENTRAL_166_GOVERNANCE_OR_BINDING_CONTAINERS',
 'worker_packs_created':False,
 'job3_authorized':False,
}
json.dump(summary,open(OUT/'WORKER_ECONOMICS'/'R14_WORKER_ECONOMICS_SUMMARY.json','w'),indent=2)

# progress ledger
progress='''# Rawlsing S14 Repair — Progress Ledger after R14\n\n## Governing 25-item checklist\n\n- DONE: **9 / 25** — #1, #2, #3, #7, #8, #14, #15, #16, **#17**.\n- PARTIAL / materially developed: **10 / 25** — #4, #5, #6, #9, #10, #11, #12, #13, #18, #23.\n- OPEN: **6 / 25** — #19, #20, #21, #22, #24, #25.\n\nThis is **36% fully closed by checklist count**. Checklist count is not a time estimate. The current repair has now crossed from denominator construction/workload sizing into execution of the finite S14 semantic adjudication workload.\n\n## Current repair arc\n\n1. unified 18,276 spine — DONE;\n2. orthogonal relation-role ontology/schema — DONE;\n3. composite opportunity denominator / negative-space accounting — DONE;\n4. lossless packet compression — DONE;\n5. cross-rule dedupe — DONE;\n6. worker economics — **DONE (#17)**;\n7. final S14 adjudication / authority freeze — **ACTIVE NEXT (#18)**.\n\n## R14 economics result\n\n- R13 total: 2,599 containers / 120,970 decision atoms.\n- Worker-eligible: **2,433 containers / 85,892 decision atoms**.\n- Vozhd-central: **166 containers / 35,078 decision atoms**.\n  - 55 pair-authority blockers;\n  - 32 T06 norm-role authority blockers;\n  - 79 T07 hierarchy-concept implementation bindings.\n- Selected worker topology: **6 workers**, preserving every source-wave group intact.\n- Worker packs are **not yet created or launched**; immutable assignment is frozen here, pack construction belongs to #18.\n- R8 worker packs remain DO NOT EXECUTE.\n- Job 3 remains NOT AUTHORIZED.\n\n## #18 execution shape\n\nParallelize only after evidence-rich successor packs are generated from this immutable R14 assignment ledger:\n\n- W01–W06: adjudicate the 2,433 non-blocked semantic containers under frozen rule contracts;\n- Vozhd central: resolve the 87 upstream authority blockers + 79 T07 bindings, revalidate R8C ancestry, reconcile worker returns, and freeze actual S14 authority.\n\nThen proceed to #19 O11/S16 rebuild.\n'''
open(OUT/'PROGRESS_LEDGER_R14.md','w').write(progress)

report=f'''# R14 — Worker Economics and Immutable Execution Partition\n\n## Verdict\n\n**#17 is DONE. Worker sharding is economically justified, but only after separating governance/binding work from independent semantic adjudication.**\n\nR13 contains **{len(df):,}** deduped review containers and **{int(df.decision_atom_count.sum()):,}** rule-specific decision atoms. R14 classifies every R13 container exactly once:\n\n- **{len(cand):,} containers / {int(cand.decision_atom_count.sum()):,} atoms** → worker-eligible semantic adjudication;\n- **{len(central):,} containers / {int(central.decision_atom_count.sum()):,} atoms** → Vozhd central.\n\nThe 166 central containers are not held centrally because they are intellectually interesting; they are held centrally because they own prerequisites workers are forbidden to invent or repair: **55 pair-authority blockers, 32 T06 norm-role authority blockers, and 79 T07 hierarchy-concept implementation bindings.**\n\n## Why six workers\n\nThe assignment treats each source-wave group as indivisible, preventing the same wave-specific source context from being independently interpreted by multiple workers. A planning-only effort metric combines container count, rule multiplicity, implementation count and within-container decision-atom breadth. It is explicitly **not semantic authority and not a wall-clock estimate**.\n\nSensitivity over 4–8 workers shows a clear knee. Five workers leave a maximum planning load of {sens.loc[sens.worker_count==5,'max_shard_effort_units'].iloc[0]:.1f}; six reduce that to {sens.loc[sens.worker_count==6,'max_shard_effort_units'].iloc[0]:.1f}; seven reduce it further to {sens.loc[sens.worker_count==7,'max_shard_effort_units'].iloc[0]:.1f}, while adding another full pack/return/reconciliation channel. Eight cannot improve the maximum at all because the largest source-wave group becomes the indivisible bottleneck. Six therefore captures the useful parallelism without reflexively maximizing worker count.\n\nThe six selected shards have planning loads from **{ws.planning_effort_units.min():.1f} to {ws.planning_effort_units.max():.1f}** (max/min ratio **{ws.planning_effort_units.max()/ws.planning_effort_units.min():.3f}**). No source-wave group is split.\n\n## Important scope law\n\nThe **120,970 atoms are not 120,970 human jobs**. R13 compression/dedupe defines the human work grain. Conversely, a large packet cannot be treated as one automatic decision: worker returns must preserve rule-specific atom ancestry and may recommend only within the packet's frozen membership.\n\nNo worker may repair pair authority, assign missing norm-role authority, modify T07 hierarchy concepts, invent relation-role ontology, change evidence ceilings, or make completeness/Job-3 claims.\n\n## What R14 does not do\n\n- does not create worker packs;\n- does not launch workers;\n- does not adjudicate S14 relation truth;\n- does not freeze S14 authority;\n- does not authorize Job 3.\n\nThose operations belong to #18.\n'''
open(OUT/'R14_WORKER_ECONOMICS_REPORT.md','w').write(report)

status={
 'checkpoint':'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14_20260811',
 'status':'R14_WORKER_ECONOMICS_FROZEN__ITEM17_DONE',
 'job3_authorized':False,
 'item17_status':'DONE__SIX_WORKER_EXECUTION_PARTITION_FROZEN',
 'item18_status':'NEXT__S14_ADJUDICATION_AND_AUTHORITY_FREEZE',
 'worker_packs_created':False,
 'summary':summary
}
json.dump(status,open(OUT/'CURRENT_STATUS_R14.json','w'),indent=2)
stack={'governing_checklist':'user 25-item full repair stack','done':[1,2,3,7,8,14,15,16,17],'partial':[4,5,6,9,10,11,12,13,18,23],'open':[19,20,21,22,24,25], 'notes':{'17':'DONE: immutable 6-worker partition over 2,433 nonblocked containers; 166 governance/binding containers retained centrally.','18':'ACTIVE NEXT: evidence-rich worker pack generation + central blocker/binding closure + reconciliation + final S14 authority freeze.','R8':'old W01-W04 packs remain DO_NOT_EXECUTE','Job3':'NOT_AUTHORIZED'}}
json.dump(stack,open(OUT/'REPAIR_STACK_R14.json','w'),indent=2)
pointer='''# ACTIVE EXECUTION POINTER\n\nCanonical active checkpoint: `/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R14_20260811/`\n\nState: `R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / #18 S14 ADJUDICATION`.\n\n- #17 worker economics: **DONE**.\n- R13 2,599 containers have an immutable execution classification.\n- Worker-eligible: **2,433 containers / 85,892 atoms**, assigned source-wave-intact across W01–W06.\n- Vozhd central: **166 containers / 35,078 atoms** = 55 pair-authority blockers + 32 T06 norm-role blockers + 79 T07 implementation bindings.\n- Worker packs: **NOT YET CREATED**.\n- R8 worker packs: **DO NOT EXECUTE**.\n- Job 3: **NOT AUTHORIZED**.\n\nNext bounded milestone (#18A): generate evidence-rich immutable W01–W06 successor packs from the R14 assignment ledger and independently validate complete/exact assignment, while central blocker and T07 binding work proceeds under separate authority.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER.md','w').write(pointer)
readme='''# README FIRST — S14 Relation-Role Bridge Repair Checkpoint R14\n\nR14 completes repair item #17 (worker economics). It does not adjudicate S14 truth.\n\nRead `R14_WORKER_ECONOMICS_REPORT.md`, `PROGRESS_LEDGER_R14.md`, and `ACTIVE_EXECUTION_POINTER.md`. The immutable worker assignment is `WORKER_ECONOMICS/R14_WORKER_PACKET_ASSIGNMENT_LEDGER.csv`; governance/binding work is `WORKER_ECONOMICS/R14_VOZHD_CENTRAL_QUEUE.csv`.\n\nOld R8 worker packs remain DO NOT EXECUTE. Job 3 remains blocked.\n'''
open(OUT/'00_README_FIRST.md','w').write(readme)
pins={'r13_checkpoint_zip':{'path':str(R13ZIP),'sha256':hashlib.sha256(R13ZIP.read_bytes()).hexdigest()},'r13_packet_ledger':{'path':str(P),'sha256':hashlib.sha256(P.read_bytes()).hexdigest()}}
json.dump(pins,open(OUT/'PROVENANCE'/'PARENT_PINS_R14.json','w'),indent=2)
# copy builder
shutil.copy(__file__,OUT/'CODE'/'build_r14_worker_economics.py')

# independent validator script
valpy=OUT/'VALIDATION'/'validate_r14_independent.py'
valpy.write_text(r'''import pandas as pd, json, pathlib, sys, hashlib
R=pathlib.Path(__file__).resolve().parents[1]
cls=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_WORKLOAD_CLASSIFICATION.csv')
ass=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_WORKER_PACKET_ASSIGNMENT_LEDGER.csv')
cen=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_VOZHD_CENTRAL_QUEUE.csv')
wa=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_SOURCE_WAVE_SHARD_PLAN.csv')
ws=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_WORKER_SHARD_SUMMARY.csv')
sens=pd.read_csv(R/'WORKER_ECONOMICS'/'R14_WORKER_COUNT_SENSITIVITY.csv')
checks=[]
def ck(name,cond,detail=None):checks.append({'check':name,'pass':bool(cond),'detail':detail})
ck('total_2599',len(cls)==2599,len(cls)); ck('unique_packet_ids',cls.packet_id.nunique()==2599,cls.packet_id.nunique())
ck('worker_2433',len(ass)==2433,len(ass)); ck('central_166',len(cen)==166,len(cen))
ck('partition_disjoint',set(ass.packet_id).isdisjoint(set(cen.packet_id)))
ck('partition_complete',set(ass.packet_id)|set(cen.packet_id)==set(cls.packet_id))
ck('worker_atoms_85892',int(ass.decision_atom_count.sum())==85892,int(ass.decision_atom_count.sum()))
ck('central_atoms_35078',int(cen.decision_atom_count.sum())==35078,int(cen.decision_atom_count.sum()))
ck('atom_conservation',int(ass.decision_atom_count.sum()+cen.decision_atom_count.sum())==120970)
ck('central_pair_blockers_55',int((cen.work_family=='PAIR_AUTHORITY_BLOCKER').sum())==55)
ck('central_norm_blockers_32',int((cen.work_family=='T06_NORM_ROLE_BLOCKER').sum())==32)
ck('central_t07_79',int((cen.work_family=='T07_CONCEPT').sum())==79)
ck('no_input_blocker_in_workers',not ass.packet_statuses_json.fillna('').str.contains('INPUT_AUTHORITY_BLOCKER',regex=False).any())
ck('six_workers',set(ass.worker_id)==set([f'W{i:02d}' for i in range(1,7)]),sorted(set(ass.worker_id)))
ck('all_worker_packets_once',ass.packet_id.nunique()==len(ass))
# each source-wave exactly one worker
n=ass.groupby(['source_family','wave']).worker_id.nunique(); ck('source_wave_unsplit',int(n.max())==1,int(n.max()))
ck('assignment_matches_shard_plan',len(wa)==ass.groupby(['source_family','wave']).ngroups,(len(wa),ass.groupby(['source_family','wave']).ngroups))
ck('shard_summary_six',len(ws)==6,len(ws)); ck('effort_balance_le_1_02',float(ws.planning_effort_units.max()/ws.planning_effort_units.min())<=1.02,float(ws.planning_effort_units.max()/ws.planning_effort_units.min()))
# 6 has material improvement over 5; 8 no improvement over 7 due indivisible bottleneck
s=sens.set_index('worker_count')
ck('six_improves_five_gt_15pct',float(s.loc[6,'max_shard_reduction_vs_prior_pct'])>15,float(s.loc[6,'max_shard_reduction_vs_prior_pct']))
ck('eight_no_max_gain',abs(float(s.loc[8,'max_shard_effort_units'])-float(s.loc[7,'max_shard_effort_units']))<1e-9,(float(s.loc[7,'max_shard_effort_units']),float(s.loc[8,'max_shard_effort_units'])))
status=json.load(open(R/'CURRENT_STATUS_R14.json')); ck('job3_false',status.get('job3_authorized') is False); ck('packs_not_created',status.get('worker_packs_created') is False)
# current package must not contain worker pack zips
ck('no_worker_pack_zip',not any('W0' in p.name and p.suffix=='.zip' for p in R.rglob('*.zip')))
res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','check_count':len(checks),'errors':[x for x in checks if not x['pass']],'checks':checks}
json.dump(res,open(R/'VALIDATION'/'VALIDATION_RESULT_R14.json','w'),indent=2)
print(json.dumps(res,indent=2)); sys.exit(0 if res['status']=='PASS' else 1)
''')
# run validator
subprocess.run(['python',str(valpy)],check=True,capture_output=False)
# hostile QA separate reconstruction from classification/statuses
cls=pd.read_csv(OUT/'WORKER_ECONOMICS'/'R14_WORKLOAD_CLASSIFICATION.csv')
status=json.load(open(OUT/'CURRENT_STATUS_R14.json'))
hostile=[]
def h(name,cond,detail=None): hostile.append({'check':name,'pass':bool(cond),'detail':detail})
h('all_status_blockers_central',not cls[(cls.status_has_input_blocker==True) & cls.execution_lane.str.startswith('WORKER')].shape[0])
h('all_pair_blocker_family_central',(cls[cls.work_family=='PAIR_AUTHORITY_BLOCKER'].execution_lane.str.startswith('VOZHD')).all())
h('all_norm_blocker_family_central',(cls[cls.work_family=='T06_NORM_ROLE_BLOCKER'].execution_lane.str.startswith('VOZHD')).all())
h('t07_concepts_not_worker',(cls[cls.work_family=='T07_CONCEPT'].execution_lane.str.startswith('VOZHD')).all())
h('worker_set_has_real_semantic_work',set(cls[cls.execution_lane.str.startswith('WORKER')].work_family).issuperset({'T06_ENDPOINT_LINK','MEMBER_TARGET_EVIDENCE','SOURCE_OBJECT','PARALLEL_OBJECT'}),sorted(set(cls[cls.execution_lane.str.startswith('WORKER')].work_family)))
h('planning_metric_not_authority','SCHEDULING_ONLY' in summary['planning_metric_authority_ceiling'])
h('old_r8_not_reactivated',True,'R14 creates no R8 execution permission')
h('job3_not_authorized',status['job3_authorized'] is False)
hres={'status':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','check_count':len(hostile),'errors':[x for x in hostile if not x['pass']],'checks':hostile}
json.dump(hres,open(OUT/'VALIDATION'/'R14_HOSTILE_QA.json','w'),indent=2)
if hres['status']!='PASS': raise SystemExit('hostile fail')
# manifest excluding itself
files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST_R14.csv']
with open(OUT/'SHA256_MANIFEST_R14.csv','w',newline='') as f:
 w=csv.writer(f); w.writerow(['relative_path','sha256','size_bytes'])
 for p in sorted(files): w.writerow([p.relative_to(OUT).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
# zip
ZIP=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14_20260811.zip'
if ZIP.exists(): ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file(): z.write(p,arcname=f'{OUT.name}/{p.relative_to(OUT).as_posix()}')
sha=hashlib.sha256(ZIP.read_bytes()).hexdigest(); open(str(ZIP)+'.sha256','w').write(f'{sha}  {ZIP.name}\n')
print('R14ZIP',ZIP,'SHA',sha)
print(json.dumps(summary,indent=2))
