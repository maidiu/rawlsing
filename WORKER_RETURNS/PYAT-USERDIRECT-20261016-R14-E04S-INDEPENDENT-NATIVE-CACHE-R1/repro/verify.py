"""Terminal E04S evidence audit, including expected genuine RED cases."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET,datetime,platform,sys
R=Path(__file__).resolve().parents[1];O=R/'observations';RT=R/'runtime_root'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def git(*a):return subprocess.check_output(['git',*a],cwd=R).decode().strip()
def suite(name):
 xml=ET.parse(O/(name+'.xml')).getroot();rows=list(xml.iter('testsuite'))
 d={k:sum(int(x.attrib.get(k,0)) for x in rows) for k in ['tests','failures','errors','skipped']}
 d['passed']=d['tests']-d['failures']-d['errors']-d['skipped']
 d['terminal']=json.loads((O/(name+'.terminal.json')).read_text())
 d['cases']=[dict(name=x.attrib['name'],status='FAIL' if x.find('failure') is not None else 'ERROR' if x.find('error') is not None else 'SKIP' if x.find('skipped') is not None else 'PASS',message=x.find('failure').attrib.get('message') if x.find('failure') is not None else None) for x in xml.iter('testcase')]
 return d
manifest=json.loads((R/'source_manifest.json').read_text());assert len(manifest)==100
byfile={str(RT/x['local']):x for x in manifest}
for x in manifest:
 p=RT/x['local'];b=p.read_bytes()
 assert sha(p)==x['sha256'] and hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
for x in json.loads((R/'input_manifest.json').read_text()):assert sha(R/x['local'])==x['sha256']
assert (R/'tests/test_full_native_independent.py').read_bytes()==(R/'inputs/E04N/tests/test_full_native_independent.py').read_bytes()
assert (R/'repro/common.py').read_bytes()==(R/'inputs/E04N/repro/common.py').read_bytes()
assert sha(R/'E04I_ORIGINAL_FROZEN_ORACLE.json')=='9f872f75e128530b8ade0103c11fad5f02a418961acf0cb008bdc37872f4269c'
oracle=R/'01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json'
assert sha(oracle)==(R/'01_ORACLE_SHA256.txt').read_text().split()[0]
assert subprocess.check_output(['git','show','40d0a5e82330bb7a68954a2066e0c9a0de83f224:'+str(oracle.relative_to(R.parents[1]))],cwd=R)==oracle.read_bytes()
counts={n:suite(n) for n in ['baseline51','independent51','author37','native231','author_hostiles37','new_hostiles']}
assert (counts['baseline51']['passed'],counts['baseline51']['failures'])==(49,2)
for n,num in [('independent51',51),('author37',37),('native231',231),('author_hostiles37',37)]:
 assert counts[n]['passed']==num and counts[n]['failures']==0 and counts[n]['terminal']['exit']==0
assert counts['new_hostiles']['passed']==53 and counts['new_hostiles']['failures']==4 and counts['new_hostiles']['terminal']['exit']==1
assert all(x['errors']==x['skipped']==0 for x in counts.values())
failed=[x for x in counts['new_hostiles']['cases'] if x['status']=='FAIL'];assert len(failed)==4 and all('current_native_authority_withdrawal' in x['name'] for x in failed)
imports=[]
for path in O.glob('*_process.json'):
 if path.name.startswith('initial_'):continue
 x=json.loads(path.read_text())
 for mod in x['imports']:
  source=byfile.get(mod['file']);assert source is not None,(path,mod)
  assert mod['git_blob']==source['git_blob'] and mod['sha256']==source['sha256']
  imports.append(dict(process_audit=path.name,**mod,source_commit=source['commit'],source_path=source['path']))
scientific=json.loads((O/'scientific_probe.json').read_text());actual=scientific['actual'];assert scientific['source_reconstruction']['actual_respondents']==58 and scientific['source_reconstruction']['actual_events']==232
assert len(actual['compositions'])==22
assert all(any(c['id'] in f['ids'] and c['evidence_ref'] in f['refs'] for f in actual['F8_actual_inputs']) for c in actual['compositions'])
f1f2=json.loads((O/'F1_F2_exact_both_clients.json').read_text());assert f1f2['control_count']==8
assert all(x['error']=='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH' and not any(y['channel']=='empirical' for y in x['reads_before_refusal']) for x in f1f2['executed_controls'])
authority=json.loads((O/'authority_registry_withdrawal_probe.json').read_text())
assert authority['withheld_registry_exact_resolution']['refused'] and authority['original_request_and_source_binding_unchanged']
assert authority['nonparent']['state']=='OPTIONS_AND_SOURCE_SUPPORT_PRODUCED' and authority['scenario']['state']=='FINITE_PROPOSALS_EVALUATED'
assert not authority['nonparent']['actual_native_call_delta'] and not authority['scenario']['actual_native_call_delta']
assert all(x['state']=='UNAVAILABLE' and x['cells']==[] and x['denominator']==0 for x in authority['cache_miss']['result']['steps'])
for mode in ['scientific_probe','authority_probe','f1_f2_probe','ceiling_probe','cold_first','cold_replay']:assert json.loads((O/(mode+'.terminal.json')).read_text())['exit']==0
cold1=json.loads((O/'cold_first.json').read_text());cold2=json.loads((O/'cold_replay.json').read_text());assert cold1['pid']!=cold2['pid'] and cold2['replay_bit_identical'] and cold2['results']['foreign_process_cache']['refused']
ceiling=json.loads((O/'actual_OC05_ceiling.json').read_text());assert not ceiling['operative_OC05']
old_fail=[x['name'] for x in counts['baseline51']['cases'] if x['status']=='FAIL'];now={x['name']:x['status'] for x in counts['independent51']['cases']};assert all(now[x]=='PASS' for x in old_fail)
result=dict(schema='E04S_INDEPENDENT_NATIVE_CACHE_COURT@1',verdict='RED_SOURCEFREE_NATIVE_AUTHORITY_LIFECYCLE',candidate='97254d0b215b5dd45580dd94608a8ec95ff8b76f',preexecution_freeze_commit='40d0a5e82330bb7a68954a2066e0c9a0de83f224',oracle_sha256=sha(oracle),suites=counts,restored_original_E04N_failures=[dict(name=n,original='FAIL',E04R='PASS') for n in old_fail],new_independent_failures=failed,source_manifest_files=len(manifest),native_imports=imports,dedicated_probe=dict(actual_call_counts=actual['counts'],actual_entry_count=sum(x['count'] for x in actual['counts']),same_concrete_evidence_objects=22,source_reconstruction=scientific['source_reconstruction'],full_evidence='observations/scientific_probe.json'),F1_F2=f1f2,authority_lifecycle_RED=authority,cold=dict(first_pid=cold1['pid'],replay_pid=cold2['pid'],common_results_bit_identical=True,foreign_process_cache_refused=True,fixture_construction_not_durable_renewal=True),OC05=ceiling,full_native_environment='EXECUTED_NO_HOLD',adoption=False)
dump('02_ACTUAL_NATIVE_IMPORTS_OLD_F1_F2_AND_NEW_HOSTILES.json',result)
passport=dict(python=sys.version,executable=sys.executable,platform=platform.platform(),pytest=git('--version'),startup='d50b6acec57713e1589b5950c0f0778c52d387f8',branch=git('branch','--show-current'),origin=git('remote','get-url','origin'),worktree=str(R.parents[1]),requested_model='GPT-6.1 Sol Medium (user assignment; runtime setting not independently inspected)',staged_exact_files=100,native_dependency_files=51,original51_test_sha256=sha(R/'tests/test_full_native_independent.py'),unchanged_native_selector='inputs/E04N/source_selector.json',import_adapter='repro/pytest_entry.py preimports exact six selected product modules; original frozen assertions untouched',suites={n:{k:v for k,v in x.items() if k!='cases'} for n,x in counts.items()},final_candidate_total=413,final_candidate_pass=409,final_candidate_fail=4,errors=0,skips=0,baseline_excluded=dict(passed=49,failures=2),actual_probes={mode:json.loads((O/(mode+'.terminal.json')).read_text()) for mode in ['scientific_probe','authority_probe','f1_f2_probe','ceiling_probe','cold_first','cold_replay']},authority_scope='SOURCEFREE_INDEPENDENT_METHOD_COURT_ONLY',verdict=result['verdict'],verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
passport['git_version']=passport.pop('pytest');passport['pytest_version']=subprocess.check_output([sys.executable,'-m','pytest','--version']).decode().strip()
dump('environment_passport_delta.json',passport)
print(json.dumps({n:{k:x[k] for k in ['tests','passed','failures','errors','skipped']} for n,x in counts.items()},indent=2));print('VERIFIED: exact sources, frozen original51, actual native evidence, old F1/F2 restored, genuine new 4 REDs, distinct-process cold replay')
