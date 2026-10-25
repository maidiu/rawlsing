from dataclasses import replace
from sorok_interval_participation_producer_r1 import (WorldRegime, EpochOutcome,
    qualify_epoch, realize_interval, non_event_v3_conditioning, diagnostic_candidate,
    example_inputs)


def base(): return example_inputs()


def test_macro_world_producer_generates_positive_condition():
    r, es=base(); x=realize_interval(r,es)
    assert x['coverage']==((96,108),(108,120))
    assert x['individual_daily_events_invented']==0


def test_exact_life_interval_is_eligible_without_new_daily_events():
    r, es=base(); x=diagnostic_candidate(r,es)
    assert x['interval_qualification']['status']=='QUALIFIED'
    assert x['test_only_formation_candidate']['candidate']=='SCOPED_INTERPRETIVE_ORIENTING'
    assert x['mutated_v3'] is False


def test_four_events_identical_with_unknown_participation():
    r, es=base(); a=diagnostic_candidate(r,es)
    b=diagnostic_candidate(r,tuple(replace(e,world_performance='UNKNOWN') for e in es))
    assert a['test_only_formation_candidate']['candidate'] is not None
    assert b['test_only_formation_candidate']['candidate'] is None
    assert a['test_only_formation_candidate']['consumed_event_ids']==b['test_only_formation_candidate']['consumed_event_ids']


def test_schedule_alone_not_activity():
    r,es=base(); assert realize_interval(r,())['coverage']==()


def test_actual_actor_act_no_world_confirmation_is_unknown():
    r, es=base(); e=replace(es[0], world_performance='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_world_claim_without_actor_act_unproven():
    r,es=base(); e=replace(es[0],actor_conduct='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_coerced_performance_not_mistaken_for_consent():
    r,es=base(); assert qualify_epoch(r,es[0]).status=='REALIZED'
    assert es[0].actor_conduct=='RESISTED_BUT_ACTED'


def test_refused_assignment_and_nonperformance_explicit_negative():
    r,es=base(); e=replace(es[0],actor_conduct='REFUSED',world_performance='NOT_PERFORMED')
    assert qualify_epoch(r,e).status=='NEGATIVE_EXPLICIT'


def test_inconsistent_actor_refusal_and_world_performance_refused():
    r,es=base(); e=replace(es[0],actor_conduct='REFUSED',world_performance='CONFIRMED')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_missing_positive_does_not_create_negative():
    r,es=base(); e=replace(es[0],world_performance='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_valid_negative_source_is_not_positive_participation():
    r,es=base(); alt=tuple(replace(e,world_performance='NOT_PERFORMED') for e in es)
    assert realize_interval(r,alt)['coverage']==()


def test_partial_coverage_keeps_gaps_not_filled():
    r,es=base(); e=replace(es[1],world_performance='UNKNOWN')
    a=diagnostic_candidate(r,(es[0],e))
    assert a['interval_qualification']['status']=='PARTIAL'
    assert a['test_only_formation_candidate']['candidate'] is None


def test_expired_source_becomes_unknown():
    r,es=base(); e=replace(es[0],source_valid_to=100)
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_superseded_source_becomes_unknown():
    r,es=base(); e=replace(es[0],superseded=True)
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_world_owner_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],source_owner='LLM')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_actor_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],actor_id='MOTHER')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_household_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],household_id='HH2')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_scope_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],scope_id='COMPANY')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_outside_regime_is_refusal():
    r,es=base(); e=replace(es[0],start=80)
    assert qualify_epoch(r,e).status=='REFUSED'


def test_missing_actor_world_evidence_is_unknown():
    r,es=base(); e=replace(es[0],world_receipt='')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_schedule_source_rule_required():
    r,es=base(); assert qualify_epoch(replace(r,schedule_ref=''),es[0]).status=='REFUSED'


def test_non_event_conditioning_no_v3_psyche_mutation():
    r,es=base(); p=realize_interval(r,es); c=non_event_v3_conditioning(r,p,r.actor_id,r.end)
    assert c['status']=='CONDITION_AVAILABLE'
    assert c['can011_persistence_emitted'] is False
    assert c['v3_response_emitted'] is False
    assert c['actor_experience_or_belief_inferred'] is False


def test_ingress_actor_scope_firewall():
    r,es=base(); p=realize_interval(r,es)
    assert non_event_v3_conditioning(r,p,'OTHER',r.end)['status']=='REFUSED'


def test_ingress_clock_not_arbitrarily_outside_interval():
    r,es=base(); p=realize_interval(r,es)
    assert non_event_v3_conditioning(r,p,r.actor_id,135)['status']=='REFUSED'


def test_no_double_counting_no_new_realized_event_list():
    r,es=base(); d=diagnostic_candidate(r,es)
    assert d['world_production']['individual_daily_events_invented']==0
    assert len(d['world_production']['epochs'])==2
    assert len(d['test_only_formation_candidate']['consumed_event_ids'])==2


def test_replay_deterministic():
    r,es=base(); assert diagnostic_candidate(r,es)==diagnostic_candidate(r,es)


def test_change_witness_changes_conditioning_not_events():
    r,es=base(); a=diagnostic_candidate(r,es)
    b=diagnostic_candidate(r,(es[0],replace(es[1],world_performance='UNKNOWN')))
    assert a['conditioning']['conditioning_receipt_hash']!=b['conditioning']['conditioning_receipt_hash']
    assert a['test_only_formation_candidate']['consumed_event_ids']==b['test_only_formation_candidate']['consumed_event_ids']


def test_absence_of_regime_assignment_still_not_an_automatic_negative():
    r,es=base(); r=replace(r,assigned=False)
    # sourcefree input can establish performed activity absent duty; assignment not a formation parent by itself
    assert qualify_epoch(r,es[0]).status=='REALIZED'


def test_witness_does_not_cause_durable_effect_without_rule():
    r,es=base(); d=diagnostic_candidate(r,es)
    assert d['test_only_formation_candidate']['persistent_v3_mutation'] is False
    assert d['mutated_v3'] is False


def test_tampered_coverage_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['coverage']=((96,120),)
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'


def test_tampered_world_receipt_hash_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['receipt_hash']='TAMPERED'
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'


def test_tampered_qualifications_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['epochs']=()
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'
