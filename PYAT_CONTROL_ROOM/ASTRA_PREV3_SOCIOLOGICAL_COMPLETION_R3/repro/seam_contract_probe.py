#!/usr/bin/env python3
"""Source-free acceptance oracle for the proposed R3 seam. Not production code.

No project runtime, source bytes, actor construction, fitting or provider calls.
Synthetic tables emulate producer outputs. No empirical validity is claimed.
"""
import hashlib
import json
from pathlib import Path


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def conditional(cells, conditions):
    selected = [r for r in cells if all(r[k] == v for k, v in conditions.items())]
    denominator = sum(r['n'] for r in selected)
    numerator = sum(r['n'] for r in selected if r['Y'] == 1)
    return {'denominator': denominator, 'numerator': numerator,
            'p_Y1': numerator / denominator if denominator else None,
            'state': 'SUPPORTED' if denominator else 'ZERO_SUPPORT',
            'conditions': dict(conditions)}


def synthesis(channels):
    """Deliberately simple disclosed blend; not an observed cross-source joint."""
    if len({c['target'] for c in channels}) != 1:
        return {'state': 'SUPPORT_MISMATCH', 'evidence_mode': 'INFERRED'}
    total = sum(c['model_weight'] for c in channels)
    if total <= 0:
        return {'state': 'INVALID_MODEL_WEIGHT', 'evidence_mode': 'INFERRED'}
    return {'state': 'MODELED', 'p': sum(c['p'] * c['model_weight'] for c in channels) / total,
            'evidence_mode': 'INFERRED', 'observed_joint': False,
            'assumption': 'Toy fixed model weights; no respondent linkage or empirical calibration',
            'source_refs': [c['id'] for c in channels],
            'uncertainty': {'sampling': 'UNKNOWN_SYNTHETIC', 'model': 'UNVALIDATED_TOY_POLICY'}}


def temporal(anchors, year, breaks=(), max_gap=10):
    lo, hi = anchors
    if year < lo['year'] or year > hi['year']:
        return {'state': 'OUTSIDE_HORIZON', 'value': None}
    if hi['year'] - lo['year'] > max_gap or any(lo['year'] < b <= hi['year'] for b in breaks):
        return {'state': 'BREAK_OR_GAP_BACKOFF', 'value': lo['value'], 'evidence_mode': 'PRIOR',
                'uncertainty': 'UNQUANTIFIED_BROAD', 'anchor_refs': [lo['id']]}
    if year in (lo['year'], hi['year']):
        chosen = lo if year == lo['year'] else hi
        return {'state': 'ANCHOR', 'value': chosen['value'], 'evidence_mode': 'TRANSFORMED', 'anchor_refs': [chosen['id']]}
    v = lo['value'] + (hi['value'] - lo['value']) * (year - lo['year']) / (hi['year'] - lo['year'])
    return {'state': 'INTERPOLATED', 'value': v, 'evidence_mode': 'INFERRED',
            'uncertainty': 'UNQUANTIFIED_MODEL', 'anchor_refs': [lo['id'], hi['id']]}


def consume(cells, conditions, channels, anchors, year, material, mode='FROZEN_TEST', revoked=False, breaks=()):
    if mode == 'CURRENT_TEST' and revoked:
        return {'state': 'CURRENT_REFUSED', 'reason': 'REVOKED_TEST_DEPENDENCY'}
    inputs = {'cells': cells, 'conditions': conditions, 'channels': channels,
              'anchors': anchors, 'year': year, 'material': material, 'mode': mode, 'breaks': list(breaks)}
    result = {'conditional': conditional(cells, conditions), 'synthesis': synthesis(channels),
              'historical_context': temporal(anchors, year, breaks),
              'opportunity_context': {'available_slots': material['available_slots']}}
    return {'state': 'CONSUMED', 'test_origin': 'SYNTHETIC_SOURCE_FREE',
            'world_scope': {'geography': 'TEST_REGION', 'target_population': 'TEST_POPULATION', 'year': year},
            'result': result,
            'receipt': {'consumer': 'R3_SYNTHETIC_CONTRACT_ORACLE_V1', 'input_hash': digest(inputs),
                        'read_value_hashes': {k: digest(v) for k, v in inputs.items()},
                        'output_hash': digest(result), 'production_owner_invoked': False,
                        'calibration_claim': False, 'actor_execution': False}}


