"""Original35 metadata accounting and actual native fail-closed boundaries.

No test in this module claims a newly executed original-source positive.
"""
from collections import Counter
import csv
import gzip
import hashlib
import json
from pathlib import Path
import sys

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[1]))
import authority_binding as binding
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog, CarrierExecutionBindingError
from rawlsing_next.pre553_c11_repository import C11Repository
from rawlsing_next.pre553_empirical_objects import ExactRef, Pre553IntegrityError


@pytest.fixture(scope='module')
def doc():
    return binding.matrix()


@pytest.fixture(scope='module')
def freeze():
    return json.loads((HERE / 'evidence/PREIMPLEMENTATION_FREEZE.json').read_text())


def test_all_metadata_preimages_exact():
    receipt = binding.verify_inputs()
    assert len(receipt) == 53
    assert {r['state'] for r in receipt} == {'EXACT'}


def test_original_owner_rows_at_exact_ordinals():
    rows = binding.audit_owner_rows()
    assert Counter(r['owner'] for r in rows) == {
        'register_A': 40, 'register_B': 40, 'v525b_semantic': 10,
        'v525b_drivers': 10, 'd62_driver_provenance_only': 10,
    }


def test_direct_original_26_plus_9(doc, freeze):
    p2_rows, p2, common, blocked = binding.original_sets(doc)
    assert len(p2_rows) == len(p2) == 18276
    assert len(common) == 18250
    assert sorted(p2 - common) == freeze['expected_p2_only_sha256']
    actual = sorted((w['atlas_id'], i['question_id'], i['var_code'], i['governed_row_payload_hash'])
                    for w in doc['waves'] for i in w['items'] if i['p2_exact_identity_sha256'] is None)
    expected = sorted((r['atlas_id'], r['question_id'], r['var_code'], r['qra_row_hash'])
                      for r in freeze['expected_qra_only_blocked'])
    assert actual == expected
    assert len(blocked) == 9


def test_declared_accounting_no_drop(doc, freeze):
    # Oracle is the separately committed preimplementation original-input freeze.
    expected_bytes = gzip.decompress((HERE / 'evidence/FROZEN_EXPECTED_declared_accounting.jsonl.gz').read_bytes())
    assert hashlib.sha256(expected_bytes).hexdigest() == freeze['declared_accounting_not_E_pre']['sha256']
    expected = [tuple(json.loads(line)) for line in expected_bytes.splitlines()]
    actual = list(binding.accounting_units(doc))
    delta = binding.anti_join(expected, actual)
    assert delta['missing'] == []
    assert delta['unexpected'] == []
    assert len(actual) == freeze['declared_accounting_not_E_pre']['unit_count']
    assert hashlib.sha256(binding.unit_bytes(actual)).hexdigest() == freeze['declared_accounting_not_E_pre']['sha256']


def test_anti_join_retains_typed_held_method(doc):
    expected = list(binding.accounting_units(doc))
    missing = next(x for x in expected if x[3] == 'I03_GOVERNED_WEIGHTED')
    actual = [x for x in expected if x != missing]
    delta = binding.anti_join(expected, actual)
    assert delta == {'missing': [missing], 'unexpected': []}
    assert doc['original_operation_status_default']['I03_GOVERNED_WEIGHTED'] == binding.HOLD


def test_historical_unknown_and_no_weight_are_not_dropped(freeze):
    with (binding.INPUT / 'as2b/06_I03_CERTIFICATION_RECEIPT.csv').open() as f:
        rows = list(csv.DictReader(f))
    executed = [r for r in rows if r['execution'] == 'EXECUTED']
    assert [r['operation'] for r in executed] == freeze['historical_operation_declarations']
    assert Counter(r['result_state'] for r in executed) == {'UNRESOLVED': 6, 'SUPPORTED': 1, 'UNAVAILABLE': 1}
    positive = next(r for r in executed if r['operation'] == 'recursive_and_or_not')
    assert positive['empirical_fact_hash'] == freeze['historical_positive']['fact_hash']
    assert (positive['raw_numerator_support'], positive['raw_denominator_support']) == ('5155', '5155')
    assert len([r for r in rows if r['execution'] == 'NOT_EXECUTED']) == 4


def test_all35_no_eligibility_or_permission_self_issued(doc):
    waves = binding.all35(doc)
    assert len(waves) == 35
    assert sum(w['qra_items'] for w in waves) == 18259
    assert sum(w['declared_candidate_profile_units_not_E_pre'] for w in waves) == 127813
    for w in waves:
        assert w['permission_warrant_ref'] is None
        assert w['competent_original_U_ref'] is None
        assert w['competent_original_E_pre_ref'] is None
        assert w['eligible_original_count'] is None
        assert w['current_permitted'] == 0
        assert w['new_original_runs'] == 0
        assert set(w['operation_statuses'].values()) == {binding.HOLD}


def test_party_is_substantive_and_six_admin_only():
    rows = binding.decisions()
    p2 = [r for r in rows if r['side'] == 'P2_ONLY']
    admin = [r['variable'] for r in p2 if r['classification'] == 'ADMIN_OR_CARRIER']
    assert sorted(admin) == ['casenumb', 'enc', 'numero', 'pais', 'region', 'wt']
    assert len(p2) - len(admin) == 20
    party = next(r for r in p2 if r['variable'] == 'party')
    assert party['inherited_role'] == 'substantive_nominal_choice'
    assert party['execution_permission'] == binding.HOLD
    assert '112 historical source labels' in party['scientific_note']


