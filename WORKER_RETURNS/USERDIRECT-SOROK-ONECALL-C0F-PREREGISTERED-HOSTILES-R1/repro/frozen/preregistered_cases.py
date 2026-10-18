"""Phase-A precommitted inputs/claims. Standalone fixture constructors, NO C0 imports."""
from __future__ import annotations
import copy
import json


def e(id, at, kind='ACTIVITY', **kw):
    return {**dict(id=id, at=at, kind=kind, actor_owner='MOCK_OWNER_TEST_ONLY',
                world_owner='MOCK_WORLD_TEST_ONLY'), **kw}


def p(candidates=(), retro=None, **kw):
    return {**dict(now=0, horizon=365, output={'retrospective':retro or {},
                  'prospective':{'candidates':list(candidates)}}), **kw}


def expectation(dispositions=None, admitted=(), render=(), **extra):
    return dict(dispositions=dispositions or {}, admitted_ids=list(admitted),
                render_refusals=list(render), **extra)


CASES = []
def add(id, family, packet, expected, why):
    CASES.append(dict(id=id, family=family, input=packet, expected=expected,
                      scientific_grain='PURE_TEST_ONLY_OWNER_BOUNDARY', rationale=why))

add('A01', 'retro_to_future_invention',
    p([e('meet_fiction_teacher', 70, 'MEET', requires_refs=['invented_teacher'])],
      retro={'surface_inventions_only':['invented_teacher']}),
    expectation({'meet_fiction_teacher':'REFUSE_UNGROUNDED_PREREQUISITE'}),
    'Render-only teacher not constructed as real other person')
add('A02','invented_emotional_history',
    p([], retro={'surface_inventions_only':['imagined_betrayal'],
                 'durable_psyche_patch':{'resentment':100}}),
    expectation(render=['REJECT_RENDER_TO_ACTOR_EFFECT'], psyche={}),
    'No retrospective invented feeling becomes a durable CAN008 change')
