from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(os.environ.get('RAWLSING_V16_ROOT','/mnt/data/rawlsing_v17_extract/Rawlsing_J_Family_Authority_Strategy_Handoff_v16_20260731'))
OUT = Path(os.environ.get('RAWLSING_V17_OUT','/mnt/data/rawlsing_v17_outputs/media_civic_3000'))
BUILDER = Path(os.environ.get('RAWLSING_V17_BUILDER','/mnt/data/rawlsing_v17_work/build_media_civic_tranche_v1.py'))
SELECTION = Path(os.environ.get('RAWLSING_FIXED_3000_SELECTION','/mnt/data/rawlsing_v17_work/fixed_tranche5_3000_candidates.csv'))


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(OUT / name, dtype=str, keep_default_na=False)


def load():
    return (
        read('Rawlsing_P2_Media_Civic_Fixed_3000_Tranche_Candidate_Surface_v1.csv'),
        read('Rawlsing_P2_Media_Civic_Lineage_Classification_v1.csv'),
        read('Rawlsing_P2_Media_Civic_3000_Pair_Rulings_v1.csv'),
        read('Rawlsing_P2_Media_Civic_3000_Two_Sided_Evidence_Ledger_v1.csv'),
        read('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv'),
    )


def pair_row(rulings: pd.DataFrame, a: str, b: str) -> pd.Series:
    mask = ((rulings.left_lineage_id == a) & (rulings.right_lineage_id == b)) | ((rulings.left_lineage_id == b) & (rulings.right_lineage_id == a))
    rows = rulings[mask]
    assert len(rows) == 1
    return rows.iloc[0]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_fixed_work_unit_is_exactly_3000():
    candidates, _, rulings, _, remaining = load()
    assert len(candidates) == 3000
    assert len(rulings) == 3000
    assert len(remaining) == 8847


def test_selection_is_unique_and_queue_partition_is_exact():
    candidates, _, rulings, _, remaining = load()
    incoming = pd.read_csv(ROOT / '37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv', dtype=str, keep_default_na=False)
    selected = set(candidates.semantic_pair_candidate_id)
    pending = set(remaining.semantic_pair_candidate_id)
    assert len(selected) == 3000
    assert len(pending) == 8847
    assert selected.isdisjoint(pending)
    assert selected | pending == set(incoming.semantic_pair_candidate_id)
    assert set(rulings.semantic_pair_candidate_id) == selected


def test_frozen_selection_matches_delivered_candidate_surface():
    candidates, *_ = load()
    frozen = pd.read_csv(SELECTION, dtype=str, keep_default_na=False)
    assert set(candidates.semantic_pair_candidate_id) == set(frozen.semantic_pair_candidate_id)
    assert len(frozen) == 3000


def test_selection_contract_counts():
    candidates, *_ = load()
    assert candidates.semantic_content_id.value_counts().to_dict() == {
        'MEDIA_NEWS_SOURCE': 893,
        'MEDIA_INTERNET': 601,
        'CIVIC_DISCUSS_POLITICS': 554,
        'CIVIC_INTEREST_POLITICS': 527,
        'CIVIC_DEMONSTRATION': 425,
    }


def test_stable_ids_are_unique():
    _, classes, rulings, evidence, _ = load()
    assert classes.classification_id.is_unique
    assert classes.lineage_id.is_unique
    assert rulings.pair_ruling_id.is_unique
    assert evidence.evidence_record_id.is_unique


def test_every_ruling_has_exactly_two_evidence_sides():
    _, _, rulings, evidence, _ = load()
    grouped = evidence.groupby('pair_ruling_id').side.agg(list)
    assert set(grouped.index) == set(rulings.pair_ruling_id)
    assert all(sorted(v) == ['LEFT', 'RIGHT'] for v in grouped)
    assert len(evidence) == 6000


