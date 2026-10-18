"""Author evidence audit; does not grant independent acceptance."""
import json,hashlib,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
from run_candidate import ROOT,OUT,dump,portable

def main():
 for p in OUT.rglob('*'):
  if not p.is_file():continue
  if p.suffix=='.xml':
   tree=ET.parse(p)
   for node in tree.iter():
    node.attrib.pop('hostname',None)
    for k,v in node.attrib.items():node.set(k,portable(v))
    if node.text:node.text=portable(node.text)
    if node.tail:node.tail=portable(node.tail)
   tree.write(p,encoding='utf-8',xml_declaration=True)
  elif p.suffix in ('.log','.json'):p.write_text(portable(p.read_text()))
 summary=json.loads((OUT/'summary.json').read_text())
 expected={'fixed/strict':(2,0),'fixed/r1':(45,0),'fixed/e2_full':(44,2),'fixed/x2':(17,1),'fixed/repair5':(5,0),'fixed/e3_frozen':(26,0),'fixed/indexed':(7,0)}
 for name,(n,f) in expected.items():
  row=summary[name];assert (int(row['tests']),int(row['failures']),int(row['errors']),int(row['skipped']))==(n,f,0,0)
 receipt=json.loads((OUT/'fixed/execution_receipt.json').read_text());assert sum(x['tests'] for x in receipt['totals'].values())==330
 native=json.loads((OUT/'fixed/inherited/f1_native_gate.log').read_text());assert len(native['failures'])==17
 assert next(c for c in receipt['commands'] if c['label']=='f1_native_gate')['exit_code']==1
 manifest=json.loads((OUT/'fixed/source_manifest.json').read_text())
 for row in manifest:
  if '/evidence/' in row['staged_path'] or row['staged_path'].endswith('execution_receipt.json'):continue
  data=(ROOT/row['staged_path']).read_bytes();assert hashlib.sha256(data).hexdigest()==row['sha256']
  if row.get('commit') and 'git_blob_sha1' in row:
   assert subprocess.check_output(['git','cat-file','blob',row['git_blob_sha1']])==data
 for row in json.loads((OUT/'frozen_manifest.json').read_text()):
  assert hashlib.sha256((ROOT/row['staged']).read_bytes()).hexdigest()==row['sha256']
 assert (ROOT/'bridge.py').read_bytes()==(ROOT/'.runtime/fixed/bridge.py').read_bytes()
 scale=json.loads((OUT/'fixed/e3_sql/indexed_scale.json').read_text());counts=[[r['vm_instructions'] for r in s['measurements']] for s in scale['stats']]
 assert len(set(n for group in counts for n in group))==1
 loaded=json.loads((OUT/'fixed/loaded_modules.json').read_text());assert loaded['modules']['bridge']['sha256']==hashlib.sha256((ROOT/'bridge.py').read_bytes()).hexdigest()
 dump(ROOT/'verification_receipt.json',dict(grade='TEST_ONLY_INDEXED_EVENT_CUSTODY_CANDIDATE_PENDING_INDEPENDENT_REVIEW',base='8f7966d6d0bbb1ea2e57359de9defbcf552268bd',candidate_sha256=loaded['modules']['bridge']['sha256'],suites=summary,inherited=330,native_reds=[x['case_id'] for x in native['failures']],indexed_lookup_vm_instructions=counts))
 print('Author audit PASS; separate independent review required')
if __name__=='__main__':main()
