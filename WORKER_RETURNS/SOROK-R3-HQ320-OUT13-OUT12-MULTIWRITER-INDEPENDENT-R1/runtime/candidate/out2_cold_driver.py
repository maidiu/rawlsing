"""OUT2 source-free independent cold-process consent/receipt check; no physical client."""
import json,os,sys
from pathlib import Path
from outbox_prototype import Journal,durable_delivery_id
mode,path=sys.argv[1],Path(sys.argv[2]);j=Journal(path)
C={'candidate_id':'OUT2-COLD','payload':{'utterance':'Hi'},'source_refs':['SYNTHETIC'], 'causal_time':'2026-10-14T20:00:00'}
if mode=='crash_before':
    j.admit_and_queue(C,viewer_id='A',crash_boundary='BEFORE_RENAME')
elif mode=='verify_before':
    p=j.recover();assert p.ledger.count()==0
    assert not p.outbox.deliveries and not p.outbox.client_deliveries
    print(json.dumps({'status':'CLEAN_BEFORE'}))
elif mode=='crash_after':
    j.admit_and_queue(C,viewer_id='A',crash_boundary='AFTER_COMMIT')
elif mode=='revoke_after':
    p=j.recover();eid='OCC-0001';did=durable_delivery_id(eid,'A')
    assert p.ledger.count()==1 and p.outbox.client_deliveries[did]['attempts']==1
    assert p.outbox.deliver_to(eid,'A');assert p.projection.offer('A',eid)
    assert p.outbox.revoke_viewer(eid,'A')
    assert not p.projection.has_opportunity('A',eid) and p.outbox.ack_to(eid,'A') is None
    j.commit(p)
    print(json.dumps({'status':'REVOKED_DURABLE','events':p.ledger.count()}))
elif mode=='verify_revocation':
    p=j.recover();eid='OCC-0001';did=durable_delivery_id(eid,'A')
    assert p.ledger.count()==1 and p.outbox.client_deliveries[did]['attempts']==1
    assert p.outbox.deliver_to(eid,'A') is None and p.outbox.ack_to(eid,'A') is None
    assert not p.projection.has_opportunity('A',eid) and not p.projection.has_perceived('A',eid)
    print(json.dumps({'status':'REVOKED_COLD','events':1,'attempts':1}))
else:raise ValueError(mode)
