"""Portable integrity checks; --native adds seven nonrespondent hostile witnesses.

Run from the qualified H48 worktree with PYTHONPATH=. and --native. No source
reader or original survey is invoked. All data in the witnesses are synthetic,
published code, or metadata indexes.
"""
import argparse,ast,collections,csv,gzip,hashlib,inspect,json,pathlib,subprocess,sys

ROOT=pathlib.Path(__file__).resolve().parent
def csvrows(name):return list(csv.DictReader(open(ROOT/name)))
def verify():
 e=json.load(open(ROOT/'EVIDENCE_MANIFEST.json'))['evidence']
 cov=csvrows('04_SOURCE35_MEASUREMENT_AND_AUTHORITY_COVERAGE.csv')
 loc=csvrows('02_ACCEPTED_AND_ARCHIVAL_AUTHORITY_LOCATOR.csv')
 inputs=csvrows('01_CURRENT_CONSUMER_INPUT_AND_PROVIDER_INDEX.csv')
 stages=csvrows('evidence/authority_stage_bindings.csv')
 with gzip.open(ROOT/'evidence/original_item_authority_candidates.json.gz','rt') as f:items=json.load(f)
 assert len(cov)==35 and len({r['wave_uid'] for r in cov})==35
 assert len(items)==18276 and len({r['question_implementation_id'] for r in items})==18276
 assert sum(int(r['p2_implementation_rows']) for r in cov)==18276
 assert len(stages)==140 and all(r['binding']=='HASH_BOUND_EXACT' for r in stages)
 assert all(e[r['evidence_id']]['sha256']==r['declared_sha256'] for r in stages)
 assert all(r['actual_eligible_E_pre']=='NULL' and r['current_host']=='NULL' and r['current_source_host_purpose_grant']=='NULL' for r in cov)
 assert len({r['source_id'] for r in cov})==35 and all(len(r['declared_source_sha256'])==64 for r in cov)
 for rows in [inputs,loc,items]:
  for r in rows:
   for k,v in r.items():
    if k.endswith('evidence_id') and v:assert v in e,(k,v)
 for r in inputs:
  assert e[r['evidence_id']]['blob_oid']==r['git_blob']
  for eid in json.loads(r.get('provider_code_evidence_ids') or '[]'):assert eid in e
 assert len({r['input_id'] for r in inputs})==len(inputs)
 assert len([r for r in items if not r['full_relation_explicit_id_bindings']])==26
 for r in items:
  assert any(b['family'].startswith('MANUAL_') for b in r['candidate_bindings'])
  for b in r['candidate_bindings']:assert b['evidence_id'] in e and b['data_row']>0
  for b in r['full_relation_explicit_id_bindings']:
   assert 'forbidden_inference' in b['preserved_assertions']
   assert b['preserved_assertions']['p2_exact_identity_sha256']==r['exact_identity_sha256']
 for eid,x in e.items():
  assert x['evidence_id']==eid and len(x['sha256'])==64
  assert '/Users/' not in x['locator']
 for p in ROOT.rglob('*'):
  if p.is_file():assert p.suffix.lower() not in ['.sav','.dta','.parquet','.arrow','.db','.sqlite']
 return dict(integrity='PASS',waves=len(cov),item_records=len(items),authority_rows=len(loc),input_rows=len(inputs),bound_stages=len(stages),evidence_entries=len(e))
