from pathlib import Path
import pandas as pd,json,collections,itertools,hashlib,sys
B=Path('/mnt/data');R=Path(__file__).resolve().parents[1]
SP=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10A.csv.gz';PAIR=B/'r9_full/PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz';CW=B/'Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10A_20260811/R14/R14_COMPREHENSIVE_SOURCE_OBJECT_CROSSWALK_R10A.csv';R6P=B/'live_parents/o12/Rawlsing_R10K_O12_Job3_Candidate_Denominator_Completeness_Repair_R2_20260811/PARENTS/INTER_QUESTION_RELATION_AUTHORITY_R2.csv';R3=B/'r3_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R3_20260811/NARROWING/T07_P2_TARGET_RELATION_DISPOSITION_R3.csv';R2N=B/'r11_inputs/t06_r2/T06_NORM_SHORE_ACCOUNTING_R2.csv'
checks=[];errs=[]
def ck(n,c,d=None):checks.append({'check':n,'pass':bool(c),'detail':d});errs.append(n) if not c else None
def jl(x):
 if pd.isna(x) or x=='':return []
 try:return json.loads(x)
 except:return []
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for z in iter(lambda:f.read(1<<20),b''):h.update(z)
 return h.hexdigest()
sp=pd.read_csv(SP,dtype=str,low_memory=False);cw=pd.read_csv(CW,dtype=str).fillna('')
# parent pins
prov=json.load(open(R/'PROVENANCE/PARENT_PINS_R11.json'))
ck('r10a_parent_hash',prov['R10A_spine_sha256']==sha(SP));ck('r9_pair_hash',prov['R9_pair_sha256']==sha(PAIR));ck('r14_crosswalk_hash',prov['R14_crosswalk_sha256']==sha(CW))
# source object accounting
soa=pd.read_csv(R/'SOURCE_OBJECTS/R11_ALL_730_SOURCE_OBJECT_ACCOUNTING.csv',dtype=str);ck('source_objects_730',len(soa)==730,len(soa));ck('source_objects_unique',soa.object_id.nunique()==730,soa.object_id.nunique());exp_multi=int((pd.to_numeric(cw.mapped_implementation_count)>=2).sum());ck('source_multi_598',exp_multi==598,exp_multi);ck('source_multi_accounted',int((soa.opportunity_status=='IN_SOURCE_OPPORTUNITY_LEDGER').sum())==598,int((soa.opportunity_status=='IN_SOURCE_OPPORTUNITY_LEDGER').sum()))
# collision groups independently reconstruct
sem=sp[sp.sem__audit_unit_id.notna()][['source_family','wave','sem__audit_unit_id','sem__canonical_driver_id','sem__canonical_structural_domain_id','sem__canonical_target_id','sem__canonical_role','t08_institution_class','t08_class_mapping_status']].drop_duplicates(['source_family','wave','sem__audit_unit_id'])
vg=sem.dropna(subset=['sem__canonical_driver_id','sem__canonical_structural_domain_id']).groupby(['source_family','wave','sem__canonical_driver_id','sem__canonical_structural_domain_id']).sem__audit_unit_id.nunique();exp_cg=int((vg>=2).sum())
cg=pd.read_csv(R/'SEMANTIC_COLLISIONS/R11_DRIVER_DOMAIN_COLLISION_GROUPS.csv',dtype=str);ck('collision_groups_410',exp_cg==410,exp_cg);ck('collision_output_exact_count',len(cg)==exp_cg,len(cg))
# pair negative-space independent channel reconstruction
unit_objs=collections.defaultdict(set)
for rr in sp[sp.sem__audit_unit_id.notna()][['source_family','wave','sem__audit_unit_id','r14c_object_ids_json']].itertuples(index=False):unit_objs[(rr.source_family,str(rr.wave),rr.sem__audit_unit_id)].update(jl(rr.r14c_object_ids_json))
P=pd.read_csv(PAIR,dtype={'wave':str},low_memory=False,usecols=['pair_id','source_family','wave','unit_a','unit_b','same_driver','same_domain','same_target','lexical_role_recall_signal'])
PO=pd.read_csv(R/'PAIR_ACCOUNTING/R11_ALL_364094_PAIR_MAP_OR_EXCLUSION.csv.gz',dtype={'wave':str},low_memory=False)
ck('pair_rows_364094',len(P)==364094,len(P));ck('pair_output_364094',len(PO)==len(P),len(PO));ck('pair_ids_exact',set(P.pair_id)==set(PO.pair_id),(P.pair_id.nunique(),PO.pair_id.nunique()))
# reconstruct map booleans; common corrected R14 or driver+domain or same-target
mapped=[]
for rr in P.itertuples(index=False):
 common=bool(unit_objs.get((rr.source_family,str(rr.wave),rr.unit_a),set()) & unit_objs.get((rr.source_family,str(rr.wave),rr.unit_b),set()))
 mapped.append(common or (rr.same_driver==1 and rr.same_domain==1) or rr.same_target==1)
