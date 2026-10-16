"""New real-os._exit cold-process candidate Journal tests; not earlier harness saves."""
import json,subprocess,sys
from pathlib import Path
from outbox_prototype import _hash,make_prototype,Journal,durable_delivery_id,durable_attempt_id,DeliveryState
SCRIPT=Path(__file__).with_name('cold_repair.py')
def run(mode,path,exit_code):
    result=subprocess.run([sys.executable,str(SCRIPT),mode,str(path)],capture_output=True,text=True,timeout=15)
    assert result.returncode==exit_code,(mode,result.stdout,result.stderr,result.returncode)
    return json.loads(result.stdout) if exit_code==0 else None

def test_real_kill_before_atomic_rename_has_no_event_or_intent(tmp_path):
    db=tmp_path/'journal.json'
    run('crash_before',db,79)
    assert not db.exists()
    a=run('verify_before',db,0)
    assert a['result']=='PRECOMMIT_NOT_DURABLE'
    assert len(list(tmp_path.glob('.outbox-pending-*')))>=1

def test_real_kill_after_commit_survives_new_process_and_lost_ack(tmp_path):
    db=tmp_path/'journal.json'
    run('crash_after',db,79)
    a=run('verify_after',db,0)
    b=run('lost_ack_retry',db,0)
    c=run('ack_no_perception',db,0)
    assert a['delivery_id']==b['delivery_id']==c['delivery_id']
    assert b['new_attempt_id']!=a['attempt_id']
    assert b['attempts']==2 and c['result']=='ACK_NOT_PERCEPTION'

# Additional discriminating hostile sourcefree tests, beyond the frozen 28+17+2.
def strict(label='X',**overrides):
    d=dict(candidate_id=label,payload={'utterance':'Hello'},source_refs=['SOURCEFREE_PUBLISHED_ONLY'],causal_time='2026-10-14T19:01:00',artifact_id='ART-1',artifact_digest='DIGEST-1',issuer_ref='ISSUER-1',authority_ref='RULE-1',release_ref='R-1',participant_refs=['ACTOR-A'],parent_refs=[],envelope_mode='STRICT')
    d.update(overrides);return d

def test_strict_missing_actual_adjudicator_rejects_token_shaped_refs():
    p=make_prototype();assert p.ledger.admit(strict()) is None
    assert p.ledger.last_refusal=='NO_COMPETENT_ADMISSION_WITNESS'

def test_strict_bound_and_revoked_decider_gate():
    p=make_prototype();decision={'granted':True};p.ledger.admission_decider=lambda d: decision['granted']
    e=p.ledger.admit(strict())
    assert e and e['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER'
    assert p.outbox.emit(e['occurrence_id'])==DeliveryState.NOT_SENT
    assert p.projection.offer('client',e['occurrence_id']) is False
    assert p.outbox.authorize_viewer(e['occurrence_id'],'client')
    assert p.outbox.emit_to(e['occurrence_id'],'client') is not None
    assert p.projection.offer('client',e['occurrence_id']) is False
    p.outbox.deliver_to(e['occurrence_id'],'client')
    assert p.projection.offer('client',e['occurrence_id']) is True
    assert p.projection.perceive('client',e['occurrence_id'],perception_witness='FORGED') is False
    decision['granted']=False
    assert p.ledger.admit(strict()) is None
    assert p.ledger.last_refusal=='NO_COMPETENT_ADMISSION_WITNESS'

def test_source_artifact_time_parent_participants_same_id_replay_conflicts():
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    first=p.ledger.admit(strict());assert first
    for mod in [dict(source_refs=['OTHER']),dict(artifact_id='OTHER'),dict(causal_time='2026-10-14T19:02:00'),dict(participant_refs=['OTHER']),dict(parent_refs=['OCC-0001'])]:
        assert p.ledger.admit(strict(**mod)) is None
    assert p.ledger.count()==1

def test_causal_missing_out_of_order_fails_closed():
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    assert p.ledger.admit(strict(causal_time=None)) is None
    assert p.ledger.last_refusal=='DEFER_MISSING_CAUSAL_TIME'
    assert p.ledger.admit(strict(causal_time='tomorrow')) is None
    assert p.ledger.admit(strict(label='CHILD',parent_refs=['OCC-9999'])) is None
    parent=p.ledger.admit(strict());assert parent
    assert p.ledger.admit(strict(label='CHILD',causal_time='2026-10-14T19:00:00',parent_refs=['OCC-0001'])) is None
    assert p.ledger.last_refusal=='CAUSAL_TIME_PRECEDES_PARENT'

def test_valid_empty_distinct_from_explicit_missing_authority():
    p=make_prototype();ok=p.ledger.admit({'candidate_id':'EMPTY','payload':{}})
    assert ok and ok['payload']=={} and ok['admission_grade']=='SOURCEFREE_LEGACY_FIXTURE_NO_OWNER_AUTHORITY'
    bad=p.ledger.admit({'candidate_id':'NO-SOURCE','payload':{},'source_refs':[]})
    assert bad is None and p.ledger.last_refusal=='MISSING_SOURCE_AUTHORITY'

def test_journal_tamper_detect_and_illicit_world_commit_fails_closed(tmp_path):
    j=Journal(tmp_path/'state.json');p=make_prototype()
    p.world_state['employment']='invented'
    try:j.commit(p);assert False,'accepted illicit world fixture'
    except ValueError as e:assert str(e)=='WORLD_STATE_REQUIRES_EXTERNAL_OWNER'
    p.world_state.clear();j.commit(p)
    import json
    d=json.loads(j.path.read_text());d['state']['ledger']=[{'forged':True}]
    j.path.write_text(json.dumps(d))
    try:j.recover();assert False,'accepted forged snapshot'
    except ValueError as e:assert str(e)=='BAD_JOURNAL_DIGEST'

def test_different_viewers_have_distinct_stable_delivery_ids():
    p=make_prototype();e=p.ledger.admit({'candidate_id':'E','payload':{'utterance':'Hello'}})
    eid=e['occurrence_id'];p.outbox.authorize_viewer(eid,'A');p.outbox.authorize_viewer(eid,'B')
    a=p.outbox.emit_to(eid,'A');b=p.outbox.emit_to(eid,'B')
    assert a['delivery_id']!=b['delivery_id'] and a['delivery_id']==durable_delivery_id(eid,'A')
    assert p.outbox.emit_to(eid,'A')['attempts']==1
    assert p.outbox.deliver_to(eid,'A')['state']=='DELIVERED_UNACKED'
    assert p.outbox.client_deliveries[b['delivery_id']]['state']=='ADMITTED_UNDELIVERED'
