from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,subprocess
ROOT=Path(__file__).resolve().parents[1]
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
for manifest in ['source_manifest.json','authority_manifest.json']:
 for x in json.loads((ROOT/manifest).read_text()):
  b=(ROOT/x['local']).read_bytes();assert hashlib.sha256(b).hexdigest()==x['sha256'];assert blob(b)==x['git_blob']
for x in json.loads((ROOT/'native_source_manifest.json').read_text()):
 b=(ROOT/'inherited_e05a/runtime'/x['local']).read_bytes();assert blob(b)==x['git_blob'];assert hashlib.sha256(b).hexdigest()==x['sha256']
d=json.loads((ROOT/'COMPETENT_HQ_DECISION_RECORD_CANDIDATE.json').read_text());assert d['status']=='COMPETENT_DECISION_PENDING' and not d['binding']
assert all(d[k] is None for k in ['reviewer','issuer','signature','decision_id','issued_at'])
for p,h in d['evidence_hashes'].items():assert hashlib.sha256((ROOT/p).read_bytes()).hexdigest()==h
s=ET.parse(ROOT/'observations/preview.xml').getroot().find('testsuite');assert [int(s.get(k)) for k in ['tests','failures','errors','skipped']]==[16,0,0,0]
for p in ROOT.rglob('*.json'):
 if 'runtime' not in p.parts:json.loads(p.read_text())
print('PASS: exact native/source/authority Git preimages, decision hashes, NULL issuers, 16/0/0/0 JUnit, JSON validity')
