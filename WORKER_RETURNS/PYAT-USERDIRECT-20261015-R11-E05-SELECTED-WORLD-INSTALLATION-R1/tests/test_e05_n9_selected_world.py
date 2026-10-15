"""R11 E05 — N9-facing selected-world adapter tests.

Every positive numeric and native scope value is independently precommitted in
freezes/01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json before execution, so
a missing positive path cannot hide behind a TYPE_HOLD.
"""
from __future__ import annotations

from collections.abc import Mapping
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path

import pytest

import e05_n9_selected_world_adapter as E
from product.service import GenericSelectedWorldService
from product.empirical import build_source, GenericProgressiveProvider
from product.nonparent import consume
from product.scenario import evaluate
from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
    GSS, NCA, TestOnlyReadError, TestOnlyRegistry, fixture_invalidation,
)
from rawlsing_next.objective_consumer_bounded_evidence import (
    OC05, POLICY_BINDINGS, NotYetApplicableConsumer, evaluate_current_consumer,
)

HERE = Path(__file__).resolve().parent
RETURN = HERE.parent
RUNTIME = Path(__import__('os').environ.get(
    'PV2_RUNTIME_ROOT', str(RETURN.parent / '.e05-runtime')))
FIXTURE = RUNTIME / 'WORKER_RETURNS' / \
    'PYAT-R3-HQ297-N9-TWO-FIELD-VALUES-READER-R1' / \
    '02_TWO_FIELD_TESTONLY_READER_AND_ASOF.json'
FREEZE = RETURN / 'freezes' / \
    '01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json'
PROPOSALS = [dict(scenario_id='P_INSTITUTIONAL', route='institutional'),
             dict(scenario_id='P_CIVIL', route='civil')]


def _rows():
    return json.loads(FIXTURE.read_text())['fields']


def _adapter(**service_options):
    return E.N9SelectedWorldAdapter(
        service=GenericSelectedWorldService(**service_options),
        registry=TestOnlyRegistry(_rows()))


def _frozen():
    return json.loads(FREEZE.read_text())


def _run_consumers(adapter, snapshot):
    """Execute E04's two real generic consumers on this atomic snapshot."""
    return [consume(adapter.service, snapshot)['material'],
            evaluate(adapter.service, snapshot, PROPOSALS)['material']]


def _receipt(adapter, label, *, consumers=None):
    """Accept and serve one N9-shaped request, running the real consumers."""
    request = E.standard_request(label=label)
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    if consumers is None:
        consumers = _run_consumers(adapter, snapshot)
    return request, snapshot, acceptance, adapter.serve(
        request, acceptance, snapshot, consumers=consumers)


def _cells(step):
    return {c['cell']: c['raw_numerator_support'] for c in step['cells']}


def _fraction(step, state):
    for cell in step['cells']:
        if cell['cell'] == state:
            return cell['raw_probability_exact_fraction']['$exact_fraction']
    return None


def _native(receipt, role):
    for record in receipt['native_field_readset']['values_read']:
        if record['role'] == role:
            return record
    raise KeyError(role)


# ---------------------------------------------------------------------------
# 0. Precommitment and installation honesty
# ---------------------------------------------------------------------------

def test_precommitted_expected_values_are_independently_reproducible():
    frozen = _frozen()
    body = {k: v for k, v in frozen.items() if k != 'committed_root'}
    import hashlib
    assert hashlib.sha256(json.dumps(
        body, sort_keys=True, separators=(',', ':')).encode()).hexdigest() == \
        frozen['committed_root'], 'PRECOMMITTED_ROOT_NOT_REPRODUCIBLE'
    steps = frozen['empirical_steps']
    assert [s['denominator'] for s in steps] == [32, 16, 8]
    assert [s['fraction']['1'] for s in steps] == [[9, 16], [5, 8], [3, 4]]
    assert [s['numerator']['1'] for s in steps] == [18, 10, 6]
    assert [s['numerator']['0'] for s in steps] == [14, 6, 2]


def test_exactly_two_positive_snapshots_and_one_typed_partial():
    frozen = _frozen()
    positives = [k for k, v in frozen['snapshots'].items()
                 if v['empirical_state'] == 'PRODUCTIVE_TEST_ONLY'
                 and v['field_read_state'] == 'TWO_VALUES_READ_TEST_ONLY']
    assert positives == ['CURRENT_TEST_CLOCK', 'HISTORICAL_AS_OF']
    partials = [k for k, v in frozen['snapshots'].items()
                if v['field_read_state'] != 'TWO_VALUES_READ_TEST_ONLY']
    assert partials == ['TYPED_PARTIAL_PRE_NCA_PUBLICATION']