exp_map=sum(mapped); got_map=int((PO.pair_disposition=='MAPS_TO_R11_NAMED_RECALL_CHANNEL__NO_RELATION_AUTHORITY').sum())
ck('pair_mapped_count_independent',got_map==exp_map,(got_map,exp_map));ck('pair_mapped_44112',got_map==44112,got_map);ck('pair_excluded_319982',len(PO)-got_map==319982,len(PO)-got_map)
# pair row disposition boolean exact by id order merge
m=PO.set_index('pair_id').pair_disposition.to_dict();bad=0
for rr,ok in zip(P.itertuples(index=False),mapped):
 want='MAPS_TO_R11_NAMED_RECALL_CHANNEL__NO_RELATION_AUTHORITY' if ok else 'INPUT_AUTHORITY_INCOMPLETE__OUTSIDE_NAMED_RECALL_CHANNEL__NO_ABSENCE_CLAIM'
 if m.get(rr.pair_id)!=want:bad+=1
ck('pair_every_row_exact_disposition',bad==0,bad)
# lexical-only excluded survives
lex_excl=0
for rr,ok in zip(P.itertuples(index=False),mapped):
 if rr.lexical_role_recall_signal==1 and not ok:lex_excl+=1
ck('lexical_only_does_not_create_membership',lex_excl>0,lex_excl)
# T06 exhaustive audit
S=sem[['source_family','wave','sem__audit_unit_id']].drop_duplicates();E=sp[sp.o04__central_s2b_disposition=='ACCEPT_ENDPOINT'][['source_family','wave','question_implementation_id']].drop_duplicates();ns=S.groupby(['source_family','wave']).size();es=E.groupby(['source_family','wave']).size();exp_t06=sum(int(n)*int(es.get(k,0)) for k,n in ns.items());T6=pd.read_csv(R/'T06/R11_T06_ALL_SEMANTIC_UNITS_X_O04_ENDPOINT_FULL_ACCOUNTING.csv.gz',dtype=str)
ck('semantic_wave_memberships_4565',len(S)==4565,len(S));ck('accepted_endpoints_2113',len(E)==2113,len(E));ck('t06_full_cross_expected_287513',exp_t06==287513,exp_t06);ck('t06_full_ledger_287513',len(T6)==exp_t06,len(T6));ck('t06_opportunity_ids_unique',T6.opportunity_id.nunique()==len(T6),T6.opportunity_id.nunique())
# by-wave exact cross counts
actual=T6.groupby(['source_family','wave']).size(); mismatch=[]
for k,n in ns.items():
 e=int(es.get(k,0));want=int(n)*e;got=int(actual.get(k,0))
 if want!=got:mismatch.append((k,want,got))
