"""Author's executable adversarial court; independent I2 review remains external."""
from copy import deepcopy
from dataclasses import asdict, replace
import json
import sqlite3
import pytest
from bfirst import (Event, HistoryEpisode, Participant, Refusal, RESPONSE_RULE, Store,
    TestOnlyCAN011Owner as Owner, UPDATE_RULE, demonstrate, digest, episode, execute,
    initialize, participant, prehistory, propose, sealed)


def setup_store(tmp_path, history=None):
    return Store(tmp_path / 'state.sqlite', initialize(history if history is not None else prehistory()))


def prepared(store, event=None):
    event = store.admit_fixture(event or episode())
    response = propose(store.state(), event)
    permission = Owner.permission(store.state(), response)
    return event, response, permission, Owner([permission['hash']])


def test_00_two_event_positive_disk_reopen_and_journal_control(tmp_path):
    evidence = demonstrate(tmp_path)
    positive, control = evidence['positive'], evidence['journal_only']
    assert positive['first_receipt']['owner_decisions'][0]['decision'] == 'ALLOW'
    assert len(positive['persisted_after_first']['middle']) == 1
    assert control['persisted_after_first']['middle'] == []
    assert positive['second']['practical_activity'] != control['second']['practical_activity']
    assert positive['persisted_after_first']['middle'][0]['middle_state_record_hash'] in positive['second']['recruited']
    assert positive['second']['target_proposals'] == []


@pytest.mark.parametrize('history_outcome,expected', [('recognized_plan','joint_check'), ('imposed_plan','private_check')])
def test_same_event_same_words_contrasting_child_history(tmp_path, history_outcome, expected):
    store = setup_store(tmp_path, prehistory(history_outcome))
    first, receipt = execute(store, episode())
    assert receipt['status'] == 'COMMITTED'
    assert first['uptake'][0]['words'] == 'Let us check what can be secured.'
    second, _ = execute(store, episode(2))
    assert second['practical_activity'] == [expected + ':caretaker']


@pytest.mark.parametrize('outcome,expected', [('tools_available',1), ('deadline_due',0), ('none',0)])
def test_independently_derived_caretaker_activity(tmp_path, outcome, expected):
    store = setup_store(tmp_path)
    other = participant(outcome=outcome)
    assert other.offer() == participant(outcome=outcome).offer()
    _, receipt = execute(store, episode(people=[other]))
    assert receipt['status'] == 'COMMITTED'
    assert len(store.state()['middle']) == expected


def test_peer_independent_history_and_contradictory_streams(tmp_path):
    history = prehistory()
    history.append(HistoryEpisode('peer_task', 'child', 'peer', 'repair_route', 1,
                                 'compare_plans_in_task', 'imposed_plan', 'EXPLICIT', (digest(asdict(history[0])),)))
    store = setup_store(tmp_path, history)
    people = [participant(), participant('peer')]
    first, _ = execute(store, episode(people=people))
    assert len({p['stream'] for p in first['target_proposals']}) == 2
    second, _ = execute(store, episode(2, people=people))
    assert second['practical_activity'] == ['joint_check:caretaker', 'private_check:peer']
    assert len(store.state()['middle']) == 2


def test_peer_response_changes_without_changing_child(tmp_path):
    store = setup_store(tmp_path, prehistory(counterpart='peer'))
    execute(store, episode(people=[participant('peer', 'deadline_due')]))
    assert store.state()['middle'] == []


def test_belief_affect_action_and_inaccessible_origin_separate(tmp_path):
    store = setup_store(tmp_path, prehistory('imposed_plan'))
    epistemic = deepcopy(store.state()['epistemic'])
    first, _ = execute(store, episode())
    assert first['uptake'][0]['affective'] == ['constrained']
    assert first['uptake'][0]['propositional'] == 'UNDECIDED_ATTRIBUTED_ASSERTION'
    assert first['practical_activity'] == ['compare_current_plan:caretaker']
    assert first['actor_surface']['origin_explanation'] == 'NOT_ACCESSIBLE'
    assert store.state()['epistemic'] == epistemic
    assert 'shared_task' in epistemic['inaccessible']


