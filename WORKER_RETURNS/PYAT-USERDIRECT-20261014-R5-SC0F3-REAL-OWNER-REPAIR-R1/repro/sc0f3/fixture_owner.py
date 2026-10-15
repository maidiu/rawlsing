"""Controlled TEST_ONLY owner layer, separate from provider/query callers.

This is a publicly inspectable closed synthetic fixture, not an authentic
original-source issuer. There is no enrollment, signing or registration API.
Arbitrary code execution modifying this module is outside the caller-data threat
model; file hashes expose such modification to the separate reviewer.
"""
import copy
import json
from pathlib import Path
from .common import Hold, digest, require, material


def fixture_world():
    from port.world_baseline import BASELINE_WORLD
    w = copy.deepcopy(BASELINE_WORLD)
    # New candidate fixture; original frozen world remains byte-for-byte intact.
    # Publication stays 2010; default knowledge cut is now lawful 2011.
    w['time_axes']['as_of'] = '2011'
    oracle = Path(__file__).resolve().parents[1]/'inputs/port/oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json'
    w['negative_states'] = json.loads(oracle.read_text())['baseline']['status_rows']
    return w


def source_catalog():
    # Immutable tuple, rebuilt from owner code, never a caller-writable store.
    return (('fx:source:synthetic', 'fx:release:fixture1', 'fx:scope:town2008',
             'RESPONDENT', ('fx:stratum:A', 'fx:stratum:B')),
            ('fx:source:synthetic', 'fx:release:fixture2', 'fx:scope:town2008',
             'RESPONDENT', ('fx:stratum:A', 'fx:stratum:B')))


def build_native_case(variant='54_6', direction='forward'):
    """Only two predeclared response laws; no submitted authority/repository."""
    require(variant in ('54_6', '50_10'), 'HELD_AUTHORITY', 'Unknown synthetic source law')
    require(direction in ('forward', 'reverse'), 'HELD_AUTHORITY', 'Unknown direction')
    from rawlsing_next.tests import n10e_empirical_slice_fixture as f
    if variant == '54_6':
        return f.build_provider_case(direction)
    rows = f.at07_rows()
    # Move four P1 yes answers to no. Cohort and denominator remain 60.
    for row in rows[:4]:
        row['responses']['ANSWER'] = 'no'
    with f.frozen_at07_source(tag='sc0f3-50-10', rows=rows,
                              scope_query_authority_to_universe=True) as (source, auth, registry):
        predicate, query = f.build_producer(source, auth, direction)
        consumer, binding = f.build_consumer(source, direction)
        return dict(direction=direction, source=source, registry=registry,
                    predicate=predicate, empirical_query=query, consumer_query=consumer,
                    conditioner_binding=binding,
                    condition_binding_witness=f.build_witness(source, direction, consumer, binding, query, predicate),
                    model_rule=f.build_model_rule(source), release_refs=(source['release_ref'],))


def reversal_fixture_permit(variant='54_6'):
    require(variant in ('54_6', '50_10'), 'HELD_AUTHORITY', 'No fixture warrant')
    # Closed pre-issued fixture records. Reading the record does not mint a new
    # source/target/operation. Reverse denominator differs from forward 60.
    case=build_native_case(variant,'reverse')
    return dict(grant_id='TEST_ONLY:reverse:'+variant, issuer='TEST_ONLY:SC0F3_OWNER',
                world_source='fx:source:synthetic', world_release='fx:release:fixture1',
                native_case=variant, target='POSITION', risk='R_ALL_100',
                native_source=material(case['consumer_query'].source_universe_ref),
                native_release=material(case['consumer_query'].release_ref),
                native_target=material(case['consumer_query'].target_ref),
                native_risk=material(case['empirical_query'].risk_set_ref),
                denominator=62 if variant == '54_6' else 58,
                operation='ROLE_REVERSAL_CONDITIONAL_QUERY',
                knowledge_as_of='2011',
                not_before='2026-10-01', expires='2026-11-01', revoked_at='2026-10-25',
                grade='TEST_ONLY')


def check_reversal(presented, world, variant, now):
    expected = reversal_fixture_permit(variant)
    require(type(presented) is dict and type(presented.get('denominator')) is int
            and digest(presented) == digest(expected),
            'HELD_AUTHORITY', 'Unissued, mistyped or altered fixture warrant')
    require(expected['not_before'] <= now < expected['expires'] and now < expected['revoked_at'],
            'HELD_AUTHORITY', 'Fixture warrant expired, revoked or not yet valid')
    require((world['source_ref'], world['source_release_ref']) ==
            (expected['world_source'], expected['world_release']), 'HELD_AUTHORITY', 'Source/release outside warrant')
    require(world['time_axes']['as_of']==expected['knowledge_as_of'],
            'HELD_AUTHORITY', 'Knowledge-as-of outside fixture warrant')
    return expected


def knowledge_basis(world):
    return {k: world[k] for k in ('source_ref', 'source_release_ref', 'values', 'routes',
                                  'public_categories', 'public_sanctions')}


def check_earlier_knowledge(world, evidence_id, asof):
    # Explicit hypothetical test evidence, not a historical claim or original
    # issuance. Never accept an arbitrary non-null string or submitted record.
    require(evidence_id == 'TEST_ONLY:earlier-publication:2008',
            'NO_CURRENT_OR_NOT_KNOWN_ASOF', 'Earlier evidence not in owner fixture')
    require('2008' <= asof and digest(knowledge_basis(world)) == digest(knowledge_basis(fixture_world())),
            'NO_CURRENT_OR_NOT_KNOWN_ASOF', 'Earlier evidence source/release/content/time mismatch')
