"""Actual legacy recurrence and explicitly provisional history-contract observations."""
from copy import deepcopy
from dataclasses import asdict
import os,subprocess,sys
import pytest
from recursive_court import (ROOT,digest,initial_state,config_and_order,run_trajectory,
    CanonLedger,propose_realization,propose_situations,admit_first_proposal,
    apply_existing_events,event,r1_world)

@pytest.fixture(scope='module')
def runs():return {w:run_trajectory(w) for w in r1_world.WORK_OUTCOMES}

def frame_from(run):return deepcopy(run['source_preimages']['episode-theft'])

def test_actual_54_field_schema_not_replacement_trait_vector(runs):
    for r in runs.values():
        assert len(r['initial'])==54
        assert r['initial']['initial_state_provenance']['not_generated_actor'] is True
        assert r['initial']['age']==6 and r['final_state']['age']==10
        assert len(r['initial']['domains'])==5

def test_ordinary_engine_steps_change_more_than_clock_before_and_after(runs):
    for r in runs.values():
        for t in r['ticks']:
            assert t['executed']=='v3.engine.yearly_step.run_one_year'
            assert t['after']['age']==t['before']['age']+1 and t['pressure_status']=='clean'
            assert any(c['path'].split('.')[0] not in {'year','age','yearly_integrity','rendered_output'} for c in t['numeric_changes'])
            assert t['after']['events_this_year']==[]

def test_upstream_pair_holds_initial_records_and_unrelated_draws_fixed(runs):
    values=list(runs.values())
    for key in ('initial','pre_encounter','world','proposal'):
        assert len({digest(r[key]) for r in values})==1
    assert len({digest(r['rng'][1:]) for r in values})==1
    assert all(r['resolved']['workplace']['clock']<r['world']['theft']['clock']<r['immediate']['clock'] for r in values)

def test_material_constraints_change_opportunity_before_effect(runs):
    a,b=runs['ROUTINE'],runs['RAISE_WITH_OVERTIME']
    assert a['resolved']['father_response']['available_minutes']==35
    assert b['resolved']['father_response']['available_minutes']==3
    assert a['resolved']['father_present'] and not b['resolved']['father_present']
    assert len(a['immediate']['selected_events'])==2 and len(b['immediate']['selected_events'])==1
    assert a['immediate']['after_hash']!=b['immediate']['after_hash']

def test_distinct_workplace_circumstances_can_converge_numerically(runs):
    a,b=runs['ROUTINE'],runs['HOURS_CUT']
    assert a['resolved']['workplace']!=b['resolved']['workplace']
    assert a['immediate']['after_hash']==b['immediate']['after_hash']
    assert a['final_state']==b['final_state']

def test_existing_runtime_effect_propagates_across_sections(runs):
    a,b=runs['ROUTINE'],runs['RAISE_WITH_OVERTIME']
    assert len({c['path'].split('.')[0] for c in a['immediate']['numeric_changes']})>1
    assert a['ticks'][2]['after_hash']!=b['ticks'][2]['after_hash']
    assert a['final_state']['capacity']['social_support']!=b['final_state']['capacity']['social_support']
    assert all(t['executed']=='v3.engine.yearly_step.run_one_year' for t in a['ticks']+b['ticks'])

def test_same_employer_event_moderated_by_prior_care_practice(runs):
    b=run_trajectory('RAISE_WITH_OVERTIME',father=r1_world.FatherHistory(protected_care_min=24));a=runs['RAISE_WITH_OVERTIME']
    assert a['resolved']['workplace']==b['resolved']['workplace']
    assert not a['resolved']['father_present'] and b['resolved']['father_present']
    f=b['resolved']['father_response']
    assert f['overtime_declined_min']+f['overtime_worked_min']==32 and f['available_minutes']==24

def test_first_call_receives_existing_age_and_state(runs):
    r=runs['ROUTINE'];p=r['proposal']
    assert p['conditioning']['state_hash']==digest(r['pre_encounter']) and p['conditioning']['age']==8
    assert len(p['situational_options'])==3 and p['legacy_parsed_packet']['branch_hypotheses']==[]
    assert p['authority']=='RECORDED_MOCK_NOT_ISSUED_CAN008'

@pytest.mark.parametrize('payload',[{'desired_personality':'future-kindness'},{'target_personality':'outcome'},{'capacity_deltas':{'skill':10}},{'branch_hypotheses':[{'id':'ending'}]}])
def test_first_call_rejects_endpoints_and_direct_metric_writes(payload):
    state=initial_state();packet=deepcopy(propose_situations(state)['raw_packet']);packet.update(payload)
    with pytest.raises(ValueError,match='FORBIDDEN'):admit_first_proposal(packet,state)

