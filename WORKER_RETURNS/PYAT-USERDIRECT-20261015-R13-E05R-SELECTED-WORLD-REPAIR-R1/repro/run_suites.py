import os,sys,subprocess,json,pathlib,platform,time,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations';O.mkdir(exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PV2_RUNTIME_ROOT=str(RT),PYTHONPATH=os.pathsep.join(map(str,[RT,RT/'rawlsing_next/tests',RT/'rawlsing_next'])))
suites={
'e05':['_e05/tests/test_e05_n9_selected_world.py'],
'e04':['_e04-candidate/repro/test_product.py'],
'n9c':['tests/test_hq297_n9c_two_field_reader.py'],
'm4_m5':['rawlsing_next/tests/test_m4_v557_v558_publication_repository.py','rawlsing_next/tests/test_m5_runtime_rsc_peer_prior.py'],
'empirical':['rawlsing_next/tests/'+n+'.py' for n in ['test_pre553_empirical_possibility_provider','test_pre553_analytical_composition','test_source_backed_positioned_subject_possibility','test_pre553_empirical_query']],
'e03':['rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py']}
results=[]
for label,paths in suites.items():
 cmd=[sys.executable,'-m','pytest','-q',*paths,'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str(O/(label+'.xml'))];t=time.monotonic()
 p=subprocess.run(cmd,cwd=RT,env=env,capture_output=True,text=True)
 (O/(label+'.log')).write_text(p.stdout+'\n'+p.stderr)
 row=dict(label=label,command=cmd,cwd=str(RT),exit=p.returncode,elapsed_seconds=time.monotonic()-t)
 if (O/(label+'.xml')).exists():row['junit']=[x.attrib for x in ET.parse(O/(label+'.xml')).getroot().iter('testsuite')]
 results.append(row);print(label,p.returncode,p.stdout[-1400:],flush=True)
(R/'environment_passport.json').write_text(json.dumps(dict(python=sys.version,executable=sys.executable,platform=platform.platform(),env={k:env[k] for k in ['PYTHONPATH','PV2_RUNTIME_ROOT','PYTHONDONTWRITEBYTECODE']},suites=results),indent=2)+'\n')
# E05R runner adaptation: never hide a failed child suite behind runner exit 0.
raise SystemExit(int(any(x['exit'] for x in results)))
