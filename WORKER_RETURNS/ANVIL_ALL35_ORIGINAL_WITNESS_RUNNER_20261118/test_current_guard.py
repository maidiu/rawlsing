#!/usr/bin/env python3
import json,sys,types
from pathlib import Path
HERE=Path(__file__).resolve().parent;CAND=Path(__import__('os').environ['ANVIL_CANDIDATE_TREE']).resolve();sys.path[:0]=[str(CAND),str(HERE)]
from single_pass_handoff import _require_current,CheckpointRefusal
from rawlsing_next.pre553_empirical_objects import ExactRef
class R:
 def __init__(self,state,rev=None):self.state=state;self.rev=rev;self.n=0
 def resolve_current(self,req):
  self.n+=1
  return types.SimpleNamespace(currentness=self.state,revocation_ref=self.rev,decision_ref=req.decision_ref,source_id=req.source_id,source_sha256=req.source_sha256,host=req.host,purpose=req.purpose,consumer_use=req.consumer_use,read_operation=req.read_operation,physical_read_extent=req.physical_read_extent,metadata_freeze_refs=req.metadata_freeze_refs,semantic_use_scope=req.semantic_use_scope)
req=types.SimpleNamespace(decision_ref=ExactRef('TEST_DECISION','d','c'*64),source_id='SRC04',source_sha256='a'*64,host='h',purpose='p',consumer_use='c',read_operation='SOURCE_RESPONSE_DECODE',physical_read_extent='EXACT_FILE',metadata_freeze_refs=(ExactRef('M','m','d'*64),),semantic_use_scope=('S',))
out={}
for name,state,rev in [('held','HELD',None),('revoked','CURRENT_GRANTED',ExactRef('R','r','e'*64))]:
 try:_require_current(R(state,rev),req,req.decision_ref)
 except CheckpointRefusal as e:out[name]=e.code
 else:out[name]='NOT_REFUSED'
(HERE/'CURRENT_GUARD_TEST.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