def test_second_call_has_both_states_and_no_numeric_write(runs):
    r=runs['ROUTINE'];n=r['narrative_input']
    assert n['before']==r['immediate']['before'] and n['after']==r['immediate']['after']
    assert r['ticks'][2]['before']==r['immediate']['after']
    assert r['recorded_second_call']['psychological_changes']=={}

def test_nonunique_compatible_flesh_preserves_transition_and_is_consumed():
    a=run_trajectory(location='hall_drawer',variant='plain');b=run_trajectory(location='garage_shelf',variant='alternate')
    assert a['immediate']==b['immediate'] and a['canon'][0]['text']!=b['canon'][0]['text']
    assert a['later']['target_location']=='hall_drawer' and b['later']['target_location']=='garage_shelf'
    assert a['later']['canon_read']['hash']==a['canon'][0]['hash']
    assert a['final_state']==b['final_state']

@pytest.mark.parametrize('field,value',[('bicycle_missing',False),('father_present',False),('lock_id','invented-lock'),('lock_location','unavailable-room')])
def test_contradictory_or_incompatible_flesh_rejected(runs,field,value):
    f=frame_from(runs['ROUTINE']);c=propose_realization(f);c['facts'][field]=value
    with pytest.raises(ValueError):CanonLedger().admit(f,c)

def test_unsupported_psychological_addition_rejected(runs):
    f=frame_from(runs['ROUTINE']);c=propose_realization(f);c['psychological_changes']={'new_belief':'always_safe'}
    with pytest.raises(ValueError,match='UNSUPPORTED_PSYCHOLOGICAL_CHANGE'):CanonLedger().admit(f,c)

def test_false_prose_cannot_hide_behind_true_facts(runs):
    f=frame_from(runs['ROUTINE']);c=propose_realization(f);c['text']='The child became permanently trusting.'
    with pytest.raises(ValueError,match='PROSE_NOT_SUPPORTED'):CanonLedger().admit(f,c)

def test_state_hash_swap_rejected(runs):
    f=frame_from(runs['ROUTINE']);c=propose_realization(f);c['poststate_hash']='0'*64
    with pytest.raises(ValueError,match='STATE_MISMATCH'):CanonLedger().admit(f,c)

def test_numerical_nochange_permits_history_append(runs):
    state=initial_state();config,_=config_and_order()
    # The legacy function normalizes initial aliases on first invocation; that
    # is recorded separately, not misrepresented as a zero-delta no-change.
    apply_existing_events(state,[],config,0)
    neutral=apply_existing_events(state,[],config,23)
    assert neutral['before_hash']==neutral['after_hash']
    original=frame_from(runs['ROUTINE'])
    frame=dict(id='neutral-observation',effect=neutral,world=original['world'],resolved={'father_present':False,'child_at_home':True})
    snapshot=deepcopy(asdict(state));ledger=CanonLedger()
    e=ledger.admit(frame,propose_realization(frame))
    assert e['prestate_hash']==e['poststate_hash'] and len(ledger.entries)==1
    assert asdict(state)==snapshot


def test_independent_counterpart_refuses_while_canon_detail_is_used(runs):
    r=runs['ROUTINE'];o=r['later']['counterpart']
    assert o['action']=='DECLINE_CONTACT' and not o['focal_child_state_read']
    assert r['later']['action']=='FETCH_EXISTING_LOCK'
    alternative=run_trajectory(busy=False)
    assert alternative['later']['counterpart']['action']=='ALLOW_CONTACT' and alternative['immediate']==r['immediate']

def test_unrelated_append_does_not_rewrite_prior_snapshot(runs):
    f=frame_from(runs['ROUTINE']);before=deepcopy(f);ledger=CanonLedger();first=ledger.admit(f,propose_realization(f));ledger.append_unrelated()
    assert f==before and ledger.entries[0]==first
    exported=ledger.entries;exported[0]['facts']['lock_location']='tampered'
    assert ledger.entries[0]==first

def test_historical_source_rewrite_refuses_continuation(runs):
    f=frame_from(runs['ROUTINE']);ledger=CanonLedger();e=ledger.admit(f,propose_realization(f))
    ledger._sources[f['id']]['world']['theft']['object']='other-bike'
    with pytest.raises(ValueError,match='SOURCE_PREIMAGE_REWRITE'):ledger.later_consume(e['id'])

