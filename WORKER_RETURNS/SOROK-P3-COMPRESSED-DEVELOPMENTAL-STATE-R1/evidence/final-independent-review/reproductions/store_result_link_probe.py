import sys, tempfile
from pathlib import Path
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1')
sys.path.insert(0,'WORKER_RETURNS/SOROK-P3-COMPRESSED-DEVELOPMENTAL-STATE-R1/tests')
sys.path.insert(0,'WORKER_RETURNS/SOROK-DEVELOPMENTAL-RECURSION-ENGINE-R1')
import test_state_store as T
root=Path(tempfile.mkdtemp(prefix='p3-store-link-'))
store=T.opened(root); ctx=T.ready(store); receipt=T.committed(store,ctx)
# exact result with effects_receipt_hash present is accepted
good=T.result_for(store,ctx,receipt)
op=store.finish('op-1',good)
print('good accepted phase',op['phase'])
store.close()
# new store / operation; omit the only linkage field and mutate accessible/receipt_ref
store=T.opened(root,'forged.sqlite'); ctx=T.ready(store); receipt=T.committed(store,ctx)
forged=T.result_for(store,ctx,receipt)
forged['consequences'].pop('effects_receipt_hash',None)
forged['accessible']={'forged_actor_surface':True}
forged['receipt_ref']='P3:forged'
try:
    op=store.finish('op-1',forged)
    print('FORGED ACCEPTED phase',op['phase'],'receipt_ref',op['result']['receipt_ref'],'accessible',op['result']['accessible'])
except Exception as e:
    print('forged refused',type(e).__name__,str(e))
print('verify',store.verify())
store.close()
