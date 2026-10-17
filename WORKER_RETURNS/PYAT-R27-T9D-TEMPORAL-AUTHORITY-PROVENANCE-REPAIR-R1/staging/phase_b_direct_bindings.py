"""T9D direct candidate bindings for the frozen coupled semantic vectors.

Signature-only calls into the pinned T9D adapter. Each binding performs an ACTUAL
candidate call and returns the raw candidate result plus a call trace. No
external filtering, permission decision, output rewriting or synthesized refusal
is supplied here: missing capabilities are expressed IN the candidate (typed
`archival_known_at_upper_year` and typed `SourceGrant`), and the candidate itself
decides. A missing/mismatched/non-current/wrong-owner issuer claim returns the
candidate's explicit UNAVAILABLE result; this binding never invents a clearance.
"""
import json
from pathlib import Path


class CapabilityUnavailable(AssertionError):
    pass


def call_vector(key, T):
    vectors = json.loads(
        (Path(__file__).parent / '01B_FROZEN_COUPLED_BINDING_VECTORS.json').read_text()
    )['vectors']
    v = vectors[key]
    C = 'SYNTH_COUNTRY_A'
    world = T.StructuralWorld(
        'W_SYNTH_INSTITUTION',
        ('ROUTE_REDUCED_BURDEN', 'ROUTE_PARTICIPATION', 'ROUTE_DEFERRED_REVIEW'),
        (), 'SYNTH_INSTITUTION')

    if key == 'D04':
        # Typed archival known-at bound: snapshot 2020, source published 2030.
        # Target valid time (1990/1995) and archival snapshot known-at time (2020)
        # are separate clocks; the candidate must not treat the 2030 publication
        # as snapshot knowledge.
        spec = v['waves'][0]
        w = T.Wave(wave_id=spec['wave_id'], source_family='SYNTH_FAMILY', country=C,
                   instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
                   observation_year=spec['observation_year'],
                   published_year=spec['published_year'], value=spec['value'])
        c = T.TemporalCase(case_id=key, country=C, waves=(w,),
                           target_year=v['target_valid_year'])
        result = T.evaluate(c, T.METHOD_M0_HOLD, clock_year=v['target_valid_year'],
                            retrospective=bool(v.get('retrospective', True)),
                            archival_known_at_upper_year=v['archival_known_at_upper_year'])
        trace = dict(
            actual_candidate_call=True, output_rewritten=False,
            module_file=T.__file__, function='evaluate',
            arguments=dict(method=T.METHOD_M0_HOLD,
                           clock_year=v['target_valid_year'],
                           retrospective=bool(v.get('retrospective', True)),
                           archival_known_at_upper_year=v['archival_known_at_upper_year']),
            wave_fields=w.__dict__,
            case_fields=dict(case_id=key, target_year=v['target_valid_year']),
            limit='D04 uses the frozen archival-known-at vector; the bound is typed '
                  'candidate metadata and is enforced by the candidate, not filtered here')
        return result, trace

    if key in ('D16', 'D17', 'D17_WRONG_OWNER'):
        # Typed source-qualified issuer claim, checked by the candidate against
        # the used basis. Presence of metadata is never itself a grant.
        w = T.Wave(wave_id='VALID', source_family=v['source_family'], country=C,
                   instrument='SYNTH_INSTRUMENT', edition=v['wave_edition'],
                   cohort='COHORT_ALL', observation_year=1990, published_year=1990,
                   value=v.get('wave_value', .6))
        c = T.TemporalCase(case_id=key, country=C, waves=(w,),
                           target_year=v['query_year'])
        grant = T.SourceGrant(grant_source_family=v['grant_source_family'],
                              grant_edition=v['grant_edition'],
                              grant_current=bool(v['grant_current']))
        result = T.read_selected_world(
            world, c, T.METHOD_M0_HOLD, v['query_year'],
            retrospective=bool(v.get('retrospective', False)),
            source_grant=grant)
        trace = dict(
            actual_candidate_call=True, output_rewritten=False,
            module_file=T.__file__, function='read_selected_world',
            arguments=dict(method=T.METHOD_M0_HOLD, clock_year=v['query_year'],
                           retrospective=bool(v.get('retrospective', False)),
                           source_grant=dict(grant_source_family=v['grant_source_family'],
                                             grant_edition=v['grant_edition'],
                                             grant_current=bool(v['grant_current']))),
            wave_fields=w.__dict__,
            case_fields=dict(case_id=key, target_year=v['query_year']),
            world_fields=world.__dict__,
            limit='the frozen source-epoch/owner/currentness vector; the candidate '
                  'checks the claimed issuer grant against the used basis and returns '
                  'explicit UNAVAILABLE; no clearance is synthesized')
        return result, trace

    # D10 and D19 require only the existing wave, structural world and consumer.
    w = T.Wave(wave_id='VALID', source_family='SYNTH_FAMILY', country=C,
               instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
               observation_year=1990, published_year=1990, value=v.get('wave_value', .6))
    c = T.TemporalCase(case_id=key, country=C, waves=(w,), target_year=1995)
    result = T.read_selected_world(world, c, T.METHOD_M0_HOLD, 1995)
    return result, dict(actual_candidate_call=True, output_rewritten=False,
                        module_file=T.__file__, function='read_selected_world',
                        wave_fields=w.__dict__,
                        case_fields=dict(case_id=key, target_year=1995),
                        world_fields=world.__dict__, clock_year=1995, retrospective=False,
                        limit='D10 uses the frozen single-wave vector; passing cannot '
                              'establish a two-anchor actor-permission gate')