def test_history_rewrite_refused_without_merkle_descendant_requirement(runs):
    f=frame_from(runs['ROUTINE']);ledger=CanonLedger();e=ledger.admit(f,propose_realization(f));ledger._entries[0]['facts']['lock_location']='garage_shelf'
    with pytest.raises(ValueError,match='HISTORY_REWRITE'):ledger.later_consume(e['id'])

def test_same_id_source_replacement_refused(runs):
    f=frame_from(runs['ROUTINE']);ledger=CanonLedger();ledger.admit(f,propose_realization(f))
    with pytest.raises(ValueError,match='SOURCE_ID_REUSE'):ledger.admit(f,propose_realization(f))

def test_future_canon_and_other_actor_private_read_refused(runs):
    f=frame_from(runs['ROUTINE']);ledger=CanonLedger();e=ledger.admit(f,propose_realization(f))
    with pytest.raises(ValueError,match='FUTURE_CANON_READ'):ledger.later_consume(e['id'],clock=24)
    with pytest.raises(ValueError,match='HISTORY_ACCESS_DENIED'):ledger.later_consume(e['id'],actor='neighbor')

def test_future_source_not_backfilled_as_earlier_narrative(runs):
    f=frame_from(runs['ROUTINE']);c=propose_realization(f);c['clock']=22
    with pytest.raises(ValueError,match='FUTURE_SOURCE'):CanonLedger().admit(f,c)

def test_canon_read_is_parent_of_delayed_numerical_feedback(runs):
    r=runs['ROUTINE'];f=r['delayed_feedback']
    assert f['actual_activity_source']==r['later'] and f['before_hash']!=f['after_hash']
    assert r['ticks'][3]['before']==f['after'] and f['clock']>r['later']['clock']>r['canon'][0]['clock']

def test_recorded_rng_and_mock_proposal_replay_deterministic(runs):
    for w,r in runs.items():assert run_trajectory(w)==r
    a=run_trajectory(workplace=None);assert a==run_trajectory(workplace=None) and a['rng'][0]['intervention'] is None

def test_cross_process_hash_seed_replay():
    code="from recursive_court import run_trajectory; print(run_trajectory()['trace_hash'])"
    outputs=[subprocess.check_output([sys.executable,'-c',code],cwd=ROOT,env={**os.environ,'PYTHONHASHSEED':str(seed),'PYTHONDONTWRITEBYTECODE':'1'},text=True).strip() for seed in (0,1,71)]
    assert len(set(outputs))==1

def test_scope_is_bounded_not_general_language_or_native_owner_claim(runs):
    for r in runs.values():
        assert r['native_grade']=='CONTRACT_HOLD_MISSING_OWNER_API'
        assert 'closed grammar, not general semantic fidelity' in r['policy_limits'] and not r['immediate']['qualified_psychological_law']

def test_legacy_event_tag_is_unqualified_assumption_not_discovered_law():
    c,_=config_and_order();a=initial_state();b=initial_state();first=event('same','loss');second=deepcopy(first);second['kind']='relationship'
    x=apply_existing_events(a,[first],c,1);y=apply_existing_events(b,[second],c,1)
    assert x['after_hash']!=y['after_hash'] and not x['qualified_psychological_law'] and not y['qualified_psychological_law']


def test_pressure_flow_can_recompute_without_a_between_world_difference(runs):
    a,b=runs['ROUTINE'],runs['RAISE_WITH_OVERTIME']
    assert a['final_state']['pressure_flow_history']==b['final_state']['pressure_flow_history']
    assert a['final_state']['capacity']['social_support']!=b['final_state']['capacity']['social_support']


def test_legacy_internal_rng_outputs_are_recorded_and_replayable(runs):
    for r in runs.values():
        assert all(t['rng_outputs'] for t in r['ticks'])
        assert any(x['operation']!='Random' for t in r['ticks'] for x in t['rng_outputs'])


def test_removing_required_canon_refuses_later_processing_and_feedback(runs):
    f=frame_from(runs['ROUTINE']);ledger=CanonLedger();e=ledger.admit(f,propose_realization(f));ledger._entries=[]
    with pytest.raises(ValueError,match='CANON_REF_MISSING'):ledger.later_consume(e['id'])


def test_native_request_is_executable_blocked_owner_without_legacy_fallback():
    from unittest.mock import patch
    from recursive_court import request_native_trajectory
    with patch('recursive_court.run_one_year',side_effect=AssertionError('native fallback attempted')):
        report=request_native_trajectory()
    assert report['status']=='BLOCKED_OWNER' and not report['executed'] and not report['legacy_fallback']
    assert report['missing'] and report['semantic_contracts_may_exist']
