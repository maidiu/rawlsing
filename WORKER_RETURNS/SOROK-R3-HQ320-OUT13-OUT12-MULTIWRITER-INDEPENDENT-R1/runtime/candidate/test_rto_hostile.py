"""Independent HQ301 RTO adversarial tests, candidate left byte-identical.

REDs are substantive counterexamples at *sourcefree interface* grain, not accepted
production defects. The tests assert the safer API behavior rather than recasting
untrusted caller values as grants. No external actual V3 or human perception.
"""
import copy, json, os, subprocess, sys
from pathlib import Path
import pytest
from outbox_prototype import (Journal, make_prototype, DeliveryState, durable_delivery_id,
                              _hash)

HERE=Path(__file__).resolve().parent

def strict(label='S', **changes):
    d=dict(candidate_id=label, payload={'utterance':'Hello'},
           source_refs=['SRC-FAKE'], causal_time='2026-10-14T20:00:00',
           artifact_id='ART-FAKE',artifact_digest='sha256:NOT_A_REAL_DIGEST',
           issuer_ref='ISSUER-FAKE',authority_ref='ADP019', release_ref='RELEASE-FAKE',
           participant_refs=['ACTOR'],parent_refs=[],envelope_mode='STRICT')
    d.update(changes)
    return d

def s_with_decider(allow=True):
    p=make_prototype()
    p.ledger.admission_decider=lambda env:allow
    return p

def legacy(label='L'):
    return {'candidate_id':label,'payload':{'utterance':'Hi'}}

def cdel(p,eid,viewer='A'):
    p.outbox.authorize_viewer(eid,viewer)
    p.outbox.emit_to(eid,viewer)
    return p.outbox.deliver_to(eid,viewer)

def assert_refused_or_no_event(p,c):
    e=p.ledger.admit(c)
    assert e is None
    assert p.ledger.count()==0

@pytest.mark.parametrize('badmode',['STRICT_TYPO','stricT','',None,'SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'])
def test_unknown_explicit_envelope_mode_must_never_downgrade(badmode):
    p=make_prototype()
    assert_refused_or_no_event(p,{'candidate_id':'TY', 'envelope_mode':badmode,'payload':{'utterance':'Hello'}})

@pytest.mark.parametrize('forbidden',[{'admit':True}, {'admitted_event_id':'v3ext:fake'},
                                       {'state_delta':{'job':'quit'}}, {'cursor_after':999},
                                       {'effect_result':'MOVE_MUG'}, {'memory_delta':{'knowledge':'secret'}}])
def test_strict_forbidden_proposal_causal_directions_refused_even_positive_callback(forbidden):
    p=s_with_decider();assert_refused_or_no_event(p,strict(**forbidden))

def test_strict_decider_false_blocks_untrusted_source_strings():
    p=s_with_decider(False)
    assert_refused_or_no_event(p,strict())
    assert p.ledger.last_refusal=='NO_COMPETENT_ADMISSION_WITNESS'

def test_strict_without_decider_holds_regardless_of_refs():
    p=make_prototype();assert_refused_or_no_event(p,strict())

def test_top_level_unlicensed_objective_effect_must_not_be_silent_event():
    p=make_prototype()
    assert_refused_or_no_event(p,{**legacy('SRC'), 'objective_employment_transition':'quit'})

def test_missing_explicit_source_holds():
    p=make_prototype();assert_refused_or_no_event(p,strict(source_refs=[]))
    assert p.ledger.last_refusal=='MISSING_SOURCE_AUTHORITY'

def test_missing_explicit_time_defers():
    p=make_prototype();assert_refused_or_no_event(p,strict(causal_time=None))
    assert p.ledger.last_refusal=='DEFER_MISSING_CAUSAL_TIME'

def test_stale_decider_replay_same_proposal_must_block_without_grant():
    p=make_prototype();state={'live':True};p.ledger.admission_decider=lambda _:state['live']
    e=p.ledger.admit(strict());assert e
    state['live']=False
    assert p.ledger.admit(strict()) is None

def test_strict_viewer_not_authorized_cannot_offer():
    p=s_with_decider();e=p.ledger.admit(strict());assert e
    assert not p.projection.offer('STRANGER',e['occurrence_id'])

def test_strict_explicit_revocation_must_block_pending_send():
    p=s_with_decider();eid=p.ledger.admit(strict())['occurrence_id']
    p.outbox.authorize_viewer(eid,'A');p.outbox.emit_to(eid,'A')
    p.outbox.viewers[eid].remove('A') # simulate new external denial
    assert p.outbox.deliver_to(eid,'A') is None

def test_strict_explicit_revocation_must_block_ack():
    p=s_with_decider();eid=p.ledger.admit(strict())['occurrence_id']
    cdel(p,eid)
    p.outbox.viewers[eid].remove('A')
    assert p.outbox.ack_to(eid,'A') is None

