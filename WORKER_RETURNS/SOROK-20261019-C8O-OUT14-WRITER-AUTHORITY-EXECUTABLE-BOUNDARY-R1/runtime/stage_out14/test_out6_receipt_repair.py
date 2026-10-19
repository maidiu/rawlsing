"""HQ311 OUT6 author tests for the three *reported*, source-free OUT5 defect mechanisms.

These are NEW, not the uncommitted OUT5 fourteen. No policy on legacy
admission or client ACK/offer order is decided here. Real API and POSIX-like
cold snapshot paths only. No claim of transport or human perception.
"""
import copy
import json
import subprocess
import sys
from pathlib import Path
import pytest
from outbox_prototype import (make_prototype, Journal, DeliveryState,
    durable_delivery_id, _hash)
from test_cold_repair import strict


def strict_event():
    p=make_prototype();p.ledger.admission_decider=lambda _:True
    ev=p.ledger.admit(strict())
    assert ev and ev['admission_grade']=='SOURCEFREE_BOUND_DECIDER_NOT_OWNER'
    return p,ev['occurrence_id']


def queued(viewer='A'):
    p,eid=strict_event()
    assert p.outbox.authorize_viewer(eid,viewer)
    assert p.outbox.emit_to(eid,viewer)
    return p,eid


def delivered(viewer='A'):
    p,eid=queued(viewer)
    assert p.outbox.deliver_to(eid,viewer)['state']=='DELIVERED_UNACKED'
    return p,eid


def acknowledged(viewer='A'):
    p,eid=delivered(viewer)
    assert p.outbox.ack_to(eid,viewer)['state']=='ACKNOWLEDGED'
    return p,eid


def test_client_ack_receipt_cannot_regress_to_failed():
    p,eid=acknowledged()
    key=durable_delivery_id(eid,'A');before=copy.deepcopy(p.outbox.client_deliveries[key])
    p.outbox.fail_to(eid,'A')
    assert p.outbox.client_deliveries[key]==before
    assert p.outbox.emit_to(eid,'A')['state']=='ACKNOWLEDGED'
    p.validate_state()