ck('t06_every_wave_cross_product_exact',not mismatch,mismatch[:10])
N=pd.read_csv(R2N,dtype=str).fillna('');r2set=set(zip(N.source_family,N.wave.astype(str),N.sem__audit_unit_id));exp_r2=0
for k,g in N.groupby(['source_family','wave']):exp_r2+=len(g)*int(es.get(k,0))
ck('r2_subset_expected_78334',exp_r2==78334,exp_r2);ck('r2_subset_flag_78334',int((T6.in_r2_norm_shore=='True').sum())==78334,int((T6.in_r2_norm_shore=='True').sum()))
# T07 exact inherited 79 terrain
r3=pd.read_csv(R3,dtype=str);t7=pd.read_csv(R/'T07/R11_T07_P2_TARGET_RELATION_79_ROW_ACCOUNTING.csv',dtype=str);ck('t07_parent_79',len(r3)==79,len(r3));ck('t07_accounting_79',len(t7)==79,len(t7));ck('t07_parent_ids_exact',set(r3.global_semantic_authority_id)==set(t7.global_semantic_authority_id))
# T08 independently reconstruct count from collision groups with >=2 class mapped and >=2 target
exp8=0
for _,g in sem.dropna(subset=['sem__canonical_driver_id','sem__canonical_structural_domain_id']).groupby(['source_family','wave','sem__canonical_driver_id','sem__canonical_structural_domain_id']):
 if g.sem__audit_unit_id.nunique()<2:continue
 h=g[g.t08_institution_class.notna()]
 if len(h)>=2 and h.sem__canonical_target_id.dropna().nunique()>=2:exp8+=1
t8=pd.read_csv(R/'T08/R11_T08_INSTITUTION_CLASS_GROUP_OPPORTUNITIES.csv',dtype=str);ck('t08_groups_52',exp8==52,exp8);ck('t08_output_52',len(t8)==52,len(t8))
# parallel source-object alignments independently
small=cw[(pd.to_numeric(cw.mapped_implementation_count)>=2)&(pd.to_numeric(cw.mapped_implementation_count)<=50)];expA=0
for k,g in small.groupby(['source_family','wave']):
 for size,sg in g.groupby('mapped_implementation_count'):
  n=len(sg);expA+=n*(n-1)//2
A=pd.read_csv(R/'T09_T10/R11_PARALLEL_SOURCE_OBJECT_EQUAL_SIZE_ALIGNMENT_OPPORTUNITIES.csv',dtype=str);ck('parallel_alignment_1718',expA==1718,expA);ck('parallel_output_1718',len(A)==1718,len(A))
# T11 same target multi-role independent
exp11=0
for _,g in sem.dropna(subset=['sem__canonical_target_id']).groupby(['source_family','wave','sem__canonical_target_id']):
 if g.sem__audit_unit_id.nunique()>=2 and g.sem__canonical_role.dropna().nunique()>=2:exp11+=1
T11=pd.read_csv(R/'T11/R11_T11_SAME_TARGET_MULTIROLE_GROUPS.csv',dtype=str);ck('t11_groups_47',exp11==47,exp11);ck('t11_output_47',len(T11)==47,len(T11))
# Canary recovery independently from release channels
obj_sets={r.object_id:set(jl(r.mapped_implementation_ids_json)) for r in cw.itertuples(index=False)};impl_objs=collections.defaultdict(set)
for o,s in obj_sets.items():
 for x in s:impl_objs[x].add(o)
# collision member sets, alignment pairs, t06 same-target semantic unit pairs
cgsets=[(r.source_family,str(r.wave),set(jl(r.semantic_unit_ids_json))) for r in cg.itertuples(index=False)]
alignpairs={tuple(sorted([r.object_a,r.object_b])) for r in A.itertuples(index=False)}
T6S=pd.read_csv(R/'T06/R11_T06_SAME_TARGET_SEMANTIC_PAIR_OPPORTUNITIES.csv',dtype=str);t6pairs={tuple(sorted([r.unit_a,r.unit_b])) for r in T6S.itertuples(index=False)}
r6=pd.read_csv(R6P,dtype=str).fillna('');types={'GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','GOAL_MEANS','COMMITMENT_PERSONAL_COST','NORM_EXPECTED_CONDUCT','GENERAL_TARGET_SUBTARGET','INSTITUTION_CLASS_DIFFERENTIATION','RECIPROCAL_ROLE_REVERSAL','TARGET_CONDITION_MATRIX','COMPLEMENTARY_ROLE_CONVERGENCE'};can=r6[r6.relation_type.isin(types)];recover=[]
for rr in can.itertuples(index=False):
 mids=[x for x in jl(rr.member_question_implementation_ids) if x];mset=set(mids);found=False
 if mids and all(impl_objs.get(x) for x in mids) and set.intersection(*(impl_objs[x] for x in mids)):found=True
 h=sp[sp.question_implementation_id.isin(mids)];units=set(h.sem__audit_unit_id.dropna().astype(str));wave='2006' if rr.source_family=='LiTS' and str(rr.wave)=='I' else str(rr.wave)
 if units and any(sf==rr.source_family and w==wave and units<=uset for sf,w,uset in cgsets):found=True
 if len(units)==2 and tuple(sorted(units)) in t6pairs:found=True
 sids=[x for x in jl(rr.source_structure_ids) if x in obj_sets]
 if len(sids)>=2 and any(tuple(sorted(p)) in alignpairs for p in itertools.combinations(sorted(sids),2)):found=True
 recover.append(found)