add('A03','future_to_past_leakage',
    p([e('future_project', 90)],retro={'asserted_fact_refs':['future_project']}),
    expectation({'future_project':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['future_project'],
                ['REJECT_UNCOMMITTED_RETRO_FACT:future_project']),
    'Proposed future cannot corroborate prior rendered past')
add('A04','post_move_revalidation',
    p([e('relocate', 20,'MOVE',destination='NEW_TOWN'),
       e('old_school_friend',45,'MEET',requires_location='OLD_TOWN')]),
    expectation({'relocate':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'old_school_friend':'INVALIDATED_CURRENT_CONTEXT'},['relocate'],material_location='NEW_TOWN'),
    'Move changes later feasible events; no forced encounter')
add('A05','other_person_refusal',
    p([e('requested_meet',70,'MEET',requires_other_consent=True,other_response='REFUSE')]),
    expectation({'requested_meet':'REFUSE_INDEPENDENT_OTHER_PERSON'}),
    'Child cannot command counterpart consent')
add('A06','objective_occurrence_without_exposure',
    p([e('parent_statement',40,'SPEECH',exposed_to_child=False)]),
    expectation({'parent_statement':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['parent_statement'],actor_knowledge=[]),
    'Speaker performed action does not make child hear it')
add('A07','missing_actor_owner',
    p([dict(e('ruleless',30),actor_owner=None)]),
    expectation({'ruleless':'DEFER_MISSING_OWNER_AUTHORITY'}),
    'Missing psychological/actor owner is not a guessed effect')
add('A08','three_events_in_one_year',
    p([e('habit_1',30,'PRACTICE',practice_owner_rule='MOCK_PRACTICE_UPTAKE'),
       e('qualified_activity',120,'ACTIVITY',requires_capacity=1),
       e('routine_walk',200,'ACTIVITY')]),
    expectation({'habit_1':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'qualified_activity':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'routine_walk':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},
                ['habit_1','qualified_activity','routine_walk'],material_capacity=1),
    'Event-time loop reads capacity after governed prior event')
add('A09','practice_without_uptake_authority',
    p([e('habit_observed',30,'PRACTICE'),
       e('advanced_class',120,'ACTIVITY',requires_capacity=1)]),
    expectation({'habit_observed':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'advanced_class':'DEFER_UNISSUED_CAPACITY_OR_LEARNING'},['habit_observed'],material_capacity=0),
    'Physical practice alone cannot issue acquired skill rule')
add('A10','zero_events_no_fallback',
    p([e('low_score',30,score=-10),e('outside',50,requires_location='MOON')]),
    expectation({'low_score':'REFUSE_SCORE_INVALID_NO_RNG_OVERRIDE',
                 'outside':'INVALIDATED_CURRENT_CONTEXT'},[],slow_time=365),
    'All refused remains lawful valid-empty, no event-count floor')
add('A11','immutable_prior_event',
    p([e('already_done',180)],ledger=[{'id':'already_done','at':-20,'kind':'ACTIVITY','committed':True}]),
    expectation({'already_done':'REFUSE_EVENT_ID_REWRITE'},[],history_ids=['already_done']),
    'Cannot rewrite immutable committed prior occurrence')
add('A12','narrative_only_variant',
    p([e('visit_library',80)],retro={'text_or_scene_fragments':['The library smelled of dust']}),
    expectation({'visit_library':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['visit_library']),
    'Changing expression text cannot cause development')
add('A13','model_score_vs_randomness',
    p([e('forbidden_for_plot',20,score=-1,rng_draw=0.999)]),
    expectation({'forbidden_for_plot':'REFUSE_SCORE_INVALID_NO_RNG_OVERRIDE'}),
    'Randomness never rescues failed owner admission')
add('A14','admission_cold_replay',
    p([e('walk_1',10),e('walk_2',40),e('walk_3',100)]),
    expectation({'walk_1':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE','walk_2':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'walk_3':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['walk_1','walk_2','walk_3']),
    'Canonical ledger identical across fresh processes')
add('A15','uncommitted_action_in_render',
    p([],retro={'asserted_fact_refs':['prose_only_dispute']}),
    expectation(render=['REJECT_UNCOMMITTED_RETRO_FACT:prose_only_dispute']),
    'Surface narrative cannot attest objective witnessed action')
add('A16','subannual_horizon_boundary',
    p([e('spring_event',120)],horizon=90),
    expectation({'spring_event':'REFUSE_CLOCK_OUTSIDE_NEXT_INTERVAL'},[],slow_time=90),
    'Quarterly horizon does not admit events from later year parts')
add('A17','source_permission_absent',
    p([e('unknown_source_right',20,source_permission='MISSING')]),
    expectation({'unknown_source_right':'DEFER_MISSING_RULE_OR_SOURCE_PERMISSION'}),
    'No original/source grant fabricated')
add('A18','forged_external_issuer',
    p([e('fake_certificate',20,external_issuer='FORGED')]),
    expectation({'fake_certificate':'REFUSE_FORGED_OR_FOREIGN_OWNER'}),
    'LLM cannot self-issue external occurrence authority')
add('A19','candidate_generated_CAN011_update',
    p([e('claimed_therapy',45,psyche_patch={'healed':True},effect_type='CAN011_UPDATE')]),
    expectation({'claimed_therapy':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['claimed_therapy'],psyche={}),
    'Accepted activity does not authorize supplied durable effect')
add('A20','valid_empty_no_proposals',
    p([],psyche={'existing_orientation':'AMBIVALENT'}),
    expectation(psyche={'existing_orientation':'AMBIVALENT'},slow_time=365),
    'No candidate is a valid interval, background clock may advance')
add('A21','witnessed_does_not_mean_believed',
    p([e('heard_speech',40,'SPEECH',exposed_to_child=True,
         possible_relevance_domains=['trust','fear'],psyche_patch={'belief':'speaker_right'})]),
    expectation({'heard_speech':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['heard_speech'],
                actor_knowledge=['heard_speech'],psyche={}),
    'Exposure only supports accessible observation, not uptake/affect')
add('A22','future_new_entity_without_constructor',
    p([e('meet_new_mentor',70,'MEET',requires_refs=['mentor_not_constructed'])]),
    expectation({'meet_new_mentor':'REFUSE_UNGROUNDED_PREREQUISITE'}),
    'Proposed unknown person needs a distinct issuer/constructor')
add('A23','past_clock_proposal',
    p([e('yesterday_event',80)],now=100,horizon=365),
    expectation({'yesterday_event':'REFUSE_CLOCK_OUTSIDE_NEXT_INTERVAL'}),
    'Cannot insert retrospective event in next interval packet')
add('A24','context_switch_revalidation_multi',
    p([e('early_project',30),e('relocate_again',45,'MOVE',destination='WEST'),
       e('invalidated_meet',48,'MEET',requires_location='OLD_TOWN'),e('valid_new_school',110,'ACTIVITY',requires_location='WEST')]),
    expectation({'early_project':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE','relocate_again':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE',
                 'invalidated_meet':'INVALIDATED_CURRENT_CONTEXT','valid_new_school':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},
                ['early_project','relocate_again','valid_new_school'],material_location='WEST'),
    'Timeline retains pre-move event while correctly rejecting one later proposal')
add('A25','contested_other_wishes_no_mindread',
    p([e('date_request',45,'MEET',requires_other_consent=True,other_response='UNKNOWN',
         possible_relevance_domains=['romance','recognition'])]),
    expectation({'date_request':'REFUSE_INDEPENDENT_OTHER_PERSON'}),
    'Desired contact plus narrative emotion cannot fill counterpart consent')
add('A26','horizon_rule_missing',
    p([e('proposed_job',30,rule='MISSING')]),
    expectation({'proposed_job':'DEFER_MISSING_RULE_OR_SOURCE_PERMISSION'}),
    'Scientific effect/admission rule missing must not default green')
add('A27','strict_owner_grade_foreign',
    p([dict(e('third_party',70), actor_owner='LLM_ASSERTED')]),
    expectation({'third_party':'REFUSE_FORGED_OR_FOREIGN_OWNER'}),
    'Model claim not equivalent to independent event owner')
add('A28','same_time_separate_events',
    p([e('b',50),e('a',50)]),
    expectation({'a':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE','b':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['a','b']),
    'Stable same-time nonsemantic tie-break only in explicit independent mock')
add('A29','two_call_identical_logical_packet',
    p([e('one_friend',80,'MEET',requires_other_consent=True,other_response='CONSENT')],arm='TWO_CALL'),
    expectation({'one_friend':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['one_friend'],physical_mock_calls=2),
    'Two-call baseline shares exactly identical adjudication when packet content is pinned')
add('A30','fixed_packet_no_provider',
    p([e('small_help',90)],arm='FIXED_PACKET'),
    expectation({'small_help':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['small_help'],physical_mock_calls=0),
    'Fixed-packet arm exercises owner rules without a physical LLM')
add('A31','first_interval_no_retrospective_fact',
    p([e('start_school',40)],retro={'asserted_fact_refs':['never_prior']}),
    expectation({'start_school':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['start_school'],
                ['REJECT_UNCOMMITTED_RETRO_FACT:never_prior']),
    'At genesis there is no previous interval to narrate')
add('A32','person_demographics_do_not_derive_person_effect',
    p([e('ordinary_shopping',50)],demographics={'country':'TST','class':'worker','age':12},
      psyche={'prior':'contradictory'},capacity=0),
    expectation({'ordinary_shopping':'ADMITTED_MOCK_EXTERNAL_OCCURRENCE'},['ordinary_shopping'],
                psyche={'prior':'contradictory'}),
    'Statistical cohort never assigns interior life')


def document():
    return {'schema':'ONECALL_C0F_PHASE_A_FROZEN_CASES@1','phase':'BLIND_PREREGISTRATION',
            'test_count':len(CASES), 'cases':CASES,
            'not_used_for_generation':True,
            'permission':'BOUNDED_SOURCEFREE_MOCK_ONLY_NO_CAN_ADP_WORLD_RIGHTS'}

if __name__ == '__main__':
    print(json.dumps(document(),indent=2,ensure_ascii=False))
