"""Unchanged inherited suites; failures retained, never masked by runner success."""
import os,sys,subprocess,json,time,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'05_REAL_PYTEST_COLD_JUNIT';O.mkdir(exist_ok=True);S=R/'selected'
for name in ['E05R','E05S']:
 p=R/'inherited'/name/'runtime'
 if not p.exists():p.symlink_to(os.path.relpath(S,p.parent))
# Tests use these exact fixture paths; symlinks only transport, not owners.
F=R/'inherited/F6M'
# inherited source already reconstructed at its original relative locations.
suites={
'original_e05':(S,['_e05/tests/test_e05_n9_selected_world.py'],S,[]),
'original_e04':(S,['_e04-candidate/repro/test_product.py'],S,[]),
'original_n9c':(S,['tests/test_hq297_n9c_two_field_reader.py'],S,[]),
'original_publication':(S,['rawlsing_next/tests/test_m4_v557_v558_publication_repository.py','rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py'],S,[]),
'original_empirical':(S,['rawlsing_next/tests/'+n+'.py' for n in ['test_pre553_empirical_possibility_provider','test_pre553_analytical_composition','test_source_backed_positioned_subject_possibility','test_pre553_empirical_query']],S,[]),
'original_progressive':(S,['rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py'],S,[]),
'native_routeB_I4_FF_temporal_admission':(S,['rawlsing_next/tests/'+n+'.py' for n in ['test_pre553_route_b_production','test_pre553_learned_world_composition','test_field_forge_conditional_support','test_m1_admitted_field_forge_relation_v554_ingress','test_m1_temporal_v554_admission_dedup']],S,[]),
'e05r_repair_and_frozen_independent':(R/'inherited/E05R',[str(R/'inherited/E05R/tests')],R/'inherited/E05R/runtime',[R/'inherited/E05R/repro']),
'e05s_independent':(R/'inherited/E05S',[str(R/'inherited/E05S/tests/test_r14_independent.py')],R/'inherited/E05S/runtime',[R/'inherited/E05S/repro']),
'pe2_existing_comparative':(S,[str(R/'inherited/PE2/probe/test_generic_progressive_possibility.py'),str(R/'inherited/PE2/probe/test_generic_c1_multi_conditioner.py')],S,[R/'inherited/PE2/probe']),
'f6m_repair':(F,[str(F/'tests/test_consumer_repair.py')],F/'candidate',[F/'inherited/F6C/02_TESTS']),
'f6m_original35':(F,[str(F/'inherited/F6C/02_TESTS/run/rawlsing_next/tests/test_pre553_heterogeneous_synthesis.py')],F/'candidate',[]),
}
results=[]
for label,(cwd,paths,rt,extra) in suites.items():
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PV2_RUNTIME_ROOT=str(rt),PYTHONPATH=os.pathsep.join(map(str,[rt,rt/'rawlsing_next/tests',rt/'rawlsing_next',*extra])))
 cmd=[sys.executable,'-m','pytest','-q',*paths,'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/(label+'.xml'))]
 t=time.monotonic();p=subprocess.run(cmd,cwd=cwd,env=env,capture_output=True,text=True)
 (O/(label+'.log')).write_text(p.stdout+'\n'+p.stderr)
 row=dict(label=label,argv=cmd,cwd=str(cwd),exit=p.returncode,seconds=time.monotonic()-t,pythonpath=env['PYTHONPATH'])
 if (O/(label+'.xml')).exists():row['junit']=[x.attrib for x in ET.parse(O/(label+'.xml')).getroot().iter('testsuite')]
 results.append(row);(O/'suite_results.json').write_text(json.dumps(results,indent=2)+'\n')
 print(label,p.returncode,p.stdout[-500:],flush=True)
raise SystemExit(int(any(r['exit'] for r in results)))
