from pathlib import Path
import os,json,subprocess
r=Path('/tmp/rawlsing-oct28-p1r2');packet=r/'packet';python='/tmp/rawlsing-oct28-p1r1/venv/bin/python'
env=dict(os.environ,PATH='/tmp/rawlsing-oct28-p1r1/venv/bin:'+os.environ['PATH'],PYTHONPATH='.'+os.pathsep+str(packet),PYTHONHASHSEED='0',PYTHONDONTWRITEBYTECODE='1',LC_ALL='C')
env.pop('RAWLSING_C11_ACCELERATOR_DIR',None)
opts=['-q','-o','addopts=','-p','no:cacheprovider'];pytest=[python,'-m','pytest'];results=[]
def run(label,cut,args,expected=0,needle=None,cache=None):
 active=dict(env)
 if cache:active['RAWLSING_C11_ACCELERATOR_DIR']=str(r/cache)
 with (r/'evidence'/f'{label}.log').open('w') as log:
  p=subprocess.run(args,cwd=r/cut,env=active,stdout=log,stderr=subprocess.STDOUT)
 text=(r/'evidence'/f'{label}.log').read_text()
 entry=dict(label=label,cut=cut,argv=args,exit=p.returncode,expected=expected,required_output=needle,ok=p.returncode==expected and (needle is None or needle in text))
 results.append(entry);(r/'evidence/commands.json').write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(entry),flush=True)
 if not entry['ok']:raise SystemExit(1)
run('original-alias-exploit','original',[python,str(packet/'probe_selector_ref_alias.py')],needle='"changed_provenance_contains_forged_hash": true')
run('original-integrity-RED','original',pytest+[str(packet/'test_selector_ref_integrity.py')]+opts,1,'1 failed')
run('fixed-integrity-GREEN','p1',pytest+[str(packet/'test_selector_ref_integrity.py')]+opts,needle='1 passed')
run('fixed-unchanged-exploit-refused','p1',[python,str(packet/'probe_selector_ref_alias.py')],1,'no exercised selector changed a downstream fact')
run('native-baseline-control','base',[python,str(packet/'probe_native_ref_baseline.py')],needle='PASS baseline')
run('related-suite','p1',['bash',str(r/'inputs/related-suite-command.sh')],needle='209 passed, 1 skipped')
focused=['test_pre553_c11_execution_view.py','test_pre553_route_b_production.py','test_pre553_source_backed_c11_facade.py','test_pre553_source_backed_c11_facade_multi_owner_r1.py','test_pre553_source_backed_c11_facade_multi_owner_qualification_r1.py']
run('focused','p1',pytest+['rawlsing_next/tests/'+name for name in focused]+opts,needle='42 passed')
run('independent-courts','p1',pytest+[str(packet/'test_independent_review.py')]+opts+['-s'],needle='9 passed')
forced=['test_pre553_empirical_query.py','test_pre553_query_frontier_hostile.py','test_pre553_discovery_exact.py']
run('forced-compact','p1',pytest+['rawlsing_next/tests/'+name for name in forced]+['-p','force_compact']+opts,needle='60 passed')
run('cache-sever-restore','p1',[python,str(packet/'cache_red_restore.py')],needle='HASH_CHECK_RESTORED_PASS')
run('p41-first-consumer','p1',pytest+['rawlsing_next/tests/test_universal_world_binding.py::test_same_source_r04_partial_resume_reaches_actual_p41']+opts,needle='1 passed',cache='p41-cache')
for cut in ['base','p1']:
 dest=r/'evidence'/('native-'+cut);dest.mkdir()
 run('native-'+cut,cut,[python,str(r/'inputs/capture_native.py'),str(r/'inputs/same-source.sav'),str(dest)],cache='native-cache' if cut=='p1' else None)
print('INDEPENDENT_TEST_AND_CAPTURE_COMMANDS_COMPLETE',flush=True)
