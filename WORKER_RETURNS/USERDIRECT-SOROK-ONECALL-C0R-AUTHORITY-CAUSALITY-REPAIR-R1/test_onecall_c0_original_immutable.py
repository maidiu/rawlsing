"""ONECALL-C0 R01–R17: TEST_ONLY real executable sourcefree adversaries.

PASS here means only the named boundary against the authored mock, NOT
native Sorok F1/B3 psychological science or independent I2 acceptance.
"""
from copy import deepcopy
import subprocess
import sys
from pathlib import Path

import pytest
import onecall_c0 as oc


@pytest.fixture(scope='module')
def result():
    return oc.run()


def decisions(r):
    return {d['id']: d for d in r['causal']['decisions']}


def by_id(r, cid):
    return [x for x in r['causal']['final_state']['events'] if x['id'].endswith(':'+cid)]


def by_rejection(r):
    return {x['id']:x for x in r['causal']['proposal_rejections']}


def test_R01_render_only_teacher_not_created(result):
    assert by_rejection(result)['invented_teacher']['reason'] == 'NARRATIVE_INVENTION_IS_NOT_A_PREREQUISITE'
    assert not by_id(result, 'invented_teacher')
    assert all(e['action'] != 'TEACHER_MEETING' for e in result['causal']['final_state']['events'])


def test_R02_render_only_betrayal_no_resenment_or_memory(result):
    assert by_rejection(result)['invented_betrayal']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    state = result['causal']['final_state']['actor']
    assert state['beliefs'] == state['affect'] == 'UNISSUED'
    assert 'render-only:betrayal' not in oc.canonical(result['causal'])


def test_R03_different_render_only_has_same_causal_receipt():
    a, b = oc.run(variant='default'), oc.run(variant='different_literary_style')
    assert a['causal'] == b['causal']
    assert a['boundaries'][1]['render']['narrative_text'] != b['boundaries'][1]['render']['narrative_text']


def test_R04_move_invalidates_friend_in_old_place(result):
    d = decisions(result)
    assert d['move']['status'] == 'ADMITTED_TEST_ONLY'
    assert d['old_friend']['status'] == 'INVALIDATED_MATERIAL_REGION'
    assert d['old_friend']['invalidated_by'] == 'move'
    assert not by_id(result, 'old_friend')
    assert result['causal']['final_state']['world']['region'] == 'new_town'


def test_R05_practice_effect_requires_named_test_owner():
    a = oc.run()
    b = oc.run(rules={'licensed_objective_actions': ['FAMILY_MOVE','PROJECT_TASK','OBSERVED_NEUTRAL','NEW_CLUB']})
    assert decisions(a)['practice']['status'] == 'ADMITTED_TEST_ONLY'
    assert decisions(a)['project']['status'] == 'ADMITTED_TEST_ONLY'
    assert decisions(b)['practice']['status'] == 'DEFERRED_MISSING_OWNER_RULE'
    assert decisions(b)['project']['status'] == 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    assert b['causal']['final_state']['actor']['practiced_tasks'] == 0


def test_R06_empty_interval_is_valid_no_fallback():
    original = oc.fixed_candidates
    try:
        oc.fixed_candidates = lambda _: []
        r = oc.run()
    finally:
        oc.fixed_candidates = original
    assert not r['causal']['final_state']['events']
    assert not r['causal']['decisions']
    assert len(r['causal']['final_state']['slow_ticks']) == 2
    assert r['causal']['final_state']['current_year'] == 2022


def test_R07_separate_parent_histories_not_self_issued_psychology():
    x = oc.initial_state(); y = oc.initial_state()
    x['counterparts']['peer']['independent_history'] = ['rehearsal_reserved']
    y['counterparts']['peer']['independent_history'] = ['rehearsal_cancelled']
    a, b = oc.run(initial=x), oc.run(initial=y)
    assert a['causal']['final_state']['counterparts'] != b['causal']['final_state']['counterparts']
    assert a['causal']['final_state']['actor']['affect'] == b['causal']['final_state']['actor']['affect'] == 'UNISSUED'
    # Full differentiated psychology explicitly NOT tested/issued here.


def test_R08_cosmetic_relevance_label_not_owner_psyche():
    a, b = oc.initial_state(), oc.initial_state()
    p = oc.candidate(2020, 30, 'a', 'OBSERVED_NEUTRAL', domains=['recognized_plan'])
    q = oc.candidate(2020, 30, 'a', 'OBSERVED_NEUTRAL', domains=['unrecognized_plan'])
    rules = {'licensed_objective_actions':['OBSERVED_NEUTRAL']}
    oc.apply_admitted(a, p, 2020, rules)
    oc.apply_admitted(b, q, 2020, rules)
    assert a['actor'] == b['actor']
    assert a['events'][0]['hash'] != b['events'][0]['hash']  # audit label differences remain visible


