"""Reconcile exact preimages, frozen case inventories, native imports and terminals."""
import pathlib,json,hashlib,xml.etree.ElementTree as ET,subprocess,collections,difflib
R=pathlib.Path(__file__).resolve().parents[1];O=R/'observations'
def write(name,value):(R/name).write_text(json.dumps(value,indent=2)+'\n')
def digest(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def cases(p):
 result=[]
 for x in ET.parse(p).getroot().iter('testcase'):
  state='FAIL' if x.find('failure') is not None else 'ERROR' if x.find('error') is not None else 'SKIP' if x.find('skipped') is not None else 'PASS'
  result.append(dict(name=x.attrib['name'],module=x.attrib.get('classname','').rsplit('.',1)[-1],status=state))
 return result
# Reverify exact original Git preimages and local bytes after execution.
inputs=[]
for name in ['primary_input_manifest.json','source_manifest.json']:
 for row in json.loads((R/name).read_text()):
  actual=(R/row['local']).read_bytes();original=subprocess.check_output(['git','-c','gc.auto=0','show',row['commit']+':'+row['path']],cwd=R)
  assert actual==original and digest(actual)==row['sha256'] and blob(actual)==row['git_blob']
  inputs.append(dict(manifest=name,local=row['local'],git_blob=row['git_blob'],sha256=row['sha256'],verified=True))
# Exact frozen assertion/helper/oracle files, no semantic or path normalization.
pairs=[('tests/test_full_native_independent.py','primary/e04n/tests/test_full_native_independent.py'),('tests/test_cache_repair_hostiles.py','primary/e04r/tests/test_cache_repair_hostiles.py'),('tests/test_e04s_hostiles.py','primary/e04s/tests/test_e04s_hostiles.py'),('repro/common.py','primary/e04s/repro/common.py'),('E04I_ORIGINAL_FROZEN_ORACLE.json','primary/e04n/E04I_ORIGINAL_FROZEN_ORACLE.json'),('01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json','primary/e04s/01_PRECOMMITTED_CACHE_SOURCE_AND_TWO_CLIENT_ORACLE.json')]
frozen=[]
for local,original in pairs:
 b=(R/local).read_bytes();assert b==(R/original).read_bytes();frozen.append(dict(local=local,primary=original,sha256=digest(b),byte_identical=True))
# The preexecution standalone oracle also stays frozen.
expected=(R/'00_ORACLE_SHA256.txt').read_text().split()[0];assert digest((R/'00_STANDALONE_AUTHORIZATION_AND_ORACLE.json').read_bytes())==expected
changed=[]
for p in sorted((R/'product').glob('*.py')):
 original=R/'primary/e04r/product'/p.name;same=p.read_bytes()==original.read_bytes()
 if not same:changed.append(str(p.relative_to(R)))
 frozen.append(dict(local=str(p.relative_to(R)),baseline='E04R',byte_identical=same,sha256=digest(p.read_bytes()),original_git_blob=blob(original.read_bytes())))
assert changed==['product/empirical.py']
(R/'product/empirical.diff').write_text(''.join(difflib.unified_diff((R/'primary/e04r/product/empirical.py').read_text().splitlines(True),(R/'product/empirical.py').read_text().splitlines(True),fromfile='E04R/product/empirical.py',tofile='E04T/product/empirical.py')))
write('06_PREIMAGE_AND_FROZEN_ASSERTION_PROOF.json',dict(exact_original_objects=len(inputs),preimages=inputs,frozen_files=frozen,changed_product_files=changed,preexecution_oracle_sha256=expected))
counts={'author37':37,'native231':231,'independent51':51,'author_hostiles37':37,'new_hostiles57':57,'lifecycle':40};suites={}
old={'author37':'primary/e04r/observations/author37.xml','native231':'primary/e04r/observations/native231.xml','independent51':'primary/e04r/observations/independent.xml','author_hostiles37':'primary/e04r/observations/hostiles.xml','new_hostiles57':'primary/e04s/observations/new_hostiles.xml'}
for name,count in counts.items():
 cs=cases(O/(name+'.xml'));terminal=json.loads((O/(name+'.terminal.json')).read_text())
 assert len(cs)==count and all(c['status']=='PASS' for c in cs) and terminal['exit']==0
 assert terminal['candidate_sha256']==digest((R/'product/empirical.py').read_bytes())
 inventory=None
 if name in old:
  prior=cases(R/old[name]);assert collections.Counter((c['module'],c['name']) for c in cs)==collections.Counter((c['module'],c['name']) for c in prior);inventory=dict(original_junit=old[name],all_original_case_ids_present=True)
 suites[name]=dict(tests=count,passed=count,failed=0,errors=0,skipped=0,terminal=terminal,case_inventory=inventory,cases=cs)
assert sum(counts.values())==453
baseline=cases(O/'baseline4.xml');assert len(baseline)==4 and all(c['status']=='FAIL' for c in baseline)
closed=[]
for c in baseline:
 final=next(x for x in suites['new_hostiles57']['cases'] if x['name']==c['name']);assert final['status']=='PASS'
 closed.append(dict(name=c['name'],baseline='FAIL_UNTOUCHED_E04R',repaired='PASS_UNCHANGED_E04S_ASSERTION'))
write('01_FOUR_ORIGINAL_RED_CLOSURES.json',dict(issue='E04S-A1',original_candidate='97254d0b215b5dd45580dd94608a8ec95ff8b76f',baseline_junit='observations/baseline4.xml',repaired_junit='observations/new_hostiles57.xml',closures=closed,all_four_closed_as_implementer_evidence=True,independent_acceptance=False))
write('03_TESTS_AND_ORIGINAL_JUNIT_RECONCILIATION.json',dict(required_original_passes=413,new_cases=40,total_final_passes=453,failed=0,errors=0,skipped=0,suites=suites,baseline_not_counted_as_final_pass=True,initial_runs_not_counted_as_additional_tests=True))
# Verify every physically imported staged/candidate file against its exact bytes.
expected={str((R/x['local']).resolve()):x['git_blob'] for x in json.loads((R/'source_manifest.json').read_text())}
expected.update({str(p.resolve()):blob(p.read_bytes()) for p in (R/'product').glob('*.py')})
imports=[];owner_counts=collections.Counter()
for label in [*counts,'baseline4','scientific_probe','f1_f2_probe','ceiling_probe']:
 audit=json.loads((O/(label+'_process.json')).read_text())
 for item in audit['imports']:
  file=item['file'];absolute=file.replace('<RETURN>',str(R))
  assert absolute in expected,(label,file)
  assert item['git_blob']==expected[absolute]
  imports.append(dict(process=label,**item,verified_exact_file=True))
 for item in audit['counts']:owner_counts[item['function']]+=item['count']
science=json.loads((O/'scientific_probe.json').read_text());source=science['source_reconstruction'];assert source['actual_respondents']==58 and source['actual_events']==232 and source['same_exact_evidence_objects_into_F8']
for function in ['ingest_c11_source_release','validate_c11_source_release','execute_empirical_query','provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility','resolve_v558','materialize_resolved_structural_context','validate_resolved_structural_context','_require_exact_i03_authority_fitness']:
 assert owner_counts[function]>0,function
for label in ['scientific_probe','f1_f2_probe','ceiling_probe']:assert json.loads((O/(label+'.terminal.json')).read_text())['exit']==0
for state in ['withdrawn','restored']:
 c=json.loads((O/('e04t_cold_'+state+'.json')).read_text());assert c['bit_identical_results'] and c['fixture_unchanged'] and len(set([c['parent_pid'],*c['child_pids']]))==3
 target=O/('cold_state_'+state+'_input.json')
 if not target.exists():
  material=next(p.read_bytes() for p in (R/'runtime_root/tmp/lifecycle').glob('*/current_grants.json') if json.loads(p.read_text())['state']==state)
  target.write_bytes(material)
 assert digest(target.read_bytes())==c['persisted_current_grants_sha256']
write('07_ACTUAL_NATIVE_IMPORT_AND_CALL_PROOF.json',dict(imports=imports,actual_native_call_counts=dict(owner_counts),method='Unmodified native functions; actual Python profile frames and file hashes. Counts are repeated executions, not independent observations.',source_reconstruction=source,scientific_probe_native_counts=science['actual']['counts'],same_concrete_C1_evidence_into_F8=len(science['actual']['compositions']),cold_evidence=['observations/e04t_cold_withdrawn.json','observations/e04t_cold_restored.json']))
print('FINAL_RECONCILED: 356 E04R + 57 E04S + 40 E04T = 453 PASS; all original case IDs, blobs and four RED closures verified')