ck('canary_relations_117',len(can)==117,len(can));ck('canary_recovery_117_without_override',sum(recover)==117,sum(recover))
# compare emitted canary ledger
CL=pd.read_csv(R/'CANARY/R6_T03_T11_CANARY_RECOVERY_R11.csv',dtype=str);ck('canary_ledger_117',len(CL)==117,len(CL));ck('canary_ledger_all_true',(CL.recovered_without_R6_candidate_overlay=='True').all(),int((CL.recovered_without_R6_candidate_overlay=='True').sum()))
# Rule-specific pair posture: independently reconstruct the release-boundary correction
RP=pd.read_csv(R/'PAIR_ACCOUNTING/R11_T03_T11_RULE_SPECIFIC_PAIR_POSTURE_LEDGER.csv.gz',dtype={'wave':str},low_memory=False)
ck('rule_pair_ledger_364094',len(RP)==364094,len(RP)); ck('rule_pair_ids_exact',set(RP.pair_id)==set(P.pair_id),(RP.pair_id.nunique(),P.pair_id.nunique()))
# align to pair order and derive metadata vectorially
rpo=RP.set_index('pair_id').loc[P.pair_id]
meta=sem.drop_duplicates('sem__audit_unit_id').set_index('sem__audit_unit_id')
ta=P.unit_a.map(meta.sem__canonical_target_id).fillna(''); tb=P.unit_b.map(meta.sem__canonical_target_id).fillna('')
sa=P.unit_a.map(meta.t08_class_mapping_status).fillna(''); sb=P.unit_b.map(meta.t08_class_mapping_status).fillna('')
ca=P.unit_a.map(meta.t08_institution_class).fillna(''); cb=P.unit_b.map(meta.t08_institution_class).fillna('')
both=ta.ne('')&tb.ne(''); same=P.same_target.eq(1); diff=both&ta.ne(tb)
# recall for relative-role rules is common corrected R14 object OR governed same driver+domain collision
common_vec=[]
for rr in P[['source_family','wave','unit_a','unit_b']].itertuples(index=False):
 common_vec.append(bool(unit_objs.get((rr.source_family,str(rr.wave),rr.unit_a),set()) & unit_objs.get((rr.source_family,str(rr.wave),rr.unit_b),set())))
rec=pd.Series(common_vec,index=P.index) | (P.same_driver.eq(1)&P.same_domain.eq(1))
for rid in ['t03','t04','t05','t09','t11']:
 want=pd.Series('INPUT_AUTHORITY_INCOMPLETE__NO_EXHAUSTIVE_RELATIVE_ROLE_ASSIGNMENT__NO_ABSENCE_CLAIM',index=P.index)
 want.loc[rec]='REQUIRES_RELATIVE_ROLE_ADJUDICATION__NAMED_RECALL_CHANNEL'
 got=pd.Series(rpo[rid+'_posture'].values,index=P.index)
 ck(f'{rid}_rule_pair_posture_exact',got.eq(want).all(),int((got!=want).sum()))
