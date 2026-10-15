import pathlib,hashlib,json,subprocess,datetime,sys,xml.etree.ElementTree as ET
R=pathlib.Path(__file__).resolve().parents[1];REPO=R.parents[1];RT=R/'runtime';O=R/'observations'
def cmd(*argv):return subprocess.check_output(argv,cwd=REPO).decode().strip()
manifest=json.loads((R/'source_manifest.json').read_text());latest={x['local']:x for x in manifest}
for p,row in latest.items():
 b=(RT/p).read_bytes();assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['git_blob'],p
freeze=R/'01_FROZEN_NATIVE_WORLD_AND_CLOCK_ORACLES.json';assert hashlib.sha256(freeze.read_bytes()).hexdigest()==(R/'01_FREEZE_SHA256.txt').read_text().split()[0]
counts={}
for label in ['e05','e04','n9c','m4_m5','empirical','e03','independent']:
 root=ET.parse(O/(label+'.xml')).getroot();suites=list(root.iter('testsuite'));counts[label]={k:sum(int(s.attrib.get(k,0)) for s in suites) for k in ['tests','failures','errors','skipped']}
assert sum(counts[x]['tests'] for x in counts if x!='independent')==271
assert all(counts[x]['failures']==counts[x]['errors']==counts[x]['skipped']==0 for x in counts if x!='independent')
assert counts['independent']==dict(tests=55,failures=11,errors=0,skipped=0),counts['independent']
cold=json.loads((O/'cold_exits.json').read_text());assert all(x['exit']==0 for x in cold)
replay=json.loads((O/'independent_cold_replay.json').read_text());assert replay['replay_bit_identical'] and replay['pid']!=replay['first_pid']
passport=json.loads((R/'environment_passport.json').read_text());passport.update(git_version=cmd('git','--version'),pytest_version=cmd(sys.executable,'-m','pytest','--version'),branch=cmd('git','branch','--show-current'),startup='e2f1b96a860d1555e072f1538eea5d913eef3b37',candidate='257dfaf41be7d2a88c11741851e9dc89363b5386',origin=cmd('git','remote','get-url','origin'),requested_model='GPT-6.1 Sol Medium (user assignment; runtime model control not independently inspected)',authority_scope='SOURCEFREE_ONLY_NONINSTALLING')
(R/'environment_passport.json').write_text(json.dumps(passport,indent=2)+'\n')
receipt=dict(verified_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),staged_objects=len(manifest),final_runtime_paths=len(latest),all_materialized_git_blobs_verified=True,independent_freeze_sha256=hashlib.sha256(freeze.read_bytes()).hexdigest(),junit=counts,independent_exit=1,independent_command=['python3','-m','pytest','-q',str((R/'tests').relative_to(REPO)),'--import-mode=importlib','-p','no:cacheprovider','--junitxml='+str((O/'independent.xml').relative_to(REPO))],independent_env={'PYTHONDONTWRITEBYTECODE':'1'},independent_cwd=str(REPO),independent_stdout=str(O/'independent.log'),cold_exits=cold,cold_distinct_pids=[replay['first_pid'],replay['pid']],cold_bit_identical=True,verdict='RED_SOURCEFREE_NONINSTALLING_E05_ADAPTER',harness_errors_excluded=['initial cold tuple/list comparison','expanded initial wrong universe/ref constructors'])
(R/'execution_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt['junit'],indent=2));print('VERIFIED runtime identities, immutable freeze, original 271, independent 55, distinct-process cold replay')
