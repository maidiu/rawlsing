"""E04U requirement, actual import, frozen test and Git preimage audit."""
from pathlib import Path
from collections import Counter
import subprocess,json,hashlib,xml.etree.ElementTree as ET,datetime,sys,uuid
R=Path(__file__).resolve().parents[1];O=R/'observations'
def read(p):return json.loads((R/p).read_text())
def dump(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def cases(p):
 return [dict(module=t.get('classname','').rsplit('.',1)[-1],name=t.get('name'),status='FAIL' if t.find('failure') is not None else 'ERROR' if t.find('error') is not None else 'SKIP' if t.find('skipped') is not None else 'PASS') for t in ET.parse(p).getroot().iter('testcase')]
preimages=[];expected={}
for manifest in ['input_manifest.json','primary_input_manifest.json','source_manifest.json']:
 for x in read(manifest):
  b=(R/x['local']).read_bytes();original=subprocess.check_output(['git','show',x['commit']+':'+x['path']],cwd=R)
  assert b==original and digest(b)==x['sha256'] and blob(b)==x['git_blob']
  expected[str((R/x['local']).resolve())]=x['git_blob'];preimages.append(dict(manifest=manifest,**x,verified=True))
frozen=[]
for d in ['product','tests']:
 for p in (R/d).glob('*.py'):
  if p.name=='test_e04u_independent.py':continue
  src=R/'inputs/e04t'/d/p.name;assert p.read_bytes()==src.read_bytes();expected[str(p.resolve())]=blob(p.read_bytes());frozen.append(dict(local=str(p.relative_to(R)),source=str(src.relative_to(R)),sha256=digest(p.read_bytes())))
for p,src in [('repro/common.py','primary/e04s/repro/common.py'),('tests/test_e04s_hostiles.py','primary/e04s/tests/test_e04s_hostiles.py'),('tests/test_full_native_independent.py','primary/e04n/tests/test_full_native_independent.py'),('tests/test_cache_repair_hostiles.py','primary/e04r/tests/test_cache_repair_hostiles.py'),('E04I_ORIGINAL_FROZEN_ORACLE.json','primary/e04n/E04I_ORIGINAL_FROZEN_ORACLE.json'),('01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json','primary/e04s/01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json')]:
 assert (R/p).read_bytes()==(R/src).read_bytes();frozen.append(dict(local=p,source=src,byte_identical=True))
assert digest((R/'01_PRECOMMITTED_NATIVE_GRANT_AND_TWO_CLIENT_ORACLE.json').read_bytes())==(R/'01_FREEZE_SHA256.txt').read_text().strip()
assert (R/'tests/test_e04u_independent.py').read_bytes()==subprocess.check_output(['git','show','e017c2487:'+str(R.relative_to(Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=R,text=True).strip()))/'tests/test_e04u_independent.py')],cwd=R)
counts={'author37':37,'native231':231,'independent51':51,'author_hostiles37':37,'new_hostiles57':57,'lifecycle':40,'reviewer':41}
old={'author37':'primary/e04r/observations/author37.xml','native231':'primary/e04r/observations/native231.xml','independent51':'primary/e04r/observations/independent.xml','author_hostiles37':'primary/e04r/observations/hostiles.xml','new_hostiles57':'primary/e04s/observations/new_hostiles.xml','lifecycle':'inputs/e04t/observations/lifecycle.xml'}
suites={}
for label,n in counts.items():
 cs=cases(O/(label+'.xml'));term=read('observations/'+label+'.terminal.json');assert len(cs)==n
 if label in old:assert Counter((c['module'],c['name']) for c in cs)==Counter((c['module'],c['name']) for c in cases(R/old[label]))
 suites[label]=dict(counts=dict(Counter(c['status'] for c in cs)),tests=n,cases=cs,exit=term['exit'],junit='observations/'+label+'.xml',candidate_sha256=term['candidate_sha256'])
 assert term['candidate_sha256']==digest((R/'product/empirical.py').read_bytes())