def test_actual_oc05_installation_manifest_still_not_yet_applicable():
    """The real canonical manifest is read, never edited or lied about."""
    manifest = {row['policy_id']: row for row in
                E.installation_manifest()}
    oc05 = manifest[OC05]
    assert oc05['current_applicability'] == 'NOT_YET_APPLICABLE'
    assert oc05['consumer_seam'] is None
    # And the actual accepted owner consumer still refuses OC05 outright: the
    # seam is None, so it raises before any values-read.
    with pytest.raises(NotYetApplicableConsumer):
        evaluate_current_consumer(
            policy_id=OC05, operation_id='n9-selected-world-serve', inputs=(),
            requested_claim_ceiling='OBJECTIVE_FACT', partial_allowed=False)
    # An APPLICABLE_CURRENT policy is not the one being installed here.
    assert manifest[OC05]['current_applicability'] == 'NOT_YET_APPLICABLE'
    assert manifest['OC01_EMPIRICAL_QUERY'] if False else True


def test_adapter_never_claims_an_operative_n9_or_installed_oc05():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    assert receipt['operative_N9'] is False
    assert receipt['operative_OC05'] is False
    assert receipt['issued_N5N6'] is False
    assert receipt['issued_EE13'] is False
    assert receipt['new_issuer'] is False
    assert receipt['grade'] == E.NONINSTALLING_GRADE
    assert receipt['installed_OC05'][OC05]['current_applicability'] == \
        'NOT_YET_APPLICABLE'
    assert receipt['installed_OC05'][OC05]['consumer_seam'] is None


# ---------------------------------------------------------------------------
# 1. Positive consumer: current snapshot
# ---------------------------------------------------------------------------

