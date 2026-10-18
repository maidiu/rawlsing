"""Fresh-process B2 entry with real SQLite trace and lock barrier."""
import sys,os,json
from pathlib import Path
sys.path.insert(0,os.environ['B2_REVIEW_ROOT'])
import bridge as m
v=json.loads(Path(sys.argv[1]).read_text());b=m.Bridge(sys.argv[2]);trace=[]
def observe(sql):
 trace.append(sql)
 if sql=='BEGIN IMMEDIATE':print('LOCK_REQUEST',flush=True)
b.store.db.set_trace_callback(observe)
b.witnesses={v['witness']['hash']:v['witness']};b.capability_witnesses=v['registry']
print(json.dumps(dict(ready=True,pid=os.getpid(),isolation=b.store.db.isolation_level)),flush=True)
assert sys.stdin.readline().strip()=='GO'
r=b.advance(v['packet'],v['context'],v['policy'],v['witness'],v['cap'],grant=v['grant'])
print(json.dumps(dict(receipt=r,pid=os.getpid(),trace=trace,module_sha256=m.hashlib.sha256(Path(m.__file__).read_bytes()).hexdigest())),flush=True)
b.close()
