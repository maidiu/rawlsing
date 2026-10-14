"""Source-free gap court against exact P01 owner, never an empirical issuer.

Run from /tmp exact P01 extraction with this file as an absolute pytest target.
Tests named gap prove observed deficiencies; green is reproduction, not closure.
"""
import json
from copy import deepcopy
from dataclasses import replace
import pytest
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next import pre553_original_workload_v2_verifier_candidate as V
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next.pre553_batch_runner import BatchManifest
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture


def keys(row):
    version = C.V2_SCHEMA_VERSION
    item = V.reconstruct_item_key(row, version)
    sem = V.reconstruct_semantic_op_key(row, version)
    dispatch = V.reconstruct_dispatch_op_key(row, version)
    return item, sem, dispatch, V.reconstruct_expected_key(item, sem, dispatch, row, version)


def payload(kwargs):
    return json.loads(kwargs['expected'].payload_json)


@pytest.mark.parametrize('field', ['respondent_namespace', 'language', 'routing_identity',
                                  'administered_occurrence', 'option_identity'])
def test_gap_original_variants_collide_in_published_v2_keys(tmp_path, field):
    kwargs, _ = _fixture(tmp_path)
    a = payload(kwargs)['declarations'][0]
    b = deepcopy(a)
    a[field], b[field] = 'SOURCEFREE-ORIGINAL-A', 'SOURCEFREE-ORIGINAL-B'
    assert a != b
    assert keys(a) == keys(b)


def test_form_source_direction_measure_and_condition_are_key_distinct(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    a = payload(kwargs)['declarations'][0]
    for field, value in [('form', 'F2'), ('source_identity', 'sourcefree-B'),
                         ('condition_order', ['Y', 'X']), ('measure_kind', 'GOVERNED_WEIGHTED'),
                         ('semantic_roles', ['TARGET', 'CONDITIONER'])]:
        b = deepcopy(a); b[field] = value
        assert keys(a)[-1] != keys(b)[-1], field


def test_gap_query_predicate_refs_are_indirect_not_in_expected_key(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    a = payload(kwargs)['declarations'][0]
    b = deepcopy(a)
    b['query_ref']['content_hash'] = 'a' * 64
    b['predicate_ref']['content_hash'] = 'b' * 64
    assert keys(a) == keys(b)


def test_independent_expected_a_plus_b_selected_a_only_fails_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    frozen_before = kwargs['expected'].payload_sha256
    original = kwargs['session']
    kwargs['session'] = replace(original, manifest=BatchManifest(original.manifest.units[:1]))
    with pytest.raises(ValueError, match='EXPECTED_OPERATION_OMITTED'):
        P.run_integrated(**kwargs)
    assert calls == [] and kwargs['expected'].payload_sha256 == frozen_before


def test_j_only_drops_independent_i03_work_and_is_rejected(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    original = kwargs['session']
    kwargs['session'] = replace(original, manifest=BatchManifest(tuple(
        u for u in original.manifest.units if u.job_kind == 'DISCOVERY')))
    with pytest.raises(ValueError, match='EXPECTED_OPERATION_OMITTED'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_same_person_substitution_rejected_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = payload(kwargs)
    doc['source_inventory'][0]['respondent_ref']['content_hash'] = '3' * 64
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='ORIGINAL_RESPONDENT_ITEM_CONFIGURATION_MISMATCH'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_two_forms_cannot_share_one_owner_job(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = payload(kwargs)
    b = deepcopy(doc['declarations'][0]); b['form'] = 'F2'
    assert keys(b)[-1] != keys(doc['declarations'][0])[-1]
    doc['declarations'].append(b)
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='DUPLICATE_OWNER_JOB_REF'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_gap_namespace_variants_reach_identical_actual_consumer(tmp_path):
    reports = []
    for variant in ['SOURCEFREE-NS-A', 'SOURCEFREE-NS-B']:
        kwargs, calls = _fixture(tmp_path / variant)
        doc = payload(kwargs)
        for row in doc['declarations']:
            row['respondent_namespace'] = variant
        kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
        report = P.run_integrated(**kwargs)
        assert report['ok'] and len(calls) == 3
        reports.append(report)
    assert reports[0]['consumer_products'] == reports[1]['consumer_products']
    assert len(reports[0]['source_inventory']) == 18


def test_gap_selected_manifest_self_certification_passes_while_original_b_is_missing(tmp_path):
    from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
    kwargs, calls = _fixture(tmp_path / 'original')
    original_expected = payload(kwargs)
    original = kwargs['session']
    selected = next(u for u in original.manifest.units if u.job_kind == 'QUERY')
    selected_ref = selected.job_ref.as_dict()
    selected_doc = deepcopy(original_expected)
    selected_doc['declarations'] = [r for r in selected_doc['declarations']
        if r.get('state') != 'RUNNABLE' or r.get('query_ref') == selected_ref]
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(selected_doc)
    kwargs['session'] = G.open_session(manifest=BatchManifest((selected,)),
        repository=original.repository, executors=original.executors,
        root=tmp_path / 'selected-only', source_sha256=original.source_sha256)
    local = P.run_integrated(**kwargs)
    assert local['ok'] and len(calls) == 1 and len(local['consumer_products']) == 1
    original_keys = {keys(r)[-1] for r in original_expected['declarations'] if r['state'] == 'RUNNABLE'}
    selected_keys = {keys(r)[-1] for r in selected_doc['declarations'] if r['state'] == 'RUNNABLE'}
    assert len(original_keys - selected_keys) == 2
    # This green local run proves exactly why the independent original E must stay frozen.


@pytest.mark.parametrize('kind,diagnostic', [
    ('UNARY', 'FIELD_FORGE_OPERATION_UNSUPPORTED'),
    ('TRIPLE_DECLARATION_OVER_PAIR_JOB', 'CONDITION_ORDER_SUBSTITUTION'),
])
def test_unsupported_original_scope_cannot_be_laundered_through_pair_consumer(tmp_path, kind, diagnostic):
    kwargs, calls = _fixture(tmp_path)
    doc = payload(kwargs)
    row = next(r for r in doc['declarations'] if 'query_ref' in r)
    if kind == 'UNARY':
        row['semantic_op_class'] = 'UNARY_DISTRIBUTION'
    else:
        row['condition_order'] = ['X', 'Y', 'Z']
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match=diagnostic):
        P.run_integrated(**kwargs)
    assert calls == []
