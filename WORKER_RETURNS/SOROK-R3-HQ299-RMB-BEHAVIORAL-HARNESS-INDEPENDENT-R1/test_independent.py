"""Independent contracts, not candidate implementation tests.

REDs are intentionally retained: each names a prerequisite for future use.
No transport, credentials, external models or generated actors are used.
"""
import copy
import inspect
import json
import socket
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'imports/LAB2'))
from lab2 import scoring, packets, behavioral_runner
from lab2.model_gate import Grant, evaluate_gate, REQUIRED_FIELDS
from lab2.scoring import ScorerInput, scorer_alpha, correctness_fraction, compare_arms


@pytest.fixture(autouse=True)
def no_network(monkeypatch):
    def denied(*args, **kwargs):
        raise AssertionError('INDEPENDENT_COURT_ZERO_NETWORK_CALL_GUARD')
    monkeypatch.setattr(socket.socket, 'connect', denied)
    monkeypatch.setattr(socket.socket, 'connect_ex', denied)
    monkeypatch.setattr(socket, 'getaddrinfo', denied)


def synthetic_grant(**changes):
    # Deliberately fabricated local test datum. NEVER an issued grant.
    values = dict(named_provider_exact_endpoint='https://example.invalid/no-call',
                  exact_model_and_version_pin='test-only@immutable',
                  privacy_permission_for_synthetic_lab_packets='LOCAL_TEST_DATUM',
                  experiment_use_grant_behavioral_actor_trials='LOCAL_TEST_DATUM',
                  explicit_monetary_cap='USD 0',
                  price_class_and_quota_observed='TEST_ONLY',
                  raw_request_response_retention_permission='LOCAL_TEST_DATUM',
                  per_trial_call_budget=1)
    return Grant(**(values | changes))


def packet(k='K3', contrast='TRACE_ACTIVE', arm='A'):
    fixture = next(f for f, c in packets.contrast_pairs(k) if c == contrast)
    return packets.build_trial_packet(k, fixture, contrast, 'S01', arm)


def core(p):
    return {k: v for k, v in p.items() if k not in
            ('typed_menu', 'presentation_code', 'counterbalance_code')}


@pytest.mark.parametrize('missing', REQUIRED_FIELDS)
def test_positive_every_missing_field_denies(missing):
    g = synthetic_grant(**{missing: None})
    r = behavioral_runner.BehavioralRunner(g)
    assert not evaluate_gate(g).allowed
    assert r.run_granted()['terminal'] == 'MODEL_BEHAVIORAL_HOLD'
    assert r.model_calls_issued == 0 and not r.calls


def test_positive_freeze_and_expected_mapping_match():
    pre = json.loads((ROOT / 'imports/LAB2/01_PREREGISTRATION_FROZEN.json').read_text())
    assert {c['id']: c['expected_typed_codes'] for c in
            pre['matched_heldout_comparisons']['cases']} == packets.EXPECTED_TYPED_CODES


def test_positive_prose_keyword_rejected():
    with pytest.raises(TypeError):
        ScorerInput('opaque', 'pc', 'SILENCE', prose='do not score me')


def test_positive_evaluator_only_sentinel_stays_out():
    p = packet()
    inj = packets.inject_hidden_origin(p, 'COURT_SENTINEL')
    assert packets.actor_visible_fingerprint(p) == packets.actor_visible_fingerprint(inj)


def test_positive_blind_oracle_rejects_wrong_label():
    expected = {'opaque': ['SILENCE']}
    recs = scorer_alpha([ScorerInput('opaque', 'pc', 'REQUEST_FEEDBACK')], expected)
    assert correctness_fraction(recs) == 0


def test_contract_scorer_ids_hide_contrast_labels():
    for t in packets.build_manifest()['trials']:
        assert t['prereg_contrast'] not in t['trial_id'], 'Contrast leaks through scorer trial_id'


def test_contract_counterbalance_is_exact_within_each_cell():
    m = packets.build_manifest()
    for k in packets.EXPECTED_TYPED_CODES:
        for c in packets.EXPECTED_TYPED_CODES[k]:
            for arm in packets.ARMS:
                rows = [t for t in m['trials'] if (t['k_id'], t['prereg_contrast'], t['arm']) == (k,c,arm)]
                counts = [sum(t['typed_menu'].index(t['expected_typed_codes'][0]) == j for t in rows)
                          for j in range(len(rows[0]['typed_menu']))]
                assert len(set(counts)) == 1, (k,c,arm,counts)


def test_contract_arm_manipulation_survives_menu_removal():
    assert core(packet(arm='A')) != core(packet(arm='B_admissible')), 'No A/B machinery manipulation'


def test_contract_k3_allowed_actor_packet_hides_inaccessible_origin():
    text = json.dumps(packet()['allowed_actor_info_packet'])
    assert 'PUBLIC_SHAMING' not in text and 'SHAMED_FOR_QUESTION' not in text


