import datetime,hashlib,json,os,pathlib,platform,resource,subprocess,sys,time,xml.etree.ElementTree as ET
OUT=pathlib.Path(__file__).resolve().parent;ROOT=OUT.parents[2];C=OUT/'composite';F='WORKER_RETURNS/PYAT-R3-HQ289-S00V2-SOURCEFREE-PRODUCER-BINDING-R1/repro'
V='aba2f6a60d21b8daeeaf9eb3cfadef2620ac13f4';expected='cfce198d628298bbc5b4fa46d820f3d2354181c17cb13db3dd29f18d48763cfa'
assert hashlib.sha256((OUT/'SOURCE_SELECTOR.json').read_bytes()).hexdigest()==expected
assert subprocess.check_output(['git','show','5798f545d:WORKER_RETURNS/PYAT-R3-HQ291-S00V3X-INDEPENDENT-OFFLINE-EXECUTION-R1/repro/SOURCE_SELECTOR.json'],cwd=ROOT)==(OUT/'SOURCE_SELECTOR.json').read_bytes()
# Author test read and copied only after independent selector/tests freeze.
for path in ['rawlsing_next/tests/test_hq290_s00v3_offline_binding.py','WORKER_RETURNS/PYAT-R3-HQ290-S00V3-OFFLINE-PRODUCER-BINDING-R1/repro/pinned_accepted_artifact.json']:
 raw=subprocess.check_output(['git','show',V+':'+path],cwd=ROOT);dest=C/path;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','PYTHONPATH':str(C),'PYAT_S00V3R_COMPOSITE_ROOT':str(C),'PYAT_S00V3R_SELECTOR':str(OUT/'SOURCE_SELECTOR.json'),'PYAT_S00V3R_SELECTOR_SHA256':expected}
selected={k:env[k] for k in ['PYTHONDONTWRITEBYTECODE','PYTHONPATH','PYAT_S00V3R_COMPOSITE_ROOT','PYAT_S00V3R_SELECTOR','PYAT_S00V3R_SELECTOR_SHA256']}
script="""import sys,json,hashlib,py_compile
from pathlib import Path
from rawlsing_next import pre553_i01_sourcefree_world_lifecycle_candidate as I
rows=[]
for name,mod in sorted(sys.modules.items()):
 if name.startswith('rawlsing_next.') and getattr(mod,'__file__',None):
  p=Path(mod.__file__).resolve();assert p.is_relative_to(Path(sys.argv[1]).resolve()),str(p)
  compile(p.read_bytes(),str(p),'exec');rows.append(dict(module=name,path=str(p),sha256=hashlib.sha256(p.read_bytes()).hexdigest()))
print(json.dumps(rows,indent=2))
"""
p=subprocess.run([sys.executable,'-c',script,str(C)],cwd=C,env=env,capture_output=True,text=True);(OUT/'loaded_imports.json').write_text(p.stdout);(OUT/'loaded_imports.stderr').write_text(p.stderr);assert p.returncode==0,p.stderr
manifest=json.loads((OUT/'source_manifest.json').read_text());identities={r['path']:r for r in manifest}
for row in json.loads(p.stdout):assert row['sha256']==identities[str(pathlib.Path(row['path']).relative_to(C))]['sha256']
(OUT/'environment.json').write_text(json.dumps(dict(executable=sys.executable,version=sys.version,platform=platform.platform(),uname=list(platform.uname()),selector_pretest_commit='5798f545d',selector_sha256=expected,selected_environment=selected,imports_verified=True),indent=2)+'\n')
suites={'s00v3r_frozen':['test_hq290_s00v3r_offline_custody_method.py'],'i01r_original_26':['test_hq288_i01r_independent_product.py'],'s00v2_71':['test_hq289_s00v2_count_derived_acceptance.py'],'s00v3_author_12':['test_hq290_s00v3_offline_binding.py'],'p04_original_42':['test_pre553_selected_world_progressive_contract.py','test_pre553_n9_n10w_progressive_candidate.py'],'original_s00c_27':[str(C/F/'frozen/test_original_s00c_27.py')],'original_s00cr_16':[str(C/F/'frozen/test_original_s00cr_16.py')],'s00e_revised_27':['test_r3_s02_seam_witness.py'],'s00e_overlay_18':['test_hq286_s00e_s00cr_overlay.py'],'s00v3x_independent':[str(OUT/'test_hq291_s00v3x_independent.py')]}
records=[];cases=[]
for label,names in suites.items():
 paths=[pathlib.Path(n) if n.startswith('/') else C/'rawlsing_next/tests'/n for n in names]
 cmd=[sys.executable,'-m','pytest',*[str(p) for p in paths],'-q','-p','no:cacheprovider','--junitxml='+str(OUT/(label+'.xml'))]
 cwd=C/F/'historical_runtime' if label.startswith('original_s00') or label.startswith('s00e_') else C
 before=resource.getrusage(resource.RUSAGE_CHILDREN);start=time.monotonic()
 p=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 after=resource.getrusage(resource.RUSAGE_CHILDREN);(OUT/(label+'.log')).write_text(p.stdout)
 rows=[]
 if (OUT/(label+'.xml')).exists():
  for t in ET.parse(OUT/(label+'.xml')).iter('testcase'):
   failure=next((ch for ch in t if ch.tag in ['failure','error','skipped']),None)
   row=dict(court=label,classname=t.get('classname'),name=t.get('name'),seconds=t.get('time'),outcome=failure.tag if failure is not None else 'passed',detail=failure.text if failure is not None else None);rows.append(row);cases.append(row)
 records.append(dict(court=label,argv=cmd,cwd=str(cwd),environment=selected,exit=p.returncode,utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),wall_seconds=time.monotonic()-start,user_cpu_seconds=after.ru_utime-before.ru_utime,system_cpu_seconds=after.ru_stime-before.ru_stime,maxrss_cumulative=after.ru_maxrss,tests=[dict(path=str(t),sha256=hashlib.sha256(t.read_bytes()).hexdigest()) for t in paths],outcomes={state:sum(r['outcome']==state for r in rows) for state in ['passed','failure','error','skipped']}))
 (OUT/'executions.json').write_text(json.dumps(records,indent=2)+'\n');(OUT/'per_case_results.json').write_text(json.dumps(cases,indent=2)+'\n')
 print(label,p.returncode,p.stdout.splitlines()[-1],flush=True)
