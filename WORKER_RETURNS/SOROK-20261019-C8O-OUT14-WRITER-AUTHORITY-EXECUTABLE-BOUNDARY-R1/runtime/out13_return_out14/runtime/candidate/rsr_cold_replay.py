"""Independent subprocess cold replay of exact SR outbox prototype.

IMPORTANT: persistence is performed by THIS HARNESS as a JSON write +
os.replace. It is *not* implemented by SR's in-memory ledger/outbox and does
not prove a transactional event+outbox commit or an fsync guarantee.
"""
from __future__ import annotations
import json,os,sys
from pathlib import Path
from outbox_prototype import make_prototype,DeliveryState


def atomic_persist(p,path):
    destination=Path(path)
    temp=destination.with_suffix('.pending')
    temp.write_text(json.dumps(p.snapshot(),sort_keys=True),encoding='utf-8')
    os.replace(temp,destination)


def recover(path):
    p=make_prototype()
    p.restore(json.loads(Path(path).read_text(encoding='utf-8')))
    return p


def main(mode,filepath):
    if mode=='prepare_committed':
        p=make_prototype()
        event=p.ledger.admit({'candidate_id':'ONE','payload':{'utterance':'Hello'},'source_refs':['SYNTHETIC']})
        p.outbox.emit(event['occurrence_id'])
        atomic_persist(p,filepath)
        os._exit(79)
    if mode=='recover_committed':
        p=recover(filepath)
        assert len(p.ledger.events)==1, p.ledger.events
        event=p.ledger.admit({'candidate_id':'ONE','payload':{'utterance':'Hello'},'source_refs':['SYNTHETIC']})
        assert event['occurrence_id']=='OCC-0001'
        assert p.ledger.count()==1
        assert p.outbox.deliver(event['occurrence_id'])==DeliveryState.DELIVERED_UNACKED
        atomic_persist(p,filepath)
        print(json.dumps({'status':'RECOVERED_COMMITTED','events':p.ledger.count(), 'delivery':p.outbox.deliveries[event['occurrence_id']]['state'],'perceived':p.projection.has_perceived('user-A',event['occurrence_id'])}))
        return
    if mode=='recover_after_delivery':
        p=recover(filepath)
        event=p.ledger.get('OCC-0001')
        assert event
        assert p.outbox.deliver('OCC-0001')==DeliveryState.DELIVERED_UNACKED
        assert p.outbox.ack('OCC-0001')==DeliveryState.ACKNOWLEDGED
        assert p.ledger.count()==1
        assert not p.projection.has_perceived('user-A','OCC-0001')
        print(json.dumps({'status':'ACK_WITHOUT_PERCEPTION_CLAIM','events':p.ledger.count(),'state':p.outbox.deliveries['OCC-0001']['state']}))
        return
    if mode=='prepare_unpersisted':
        p=make_prototype()
        atomic_persist(p,filepath)  # known persisted baseline before admission
        e=p.ledger.admit({'candidate_id':'LOST','payload':{'utterance':'I was here'}})
        assert e
        # No persistence hook exists at OccurrenceLedger.admit(). Crash now.
        os._exit(79)
    if mode=='recover_unpersisted':
        p=recover(filepath)
        assert p.ledger.count()==0
        assert not p.outbox.deliveries
        print(json.dumps({'status':'UNPERSISTED_ADMIT_LOST','events':p.ledger.count(),'outbox':len(p.outbox.deliveries)}))
        return
    raise ValueError(mode)

if __name__=='__main__':
    main(sys.argv[1],sys.argv[2])
