from dataclasses import replace
from sorok_interval_witness_lab import (
    Interval, Episode, Witness, EPISODES, TEST_OWNER, formation_candidate,
    interval_qualification, scenario, counterfactual_report,
)


def witness(**kw):
    return replace(scenario().witness, **kw)


def test_same_four_events_but_different_regime():
    a,b=scenario(True), scenario(False)
    assert a.episodes == b.episodes
    assert formation_candidate(a)['candidate'] is not None
    assert formation_candidate(b)['candidate'] is None


def test_no_owner_psyche_writes():
    assert formation_candidate(scenario())['persistent_v3_mutation'] is False


def test_schedule_not_participation():
    x=replace(scenario(), witness=witness(kind='SCHEDULE_ONLY'))
    assert interval_qualification(x)['status']=='NOT_PROVEN_REALIZED'
    assert formation_candidate(x)['candidate'] is None


def test_obligation_not_participation():
    x=replace(scenario(), witness=witness(kind='OBLIGATION_ONLY'))
    assert formation_candidate(x)['candidate'] is None


def test_no_implicit_negative_from_missing():
    assert interval_qualification(scenario(False))['status']=='UNKNOWN'


def test_negative_requires_explicit_witness():
    x=replace(scenario(), witness=witness(polarity='NEGATIVE'))
    assert interval_qualification(x)['status']=='EXPLICIT_NEGATIVE'


def test_invalid_owner_refused():
    x=replace(scenario(), witness=witness(owner='UNLICENSED_LLM'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_wrong_actor_refused():
    x=replace(scenario(), witness=witness(actor_id='MOTHER'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_expired_witness_unknown_not_negative():
    x=replace(scenario(), witness=witness(valid_until=110))
    assert interval_qualification(x)['status']=='UNKNOWN'


def test_superseded_witness_unknown():
    x=replace(scenario(), witness=witness(status='SUPERSEDED'))
    assert interval_qualification(x)['status']=='UNKNOWN'


def test_gap_in_coverage_is_partial():
    x=replace(scenario(), witness=witness(coverage=((96,106),(110,120))))
    assert interval_qualification(x)['status']=='PARTIAL'


def test_partial_first_year_not_entire_two_years():
    x=replace(scenario(), witness=witness(coverage=((96,108),)))
    assert interval_qualification(x)['status']=='PARTIAL'


def test_overlapping_contiguous_segments_qualify():
    x=replace(scenario(), witness=witness(coverage=((96,110),(108,120))))
    assert interval_qualification(x)['status']=='QUALIFIED'


def test_missing_actor_uptake_no_formation():
    x=replace(scenario(), uptake_refs=())
    assert formation_candidate(x)['candidate'] is None


def test_unreceived_event_no_formation():
    eps=tuple(replace(e,actor_access=False) if e.episode_id=='E2_SCHOOL_CONFLICT' else e for e in EPISODES)
    x=replace(scenario(), episodes=eps)
    assert formation_candidate(x)['candidate'] is None


def test_no_conflict_episode_no_formation():
    x=replace(scenario(),episodes=tuple(e for e in EPISODES if e.episode_id!='E2_SCHOOL_CONFLICT'))
    assert formation_candidate(x)['candidate'] is None


def test_no_count_multiplier_or_event_count_condition():
    r=counterfactual_report()
    assert r['same_episode_count']==4
    assert not r['naive_event_count_baseline']['discriminates']
    assert r['A_recurrence']['verdict']!=r['B_isolated']['verdict']


def test_replay_exact_receipt():
    assert formation_candidate(scenario())==formation_candidate(scenario())


def test_context_change_affects_receipt_not_prior_events():
    x=scenario(); y=replace(x,witness=witness(coverage=((96,110),)))
    assert x.episodes==y.episodes
    assert formation_candidate(x)['receipt_hash']!=formation_candidate(y)['receipt_hash']


def test_no_double_counting():
    r=formation_candidate(scenario())
    assert r['consumed_event_ids']==('E2_SCHOOL_CONFLICT','E4_NEGOTIATION_TRY')
    assert r['source_witness_id']=='W_REAL_CARE_96_120'


def test_current_wrong_scope_fails():
    x=replace(scenario(),witness=witness(scope_id='EMPLOYER'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_no_events_not_fabricated_by_recurrence():
    x=replace(scenario(),episodes=())
    assert interval_qualification(x)['status']=='QUALIFIED'
    assert formation_candidate(x)['candidate'] is None


def test_absent_test_rule_prevents_retroactive_formation():
    x=replace(scenario(),witness=witness(rule_id='UNREGISTERED'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_representative_prose_no_mutation():
    x=replace(scenario(),episodes=(Episode('E1_CARE_AFTERNOON','EPIC_LIFECHANGING_CARE'),)+EPISODES[1:])
    assert formation_candidate(x)['candidate'] is not None
    assert formation_candidate(x)['persistent_v3_mutation'] is False
