from dataclasses import replace
from sorok_macro_period_world_realizer_r1 import (
    MacroActorAct, MacroWorldResponse, realize_period, produce_life
)
from sorok_interval_participation_producer_r1 import (
    example_inputs, realize_interval, diagnostic_candidate
)


def base():
    r,_=example_inputs()
    return r,MacroActorAct('NADIA',96,108,'UNRESOLVED','RESISTED_BUT_ACTED','ACT_1'),MacroWorldResponse('HH1',96,108,'AVAILABLE','ACCOMMODATED','WORLD_1')


def test_actor_proposal_not_enough():
    r,a,w=base(); d=realize_period(r,replace(a,proposal='AGREE',realized_conduct='UNKNOWN'),w)
    assert d['epoch'].world_performance=='UNKNOWN'


def test_performance_generates_positive_epoch_world_fact():
    r,a,w=base(); x=realize_period(r,a,w)
    assert x['epoch'].world_performance=='CONFIRMED'
    assert x['epoch'].actor_conduct=='RESISTED_BUT_ACTED'


def test_declining_participation_yields_negative():
    r,a,w=base(); x=realize_period(r,replace(a,proposal='REFUSE',realized_conduct='REFUSED'),w)
    assert x['epoch'].world_performance=='NOT_PERFORMED'


def test_material_obstacle_yields_nonperformance():
    r,a,w=base(); x=realize_period(r,a,replace(w,material_status='BLOCKED'))
    assert x['epoch'].world_performance=='NOT_PERFORMED'


def test_other_actor_obstruction_yields_nonperformance():
    r,a,w=base(); x=realize_period(r,a,replace(w,counterpart_response='OBSTRUCTED'))
    assert x['epoch'].world_performance=='NOT_PERFORMED'


def test_other_actor_unknown_not_false_confirmation():
    r,a,w=base(); x=realize_period(r,a,replace(w,counterpart_response='UNKNOWN'))
    assert x['epoch'].world_performance=='UNKNOWN'


def test_actor_source_owner_mismatch_refuses():
    r,a,w=base(); assert realize_period(r,replace(a,source_owner='NARRATOR'),w)['status']=='REFUSED'


def test_counterpart_source_owner_mismatch_refuses():
    r,a,w=base(); assert realize_period(r,a,replace(w,source_owner='NARRATOR'))['status']=='REFUSED'


def test_household_mismatch_refuses():
    r,a,w=base(); assert realize_period(r,a,replace(w,household_id='HH2'))['status']=='REFUSED'


def test_actor_mismatch_refuses():
    r,a,w=base(); assert realize_period(r,replace(a,actor_id='OTHER'),w)['status']=='REFUSED'


def test_different_periods_refuse():
    r,a,w=base(); assert realize_period(r,a,replace(w,start=100))['status']=='REFUSED'


def test_missing_actor_performance_source_refuses():
    r,a,w=base(); assert realize_period(r,replace(a,actual_act_ref=''),w)['status']=='REFUSED'


def test_missing_world_source_refuses():
    r,a,w=base(); assert realize_period(r,a,replace(w,actual_world_ref=''))['status']=='REFUSED'


def test_out_of_regime_refuses():
    r,a,w=base(); assert realize_period(r,replace(a,start=80),replace(w,start=80))['status']=='REFUSED'


def test_unknown_actor_kind_refuses():
    r,a,w=base(); assert realize_period(r,replace(a,realized_conduct='IMAGINED'),w)['status']=='REFUSED'


def test_unknown_world_kind_refuses():
    r,a,w=base(); assert realize_period(r,a,replace(w,material_status='HAPPY'))['status']=='REFUSED'


def test_intent_can_differ_without_changing_act():
    r,a,w=base(); first=realize_period(r,a,w); second=realize_period(r,replace(a,proposal='AGREE'),w)
    assert first['epoch']==second['epoch']
    assert first['receipt_hash']!=second['receipt_hash']


def test_complete_two_period_macro_life_yields_condition():
    x=produce_life()
    assert x['formation_diagnostic']['interval_qualification']['status']=='QUALIFIED'
    assert x['formation_diagnostic']['test_only_formation_candidate']['candidate'] is not None
    assert x['formation_diagnostic']['mutated_v3'] is False


def test_no_daily_events_generated_in_macro_life():
    x=produce_life(); assert x['formation_diagnostic']['world_production']['individual_daily_events_invented']==0


def test_two_period_inputs_are_actual_world_producer_outputs():
    x=produce_life()
    assert len(x['periods'])==2
    assert all(z['status']=='DERIVED' and z['world_rule']=='TEST_ONLY_PERIOD_WORLD_EFFECT@1' for z in x['periods'])


def test_macroworld_replay_deterministic():
    assert produce_life()==produce_life()


def test_invalid_world_not_converted_to_positive_formation():
    r,a,w=base(); d=realize_period(r,a,replace(w,material_status='BLOCKED'))
    assert d['epoch'].world_performance!='CONFIRMED'
    assert realize_interval(r,(d['epoch'],))['coverage']==()


def test_coerced_activity_is_not_voluntary_belief():
    x=produce_life()
    assert x['periods'][0]['actor_intent']=='UNRESOLVED'
    assert x['formation_diagnostic']['conditioning']['actor_experience_or_belief_inferred'] is False
