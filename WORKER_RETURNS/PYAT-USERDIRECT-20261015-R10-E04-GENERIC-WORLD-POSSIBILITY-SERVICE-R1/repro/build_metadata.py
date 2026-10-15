from pathlib import Path
import json,hashlib,datetime,subprocess,xml.etree.ElementTree as ET,shutil
RET=Path(__file__).resolve().parents[1]
for name in ('initial_junit.xml','expanded_junit.xml'):
 p=RET/'runtime_root'/name
 if p.exists():shutil.copyfile(p,RET/'outputs'/('history_'+name))
runs=[]
for f in sorted((RET/'outputs').glob('tests_*/junit.xml')):
 root=ET.parse(f).getroot();suites=list(root.iter('testsuite'));cases=[]
 for c in root.iter('testcase'):
  status='PASS';message=None
  for n in c:
   if n.tag in ('failure','error','skipped'):status={'failure':'RED','error':'ERROR','skipped':'SKIP'}[n.tag];message=n.get('message')
  cases.append(dict(name=c.get('name'),classname=c.get('classname'),status=status,message=message))
 execution=json.loads((f.parent/'execution.json').read_text())
 runs.append(dict(run=f.parent.name,primary=f.parent.name in ('tests_product_sanction_final','tests_native_final'),counts={k:sum(int(s.get(k,0)) for s in suites) for k in ('tests','failures','errors','skipped')},cases=cases,execution=execution,junit=str(f.relative_to(RET))))
(RET/'test_case_matrix.json').write_text(json.dumps(dict(schema='E04_EXECUTED_CASE_MATRIX@1',independent_acceptance=False,runs=runs),indent=2)+'\n')
p=RET/'environment_passport_delta.json';d=json.loads(p.read_text());d.update(last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),source_manifest='source_manifest.json',materialized_source_refs=json.loads((RET/'source_manifest.json').read_text()),dependency_closure_status='BOUNDED_EXACT_51_OBJECTS',covered_test_suites=[dict(run=r['run'],counts=r['counts'],receipt=r['junit']) for r in runs if r['primary']],source_commit='c2bc29af1128ff550b2ab61a876e1c97076e7b1f',current_source_HASH_probe='product_source_freeze.json matches exact local bytes',model_provider='UNKNOWN via runtime; user selected Codex GPT-6.1 Sol Medium',effort='USER_SELECTED_MEDIUM; actual telemetry UNKNOWN',pricing_class='UNKNOWN',observed_credits_usage=None,nearest_expected_slot_reset=None,machine_alias='AUTHORIZED_LOCAL_HOST',git_object_store_alias='EXISTING_PRIVATE_SHARED_STORE',worktree_alias='AUTHORIZED_SPARSE_WORKTREE',source_scope='SYNTHETIC_ONLY; native N9C documentary fixture regression only, not E04 input or original source read',assignments_completed=['E04 sourcefree service and two productive consumers'],next_good_affinity_tags=['N9_BOUNDARY','N10E_C1_F8','CLOCKS','GENERIC_POSSIBILITY'],staged_state_preservation='Ignored source cache and marker preserved; next session must probe live',capabilities={'Python':'VERIFIED','pytest':'VERIFIED','privateGit':'VERIFIED','filesystemShell':'VERIFIED','nativeImports':'VERIFIED','modelAPIorV3':'NOT_AUTHORIZED; zero calls'},independent_review_separation='Author return; distinct independent court after return',retire_or_rebuild_reason=None)
p.write_text(json.dumps(d,indent=2)+'\n')
print('Executed runs',len(runs),'primary cases',sum(r['counts']['tests'] for r in runs if r['primary']))
