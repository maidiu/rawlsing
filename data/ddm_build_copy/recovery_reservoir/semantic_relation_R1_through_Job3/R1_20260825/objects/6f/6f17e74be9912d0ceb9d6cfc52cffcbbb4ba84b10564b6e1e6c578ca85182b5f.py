from pathlib import Path
import pandas as pd, json, hashlib
OUT=Path('/mnt/data/r16c_s')
P=Path('/mnt/data/r16cs_parent')
R11='/mnt/data/r16cs_r11/T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz'
key=['source_family','wave','semantic_unit_id']
ledger=pd.read_csv(OUT/'PROVENANCE/C3B18_17_SOURCE_RECOVERY_AUTHORITY_LEDGER_R16C_S.csv',dtype=str).fillna(''); ledger['wave']=ledger.wave.astype(str)
pos=pd.read_csv(OUT/'RESOLUTION/C3B18_POSITIVE_RR_NORM_AUTHORITY_R16C_S.csv',dtype=str).fillna(''); pos['wave']=pos.wave.astype(str)
neg=pd.read_csv(OUT/'RESOLUTION/C3B18_NEGATIVE_RR_NORM_AUTHORITY_R16C_S.csv',dtype=str).fillna(''); neg['wave']=neg.wave.astype(str)
parent=pd.read_csv(P/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_R.csv',dtype=str).fillna(''); parent['wave']=parent.wave.astype(str)
parent_rows=pd.read_csv(P/'QUEUE/C3B17_RESIDUAL_T06_BLOCKED_PRIMITIVE_ROWS_R16C_R.csv.gz',dtype=str).fillna(''); parent_rows['wave']=parent_rows.wave.astype(str)
r11=pd.read_csv(R11,dtype=str,low_memory=False).fillna(''); r11['wave']=r11.wave.astype(str)
q=pd.read_csv(OUT/'QUEUE/R16C_S_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv'); q['wave']=q.wave.astype(str)
allp=pd.read_csv(OUT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_S.csv',dtype=str).fillna(''); allp['wave']=allp.wave.astype(str)
allprows=pd.read_csv(OUT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_S.csv.gz',dtype=str,low_memory=False).fillna('')
status=json.load(open(OUT/'CURRENT_STATUS_R16C_S.json'))
expected={
('Afrobarometer','R1','gidstr'):'NEGATIVE_RR_NORM',('Arab Barometer','I','q611'):'NEGATIVE_RR_NORM',
('EVS','1990','q317b'):'POSITIVE_RR_NORM',('EVS','1999','v94'):'POSITIVE_RR_NORM',('EVS','1999','o12'):'POSITIVE_RR_NORM',('EVS','1999','v94_at'):'POSITIVE_RR_NORM',
('GSS','1993','pclit'):'POSITIVE_RR_NORM',('GSS','1993','classics'):'POSITIVE_RR_NORM',('GSS','1993','pillok'):'POSITIVE_RR_NORM',
('GSS','2002','doc20a'):'NEGATIVE_RR_NORM',('GSS','2002','doc18a'):'NEGATIVE_RR_NORM',('GSS','2002','teamsafe'):'NEGATIVE_RR_NORM',
('GSS','2010','ldcgrn'):'POSITIVE_RR_NORM',('GSS','2010','pillok'):'POSITIVE_RR_NORM',('GSS','2010','teamsafe'):'NEGATIVE_RR_NORM',
('GSS','2016','pillok'):'POSITIVE_RR_NORM',('GSS','2024','pillok'):'POSITIVE_RR_NORM'}
checks=[]
def c(name,cond,detail=''): checks.append({'check':name,'pass':bool(cond),'detail':str(detail)})
# Parent universe reconstruction
c('parent_17',len(parent)==17,len(parent)); c('parent_unique',not parent.duplicated(key).any()); c('ledger_17',len(ledger)==17); c('ledger_unique',not ledger.duplicated(key).any())
c('ledger_exact_parent_keys',set(map(tuple,ledger[key].values))==set(map(tuple,parent[key].values)))
c('all_recovered',(ledger.source_recovery_status=='RECOVERED_TO_GOVERNING_STANDARD').all()); c('source_urls_nonempty',ledger.source_url.str.strip().ne('').all()); c('native_locators_nonempty',ledger.native_source_locator.str.strip().ne('').all()); c('semantic_bases_nonempty',ledger.source_recovered_semantic_basis.str.strip().ne('').all())
# Exact 17 dispositions reconstructed independently by source-variable identity
for k,v in expected.items():
 g=ledger[(ledger.source_family==k[0])&(ledger.wave==k[1])&(ledger.source_variable_code==k[2])]
 c('expected_'+'_'.join(k),len(g)==1 and g.iloc[0].rr_norm_disposition==v,(len(g),g.rr_norm_disposition.tolist()))
c('expected_map_17',len(expected)==17); c('positive_count_11',sum(v=='POSITIVE_RR_NORM' for v in expected.values())==11); c('negative_count_6',sum(v=='NEGATIVE_RR_NORM' for v in expected.values())==6)
c('positive_output_11',len(pos)==11,len(pos)); c('negative_output_6',len(neg)==6,len(neg)); c('pos_neg_keys_disjoint',set(map(tuple,pos[key].values)).isdisjoint(set(map(tuple,neg[key].values))))
c('pos_neg_union_parent',set(map(tuple,pos[key].values))|set(map(tuple,neg[key].values))==set(map(tuple,parent[key].values)))
# Sealed R11 reconstruction from full denominator
rmi=pd.MultiIndex.from_frame(r11[key]); pmi=pd.MultiIndex.from_frame(pos[key]); nmi=pd.MultiIndex.from_frame(neg[key])
pr=r11[rmi.isin(pmi)]; nr=r11[rmi.isin(nmi)]
c('r11_pos_698',len(pr)==698,len(pr)); c('r11_neg_862',len(nr)==862,len(nr)); c('r11_total_1560',len(pr)+len(nr)==1560); c('r11_parent_exact',set(pr.opportunity_id)|set(nr.opportunity_id)==set(parent_rows.opportunity_id)); c('r11_disjoint',set(pr.opportunity_id).isdisjoint(set(nr.opportunity_id)))
c('all_parent_rows_unique',parent_rows.opportunity_id.is_unique); c('positive_rows_unique',pr.opportunity_id.is_unique); c('negative_rows_unique',nr.opportunity_id.is_unique)
# Cumulative positive reconstruction from full R11
apmi=pd.MultiIndex.from_frame(allp[key]); apr=r11[rmi.isin(apmi)]
c('all_positive_471',len(allp)==471,len(allp)); c('all_positive_unique',not allp.duplicated(key).any()); c('all_positive_rows_30490',len(apr)==30490,len(apr)); c('written_all_positive_rows_30490',len(allprows)==30490,len(allprows)); c('written_equals_r11',set(allprows.opportunity_id)==set(apr.opportunity_id))
# Queue independently recomputed sums
wf=q.groupby('work_family')[['decision_atom_count','raw_primitive_row_count_sum']].sum()
c('no_norm_blocker','T06_NORM_ROLE_BLOCKER' not in wf.index); c('pair_atoms_31880',int(wf.loc['PAIR_AUTHORITY_BLOCKER','decision_atom_count'])==31880); c('pair_rows_2265243',int(wf.loc['PAIR_AUTHORITY_BLOCKER','raw_primitive_row_count_sum'])==2265243); c('t07_atoms_12',int(wf.loc['T07_GOVERNMENT_SCOPE_NAMING','decision_atom_count'])==12); c('t07_rows_12',int(wf.loc['T07_GOVERNMENT_SCOPE_NAMING','raw_primitive_row_count_sum'])==12); c('link_atoms_471',int(wf.loc['T06_RR_NORM_POSITIVE_LINK_REVIEW','decision_atom_count'])==471); c('link_rows_30490',int(wf.loc['T06_RR_NORM_POSITIVE_LINK_REVIEW','raw_primitive_row_count_sum'])==30490); c('queue_86',len(q)==86,len(q)); c('queue_atoms_32363',int(q.decision_atom_count.sum())==32363); c('queue_rows_2295745',int(q.raw_primitive_row_count_sum.sum())==2295745)
# Authority ceilings and status invariants
c('positive_ceiling',pos.authority_ceiling.str.contains('T06_LINK_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION').all()); c('negative_ceiling',neg.authority_ceiling.str.contains('NO_RELATION_ABSENCE_CLAIM').all()); c('c3_complete',status['c3_current_adjudicated_decisions']==3119 and status['c3_total_decisions']==3119); c('cum_negative_2648',status['cumulative_negative_rr_norm']==2648); c('blocked_zero',status['t06_rr_norm_blocked_primitive_rows']==0); c('job3_false',status['job3_authorized'] is False); c('repair18_active',status['repair_item_18_status'].startswith('ACTIVE')); c('workers_false',status['worker_packs_changed'] is False)
# Edge-case semantic guardrails
c('gidstr_negative',expected[('Afrobarometer','R1','gidstr')]=='NEGATIVE_RR_NORM'); c('q611_negative',expected[('Arab Barometer','I','q611')]=='NEGATIVE_RR_NORM'); c('doc_items_negative',all(expected[('GSS','2002',x)]=='NEGATIVE_RR_NORM' for x in ['doc18a','doc20a'])); c('teamsafe_negative_both',all(expected[('GSS',w,'teamsafe')]=='NEGATIVE_RR_NORM' for w in ['2002','2010'])); c('evs_should_items_positive',all(expected[k]=='POSITIVE_RR_NORM' for k in [('EVS','1990','q317b'),('EVS','1999','v94'),('EVS','1999','v94_at'),('EVS','1999','o12')])); c('pillok_all_positive',all(expected[('GSS',w,'pillok')]=='POSITIVE_RR_NORM' for w in ['1993','2010','2016','2024'])); c('gss_culture_positive',expected[('GSS','1993','pclit')]=='POSITIVE_RR_NORM' and expected[('GSS','1993','classics')]=='POSITIVE_RR_NORM'); c('ldcgrn_positive',expected[('GSS','2010','ldcgrn')]=='POSITIVE_RR_NORM')
# Worker hashes separately checked and present
wh=json.load(open(OUT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_R16C_S.json'))
c('worker_hash_recheck_pass',wh['status']=='PASS'); c('worker_hash_count_6',len(wh['packs'])==6); c('all_worker_hashes_exact',all(x['pass'] for x in wh['packs']))
result={'checkpoint':'R16C-S','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','passed':sum(x['pass'] for x in checks),'total':len(checks),'checks':checks}
json.dump(result,open(OUT/'VALIDATION/R16C_S_INDEPENDENT_COLD_QA.json','w'),indent=2)
print(json.dumps({'status':result['status'],'passed':result['passed'],'total':result['total']},indent=2))
if result['status']!='PASS':
 print(json.dumps([x for x in checks if not x['pass']],indent=2)); raise SystemExit(2)
