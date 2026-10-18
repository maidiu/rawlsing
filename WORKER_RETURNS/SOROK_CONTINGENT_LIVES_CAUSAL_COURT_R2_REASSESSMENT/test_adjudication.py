"""Observation tests for claim scope; passing does not mean original defects repaired."""
from dataclasses import replace
from unittest.mock import patch
import pytest
from audit_support import m, intervene, rehash, replace_event, ancestors


@pytest.mark.parametrize('event',m.WORK_OUTCOMES)
def test_normal_run_summary_matches_its_recorded_activities(event):
    t=m.simulate(event)
    activities=tuple(t.get(key).fact('action') for key in (
        'child_activity_day4','child_activity_day5','child_later_enacted_response'))
    assert t.actor_actions==activities
    prior=t.get('child_history').fact('practical_bicycle_episodes')
    expected=prior+sum(a in {'PARTICIPATE_JOINT_REPAIR','REHEARSE_BICYCLE_REPAIR'} for a in activities[:2])
    assert t.child_practice_count==expected
    assert t.child_project_after==activities[-1]


def test_summary_forgery_is_a_real_validation_gap_but_not_normal_output():
    t=m.simulate('HOURS_CUT')
    forged=replace(t,child_practice_count=999,actor_actions=('REHEARSE_BICYCLE_REPAIR',))
    assert forged.validate()
    assert forged.content_digest()==t.content_digest()
    assert forged.child_practice_count != t.child_practice_count


def test_missing_required_edge_is_not_rejected_but_changes_complete_trace_identity():
    t=m.simulate('HOURS_CUT')
    response=t.get('father_response')
    edited=replace_event(t,rehash(response,parents=tuple(p for p in response.parents if p!='father_receives_work_news')))
    assert edited.validate()
    assert 'father_receives_work_news' not in ancestors(edited,'father_response')
    assert edited.content_digest()!=t.content_digest()


def test_parent_digest_propagation_is_not_required_for_full_trace_content_binding():
    t=m.simulate('ROUTINE')
    changed=intervene({**m.work_facts('ROUTINE'),'wage_delta':1})
    assert t.get('father_receives_work_news').hash==changed.get('father_receives_work_news').hash
    assert t.get('workplace').hash!=changed.get('workplace').hash
    assert t.content_digest()!=changed.content_digest()
    assert changed.validate()
    # Raw content corruption is rejected without any Merkle propagation rule.
    corrupt=replace_event(t,replace(t.get('workplace'),facts=changed.get('workplace').facts))
    with pytest.raises(AssertionError,match='CONTENT_CHANGED'):
        corrupt.validate()


@pytest.mark.parametrize('event',m.WORK_OUTCOMES)
def test_unmodified_producer_records_the_same_work_facts_it_computes_from(event):
    t=m.simulate(event)
    recorded=dict(t.get('workplace').facts)
    assert recorded==m.work_facts(event)
    expected=m.father_action(recorded,m.FatherHistory(),175,18)
    assert dict(t.get('father_response').facts)==expected


def test_false_producer_receipt_requires_a_privileged_hook_in_this_reproducer():
    original=m.Journal.add
    def lying_logger(j,event_id,day,minute,actor,kind,facts,*args,**kwargs):
        if event_id=='workplace':facts=m.work_facts('ROUTINE')
        return original(j,event_id,day,minute,actor,kind,facts,*args,**kwargs)
    with patch.object(m.Journal,'add',lying_logger):
        trace=m.simulate('HOURS_CUT')
    assert trace.validate()
    assert trace.get('workplace').fact('kind')=='ROUTINE'
    assert trace.get('father_response').fact('cash_after_work')==-50
    assert trace.content_digest()!=m.simulate('HOURS_CUT').content_digest()


def test_negative_neighbor_condition_changes_action_without_any_neighbor_ancestor():
    p=m.WorldParameters(child=m.ChildHistory(bus_route_accessible=False),neighbor=m.NeighborHistory(tool_lending_available=True))
    unavailable=m.simulate('RAISE_WITH_OVERTIME',p)
    available=m.simulate('RAISE_WITH_OVERTIME',replace(p,neighbor=replace(p.neighbor,independently_scheduled_shift_day4=False)))
    assert unavailable.actor_actions[0]=='MISS_TRIP_AND_SEEK_ALTERNATIVE'
    assert available.actor_actions[0]=='ASK_NEIGHBOR_FOR_TOOL'
    assert not any(key.startswith('neighbor') for key in ancestors(unavailable,'child_activity_day4'))
    assert 'neighbor_history' in ancestors(available,'child_activity_day4')


def test_unrelated_neighbor_is_not_read_when_bus_is_available():
    class UnreadableNeighbor:
        def __getattribute__(self,key):
            raise AssertionError('unrelated neighbor read: '+key)
    response=m.father_action(m.work_facts('RAISE_WITH_OVERTIME'),m.FatherHistory(),175,18)
    assert m.child_next_activity(response,m.ChildHistory(),UnreadableNeighbor())=='TAKE_BUS'


def test_available_time_is_a_feasibility_bound_not_time_actually_spent_with_child():
    t=m.simulate('ROUTINE')
    response=dict(t.get('father_response').facts)
    assert response['available_minutes']==35
    # Only opportunity/offer is represented for father. The recorded day4 act
    # is the child's participation, with no separate father attendance event.
    father_events=[e for e in t.events if e.actor=='father']
    assert not any(e.kind=='REPAIR_ATTENDANCE' for e in father_events)
    assert t.get('child_activity_day4').fact('action')=='PARTICIPATE_JOINT_REPAIR'


@pytest.mark.parametrize('wage,overtime,father,child',[
    (-175,0,'DISCUSS_NONPURCHASE_OPTIONS','TAKE_BUS'),
    (-175,32,'DEFER_CONVERSATION','TAKE_BUS'),
    (0,0,'OFFER_JOINT_REPAIR','PARTICIPATE_JOINT_REPAIR'),
    (0,32,'DEFER_CONVERSATION','TAKE_BUS'),
])
def test_pay_and_time_factors_separated_with_all_biographies_fixed(wage,overtime,father,child):
    t=intervene(dict(kind='OPAQUE',wage_delta=wage,required_overtime_min=overtime,job_security_warning=False))
    reference=m.simulate('ROUTINE')
    for key in ('theft','father_history','child_history','neighbor_history'):
        assert t.get(key)==reference.get(key)
    assert t.get('father_response').fact('action')==father
    assert t.actor_actions[0]==child


def test_simulation_reuses_history_without_a_cross_run_person_state():
    p=m.WorldParameters()
    first=m.simulate('ROUTINE',p)
    again=m.simulate('ROUTINE',p)
    assert first.content_digest()==again.content_digest()
    assert first.get('child_history')==again.get('child_history')
    assert p.child.practical_bicycle_episodes==1
    assert first.child_practice_count==3
    # The function returns a trace; the resulting count is not fed into the next
    # run's history. This bounds the implemented recurrence, not a requirement
    # that every prototype already implement the production person.
