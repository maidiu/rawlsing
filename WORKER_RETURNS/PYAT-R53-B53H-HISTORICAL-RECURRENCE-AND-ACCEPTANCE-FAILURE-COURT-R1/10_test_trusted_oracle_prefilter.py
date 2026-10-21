"""Source-free structural controls; no Rawlsing native execution whatsoever."""
import copy
import importlib.util
from pathlib import Path
spec = importlib.util.spec_from_file_location('b53h2', Path(__file__).with_name('09_trusted_oracle_prefilter.py'))
g = importlib.util.module_from_spec(spec)
spec.loader.exec_module(g)


def case():
    policy = {'schema': g.SCHEMA, 'original35': [{'id': f's{i}', 'format': 'SAV' if i < 31 else 'DTA'} for i in range(35)],
        'mandatory_edge_classes': ['ROUTED', 'HOUSEHOLD', 'WEIGHTED'], 'fixtures': []}
    for i,(family,fmt,klass) in enumerate([('a','SAV','ROUTED'),('b','DTA','HOUSEHOLD'),('c','SAV','WEIGHTED')]):
        policy['fixtures'].append({'id':f'fx{i}','family':family,'format':fmt,
            'edge_classes':[klass], 'structural_topology':{'risk_class':klass,'levels':i+1},
            'expected_operation_states': {f'op{i}': 'NATIVE_PRODUCED'}, 'pre_outcome_root': f'pre{i}', 'i05_required':True})
    result = {'candidate_commit':'f'*40, 'original35':[{'id':f's{i}', 'grade':'NO_SCIENCE', 'original_u':None,
        'original_e_pre':None,'hold_reason':'original not issued'} for i in range(35)],
        'fixture_runs':[], 'original_science_claim':'HOLD',
        'metamorphic_events':[{'kind':'RENAMING','source_fixture':'fx0','same_normalized_op_root':True,
            'same_consumer_value_root':True,'no_reserved_fixture_ids':True},
            {'kind':'MUTATION','baseline':'PASS','mutant':'ASSERTION_FAILED','cold_restore':'PASS','real_consumer_id':'E04'}]}
    for f in policy['fixtures']:
        result['fixture_runs'].append({'id': f['id'],'operation_states':f['expected_operation_states'],
        'frozen_pre_outcome_root':f['pre_outcome_root'], 'public_call_trace_id':'trace:'+f['id'],
        'actual_native_c11':True,'actual_native_i03':True,'actual_native_i05':True,'grade':'SOURCEFREE_TEST_ONLY'})
    return policy, g.digest(policy), result


def hasfail(p, pin, r, code):
    out = g.analyze(p, pin, r)
    assert code in out['failures'], out


def test_good_structural_crosswalk_is_not_an_execution_certificate():
    p, pin, r = case()
    out = g.analyze(p, pin, r)
    assert not out['failures']
    assert out['status'] == 'STRUCTURAL_CROSSWALK_READY_FOR_INDEPENDENT_NATIVE_VALIDATION'
    assert out['limit'] == 'NO_NATIVE_EXECUTION_OR_ATTESTATION_VALIDATED_HERE'


def test_candidate_cannot_rewrite_external_expected_operations():
    p,pin,r=case()
    r['fixture_runs'][0]['operation_states']={'fake_op':'NATIVE_PRODUCED'}
    hasfail(p,pin,r,'OPERATION_STATE_ANTI_JOIN:fx0')


def test_candidate_cannot_self_select_source_shape():
    p,pin,r=case()
    # Same native variable names are irrelevant; topology must differ in protected oracle.
    p['fixtures'][1]['structural_topology'] = p['fixtures'][0]['structural_topology']
    p['fixtures'][2]['structural_topology'] = p['fixtures'][0]['structural_topology']
    hasfail(p,g.digest(p),r,'INSUFFICIENT_GENUINE_SHAPE_DIVERSITY')


def test_mutation_of_protected_policy_invalidates_pin():
    p,pin,r=case()
    p['fixtures'][0]['expected_operation_states']={'new':'NATIVE_PRODUCED'}
    hasfail(p,pin,r,'POLICY_PIN_MISMATCH')


def test_missing_expected_fixture_rejected():
    p,pin,r=case()
    r['fixture_runs'].pop()
    hasfail(p,pin,r,'FIXTURE_EXPECTED_ACTUAL_ANTI_JOIN')


def test_refusal_cannot_be_original_measured_null():
    p,pin,r=case()
    r['original35'][0]['original_e_pre']=0
    hasfail(p,pin,r,'HOLD_AS_FALSE_ZERO_OR_PRODUCT:s0')


def test_missing_i05_rejected_if_independently_expected():
    p,pin,r=case()
    r['fixture_runs'][1]['actual_native_i05']=False
    hasfail(p,pin,r,'I05_UNOBSERVED:fx1')


def test_fake_scientific_completion_rejected():
    p,pin,r=case()
    r['original_science_claim']='COMPLETE'
    hasfail(p,pin,r,'SCIENTIFIC_ORIGINAL_CLAIM_ELEVATED')