def test_global_ack_receipt_cannot_regress_to_failed():
    p,eid=acknowledged()
    assert p.projection.offer('A',eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    before=copy.deepcopy(p.outbox.deliveries[eid])
    assert p.outbox.fail(eid)==DeliveryState.ACKNOWLEDGED
    assert p.outbox.deliveries[eid]==before
    assert p.outbox.retry(eid)==DeliveryState.ACKNOWLEDGED
    p.validate_state()


def test_failed_client_without_ack_retries_with_next_attempt():
    p,eid=delivered()
    key=durable_delivery_id(eid,'A');before=p.outbox.client_deliveries[key]['last_attempt_id']
    assert p.outbox.fail_to(eid,'A')['state']=='FAILED'
    again=p.outbox.emit_to(eid,'A')
    assert again['state']=='ADMITTED_UNDELIVERED'
    assert again['attempts']==2 and again['last_attempt_id']!=before
    p.validate_state()


def test_failed_global_without_revocation_retries():
    p,eid=queued()
    p.outbox.fail(eid)
    assert p.outbox.retry(eid)==DeliveryState.ADMITTED_UNDELIVERED
    assert p.outbox.deliveries[eid]['attempts']==2
    p.validate_state()


def test_sole_viewer_revocation_blocks_global_retry():
    p,eid=queued()
    assert p.outbox.fail(eid)==DeliveryState.FAILED
    before=copy.deepcopy(p.outbox.deliveries[eid])
    assert p.outbox.revoke_viewer(eid,'A')
    assert p.outbox.retry(eid)==DeliveryState.NOT_SENT
    assert p.outbox.deliveries[eid]==before
    assert p.outbox.emit(eid)==DeliveryState.NOT_SENT
    assert p.outbox.deliveries[eid]==before
    p.validate_state()


def test_sole_viewer_revocation_blocks_retry_after_cold_restore(tmp_path):
    p,eid=queued()
    p.outbox.fail(eid);assert p.outbox.revoke_viewer(eid,'A')
    j=Journal(tmp_path/'receipt.json');j.commit(p)
    q=j.recover();before=copy.deepcopy(q.snapshot())
    assert q.outbox.retry(eid)==DeliveryState.NOT_SENT
    assert q.outbox.emit(eid)==DeliveryState.NOT_SENT
    assert q.snapshot()==before


def test_authorized_other_viewer_can_retry_failed_global():
    p,eid=queued('A')
    assert p.outbox.authorize_viewer(eid,'B')
    p.outbox.emit_to(eid,'B')
    assert p.outbox.fail(eid)==DeliveryState.FAILED
    assert p.outbox.revoke_viewer(eid,'A')
    assert p.outbox.retry(eid)==DeliveryState.ADMITTED_UNDELIVERED
    p.validate_state()


def test_restore_rejects_ghost_client_for_unknown_viewer_atomically():
    p,eid=queued('A')
    good=p.snapshot();bad=copy.deepcopy(good)
    key=durable_delivery_id(eid,'B')
    ghost=copy.deepcopy(good['client_deliveries'][durable_delivery_id(eid,'A')])
    ghost.update(viewer_id='B',delivery_id=key)
    from outbox_prototype import durable_attempt_id
    ghost['last_attempt_id']=durable_attempt_id(eid,'B',ghost['attempts'])
    bad['client_deliveries'][key]=ghost
    with pytest.raises(ValueError,match='UNAUTHORIZED_CLIENT_DELIVERY'):
        p.restore(bad)
    assert p.snapshot()==good


def test_restore_rejects_only_ghost_client_even_for_legacy_event():
    p=make_prototype();eid=p.ledger.admit({'candidate_id':'legacy-1','payload':{'s':'hi'}})['occurrence_id']
    assert p.outbox.emit(eid)==DeliveryState.ADMITTED_UNDELIVERED
    snap=p.snapshot()
    key=durable_delivery_id(eid,'B')
    from outbox_prototype import durable_attempt_id
    snap['client_deliveries'][key]={'event_id':eid,'viewer_id':'B','delivery_id':key,
        'state':'ADMITTED_UNDELIVERED','attempts':1,'ack_count':0,'last_attempt_id':durable_attempt_id(eid,'B',1)}
    with pytest.raises(ValueError,match='UNAUTHORIZED_CLIENT_DELIVERY'):
        p.restore(snap)


def test_legit_revoke_preserves_historical_client_receipt_restore(tmp_path):
    p,eid=delivered('A')
    assert p.outbox.revoke_viewer(eid,'A')
    old=copy.deepcopy(p.outbox.client_deliveries[durable_delivery_id(eid,'A')])
    j=Journal(tmp_path/'audit.json');j.commit(p)
    q=j.recover()
    assert q.outbox.client_deliveries[durable_delivery_id(eid,'A')]==old
    assert q.outbox.ack_to(eid,'A') is None
    assert q.outbox.deliver_to(eid,'A') is None
    q.validate_state()


def test_rehashed_journal_forgery_of_unauthorized_viewer_refused(tmp_path):
    p,eid=queued('A')
    j=Journal(tmp_path/'receipt.json');j.commit(p)
    raw=json.loads(j.path.read_text());key=durable_delivery_id(eid,'B')
    from outbox_prototype import durable_attempt_id
    raw['state']['client_deliveries'][key]={'event_id':eid,'viewer_id':'B','delivery_id':key,
        'state':'ADMITTED_UNDELIVERED','attempts':1,'ack_count':0,'last_attempt_id':durable_attempt_id(eid,'B',1)}
    raw['state_digest']=_hash(raw['state'])
    j.path.write_text(json.dumps(raw))
    with pytest.raises(ValueError,match='UNAUTHORIZED_CLIENT_DELIVERY'):
        j.recover()


def test_rejected_snapshot_preserves_live_state_including_world():
    p,eid=queued();p.world_state['fixture-marker']='unchanged'
    before=p.snapshot();bad=copy.deepcopy(before)
    key=durable_delivery_id(eid,'B')
    bad['client_deliveries'][key]={'event_id':eid,'viewer_id':'B','delivery_id':key,
        'state':'NOT_SENT','attempts':0,'ack_count':0,'last_attempt_id':None}
    with pytest.raises(ValueError,match='UNAUTHORIZED_CLIENT_DELIVERY'):
        p.restore(bad)
    assert p.snapshot()==before


def test_rejected_persisted_forgery_keeps_existing_disk_state(tmp_path):
    p,eid=queued();j=Journal(tmp_path/'p.json');j.commit(p)
    original=j.path.read_bytes();before=p.snapshot();bad=copy.deepcopy(before)
    key=durable_delivery_id(eid,'B')
    bad['client_deliveries'][key]={'event_id':eid,'viewer_id':'B','delivery_id':key,
        'state':'NOT_SENT','attempts':0,'ack_count':0,'last_attempt_id':None}
    with pytest.raises(ValueError):p.restore(bad)
    assert j.path.read_bytes()==original
    assert j.recover().snapshot()==before


def test_terminal_ack_survives_actual_cold_python_process(tmp_path):
    p,eid=acknowledged();assert p.projection.offer('A',eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    j=Journal(tmp_path/'ack.json');j.commit(p)
    code="""import sys
from outbox_prototype import Journal,DeliveryState,durable_delivery_id
q=Journal(sys.argv[1]).recover()
e='OCC-0001';key=durable_delivery_id(e,'A')
assert q.outbox.fail(e)==DeliveryState.ACKNOWLEDGED
assert q.outbox.fail_to(e,'A')['state']==DeliveryState.ACKNOWLEDGED.value
assert q.outbox.retry(e)==DeliveryState.ACKNOWLEDGED
assert q.outbox.client_deliveries[key]['ack_count']==1
q.validate_state()
"""
    ret=subprocess.run([sys.executable,'-c',code,str(j.path)],text=True,capture_output=True,timeout=12,
                       cwd=Path(__file__).parent)
    assert ret.returncode==0,(ret.stdout,ret.stderr)


def test_sole_revoked_retries_refused_in_actual_cold_python_process(tmp_path):
    p,eid=queued();assert p.outbox.fail(eid)==DeliveryState.FAILED
    assert p.outbox.revoke_viewer(eid,'A')
    j=Journal(tmp_path/'revoked.json');j.commit(p)
    code="""import sys
from outbox_prototype import Journal,DeliveryState
q=Journal(sys.argv[1]).recover()
before=q.snapshot();e='OCC-0001'
assert q.outbox.retry(e)==DeliveryState.NOT_SENT
assert q.outbox.emit(e)==DeliveryState.NOT_SENT
assert q.snapshot()==before
"""
    ret=subprocess.run([sys.executable,'-c',code,str(j.path)],text=True,capture_output=True,timeout=12,
                       cwd=Path(__file__).parent)
    assert ret.returncode==0,(ret.stdout,ret.stderr)


def test_rehashed_ghost_journal_rejected_in_actual_cold_python_process(tmp_path):
    p,eid=queued();j=Journal(tmp_path/'corrupt.json');j.commit(p)
    state=json.loads(j.path.read_text());key=durable_delivery_id(eid,'ghost')
    state['state']['client_deliveries'][key]={'event_id':eid,'viewer_id':'ghost','delivery_id':key,
        'state':'NOT_SENT','attempts':0,'ack_count':0,'last_attempt_id':None}
    state['state_digest']=_hash(state['state']);j.path.write_text(json.dumps(state))
    code="""import sys
from outbox_prototype import Journal
try:Journal(sys.argv[1]).recover()
except ValueError as exc:
    assert str(exc)=='UNAUTHORIZED_CLIENT_DELIVERY',str(exc)
else:raise AssertionError('forged viewer accepted')
"""
    ret=subprocess.run([sys.executable,'-c',code,str(j.path)],text=True,capture_output=True,timeout=12,
                       cwd=Path(__file__).parent)
    assert ret.returncode==0,(ret.stdout,ret.stderr)


def test_failed_not_sent_state_not_fabricated_by_client_fail():
    p,eid=queued();key=durable_delivery_id(eid,'A')
    rec=p.outbox.client_deliveries[key]
    rec.update(state='NOT_SENT',attempts=0,ack_count=0,last_attempt_id=None)
    assert p.outbox.fail_to(eid,'A')['state']=='NOT_SENT'
    p.validate_state()


def test_failed_not_sent_state_not_fabricated_by_global_fail():
    p,eid=strict_event()
    assert p.outbox.emit(eid,viewer_id=None)==DeliveryState.NOT_SENT
    assert p.outbox.fail(eid)==DeliveryState.NOT_SENT
    p.validate_state()