def test_evidence_references_resolve_and_match_ruling_sides():
    _, classes, rulings, evidence, _ = load()
    c = classes.set_index('lineage_id')
    assert set(evidence.lineage_id) <= set(c.index)
    assert set(evidence.classification_id) <= set(classes.classification_id)
    assert set(evidence.pair_ruling_id) == set(rulings.pair_ruling_id)
    for _, rr in rulings.iterrows():
        ev = evidence[evidence.pair_ruling_id == rr.pair_ruling_id].set_index('side')
        assert ev.loc['LEFT'].lineage_id == rr.left_lineage_id
        assert ev.loc['RIGHT'].lineage_id == rr.right_lineage_id
        assert ev.loc['LEFT'].classification_id == rr.left_classification_id
        assert ev.loc['RIGHT'].classification_id == rr.right_classification_id


def test_authority_partition_is_exact():
    _, _, rulings, _, _ = load()
    assert rulings.authority_status.value_counts().to_dict() == {
        'REJECTED_MEDIA_CIVIC_VERSUS_OTHER_DOMAIN_MISMATCH': 1133,
        'REJECTED_FALSE_EQUIVALENCE_MEDIA_CIVIC_RELATION_OR_TARGET_MISMATCH': 1017,
        'REJECTED_CONTAMINATED_NEIGHBORHOOD_OTHER_DOMAIN_MISMATCH': 404,
        'ACCEPTED_DOMAIN_COORDINATE_ONLY_RELATION_OR_TARGET_SCOPE_DIFFERS': 287,
        'ACCEPTED_TYPED_MEDIA_CIVIC_PROPOSITION_RELATION': 72,
        'UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_SOURCE_LOCAL_EVIDENCE': 35,
        'REDIRECTED_OUT_OF_MEDIA_CIVIC_DOMAIN_SHARED_OTHER_AXIS_NOT_ADJUDICATED': 27,
        'ACCEPTED_SAME_CONSTRUCT_TARGET_DIFFERENT_OPERATOR_OR_INCOMPLETE_EVIDENCE_COORDINATE_ONLY': 25,
    }


def test_proposition_equivalence_requires_exact_axis_target_operator_and_high_confidence():
    _, classes, rulings, _, _ = load()
    accepted = rulings[rulings.relation_type == 'REWORDED_PROPOSITION_EQUIVALENCE']
    assert len(accepted) == 72
    assert (accepted.left_relation_axis == accepted.right_relation_axis).all()
    assert (accepted.left_target_or_scope == accepted.right_target_or_scope).all()
    assert (accepted.left_operator == accepted.right_operator).all()
    assert (accepted.left_classification_confidence == 'HIGH').all()
    assert (accepted.right_classification_confidence == 'HIGH').all()
    c = classes.set_index('lineage_id')
    for _, row in accepted.iterrows():
        assert c.loc[row.left_lineage_id].authority_status == 'P2_MEDIA_CIVIC_LINEAGE_CLASSIFIED'
        assert c.loc[row.right_lineage_id].authority_status == 'P2_MEDIA_CIVIC_LINEAGE_CLASSIFIED'


def test_no_high_confidence_same_proposition_is_silently_rejected():
    _, _, rulings, _, _ = load()
    same = (
        (rulings.left_relation_axis == rulings.right_relation_axis)
        & (rulings.left_target_or_scope == rulings.right_target_or_scope)
        & (rulings.left_operator == rulings.right_operator)
        & (rulings.left_classification_confidence == 'HIGH')
        & (rulings.right_classification_confidence == 'HIGH')
    )
    missed = rulings[same & (rulings.relation_type != 'REWORDED_PROPOSITION_EQUIVALENCE')]
    assert len(missed) == 1
    row = missed.iloc[0]
    assert row.relation_type == 'OTHER_DOMAIN_REVIEW_REQUIRED'
    assert row.left_relation_axis == row.right_relation_axis == 'other_domain'
    assert row.left_target_or_scope == row.right_target_or_scope == 'respondent_education'


