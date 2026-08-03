from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def read(name):
    return pd.read_csv(HERE / name, dtype=str, keep_default_na=False)


CLASS = read('Rawlsing_P2_Trust_Lineage_Axis_Target_Classification_v2.csv').set_index('lineage_id')
RULINGS = read('Rawlsing_P2_Trust_Neighborhood_Pair_Rulings_v2.csv')
EVIDENCE = read('Rawlsing_P2_Trust_Neighborhood_Two_Sided_Evidence_Ledger_v2.csv')
REMAINING = read('Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Trust_Tranche_v3.csv')


def pair(left, right):
    mask = (
        ((RULINGS.left_lineage_id == left) & (RULINGS.right_lineage_id == right)) |
        ((RULINGS.left_lineage_id == right) & (RULINGS.right_lineage_id == left))
    )
    result = RULINGS[mask]
    assert len(result) == 1
    return result.iloc[0]


def test_cardinality_and_queue_partition():
    assert len(CLASS) == 562
    assert len(RULINGS) == 3863
    assert len(REMAINING) == 14847
    assert len(RULINGS) + len(REMAINING) == 18710
    assert RULINGS.semantic_pair_candidate_id.is_unique
    assert set(RULINGS.semantic_pair_candidate_id).isdisjoint(set(REMAINING.semantic_pair_candidate_id))


def test_evidence_is_exactly_two_sided_per_ruling():
    assert len(EVIDENCE) == 7726
    counts = EVIDENCE.groupby('trust_pair_ruling_id').size()
    assert counts.eq(2).all()
    sides = EVIDENCE.groupby('trust_pair_ruling_id').side.apply(set)
    assert all(value == {'LEFT', 'RIGHT'} for value in sides)
    assert set(EVIDENCE.trust_pair_ruling_id) == set(RULINGS.trust_pair_ruling_id)


def test_proposition_equivalence_requires_exact_axis_and_target():
    accepted = RULINGS[RULINGS.authority_status == 'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION']
    assert (accepted.left_relation_axis == accepted.right_relation_axis).all()
    assert (accepted.left_target_entity == accepted.right_target_entity).all()
    assert accepted.relation_type.eq('REWORDED_PROPOSITION_EQUIVALENCE').all()


def test_heterogeneous_source_lineage_is_unresolved():
    lineage = CLASS.loc['p2lineage_10daf1f92d9d657d326d208c']
    assert lineage.governed_relation_axis == 'trust_target_heterogeneous'
    assert lineage.governed_target_entity == 'heterogeneous_target_lineage'
    related = RULINGS[(RULINGS.left_lineage_id == lineage.name) | (RULINGS.right_lineage_id == lineage.name)]
    assert related.authority_status.eq('UNRESOLVED_INSUFFICIENT_OR_HETEROGENEOUS_RELATION_AXIS_OR_TARGET_EVIDENCE').all()



def test_pollice_typo_lineage_recovers_police_assistance_target():
    lineage_id = 'p2lineage_f47e6b84e36bddf926693820'
    lineage = CLASS.loc[lineage_id]
    assert lineage.governed_relation_axis == 'service_access_difficulty'
    assert lineage.governed_target_entity == 'police_assistance_service'
    assert lineage.observed_exact_text_targets_json == '["police_assistance_service"]'
    row = pair(lineage_id, 'p2lineage_dd092cb8562e63bdd9e36bea')
    assert row.authority_status == 'ACCEPTED_NONTRUST_RELATION_REDIRECTED_FROM_CONTAMINATED_TRUST_NEIGHBORHOOD'
    assert row.relation_type == 'REWORDED_PROPOSITION_EQUIVALENCE'

def test_cabinet_and_prime_minister_are_coordinate_only():
    row = pair('p2lineage_9140f344f08e88eb9bdcccff', 'p2lineage_fd3ef2e210c6298b9d35f26f')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'
    assert row.relation_type == 'TARGET_RELATION_COORDINATE_ONLY'


def test_family_and_co_resident_family_are_coordinate_only():
    row = pair('p2lineage_a431c3ecc261195a668ffaf3', 'p2lineage_b861794ba82ef8c7be2f3e96')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'


def test_opposition_and_generic_parties_are_coordinate_only():
    row = pair('p2lineage_f3a65004b83da779f79d7f2a', 'p2lineage_6cfc2c25546f4102569aece4')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'


def test_comparative_and_absolute_social_media_trust_are_not_equivalent():
    row = pair('p2lineage_a7df14a03a46e06155004b31', 'p2lineage_e16b6c4020a44c465f6e0c00')
    assert row.authority_status == 'ACCEPTED_TRUST_CONSTRUCT_OR_TARGET_COORDINATE_ONLY'
    assert row.relation_type == 'TRUST_CONSTRUCT_COORDINATE_ONLY'


def test_police_station_and_police_are_coordinate_only():
    row = pair('p2lineage_779b9d4268bc2f23fb76c58e', 'p2lineage_08416d4c0d4434c38c7ecd47')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'


def test_american_courts_and_generic_courts_are_coordinate_only():
    row = pair('p2lineage_3b47a4c611bb0054486f99eb', 'p2lineage_db7307040843c0042debe2d0')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'


def test_shura_council_is_not_flattened_to_parliament():
    lineage = CLASS.loc['p2lineage_309f41fbd8a9f147efd7cff0']
    assert lineage.governed_target_entity == 'shura_council'
    related = RULINGS[(RULINGS.left_lineage_id == lineage.name) | (RULINGS.right_lineage_id == lineage.name)]
    false_equivalence = related[(related.authority_status == 'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION') & (related.left_target_entity != related.right_target_entity)]
    assert false_equivalence.empty


def test_military_governing_council_is_not_flattened_to_army():
    lineage = CLASS.loc['p2lineage_b3bb45cdc726e14351c55506']
    assert lineage.governed_target_entity == 'military_governing_council'
    related = RULINGS[(RULINGS.left_lineage_id == lineage.name) | (RULINGS.right_lineage_id == lineage.name)]
    false_equivalence = related[(related.authority_status == 'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION') & (related.left_target_entity != related.right_target_entity)]
    assert false_equivalence.empty


def test_generalized_fellow_citizens_is_not_flattened_to_people_in_general():
    row = pair('p2lineage_d6366162c024759b0b7345c5', 'p2lineage_570016fa3c3eb4ef1e65fe09')
    assert row.authority_status == 'ACCEPTED_NESTED_OR_FUNCTIONAL_TRUST_TARGET_COORDINATE_ONLY'


def test_online_acquaintances_is_interpersonal_trust():
    row = CLASS.loc['p2lineage_7fa349925a94676d493515b4']
    assert row.governed_relation_axis == 'interpersonal_trust'
    assert row.governed_target_entity == 'online_acquaintances'


def test_nontrust_contamination_never_inherits_trust_authority():
    contaminated = RULINGS[
        (RULINGS.left_relation_axis.isin({'service_access_difficulty', 'institutional_performance', 'membership_participation', 'corruption_perception'})) |
        (RULINGS.right_relation_axis.isin({'service_access_difficulty', 'institutional_performance', 'membership_participation', 'corruption_perception'}))
    ]
    assert not contaminated.authority_status.isin({
        'ACCEPTED_TYPED_CROSS_SOURCE_TRUST_RELATION',
        'ACCEPTED_TRUST_CONSTRUCT_COORDINATE_WITH_DERIVED_INDEX',
    }).any()