@pytest.mark.parametrize('change', ['other_project', 'other_relation', 'no_history'])
def test_historical_counterfactual_untouched_routes(tmp_path, change):
    history = prehistory(project='other') if change == 'other_project' else prehistory(counterpart='other') if change == 'other_relation' else []
    store = setup_store(tmp_path, history)
    execute(store, episode())
    assert store.state()['middle'] == []
    second, _ = execute(store, episode(2))
    assert second['practical_activity'] == ['inspect_alone:caretaker']


def test_event_label_does_not_determine_psychology(tmp_path):
    store = setup_store(tmp_path)
    execute(store, episode(label='storm_damage'))
    second, _ = execute(store, episode(2))
    assert second['practical_activity'] == ['joint_check:caretaker']


def test_later_relation_and_project_scope(tmp_path):
    store = setup_store(tmp_path)
    execute(store, episode())
    second, _ = execute(store, episode(2, people=[participant('peer')]))
    assert second['practical_activity'] == ['inspect_alone:peer']
    before = deepcopy(store.state()['middle'])
    third, _ = execute(store, episode(3, project='unrelated_project'))
    assert third['status'] == 'RESPONSE_EFFECTS_VALID_EMPTY'
    assert store.state()['middle'] == before


def test_failed_permission_rolls_back_response_not_occurrence(tmp_path):
    store = setup_store(tmp_path)
    event, response, permission, _ = prepared(store)
    before = store.state()
    receipt = store.commit(event, response, Owner(), permission)
    assert receipt['reason'] == 'FOREIGN_OWNER_PERMISSION_DENIED'
    assert receipt['status'] == 'TRANSACTION_ABORTED_ROLLBACK'
    assert store.state() == before
    assert store.db.execute('SELECT count(*) FROM occurrence').fetchone()[0] == 1
    assert store.db.execute('SELECT count(*) FROM joint_receipt').fetchone()[0] == 0


def test_storage_failure_after_real_sql_write_rolls_back_all(tmp_path):
    store = setup_store(tmp_path)
    before = store.state()
    _, receipt = execute(store, episode(), fault='after_checkpoint')
    assert receipt['reason'] == 'INJECTED_STORAGE_FAILURE'
    assert store.state() == before
    store.close()
    reopened = Store(tmp_path / 'state.sqlite')
    assert reopened.state() == before
    assert reopened.db.execute('SELECT count(*) FROM occurrence').fetchone()[0] == 1
    assert reopened.db.execute('SELECT count(*) FROM joint_receipt').fetchone()[0] == 0


@pytest.mark.parametrize('field,value,reason', [
    ('operation', 'WEAKEN', 'INVALID_TARGET'),
    ('state_kind_id', 'WoundVector', 'INVALID_TARGET'),
    ('actor_id', 'stranger', 'TARGET_IDENTITY_INVALID'),
    ('proposed_effective_time', 99, 'TARGET_TIME_INVALID'),
    ('causal_parent_refs', ['stale'], 'STALE_CAUSAL_PARENT'),
    ('proposed_payload_delta_or_replacement', {'mode':'trust'}, 'TARGET_PAYLOAD_DENIED'),
    ('numeric_rule_ref', 'invented', 'NUMERIC_OR_STOCHASTIC_UNBOUND'),
    ('source_update_rule_ref', {}, 'UPDATE_RULE_INTEGRITY'),
])
def test_independent_owner_rejects_forged_proposal_even_with_permission(tmp_path, field, value, reason):
    store = setup_store(tmp_path)
    event, response, _, _ = prepared(store)
    response = deepcopy(response)
    p = dict(response['target_proposals'][0])
    p.pop('hash')
    p[field] = value
    response['target_proposals'] = [sealed(p)]
    response.pop('hash')
    response = sealed(response)
    permission = Owner.permission(store.state(), response)
    owner = Owner([permission['hash']])
    with pytest.raises(Refusal, match=reason):
        owner.validate(store.state(), event, response, permission)
    # Joint layer additionally checks CAN008 candidate integrity.
    assert store.commit(event, response, owner, permission)['reason'] == 'RESPONSE_RULE_DIVERGENCE'
    assert store.state()['middle'] == []


