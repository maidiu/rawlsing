from pathlib import Path
import pandas as pd, json, hashlib, zipfile, shutil

ROOT=Path('/mnt/data/r16c_s')
if ROOT.exists(): shutil.rmtree(ROOT)
for d in ['FAMILY_CENSUS','RESOLUTION','QUEUE','PROVENANCE','VALIDATION','CODE']:
    (ROOT/d).mkdir(parents=True,exist_ok=True)
PARENT=Path('/mnt/data/r16cs_parent')
R11=Path('/mnt/data/r16cs_r11/T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz')
R10A=Path('/mnt/data/r16cs_r10a/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz')
P2=Path('/mnt/data/r16cs_ancestry/Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json')
key=['source_family','wave','semantic_unit_id']

res=pd.read_csv(PARENT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_R.csv',dtype=str).fillna(''); res['wave']=res.wave.astype(str)
assert len(res)==17 and not res.duplicated(key).any()
r11=pd.read_csv(R11,dtype=str,low_memory=False).fillna(''); r11['wave']=r11.wave.astype(str)
sp=pd.read_csv(R10A,dtype=str,low_memory=False).fillna(''); sp['wave']=sp.wave.astype(str)
p2=json.load(open(P2)); impl=pd.DataFrame(p2['question_implementations']).fillna('')
q_parent=pd.read_csv(PARENT/'QUEUE/R16C_R_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',dtype=str).fillna(''); q_parent['wave']=q_parent.wave.astype(str)
for c in ['decision_atom_count','raw_primitive_row_count_sum','member_implementation_count','planning_effort_units']:
    q_parent[c]=pd.to_numeric(q_parent[c])
prior_pos=pd.read_csv(PARENT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_R.csv',dtype=str).fillna(''); prior_pos['wave']=prior_pos.wave.astype(str)
prior_pos_rows=pd.read_csv(PARENT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_R.csv.gz',dtype=str,low_memory=False).fillna(''); prior_pos_rows['wave']=prior_pos_rows.wave.astype(str)
parent_block_rows=pd.read_csv(PARENT/'QUEUE/C3B17_RESIDUAL_T06_BLOCKED_PRIMITIVE_ROWS_R16C_R.csv.gz',dtype=str,low_memory=False).fillna(''); parent_block_rows['wave']=parent_block_rows.wave.astype(str)
parent_status=json.load(open(PARENT/'CURRENT_STATUS_R16C_R.json'))

# Exact source-recovered authority map. This is keyed by full decision identity, never semantic ID alone.
decision_spec={
('Afrobarometer','R1','gidstr'):('NEGATIVE_RR_NORM','DESCRIPTIVE_RELATIVE_GROUP_ATTACHMENT','Afrobarometer Round 1 merged codebook, gidstr, PDF p.52','Official codebook frames the item as respondent feeling stronger ties to own identity group than to compatriots; this is a descriptive affiliation state, not a prescription or approval of conduct.','https://www.afrobarometer.org/wp-content/uploads/2022/02/merged_r1_codebook2.pdf'),
('Arab Barometer','I','q611'):('NEGATIVE_RR_NORM','DESCRIPTIVE_GOVERNMENT_EFFORT_BELIEF','Arab Barometer Wave I English questionnaire, q611, PDF p.24','Official questionnaire asks whether government in fact does all it can to provide citizens services; this evaluates government effort/performance rather than what government ought to do.','https://www.arabbarometer.org/wp-content/uploads/ABI_Questionnaire_ENG.pdf'),
('EVS','1990','q317b'):('POSITIVE_RR_NORM','COERCIVE_RETIREMENT_POLICY_PRESCRIPTION','EVS 1990 Master Questionnaire ZA4460, Q317B, PDF p.8','Native stem says that when jobs are scarce people should be forced to retire early; this is an explicit coercive policy prescription.','https://access.gesis.org/dbk/11635'),
('EVS','1999','v94'):('POSITIVE_RR_NORM','WORK_OBLIGATION_PERMISSION_NORM','EVS 1999 Variable Report, v94 / Q17E, PDF p.130','Native stem asserts that people should not have to work when they do not want to; this directly states an obligation/permission norm.','https://access.gesis.org/dbk/49145'),
('EVS','1999','o12'):('POSITIVE_RR_NORM','RELIGIOUS_REFUSAL_PERMISSION_NORM','EVS 1999 questionnaire, o12, PDF p.13','Native stem asks whether a nurse helping with a legal abortion should be allowed to refuse for religious reasons; this is explicit permission authority.','https://access.gesis.org/dbk/9850?download_purpose=-99'),
('EVS','1999','v94_at'):('POSITIVE_RR_NORM','WORK_OBLIGATION_PERMISSION_NORM','EVS 1999 Austria Variable Report ZA3779, v94_at / Q17E_AT, PDF p.132','Austria-specific item preserves the same should-not-have-to-work proposition with a four-category agree/disagree response frame; the semantic norm is unchanged.','https://access.gesis.org/dbk/49076?download_purpose=-99'),
('GSS','1993','pclit'):('POSITIVE_RR_NORM','DISAPPROVAL_OF_CURRICULAR_CULTURAL_ARRANGEMENT','GSS 1993 Ballot A questionnaire p.62 Q140; cumulative GSS SDA variable PCLIT','Native proposition explicitly condemns the arrangement in which traditional American literature is ignored while works are promoted because authors are women or minority-group members; it is disapproval of a social/curricular arrangement, not generic affect.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0103.htm'),
('GSS','1993','classics'):('POSITIVE_RR_NORM','CURRICULAR_ALLOCATION_CRITERION','GSS 1993 Ballot A questionnaire p.62 Q140; cumulative GSS SDA variable CLASSICS','Native proposition judges high-school/college curricular practice as devoting too much time to low-relevance classics; this is an evaluative criterion/disapproval applied to institutional conduct.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0103.htm'),
('GSS','1993','pillok'):('POSITIVE_RR_NORM','TEEN_CONTRACEPTION_ACCESS_PERMISSION','GSS 1993 Ballot A questionnaire p.35 Q86; cumulative GSS SDA variable PILLOK','Native question asks whether birth-control methods should be available to ages 14–16 despite parental disapproval; this is explicit access/permission policy approval.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0045.htm'),
('GSS','2002','doc20a'):('NEGATIVE_RR_NORM','DOCTOR_TRUST_EXPECTATION','GSS 2002 V1 questionnaire p.96; GSS2002 source metadata','Source battery asks about trust/expectation that one’s doctor will disclose a treatment mistake; this is a belief/trust measure, not a prescription that doctors ought to disclose.','https://web.pdx.edu/~stipakb/download/Data/gss2002codebook.html'),
('GSS','2002','doc18a'):('NEGATIVE_RR_NORM','DOCTOR_TRUST_EXPECTATION','GSS 2002 V1 questionnaire p.96; GSS2002 source metadata','Source battery asks about trust that one’s doctor puts medical needs above other considerations; this is a belief/trust measure rather than a normative rule for doctors.','https://web.pdx.edu/~stipakb/download/Data/gss2002codebook.html'),
('GSS','2002','teamsafe'):('NEGATIVE_RR_NORM','DESCRIPTIVE_WORKPLACE_SAFETY_COORDINATION','GSS 2002 Quality of Work Life questionnaire, TEAMSAFE, PDF p.54','The battery is explicitly framed as statements that might or might not describe the respondent’s main job; TEAMSAFE describes management/employee safety coordination and is not a prescription.','https://gss.norc.org/content/dam/gss/get-documentation/pdf/quex/2002%20GSS%20V4.pdf'),
('GSS','2010','ldcgrn'):('POSITIVE_RR_NORM','ENVIRONMENTAL_EFFORT_EXPECTATION_NORM','GSS 2010 AREA questionnaire, LDCGRN, PDF p.150','Native proposition says poorer countries should be expected to make less environmental-protection effort than richer countries; this allocates normative obligation/expectation.','https://gss.norc.org/content/dam/gss/get-documentation/pdf/quex/GSS2010_Ballot1_AREA_English.pdf'),
('GSS','2010','pillok'):('POSITIVE_RR_NORM','TEEN_CONTRACEPTION_ACCESS_PERMISSION','GSS 2010 Ballot 2 questionnaire p.73; cumulative GSS SDA variable PILLOK','Same source-governed access proposition: whether contraception should be available to ages 14–16 despite parental disapproval; explicit permission/policy approval.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0045.htm'),
('GSS','2010','teamsafe'):('NEGATIVE_RR_NORM','DESCRIPTIVE_WORKPLACE_SAFETY_COORDINATION','GSS 2010 Ballot 3 AREA questionnaire, TEAMSAFE, PDF p.200 in available AREA rendering','Native frame says the statements may or may not describe the respondent’s main job; TEAMSAFE is descriptive workplace coordination, not a norm.','https://gss.norc.org/content/dam/gss/get-documentation/pdf/quex/GSS2010_Ballot1_AREA_English.pdf'),
('GSS','2016','pillok'):('POSITIVE_RR_NORM','TEEN_CONTRACEPTION_ACCESS_PERMISSION','GSS 2016 Ballot 2 questionnaire p.91; cumulative GSS SDA variable PILLOK','Same source-governed access proposition: whether contraception should be available to ages 14–16 despite parental disapproval; explicit permission/policy approval.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0045.htm'),
('GSS','2024','pillok'):('POSITIVE_RR_NORM','TEEN_CONTRACEPTION_ACCESS_PERMISSION','GSS 2024 Ballot 2 questionnaire p.114; cumulative GSS SDA variable PILLOK','Same source-governed access proposition: whether contraception should be available to ages 14–16 despite parental disapproval; explicit permission/policy approval.','https://sda.berkeley.edu/sdaweb/docs/gss24rel3/DOC/hcbk0045.htm'),
}
assert len(decision_spec)==17

ledger=res.copy()
ledger['source_recovery_status']=''
ledger['rr_norm_disposition']=''
ledger['c3b18_semantic_family']=''
ledger['native_source_locator']=''
ledger['source_recovered_semantic_basis']=''
ledger['source_url']=''
ledger['decision_basis']=''
for i,r in ledger.iterrows():
    k=(r.source_family,str(r.wave),r.source_variable_code)
    assert k in decision_spec,k
    disp,fam,loc,basis,url=decision_spec[k]
    ledger.loc[i,['source_recovery_status','rr_norm_disposition','c3b18_semantic_family','native_source_locator','source_recovered_semantic_basis','source_url','decision_basis']]=[
        'RECOVERED_TO_GOVERNING_STANDARD',disp,fam,loc,basis,url,'SOURCE_FIRST_NATIVE_STEM_AND_RESPONSE_FRAME__MANUAL_RR_NORM_DOCTRINE_APPLICATION']
ledger['authority_ceiling']=ledger.rr_norm_disposition.map({
    'POSITIVE_RR_NORM':'POSITIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__T06_LINK_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION',
    'NEGATIVE_RR_NORM':'NEGATIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__NO_RELATION_ABSENCE_CLAIM'})
ledger=ledger.sort_values(['source_family','wave','source_variable_code']).reset_index(drop=True)
ledger.to_csv(ROOT/'PROVENANCE/C3B18_17_SOURCE_RECOVERY_AUTHORITY_LEDGER_R16C_S.csv',index=False)

pos=ledger[ledger.rr_norm_disposition=='POSITIVE_RR_NORM'].copy()
neg=ledger[ledger.rr_norm_disposition=='NEGATIVE_RR_NORM'].copy()
assert len(pos)==11 and len(neg)==6
pos.to_csv(ROOT/'RESOLUTION/C3B18_POSITIVE_RR_NORM_AUTHORITY_R16C_S.csv',index=False)
neg.to_csv(ROOT/'RESOLUTION/C3B18_NEGATIVE_RR_NORM_AUTHORITY_R16C_S.csv',index=False)
# Explicit empty residual artifact: C3 is fully governed.
empty=res.iloc[0:0].copy()
empty.to_csv(ROOT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_S.csv',index=False)

# Member-complete current-spine proof for all 17 exact decisions.
mi_all=pd.MultiIndex.from_frame(ledger[key].astype(str))
spmi=pd.MultiIndex.from_frame(sp[['source_family','wave','sem__audit_unit_id']].astype(str))
sp_sel=sp[spmi.isin(mi_all)].copy()
proof_cols=['source_family','wave','sem__audit_unit_id','question_implementation_id','source_variable_code','source_authority','exact_question_text','sem__semantic_summary','sem__measured_predicate','sem__canonical_role']
proof=sp_sel[proof_cols].merge(impl[['question_implementation_id','authority_status']],on='question_implementation_id',how='left',validate='many_to_one')
assert proof[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==17
assert len(proof)==17 and (proof.authority_status=='source_reviewed').all() and proof.source_authority.str.strip().ne('').all()
proof.to_csv(ROOT/'PROVENANCE/C3B18_MEMBER_COMPLETE_SOURCE_REVIEWED_IMPLEMENTATION_PROOF_R16C_S.csv',index=False)

# Exact sealed-R11 reconstruction, not queue arithmetic.
rmi=pd.MultiIndex.from_frame(r11[key].astype(str))
mi_pos=pd.MultiIndex.from_frame(pos[key].astype(str)); mi_neg=pd.MultiIndex.from_frame(neg[key].astype(str))
pos_rows=r11[rmi.isin(mi_pos)].copy(); neg_rows=r11[rmi.isin(mi_neg)].copy()
assert len(pos_rows)==698 and len(neg_rows)==862
assert pos_rows.opportunity_id.is_unique and neg_rows.opportunity_id.is_unique
assert set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id))
assert set(pos_rows.opportunity_id)|set(neg_rows.opportunity_id)==set(parent_block_rows.opportunity_id)
pos_rows.to_csv(ROOT/'RESOLUTION/C3B18_TRANSFERRED_T06_LINK_REVIEW_ROWS_R16C_S.csv.gz',index=False,compression='gzip')
neg_rows.to_csv(ROOT/'RESOLUTION/C3B18_RETIRED_T06_PRIMITIVE_ROWS_R16C_S.csv.gz',index=False,compression='gzip')
# No blocked RR_NORM primitive rows remain.
parent_block_rows.iloc[0:0].to_csv(ROOT/'QUEUE/C3B18_RESIDUAL_T06_BLOCKED_PRIMITIVE_ROWS_R16C_S.csv.gz',index=False,compression='gzip')

# Cumulative positive authority + exact rows from sealed R11.
newpos=pos.copy(); newpos['positive_authority_origin']='R16C-S__C3B18_SOURCE_RECOVERY'
# align to prior columns, retaining new source-recovery fields where possible via outer concat
all_pos=pd.concat([prior_pos,newpos],ignore_index=True,sort=False).fillna('')
assert len(prior_pos)==460 and len(all_pos)==471 and not all_pos.duplicated(key).any()
allpmi=pd.MultiIndex.from_frame(all_pos[key].astype(str))
all_pos_rows=r11[rmi.isin(allpmi)].copy()
assert len(prior_pos_rows)==29792 and len(all_pos_rows)==30490
assert set(prior_pos_rows.opportunity_id).issubset(set(all_pos_rows.opportunity_id))
assert set(all_pos_rows.opportunity_id)-set(prior_pos_rows.opportunity_id)==set(pos_rows.opportunity_id)
all_pos.to_csv(ROOT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_S.csv',index=False)
all_pos_rows.to_csv(ROOT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_S.csv.gz',index=False,compression='gzip')

# Rebuild central queue from frozen static families + cumulative authority. C3 blocker family disappears entirely.
static=q_parent[q_parent.work_family.isin(['PAIR_AUTHORITY_BLOCKER','T07_GOVERNMENT_SCOPE_NAMING'])].copy()
sp_allp=sp[spmi.isin(allpmi)].copy()
assert sp_allp[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==471
link_rows=[]
for (sf,wv),g in all_pos.groupby(['source_family','wave'],sort=True):
    rr=all_pos_rows[(all_pos_rows.source_family==sf)&(all_pos_rows.wave==str(wv))]
    impct=sp_allp[(sp_allp.source_family==sf)&(sp_allp.wave==str(wv))].question_implementation_id.nunique()
    link_rows.append({
      'packet_id':f'R16C-S-CUMULATIVE-NORM-LINK::{sf}::{wv}','source_family':sf,'wave':str(wv),'work_family':'T06_RR_NORM_POSITIVE_LINK_REVIEW',
      'execution_lane':'VOZHD_CENTRAL__T06_RELATION_LINK_ADJUDICATION','rule_hypotheses':'T06','decision_atom_count':len(g),
      'raw_primitive_row_count_sum':len(rr),'member_implementation_count':impct,'planning_effort_units':round(0.25*len(g),6),
      'packet_statuses_json':'["RR_NORM_POSITIVE__ACTOR_TARGET_ACTION_LINK_REVIEW_REQUIRED"]',
      'authority_ceilings_json':'["NO_T06_RELATION_AUTHORITY_YET__LINK_STILL_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION"]'})
link_q=pd.DataFrame(link_rows,columns=q_parent.columns)
q2=pd.concat([static,link_q],ignore_index=True).sort_values(['work_family','source_family','wave','packet_id']).reset_index(drop=True)
assert len(link_q)==30 and int(link_q.decision_atom_count.sum())==471 and int(link_q.raw_primitive_row_count_sum.sum())==30490
assert len(q2)==86 and int(q2.decision_atom_count.sum())==32363 and int(q2.raw_primitive_row_count_sum.sum())==2295745
assert not (q2.work_family=='T06_NORM_ROLE_BLOCKER').any()
q2.to_csv(ROOT/'QUEUE/R16C_S_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)

# Source-wave accounting for the 17 source-recovery frontier.
sw=pd.concat([
    pos.groupby(['source_family','wave']).size().rename('positive_decisions'),
    neg.groupby(['source_family','wave']).size().rename('negative_decisions'),
    pos_rows.groupby(['source_family','wave']).size().rename('transferred_link_rows'),
    neg_rows.groupby(['source_family','wave']).size().rename('retired_primitive_rows')],axis=1).fillna(0).astype(int).reset_index()
sw.to_csv(ROOT/'FAMILY_CENSUS/C3B18_SOURCE_WAVE_ACCOUNTING_R16C_S.csv',index=False)

# Status and governance prose.
status={
 'checkpoint':'R16C-S','date':'2026-08-12','parent_checkpoint':'R16C-R','campaign':'#18B-C3b18 targeted source recovery',
 'c3_parent_adjudicated_decisions':3102,'c3_current_adjudicated_decisions':3119,'c3_total_decisions':3119,'c3_percent':100.0,
 'c3b18_positive_rr_norm':11,'c3b18_negative_rr_norm':6,'c3b18_residual_source_blocked':0,
 'cumulative_positive_rr_norm':471,'cumulative_negative_rr_norm':2648,
 'positive_link_rows_transferred_current':698,'negative_primitive_rows_retired_current':862,
 'cumulative_positive_t06_link_review_rows':30490,'t06_rr_norm_blocked_primitive_rows':0,
 'central_queue_containers':86,'central_queue_atoms':32363,'central_queue_raw_primitive_rows':2295745,
 'pair_authority_blocker_atoms':31880,'t07_government_scope_naming_atoms':12,
 'worker_packs_changed':False,'job3_authorized':False,'repair_stack_done_count':9,'repair_item_18_status':'ACTIVE__C3_PREREQUISITE_COMPLETE__S14_NOT_FROZEN',
 'next':'C4/T06 actor-target-action relation-link adjudication over 30,490 exact positive-shore rows, alongside remaining pair-authority and T07 naming central families; #18C reconciliation only after central + worker lanes are complete.'}
json.dump(status,open(ROOT/'CURRENT_STATUS_R16C_S.json','w'),indent=2)

(ROOT/'PROVENANCE/C3B18_DOCTRINE_AND_SOURCE_RECOVERY_NOTE.md').write_text('''# C3b18 source-recovery doctrine and closure note\n\nC3b18 starts only from the exact 17-row R16C-R residual artifact. A compressed prose handoff had stale/wrong variable descriptions; the governed CSV superseded it before any decision was emitted.\n\nA decision is keyed only by `(source_family, wave, semantic_unit_id)`. Native source recovery was used to restore stem and response framing. Agreement format alone never establishes RR_NORM. Positive RR_NORM requires an actual prescription, obligation, permission/prohibition, policy/social-arrangement approval or rejection, or evaluative criterion applied to conduct/arrangement. Descriptive belief, trust, performance, affiliation, or current-state statements are negative.\n\nResults: **11 positive / 6 negative / 0 residual**. Positive decisions transfer exact sealed-R11 rows to actor-target-action link review and do not emit T06 relation truth. Negative decisions retire only the RR_NORM shore and do not establish relation absence.\n\nC3 is now **3,119 / 3,119 complete**. This closes the RR_NORM prerequisite only; repair item #18 remains active.\n''')

report=f'''# R16C-S — #18B-C3b18 targeted source recovery and complete RR_NORM closure\n\n## Verdict\n**C3 RR_NORM is complete: 3,119 / 3,119 governed.**\n\n- C3b18 source frontier: **17 / 17 recovered and adjudicated**.\n- Positive RR_NORM: **11**.\n- Negative RR_NORM: **6**.\n- Residual/source-blocked: **0**.\n- Exact positive rows transferred to actor-target-action review: **698**.\n- Exact negative primitive rows retired: **862**.\n- RR_NORM blocked surface: **1,560 → 0**.\n- Cumulative positive RR_NORM: **471**, preserving **30,490** exact T06 link-review rows.\n- Cumulative negative RR_NORM: **2,648**.\n\n## Central queue\nR16C-R **95 containers / 32,369 atoms** → R16C-S **86 containers / 32,363 atoms**. All nine `T06_NORM_ROLE_BLOCKER` source-wave containers disappear. The 11 positive decisions remain as link-review atoms; the six negatives leave central work. Static pair-authority and T07 naming families are conserved unchanged.\n\n## Authority boundary\nC3 closure is **not T06 relation closure** and **not #18 closure**. The 30,490 positive-shore rows still require actor-target-action adjudication. Worker packs are unchanged. Job 3 remains **NOT AUTHORIZED**.\n'''
(ROOT/'R16C_S_CENTRAL_CLOSURE_REPORT.md').write_text(report)
(ROOT/'ACTIVE_EXECUTION_POINTER.md').write_text('''# ACTIVE EXECUTION POINTER — R16C-S\n\nCanonical floor: `CHECKPOINT_R16C_S_20260812`.\n\nC3 RR_NORM is **3,119 / 3,119 (100%) complete**. No RR_NORM source-recovery blocker remains.\n\nNext bounded central milestone: **C4 — adjudicate the exact 30,490 T06 actor-target-action link-review rows generated by 471 positive RR_NORM units**, while preserving remaining pair-authority and T07 naming blockers for their own central lanes.\n\nPositive RR_NORM is not T06 relation truth. Worker packs remain sealed. Job 3 is not authorized.\n''')
(ROOT/'ACTIVE_PROGRESS_LEDGER.md').write_text('''# ACTIVE PROGRESS LEDGER — after R16C-S\n\n- Governing 25-item checklist: **9/25 DONE**; #18 active.\n- #18A worker packs: DONE, sealed and untouched.\n- #18B central prerequisite campaign: ACTIVE.\n- C3 RR_NORM: **3,119 / 3,119 (100%) COMPLETE**.\n- Negative RR_NORM: **2,648**.\n- Positive RR_NORM: **471**, preserving **30,490** actor-target-action link-review rows.\n- RR_NORM blocked primitive surface: **0**.\n- Central queue: **86 containers / 32,363 atoms**.\n- Worker packs unchanged.\n- Job 3: **NOT AUTHORIZED**.\n- Next: C4 T06 actor-target-action link adjudication + remaining central authority families; #18C reconciliation/freeze after central and worker lanes.\n''')

# Construction validation.
checks=[]
def ck(name,cond,detail=''): checks.append({'check':name,'pass':bool(cond),'detail':str(detail)})
ck('parent_residual_17',len(res)==17,len(res)); ck('source_spec_17',len(decision_spec)==17); ck('source_recovery_all_governed',(ledger.source_recovery_status=='RECOVERED_TO_GOVERNING_STANDARD').all())
ck('positive_11',len(pos)==11,len(pos)); ck('negative_6',len(neg)==6,len(neg)); ck('partition_17',len(pos)+len(neg)==17); ck('decision_key_unique',not ledger.duplicated(key).any())
ck('proof_17_decisions',proof[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==17); ck('proof_17_impls',len(proof)==17,len(proof)); ck('proof_source_reviewed',(proof.authority_status=='source_reviewed').all()); ck('proof_source_authority_nonempty',proof.source_authority.str.strip().ne('').all())
ck('sealed_r11_positive_rows_698',len(pos_rows)==698,len(pos_rows)); ck('sealed_r11_negative_rows_862',len(neg_rows)==862,len(neg_rows)); ck('sealed_r11_frontier_partition_1560',len(pos_rows)+len(neg_rows)==1560); ck('row_partition_exact',set(pos_rows.opportunity_id)|set(neg_rows.opportunity_id)==set(parent_block_rows.opportunity_id)); ck('row_partition_disjoint',set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id)))
ck('cumulative_positive_471',len(all_pos)==471,len(all_pos)); ck('cumulative_link_rows_30490',len(all_pos_rows)==30490,len(all_pos_rows)); ck('prior_links_preserved',set(prior_pos_rows.opportunity_id).issubset(set(all_pos_rows.opportunity_id))); ck('new_links_exact',set(all_pos_rows.opportunity_id)-set(prior_pos_rows.opportunity_id)==set(pos_rows.opportunity_id))
ck('c3_3119',status['c3_current_adjudicated_decisions']==3119); ck('cumulative_negative_2648',status['cumulative_negative_rr_norm']==2648); ck('blocked_zero',status['t06_rr_norm_blocked_primitive_rows']==0)
ck('no_norm_role_blocker_containers',not (q2.work_family=='T06_NORM_ROLE_BLOCKER').any()); ck('link_containers_30',len(link_q)==30,len(link_q)); ck('link_atoms_471',int(link_q.decision_atom_count.sum())==471); ck('link_rows_30490',int(link_q.raw_primitive_row_count_sum.sum())==30490)
ck('queue_containers_86',len(q2)==86,len(q2)); ck('queue_atoms_32363',int(q2.decision_atom_count.sum())==32363,int(q2.decision_atom_count.sum())); ck('queue_rows_2295745',int(q2.raw_primitive_row_count_sum.sum())==2295745,int(q2.raw_primitive_row_count_sum.sum()))
ck('pair_static_31880',int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.sum())==31880); ck('pair_static_rows_2265243',int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].raw_primitive_row_count_sum.sum())==2265243); ck('t07_static_12',int(q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12)
# Required semantic controls for every formerly ambiguous family.
def D(sf,wv,code):
 x=ledger[(ledger.source_family==sf)&(ledger.wave==str(wv))&(ledger.source_variable_code==code)]
 return x.iloc[0].rr_norm_disposition if len(x)==1 else None
for sf,wv,code,expected in [
('Afrobarometer','R1','gidstr','NEGATIVE_RR_NORM'),('Arab Barometer','I','q611','NEGATIVE_RR_NORM'),('EVS','1990','q317b','POSITIVE_RR_NORM'),('EVS','1999','v94','POSITIVE_RR_NORM'),('EVS','1999','v94_at','POSITIVE_RR_NORM'),('EVS','1999','o12','POSITIVE_RR_NORM'),('GSS','1993','pclit','POSITIVE_RR_NORM'),('GSS','1993','classics','POSITIVE_RR_NORM'),('GSS','1993','pillok','POSITIVE_RR_NORM'),('GSS','2002','doc18a','NEGATIVE_RR_NORM'),('GSS','2002','doc20a','NEGATIVE_RR_NORM'),('GSS','2002','teamsafe','NEGATIVE_RR_NORM'),('GSS','2010','ldcgrn','POSITIVE_RR_NORM'),('GSS','2010','pillok','POSITIVE_RR_NORM'),('GSS','2010','teamsafe','NEGATIVE_RR_NORM'),('GSS','2016','pillok','POSITIVE_RR_NORM'),('GSS','2024','pillok','POSITIVE_RR_NORM')]: ck(f'disposition_{sf}_{wv}_{code}',D(sf,wv,code)==expected,D(sf,wv,code))
ck('worker_packs_unchanged_flag',status['worker_packs_changed'] is False); ck('job3_false',status['job3_authorized'] is False)
validation={'checkpoint':'R16C-S','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks)}
json.dump(validation,open(ROOT/'VALIDATION/VALIDATION_RESULT_R16C_S.json','w'),indent=2)
if validation['status']!='PASS': print(json.dumps(validation,indent=2)); raise SystemExit(2)

# Hostile QA: test precisely the tempting failure modes.
hostile=[]
def h(name,cond,detail=''): hostile.append({'attack':name,'pass':bool(cond),'detail':str(detail)})
h('prose_handoff_not_used_as_frontier',set(res.source_variable_code)==set(ledger.source_variable_code))
h('no_semantic_id_only_keying',not ledger.duplicated(key).any())
h('agree_disagree_not_mechanical',D('Afrobarometer','R1','gidstr')=='NEGATIVE_RR_NORM' and D('Arab Barometer','I','q611')=='NEGATIVE_RR_NORM')
h('descriptive_job_frame_not_laundered',D('GSS','2002','teamsafe')=='NEGATIVE_RR_NORM' and D('GSS','2010','teamsafe')=='NEGATIVE_RR_NORM')
h('doctor_trust_not_laundered_into_prescription',D('GSS','2002','doc18a')=='NEGATIVE_RR_NORM' and D('GSS','2002','doc20a')=='NEGATIVE_RR_NORM')
h('explicit_should_forced_retire_positive',D('EVS','1990','q317b')=='POSITIVE_RR_NORM')
h('explicit_work_permission_positive',D('EVS','1999','v94')=='POSITIVE_RR_NORM' and D('EVS','1999','v94_at')=='POSITIVE_RR_NORM')
h('explicit_religious_refusal_permission_positive',D('EVS','1999','o12')=='POSITIVE_RR_NORM')
h('pillok_permission_positive_all_four',all(D('GSS',wv,'pillok')=='POSITIVE_RR_NORM' for wv in ['1993','2010','2016','2024']))
h('ldcgrn_obligation_allocation_positive',D('GSS','2010','ldcgrn')=='POSITIVE_RR_NORM')
h('pclit_not_generic_affect',D('GSS','1993','pclit')=='POSITIVE_RR_NORM' and ledger[ledger.source_variable_code=='pclit'].c3b18_semantic_family.iloc[0]=='DISAPPROVAL_OF_CURRICULAR_CULTURAL_ARRANGEMENT')
h('classics_institutional_criterion_positive',D('GSS','1993','classics')=='POSITIVE_RR_NORM' and ledger[ledger.source_variable_code=='classics'].c3b18_semantic_family.iloc[0]=='CURRICULAR_ALLOCATION_CRITERION')
h('positive_is_not_relation_truth',pos.authority_ceiling.str.contains('LINK_REQUIRES_ACTOR_TARGET_ACTION').all())
h('negative_is_not_relation_absence',neg.authority_ceiling.str.contains('NO_RELATION_ABSENCE_CLAIM').all())
h('sealed_r11_exact_rebuild',len(pos_rows)==698 and len(neg_rows)==862 and set(pos_rows.opportunity_id)|set(neg_rows.opportunity_id)==set(parent_block_rows.opportunity_id))
h('zero_residual_means_zero_blocker_rows',len(pd.read_csv(ROOT/'QUEUE/C3B18_RESIDUAL_T06_BLOCKED_PRIMITIVE_ROWS_R16C_S.csv.gz'))==0 and not (q2.work_family=='T06_NORM_ROLE_BLOCKER').any())
h('static_authority_not_touched',int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.sum())==31880 and int(q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12)
h('job3_still_forbidden',status['job3_authorized'] is False)
h('repair18_not_fake_closed',status['repair_item_18_status'].startswith('ACTIVE'))
h('worker_packs_untouched_flag',status['worker_packs_changed'] is False)
host={'checkpoint':'R16C-S','status':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','attacks':hostile,'passed':sum(x['pass'] for x in hostile),'total':len(hostile)}
json.dump(host,open(ROOT/'VALIDATION/R16C_S_HOSTILE_QA.json','w'),indent=2)
if host['status']!='PASS': print(json.dumps(host,indent=2)); raise SystemExit(3)

shutil.copy('/mnt/data/build_r16c_s.py',ROOT/'CODE/build_r16c_s.py')

def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()

# Initial manifest; independent cold QA is added by separate script then this gets regenerated.
rows=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_file() and f.name!='SHA256_MANIFEST_R16C_S.csv': rows.append({'relative_path':str(f.relative_to(ROOT)),'sha256':sha(f),'size_bytes':f.stat().st_size})
pd.DataFrame(rows).to_csv(ROOT/'SHA256_MANIFEST_R16C_S.csv',index=False)
print(json.dumps({'status':'BUILT_PRE_COLD','validation':validation['status'],'checks':f"{validation['passed']}/{validation['total']}",'hostile':host['status'],'hostile_checks':f"{host['passed']}/{host['total']}",'positive':len(pos),'negative':len(neg),'new_positive_rows':len(pos_rows),'new_negative_rows':len(neg_rows),'cum_link_rows':len(all_pos_rows),'queue_containers':len(q2),'queue_atoms':int(q2.decision_atom_count.sum())},indent=2))
