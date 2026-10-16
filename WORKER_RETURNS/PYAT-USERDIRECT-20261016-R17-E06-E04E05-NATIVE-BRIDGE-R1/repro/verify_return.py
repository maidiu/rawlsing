from bootstrap import ROOT
import json,hashlib,subprocess,xml.etree.ElementTree as ET
for manifest in ['source_manifest.json','evidence_manifest.json']:
 entries=json.loads((ROOT/manifest).read_text())
 if manifest=='source_manifest.json':assert len(entries)==402
 for x in entries:
  b=(ROOT/x['local']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256'];assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==x['git_blob']
p=ROOT/'01_FROZEN_E04T_E05R_BRIDGE_CONTRACT.json';assert hashlib.sha256(p.read_bytes()).hexdigest()==(ROOT/'01_FREEZE_SHA256.txt').read_text().split()[0]
assert p.read_bytes()==subprocess.check_output(['git','show','14f247b75:'+str(p.relative_to(ROOT.parents[1]))],cwd=ROOT)
d=json.loads((ROOT/'02_ACTUAL_NATIVE_TO_TWO_CONSUMER_PRODUCTS.json').read_text());assert hashlib.sha256((ROOT/d['native_trace']['path']).read_bytes()).hexdigest()==d['native_trace']['sha256']
assert d['grade']=='TEST_ONLY_SOURCEFREE_BRIDGE_CANDIDATE' and not d['independent_bridge_acceptance']
s=ET.parse(ROOT/'observations/bridge.xml').getroot().find('testsuite');assert [int(s.get(k)) for k in ['tests','failures','errors','skipped']]==[40,0,0,0]
for state in ['restored','withdrawn']:
 c=json.loads((ROOT/'observations'/('cold_'+state+'_comparison.json')).read_text());assert c['bit_identical_serialized_result'] and len(set(c['child_pids']))==2
 assert hashlib.sha256((ROOT/'observations'/('current_grants_'+state+'.json')).read_bytes()).hexdigest()==c['persisted_ledger_sha256']
for p in ROOT.rglob('*.json'):
 if 'runtime' not in p.parts:json.loads(p.read_text())
artifact=ROOT/'artifact_sha256.json'
if artifact.exists():
 for p,h in json.loads(artifact.read_text()).items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h,p
print('PASS: 402 exact source preimages; frozen contract unchanged; native trace; 40/0/0/0 JUnit; four cold processes/current ledgers; candidate ceiling')
