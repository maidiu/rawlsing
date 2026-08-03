from __future__ import annotations
import hashlib, json, os, subprocess, sys, tempfile
from pathlib import Path
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V17_ROOT','/mnt/data/rawlsing_v17_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v17_20260731'))
OUT=Path(os.environ.get('RAWLSING_V18_OUT','/mnt/data/rawlsing_v18_outputs/material_economy_3000'))
BUILDER=Path(os.environ.get('RAWLSING_V18_BUILDER','/mnt/data/rawlsing_v18_work/build_material_economy_tranche_v1.py'))
SELECTION=Path(os.environ.get('RAWLSING_FIXED_3000_SELECTION','/mnt/data/rawlsing_v18_work/fixed_tranche6_3000_candidates.csv'))

def read(name): return pd.read_csv(OUT/name,dtype=str,keep_default_na=False)
def load():
 return (read('Rawlsing_P2_Material_Economy_Fixed_3000_Tranche_Candidate_Surface_v1.csv'),read('Rawlsing_P2_Material_Economy_Lineage_Classification_v1.csv'),read('Rawlsing_P2_Material_Economy_3000_Pair_Rulings_v1.csv'),read('Rawlsing_P2_Material_Economy_3000_Two_Sided_Evidence_Ledger_v1.csv'),read('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Material_Economy_Fixed_3000_Tranche_v6.csv'))
def cidx(): return load()[1].set_index('lineage_id')
def pair(r,a,b):
 m=((r.left_lineage_id==a)&(r.right_lineage_id==b))|((r.left_lineage_id==b)&(r.right_lineage_id==a)); x=r[m]; assert len(x)==1; return x.iloc[0]
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def test_exact_work_unit_and_remaining():
 c,_,r,_,q=load(); assert len(c)==len(r)==3000; assert len(q)==5847

def test_incoming_queue_partition_exact():
 c,_,r,_,q=load(); inc=pd.read_csv(ROOT/'38_P2_GLOBAL_MEDIA_CIVIC_FIXED_3000_TRANCHE5/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv',dtype=str,keep_default_na=False)
 s=set(c.semantic_pair_candidate_id); p=set(q.semantic_pair_candidate_id); assert s.isdisjoint(p); assert s|p==set(inc.semantic_pair_candidate_id); assert set(r.semantic_pair_candidate_id)==s

def test_frozen_selection_exact():
 c,*_=load(); f=pd.read_csv(SELECTION,dtype=str,keep_default_na=False); assert len(f)==3000; assert list(c.semantic_pair_candidate_id)==list(f.semantic_pair_candidate_id)

def test_selection_contract_counts():
 c,*_=load(); expected={'ECON_COUNTRY_FUTURE':690,'ECON_PERSONAL_NOW':408,'ECON_COUNTRY_NOW':349,'ECON_GAP_RICH_POOR':218,'ECON_SATISFACTION_FINANCIAL':190,'ECON_GOVT_VS_INDIVIDUAL':94,'WORK_SUCCESS_HARDWORK':91,'ECON_INEQUALITY_ATTITUDE':70,'ECON_ELITE_CAPTURE':59,'ECON_PERSONAL_FUTURE':53,'INTERGENERATIONAL_COMPARE':49,'INTERGENERATIONAL_FUTURE':15,'LIVING_CONDITIONS':8,'DEPRIVATION_FOOD':156,'DEPRIVATION_MEDICINE':82,'DEPRIVATION_WATER':72,'DEPRIVATION_CASH':27,'WASTA_JOBS':136,'IMMIGRANT_JOBS':68,'WORK_IMPORTANCE':45,'WORK_DUTY_SOCIETY':8,'materialSecurity::important_in_a_job_good_hours':1,'materialSecurity::important_in_a_job_good_pay':1,'materialSecurity::important_in_a_job_generous_holidays':1,'GENDER_JOBS_SCARCE':109}; assert c.semantic_content_id.value_counts().to_dict()==expected

def test_stable_ids_unique():
 _,cl,r,e,_=load(); assert cl.lineage_id.is_unique and cl.classification_id.is_unique and r.pair_ruling_id.is_unique and e.evidence_record_id.is_unique

