from pathlib import Path
import json,sys
import pytest
from g12_assays import ROOT,endpoint,DadHistoryBuilder,build_mother_checkpoint,ScopedRNG
from lab_sgi1.relation import reconcile
from lab_sgi1.continuation import forward_continuation

def write(name,record):
    (ROOT/'evidence'/('supplemental_'+name+'.json')).write_text(json.dumps(record,indent=2)+'\n')

def test_invalid_root_seed_is_refused():
    rng=ScopedRNG('short','v3.causal.adp015.conception_scenario_selection','G12_SCOPE')
    with pytest.raises((ValueError,TypeError)):
        r=rng.draw(3,'slot','cset');write('invalid_root',r.as_dict())

def test_mapping_rejects_entropy_outside_unbiased_range():
    rng=ScopedRNG('00'*32,'v3.causal.adp015.conception_scenario_selection','G12_SCOPE')
    calls=[]
    def raw(*args):
        calls.append(args)
        return 2**64-1 if len(calls)==1 else 1
    rng._raw=raw
    r=rng.draw(3,'slot','cset');write('entropy_rejection',dict(calls=len(calls),receipt=r.as_dict()))
    assert len(calls)==2
    assert r.draw_value==1

def test_no_relationship_admission_without_second_parent_or_witness():
    anchor=build_mother_checkpoint('G12_RELATION','M0').anchor_dict()
    result=reconcile(anchor,[],{'candidate_kind':'PROVISIONAL_COUNTERPART'})
    write('no_witness',result)
    assert result['status']!='COMMITTED'

def test_objective_relation_binds_actual_second_parent_identity():
    anchor=build_mother_checkpoint('G12_RELATION','M0').anchor_dict()
    events=DadHistoryBuilder('G12_ACTUAL_SECOND_PARENT','G12_SEED',endpoint()).build()
    result=reconcile(anchor,events,{'candidate_kind':'PROVISIONAL_COUNTERPART'})
    write('actor_identity',dict(expected_actor='G12_ACTUAL_SECOND_PARENT',relation=result))
    assert result['objective_relation']['participants'][1]=='G12_ACTUAL_SECOND_PARENT'

def test_empty_parent_history_cannot_emit_paternal_world_continuation():
    anchor=build_mother_checkpoint('G12_RELATION','M0').anchor_dict()
    result=forward_continuation(anchor,[],{'objective_relation':{'participants':[anchor['actor_id'],'G12_UNFORMED']}})
    write('empty_continuation',result)
    assert not [e for e in result.get('continuation_events',[]) if e['actor']=='G12_UNFORMED']

def test_explicit_asymmetry_and_no_automatic_household_control():
    anchor=build_mother_checkpoint('G12_RELATION','M0').anchor_dict()
    events=DadHistoryBuilder('G12_ACTUAL_SECOND_PARENT','G12_SEED',endpoint()).build()
    result=reconcile(anchor,events,{'candidate_kind':'PROVISIONAL_COUNTERPART'},True)
    write('asymmetry',result)
    assert result['perceived_states'][0]['perceived_state']=='affectionate_bond_perceived'
    assert result['perceived_states'][1]['perceived_state']=='UNKNOWN_OR_NONRECIPROCAL'
    assert not result['household_membership_auto']
