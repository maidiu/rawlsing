"""Fresh-process inspection or injected process-death boundary."""
import json,sys,os
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent/'candidate'))
from integration import Integration
from fixture_authority import FixtureAuthority
from developmental_loop import permission_for
path,mode=sys.argv[1:3]
if mode=='inspect':
 e=Integration(path);print(json.dumps(dict(pid=os.getpid(),snapshot=e.snapshot(),middle=e.middle(),integrity=e.db.execute('PRAGMA integrity_check').fetchone()[0])));e.close()
else:
 f=json.loads(Path(sys.argv[3]).read_text());a=FixtureAuthority();a.register_observed(f);e=Integration(path,a)
 def fault(stage):
  if stage==mode:
   print(json.dumps(dict(pid=os.getpid(),stage=stage)),flush=True)
   sys.stdin.readline() # parent issues SIGKILL while staged or public writes exist
 e.fault=fault;p=permission_for(e.middle(),f)
 r=e.run(f,owner_permission=p,registered_permissions=(p,));print(json.dumps(r),flush=True);e.close()