def test_global_ack_does_not_create_viewer_opportunity():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    p.outbox.emit(eid);p.outbox.deliver(eid);p.outbox.ack(eid)
    assert not p.projection.has_opportunity('A',eid)
    assert not p.projection.has_perceived('A',eid)

def test_unknown_event_refused_at_emit_and_offer():
    p=make_prototype();assert p.outbox.emit('OCC-9999')==DeliveryState.NOT_SENT
    assert not p.projection.offer('A','OCC-9999')

def test_negative_perception_callback_never_authenticates():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    p.outbox.emit(eid);p.outbox.deliver(eid);p.projection.offer('A',eid)
    p.projection.perception_decider=lambda *_:False
    assert not p.projection.perceive('A',eid,perception_witness='forged')

def test_caller_owned_true_perception_callback_must_not_establish_real_human_perceived():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    p.outbox.emit(eid);p.outbox.deliver(eid);p.projection.offer('A',eid)
    p.projection.perception_decider=lambda *_:True  # unauthenticated caller-side callback
    assert not p.projection.perceive('A',eid,perception_witness={'human_seen':True})
    assert not p.projection.has_perceived('A',eid)

def test_revoked_strict_client_receipt_must_not_be_usable_to_perceive_after_global_delivery():
    p=s_with_decider();eid=p.ledger.admit(strict())['occurrence_id']
    cdel(p,eid,'A');assert p.projection.offer('A',eid)
    p.outbox.fail_to(eid,'A')
    p.outbox.emit(eid,viewer_id='A');p.outbox.deliver(eid)
    p.projection.perception_decider=lambda *_:True
    assert not p.projection.perceive('A',eid,perception_witness='NO_OWNER_RECEIPT')

def test_signed_journal_digest_refuses_one_byte_corruption(tmp_path):
    j=Journal(tmp_path/'state.json');p=make_prototype();j.commit(p)
    d=json.loads(j.path.read_text());d['state']['world']={'invented':'YES'}
    j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError, match='BAD_JOURNAL_DIGEST'):j.recover()

def test_crafted_journal_with_recomputed_unkeyed_digest_must_not_create_authority(tmp_path):
    j=Journal(tmp_path/'state.json');p=make_prototype();j.commit(p)
    d=json.loads(j.path.read_text());d['state']['world']={'invented':'YES'}
    d['state_digest']=_hash(d['state'])
    j.path.write_text(json.dumps(d))
    with pytest.raises(ValueError):j.recover()

def test_forged_perceived_ghost_same_user_as_good_opportunity_is_rejected(tmp_path):
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    p.projection.offer('A',eid)
    p.projection.perceived['A']=['OCC-9999']
    with pytest.raises(ValueError,match='GHOST_PROJECTION_STATE'):
        Journal(tmp_path/'j.json').commit(p)

def test_forged_client_attempt_identity_rejected_at_journal_commit(tmp_path):
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    cdel(p,eid,'A');key=durable_delivery_id(eid,'A')
    p.outbox.client_deliveries[key]['last_attempt_id']='ATT-FORGED'
    with pytest.raises(ValueError):Journal(tmp_path/'j.json').commit(p)

def test_client_outbox_revocation_not_automatically_deletion_of_old_receipt():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    cdel(p,eid,'A');p.outbox.viewers[eid].remove('A')
    # Present model explicitly has no revocation protocol: should not falsely claim one.
    assert 'A' not in p.outbox.viewers[eid]

def test_lost_ack_retry_distinct_attempt_same_delivery_identity():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    a=p.outbox.authorize_viewer(eid,'A');assert a
    d=p.outbox.emit_to(eid,'A');did=d['delivery_id'];old=d['last_attempt_id']
    p.outbox.deliver_to(eid,'A');p.outbox.fail_to(eid,'A')
    d2=p.outbox.emit_to(eid,'A')
    assert d2['delivery_id']==did and d2['last_attempt_id']!=old
    assert d2['attempts']==2 and p.ledger.count()==1

def test_distinct_delivery_ids_for_distinct_viewers():
    p=make_prototype();eid=p.ledger.admit(legacy())['occurrence_id']
    p.outbox.authorize_viewer(eid,'A');p.outbox.authorize_viewer(eid,'B')
    assert p.outbox.emit_to(eid,'A')['delivery_id']!=p.outbox.emit_to(eid,'B')['delivery_id']

def test_source_and_artifact_replay_collision_refuses():
    p=s_with_decider();assert p.ledger.admit(strict())
    assert p.ledger.admit(strict(source_refs=['SOURCE-CHANGED'])) is None
    assert p.ledger.admit(strict(artifact_id='ART-CHANGED')) is None
    assert p.ledger.count()==1

def test_strict_future_parent_time_requires_defer():
    p=s_with_decider();parent=p.ledger.admit(strict());assert parent
    assert p.ledger.admit(strict('CHILD',parent_refs=[parent['occurrence_id']],causal_time='2026-10-14T19:00:00')) is None

