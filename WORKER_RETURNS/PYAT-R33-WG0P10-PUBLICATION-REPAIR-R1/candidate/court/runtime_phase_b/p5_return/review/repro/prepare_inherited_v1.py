"""Fresh reviewer baseline and cold/shard evidence for original WG0J assertions."""
import importlib.util,os,subprocess,uuid
import reviewer_common_v1 as common
from phase_b_support_v1 import *
from phase_b_adapter_v1 import Adapter
sys.modules['common']=common
source=C/'pinned/predecessors/j/repro/probe.py'
# Execute the byte-exact original independent probe, with only its named common API mapped.
spec=importlib.util.spec_from_file_location('_reviewer_original_probe',source)
module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
outputs={};logs={}
for mode in ('full','full_again','shard0','shard1'):
 folder=common.R/mode;cmd=[sys.executable,str(R/'repro/phase_b_cold_worker_v1.py'),'full' if mode=='full_again' else mode,str(folder)]
 child=subprocess.run(cmd,capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 logs[mode]={'command':cmd,'exit':child.returncode,'stdout':child.stdout,'stderr':child.stderr}
 if child.returncode:raise RuntimeError(logs[mode])
 outputs[mode]=json.loads((folder/'full.json').read_text())
a=Adapter(O);a.out=common.R/'cold';a.out.mkdir();a.ensure_cold()
x=json.loads((a.cold_folder/'crash.json').read_text());y=json.loads((a.cold_folder/'resume.json').read_text());commands=json.loads((a.cold_folder/'commands.json').read_text())
u=outputs['full'];v=outputs['full_again'];shards=[outputs['shard0'],outputs['shard1']]
receipt_hashes=lambda d:sorted(r['receipt_hash'] for r in d['receipts'])
comparison={'cold_identical_receipts':receipt_hashes(u)==receipt_hashes(v),'cold_identical_values':stripped(u['consumer'])==stripped(v['consumer']),'cold_frontier25':u['frontier']==v['frontier']==O['operations'],'processes':{'checkpoint':commands[0],'resume':commands[1],**logs},'resume':{'summary':y['summary'],'consumer':y['consumer'],'values':stripped(y['consumer'])},'shard_combined_unit_keys_match_full':sorted(k for d in shards for k in d['unit_keys'])==u['unit_keys'],'shard_values_match_full':{k:v for d in shards for k,v in stripped(d['consumer']).items()}==stripped(u['consumer']),'scope':'Actual separate-process source-free shards retain original manifest; nonassigned units receive native BatchDeferred. Only COMPLETED results are combined. No original-source or all-estate claim.','original_receipt_recovered_exactly':x['receipt']==y['restored_receipt'] and x['receipt'] in y['receipts'],'cold_directory':str(a.cold_folder)}
common.dump('cold_comparison.json',comparison)
print(json.dumps({k:v for k,v in comparison.items() if isinstance(v,bool)}))
