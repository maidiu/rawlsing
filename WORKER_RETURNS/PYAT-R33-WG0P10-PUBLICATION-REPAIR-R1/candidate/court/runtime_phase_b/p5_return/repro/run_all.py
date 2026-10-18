import os,pathlib,subprocess,json,time,xml.etree.ElementTree as ET,hashlib,sys
R=pathlib.Path(__file__).resolve().parents[1];V=R/'review';C=V/'runtime_phase_b/candidate';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',PYTHONPATH=os.pathsep.join([str(V/'repro'),str(C/'pinned')]),WG0L_PHASE_B_ADAPTER='phase_b_adapter_p5')
failed=[]
def clean(s):return s.replace(str(R.parents[1]),'<WORKTREE>').replace(str(pathlib.Path.home()),'<HOME>')
def run(name,args):
 t=time.time();p=subprocess.run(args,cwd=R,env=env,text=True,capture_output=True)
 if p.returncode:failed.append((name,p.returncode))
 raw=R/'runtime/raw_logs';raw.mkdir(parents=True,exist_ok=True);(raw/(name+'.stdout')).write_text(p.stdout+p.stderr)
 (R/'observations'/(name+'.stdout')).write_text(clean(p.stdout+p.stderr));d={'command':[clean(x) for x in args],'exit':p.returncode,'seconds':time.time()-t,'candidate_sha256':hashlib.sha256((C/'repro/wg0p4_workload.py').read_bytes()).hexdigest(),'claim_grade':'WG0P5_IMPLEMENTER_REPRODUCTION_ONLY_NOT_INDEPENDENT_ACCEPTANCE'}
 xml=R/'observations'/(name+'.xml')
 if xml.exists():
  tree=ET.parse(xml);d.update(tests=len(tree.findall('.//testcase')),failures=len(tree.findall('.//failure')),errors=len(tree.findall('.//error')),skips=len(tree.findall('.//skipped')));xml.write_text(clean(xml.read_text()))
 (R/'observations'/(name+'.terminal.json')).write_text(json.dumps(d,indent=2)+'\n');print(name,json.dumps(d),flush=True);print((p.stdout+p.stderr)[-1100:],flush=True)
for name in sys.argv[1:]:
 if name=='prepare':run(name,[sys.executable,str(V/'repro/prepare_inherited_v1.py')]);continue
 if name=='author_inputs':run(name,[sys.executable,str(R/'repro/prepare_author_inputs.py')]);continue
 if name=='author':run(name,[sys.executable,str(C/'repro/run_suites.py'),'prepare_native','wg0p4','historical_p2','historical_p3']);continue
 tests={'descriptor':[V/'tests/phase_b/test_descriptor_p5_v1.py'],'frozen65':[V/'tests/test_precommitted_phase_b.py'],'inherited':[V/'tests/phase_b/test_original_j_adapter_v1.py',V/'tests/phase_b/test_original_k_adapter_v1.py',V/'tests/phase_b/test_documented_k_contracts_v1.py'],'owners80':[V/'runtime_phase_b/owner_tests']}[name]
 run(name,[sys.executable,'-m','pytest','-c',str(C/'pytest.ini'),*[str(x) for x in tests],'-vv','--tb=short','--junitxml='+str(R/'observations'/(name+'.xml'))])

if failed:
 print('FAILED subprocesses:',failed,flush=True)
 sys.exit(1)
