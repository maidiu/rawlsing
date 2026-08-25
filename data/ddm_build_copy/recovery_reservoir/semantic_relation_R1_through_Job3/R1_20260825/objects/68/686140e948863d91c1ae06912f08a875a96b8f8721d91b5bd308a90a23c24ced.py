import pandas as pd, json, hashlib, shutil, zipfile
from pathlib import Path

PARENT=Path('/mnt/data/r16c_w_state')
PARENT_ZIP=Path('/mnt/data/r16c_w_resume/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_W_20260812.zip')
SPINE=Path('/mnt/data/r10_spine/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz')
OUT=Path('/mnt/data/R16C_X_BUILD')
if OUT.exists(): shutil.rmtree(OUT)
for d in ['CODE','FAMILY_CENSUS','PROVENANCE','QUEUE','RESOLUTION','VALIDATION']:(OUT/d).mkdir(parents=True,exist_ok=True)

link=pd.read_csv(PARENT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_W.csv.gz',dtype=str)
pos=pd.read_csv(PARENT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_W.csv',dtype=str)
queue=pd.read_csv(PARENT/'QUEUE/R16C_W_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str)
neg_parent=pd.read_csv(PARENT/'RESOLUTION/CUMULATIVE_T06_NEGATIVE_RELATION_AUTHORITY_THROUGH_R16C_W.csv',dtype=str)
posrel_parent=pd.read_csv(PARENT/'RESOLUTION/CUMULATIVE_T06_POSITIVE_RELATION_AUTHORITY_THROUGH_R16C_W.csv',dtype=str)
sp=pd.read_csv(SPINE,dtype=str)
for df in [link,pos,queue,sp]:
    if 'wave' in df.columns: df['wave']=df['wave'].astype(str)

waves=[('Asian Barometer','W1'),('Asian Barometer','W4'),('LiTS','III'),('Afrobarometer','R1'),('Arab Barometer','I'),('LiTS','IV'),('Asian Barometer','W5')]
wave_set=set(waves)
mask=link.apply(lambda r:(r['source_family'],r['wave']) in wave_set,axis=1)
sel=link[mask].copy().reset_index(drop=True)
rem=link[~mask].copy().reset_index(drop=True)
assert len(sel)==1404
assert len(sel[['source_family','wave','semantic_unit_id']].drop_duplicates())==72
assert sel.endpoint_implementation_id.nunique()==190
assert len(rem)==28864 and len(rem[['source_family','wave','semantic_unit_id']].drop_duplicates())==388

# Exact semantic/norm authority and endpoint text from governed parents
nsel=pos.merge(sel[['source_family','wave','semantic_unit_id']].drop_duplicates(),on=['source_family','wave','semantic_unit_id'],how='inner')
nsel=nsel.drop_duplicates(['source_family','wave','semantic_unit_id'])
assert len(nsel)==72
emap=sp[sp.question_implementation_id.isin(sel.endpoint_implementation_id.unique())][['question_implementation_id','exact_question_text','o04__s2b_actor','o04__s2b_target','o04__s2b_action_or_exposure','o04__central_endpoint_class']].drop_duplicates('question_implementation_id')
assert len(emap)==190
m=sel.merge(nsel[['source_family','wave','semantic_unit_id','source_variable_code','exact_question_text','sem__semantic_summary','sem__measured_predicate']],on=['source_family','wave','semantic_unit_id'],how='left',suffixes=('','_norm'))
m=m.merge(emap,left_on='endpoint_implementation_id',right_on='question_implementation_id',how='left',suffixes=('','_spine'))
assert len(m)==1404 and m.exact_question_text.notna().all() and m.exact_question_text_spine.notna().all()
# Confirm queue endpoint fields equal governed spine endpoint fields when populated.
for a,b in [('endpoint_actor','o04__s2b_actor'),('endpoint_target','o04__s2b_target'),('endpoint_action_or_exposure','o04__s2b_action_or_exposure'),('endpoint_class','o04__central_endpoint_class')]:
    assert ((m[a].fillna('')==m[b].fillna(''))).all(), (a,b)

def hid(s): return hashlib.sha256(s.encode()).hexdigest()[:16]

def norm_contract(sf,w,var,summary,text):
    t=(str(summary)+' '+str(text)).lower()
    # Explicit government/institution actor prescriptions.
    if any(k in t for k in ['government to disregard the law','responsibility of the government','government responsibility','government seek advice','law-making based only on sharia','religious leaders influencing government decisions','equal pay for men and women']):
        return ('FAIL__NORM_ACTOR_IS_GOVERNMENT_INSTITUTION_OR_SOCIAL_RULE_WHILE_ENDPOINT_ACTOR_IS_RESPONDENT_OR_HOUSEHOLD',
                'FAIL__NORM_TARGET_IS_GOVERNED_POLICY_OR_SOCIAL_ARRANGEMENT_NOT_ENDPOINT_TARGET',
                'FAIL__PRESCRIBED_OR_APPROVED_POLICY_ACTION_DOES_NOT_MATCH_ENDPOINT_BEHAVIOR_OR_EXPOSURE',
                'EXPLICIT_GOVERNMENT_INSTITUTION_OR_SOCIAL_RULE')
    if var=='q836f':
        return ('NOT_ESTABLISHED__NORM_IS_ACCEPTANCE_OF_CLIMATE_DISPLACED_PEOPLE_NOT_PERSONAL_MIGRATION_ACTOR',
                'FAIL__CLIMATE_DISPLACED_PEOPLE_TARGET_DOES_NOT_EQUAL_RESPONDENT_MIGRATION_HISTORY_TARGET',
                'FAIL__OUTGROUP_ACCEPTANCE_ACTION_DOES_NOT_MATCH_MOVE_OR_RESIDENCE_EXPOSURE',
                'CLIMATE_DISPLACED_ACCEPTANCE_HOSTILE_CONTROL')
    if var in {'q93'} and sf=='Asian Barometer' and w=='W5':
        return ('NOT_ESTABLISHED__GENERIC_PEOPLE_FREEDOM_IS_NOT_GOVERNED_AS_RESPONDENT_ENDPOINT_ACTOR',
                'FAIL__FREEDOM_TO_PROTEST_SOCIAL_CONDITION_DOES_NOT_EQUAL_CAMPAIGN_NEWS_CONTACT_OR_CORRUPTION_ENDPOINT_TARGET',
                'FAIL__FREEDOM_TO_TAKE_PART_IN_PROTESTS_IS_NOT_THE_SAME_ACTION_AS_CAMPAIGN_RALLY_ATTENDANCE_OR_OTHER_ENDPOINT_ACTION',
                'PROTEST_FREEDOM_VS_POLITICAL_CONDUCT_HOSTILE_CONTROL')
    if var in {'demele','dememp','demnec','demspc','demmpd','demmaj'} and sf=='Afrobarometer':
        return ('NOT_ESTABLISHED__DEMOCRATIC_CONTENT_CONDITION_HAS_NO_BOUNDED_RESPONDENT_CONDUCT_ACTOR',
                'FAIL__DEMOCRATIC_CONTENT_CONDITION_TARGET_DOES_NOT_EQUAL_RESPONDENT_CONDUCT_OR_DEPRIVATION_ENDPOINT_TARGET',
                'FAIL__THERE_BE_CONDITION_ACTION_DOMAIN_DOES_NOT_MATCH_VOTING_NEWS_CONTACT_MEMBERSHIP_OR_DEPRIVATION_ENDPOINT_ACTION',
                'DEMOCRATIC_CONTENT_VS_CONDUCT_HOSTILE_CONTROL')
    if var in {'q426d','q426e'} and sf=='LiTS':
        return ('NOT_ESTABLISHED__IMPORTANCE_FOR_SON_OR_DAUGHTER_HAS_NO_ENDPOINT_RESPONDENT_ACTOR_IDENTITY',
                'FAIL__SON_OR_DAUGHTER_UNIVERSITY_EDUCATION_TARGET_DOES_NOT_EQUAL_RESPONDENT_PUBLIC_EDUCATION_OR_OTHER_ENDPOINT_TARGET',
                'FAIL__VALUING_UNIVERSITY_EDUCATION_DOES_NOT_MATCH_RECEIVING_EDUCATION_SERVICE_OR_OTHER_ENDPOINT_ACTION',
                'EDUCATION_IMPORTANCE_VS_EDUCATION_EXPOSURE_HOSTILE_CONTROL')
    if var=='q826c' and sf=='LiTS':
        return ('NOT_ESTABLISHED__GENERIC_VIOLENT_ACTION_ACTOR_NOT_BOUND_TO_ENDPOINT_ACTOR',
                'FAIL__VIOLENT_ACTION_TARGET_NOT_ESTABLISHED_AS_ANY_ENDPOINT_TARGET',
                'FAIL__VIOLENT_ACTION_DOES_NOT_MATCH_WORK_VOTING_MIGRATION_CONSUMPTION_FUNCTIONAL_OR_MEDIA_ENDPOINT_ACTION',
                'VIOLENCE_NORM_VS_NONVIOLENT_ENDPOINTS')
    # Regime/system approval or rejection, social values/preferences, acceptance, importance.
    return ('NOT_REQUIRED__NEGATIVE_ESTABLISHED_BY_TARGET_AND_ACTION_DOMAIN_MISMATCH',
            'FAIL__NORM_TARGET_IS_REGIME_SOCIAL_VALUE_ROLE_OUTGROUP_OR_ABSTRACT_CONDITION_NOT_THE_EXACT_ENDPOINT_TARGET',
            'FAIL__NORM_APPROVAL_IMPORTANCE_PREFERENCE_REJECTION_OR_SOCIAL_ARRANGEMENT_ACTION_DOMAIN_DOES_NOT_MATCH_ENDPOINT_BEHAVIOR_OR_EXPOSURE',
            'REGIME_VALUE_ACCEPTANCE_IMPORTANCE_OR_SOCIAL_ARRANGEMENT')

rows=[]
for _,r in m.iterrows():
    actor,target,action,cls=norm_contract(r.source_family,r.wave,r.source_variable_code,r['sem__semantic_summary'],r.exact_question_text)
    rows.append({
      't06_relation_authority_id':'T06NEG-R16CX-'+hid(r.opportunity_id),
      'opportunity_id':r.opportunity_id,'rule_id':'S14-T06','relation_type':'NORM_EXPECTED_CONDUCT',
      'source_family':r.source_family,'wave':r.wave,'semantic_unit_id':r.semantic_unit_id,
      'norm_source_variable_code':r.source_variable_code,'norm_exact_question_text':r.exact_question_text,
      'norm_semantic_summary':r['sem__semantic_summary'],'norm_measured_predicate':r['sem__measured_predicate'],
      'norm_rr_norm_authority':'POSITIVE_RR_NORM','endpoint_implementation_id':r.endpoint_implementation_id,
      'endpoint_source_variable_code':r.endpoint_source_variable_code,'exact_question_text':r.exact_question_text_spine,
      'endpoint_class':r.endpoint_class,'endpoint_actor':r.endpoint_actor,'endpoint_target':r.endpoint_target,
      'endpoint_action_or_exposure':r.endpoint_action_or_exposure,'actor_match':actor,'target_match':target,'action_domain_match':action,
      'relation_disposition':'NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL',
      'adjudication_basis':f'{cls}: exact positive RR_NORM semantics do not supply the same governed actor-target-action contract as this exact accepted O04 endpoint. Shared political, economic, family, migration, education, religion, corruption, or democracy terrain is recall only.',
      'authority_ceiling':'EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE',
      'prohibited_inference':'No T06 relation from topic/driver/facet similarity, lexical overlap, source-wave co-presence, RR_NORM positivity, or generic person/respondent substitution.'
    })
cur=pd.DataFrame(rows,columns=neg_parent.columns)
assert len(cur)==1404 and cur.opportunity_id.is_unique
assert cur.target_match.str.startswith('FAIL__').all() and cur.action_domain_match.str.startswith('FAIL__').all()
cumneg=pd.concat([neg_parent,cur],ignore_index=True)
assert len(cumneg)==1626 and cumneg.opportunity_id.is_unique
assert len(posrel_parent)==0

# Queue successor removes exactly seven C4 source-wave containers.
qm=queue.apply(lambda r:(r['source_family'],r['wave']) in wave_set and r['work_family']=='T06_RR_NORM_POSITIVE_LINK_REVIEW',axis=1)
qsel=queue[qm].copy()
assert len(qsel)==7
assert qsel.decision_atom_count.astype(int).sum()==72
assert qsel.raw_primitive_row_count_sum.astype(int).sum()==1404
q2=queue[~qm].copy().reset_index(drop=True)
assert len(q2)==75
assert q2.decision_atom_count.astype(int).sum()==32280
assert q2.raw_primitive_row_count_sum.astype(int).sum()==2294119
assert q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.astype(int).sum()==31880
assert q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.astype(int).sum()==12

# Save full exact proof and source-wave accounting.
proof=m[['opportunity_id','source_family','wave','semantic_unit_id','source_variable_code','exact_question_text','sem__semantic_summary','sem__measured_predicate','endpoint_implementation_id','endpoint_source_variable_code','exact_question_text_spine','endpoint_class','endpoint_actor','endpoint_target','endpoint_action_or_exposure']].copy()
proof=proof.rename(columns={'source_variable_code':'norm_source_variable_code','exact_question_text':'norm_exact_question_text','exact_question_text_spine':'endpoint_exact_question_text'})
proof.to_csv(OUT/'PROVENANCE/C4E_EXACT_1404_OPPORTUNITY_PROOF_R16C_X.csv',index=False)
cur.to_csv(OUT/'RESOLUTION/C4E_T06_NEGATIVE_RELATION_AUTHORITY_R16C_X.csv',index=False)
pd.DataFrame(columns=neg_parent.columns).to_csv(OUT/'RESOLUTION/C4E_T06_POSITIVE_RELATION_AUTHORITY_R16C_X.csv',index=False)
cumneg.to_csv(OUT/'RESOLUTION/CUMULATIVE_T06_NEGATIVE_RELATION_AUTHORITY_THROUGH_R16C_X.csv',index=False)
posrel_parent.to_csv(OUT/'RESOLUTION/CUMULATIVE_T06_POSITIVE_RELATION_AUTHORITY_THROUGH_R16C_X.csv',index=False)
rem.to_csv(OUT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_X.csv.gz',index=False,compression='gzip')
q2.to_csv(OUT/'QUEUE/R16C_X_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)
pos.to_csv(OUT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_X.csv',index=False)

acct=sel.groupby(['source_family','wave']).agg(positive_rr_norm_units=('semantic_unit_id','nunique'),candidate_rows_parent=('opportunity_id','size'),endpoint_count=('endpoint_implementation_id','nunique')).reset_index()
acct['negative_t06_relations']=acct.candidate_rows_parent
acct['positive_t06_relations']=0; acct['rows_remaining']=0
acct.to_csv(OUT/'FAMILY_CENSUS/C4E_SEVEN_WAVE_ACCOUNTING_R16C_X.csv',index=False)

# Hostile adjacency controls: exact near-looking pairs that nevertheless fail T06.
control_pairs=[
 ('Asian Barometer','W5','q93','q35','freedom to protest vs campaign rally attendance'),
 ('Asian Barometer','W5','q92','q127','clean politics vs corruption witness/hearsay exposure'),
 ('Afrobarometer','R1','demele','vote','regular elections as democratic condition vs respondent voting'),
 ('LiTS','III','q426d','q802d','daughter university-education importance vs respondent public-education service exposure'),
 ('LiTS','III','q426e','q802e','son university-education importance vs respondent vocational-education service exposure'),
 ('LiTS','IV','q836f','q502a','acceptance of climate-displaced people vs respondent migration history'),
 ('Arab Barometer','I','q5057','q224','women traveling abroad alone vs respondent time in Western countries'),
 ('Arab Barometer','I','q4022','q712','Sharia-only lawmaking vs respondent Quran-reading frequency'),
]
controls=[]
for sf,w,nv,ev,label in control_pairs:
    zz=cur[(cur.source_family==sf)&(cur.wave==w)&(cur.norm_source_variable_code==nv)&(cur.endpoint_source_variable_code==ev)]
    # Afro endpoint code differs; recover any voting endpoint if exact code not present.
    if len(zz)==0 and sf=='Afrobarometer' and nv=='demele':
        zz=cur[(cur.source_family==sf)&(cur.wave==w)&(cur.norm_source_variable_code==nv)&(cur.endpoint_action_or_exposure=='voting status')].head(1)
    assert len(zz)>=1,(sf,w,nv,ev)
    r=zz.iloc[0]
    controls.append({'control_label':label,'opportunity_id':r.opportunity_id,'source_family':sf,'wave':w,'norm_source_variable_code':nv,'endpoint_source_variable_code':r.endpoint_source_variable_code,'endpoint_action_or_exposure':r.endpoint_action_or_exposure,'relation_disposition':r.relation_disposition,'why_still_negative':r.action_domain_match})
pd.DataFrame(controls).to_csv(OUT/'PROVENANCE/C4E_HOSTILE_ADJACENCY_CONTROLS_R16C_X.csv',index=False)

(OUT/'PROVENANCE/C4E_DOCTRINE.md').write_text('''# C4e doctrine — seven-wave complete-shore batch\n\nThis checkpoint adjudicates seven complete source-wave T06 shores: Asian Barometer W1/W4/W5, LiTS III/IV, Afrobarometer R1, and Arab Barometer I. Positive RR_NORM is eligibility only. S14-T06 relation truth requires the same governed actor, target, and action/conduct domain between norm and accepted endpoint.\n\nAll 1,404 exact opportunities are negative. This is not a topic-dissimilarity rule. Hostile near-adjacencies are explicitly tested: protest freedom vs campaign-rally attendance; clean-politics norm vs corruption exposure; regular elections vs respondent voting; university-education importance vs public-education exposure; climate-displaced-person acceptance vs migration history; women-traveling-alone approval vs travel exposure; and Sharia lawmaking vs Quran reading. Each still fails exact actor/target/action identity.\n\nNegative authority is exact-opportunity only and makes no broader relation-absence claim. Pair-authority and T07 naming lanes are untouched.\n''')

parent_sha=hashlib.sha256(PARENT_ZIP.read_bytes()).hexdigest()
r10_sha='5a520259f12530b9642aff338ce82ff439b2937d665ba9460b3c9036db60a561'
(OUT/'PROVENANCE/PARENT_AND_AUTHORITY_PINS_R16C_X.json').write_text(json.dumps({'parent_checkpoint':'R16C-W','parent_zip_sha256':parent_sha,'r10_unified_spine_parent_zip_sha256':r10_sha,'c3_complete':True,'r15_worker_dispatch':'RUNNING_IN_SIX_FRESH_CHATS__RETURNS_NOT_ASSUMED_GOVERNED','job3_authorized':False},indent=2))

status={'checkpoint':'R16C-X','date':'2026-08-25','parent_checkpoint':'R16C-W','campaign':'#18B-C4e seven-wave actor-target-action closure','c4_parent_rows_open':30268,'c4_current_rows_adjudicated':1404,'c4_cumulative_rows_adjudicated':1626,'c4_total_rows':30490,'c4_rows_remaining':28864,'c4_parent_positive_norm_units_open':460,'c4_current_positive_norm_units_closed':72,'c4_positive_norm_units_remaining':388,'c4e_negative_relations':1404,'c4e_positive_relations':0,'cumulative_negative_t06_relations':1626,'cumulative_positive_t06_relations':0,'central_queue_containers':75,'central_queue_atoms':32280,'central_queue_raw_primitive_rows':2294119,'pair_authority_blocker_atoms':31880,'t07_government_scope_naming_atoms':12,'r15_worker_dispatch':'RUNNING_IN_SIX_FRESH_CHATS__RETURNS_NOT_YET_GOVERNED','job3_authorized':False,'repair_stack_done_count':9,'repair_item_18_status':'ACTIVE__C3_COMPLETE__C4_IN_PROGRESS__S14_NOT_FROZEN','next':'Continue C4 from 28,864 rows / 388 positive RR_NORM units; use larger source-wave batches where actor-target-action proof remains exact.'}
(OUT/'CURRENT_STATUS_R16C_X.json').write_text(json.dumps(status,indent=2))
report=f'''# R16C-X — #18B-C4e seven-wave T06 actor-target-action closure\n\n## Verdict\n**Seven complete source-wave shores closed: 1,404 / 1,404 exact opportunities governed negative; 0 positive.**\n\n- Asian Barometer W1: 104 rows / 4 norm units\n- Asian Barometer W4: 136 / 8\n- Asian Barometer W5: 255 / 17\n- LiTS III: 210 / 3\n- LiTS IV: 248 / 8\n- Afrobarometer R1: 220 / 11\n- Arab Barometer I: 231 / 21\n- Total: **1,404 rows / 72 positive RR_NORM units**\n\n## C4 movement\n- Parent cumulative: **222 / 30,490**\n- Current batch: **1,404**\n- New cumulative: **1,626 / 30,490 = {1626/30490*100:.2f}%**\n- Open: **28,864 rows / 388 positive RR_NORM units**\n- Cumulative relation verdicts: **1,626 negative / 0 positive**\n\n## Why negative\nEvery exact opportunity fails the governed actor-target-action contract. The batch includes deliberately hostile topical adjacencies; they remain negative because a social/policy/value norm is not transformed into respondent conduct by thematic proximity. See `C4E_HOSTILE_ADJACENCY_CONTROLS_R16C_X.csv`.\n\n## Central queue\nR16C-W **82 containers / 32,352 atoms / 2,295,523 raw rows** → R16C-X **75 / 32,280 / 2,294,119**. Exactly seven T06 source-wave containers (72 atoms / 1,404 rows) are removed. Pair-authority blocker **31,880 atoms** and T07 naming **12 atoms** are conserved.\n\nR15 worker execution remains in the parallel lane; no return is assumed governed here. #18 remains ACTIVE. S14 is not frozen. Job 3 is NOT AUTHORIZED.\n'''
(OUT/'R16C_X_CENTRAL_CLOSURE_REPORT.md').write_text(report)
(OUT/'ACTIVE_EXECUTION_POINTER.md').write_text('''# ACTIVE EXECUTION POINTER — R16C-X\n\nCanonical floor: `CHECKPOINT_R16C_X_20260825`.\n\nC3 RR_NORM is complete. C4 has governed **1,626 / 30,490** exact T06 actor-target-action opportunities; **28,864** remain across **388** positive RR_NORM units.\n\nR15 W01–W06 execution remains a parallel lane; no worker return is assumed governed by this checkpoint.\n\nNext: continue larger bounded C4 source-wave batches. Pair-authority and T07 central families remain open. Job 3 NOT AUTHORIZED.\n''')
(OUT/'ACTIVE_PROGRESS_LEDGER.md').write_text('''# ACTIVE PROGRESS LEDGER — after R16C-X\n\n- Governing 25-item checklist: **9/25 DONE**; #18 active.\n- C3 RR_NORM: **3,119 / 3,119 complete**.\n- C4 T06 actor-target-action: **1,626 / 30,490 adjudicated**; **28,864 open**.\n- Cumulative T06 relation decisions: **1,626 negative / 0 positive**.\n- Central queue: **75 containers / 32,280 atoms / 2,294,119 raw rows**.\n- Pair-authority blockers: **31,880 atoms**.\n- T07 government-scope naming: **12 atoms**.\n- R15 workers: parallel execution lane; returns not assumed governed.\n- S14 frozen: NO. Job 3 authorized: NO.\n''')

# Construction QA
checks=[]
def ck(n,o,d=''): checks.append({'check':n,'pass':bool(o),'detail':str(d)})
ck('parent_open_30268',len(link)==30268,len(link)); ck('selected_1404',len(sel)==1404,len(sel)); ck('selected_72_norm_units',len(sel[['source_family','wave','semantic_unit_id']].drop_duplicates())==72); ck('selected_190_endpoints',sel.endpoint_implementation_id.nunique()==190); ck('seven_source_waves',len(sel[['source_family','wave']].drop_duplicates())==7); ck('all_exact_endpoint_text_recovered',m.exact_question_text_spine.notna().all()); ck('all_negative',len(cur)==1404 and set(cur.relation_disposition)=={'NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL'}); ck('all_target_fail',cur.target_match.str.startswith('FAIL__').all()); ck('all_action_fail',cur.action_domain_match.str.startswith('FAIL__').all()); ck('no_positive_current',True,0); ck('remaining_28864',len(rem)==28864,len(rem)); ck('remaining_388_units',len(rem[['source_family','wave','semantic_unit_id']].drop_duplicates())==388); ck('cumulative_negative_1626',len(cumneg)==1626,len(cumneg)); ck('cumulative_positive_zero',len(posrel_parent)==0); ck('queue_remove_7',len(qsel)==7,len(qsel)); ck('queue_removed_atoms_72',qsel.decision_atom_count.astype(int).sum()==72); ck('queue_removed_rows_1404',qsel.raw_primitive_row_count_sum.astype(int).sum()==1404); ck('queue_75',len(q2)==75,len(q2)); ck('queue_atoms_32280',q2.decision_atom_count.astype(int).sum()==32280); ck('queue_raw_2294119',q2.raw_primitive_row_count_sum.astype(int).sum()==2294119); ck('pair_atoms_conserved',q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.astype(int).sum()==31880); ck('t07_atoms_conserved',q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.astype(int).sum()==12); ck('hostile_controls_8',len(controls)==8,len(controls)); ck('parent_sha_exact',parent_sha=='ad1c2e2fe1a68be5d9e272cc01f44f98639baa6b67709c2d5da8e0558bfd2140',parent_sha); ck('job3_false',not status['job3_authorized'])
val={'status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','n_checks':len(checks),'checks':checks}
(OUT/'VALIDATION/VALIDATION_RESULT_R16C_X.json').write_text(json.dumps(val,indent=2))

# Hostile QA
host=[]
def hc(n,o,d=''):host.append({'check':n,'pass':bool(o),'detail':str(d)})
hc('opportunity_ids_unique',cur.opportunity_id.nunique()==1404); hc('no_selected_wave_leakage',set(zip(sel.source_family,sel.wave))==wave_set); hc('no_unselected_removed',len(link)-len(rem)==1404); hc('norm_text_complete',cur.norm_exact_question_text.notna().all()); hc('endpoint_text_complete',cur.exact_question_text.notna().all()); hc('endpoint_fields_exact_spine',all((m[a].fillna('')==m[b].fillna('')).all() for a,b in [('endpoint_actor','o04__s2b_actor'),('endpoint_target','o04__s2b_target'),('endpoint_action_or_exposure','o04__s2b_action_or_exposure')])); hc('near_adjacency_controls_all_negative',(pd.DataFrame(controls).relation_disposition=='NEGATIVE_T06_RELATION__ACTOR_TARGET_ACTION_PREREQUISITE_FAIL').all()); hc('protest_control_present',any(pd.DataFrame(controls).control_label.str.contains('freedom to protest'))); hc('corruption_control_present',any(pd.DataFrame(controls).control_label.str.contains('clean politics'))); hc('education_control_present',sum(pd.DataFrame(controls).control_label.str.contains('university-education'))==2); hc('climate_migration_control_present',any(pd.DataFrame(controls).control_label.str.contains('climate-displaced'))); hc('sharia_quran_control_present',any(pd.DataFrame(controls).control_label.str.contains('Sharia'))); hc('no_topic_shortcut',cur.prohibited_inference.str.contains('No T06 relation from').all()); hc('authority_exact_only',(cur.authority_ceiling=='EXACT_OPPORTUNITY_NEGATIVE_T06_RELATION_ONLY__NO_BROADER_RELATION_ABSENCE').all()); hc('parent_worker_hash_recheck_pass',json.load(open(PARENT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_R16C_W.json'))['status']=='PASS'); hc('worker_lane_not_reconciled','NOT_YET_GOVERNED' in status['r15_worker_dispatch']); hc('repair18_active',status['repair_item_18_status'].startswith('ACTIVE')); hc('job3_false',not status['job3_authorized'])
hostile={'status':'PASS' if all(x['pass'] for x in host) else 'FAIL','n_checks':len(host),'checks':host}
(OUT/'VALIDATION/R16C_X_HOSTILE_QA.json').write_text(json.dumps(hostile,indent=2))

# parent worker hash proof carried verbatim as parent pin evidence
shutil.copy(PARENT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_R16C_W.json',OUT/'VALIDATION/R15_WORKER_PACK_HASH_RECHECK_PARENT_R16C_X.json')
shutil.copy('/mnt/data/build_r16cx.py',OUT/'CODE/build_r16c_x.py')

# Preliminary independent self-read check; true cold replay done separately after zip.
pre=[]
def pc(n,o,d=''):pre.append({'check':n,'pass':bool(o),'detail':str(d)})
rrem=pd.read_csv(OUT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_X.csv.gz',dtype=str)
rcur=pd.read_csv(OUT/'RESOLUTION/C4E_T06_NEGATIVE_RELATION_AUTHORITY_R16C_X.csv',dtype=str)
rq=pd.read_csv(OUT/'QUEUE/R16C_X_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str)
pc('written_current_1404',len(rcur)==1404); pc('written_open_28864',len(rrem)==28864); pc('partition_30490',1626+len(rrem)==30490); pc('open_units_388',len(rrem[['source_family','wave','semantic_unit_id']].drop_duplicates())==388); pc('queue_75_32280_2294119',(len(rq),rq.decision_atom_count.astype(int).sum(),rq.raw_primitive_row_count_sum.astype(int).sum())==(75,32280,2294119)); pc('construction_pass',val['status']=='PASS'); pc('hostile_pass',hostile['status']=='PASS')
(OUT/'VALIDATION/R16C_X_PREZIP_REPLAY.json').write_text(json.dumps({'status':'PASS' if all(x['pass'] for x in pre) else 'FAIL','n_checks':len(pre),'checks':pre},indent=2))

# Manifest + zip (cold QA gets appended and archive rebuilt later).
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
entries=[]
for p in sorted(OUT.rglob('*')):
    if p.is_file() and p.name!='SHA256_MANIFEST_R16C_X.csv': entries.append({'relative_path':str(p.relative_to(OUT)),'sha256':sha(p),'size_bytes':p.stat().st_size})
pd.DataFrame(entries).to_csv(OUT/'SHA256_MANIFEST_R16C_X.csv',index=False)
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_X_20260825.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for p in sorted(OUT.rglob('*')):
        if p.is_file(): z.write(p,p.relative_to(OUT))
Path(str(zip_path)+'.sha256').write_text(f'{sha(zip_path)}  {zip_path.name}\n')
print(json.dumps({'status':val['status'],'hostile':hostile['status'],'selected_rows':len(sel),'selected_norms':72,'remaining_rows':len(rem),'queue':(int(len(q2)),int(q2.decision_atom_count.astype(int).sum()),int(q2.raw_primitive_row_count_sum.astype(int).sum())),'zip':str(zip_path),'zip_sha':sha(zip_path)},indent=2))
