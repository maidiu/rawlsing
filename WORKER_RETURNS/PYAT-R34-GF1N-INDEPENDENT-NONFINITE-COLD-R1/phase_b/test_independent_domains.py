"""GF1M Phase A independent adversarial expectations; frozen before candidate inspection."""
import importlib.util, os, json
from pathlib import Path
import pytest
spec=importlib.util.spec_from_file_location('gf1m_independent_helper',os.environ['GF1M_HISTORICAL_HELPER'])
p=importlib.util.module_from_spec(spec);spec.loader.exec_module(p)
class Text(str): pass
DOMAINS=[(0,False),(0,0.0),('0',0),('0',0.0),(-1,'-1'),('é','e\u0301'),(2**100,2**100+1),(float('inf'),1.0),(float('nan'),1.0),(-0.0,0.0),(Text('0'),'0'),('a:b','a|b')]
IDS=['bool_collision','float_collision','string_int','string_float','negative_string','unicode','huge_int','infinity','nan','signed_zero','subclass','delimiters']

def build(role,domain):
    f=p.fields()
    cd=domain if role=='condition' else tuple(f['conditioner_domain'])
    td=domain if role=='target' else tuple(f['target_domain'])
    f['conditioner_domain']=cd;f['target_domain']=td
    f['conditional_count_profile']=tuple(dict(condition_state=c,source_native_conditioner=f['conditioner_source_native_variable'],condition_denominator_support=1,target_counts=tuple(dict(target_state=t,source_native_target=f['target_source_native_variable'],joint_support_count=int(ci==ti),joint_cell_state='OBSERVED_POSITIVE' if ci==ti else 'OBSERVED_ZERO_IN_SUPPORTED_RISK_SET') for ti,t in enumerate(td))) for ci,c in enumerate(cd))
    return p.make(f)

@pytest.mark.parametrize('role',['condition','target'])
@pytest.mark.parametrize('domain',DOMAINS,ids=IDS)
def test_independent_domain_integrity(role,domain):
    try: rel=build(role,domain)
    except p.h.G.GenericNativePairError: return
    got=p.h.CONS(rel)
    assert got['production_owner_commit'] is False
    if got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED':
        assert got['separation_class'] is None and got['downstream_value_produced'] is False
        return
    # Same-type equal categories cannot represent two distinct declared states.
    assert not (type(domain[0]) is type(domain[1]) and domain[0]==domain[1]),got
    assert got['decision_state']=='PAIR_SUPPORT_SIGNATURE_COMPUTED',got
    assert got['joint_support_total']==2 and got['separation_class']=='EXACT_PAIR_SEPARATION',got
    assert len(got['support_vectors'])==2
    assert all(len(v)==2 for v in got['support_vectors'].values())
    encoded=json.dumps(got,sort_keys=True,allow_nan=False)
    assert json.dumps(p.h.CONS(rel),sort_keys=True,allow_nan=False)==encoded
    assert got['result_hash']==p.h.CONS(rel)['result_hash']

@pytest.mark.parametrize('role',['condition','target'])
def test_type_swap_changes_relation_identity_and_refuses(role):
    f=p.fields(); original=p.make(f)
    if role=='condition': f['conditional_count_profile'][0]['condition_state']=0
    else: f['conditional_count_profile'][0]['target_counts'][0]['target_state']=0
    altered=p.make(f)
    assert altered.content_hash!=original.content_hash
    got=p.h.CONS(altered)
    assert got['decision_state']=='CONSUMER_RELATION_INTEGRITY_REJECTED'
    assert got['separation_class'] is None and got['downstream_value_produced'] is False