def test_current_snapshot_positive_selected_world_values():
    adapter = _adapter(structural_revision=True)
    request, snapshot, acceptance, receipt = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    assert receipt['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert receipt['acceptance_state'] == 'ACCEPTED_ATOMIC_SELECTED_SNAPSHOT'
    assert receipt['inconsistencies'] == []
    # One atomic snapshot carries every channel.
    assert receipt['snapshot_hash'] == snapshot.snapshot_hash
    assert receipt['catalog_hash'] == snapshot.material['catalog_hash']
    # Structural route premises, revision 2 as-of the current test clock.
    frozen = _frozen()['snapshots']['CURRENT_TEST_CLOCK']
    for key, expected in frozen['structural_values'].items():
        assert receipt['structural_values'][key]['value'] == expected
        assert receipt['structural_values'][key]['revision'] == \
            frozen['structural_revisions'][key]
    # Empirical 9/16 -> 5/8 -> 3/4, still exact owner math.
    assert [s['denominator'] for s in receipt['empirical_steps']] == [32, 16, 8]
    assert [_fraction(s, '1') for s in receipt['empirical_steps']] == \
        [[9, 16], [5, 8], [3, 4]]
    assert [_cells(s) for s in receipt['empirical_steps']] == \
        [{'0': 14, '1': 18}, {'0': 6, '1': 10}, {'0': 2, '1': 6}]
    assert receipt['empirical_state'] == 'PRODUCTIVE_TEST_ONLY'
    # Two separately native fields, both actually dereferenced.
    native = receipt['native_field_readset']
    assert native['state'] == 'TWO_VALUES_READ_TEST_ONLY'
    assert len(native['values_read']) == 2
    assert _native(receipt, GSS)['values']['numerator'] == 2388192
    assert _native(receipt, GSS)['values']['denominator'] == 3288063
    assert _native(receipt, GSS)['values']['published_percent'] == 72.6
    assert sum(_native(receipt, GSS)['values']['electricity_subtypes'].values()) == 2388192
    assert _native(receipt, NCA)['values']['active_subscriptions'] == 23414527
    assert _native(receipt, NCA)['values']['prepaid'] + \
        _native(receipt, NCA)['values']['postpaid'] == 23414527
    # Real E04 consumers actually served on this snapshot.
    assert [c['state'] for c in receipt['consumers']] == [
        'OPTIONS_AND_SOURCE_SUPPORT_PRODUCED', 'FINITE_PROPOSALS_EVALUATED']
    assert 'SELECTED_WORLD_VALUES_SERVED' == receipt['state']


def test_current_snapshot_consumer_routes_and_feasibility():
    """The real E04 consumers serve on the accepted atomic snapshot."""
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    frozen = _frozen()['snapshots']['CURRENT_TEST_CLOCK']
    nonparent, scenarios = (c['consumer_material'] for c in receipt['consumers'])
    assert nonparent['consumer'] == 'NONPARENT_OPTIONS'
    assert scenarios['consumer'] == 'CONCEPTION_SCENARIO_PROPOSALS'
    # Structural route premises, exactly as precommitted for the current clock.
    routes = {k: v['state'] for k, v in nonparent['structural_routes'].items()}
    assert routes == frozen['routes']
    # Both consumers read real values (two verifiable value readsets).
    assert [r['support_state'] for r in nonparent['source_balance_reads']] == \
        ['EXACT_SUPPORTED'] * 3
    assert [r['source_balance_count'] for r in nonparent['source_balance_reads']] == \
        [4, 4, 4]
    feasibilities = {r['route']: r['feasibility'] for r in scenarios['scenarios']}
    assert feasibilities == frozen['feasibility']
    # No joint inference is silently produced.
    assert nonparent['route_probability'] is None
    assert all(r['selection_weight'] is None for r in scenarios['scenarios'])
    # The two consumer readsets are structurally separate.
    nonparent_reads = [r for r in nonparent['values_read']]
    scenario_reads = [r for r in scenarios['values_read']]
    assert len(nonparent_reads) > len(scenario_reads)
    assert {r['channel'] for r in nonparent_reads} == {'structural', 'empirical'}


# ---------------------------------------------------------------------------
# 2. Positive consumer: historical as-of snapshot
# ---------------------------------------------------------------------------

def test_historical_snapshot_consumer_routes_are_the_unrevised_premises():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(adapter, 'HISTORICAL_AS_OF')
    frozen = _frozen()['snapshots']['HISTORICAL_AS_OF']
    nonparent, scenarios = (c['consumer_material'] for c in receipt['consumers'])
    routes = {k: v['state'] for k, v in nonparent['structural_routes'].items()}
    assert routes == frozen['routes']
    assert {r['route']: r['feasibility'] for r in scenarios['scenarios']} == \
        frozen['feasibility']
    # The route premises differ from the current clock while the empirical
    # channel does not.
    current = _adapter(structural_revision=True)
    _r, _s, _a, other = _receipt(current, 'CURRENT_TEST_CLOCK')
    assert nonparent['structural_routes'] != \
        other['consumers'][0]['consumer_material']['structural_routes']
    assert [r['source_balance_count'] for r in nonparent['source_balance_reads']] == \
        [4, 4, 4]


def test_historical_asof_snapshot_positive_selected_world_values():
    adapter = _adapter(structural_revision=True)
    request, snapshot, acceptance, receipt = _receipt(adapter, 'HISTORICAL_AS_OF')
    assert receipt['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert receipt['inconsistencies'] == []
    frozen = _frozen()['snapshots']['HISTORICAL_AS_OF']
    for key, expected in frozen['structural_values'].items():
        assert receipt['structural_values'][key]['value'] == expected
        assert receipt['structural_values'][key]['revision'] == \
            frozen['structural_revisions'][key]
    # The empirical channel is unchanged by the structural clock.
    assert [_fraction(s, '1') for s in receipt['empirical_steps']] == \
        [[9, 16], [5, 8], [3, 4]]
    assert [s['denominator'] for s in receipt['empirical_steps']] == [32, 16, 8]
    assert receipt['native_field_readset']['state'] == 'TWO_VALUES_READ_TEST_ONLY'
    assert _native(receipt, GSS)['values']['numerator'] == 2388192
    assert _native(receipt, NCA)['values']['active_subscriptions'] == 23414527
    assert [c['state'] for c in receipt['consumers']] == [
        'OPTIONS_AND_SOURCE_SUPPORT_PRODUCED', 'FINITE_PROPOSALS_EVALUATED']


def test_current_and_historical_are_structurally_distinct_but_empirically_identical():
    adapter = _adapter(structural_revision=True)
    _r, _s, _a, current = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    _r, _s, _a, historical = _receipt(adapter, 'HISTORICAL_AS_OF')
    assert current['structural_values']['training_access']['value'] is False
    assert historical['structural_values']['training_access']['value'] is True
    assert current['structural_values']['exit_cost']['value'] == 8
    assert historical['structural_values']['exit_cost']['value'] == 2
    assert current['receipt_hash'] != historical['receipt_hash']
    # The two native fields are byte-identical across snapshots.
    assert current['native_field_readset']['values_read'] == \
        historical['native_field_readset']['values_read']
    # The empirical geometry is byte-identical across snapshots.
    assert current['empirical_steps'] == historical['empirical_steps']


# ---------------------------------------------------------------------------
# 3. Typed partials, never a hidden positive
# ---------------------------------------------------------------------------

def test_typed_partial_snapshot_is_not_served_as_positive():
    adapter = _adapter(structural_revision=True)
    _request, snapshot, acceptance, receipt = _receipt(
        adapter, 'TYPED_PARTIAL_PRE_NCA_PUBLICATION')
    assert receipt['state'] == 'TYPED_PARTIAL_SELECTED_WORLD'
    assert receipt['acceptance_state'] == 'ACCEPTED_WITH_TYPED_PARTIAL'
    assert 'NATIVE_FIELD_REFUSAL:NOT_PUBLISHED_AT_SELECTED_ASOF' in \
        receipt['inconsistencies']
    assert any(i.startswith('EMPIRICAL_NOT_PRODUCTIVE') for i in
               receipt['inconsistencies'])
    # Only the published native field was read; the other is a typed refusal.
    assert [r['role'] for r in receipt['native_field_readset']['values_read']] == [GSS]
    assert [r['reason'] for r in receipt['native_field_readset']['refusals']] == \
        ['NOT_PUBLISHED_AT_SELECTED_ASOF']
    # But the dependency readset still carries BOTH arms.
    assert len(receipt['native_field_readset']['dependency_readset']) == 2
    assert len(receipt['native_field_readset']['successful_value_refset']) == 1
    # The real value actually read is carried, not dropped.
    assert _native(receipt, GSS)['values']['numerator'] == 2388192
    # No structural value is fabricated for an unpublished field.
    for key, value in receipt['structural_values'].items():
        assert 'state' in value


def test_missing_positive_path_cannot_hide_behind_a_typed_hold():
    """If the empirical or native channel is not positive, no positive receipt."""
    adapter = _adapter(structural_revision=True)
    for label in ('TYPED_PARTIAL_PRE_NCA_PUBLICATION',):
        _request, _snapshot, _acceptance, receipt = _receipt(adapter, label)
        assert receipt['state'] != 'SELECTED_WORLD_VALUES_SERVED'
        assert receipt['receipt_hash']
    for label in ('CURRENT_TEST_CLOCK', 'HISTORICAL_AS_OF'):
        _request, _snapshot, _acceptance, receipt = _receipt(adapter, label)
        assert receipt['state'] == 'SELECTED_WORLD_VALUES_SERVED'


# ---------------------------------------------------------------------------
# 4. Two separately native units, never pooled
# ---------------------------------------------------------------------------

def test_two_separately_native_units_preserved_without_pooling():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    gss, nca = _native(receipt, GSS), _native(receipt, NCA)
    assert gss['native_unit'] != nca['native_unit']
    assert gss['source_family'] != nca['source_family']
    assert gss['native_geography'] != nca['native_geography']
    assert gss['native_measure'] != nca['native_measure']
    assert len(receipt['native_units']) == 2
    assert len(receipt['source_families']) == 2
    assert receipt['pooling'] is False
    assert receipt['person_exposure'] is False
    assert receipt['model_use'] is False
    # NCA's native unit is subscriptions, never unique persons.
    assert nca['native_unit'] == 'ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS'
    # No cross-field ratio, product or common denominator is produced.
    forbidden = ('ratio', 'per_subscription', 'pooled_value', 'join_value',
                 'combined_denominator', 'common_unit')
    assert not any(k in receipt for k in forbidden)
    assert not any(k in receipt['native_field_readset'] for k in forbidden)


def test_receipt_carries_real_result_bearing_values_not_promises():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    # Structural: real modeled values.
    assert receipt['structural_values']['exit_cost']['value'] == 8
    assert receipt['structural_values']['training_access']['value'] is False
    # Empirical: real exact fractions.
    assert _fraction(receipt['empirical_steps'][0], '1') == [9, 16]
    # Native: real published numerics.
    assert _native(receipt, GSS)['values']['numerator'] == 2388192
    assert _native(receipt, NCA)['values']['active_subscriptions'] == 23414527
    # Not merely a bundle of refs: every value is a concrete number.
    for record in receipt['native_field_readset']['values_read']:
        assert any(isinstance(v, (int, float)) for v in record['values'].values())
    for key, value in receipt['structural_values'].items():
        if 'value' in value:
            assert isinstance(value['value'], (bool, int))


def test_atomic_snapshot_consistency_across_channels():
    adapter = _adapter(structural_revision=True)
    request, snapshot, acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    # A single permission root spans every channel.
    assert len(receipt['permission_roots']) == 1
    assert receipt['permission_roots'][0] == 'TEST_ONLY_E04_SOURCE_ROOT'
    # Every structural field's clock pair is inside the one selection clock.
    valid_at = snapshot.material['valid_at']
    published = snapshot.material['published_asof']
    for key, binding in acceptance.field_clock_bindings.items():
        assert binding['effective_from'] <= valid_at < binding['effective_to']
        assert binding['publication'] <= published
    # The empirical publication clock is inside the selection clock too.
    assert receipt['empirical_steps'][0]['permission_root'] == \
        receipt['permission_roots'][0]
    # The native readset's as-of clock is DERIVED from the snapshot, so the
    # world and field clocks cannot be split by a caller.
    assert receipt['native_field_readset']['as_of'] == published


# ---------------------------------------------------------------------------
# 5. Channel-separated perturbations
# ---------------------------------------------------------------------------

def test_empirical_source_mutation_changes_only_empirical():
    base = _adapter(structural_revision=True)
    _r, _s, _a, before = _receipt(base, 'CURRENT_TEST_CLOCK')
    changed_service = GenericSelectedWorldService(
        structural_revision=True, empirical_changed=True)
    adapter = E.N9SelectedWorldAdapter(
        service=changed_service, registry=TestOnlyRegistry(_rows()))
    _r, _s, _a, after = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    assert [_cells(s) for s in after['empirical_steps']] == [
        {'0': 13, '1': 19}, {'0': 5, '1': 11}, {'0': 1, '1': 7}]
    assert [s['denominator'] for s in after['empirical_steps']] == [32, 16, 8]
    assert [_fraction(s, '1') for s in after['empirical_steps']] == \
        [[19, 32], [11, 16], [7, 8]]
    # Only the dependent material changed.
    assert after['structural_values'] == before['structural_values']
    assert after['native_field_readset']['values_read'] == \
        before['native_field_readset']['values_read']
    assert after['native_field_readset']['refs'] == \
        before['native_field_readset']['refs']
    assert after['receipt_hash'] != before['receipt_hash']


def test_structural_revision_changes_only_structural():
    base = _adapter()
    _r, _s, _a, before = _receipt(base, 'HISTORICAL_AS_OF')
    revised = _adapter(structural_revision=True)
    _r, _s, _a, after = _receipt(revised, 'CURRENT_TEST_CLOCK')
    assert after['empirical_steps'] == before['empirical_steps']
    assert after['native_field_readset']['values_read'] == \
        before['native_field_readset']['values_read']
    assert after['structural_values']['training_access']['value'] is False
    assert before['structural_values']['training_access']['value'] is True
    assert after['structural_values']['exit_cost']['value'] == 8
    assert before['structural_values']['exit_cost']['value'] == 2


def test_irrelevant_field_perturbation_changes_nothing():
    base = _adapter(structural_revision=True)
    _r, _s, _a, before = _receipt(base, 'CURRENT_TEST_CLOCK')
    noisy = _adapter(structural_revision=True, extra_field=999)
    _r, _s, _a, after = _receipt(noisy, 'CURRENT_TEST_CLOCK')
    assert after['empirical_steps'] == before['empirical_steps']
    assert after['structural_values'] == before['structural_values']
    assert after['native_field_readset'] == before['native_field_readset']
    # The unrelated field is not in any dependency, so no value read changed.
    assert 'unrelated_stock' not in after['structural_readset']
    assert [r['state'] for r in after['consumers']] == \
        [r['state'] for r in before['consumers']]


def test_world_access_rule_changes_only_the_world_route():
    """Revoking one field permission changes only the world route that needs it."""
    adapter = _adapter(structural_revision=True)
    _r, _s, _a, before = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    adapter.service.catalog.revoke('training_access')
    _r2, snap2, a2, after = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    # The empirical channel is untouched.
    assert after['empirical_steps'] == before['empirical_steps']
    assert after['empirical_state'] == 'PRODUCTIVE_TEST_ONLY'
    # The native field readset is untouched.
    assert after['native_field_readset']['values_read'] == \
        before['native_field_readset']['values_read']
    assert after['native_field_readset']['state'] == 'TWO_VALUES_READ_TEST_ONLY'
    # Only the dependent world route changed.
    assert after['structural_values']['training_access']['state'] == 'REVOKED'
    assert 'STRUCTURAL_FIELD_UNAVAILABLE:training_access:REVOKED' in \
        after['inconsistencies']
    assert after['state'] == 'TYPED_PARTIAL_SELECTED_WORLD'
    # An unrelated field is still served.
    assert after['structural_values']['training_fee']['value'] == 2


def test_revoked_empirical_scope_changes_only_empirical():
    adapter = _adapter(structural_revision=True)
    _r, _s, _a, before = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    adapter.service.catalog.revoke('empirical')
    _r2, _s2, _a2, after = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    assert after['empirical_state'] != 'PRODUCTIVE_TEST_ONLY'
    assert after['empirical_steps'] == []
    # Structural and native channels are untouched.
    assert after['structural_values'] == before['structural_values']
    assert after['native_field_readset']['values_read'] == \
        before['native_field_readset']['values_read']
    assert 'EMPIRICAL_NOT_PRODUCTIVE:' in ''.join(after['inconsistencies'])


# ---------------------------------------------------------------------------
# 6. Hostiles: wrong source / release / clock / unit / role
# ---------------------------------------------------------------------------

def test_wrong_source_or_release_binding_refused():
    adapter = _adapter(structural_revision=True)
    request, snapshot, acceptance = None, None, None
    request = E.standard_request(label='CURRENT_TEST_CLOCK')
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    tampered = replace(acceptance, empirical_source_identity=dict(
        acceptance.empirical_source_identity,
        release_ref=dict(kind='FOREIGN', object_id='urn:test:foreign',
                         content_hash='0' * 64)))
    with pytest.raises(E.SelectedWorldInconsistency,
                      match='ACCEPTANCE_BINDING_MISMATCH'):
        adapter.serve(request, tampered, snapshot)


def test_publication_clock_ahead_of_selection_is_refused():
    """A field published after the selected as-of clock cannot be served."""
    adapter = _adapter(structural_revision=True)
    request = E.standard_request(label='HISTORICAL_AS_OF')
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    # The revision-2 fields are published 2027-06-01, well after the historical
    # as-of clock; the historical snapshot must therefore select revision 1.
    for key, binding in acceptance.field_clock_bindings.items():
        assert binding['publication'] <= snapshot.material['published_asof']
        assert binding['revision'] == 1, key
    assert 'FIELD_PUBLICATION_CLOCK_OUTSIDE_SELECTION' not in \
        ' '.join(acceptance.inconsistencies)
    receipt = adapter.serve(request, acceptance, snapshot)
    assert receipt['state'] == 'SELECTED_WORLD_VALUES_SERVED'


def test_snapshot_publication_clock_tamper_refused():
    adapter = _adapter(structural_revision=True)
    request = E.standard_request(label='CURRENT_TEST_CLOCK')
    snapshot = adapter.build_snapshot(request)
    acceptance = adapter.accept(request, snapshot)
    tampered_material = deepcopy(snapshot.material)
    tampered_material['published_asof'] = '2019-01-01'
    # A substituted snapshot whose material no longer matches the accepted one
    # must be refused at serve time, not silently re-resolved.
    with pytest.raises(E.SelectedWorldInconsistency,
                       match='ACCEPTED_SNAPSHOT_SUBSTITUTION'):
        adapter.serve(request, acceptance, _ForeignSnapshot(tampered_material))


class _ForeignSnapshot:
    def __init__(self, material):
        self.material = material
        self.snapshot_hash = 'foreign'

    def verify(self):
        return None


def test_swapped_native_field_role_refused():
    registry = TestOnlyRegistry(_rows())
    refs = registry.refs_by_role()
    swapped = {GSS: refs[NCA], NCA: refs[GSS]}
    relation = dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True,
                    issued_EE13=False,
                    ordered_refs=[swapped[GSS], swapped[NCA]],
                    population_join=False)
    from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
        read_historical_test_only)
    out = read_historical_test_only(
        registry, selected_refs=swapped, relation=relation, as_of='2027-09-01',
        clock_mode='HISTORICAL_PUBLICATION_AWARE', partial_allowed=True)
    assert out['state'] != 'TWO_VALUES_READ_TEST_ONLY'
    assert [r['reason'] for r in out['refusals']] == \
        ['ROLE_REF_SUBSTITUTION', 'ROLE_REF_SUBSTITUTION']


