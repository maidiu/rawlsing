"""Build documentary packet from executed receipts; never alter scientific oracles."""
from pathlib import Path
import json,hashlib,shutil,xml.etree.ElementTree as ET,datetime,subprocess
RET=Path(__file__).resolve().parents[1]
# Keep actual initial/intermediate results. Some intermediate candidate bytes
# were superseded before commit; their import hashes survive but are not claimed
# as fully reconstructable snapshots. Final receipts bind the frozen source.
for label in ('original','repaired'):
 for f in (RET/'runtime_root'/('court_'+label)/'repro/runs').glob('*'):
  target=RET/'evidence'/(label+'_'+f.name.replace('__','_'))
  if target.exists():continue
  target.mkdir()
  for name in ('junit.xml','execution.json'):shutil.copyfile(f/name,target/name)
receipts=[];imports=[]
for f in sorted((RET/'evidence').glob('*/junit.xml')):
 root=ET.parse(f).getroot();suites=list(root.iter('testsuite'));name=f.parent.name
 final=name in ['repaired_'+s+'_sealed2' for s in ('owners','rsm','candidate','candidate_unset','reviewer')]+['repair_sealed2']
 cases=[]
 for c in root.iter('testcase'):
  status='PASS';message=''
  for result in c:
   if result.tag in ('failure','error','skipped'):status={'failure':'RED','error':'ERROR','skipped':'SKIP'}[result.tag];message=result.get('message','')
  cases.append(dict(name=c.get('name'),classname=c.get('classname'),status=status,message=message))
 counts={k:sum(int(s.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')};counts['pass']=sum(c['status']=='PASS' for c in cases)
 execution=json.loads((f.parent/'execution.json').read_text()) if (f.parent/'execution.json').exists() else None
 receipts.append(dict(run=name,final=final,counts=counts,execution=execution,cases=cases,junit=str(f.relative_to(RET))))
 if execution:
  root_alias='runtime_root/court_original' if name.startswith('original_') else 'runtime_root/court_repaired' if name.startswith('repaired_') else '.'
  for row in execution.get('imports',[]):
   local=RET/root_alias/row['file'];current=hashlib.sha256(local.read_bytes()).hexdigest() if local.exists() else None
   imports.append(dict(run=name,final=final,**row,canonical_local=str(local.relative_to(RET)),current_materialized_matches=current==row['sha256']))
(RET/'02_EXECUTED_CASE_MATRIX.json').write_text(json.dumps(dict(schema='CAN2_EXECUTED_CASE_MATRIX@1',independent_acceptance=False,red_policy='All original assertions remain; RED never inverted or xfailed',runs=receipts),indent=2)+'\n')
(RET/'03_ACTUAL_IMPORT_RECEIPTS.json').write_text(json.dumps(dict(schema='CAN2_IMPORT_LINEAGE@1',final_source_commit='f9ff05197fb2837c733f8b453c678043e90c77d8',historical_note='Intermediate non-final candidate versions are hash-only receipts; final and original source identities independently verified',rows=imports),indent=2)+'\n')
# Independent predecessor law bindings remain the adopted-law reference; author
# annotations name where the repair acts, without editing inherited freeze.
prior=RET/'runtime_root/rcp3'
for source,name in [('01_CAN008_23_LAW_BINDINGS.json','04_INHERITED_LAW_BINDINGS.json'),('02_ADP016_ADP017_LAW_GATES.json','05_INHERITED_OWNER_LAW_GATES.json')]:shutil.copyfile(prior/source,RET/name)
p=RET/'environment_passport_delta.json';passport=json.loads(p.read_text());passport.update(last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),covered_test_suites=[dict(run=r['run'],counts=r['counts'],junit=r['junit']) for r in receipts if r['final'] or r['run'].startswith('original_')],source_refs_manifest='lineage/00_ORIGINAL_SOURCE_MANIFEST.json',materialized_source_refs=json.loads((RET/'lineage/00_ORIGINAL_SOURCE_MANIFEST.json').read_text()),candidate_source_freeze='01_CANDIDATE_SOURCE_FREEZE.json',actual_import_receipts='03_ACTUAL_IMPORT_RECEIPTS.json',assignments_completed=['CAN2 bounded implementation repair, actual tests and causal controls'],next_good_affinity_tags=['CAN008','ADP016','ADP017','CAUSAL_HISTORY'],staged_state_preservation='PRESERVED_IGNORED; verify live marker/bytes next time',retire_or_rebuild_reason=None,independent_review_separation='Current worker is repair author; distinct future HQ-commissioned I2 required',actual_current_HEAD=subprocess.check_output(['git','rev-parse','HEAD']).decode().strip(),clean_dirty_state='Candidate source committed; documentary receipts pending',account_affinity='CURRENT_CODEX_SESSION; account telemetry UNKNOWN')
p.write_text(json.dumps(passport,indent=2)+'\n')
print('runs',len(receipts),'cases',sum(len(x['cases']) for x in receipts),'import rows',len(imports),'final imported bytes match',all(r['current_materialized_matches'] for r in imports if r['final']))