def test_stale_response_after_another_committed_history(tmp_path):
    store = setup_store(tmp_path)
    event, response, permission, owner = prepared(store)
    execute(store, replace(episode(), event_id='other_event'))
    assert store.commit(event, response, owner, permission)['reason'] == 'STALE_RESPONSE'


def test_same_time_conflict_no_lexical_priority(tmp_path):
    store = setup_store(tmp_path)
    execute(store, episode())
    event, response, permission, owner = prepared(store, replace(episode(), event_id='aaa'))
    before = store.state()
    assert store.commit(event, response, owner, permission)['reason'] == 'SAME_TIME_ORDER_UNRESOLVED'
    assert store.state() == before


def test_exact_replay_receipts_and_hashes(tmp_path):
    assert demonstrate(tmp_path / 'run1') == demonstrate(tmp_path / 'run2')


def test_rule_version_divergence(tmp_path):
    store = setup_store(tmp_path)
    event, response, permission, owner = prepared(store)
    changed = deepcopy(response)
    changed['response_rule_ref']['rule_version'] = '2'
    changed.pop('hash')
    changed = sealed(changed)
    assert store.commit(event, changed, owner, permission)['reason'] == 'RESPONSE_RULE_DIVERGENCE'


def test_unadmitted_and_cross_actor_and_capability_fail_closed(tmp_path):
    store = setup_store(tmp_path)
    event, response, permission, owner = prepared(store)
    store.db.execute('DELETE FROM occurrence')
    assert store.commit(event, response, owner, permission)['reason'] == 'EVENT_NOT_ADMITTED'
    with pytest.raises(Refusal, match='ACTOR_MISMATCH'):
        propose(store.state(), sealed(asdict(replace(episode(), actor_id='other'))))
    state = store.state()
    state['capabilities'] = []
    with pytest.raises(Refusal, match='CAPABILITY_UNBOUND'):
        propose(state, event)


def test_empty_and_noop_have_no_filler_target(tmp_path):
    store = setup_store(tmp_path, [])
    event = replace(episode(), offers=())
    response, receipt = execute(store, event)
    assert response['target_proposals'] == [] and response['practical_activity'] == []
    assert receipt['owner_decisions'] == [] and receipt['rng_draws'] == 0
    assert store.state()['middle'] == []


def test_persistence_is_not_reinforcement(tmp_path):
    store = setup_store(tmp_path)
    execute(store, episode())
    before = deepcopy(store.state()['middle'])
    execute(store, replace(episode(2), time=1000))
    assert store.state()['middle'] == before
    assert len(store.state()['transitions']) == 1


def test_tampered_history_and_missing_parent_rejected(tmp_path):
    store = setup_store(tmp_path)
    state = store.state()
    state['history'][0]['outcome'] = 'invented'
    with pytest.raises(Refusal, match='HISTORY_INTEGRITY_FAILURE'):
        propose(state, sealed(asdict(episode())))
    state = store.state()
    state['history'][1] = sealed(dict({k:v for k,v in state['history'][1].items() if k != 'hash'}, parent_refs=['missing']))
    with pytest.raises(Refusal, match='HISTORY_LINEAGE_INVALID'):
        propose(state, sealed(asdict(episode())))


def test_checkpoint_tamper_rejected(tmp_path):
    store = setup_store(tmp_path)
    execute(store, episode())
    state = store.state()
    state['middle'][0]['governed_payload']['mode'] = 'hardness'
    with pytest.raises(Refusal, match='MIDDLE_STATE_INTEGRITY_FAILURE'):
        propose(state, sealed(asdict(episode(2))))