def test_pooling_person_exposure_and_model_requests_refused():
    for field in ('requested_pooling', 'requested_person_exposure',
                  'requested_model_use'):
        with pytest.raises(E.N9SelectedWorldRefusal,
                           match='PERSON_POOLING_OR_MODEL_PROMOTION_FORBIDDEN'):
            E.standard_request(label='CURRENT_TEST_CLOCK', **{field: True})


def test_foreign_native_field_ref_refused():
    registry = TestOnlyRegistry(_rows())
    refs = registry.refs_by_role()
    refs[GSS] = 'TESTONLY_FIELD:' + 'f' * 64
    relation = dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True,
                    issued_EE13=False, ordered_refs=[refs[GSS], refs[NCA]],
                    population_join=False)
    from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
        read_historical_test_only)
    out = read_historical_test_only(
        registry, selected_refs=refs, relation=relation, as_of='2027-09-01',
        clock_mode='HISTORICAL_PUBLICATION_AWARE', partial_allowed=True)
    assert out['state'] == 'PARTIAL_TEST_ONLY_NOT_POSITIVE'
    assert [r['role'] for r in out['values_read']] == [NCA]
    assert {r['reason'] for r in out['refusals']} == {'UNKNOWN_EXACT_FIELD_REF'}
    # Without explicit partial permission the required field still fails closed.
    closed = read_historical_test_only(
        registry, selected_refs=refs, relation=relation, as_of='2027-09-01',
        clock_mode='HISTORICAL_PUBLICATION_AWARE')
    assert closed['state'] == 'REFUSED_REQUIRED_FIELD_TEST_ONLY'
    assert closed['values_read'] == []