def run_driver(mode,path):
    env=dict(os.environ, PYTHONPATH=str(HERE.parent/'source'))
    r=subprocess.run([sys.executable,str(HERE/'rto_cold_driver.py'),mode,str(path)],env=env,timeout=15,capture_output=True,text=True)
    return r

def test_new_independent_cold_before_rename(tmp_path):
    path=tmp_path/'journal.json'
    r=run_driver('kill_before',path);assert r.returncode==79,r.stderr
    assert not path.exists()
    r=run_driver('read_empty',path);assert r.returncode==0,(r.stdout,r.stderr)

def test_new_independent_cold_after_fsync_then_restart(tmp_path):
    path=tmp_path/'journal.json'
    r=run_driver('kill_after',path);assert r.returncode==79,r.stderr
    r=run_driver('read_durable',path);assert r.returncode==0,(r.stdout,r.stderr)

def test_existing_durable_entry_survives_subsequent_precommit_crash(tmp_path):
    path=tmp_path/'journal.json'
    r=run_driver('kill_after',path);assert r.returncode==79
    r=run_driver('kill_second_before',path);assert r.returncode==79
    r=run_driver('read_durable',path);assert r.returncode==0,(r.stdout,r.stderr)

def test_corrupt_snapshot_refuses_new_process(tmp_path):
    path=tmp_path/'journal.json';r=run_driver('kill_after',path);assert r.returncode==79
    path.write_bytes(path.read_bytes()[:-9])
    r=run_driver('read_durable',path)
    assert r.returncode!=0 and 'Traceback' in r.stderr

def test_replay_manual_two_writers_can_lose_first_committed_event(tmp_path):
    j=Journal(tmp_path/'journal.json'); a=j.recover();b=j.recover()
    first=a.ledger.admit(legacy('A'));a.outbox.emit(first['occurrence_id']);j.commit(a)
    second=b.ledger.admit(legacy('B'));b.outbox.emit(second['occurrence_id']);j.commit(b)
    # A second stale writer must not erase the original commit.
    reread=j.recover(); assert reread.ledger.get('OCC-0001')['candidate_id']=='A'
    assert reread.ledger.count()==2

@pytest.mark.parametrize('extra_key',[ 'producer_instance_ref','producer_rule_version','expected_v3_event_cursor',
                                      'expected_v3_history_hash','render_receipt_hash','render_context_hash',
                                      'expected_causal_session_cursor','payload_hash'])
def test_strict_full_adp019_relevant_fields_cannot_change_under_same_proposal_id(extra_key):
    # Metadata here is exactly within ADP019 causal/event/render provenance jurisdiction,
    # though this sourcefree candidate explicitly implements only its own smaller envelope.
    p=s_with_decider()
    first=strict(**{extra_key:'A'})
    second=strict(**{extra_key:'B'})
    assert p.ledger.admit(first)
    assert p.ledger.admit(second) is None

@pytest.mark.parametrize('changed', [
    {'source_refs':['OTHER']}, {'issuer_ref':'OTHER'}, {'release_ref':'OTHER'},
    {'artifact_id':'OTHER'},{'artifact_digest':'OTHER'},{'authority_ref':'OTHER'},
    {'participant_refs':['OTHER']},{'causal_time':'2026-10-14T21:00:00'},
])
def test_frozen_narrow_identity_fields_are_bound_at_sourcefree_grain(changed):
    p=s_with_decider();first=p.ledger.admit(strict());assert first
    assert p.ledger.admit(strict(**changed)) is None


def test_seeded_fuzz_160_narrow_mutations_keep_first_event_immutable():
    import random
    random.seed(301)
    for index in range(160):
        p=s_with_decider();initial=strict(label=f'CAN-{index}')
        first=p.ledger.admit(initial)
        original=copy.deepcopy(first)
        variant=copy.deepcopy(initial)
        field=random.choice(['source_refs','issuer_ref','release_ref','artifact_id','artifact_digest',
                             'authority_ref','participant_refs','causal_time','payload'])
        if field=='source_refs':variant[field]=[f'REF-{index}']
        elif field=='participant_refs':variant[field]=[f'ACTOR-{index}']
        elif field=='causal_time':variant[field]='2026-10-14T21:00:00'
        elif field=='payload':variant[field]={'utterance':f'MUTATED-{index}'}
        else:variant[field]=f'MUTATED-{index}'
        assert p.ledger.admit(variant) is None
        assert p.ledger.count()==1 and p.ledger.get(first['occurrence_id'])==original


def test_snapshot_restore_invalid_event_should_not_leave_mutated_failed_restore_state():
    p=make_prototype();eid=p.ledger.admit(legacy('SAFE'))['occurrence_id']
    before=p.snapshot();bad=copy.deepcopy(before)
    bad['ledger'][0]['payload']['utterance']='TAMPER'
    with pytest.raises(ValueError):p.restore(bad)
    # Fail-atomicity expected for an in-use restored object, even if cold Journal
    # recover normally constructs and discards its new instance on failure.
    assert p.ledger.get(eid)['payload']==before['ledger'][0]['payload']