def test_contract_k5_actor_view_excludes_objective_owner_effects():
    p = packet('K5', 'WITNESS_REGISTRAR')
    visible = {k:v for k,v in p.items() if k not in
               ('presentation_code','counterbalance_code','evaluator_only_metadata','style_wrapper')}
    assert 'PUBLIC_STANDING_CHANGE' not in json.dumps(visible)


def test_contract_candidate_packet_refuses_unadmitted_event(monkeypatch):
    original = packets.case_fixture
    def bad_fixture(k):
        fx = copy.deepcopy(original(k))
        fx['histories']['H_RESPONSIVE']['events'][0]['admission'] = 'DRAFT'
        return fx
    monkeypatch.setattr(packets, 'case_fixture', bad_fixture)
    p = packet('K1', 'H_RESPONSIVE')
    assert p.get('invalid_and_hold_codes'), 'DRAFT ancestry accepted into packet without INVALID/HOLD'


def test_contract_primary_denominator_includes_unscorable():
    expected = {'a':['SILENCE'], 'b':['SILENCE']}
    recs = scorer_alpha([ScorerInput('a','p','SILENCE'), ScorerInput('b','p','OTHER_UNSCORABLE')], expected)
    assert correctness_fraction(recs) == .5, 'Unscorable silently removed from denominator'


def test_contract_dual_scorers_refuse_corrupt_answer_key():
    inputs = [ScorerInput('opaque','p','NOT_A_VALID_CODE')]
    out = scoring.dual_score(inputs, {'opaque':['NOT_A_VALID_CODE']})
    assert not out['records'][0]['correct'], 'Both scorers accept same invalid answer-key code'


def test_contract_pairing_requires_same_ids():
    a = scorer_alpha([ScorerInput('a','p','SILENCE')], {'a':['SILENCE']})
    b = scorer_alpha([ScorerInput('different','p','REQUEST_FEEDBACK')], {'different':['REQUEST_FEEDBACK']})
    with pytest.raises(scoring.ScorerIntegrityError):
        compare_arms({'A':a, 'B_admissible':b})


def test_contract_interval_required_before_promotion_screen():
    a = scorer_alpha([ScorerInput('a','p','REQUEST_FEEDBACK')], {'a':['SILENCE']})
    b = scorer_alpha([ScorerInput('a','p','SILENCE')], {'a':['SILENCE']})
    out = compare_arms({'A':a, 'B_admissible':b})['comparisons']['B_admissible']
    assert 'paired_interval' in out, 'No paired interval computed'


@pytest.mark.parametrize('change', [
    {'privacy_permission_for_synthetic_lab_packets':'DENIED'},
    {'experiment_use_grant_behavioral_actor_trials':'DENIED'},
    {'raw_request_response_retention_permission':False},
    {'exact_model_and_version_pin':'latest'},
    {'explicit_monetary_cap':'USD -1'},
    {'per_trial_call_budget':True},
    {'per_trial_call_budget':1.5},
])
def test_contract_gate_refuses_semantically_invalid_grant(change):
    assert not evaluate_gate(synthetic_grant(**change)).allowed, change


def test_contract_grant_alone_is_not_unimplemented():
    r = behavioral_runner.BehavioralRunner(synthetic_grant(), preregistration_sha256='NOT_A_FREEZE')
    # No transport exists: this exercises a local stub only and issues zero calls.
    try:
        r.run_granted()
    except NotImplementedError:
        pytest.fail('Filled test fields reach NotImplementedError; grant alone cannot run assay')
    finally:
        assert r.model_calls_issued == 0


def test_contract_null_runner_has_order_and_budget_result():
    out = behavioral_runner.run_packet_nulls()
    assert 'N3_ORDER' in out and 'N7_BUDGET' in out, 'N3/N7 are declarations only'


def test_contract_secondary_free_text_capture_implemented():
    assert hasattr(behavioral_runner.BehavioralRunner, 'run_free_text_validation')


def test_contract_k1_preserves_predecessor_lawful_appeal():
    assert 'APPEAL' in packets.MENU_ORDER['K1']
    assert 'APPEAL' in packets.EXPECTED_TYPED_CODES['K1']['H_PUNITIVE']


def test_contract_k5_preserves_remain_doubtful_outcome():
    assert 'REMAIN_DOUBTFUL' in packets.MENU_ORDER['K5']
    assert 'REMAIN_DOUBTFUL' in packets.EXPECTED_TYPED_CODES['K5']['WITNESS_REGISTRAR']


def test_contract_k6_candidate_does_not_become_mandatory():
    assert 'NO_SANCTION' in packets.EXPECTED_TYPED_CODES['K6']['PRACTICE_AND_CAPACITY']


def test_contract_k6_capacity_contrast_contains_capacity_evidence():
    yes = packet('K6', 'PRACTICE_AND_CAPACITY')
    no = packet('K6', 'PRACTICE_NO_CAPACITY')
    facts = ('world_snapshot','admitted_history','allowed_actor_info_packet','present_occurrence')
    assert {k:yes[k] for k in facts} != {k:no[k] for k in facts}, 'Opposite expected codes, identical factual input; position/capacity omitted'