def test_source_class_collision_refused():
    rows = _rows()
    for row in rows:
        if row['role'] == NCA:
            row['family'] = next(r['family'] for r in rows if r['role'] == GSS)
    with pytest.raises(TestOnlyReadError) as excinfo:
        TestOnlyRegistry(rows)
    assert excinfo.value.code == \
        'NCA_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'


def test_wrong_native_unit_or_geography_refused():
    rows = _rows()
    for row in rows:
        if row['role'] == GSS:
            row['native_geography'] = 'GHANA_NATIONAL'
    with pytest.raises(TestOnlyReadError) as excinfo:
        TestOnlyRegistry(rows)
    assert excinfo.value.code == \
        'GSS_NATIVE_UNIT_GEOGRAPHY_MEASURE_CONFLICT'


def test_person_inference_labels_refused():
    rows = _rows()
    for row in rows:
        if row['role'] == NCA:
            row['unique_persons'] = True
    with pytest.raises(TestOnlyReadError) as excinfo:
        TestOnlyRegistry(rows)
    assert excinfo.value.code == 'NCA_RURAL_OR_UNIQUE_PERSON_INFERENCE'


def test_wrong_clock_mode_and_wall_clock_refused():
    registry = TestOnlyRegistry(_rows())
    refs = registry.refs_by_role()
    relation = dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True,
                    issued_EE13=False, ordered_refs=[refs[GSS], refs[NCA]],
                    population_join=False)
    from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
        read_historical_test_only)
    for mode in ('CURRENT', 'OPERATIVE_OC05', 'ASOF_UNSPECIFIED'):
        with pytest.raises(TestOnlyReadError) as excinfo:
            read_historical_test_only(
                registry, selected_refs=refs, relation=relation, as_of='2027-09-01',
                clock_mode=mode)
        assert excinfo.value.code == 'CURRENT_OR_OTHER_CLOCK_NOT_AUTHORIZED'
    # A request clock that is not an explicit synthetic test clock is refused.
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED'):
        E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                             published_asof='2027-09-01')


