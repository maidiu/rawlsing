"""POST-INSPECTION additions: not part of the Phase A oracle.
Exercise exact original native constructor with fully rehashed TEST_ONLY domain
variants, not source-qualified producer outputs or cross-instrument mappings.
"""
import importlib.util,os
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('gf1l_frozen_helper',Path(__file__).resolve().parents[1]/'phase_a/test_gf1l_executable_v2.py')
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)


def typed_equal(a,b):
    return type(a) is type(b) and a==b


def relation(role,domain):
    f=p.fields()
    cdom=domain if role=='condition' else tuple(f['conditioner_domain'])
    tdom=domain if role=='target' else tuple(f['target_domain'])
    f['conditioner_domain']=cdom;f['target_domain']=tdom
    f['conditional_count_profile']=tuple({
        'condition_state':c,'source_native_conditioner':f['conditioner_source_native_variable'],
        'condition_denominator_support':1,
        'target_counts':tuple({'target_state':t,
            'source_native_target':f['target_source_native_variable'],
            'joint_support_count':int(ci==ti),
            'joint_cell_state':'OBSERVED_POSITIVE' if ci==ti else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET'}
            for ti,t in enumerate(tdom))} for ci,c in enumerate(cdom))
    return p.make(f)


@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('domain',[(0,False),(0,0.0),('0',0),('0','1'),(0,1)],ids=['int_bool','int_float','string_int','strings_control','integers_control'])
def test_type_distinct_categories_never_silently_collapse_or_crash(role,domain):
    assert not typed_equal(*domain)
    rel=relation(role,domain)
    # Either fail closed as an explicitly unsupported typed-domain shape or
    # preserve both genuine constructor category identities and all support.
    got=p.h.CONS(rel)
    if got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED':
        assert got['separation_class'] is None
        assert got['downstream_value_produced'] is False
        return
    assert got['decision_state']=='PAIR_SUPPORT_SIGNATURE_COMPUTED',got
    assert got['joint_support_total']==2,got
    assert got['separation_class']=='EXACT_PAIR_SEPARATION',got
    assert len(got['support_vectors'])==2,got
    assert all(len(cells)==2 for cells in got['support_vectors'].values()),got
    assert got['production_owner_commit'] is False
