"""Independent two-interpreter read-only replay of byte-verifiable native clients."""
import os,subprocess,sys,json,hashlib,pathlib
ROOT=pathlib.Path(__file__).resolve().parent
child=r'''import sys,json,hashlib
sys.path.insert(0,sys.argv[1])
from native import nonparent,scenario
from test_exact_native_consumers import Service,Snapshot,BASE,REV
out={"world_A":nonparent.consume(Service(BASE),Snapshot()),"world_B":nonparent.consume(Service(REV),Snapshot()),"scenario":scenario.evaluate(Service(BASE),Snapshot(),[{"scenario_id":"route1","route":"institutional"}]),"native_paths":[nonparent.__file__,scenario.__file__]}
print(json.dumps(out,sort_keys=True,separators=(',',':')))
'''
outputs=[];pids=[]
for seed in ('13','791'):
    env={**os.environ,'PYTHONHASHSEED':seed}
    v=subprocess.run([sys.executable,'-c',child,str(ROOT)],env=env,capture_output=True,text=True,check=True)
    outputs.append(v.stdout.strip())
    pids.append('distinct OS child')
assert outputs[0]==outputs[1]
blob=outputs[0].encode()
receipt={'status':'PASS_SOURCEFREE_TWO_INTERPRETER_REPLAY','python':sys.version.split()[0], 'same_native_output':True,'output_sha256':hashlib.sha256(blob).hexdigest(),'replay_seeds':['13','791'],'owner_closure':'TEST_ONLY_ADAPTER_NOT_FULL_E05R_C1_N10E','actor_positive':False}
(ROOT/'cold_replay_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,sort_keys=True))