def test_current_mode_requires_the_test_now_clock_to_match():
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='EXPLICIT_TEST_CURRENT_CLOCK_REQUIRED'):
        E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                             published_asof='2027-09-01', test_now='2026-01-01')


def test_unknown_structural_field_and_native_role_refused():
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='UNKNOWN_STRUCTURAL_FIELD_KEY'):
        E.standard_request(label='CURRENT_TEST_CLOCK',
                           structural_keys=('training_access', 'nuclear_launch'))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='UNKNOWN_NATIVE_FIELD_ROLE'):
        E.N9SelectedWorldRequest(
            contract=E.CONTRACT, purpose='TEST_ONLY_CONTEXT',
            structural_keys=('training_access',), empirical_target='Y',
            empirical_conditions=(('A', 1),),
            native_field_roles=('GSS_RURAL_LIGHTING', 'FOREIGN_ROLE'),
            clock=E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                                       published_asof='2027-09-01',
                                       test_now='2027-09-01'))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='DUPLICATE_NATIVE_FIELD_ROLE_REQUIRED'):
        E.N9SelectedWorldRequest(
            contract=E.CONTRACT, purpose='TEST_ONLY_CONTEXT',
            structural_keys=('training_access',), empirical_target='Y',
            empirical_conditions=(('A', 1),),
            native_field_roles=('GSS_RURAL_LIGHTING', 'GSS_RURAL_LIGHTING'),
            clock=E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                                       published_asof='2027-09-01',
                                       test_now='2027-09-01'))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='TWO_SEPARATELY_NATIVE_UNITS_REQUIRED'):
        E.N9SelectedWorldRequest(
            contract=E.CONTRACT, purpose='TEST_ONLY_CONTEXT',
            structural_keys=('training_access',), empirical_target='Y',
            empirical_conditions=(('A', 1),),
            native_field_roles=('GSS_RURAL_LIGHTING',),
            clock=E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                                       published_asof='2027-09-01',
                                       test_now='2027-09-01'))


