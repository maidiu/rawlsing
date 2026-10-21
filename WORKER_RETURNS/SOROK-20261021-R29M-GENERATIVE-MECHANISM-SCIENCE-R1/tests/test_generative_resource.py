import copy
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'source'))

import pytest
from generative_resource import (CASE, GRADE, candidate_resource,
                                  observation, evaluate, sha)

A = 'TEST_ONLY_SYNTH_A'
B = 'TEST_ONLY_SYNTH_B'
R = candidate_resource()


def e(kind, subject, n, when, performed=True, **props):
    return observation(kind, subject, 'TEST_ONLY_OWNER_' + n, when,
                       ref='TEST_ONLY_EVENT_' + n, performed=performed, **props)


def case(share=True, history=True, e2=True, contrary=False, starting_tools=0):
    events = [e('WORLD', A, 'world', 1, tools_for_a=starting_tools)]
    if history:
        events.append(e('A_PAST_ENACTED', A, 'earlier', 2, operation='INSPECT_WITH_TOOL'))
    if share:
        events.append(e('OTHER_PERFORMED', B, 'share', 5, operation='SHARE_TOOL', to_actor=A, quantity=1))
    else:
        events.append(e('OTHER_PERFORMED', B, 'refusal', 5, operation='REFUSE_TOOL', to_actor=A, quantity=0))
    events.append(e('E1_EVENT', A, 'e1', 6))
    if contrary:
        events.append(e('A_CONTRARY_PROJECT', A, 'contrary', 7, operation='INCOMPATIBLE_COMMITMENT'))
    if e2:
        events.append(e('A_E2_PERFORMED', A, 'e2', 9, operation='INSPECT_WITH_TOOL'))
    return dict(schema=CASE, case_id='TEST_ONLY_R29M_CASE', actor=A, other=B,
                as_of=10, social_role='repair_worker', demographic_label='CLASS_A',
                records=events)


def run(c):
    return evaluate(c, R)


def named_consumer_assertion(c):
    # Same result assertion; no exception from builder is counted as a behavioral result.
    o = run(c)
    return (o['material_feasible_after'] is True and
            o['world_effect'] == 'INSPECTION_OCCURRED' and
            o['actor_e2_performed'] is True)


def test_schema_nonissuing_separate_a_t():
    assert R['schema'] == 'GENERATIVE_SCIENCE_RESOURCE_CANDIDATE@1'
    assert R['legal_issuance'] is False
    assert R['native_grant'] is None and R['source_grant'] is None
    assert R['production_registries'] == {'CAN008': [], 'CAN011': []}
    assert R['candidate_rule_a']['owner'] != R['candidate_rule_t']['owner']
    assert R['candidate_rule_t']['operation'] == 'NO_CHANGE'
    assert R['candidate_rule_t']['response_rule_content_hash'] == R['candidate_rule_a_hash']


def test_b_performed_changes_feasible_options_without_psyche():
    positive = run(case())
    refused = run(case(share=False, e2=False))
    assert positive['status'] == 'OPPORTUNITY_CHANGED_BY_INDEPENDENT_B'
    assert positive['material_feasible_before'] is False
    assert positive['material_feasible_after'] is True
    assert refused['material_feasible_after'] is False
    assert positive['psyche_delta'] == refused['psyche_delta'] == {}
    assert positive['v3ms_created'] == refused['v3ms_created'] == 0


def test_a_act_produces_world_effect_but_no_trait():
    x = run(case())
    assert x['actor_e2_performed'] is True
    assert x['world_effect'] == 'INSPECTION_OCCURRED'
    assert x['rule_t_result'] == 'NO_CHANGE' and x['rule_t_grant'] is None
    assert x['native_rules_issued'] is False


def test_b_gives_option_but_cannot_author_a_act():
    x = run(case(e2=False))
    assert x['material_feasible_after'] is True
    assert x['world_effect'] == 'NO_CHANGE' and x['actor_e2_performed'] is False


