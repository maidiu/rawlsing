"""Fail-closed audit of physical originals, final JUnit and imported sources."""
from pathlib import Path
import json,hashlib,subprocess,xml.etree.ElementTree as ET
from collections import Counter
R=Path(__file__).resolve().parents[1];W=R.parents[1];RT=R/'runtime_root';O=R/'observations'
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def save(name,data):(R/name).write_text(json.dumps(data,indent=2)+'\n')
selector=json.loads((R/'source_selector.json').read_text());expected={};verified=[]
for row in selector['files']:
 p=RT/row['staged_path'];data=p.read_bytes();assert sha(data)==row['sha256'] and blob(data)==row['git_blob_sha1']
 assert subprocess.check_output(['git','hash-object',str(p)],text=True).strip()==row['git_blob_sha1']
 expected[str(p)]=row['git_blob_sha1'];verified.append(dict(path=str(p),blob=row['git_blob_sha1'],sha256=row['sha256']))
assert len(verified)==94
native=json.loads((RT/'candidate/source_manifest.json').read_text());assert len(native)==51
pins={'pre553_empirical_possibility_provider':'23167aa25291fb148b1e3cf210ac33fe7769b783','pre553_analytical_composition':'604c8d591d4cc2b646e9b149cdb233fc9d69cf6b','source_backed_positioned_subject_possibility':'62e5eced47b64512f47b004e3e13a6ef3fe21de7','m4_v557_v558_publication_repository':'8ec5c8e1c1a3cb7e998bb6cf0972ac87f396e360','m5_runtime_rsc_peer_prior':'18735bdb31a220aed032aa722574d685e2bdddf5','pre553_empirical_query':'03facecf70890bfd13b80418620d274cbcd69d02'}
products=[]
for p in sorted((R/'product').glob('*.py')):
 data=p.read_bytes();old=(RT/'candidate/product'/p.name).read_bytes();products.append(dict(path=str(p),blob=blob(data),sha256=sha(data),unchanged_from_E04=data==old));expected[str(p)]=blob(data)
assert [Path(p['path']).name for p in products if not p['unchanged_from_E04']]==['empirical.py']
# Reconfirm the exact original independent body, helper and independent oracle.
for record in json.loads((R/'frozen_E04N/source_manifest.json').read_text()):
 assert sha((R/record['local']).read_bytes())==record['sha256']
assert sha((R/'E04I_ORIGINAL_FROZEN_ORACLE.json').read_bytes())=='9f872f75e128530b8ade0103c11fad5f02a418961acf0cb008bdc37872f4269c'
suites={};all_imports=[];all_calls=Counter();processes=[]
for mode,count in [('author37',37),('native231',231),('independent',51),('hostiles',37)]:
 root=ET.parse(O/(mode+'.xml')).getroot();cases=[]
 for c in root.iter('testcase'):
  status='FAIL' if c.find('failure') is not None else 'ERROR' if c.find('error') is not None else 'SKIP' if c.find('skipped') is not None else 'PASS'
  cases.append(dict(name=c.attrib['name'],classname=c.attrib.get('classname'),status=status))
 assert len(cases)==count and all(c['status']=='PASS' for c in cases),(mode,Counter(c['status'] for c in cases))
 terminal=json.loads((O/(mode+'.terminal.json')).read_text());assert terminal['exit']==0
 audits=sorted((O/(mode+'_process_audits')).glob('*.json'));assert audits
 for p in audits:
  d=json.loads(p.read_text());processes.append(dict(suite=mode,audit=str(p.relative_to(R)),pid=d['pid'],imports=len(d['imports']),call_frames=sum(d['calls'].values())))
  for i in d['imports']:
   data=Path(i['file']).read_bytes();assert blob(data)==i['git_blob_sha1'] and sha(data)==i['sha256']
   if i['module']=='sitecustomize':assert data==(R/'repro/sitecustomize.py').read_bytes()
   else:assert expected[i['file']]==i['git_blob_sha1'],i
   all_imports.append(dict(suite=mode,**i))
  for frame,n in d['calls'].items():
   file,line,func=frame.rsplit(':',2);assert file in expected,frame;all_calls[func]+=n
 suites[mode]=dict(executed_against='E04R candidate with original frozen assertions' if mode in ('author37','independent') else 'exact native regression sources' if mode=='native231' else 'new implementer hostile cases',cases=cases,counts=dict(Counter(c['status'] for c in cases)),terminal=terminal)
for name,pin in pins.items():
 found=[i for i in all_imports if i['module']=='rawlsing_next.'+name];assert found and all(i['git_blob_sha1']==pin for i in found),(name,found)
