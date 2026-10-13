"""Emit an actual product once; use a new directory for each reproduction."""
import json, pathlib, subprocess, sys
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as i
root=pathlib.Path(sys.argv[1]).resolve()
if root.exists():raise SystemExit('REFUSE_EXISTING_EVIDENCE_ROOT')
p,summary=i.build_product(root)
def emit(name,value):i.save_json(root/(name+'.json'),value)
emit('execution_summary',summary)
emit('served_before',i.serve(p))
emit('lifecycle_before',p.lifecycle.export_checkpoint())
emit('selected_receipt',p.selected_receipt.as_dict())
code="""import json,sys
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as i
p,summary=i.build_product(sys.argv[1])
assert not p.calls
print(json.dumps({'summary':summary,'serve':i.serve(p),'producer_calls':p.calls},sort_keys=True))
"""
cmd=[sys.executable,'-c',code,str(root)]
r=subprocess.run(cmd,text=True,capture_output=True)
emit('fresh_process_execution',dict(argv=cmd,exit=r.returncode,stdout=r.stdout,stderr=r.stderr))
if r.returncode:raise SystemExit(r.returncode)
cold=json.loads(r.stdout);assert cold['serve']==i.serve(p)
emit('invalidation_receipt',i.invalidate(p))
try:i.serve(p)
except Exception as exc:emit('current_after_invalidation',{'status':'REFUSED','type':type(exc).__name__,'detail':str(exc)})
else:raise AssertionError('invalidated current served')
q,again=i.build_product(root);assert not q.calls
emit('resume_after_invalidation',{'summary':again,'producer_calls':q.calls})
emit('served_as_of',i.serve(q,historical=True))
print(json.dumps({'status':'EXECUTED_SOURCEFREE_LOCAL_PRODUCT','root':str(root),'subject_ref':p.subject_ref.as_dict(),'release_ref':p.release.ref.as_dict(),'producer_calls':len(p.calls),'fresh_process_exit':r.returncode},sort_keys=True))
