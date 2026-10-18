"""Test exact counterfactual intervention, immutability and anti-fakery."""
from dataclasses import asdict,replace
import json
import pytest
from world_intersection import (simulate, paired_counterfactual, output_table, sample_independent_workplace,
    work_facts, WorldParameters,FatherHistory,ChildHistory,NeighborHistory,Journal)


def test_three_scenarios_are_valid_immutable_causal_dags():
    for w in ('HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'):
        assert simulate(w).validate()


def test_theft_and_all_biographies_identical_between_pair():
    t=paired_counterfactual()
    for k in ('father_history','child_history','neighbor_history','theft'):
        assert len({r.get(k).hash for r in t.values()})==1


def test_workplace_happens_before_theft_independently():
    t=simulate('HOURS_CUT')
    assert t.get('workplace').day==t.get('theft').day
    assert t.get('workplace').minute<t.get('theft').minute
    assert 'theft' not in t.get('workplace').parents
    assert t.get('workplace').actor=='employer'


def test_workplace_salaries_are_material_not_disposition_labels():
    for x in ('HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'):
        facts=work_facts(x)
        assert set(facts)=={'kind','wage_delta','required_overtime_min','job_security_warning'}
        assert not any(q in facts for q in ('attachment','insecurity','father_angry','child_belief'))


def test_hold_bike_theft_fixed_change_job_produces_distinct_encounters():
    t=paired_counterfactual()
    assert t['HOURS_CUT'].get('father_response').hash != t['RAISE_WITH_OVERTIME'].get('father_response').hash
    # A changed encounter need not change every subsequent observable action.
    assert t['HOURS_CUT'].get('child_activity_day4').fact('action') == t['RAISE_WITH_OVERTIME'].get('child_activity_day4').fact('action') == 'TAKE_BUS'


def test_same_shock_varies_child_path_given_independent_father_resources():
    params=WorldParameters(father=FatherHistory(cash_buffer=220))
    t=paired_counterfactual(params=params)
    assert t['HOURS_CUT'].get('father_response').fact('action')=='OFFER_JOINT_REPAIR'
    assert t['RAISE_WITH_OVERTIME'].get('father_response').fact('action')=='DEFER_CONVERSATION'
    assert t['HOURS_CUT'].get('child_activity_day4').fact('action')=='PARTICIPATE_JOINT_REPAIR'
    assert t['RAISE_WITH_OVERTIME'].get('child_activity_day4').fact('action')=='TAKE_BUS'
    assert t['HOURS_CUT'].child_practice_count>t['RAISE_WITH_OVERTIME'].child_practice_count

def test_raise_does_not_force_warm_or_supportive_outcome():
    t=simulate('RAISE_WITH_OVERTIME')
    assert t.get('father_response').fact('cash_after_work')>0
    assert t.get('father_response').fact('action')=='DEFER_CONVERSATION'


def test_income_loss_does_not_force_anger_or_child_insecurity():
    t=simulate('HOURS_CUT')
    assert t.get('father_response').fact('cash_after_work')<0
    assert t.get('father_response').fact('action')=='DISCUSS_NONPURCHASE_OPTIONS'
    assert 'child_secure' not in str(t).lower() and 'child_insecure' not in str(t).lower()


def test_sufficient_cash_and_time_without_repair_practice_can_offer_replacement():
    params=WorldParameters(father=FatherHistory(joint_repair_episodes=0))
    assert simulate('ROUTINE',params).get('father_response').fact('action')=='DISCUSS_NONPURCHASE_OPTIONS'


def test_care_history_can_moderate_an_employer_event_without_moral_classifier():
    # Independently acquired father protected-care practice changes action while job remains fixed.
    p=WorldParameters(father=FatherHistory(protected_care_min=24))
    a=simulate('RAISE_WITH_OVERTIME')
    b=simulate('RAISE_WITH_OVERTIME',p)
    assert a.get('workplace').hash==b.get('workplace').hash
    assert a.get('father_response').fact('action')=='DEFER_CONVERSATION'
    assert b.get('father_response').fact('action')=='OFFER_JOINT_REPAIR'
    assert b.get('father_response').fact('overtime_declined_min')==21
    assert b.get('father_response').fact('overtime_worked_min')==11


def test_child_practice_depends_on_enacted_activity_not_work_outcome_string():
    t=simulate('HOURS_CUT')
    n=sum(x in ('PARTICIPATE_JOINT_REPAIR','REHEARSE_BICYCLE_REPAIR')
          for x in t.actor_actions)
    assert t.child_practice_count==1+n