def test_past_act_removal_loses_h1_evidence_no_acquisition():
    x = run(case(history=True))
    y = run(case(history=False))
    assert x['hypotheses']['H1'] == 'PAST_ACTION_PRESENT_NO_ACQUISITION_LAW'
    assert y['hypotheses']['H1'] == 'PAST_ACTION_ABSENT'
    assert x['rule_t_result'] == y['rule_t_result'] == 'NO_CHANGE'
    assert x['v3ms_created'] == y['v3ms_created'] == 0


def test_contradictory_project_yields_uncertain_not_repaired_automatically():
    x = run(case(contrary=True, e2=False))
    assert x['status'] == 'UNCERTAIN_CONTRADICTORY_PROJECTS'
    assert x['hypotheses']['H3'] == 'CONTRARY_PROJECT_PRESENT_NOT_RESOLVED'
    assert x['world_effect'] == 'NO_CHANGE' and x['psyche_delta'] == {}


def test_contradictory_project_coexists_with_enacted_action():
    x = run(case(contrary=True))
    assert x['world_effect'] == 'INSPECTION_OCCURRED'
    assert x['hypotheses']['H3'] == 'CONTRARY_PROJECT_PRESENT_NOT_RESOLVED'
    assert x['rule_t_result'] == 'NO_CHANGE'


def test_class_role_type_label_cannot_create_person_state():
    c = case()
    baseline = run(c)
    for label in ['CLASS_B', 'STEREOTYPE_2', 'ENNEAGRAM_4', 'UNKNOWN']:
        other = copy.deepcopy(c)
        other['demographic_label'] = label
        other['social_role'] = 'other_job'
        assert run(other) == baseline


def test_no_b_share_breaks_same_named_actor_outcome():
    good = case()
    bad = case(share=False)
    assert named_consumer_assertion(good) is True
    assert named_consumer_assertion(bad) is False
    assert run(bad)['status'] == 'DENY_ACTION_WITHOUT_MATERIAL'


def test_b_source_cut_breaks_same_named_actor_outcome():
    good = case()
    bad = copy.deepcopy(good)
    bad['records'] = [x for x in bad['records'] if x['kind'] != 'OTHER_PERFORMED']
    assert named_consumer_assertion(good) is True
    assert named_consumer_assertion(bad) is False
    assert run(bad)['world_effect'] != 'INSPECTION_OCCURRED'


def test_unauthorized_actor_can_never_write_b_act():
    c = case()
    c['records'][2]['subject'] = A
    assert run(c)['status'] == 'DENY_SOURCE_INTEGRITY_OWNER_CLOCK'


def test_unexecuted_b_share_leaves_options_unavailable():
    c = case(e2=False)
    b = next(x for x in c['records'] if x['kind'] == 'OTHER_PERFORMED')
    b['performed'] = False
    b['content_hash'] = sha({k:v for k,v in b.items() if k!='content_hash'})
    assert run(c)['material_feasible_after'] is False


def test_event_absent_is_not_knowledge_or_action():
    c = case()
    c['records'] = [x for x in c['records'] if x['kind'] != 'E1_EVENT']
    x = run(c)
    assert x['status'] == 'HOLD_E1_NOT_ADMITTED_TEST_ONLY'
    assert x['world_effect'] == 'NO_CHANGE'


def test_world_absent_fails_closed():
    c = case()
    c['records'] = [x for x in c['records'] if x['kind'] != 'WORLD']
    assert run(c)['status'] == 'HOLD_WORLD_SOURCE_MISSING'


def test_resource_content_tamper_denied():
    bad = copy.deepcopy(R)
    bad['candidate_rule_t']['operation'] = 'CREATE'
    assert evaluate(case(), bad)['status'] == 'DENY_RESOURCE_TAMPER_OR_NATIVE_AUTHORITY'


