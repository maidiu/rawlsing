import copy
from xsp_world_pair_court import decide, load_precommit, world_from, run

P = load_precommit()

def case(idx):
    pair=P['pairs'][idx]
    return decide(pair['base']), decide(world_from(pair['base'],pair['contrast']))

def test_precommit_is_usable():
    assert len(P['pairs'])==3 and len(P['negative_controls'])==2

def test_p1_historical_publication_is_held_before_known():
    a,b=case(0)
    assert a['state']=='HELD_NOT_KNOWN_ASOF' and b['state']=='TEST_ONLY_CONDITIONED'

def test_p1_no_imputed_private_actor_knowledge():
    a,b=case(0)
    assert a['person_fact'] is None and b['person_fact'] is None

def test_p2_formal_access_changes():
    a,b=case(1)
    assert a['routes']['formal_schooling']=='ELIGIBLE_IN_MODELED_CONTEXT'
    assert b['routes']['formal_schooling']=='BLOCKED_BY_MODELED_FEE_RULE'

def test_p2_care_time_changes_nonformal_and_apprenticeship():
    a,b=case(1)
    for k in ('nonformal_peer_study','paid_apprenticeship'):
        assert a['routes'][k]!=b['routes'][k]

def test_p2_mutual_aid_and_family_care_semantics_remain():
    a,b=case(1)
    for k in ('mutual_aid_participation','family_care_work'):
        assert a['routes'][k]==b['routes'][k]

def test_p2_no_unearned_empirical_probability_change():
    a,b=case(1)
    assert a['empirical']==b['empirical'] and a['route_probabilities'] is None and b['route_probabilities'] is None

def test_p3_minorities_change_without_disappearing():
    a,b=case(2)
    assert a['empirical']['no']==[1,10] and b['empirical']['no']==[1,6]
    assert a['empirical']['yes']==[9,10] and b['empirical']['yes']==[5,6]

def test_p3_world_routes_are_unchanged():
    a,b=case(2)
    assert a['routes']==b['routes']

def test_deny_parent_dyad_inference():
    assert decide(P['pairs'][2]['base'],'PARENT_DYAD_PROBABILITY')['state']=='REFUSE_SAMPLING_UNIT_AUTHORITY'

def test_deny_biography():
    assert decide(P['pairs'][2]['base'],'GENERATED_PERSON_BIOGRAPHY')['state']=='REFUSE_ACTOR_AUTHORITY'

def test_deny_operational_source_claim():
    assert decide(P['pairs'][2]['base'],'OPERATIVE_ORIGINAL_WORLD')['state']=='REFUSE_UNISSUED_SOURCE_AND_N9'

def test_label_only_is_invariant():
    w=P['pairs'][1]['base'];assert decide(w)==decide(world_from(w,{'label':'renamed town'}))

def test_unrelated_ghana_aggregate_is_invariant():
    w=P['pairs'][1]['base'];assert decide(w)==decide(world_from(w,{'ghana_subscription_aggregate':1}))

def test_ghana_subscriptions_never_in_person_probability():
    w=P['pairs'][1]['base'];out=decide(w);assert 'ghana' not in str(out).lower() and out['person_fact'] is None

def test_invalid_denominator_is_typed_refusal():
    w=copy.deepcopy(P['pairs'][1]['base']);w['empirical']['denominator']=100
    assert decide(w)['state']=='REFUSE_INVALID_NATIVE_GEOMETRY'

def test_unknown_world_permission_is_refusal():
    w=copy.deepcopy(P['pairs'][1]['base']);w['world_read']=False
    assert decide(w)['state']=='REFUSE_WORLD_READ'

def test_identity_replay_is_stable():
    x=run();y=run();assert x==y and len(x['outcomes'])==5

def test_no_native_or_actor_execution_claims():
    x=run();assert [x[k] for k in ('native_pyat_calls','native_sorok_calls','original_survey_reads','actor_or_model_calls')]==[0]*4
