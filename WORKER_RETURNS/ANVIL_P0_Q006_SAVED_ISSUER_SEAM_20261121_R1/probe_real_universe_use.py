#!/usr/bin/env python3
"""Real metadata-only preflight for the scoped historical DEFER universe use."""
from __future__ import annotations
import argparse, hashlib, json
from pathlib import Path
from types import SimpleNamespace
from rawlsing_next.pre553_anvil_stream_carrier_qualification import HeldStreamPins
from rawlsing_next.pre553_anvil_stream_native_i03 import VerifiedAnvilStreamEstate
from rawlsing_next.pre553_anvil_stream_recorded import RecordedUniverseUse
from rawlsing_next.pre553_empirical_objects import AuthorityRef, ExactRef


def ref(v):
    p=v.split('|'); return ExactRef(p[0],p[1],p[2])
def aref(v):
    p=v.split('|'); return AuthorityRef(p[0],p[1],p[2])

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--owner-use-decision',type=Path,required=True)
    ap.add_argument('--owner-decision',type=Path,required=True)
    ap.add_argument('--r2-decision',type=Path,required=True)
    ap.add_argument('--operation-json',type=Path,required=True)
    ap.add_argument('--closure',type=Path,required=True)
    ap.add_argument('--actual-output',type=Path,required=True)
    ap.add_argument('--stream-root',type=Path,required=True)
    ap.add_argument('--release-path',type=Path,required=True)
    a=ap.parse_args()
    use_bytes=a.owner_use_decision.read_bytes(); use_hash=hashlib.sha256(use_bytes).hexdigest()
    if use_hash!='972a56f2f46ec0d5f30d13ae62198df4988755f54016ac65892a288d4848f212':
        raise SystemExit('OWNER_USE_DECISION_HASH_MISMATCH')
    use=json.loads(use_bytes); owner=json.loads(a.owner_decision.read_text()); r2=json.loads(a.r2_decision.read_text())['waves'][owner['source_id']]
    op=json.loads(a.operation_json.read_text()); closure=json.loads(a.closure.read_text()); actual=json.loads(a.actual_output.read_text())
    if len(closure)!=1 or closure[0]['state']!='DEFER': raise SystemExit('HISTORICAL_DEFER_MISSING')
    hist=aref(closure[0]['ref']); pos=AuthorityRef('Q006_RECORDED_UNIVERSE_USE','Q006-USE-'+use_hash[:24],use_hash)
    qref=actual['query_ref']; pref=actual['predicate_ref']
    handle=RecordedUniverseUse(historical_ref=hist,positive_ref=pos,owner_decision_sha256=use_hash,operation_document_sha256=hashlib.sha256(a.operation_json.read_bytes()).hexdigest(),source_root=owner['source_binding']['saved_i02']['source'],release_root=owner['source_binding']['saved_i02']['release'],universe_root=owner['source_binding']['saved_i02']['universe'],replay_root=owner['source_binding']['saved_i02']['replay'],question_ref=ExactRef(op['question_ref']['kind'],op['question_ref']['object_id'],op['question_ref']['content_hash']),query_ref=ExactRef(qref['kind'],qref['object_id'],qref['content_hash']),predicate_ref=ExactRef(pref['kind'],pref['object_id'],pref['content_hash']),scope=use['scope'])
    pins=HeldStreamPins(owner['source_id'],owner['source_binding']['source_sha256'],owner['source_binding']['manifest_sha256'],str(a.release_path),dict(owner['source_binding']['saved_i02']))
    def current(p):
        cur=json.loads(a.owner_decision.read_text()); src=json.loads(a.r2_decision.read_text())['waves'][owner['source_id']]
        return p.manifest_sha256==owner['source_binding']['manifest_sha256'] and src['manifest_sha256']==owner['source_binding']['manifest_sha256'] and cur['source_binding']==owner['source_binding']
    estate=VerifiedAnvilStreamEstate(a.stream_root,exact_path=a.release_path,independently_held=pins,current_authorizer=current)
    universe=next(estate.iter_family('EmpiricalUniverse'))
    q=SimpleNamespace(ref=handle.query_ref); p=SimpleNamespace(ref=handle.predicate_ref)
    auth=handle.authorize(universe,q,p)
    print(json.dumps({'schema':'ANVIL_Q006_UNIVERSE_USE_METADATA_PREFLIGHT@1','status':'PASS','historical_state':'DEFER','historical_identity_retained':auth[0].key!=auth[1].key,'positive_use_identity_retained':auth[1].key==pos.key,'respondent_bodies_read':False,'index_built':False,'private_ids_published':False},indent=2,sort_keys=True))
    return 0
if __name__=='__main__': raise SystemExit(main())
