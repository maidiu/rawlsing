"""Reviewer-owned cold-process proof; never relies on author test helper."""
import json,os,sys
from pathlib import Path
from outbox_prototype import Journal,durable_delivery_id

C={'candidate_id':'RTO','payload':{'utterance':'Hello'},'source_refs':['SYNTHETIC_RTO'],'causal_time':'2026-10-14T20:00:00'}
D={'candidate_id':'RTO-SECOND','payload':{'utterance':'Hello again'},'source_refs':['SYNTHETIC_RTO'],'causal_time':'2026-10-14T20:01:00'}
mode,path=sys.argv[1],Path(sys.argv[2]);j=Journal(path)
if mode=='kill_before':
    j.admit_and_queue(C,'A',crash_boundary='BEFORE_RENAME')
    raise RuntimeError('missing crash')
elif mode=='kill_after':
    j.admit_and_queue(C,'A',crash_boundary='AFTER_COMMIT')
    raise RuntimeError('missing crash')
elif mode=='kill_second_before':
    j.admit_and_queue(D,'B',crash_boundary='BEFORE_RENAME')
    raise RuntimeError('missing crash')
elif mode=='read_empty':
    p=j.recover();assert p.ledger.count()==0;assert not p.outbox.deliveries and not p.outbox.client_deliveries
    print(json.dumps({'status':'BEFORE_NONCOMMIT','events':0}))
elif mode=='read_durable':
    p=j.recover();assert p.ledger.count()==1;assert p.ledger.get('OCC-0001')['candidate_id']=='RTO'
    assert p.outbox.deliveries['OCC-0001']['state']=='ADMITTED_UNDELIVERED'
    did=durable_delivery_id('OCC-0001','A');assert p.outbox.client_deliveries[did]['attempts']==1
    assert not p.projection.has_perceived('A','OCC-0001')
    print(json.dumps({'status':'AFTER_DURABLE','events':1,'delivery':did}))
else: raise ValueError(mode)
