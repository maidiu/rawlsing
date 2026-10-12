import os,sys,time
sys.path.insert(0,'/Users/matthewsmith/Desktop/Rawlsing_Worktrees/hq280-b01dr')
from pathlib import Path
from rawlsing_next import pre553_batch_durable_checkpoint_candidate as cp
import importlib
T=importlib.import_module('rawlsing_next.tests.test_pre553_batch_durable_checkpoint_candidate')
man=T._manifest(3);ident=T._identity(man)
rec=cp.UnitRecord(unit_key=ident.unit_keys[0],unit_ref=cp.ExactRef('Unit','urn:x',__import__('hashlib').sha256(b'u').hexdigest()),state=cp.UNIT_STATE_INTENT,attempt_index=1,intent_hash=__import__('hashlib').sha256(b'i').hexdigest(),receipt_projection=None,receipt_hash=None)
ck=cp.DurableCheckpoint(identity=ident,records=(rec,))
st=cp.DurableCheckpointStore(Path(sys.argv[1]));st.save(ck)
print('PERSISTED',flush=True)
time.sleep(5)
