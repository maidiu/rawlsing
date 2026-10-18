"""Fresh-process writer. Pauses are test instrumentation; source bytes untouched."""
from pathlib import Path
import json, os, sys
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
from probe_e2 import tables
v=json.loads(Path(sys.argv[1]).read_text())
b=m.Bridge(sys.argv[2],witnesses=[v['witness']],capability_witnesses=v['registry'])
sql=[]
def trace(statement):
    sql.append(statement)
    if statement=='BEGIN IMMEDIATE' and v.get('observe_lock'):
        print('BEGIN_REQUESTED',flush=True)
    pause=v.get('pause')
    match=(pause=='ingress' and statement.startswith('INSERT INTO b2_event_identity')) or (pause=='identity' and statement=='COMMIT')
    if match:
        print(json.dumps(dict(paused=pause,in_transaction=b.store.db.in_transaction,local=tables(b.store.db))),flush=True)
        sys.stdin.readline()
b.store.db.set_trace_callback(trace)
if v.get('pause')=='occurrence':
    original=b.store.admit_fixture
    def after_occurrence(event):
        result=original(event)
        print(json.dumps(dict(paused='occurrence',in_transaction=b.store.db.in_transaction,local=tables(b.store.db))),flush=True)
        sys.stdin.readline()
        return result
    b.store.admit_fixture=after_occurrence
print(json.dumps(dict(ready=True,pid=os.getpid(),isolation_level=b.store.db.isolation_level)),flush=True)
sys.stdin.readline()
receipt=b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],**v.get('kwargs',{}))
print(json.dumps(dict(receipt=receipt,sql=sql,tables=tables(b.store.db),pid=os.getpid())),flush=True)
b.close()