def test_R09_history_not_demographics_changes_practical_possibility():
    a, b = oc.initial_state(), oc.initial_state()
    b['actor']['practiced_tasks'] = 1
    p = oc.candidate(2020, 100, 'project', 'PROJECT_TASK', min_practice=1)
    r = {'licensed_objective_actions':['PROJECT_TASK']}
    assert a['actor']['demographics'] == b['actor']['demographics']
    assert oc.evaluate(a,p,r) == 'DEFERRED_MISSING_OBSERVED_PRACTICE'
    assert oc.evaluate(b,p,r) == 'ELIGIBLE_TEST_ONLY'
    assert a['actor']['beliefs'] == b['actor']['beliefs'] == 'UNISSUED'


def test_R10_speech_without_exposure_not_known(result):
    assert decisions(result)['speech']['status'] == 'DEFERRED_NO_ACTOR_EXPOSURE'
    assert result['causal']['final_state']['actor']['actor_knowledge'] == []
    assert not by_id(result, 'speech')


def test_R11_independent_counterpart_refusal(result):
    assert decisions(result)['peer_contact']['status'] == 'REFUSED_INDEPENDENT_COUNTERPART'
    assert not by_id(result, 'peer_contact')
    s = oc.initial_state()
    s['counterparts']['peer']['available'] = True
    p = oc.candidate(2020, 250, 'peer_contact', 'COUNTERPART_CONTACT', counterpart='peer')
    assert oc.evaluate(s,p,{'licensed_objective_actions':['COUNTERPART_CONTACT']}) == 'ELIGIBLE_TEST_ONLY'


def test_R12_observed_practice_does_not_erase_conflicting_appraisal(result):
    x = oc.initial_state()
    x['actor']['beliefs'] = 'TEST_ONLY_SELF_REPORT_CONTRADICTS_PRACTICE'
    a = oc.run(initial=x)
    assert a['causal']['final_state']['actor']['practiced_tasks'] == 1
    assert a['causal']['final_state']['actor']['beliefs'] == 'TEST_ONLY_SELF_REPORT_CONTRADICTS_PRACTICE'
    assert all(d.get('psyche_effect_status') == 'VALID_EMPTY__NO_CAN008_CAN011_ADP016_RULE'
               for d in a['causal']['decisions'] if d['status'] == 'ADMITTED_TEST_ONLY')


def test_R13_render_future_proposal_not_backdated(result):
    r = result['boundaries'][1]['render']
    assert oc.fact_id(2021, 'future_unoccurred') in r['future_claims_rejected']
    assert not any(e['id'] == oc.fact_id(2021,'future_unoccurred')
                   for e in result['causal']['final_state']['events'])
    assert all(e['year'] in (2020,2021) for e in result['causal']['final_state']['events'])


def test_R14_source_scope_mismatch_refuses():
    s = oc.initial_state(); inp = oc.render_input(s, 2020)
    r,p = oc.mocked_artifacts(inp)
    p['source_scope_refs'] = ['UNISSUED_ORIGINAL35']
    with pytest.raises(AssertionError,match='source mismatch'):
        oc.validate_packet(p,inp)


def test_R14_unknown_position_refuses():
    inp = oc.render_input(oc.initial_state(), 2020)
    _,p = oc.mocked_artifacts(inp)
    inp['position_ref'] = None
    with pytest.raises(AssertionError,match='position unbound'):
        oc.validate_packet(p,inp)


def test_R14_no_individual_probabilities_created(result):
    assert result['boundaries'][0]['prospective_validation']['no_personal_probability']
    assert 'route_probability' not in oc.canonical(result['causal'])
    assert all(x['sampling_metadata']['probability_grade'] == 'NONE'
               for x in [oc.mocked_artifacts(oc.render_input(oc.initial_state(),2020))[1]])


def test_R15_same_process_replay_exact():
    a,b = oc.run(),oc.run()
    assert a['causal']['receipt_hash'] == b['causal']['receipt_hash']
    assert a['causal']['final_state'] == b['causal']['final_state']


def test_R15_external_distinct_processes():
    script = Path(oc.__file__).resolve()
    x = subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True).stdout
    y = subprocess.run([sys.executable,str(script)],text=True,capture_output=True,check=True).stdout
    assert x == y
    assert '"causal_hash"' in x


def test_R16_model_cannot_apply_CAN011_ADP016(result):
    rejects = by_rejection(result)
    assert rejects['covert_memory']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    assert rejects['invented_betrayal']['reason'] == 'UNISSUED_PSYCHOLOGICAL_EFFECT'
    assert result['causal']['final_state']['actor']['beliefs'] == 'UNISSUED'