probe=json.loads((O/'full_native_probe.json').read_text());assert probe['same_concrete_evidence_objects_verified'] and sum(probe['call_counts'].values())==205
for i in probe['imports']:
 if i['module']=='sitecustomize':assert Path(i['file']).read_bytes()==(R/'repro/sitecustomize.py').read_bytes()
 else:assert expected[i['file']]==i['git_blob_sha1']
for c in probe['actual_calls']:assert c['file'] in expected
closure=json.loads((O/'two_RED_closure_probe.json').read_text());assert len(closure['cases'])==4
for c in closure['cases']:
 assert c['trusted_projection']==c['before'] and len(c['both_client_results'])==2
 for result in c['both_client_results']:
  assert result['refusal']=='NATIVE_OWNER_CACHE_PROJECTION_MISMATCH' and result['new_empirical_value_reads']==result['new_product_receipts']==0
closures=dict(schema='E04R_IMPLEMENTER_TWO_RED_CLOSURES@1',verdict='TWO_PRIOR_RED_CASES_CLOSED_IN_IMPLEMENTER_RUNTIME_REQUIRES_DISTINCT_REVIEW',prior=dict(commit='644a68b76042309be71f0eb65fabc4a6903f15b8',independent51='49PASS_2FAIL'),now=dict(independent51='51PASS_0FAIL',original_test_and_common_bytes_unchanged=True,oracle_sha256=sha((R/'E04I_ORIGINAL_FROZEN_ORACLE.json').read_bytes())),findings=[dict(id='E04N_F1',attack='18 replaced by999, stale and recomputed local hash',closure='Both original independent guard and both real clients refuse before empirical read',evidence='observations/two_RED_closure_probe.json'),dict(id='E04N_F2',attack='Same values, foreign well-formed C11 release ref, stale and recomputed local hash',closure='Original independent guard and both real clients refuse before empirical read',evidence='observations/two_RED_closure_probe.json')],additional_hostiles=dict(PASS=37,FAIL=0,errors=0,skips=0),adoption=False)
save('01_TWO_E04N_RED_CLOSURES.json',closures)
save('03_REAL_C1_F8_M4_M5_TWO_CONSUMER_TESTS_AND_JUNIT.json',dict(schema='E04R_EXECUTED_CANDIDATE_FULL_NATIVE_EVIDENCE@1',suites=suites,final_pass_total=356,final_fail_total=0,final_skip_total=0,originals_byte_verified=verified,product_modules=products,physical_six_pins=pins,processes=processes,actual_import_observations=all_imports,pytest_observed_owner_entries=dict(all_calls),dedicated_probe=dict(actual_calls=probe['actual_calls'],counts=probe['call_counts'],same_concrete_evidence_verified=True,concrete_C1_evidence_objects=len(probe['composition_returns'])),C11_reconstruction=json.loads((O/'independent_C11_native_reconstruction.json').read_text()),two_client_closures=[dict(mutation=c['mutation'],results=c['both_client_results']) for c in closure['cases']],initial_new_hostile_harness_error='observations/hostiles_initial_harness_error.xml; 33PASS/1FAIL in attack construction, corrected without product change; not included in final356',historical_author_E04='Original archived37/231 receipts preserved in runtime_root/candidate; not added to new356',scope='SOURCEFREE_IMPLEMENTER_CANDIDATE_ONLY_REQUIRES_DISTINCT_REVIEW',operative_N9=False,adoption=False))
save('05_REQUIREMENT_AUDIT.json',dict(commission='WORKER_COMMISSIONS/PYAT-USERDIRECT-20261015-R13-E04R-NATIVE-CACHE-INTEGRITY-REPAIR-R1/00_COMMISSION.md',requirements=[dict(id=1,status='DONE_CANDIDATE',evidence='product/empirical.py; immutable bytes from real native producer/F8;37 new hostiles'),dict(id=2,status='DONE_CANDIDATE',evidence='01_TWO_E04N_RED_CLOSURES.json; complete projection/request equality; actual release object retained'),dict(id=3,status='PRESERVED_EXECUTED',evidence='37+231+51 unchanged suites; full_native_probe and C11 reconstruction; no native owner changes'),dict(id=4,status='DONE_EXECUTED',evidence='37+231+51+37=356PASS; original oracle/test/helper byte matched; versioned preload adapter; imports and calls verified'),dict(id=5,status='CEILING_RETAINED',evidence='04_SOURCE_N9_AND_ADOPTION_CEILING.md; distinct review required; no issuance/adoption/V3')],publication='Final containing commit and direct remote readback reported after push; commit cannot self-embed its own hash',self_acceptance=False))
print('AUDIT_PASS',len(verified),'original objects;',len(all_imports),'physical imports;',len(processes),'process audits;356PASS;205probe frames;6pins exact')
