"""Add only absent exact source-free Python blobs; never overwrite an owner."""
import ast,hashlib,json,pathlib,subprocess
ROOT=pathlib.Path.cwd();OUT=ROOT/'WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1'
P01='73d45f3ac6a50fbee6666ad3a5023840f01ef196';P04='c98e888166a941a06ad694411911bc58f9c4639b';S00='ac75c6fc899804b226a0fbd22245cbe0030ce876';GR='d681f3516c847ecb89230272d3647d322e04d6ca'
roots={P01:['rawlsing_next/'+s for s in ['pre553_v2_durable_consumer_integration_candidate.py','tests/test_pre553_v2_durable_consumer_integration_candidate.py','tests/test_pre553_batch_durable_checkpoint_candidate.py','tests/test_pre553_governed_batch_checkpoint_integration_candidate.py','tests/test_pre553_original_workload_v2_verifier_candidate.py','tests/test_pre553_original_workload_v2_mutation_hostiles_candidate.py']],P04:['rawlsing_next/pre553_selected_world_progressive_contract.py','rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py','rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py'],S00:['rawlsing_next/r3_s02_seam_witness.py','rawlsing_next/tests/test_r3_s02_seam_witness.py','rawlsing_next/tests/test_hq286_s00e_s00cr_overlay.py'],GR:['rawlsing_next/tests/test_hq286_s06gr_independent_atomic_review.py']}
seen=set();records=[]
def blob(sha,p):
 result=subprocess.run(['git','show',sha+':'+p],capture_output=True)
 return result.stdout if result.returncode==0 else None

def visit(sha,p):
 if (sha,p) in seen:return
 seen.add((sha,p));data=blob(sha,p)
 if data is None:return
 dest=ROOT/p;existing=dest.exists()
 row=dict(path=p,commit=sha,blob=subprocess.check_output(['git','rev-parse',sha+':'+p],text=True).strip(),sha256=hashlib.sha256(data).hexdigest(),action='EXISTING_EXACT' if existing and dest.read_bytes()==data else 'EXISTING_DIFFERENT_NO_OVERWRITE' if existing else 'COPIED_EXACT_ABSENT')
 records.append(row)
 if existing:return
 dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(data)
 tree=ast.parse(data)
 for n in ast.walk(tree):
  modules=[]
  if isinstance(n,ast.Import):modules=[a.name for a in n.names]
  elif isinstance(n,ast.ImportFrom) and n.module:
   modules=[n.module]
   if n.module in ('rawlsing_next','rawlsing_next.tests'):modules += [n.module+'.'+a.name for a in n.names]
  for name in modules:
   if name.startswith('rawlsing_next.'):
    visit(sha,name.replace('.','/')+'.py')
for sha,paths in roots.items():
 for p in paths:visit(sha,p)
(OUT/'01_PIN_CUSTODY.json').write_text(json.dumps(records,indent=2)+'\n')
print('New exact blobs:',sum(r['action']=='COPIED_EXACT_ABSENT' for r in records))
for r in records:
 if r['action']=='EXISTING_DIFFERENT_NO_OVERWRITE':print('Common-owner different bytes preserved:',r['path'])
