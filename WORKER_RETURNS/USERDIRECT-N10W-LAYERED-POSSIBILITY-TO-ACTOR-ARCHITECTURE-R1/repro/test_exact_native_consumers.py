"""Genuine byte-verified inherited E04 clients; synthetic read-only service adapter.
No owner E05R/C1/N10E reexecution, no model, no actor.
"""
import copy, subprocess, sys, json, os, pathlib
from dataclasses import dataclass
import pytest
from native import nonparent,scenario

BASE=dict(training_access=True,training_fee=2,exit_cost=2,civil_open=True,civil_sanction=False)
REV=dict(training_access=False,training_fee=2,exit_cost=8,civil_open=True,civil_sanction=False)
@dataclass
class Snapshot: snapshot_hash:str='TEST_ONLY_SELECTED_SNAPSHOT'
class Service:
    def __init__(self,fields,empirical=None):
        self.fields=fields;self.value_reads=[];self.empirical=empirical or {'state':'PRODUCTIVE_TEST_ONLY','steps':[{'target':'Y','conditioners':['X'],'denominator':32,'state':'SUPPORTED','cells':[{'cell':'1','raw_numerator_support':18},{'cell':'0','raw_numerator_support':14}],'evidence_ref':'TEST_ONLY_PRODUCER'}]}
    def structural(self,snap,key,consumer):
        v=self.fields.get(key);item=dict(state='SUPPORTED_TEST_ONLY' if v is not None else 'UNAVAILABLE_AUTHORITY_OR_CLOCK',value=v,field_ref='TEST_ONLY_'+key)
        self.value_reads.append(dict(key=key,consumer=consumer,snapshot=snap.snapshot_hash))
        return item
    def possibilities(self,snap,consumer):return copy.deepcopy(self.empirical)
    def _record(self,x):return x

def test_native_blob_sha():
    root=pathlib.Path(__file__).parent/'native'
    for fn,expected in [('nonparent.py','2181b832d3c4376d4b9428e13f4354f273be8f32'),('scenario.py','b7e568166cd277c1ba127374ea1a350d1b3841a2')]:
        assert subprocess.check_output(['git','hash-object',str(root/fn)],text=True).strip()==expected
    assert pathlib.Path(nonparent.__file__).resolve()==(root/'nonparent.py').resolve()

def test_training_world_difference_real_code():
    a=nonparent.consume(Service(BASE),Snapshot())
    b=nonparent.consume(Service(REV),Snapshot())
    assert a['structural_routes']['training']['state']=='ELIGIBLE'
    assert b['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
    assert a['structural_routes']['exit_constraint']['state']=='WITHIN_MODELED_BUDGET'
    assert b['structural_routes']['exit_constraint']['state']=='RESOURCE_CONSTRAINED'
    assert a['structural_routes']['civil']==b['structural_routes']['civil']
    assert a['empirical']==b['empirical'] and a['route_probability'] is b['route_probability'] is None

def test_native_proposal_access_does_not_mean_affordable():
    case={**BASE,'training_fee':7}
    a=nonparent.consume(Service(case),Snapshot())
    b=scenario.evaluate(Service(case),Snapshot(),[dict(scenario_id='q1',route='institutional')])
    assert a['structural_routes']['training']['state']=='BLOCKED_BY_MODELED_RULE'
    assert b['scenarios'][0]['feasibility']=='FEASIBLE_MODELED_PREMISE'
    assert b['scenarios'][0]['selection_weight'] is None

def test_sanction_can_block_civil():
    p=nonparent.consume(Service({**BASE,'civil_sanction':True}),Snapshot())
    q=scenario.evaluate(Service({**BASE,'civil_sanction':True}),Snapshot(),[dict(scenario_id='c',route='civil')])
    assert p['structural_routes']['civil']['state']=='BLOCKED_BY_MODELED_RULE'
    assert q['scenarios'][0]['feasibility']=='INFEASIBLE_MODELED_PREMISE'

def test_unknown_and_revoked_no_false_known():
    p=nonparent.consume(Service({**BASE,'training_access':None}),Snapshot())
    q=scenario.evaluate(Service({**BASE,'training_access':None}),Snapshot(),[dict(scenario_id='t',route='institutional')])
    assert p['structural_routes']['training']['state']=='UNAVAILABLE_AUTHORITY_OR_CLOCK'
    assert q['scenarios'][0]['feasibility']=='UNKNOWN_PREMISE'

def test_missing_empirical_support_preserves_null():
    e={'state':'PARTIAL_TEST_ONLY','steps':[{'target':'Y','conditioners':['X'],'denominator':0,'cells':[{'cell':'null','raw_numerator_support':0}],'state':'ZERO_SUPPORT'}]}
    p=nonparent.consume(Service(BASE,e),Snapshot())
    assert p['state']=='PARTIAL_OPTIONS_OR_EMPIRICAL_SUPPORT'
    assert p['source_balance_reads'][0]['source_balance_count'] is None
    assert p['route_probability'] is None

def test_native_empirical_only_mutation_leaves_structural():
    e={'state':'PRODUCTIVE_TEST_ONLY','steps':[{'target':'Y','conditioners':['X'],'denominator':32,'cells':[{'cell':'1','raw_numerator_support':19},{'cell':'0','raw_numerator_support':13}],'state':'SUPPORTED'}]}
    a=nonparent.consume(Service(BASE),Snapshot())
    b=nonparent.consume(Service(BASE,e),Snapshot())
    assert a['source_balance_reads'][0]['source_balance_count']==4
    assert b['source_balance_reads'][0]['source_balance_count']==6
    assert a['structural_routes']==b['structural_routes']

def test_no_person_or_conception_claims():
    p=scenario.evaluate(Service(BASE),Snapshot(),[dict(scenario_id='a',route='civil')])
    assert p['person_generation'] is p['actual_conception'] is p['relationships_generated'] is False
    assert p['scenarios'][0]['selection_weight'] is None

def test_no_unsupported_scenario_fields():
    with pytest.raises(ValueError):scenario.evaluate(Service(BASE),Snapshot(),[dict(scenario_id='a',route='institutional',actor_personality=0.9)])

def test_native_budget_exact_integer_required():
    with pytest.raises(ValueError):nonparent.consume(Service(BASE),Snapshot(),budget_tokens=5.0)

def test_native_empty_proposals_fail():
    with pytest.raises(ValueError):scenario.evaluate(Service(BASE),Snapshot(),[])

def test_native_duplicate_id_fail():
    with pytest.raises(ValueError):scenario.evaluate(Service(BASE),Snapshot(),[dict(scenario_id='a',route='civil'),dict(scenario_id='a',route='institutional')])

def test_no_route_prob_even_when_access_true():
    p=nonparent.consume(Service(BASE),Snapshot());assert p['route_probability'] is None

def test_original_proposal_scenario_is_access_premise_only():
    p=scenario.evaluate(Service(REV),Snapshot(),[dict(scenario_id='train',route='institutional'),dict(scenario_id='civil',route='civil')])
    assert [v['feasibility'] for v in p['scenarios']]==['INFEASIBLE_MODELED_PREMISE','FEASIBLE_MODELED_PREMISE']