def test_exact_text_match_does_not_override_material_relation_difference():
    candidates, _, rulings, _, _ = load()
    merged = candidates[['semantic_pair_candidate_id','exact_normalized_text_match']].merge(rulings, on='semantic_pair_candidate_id')
    exact_nonaccepted = merged[(merged.exact_normalized_text_match.str.casefold() == 'true') & (merged.relation_type != 'REWORDED_PROPOSITION_EQUIVALENCE')]
    assert len(exact_nonaccepted) == 1
    row = exact_nonaccepted.iloc[0]
    assert row.relation_type == 'NEGATIVE_AUTHORITY'
    assert {row.left_relation_axis, row.right_relation_axis} == {'other_domain', 'media_device_or_medium_indicator'}


def test_only_two_under_specified_lineages_generate_unresolved_pairs():
    _, classes, rulings, _, _ = load()
    unresolved_classes = classes[classes.authority_status == 'P2_MEDIA_CIVIC_LINEAGE_UNRESOLVED']
    assert set(unresolved_classes.lineage_id) == {
        'p2lineage_a153e49c62457bf801d60b1b',
        'p2lineage_78193a6f13f138c9728f81d8',
    }
    unresolved_pairs = rulings[rulings.relation_type == 'UNRESOLVED']
    assert len(unresolved_pairs) == 35
    touched = set(unresolved_pairs.left_lineage_id) | set(unresolved_pairs.right_lineage_id)
    assert touched & set(unresolved_classes.lineage_id) == set(unresolved_classes.lineage_id)
    assert all((row.left_lineage_id in set(unresolved_classes.lineage_id)) or (row.right_lineage_id in set(unresolved_classes.lineage_id)) for _, row in unresolved_pairs.iterrows())


def test_mobile_and_home_internet_targets_remain_distinct():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_811115fce5604490813e58a1', 'p2lineage_8e195760cd4d34db97e1c9a1')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'
    assert {row.left_target_or_scope, row.right_target_or_scope} == {'mobile_device_internet', 'home_internet'}


def test_home_broadband_is_not_generic_home_internet():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_302e35ca68490e15812f98c9'].governed_target_or_scope == 'home_broadband_internet'
    assert c.loc['p2lineage_8e195760cd4d34db97e1c9a1'].governed_target_or_scope == 'home_internet'


def test_home_access_frequency_is_not_access_availability():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_6d0b6f5e2cc0692ff727f0da'].governed_relation_axis == 'internet_access_frequency'
    assert c.loc['p2lineage_8e195760cd4d34db97e1c9a1'].governed_relation_axis == 'internet_access'


def test_political_discussion_targets_are_not_flattened():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_afde4929ab899ff57b031faf', 'p2lineage_085a8b3be3d8c6525af7de69')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'
    assert {row.left_target_or_scope, row.right_target_or_scope} == {'friends', 'friends_and_colleagues'}


def test_political_persuasion_targets_are_not_flattened():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_407156e90402d04d8178d8d0', 'p2lineage_f95b10429fb776a1f8b5322a')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'
    assert {row.left_target_or_scope, row.right_target_or_scope} == {'friends', 'other_people_unspecified'}


def test_campaign_rally_timeframes_remain_distinct_in_classification():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_6bfa374351c67cbeea78bfd1'].governed_target_or_scope == 'campaign_rally_last_national_election'
    assert c.loc['p2lineage_fa3af0f25f5b76b7b2416733'].governed_target_or_scope == 'election_rally_ever'
    assert c.loc['p2lineage_677ee7ea2987fb2dc041f327'].governed_target_or_scope == 'campaign_or_election_rally_unspecified_period'


def test_protest_disposition_is_not_retrospective_participation():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_67acaa58def29af73a931a70', 'p2lineage_76b84082bd648fe769ea0ce7')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'
    assert {row.left_relation_axis, row.right_relation_axis} == {'protest_disposition', 'protest_participation'}