def run():
    # Distinct from P04's 58-person/32→16→8 fixture. This is aggregated toy support.
    cells = [dict(A=a, B=b, Y=y, n=n) for a, b, y, n in
             [(0,0,0,9),(0,0,1,1),(0,1,0,9),(0,1,1,1),
              (1,0,0,1),(1,0,1,9),(1,1,0,1),(1,1,1,9)]]
    flipped = [dict(r, Y=1-r['Y']) for r in cells]
    channels = [dict(id='SYNTH_SOURCE_A', target='TEST_POPULATION', p=.2, model_weight=1),
                dict(id='SYNTH_SOURCE_B', target='TEST_POPULATION', p=.8, model_weight=1)]
    anchors = [dict(id='SYNTH_ANCHOR_2000', year=2000, value=10), dict(id='SYNTH_ANCHOR_2010', year=2010, value=30)]
    material = {'available_slots': 100}
    cases = []
    def check(name, passed, evidence):
        if not passed:
            raise AssertionError(name)
        cases.append({'case': name, 'status': 'PASS_SOURCE_FREE_ONLY', 'evidence': evidence})
    def call(**kw):
        args=dict(cells=cells, conditions={'A':1}, channels=channels, anchors=anchors, year=2005, material=material)
        args.update(kw)
        return consume(**args)
    baseline = call()
    opposite = call(cells=flipped)
    check('same_marginals_opposite_joints', conditional(cells,{})['p_Y1']==conditional(flipped,{})['p_Y1']==.5 and baseline['result']['conditional']['p_Y1']==.9 and opposite['result']['conditional']['p_Y1']==.1,
          {'unconditional':.5, 'conditioned_baseline':.9, 'conditioned_opposite':.1})
    nested=call(conditions={'A':1,'B':1})
    check('cumulative_condition_and_minority', [conditional(cells,{})['denominator'],baseline['result']['conditional']['denominator'],nested['result']['conditional']['denominator']]==[40,20,10] and nested['result']['conditional']['numerator']==9,
          {'denominators':[40,20,10], 'minority_count':1})
    changed=call(channels=[channels[0],dict(channels[1],p=.4)])
    check('synthesis_input_consumed', baseline['result']['synthesis']['p']==.5 and abs(changed['result']['synthesis']['p']-.3)<1e-12 and not changed['result']['synthesis']['observed_joint'], {'before':.5,'after':.3,'mode':'INFERRED'})
    mismatch=call(channels=[channels[0],dict(channels[1],target='ALIEN_POPULATION')])
    check('source_support_mismatch', mismatch['result']['synthesis']['state']=='SUPPORT_MISMATCH', mismatch['result']['synthesis'])
    history=call(anchors=[anchors[0],dict(anchors[1],value=50)])
    check('historical_input_consumed', baseline['result']['historical_context']['value']==20 and history['result']['historical_context']['value']==30 and history['result']['conditional']==baseline['result']['conditional'], {'before':20,'after':30,'mode':'INFERRED'})
    broken=call(breaks=(2004,)); outside=call(year=2020)
    check('break_gap_and_horizon', broken['result']['historical_context']['state']=='BREAK_OR_GAP_BACKOFF' and temporal(anchors,2005,max_gap=5)['state']=='BREAK_OR_GAP_BACKOFF' and outside['result']['historical_context']['state']=='OUTSIDE_HORIZON', {'break':broken['result']['historical_context'],'outside':outside['result']['historical_context']})
    altered_material=call(material={'available_slots':10})
    check('material_value_consumed_selectively', altered_material['result']['opportunity_context']!=baseline['result']['opportunity_context'] and altered_material['result']['conditional']==baseline['result']['conditional'], {'before':100,'after':10})
    irrelevant=call(material={'available_slots':100,'unused_label':'irrelevant'})
    check('irrelevant_context_and_replay', irrelevant['result']==baseline['result'] and call()==baseline, {'identical_semantic_result':True,'identical_replay':True})
    revoked=call(mode='CURRENT_TEST',revoked=True); historical=call(revoked=True)
    check('synthetic_current_refusal_historical_survival', revoked['state']=='CURRENT_REFUSED' and historical['state']=='CONSUMED', {'current':revoked['state'],'frozen_test':historical['state'],'limit':'Toy policy only; not B5 authentication proof'})
    unsupported=call(conditions={'A':2})
    check('unsupported_condition', unsupported['result']['conditional']['state']=='ZERO_SUPPORT' and unsupported['result']['conditional']['p_Y1'] is None, unsupported['result']['conditional'])
    return {'scope':'R3_SYNTHETIC_CONTRACT_ACCEPTANCE_ORACLE_ONLY', 'cases':cases,
            'production_tests_run':False,'real_source_evidence':False,'v3_executed':False,
            'baseline_bundle':baseline,'changed_joint_bundle':opposite,
            'limits':['No production owner imported or qualified','No source or fitted model validated','No independent reviewer execution','No full35/F6/F7/F8 acceptance']}


if __name__ == '__main__':
    output=run()
    path=Path(__file__).with_name('seam_contract_probe_result.json')
    path.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    print(f"{len(output['cases'])} source-free case groups passed; wrote {path}")
