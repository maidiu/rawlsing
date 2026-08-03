from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(os.environ.get('RAWLSING_V15_ROOT','/mnt/data/rawlsing_v15_build/Rawlsing_J_Family_Authority_Strategy_Handoff_v15_20260731'))
OUT = Path(os.environ.get('RAWLSING_V16_OUT','/mnt/data/rawlsing_v16_outputs/democracy_electoral_3000'))
BUILDER = Path(os.environ.get('RAWLSING_V16_BUILDER','/mnt/data/rawlsing_v16_work/build_democracy_electoral_tranche_v1.py'))


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(OUT / name, dtype=str, keep_default_na=False)


def load():
    return (
        read('Rawlsing_P2_Fixed_3000_Tranche_Candidate_Surface_v1.csv'),
        read('Rawlsing_P2_Democracy_Electoral_Lineage_Classification_v1.csv'),
        read('Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv'),
        read('Rawlsing_P2_Democracy_Electoral_3000_Two_Sided_Evidence_Ledger_v1.csv'),
        read('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv'),
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
    assert len(remaining) == 11847


def test_selection_is_unique_and_partition_exact():
    candidates, _, rulings, _, remaining = load()
    original = pd.read_csv(ROOT / '36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv', dtype=str, keep_default_na=False)
    selected = set(candidates.semantic_pair_candidate_id)
    left = set(remaining.semantic_pair_candidate_id)
    assert len(selected) == 3000
    assert selected.isdisjoint(left)
    assert selected | left == set(original.semantic_pair_candidate_id)
    assert set(rulings.semantic_pair_candidate_id) == selected


def test_selection_contract_counts():
    candidates, *_ = load()
    assert candidates.semantic_content_id.value_counts().to_dict() == {
        'DEMO_EXTENT': 843,
        'CIVIC_VOTE_MATTERS': 810,
        'CIVIC_VOTE': 783,
        'REJECT_STRONGMAN': 333,
        'REJECT_MILITARY': 204,
        'REJECT_ONEPARTY': 27,
    }


def test_stable_ids_are_unique():
    _, classes, rulings, evidence, _ = load()
    assert classes.classification_id.is_unique
    assert rulings.pair_ruling_id.is_unique
    assert evidence.evidence_record_id.is_unique


def test_every_ruling_has_exactly_two_evidence_sides():
    _, _, rulings, evidence, _ = load()
    counts = evidence.groupby('pair_ruling_id').side.agg(list)
    assert set(counts.index) == set(rulings.pair_ruling_id)
    assert all(sorted(v) == ['LEFT', 'RIGHT'] for v in counts)
    assert len(evidence) == 6000


def test_evidence_lineage_and_classification_references_resolve():
    _, classes, rulings, evidence, _ = load()
    assert set(evidence.lineage_id) <= set(classes.lineage_id)
    assert set(evidence.classification_id) <= set(classes.classification_id)
    assert set(evidence.pair_ruling_id) == set(rulings.pair_ruling_id)


def test_proposition_equivalence_requires_axis_target_operator_identity():
    _, classes, rulings, _, _ = load()
    accepted = rulings[rulings.authority_status == 'ACCEPTED_TYPED_DEMOCRACY_ELECTORAL_PROPOSITION_RELATION']
    assert len(accepted) == 13
    assert (accepted.left_relation_axis == accepted.right_relation_axis).all()
    assert (accepted.left_target_or_scope == accepted.right_target_or_scope).all()
    assert (accepted.left_operator == accepted.right_operator).all()
    c = classes.set_index('lineage_id')
    assert all(c.loc[row.left_lineage_id].classification_confidence == 'HIGH' and c.loc[row.right_lineage_id].classification_confidence == 'HIGH' for _, row in accepted.iterrows())


def test_no_medium_or_unresolved_lineage_exports_proposition_equivalence():
    _, classes, rulings, _, _ = load()
    c = classes.set_index('lineage_id')
    accepted = rulings[rulings.relation_type == 'REWORDED_PROPOSITION_EQUIVALENCE']
    for _, row in accepted.iterrows():
        assert c.loc[row.left_lineage_id].authority_status == 'P2_DEMO_ELECTORAL_LINEAGE_CLASSIFIED'
        assert c.loc[row.right_lineage_id].authority_status == 'P2_DEMO_ELECTORAL_LINEAGE_CLASSIFIED'
        assert c.loc[row.left_lineage_id].classification_confidence == 'HIGH'
        assert c.loc[row.right_lineage_id].classification_confidence == 'HIGH'


def test_regular_elections_not_flattened_into_free_fair_elections():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_ad8823b8fce841ec93f4a048', 'p2lineage_ea8609579f8828ca0ab05653')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'


def test_individual_vote_effect_not_flattened_into_honest_elections_effect():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_bc893195eb01f8eedf383c6d', 'p2lineage_31e17acf0134ef6f2f03d094')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'


def test_hybrid_strong_president_military_not_flattened_into_generic_strong_leader():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_a261a2da4eb31bb3fa4ae99e', 'p2lineage_fc2d01c4a569d8582d904c79')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'


def test_defined_democratic_system_not_flattened_into_undefined_generic_item():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_016edfec1d9701aaebce6d29', 'p2lineage_9299cc4c5dc93bf7b372e685')
    assert row.relation_type == 'DOMAIN_COORDINATE_ONLY'


def test_ambiguous_participation_not_certified_as_voting():
    _, _, rulings, _, _ = load()
    row = pair_row(rulings, 'p2lineage_de1dfbc5c6ca3d676c9d4139', 'p2lineage_d1606c2da514ff9c5c3f501e')
    assert row.relation_type == 'NEGATIVE_AUTHORITY'


def test_former_colonial_power_is_not_labeled_spain():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_a2ecb4ae74935326b3205056'].governed_target_or_scope == 'named_country:former_colonial_power_unspecified'
    assert c.loc['p2lineage_6e77a3212ba51b4a23cbb125'].governed_target_or_scope == 'named_country:spain'


def test_named_country_targets_remain_distinct():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    expected = {
        'p2lineage_1157f58d1923ab69709d7a90': 'named_country:china',
        'p2lineage_c4e01502ecb5a9261fc82476': 'named_country:iran',
        'p2lineage_d3a8958775b1491d77b7c7ab': 'named_country:israel',
        'p2lineage_8dfa815352ecf0c46e09c25a': 'named_country:turkey',
        'p2lineage_99f3bd6bad7d7eb8922878fe': 'named_country:united_states',
        'p2lineage_e54acbfdbbcdb1a5263ac7e3': 'named_country:south_africa',
        'p2lineage_e799ccbf6977e297bb674a84': 'named_country:zimbabwe',
    }
    for lineage_id, target in expected.items():
        assert c.loc[lineage_id].governed_target_or_scope == target


def test_temporal_democracy_targets_remain_distinct():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    assert c.loc['p2lineage_74b83e688647e692819f1bc7'].governed_target_or_scope == 'respondent_country_current'
    assert c.loc['p2lineage_baa7eb646bf21458a1f1df58'].governed_target_or_scope == 'respondent_country_past'
    assert c.loc['p2lineage_2c9af85663c5237dc9107c16'].governed_target_or_scope == 'respondent_country_future_desired'


def test_terse_afro_r1_system_ratings_remain_unresolved():
    _, classes, _, _, _ = load()
    c = classes.set_index('lineage_id')
    for lineage_id in ['p2lineage_37b86896fab8c2adc3e8070c','p2lineage_440c5652e50c423b63a8ae59','p2lineage_d24d7cb6c8a6e216141c2753']:
        assert c.loc[lineage_id].authority_status == 'P2_DEMO_ELECTORAL_LINEAGE_UNRESOLVED'


def test_prior_trust_pairs_are_not_reintroduced():
    candidates, _, _, _, _ = load()
    trust = pd.read_csv(ROOT / '36_P2_GLOBAL_TRUST_SEMANTIC_NEIGHBORHOOD_ADJUDICATION_TRANCHE3/Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv', dtype=str, keep_default_na=False)
    assert set(candidates.semantic_pair_candidate_id).isdisjoint(set(trust.semantic_pair_candidate_id))


def test_authority_boundary_is_consistent():
    _, _, rulings, _, _ = load()
    assert (rulings.prohibited_use == 'No J-family authority, value harmonization, or respondent join follows from this ruling.').all()
    assert not rulings.portability_ceiling.str.contains('VALUE|RESPONDENT|J_FAMILY', regex=True).any()


def test_deterministic_rebuild(tmp_path: Path):
    rebuild = tmp_path / 'rebuild'
    env = os.environ.copy()
    env['RAWLSING_V15_ROOT'] = str(ROOT)
    env['RAWLSING_V16_OUT'] = str(rebuild)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    subprocess.run([sys.executable, str(BUILDER)], env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    names = [
        'Rawlsing_P2_Fixed_3000_Tranche_Candidate_Surface_v1.csv',
        'Rawlsing_P2_Democracy_Electoral_Lineage_Classification_v1.csv',
        'Rawlsing_P2_Democracy_Electoral_3000_Pair_Rulings_v1.csv',
        'Rawlsing_P2_Democracy_Electoral_3000_Two_Sided_Evidence_Ledger_v1.csv',
        'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Fixed_3000_Tranche_v4.csv',
        'FIXED_3000_TRANCHE_RETURN.json',
    ]
    assert {name: sha(OUT / name) for name in names} == {name: sha(rebuild / name) for name in names}
