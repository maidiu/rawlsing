import datetime,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=pathlib.Path(__file__).resolve().parent
AUTHOR=ROOT/'WORKER_RETURNS/PYAT-R3-HQ287-I01-SOURCEFREE-INTEGRATED-WORLD-LIFECYCLE-R1/repro'
records=[]
suites={'independent':['rawlsing_next/tests/test_hq288_i01r_independent_product.py'],'i01':['rawlsing_next/tests/test_hq287_i01_sourcefree_world_lifecycle.py'],'p01':['rawlsing_next/tests/'+n for n in ('test_pre553_v2_durable_consumer_integration_candidate.py','test_pre553_batch_durable_checkpoint_candidate.py','test_pre553_governed_batch_checkpoint_integration_candidate.py','test_pre553_original_workload_v2_verifier_candidate.py','test_pre553_original_workload_v2_mutation_hostiles_candidate.py')],'p04_s00e':['rawlsing_next/tests/'+n for n in ('test_pre553_selected_world_progressive_contract.py','test_pre553_n9_n10w_progressive_candidate.py','test_r3_s02_seam_witness.py','test_hq286_s00e_s00cr_overlay.py')],'native':['rawlsing_next/tests/'+n for n in ('test_hq286_s06gr_independent_atomic_review.py','test_pre553_s06g_atomic_integrity.py','test_pre553_learned_product_lifecycle.py','test_pre553_learned_product_release.py','test_pre553_s06f_native_owner_security.py')]}
for label,paths in suites.items():
 cmd=[sys.executable,'-m','pytest',*paths,'-q','-p','no:cacheprovider','--junitxml='+str(OUT/(label+'.xml'))]
 if label=='p01':cmd+=['-p','p01_paths']
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(AUTHOR)+os.pathsep+str(ROOT)}
 p=subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(label+'.log')).write_text(p.stdout)
 records.append(dict(label=label,argv=cmd,cwd=str(ROOT),exit=p.returncode,timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat()))
 (OUT/'executions.json').write_text(json.dumps(records,indent=2)+'\n')
 print(label,p.returncode,p.stdout.splitlines()[-1],flush=True)
