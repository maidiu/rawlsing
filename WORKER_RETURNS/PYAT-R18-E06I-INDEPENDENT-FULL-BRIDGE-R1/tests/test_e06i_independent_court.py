"""E06I — independent hostile court over the exact E06 candidate bridge.

This module is authored by the independent reviewer.  It does NOT reuse the
author's assertions: expectations come from
01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json (numerical) and from the permission /
clock / cold hypotheses stated there, all frozen before execution.

The exact candidate is imported read-only from E06_CANDIDATE_ROOT (its own
staged `runtime/` closure).  Nothing here writes into the candidate.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from copy import deepcopy
from dataclasses import replace as dc_replace

import pytest

_RET_HINT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(_RET_HINT, 'repro'))

from support import *  # noqa: F401,F403  (candidate's own readers/constructors)
from support import (bridge, request, rows, grants, hydrate, clone, AuthorityRegistry,
                     GSS, NCA, TestOnlyRegistry, E, NativeBridge)
import e04t_empirical as T  # noqa: E402

from rawlsing_next.pre553_empirical_authority import Pre553AuthorityError
from rawlsing_next.pre553_empirical_objects import ExactRef, semantic_hash
from rawlsing_next import pre553_n9_n10w_progressive_candidate as e03

RET = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ORACLE = json.loads(open(os.path.join(RET, '01_PRECOMMITTED_JOINED_NATIVE_ORACLE.json')).read())
EXP = ORACLE['numerical_expectations']
CAND = os.environ.get('E06_CANDIDATE_ROOT')
if not CAND:
    raise RuntimeError('E06_CANDIDATE_ROOT must point at the candidate return directory')
CAND = os.path.abspath(CAND)
ALL_GRANTS_ORDER = None  # filled per world


# --------------------------------------------------------------------------- #
# independent readers (not the author's `support()` helper)
# --------------------------------------------------------------------------- #
def pair_of(receipt):
    """(cell-1 support, denominator) per progressive step, from the receipt."""
    out = []
    for s in receipt['empirical_steps']:
        cells = {c['cell']: c['raw_numerator_support'] for c in s['cells']}
        out.append((cells.get('1'), s['denominator']))
    return out


def minority_of(receipt):
    out = []
    for s in receipt['empirical_steps']:
        cells = {c['cell']: c['raw_numerator_support'] for c in s['cells']}
        out.append((cells.get('0'), s['denominator']))
    return out


def no_positive(receipt):
    """True iff no step carries a numerator cell or native evidence ref."""
    if receipt['empirical_state'] == 'PRODUCTIVE_TEST_ONLY':
        return False
    for s in receipt['empirical_steps']:
        if s['cells'] or s.get('evidence_ref'):
            return False
    return True


def attach(world, snapshots):
    world['registry'] = AuthorityRegistry(snapshots)


def source_only(world):
    return AuthorityRegistry(world['source']['authorities'])


def exact_restore(world):
    order = (*world['source']['authorities'], world['qauth'])
    return tuple(hydrate(g.as_dict()) for g in reversed(order))


def derive_from_raw_source():
    def rows_of(changed=False, support_loss=False):
        rs = [dict(r, responses=dict(r['responses'])) for r in e03.synthetic_world_rows()]
        if changed:
            next(r for r in rs if all(r['responses'][q] == 1 for q in 'ABC')
                 and r['responses']['Y'] == 0)['responses']['Y'] = 1
        if support_loss:
            rs = [r for r in rs if not all(r['responses'][q] == 1 for q in 'ABC')]
        return rs

    def table(rs, target, conds):
        sel = [r for r in rs if all(r['responses'][q] == v for q, v in conds)]
        return (sum(1 for r in sel if r['responses'][target] == 1), len(sel))

    base, changed, loss = rows_of(), rows_of(changed=True), rows_of(support_loss=True)
    depth = [(('A', 1),), (('A', 1), ('B', 1)), (('A', 1), ('B', 1), ('C', 1))]
    return dict(
        forward=[list(table(base, 'Y', c)) for c in depth],
        minority=[[table(base, 'Y', c)[1] - table(base, 'Y', c)[0], table(base, 'Y', c)[1]] for c in depth],
        reverse=list(table(base, 'A', (('Y', 1),))),
        y01=[list(table(changed, 'Y', c)) for c in depth],
        zero_early=[list(table(loss, 'Y', c)) for c in depth[:2]],
        zero_terminal=table(loss, 'Y', depth[2]),
        respondents=len(base), events=4 * len(base),
    )


# =========================================================================== #
# A — positive joined path and independent numerical oracle
# =========================================================================== #
def test_A01_positive_joined_two_original_consumers():
    b = bridge()
    p = b.prepare(request())
    out = b.read(p)
    r = out['selected_world_receipt']
    assert out['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert r['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert r['empirical_state'] == 'PRODUCTIVE_TEST_ONLY'
    assert [c['consumer'] for c in r['consumers']] == ['NONPARENT_OPTIONS', 'CONCEPTION_SCENARIO_PROPOSALS']
    assert [c['state'] for c in r['consumers']] == ['OPTIONS_AND_SOURCE_SUPPORT_PRODUCED',
                                                    'FINITE_PROPOSALS_EVALUATED']
    ss = r['snapshot_hash']
    for c in r['consumers']:
        m = c['consumer_material']
        assert m['snapshot_ref'] == ss
        assert m['empirical']['steps'] == r['empirical_steps']
        assert all(v['snapshot_ref'] == ss for v in m['values_read'])
    assert out['successful_consumers'] == r['consumers']
    assert r['native_field_readset']['state'] == 'TWO_VALUES_READ_TEST_ONLY'


def test_A02_independent_numerical_oracle_from_raw_source():
    d = derive_from_raw_source()
    assert d['respondents'] == 58 and d['events'] == 232
    assert d['forward'] == EXP['forward_Y_given_A_AB_ABC']
    assert d['minority'] == EXP['minority_cell0']
    assert d['reverse'] == EXP['reverse_A_given_Y16']
    assert d['y01'] == EXP['Y0to1_counterfactual']
    assert d['zero_early'] == EXP['zero_support_early']
    assert d['zero_terminal'][1] == EXP['zero_support_terminal_denominator']

    cur = bridge().execute(request())
    assert pair_of(cur['selected_world_receipt']) == [tuple(x) for x in d['forward']]
    assert minority_of(cur['selected_world_receipt']) == [tuple(x) for x in d['minority']]
    rev = bridge().execute(request(target='A', conditions=(('Y', 1),)), scalar_only=True)
    assert pair_of(rev['selected_world_receipt']) == [tuple(d['reverse'])]
    ych = bridge(empirical_changed=True).execute(request())
    assert pair_of(ych['selected_world_receipt']) == [tuple(x) for x in d['y01']]
    zs = bridge(support_loss=True).execute(request())
    assert pair_of(zs['selected_world_receipt'])[:2] == [tuple(x) for x in d['zero_early']]
    assert zs['selected_world_receipt']['empirical_steps'][-1]['state'] == EXP['zero_support_terminal_state']
    assert zs['selected_world_receipt']['empirical_steps'][-1]['denominator'] == 0
    assert zs['selected_world_receipt']['empirical_steps'][-1]['cells'] == []


def test_A03_two_separately_native_field_units_no_pooling():
    r = bridge().execute(request())['selected_world_receipt']
    v = {x['role']: x for x in r['native_field_readset']['values_read']}
    g, n = v[GSS], v[NCA]
    assert (g['values']['numerator'], g['values']['denominator']) == (EXP['gss']['numerator'], EXP['gss']['denominator'])
    assert sum(g['values']['electricity_subtypes'].values()) == EXP['gss']['electricity_subtypes_sum']
    assert n['values']['active_subscriptions'] == EXP['nca']['active_subscriptions']
    assert g['native_unit'] == EXP['gss']['unit'] and g['native_geography'] == EXP['gss']['geography']
    assert n['native_unit'] == EXP['nca']['unit'] and n['native_geography'] == EXP['nca']['geography']
    assert g['native_unit'] != n['native_unit'] and g['native_geography'] != n['native_geography']
    assert g['publication_date'] == EXP['gss']['publication']
    assert n['publication_date'] == EXP['nca']['publication']
    assert r['pooling'] is False and r['person_exposure'] is False and r['model_use'] is False
    assert len({x['source_family'] for x in r['native_field_readset']['values_read']}) == 2


def test_A04_current_vs_historical_clock_split():
    cur = bridge().execute(request('CURRENT_TEST_CLOCK'))['selected_world_receipt']
    hist = bridge().execute(request('HISTORICAL_AS_OF'))['selected_world_receipt']
    for key, want in EXP['current_struct'].items():
        assert cur['structural_values'][key]['value'] is want
    for key, want in EXP['historical_struct'].items():
        assert hist['structural_values'][key]['value'] is want
    assert cur['empirical_steps'] == hist['empirical_steps']
    assert cur['native_field_readset']['values_read'] == hist['native_field_readset']['values_read']
    assert cur['consumers'][0]['consumer_material']['structural_routes']['training']['state'] == 'BLOCKED_BY_MODELED_RULE'
    assert hist['consumers'][0]['consumer_material']['structural_routes']['training']['state'] == 'ELIGIBLE'


def test_A05_Y_intervention_changes_clients_not_structural():
    a = bridge().execute(request())['selected_world_receipt']
    b = bridge(empirical_changed=True).execute(request())['selected_world_receipt']
    assert pair_of(b) == [tuple(x) for x in EXP['Y0to1_counterfactual']]
    assert a['structural_values'] == b['structural_values']
    assert a['native_field_readset'] == b['native_field_readset']
    assert a['empirical_steps'][0]['release_ref'] != b['empirical_steps'][0]['release_ref']
    for x, y in zip(a['consumers'], b['consumers']):
        assert x['consumer_material']['empirical']['steps'] != y['consumer_material']['empirical']['steps']


# =========================================================================== #
# B — source-current grant withdrawal / restoration / reissue
# =========================================================================== #
def _warm_withdrawn():
    b = bridge()
    p = b.prepare(request())
    before = b.read(p)
    attach(b.provider.world, [*b.provider.world['source']['authorities']])
    return b, p, before


def test_B01_warm_query_grant_withdrawal_refuses_without_values():
    b, p, before = _warm_withdrawn()
    d = b.read(p)
    assert d['state'] == 'DEPENDENT_EMPIRICAL_USE_REFUSED'
    assert d['fresh_empirical_use_authorized'] is False
    assert d['empirical_values'] is None
    assert len(d['actual_warm_client_denials']) == 2
    assert all(x['fresh_receipt'] is False for x in d['actual_warm_client_denials'])
    part = d['selected_world_receipt']
    assert part['state'] == 'TYPED_PARTIAL_SELECTED_WORLD'
    assert no_positive(part)
    assert all('PARTIAL' in c['state'] for c in part['consumers'])
    assert part['structural_values'] == before['selected_world_receipt']['structural_values']
    assert part['native_field_readset'] == before['selected_world_receipt']['native_field_readset']
    assert d['unrelated_structural_product']['material']['state'] == 'VALUES_READ'


def test_B02_repeat_withdrawn_read_still_no_values():
    b, p, before = _warm_withdrawn()
    b.read(p)
    d2 = b.read(p)
    assert d2['state'] != 'SELECTED_WORLD_VALUES_SERVED'
    assert no_positive(d2['selected_world_receipt'])
    assert d2.get('fresh_empirical_use_authorized') is not True
    assert all('PRODUCTIVE' not in c['state'] for c in d2['selected_world_receipt']['consumers'])
    # the still-positive structural/native channels never gained empirical cells
    assert d2['selected_world_receipt']['structural_values']['training_access']['value'] is False


def test_B03_cold_bridge_with_never_attached_query_grant():
    b = NativeBridge(rows(), enabled=True)
    attach(b.provider.world, [*b.provider.world['source']['authorities']])
    out = b.read(b.prepare(request()), scalar_only=True)
    assert no_positive(out['selected_world_receipt'])
    assert out['state'] != 'SELECTED_WORLD_VALUES_SERVED'


def test_B04_warm_withdrawal_then_cold_cache_key_no_bypass():
    b, p, before = _warm_withdrawn()
    b.read(p)  # exercise the warm refusal first
    fresh = b.prepare(request(target='Y', conditions=(('B', 1),)))
    out = b.read(fresh, scalar_only=True)
    assert no_positive(out['selected_world_receipt'])
    assert out['state'] != 'SELECTED_WORLD_VALUES_SERVED'


def test_B05_exact_restoration_restores_positive_same_acceptance():
    b, p, before = _warm_withdrawn()
    d = b.read(p)
    assert d['state'] == 'DEPENDENT_EMPIRICAL_USE_REFUSED'
    attach(b.provider.world, exact_restore(b.provider.world))
    z = b.read(p)
    assert z['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert z['acceptance'] == before['acceptance']
    assert z['selected_world_receipt'] == before['selected_world_receipt']


def test_B06_refusal_does_not_auto_issue_or_renew_authority():
    b, p, before = _warm_withdrawn()
    w = b.provider.world
    snap_before = [g.as_dict() for g in (*w['source']['authorities'], w['qauth'])]
    reg_before = len(w['registry'])
    d = b.read(p)
    assert d['state'] == 'DEPENDENT_EMPIRICAL_USE_REFUSED'
    assert [g.as_dict() for g in (*w['source']['authorities'], w['qauth'])] == snap_before
    assert len(w['registry']) == reg_before
    assert d['fresh_empirical_use_authorized'] is False


def test_B07_archive_is_archival_not_a_grant():
    b, p, before = _warm_withdrawn()
    arch_a = b.archive(before)
    b.read(p)
    arch_b = b.archive(before)
    assert arch_a == arch_b
    assert arch_a['archival_only'] is True and arch_a['fresh_use_authorized'] is False
    q = bridge()
    qp = q.prepare(request())
    q.read(qp)
    assert q.archive(q.read(qp))['fresh_use_authorized'] is False


@pytest.mark.parametrize('delta', [
    dict(authority_version='2.0.0', authority_content_hash='b' * 64),          # successor
    dict(authority_id='FOREIGN-ISSUER', authority_content_hash='c' * 64),      # foreign issuer
    dict(decision_state='DENY'),                                               # same-ref deny
])
def test_B08_forged_query_grant_refuses_warm_and_cold(delta):
    b, p, before = _warm_withdrawn()
    attach(b.provider.world, [*b.provider.world['source']['authorities'],
                              clone(b.provider.world['qauth'], **delta)])
    d = None
    try:
        d = b.read(p)
    except (Pre553AuthorityError, ValueError):
        pass  # same-ref forged content is an integrity error and must propagate
    if d is not None:
        assert d['state'] != 'SELECTED_WORLD_VALUES_SERVED'
        assert no_positive(d['selected_world_receipt'])
    c = NativeBridge(rows(), enabled=True)
    attach(c.provider.world, [*c.provider.world['source']['authorities'],
                              clone(c.provider.world['qauth'], **delta)])
    try:
        cold = c.read(c.prepare(request()), scalar_only=True)
    except (Pre553AuthorityError, ValueError):
        return
    assert no_positive(cold['selected_world_receipt'])


def test_B09_wrong_operation_same_ref_refuses_both_paths():
    b, p, before = _warm_withdrawn()
    attach(b.provider.world, [*b.provider.world['source']['authorities'],
                              clone(b.provider.world['qauth'], governed_operations=['FOREIGN'])])
    try:
        d = b.read(p)
    except (Pre553AuthorityError, ValueError):
        pass  # an integrity/same-ref forgery error must propagate, never yield values
    else:
        assert d['state'] != 'SELECTED_WORLD_VALUES_SERVED'
        assert no_positive(d['selected_world_receipt'])
    c = NativeBridge(rows(), enabled=True)
    attach(c.provider.world, [*c.provider.world['source']['authorities'],
                              clone(c.provider.world['qauth'], governed_operations=['FOREIGN'])])
    try:
        cold = c.read(c.prepare(request()), scalar_only=True)
    except (Pre553AuthorityError, ValueError):
        return
    assert no_positive(cold['selected_world_receipt'])


def test_B10_source_authority_deny_refuses():
    b, p, before = _warm_withdrawn()
    srcs = list(b.provider.world['source']['authorities'])
    attach(b.provider.world, [clone(srcs[0], decision_state='DENY'),
                              *srcs[1:], b.provider.world['qauth']])
    d = b.read(p)
    assert d['state'] != 'SELECTED_WORLD_VALUES_SERVED'
    assert no_positive(d['selected_world_receipt'])


def test_B11_missing_source_authority_refuses():
    b, p, before = _warm_withdrawn()
    full = (*b.provider.world['source']['authorities'], b.provider.world['qauth'])
    attach(b.provider.world, full[1:])
    d = b.read(p)
    assert d['state'] != 'SELECTED_WORLD_VALUES_SERVED'
    assert no_positive(d['selected_world_receipt'])


# =========================================================================== #
# C — cache and issuer identity
# =========================================================================== #
def test_C01_foreign_process_projection_is_unattested():
    donor = bridge()
    dp = donor.prepare(request())
    donor.read(dp)
    key = ('Y', (('A', 1),))
    projection = deepcopy(donor.provider.cache[key])
    fresh = NativeBridge(rows(), enabled=True)
    fresh.provider.cache[key] = projection
    with pytest.raises(ValueError, match='UNATTESTED_NATIVE_CACHE_ENTRY'):
        fresh.prepare(request())


def test_C02_rehashed_cache_tamper_is_integrity_error_not_envelope():
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    cached = b.provider.cache[('Y', (('A', 1),))]
    cached['cells'][1]['raw_numerator_support'] = 999
    content = deepcopy(cached)
    content.pop('content_hash')
    cached['content_hash'] = semantic_hash(content)
    with pytest.raises(ValueError, match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):
        b.read(p)


def test_C03_cross_binding_projection_mismatch():
    donor = bridge(empirical_changed=True)
    dp = donor.prepare(request())
    donor.read(dp)
    foreign = deepcopy(donor.provider.cache[('Y', (('A', 1),))])
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.provider.cache[('Y', (('A', 1),))] = foreign
    with pytest.raises(ValueError, match='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH'):
        b.read(p)


def test_C04_foreign_prepared_handoff_refused():
    a = bridge()
    pa = a.prepare(request())
    a.read(pa)
    b = bridge()
    b.prepare(request())
    with pytest.raises(ValueError, match='E06_FOREIGN_PREPARED_HANDOFF'):
        b.read(pa)


# =========================================================================== #
# D — mixed-source provenance and native fact readsets
# =========================================================================== #
def test_D01_release_ref_substitution_refused():
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.provider.world['source']['release_ref'] = ExactRef('C11_RELEASE', 'urn:foreign', 'f' * 64)
    with pytest.raises(ValueError):
        b.read(p)


def test_D02_same_ref_foreign_release_object_refused():
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.provider.world['source']['repo'] = T.build_source()['source']['repo']
    with pytest.raises(ValueError, match='ACCEPTED_NATIVE_SOURCE_REPLACED'):
        b.read(p)


@pytest.mark.parametrize('mutate', ['risk', 'permission', 'model', 'coordinates'])
def test_D03_risk_permission_model_coordinate_substitution_refused(mutate):
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    w = b.provider.world
    if mutate == 'risk':
        w['source']['risk_refs']['R'] = ExactRef('RISK_SET', 'urn:foreign', 'b' * 64)
    elif mutate == 'permission':
        w['permission_root'] = 'FOREIGN'
    elif mutate == 'model':
        w['model_rule'] = dc_replace(w['model_rule'],
                                     source_universe_refs=(ExactRef('X', 'urn:foreign', 'f' * 64),))
    else:
        w['source']['qrefs']['A'] = ExactRef('COORDINATE', 'urn:foreign', 'a' * 64)
    with pytest.raises(ValueError):
        b.read(p)


def test_D04_supplied_consumer_material_native_contamination_refused():
    b = bridge()
    p = b.prepare(request())
    a = b.read(p)
    supplied = [x['consumer_material'] for x in a['selected_world_receipt']['consumers']]
    supplied[0]['native_field_readset'] = {
        'state': 'TWO_VALUES_READ_TEST_ONLY',
        'values_read': [{'role': NCA, 'values': {'active_subscriptions': 999}}]}
    with pytest.raises(E.N9SelectedWorldRefusal):
        b.read(p, supplied_consumers=supplied)


def test_D04b_supplied_exact_consumer_material_reproves_itself():
    b = bridge()
    p = b.prepare(request())
    a = b.read(p)
    supplied = [x['consumer_material'] for x in a['selected_world_receipt']['consumers']]
    o = b.read(p, supplied_consumers=supplied)
    assert o['selected_world_receipt'] == a['selected_world_receipt']


@pytest.mark.parametrize('role', [GSS, NCA])
def test_D05_selective_native_revocation_is_partial_and_stable(role):
    b = bridge()
    p = b.prepare(request())
    a = b.read(p)['selected_world_receipt']
    rr = rows()
    next(x for x in rr if x['role'] == role)['status'] = 'REVOKED_TEST_ONLY'
    b.adapter.registry = TestOnlyRegistry(rr)
    z = b.read(p)['selected_world_receipt']
    assert z['state'] == 'TYPED_PARTIAL_SELECTED_WORLD'
    assert z['native_field_readset']['values_read'] == [v for v in a['native_field_readset']['values_read'] if v['role'] != role]
    assert any(v['role'] == role for v in z['native_field_readset']['refusals'])
    assert z['native_field_readset']['dependency_readset'] == a['native_field_readset']['dependency_readset']
    for k in ('structural_values', 'empirical_steps', 'consumers'):
        assert a[k] == z[k]


@pytest.mark.parametrize('role', [GSS, NCA])
def test_D06_explicit_withdrawal_is_source_revoked_not_rekey_or_publication(role):
    b = bridge()
    p = b.prepare(request())
    a = b.read(p)['selected_world_receipt']
    inv = b.adapter.invalidate(role)
    z = b.read(p)['selected_world_receipt']
    assert any(v['role'] == role and v['reason'] == 'SOURCE_REVOKED'
               for v in z['native_field_readset']['refusals'])
    assert z['native_field_readset']['values_read'] == [v for v in a['native_field_readset']['values_read'] if v['role'] != role]
    assert a['receipt_hash'] in inv['invalidated_for_fresh_use']
    assert a['empirical_steps'] == z['empirical_steps']
    assert a['structural_values'] == z['structural_values']


# =========================================================================== #
# E — historical publication clocks
# =========================================================================== #
def test_E01_prepublication_denial_is_unavailable_and_does_not_prewarm():
    b = bridge()
    p = b.prepare(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION'))
    out = b.read(p)
    assert b.provider.cache == {} and b.provider._accepted == {} and b.provider.trace == []
    r = out['selected_world_receipt']
    assert r['empirical_steps'] == []
    assert r['empirical_state'] == 'UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'
    assert any(x['reason'] == 'NOT_PUBLISHED_AT_SELECTED_ASOF' for x in r['native_field_readset']['refusals'])


def test_E02_clock_denial_does_not_poison_later_current():
    b = bridge()
    b.read(b.prepare(request('TYPED_PARTIAL_PRE_NCA_PUBLICATION')))
    out = b.read(b.prepare(request('CURRENT_TEST_CLOCK')))
    assert out['state'] == 'SELECTED_WORLD_VALUES_SERVED'
    assert pair_of(out['selected_world_receipt']) == [tuple(x) for x in EXP['forward_Y_given_A_AB_ABC']]


def test_E03_serve_with_foreign_clock_refused():
    b = bridge()
    p = b.prepare(request('CURRENT_TEST_CLOCK'))
    b.read(p)
    q = E.N9SelectedWorldRequest.from_binding(request('HISTORICAL_AS_OF'))
    with pytest.raises(E.N9SelectedWorldRefusal):
        b.adapter.serve(q, p.acceptance, p.snapshot)


def test_E04_publication_clock_before_source_never_prewarms():
    b = bridge()
    clock = E.SelectedWorldClock(mode='AS_OF', valid_at='2026-06-01', published_asof='2022-06-01')
    q = E.N9SelectedWorldRequest(contract=E.CONTRACT, purpose='TEST_ONLY_CONTEXT',
                                 structural_keys=E.STRUCTURAL_KEYS, empirical_target='Y',
                                 empirical_conditions=(('A', 1), ('B', 1), ('C', 1)),
                                 native_field_roles=E.NATIVE_FIELD_ROLES, clock=clock)
    out = b.read(b.prepare(q.binding()))
    assert b.provider.cache == {} and b.provider._accepted == {}
    assert out['selected_world_receipt']['empirical_state'] == 'UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK'


# =========================================================================== #
# F — no estimator / factory downgrade
# =========================================================================== #
def test_F01_e04r_service_factory_downgrade_refused():
    from product.service import GenericSelectedWorldService
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.adapter.service = GenericSelectedWorldService(structural_revision=True)
    with pytest.raises(ValueError, match='E06_PINNED_E04T_PROVIDER_SUBSTITUTED'):
        b.read(p)


def test_F02_provider_substitution_refused():
    import product.empirical as PE
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.service.provider = PE.GenericProgressiveProvider(b.provider.world)
    with pytest.raises(ValueError, match='E06_PINNED_E04T_PROVIDER_SUBSTITUTED'):
        b.read(p)


def test_F03_live_catalog_mutation_refused():
    b = bridge()
    p = b.prepare(request())
    b.read(p)
    b.service.catalog.records.append(dict(key='training_access', unit='x', start='2026-01-01',
                                          end='2028-01-01', publication='2026-03-01',
                                          revision=9, ref=dict(kind='E04_TEST_ONLY_FIELD',
                                                               object_id='urn:foreign', content_hash='f' * 64)))
    with pytest.raises(ValueError):
        b.read(p)


def test_F04_off_by_default_produces_no_native_evidence():
    with pytest.raises(ValueError):
        NativeBridge(rows())
    with pytest.raises(ValueError):
        NativeBridge(rows(), enabled=1)
    with pytest.raises(ValueError):
        NativeBridge(rows(), enabled=False)


# =========================================================================== #
# G — real imports, frozen contract, no installation
# =========================================================================== #
def _git_blob(path):
    b = open(path, 'rb').read()
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()


def test_G01_real_producer_module_and_git_blob():
    import e04t_empirical
    import product.empirical
    assert e04t_empirical.__file__.endswith(os.path.join('runtime', 'owners', 'e04t_empirical.py'))
    assert product.empirical.__file__.endswith(os.path.join('runtime', 'product', 'empirical.py'))
    assert e04t_empirical.__file__ != product.empirical.__file__
    assert e04t_empirical.GenericProgressiveProvider is not product.empirical.GenericProgressiveProvider
    manifest = json.loads(open(os.path.join(CAND, 'source_manifest.json')).read())
    entry = next(x for x in manifest if x['local'].endswith('runtime/owners/e04t_empirical.py'))
    assert entry['commit'] == ORACLE['candidate']['pins']['E04T']
    assert _git_blob(e04t_empirical.__file__) == entry['git_blob']
    assert hashlib.sha256(open(e04t_empirical.__file__, 'rb').read()).hexdigest() == entry['sha256']


def test_G02_no_installation_or_issuance():
    r = bridge().execute(request())['selected_world_receipt']
    for row in r['installed_OC05'].values():
        if 'OC05' in row['policy_id']:
            assert row['consumer_seam'] is None
            assert row['current_applicability'] == 'NOT_YET_APPLICABLE'
    assert r['issued_N5N6'] is False and r['issued_EE13'] is False
    assert r['operative_N9'] is False and r['operative_OC05'] is False
    assert r['new_issuer'] is False


def test_G03_candidate_frozen_contract_is_the_committed_preimage():
    p = os.path.join(CAND, '01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json')
    digest = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    assert digest == ORACLE['candidate']['frozen_contract_sha256']
    freeze_line = open(os.path.join(CAND, '01_FREEZE_SHA256.txt')).read().split()[0]
    assert digest == freeze_line
    commit_bytes = subprocess.check_output(
        ['git', 'show', '14f247b75:WORKER_RETURNS/PYAT-USERDIRECT-20261016-R17-E06-E04E05-NATIVE-BRIDGE-R1/'
         '01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json'], cwd=CAND)
    assert commit_bytes == open(p, 'rb').read()


# =========================================================================== #
# H — cold processes and stale permission
# =========================================================================== #
COLD = os.path.join(RET, 'repro', 'cold_independent.py')


def _cold(ledger, dest):
    subprocess.run([sys.executable, COLD, ledger, dest], cwd=RET, check=True,
                   capture_output=True, text=True,
                   env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
    return json.loads(open(dest).read())


def _make_ledgers():
    b = bridge()
    p = b.prepare(request())
    before = b.read(p)
    w = b.provider.world
    key = ('Y', (('A', 1),))
    projection = deepcopy(b.provider.cache[key])
    ledger_restored = dict(state='restored', grants=[g.as_dict() for g in (*w['source']['authorities'], w['qauth'])],
                           projection=projection)
    ledger_withdrawn = dict(state='withdrawn', grants=[g.as_dict() for g in w['source']['authorities']],
                            projection=projection)
    return before, ledger_restored, ledger_withdrawn


def test_H01_cold_restored_two_processes_bit_identical_and_positive():
    before, restored, _ = _make_ledgers()
    lpath = os.path.join(RET, 'observations', 'e06i_cold_restored_ledger.json')
    open(lpath, 'w').write(json.dumps(restored))
    outs = [_cold(lpath, os.path.join(RET, 'observations', 'e06i_cold_restored_%d.json' % i))
            for i in range(2)]
    assert len({o['pid'] for o in outs}) == 2
    assert json.dumps(outs[0]['result'], sort_keys=True) == json.dumps(outs[1]['result'], sort_keys=True)
    assert outs[0]['ledger_sha256'] == hashlib.sha256(open(lpath, 'rb').read()).hexdigest()
    assert json.loads(json.dumps(before['selected_world_receipt'])) == outs[0]['result']['selected_world_receipt']
    assert pair_of(outs[0]['result']['selected_world_receipt']) == [tuple(x) for x in EXP['forward_Y_given_A_AB_ABC']]
    assert outs[0]['foreign_projection_reason'] == 'UNATTESTED_NATIVE_CACHE_ENTRY'


def test_H02_cold_withdrawn_two_processes_bit_identical_and_stale_permission_refused():
    before, _, withdrawn = _make_ledgers()
    lpath = os.path.join(RET, 'observations', 'e06i_cold_withdrawn_ledger.json')
    open(lpath, 'w').write(json.dumps(withdrawn))
    outs = [_cold(lpath, os.path.join(RET, 'observations', 'e06i_cold_withdrawn_%d.json' % i))
            for i in range(2)]
    assert len({o['pid'] for o in outs}) == 2
    assert json.dumps(outs[0]['result'], sort_keys=True) == json.dumps(outs[1]['result'], sort_keys=True)
    r = outs[0]['result']['selected_world_receipt']
    assert no_positive(r)
    assert any(f['function'] == 'ingest_c11_source_release' and f['count'] for f in outs[0]['frames'])
    assert outs[0]['foreign_projection_reason'] == 'UNATTESTED_NATIVE_CACHE_ENTRY'


# =========================================================================== #
# I — author 40 is regression, not independent acceptance (documented check)
# =========================================================================== #
def test_I01_author_suite_is_present_and_distinct_from_this_court():
    author_bytes = open(os.path.join(CAND, 'tests', 'test_bridge.py'), 'rb').read()
    assert b'def test_frozen_contract_precedes_candidate' in author_bytes
    assert hashlib.sha256(author_bytes).hexdigest() == ORACLE['candidate']['author_tests_sha256']
    assert os.path.abspath(__file__) != os.path.abspath(os.path.join(CAND, 'tests', 'test_bridge.py'))
