"""Capture complete actual entrypoint outputs and native call/return preimages."""
from pathlib import Path
import sys,json,gzip,hashlib
HERE=Path(__file__).resolve().parent
sys.path[:0]=[str(HERE),str(HERE/'inputs/port'),str(HERE/'inputs/sc0f/repro'),str(HERE/'inputs/port/staging/ns')]
from sc0f3.adapter import TwoContractAdapter,provider_equivalence_report
from sc0f3.providers import ProviderA,ProviderB
from sc0f3.fixture_owner import reversal_fixture_permit
from sc0f3.receipts import verify
from sc0f3.common import digest
out=HERE/'proof'/sys.argv[1];out.mkdir(parents=True,exist_ok=False)
rows=[]
for name,provider,variant,reverse in [('baseline_A',ProviderA,'54_6',False),('baseline_B',ProviderB,'54_6',False),('changed_A',ProviderA,'50_10',False),('changed_B',ProviderB,'50_10',False),('reverse_A',ProviderA,'54_6',True),('reverse_changed_A',ProviderA,'50_10',True)]:
 ad=TwoContractAdapter(provider(variant=variant))
 b=ad.request_role_reversal(reversal_fixture_permit(variant)) if reverse else ad.run()
 if not reverse:assert verify(b)
 raw=json.dumps(b,sort_keys=True,separators=(',',':')).encode()
 path=out/(name+'.json.gz')
 path.write_bytes(gzip.compress(raw,mtime=0))
 n=b['native_computation'];calls={}
 for c in n['calls']:calls[c['function']]=calls.get(c['function'],0)+1
 rows.append(dict(name=name,artifact=path.name,uncompressed_sha256=hashlib.sha256(raw).hexdigest(),compressed_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),native_support=n['support'],native_completed_calls=calls,actual_source_values_read=len(n['values_read'])))
 print(name,n['support'],calls,flush=True)
a=json.loads(gzip.decompress((out/'baseline_A.json.gz').read_bytes()))
b=json.loads(gzip.decompress((out/'baseline_B.json.gz').read_bytes()))
assert provider_equivalence_report(a,b)['equivalent_except_physical_lineage']
assert provider_equivalence_report(json.loads(gzip.decompress((out/'changed_A.json.gz').read_bytes())),json.loads(gzip.decompress((out/'changed_B.json.gz').read_bytes())))['equivalent_except_physical_lineage']
summary=dict(schema='SC0F3_ACTUAL_NATIVE_ENTRYPOINT_PROOF@1',runs=rows,full_AB_equivalence=True,real_source_operations=0,model_calls=0,actor_calls=0,grade='SOURCEFREE_INTERFACE_CANDIDATE')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
