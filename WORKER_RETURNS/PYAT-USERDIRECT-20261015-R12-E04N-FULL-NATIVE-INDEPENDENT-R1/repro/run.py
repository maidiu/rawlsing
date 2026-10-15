from pathlib import Path
import sys,subprocess,os,time,json
R=Path(__file__).resolve().parents[1];RT=R/'runtime_root';C=RT/'candidate';S=C/'runtime_root/source';mode=sys.argv[1];(RT/'tmp').mkdir(exist_ok=True)
env=dict(os.environ,PYTHONPATH=os.pathsep.join(map(str,[C,S,S/'rawlsing_next/tests',R/'repro'])),PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1')
native=['test_pre553_analytical_composition','test_pre553_analytical_composition_higher_order','test_pre553_empirical_possibility_provider','test_pre553_empirical_query','test_source_backed_positioned_subject_possibility','test_m4_v557_v558_publication_repository','test_m5_runtime_rsc_peer_prior','test_pre553_n9_n10w_progressive_candidate']
targets={'author37':[C/'repro/test_product.py'],'native231':[*(S/'rawlsing_next/tests'/(n+'.py') for n in native),S/'tests/test_hq297_n9c_two_field_reader.py'],'independent':[R/'tests']}
cmd=[sys.executable,'-m','pytest',*map(str,targets[mode]),'-vv','--tb=short','--assert=plain','--rootdir='+str(R),'--confcutdir='+str(R),'--basetemp='+str(RT/'tmp'/mode),'--junitxml='+str(R/'observations'/f'{mode}.xml')] if mode in targets else [sys.executable,str(R/'repro'/(mode+'.py')),*sys.argv[2:]]
if mode in targets:env['E04N_AUDIT_DIR']=str(R/'observations'/f'{mode}_process_audits')
t=time.time();p=subprocess.run(cmd,cwd=C,env=env,capture_output=True,text=True);(R/f'observations/{mode}.stdout').write_text(p.stdout+p.stderr);(R/f'observations/{mode}.terminal.json').write_text(json.dumps({'argv':cmd,'cwd':str(C),'PYTHONPATH':env['PYTHONPATH'],'exit':p.returncode,'seconds':time.time()-t},indent=2)+'\n');print(mode,'EXIT',p.returncode);print('\n'.join((p.stdout+p.stderr).splitlines()[-5:]));sys.exit(p.returncode)