@pytest.mark.parametrize('variable,alias', [('Q45ST', 'P45ST'), ('Q47STC', 'P47ST.C'),
    ('Q8NCVA', 'P8NCV.A'), ('Q8NCVB', 'P8NCV.B'), ('Q8NCVC', 'P8NCV.C')])
def test_alias_is_candidate_not_physical_identity(variable, alias):
    row = next(r for r in binding.decisions() if r['variable'] == variable)
    assert row['physical_alias_candidate'] == alias
    assert row['source_version']['actual_source_edition_hash'] == 'UNBOUND'
    assert row['form'] == 'UNBOUND_REQUIRES_ORIGINAL_SOURCE_OWNER'
    assert row['execution_permission'] == binding.HOLD


def test_duplicate_q47st_assertions_not_last_row_wins():
    owner = binding.load('wg0x/sources/owner_row_projections.json')
    rows = [r for r in owner['v525b_semantic']['selected_records'] if r['exact_case_key'][-1] == 'Q47ST']
    assert [r['csv_record'] for r in rows] == [4895, 4896]
    assert len({r['row_sha256'] for r in rows}) == 2
    assert len({r['row']['display_text'] for r in rows}) == 2
    held = next(r for r in binding.decisions() if r['variable'] == 'Q47ST')
    assert held['classification'] == 'DUPLICATE_KEY_DISTINCT_ACCEPTED_MEANINGS'
    assert held['p2_exact_identity_sha256'] is None


@pytest.mark.parametrize('variable', ['P43', 'P47'])
def test_v525b_d62_disagreement_not_semantic_succession(variable):
    owner = binding.load('wg0x/sources/owner_row_projections.json')
    v = [r['row'] for r in owner['v525b_drivers']['selected_records']
         if r['exact_case_key'] == ['Latinobarómetro', '1995', variable]]
    d = [r['row'] for r in owner['d62_driver_provenance_only']['selected_records']
         if r['exact_case_key'] == ['Latinobarómetro', '1995', variable]]
    assert len(v) == len(d) == 1
    assert v[0]['final_driver_id'] == {'P43': 'genderEquality', 'P47': 'temporalOrientation'}[variable]
    assert v[0]['final_driver_id'] != d[0]['driver_id']
    assert d[0]['driver_id'] == 'imperialAlignment'
    assert next(r for r in binding.decisions() if r['variable'] == variable)['execution_permission'] == binding.HOLD


def test_eu_country_items_do_not_become_joint_battery():
    rows = [r for r in binding.decisions() if r['variable'].startswith('p46')]
    assert {r['variable'] for r in rows} == {'p46' + x for x in 'abcdefgh'}
    assert {r['inherited_role'] for r in rows} == {'structural_context'}
    assert all('NO_DIRECTED_SCALE_OR_JOINT_BATTERY_ISSUED' in r['operation_binding_decision'] for r in rows)


def test_route_form_weight_time_respondent_gaps_remain_explicit():
    required = {'administered_form_and_physical_item', 'country_population_and_time',
                'respondent_person_household_namespace', 'routing_and_risk_denominator',
                'weights_design_or_explicit_raw_mode', 'repeat_missing_and_duplicate_respondent_policy'}
    for r in binding.decisions():
        assert required <= r['owner_packet_missing'].keys()
        assert r['new_native_product'] == 'NOT_RUN'


def test_inactive_rows_and_76_p10_holds_preserved():
    inactive = (binding.INPUT / 'wg0x/evidence/excluded_inactive_ledger.jsonl').read_text().splitlines()
    assert len(inactive) == 259
    with (binding.INPUT / 'p10/03_P10_FINAL_AUTHORITY_FUNCTION_CENSUS.csv').open() as f:
        census = list(csv.DictReader(f))
    held = [r for r in census if r['primary_disposition'] == 'PRESERVED_AS_EXACT_UNRESOLVED/BLOCKED_AUTHORITY']
    assert sum(int(r['unit_count']) for r in census) == 65354
    assert sum(int(r['unit_count']) for r in held) == 76
    assert sorted(int(r['unit_count']) for r in held) == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 15, 42]


def test_receipt_summary_cannot_materialize_native_catalog(freeze):
    # Actual native entry point, historical fact hash only: no counterfeit query.
    receipt_only = {'kind': 'EmpiricalFact', 'hash': freeze['historical_positive']['fact_hash']}
    with pytest.raises((CarrierExecutionBindingError, Pre553IntegrityError), match='preimage|document|public|object|kind|family|fields'):
        RuntimeObjectCatalog.from_documents(authority_documents=(), predicate_documents=(), query_documents=[receipt_only])


def test_historical_release_ref_cannot_resolve_without_c11_preimage():
    ref = ExactRef('C11LogicalRelease', 'LITS1-AS2B-C11-7cac43e2ca5b31cb-9dd1e6b7350ebb79',
                   'e6c954538fa1830820120465a10a6d065b8a18d1e6b7b08d3f863b0917741e26')
    with pytest.raises(KeyError):
        C11Repository().resolve_release_exact(ref)
