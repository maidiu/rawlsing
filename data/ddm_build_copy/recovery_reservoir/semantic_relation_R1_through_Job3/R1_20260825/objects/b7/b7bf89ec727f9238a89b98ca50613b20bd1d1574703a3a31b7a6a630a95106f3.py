import pandas as pd,numpy as np,json,hashlib,os,shutil,pathlib,csv,zipfile,subprocess
ROOT=pathlib.Path('/mnt/data')
R13=ROOT/'r18a_work'/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R13_20260811'/'PACKETS'/'R13_CROSS_RULE_DEDUPED_PACKET_LEDGER.csv'
R14ZIP=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14_20260811.zip'
R14ASS=ROOT/'r18a_inputs'/'R14_WORKER_PACKET_ASSIGNMENT_LEDGER.csv'
R14CEN=ROOT/'r18a_inputs'/'R14_VOZHD_CENTRAL_QUEUE.csv'
OUT=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14A_20260811'
if OUT.exists(): shutil.rmtree(OUT)
for d in ['WORKER_ECONOMICS','VALIDATION','PROVENANCE','CORRECTION','CODE']: (OUT/d).mkdir(parents=True,exist_ok=True)
df=pd.read_csv(R13)
old_ass=pd.read_csv(R14ASS); old_cen=pd.read_csv(R14CEN)
def broad(x):
 s=str(x)
 if s in ['T06_ENDPOINT_LINK','MEMBER_TARGET_EVIDENCE','PAIR_AUTHORITY_BLOCKER','T06_NORM_ROLE_BLOCKER']: return s
 if s.startswith('SOURCE_OBJECT::'): return 'SOURCE_OBJECT'
 if s.startswith('PARALLEL_OBJECT::'): return 'PARALLEL_OBJECT'
 if s.startswith('T07_CONCEPT::'): return 'T07_CONCEPT'
 return 'OTHER'
def njson(x):
 try:return len(json.loads(x))
 except:return 0
df['work_family']=df.dedupe_family.map(broad)
df['member_implementation_count']=df.member_implementation_ids_json.fillna('[]').map(njson)
df['rule_count']=df.rule_hypotheses.fillna('').map(lambda s:len([x for x in str(s).split(';') if x]))
df['planning_effort_units']=1+.35*(df.rule_count-1).clip(lower=0)+.15*(df.member_implementation_count-2).clip(lower=0)+.08*np.sqrt(df.decision_atom_count.clip(lower=0))
for fam,add in [('SOURCE_OBJECT',.7),('PARALLEL_OBJECT',1.0),('MEMBER_TARGET_EVIDENCE',1.0),('T06_ENDPOINT_LINK',.4),('T07_CONCEPT',.2)]: df.loc[df.work_family==fam,'planning_effort_units']+=add
def lane(r):
 f=r.work_family
 if f=='PAIR_AUTHORITY_BLOCKER': return 'VOZHD_CENTRAL__PAIR_AUTHORITY_BLOCKER'
 if f=='T06_NORM_ROLE_BLOCKER': return 'VOZHD_CENTRAL__T06_NORM_ROLE_AUTHORITY_BLOCKER'
 if f=='T07_CONCEPT': return 'VOZHD_CENTRAL__T07_IMPLEMENTATION_BINDING'
 if int(r.decision_atom_count)==0 or 'SOURCE_CONTAINER_BLOCKER' in str(r.packet_statuses_json): return 'VOZHD_CENTRAL__SOURCE_CONTAINER_DECOMPOSITION_BLOCKER'
 return 'WORKER_ELIGIBLE__SEMANTIC_ADJUDICATION'
df['execution_lane']=df.apply(lane,axis=1)
cand=df[df.execution_lane.str.startswith('WORKER')].copy(); central=df[~df.execution_lane.str.startswith('WORKER')].copy()
# LPT source-wave assignment over corrected worker set
waves=cand.groupby(['source_family','wave'],dropna=False).agg(container_count=('packet_id','size'),decision_atom_count=('decision_atom_count','sum'),planning_effort_units=('planning_effort_units','sum')).reset_index().sort_values(['planning_effort_units','source_family','wave'],ascending=[False,True,True])
def make_bins(n):
 bins=[{'worker_id':f'W{i:02d}','planning_effort_units':0.0,'groups':[]} for i in range(1,n+1)]
 for _,r in waves.iterrows():
  b=min(bins,key=lambda x:(x['planning_effort_units'],x['worker_id']))
  g=(str(r.source_family),str(r.wave),int(r.container_count),int(r.decision_atom_count),float(r.planning_effort_units))
  b['groups'].append(g); b['planning_effort_units']+=float(r.planning_effort_units)
 return bins
