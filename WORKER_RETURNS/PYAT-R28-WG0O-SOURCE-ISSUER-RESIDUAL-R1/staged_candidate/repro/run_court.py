"""Explicit fresh-process court runner; records literal commands and exits."""
import hashlib,json,os,subprocess,sys,time
from pathlib import Path
import xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1];C=R/'court'
P=C/'runtime_phase_b/p5_return/review/runtime_phase_b/candidate'
def clean(s):return str(s).replace(str(R.parents[1]),'<WORKTREE>').replace(str(Path.home()),'<HOME>')
name=sys.argv[1]
bootstrap=C/('bootstrap_p5' if name.startswith('baseline') else 'bootstrap_p6')
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',
         PYTHONPATH=os.pathsep.join([str(bootstrap),str(C/'repro')]),WG0M_RUN=name,
         WG0L_PHASE_B_ADAPTER='phase_b_adapter_v1')
if name=='baseline_literal':cmd=[sys.executable,'-B',str(R/'repro/baseline_source_attack.py')]
elif name=='prepare':cmd=[sys.executable,'-B',str(C/'repro/prepare_inherited_v1.py')]
elif name=='author26':cmd=[sys.executable,'-B',str(R/'repro/run_author26.py')]
elif name=='author69':cmd=[sys.executable,'-B',str(R/'repro/run_author69.py')]
elif name=='prepare_native':cmd=[sys.executable,'-B',str(P/'repro/prepare_evidence.py')]
elif name=='author_inputs':cmd=[sys.executable,'-B',str(C/'runtime_phase_b/p5_return/repro/prepare_author_inputs.py')]
else:
 tests={'baseline33':[C/'tests/test_descriptor_delta_frozen.py'],
        'wg0m33':[C/'tests/test_descriptor_delta_frozen.py'],
        'original65':[C/'tests/test_precommitted_phase_b.py'],
        'j44_k11':[C/'tests/phase_b/test_original_j_adapter_v1.py',C/'tests/phase_b/test_original_k_adapter_v1.py'],
        'owners80':[C/'runtime_phase_b/owner_tests'],
        'original3':[C/'tests/p5_mapping/test_original_three_adapter_v1.py'],
        'fresh':[R/'tests/test_source_view_binding.py'],
        'cold_pointer':[R/'tests/test_cold_pointer_process.py'],
        'author69':[P/'tests/test_wg0p4.py']}[name]
 cmd=[sys.executable,'-B','-m','pytest','-c',str(C/'runtime_phase_b/candidate/pytest.ini'),'-vv','--tb=short',
      '--junitxml='+str(R/'observations'/(name+'.xml')),*map(str,tests)]
 if name=='baseline33':cmd+=['-k','release_source_artifact']
start=time.time();proc=subprocess.run(cmd,cwd=C,env=env,capture_output=True,text=True)
(R/'runtime/raw_logs').mkdir(parents=True,exist_ok=True)
(R/'runtime/raw_logs'/(name+'.stdout')).write_text(proc.stdout+proc.stderr)
(R/'observations'/(name+'.stdout')).write_text(clean(proc.stdout+proc.stderr))
record=dict(command=[clean(a) for a in cmd],exit=proc.returncode,seconds=time.time()-start,
            scope='WG0P6_IMPLEMENTER_REGRESSION_NOT_INDEPENDENT_ACCEPTANCE')
xml=R/'observations'/(name+'.xml')
if xml.exists():
 tree=ET.parse(xml);record.update(tests=len(tree.findall('.//testcase')),failures=len(tree.findall('.//failure')),errors=len(tree.findall('.//error')),skips=len(tree.findall('.//skipped')))
 xml.write_text(clean(xml.read_text()))
(R/'observations'/(name+'.terminal.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2));print(clean((proc.stdout+proc.stderr)[-1200:]))
sys.exit(proc.returncode)
