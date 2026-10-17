from pathlib import Path
import pandas as pd, json, hashlib, zipfile, shutil, sys
sys.path.insert(0,'/mnt/data')
import candidate_r16c_r as cand

ROOT=Path('/mnt/data/r16c_r')
if ROOT.exists(): shutil.rmtree(ROOT)
for d in ['FAMILY_CENSUS','RESOLUTION','QUEUE','PROVENANCE','VALIDATION','CODE']:
    (ROOT/d).mkdir(parents=True,exist_ok=True)
PARENT=Path('/mnt/data/r16c_q')
R10A=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811')
R11=Path('/mnt/data/r11_work')
P2=Path('/mnt/data/c3_work/Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json')
key=['source_family','wave','semantic_unit_id']

res=cand.res.copy(); res['wave']=res.wave.astype(str)
pos=cand.P.copy(); pos['wave']=pos.wave.astype(str)
neg=cand.N.copy(); neg['wave']=neg.wave.astype(str)
child=cand.remaining.copy(); child['wave']=child.wave.astype(str)
selected=cand.selected.copy(); selected['wave']=selected.wave.astype(str)
front=cand.front.copy(); front['wave']=front.wave.astype(str)
assert len(res)==390 and len(pos)==35 and len(neg)==338 and len(child)==17 and len(selected)==373

