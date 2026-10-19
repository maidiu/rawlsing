"""Prospective requirements deliberately left RED when inherited candidate violates them.

No xfail, changed frozen tests, or repair to make these scientific defects disappear.
"""
from dataclasses import replace
from unittest.mock import patch
import pytest
from court import model as m, intervene, rehash, replace_event


def test_trace_validation_rejects_forged_summary():
    t=m.simulate('HOURS_CUT')
    forged=replace(t,child_practice_count=999,child_project_after='TRY_INDEPENDENT_REPAIR',actor_actions=('REHEARSE_BICYCLE_REPAIR',))
    with pytest.raises((AssertionError,ValueError)):
        forged.validate()


def test_trace_validation_requires_notification_dependency():
    t=m.simulate('HOURS_CUT')
    e=t.get('father_response')
    forged=replace_event(t,rehash(e,parents=tuple(p for p in e.parents if p!='father_receives_work_news')))
    with pytest.raises((AssertionError,ValueError)):
        forged.validate()


def test_descendant_identity_binds_consumed_parent_content():
    a=m.simulate('ROUTINE')
    b=intervene({**m.work_facts('ROUTINE'),'wage_delta':1})
    assert a.get('workplace').hash != b.get('workplace').hash
    assert a.get('father_receives_work_news').hash != b.get('father_receives_work_news').hash


def test_negative_neighbor_availability_has_recorded_causal_dependency():
    p=m.WorldParameters(child=m.ChildHistory(bus_route_accessible=False),neighbor=m.NeighborHistory(tool_lending_available=True))
    a=m.simulate('RAISE_WITH_OVERTIME',p)
    b=m.simulate('RAISE_WITH_OVERTIME',replace(p,neighbor=replace(p.neighbor,independently_scheduled_shift_day4=False)))
    assert a.actor_actions[0]=='MISS_TRIP_AND_SEEK_ALTERNATIVE'
    assert b.actor_actions[0]=='ASK_NEIGHBOR_FOR_TOOL'
    # For a negative availability observation, require a witnessed source just as
    # the positive branch has neighbor_tool_response. Neither is in a's ancestry.
    parents=a.get('child_activity_day4').parents
    assert any(p.startswith('neighbor') for p in parents)


def test_recorded_workplace_facts_are_actual_computation_source():
    original=m.Journal.add
    def add(j,event_id,day,minute,actor,kind,facts,*args,**kwargs):
        if event_id=='workplace': facts=m.work_facts('ROUTINE')
        return original(j,event_id,day,minute,actor,kind,facts,*args,**kwargs)
    with patch.object(m.Journal,'add',add):
        t=m.simulate('HOURS_CUT')
    # Either reject mismatched receipts or compute from their witnessed contents.
    expected=m.father_action(dict(t.get('workplace').facts),m.FatherHistory(),175,18)
    assert dict(t.get('father_response').facts)==expected


def test_repair_requires_a_witnessed_available_bicycle():
    t=m.simulate('ROUTINE')
    assert t.get('theft').fact('object')=='bicycle'
    assert t.actor_actions[0]=='PARTICIPATE_JOINT_REPAIR'
    # No recovered bicycle, spare bicycle or borrowed repair object exists in the
    # frozen world. Reporting joint repair is unsupported without such an event.
    assert any(e.kind in {'BICYCLE_RECOVERED','SPARE_BICYCLE_AVAILABLE','BORROWED_BICYCLE_AVAILABLE'} for e in t.events if (e.day,e.minute)<(4,480))