def test_R16_top_level_effect_cannot_be_launched():
    inp=oc.render_input(oc.initial_state(),2020)
    _,p=oc.mocked_artifacts(inp)
    p['CAN011_UPDATE']={'memory':'fake'}
    with pytest.raises(AssertionError,match='top-level effect'):
        oc.validate_packet(p,inp)


def test_R17_onecall_contamination_stress_selects_two_call_fallback():
    comparison=oc.mode_comparison('combined_contamination')
    assert comparison['selected_research_fallback']=='TWO_CALL'
    assert comparison['causal_equal'] is False  # audit rejects disclose contamination
    assert any(k=='extra_fabricated_teacher' for k,_ in comparison['rejected']['ONE_CALL'])
    assert not any(k=='extra_fabricated_teacher' for k,_ in comparison['rejected']['TWO_CALL'])


def test_R17_baseline_all_three_logically_equivalent():
    c=oc.mode_comparison()
    assert c['causal_equal']
    assert c['selected_research_fallback']=='ONE_CALL'
    assert c['physical_mock_invocations']=={'ONE_CALL':3,'TWO_CALL':4,'FIXED_PACKET':0}


def test_EXTRA_each_year_and_three_event_opportunities(result):
    assert [b['year'] for b in result['boundaries']] == [2020,2021,2022]
    assert len([d for d in result['causal']['decisions'] if d['year']==2020]) >= 3
    assert len([d for d in result['causal']['decisions'] if d['year']==2021]) >= 3
    assert len(result['causal']['final_state']['events']) >= 3


def test_EXTRA_candidate_unknown_referent_cannot_create_person():
    inp=oc.render_input(oc.initial_state(),2020); _,p=oc.mocked_artifacts(inp)
    p['candidates'].append(oc.candidate(2020,13,'unknown_person','TEACHER_MEETING', prerequisites=['person:invented']))
    _,items=oc.validate_packet(p,inp)
    assert 'unknown_person' not in {x['id'] for x in items}


def test_EXTRA_adaptive_update_legal_vs_position_unknown():
    p=oc.candidate(2020,180,'old_friend','FRIEND_MEETING',required_region='old_town')
    s=oc.initial_state();r={'licensed_objective_actions':['FRIEND_MEETING']}
    assert oc.evaluate(s,p,r)=='ELIGIBLE_TEST_ONLY'
    s['world']['region']='new_town'
    assert oc.evaluate(s,p,r)=='INVALIDATED_MATERIAL_REGION'


def test_EXTRA_no_laundering_back_to_checkpoint(result):
    a=result['boundaries'][1]
    assert a['render']['causal_hash_before']==a['checkpoint_ref']
    assert not any('teacher-nova' in e['id'] or 'betrayal' in e['id']
                   for e in result['causal']['final_state']['events'])
    assert len(result['causal']['final_state']['events'])==6


def test_EXTRA_hidden_future_ignored_by_render():
    inp=oc.render_input(oc.initial_state(),2020)
    render,_=oc.mocked_artifacts(inp)
    render['allowed_fact_refs']=['future:forged']
    with pytest.raises(AssertionError,match='render fact grant forged'):
        oc.validate_render(render,inp)


def test_EXTRA_no_time_retroaction(result):
    records=result['causal']['final_state']['events']
    assert [(r['year'],r['day']) for r in records]==sorted((r['year'],r['day']) for r in records)
    assert all(r['prior_state_hash'] != r['hash'] for r in records)


def test_EXTRA_no_forced_duplicate_or_replacement(result):
    planned=sum(len(oc.fixed_candidates(y)) for y in (2020,2021))
    actual=len(result['causal']['final_state']['events'])
    assert actual < planned
    assert not any(d['id'].endswith('fallback') for d in result['causal']['decisions'])


def test_EXTRA_unauthorized_owner_all_events_defer():
    s=oc.run(rules={'licensed_objective_actions':[]})
    assert not s['causal']['final_state']['events']
    assert all(d['status']!='ADMITTED_TEST_ONLY' for d in s['causal']['decisions'])
    assert s['causal']['final_state']['actor']['practiced_tasks']==0


def test_EXTRA_actor_view_no_render_into_state(result):
    body=oc.canonical(result['causal']['final_state'])
    assert 'teacher-nova' not in body and 'future_unoccurred' not in body
    assert 'text_or_scene_fragments' not in body


def test_EXTRA_proposals_are_audited_independent(result):
    assert all(b['prospective_validation']['proposal_checkpoint']==b['checkpoint_ref'] for b in result['boundaries'])
    assert all(b['render']['causal_hash_before']==b['checkpoint_ref'] for b in result['boundaries'])
    assert result['experiment_grade']==oc.GRADE
