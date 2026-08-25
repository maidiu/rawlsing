from pathlib import Path
import pandas as pd, json, hashlib, os
from collections import defaultdict
OUT=Path('/mnt/data/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R10_20260811')
(OUT/'ONTOLOGY').mkdir(exist_ok=True); (OUT/'COVERAGE').mkdir(exist_ok=True); (OUT/'VALIDATION').mkdir(exist_ok=True); (OUT/'PROVENANCE').mkdir(exist_ok=True); (OUT/'INDEX').mkdir(exist_ok=True)
sp=pd.read_csv(OUT/'SPINE/UNIFIED_18276_STRUCTURAL_SEMANTIC_SPINE_R10.csv.gz',low_memory=False)
# ---- reverse indices ----
def emit_index(col, fn, keyname):
    h=sp[sp[col].notna() & (sp[col].astype(str).str.strip()!='')].copy()
    rows=[]
    for (sf,w,v),g in h.groupby(['source_family','wave',col],dropna=False,sort=True):
        rows.append({'source_family':sf,'wave':w,keyname:v,'implementation_count':len(g),'question_implementation_ids_json':json.dumps(sorted(g.question_implementation_id.astype(str).unique().tolist())),'semantic_unit_ids_json':json.dumps(sorted(g.sem__audit_unit_id.dropna().astype(str).unique().tolist()))})
    pd.DataFrame(rows).to_csv(OUT/'INDEX'/fn,index=False)
emit_index('sem__measured_predicate','PREDICATE_TO_IMPLEMENTATIONS_BY_WAVE_R10.csv','measured_predicate')
emit_index('sem__canonical_target_id','TARGET_TO_IMPLEMENTATIONS_BY_WAVE_R10.csv','canonical_target_id')
emit_index('sem__canonical_condition_id','CONDITION_TO_IMPLEMENTATIONS_BY_WAVE_R10.csv','canonical_condition_id')
emit_index('sem__canonical_role','SEMANTIC_ACT_ROLE_TO_IMPLEMENTATIONS_BY_WAVE_R10.csv','semantic_act_role')
emit_index('sem__canonical_component_id','COMPONENT_TO_IMPLEMENTATIONS_BY_WAVE_R10.csv','canonical_component_id')
# lineage index
rows=[]
for lin,g in sp[sp.lineage_id.notna() & (sp.lineage_id.astype(str).str.strip()!='')].groupby('lineage_id',sort=True):
    rows.append({'lineage_id':lin,'implementation_count':len(g),'question_implementation_ids_json':json.dumps(sorted(g.question_implementation_id.astype(str).tolist())),'source_wave_json':json.dumps(sorted(set((str(a)+'::'+str(b)) for a,b in zip(g.source_family,g.wave))))})