def test_real_json_fixture_roundtrip(tmp_path):
    from pathlib import Path
    fixture = json.loads((Path(__file__).parent / 'scenario.json').read_text())
    history = [HistoryEpisode(**h) for h in fixture['child_history']]
    people = [Participant(p['actor_id'], p['project'], tuple(HistoryEpisode(**h) for h in p['history']))
              for p in fixture['participants']]
    store = setup_store(tmp_path, history)
    response, receipt = execute(store, Event(**fixture['events'][0]))
    assert receipt['status'] == 'COMMITTED'
    assert len(response['target_proposals']) == 1
    assert fixture['grade'] == 'SYNTHETIC_PREHISTORY_FIXTURE'


def test_factually_accepted_statement_can_coexist_with_affective_constraint(tmp_path):
    store = setup_store(tmp_path, prehistory('imposed_plan'))
    event = replace(episode(), offers=(('caretaker', 'locking_reduces_access', 'joint_inventory'),))
    response, _ = execute(store, event)
    assert response['uptake'][0]['words'] in store.state()['epistemic']['beliefs']
    assert response['uptake'][0]['affective'] == ['constrained']
    assert store.state()['middle'][0]['governed_payload']['mode'] == 'private_check'


def test_same_history_multiple_opposed_mediators_coexist(tmp_path):
    history = prehistory()
    history.append(HistoryEpisode('other_plan', 'child', 'caretaker', 'repair_route', 1,
        'compare_plans_in_task', 'imposed_plan', 'EXPLICIT', (digest(asdict(history[0])),)))
    store = setup_store(tmp_path, history)
    execute(store, episode())
    second, _ = execute(store, episode(2))
    assert second['practical_activity'] == ['joint_check:caretaker', 'private_check:caretaker']
    assert len(store.state()['middle']) == 2


def test_parent_time_and_future_conditioning_fail_closed(tmp_path):
    store = setup_store(tmp_path)
    history = prehistory()
    with pytest.raises(Refusal, match='FUTURE_CONDITIONING'):
        propose(initialize([replace(history[0], time=99)]), sealed(asdict(episode())))
    with pytest.raises(Refusal, match='HISTORY_LINEAGE_INVALID'):
        propose(initialize([history[0], replace(history[1], time=0)]), sealed(asdict(episode())))


def test_one_bad_effect_rejects_whole_joint_transaction(tmp_path):
    history = prehistory()
    history.append(HistoryEpisode('peer_task', 'child', 'peer', 'repair_route', 1,
        'compare_plans_in_task', 'recognized_plan', 'EXPLICIT', (digest(asdict(history[0])),)))
    store = setup_store(tmp_path, history)
    event, response, _, _ = prepared(store, episode(people=[participant(), participant('peer')]))
    response = deepcopy(response)
    second = response['target_proposals'][1]
    second.pop('hash')
    second['operation'] = 'UNOWNED'
    response['target_proposals'][1] = sealed(second)
    response.pop('hash')
    response = sealed(response)
    permission = Owner.permission(store.state(), response)
    owner = Owner([permission['hash']])
    with pytest.raises(Refusal, match='INVALID_TARGET'):
        owner.validate(store.state(), event, response, permission)
    before = store.state()
    assert store.commit(event, response, owner, permission)['status'] == 'TRANSACTION_ABORTED_ROLLBACK'
    assert store.state() == before


def test_malformed_response_rolls_back_and_leaves_connection_usable(tmp_path):
    store = setup_store(tmp_path)
    event, _, permission, owner = prepared(store)
    before = store.state()
    result = store.commit(event, sealed({'schema':'malformed'}), owner, permission)
    assert result['reason'] == 'INPUT_SCHEMA_INVALID:KeyError'
    assert result['status'] == 'TRANSACTION_ABORTED_ROLLBACK'
    assert not store.db.in_transaction and store.state() == before
    assert execute(store, episode())[1]['status'] == 'COMMITTED'