def test_child_prior_skill_changes_future_affordance_not_theft():
    a=simulate('ROUTINE')
    p=WorldParameters(child=ChildHistory(practical_bicycle_episodes=2))
    b=simulate('ROUTINE',p)
    assert a.get('theft').hash==b.get('theft').hash
    assert a.get('father_response').fact('action')==b.get('father_response').fact('action')
    assert b.child_practice_count==a.child_practice_count+1


def test_neighbour_independence_can_be_varied_without_retrocausal_work_shock():
    a=simulate('RAISE_WITH_OVERTIME')
    p=WorldParameters(neighbor=NeighborHistory(independently_scheduled_shift_day4=False))
    b=simulate('RAISE_WITH_OVERTIME',p)
    assert a.get('workplace').hash==b.get('workplace').hash
    assert a.get('theft').hash==b.get('theft').hash
    assert a.get('neighbor_independent_shift').hash!=b.get('neighbor_independent_shift').hash


def test_idempotent_counterfactual_replay():
    assert simulate('HOURS_CUT').content_digest()==simulate('HOURS_CUT').content_digest()


def test_seeded_exogenous_randomness_is_reproducible_and_not_psi_draw():
    assert sample_independent_workplace(12345)==sample_independent_workplace(12345)
    assert {sample_independent_workplace(i) for i in range(30)}=={'HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'}


def test_no_calibrated_probabilities_or_disposition_predictions():
    table=output_table()
    assert all(x['inferred_psychological_disposition'] is None for x in table)
    assert all('trace_sha256' in x for x in table)


def test_journal_rejects_unwitnessed_or_later_parent():
    j=Journal()
    with pytest.raises(ValueError,match='UNWITNESSED_PARENT'):
        j.add('orphan',3,9,'child','RETRO',{},parents=('notyet',))
    j.add('first',3,10,'child','ACTION',{})
    with pytest.raises(ValueError,match='TEMPORAL_LEAKAGE'):
        j.add('retro',3,9,'father','ACTION',{},parents=('first',))


def test_journal_rejects_same_id_second_occurrence():
    j=Journal();j.add('same',1,1,'world','OBSERVED',{})
    with pytest.raises(ValueError,match='EVENT_ID_COLLISION'):
        j.add('same',1,2,'world','CHANGED',{})


def test_later_act_is_not_recorded_as_forced_belief():
    t=simulate('ROUTINE')
    assert t.degree_of_psychological_change is None
    assert t.evidence_grade.startswith('SOURCEFREE_UNCALIBRATED')


def test_more_practice_cannot_be_recorded_without_enacted_rehearsal():
    p=WorldParameters(child=ChildHistory(weekday_practice_slots=0))
    t=simulate('ROUTINE',p)
    assert t.child_practice_count==1
    assert t.get('child_activity_day4').fact('action')=='TAKE_BUS'


def test_observer_cannot_backfill_day4_from_day5():
    t=simulate('ROUTINE')
    v=list(t.events)
    old=next(i for i,e in enumerate(v) if e.id=='child_activity_day4')
    v[old]=replace(v[old],day=6)
    with pytest.raises(AssertionError):
        replace(t,events=tuple(v)).validate()


def test_no_magical_time_from_protected_care_commitment():
    for w in ('HOURS_CUT','RAISE_WITH_OVERTIME','ROUTINE'):
        t=simulate(w,WorldParameters(father=FatherHistory(protected_care_min=24)))
        response=t.get('father_response')
        assert response.fact('overtime_declined_min')+response.fact('overtime_worked_min')==response.fact('assigned_overtime_min')
        assert response.fact('available_minutes')==max(0,35-response.fact('overtime_worked_min'))


def test_unrelated_neighbor_project_not_consulted_by_child():
    t=simulate('RAISE_WITH_OVERTIME')
    assert 'neighbor_independent_shift' not in t.get('child_activity_day4').parents


def test_neighbor_actual_interaction_qualifies_child_causal_readset_when_bus_unavailable():
    p=WorldParameters(child=ChildHistory(bus_route_accessible=False),
                      neighbor=NeighborHistory(independently_scheduled_shift_day4=False,tool_lending_available=True))
    t=simulate('RAISE_WITH_OVERTIME',p)
    assert t.get('child_activity_day4').fact('action')=='ASK_NEIGHBOR_FOR_TOOL'
    assert 'neighbor_tool_response' in t.get('child_activity_day4').parents
    assert t.get('neighbor_tool_response').actor=='neighbor'
