from pathlib import Path
import json, os, subprocess, sys, tempfile, hashlib
import pandas as pd

ROOT=Path(os.environ.get('RAWLSING_V19_TEST_ROOT','/mnt/data/rawlsing_v19_outputs/social_order_3000'))
V18=Path(os.environ.get('RAWLSING_V18_ROOT','/mnt/data/rawlsing_v19_work/Rawlsing_J_Family_Authority_Strategy_Handoff_v18_20260731'))

def rd(name): return pd.read_csv(ROOT/name,dtype=str,keep_default_na=False)
def sha(p):
 h=hashlib.sha256(); h.update(Path(p).read_bytes()); return h.hexdigest()

def test_fixed_3000(): assert len(rd('Rawlsing_P2_Social_Order_Fixed_3000_Tranche_Candidate_Surface_v1.csv'))==3000
def test_input_count(): assert json.loads((ROOT/'FIXED_3000_SOCIAL_ORDER_TRANCHE_RETURN.json').read_text())['input_pending_pairs']==5847
def test_remaining_count(): assert len(rd('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv'))==2847
def test_queue_partition_disjoint():
 a=set(rd('Rawlsing_P2_Social_Order_Fixed_3000_Tranche_Candidate_Surface_v1.csv').semantic_pair_candidate_id); b=set(rd('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv').semantic_pair_candidate_id)
 assert not a&b and len(a|b)==5847
def test_rulings_exact(): assert len(rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'))==3000
def test_evidence_exact(): assert len(rd('Rawlsing_P2_Social_Order_3000_Two_Sided_Evidence_Ledger_v1.csv'))==6000
def test_unique_pair_ids(): assert rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv').pair_ruling_id.nunique()==3000
def test_unique_evidence_ids(): assert rd('Rawlsing_P2_Social_Order_3000_Two_Sided_Evidence_Ledger_v1.csv').evidence_record_id.nunique()==6000
def test_two_evidence_sides_per_pair():
 e=rd('Rawlsing_P2_Social_Order_3000_Two_Sided_Evidence_Ledger_v1.csv'); g=e.groupby('pair_ruling_id').side.apply(set)
 assert len(g)==3000 and all(x=={'LEFT','RIGHT'} for x in g)
def test_relation_partition():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); assert r.relation_type.value_counts().to_dict()=={'NEGATIVE_AUTHORITY':2561,'OTHER_DOMAIN_REVIEW_REQUIRED':189,'UNRESOLVED':137,'DOMAIN_COORDINATE_ONLY':85,'REWORDED_PROPOSITION_EQUIVALENCE':17,'CONSTRUCT_TARGET_COORDINATE_ONLY':11}
def test_positive_gate():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE')]
 assert ((a.left_relation_axis==a.right_relation_axis)&(a.left_target_or_scope==a.right_target_or_scope)&(a.left_operator==a.right_operator)&a.left_classification_confidence.eq('HIGH')&a.right_classification_confidence.eq('HIGH')).all()
def test_positive_count(): assert len(rd('Rawlsing_P2_Social_Order_Accepted_Proposition_Review_Surface_v1.csv'))==17
def test_no_generic_or_truncated_positive():
 c=rd('Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv').set_index('lineage_id'); r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE')]
 bad=('which of the following actions aimed at fighting climate change have y','basic kinds of attitudes concerning society','you will find here four statements','se7 religiosity')
 for x in a.itertuples():
  text=(c.loc[x.left_lineage_id].exact_question_texts_json+' '+c.loc[x.right_lineage_id].exact_question_texts_json).casefold()
  assert not any(z in text for z in bad)
def test_climate_vs_environment_not_proposition():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); x=r[(r.left_relation_axis.eq('climate_growth_priority_tradeoff')&r.right_relation_axis.eq('environment_growth_priority_tradeoff'))|(r.right_relation_axis.eq('climate_growth_priority_tradeoff')&r.left_relation_axis.eq('environment_growth_priority_tradeoff'))]
 assert len(x)>0 and not x.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE').any()
