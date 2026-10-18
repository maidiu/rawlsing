"""Author tests: representable keys preserve types; unsafe keys fail closed.
Uses the original native constructor and fixture tree, with TEST_ONLY variants.
"""
import importlib.util
from pathlib import Path
import pytest

s=importlib.util.spec_from_file_location('gf1l_supplemental',Path(__file__).resolve().parents[1]/'postinspection/test_gf1l_typed_domain_conservation.py')
t=importlib.util.module_from_spec(s);s.loader.exec_module(t)


@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('domain',[
    ('0','1'),(0,1),(0.0,1.0),(False,True),(0,True),(False,1),(0,1.5),
],ids=['strings','integers','floats','booleans','int_bool_distinct','bool_int_distinct','int_float_distinct'])
def test_representable_domains_preserve_native_keys_and_counts(role,domain):
    rel=t.relation(role,domain)
    got=t.p.h.CONS(rel)
    assert got['decision_state']=='PAIR_SUPPORT_SIGNATURE_COMPUTED',got
    assert got['separation_class']=='EXACT_PAIR_SEPARATION',got
    assert got['joint_support_total']==2
    assert got['production_owner_commit'] is False
    for c,(actual_c,cells) in zip(rel.conditioner_domain,got['support_vectors'].items(),strict=True):
        assert type(actual_c) is type(c) and actual_c==c
        for target,actual_target in zip(rel.target_domain,cells,strict=True):
            assert type(actual_target) is type(target) and actual_target==target
    assert sum(sum(row.values()) for row in got['support_vectors'].values())==2


@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('domain',[
    (0,False),(0,0.0),('0',0),('x',1),(None,1),([0],[1]),
],ids=['bool_collision','float_collision','string_int_collision','unsortable_distinct','none_int','unhashable'])
def test_unrepresentable_keys_refused_before_any_scientific_product(role,domain):
    rel=t.relation(role,domain)
    got=t.p.h.CONS(rel)
    assert got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED',got
    assert got['separation_class'] is None
    assert got['downstream_value_produced'] is False
    assert got['production_owner_commit'] is False
    for field in ('joint_support_total','support_vectors','separation_signature','result_hash'):
        assert field not in got,got