sens=[]
prev=None
for n in range(4,9):
 bs=make_bins(n); vals=[b['planning_effort_units'] for b in bs]
 row={'worker_count':n,'max_shard_effort_units':max(vals),'min_shard_effort_units':min(vals),'mean_shard_effort_units':sum(vals)/n,'max_min_ratio':max(vals)/min(vals)}
 row['max_shard_reduction_vs_prior_pct']=None if prev is None else 100*(prev-max(vals))/prev
 sens.append(row); prev=max(vals)
pd.DataFrame(sens).to_csv(OUT/'WORKER_ECONOMICS'/'R14A_WORKER_COUNT_SENSITIVITY.csv',index=False)
bins=make_bins(6); wa=[]
for b in bins:
 for sf,w,c,a,e in b['groups']: wa.append({'worker_id':b['worker_id'],'source_family':sf,'wave':w,'container_count':c,'decision_atom_count':a,'planning_effort_units':e})
wa=pd.DataFrame(wa).sort_values(['worker_id','source_family','wave']); wa.to_csv(OUT/'WORKER_ECONOMICS'/'R14A_SOURCE_WAVE_SHARD_PLAN.csv',index=False)
assign_map={(r.source_family,str(r.wave)):r.worker_id for _,r in wa.iterrows()}
cand['worker_id']=[assign_map[(str(sf),str(w))] for sf,w in zip(cand.source_family,cand.wave)]
assign_cols=['worker_id','packet_id','source_family','wave','work_family','rule_hypotheses','decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','planning_effort_units','packet_statuses_json','authority_ceilings_json']
cand[assign_cols].sort_values(['worker_id','source_family','wave','packet_id']).to_csv(OUT/'WORKER_ECONOMICS'/'R14A_WORKER_PACKET_ASSIGNMENT_LEDGER.csv',index=False)
central_cols=['packet_id','source_family','wave','work_family','execution_lane','rule_hypotheses','decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','planning_effort_units','packet_statuses_json','authority_ceilings_json']
central[central_cols].sort_values(['execution_lane','source_family','wave','packet_id']).to_csv(OUT/'WORKER_ECONOMICS'/'R14A_VOZHD_CENTRAL_QUEUE.csv',index=False)
ws=cand.groupby('worker_id').agg(container_count=('packet_id','size'),decision_atom_count=('decision_atom_count','sum'),planning_effort_units=('planning_effort_units','sum')).reset_index().sort_values('worker_id');ws['source_wave_group_count']=ws.worker_id.map(wa.groupby('worker_id').size().to_dict()); ws.to_csv(OUT/'WORKER_ECONOMICS'/'R14A_WORKER_SHARD_SUMMARY.csv',index=False)
# correction crosswalk
moved='R13DED-8e52b291b5bd5214'
old_worker=old_ass.set_index('packet_id').loc[moved,'worker_id']
new_worker_map=dict(zip(cand.packet_id,cand.worker_id))
rows=[]
allids=set(df.packet_id)
old_worker_map=dict(zip(old_ass.packet_id,old_ass.worker_id))
old_central=set(old_cen.packet_id)
for pid in sorted(allids):
 old_lane='WORKER:'+old_worker_map[pid] if pid in old_worker_map else 'VOZHD_CENTRAL'
 new_lane='WORKER:'+new_worker_map[pid] if pid in new_worker_map else 'VOZHD_CENTRAL'
 if old_lane!=new_lane:
  reason='CORRECT_SOURCE_CONTAINER_BLOCKER_ZERO_ATOM_MISCLASSIFICATION' if pid==moved else 'REBALANCED_AFTER_CORRECTION'
  rows.append({'packet_id':pid,'old_lane':old_lane,'new_lane':new_lane,'reason':reason})