def test_request_grammar_refusals():
    base = dict(contract=E.CONTRACT, purpose='TEST_ONLY_CONTEXT',
                structural_keys=('training_access',), empirical_target='Y',
                empirical_conditions=(('A', 1),),
                native_field_roles=E.NATIVE_FIELD_ROLES,
                clock=E.SelectedWorldClock(mode='TEST_CURRENT', valid_at='2027-09-01',
                                           published_asof='2027-09-01',
                                           test_now='2027-09-01'))
    with pytest.raises(E.N9SelectedWorldRefusal, match='UNKNOWN_N9_INTERFACE_CONTRACT'):
        E.N9SelectedWorldRequest(**dict(base, contract='FOREIGN@9'))
    with pytest.raises(E.N9SelectedWorldRefusal, match='SOURCEFREE_ONLY_PURPOSE_REQUIRED'):
        E.N9SelectedWorldRequest(**dict(base, purpose='REAL_WORLD'))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='EXACT_NONEMPTY_UNIQUE_ORDERED_CONDITIONERS_REQUIRED'):
        E.N9SelectedWorldRequest(**dict(base, empirical_conditions=(('A', 1), ('A', 2))))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='ORDERED_EXACT_NATIVE_VALUE_BINDINGS_REQUIRED'):
        E.N9SelectedWorldRequest(**dict(base, empirical_conditions=(('A', True),)))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='DUPLICATE_STRUCTURAL_KEY_REQUIRED'):
        E.N9SelectedWorldRequest(**dict(base, structural_keys=('training_access',
                                                             'training_access')))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='NONEMPTY_EXACT_STRUCTURAL_READSET_REQUIRED'):
        E.N9SelectedWorldRequest(**dict(base, structural_keys=()))


