"""Derive exact per-case results and before/after RC0 transitions from real JUnit."""
import hashlib, json, pathlib, xml.etree.ElementTree as ET
RET=pathlib.Path(__file__).resolve().parents[1]
SUITES=['smoke','baseline_rc0','rc0','k9_k10','original_k9_k10','connection','n10e_c1','pe','hostile']
def read(suite):
 root=ET.parse(RET/'repro'/f'{suite}.xml').getroot(); cases=[]
 for case in root.iter('testcase'):
  f=case.find('failure');e=case.find('error');skip=case.find('skipped')
  status='RED' if f is not None else 'ERROR' if e is not None else 'SKIP' if skip is not None else 'PASS'
  x=f if f is not None else e if e is not None else skip
  cases.append(dict(name=case.attrib['name'],classname=case.attrib.get('classname'),seconds=case.attrib.get('time'),status=status,diagnostic=x.text if x is not None else None))
 receipt=json.loads((RET/'repro'/f'{suite}_execution.json').read_text())
 counts={k:sum(c['status']==k for c in cases) for k in ['PASS','RED','ERROR','SKIP']}
 return dict(suite=suite,counts=counts,total=len(cases),execution=receipt,cases=cases)
def classify(name):
 classes={
 'test_possibility_query_permission':'CANDIDATE_AUTHORIZATION_DEFECT',
 'test_prior_knowledge_requires':'CANDIDATE_VALIDATION_DEFECT',
 'test_declared_prior_knowledge':'MISSING_DECLARATION_CARRIAGE',
 'test_reverse_claim':'CANDIDATE_REVERSE_VALIDATION_AND_ISSUANCE_CLAIM_DEFECT',
 'test_real_pe_producer':'INCOMPLETE_PE_CONNECTION_GATE',
 'test_fake_profile':'PROVENANCE_CLAIM_FALSIFIER; NOT_MALICIOUS_RUNTIME_SECURITY_PROOF',
 'test_schema_pass':'UNPROVED_NEGATIVE_REF_DEREFERENCE; SCHEMA_SYNTAX_PASS',
 'test_receipt_identity':'WORLD_BOUND_RECEIPT_IDENTITY_DEFECT',
 'test_facade_cannot':'CONSUMER_LINEAGE_CHECKER_SCOPE_LIMIT',
 'test_producer_geometry':'UNBOUND_PRODUCER_TARGET_OR_RELEASE',
 'test_f2_f1':'F1_F2_REFERENCE_SUBSTITUTION',
 }
 return next((v for k,v in classes.items() if name.startswith(k)),'UNCLASSIFIED_REQUIRES_REVIEW')
results=[read(s) for s in SUITES]
for result in results:
 for c in result['cases']:
  if result['suite']=='hostile' and c['status']=='RED':c['scientific_classification']=classify(c['name'])
  if result['suite']=='original_k9_k10' and c['status']=='RED':
   c['scientific_classification']='RETURN_STATE_COMPATIBILITY_DRIFT' if c['name'].startswith('test_k9_01') else 'ORIGINAL_TEST_EXPECTS_DENIED_ADAPTER_TO_RETURN; REPAIR_FAILS_CLOSED_EARLIER'
baseline={c['name']:c for c in next(r for r in results if r['suite']=='baseline_rc0')['cases']}
repaired={c['name']:c for c in next(r for r in results if r['suite']=='rc0')['cases']}
assert set(baseline)==set(repaired) and len(baseline)==25
transitions=[dict(case=n,before=baseline[n]['status'],after=repaired[n]['status'],evidence_before='repro/baseline_rc0.xml',evidence_after='repro/rc0.xml') for n in baseline]
assert sum(x['before']=='RED' for x in transitions)==12
assert sum(x['before']=='PASS' for x in transitions)==13
assert all(x['after']=='PASS' for x in transitions)
obj=dict(schema='RSC0_ACTUAL_EXECUTION_PER_CASE@1',results=results,RC0_unchanged25_transitions=transitions,oracles_not_edited=True,setup_errors='initial_layout_rc0:23PASS2layout failures, corrected RC0_RETURN without test edits; retained. Pre-isolation repeats retained but not independent evidence.',reviewer_revisions='initial41 retains25RED16PASS. Two assertions were narrowed: negative refs are schema-lawful so final test probes real read_values dereference; H2 no-op generation is not a publication boundary so final test changes publication/as_of and verifies world-bound possibility identity. Six target/release/F1-F2 cases added. No frozen expected matrix or candidate code changed.')
(RET/'02_EXECUTION_PER_CASE.json').write_text(json.dumps(obj,indent=2)+'\n')
for r in results:print(r['suite'],r['counts'])
print('RC0_12_RED_TO_PASS_AND13_PRESERVED_VERIFIED')