def native():
 from rawlsing_next.tests.test_pre553_empirical_query import _auth
 from rawlsing_next.pre553_empirical_objects import AuthoritySnapshot
 from rawlsing_next.pre553_empirical_authority import require_positive_authority,Pre553AuthorityError
 from rawlsing_next.pre553_discovery_exact import _compile_frontier,COVERAGE_CLAIM
 from rawlsing_next.pre553_route_b_production import execute_route_b_production
 results=[]
 def witness(n,fn):
  note=fn();results.append(dict(witness=n,state='PASS',observation=note))
 def denied(fn):
  try:fn()
  except Pre553AuthorityError as x:return str(x)
  raise AssertionError('Required refusal did not occur')
 def stale():
  a=_auth('h48-synthetic','PREDICATE_GRAMMAR',families=('EmpiricalQuerySpec@1.0.0',));d=dict(a.semantic_fields);d['decision_state']='SUPERSEDED_NOT_REPLAYABLE'
  b=AuthoritySnapshot(typed_state='SUPERSEDED_NOT_REPLAYABLE',authority_snapshot_refs=(),dependency_refs=(),producer_replay_locator_or_reference_root=a.producer_replay_locator_or_reference_root,**d)
  return denied(lambda:require_positive_authority(b))
 witness('i_archival_superseded_not_current',stale)
 def frontier():
  x=_compile_frontier({'limits':{'maximum_conditioner_arity_K':1,'maximum_target_arity_J':1},'rules':[],'allow_empty_frontier':True},{},{})
  assert x==() and COVERAGE_CLAIM=='COMPLETE_FOR_EXACT_DECLARED_FRONTIER'
  return 'An explicitly empty declared grammar compiles to zero; it says nothing about complete original administered U.'
 witness('ii_declared_frontier_not_full_source',frontier)
 def prep():
  p=json.load(open(ROOT/'evidence/source_prep71_documentary_ledgers.json'));n=sum(len(x['rows']) for x in p)
  assert n==34 and len(csvrows('04_SOURCE35_MEASUREMENT_AND_AUTHORITY_COVERAGE.csv'))==35
  assert not any('WVS Wave 7' in r['source_file'] for x in p for r in x['rows'])
  return 'PREP71 has 34 documentary source rows; original35 independently includes WVS7, without inherited 35th grant.'
 witness('iii_34_does_not_authorize_35',prep)
 def file_presence():
  # Execute only exact class and guard AST definitions from the returned B43 code.
  path='WORKER_RETURNS/PYAT-R43-B43-SELECTED-ROUTE-B-ORIGINAL35-SOURCE-POSITIVE-ENDTOEND-R1/b43/feeder.py'
  raw=subprocess.check_output(['git','show','0fa15c1eda1ca36d89b0bbd948b655aa68f17370:'+path])
  t=ast.parse(raw);nodes=[n for n in t.body if isinstance(n,(ast.FunctionDef,ast.ClassDef)) and n.name in ['B43GrantDenied','guard_raw_source_read']]
  ns={};exec(compile('from __future__ import annotations\n','<future>','exec'),ns)
  mod=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),*nodes],type_ignores=[]);ast.fix_missing_locations(mod);exec(compile(mod,'<exact-b43-guard>','exec'),ns)
  try:ns['guard_raw_source_read']('UNOPENED_SOURCE.sav',None)
  except ns['B43GrantDenied'] as x:
   assert x.code=='B43_RAW_SOURCE_READ_WITHOUT_GRANT';return x.code+'; no filesystem source open performed'
  raise AssertionError('source guard did not refuse')
 witness('iv_file_presence_not_grant',file_presence)
 def scoped():
  a=_auth('h48-operation-synthetic','PREDICATE_GRAMMAR',families=('EmpiricalQuerySpec@1.0.0',))
  return denied(lambda:require_positive_authority(a,operation='UNISSUED_OTHER_OPERATION'))
 witness('v_manual_or_relation_scope_not_all_operations',scoped)
 def lits():
  row=next(r for r in csvrows('04_SOURCE35_MEASUREMENT_AND_AUTHORITY_COVERAGE.csv') if r['source_id']=='27');assert int(row['p2_implementation_rows'])==1198
  return 'LiTS-I inventory has 1198 implementations. AS2B code maps q301_2/q301_7; R47 documents the separate four-question old snapshot. Neither is whole-source U or required generic Route B storage.'
 witness('vi_bounded_lits_not_entire_source',lits)
 def route():
  names=inspect.signature(execute_route_b_production).parameters
  for k in ['source','projection','runtime_catalog','i03_requests','discovery_authority_ref']:assert names[k].default is inspect.Parameter.empty
  try:execute_route_b_production()
  except TypeError:return 'Actual Route B requires supplied source/projection/catalog/requests/discovery authority; no survey workload generated by an empty call.'
  raise AssertionError('Required arguments absent')
 witness('vii_route_b_is_consumer_not_source_rule_issuer',route)
 return results
if __name__=='__main__':
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--native',action='store_true');a=p.parse_args()
 result=verify()
 if a.native:result['hostile_witnesses']=native()
 print(json.dumps(result,indent=2))
