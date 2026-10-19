"""Author-created OUT8 repair controls; independent OUT7 source stays byte-identical.

Only structural source-free receipt reachability is asserted. These tests do not
choose OUTP L1/L2 or A1/A2, establish real perception, or authenticate journal writers.
"""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from outbox_prototype import DeliveryState, Journal, _hash, durable_attempt_id, durable_delivery_id, make_prototype
from test_out7_independent_hostile import strict, strict_queued, strict_delivered, strict_acked


def _client(eid,viewer,n=0,state='NOT_SENT',ack=0):
    key=durable_delivery_id(eid,viewer)
    return key,dict(event_id=eid,viewer_id=viewer,delivery_id=key,state=state,
                    attempts=n,ack_count=ack,last_attempt_id=durable_attempt_id(eid,viewer,n) if n else None)


def _fork(code,*args):
    r=subprocess.run([sys.executable,'-c',code,*map(str,args)],
                     cwd=Path(__file__).parent,capture_output=True,text=True,timeout=18)
    assert r.returncode==0,(r.returncode,r.stdout,r.stderr)
    return r


@pytest.mark.parametrize('state', ['ADMITTED_UNDELIVERED','DELIVERED_UNACKED','FAILED'])
def test_X01_forged_aggregate_ack_refuses_all_live_nonacked_client_states(state):
    p,eid=strict_queued('V')
    if state=='DELIVERED_UNACKED':p.outbox.deliver_to(eid,'V')
    if state=='FAILED':p.outbox.fail_to(eid,'V')
    before=p.snapshot();bad=copy.deepcopy(before)
    bad['outbox'][eid].update(state='ACKNOWLEDGED',ack_count=1)
    with pytest.raises(ValueError,match='FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT'):
        p.restore(bad)
    assert p.snapshot()==before


@pytest.mark.parametrize('phase', ['active','revoked'])
def test_X02_zero_attempt_placeholder_active_fixture_vs_revoked_history(phase):
    p,eid=strict_queued('A');before=p.snapshot();bad=copy.deepcopy(before)
    if phase=='active':bad['viewers'][eid].append('B')
    else:bad['revoked_viewers'][eid]=['B']
    key,row=_client(eid,'B')
    bad['client_deliveries'][key]=row
    if phase=='revoked':
        with pytest.raises(ValueError,match='FORGED_ZERO_ATTEMPT_CLIENT_HISTORY'):
            p.restore(bad)
        assert p.snapshot()==before
    else:
        # OUT6 inherited fixture explicitly validates active NOT_SENT placeholders.
        p.restore(bad);assert p.validate_state() is None


@pytest.mark.parametrize('state,acks', [
    ('NOT_SENT',0),('DELIVERED_UNACKED',0),('ACKNOWLEDGED',1)])
def test_X03_zero_attempt_cannot_masquer_as_historical_client_state(state,acks):
    p,eid=strict_queued('A');before=p.snapshot();bad=copy.deepcopy(before)
    bad['revoked_viewers'][eid]=['B']
    key,row=_client(eid,'B',n=0,state=state,ack=acks)
    bad['client_deliveries'][key]=row
    with pytest.raises(ValueError):p.restore(bad)
    assert p.snapshot()==before


