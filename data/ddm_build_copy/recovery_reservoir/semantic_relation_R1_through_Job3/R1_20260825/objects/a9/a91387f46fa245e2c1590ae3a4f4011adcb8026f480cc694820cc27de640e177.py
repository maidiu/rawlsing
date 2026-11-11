import pandas as pd, json, pathlib, sys, hashlib
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
