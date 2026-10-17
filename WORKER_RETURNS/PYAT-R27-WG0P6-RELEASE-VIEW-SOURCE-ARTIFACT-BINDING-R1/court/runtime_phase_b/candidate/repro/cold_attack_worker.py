"""A fresh untrusted checkpoint reader; trusted fixture owner is provisioned separately."""
import json,pathlib,sys
from common_v1 import w,plan
owner_dir,cpfile,variant=sys.argv[1:]
if variant=='source_leaf':w.COHORTS['REL-A-W1']['rows'][0]['responses']['Q-ORD-A']='3'
owner=w.FixtureOwner(owner_dir);calls=[]
def trace(frame,event,arg):
    if event=='call' and frame.f_code.co_name in ['execute_empirical_query','run'] and 'pinned/rawlsing_next/' in frame.f_code.co_filename:calls.append(frame.f_code.co_name)
sys.settrace(trace)
try:
    p=plan(releases=w.build_all_releases(fixture_owner=owner))
    cp=w.ColdCheckpoint.from_json(pathlib.Path(cpfile).read_text(),fixture_owner=owner)
    result=w.resume_plan(p,cp,w.make_executor(p))
    out={'accepted':True,'remaining':result['remaining_units'],'actual_owner_calls':calls}
except (w.IdentityError,w.ColdRestartError,w.RevocationError) as e:out={'accepted':False,'exception':type(e).__name__,'reason':str(e),'actual_owner_calls':calls}
sys.settrace(None);print(json.dumps(out))
