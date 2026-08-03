from pathlib import Path
import json
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=Path(__file__).resolve().parent

def test_semantic_queue_exact_coverage_and_partition():
    initial=pd.read_csv(ROOT/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1/Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv')
    reg=pd.read_csv(OUT/'Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv')
    assert len(reg)==18831 and reg.semantic_pair_candidate_id.is_unique
    assert set(reg.semantic_pair_candidate_id)==set(initial.semantic_pair_candidate_id)
    assert reg.normalized_authority_class.value_counts().to_dict()=={
      'NEGATIVE_AUTHORITY':14857,'REDIRECTED_OTHER_DOMAIN_AUTHORITY':1958,
      'COORDINATE_OR_BOUNDED_RELATION_AUTHORITY':1024,'PROPOSITION_RELATION_AUTHORITY':641,
      'UNRESOLVED_FAIL_CLOSED_AUTHORITY':351}

def test_all_source_pairs_and_tranches_present():
    reg=pd.read_csv(OUT/'Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv')
    assert reg[['left_source_family','right_source_family']].drop_duplicates().shape[0]==36
    assert reg.origin_tranche.value_counts().to_dict()=={
      'TRANCHE2_HIGH_PRECISION':121,'TRANCHE3_TRUST':3863,'TRANCHE4_DEMOCRACY_ELECTORAL':3000,
      'TRANCHE5_MEDIA_CIVIC':3000,'TRANCHE6_MATERIAL_ECONOMY':3000,'TRANCHE7_SOCIAL_ORDER':3000,'TRANCHE8_FINAL_2847':2847}

def test_exact_foundation_closed_without_forcing_unresolved():
    d=pd.read_csv(OUT/'Rawlsing_P2_Global_Exact_Foundation_Authority_Registry_v1.csv')
    assert len(d)==751
    assert d.normalized_authority_class.value_counts().to_dict()=={
      'UNRESOLVED_EXACT_FOUNDATION_AUTHORITY':403,'ACCEPTED_EXACT_FOUNDATION_AUTHORITY':270,'REJECTED_EXACT_FOUNDATION_AUTHORITY':78}

def test_closure_return_is_truthful():
    ret=json.loads((OUT/'GLOBAL_P2_CLOSURE_RETURN.json').read_text())
    assert ret['global_p2_closed'] is True and ret['semantic_priority_pairs_remaining']==0
    assert ret['canonical_j_family_authority_authored'] is False
    assert ret['respondents_joined'] is False and ret['values_harmonized'] is False and ret['database_or_registry_written'] is False
    assert ret['live_component_bridge_installed'] is False
    assert ret['next_pass']=='P3_TYPED_COLLISION_HYPEREDGE_CANDIDATE_FAMILY_RANKING_AND_CANONICAL_V550J_ADJUDICATION'

def test_runtime_boundary_is_not_counterfeit_installation():
    d=json.loads((OUT/'LIVE_COMPONENT_BRIDGE_INSTALLATION_BOUNDARY_AUDIT.json').read_text())
    assert d['user_designated_current_live_repository_found'] is False
    assert d['installation_performed'] is False
    assert d['recovered_runtime_snapshot_present'] is True

def test_validation_checks_all_pass():
    d=pd.read_csv(OUT/'GLOBAL_P2_CLOSURE_VALIDATION_CHECKS.csv')
    assert len(d)==16 and (d.status=='PASS').all()
