from dataclasses import replace, asdict
import json
import os
import subprocess
import sys
import pytest
from court import model as m, intervene, behavior


@pytest.mark.parametrize('event', m.WORK_OUTCOMES)
def test_relabeling_does_not_change_behavior(event):
    original=m.work_facts(event)
    renamed={**original, 'kind':'OPAQUE_LABEL', 'job_security_warning':not original['job_security_warning']}
    assert behavior(intervene(original)) == behavior(intervene(renamed))


def test_same_label_different_materials_changes_behavior():
    cut={**m.work_facts('HOURS_CUT'), 'kind':'SAME'}
    routine={**m.work_facts('ROUTINE'), 'kind':'SAME'}
    a,b=intervene(cut),intervene(routine)
    assert a.get('father_response').fact('action') != b.get('father_response').fact('action')
    assert a.actor_actions != b.actor_actions
    for key in ('theft','father_history','child_history','neighbor_history'):
        assert a.get(key)==b.get(key)


def test_different_encounters_same_downstream():
    a,b=m.simulate('HOURS_CUT'),m.simulate('RAISE_WITH_OVERTIME')
    assert a.get('father_response').facts != b.get('father_response').facts
    assert a.actor_actions == b.actor_actions


def test_no_change_with_large_reserve_and_protected_time():
    p=m.WorldParameters(father=m.FatherHistory(cash_buffer=400,protected_care_min=35))
    traces=m.paired_counterfactual(params=p)
    assert len({t.actor_actions for t in traces.values()})==1


def test_prior_father_practices_same_event():
    a=m.simulate('ROUTINE')
    b=m.simulate('ROUTINE',m.WorldParameters(father=m.FatherHistory(joint_repair_episodes=0)))
    assert a.get('workplace')==b.get('workplace')
    assert a.get('father_response').fact('action') != b.get('father_response').fact('action')


def test_unrelated_neighbor_changes_neither_child_nor_work():
    a=m.simulate('ROUTINE')
    b=m.simulate('ROUTINE',m.WorldParameters(neighbor=m.NeighborHistory(independent_project='garden',independently_scheduled_shift_day4=False)))
    assert a.get('neighbor_independent_shift') != b.get('neighbor_independent_shift')
    assert behavior(a)==behavior(b)
    assert a.get('workplace')==b.get('workplace')


@pytest.mark.parametrize('minute',[1081,1082,1200])
def test_late_notification_cannot_parent_earlier_response(minute):
    with pytest.raises(ValueError,match='TEMPORAL_LEAKAGE'):
        intervene(m.work_facts('ROUTINE'),notification_minute=minute)


def test_earlier_notification_no_behavior_change():
    assert behavior(intervene(m.work_facts('ROUTINE'),notification_minute=1000))==behavior(m.simulate('ROUTINE'))


def test_competing_overtime_conserves_time_but_not_pay_model():
    t=m.simulate('RAISE_WITH_OVERTIME',m.WorldParameters(father=m.FatherHistory(protected_care_min=24)))
    f=dict(t.get('father_response').facts)
    assert (f['overtime_declined_min'],f['overtime_worked_min'],f['available_minutes'])==(21,11,24)
    assert f['overtime_declined_min']+f['overtime_worked_min']==f['assigned_overtime_min']
    # Observation of a limitation, not endorsement of full-pay retention.
    assert f['cash_after_work']==335


def test_zero_child_slots_blocks_parent_repair_offer_uptake():
    t=m.simulate('ROUTINE',m.WorldParameters(child=m.ChildHistory(weekday_practice_slots=0)))
    assert t.get('father_response').fact('action')=='OFFER_JOINT_REPAIR'
    assert t.child_practice_count==1 and t.actor_actions[0]=='TAKE_BUS'


def test_material_feasibility_boundary():
    p=m.WorldParameters(father=m.FatherHistory(cash_buffer=192))
    q=replace(p,father=replace(p.father,cash_buffer=193))
    assert m.simulate('HOURS_CUT',p).get('father_response').fact('action')=='DISCUSS_NONPURCHASE_OPTIONS'
    assert m.simulate('HOURS_CUT',q).get('father_response').fact('action')=='OFFER_JOINT_REPAIR'


def test_determinism_across_process_hash_seeds():
    code="from court import model as m; print(m.simulate('ROUTINE').content_digest())"
    outputs=[subprocess.check_output([sys.executable,'-c',code],env={**os.environ,'PYTHONHASHSEED':str(s)},text=True).strip() for s in (0,1,314)]
    assert len(set(outputs))==1


def test_seed_sweep_is_only_selection_not_development():
    seen=set()
    for seed in range(100):
        event=m.sample_independent_workplace(seed); seen.add(event)
        assert behavior(m.simulate(event))==behavior(m.simulate(event))
    assert seen==set(m.WORK_OUTCOMES)


def test_source_readset_spy_father_does_not_consume_label():
    class Reads(dict):
        def __getitem__(self,key):
            consumed.add(key); return super().__getitem__(key)
    consumed=set()
    m.father_action(Reads(m.work_facts('HOURS_CUT')),m.FatherHistory(),175,18)
    assert consumed=={'wage_delta','required_overtime_min'}


def test_child_policy_does_not_receive_employer_facts():
    response=m.father_action(m.work_facts('ROUTINE'),m.FatherHistory(),175,18)
    class ActionOnly(dict):
        def __getitem__(self,key):
            assert key=='action';return super().__getitem__(key)
    assert m.child_next_activity(ActionOnly(response),m.ChildHistory(),m.NeighborHistory())=='PARTICIPATE_JOINT_REPAIR'


def test_later_rule_threshold_is_authored_not_necessarily_changed_by_encounter():
    p=m.WorldParameters(child=m.ChildHistory(practical_bicycle_episodes=3))
    ts=m.paired_counterfactual(params=p)
    assert len({t.child_project_after for t in ts.values()})==1
    assert len({t.actor_actions[:2] for t in ts.values()})>1


def test_one_literal_threshold_mutation_changes_later_action_without_history_change():
    from court import threshold_variant
    a=m.simulate('ROUTINE'); b=threshold_variant(4).simulate('ROUTINE')
    assert a.child_practice_count==b.child_practice_count==3
    assert a.actor_actions[:2]==b.actor_actions[:2]
    assert a.child_project_after=='TRY_INDEPENDENT_REPAIR'
    assert b.child_project_after=='ASK_FOR_ASSISTANCE'
    assert a.get('theft').facts==b.get('theft').facts


def test_label_only_policy_mutant_is_killed_by_same_label_material_control():
    from unittest.mock import patch
    original=m.father_action
    canonical=m.work_facts('ROUTINE')
    # A deliberately bad policy maps a label to canonical material facts and
    # ignores the actual wage/overtime values. The hostile control must kill it.
    def label_script(work,history,replacement_cost,repair_cost):
        return original(canonical,history,replacement_cost,repair_cost)
    with patch.object(m,'father_action',label_script):
        with pytest.raises(AssertionError):
            test_same_label_different_materials_changes_behavior()


def test_clamped_encounter_blocks_workplace_effect_on_child():
    from unittest.mock import patch
    fixed=m.father_action(m.work_facts('ROUTINE'),m.FatherHistory(),175,18)
    with patch.object(m,'father_action',return_value=fixed):
        ts=m.paired_counterfactual()
    assert len({t.actor_actions for t in ts.values()})==1
    assert len({t.get('workplace').hash for t in ts.values()})==3
