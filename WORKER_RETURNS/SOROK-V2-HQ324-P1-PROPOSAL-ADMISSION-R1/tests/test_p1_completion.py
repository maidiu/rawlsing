"""HQ324 P1 final hostile completion tests, additive; sourcefree test-only."""
import copy
import json
from pathlib import Path

import pytest
from p1_contract import canonical, digest, evaluate, replay_test_only, select_test_only

F = Path(__file__).resolve().parents[1] / 'fixtures'
SEED = '0f' * 32


def load(name):
    return json.loads((F / name).read_text())


def rehash(p):
    p['proposal_hash'] = digest({k: v for k, v in p.items() if k != 'proposal_hash'})
    return p


def refresh(c):
    c['context_hash'] = digest({k: v for k, v in c.items() if k != 'context_hash'})
    return c


def code(e, target='ALT-CARE'):
    return next(x['code'] for x in e['candidates'] if x['candidate_id'] == target)


def test_course_cannot_claim_other_persons_action():
    p = load('packet_base.json')
    p['candidates'][0]['courses'][0]['actor_ref'] = 'CHILD-1'
    r = evaluate(rehash(p), load('context_base.json'))
    assert code(r) == 'CROSS_ACTOR_COURSE_ACTION_FORBIDDEN'


def test_private_state_cannot_be_prerequisite_world_fact():
    p = load('packet_base.json')
    p['candidates'][0]['prerequisites'].append({'kind': 'WORLD_FACT_TRUE', 'ref': 'PRIVATE-CAREGIVER-1'})
    r = evaluate(rehash(p), load('context_base.json'))
    assert code(r) == 'PREREQUISITE_NOT_OBJECTIVE_WORLD_FACT'


def test_caregiver_cannot_recruit_child_history_as_own():
    c = load('context_base.json')
    c['people']['CARE-1']['history_ref'] = 'H-CHILD-1'
    c = refresh(c)
    p = load('packet_base.json')
    p['context_hash'] = c['context_hash']
    p['candidates'][0]['prerequisites'][-1]['ref'] = 'CARE-1|H-CHILD-1'
    result = evaluate(rehash(p), c)
    assert result['decision'] == 'REJECT'
    assert 'CONTEXT_HISTORY_OWNER_MISMATCH' in result['detail']


def test_evaluation_candidate_set_forgery_blocks_selection():
    e = evaluate(load('packet_base.json'), load('context_base.json'))
    assert e['decision'] == 'ADMIT'
    e['eligible_entries'].append({
        'candidate_id': 'FORGED-CAUSAL-CANDIDATE',
        'candidate_replay_hash': '1' * 64,
        'candidate_authority_id': 'P1_CANDIDATE_ELIGIBILITY_TEST_ONLY@1.0.0',
        'candidate_authority_version': '1.0.0',
        'eligibility_or_admission_receipt_hash': '2' * 64,
    })
    import hashlib
    e['candidate_set_hash'] = hashlib.sha256(b'P1_CANDIDATE_SET_V1\0' + canonical(e['eligible_entries'])).hexdigest()
    pol = load('policy_design_weights.json')
    pol['candidate_set_hash'] = e['candidate_set_hash']
    pol['weight_units'] = {'ALT-CARE': 0, 'ALT-CHILD-SEARCH': 0, 'ALT-NONE': 0,
                           'ALT-PEER': 0, 'FORGED-CAUSAL-CANDIDATE': 1}
    pol['policy_hash'] = digest({k: v for k, v in pol.items() if k != 'policy_hash'})
    r = select_test_only(e, pol, seed_hex=SEED, coordinate=0)
    assert r['decision'] == 'REJECT'
    assert r['reason'] == 'EVALUATION_RECEIPT_INTEGRITY_FAILURE'
    assert r['consumption'] is None


def test_replay_does_not_accept_partial_null_hash_receipt():
    e = evaluate(load('packet_valid_empty.json'), load('context_base.json'))
    prior = {'decision': 'REJECT', 'selected_candidate_id': None}
    current = replay_test_only(prior, e, load('policy_design_weights.json'), seed_hex=SEED, coordinate=0)
    assert current['decision'] == 'REJECT'
    assert current['reason'] == 'TEST_ONLY_REPLAY_DIVERGENCE'


def test_replay_of_exact_valid_empty_receipt_is_deterministic():
    e = evaluate(load('packet_valid_empty.json'), load('context_base.json'))
    s = select_test_only(e, load('policy_design_weights.json'), seed_hex=SEED, coordinate=0)
    assert replay_test_only(copy.deepcopy(s), e, load('policy_design_weights.json'),
                            seed_hex=SEED, coordinate=0) == s


def test_nonnumeric_weight_is_refused_not_crash():
    e = evaluate(load('packet_base.json'), load('context_base.json'))
    pol = load('policy_design_weights.json')
    pol['weight_units']['ALT-CARE'] = 'five'
    pol['policy_hash'] = digest({k: v for k, v in pol.items() if k != 'policy_hash'})
    r = select_test_only(e, pol, seed_hex=SEED, coordinate=1)
    assert r['decision'] == 'DEFER'
    assert r['reason'] == 'UNLICENSED_OR_INCOMPLETE_WEIGHT_UNITS'


def test_nonoccurrence_stays_real_no_change_and_no_foreign_owner_effect():
    e = evaluate(load('packet_explicit_nonoccurrence.json'), load('context_base.json'))
    pol = load('policy_design_weights.json')
    pol['candidate_set_hash'] = e['candidate_set_hash']
    pol['weight_units'] = {'ALT-NONE': 1}
    pol['policy_hash'] = digest({k: v for k, v in pol.items() if k != 'policy_hash'})
    s = select_test_only(e, pol, seed_hex=SEED, coordinate=7)
    assert s['selected_candidate_id'] == 'ALT-NONE'
    assert s['consumption']['target_CAN011_update_proposals'] == []
    assert s['consumption']['event_admission'] == 'NOT_PERFORMED'