pd.DataFrame(rows).to_csv(OUT/'INDEX/LINEAGE_TO_IMPLEMENTATIONS_R10.csv',index=False)
# ---- orthogonal relation-role ontology ----
roles=[
('RR_PRINCIPLE','T03','QUESTION_MEMBER_ROLE','General/abstract principle shore','Explicit source/semantic authority that the item states the general principle; not merely normative wording','Does not imply sincerity, universality, or application'),
('RR_APPLICATION','T03','QUESTION_MEMBER_ROLE','Concrete application/case of a governed principle','Explicit source/semantic tie to the same narrow principle','Shared topic/driver is insufficient'),
('RR_GOAL','T04','QUESTION_MEMBER_ROLE','Stated end/goal shore','Explicit governed end','Does not imply acceptance of any mechanism'),
('RR_MEANS','T04','QUESTION_MEMBER_ROLE','Mechanism/means shore tied to a governed end','Explicit common-end tie','Logical usefulness alone is not means authority'),
('RR_COMMITMENT','T05','QUESTION_MEMBER_ROLE','Commitment shore','Explicit commitment/endorsement with same substantive object as cost-bearing shore','Does not imply actual sacrifice'),
('RR_COST_BEARING_APPLICATION','T05','QUESTION_MEMBER_ROLE','Explicit personal/fiscal/risk/autonomy cost-bearing application','Explicit burden plus semantic tie to commitment','Generic material pressure or inconvenience is insufficient'),
('RR_NORM','T06','QUESTION_MEMBER_ROLE','Norm/obligation/approval shore','Governed norm semantics; broad semantic-act role is only evidence, not sufficient by itself','Cannot be inferred merely from moral vocabulary'),
('RR_STATED_OR_INTENDED_CONDUCT','T06','QUESTION_MEMBER_ROLE','Stated/intended/expected action shore','Explicit actor-target-action alignment with norm','Must not be promoted to realized behavior'),
('RR_BEHAVIOR_OR_EXPOSURE_ENDPOINT','T06','QUESTION_MEMBER_ROLE','O04-authorized behavior/exposure endpoint shore','O04 ACCEPT_ENDPOINT plus exact actor/target/action-or-exposure alignment','Exposure remains exposure; endpoint permission does not create link'),
('RR_GENERAL_TARGET','T07','QUESTION_MEMBER_ROLE','Broader governed target scope','Directional hierarchy/broader-than authority','Lexical generality alone is insufficient'),
('RR_SUBTARGET','T07','QUESTION_MEMBER_ROLE','Narrower/subtype target scope','Directional hierarchy/narrower-than authority','Functional adjacency is not subtype'),
('RR_INSTITUTION_TARGET','T08','QUESTION_MEMBER_ROLE','Exact institution target participating in class differentiation','Exact target identity plus controlled class mapping','Class never replaces exact target'),
('RR_INSTITUTION_CLASS','T08','RELATION_METADATA','Controlled institution class','Governed class mapping distinct from exact target and predicate','Shared trust battery does not establish class'),
('RR_DIRECTIONAL_ACTOR_RECIPIENT','T09','QUESTION_MEMBER_ROLE','One directed actor→recipient proposition','Explicit actor, recipient, proposition/action and direction','No symmetry from wording similarity'),
('RR_RECIPROCAL_DIRECTION','T09','RELATION_METADATA','Governed reversal identity for matched actor/recipient roles','Explicit reversed actor/recipient structure with same narrow proposition','Gender/condition variation is not reciprocity'),
('RR_MATRIX_CELL','T10','QUESTION_MEMBER_ROLE','Exact cell in a target×condition structure','Cell bound to governed target and condition dimensions','One-dimensional battery is not a matrix'),
('RR_MATRIX_TARGET_DIMENSION','T10','STRUCTURE_METADATA','Governed target dimension identity','Repeated targets across conditions','Target inferred from contaminated condition labels must be corrected before use'),
('RR_MATRIX_CONDITION_DIMENSION','T10','STRUCTURE_METADATA','Governed condition dimension identity','Repeated conditions across targets','Routing/time variation is not automatically a condition'),
('RR_COMPLEMENTARY_COMPONENT','T11','QUESTION_MEMBER_ROLE','Distinct bounded role contributing to one narrow proposition','Explicit differentiated role and narrow common proposition','No latent scale/additivity from multiple indicators'),
('RR_COMMON_PROPOSITION','T03;T04;T05;T06;T09;T11','RELATION_METADATA','Narrow common proposition/end/action domain tying member roles','Source or governed semantic authority','Broad driver/facet/topic is insufficient')]
rr=pd.DataFrame(roles,columns=['relation_role_id','rule_ids','role_kind','definition','required_authority','prohibited_inference'])
rr['orthogonality_law']='Relation-role ontology is orthogonal to R10G semantic-act roles; neither substitutes for the other.'
rr['status']='GOVERNING_SCHEMA_ROLE_DEFINITION__DOES_NOT_ASSIGN_MEMBERSHIP'
rr.to_csv(OUT/'ONTOLOGY/RELATION_ROLE_ONTOLOGY_R10.csv',index=False)
# rule contracts
contracts=[
('S14-T03','GENERAL_PRINCIPLE_SPECIFIC_APPLICATION','RR_PRINCIPLE + RR_APPLICATION + RR_COMMON_PROPOSITION','relational pair census; source-parent structures; R6/R8 calibration','REQUIRES_ADJUDICATION','No exhaustive per-unit principle/application role assignments yet; R8 frontier is bounded.'),
('S14-T04','GOAL_MEANS','RR_GOAL + RR_MEANS + RR_COMMON_PROPOSITION','relational pair census; source-parent structures; R6/R8 calibration','REQUIRES_ADJUDICATION','No exhaustive goal/means/common-end assignments yet.'),
('S14-T05','COMMITMENT_PERSONAL_COST','RR_COMMITMENT + RR_COST_BEARING_APPLICATION + RR_COMMON_PROPOSITION','relational pair census; source-parent structures; R6/R8 calibration','REQUIRES_ADJUDICATION','No exhaustive commitment/cost/tie assignments yet.'),
('S14-T06','NORM_EXPECTED_CONDUCT','RR_NORM + conduct/endpoint role + RR_COMMON_PROPOSITION','semantic norm shore + all 2,113 O04 accepted endpoints + source structures','REQUIRES_ADJUDICATION','Both shores are governed but exhaustive actor-target-action link authority is not installed.'),
('S14-T07','GENERAL_TARGET_SUBTARGET','RR_GENERAL_TARGET + RR_SUBTARGET','P2/P3 explicit hierarchy + exact target/source structures + R3 narrowing','RECOVERABLE','Directional P2/P3 hierarchy exists; remaining target-relation terrain and source hierarchies require terminal disposition.'),
('S14-T08','INSTITUTION_CLASS_DIFFERENTIATION','RR_INSTITUTION_TARGET + RR_INSTITUTION_CLASS','R4 controlled class mapping + exact targets + source structures','RECOVERABLE','Controlled mapping exists but review-required/ambiguous class mappings remain and class pair opportunity ledger is not globally terminal.'),
('S14-T09','RECIPROCAL_ROLE_REVERSAL','RR_DIRECTIONAL_ACTOR_RECIPIENT + RR_RECIPROCAL_DIRECTION','exact source parents + source roles + R6/R5 calibration','REQUIRES_ADJUDICATION','No exhaustive actor/recipient/direction registry across all relevant source terrain.'),
('S14-T10','TARGET_CONDITION_MATRIX','RR_MATRIX_CELL + target/condition dimension metadata','R9 relational pairs + topology/context/non-scalar lanes + exact source-parent/R14 structures + R6/R6-narrowing','REQUIRES_ADJUDICATION','Matrix canaries prove non-relational lanes are required; complete source-parent matrix identity universe not yet terminal.'),
('S14-T11','COMPLEMENTARY_ROLE_CONVERGENCE','RR_COMPLEMENTARY_COMPONENT + RR_COMMON_PROPOSITION','R9 relational pairs + non-relational lanes + R14/source structures + R7 narrowing','REQUIRES_ADJUDICATION','No exhaustive bounded-role/common-proposition registry; R7 same-target multi-role and R14 scans are narrowing only.')]
ct=pd.DataFrame(contracts,columns=['rule_id','relation_type','required_relation_roles','composite_input_shores','input_contract_status','remaining_obligation'])
ct['candidate_generation_authorized_for_final_absence_claim']=False
ct['job3_authorized']=False
ct.to_csv(OUT/'COVERAGE/S14_T03_T11_INPUT_CONTRACT_STATUS_R10.csv',index=False)
# ---- per-wave composite shore census, NOT old S16 truth ----
# Basic exact counts from spine; no relation inference.
# R4 class status propagated in spine; P2 hierarchy terrain + O04 + R14 + R6.
rules=ct[['rule_id','relation_type','input_contract_status']].to_dict('records')
rows=[]
for (sf,w),g in sp.groupby(['source_family','wave'],sort=True):
    norm = g['sem__canonical_role'].fillna('').astype(str).eq('NORMATIVE_OR_POLICY_STANCE').sum()
    o04 = g['o04__central_s2b_disposition'].fillna('').astype(str).eq('ACCEPT_ENDPOINT').sum()
    for r in rules:
        rid=r['rule_id']; rt=r['relation_type']
        r6mask=g['r6_relation_types_json'].fillna('').astype(str).str.contains(rt,regex=False)
        rec={
          'source_family':sf,'wave':w,'rule_id':rid,'relation_type':rt,
          'implementation_count':len(g),
          'semantic_unit_membership_rows':int(g.sem__audit_unit_id.notna().sum()),
          'accepted_o04_endpoints':int(o04),
          'normative_semantic_act_rows':int(norm),
          'r14_member_rows':int((g.r14_object_count.fillna(0)>0).sum()),
          'p2_p3_pair_authority_member_rows':int(((g.p2_pair_authority_count.fillna(0)+g.p3c_pair_resolution_count.fillna(0)+g.p3c_stronger_boundary_count.fillna(0))>0).sum()),
          'p2_explicit_nested_target_member_rows':int((g.p2_explicit_nested_target_relation_count.fillna(0)>0).sum()),
          'p2_target_relation_terrain_member_rows':int((g.p2_target_relation_terrain_count.fillna(0)>0).sum()),
          't08_class_mapped_implementation_rows':int(g.t08_institution_class.notna().sum()),
          'existing_r6_positive_member_rows_for_rule':int(r6mask.sum()),
          'input_contract_status_global':r['input_contract_status'],
          'denominator_completion_status':'INPUT_AUTHORITY_INCOMPLETE__NO_FINAL_ABSENCE_CLAIM',
          'law':'Counts are primitive-shore accounting only. A zero candidate count is not absence until the rule-specific bridge authority and complete opportunity/disposition ledger close.'}
        rows.append(rec)
