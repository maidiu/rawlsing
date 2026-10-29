"""Cold concurrent B3 worker: explicit ready/go barrier, real file and process."""
from pathlib import Path
import json,os,sys
from integration import Integration
from fixture_authority import FixtureAuthority
frame=json.loads(Path(sys.argv[1]).read_text());authority=FixtureAuthority();authority.register_observed(frame)
e=Integration(Path(sys.argv[2]),authority)
print(json.dumps({'ready':True,'pid':os.getpid()}),flush=True)
assert sys.stdin.readline().strip()=='GO'
r=e.run(frame)
print(json.dumps(dict(pid=os.getpid(),receipt=r,snapshot=e.snapshot())),flush=True);e.close()