def test_two_evidence_sides_per_ruling():
 _,_,r,e,_=load(); g=e.groupby('pair_ruling_id').side.agg(list); assert set(g.index)==set(r.pair_ruling_id); assert all(sorted(v)==['LEFT','RIGHT'] for v in g); assert len(e)==6000

def test_evidence_resolves_exact_sides():
 _,cl,r,e,_=load(); ids=set(cl.classification_id); assert set(e.classification_id)<=ids
 for _,x in r.iterrows():
  z=e[e.pair_ruling_id==x.pair_ruling_id].set_index('side'); assert z.loc['LEFT'].lineage_id==x.left_lineage_id; assert z.loc['RIGHT'].lineage_id==x.right_lineage_id

def test_authority_partition_exact():
 _,_,r,_,_=load(); assert r.relation_type.value_counts().to_dict()=={'NEGATIVE_AUTHORITY':2884,'DOMAIN_COORDINATE_ONLY':60,'REWORDED_PROPOSITION_EQUIVALENCE':28,'OTHER_DOMAIN_REVIEW_REQUIRED':19,'CONSTRUCT_TARGET_COORDINATE_ONLY':9}

def test_no_unresolved_rows():
 _,cl,r,_,_=load(); assert not (r.relation_type=='UNRESOLVED').any(); assert not cl.authority_status.str.contains('UNRESOLVED').any()

