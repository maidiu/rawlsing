"""Execute genuine fresh-process crash boundaries of the *candidate's own* Journal.
The journal is single-writer source-free F2; no accepted ADP019 owner or transport.
"""
import json,os,sys
from pathlib import Path
from outbox_prototype import Journal,DeliveryState,durable_delivery_id

C={'candidate_id':'ONE','payload':{'utterance':'Hello'},'causal_time':'2026-10-14T19:00:00','source_refs':['SOURCEFREE_FIXTURE']}
def main(mode,filename):
    j=Journal(filename)
    if mode in ('crash_before','crash_after'):
        j.admit_and_queue(C,'viewer-A',crash_boundary={'crash_before':'BEFORE_RENAME','crash_after':'AFTER_COMMIT'}[mode])
        raise AssertionError('crash hook did not execute')
    if mode=='verify_before':
        p=j.recover()
        assert p.ledger.count()==0 and not p.outbox.deliveries and not p.outbox.client_deliveries
        e,err=j.admit_and_queue(C,'viewer-A')
        assert err is None and e['occurrence_id']=='OCC-0001'
        print(json.dumps({'result':'PRECOMMIT_NOT_DURABLE','count_before':0,'new_event':e['occurrence_id']}))
    if mode=='verify_after':
        p=j.recover();eid='OCC-0001';did=durable_delivery_id(eid,'viewer-A')
        assert p.ledger.count()==1 and did in p.outbox.client_deliveries
        assert p.outbox.client_deliveries[did]['attempts']==1
        e,err=j.admit_and_queue(C,'viewer-A')
        assert err is None and e['occurrence_id']==eid
        p=j.recover();assert p.ledger.count()==1 and p.outbox.client_deliveries[did]['attempts']==1
        p.outbox.deliver_to(eid,'viewer-A')
        assert p.outbox.client_deliveries[did]['state']==DeliveryState.DELIVERED_UNACKED.value
        first=p.outbox.client_deliveries[did]['last_attempt_id'];j.commit(p)
        print(json.dumps({'result':'POSTCOMMIT_DURABLE','event_id':eid,'delivery_id':did,'attempt_id':first,'count':1,'perceived':p.projection.has_perceived('viewer-A',eid)}))
    if mode=='lost_ack_retry':
        p=j.recover();eid='OCC-0001';did=durable_delivery_id(eid,'viewer-A')
        before=p.outbox.client_deliveries[did]['last_attempt_id']
        p.outbox.fail_to(eid,'viewer-A')
        again=p.outbox.emit_to(eid,'viewer-A')
        assert again['last_attempt_id']!=before and again['delivery_id']==did and again['attempts']==2
        j.commit(p)
        print(json.dumps({'result':'LOST_ACK_RETRY_AT_LEAST_ONCE','delivery_id':did,'attempts':2,'new_attempt_id':again['last_attempt_id'],'perceived':p.projection.has_perceived('viewer-A',eid)}))
    if mode=='ack_no_perception':
        p=j.recover();eid='OCC-0001';did=durable_delivery_id(eid,'viewer-A')
        p.outbox.deliver_to(eid,'viewer-A');p.outbox.ack_to(eid,'viewer-A');j.commit(p)
        assert not p.projection.has_perceived('viewer-A',eid)
        print(json.dumps({'result':'ACK_NOT_PERCEPTION','delivery_id':did,'state':p.outbox.client_deliveries[did]['state']}))
if __name__=='__main__':main(sys.argv[1],Path(sys.argv[2]))
