"""Bounded independent processes; original test bytes and owner code unchanged."""
import pathlib,sys,subprocess,os,json,time
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime_root';S=RT/'candidate/runtime_root/source';O=R/'observations';O.mkdir(exist_ok=True)
(RT/'tmp').mkdir(exist_ok=True)
mode=sys.argv[1];label=sys.argv[2] if len(sys.argv)>2 else mode
native=['test_pre553_analytical_composition','test_pre553_analytical_composition_higher_order','test_pre553_empirical_possibility_provider','test_pre553_empirical_query','test_source_backed_positioned_subject_possibility','test_m4_v557_v558_publication_repository','test_m5_runtime_rsc_peer_prior','test_pre553_n9_n10w_progressive_candidate']
targets={'author37':[RT/'candidate/repro/test_product.py'],'native231':[*(S/'rawlsing_next/tests'/(n+'.py') for n in native),S/'tests/test_hq297_n9c_two_field_reader.py'],'independent51':[R/'tests/test_full_native_independent.py'],'author_hostiles37':[R/'tests/test_cache_repair_hostiles.py'],'new_hostiles57':[R/'tests/test_e04s_hostiles.py'],'baseline4':[R/'tests/test_e04s_hostiles.py'],'lifecycle':[R/'tests/test_current_grant_lifecycle.py']}
variant='e04r' if mode=='baseline4' else 'repaired'
if mode in targets:
 args=['-vv','--tb=short','--assert=plain',*map(str,targets[mode]),'--import-mode=importlib','-p','no:cacheprovider','--rootdir='+str(R),'--confcutdir='+str(R),'--basetemp='+str(RT/'tmp'/label),'--junitxml='+str(O/(label+'.xml'))]
 if mode=='baseline4':args+=['-k','current_native_authority_withdrawal']
else:args=['--script',str(R/'repro'/(mode+'.py'))]
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTEST_DISABLE_PLUGIN_AUTOLOAD='1',E04S_VARIANT=variant,E04S_PROCESS_AUDIT=str(O/(label+'_process.json')))
candidate_sha256=__import__('hashlib').sha256((R/'product/empirical.py').read_bytes()).hexdigest()
cmd=[sys.executable,str(R/'repro/pytest_entry.py'),*args];t=time.monotonic();p=subprocess.run(cmd,cwd=R,env=env,capture_output=True,text=True)
(O/(label+'.stdout')).write_text(p.stdout+'\n'+p.stderr)
(O/(label+'.terminal.json')).write_text(json.dumps(dict(candidate_sha256=candidate_sha256,argv=cmd,cwd=str(R),variant=variant,exit=p.returncode,seconds=time.monotonic()-t,env={k:env[k] for k in ['PYTHONDONTWRITEBYTECODE','PYTEST_DISABLE_PLUGIN_AUTOLOAD','E04S_VARIANT','E04S_PROCESS_AUDIT']}),indent=2)+'\n')
print(label,'EXIT',p.returncode);print('\n'.join((p.stdout+p.stderr).splitlines()[-8:]));sys.exit(p.returncode)