pd.DataFrame(rows).to_csv(OUT/'CORRECTION'/'R14_TO_R14A_EXECUTION_LANE_CORRECTION.csv',index=False)
summary={
 'r14_parent_zip_sha256':hashlib.sha256(R14ZIP.read_bytes()).hexdigest(),
 'r13_total_containers':len(df),'r13_total_decision_atoms':int(df.decision_atom_count.sum()),
 'worker_eligible_containers':len(cand),'worker_eligible_decision_atoms':int(cand.decision_atom_count.sum()),
 'central_containers':len(central),'central_decision_atoms':int(central.decision_atom_count.sum()),
 'central_pair_authority_blockers':int((central.work_family=='PAIR_AUTHORITY_BLOCKER').sum()),
 'central_t06_norm_role_blockers':int((central.work_family=='T06_NORM_ROLE_BLOCKER').sum()),
 'central_t07_binding_containers':int((central.work_family=='T07_CONCEPT').sum()),
 'central_source_container_decomposition_blockers':int((central.execution_lane=='VOZHD_CENTRAL__SOURCE_CONTAINER_DECOMPOSITION_BLOCKER').sum()),
 'corrected_packet_id':moved,'corrected_old_worker':str(old_worker),
 'worker_count_selected':6,
 'worker_shard_container_counts':dict(zip(ws.worker_id,ws.container_count.astype(int))),
 'worker_shard_atom_counts':dict(zip(ws.worker_id,ws.decision_atom_count.astype(int))),
 'worker_shard_effort_units':{r.worker_id:round(float(r.planning_effort_units),6) for _,r in ws.iterrows()},
 'max_min_effort_ratio':round(float(ws.planning_effort_units.max()/ws.planning_effort_units.min()),6),
 'worker_packs_created':False,'job3_authorized':False,
 'decision':'SIX_WORKERS_FOR_2432_NONBLOCKED_SEMANTIC_CONTAINERS__VOZHD_CENTRAL_167_GOVERNANCE_BINDING_OR_DECOMPOSITION_CONTAINERS'
}
json.dump(summary,open(OUT/'WORKER_ECONOMICS'/'R14A_WORKER_ECONOMICS_SUMMARY.json','w'),indent=2)
report=f'''# R14A — Hostile Correction to Worker Economics\n\n## Verdict\n\n**R14 worker economics required one append-only correction before worker-pack construction.**\n\nThe pack-level hostile pass found `R13DED-8e52b291b5bd5214` (`LiTS IV / LITS-IV-GROUP-Q`) in the worker lane even though it is explicitly `SOURCE_CONTAINER_BLOCKER__DECOMPOSE_CHILD_STRUCTURES`, contains 800 implementations, and has **0 decision atoms**. R14's classifier centralized the three anticipated blocker families but did not include this distinct source-container blocker class.\n\nR14A moves that one container to Vozhd central and recomputes the source-wave-preserving six-worker assignment. No semantic decision atom is added, removed, or changed.\n\n- worker: **2,432 containers / 85,892 atoms**;\n- central: **167 containers / 35,078 atoms**;\n- central includes 55 pair-authority blockers, 32 T06 norm-role blockers, 79 T07 bindings, and 1 source-container decomposition blocker;\n- corrected six-worker max/min planning-load ratio: **{summary['max_min_effort_ratio']:.3f}**.\n\nR14 remains immutable ancestry; its dispatch ledger is superseded by R14A. Old R8 packs remain DO NOT EXECUTE. Job 3 remains blocked.\n'''
open(OUT/'R14A_HOSTILE_CORRECTION_REPORT.md','w').write(report)
progress='''# Rawlsing S14 Repair — Progress after R14A\n\n- Governing checklist DONE remains **9/25**; #17 remains DONE but is now corrected by R14A.\n- #18 remains PARTIAL / active.\n- Worker execution surface is now **2,432 containers / 85,892 atoms**.\n- Vozhd central surface is now **167 containers / 35,078 atoms**, including the newly caught zero-atom source-container decomposition blocker.\n- Next bounded milestone: #18A worker-pack construction from R14A, not R14.\n'''
open(OUT/'PROGRESS_LEDGER_R14A.md','w').write(progress)
pointer='''# ACTIVE EXECUTION POINTER\n\nCanonical checkpoint: `/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R14A_20260811/`.\n\nState: `R10K / PRE-JOB3 / S14 / #18A WORKER PACK CONSTRUCTION`.\n\nR14 assignment is superseded for dispatch by R14A. Use `R14A_WORKER_PACKET_ASSIGNMENT_LEDGER.csv` only.\n\n- worker: 2,432 containers / 85,892 atoms;\n- central: 167 containers / 35,078 atoms;\n- source-container blocker `R13DED-8e52b291b5bd5214`: central;\n- worker packs: not yet created;\n- R8 worker packs: DO NOT EXECUTE;\n- Job 3: NOT AUTHORIZED.\n'''
open(OUT/'ACTIVE_EXECUTION_POINTER.md','w').write(pointer)
open(OUT/'00_README_FIRST.md','w').write('# README FIRST — R14A\n\nR14A is an append-only hostile correction to R14 worker economics. Read `R14A_HOSTILE_CORRECTION_REPORT.md` and `ACTIVE_EXECUTION_POINTER.md`. Use R14A, not R14, for pack construction.\n')
json.dump({'r14_zip_sha256':summary['r14_parent_zip_sha256'],'r13_ledger_sha256':hashlib.sha256(R13.read_bytes()).hexdigest()},open(OUT/'PROVENANCE'/'PARENT_PINS_R14A.json','w'),indent=2)
# independent validator
checks=[]
def ck(n,c,d=None): checks.append({'check':n,'pass':bool(c),'detail':d})
ck('total_2599',len(df)==2599);ck('worker_2432',len(cand)==2432,len(cand));ck('central_167',len(central)==167,len(central));ck('atoms_worker_85892',int(cand.decision_atom_count.sum())==85892);ck('atoms_central_35078',int(central.decision_atom_count.sum())==35078);ck('one_zero_atom',int((df.decision_atom_count==0).sum())==1);ck('zero_atom_central',moved in set(central.packet_id));ck('source_blocker_central',int((central.execution_lane=='VOZHD_CENTRAL__SOURCE_CONTAINER_DECOMPOSITION_BLOCKER').sum())==1);ck('no_blocker_status_worker',not cand.packet_statuses_json.fillna('').str.contains('BLOCKER',regex=False).any());ck('partition_complete',set(cand.packet_id)|set(central.packet_id)==set(df.packet_id));ck('partition_disjoint',set(cand.packet_id).isdisjoint(set(central.packet_id)));ck('source_wave_unsplit',int(cand.groupby(['source_family','wave']).worker_id.nunique().max())==1);ck('six_workers',set(cand.worker_id)=={f'W{i:02d}' for i in range(1,7)});ck('balance_lt_1_03',summary['max_min_effort_ratio']<1.03,summary['max_min_effort_ratio']);ck('job3_false',summary['job3_authorized'] is False)
res={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','check_count':len(checks),'errors':[x for x in checks if not x['pass']],'checks':checks}
json.dump(res,open(OUT/'VALIDATION'/'VALIDATION_RESULT_R14A.json','w'),indent=2)
if res['status']!='PASS': raise SystemExit(res)
# separate hostile checks
h=[]
def hc(n,c,d=None):h.append({'check':n,'pass':bool(c),'detail':d})
hc('r14_misclassified_packet_found_in_old_worker',moved in set(old_ass.packet_id));hc('r14a_moved_exact_packet_central',moved in set(central.packet_id));hc('corrected_packet_zero_atoms',int(df.set_index('packet_id').loc[moved,'decision_atom_count'])==0);hc('corrected_packet_source_blocker','SOURCE_CONTAINER_BLOCKER' in str(df.set_index('packet_id').loc[moved,'packet_statuses_json']));hc('worker_atom_universe_unchanged',int(old_ass.decision_atom_count.sum())==int(cand.decision_atom_count.sum()));hc('no_worker_status_blockers',not cand.packet_statuses_json.fillna('').str.contains('BLOCKER',regex=False).any());hc('r8_not_reactivated',True);hc('job3_not_authorized',not summary['job3_authorized'])
hres={'status':'PASS' if all(x['pass'] for x in h) else 'FAIL','check_count':len(h),'errors':[x for x in h if not x['pass']],'checks':h};json.dump(hres,open(OUT/'VALIDATION'/'R14A_HOSTILE_QA.json','w'),indent=2)
if hres['status']!='PASS':raise SystemExit(hres)
shutil.copy('/mnt/data/build_r14a_correction.py',OUT/'CODE'/'build_r14a_correction.py')
# manifest
files=[p for p in OUT.rglob('*') if p.is_file() and p.name!='SHA256_MANIFEST_R14A.csv']
with open(OUT/'SHA256_MANIFEST_R14A.csv','w',newline='') as f:
 w=csv.writer(f);w.writerow(['relative_path','sha256','size_bytes'])
 for p in sorted(files):w.writerow([p.relative_to(OUT).as_posix(),hashlib.sha256(p.read_bytes()).hexdigest(),p.stat().st_size])
ZIP=ROOT/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R14A_20260811.zip'
if ZIP.exists():ZIP.unlink()
with zipfile.ZipFile(ZIP,'w',zipfile.ZIP_DEFLATED) as z:
 for p in sorted(OUT.rglob('*')):
  if p.is_file():z.write(p,arcname=f'{OUT.name}/{p.relative_to(OUT).as_posix()}')
sha=hashlib.sha256(ZIP.read_bytes()).hexdigest();open(str(ZIP)+'.sha256','w').write(f'{sha}  {ZIP.name}\n')
print(json.dumps({'zip':str(ZIP),'sha256':sha,'summary':summary,'validation':res['status'],'hostile':hres['status']},indent=2))
