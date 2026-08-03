from pathlib import Path
import json
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent
INQ=ROOT/'40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv'

def read(name): return pd.read_csv(OUT/name)

def test_exact_work_unit_and_queue_closure():
    q=pd.read_csv(INQ); r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv'); rem=read('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Final_Tranche_v8.csv')
    assert len(q)==2847 and len(r)==2847 and len(rem)==0
    assert set(q.semantic_pair_candidate_id)==set(r.semantic_pair_candidate_id)
    assert r.semantic_pair_candidate_id.is_unique and r.pair_ruling_id.is_unique

def test_partition_and_allowed_relations():
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv')
    assert len(r)==sum(r.relation_type.value_counts())
    assert set(r.relation_type)<={'REWORDED_PROPOSITION_EQUIVALENCE','CONSTRUCT_TARGET_COORDINATE_ONLY','DOMAIN_COORDINATE_ONLY','NEGATIVE_AUTHORITY','OTHER_DOMAIN_REVIEW_REQUIRED','UNRESOLVED'}

def test_two_sided_evidence_complete():
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv'); e=read('Rawlsing_P2_Final_2847_Two_Sided_Evidence_Ledger_v1.csv')
    assert len(e)==2*len(r) and e.evidence_record_id.is_unique
    counts=e.groupby('pair_ruling_id').side.agg(lambda x:set(x))
    assert all(v=={'LEFT','RIGHT'} for v in counts)
    assert set(counts.index)==set(r.pair_ruling_id)

def test_proposition_acceptance_is_fail_closed():
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv')
    a=r[r.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE']
    assert len(a)==89
    assert (a.left_relation_axis==a.right_relation_axis).all()
    assert (a.left_target_or_scope==a.right_target_or_scope).all()
    assert (a.left_operator==a.right_operator).all()
    assert (a.left_classification_confidence=='HIGH').all() and (a.right_classification_confidence=='HIGH').all()
    assert set(a.portability_ceiling)<={'QUESTION_PROPOSITION_ONLY','QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY'}

def test_known_false_equivalences_absent():
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv')
    a=r[r.relation_type=='REWORDED_PROPOSITION_EQUIVALENCE']
    # Specific prayers never collapse into generic prayer.
    assert not ((a.left_target_or_scope.isin(['fajr_on_time','istikhara'])) ^ (a.right_target_or_scope.isin(['fajr_on_time','istikhara']))).any()
    # Respondent attendance never collapses into parents' attendance.
    assert not ((a.left_target_or_scope=='respondent_religious_services') ^ (a.right_target_or_scope=='respondent_religious_services')).any()
    # Democratic-system support cannot equal support for non-democratic systems.
    assert not ((a.left_target_or_scope=='democratic_system') ^ (a.right_target_or_scope=='democratic_system')).any()
    # Contextualized happiness is below proposition identity with unprompted happiness.
    assert not ((a.left_relation_axis=='general_happiness_contextualized') ^ (a.right_relation_axis=='general_happiness_contextualized')).any()
    # Narrow foreign-worker target cannot equal combined immigrants/foreign-workers target.
    assert not ((a.left_target_or_scope=='foreign_workers') ^ (a.right_target_or_scope=='foreign_workers')).any()
    # Like/dislike race rating cannot equal binary neighbor exclusion.
    assert not ((a.left_relation_axis=='neighbor_closeness_preference') ^ (a.right_relation_axis=='neighbor_closeness_preference')).any()

def test_unresolved_is_bounded():
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv'); u=r[r.relation_type=='UNRESOLVED']
    assert len(u)==84
    assert (u.portability_ceiling=='NO_AUTHORITY').all()
    assert set(u.semantic_content_id)=={'CHILD_OBEDIENCE'}

def test_return_matches_artifacts():
    ret=json.loads((OUT/'FINAL_2847_TRANCHE_RETURN.json').read_text())
    r=read('Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv')
    assert ret['input_pending_pairs']==2847 and ret['remaining_pairs']==0 and ret['queue_closed'] is True
    assert ret['relation_type_counts']==r.relation_type.value_counts().to_dict()
