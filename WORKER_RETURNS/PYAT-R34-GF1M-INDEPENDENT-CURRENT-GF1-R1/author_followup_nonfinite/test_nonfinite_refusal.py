"""Author follow-up tests. Original GF1M26 stays byte-identical and separate."""
import importlib.util, json, os, sys
import pytest
s=importlib.util.spec_from_file_location('gf1m_original_phase_a',os.environ['GF1M_ORIGINAL_PHASE_A'])
f=importlib.util.module_from_spec(s);s.loader.exec_module(f)

@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('nonfinite',[float('inf'),float('-inf'),float('nan')],ids=['positive_inf','negative_inf','nan'])
@pytest.mark.parametrize('position',[0,1])
def test_nonfinite_category_typed_refusal_has_no_scientific_fields(role,nonfinite,position):
    domain=[1.0,1.0];domain[position]=nonfinite
    relation=f.build(role,tuple(domain))
    got=f.p.h.CONS(relation)
    assert got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED',got
    assert got['separation_class'] is None and got['downstream_value_produced'] is False
    assert got['production_owner_commit'] is False
    assert got['generic_native_semantics_hold']=='RETAINED'
    assert not {'result_hash','support_vectors','joint_support_total','separation_signature'} & got.keys()
    json.dumps(got,sort_keys=True,allow_nan=False)

@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('domain',[(0.0,1.0),(-sys.float_info.max,sys.float_info.max),(5e-324,1e-323),(0,1.5),('0','1')],ids=['finite','finite_extremes','subnormal','heterogeneous_numeric','source_strings'])
def test_finite_native_controls_preserve_identity_support_and_serialization(role,domain):
    relation=f.build(role,domain);got=f.p.h.CONS(relation)
    assert got['decision_state']=='PAIR_SUPPORT_SIGNATURE_COMPUTED'
    assert got['separation_class']=='EXACT_PAIR_SEPARATION' and got['joint_support_total']==2
    assert got['production_owner_commit'] is False
    assert sum(sum(row.values()) for row in got['support_vectors'].values())==2
    for expected,(actual,cells) in zip(relation.conditioner_domain,got['support_vectors'].items(),strict=True):
        assert type(actual) is type(expected) and actual==expected
        for expected_target,actual_target in zip(relation.target_domain,cells,strict=True):
            assert type(actual_target) is type(expected_target) and actual_target==expected_target
    assert got['result_hash']==f.p.h.CONS(relation)['result_hash']
    json.dumps(got,sort_keys=True,allow_nan=False)