def test_terse_religiosity_coordinate_only():
 c=rd('Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv'); x=c[c.exact_question_texts_json.str.casefold().str.contains('se7 religiosity',regex=False)]
 assert len(x)==1 and x.iloc[0].classification_confidence=='MEDIUM'
def test_environment_tradeoff_positive_axes():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE') & r.semantic_content_id.eq('ENVIRONMENT_VS_ECONOMY')]
 assert len(a)==6 and set(a.left_relation_axis)|set(a.right_relation_axis)=={'environment_growth_priority_tradeoff'}
def test_gender_education_positive():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE') & r.semantic_content_id.eq('GENDER_EDUCATION')]
 assert len(a)==4 and set(a.left_relation_axis)=={'gendered_university_priority'}
def test_gender_jobs_positive():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE') & r.semantic_content_id.eq('GENDER_JOBS_SCARCE')]
 assert len(a)==1 and a.iloc[0].left_operator==a.iloc[0].right_operator=='men_over_women_priority'
def test_religiosity_positive():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE') & r.semantic_content_id.eq('RELIGION_SELF_RELIGIOSITY')]
 assert len(a)==4 and set(a.left_relation_axis)|set(a.right_relation_axis)<={'self_religiosity_intensity','self_religious_identification'}
def test_safety_positive():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE') & r.semantic_content_id.eq('SECURITY_NEIGHBORHOOD')]
 assert len(a)==2 and set(a.left_relation_axis)=={'local_area_safety_rating'}
def test_unresolved_touches_unresolved_lineage():
 c=rd('Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv').set_index('lineage_id'); r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); u=r[r.relation_type.eq('UNRESOLVED')]
 assert all('UNRESOLVED' in c.loc[x.left_lineage_id].authority_status or 'UNRESOLVED' in c.loc[x.right_lineage_id].authority_status for x in u.itertuples())
def test_no_positive_derived_index():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); a=r[r.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE')]
 assert not a.left_operator.str.contains('derived',case=False).any() and not a.right_operator.str.contains('derived',case=False).any()
def test_selected_semantic_counts():
 s=rd('Rawlsing_P2_Social_Order_Fixed_3000_Tranche_Candidate_Surface_v1.csv').semantic_content_id.value_counts().to_dict()
 assert s=={'DEMO_SUPPORT':726,'GENDER_EDUCATION':432,'GENDER_JOBS_SCARCE':393,'RELIGION_SELF_RELIGIOSITY':365,'SECURITY_NEIGHBORHOOD':323,'ENVIRONMENT_VS_ECONOMY':256,'CHANGE_SOCIETY':243,'FREEDOM_SPEECH':214,'CIVIC_DEMONSTRATION':48}
def test_authority_boundary_text():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); assert r.prohibited_use.str.contains('No J-family authority').all()
def test_classification_referential_integrity():
 r=rd('Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv'); c=set(rd('Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv').classification_id)
 assert set(r.left_classification_id)<=c and set(r.right_classification_id)<=c
def test_deterministic_rebuild():
 names=['Rawlsing_P2_Social_Order_Lineage_Classification_v1.csv','Rawlsing_P2_Social_Order_3000_Pair_Rulings_v1.csv','Rawlsing_P2_Social_Order_3000_Two_Sided_Evidence_Ledger_v1.csv','Rawlsing_P2_Social_Order_Fixed_3000_Tranche_Candidate_Surface_v1.csv','Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv','FIXED_3000_SOCIAL_ORDER_TRANCHE_RETURN.json']
 with tempfile.TemporaryDirectory() as td:
  env=os.environ.copy(); env['RAWLSING_V18_ROOT']=str(V18); env['RAWLSING_V19_OUT']=td; env['PYTHONDONTWRITEBYTECODE']='1'
  subprocess.run([sys.executable,str(ROOT/'build_social_order_tranche_v1.py')],env=env,check=True,capture_output=True,text=True)
  assert all(sha(ROOT/n)==sha(Path(td)/n) for n in names)
