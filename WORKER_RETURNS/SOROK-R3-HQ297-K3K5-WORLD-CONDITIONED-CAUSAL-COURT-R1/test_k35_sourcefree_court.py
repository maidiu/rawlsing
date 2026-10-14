"""Post-freeze checks against the upstream-preregistered K3/K5 lab predicates."""
import dataclasses
import pytest
from k35_sourcefree_court import (GRAIN, AccessLeakBlocked, Fixture, all_predeclared_arms,
    evaluate, typed_projection, visible_projection, request_hidden_origin_claim)

@pytest.mark.parametrize('model', ['B0','B1'])
@pytest.mark.parametrize('key,expected', [
 ('K3_A_TRACE', ('ADP016_TRACE_T7','BUFFER','DENY_FIRST_PERSON_CLAIM')),
 ('K3_B_NO_TRACE', ('NONE','RESPONSE_EFFECTS_VALID_EMPTY','DENY_FIRST_PERSON_CLAIM')),
 ('K3_C_UNAVAILABLE_NO_TRACE', ('NONE','RESPONSE_EFFECTS_VALID_EMPTY','DENY_FIRST_PERSON_CLAIM')),
])
def test_k3_independent_expected(key,expected,model):
    r=evaluate(all_predeclared_arms()[key],model)
    assert (r['trace_recruitment'],r['effect'],r['claim']) == expected
    assert r['world_effect_is_committed'] is False

@pytest.mark.parametrize('model', ['B0','B1'])
@pytest.mark.parametrize('key,expected', [
 ('K5_A_OFFICIAL_UNSAFE',('PRESENT','OFFICIAL_RECOGNITION','DEFLECT')),
 ('K5_B_PEER_TRUSTED',('ABSENT','NO_INSTITUTIONAL_CHANGE','AMPLIFY')),
 ('K5_C_OFFICIAL_TRUSTED',('PRESENT','OFFICIAL_RECOGNITION','REROUTE')),
 ('K5_D_PEER_UNSAFE',('ABSENT','NO_INSTITUTIONAL_CHANGE','DEFLECT')),
])
def test_k5_independent_expected(key,expected,model):
    r=evaluate(all_predeclared_arms()[key],model)
    assert (r['institutional_permission'],r['world_effect'],r['effect']) == expected
    assert r['world_effect_is_committed'] is False

@pytest.mark.parametrize('model', ['B0','B1'])
def test_k3_analyst_only_origin_changes_neither_output_nor_visible_view(model):
    f=all_predeclared_arms()['K3_A_TRACE']
    a,b=evaluate(f,model),evaluate(dataclasses.replace(f,analyst_only_childhood_origin='DIFFERENT_SEALED_HISTORY'),model)
    assert typed_projection(a)==typed_projection(b)
    assert visible_projection(a)==visible_projection(b)
    assert 'sealed_origin_alpha' not in str(visible_projection(a))

@pytest.mark.parametrize('model', ['B0','B1'])
def test_k3_unavailable_childhood_feature_cannot_rehydrate(model):
    f=all_predeclared_arms()['K3_A_TRACE']
    with pytest.raises(AccessLeakBlocked,match='BLOCK_UNAVAILABLE'):
        request_hidden_origin_claim(f)
    assert visible_projection(evaluate(f,model))['childhood_origin_claim'] is None

@pytest.mark.parametrize('model', ['B0','B1'])
def test_k5_world_only_control(model):
    a=all_predeclared_arms()['K5_A_OFFICIAL_UNSAFE']
    yes,no=evaluate(a,model),evaluate(dataclasses.replace(a,world_role='PEER'),model)
    assert yes['world_effect'] == 'OFFICIAL_RECOGNITION'
    assert no['world_effect'] == 'NO_INSTITUTIONAL_CHANGE'
    assert yes['effect']==no['effect']=='DEFLECT'

@pytest.mark.parametrize('model', ['B0','B1'])
def test_k5_actor_history_only_control(model):
    a=all_predeclared_arms()['K5_A_OFFICIAL_UNSAFE']
    no,yes=evaluate(a,model),evaluate(dataclasses.replace(a,history='TRUSTED'),model)
    assert no['world_effect']==yes['world_effect']=='OFFICIAL_RECOGNITION'
    assert no['effect']=='DEFLECT' and yes['effect']=='REROUTE'

@pytest.mark.parametrize('model', ['B0','B1'])
def test_missing_world_owner_grant_does_not_commit_official_grant(model):
    f=dataclasses.replace(all_predeclared_arms()['K5_C_OFFICIAL_TRUSTED'],world_owner_grant=False)
    r=evaluate(f,model)
    assert r['institutional_permission']=='PRESENT'
    assert r['world_effect']=='NO_INSTITUTIONAL_CHANGE'
    assert r['world_effect_is_committed'] is False
    assert r['effect']=='REROUTE'

@pytest.mark.parametrize('model', ['B0','B1'])
def test_unadmitted_events_no_effect(model):
    for case in ['K3_A_TRACE','K5_C_OFFICIAL_TRUSTED']:
        f=dataclasses.replace(all_predeclared_arms()[case],admitted=False)
        r=evaluate(f,model)
        assert r['status']=='BLOCK_UNADMITTED_EVENT'
        assert r['effect']=='RESPONSE_EFFECTS_VALID_EMPTY'
        assert r['world_effect']=='NO_INSTITUTIONAL_CHANGE'

@pytest.mark.parametrize('model', ['B0','B1'])
def test_identical_fixture_replays_exact(model):
    for f in all_predeclared_arms().values():
        assert evaluate(f,model)==evaluate(f,model)

@pytest.mark.parametrize('model', ['B0','B1'])
def test_biography_annotation_is_not_causal_parent(model):
    f=all_predeclared_arms()['K3_A_TRACE']
    a,b=evaluate(f,model),evaluate(dataclasses.replace(f,biography_annotation='LABEL_ONLY_DIFFERENT'),model)
    assert typed_projection(a)==typed_projection(b)

@pytest.mark.parametrize('key', list(all_predeclared_arms()))
def test_b1_no_incremental_heldout_typed_result(key):
    f=all_predeclared_arms()[key]
    assert typed_projection(evaluate(f,'B0'))==typed_projection(evaluate(f,'B1'))


def test_no_actor_positive_authority_claim():
    assert GRAIN == 'ISOLATED_RULE_PROTOTYPE_ONLY__NOT_REAL_CAN008_RUNTIME'
