"""Signature-only calls of frozen vectors; missing capabilities fail explicitly.

No external filtering, permission decision or output transformation is supplied.
"""
import json
from pathlib import Path

class CapabilityUnavailable(AssertionError):
    pass

def call_vector(key, T):
    vectors = json.loads((Path(__file__).parent/'01B_FROZEN_COUPLED_BINDING_VECTORS.json').read_text())['vectors']
    v = vectors[key]
    if key == 'D04':
        raise CapabilityUnavailable('D04: evaluate has no archival_known_at_upper_year; 2020 snapshot cannot be represented without forbidden reviewer filtering')
    if key in ['D16', 'D17', 'D17_WRONG_OWNER']:
        raise CapabilityUnavailable(key+': source-owner/edition/current grant pair has no candidate API representation; refusing to invent a permission gate')
    # D10 and D19 require only the existing wave, structural world and consumer.
    w = T.Wave(wave_id='VALID', source_family='SYNTH_FAMILY', country='SYNTH_COUNTRY_A',
               instrument='SYNTH_INSTRUMENT', edition='E1', cohort='COHORT_ALL',
               observation_year=1990, published_year=1990, value=v.get('wave_value', .6))
    c = T.TemporalCase(case_id=key, country='SYNTH_COUNTRY_A', waves=(w,), target_year=1995)
    world = T.StructuralWorld('W_SYNTH_INSTITUTION',
              ('ROUTE_REDUCED_BURDEN','ROUTE_PARTICIPATION','ROUTE_DEFERRED_REVIEW'),
              (), 'SYNTH_INSTITUTION')
    result = T.read_selected_world(world, c, T.METHOD_M0_HOLD, 1995)
    return result, dict(actual_candidate_call=True, output_rewritten=False,
                        module_file=T.__file__, function='read_selected_world',
                        wave_fields=w.__dict__, case_fields=dict(case_id=key, target_year=1995),
                        world_fields=world.__dict__, clock_year=1995, retrospective=False,
                        limit='D10 uses the frozen single-wave vector; passing cannot establish a two-anchor actor-permission gate')