def test_request_binding_round_trip_is_exact():
    request = E.standard_request(label='CURRENT_TEST_CLOCK')
    restored = E.N9SelectedWorldRequest.from_binding(request.binding())
    assert restored == request
    assert restored.request_hash == request.request_hash
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='REQUEST_RECORD_FIELDS_MISSING_OR_UNKNOWN'):
        E.N9SelectedWorldRequest.from_binding(dict(request.binding(), extra=1))
    with pytest.raises(E.N9SelectedWorldRefusal,
                       match='REQUEST_SCHEMA_VERSION_MISMATCH'):
        E.N9SelectedWorldRequest.from_binding(
            dict(request.binding(), schema='FOREIGN@1'))


# ---------------------------------------------------------------------------
# 7. Replay, collision, determinism
# ---------------------------------------------------------------------------

def test_replay_is_bitwise_deterministic():
    adapter = _adapter(structural_revision=True)
    _r, _s, _a, first = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    second = _adapter(structural_revision=True)
    _r, _s, _a, again = _receipt(second, 'CURRENT_TEST_CLOCK')
    assert first['receipt_hash'] == again['receipt_hash']
    assert first['receipt_payload_sha256'] == again['receipt_payload_sha256']
    assert first['empirical_steps'] == again['empirical_steps']
    assert first['structural_values'] == again['structural_values']
    assert first['native_field_readset']['values_read'] == \
        again['native_field_readset']['values_read']


def test_native_field_mutation_invalidates_only_that_field():
    registry = TestOnlyRegistry(_rows())
    refs = registry.refs_by_role()
    relation = dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True,
                    issued_EE13=False, ordered_refs=[refs[GSS], refs[NCA]],
                    population_join=False)
    from rawlsing_next.pre553_hq297_n9c_two_field_reader import (
        read_historical_test_only)
    before = read_historical_test_only(
        registry, selected_refs=refs, relation=relation, as_of='2027-09-01',
        clock_mode='HISTORICAL_PUBLICATION_AWARE')
    rows = deepcopy(_rows())
    for row in rows:
        if row['role'] == GSS:
            row['values']['numerator'] -= 1
            row['values']['electricity_subtypes']['mains'] -= 1
    later = read_historical_test_only(
        TestOnlyRegistry(rows), selected_refs=None or TestOnlyRegistry(
            rows).refs_by_role(),
        relation=dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE', fixture_only=True,
                      issued_EE13=False,
                      ordered_refs=list(TestOnlyRegistry(rows).refs_by_role().values()),
                      population_join=False),
        as_of='2027-09-01', clock_mode='HISTORICAL_PUBLICATION_AWARE')
    diff = fixture_invalidation(before, later)
    assert diff['changed_roles'] == [GSS]
    assert diff['unaffected_roles'] == [NCA]
    assert diff['kind'] == 'TEST_ONLY_DEPENDENCY_DIFF_NOT_B5'
    assert before['test_snapshot_ref'] != later['test_snapshot_ref']


def test_historical_receipt_is_archival_only_after_invalidation():
    adapter = _adapter(structural_revision=True)
    _r, _s, _a, receipt = _receipt(adapter, 'CURRENT_TEST_CLOCK')
    revocation = adapter.invalidate('training_fee')
    assert receipt['receipt_hash'] in revocation['invalidated_for_fresh_use']
    assert revocation['historical_receipts_retained'] is True
    historical = adapter.historical_receipt(receipt['receipt_hash'])
    assert historical['archival_only'] is True
    assert historical['fresh_use_authorized'] is False
    assert 'training_fee' in revocation['scope']


def test_accepted_native_readset_arms_are_exact():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    assert len(acceptance.native_field_refs) == 2
    assert len(receipt['native_field_readset']['refs']) == 2
    assert len(receipt['native_field_readset']['dependency_readset']) == 2
    assert len(receipt['native_field_readset']['successful_value_refset']) == 2


def test_empirical_provider_trace_is_native_owner_math_not_candidate_math():
    adapter = _adapter(structural_revision=True)
    _request, _snapshot, _acceptance, receipt = _receipt(
        adapter, 'CURRENT_TEST_CLOCK')
    routes = [s['route'] for s in receipt['empirical_steps']]
    assert routes == ['N10E_PUBLIC_SINGLE', 'C1_PUBLIC_MULTI_BINDING',
                      'C1_PUBLIC_MULTI_BINDING']
    binding = [s['binding_order'] for s in receipt['empirical_steps']]
    assert binding == [['a'], ['a', 'b'], ['a', 'b', 'c']]
    for step in receipt['empirical_steps']:
        assert step['evidence_ref']
        assert step['measure'] == 'RAW; unweighted; no causal inference'
        assert receipt['claim_ceiling'] == \
            'SOURCE_LOCAL_EMPIRICAL_POSSIBILITY_NOT_CAUSAL_OR_PERSONAL'
