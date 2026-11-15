from pathlib import Path
import pandas as pd,json,hashlib,re,collections,sys,zipfile,os
R=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811')
R10=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811')
R14=Path('/mnt/data/live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/R14_SOURCE_NATIVE_AUTHORITY_FINAL_708047.json')
R6=Path('/mnt/data/live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/INTER_QUESTION_RELATION_AUTHORITY_R2.csv')
checks=[];errs=[]
def ck(n,c,d=None): checks.append({'check':n,'pass':bool(c),'detail':d}); errs.append(n) if not c else None
def jl(x):
 if pd.isna(x) or x=='':return []
 try:return json.loads(x)
 except:return []
sp10=pd.read_csv(R10/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz',dtype=str,low_memory=False)
sp=pd.read_csv(R/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz',dtype=str,low_memory=False)
ck('rows_18276',len(sp)==18276,len(sp));ck('unique_ids',sp.question_implementation_id.nunique()==18276,sp.question_implementation_id.nunique())
ck('r10_columns_prefix',list(sp.columns[:len(sp10.columns)])==list(sp10.columns),(len(sp10.columns),len(sp.columns)))
# exact parent conservation
mut=[]
for c in sp10.columns:
 if not sp[c].fillna('__NA__').astype(str).equals(sp10[c].fillna('__NA__').astype(str)):mut.append(c)
ck('zero_R10_parent_field_mutations',not mut,mut[:10])
# R14 parent hetero schema independent audit
d=json.load(open(R14)); objs=d['objects'];ck('r14_object_count_730',len(objs)==730,len(objs))
ordered=[o for o in objs if o.get('ordered_members')];ck('ordered_schema_objects_296',len(ordered)==296,len(ordered))
# current object index
cw=pd.read_csv(R/'R14/R14_COMPREHENSIVE_SOURCE_OBJECT_CROSSWALK_R10A.csv',dtype=str).fillna('')
ck('crosswalk_730',len(cw)==730,len(cw)); ck('all_r14_objects_once',cw.object_id.nunique()==730,cw.object_id.nunique())
ck('ordered_objects_all_current_mapped',((cw.extraction_methods.str.contains('ordered_members')) & (pd.to_numeric(cw.mapped_implementation_count)>0)).sum()==296,int(((cw.extraction_methods.str.contains('ordered_members')) & (pd.to_numeric(cw.mapped_implementation_count)>0)).sum()))
ck('mapped_objects_724',int((pd.to_numeric(cw.mapped_implementation_count)>0).sum())==724,int((pd.to_numeric(cw.mapped_implementation_count)>0).sum()))
ck('no_map_objects_6',int((pd.to_numeric(cw.mapped_implementation_count)==0).sum())==6,int((pd.to_numeric(cw.mapped_implementation_count)==0).sum()))
ck('full_objects_696',int((cw.mapping_status=='FULL_CURRENT_IMPLEMENTATION_CROSSWALK').sum())==696,int((cw.mapping_status=='FULL_CURRENT_IMPLEMENTATION_CROSSWALK').sum()))
ck('partial_objects_28',int((cw.mapping_status=='PARTIAL_CURRENT_IMPLEMENTATION_CROSSWALK').sum())==28,int((cw.mapping_status=='PARTIAL_CURRENT_IMPLEMENTATION_CROSSWALK').sum()))
ck('unresolved_codes_198',int(pd.to_numeric(cw.unresolved_member_code_count).sum())==198,int(pd.to_numeric(cw.unresolved_member_code_count).sum()))
# independent q833 source code exact lookup
q=cw[cw.object_id=='LITS-IV-GROUP-Q833'];ck('q833_object_present',len(q)==1,len(q))
if len(q):
 mids=set(jl(q.iloc[0].mapped_implementation_ids_json)); h=sp[sp.question_implementation_id.isin(mids)]
 ck('q833_maps_three',len(mids)==3,len(mids));ck('q833_codes_exact',set(h.source_variable_code.str.lower())=={'q833a','q833b','q833c'},sorted(h.source_variable_code.tolist()))
# corrected spine object memberships match object ledger aggregate
impl_to_objs=collections.defaultdict(set)
for _,r in cw.iterrows():
 for iid in jl(r.mapped_implementation_ids_json): impl_to_objs[iid].add(r.object_id)
mismatch=[]
for _,r in sp[['question_implementation_id','r14c_object_ids_json']].iterrows():
 if set(jl(r.r14c_object_ids_json))!=impl_to_objs.get(r.question_implementation_id,set()):mismatch.append(r.question_implementation_id)
ck('spine_r14c_exact_from_object_ledger',not mismatch,len(mismatch))
ck('r14c_member_rows_4853',int((pd.to_numeric(sp.r14c_object_count)>0).sum())==4853,int((pd.to_numeric(sp.r14c_object_count)>0).sum()))
# old vs corrected delta explicit
ck('r14c_expands_r10',int((pd.to_numeric(sp.r14c_object_count)>0).sum())>int((pd.to_numeric(sp.r14_object_count)>0).sum()),(int((pd.to_numeric(sp.r14_object_count)>0).sum()),int((pd.to_numeric(sp.r14c_object_count)>0).sum())))
# every corrected R14 ID exists in parent
parent_oids={o['object_id'] for o in objs}; bad=[]
for x in sp.r14c_object_ids_json:
 for o in jl(x):
  if o not in parent_oids:bad.append(o)
ck('no_invented_r14_object_ids',not bad,bad[:10])
# R6 source structure refs: 341/342 unique in R14, lone GSS crosswalk external
r6=pd.read_csv(R6,dtype=str).fillna(''); refs=[]
for _,r in r6.iterrows():
 for sid in jl(r.source_structure_ids):refs.append(sid)
uniq=set(refs); found=uniq&parent_oids; miss=uniq-parent_oids
ck('r6_source_structure_refs_342',len(uniq)==342,len(uniq));ck('r6_r14_refs_341',len(found)==341,len(found));ck('r6_only_external_structure_expected',miss=={'GSS-1984-ABORTION-BATTERY-SOURCE-CROSSWALK'},sorted(miss))
# all T03-T11 exact R6 members still on spine
types={'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE'}
ids=set(sp.question_implementation_id); can=r6[r6.relation_type.isin(types)]; missing=[]
for _,r in can.iterrows():
 for iid in [x for x in jl(r.member_question_implementation_ids) if x]:
  if iid not in ids:missing.append((r.relation_authority_id,iid))
ck('117_canary_relations',len(can)==117,len(can));ck('all_canary_exact_members_on_spine',not missing,missing[:10])
# known canary source structure recovery materially improved: T03/T05/T07/T08 common R14; T10 any overlap all
impl_objs=impl_to_objs
stats={}
for t,g in can.groupby('relation_type'):
 common=anyov=0
 for _,r in g.iterrows():
  mids=[x for x in jl(r.member_question_implementation_ids) if x]; sets=[impl_objs.get(x,set()) for x in mids]
  if sets and all(sets) and set.intersection(*sets):common+=1
  if len(sets)>=2 and any(sets[i]&sets[j] for i in range(len(sets)) for j in range(i+1,len(sets))):anyov+=1
 stats[t]={'relations':len(g),'common_r14_object':common,'any_r14_overlap':anyov}
ck('T03_all_common_R14',stats['GENERAL_PRINCIPLE_SPECIFIC_APPLICATION']['common_r14_object']==8,stats['GENERAL_PRINCIPLE_SPECIFIC_APPLICATION'])
ck('T05_all_common_R14',stats['COMMITMENT_PERSONAL_COST']['common_r14_object']==3,stats['COMMITMENT_PERSONAL_COST'])
ck('T07_all_common_R14',stats['GENERAL_TARGET_SUBTARGET']['common_r14_object']==6,stats['GENERAL_TARGET_SUBTARGET'])
ck('T08_all_common_R14',stats['INSTITUTION_CLASS_DIFFERENTIATION']['common_r14_object']==20,stats['INSTITUTION_CLASS_DIFFERENTIATION'])
ck('T10_all_any_R14_overlap',stats['TARGET_CONDITION_MATRIX']['any_r14_overlap']==14,stats['TARGET_CONDITION_MATRIX'])
# governance files
st=json.load(open(R/'CURRENT_STATUS_R10A.json'));ck('job3_false',st['job3_authorized'] is False);ck('item2_done',st['item_2_unified_18276_spine'].startswith('DONE'))
ptr=open(R/'ACTIVE_EXECUTION_POINTER.md').read();ck('pointer_uses_r14c','r14c_*' in ptr);ck('pointer_job3_blocked','NOT AUTHORIZED' in ptr)
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks,'canary_source_structure_stats':stats}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R10A.json','w'),indent=2)
print(json.dumps(res,indent=2))
sys.exit(1 if errs else 0)