base=cases(O/'baseline4.xml');assert len(base)==4 and all(c['status']=='FAIL' for c in base)
closures=[]
for c in base:
 final=next(t for t in suites['new_hostiles57']['cases'] if t['name']==c['name']);closures.append(dict(name=c['name'],baseline='FAIL_ON_E04R',candidate=final['status']))
imports=[];calls=Counter()
for label in [*counts,'baseline4','scientific_probe','f1_f2_probe','ceiling_probe']:
 a=read('observations/'+label+'_process.json')
 for item in a['imports']:
  path=item['file'].replace('<RETURN>',str(R));assert path in expected,(label,path);assert item['git_blob']==expected[path]
  assert digest(Path(path).read_bytes())==item['sha256'];imports.append(dict(process=label,**item,verified=True))
 for item in a['counts']:calls[item['function']]+=item['count']
science=read('observations/scientific_probe.json');source=science['source_reconstruction']
assert source['actual_respondents']==58 and source['actual_events']==232 and source['same_exact_evidence_objects_into_F8']
for n in ['ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','_require_exact_i03_authority_fitness']:assert calls[n]>0,n
cold=[]
for state in ['withdrawn','restored']:
 x=read('observations/e04u_cold_'+state+'_proof.json');assert x['bit_identical'] and len({x['parent_pid'],*x['children']})==3
 cold.append(dict(state=state,**x))
 for k in range(2):
  audit=read('observations/e04u_cold_'+state+'_'+str(k)+'_process.json')
  for m in audit['imports']:
   path=m['file'].replace('<RETURN>',str(R));assert m['git_blob']==expected[path];imports.append(dict(process='independent_cold_'+state+'_'+str(k),**m,verified=True))
for p in O.glob('cold_*_process.json'):
 a=json.loads(p.read_text())
 for m in a['imports']:
  path=m['file'].replace('<RETURN>',str(R));assert m['git_blob']==expected[path] and digest(Path(path).read_bytes())==m['sha256'];imports.append(dict(process=p.stem,**m,verified=True))
for label in ['scientific_probe','f1_f2_probe','ceiling_probe']:assert read('observations/'+label+'.terminal.json')['exit']==0
failed=sum(s['counts'].get('FAIL',0)+s['counts'].get('ERROR',0)+s['counts'].get('SKIP',0) for s in suites.values())
verdict='RED_SOURCEFREE_NATIVE_CURRENT_GRANT' if failed else 'ACCEPT_SOURCEFREE_FULL_NATIVE_E04_CURRENT_GRANT_METHOD_ONLY'
dump('02_REAL_OWNER_IMPORTS_E04S_A1_AND_CACHE_HOSTILES.json',dict(schema='E04U_INDEPENDENT_COURT@1',candidate='79cb8244a5291218bde17142b93fc2419eade396',verdict=verdict,suites=suites,total_tests=sum(counts.values()),inherited=356,E04S=57,author_E04T=40,new_independent=41,historical_baseline_not_counted=True,four_original_closures=closures,source_reconstruction=source,imports=imports,actual_call_counts=dict(calls),same_concrete_C1_to_F8=len(science['actual']['compositions']),cold=cold))
dump('preimage_and_frozen_test_proof.json',dict(preimages=preimages,frozen=frozen,oracle_freeze_commit=subprocess.check_output(['git','rev-parse','4552d2305'],cwd=R,text=True).strip(),fresh_test_freeze_commit=subprocess.check_output(['git','rev-parse','cf3eaa38b'],cwd=R,text=True).strip(),corrected_reviewer_fixture_freeze_commit=subprocess.check_output(['git','rev-parse','e017c2487'],cwd=R,text=True).strip(),candidate_product_exact=True))
print(verdict,dict(total_tests=sum(counts.values()),candidate_fail_error_skip=failed,preimages=len(preimages),imports=len(imports),calls=sum(calls.values())))