def test_self_issue_is_denied():
    bad = copy.deepcopy(R)
    bad['native_grant'] = 'FORGED_TEST_SIGNED'
    bad['content_hash'] = sha({k:v for k,v in bad.items() if k!='content_hash'})
    assert evaluate(case(), bad)['status'] == 'DENY_RESOURCE_TAMPER_OR_NATIVE_AUTHORITY'


def test_revoked_resource_denied():
    bad = copy.deepcopy(R)
    bad['revoked'] = True
    bad['content_hash'] = sha({k:v for k,v in bad.items() if k!='content_hash'})
    assert evaluate(case(), bad)['status'] == 'DENY_REVOKED'


def test_expired_asof_denied():
    bad = copy.deepcopy(R)
    bad['expires_at'] = 10
    bad['content_hash'] = sha({k:v for k,v in bad.items() if k!='content_hash'})
    assert evaluate(case(), bad)['status'] == 'DENY_CASE_IDENTITY_OR_TIME'


def test_future_earlier_action_denied():
    c = case()
    one = next(x for x in c['records'] if x['kind'] == 'A_PAST_ENACTED')
    one['at'] = 11
    one['content_hash'] = sha({k:v for k,v in one.items() if k!='content_hash'})
    assert run(c)['status'] == 'DENY_SOURCE_INTEGRITY_OWNER_CLOCK'


def test_backwards_e2_denied():
    c = case()
    one = next(x for x in c['records'] if x['kind'] == 'A_E2_PERFORMED')
    one['at'] = 5
    one['content_hash'] = sha({k:v for k,v in one.items() if k!='content_hash'})
    assert run(c)['status'] == 'DENY_E2_NOT_LATER'


def test_forged_world_resource_denied():
    c = case()
    c['records'][0]['payload']['tools_for_a'] = 2
    assert run(c)['status'] == 'DENY_SOURCE_INTEGRITY_OWNER_CLOCK'


def test_a_without_b_still_can_use_prior_own_tool():
    x = run(case(share=False, starting_tools=1))
    assert x['material_feasible_before'] is True
    assert x['material_feasible_after'] is True
    assert x['world_effect'] == 'INSPECTION_OCCURRED'
    assert x['independent_other_changes_options'] is False


def test_reversal_order_of_records_no_change():
    c = case()
    result = run(c)
    c['records'] = list(reversed(c['records']))
    assert run(c) == result


def test_empty_native_cannot_be_obviated_with_type_prior():
    c = case(share=False, e2=False, history=False)
    c['type'] = 'ENNEAGRAM_8'
    assert run(c)['v3ms_created'] == 0
    assert run(c)['world_effect'] == 'NO_CHANGE'


def test_native_actor_swap_is_denied():
    c = case()
    c['other'] = A
    assert run(c)['status'] == 'DENY_CASE_IDENTITY_OR_TIME'


def test_independent_b_refusal_is_not_a_personality_change():
    x = run(case(share=False,e2=False))
    assert x['hypotheses']['H2'] == 'B_NO_RELEVANT_TRANSFER'
    assert x['psyche_delta'] == {} and x['belief_delta'] == {}


def test_positive_resource_hash_is_stable():
    assert candidate_resource() == R
    assert R['content_hash'] == sha({k:v for k,v in R.items() if k!='content_hash'})


def test_can008_is_not_world_option_issuer_or_actor_uptake():
    x = run(case())
    assert R['candidate_rule_a']['operation'] == 'PERSON_X_E1_RECEIVABILITY_CONDITIONED_BY_EXTERNAL_MATERIAL_OPTION'
    assert x['actor_receivability'].startswith('UNKNOWN_')
    assert x['rule_a_result'].startswith('CANDIDATE_CONDITIONING_EVIDENCE_ONLY')


def test_effect_requires_an_actor_performed_receipt_not_response_text():
    c = case(e2=False)
    c['narrator_says_actor_inspected'] = True
    c['llm_generated_response'] = 'I inspected the tool'
    assert run(c)['world_effect'] == 'NO_CHANGE'