def test_X04_genuine_full_ack_then_revocation_is_valid_history():
    p,eid=strict_acked('A')
    assert p.projection.offer('A',eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    assert p.outbox.revoke_viewer(eid,'A')
    assert p.validate_state() is None
    q=make_prototype();q.restore(p.snapshot())
    assert q.outbox.deliveries[eid]['state']==DeliveryState.ACKNOWLEDGED.value
    assert q.outbox.emit_to(eid,'A') is None
    assert q.projection.has_perceived('A',eid) is False


def test_X05_genuine_revoked_unacked_receipt_keeps_nonterminal_aggregate_valid():
    p,eid=strict_delivered('A')
    assert p.outbox.revoke_viewer(eid,'A')
    assert p.validate_state() is None
    q=make_prototype();q.restore(p.snapshot())
    assert q.outbox.client_deliveries[durable_delivery_id(eid,'A')]['attempts']==1
    before=q.snapshot()
    assert q.outbox.retry(eid)==DeliveryState.ADMITTED_UNDELIVERED
    assert q.snapshot()==before


def test_X06_second_active_viewer_after_first_revocation_preserves_valid_ack():
    p,eid=strict_acked('A')
    assert p.outbox.authorize_viewer(eid,'B')
    assert p.outbox.emit_to(eid,'B') is not None
    p.outbox.deliver_to(eid,'B')
    p.outbox.ack_to(eid,'B')
    assert p.projection.offer('B',eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    assert p.outbox.revoke_viewer(eid,'A')
    assert p.validate_state() is None
    q=make_prototype();q.restore(p.snapshot());assert q.validate_state() is None


def test_X07_other_event_client_ack_cannot_satisfy_forged_global_ack():
    p,eid=strict_acked('A');assert p.projection.offer('A',eid)
    p.outbox.deliver(eid);p.outbox.ack(eid)
    second=p.ledger.admit(strict(label='ANOTHER'))['occurrence_id']
    p.outbox.authorize_viewer(second,'A');p.outbox.emit_to(second,'A');p.outbox.deliver_to(second,'A')
    good=p.snapshot();bad=copy.deepcopy(good)
    bad['outbox'][second].update(state='ACKNOWLEDGED',ack_count=1)
    with pytest.raises(ValueError,match='FORGED_AGGREGATE_ACK_WITHOUT_CLIENT_RECEIPT'):
        p.restore(bad)
    assert p.snapshot()==good


def test_X08_unknown_viewer_cannot_restore_even_with_nonzero_attempt():
    p,eid=strict_queued('A');good=p.snapshot();bad=copy.deepcopy(good)
    key,row=_client(eid,'Ghost',n=1,state='ADMITTED_UNDELIVERED')
    bad['client_deliveries'][key]=row
    with pytest.raises(ValueError,match='UNAUTHORIZED_CLIENT_DELIVERY'):
        p.restore(bad)
    assert p.snapshot()==good


@pytest.mark.parametrize('attack',['aggregate_ack','revoked_zero'])
def test_X09_rehashed_cold_snapshot_defects_refused_in_fresh_python(tmp_path,attack):
    p,eid=strict_delivered('A');j=Journal(tmp_path/f'{attack}.json');j.commit(p)
    doc=json.loads(j.path.read_text())
    if attack=='aggregate_ack':
        doc['state']['outbox'][eid].update(state='ACKNOWLEDGED',ack_count=1)
    else:
        doc['state']['revoked_viewers'][eid]=['B']
        key,row=_client(eid,'B')
        doc['state']['client_deliveries'][key]=row
    doc['state_digest']=_hash(doc['state']);j.path.write_text(json.dumps(doc))
    _fork("""import sys
from outbox_prototype import Journal
try:Journal(sys.argv[1]).recover()
except ValueError as e:
    assert 'FORGED_' in str(e),str(e)
else:raise AssertionError('fabricated journal accepted')
""",j.path)


@pytest.mark.parametrize('state',['ACKNOWLEDGED','DELIVERED_UNACKED'])
def test_X10_real_cold_roundtrip_preserves_legitimate_revoked_viewer_history(tmp_path,state):
    p,eid=strict_delivered('A')
    if state=='ACKNOWLEDGED':
        p.outbox.ack_to(eid,'A');p.projection.offer('A',eid)
        p.outbox.deliver(eid);p.outbox.ack(eid)
    assert p.outbox.revoke_viewer(eid,'A')
    j=Journal(tmp_path/'legit.json');j.commit(p)
    _fork("""import sys
from outbox_prototype import Journal,durable_delivery_id
p=Journal(sys.argv[1]).recover();p.validate_state()
assert 'A' in p.outbox.revoked_viewers['OCC-0001']
assert p.outbox.client_deliveries[durable_delivery_id('OCC-0001','A')]['attempts']==1
assert p.outbox.emit_to('OCC-0001','A') is None
""",j.path)


@pytest.mark.parametrize('boundary',['BEFORE_RENAME','AFTER_COMMIT'])
def test_X11_real_os_exit_cold_commit_boundaries_hold(tmp_path,boundary):
    p,eid=strict_queued('A');j=Journal(tmp_path/'atomic.json');j.commit(p)
    original=j.recover().snapshot()
    r=subprocess.run([sys.executable,'-c',"""import sys
from outbox_prototype import Journal
j=Journal(sys.argv[1]);p=j.recover()
assert p.outbox.deliver_to('OCC-0001','A')
j.commit(p,crash_boundary=sys.argv[2])
raise AssertionError('expected cold kill')
""",str(j.path),boundary],cwd=Path(__file__).parent,capture_output=True,text=True,timeout=18)
    assert r.returncode==79,(r.returncode,r.stderr)
    restored=j.recover().snapshot()
    if boundary=='BEFORE_RENAME':assert restored==original
    else:assert restored['client_deliveries'][durable_delivery_id(eid,'A')]['state']=='DELIVERED_UNACKED'


def test_X12_legacy_no_viewer_scalar_ack_remains_unadjudicated_and_unchanged():
    p=make_prototype();event=p.ledger.admit({'candidate_id':'fixture','payload':{'utterance':'hi'}})
    eid=event['occurrence_id']
    p.outbox.emit(eid)
    p.outbox.deliver(eid)
    p.outbox.ack(eid)
    assert p.validate_state() is None
    q=make_prototype();q.restore(p.snapshot())
    assert q.outbox.deliveries[eid]['ack_count']==1
    assert not q.projection.has_perceived('anyone',eid)