def test_news_timeframes_remain_operator_bounded():
    _, _, rulings, _, _ = load()
    last_vs_ordinary = pair_row(rulings, 'p2lineage_2a3adcc60effbdaf48644913', 'p2lineage_ec5eeaaf9c01eb49dee7dde2')
    ordinary_vs_general = pair_row(rulings, 'p2lineage_2a3adcc60effbdaf48644913', 'p2lineage_854a85ab4fd9b9b48cdf0549')
    assert last_vs_ordinary.relation_type == 'CONSTRUCT_TARGET_COORDINATE_ONLY'
    assert ordinary_vs_general.relation_type == 'CONSTRUCT_TARGET_COORDINATE_ONLY'
    assert {last_vs_ordinary.left_operator, last_vs_ordinary.right_operator} == {'last_week_days_count','ordinary_week_frequency'}
    assert {ordinary_vs_general.left_operator, ordinary_vs_general.right_operator} == {'ordinary_week_frequency','general_frequency'}


def test_medium_specific_political_news_targets_remain_distinct():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_aa466d9473d5c2d037cec3c9'].governed_target_or_scope == 'political_news_on_television'
    assert c.loc['p2lineage_7da99d408853ea2302587811'].governed_target_or_scope == 'political_news_newspaper_television_radio'
    assert c.loc['p2lineage_928a9732ed37d66494cb18f9'].governed_target_or_scope == 'politics_news_television_radio_newspaper'


def test_medium_confidence_lineages_never_export_proposition_equivalence():
    _, classes, rulings, _, _ = load()
    medium = set(classes[classes.classification_confidence == 'MEDIUM'].lineage_id)
    accepted = rulings[rulings.relation_type == 'REWORDED_PROPOSITION_EQUIVALENCE']
    assert not ((set(accepted.left_lineage_id) | set(accepted.right_lineage_id)) & medium)


def test_prior_tranches_are_not_reintroduced():
    candidates, _, _, _, _ = load()
    trust = pd.read_csv(ROOT / '36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv', dtype=str, keep_default_na=False)
    demo = pd.read_csv(ROOT / '37_P2_GLOBAL_DEMOCRACY_ELECTORAL_FIXED_3000_TRANCHE4/Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv', dtype=str, keep_default_na=False)
    current = set(candidates.semantic_pair_candidate_id)
    assert current.isdisjoint(set(trust.semantic_pair_candidate_id))
    assert current.isdisjoint(set(demo.semantic_pair_candidate_id))


def test_authority_boundary_is_consistent():
    _, classes, rulings, _, _ = load()
    assert (rulings.prohibited_use == 'No J-family authority, value harmonization, or respondent join follows from this ruling.').all()
    assert (classes.prohibited_use == 'Classification coordinate only; no J-family membership, value harmonization, or respondent join.').all()
    assert not rulings.portability_ceiling.str.contains('VALUE|RESPONDENT|J_FAMILY', regex=True).any()


def test_deterministic_rebuild(tmp_path: Path):
    rebuild = tmp_path / 'rebuild'
    env = os.environ.copy()
    env['RAWLSING_V16_ROOT'] = str(ROOT)
    env['RAWLSING_V17_OUT'] = str(rebuild)
    env['RAWLSING_FIXED_3000_SELECTION'] = str(SELECTION)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    subprocess.run([sys.executable, str(BUILDER)], env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    names = [
        'Rawlsing_P2_Media_Civic_Fixed_3000_Tranche_Candidate_Surface_v1.csv',
        'Rawlsing_P2_Media_Civic_Lineage_Classification_v1.csv',
        'Rawlsing_P2_Media_Civic_3000_Pair_Rulings_v1.csv',
        'Rawlsing_P2_Media_Civic_3000_Two_Sided_Evidence_Ledger_v1.csv',
        'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Media_Civic_Fixed_3000_Tranche_v5.csv',
        'FIXED_3000_MEDIA_CIVIC_TRANCHE_RETURN.json',
    ]
    assert {name: sha(OUT / name) for name in names} == {name: sha(rebuild / name) for name in names}
