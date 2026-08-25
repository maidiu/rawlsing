from pathlib import Path
import pandas as pd, json, re, hashlib, zipfile, shutil, os, sys
sys.path.insert(0,'/mnt/data')
import candidate_r16c_q as cand

ROOT=Path('/mnt/data/r16c_q')
if ROOT.exists(): shutil.rmtree(ROOT)
for d in ['FAMILY_CENSUS','RESOLUTION','QUEUE','PROVENANCE','VALIDATION','CODE','PARENT_CORRECTION']:
    (ROOT/d).mkdir(parents=True,exist_ok=True)
PARENT=Path('/mnt/data/r16c_p_next')
R10A=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811')
R11=Path('/mnt/data/r11_work')
P2=Path('/mnt/data/c3_work/Rawlsing_P2_Phase0_Governed_Question_Node_Catalog_v1.json')
key=['source_family','wave','semantic_unit_id']

res=cand.res.copy(); res['wave']=res['wave'].astype(str)
pos=cand.P.copy(); pos['wave']=pos['wave'].astype(str)
neg=cand.N.copy(); neg['wave']=neg['wave'].astype(str)
selected=cand.selected.copy(); selected['wave']=selected['wave'].astype(str)
child=cand.remaining.copy(); child['wave']=child['wave'].astype(str)
prop_boundary=pd.read_csv(PARENT/'PROVENANCE/C3B15_PROPOSITION_BOUNDARY_FRONTIER_R16C_P.csv').fillna(''); prop_boundary['wave']=prop_boundary['wave'].astype(str)
assert len(res)==794 and len(pos)==199 and len(neg)==205 and len(child)==390 and len(prop_boundary)==243

