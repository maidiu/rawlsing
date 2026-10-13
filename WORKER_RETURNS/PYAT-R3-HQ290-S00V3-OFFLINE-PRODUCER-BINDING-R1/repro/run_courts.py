"""Reproduce distinct frozen/successor courts; never filter historical red."""
import datetime,hashlib,json,os,pathlib,subprocess,sys
ROOT=pathlib.Path(__file__).resolve().parents[3];OUT=pathlib.Path(__file__).resolve().parent
FROZEN=ROOT/'WORKER_RETURNS/PYAT-R3-HQ289-S00V2-SOURCEFREE-PRODUCER-BINDING-R1/repro'
suites={'original_s00c_27':[FROZEN/'frozen/test_original_s00c_27.py'],'original_s00cr_16':[FROZEN/'frozen/test_original_s00cr_16.py'],'s00e_revised_27':[ROOT/'rawlsing_next/tests/test_r3_s02_seam_witness.py'],'s00e_overlay_18':[ROOT/'rawlsing_next/tests/test_hq286_s00e_s00cr_overlay.py'],'offline':[ROOT/'rawlsing_next/tests/test_hq290_s00v3_offline_binding.py'],'v2':[ROOT/'rawlsing_next/tests/test_hq289_s00v2_count_derived_acceptance.py'],'p04':[ROOT/'rawlsing_next/tests/test_pre553_selected_world_progressive_contract.py',ROOT/'rawlsing_next/tests/test_pre553_n9_n10w_progressive_candidate.py']}
records=[]
for label,paths in suites.items():
 cmd=[sys.executable,'-m','pytest',*[str(p) for p in paths],'-q','-p','no:cacheprovider','--junitxml='+str(OUT/(label+'.xml'))]
 env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(ROOT)}
 # Historical documentary fixture is isolated here; it is not installed or
 # promoted into the product's real-source authority terrain.
 cwd=FROZEN/'historical_runtime'
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 (OUT/(label+'.log')).write_text(p.stdout)
 records.append(dict(label=label,argv=cmd,cwd=str(cwd),environment={'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(ROOT)},exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),tests=[dict(path=str(t),sha256=hashlib.sha256(t.read_bytes()).hexdigest()) for t in paths]))
 (OUT/'executions.json').write_text(json.dumps(records,indent=2)+'\n');print(label,p.returncode,p.stdout.splitlines()[-1],flush=True)
