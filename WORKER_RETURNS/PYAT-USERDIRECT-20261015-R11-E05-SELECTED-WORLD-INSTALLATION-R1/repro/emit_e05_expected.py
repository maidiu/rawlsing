#!/usr/bin/env python3
"""Precommit the independently authored R11 E05 positive expected values.

Authored BEFORE any adapter or owner execution and committed to freezes/.
Every number below is independently spelled, never read back from an owner
result, so a candidate cannot hide a missing positive path behind a HOLD.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

RETURN = Path(__file__).resolve().parent.parent

CONTRACT = 'R11_E05_N9_SELECTED_WORLD_INTERFACE@1'

EMPIRICAL_STEPS = [
    dict(target='Y', conditioners=[['A', 1]],
         denominator=32, numerator={'1': 18, '0': 14}, fraction={'1': [9, 16]},
         binding_order=['a'], route='N10E_PUBLIC_SINGLE'),
    dict(target='Y', conditioners=[['A', 1], ['B', 1]],
         denominator=16, numerator={'1': 10, '0': 6}, fraction={'1': [5, 8]},
         binding_order=['a', 'b'], route='C1_PUBLIC_MULTI_BINDING'),
    dict(target='Y', conditioners=[['A', 1], ['B', 1], ['C', 1]],
         denominator=8, numerator={'1': 6, '0': 2}, fraction={'1': [3, 4]},
         binding_order=['a', 'b', 'c'], route='C1_PUBLIC_MULTI_BINDING'),
]

# The empirical source intervention: one A=B=C=1, Y=0 row is flipped to Y=1.
EMPIRICAL_INTERVENED = [
    dict(target='Y', denominator=32, numerator={'1': 19, '0': 13}, fraction={'1': [19, 32]}),
    dict(target='Y', denominator=16, numerator={'1': 11, '0': 5}, fraction={'1': [11, 16]}),
    dict(target='Y', denominator=8, numerator={'1': 7, '0': 1}, fraction={'1': [7, 8]}),
]

GSS = dict(
    role='GSS_RURAL_LIGHTING', source_family='GH_GSS_PHC_2021',
    native_unit='RURAL_OCCUPIED_HOUSEHOLD_MAIN_LIGHTING',
    native_geography='GHANA_RURAL',
    native_measure='ELECTRICITY_MAIN_LIGHTING_ALL_SUBTYPES',
    publication_date='2022-02-24', observation_period='2021 PHC',
    numerator=2388192, denominator=3288063, published_percent=72.6,
    subtypes={'mains': 2288193, 'community_grid': 74490, 'generator': 3640,
              'solar_inverter': 21512, 'wind': 357},
    exclusions=['SECONDARY_HOUSING', 'VACANT_DWELLINGS'],
)
NCA = dict(
    role='NCA_NATIONAL_MOBILE_DATA', source_family='GH_NCA_LICENSEE_REPORTS_2021Q4',
    native_unit='ACTIVE_MOBILE_DATA_SUBSCRIPTIONS_NOT_UNIQUE_PERSONS',
    native_geography='GHANA_NATIONAL',
    native_measure='ACTIVE_MOBILE_DATA_90_DAY_TRAFFIC',
    publication_date='2022-07-08',
    observation_period='2021-Q4 (90-day activity definition)',
    active_subscriptions=23414527, prepaid=23237338, postpaid=177189,
)

STRUCTURAL_UNITS = {
    'training_access': 'modeled policy eligibility boolean',
    'training_fee': 'modeled resource tokens',
    'exit_cost': 'modeled resource tokens',
    'civil_sanction': 'modeled sanction boolean',
    'civil_open': 'modeled route eligibility boolean',
}

SNAPSHOTS = {
    'CURRENT_TEST_CLOCK': dict(
        label='CURRENT_TEST_CLOCK', mode='TEST_CURRENT',
        valid_at='2027-09-01', published_asof='2027-09-01',
        service_options={'structural_revision': True},
        structural_values={'training_access': False, 'training_fee': 2, 'exit_cost': 8,
                           'civil_sanction': False, 'civil_open': True},
        structural_revisions={'training_access': 2, 'training_fee': 1, 'exit_cost': 2,
                              'civil_sanction': 1, 'civil_open': 1},
        routes={'training': 'BLOCKED_BY_MODELED_RULE',
                'civil': 'ELIGIBLE',
                'exit_constraint': 'RESOURCE_CONSTRAINED'},
        feasibility={'institutional': 'INFEASIBLE_MODELED_PREMISE',
                     'civil': 'FEASIBLE_MODELED_PREMISE'},
        empirical_state='PRODUCTIVE_TEST_ONLY',
        field_read_state='TWO_VALUES_READ_TEST_ONLY'),
    'HISTORICAL_AS_OF': dict(
        label='HISTORICAL_AS_OF', mode='AS_OF',
        valid_at='2026-06-01', published_asof='2026-03-01',
        service_options={'structural_revision': True},
        structural_values={'training_access': True, 'training_fee': 2, 'exit_cost': 2,
                           'civil_sanction': False, 'civil_open': True},
        structural_revisions={'training_access': 1, 'training_fee': 1, 'exit_cost': 1,
                              'civil_sanction': 1, 'civil_open': 1},
        routes={'training': 'ELIGIBLE',
                'civil': 'ELIGIBLE',
                'exit_constraint': 'WITHIN_MODELED_BUDGET'},
        feasibility={'institutional': 'FEASIBLE_MODELED_PREMISE',
                     'civil': 'FEASIBLE_MODELED_PREMISE'},
        empirical_state='PRODUCTIVE_TEST_ONLY',
        field_read_state='TWO_VALUES_READ_TEST_ONLY'),
    # A published-as-of clock before the second native field's publication: a
    # typed partial, never a silently hidden positive.
    'TYPED_PARTIAL_PRE_NCA_PUBLICATION': dict(
        label='TYPED_PARTIAL_PRE_NCA_PUBLICATION', mode='AS_OF',
        valid_at='2022-06-01', published_asof='2022-06-01',
        service_options={'structural_revision': True},
        structural_values={},
        structural_revisions={},
        routes={'training': 'UNAVAILABLE_AUTHORITY_OR_CLOCK',
                'civil': 'UNAVAILABLE_AUTHORITY_OR_CLOCK',
                'exit_constraint': 'UNAVAILABLE_AUTHORITY_OR_CLOCK'},
        feasibility={'institutional': 'UNKNOWN_PREMISE', 'civil': 'UNKNOWN_PREMISE'},
        empirical_state='UNAVAILABLE_PUBLICATION_OR_EFFECTIVE_CLOCK',
        field_read_state='PARTIAL_TEST_ONLY_NOT_POSITIVE',
        field_roles_read=['GSS_RURAL_LIGHTING'],
        field_refusal_reasons=['NOT_PUBLISHED_AT_SELECTED_ASOF']),
}


def main() -> int:
    # Independent internal consistency of the authored expectations.
    assert sum(sum(v['numerator'].values()) for v in EMPIRICAL_STEPS) == 32 + 16 + 8
    assert EMPIRICAL_STEPS[0]['numerator']['1'] == 18 and \
        EMPIRICAL_STEPS[0]['denominator'] == 32
    assert EMPIRICAL_STEPS[0]['fraction']['1'] == [9, 16]
    assert EMPIRICAL_STEPS[1]['fraction']['1'] == [5, 8]
    assert EMPIRICAL_STEPS[2]['fraction']['1'] == [3, 4]
    assert sum(GSS['subtypes'].values()) == GSS['numerator']
    assert GSS['numerator'] <= GSS['denominator']
    assert round(100 * GSS['numerator'] / GSS['denominator'], 1) == GSS['published_percent']
    assert NCA['prepaid'] + NCA['postpaid'] == NCA['active_subscriptions']
    assert GSS['native_unit'] != NCA['native_unit'], 'native units must stay distinct'
    assert GSS['source_family'] != NCA['source_family'], 'source classes must stay distinct'
    assert len(SNAPSHOTS) == 3
    positives = [s for s in SNAPSHOTS.values()
                 if s['empirical_state'] == 'PRODUCTIVE_TEST_ONLY'
                 and s['field_read_state'] == 'TWO_VALUES_READ_TEST_ONLY']
    assert len(positives) == 2, 'exactly one current and one historical positive'
    assert SNAPSHOTS['CURRENT_TEST_CLOCK']['structural_values']['training_access'] is False
    assert SNAPSHOTS['HISTORICAL_AS_OF']['structural_values']['training_access'] is True

    payload = dict(
        contract=CONTRACT, origin='INDEPENDENT_SOURCEFREE_BEFORE_EXECUTION',
        source_kind='TEST_ONLY_SYNTHETIC_NOT_OBSERVED',
        empirical_steps=EMPIRICAL_STEPS,
        empirical_intervention=EMPIRICAL_INTERVENED,
        empirical_source_balance=[4, 4, 4],
        empirical_intervened_source_balance=[6, 6, 6],
        native_fields=dict(gss=GSS, nca=NCA),
        structural_units=STRUCTURAL_UNITS,
        snapshots=SNAPSHOTS,
        holds=dict(operative_N9=False, operative_OC05=False, issued_N5N6=False,
                   issued_EE13=False, new_issuer=False, person_exposure=False,
                   pooling=False, model_use=False),
    )
    body = json.dumps(payload, sort_keys=True, separators=(',', ':'))
    root = hashlib.sha256(body.encode()).hexdigest()
    payload['committed_root'] = root
    target = RETURN / 'freezes' / '01_PRECOMMITTED_SELECTED_WORLD_EXPECTED_VALUES.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
    print(json.dumps(dict(frozen=str(target), committed_root=root,
                          empirical_fractions=[[9, 16], [5, 8], [3, 4]],
                          positive_snapshots=[s['label'] for s in positives],
                          typed_partial_snapshots=[
                              s['label'] for s in SNAPSHOTS.values()
                              if s['field_read_state'] != 'TWO_VALUES_READ_TEST_ONLY'],
                          gss_numerator=GSS['numerator'],
                          nca_subscriptions=NCA['active_subscriptions'],
                          sha256=hashlib.sha256(
                              target.read_bytes()).hexdigest()), indent=2))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