# Immutable authority sources.
sp=pd.read_csv(R10A/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',low_memory=False).fillna(''); sp['wave']=sp['wave'].astype(str)
r11=pd.read_csv(R11/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',low_memory=False).fillna(''); r11['wave']=r11['wave'].astype(str)
p2=json.load(open(P2)); impl=pd.DataFrame(p2['question_implementations']).fillna('')
q_parent=pd.read_csv(PARENT/'QUEUE/R16C_P_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv').fillna(''); q_parent['wave']=q_parent['wave'].astype(str)

# ---- Full C3b16 family census ----
# Every one of 794 parent decisions gets exactly one C3b16 action.
mi_sel=pd.MultiIndex.from_frame(selected[key].astype(str)); mi_pos=pd.MultiIndex.from_frame(pos[key].astype(str)); mi_neg=pd.MultiIndex.from_frame(neg[key].astype(str)); mi_pb=pd.MultiIndex.from_frame(prop_boundary[key].astype(str))
census=res.copy()
mi_res=pd.MultiIndex.from_frame(census[key].astype(str))
census['c3b16_action']='RETAIN_FOR_FURTHER_ADJUDICATION'
census['c3b16_subfamily']='NONPROPOSITION_EDGE_BOUNDARY'
census['c3b16_basis']='No large-batch RR_NORM rule established at this checkpoint.'
census.loc[mi_res.isin(mi_pb),'c3b16_subfamily']='PROPOSITION_BOUNDARY_PRESERVED_FROM_R16C_P'
census.loc[mi_res.isin(mi_pb),'c3b16_basis']='R16C-P proposition boundary remains fail-closed; not touched by non-proposition family rules.'
census.loc[mi_res.isin(mi_pos),'c3b16_action']='CLOSE_POSITIVE_RR_NORM'
census.loc[mi_res.isin(mi_pos),'c3b16_subfamily']='NORMATIVE_APPROVAL_PREFERENCE_CRITERION_OR_POLICY'
census.loc[mi_res.isin(mi_pos),'c3b16_basis']='Governed semantics express norm/approval/preference/acceptance/rejection/responsibility/criterion or explicit evaluation of a proposed social/political form.'
census.loc[mi_res.isin(mi_neg),'c3b16_action']='CLOSE_NEGATIVE_RR_NORM'
census.loc[mi_res.isin(mi_neg),'c3b16_subfamily']='DESCRIPTIVE_TRUST_STATE_CAPACITY_EXPECTATION_PERSONAL_SALIENCE_OR_CAUSAL'
census.loc[mi_res.isin(mi_neg),'c3b16_basis']='Governed semantics are descriptive trust/state/capacity/experience/expectation/personal salience/causal appraisal, not a norm/obligation/approval shore.'
assert len(census)==794
assert (census.c3b16_action=='CLOSE_POSITIVE_RR_NORM').sum()==199
assert (census.c3b16_action=='CLOSE_NEGATIVE_RR_NORM').sum()==205
assert (census.c3b16_action=='RETAIN_FOR_FURTHER_ADJUDICATION').sum()==390
assert (census.c3b16_subfamily=='PROPOSITION_BOUNDARY_PRESERVED_FROM_R16C_P').sum()==243
census.to_csv(ROOT/'FAMILY_CENSUS/C3B16_FULL_794_DECISION_FAMILY_CENSUS_R16C_Q.csv',index=False)
summary=census.groupby(['c3b16_action','c3b16_subfamily']).size().rename('decision_count').reset_index().sort_values('decision_count',ascending=False)
summary.to_csv(ROOT/'FAMILY_CENSUS/C3B16_FAMILY_ACTION_SUMMARY_R16C_Q.csv',index=False)

# ---- Exact RR_NORM ledgers ----
pos_out=pos.copy(); pos_out['rr_norm_disposition']='POSITIVE_RR_NORM__NORMATIVE_APPROVAL_PREFERENCE_CRITERION_OR_POLICY'; pos_out['authority_ceiling']='POSITIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__T06_LINK_STILL_REQUIRES_ACTOR_TARGET_ACTION_ADJUDICATION'
neg_out=neg.copy(); neg_out['rr_norm_disposition']='NEGATIVE_RR_NORM__DESCRIPTIVE_NONAPPROVAL_SEMANTICS'; neg_out['authority_ceiling']='NEGATIVE_RELATION_ROLE_AUTHORITY__RR_NORM_ONLY__NO_RELATION_ABSENCE_CLAIM'
pos_out.to_csv(ROOT/'RESOLUTION/C3B16_POSITIVE_RR_NORM_AUTHORITY_R16C_Q.csv',index=False)
neg_out.to_csv(ROOT/'RESOLUTION/C3B16_NEGATIVE_RR_NORM_AUTHORITY_R16C_Q.csv',index=False)
child.drop(columns=['is_prop_boundary'],errors='ignore').to_csv(ROOT/'QUEUE/C3B_RESIDUAL_RR_NORM_REVIEW_SHORE_R16C_Q.csv',index=False)

# Explicit preserved boundaries.
left=census[census.c3b16_action=='RETAIN_FOR_FURTHER_ADJUDICATION'].copy()
left.to_csv(ROOT/'PROVENANCE/C3B16_PRESERVED_BOUNDARY_FRONTIER_R16C_Q.csv',index=False)
# Approval/affect and ambiguity controls must remain.
affect_preds={'liking','favorability rating','favorability_rating','named_population_positive_affinity','country affect/favorability','people_affinity_despite_state_policy','political-system affect/evaluation','music liking','immigrants__sympathy','elderly_people__sympathy','aversion_intensity'}
affect=child[child['sem__measured_predicate'].isin(affect_preds)].copy(); affect.to_csv(ROOT/'PROVENANCE/C3B16_AFFECT_APPROVAL_BOUNDARY_R16C_Q.csv',index=False)

# ---- Member-complete source-reviewed implementation proof ----
# Decision key may lawfully map to >1 exact implementation in the same source-wave; prove completeness rather than forcing one-to-one.
spmi=pd.MultiIndex.from_frame(sp[['source_family','wave','sem__audit_unit_id']].astype(str))
sp_sel=sp[spmi.isin(mi_sel)].copy()
sp_sel=sp_sel[['source_family','wave','sem__audit_unit_id','question_implementation_id','source_variable_code','source_authority','exact_question_text','sem__semantic_summary','sem__measured_predicate','sem__canonical_role']]
assert sp_sel[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==404
assert len(sp_sel)==407
proof=sp_sel.merge(impl[['question_implementation_id','authority_status']],on='question_implementation_id',how='left',validate='many_to_one')
assert (proof.authority_status=='source_reviewed').all()
assert proof.source_authority.astype(str).str.strip().ne('').all()
assert proof.question_implementation_id.nunique()==407
proof.to_csv(ROOT/'PROVENANCE/C3B16_MEMBER_COMPLETE_SOURCE_REVIEWED_IMPLEMENTATION_PROOF_R16C_Q.csv',index=False)
member_counts=proof.groupby(['source_family','wave','sem__audit_unit_id']).size().rename('exact_implementation_count').reset_index()
member_counts.to_csv(ROOT/'PROVENANCE/C3B16_DECISION_TO_IMPLEMENTATION_MULTIPLICITY_R16C_Q.csv',index=False)

# ---- Exact R11 row accounting ----
rmi=pd.MultiIndex.from_frame(r11[key].astype(str))
pos_rows=r11[rmi.isin(mi_pos)].copy(); neg_rows=r11[rmi.isin(mi_neg)].copy()
assert len(pos_rows)==9661
assert len(neg_rows)==14770
assert pos_rows.opportunity_id.is_unique and neg_rows.opportunity_id.is_unique
assert set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id))
pos_rows.to_csv(ROOT/'RESOLUTION/C3B16_TRANSFERRED_T06_LINK_REVIEW_ROWS_R16C_Q.csv.gz',index=False,compression='gzip')
neg_rows.to_csv(ROOT/'RESOLUTION/C3B16_RETIRED_T06_PRIMITIVE_ROWS_R16C_Q.csv.gz',index=False,compression='gzip')

# ---- R16C-P queue-accounting defect repair ----
prior_pos_files=[
('R16C-B',Path('/mnt/data/r16c_b/RESOLUTION/C3B1_CIVIL_LIBERTY_POSITIVE_RR_NORM_AUTHORITY_R16C_B.csv')),
('R16C-C',Path('/mnt/data/r16c_c/RESOLUTION/C3B2_QRA_PERMISSION_POSITIVE_RR_NORM_AUTHORITY_R16C_C.csv')),
('R16C-D',Path('/mnt/data/r16c_d/RESOLUTION/C3B3_GSS_POLICY_SUPPORT_POSITIVE_RR_NORM_AUTHORITY_R16C_D.csv')),
('R16C-E',Path('/mnt/data/r16c_e/RESOLUTION/C3B4_ASB_W5_GOVERNMENT_RESPONSIBILITY_POSITIVE_RR_NORM_R16C_E.csv')),
('R16C-G',Path('/mnt/data/r16c_g/RESOLUTION/C3B6_EXPLICIT_OPERATOR_POSITIVE_RR_NORM_AUTHORITY_R16C_G.csv')),
('R16C-H',Path('/mnt/data/r16c_h/RESOLUTION/C3B7_SOURCE_NATIVE_SIBLING_POSITIVE_RR_NORM_AUTHORITY_R16C_H.csv')),
('R16C-P',PARENT/'RESOLUTION/C3B15_POSITIVE_RR_NORM_AUTHORITY_R16C_P.csv')]
plist=[]
for origin,f in prior_pos_files:
    x=pd.read_csv(f).fillna(''); x['wave']=x['wave'].astype(str); x['positive_authority_origin']=origin; plist.append(x)
prior_pos=pd.concat(plist,ignore_index=True)
assert len(prior_pos)==226
assert not prior_pos.duplicated(key).any()
# Reconstruct all prior positive rows from sealed R11, not from inherited queue totals.
pmi_prior=pd.MultiIndex.from_frame(prior_pos[key].astype(str))
prior_pos_rows=r11[rmi.isin(pmi_prior)].copy()
assert len(prior_pos_rows)==18469
# Parent P queue contains only pre-P 162 / 14270 positive-link workload: exact defect proof.
qpl=q_parent[q_parent.work_family=='T06_RR_NORM_POSITIVE_LINK_REVIEW'].copy()
assert int(qpl.decision_atom_count.sum())==162
assert int(qpl.raw_primitive_row_count_sum.sum())==14270
assert len(prior_pos)-int(qpl.decision_atom_count.sum())==64
assert len(prior_pos_rows)-int(qpl.raw_primitive_row_count_sum.sum())==4199
p_repair=prior_pos[prior_pos.positive_authority_origin=='R16C-P'].groupby(['source_family','wave']).size().rename('missing_positive_link_atoms').reset_index()
p_rows=prior_pos_rows[pd.MultiIndex.from_frame(prior_pos_rows[key].astype(str)).isin(pd.MultiIndex.from_frame(prior_pos[prior_pos.positive_authority_origin=='R16C-P'][key].astype(str)))]
p_repair=p_repair.merge(p_rows.groupby(['source_family','wave']).size().rename('missing_positive_link_rows').reset_index(),on=['source_family','wave'],how='left')
p_repair['repair_disposition']='RESTORE_TO_CENTRAL_T06_LINK_REVIEW_QUEUE__SEMANTIC_AUTHORITY_UNCHANGED'
p_repair.to_csv(ROOT/'PARENT_CORRECTION/R16C_P_MISSING_POSITIVE_LINK_QUEUE_REPAIR_R16C_Q.csv',index=False)

# ---- Cumulative positive authority + link review reconstruction through Q ----
qpos=pos.copy(); qpos['positive_authority_origin']='R16C-Q'
all_pos=pd.concat([prior_pos,qpos],ignore_index=True)
assert len(all_pos)==425
assert not all_pos.duplicated(key).any()
# No new negative may collide with any governed positive semantic identity, even cross-wave.
assert set(neg.semantic_unit_id).isdisjoint(set(prior_pos.semantic_unit_id))
assert not (pd.concat([pos.assign(_d='P'),neg.assign(_d='N')]).groupby('semantic_unit_id')._d.nunique()>1).any()
all_pos.to_csv(ROOT/'PROVENANCE/CUMULATIVE_POSITIVE_RR_NORM_AUTHORITY_THROUGH_R16C_Q.csv',index=False)
allpmi=pd.MultiIndex.from_frame(all_pos[key].astype(str))
all_pos_rows=r11[rmi.isin(allpmi)].copy()
assert len(all_pos_rows)==28130
all_pos_rows.to_csv(ROOT/'QUEUE/CUMULATIVE_T06_RR_NORM_POSITIVE_LINK_REVIEW_ROWS_R16C_Q.csv.gz',index=False,compression='gzip')

# ---- Successor central queue reconstructed, not incrementally patched ----
# Keep pair blockers and T07 exactly as P. Rebuild T06 role blockers from residual 390 and cumulative positive link review from 425.
static=q_parent[q_parent.work_family.isin(['PAIR_AUTHORITY_BLOCKER','T07_GOVERNMENT_SCOPE_NAMING'])].copy()
# residual blocker rows exact from child and R11
cmi=pd.MultiIndex.from_frame(child[key].astype(str)); child_r11=r11[rmi.isin(cmi)].copy(); assert len(child_r11)==25920
parent_block=q_parent[q_parent.work_family=='T06_NORM_ROLE_BLOCKER'].copy()
block_rows=[]
for (sf,wv),g in child.groupby(['source_family','wave']):
    src=parent_block[(parent_block.source_family==sf)&(parent_block.wave==str(wv))]
    assert len(src)==1,(sf,wv,len(src))
    row=src.iloc[0].copy()
    row['decision_atom_count']=len(g)
    rr=child_r11[(child_r11.source_family==sf)&(child_r11.wave==str(wv))]
    row['raw_primitive_row_count_sum']=len(rr)
    # Preserve workbench member context; planning metric remains scheduling-only and is reset to simple role-decision burden.
    row['planning_effort_units']=round(0.25*len(g),6)
    row['packet_statuses_json']='["C3B16_PARTIAL_ROLE_AUTHORITY__RESIDUAL_RR_NORM_REVIEW"]'
    row['authority_ceilings_json']='["NO_T06_ABSENCE_CLAIM__RESIDUAL_RELATIVE_NORM_ROLE_UNRESOLVED"]'
    block_rows.append(row)
block_q=pd.DataFrame(block_rows,columns=q_parent.columns)
assert len(block_q)==31
assert int(block_q.decision_atom_count.sum())==390
assert int(block_q.raw_primitive_row_count_sum.sum())==25920
# consolidated positive-link queue, one source-wave packet each
# exact implementation count from R10A member-complete mapping of cumulative positives
sp_allp=sp[spmi.isin(allpmi)].copy(); assert sp_allp[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==425
link_rows=[]
for (sf,wv),g in all_pos.groupby(['source_family','wave']):
    rr=all_pos_rows[(all_pos_rows.source_family==sf)&(all_pos_rows.wave==str(wv))]
    impct=sp_allp[(sp_allp.source_family==sf)&(sp_allp.wave==str(wv))].question_implementation_id.nunique()
    link_rows.append({
        'packet_id':f'R16C-Q-CUMULATIVE-NORM-LINK::{sf}::{wv}',
        'source_family':sf,'wave':str(wv),'work_family':'T06_RR_NORM_POSITIVE_LINK_REVIEW',
        'execution_lane':'VOZHD_CENTRAL__T06_RELATION_LINK_ADJUDICATION','rule_hypotheses':'T06',
        'decision_atom_count':len(g),'raw_primitive_row_count_sum':len(rr),'member_implementation_count':impct,
        'planning_effort_units':round(0.25*len(g),6),
        'packet_statuses_json':'["RR_NORM_GOVERNED_POSITIVE__RELATION_LINK_REVIEW_REQUIRED__CUMULATIVE_THROUGH_R16C_Q"]',
        'authority_ceilings_json':'["NO_T06_RELATION_AUTHORITY_YET"]'})
link_q=pd.DataFrame(link_rows,columns=q_parent.columns)
assert len(link_q)==29
assert int(link_q.decision_atom_count.sum())==425
assert int(link_q.raw_primitive_row_count_sum.sum())==28130
q2=pd.concat([static,block_q,link_q],ignore_index=True)
q2=q2.sort_values(['work_family','source_family','wave','packet_id']).reset_index(drop=True)
assert len(q2)==116
assert int(q2.decision_atom_count.sum())==32707
assert int(q2.raw_primitive_row_count_sum.sum())==2319305
assert int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.sum())==31880
assert int(q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12
q2.to_csv(ROOT/'QUEUE/R16C_Q_VOZHD_CENTRAL_QUEUE_SUCCESSOR.csv',index=False)
# Queue delta report explicitly distinguishes P accounting repair from Q semantic closure.
queue_delta=pd.DataFrame([
 {'stage':'R16C-P_REPORTED_QUEUE','containers':len(q_parent),'atoms':int(q_parent.decision_atom_count.sum()),'raw_rows':int(q_parent.raw_primitive_row_count_sum.sum())},
 {'stage':'R16C-P_CORRECTED_QUEUE','containers':len(static)+len(parent_block)+len(all_pos[all_pos.positive_authority_origin!='R16C-Q'].groupby(['source_family','wave'])),'atoms':32912,'raw_rows':2334075},
 {'stage':'R16C-Q_SUCCESSOR_QUEUE','containers':len(q2),'atoms':32707,'raw_rows':2319305}
])
queue_delta.to_csv(ROOT/'PARENT_CORRECTION/R16C_P_TO_Q_CENTRAL_QUEUE_ACCOUNTING_DELTA.csv',index=False)

# ---- Source-wave accounting for current closure ----
acct_dec=pd.concat([pos.groupby(['source_family','wave']).size().rename('positive_rr_norm_decisions'),neg.groupby(['source_family','wave']).size().rename('negative_rr_norm_decisions')],axis=1).fillna(0).astype(int)
acct_rows=pd.concat([pos_rows.groupby(['source_family','wave']).size().rename('transferred_link_rows'),neg_rows.groupby(['source_family','wave']).size().rename('retired_primitive_rows')],axis=1).fillna(0).astype(int)
acct=acct_dec.join(acct_rows,how='outer').fillna(0).astype(int).reset_index(); acct.to_csv(ROOT/'RESOLUTION/C3B16_SOURCE_WAVE_ACCOUNTING_R16C_Q.csv',index=False)

# Repeated semantic-ID audit and conflict audit.
dup=child[child.duplicated('semantic_unit_id',keep=False)].sort_values(['semantic_unit_id','source_family','wave'])
dup.to_csv(ROOT/'PROVENANCE/C3B16_REPEATED_SEMANTIC_ID_AUDIT_R16C_Q.csv',index=False)
conf=pd.DataFrame(columns=['semantic_unit_id','conflict'])
conf.to_csv(ROOT/'PROVENANCE/C3B16_POSITIVE_NEGATIVE_SEMANTIC_ID_CONFLICT_AUDIT_R16C_Q.csv',index=False)

# ---- Doctrine ----
(ROOT/'PROVENANCE/C3B16_DOCTRINE.md').write_text('''# C3b16 doctrine — large-batch non-proposition RR_NORM adjudication + R16C-P queue repair

This checkpoint adjudicates **404 / 794** parent RR_NORM decisions in one governed batch: **199 positive** and **205 negative**. It does not touch the **243** proposition-boundary decisions preserved from R16C-P.

Positive RR_NORM requires governed semantics that function as a norm/approval/preference/acceptance/rejection/responsibility/criterion or an explicit approval evaluation of a proposed social/political form. Generic liking/favorability/affinity remains fail-closed because the ontology's approval shore does not license collapsing affect into norm authority without a narrower ruling.

Negative RR_NORM requires governed semantics that are descriptive trust/confidence, state/capacity/performance, expectation, experience, personal salience/importance, causal-impact appraisal, or epistemic reliance rather than a norm/obligation/approval shore. The Q7112 causal-necessity control remains negative: modal necessity language is not automatically normative.

`social acceptance/tolerance` labels are not trusted mechanically: the seven residual EVS rows under that label are immigration-effect beliefs and are closed negative on governed content, not on the label.

Exact decision identity remains `(source_family, wave, semantic_unit_id)`. Member-complete proof permits a decision to map to multiple exact implementations in one source-wave; this checkpoint has 404 decisions represented by 407 exact source-reviewed implementations.

R16C-P semantic adjudication remains valid, but its successor central queue omitted the 64 newly positive RR_NORM link-review atoms and 4,199 link rows. Its residual blocker raw-row total was also 16 rows below exact sealed-R11 reconstruction (Asian Barometer W4 +6, W5 +2, LiTS IV +8). R16C-Q repairs both accounting defects append-only and reconstructs the T06 blocker and cumulative positive-link queues from governed decision authority plus sealed R11, rather than trusting inherited totals.

Positive RR_NORM does not emit a T06 relation. All positive primitive rows remain explicit actor-target-action link-review obligations. Negative RR_NORM retires only the impossible norm-shore path.
''')

# ---- Report/status/pointers ----
status={
'checkpoint':'R16C-Q','subtask':'#18B-C3b16 large-batch non-proposition RR_NORM adjudication plus R16C-P central-queue accounting repair',
'parent_residual':794,'positive_rr_norm_closed':199,'negative_rr_norm_closed':205,'total_role_decisions_closed':404,'residual_rr_norm':390,
'proposition_boundary_preserved':243,'nonproposition_boundary_remaining':147,
'positive_link_rows_transferred_current':9661,'negative_primitive_rows_retired_current':14770,'blocked_rows_removed_current':24431,
'c3_total_role_adjudicated':2729,'c3_parent':3119,'c3_percent':round(2729/3119*100,4),'c3_negative_rr_norm':2304,'c3_positive_rr_norm':425,'c3_positive_link_rows_total':28130,
't06_blocked_primitive_rows_parent_reported':50335,'t06_blocked_primitive_rows_parent_reconstructed':50351,'t06_blocked_primitive_rows_successor':25920,
'r16c_p_queue_missing_positive_atoms_repaired':64,'r16c_p_queue_missing_positive_rows_repaired':4199,
'central_parent_reported_containers':114,'central_parent_reported_atoms':32848,'central_parent_corrected_atoms':32912,
'central_successor_containers':116,'central_successor_atoms':32707,'central_successor_raw_rows':2319305,
'worker_packs_changed':False,'job3_authorized':False,
'next':'C3b17 attack the 390 residual as two finite fronts: 243 proposition boundary + 147 non-proposition approval/importance/fairness/legacy edge cases; keep large-batch cadence.'}
json.dump(status,open(ROOT/'CURRENT_STATUS_R16C_Q.json','w'),indent=2)
report=f'''# R16C-Q — #18B-C3b16 large-batch RR_NORM closure + R16C-P queue repair

## Semantic closure
- Parent residual: **794**.
- Closed positive RR_NORM: **199**.
- Closed negative RR_NORM: **205**.
- Total closed in this batch: **404**.
- Residual: **390** = **243** preserved proposition-boundary + **147** non-proposition edge cases.
- Current positive rows transferred to T06 actor-target-action link review: **9,661**.
- Current negative impossible norm-shore rows retired: **14,770**.
- R16C-P reported blocked primitive surface: **50,335**; exact parent reconstruction: **50,351**.
- R16C-Q blocked primitive surface after this batch: **25,920**.
- C3 adjudicated **2,729 / 3,119 = {2729/3119*100:.2f}%**.
- Cumulative negative RR_NORM: **2,304**.
- Cumulative positive RR_NORM: **425**, preserving **28,130** link-review rows.

## R16C-P central-queue accounting repair
R16C-P's semantic authority was correct, but its successor queue had two accounting-only defects: it omitted the **64** newly positive RR_NORM link-review atoms and their **4,199** transferred rows, and its residual blocker raw-row totals understated sealed-R11 reconstruction by **16 rows** (Asian Barometer W4 +6, W5 +2, LiTS IV +8). The reported central atom count **32,848** was therefore understated by 64. R16C-Q reconstructs both T06 queue families from governed decision authority + sealed R11 rather than inherited arithmetic.

- Corrected R16C-P central atoms: **32,912**.
- R16C-Q successor central atoms: **32,707**.
- R16C-Q successor containers: **116**.
- The semantic batch removes **205** central atoms (the negative closures); the **199** positive closures transfer to relation-link review and therefore remain central work.

## Family action summary
{summary.to_markdown(index=False)}

Worker packs unchanged. Job 3 **NOT AUTHORIZED**.
'''
(ROOT/'R16C_Q_CENTRAL_CLOSURE_REPORT.md').write_text(report)
pointer=f'''# ACTIVE EXECUTION POINTER — R16C-Q

Canonical floor: `CHECKPOINT_R16C_Q_20260812`.

Current state: C3 RR_NORM **2,729 / 3,119 = {2729/3119*100:.2f}% adjudicated**; residual **390**.

C3b16 closed **404** decisions in one governed batch (**199 positive / 205 negative**) and repaired the R16C-P central-queue accounting omission for **64 positive link-review atoms / 4,199 rows** without changing R16C-P semantic authority.

Next execution: **C3b17 — attack the remaining 390 as two finite fronts: 243 proposition-boundary decisions and 147 non-proposition approval/importance/fairness/legacy edge cases. Maintain large-batch cadence.**

Hard invariants:
- exact decision key = `(source_family, wave, semantic_unit_id)`;
- semantic-ID-only removal/keying is forbidden;
- member-complete proof may be one-to-many in exact implementations;
- affect/favorability is not silently collapsed into RR_NORM approval;
- positive RR_NORM transfers to link review; it never directly emits T06 relation authority;
- worker packs remain sealed; Job 3 not authorized.
'''
(ROOT/'ACTIVE_EXECUTION_POINTER.md').write_text(pointer)
ledger=f'''# ACTIVE PROGRESS LEDGER — after R16C-Q

- Governing 25-item checklist: **9/25 DONE**; #18 active.
- #18A worker-pack construction: DONE, packs sealed and untouched.
- #18B central prerequisite campaign: ACTIVE.
- C3 RR_NORM shore: **2,729 / 3,119 ({2729/3119*100:.2f}%) adjudicated**.
- Residual RR_NORM decisions: **390**.
- Negative RR_NORM: **2,304**.
- Positive RR_NORM: **425**, preserving **28,130** link-review rows.
- T06 input-authority blocked primitive surface: **25,920 rows** (exact sealed-R11 reconstruction).
- Central queue: **116 containers / 32,707 atoms** after repairing the R16C-P positive-link queue omission.
- Worker packs: unchanged.
- Job 3: NOT AUTHORIZED.
- Next: C3b17 large-batch residual attack.
'''
(ROOT/'ACTIVE_PROGRESS_LEDGER.md').write_text(ledger)

# Copy code.
shutil.copy('/mnt/data/candidate_r16c_q.py',ROOT/'CODE/candidate_r16c_q.py')
shutil.copy('/mnt/data/build_r16c_q.py',ROOT/'CODE/build_r16c_q.py')

# ---- Validation / hostile QA ----
checks=[]
def ck(name,cond,detail=''):
    checks.append({'check':name,'pass':bool(cond),'detail':str(detail)})
ck('parent_794',len(res)==794,len(res)); ck('positive_199',len(pos)==199,len(pos)); ck('negative_205',len(neg)==205,len(neg)); ck('selected_404',len(selected)==404,len(selected)); ck('child_390',len(child)==390,len(child)); ck('prop_boundary_243_survives',pd.MultiIndex.from_frame(child[key].astype(str)).isin(mi_pb).sum()==243)
ck('p_n_disjoint',set(map(tuple,pos[key].astype(str).values.tolist())).isdisjoint(set(map(tuple,neg[key].astype(str).values.tolist()))))
ck('407_exact_impls',len(proof)==407,len(proof)); ck('404_decisions_in_proof',proof[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==404); ck('all_source_reviewed',(proof.authority_status=='source_reviewed').all(),proof.authority_status.value_counts().to_dict()); ck('source_authority_nonempty',proof.source_authority.astype(str).str.strip().ne('').all())
ck('pos_rows_9661',len(pos_rows)==9661,len(pos_rows)); ck('neg_rows_14770',len(neg_rows)==14770,len(neg_rows)); ck('row_sets_disjoint',set(pos_rows.opportunity_id).isdisjoint(set(neg_rows.opportunity_id)))
ck('prior_positive_226',len(prior_pos)==226,len(prior_pos)); ck('prior_positive_rows_18469',len(prior_pos_rows)==18469,len(prior_pos_rows)); ck('parent_queue_positive_atoms_162',int(qpl.decision_atom_count.sum())==162,int(qpl.decision_atom_count.sum())); ck('parent_queue_missing_64',len(prior_pos)-int(qpl.decision_atom_count.sum())==64); ck('parent_queue_missing_rows_4199',len(prior_pos_rows)-int(qpl.raw_primitive_row_count_sum.sum())==4199)
ck('cum_positive_425',len(all_pos)==425,len(all_pos)); ck('cum_positive_rows_28130',len(all_pos_rows)==28130,len(all_pos_rows)); ck('new_negative_no_prior_positive_semid',set(neg.semantic_unit_id).isdisjoint(set(prior_pos.semantic_unit_id))); ck('q_no_pos_neg_semid_conflict',not (pd.concat([pos.assign(_d='P'),neg.assign(_d='N')]).groupby('semantic_unit_id')._d.nunique()>1).any())
# R6 hostile: no negative row may carry an R6 role string suggestive of T06 norm/support authority.
neg_r6_bad=neg[neg.r6_member_roles_json.astype(str).str.contains('norm|duty|support|approval|principle|commitment|sacrifice|cost',case=False,regex=True)]
ck('negative_no_normative_r6_role_strings',len(neg_r6_bad)==0,len(neg_r6_bad))
# Required semantic controls.
ck('q7112_negative_control',len(neg[(neg.source_family=='Arab Barometer')&(neg.wave=='II')&(neg.source_variable_code=='q7112')])==1)
ck('social_tolerance_label_content_checked',(neg.sem__measured_predicate=='social acceptance/tolerance').sum()==7,(neg.sem__measured_predicate=='social acceptance/tolerance').sum())
ck('affect_boundary_preserved',len(affect)>=51,len(affect))
ck('state_economic_intervention_ambiguous_preserved',(child.sem__measured_predicate=='state economic intervention/role').sum()==6,(child.sem__measured_predicate=='state economic intervention/role').sum())
ck('fairness_assessment_preserved',(child.sem__measured_predicate=='fairness_assessment').sum()==6)
ck('electoral_fairness_preserved',(child.sem__measured_predicate=='electoral fairness evaluation').sum()==6)
ck('block_q_31',len(block_q)==31,len(block_q)); ck('block_atoms_390',int(block_q.decision_atom_count.sum())==390,int(block_q.decision_atom_count.sum())); ck('block_rows_25920',int(block_q.raw_primitive_row_count_sum.sum())==25920,int(block_q.raw_primitive_row_count_sum.sum())); ck('link_q_29',len(link_q)==29,len(link_q)); ck('link_atoms_425',int(link_q.decision_atom_count.sum())==425,int(link_q.decision_atom_count.sum())); ck('link_rows_28130',int(link_q['raw_primitive_row_count_sum'].sum())==28130,int(link_q['raw_primitive_row_count_sum'].sum()))
ck('queue_containers_116',len(q2)==116,len(q2)); ck('queue_atoms_32707',int(q2.decision_atom_count.sum())==32707,int(q2.decision_atom_count.sum())); ck('queue_raw_2319305',int(q2.raw_primitive_row_count_sum.sum())==2319305,int(q2.raw_primitive_row_count_sum.sum())); ck('pair_static_31880',int(q2[q2.work_family=='PAIR_AUTHORITY_BLOCKER'].decision_atom_count.sum())==31880); ck('t07_static_12',int(q2[q2.work_family=='T07_GOVERNMENT_SCOPE_NAMING'].decision_atom_count.sum())==12)
validation={'checkpoint':'R16C-Q','status':'PASS' if all(x['pass'] for x in checks) else 'FAIL','checks':checks,'passed':sum(x['pass'] for x in checks),'total':len(checks)}
json.dump(validation,open(ROOT/'VALIDATION/VALIDATION_RESULT_R16C_Q.json','w'),indent=2)
if validation['status']!='PASS':
    print(json.dumps(validation,indent=2)); raise SystemExit(2)
# hostile QA separate, focused on release-boundary failures
hostile=[]
def h(name,cond,detail=''): hostile.append({'attack':name,'pass':bool(cond),'detail':str(detail)})
h('no_semantic_id_only_crosswave_bleed',not (pd.concat([pos.assign(_d='P'),neg.assign(_d='N')]).groupby('semantic_unit_id')._d.nunique()>1).any())
h('proposition_boundary_not_touched',pd.MultiIndex.from_frame(selected[key].astype(str)).isin(mi_pb).sum()==0)
h('affect_not_laundered_into_norm',not selected.sem__measured_predicate.isin(affect_preds).any(),selected[selected.sem__measured_predicate.isin(affect_preds)].sem__measured_predicate.value_counts().to_dict())
h('trust_placeholders_negative_not_positive',not pos.sem__measured_predicate.str.contains('SOURCE_FIRST_SEMANTIC_CORE').any())
h('social_tolerance_label_not_mechanically_positive',not pos.sem__measured_predicate.eq('social acceptance/tolerance').any())
h('q7112_modal_necessity_not_promoted',len(neg[(neg.source_variable_code=='q7112')])==1)
h('r16c_p_positive_authority_preserved_exact',len(prior_pos[prior_pos.positive_authority_origin=='R16C-P'])==64)
h('r16c_p_queue_defect_repaired_not_semantics_changed',int(p_repair.missing_positive_link_atoms.sum())==64 and int(p_repair.missing_positive_link_rows.sum())==4199)
h('positive_transfers_not_relations',(pos_out.authority_ceiling.str.contains('LINK_STILL_REQUIRES').all()))
h('negative_only_retires_norm_shore',(neg_out.authority_ceiling.str.contains('NO_RELATION_ABSENCE_CLAIM').all()))
h('member_complete_proof_all_selected',proof[['source_family','wave','sem__audit_unit_id']].drop_duplicates().shape[0]==404)
h('multi_impl_decisions_preserved',(member_counts.exact_implementation_count>1).sum()==3,(member_counts.exact_implementation_count>1).sum())
h('job3_false',status['job3_authorized'] is False)
h('worker_packs_unchanged',status['worker_packs_changed'] is False)
host={'checkpoint':'R16C-Q','status':'PASS' if all(x['pass'] for x in hostile) else 'FAIL','attacks':hostile,'passed':sum(x['pass'] for x in hostile),'total':len(hostile)}
json.dump(host,open(ROOT/'VALIDATION/R16C_Q_HOSTILE_QA.json','w'),indent=2)
if host['status']!='PASS': print(json.dumps(host,indent=2)); raise SystemExit(3)

# ---- Manifest + ZIP ----
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
# manifest excludes itself and zip
rows=[]
for f in sorted(ROOT.rglob('*')):
 if f.is_file() and f.name!='SHA256_MANIFEST_R16C_Q.csv': rows.append({'relative_path':str(f.relative_to(ROOT)),'sha256':sha(f),'size_bytes':f.stat().st_size})
pd.DataFrame(rows).to_csv(ROOT/'SHA256_MANIFEST_R16C_Q.csv',index=False)
# final zip deterministic-ish: fixed ordering, no cache junk
zip_path=Path('/mnt/data/Rawlsing_R10K_S14_Central_Closure_Checkpoint_R16C_Q_20260812.zip')
if zip_path.exists(): zip_path.unlink()
with zipfile.ZipFile(zip_path,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for f in sorted(ROOT.rglob('*')):
  if f.is_file(): z.write(f,arcname=str(f.relative_to(ROOT)))
zipsha=sha(zip_path)
Path(str(zip_path)+'.sha256').write_text(f'{zipsha}  {zip_path.name}\n')
print(json.dumps({'validation':validation['status'],'validation_checks':f"{validation['passed']}/{validation['total']}",'hostile':host['status'],'hostile_checks':f"{host['passed']}/{host['total']}",'zip':str(zip_path),'sha256':zipsha,'size':zip_path.stat().st_size},indent=2))