pd.DataFrame(rows).to_csv(OUT/'COVERAGE/S14_T03_T11_COMPOSITE_SHORE_CENSUS_BY_WAVE_R10.csv',index=False)
# R4 unresolved mapping census
r4p=Path('/mnt/data/r4_full/Rawlsing_R10K_S14_Relation_Role_Bridge_Repair_Checkpoint_R4_20260811/NARROWING/T08_INSTITUTION_CLASS_MAPPING_R4.csv')
if r4p.exists():
    r4=pd.read_csv(r4p,low_memory=False)
    (r4.groupby(['class_mapping_status'],dropna=False).size().reset_index(name='semantic_unit_count')
       .to_csv(OUT/'COVERAGE/T08_CLASS_MAPPING_STATUS_CENSUS_R10.csv',index=False))
# historical controls pinned, not promoted
for src in [Path('/mnt/data/r10_historical_inputs/DDM_STRUCTURAL_INFORMATION_REQUIREMENTS_R7J.csv'),Path('/mnt/data/r10_historical_inputs/RELATION_LAYERING_CONTRACT_R7J.csv')]:
    if src.exists():
        dst=OUT/'PROVENANCE'/src.name
        dst.write_bytes(src.read_bytes())
# R9 pair base pointer
pair=Path('/mnt/data/r9_full/PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz')
def sha(p):
 h=hashlib.sha256();
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
json.dump({'r9_pair_census_path':'/Rawlsing/R10K/S14_RELATION_ROLE_BRIDGE_REPAIR/CHECKPOINT_R9_20260811/PAIR_CENSUS/ALL_SAME_SOURCE_WAVE_SEMANTIC_UNIT_PAIRS_R9.csv.gz','local_sha256':sha(pair),'pair_count':364094,'jurisdiction':'complete same-source-wave pair base for current 3324 relational semantic units only; not full S14 universe'},open(OUT/'PROVENANCE/R9_PAIR_CENSUS_POINTER_R10.json','w'),indent=2)
# status
status={
 'checkpoint':'R10','active_state':'R10K / PRE-JOB3 / S14 RELATION-ROLE BRIDGE REPAIR / COMPOSITE DENOMINATOR REPAIR',
 'repair_item_2_unified_18276_spine':'DONE_PENDING_COLD_LIBRARY_ROUNDTRIP',
 'repair_item_3_relation_role_ontology':'DONE_SCHEMA_DEFINITIONS__MEMBERSHIP_INSTALLATION_REMAINS_RULE_ADJUDICATION',
 'repair_item_14_composite_denominator':'ACTIVE_NOT_COMPLETE',
 'r8_worker_packs':'DO_NOT_EXECUTE','r8c':'PRESERVE_PROVISIONALLY_REVALIDATE_LATER','job3_authorized':False,
 'next':'Build denominator-complete rule-specific opportunity/disposition ledgers T03-T11 using R10 spine, R9 pair census, source-parent structures and recovered narrowing; terminally resolve bridge-role membership or typed blockers before recompression/worker economics.'}
json.dump(status,open(OUT/'CURRENT_STATUS_R10.json','w'),indent=2)
print('done')
