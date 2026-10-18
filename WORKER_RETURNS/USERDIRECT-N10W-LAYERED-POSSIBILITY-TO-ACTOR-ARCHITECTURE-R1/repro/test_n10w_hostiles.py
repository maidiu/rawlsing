"""T01–T22 sealed-plan negative science/contract probes. All are research-only;
actor-positive/accepted native evidence remains separate NOT_REACHED, never passed.
"""
import pytest
from fractions import Fraction as F
from n10w_reference import *
A=dict(training_access=True,training_fee=2,exit_cost=2,civil_open=True,civil_sanction=False)
B=dict(training_access=False,training_fee=2,exit_cost=8,civil_open=True,civil_sanction=False)

def test_T01_rule_change_without_actor_knowledge():
    x,y=structural(A,5),structural(B,5)
    assert x['institutional_access'] is True and y['institutional_access'] is False
    assert perspective(institutional=x['institutional_access'],practical=x['training_practicable'])['actor_knowledge']==NOT_REACHED

def test_T02_permission_not_affordability():
    rule={**A,'training_fee':7};o=structural(rule,5)
    assert o['institutional_access'] is True and o['budget_affordability'] is False and o['training_practicable'] is False
    # inherited original 'scenario' checks only the first; 'nonparent' checks the last.

def test_T03_exposure_not_from_permission():
    o=structural(A,5)
    assert perspective(institutional=o['institutional_access'],practical=o['training_practicable'])['exposure']==UNKNOWN
    assert perspective(institutional=True,practical=True,witnessed_channel=True)['actor_knowledge']==NOT_REACHED

def test_T04_same_demographics_not_same_history():
    histories=('witnessed_training','witnessed_rejected_attempt')
    assert histories[0]!=histories[1]
    assert all(candidate_actor_transition(actor_ref='one',history_replayed=True,owner_receipt=h)==NOT_REACHED for h in histories)

def test_T05_no_backdated_identity_epoch():
    old=canonical_hash(dict(actor='a',epoch=1,history=['evt1']));new=canonical_hash(dict(actor='a',epoch=2,history=['evt1','evt2']))
    assert old!=new and canonical_hash(dict(actor='a',epoch=1,history=['evt1']))==old
    assert candidate_actor_transition(actor_ref='a',history_replayed=True)==NOT_REACHED

def test_T06_multi_conations_no_scalar_policy():
    state=('care','escape','fear','competence','ambivalence','nonaction')
    assert len(state)==6
    assert audit_joint_probability()['simulation_policy'] is None
    assert candidate_actor_transition(actor_ref='a',history_replayed=True)==NOT_REACHED

def test_T07_illegal_not_physically_impossible():
    rule={**A,'training_access':False};out=structural(rule,5)
    assert out['institutional_access'] is False and out['budget_affordability'] is True
    assert audit_joint_probability()['empirical'] is None

def test_T08_power_resources_independent_from_label():
    one=structural({**A,'training_fee':7},5);two=structural({**A,'training_fee':7},9)
    assert one['institutional_access'] == two['institutional_access'] == True
    assert one['training_practicable'] is False and two['training_practicable'] is True

def test_T09_unknown_minority_not_majority_substitution():
    one=structural({**A,'training_access':UNKNOWN},5)
    assert one['institutional_access']==UNKNOWN and one['training_practicable']==UNKNOWN
    assert partial_bounds(F(1,8),F(1,2))==(F(1,8),F(5,8))

def test_T10_same_words_two_relations_without_issuer():
    for relation in ('mentor','hostile_employer'):
        assert candidate_actor_transition(actor_ref='a',owner_receipt=relation,history_replayed=True)==NOT_REACHED

def test_T11_two_minds_separate_scopes():
    worlds=(dict(actor='a',channel=False),dict(actor='b',channel=True))
    assert worlds[0]['actor']!=worlds[1]['actor']
    assert perspective(institutional=True,practical=True,witnessed_channel=False)['exposure'] is False
    assert perspective(institutional=True,practical=True,witnessed_channel=True)['exposure'] is True
    assert candidate_actor_transition(actor_ref='b',owner_receipt='event')==NOT_REACHED

def test_T12_preconscious_residue_not_provable_from_label():
    assert candidate_actor_transition(actor_ref='a',owner_receipt='claimed_hidden_cause',history_replayed=False)==NOT_REACHED

def test_T13_nonaction_cannot_be_forced_from_feasible():
    assert structural(A,5)['training_practicable'] is True
    assert perspective(institutional=True,practical=True,witnessed_channel=True)['proposed_action']==NOT_REACHED

def test_T14_four_clocks():
    assert select_world(effective='2025-01-01',published='2025-03-01',requested='2025-02-01')==UNKNOWN
    assert select_world(effective='2025-01-01',published='2025-03-01',requested='2025-04-01')['actor_knows']==UNKNOWN
    assert select_world(effective='2025-01-01',published='2025-03-01',requested='2025-04-01',known_at='2025-04-02')['actor_knows'] is False

def test_T15_sim_policy_not_observed_probability():
    out=audit_joint_probability(model_policy='UNVALIDATED_LAW_PROPOSAL')
    assert out['empirical'] is None and out['simulation_policy']['candidate']=='UNISSUED_TEST_ONLY'

def test_T16_denominator_selection_changes_estimand():
    e=F(3,10);x=F(3,6);attempted=F(3,3)
    assert e!=x and x!=attempted
    assert audit_joint_probability(joint_attempted=3,eligible_denominator=10,provenance_granted=False)['empirical'] is None

def test_T17_bounds_not_person_propensity():
    assert partial_bounds(F(1,8),F(1,2))==(F(1,8),F(5,8))
    assert audit_joint_probability()['empirical'] is None

def test_T18_attempt_never_guarantees_external_acceptance():
    assert admitted_consequence(event_receipt='attempt',world_owner_permission=True)==NOT_REACHED
    assert admitted_consequence(event_receipt='attempt',counterpart_receipt='accept',world_owner_permission=False)==NOT_REACHED

def test_T19_replay_never_rewrites_history():
    history=['origin','receipt1'];digest=canonical_hash(history)
    revised=history+['interpretation2'];assert canonical_hash(history)==digest and canonical_hash(revised)!=digest
    assert candidate_actor_transition(actor_ref='a',owner_receipt='r',history_replayed=False)==NOT_REACHED

def test_T20_counterparty_independent_action():
    assert admitted_consequence(event_receipt='actor_attempt',counterpart_receipt=None,world_owner_permission=True)==NOT_REACHED

def test_T21_rule_perturbation_not_person_knowledge():
    a,b=structural(A,5),structural(B,5)
    assert a['institutional_access']!=b['institutional_access']
    assert perspective(institutional=True,practical=True)['actor_knowledge']==NOT_REACHED
    assert audit_joint_probability()['empirical'] is None

def test_T22_baselines_have_distinct_falsifiers():
    # H1: marginals do not identify actor uptake; H2: feasible menu doesn't imply exposure;
    # H3: prose no owner grant; H4: required full causal bridge not present; H5: simulation != data.
    assert audit_joint_probability()['empirical_identification']=='UNIDENTIFIED'
    assert perspective(institutional=True,practical=True)['exposure']==UNKNOWN
    assert candidate_actor_transition(actor_ref='a',owner_receipt='LLM_story',history_replayed=False)==NOT_REACHED
    assert audit_joint_probability(model_policy='hypothesis')['simulation_policy']['candidate']=='UNISSUED_TEST_ONLY'
