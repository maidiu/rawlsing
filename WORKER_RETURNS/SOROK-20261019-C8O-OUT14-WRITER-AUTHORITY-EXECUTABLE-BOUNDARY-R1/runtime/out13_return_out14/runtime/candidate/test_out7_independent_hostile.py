"""Fresh OUT7 independent sourcefree court. Frozen expectations in ../evidence/00_FROZEN_EXPECTATIONS.json.
No real perception, institutional actor, external signer, or OUTP policy selection."""
import copy
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from outbox_prototype import (DeliveryState, Journal, _hash, durable_attempt_id,
    durable_delivery_id, make_prototype)
from test_cold_repair import strict


def strict_queued(viewer="V"):
    p = make_prototype()
    p.ledger.admission_decider = lambda _: True
    event = p.ledger.admit(strict())
    assert event is not None
    eid = event["occurrence_id"]
    assert p.outbox.authorize_viewer(eid, viewer)
    assert p.outbox.emit_to(eid, viewer)["state"] == "ADMITTED_UNDELIVERED"
    return p, eid


def strict_delivered(viewer="V"):
    p,eid = strict_queued(viewer)
    assert p.outbox.deliver_to(eid,viewer)["state"] == "DELIVERED_UNACKED"
    return p,eid


def strict_acked(viewer="V"):
    p,eid=strict_delivered(viewer)
    assert p.outbox.ack_to(eid,viewer)["state"] == "ACKNOWLEDGED"
    return p,eid


def run_cold(code,*args):
    out = subprocess.run([sys.executable,"-c",code,*map(str,args)],cwd=Path(__file__).parent,
                         text=True,capture_output=True,timeout=14)
    assert out.returncode == 0,(out.stdout,out.stderr,out.returncode)
    return out


@pytest.mark.parametrize("failure_count",[1,3])
def test_I01_client_receipt_stays_acknowledged_after_duplicate_ack_and_failure(failure_count):
    p,eid=strict_acked(); key=durable_delivery_id(eid,"V")
    before=copy.deepcopy(p.outbox.client_deliveries[key])
    for _ in range(failure_count):
        assert p.outbox.fail_to(eid,"V")==before
        assert p.outbox.ack_to(eid,"V")==before
    assert p.outbox.client_deliveries[key]==before
    p.validate_state()