def test_proposition_gate_exact():
 _,cl,r,_,_=load(); a=r[r.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE']; assert len(a)==28; assert (a.left_relation_axis==a.right_relation_axis).all(); assert (a.left_target_or_scope==a.right_target_or_scope).all(); assert (a.left_operator==a.right_operator).all(); assert (a.left_classification_confidence=='HIGH').all(); assert (a.right_classification_confidence=='HIGH').all()

def test_no_high_identity_silently_nonaccepted_except_other_domain():
 _,_,r,_,_=load(); same=(r.left_relation_axis==r.right_relation_axis)&(r.left_target_or_scope==r.right_target_or_scope)&(r.left_operator==r.right_operator)&(r.left_classification_confidence=='HIGH')&(r.right_classification_confidence=='HIGH'); m=r[same&(r.relation_type!='REWORDED_PROPOSITION_EQUIVALENCE')]; allowed=((m.relation_type=='OTHER_DOMAIN_REVIEW_REQUIRED')|((m.relation_type=='NEGATIVE_AUTHORITY')&(m.left_relation_axis=='other_domain')&(m.left_target_or_scope.isin({'survey_metadata','derived_or_constructed_variable'})))); assert allowed.all()

def test_national_economy_satisfaction_not_condition_equivalence():
 _,cl,r,_,_=load(); c=cl.set_index('lineage_id'); lid='p2lineage_b766a24a7cca542f1834f424'; assert c.loc[lid].governed_relation_axis=='country_economic_satisfaction'; touched=r[(r.left_lineage_id==lid)|(r.right_lineage_id==lid)]; assert not (touched.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE').any()

def test_government_economy_management_not_inequality_performance():
 c=cidx(); assert c.loc['p2lineage_ac7725f47dacb3755fa3addc'].governed_relation_axis=='government_economy_management_performance'; assert c.loc['p2lineage_f57929f1c73b0f3d084e90c8'].governed_relation_axis=='government_inequality_performance_evaluation'

def test_income_ladder_not_income_equality_preference():
 c=cidx(); assert c.loc['p2lineage_b10221f585666a7b1ddefdb8'].governed_relation_axis=='subjective_income_position'

def test_democracy_income_equalization_not_equality_preference():
 c=cidx(); assert c.loc['p2lineage_6f947aa22dc1d8d81d16091e'].governed_relation_axis=='democracy_feature_evaluation'

def test_healthcare_access_not_medicine_deprivation_proposition():
 _,_,r,_,_=load(); m=((r.left_target_or_scope=='healthcare_access')&(r.right_target_or_scope=='medicine_or_medical_treatment'))|((r.right_target_or_scope=='healthcare_access')&(r.left_target_or_scope=='medicine_or_medical_treatment')); assert not (r[m].relation_type=='REWORDED_PROPOSITION_EQUIVALENCE').any()

def test_current_job_usefulness_not_desired_job_attribute():
 c=cidx(); assert c.loc['p2lineage_5b29b6d5f24778595a5a5c3b'].governed_relation_axis=='current_job_social_usefulness'; assert c.loc['p2lineage_51c3bb6532299da4600d9a5f'].governed_relation_axis=='job_attribute_importance'

def test_country_future_timeframes_preserved():
 c=cidx(); ops={c.loc[x].governed_operator for x in ['p2lineage_b019c858db0a8556705df940','p2lineage_d263f982cacdc302f45a8765','p2lineage_35d53915a72978009d151d1b']}; assert len(ops)==3

def test_personal_family_targets_preserved():
 c=cidx(); targets={c.loc[x].governed_target_or_scope for x in ['p2lineage_dddb209a62b6fb0bfb8e3f8f','p2lineage_b5134ab9662ff5401ec339ae','p2lineage_5891e5d5cb0fd4be06a03abd']}; assert targets=={'family_or_household_economy','personal_and_family_economy','personal_economy'}

def test_household_income_adequacy_not_satisfaction():
 c=cidx(); assert c.loc['p2lineage_302a35c5ed8df0545586b692'].governed_relation_axis=='household_income_adequacy'; assert c.loc['p2lineage_577ceab2ecada0c87288c645'].governed_operator=='income_situation_category'

def test_scarce_jobs_targets_preserved():
 c=cidx(); assert c.loc['p2lineage_dfe0636afbf9a4f25877d87e'].governed_target_or_scope=='men_over_women'; assert c.loc['p2lineage_6351211e2601a95eae396316'].governed_target_or_scope=='nationals_over_foreigners'; assert c.loc['p2lineage_0a8ccba6feaa1a616b64d895'].governed_target_or_scope=='locals_over_nonlocals'

def test_proposition_evidence_sufficiency_complete():
 _,_,r,e,_=load(); ids=set(r[r.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE'].pair_ruling_id); z=e[e.pair_ruling_id.isin(ids)]; assert len(z)==56; assert (z.evidence_sufficiency=='COMPLETE_FOR_PROPOSITION_CEILING').all()

def test_all_authority_boundaries_prohibit_downstream_use():
 _,_,r,_,_=load(); assert r.prohibited_use.str.contains('No J-family authority').all()

def test_return_contract_matches_outputs():
 ret=json.loads((OUT/'FIXED_3000_MATERIAL_ECONOMY_TRANCHE_RETURN.json').read_text()); assert ret['input_pending_pairs']==8847 and ret['fixed_work_unit_pairs']==3000 and ret['remaining_pairs']==5847; assert ret['relation_type_counts']['REWORDED_PROPOSITION_EQUIVALENCE']==28

def test_builder_is_deterministic_for_tracked_outputs(tmp_path):
 env=os.environ.copy(); env['RAWLSING_V18_OUT']=str(tmp_path); env['RAWLSING_V17_ROOT']=str(ROOT); env['RAWLSING_FIXED_3000_SELECTION']=str(SELECTION); env['PYTHONDONTWRITEBYTECODE']='1'; subprocess.run([sys.executable,str(BUILDER)],check=True,env=env,stdout=subprocess.DEVNULL)
 names=['Rawlsing_P2_Material_Economy_Fixed_3000_Tranche_Candidate_Surface_v1.csv','Rawlsing_P2_Material_Economy_Lineage_Classification_v1.csv','Rawlsing_P2_Material_Economy_3000_Pair_Rulings_v1.csv','Rawlsing_P2_Material_Economy_3000_Two_Sided_Evidence_Ledger_v1.csv','Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Material_Economy_Fixed_3000_Tranche_v6.csv','FIXED_3000_MATERIAL_ECONOMY_TRANCHE_RETURN.json']; assert all(sha(OUT/n)==sha(tmp_path/n) for n in names)
