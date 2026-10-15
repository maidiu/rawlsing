"""Run each exact prior suite in its own interpreter; relocate harness paths only."""
from pathlib import Path
import os,sys,json,hashlib,time
HERE=Path(__file__).resolve().parent
INPUT=HERE/'inputs';PORT=INPUT/'port';NS=PORT/'staging/ns'
sys.path[:0]=[str(HERE),str(PORT),str(NS),str(NS/'rawlsing_next/tests'),str(INPUT/'sc0f/repro')]
os.environ['SC0_PORT_ROOT']=str(PORT)
os.environ['HQ297_EXACT_PE_ROOT']=str(NS)
name=sys.argv[1]
out=HERE/'runs'/name;out.mkdir(parents=True,exist_ok=False)
os.environ['RC0_RETURN']=str(out)
# Exact old reviewer harness embeds a prior host's disposable staging root.
# Redirect those reads only; candidate functions, assertions and frozen bytes unchanged.
orig_read=Path.read_text
redirects={
 '/tmp/wg0p/.sc0i_tmp/tests/test_sc0f_repair.py':INPUT/'sc0f/repro/tests/test_sc0f_repair.py',
 str(out/'runtime_root/WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1/oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json'):PORT/'oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json',
 str(out/'runtime_root/WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1/oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json'):PORT/'oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json',
}
def relocated_read(self,*a,**kw):return orig_read(redirects.get(str(self),self),*a,**kw)
Path.read_text=relocated_read
(out/'repro').mkdir()
tests={
 'old_sc0f':[INPUT/'sc0f/repro/tests/test_sc0f_repair.py'],
 'old_sc0i':[INPUT/'sc0i/repro/test_sc0i_hostiles.py'],
 'old_i2':[INPUT/'i2/repro/test_i2_sc0_hostiles.py'],
 'old_rc0':[INPUT/'rc0/reviewer_tests/test_rc0_hostile.py'],
 'k9':[PORT/'port/test_k9_provider_swap.py'],
 'k10':[PORT/'port/test_k10_structural_conservation.py'],
 'n10e_c1':[NS/'rawlsing_next/tests/test_pre553_empirical_possibility_provider.py',NS/'rawlsing_next/tests/test_pre553_analytical_composition.py'],
 'pe_author':[NS/'rawlsing_next/tests/test_postastra_pe_generic_world_possibility.py'],
 'pe_independent':[NS/'rawlsing_next/tests/test_hq297_k9k10_sc0_pe_independent.py'],
 'candidate':[HERE/'tests'],
}
import pytest
candidate_bindings='--candidate-bindings' in sys.argv
if candidate_bindings:
 import types
 import port,sc0f
 import sc0f3.adapter as candidate_adapter
 import sc0f3.producer as candidate_producer
 import sc0f3.providers as candidate_providers
 from sc0f3.common import Hold
 sys.modules['port.adapter']=candidate_adapter
 port.adapter=candidate_adapter
 for suffix,cls in [('a',candidate_providers.ProviderA),('b',candidate_providers.ProviderB)]:
  module=types.ModuleType('port.provider_'+suffix)
  module.ProviderA=cls;module.ProviderB=cls
  setattr(module,'build_provider_'+suffix,cls)
  sys.modules['port.provider_'+suffix]=module
  setattr(port,'provider_'+suffix,module)
 # Removed unsafe enrollment/bridge APIs remain absent; no compatibility
 # grant-minting stub or fake producer method is supplied to green old tests.
 retired=types.ModuleType('sc0f.adapter')
 retired.SC0FTwoContractAdapter=candidate_adapter.TwoContractAdapter
 retired.SC0FError=Hold
 sys.modules['sc0f.adapter']=retired;sc0f.adapter=retired
 sys.modules['sc0f.producer_bridge']=candidate_producer
 sc0f.producer_bridge=candidate_producer
start=time.time();code=pytest.main(['-q','--tb=short','--rootdir='+str(HERE),'--confcutdir='+str(HERE),*map(str,tests[name.split('__')[0]]),'--junitxml='+str(out/'junit.xml')])
mods=[]
for n,m in sorted(sys.modules.items()):
 f=getattr(m,'__file__',None)
 if f and n.startswith(('rawlsing_next.','port.','sc0f.','sc0f3.')):
  p=Path(f)
  if p.suffix=='.py' and p.is_file():
   b=p.read_bytes();mods.append(dict(module=n,file=str(p.resolve().relative_to(HERE)),sha256=hashlib.sha256(b).hexdigest(),git_blob_sha1=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()))
(out/'execution.json').write_text(json.dumps(dict(suite=name,candidate_import_bindings=candidate_bindings,exit_code=int(code),seconds=time.time()-start,imports=mods,relocations={k:str(v.relative_to(HERE)) for k,v in redirects.items()}),indent=2)+'\n')
raise SystemExit(code)
