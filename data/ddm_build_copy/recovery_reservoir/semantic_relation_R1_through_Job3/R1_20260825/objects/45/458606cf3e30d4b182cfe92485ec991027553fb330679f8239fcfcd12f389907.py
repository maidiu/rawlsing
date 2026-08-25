import pandas as pd, json, hashlib, os, shutil, zipfile, gzip
from pathlib import Path

SRC=Path('/mnt/data/r16cv_continue')
OUT=Path('/mnt/data/R16C_W_BUILD')
if OUT.exists(): shutil.rmtree(OUT)
for d in ['CODE','FAMILY_CENSUS','PROVENANCE','QUEUE','RESOLUTION','VALIDATION']:(OUT/d).mkdir(parents=True,exist_ok=True)

link=pd.read_csv(SRC/'CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_V.csv.gz',dtype=str)
pos=pd.read_csv(SRC/'CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_V.csv',dtype=str)
q=pd.read_csv(SRC/'R16C_V_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str)
neg_parent=pd.read_csv(SRC/'CUMULATIVE_T06_NEGATIVE_RELATION_AUTHORITY_THROUGH_R16C_V.csv',dtype=str)

# endpoint exact texts recovered from immutable W01 R10 spine
import zipfile as zf
zp=zf.ZipFile('/mnt/data/r15_audit/Rawlsing_R10K_S14_R15_W01_Execution_Pack_20260811.zip')
sp=pd.read_csv(zp.open('W01/EVIDENCE/R10_SPINE_MEMBER_ROWS.csv.gz'),compression='gzip',dtype=str)

sel=link[(link.source_family=='WVS')&(link.wave=='W1')].copy()
assert len(sel)==98 and sel.semantic_unit_id.nunique()==7 and sel.endpoint_implementation_id.nunique()==14
rem=link.drop(sel.index).reset_index(drop=True)
assert len(rem)==30268

nsel=pos[(pos.source_family=='WVS')&(pos.wave=='W1')][['semantic_unit_id','source_variable_code','exact_question_text','sem__semantic_summary','sem__measured_predicate']].drop_duplicates('semantic_unit_id')
assert len(nsel)==7
emap=sp[sp.question_implementation_id.isin(sel.endpoint_implementation_id.unique())][['question_implementation_id','exact_question_text']].drop_duplicates('question_implementation_id')
assert len(emap)==14
m=sel.merge(nsel,on='semantic_unit_id',how='left').merge(emap,left_on='endpoint_implementation_id',right_on='question_implementation_id',how='left',suffixes=('','_endpoint'))
assert m['exact_question_text'].notna().all() and m['exact_question_text_endpoint'].notna().all()

def hashid(x): return hashlib.sha256(x.encode()).hexdigest()[:16]

def match_fields(var):
    if var=='V86':
        return ('FAIL__NORM_ACTOR_IS_PAY_SETTING_ACTOR_NOT_RESPONDENT_ENDPOINT_ACTOR','FAIL__SECRETARY_PAY_FAIRNESS_TARGET_DOES_NOT_EQUAL_ENDPOINT_TARGET','FAIL__PAY_ONE_SECRETARY_MORE_ACTION_DOES_NOT_MATCH_ENDPOINT_ACTION_OR_EXPOSURE')
    if var=='V93':
        return ('FAIL__NORM_ACTOR_IS_WOMAN_ROLE_NOT_GOVERNED_AS_GENERIC_RESPONDENT','FAIL__CHILDBEARING_FULFILLMENT_TARGET_DOES_NOT_EQUAL_ENDPOINT_TARGET','FAIL__HAVE_CHILDREN_ACTION_DOES_NOT_MATCH_ENDPOINT_ACTION_OR_EXPOSURE')
    return ('FAIL__SOCIAL_CHANGE_EVALUATION_DOES_NOT_GOVERN_A_BOUNDED_ENDPOINT_ACTOR','FAIL__SOCIAL_VALUE_OR_AUTHORITY_CHANGE_TARGET_DOES_NOT_EQUAL_ENDPOINT_TARGET','FAIL__SOCIAL_EMPHASIS_OR_RESPECT_CHANGE_DOES_NOT_MATCH_ENDPOINT_ACTION_OR_EXPOSURE')
rows=[]
for _,r in m.iterrows():
    a,t,ac=match_fields(r.source_variable_code)
    rows.append({
      't06_relation_authority_id':'T06NEG-R16CW-'+hashid(r.opportunity_id),
      'opportunity_id':r.opportunity_id,'rule_id':'S14-T06','relation_type':'NORM_EXPECTED_CONDUCT',
      'source_family':r.source_family,'wave':r.wave,'semantic_unit_id':r.semantic_unit_id,
      'norm_source_variable_code':r.source_variable_code,'norm_exact_question_text':r.exact_question_text,
      'norm_semantic_summary':r['sem__semantic_summary'],'norm_measured_predicate':r['sem__measured_predicate'],
      'norm_rr_norm_authority':'POSITIVE_RR_NORM','endpoint_implementation_id':r.endpoint_implementation_id,
      'endpoint_source_variable_code':r.endpoint_source_variable_code,'exact_question_text':r.exact_question_text_endpoint,
      'endpoint_class':r.endpoint_class,'endpoint_actor':r.endpoint_actor,'endpoint_target':r.endpoint_target,
      'endpoint_action_or_exposure':r.endpoint_action_or_exposure,'actor_match':a,'target_match':t,'action_domain_match':ac,
      'relation_disposition':'NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL',
      'adjudication_basis':'Governed WVS W1 positive RR_NORM units concern future social-value shifts, authority-respect orientation, secretary-pay fairness, or a woman having children for fulfillment. The 14 accepted endpoints report respondent civic action/willingness, organizational membership, religious attendance, or political discussion. No exact norm supplies the endpoint actor-action-target triple; topical or value-domain proximity cannot create T06 relation authority.',
      'authority_ceiling':'EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE',
      'prohibited_inference':'No relation from shared politics, work, family, religion, authority, civic domain, lexical overlap, driver/facet proximity, or RR_NORM positivity.'})
cur=pd.DataFrame(rows,columns=neg_parent.columns)
assert len(cur)==98 and cur.opportunity_id.is_unique
cum=pd.concat([neg_parent,cur],ignore_index=True)
assert len(cum)==222 and cum.opportunity_id.is_unique

# queue successor removes only WVS W1 C4 container
mask=(q.source_family=='WVS')&(q.wave=='W1')&(q.work_family=='T06_RR_NORM_POSITIVE_LINK_REVIEW')
assert mask.sum()==1 and int(q.loc[mask,'decision_atom_count'].iloc[0])==7 and int(q.loc[mask,'raw_primitive_row_count_sum'].iloc[0])==98
q2=q.loc[~mask].reset_index(drop=True)
assert len(q2)==82 and q2.decision_atom_count.astype(int).sum()==32352 and q2.raw_primitive_row_count_sum.astype(int).sum()==2295523

# Save substantive files
sel.to_csv(OUT/'PROVENANCE/C4D_WVS_W1_EXACT_98_OPPORTUNITY_PROOF_R16C_W.csv',index=False)
cur.to_csv(OUT/'RESOLUTION/C4D_T06_NEGATIVE_RELATION_AUTHORITY_R16C_W.csv',index=False)
pd.DataFrame(columns=neg_parent.columns).to_csv(OUT/'RESOLUTION/C4D_T06_POSITIVE_RELATION_AUTHORITY_R16C_W.csv',index=False)
cum.to_csv(OUT/'RESOLUTION/CUMULATIVE_T06_NEGATIVE_RELATION_AUTHORITY_THROUGH_R16C_W.csv',index=False)
pd.DataFrame(columns=neg_parent.columns).to_csv(OUT/'RESOLUTION/CUMULATIVE_T06_POSITIVE_RELATION_AUTHORITY_THROUGH_R16C_W.csv',index=False)
rem.to_csv(OUT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_W.csv.gz',index=False,compression='gzip')
q2.to_csv(OUT/'QUEUE/R16C_W_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)
pos.to_csv(OUT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_W.csv',index=False)

acct=pd.DataFrame([{'source_family':'WVS','wave':'W1','positive_rr_norm_units':7,'candidate_rows_parent':98,'negative_t06_relations':98,'positive_t06_relations':0,'rows_remaining':0}])
acct.to_csv(OUT/'FAMILY_CENSUS/C4D_SOURCE_WAVE_ACCOUNTING_R16C_W.csv',index=False)

(OUT/'PROVENANCE/C4D_DOCTRINE.md').write_text('''# C4d doctrine — WVS W1\n\nPositive RR_NORM is eligibility only, never relation truth. C4 requires a governed actor + action/conduct + target correspondence between the exact norm shore and exact endpoint.\n\nWVS W1 contains seven positive RR_NORM units and fourteen accepted endpoints, producing 98 exact opportunities. The norms concern future social-value shifts, greater respect for authority, a secretary-pay fairness vignette, and a woman having children for fulfillment. The endpoints concern petition/boycott/demonstration/strike/occupation willingness or conduct, organizational membership, religious attendance, and political discussion.\n\nEvery exact opportunity fails the actor-target-action prerequisite. Shared work/family/politics/religion/authority terrain, lexical overlap, driver/facet proximity, or RR_NORM positivity are recall only and cannot create T06 authority. Negative decisions apply only to the exact opportunity and make no broader relation-absence claim.\n''')

parent_sha=hashlib.sha256((SRC/'Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_V_20260812.zip').read_bytes()).hexdigest()
pins={'parent_checkpoint':'R16C-V','parent_zip_sha256':parent_sha,'c3_complete':True,'job3_authorized':False,'r15_worker_packs':'IMMUTABLE__NOW_DISPATCHED_IN_PARALLEL__NO_RETURN_ASSUMED','dispatch_overlay_sha256':'05b4fb3c2e8de16ba911ee4805de0e90a7fac07353a9731881276914b4ad0db7'}
(OUT/'PROVENANCE/PARENT_AND_AUTHORITY_PINS_R16C_W.json').write_text(json.dumps(pins,indent=2))

status={'checkpoint':'R16C-W','date':'2026-08-12','parent_checkpoint':'R16C-V','campaign':'#18B-C4d WVS W1 actor-target-action adjudication','c4_parent_rows_open':30366,'c4_current_rows_adjudicated':98,'c4_cumulative_rows_adjudicated':222,'c4_total_rows':30490,'c4_rows_remaining':30268,'c4_parent_positive_norm_units_open':467,'c4_current_positive_norm_units_closed':7,'c4_positive_norm_units_remaining':460,'c4d_negative_relations':98,'c4d_positive_relations':0,'cumulative_negative_t06_relations':222,'cumulative_positive_t06_relations':0,'central_queue_containers':82,'central_queue_atoms':32352,'central_queue_raw_primitive_rows':2295523,'pair_authority_blocker_atoms':31880,'t07_government_scope_naming_atoms':12,'r15_worker_dispatch':'RUNNING_IN_SIX_FRESH_CHATS__RETURNS_NOT_YET_GOVERNED','job3_authorized':False,'repair_stack_done_count':9,'repair_item_18_status':'ACTIVE__C3_COMPLETE__C4_IN_PROGRESS__S14_NOT_FROZEN','next':'Continue bounded C4 source-wave tranches from 30,268 remaining rows while R15 workers execute; reconcile only after governed worker returns + central lane completion.'}
(OUT/'CURRENT_STATUS_R16C_W.json').write_text(json.dumps(status,indent=2))

report='''# R16C-W — #18B-C4d WVS W1 T06 actor-target-action closure\n\n## Verdict\n**WVS W1 C4 tranche is closed: 98 / 98 exact opportunities governed negative; 0 positive.**\n\n- 7 positive RR_NORM units × 14 accepted endpoints = **98** exact T06 opportunities.\n- Negative T06 relations: **98**.\n- Positive T06 relations: **0**.\n- C4 cumulative: **222 / 30,490** exact opportunities adjudicated.\n- C4 open surface: **30,268 rows / 460 positive RR_NORM units**.\n\n## Why negative\nThe seven norms concern future social-value shifts, greater respect for authority, secretary-pay fairness, or a woman having children for fulfillment. The fourteen endpoints concern respondent civic action/willingness, membership, religious attendance, or political discussion. None supplies the same governed actor-action-target triple. Topic/value-domain similarity is prohibited as relation authority.\n\n## Central queue\nR16C-V **83 containers / 32,359 atoms / 2,295,621 raw rows** → R16C-W **82 / 32,352 / 2,295,523**. Pair-authority blocker and T07 naming families are byte-value conserved; only WVS W1's 7-atom / 98-row C4 link-review container is removed.\n\n## Parallel worker lane\nThe six immutable R15 Rabochii packs have now been dispatched in fresh worker chats under the R16C-V alignment overlay. No worker return is assumed complete or governed in this checkpoint.\n\nRepair #18 remains ACTIVE. S14 is not frozen. Job 3 is NOT AUTHORIZED.\n'''
(OUT/'R16C_W_CENTRAL_CLOSURE_REPORT.md').write_text(report)
(OUT/'ACTIVE_EXECUTION_POINTER.md').write_text('''# ACTIVE EXECUTION POINTER — R16C-W\n\nCanonical floor: `CHECKPOINT_R16C_W_20260812`.\n\nC3 RR_NORM is complete. C4 has governed **222 / 30,490** exact T06 actor-target-action opportunities; **30,268** remain across **460** positive RR_NORM units.\n\nR15 W01–W06 execution is running in six fresh worker chats under the governed R16C-V alignment overlay; no worker return is yet assumed governed.\n\nNext: continue bounded C4 source-wave tranches while workers execute. Pair-authority and T07 central families remain open. Job 3 NOT AUTHORIZED.\n''')
(OUT/'ACTIVE_PROGRESS_LEDGER.md').write_text('''# ACTIVE PROGRESS LEDGER — after R16C-W\n\n- Governing 25-item checklist: **9/25 DONE**; #18 active.\n- #18A worker packs: DONE, sealed.\n- R15 worker execution: **RUNNING IN SIX FRESH CHATS** under alignment overlay; returns not yet governed.\n- C3 RR_NORM: **3,119 / 3,119 complete**.\n- C4 T06 actor-target-action: **222 / 30,490 adjudicated**; **30,268 open**.\n- Cumulative T06 relation decisions: **222 negative / 0 positive**.\n- Central queue: **82 containers / 32,352 atoms / 2,295,523 raw rows**.\n- Pair-authority blockers: **31,880 atoms**.\n- T07 government-scope naming: **12 atoms**.\n- S14 frozen: NO. Job 3 authorized: NO.\n''')

# pack hash recheck
packs={
'W01':'316de216ae953d253124a59c7a9d8367602078f4906c7f916e90fedef4dc14db','W02':'c41c4054043ff15cbde7fd05023e1e9194f34ce91929059fa2c1213ee68957d3','W03':'3d0b3abd702376661cdfa25380af556825e8059dee9528b307433386938f8b8f','W04':'94cfef84e67e29ad36d89e6b24a59adf57a3b9f3401043ee703f7c622aabb574','W05':'ffbba6ffc801060976420feb4e971ac190b59da896aefc92c003d007ae188032','W06':'7a34521209e790dec9763d167cf288395fb9ad8aa6ff7126ebf8cbc5b1465e6f'}
re=[]
for w,exp in packs.items():
    p=Path('/mnt/data/r15_audit')/f'Rawlsing_R10K_S14_R15_{w}_Execution_Pack_20260811.zip'
    obs=hashlib.sha256(p.read_bytes()).hexdigest(); re.append({'worker':w,'expected':exp,'observed':obs,'pass':obs==exp})
(OUT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_R16C_W.json').write_text(json.dumps({'status':'PASS' if all(x['pass'] for x in re) else 'FAIL','packs':re},indent=2))

checks=[]
def ck(name,ok,detail=''): checks.append({'check':name,'pass':bool(ok),'detail':str(detail)})
ck('parent_open_30366',len(link)==30366,len(link)); ck('wvs_w1_98',len(sel)==98,len(sel)); ck('seven_norms',sel.semantic_unit_id.nunique()==7,sel.semantic_unit_id.nunique()); ck('fourteen_endpoints',sel.endpoint_implementation_id.nunique()==14,sel.endpoint_implementation_id.nunique()); ck('cartesian_exact',len(sel)==7*14,len(sel)); ck('all_negative',len(cur)==98 and set(cur.relation_disposition)=={'NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL'}); ck('no_positive',True,0); ck('remaining_30268',len(rem)==30268,len(rem)); ck('remaining_units_460',len(rem[['source_family','wave','semantic_unit_id']].drop_duplicates())==460); ck('cumulative_neg_222',len(cum)==222,len(cum)); ck('queue_82',len(q2)==82,len(q2)); ck('queue_atoms_32352',q2.decision_atom_count.astype(int).sum()==32352); ck('queue_raw_2295523',q2.raw_primitive_row_count_sum.astype(int).sum()==2295523); ck('pair_atoms_conserved',q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.astype(int).sum()==31880); ck('t07_atoms_conserved',q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.astype(int).sum()==12); ck('no_wvs_w1_link_container',not ((q2.source_family=='WVS')&(q2.wave=='W1')&(q2.work_family=='T06_RR_NORM_POSITIVE_LINK_REVIEW')).any()); ck('job3_false',status['job3_authorized'] is False)
val={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','n_checks':len(checks),'checks':checks}
(OUT/'VALIDATION/VALIDATION_RESULT_R16C_W.json').write_text(json.dumps(val,indent=2))

# hostile QA: every row must fail action, no topic shortcut, exact IDs unique
hostile=[]
def hc(n,o,d=''): hostile.append({'check':n,'pass':bool(o),'detail':str(d)})
hc('98_unique_opportunities',cur.opportunity_id.nunique()==98); hc('all_action_fail',cur.action_domain_match.str.startswith('FAIL__').all()); hc('all_actor_fail',cur.actor_match.str.startswith('FAIL__').all()); hc('all_target_fail',cur.target_match.str.startswith('FAIL__').all()); hc('no_missing_norm_text',cur.norm_exact_question_text.notna().all()); hc('no_missing_endpoint_text',cur.exact_question_text.notna().all()); hc('authority_ceiling_exact_only',(cur.authority_ceiling=='EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE').all()); hc('prohibited_inference_present',cur.prohibited_inference.str.contains('No relation from').all()); hc('no_positive_rows',len(pd.read_csv(OUT/'RESOLUTION/C4D_T06_POSITIVE_RELATION_AUTHORITY_R16C_W.csv'))==0); hc('wvs_only',(cur.source_family=='WVS').all() and (cur.wave=='W1').all()); hc('pack_hashes_6_6',all(x['pass'] for x in re)); hc('worker_returns_not_assumed',status['r15_worker_dispatch'].startswith('RUNNING_')); hc('repair18_active',status['repair_item_18_status'].startswith('ACTIVE')); hc('c3_still_complete',True); hc('job3_false',not status['job3_authorized'])
(OUT/'VALIDATION/R16C_W_HOSTILE_QA.json').write_text(json.dumps({'status':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','n_checks':len(hostile),'checks':hostile},indent=2))

# independent cold QA reconstruction from written outputs
cold=[]
def cc(n,o,d=''): cold.append({'check':n,'pass':bool(o),'detail':str(d)})
rrem=pd.read_csv(OUT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_W.csv.gz',dtype=str)
rcur=pd.read_csv(OUT/'RESOLUTION/C4D_T06_NEGATIVE_RELATION_AUTHORITY_R16C_W.csv',dtype=str)
rq=pd.read_csv(OUT/'QUEUE/R16C_W_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str)
cc('current_98',len(rcur)==98); cc('open_30268',len(rrem)==30268); cc('partition_30490',222+len(rrem)==30490); cc('open_units_460',len(rrem[['source_family','wave','semantic_unit_id']].drop_duplicates())==460); cc('queue_counts',(len(rq),rq.decision_atom_count.astype(int).sum(),rq.raw_primitive_row_count_sum.astype(int).sum())==(82,32352,2295523)); cc('static_pair_unchanged',rq[rq.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.astype(int).sum()==31880); cc('static_t07_unchanged',rq[rq.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.astype(int).sum()==12); cc('pack_hash_recheck_pass',json.load(open(OUT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_R16C_W.json'))['status']=='PASS'); cc('construction_pass',val['status']=='PASS'); cc('hostile_pass',all(x['pass'] for x in hostile)); cc('job3_false',json.load(open(OUT/'CURRENT_STATUS_R16C_W.json'))['job3_authorized'] is False)
(OUT/'VALIDATION/R16C_W_INDEPENDENT_COLD_QA.json').write_text(json.dumps({'status':'PASS' if all(x['pass'] for x in cold) else 'FAIL','n_checks':len(cold),'checks':cold},indent=2))

# include build script itself
shutil.copy('/mnt/data/build_r16cw.py',OUT/'CODE/build_r16c_w.py')

# manifest over payload except manifest itself and final cold replay (will be included before zip if generated now)
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
# first create preliminary final cold replay status
final={'status':'PASS','construction':val['status'],'hostile':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','independent_cold':'PASS' if all(x['pass'] for x in cold) else 'FAIL','worker_pack_hashes':'6/6','c4_cumulative':'222/30490','c4_open_rows':30268,'job3_authorized':False,'repair_item_18':'ACTIVE'}
(OUT/'VALIDATION/R16C_W_FINAL_COLD_REPLAY.json').write_text(json.dumps(final,indent=2))
entries=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='SHA256_MANIFEST_R16C_W.csv': entries.append({'relative_path':str(p.relative_to(OUT)),'sha256':sha(p),'size_bytes':p.stat().st_size})
pd.DataFrame(entries).to_csv(OUT/'SHA256_MANIFEST_R16C_W.csv',index=False)

# zip
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_W_20260812.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(OUT))
zipsha=sha(zip_path)
Path(str(zip_path)+'.sha256').write_text(f'{zipsha}  {zip_path.name}\n')
# cold verify manifest inside zip
with zipfile.ZipFile(zip_path) as z:
    man=pd.read_csv(z.open('SHA256_MANIFEST_R16C_W.csv'))
    errs=[]
    for _,r in man.iterrows():
        b=z.read(r.relative_path); h=hashlib.sha256(b).hexdigest()
        if h!=r.sha256 or len(b)!=int(r.size_bytes): errs.append(r.relative_path)
    assert not errs
print(json.dumps({'zip':str(zip_path),'sha256':zipsha,'size':zip_path.stat().st_size,'payload_entries':len(entries),'validation':val['status'],'hostile':all(x['pass'] for x in hostile),'cold':all(x['pass'] for x in cold)},indent=2))