sp=pd.read_csv(R10A/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',low_memory=False).fillna(''); sp['wave']=sp.wave.astype(str)
r11=pd.read_csv(R11/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',low_memory=False).fillna(''); r11['wave']=r11.wave.astype(str)
p2=json.load(open(P2)); impl=pd.DataFrame(p2['question_implementations']).fillna('')
q_parent=pd.read_csv(PARENT/'QUEUE/R16C_Q_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv').fillna(''); q_parent['wave']=q_parent.wave.astype(str)
prior_pos=pd.read_csv(PARENT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_Q.csv').fillna(''); prior_pos['wave']=prior_pos.wave.astype(str)
prior_pos_rows=pd.read_csv(PARENT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_Q.csv.gz',low_memory=False).fillna(''); prior_pos_rows['wave']=prior_pos_rows.wave.astype(str)

mi_res=pd.MultiIndex.from_frame(res[key].astype(str)); mi_pos=pd.MultiIndex.from_frame(pos[key].astype(str)); mi_neg=pd.MultiIndex.from_frame(neg[key].astype(str)); mi_child=pd.MultiIndex.from_frame(child[key].astype(str)); mi_sel=pd.MultiIndex.from_frame(selected[key].astype(str))

# Full 390 census, including the 17 explicitly preserved source-shorthand residuals.
census=res.copy()
census['c3b17_action']='RETAIN_SOURCE_STEM_REQUIRED'
census['c3b17_subfamily']='SOURCE_SHORTHAND_POLARITY_OR_STEM_UNRESOLVED'
census['c3b17_basis']='Exact source stem/polarity is insufficient to distinguish RR_NORM approval from descriptive, conduct, or cost semantics; preserve fail-closed.'
mi_c=pd.MultiIndex.from_frame(census[key].astype(str))
census.loc[mi_c.isin(mi_pos),'c3b17_action']='CLOSE_POSITIVE_RR_NORM'
census.loc[mi_c.isin(mi_pos),'c3b17_subfamily']='EXPLICIT_NORM_OBLIGATION_PERMISSION_APPROVAL_ROLE_POLICY_OR_SOCIAL_ARRANGEMENT'
census.loc[mi_c.isin(mi_pos),'c3b17_basis']='Governed semantics directly express norm/obligation/permission/rejection/approval or preference about an action, rule, role, policy, social/political arrangement, or explicit epistemic/religious rule.'
census.loc[mi_c.isin(mi_neg),'c3b17_action']='CLOSE_NEGATIVE_RR_NORM'
census.loc[mi_c.isin(mi_neg),'c3b17_subfamily']='DESCRIPTIVE_CAUSAL_CAPACITY_AFFECT_PERSONAL_IMPORTANCE_COMMITMENT_OR_PERFORMANCE'
census.loc[mi_c.isin(mi_neg),'c3b17_basis']='Governed semantics are descriptive/causal/capacity/performance/trust/affect/personal-importance/self-commitment/outcome-valence rather than a norm/obligation/approval shore.'
assert (census.c3b17_action=='CLOSE_POSITIVE_RR_NORM').sum()==35
assert (census.c3b17_action=='CLOSE_NEGATIVE_RR_NORM').sum()==338
assert (census.c3b17_action=='RETAIN_SOURCE_STEM_REQUIRED').sum()==17
census.to_csv(ROOT/'FAMILY_CENSUS/C3B17_FULL_390_DECISION_ENDGAME_CENSUS_R16C_R.csv',index=False)
summary=census.groupby(['c3b17_action','c3b17_subfamily']).size().rename('decision_count').reset_index().sort_values('decision_count',ascending=False)
summary.to_csv(ROOT/'FAMILY_CENSUS/C3B17_ENDGAME_ACTION_SUMMARY_R16C_R.csv',index=False)

# Exact role authority outputs.
pos_out=pos.copy(); pos_out['rr_norm_disposition']='POSITIVE_RR_NORM__EXPLICIT_NORM_APPROVAL_PERMISSION_POLICY_ROLE_OR_SOCIAL_ARRANGEMENT'; pos_out['authority_ceiling']='POSITIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__T06_LINK_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION'
neg_out=neg.copy(); neg_out['rr_norm_disposition']='NEGATIVE_RR_NORM__NONNORMATIVE_DESCRIPTIVE_AFFECTIVE_PERSONAL_OR_CONDUCT_SEMANTICS'; neg_out['authority_ceiling']='NEGATIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__NO_RELATION_ABSENCE_CLAIM'
pos_out.to_csv(ROOT/'RESOLUTION/C3B17_POSITIVE_RR_NORM_AUTHORITY_R16C_R.csv',index=False)
neg_out.to_csv(ROOT/'RESOLUTION/C3B17_NEGATIVE_RR_NORM_AUTHORITY_R16C_R.csv',index=False)
child.to_csv(ROOT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_R.csv',index=False)
child.assign(residual_reason='SOURCE_STEM_OR_POLARITY_NOT_RECOVERED_TO_GOVERNING_STANDARD__NO_RR_NORM_CLAIM').to_csv(ROOT/'PROVENANCE/C3B17_17_ITEM_FAIL_CLOSED_SOURCE_RECOVERY_FRONTIER_R16C_R.csv',index=False)

# Member-complete source-reviewed implementation proof (one-to-many allowed).
spmi=pd.MultiIndex.from_frame(sp[['source_family','wave','sem__audit_unit_id']].astype(str))
sp_sel=sp[spmi.isin(mi_sel)].copy()
proof_cols=['source_family','wave','sem__audit_unit_id','question_implementation_id','source_variable_code','source_authority','exact_question_text','sem__semantic_summary','sem__measured_predicate','sem__canonical_role']
sp_sel=sp_sel[proof_cols]
assert sp_sel[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==373
assert len(sp_sel)==375
proof=sp_sel.merge(impl[['question_implementation_id','authority_status']],on='question_implementation_id',how='left',validate='many_to_one')
assert (proof.authority_status=='source_reviewed').all()
assert proof.source_authority.astype(str).str.strip().ne('').all()
proof.to_csv(ROOT/'PROVENANCE/C3B17_MEMBER_COMPLETE_SOURCE_REVIEWED_IMPLEMENTATION_PROOF_R16C_R.csv',index=False)
mult=proof.groupby(['source_family','wave','sem__audit_unit_id']).size().rename('exact_implementation_count').reset_index()
mult.to_csv(ROOT/'PROVENANCE/C3B17_DECISION_TO_IMPLEMENTATION_MULTIPLICITY_R16C_R.csv',index=False)

# Exact R11 accounting.
rmi=pd.MultiIndex.from_frame(r11[key].astype(str))
pos_rows=r11[rmi.isin(mi_pos)].copy(); neg_rows=r11[rmi.isin(mi_neg)].copy(); child_rows=r11[rmi.isin(mi_child)].copy()
assert len(pos_rows)==1662 and len(neg_rows)==22698 and len(child_rows)==1560
assert pos_rows.opportunity_id.is_unique and neg_rows.opportunity_id.is_unique and child_rows.opportunity_id.is_unique
assert set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id))
assert set(pos_rows.opportunity_id).isdisjoint(set(child_rows.opportunity_id))
assert set(neg_rows.opportunity_id).isdisjoint(set(child_rows.opportunity_id))
pos_rows.to_csv(ROOT/'RESOLUTION/C3B17_TRANSFERRED_T06_LINK_REVIEW_ROWS_R16C_R.csv.gz',index=False,compression='gzip')
neg_rows.to_csv(ROOT/'RESOLUTION/C3B17_RETIRED_T06_PRIMITIVE_ROWS_R16C_R.csv.gz',index=False,compression='gzip')
child_rows.to_csv(ROOT/'QUEUE/C3B17_RESIDUAL_T06_BLOCKED_PRIMITIVE_ROWS_R16C_R.csv.gz',index=False,compression='gzip')

# Cumulative positive authority / T06 link workload through R.
rpos=pos.copy(); rpos['positive_authority_origin']='R16C-R'
all_pos=pd.concat([prior_pos,rpos],ignore_index=True)
assert len(prior_pos)==425 and len(all_pos)==460 and not all_pos.duplicated(key).any()
allpmi=pd.MultiIndex.from_frame(all_pos[key].astype(str))
all_pos_rows=r11[rmi.isin(allpmi)].copy()
assert len(prior_pos_rows)==28130 and len(all_pos_rows)==29792
assert set(prior_pos_rows.opportunity_id).issubset(set(all_pos_rows.opportunity_id))
assert len(set(all_pos_rows.opportunity_id)-set(prior_pos_rows.opportunity_id))==1662
all_pos.to_csv(ROOT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_R.csv',index=False)
all_pos_rows.to_csv(ROOT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_R.csv.gz',index=False,compression='gzip')

# Rebuild central queue from authority, not inherited arithmetic.
static=q_parent[q_parent.work_family.isin(['PAIR_AUTHORITY_BLOCKER','T07_GOVERNMENT_SCOPE_NAMING'])].copy()
parent_block=q_parent[q_parent.work_family=='T06_NORM_ROLE_BLOCKER'].copy()
block_rows=[]
for (sf,wv),g in child.groupby(['source_family','wave']):
    src=parent_block[(parent_block.source_family==sf)&(parent_block.wave==str(wv))]
    assert len(src)==1,(sf,wv,len(src))
    row=src.iloc[0].copy(); rr=child_rows[(child_rows.source_family==sf)&(child_rows.wave==str(wv))]
    row['decision_atom_count']=len(g); row['raw_primitive_row_count_sum']=len(rr); row['planning_effort_units']=round(0.25*len(g),6)
    row['packet_statuses_json']='["C3B17_SOURCE_RECOVERY_FRONTIER__RR_NORM_UNRESOLVED"]'
    row['authority_ceilings_json']='["NO_T06_ABSENCE_CLAIM__SOURCE_STEM_REQUIRED"]'
    block_rows.append(row)
block_q=pd.DataFrame(block_rows,columns=q_parent.columns)
assert len(block_q)==9 and int(block_q.decision_atom_count.sum())==17 and int(block_q.raw_primitive_row_count_sum.sum())==1560
# cumulative positive link queue by source-wave
sp_allp=sp[spmi.isin(allpmi)].copy()
assert sp_allp[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==460
link_rows=[]
for (sf,wv),g in all_pos.groupby(['source_family','wave']):
    rr=all_pos_rows[(all_pos_rows.source_family==sf)&(all_pos_rows.wave==str(wv))]
    impct=sp_allp[(sp_allp.source_family==sf)&(sp_allp.wave==str(wv))].question_implementation_id.nunique()
    link_rows.append({
      'packet_id':f'R16C-R-CUMULATIVE-NORM-LINK::{sf}::{wv}','source_family':sf,'wave':str(wv),'work_family':'T06_RR_NORM_POSITIVE_LINK_REVIEW',
      'execution_lane':'VOZHD_CENTRAL__T06_RELATION_LINK_ADJUDICATION','rule_hypotheses':'T06','decision_atom_count':len(g),
      'raw_primitive_row_count_sum':len(rr),'member_implementation_count':impct,'planning_effort_units':round(0.25*len(g),6),
      'packet_statuses_json':'["RR_NORM_GOVERNED_POSITIVE__RELATION_LINK_REVIEW_REQUIRED__CUMULATIVE_THROUGH_R16C_R"]',
      'authority_ceilings_json':'["NO_T06_RELATION_AUTHORITY_YET"]'})
link_q=pd.DataFrame(link_rows,columns=q_parent.columns)
assert len(link_q)==30 and int(link_q.decision_atom_count.sum())==460 and int(link_q.raw_primitive_row_count_sum.sum())==29792
q2=pd.concat([static,block_q,link_q],ignore_index=True).sort_values(['work_family','source_family','wave','packet_id']).reset_index(drop=True)
assert len(q2)==95
assert int(q2.decision_atom_count.sum())==32369
assert int(q2.raw_primitive_row_count_sum.sum())==2296607
q2.to_csv(ROOT/'QUEUE/R16C_R_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)

# Source-wave accounting.
acct_dec=pd.concat([pos.groupby(['source_family','wave']).size().rename('positive_rr_norm_decisions'),neg.groupby(['source_family','wave']).size().rename('negative_rr_norm_decisions'),child.groupby(['source_family','wave']).size().rename('residual_rr_norm_decisions')],axis=1).fillna(0).astype(int)
acct_rows=pd.concat([pos_rows.groupby(['source_family','wave']).size().rename('transferred_link_rows'),neg_rows.groupby(['source_family','wave']).size().rename('retired_primitive_rows'),child_rows.groupby(['source_family','wave']).size().rename('residual_blocked_rows')],axis=1).fillna(0).astype(int)
acct=acct_dec.join(acct_rows,how='outer').fillna(0).astype(int).reset_index(); acct.to_csv(ROOT/'RESOLUTION/C3B17_SOURCE_WAVE_ACCOUNTING_R16C_R.csv',index=False)

# Source recovery note and doctrine.
(ROOT/'PROVENANCE/C3B17_SOURCE_RECOVERY_NOTE.md').write_text('''# C3b17 source recovery note\n\nHistorical/source recovery was performed before adjudicating shorthand cases.\n\n- **Arab Barometer Wave V Q605A**: the official questionnaire stem asks whether respondents agree that **“Shari’a government means …”** the listed attributes (basic services, no corruption, physical punishment, restricting women’s role). These are definitional/conceptual beliefs about what Sharia government means, not respondent approval of those arrangements. Q605A_1..4 therefore receive **NEGATIVE RR_NORM**.\n- **Arab Barometer Wave I**: official questionnaire text establishes explicit normative forms where present (e.g. banks **must be forbidden** from interest; women’s social principles; political-system suitability). Those support positive RR_NORM only when the proposition itself is normative/permission/approval.\n- **LiTS 2006 q305_1..q305_6**: exact governed text is *perception of state involvement* in the listed economic roles, not respondent preference. These receive **NEGATIVE RR_NORM**.\n- **WVS W1 V113/V115 and W4 V131**: proposed future social changes are evaluated as **Good thing / Don’t mind / Bad thing**, which is explicit approval/disapproval of a social change. These receive **POSITIVE RR_NORM**.\n- **WVS confidence placeholders (e.g. V160P / W7 Q82_AFRICANUNION)** remain trust/confidence measures and are **NEGATIVE RR_NORM**.\n- **17 source-shorthand cases remain fail-closed** because the recovered project authority does not preserve enough stem/polarity to distinguish norm/approval from descriptive, conduct, or cost semantics. No guess is promoted to authority.\n''')
(ROOT/'PROVENANCE/C3B17_DOCTRINE.md').write_text('''# C3b17 RR_NORM endgame doctrine\n\n`RR_NORM` is the **norm / obligation / approval shore** for T06. The approval shore is bounded: it includes approval, preference, permission, rejection, or normative criterion concerning an **actor, action, rule, role, policy, or social/political arrangement**. It does **not** automatically include mere liking/favorability, personal importance, perceived fairness, sympathy, confidence, performance evaluation, causal belief, expectation, self-reported commitment/cost, or generic outcome valence.\n\nA broad semantic-act role, lexical cue, or proposition-endorsement label is never sufficient by itself. Exact source semantics control.\n\nPositive RR_NORM does **not** emit a T06 relation; it transfers every exact R11 opportunity into actor-target-action link review. Negative RR_NORM retires only the impossible norm-shore path and creates no broader relation-absence claim.\n\nExact decision identity remains `(source_family, wave, semantic_unit_id)`; semantic-ID-only keying is forbidden. Member-complete source proof permits one decision to map to multiple exact current implementations.\n''')

# Reports / status / pointers.
new_adjudicated=3119-len(child); pct=new_adjudicated/3119*100
status={
 'checkpoint':'R16C-R','subtask':'#18B-C3b17 endgame RR_NORM closure with fail-closed source recovery frontier',
 'parent_residual':390,'positive_rr_norm_closed':35,'negative_rr_norm_closed':338,'total_role_decisions_closed':373,'residual_rr_norm':17,
 'positive_link_rows_transferred_current':1662,'negative_primitive_rows_retired_current':22698,'residual_blocked_rows':1560,
 'c3_total_role_adjudicated':new_adjudicated,'c3_parent':3119,'c3_percent':round(pct,4),'c3_negative_rr_norm':2304+338,'c3_positive_rr_norm':425+35,'c3_positive_link_rows_total':29792,
 't06_blocked_primitive_rows_parent':25920,'t06_blocked_primitive_rows_successor':1560,
 'central_parent_containers':116,'central_parent_atoms':32707,'central_successor_containers':95,'central_successor_atoms':32369,'central_successor_raw_rows':2296607,
 'worker_packs_changed':False,'job3_authorized':False,
 'next':'C3b18 targeted source recovery for the 17 exact residual RR_NORM decisions; do not claim C3 complete until each is governed or source-blocked.'}
json.dump(status,open(ROOT/'CURRENT_STATUS_R16C_R.json','w'),indent=2)
report=f'''# R16C-R — #18B-C3b17 RR_NORM endgame closure\n\n## Semantic closure\n- Parent residual: **390**.\n- Closed positive RR_NORM: **35**.\n- Closed negative RR_NORM: **338**.\n- Total closed in this batch: **373**.\n- Fail-closed source-recovery frontier: **17**.\n- Current positive rows transferred to T06 link review: **1,662**.\n- Current negative impossible norm-shore rows retired: **22,698**.\n- Blocked primitive surface: **25,920 → 1,560**.\n- C3 adjudicated **{new_adjudicated} / 3,119 = {pct:.2f}%**.\n- Cumulative negative RR_NORM: **{2304+338}**.\n- Cumulative positive RR_NORM: **{425+35}**, preserving **29,792** link-review rows.\n\n## Fail-closed frontier\nThe 17 remaining decisions are not treated as semantic ambiguity by default; they are an explicit **source-stem/polarity recovery frontier**. Their compact project text does not preserve enough context to distinguish norm/approval from descriptive, conduct, or cost semantics. No absence or positive claim is made.\n\n## Central queue\n- Parent: **116 containers / 32,707 atoms**.\n- Successor: **95 containers / 32,369 atoms**.\n- The 338 negative closures remove 338 central atoms.\n- The 35 positive closures transfer to T06 link review and remain central atoms.\n\n## Endgame action summary\n{summary.to_markdown(index=False)}\n\nWorker packs unchanged. Job 3 **NOT AUTHORIZED**. C3 is **not complete** until the 17-item source frontier is resolved or governed source-blocked.\n'''
(ROOT/'R16C_R_CENTRAL_CLOSURE_REPORT.md').write_text(report)
(ROOT/'ACTIVE_EXECUTION_POINTER.md').write_text(f'''# ACTIVE EXECUTION POINTER — R16C-R\n\nCanonical floor: `CHECKPOINT_R16C_R_20260812`.\n\nC3 RR_NORM is **{new_adjudicated} / 3,119 = {pct:.2f}% adjudicated**; residual **17** exact source-recovery decisions.\n\nNext: **C3b18 targeted source recovery for the 17 exact residuals**. Do not force a semantic verdict without stem/polarity authority.\n\nHard invariants: exact `(source_family, wave, semantic_unit_id)` key; positive RR_NORM transfers to link review; negative RR_NORM only retires the norm shore; worker packs sealed; Job 3 not authorized.\n''')
(ROOT/'ACTIVE_PROGRESS_LEDGER.md').write_text(f'''# ACTIVE PROGRESS LEDGER — after R16C-R\n\n- Governing 25-item checklist: **9/25 DONE**; #18 active.\n- #18A worker packs: DONE, sealed and untouched.\n- #18B central prerequisite campaign: ACTIVE.\n- C3 RR_NORM shore: **{new_adjudicated} / 3,119 ({pct:.2f}%) adjudicated**.\n- Residual RR_NORM decisions: **17**.\n- Negative RR_NORM: **{2304+338}**.\n- Positive RR_NORM: **{425+35}**, preserving **29,792** link-review rows.\n- T06 input-authority blocked primitive surface: **1,560 rows**.\n- Central queue: **95 containers / 32,369 atoms**.\n- Worker packs unchanged.\n- Job 3: NOT AUTHORIZED.\n- Next: C3b18 source recovery for 17 exact residuals.\n''')

# Code copies.
shutil.copy('/mnt/data/candidate_r16c_r.py',ROOT/'CODE/candidate_r16c_r.py')
shutil.copy('/mnt/data/build_r16c_r.py',ROOT/'CODE/build_r16c_r.py')

# Validation + hostile QA.
checks=[]
def ck(name,cond,detail=''): checks.append({'check':name,'pass':bool(cond),'detail':str(detail)})
ck('parent_390',len(res)==390,len(res)); ck('positive_35',len(pos)==35,len(pos)); ck('negative_338',len(neg)==338,len(neg)); ck('selected_373',len(selected)==373,len(selected)); ck('residual_17',len(child)==17,len(child))
ck('partition_exact',set(map(tuple,selected[key].astype(str).values.tolist()))|set(map(tuple,child[key].astype(str).values.tolist()))==set(map(tuple,res[key].astype(str).values.tolist())))
ck('selected_child_disjoint',set(map(tuple,selected[key].astype(str).values.tolist())).isdisjoint(set(map(tuple,child[key].astype(str).values.tolist()))))
ck('p_n_disjoint',set(map(tuple,pos[key].astype(str).values.tolist())).isdisjoint(set(map(tuple,neg[key].astype(str).values.tolist()))))
ck('proof_373_decisions',proof[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==373); ck('proof_375_impls',len(proof)==375,len(proof)); ck('proof_all_source_reviewed',(proof.authority_status=='source_reviewed').all()); ck('proof_authority_nonempty',proof.source_authority.astype(str).str.strip().ne('').all())
ck('pos_rows_1662',len(pos_rows)==1662,len(pos_rows)); ck('neg_rows_22698',len(neg_rows)==22698,len(neg_rows)); ck('residual_rows_1560',len(child_rows)==1560,len(child_rows)); ck('r11_partition_25920',len(pos_rows)+len(neg_rows)+len(child_rows)==25920)
ck('prior_positive_425',len(prior_pos)==425,len(prior_pos)); ck('cum_positive_460',len(all_pos)==460,len(all_pos)); ck('cum_positive_rows_29792',len(all_pos_rows)==29792,len(all_pos_rows)); ck('new_negative_no_prior_positive_semid',set(neg.semantic_unit_id).isdisjoint(set(prior_pos.semantic_unit_id)))
conf=pd.concat([pos.assign(_d='P'),neg.assign(_d='N')]).groupby('semantic_unit_id')._d.nunique(); ck('no_new_pos_neg_semid_conflict',not (conf>1).any(),int((conf>1).sum()))
# Critical source/doctrine controls.
def has(df,sf,wv,code): return len(df[(df.source_family==sf)&(df.wave==str(wv))&(df.source_variable_code==code)])==1
for code in ['Q605A_1','Q605A_2','Q605A_3','Q605A_4']: ck(f'abv_{code}_definitional_negative',has(neg,'Arab Barometer','V',code))
for code in ['q305_1','q305_2','q305_3','q305_4','q305_5','q305_6']: ck(f'lits2006_{code}_perception_negative',has(neg,'LiTS','2006',code))
for sf,wv,code in cand.EDGE_POS: ck(f'edge_positive_{sf}_{wv}_{code}',has(pos,sf,wv,code))
for code in ['pclit','classics','pillok']: ck(f'gss1993_{code}_failclosed',has(child,'GSS','1993',code))
ck('evs_o12_failclosed',has(child,'EVS','1999','o12')); ck('ab_q611_failclosed',has(child,'Arab Barometer','I','q611'))
# Generic affect / personal importance / cost commitments must not be silently promoted.
affect_terms='liking|favorability|named_population_positive_affinity|people_affinity_despite_state_policy|country affect/favorability|music liking|sympathy|influence_valence'
ck('no_generic_affect_positive',not pos.sem__measured_predicate.astype(str).str.contains(affect_terms,case=False,regex=True).any(),pos[pos.sem__measured_predicate.astype(str).str.contains(affect_terms,case=False,regex=True)].source_variable_code.tolist())
ck('no_personal_importance_positive',not pos.sem__measured_predicate.astype(str).str.fullmatch('importance|importance evaluation',case=False).any())
# Queue exact.
ck('block_containers_9',len(block_q)==9,len(block_q)); ck('block_atoms_17',int(block_q.decision_atom_count.sum())==17); ck('block_rows_1560',int(block_q.raw_primitive_row_count_sum.sum())==1560)
ck('link_containers_30',len(link_q)==30,len(link_q)); ck('link_atoms_460',int(link_q.decision_atom_count.sum())==460); ck('link_rows_29792',int(link_q.raw_primitive_row_count_sum.sum())==29792)
ck('queue_containers_95',len(q2)==95,len(q2)); ck('queue_atoms_32369',int(q2.decision_atom_count.sum())==32369,int(q2.decision_atom_count.sum())); ck('queue_rows_2296607',int(q2.raw_primitive_row_count_sum.sum())==2296607)
ck('pair_static_31880',int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.sum())==31880); ck('t07_static_12',int(q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12)
ck('job3_false',status['job3_authorized'] is False); ck('worker_packs_unchanged',status['worker_packs_changed'] is False)
validation={'checkpoint':'R16C-R','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks)}
json.dump(validation,open(ROOT/'VALIDATION/VALIDATION_RESULT_R16C_R.json','w'),indent=2)
if validation['status']!='PASS': print(json.dumps(validation,indent=2)); raise SystemExit(2)

hostile=[]
def h(name,cond,detail=''): hostile.append({'attack':name,'pass':bool(cond),'detail':str(detail)})
h('no_semantic_id_only_crosswave_bleed',not (conf>1).any(),int((conf>1).sum()))
h('all_17_residuals_preserved_exact',len(child)==17 and len(child_rows)==1560)
h('source_shorthand_not_forced',all(has(child,*x) for x in [('Arab Barometer','I','q611'),('EVS','1990','q317b'),('EVS','1999','o12'),('GSS','2002','doc20a'),('GSS','2002','doc18a'),('GSS','2010','ldcgrn')]))
h('q605a_not_misread_as_policy_support',all(has(neg,'Arab Barometer','V',c) for c in ['Q605A_1','Q605A_2','Q605A_3','Q605A_4']))
h('lits_state_involvement_not_misread_as_preference',all(has(neg,'LiTS','2006',c) for c in ['q305_1','q305_2','q305_3','q305_4','q305_5','q305_6']))
h('affect_not_laundered_into_approval',not pos.sem__measured_predicate.astype(str).str.contains(affect_terms,case=False,regex=True).any())
h('self_commitment_cost_not_laundered',not pos.exact_question_text.astype(str).str.contains('give part of my income|paying more in taxes|give information to help justice',case=False,regex=True).any())
h('positive_transfers_not_relations',pos_out.authority_ceiling.str.contains('LINK_REQUIRES').all())
h('negative_no_relation_absence',neg_out.authority_ceiling.str.contains('NO_RELATION_ABSENCE_CLAIM').all())
h('member_complete_one_to_many_allowed',(mult.exact_implementation_count>1).sum()==2,int((mult.exact_implementation_count>1).sum()))
h('cumulative_positive_exact',len(all_pos)==460 and len(all_pos_rows)==29792)
h('queue_rebuilt_from_authority',len(q2)==95 and int(q2.decision_atom_count.sum())==32369)
h('job3_false',status['job3_authorized'] is False)
h('worker_packs_unchanged',status['worker_packs_changed'] is False)
host={'checkpoint':'R16C-R','status':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','attacks':hostile,'passed':sum(x['pass'] for x in hostile),'total':len(hostile)}
json.dump(host,open(ROOT/'VALIDATION/R16C_R_HOSTILE_QA.json','w'),indent=2)
if host['status']!='PASS': print(json.dumps(host,indent=2)); raise SystemExit(3)

# Manifest + initial ZIP.
def sha(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
rows=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_file() and f.name!='SHA256_MANIFEST_R16C_R.csv': rows.append({'relative_path':str(f.relative_to(ROOT)),'sha256':sha(f),'size_bytes':f.stat().st_size})
pd.DataFrame(rows).to_csv(ROOT/'SHA256_MANIFEST_R16C_R.csv',index=False)
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_R_20260812.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(ROOT.rglob('*')):
  if f.is_file(): z.write(f,arcname=str(f.relative_to(ROOT)))
zipsha=sha(zip_path)
Path(str(zip_path)+'.sha256').write_text(f'{zipsha}  {zip_path.name}\n')
print(json.dumps({'validation':validation['status'],'checks':f"{validation['passed']}/{validation['total']}",'hostile':host['status'],'hostile_checks':f"{host['passed']}/{host['total']}",'zip':str(zip_path),'sha256':zipsha,'size':zip_path.stat().st_size,'selected':len(selected),'residual':len(child)},indent=2))
