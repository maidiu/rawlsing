"""Audit exact imported preimages, frozen code, executable receipts and proof."""
from pathlib import Path
import sys,json,hashlib,gzip,xml.etree.ElementTree as ET
HERE=Path(__file__).resolve().parent;RET=HERE.parent
sys.path[:0]=[str(HERE),str(HERE/'inputs/port'),str(HERE/'inputs/sc0f/repro'),str(HERE/'inputs/port/staging/ns')]
from sc0f3.receipts import verify
from sc0f3.common import digest
manifest=json.loads((RET/'source_manifest.json').read_text());by_path={}
for row in manifest:
 p=RET/row['staged'];b=p.read_bytes()
 assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==row['blob_sha1']
 assert hashlib.sha256(b).hexdigest()==row['sha256']
 by_path[str(p.relative_to(HERE))]=row
frozen=json.loads((RET/'candidate_freeze.json').read_text())
for name,h in frozen['files'].items():assert hashlib.sha256((RET/name).read_bytes()).hexdigest()==h
imports=0
superseded=[]
for p in (HERE/'runs').glob('*/execution.json'):
 for row in json.loads(p.read_text())['imports']:
  if row['module'].startswith('sc0f3.') and p.parent.name!='candidate__r5':
   superseded.append(dict(run=p.parent.name,module=row['module'],recorded_sha256=row['sha256'],status='SUPERSEDED_DIAGNOSTIC_NOT_CURRENT_CODE_PROOF'))
   continue
  b=(HERE/row['file']).read_bytes()
  assert hashlib.sha256(b).hexdigest()==row['sha256']
  if row['file'] in by_path:assert row['git_blob_sha1']==by_path[row['file']]['blob_sha1']
  imports+=1
summary=json.loads((HERE/'proof/final_r5/summary.json').read_text())
for row in summary['runs']:
 path=HERE/'proof/final_r5'/row['artifact'];raw=gzip.decompress(path.read_bytes())
 assert hashlib.sha256(raw).hexdigest()==row['uncompressed_sha256']
 assert hashlib.sha256(path.read_bytes()).hexdigest()==row['compressed_sha256']
 obj=json.loads(raw)
 if 'world_receipt' in obj:verify(obj)
 n=obj['native_computation']
 assert n['values_read']
 for c in n['calls']:
  assert digest(c['args'])==c['args_digest'] and digest(c['result'])==c['result_digest']
  b=(HERE/c['module_file']).read_bytes()
  assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==c['git_blob_sha1']
 for value in n['values_read']:assert digest(value['value'])==value['value_digest']
r=ET.parse(HERE/'runs/candidate__r5/junit.xml').getroot()
assert sum(int(s.attrib['tests']) for s in r.iter('testsuite'))==76
assert not any(int(s.attrib[k]) for s in r.iter('testsuite') for k in ('errors','failures','skipped'))
result=dict(frozen_input_files=len(manifest),import_rows_checked=imports,final_candidate_tests=76,full_native_proof_runs=len(summary['runs']),proof_pass=True,original_bytes_unchanged=True,superseded_candidate_imports=superseded,initial_audit_correction='Initial audit incorrectly compared superseded candidate import hashes to current bytes and failed; only final76 own modules certify current code. Prior67 source archive and all pinned predecessor imports remain checked separately.')
(RET/'audit_receipt.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
