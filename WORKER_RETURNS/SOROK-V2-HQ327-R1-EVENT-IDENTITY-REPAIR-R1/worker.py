"""Fresh interpreter writer; stdin releases independently connected SQLite writer."""
import json, os, sys
from pathlib import Path
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
v=json.loads(Path(sys.argv[1]).read_text())
b=m.Bridge(sys.argv[2],witnesses=[v['witness']],capability_witnesses=v['registry'])
print('READY',flush=True)
sys.stdin.readline()
if v.get('lock_probe'):
    b.store.db.set_trace_callback(lambda sql: print('LOCK_REQUESTED',flush=True) if sql=='BEGIN IMMEDIATE' else None)
if v.get('admission_pause'):
    original=b.store.admit_fixture
    def paused(event):
        value=original(event)
        assert b.store.db.in_transaction
        print('UNCOMMITTED_OCCURRENCE',flush=True)
        sys.stdin.readline()
        return value
    b.store.admit_fixture=paused
r=b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],**v.get('kwargs',{}))
print(json.dumps(r),flush=True)
b.close()