want=pd.Series('INPUT_AUTHORITY_INCOMPLETE__TARGET_ALIGNMENT_UNRESOLVED__NO_ABSENCE_CLAIM',index=P.index)
want.loc[both&~same]='TERMINAL_NOT_APPLICABLE__GOVERNED_TARGET_MISMATCH';want.loc[same]='REQUIRES_NORM_CONDUCT_ROLE_ADJUDICATION__GOVERNED_SAME_TARGET'
got=pd.Series(rpo.t06_posture.values,index=P.index);ck('t06_rule_pair_posture_exact',got.eq(want).all(),int((got!=want).sum()))
want=pd.Series('INPUT_AUTHORITY_INCOMPLETE__TARGET_IDENTITY_OR_HIERARCHY_UNRESOLVED__NO_ABSENCE_CLAIM',index=P.index)
want.loc[diff]='INPUT_AUTHORITY_INCOMPLETE__NO_EXHAUSTIVE_TARGET_HIERARCHY_ASSIGNMENT__NO_ABSENCE_CLAIM';want.loc[rec&diff]='REQUIRES_HIERARCHY_ADJUDICATION__NAMED_RECALL_CHANNEL';want.loc[both&ta.eq(tb)]='TERMINAL_NOT_APPLICABLE__SAME_GOVERNED_TARGET'
got=pd.Series(rpo.t07_posture.values,index=P.index);ck('t07_rule_pair_posture_exact',got.eq(want).all(),int((got!=want).sum()))
bm=sa.str.startswith('MAPPED_')&sb.str.startswith('MAPPED_')&ca.ne('')&cb.ne('');ena=sa.isin(['NOT_APPLICABLE_NONINSTITUTION','ACTOR_NOT_INSTITUTION']);enb=sb.isin(['NOT_APPLICABLE_NONINSTITUTION','ACTOR_NOT_INSTITUTION']);rev=sa.str.startswith('REVIEW_REQUIRED')|sb.str.startswith('REVIEW_REQUIRED')
want=pd.Series('INPUT_AUTHORITY_INCOMPLETE__INSTITUTION_CLASS_ELIGIBILITY_NOT_EXHAUSTIVELY_GOVERNED__NO_ABSENCE_CLAIM',index=P.index)
want.loc[rev]='INPUT_AUTHORITY_INCOMPLETE__INSTITUTION_CLASS_MAPPING_REVIEW_REQUIRED';want.loc[bm&diff]='REQUIRES_INSTITUTION_CLASS_RELATION_ADJUDICATION__MAPPINGS_GOVERNED';want.loc[(ena|enb)&~rev]='TERMINAL_NOT_APPLICABLE__EXPLICIT_NONINSTITUTION_MEMBER';want.loc[both&ta.eq(tb)]='TERMINAL_NOT_APPLICABLE__SAME_EXACT_INSTITUTION_TARGET'
got=pd.Series(rpo.t08_posture.values,index=P.index);ck('t08_rule_pair_posture_exact',got.eq(want).all(),int((got!=want).sum()))
ck('t10_nonpair_posture_exact',(rpo.t10_posture=='NOT_PRIMARY_PAIR_GRAIN__SEE_EXHAUSTIVE_SOURCE_OBJECT_AND_ALIGNMENT_LEDGERS__NO_PAIR_ABSENCE_CLAIM').all())
ck('outside_recall_no_absence_claim',PO.loc[~pd.Series(mapped).values,'pair_disposition'].str.contains('NO_ABSENCE_CLAIM').all())
smry=json.load(open(R/'COVERAGE/R11_OPPORTUNITY_DENOMINATOR_SUMMARY.json'));ck('summary_no_pair_absence_claim',smry.get('pair_absence_claim_from_outside_recall_channel') is False,smry.get('pair_absence_claim_from_outside_recall_channel'))
# governance
st=json.load(open(R/'CURRENT_STATUS_R11.json'));ck('job3_false',st['job3_authorized'] is False);ptr=open(R/'ACTIVE_EXECUTION_POINTER.md').read();ck('pointer_job3_not_authorized','NOT AUTHORIZED' in ptr);ck('r8_do_not_execute',st['r8_worker_packs']=='DO_NOT_EXECUTE')
res={'status':'PASS' if not errs else 'FAIL','check_count':len(checks),'errors':errs,'checks':checks}
json.dump(res,open(R/'VALIDATION/VALIDATION_RESULT_R11.json','w'),indent=2)
print(json.dumps(res,indent=2));sys.exit(1 if errs else 0)
