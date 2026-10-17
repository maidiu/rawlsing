"""E05R artifact/identity audit; baseline REDs and final results stay distinct."""
import pathlib,hashlib,json,subprocess,datetime,sys,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];RT=R/'runtime';O=R/'observations'
def dump(p,x):(R/p).write_text(json.dumps(x,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def cmd(*a):return subprocess.check_output(a,cwd=R).decode().strip()
def counts(path):
 suites=list(ET.parse(path).getroot().iter('testsuite'))
 return {k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ['tests','failures','errors','skipped']}
m=json.loads((R/'source_manifest.json').read_text());orig=json.loads((R/'original_source_manifest.json').read_text())
assert len(m)==len(orig)==401
changed=[]
for row,old in zip(m,orig):
 b=(RT/row['local']).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob']
 assert sha(RT/row['local'])==row['sha256']
 if row!=old:changed.append(row['local'])
assert changed==['e05_n9_selected_world_adapter.py']
assert (RT/changed[0]).read_bytes()==(R/'candidate/e05r_selected_world_adapter.py').read_bytes()
for x in json.loads((R/'input_manifest.json').read_text()):assert sha(R/x['local'])==x['sha256']
for group,rels in [('e05i',['tests/conftest.py','tests/test_independent_court.py','repro/court_support.py']),('e05',['tests/test_e05_n9_selected_world.py'])]:
 for rel in rels:
  d=R/rel if group=='e05i' else RT/'_e05'/rel
  assert d.read_bytes()==(R/'inputs'/group/rel).read_bytes()
for p in (R/'freezes').iterdir():
 matches=list((R/'inputs').rglob(p.name));assert any(p.read_bytes()==x.read_bytes() for x in matches)
labels=['e05','e04','n9c','m4_m5','empirical','e03']
c={n:counts(O/(n+'.xml')) for n in labels}
c['independent_55']=counts(O/'repaired_independent.xml');c['additional_32']=counts(O/'e05r_additional.xml')
assert sum(c[n]['tests'] for n in labels)==271
assert c['independent_55']['tests']==55 and c['additional_32']['tests']==32
assert all(x['failures']==x['errors']==x['skipped']==0 for x in c.values())
baseline=counts(O/'baseline_independent.xml');assert baseline==dict(tests=55,failures=11,errors=0,skipped=0)
base=ET.parse(O/'baseline_independent.xml').getroot();final=ET.parse(O/'repaired_independent.xml').getroot()
passed={x.attrib['name']:x for x in final.iter('testcase') if x.find('failure') is None and x.find('error') is None}
closure=[]
for tc in base.iter('testcase'):
 if tc.find('failure') is not None:
  assert tc.attrib['name'] in passed
  closure.append(dict(test=tc.attrib['name'],baseline='FAIL',repaired='PASS',frozen_expectation_modified=False))
assert len(closure)==11
dump('01_E05I_ELEVEN_RED_CLOSURE.json',dict(schema='E05R_ELEVEN_RED_EXECUTION_CLOSURE@1',baseline=baseline,repaired=c['independent_55'],closures=closure,adapter_contract='R13_E05R_N9_SELECTED_WORLD_INTERFACE@2',distinct_independent_E05R_adjudication='REQUIRED_NOT_PERFORMED',original_tests_modified=False))
cold=json.loads((O/'cold_exits.json').read_text());assert all(x['exit']==0 for x in cold)
replay=json.loads((O/'independent_cold_replay.json').read_text());assert replay['replay_bit_identical'] and replay['pid']!=replay['first_pid']
zero=json.loads((O/'repair_zero_support.json').read_text())
assert [x['denominator'] for x in zero['empirical_steps']]==[24,8,0]
assert zero['empirical_steps'][-1]['state']=='ZERO_SUPPORT' and zero['empirical_steps'][-1]['cells']==[]
assert zero['state']=='TYPED_PARTIAL_SELECTED_WORLD' and len(zero['native_field_readset']['values_read'])==2
positives={}
for label in ['CURRENT_TEST_CLOCK','HISTORICAL_AS_OF']:
 x=json.loads((O/(label+'.json')).read_text());positives[label]=x
 assert len(x['receipt']['consumers'])==2
 assert all(c['consumer_material']['snapshot_ref']==x['receipt']['snapshot_hash'] for c in x['receipt']['consumers'])
dump('03_TWO_ORIGINAL_CONSUMERS_AND_TYPED_NULL_EXECUTION.json',dict(current=positives['CURRENT_TEST_CLOCK'],historical=positives['HISTORICAL_AS_OF'],typed_ZERO_SUPPORT=zero,client_authentication='Full original functions re-executed inside serve; exact complete material equality, no caller hash trust',cache_seam='Original E04 transient provider cache cleared before original owner/client derivation; no E04R code imported',native_lifecycle_cases=sorted(p.name for p in O.glob('repair_late_*.json')),cold=dict(exits=cold,first_pid=replay['first_pid'],replay_pid=replay['pid'],bit_identical=True,permission_limit='Fresh fixture construction resets local grants; no durable renewal or real issuer authority')))
trace=json.loads((R/'02_ACTUAL_M4_M5_N9C_E04_NATIVE_OWNER_TRACE.json').read_text())
assert trace['imported_modules']
for mod in trace['imported_modules']:
 assert sha(pathlib.Path(mod['file']))==mod['sha256']
 if mod['module']!='e05_n9_selected_world_adapter':assert mod['source_commit']!='E05R_VERSIONED_WORKING_CANDIDATE'
passport=json.loads((R/'environment_passport.json').read_text())
passport.update(startup='69f961a7b2d835a6f925563179fdb8716df13f8b',branch=cmd('git','branch','--show-current'),origin=cmd('git','remote','get-url','origin'),git_version=cmd('git','--version'),pytest_version=cmd(sys.executable,'-m','pytest','--version'),requested_model='GPT-6.1 Sol Medium (user assignment; runtime model setting not independently inspected)',authority_scope='SOURCEFREE_ONLY_NONINSTALLING')
dump('environment_passport.json',passport)
receipt=dict(verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),original_staged_objects=401,unchanged_runtime_objects=400,versioned_adapter_sha256=sha(R/'candidate/e05r_selected_world_adapter.py'),frozen_test_bytes_unchanged=True,junit=c,final_total=358,baseline_independent=baseline,baseline_independent_exit=1,final_independent_exit=0,additional_exit=0,original_suite_exits=[x['exit'] for x in passport['suites']],independent_command=[sys.executable,'-m','pytest','-q','tests/test_independent_court.py','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/repaired_independent.xml'],independent_cwd=str(R),independent_env={'PYTHONDONTWRITEBYTECODE':'1'},additional_command=[sys.executable,'-m','pytest','-q','tests/test_e05r_repair.py','--noconftest','--import-mode=importlib','-p','no:cacheprovider','--junitxml=observations/e05r_additional.xml'],cold_exits=cold,cold_distinct_pids=[replay['first_pid'],replay['pid']],cold_bit_identical=True,imported_profile_modules=len(trace['imported_modules']),disposition='REPAIRED_SOURCEFREE_CANDIDATE_EXECUTED_AWAITING_DISTINCT_E05R_REVIEW',operative_OC05=False,new_issuer=False)
assert all(x==0 for x in receipt['original_suite_exits'])
dump('execution_receipt.json',receipt)
print(json.dumps(dict(junit=c,baseline=baseline,closed_reds=len(closure),cold=receipt['cold_distinct_pids']),indent=2))