def test_I02_global_ack_survives_failing_callback_after_real_cold_reload(tmp_path):
    p,eid=strict_acked()
    assert p.projection.offer("V",eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    j=Journal(tmp_path/"state.json");j.commit(p)
    run_cold("""import sys
from outbox_prototype import Journal,DeliveryState
j=Journal(sys.argv[1]);p=j.recover();e='OCC-0001'
assert p.outbox.fail(e)==DeliveryState.ACKNOWLEDGED
assert p.outbox.retry(e)==DeliveryState.ACKNOWLEDGED
assert p.outbox.ack(e)==DeliveryState.ACKNOWLEDGED
assert p.outbox.deliveries[e]['ack_count']==1
p.validate_state();j.commit(p)
""",j.path)
    reread=j.recover();assert reread.outbox.deliveries[eid]["ack_count"]==1


def test_I03_nonacked_failure_retry_increments_attempt_ids():
    p,eid=strict_delivered();k=durable_delivery_id(eid,"V")
    old=p.outbox.client_deliveries[k]["last_attempt_id"]
    assert p.outbox.fail_to(eid,"V")["state"] == DeliveryState.FAILED.value
    again=p.outbox.emit_to(eid,"V")
    assert again["state"]==DeliveryState.ADMITTED_UNDELIVERED.value
    assert again["attempts"]==2 and again["last_attempt_id"]!=old
    p.validate_state()


def test_I04_revoked_sole_viewer_cannot_cold_retry(tmp_path):
    p,eid=strict_queued();assert p.outbox.fail(eid)==DeliveryState.FAILED
    assert p.outbox.revoke_viewer(eid,"V")
    j=Journal(tmp_path/"revoked.json");j.commit(p)
    run_cold("""import sys
from outbox_prototype import Journal,DeliveryState
q=Journal(sys.argv[1]).recover();before=q.snapshot();e='OCC-0001'
assert q.outbox.retry(e)==DeliveryState.NOT_SENT
assert q.outbox.emit(e)==DeliveryState.NOT_SENT
assert q.snapshot()==before
""",j.path)


def test_I05_other_authorized_client_can_continue_after_revocation():
    p,eid=strict_queued("A")
    assert p.outbox.authorize_viewer(eid,"B")
    assert p.outbox.emit_to(eid,"B")
    assert p.outbox.fail(eid)==DeliveryState.FAILED
    assert p.outbox.revoke_viewer(eid,"A")
    assert p.outbox.retry(eid)==DeliveryState.ADMITTED_UNDELIVERED
    assert p.outbox.deliver_to(eid,"B")["state"]==DeliveryState.DELIVERED_UNACKED.value
    assert p.outbox.ack_to(eid,"B")["state"]==DeliveryState.ACKNOWLEDGED.value
    assert p.projection.offer("B",eid)
    assert p.outbox.deliver(eid)==DeliveryState.DELIVERED_UNACKED
    assert p.outbox.ack(eid)==DeliveryState.ACKNOWLEDGED
    assert not p.projection.has_perceived("B",eid)
    p.validate_state()


@pytest.mark.parametrize("state",["NOT_SENT","ADMITTED_UNDELIVERED","ACKNOWLEDGED"])
def test_I06_restore_refuses_never_authorized_viewer_without_partial_mutation(state):
    p,eid=strict_queued();good=p.snapshot();bad=copy.deepcopy(good)
    k=durable_delivery_id(eid,"Ghost")
    n=0 if state=="NOT_SENT" else 1
    bad["client_deliveries"][k]={"event_id":eid,"viewer_id":"Ghost","delivery_id":k,
        "state":state,"attempts":n,"ack_count":int(state=="ACKNOWLEDGED"),
        "last_attempt_id":durable_attempt_id(eid,"Ghost",n) if n else None}
    with pytest.raises(ValueError,match="UNAUTHORIZED_CLIENT_DELIVERY"):
        p.restore(bad)
    assert p.snapshot()==good


@pytest.mark.parametrize("attack",["negative","bool_attempts","ack_before_send","oversized_ack"])
def test_I07_restore_rejects_corrupted_counters(attack):
    p,eid=strict_queued();before=p.snapshot();bad=copy.deepcopy(before)
    d=bad["client_deliveries"][durable_delivery_id(eid,"V")]
    if attack=="negative":d["attempts"]=-1
    if attack=="bool_attempts":d["attempts"]=True
    if attack=="ack_before_send":d["ack_count"]=1
    if attack=="oversized_ack":d["ack_count"]=2
    with pytest.raises(ValueError):p.restore(bad)
    assert p.snapshot()==before


def test_I08_strict_global_ACK_forgery_with_no_client_ACK_refused():
    p,eid=strict_delivered()
    # The global emission exists but no client has acknowledged transport.
    good=p.snapshot();bad=copy.deepcopy(good)
    bad['outbox'][eid]['state']=DeliveryState.ACKNOWLEDGED.value
    bad['outbox'][eid]['ack_count']=1
    with pytest.raises(ValueError,match='(?:FORGED|UNWITNESSED|INCONSISTENT|ACK)'):
        p.restore(bad)
    assert p.snapshot()==good


def test_I09_forged_revocation_tombstone_must_not_create_client_history():
    p,eid=strict_queued('A');good=p.snapshot();bad=copy.deepcopy(good)
    # An attacker can recompute an *unkeyed* journal SHA256. A fabricated
    # revoked-set membership must not itself prove historical authorization.
    bad['revoked_viewers'][eid]=['B']
    key=durable_delivery_id(eid,'B')
    bad['client_deliveries'][key]={"event_id":eid,"viewer_id":"B","delivery_id":key,
        "state":"NOT_SENT","attempts":0,"ack_count":0,"last_attempt_id":None}
    with pytest.raises(ValueError,match='(?:UNAUTHORIZED|FORGED|HISTORY|REVOK)'):
        p.restore(bad)
    assert p.snapshot()==good


def test_I10_fixture_mutation_and_ACK_never_prove_human_perception():
    p,eid=strict_acked()
    p.projection.perceived['V']=[eid]
    assert not p.projection.has_perceived('V',eid)
    assert not p.projection.perceive('V',eid,perception_witness=True)
    with pytest.raises(ValueError,match='NO_PERCEPTION_OWNER'):p.validate_state()


def test_I11_rehashed_unknown_viewer_cold_restore_fails(tmp_path):
    p,eid=strict_queued('A');j=Journal(tmp_path/'j.json');j.commit(p)
    raw=json.loads(j.path.read_text());k=durable_delivery_id(eid,'Ghost')
    raw['state']['client_deliveries'][k]={"event_id":eid,"viewer_id":"Ghost","delivery_id":k,
        "state":"NOT_SENT","attempts":0,"ack_count":0,"last_attempt_id":None}
    raw['state_digest']=_hash(raw['state']);j.path.write_text(json.dumps(raw))
    run_cold("""import sys
from outbox_prototype import Journal
try:Journal(sys.argv[1]).recover()
except ValueError as e:
    assert 'UNAUTHORIZED_CLIENT_DELIVERY' in str(e),str(e)
else:raise AssertionError('forged receipt survived')
""",j.path)


@pytest.mark.parametrize('crash_boundary',["BEFORE_RENAME","AFTER_COMMIT"])
def test_I12_actual_os_exit_crash_boundaries_preserve_atomic_valid_state(tmp_path,crash_boundary):
    p,eid=strict_queued();j=Journal(tmp_path/'j.json');j.commit(p)
    old=j.recover().snapshot()
    # modify with valid client delivery; os._exit inside actual child Journal.commit.
    run=subprocess.run([sys.executable,'-c',"""import sys
from outbox_prototype import Journal
j=Journal(sys.argv[1]);p=j.recover();e='OCC-0001'
assert p.outbox.deliver_to(e,'V')
j.commit(p,crash_boundary=sys.argv[2]);raise AssertionError('did not crash')
""",str(j.path),crash_boundary],cwd=Path(__file__).parent,text=True,capture_output=True,timeout=14)
    assert run.returncode==79,(run.stdout,run.stderr,run.returncode)
    new=j.recover().snapshot()
    if crash_boundary=="BEFORE_RENAME":assert new==old
    else:
        assert new!=old
        assert new['client_deliveries'][durable_delivery_id(eid,'V')]['state']==DeliveryState.DELIVERED_UNACKED.value


def test_I13_cold_rehashed_aggregate_ACK_without_client_receipt_refused(tmp_path):
    p,eid=strict_delivered('V');j=Journal(tmp_path/'aggregate-forgery.json');j.commit(p)
    raw=json.loads(j.path.read_text());raw['state']['outbox'][eid]['state']=DeliveryState.ACKNOWLEDGED.value
    raw['state']['outbox'][eid]['ack_count']=1
    raw['state_digest']=_hash(raw['state']);j.path.write_text(json.dumps(raw))
    run_cold("""import sys
from outbox_prototype import Journal
try:Journal(sys.argv[1]).recover()
except ValueError:pass
else:raise AssertionError('rehashed aggregate ACK accepted without client ACK')
""",j.path)


def test_I14_cold_rehashed_revocation_tombstone_cannot_create_zero_attempt_receipt(tmp_path):
    p,eid=strict_queued('A');j=Journal(tmp_path/'tombstone-forgery.json');j.commit(p)
    raw=json.loads(j.path.read_text());k=durable_delivery_id(eid,'B')
    raw['state']['revoked_viewers'][eid]=['B']
    raw['state']['client_deliveries'][k]={"event_id":eid,"viewer_id":"B","delivery_id":k,
        "state":"NOT_SENT","attempts":0,"ack_count":0,"last_attempt_id":None}
    raw['state_digest']=_hash(raw['state']);j.path.write_text(json.dumps(raw))
    run_cold("""import sys
from outbox_prototype import Journal
try:Journal(sys.argv[1]).recover()
except ValueError:pass
else:raise AssertionError('rehashed fabricated historical client receipt accepted')
""",j.path)
