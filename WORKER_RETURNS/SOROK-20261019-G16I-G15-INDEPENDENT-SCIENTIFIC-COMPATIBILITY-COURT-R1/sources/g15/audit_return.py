"""Verify source closure, immutable oracles, all literal courts and publication terrain."""
from pathlib import Path
import collections,hashlib,json,subprocess,sys
from court_runner import ROOT,REPO,dump

def read(p):return json.loads((ROOT/p).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def counts(cases):return dict(collections.Counter(x['status'] for x in cases))
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)

def main():
 frozen=read('frozen/source_manifest.json')+read('frozen/shared_manifest.json')
 for row in frozen:
  p=ROOT/row['staged'];b=p.read_bytes()
  assert sha(p)==row['sha256'] and blob(b)==row['blob_sha1'],row
  assert blob(git('show',row['commit']+':'+row['path']))==row['blob_sha1']
 # All 14 actual imported baseline modules and all historical/native preimages.
 imports=read('execution/baseline/g14_observations.json')['imports'];original=read('frozen/g14/custody/module_preimages_and_imports.json');modules=[]
 for row in original['modules']:
  imp=next(x for x in imports if x['module_file'].endswith('/'+row['module']))
  assert imp['git_blob_sha1']==row['target_blob_sha1']
  modules.append(dict(module=row['module'],imported_baseline=imp,exact_G13_target_blob=row['target_blob_sha1']))
 assert len(modules)==14
 for row in original['original_manifest_preimages']:
  assert blob(git('show',row['commit']+':'+row['path']))==row['blob_sha1']
 suites={name:read('execution/'+name+'/results.json') for name in ['baseline','candidate']}
 for epoch,rows in suites.items():
  all_cases=[dict(suite=r['suite'],**c) for r in rows[:-1] for c in r['cases']]
  assert len(all_cases)==181
  assert len(rows[-1]['cases'])==67
  assert all(c['status'] in {'PASS','RED'} for c in all_cases+rows[-1]['cases'])
  for r in rows:
   if r['suite']=='g14_science':assert (ROOT/'runs'/epoch/'test_g14_science.py').read_bytes()==(ROOT/'frozen/g14/test_g14_science.py').read_bytes()
  if epoch=='baseline':assert counts(all_cases)=={'PASS':164,'RED':17} and counts(rows[-1]['cases'])=={'PASS':40,'RED':27}
  dump(ROOT/('execution/'+epoch+'/case_matrix.json'),dict(court_181=all_cases,counts_181=counts(all_cases),g14_67=rows[-1]['cases'],counts_g14=counts(rows[-1]['cases'])))
 frozen_red=read('frozen/g14/02_ORIGINAL_17_REDS.json')['cases'];base=read('execution/baseline/case_matrix.json');cand=read('execution/candidate/case_matrix.json')
 bindex={(c['suite'],c['name']):c for c in base['court_181']};cindex={(c['suite'],c['name']):c for c in cand['court_181']}
 preserved=[]
 for row in frozen_red:
  key=(row['suite'],row['name']);assert bindex[key]['status']=='RED';assert cindex[key]['status']=='RED',key
  preserved.append(dict(**row,G15_literal_status=cindex[key]['status'],baseline_literal_status=bindex[key]['status']))
 dump(ROOT/'04_ORIGINAL_17_RED_COMPARISON.json',dict(count=17,all_17_remain_literal_RED=True,no_oracle_changes=True,cases=preserved))
 # Literal new failures are never waived. Preserve per-case handler exceptions as
 # NOT_EVALUABLE, never as direct scientific falsification or a green predicate.
 actual=read('runs/candidate/reproduction/03_POSTREPAIR_COURT/evidence/sgi1_actual.json')
 not_evaluable=[dict(case_id=c['case_id'],observed=c['observed_state']) for c in actual['cases'] if c['observed_state'].get('status')=='LEGACY_HANDLER_NOT_EVALUABLE']
 newreds=[dict(**c,baseline_status=bindex[(c['suite'],c['name'])]['status']) for c in cand['court_181'] if c['status']=='RED' and bindex[(c['suite'],c['name'])]['status']=='PASS']
 dump(ROOT/'05_INHERITED_RED_FLAGS.json',dict(additional_literal_RED_count=len(newreds),cases=newreds,legacy_handlers_not_evaluable=not_evaluable,qualification='All 181 frozen pytest tests execute unchanged. G15 runner records former positive-handler shape exceptions as all-unproved, with exact exception evidence. These predicate groups were NOT individually evaluated and are not claimed scientifically disproved.'))
 # Independent same assertions, before and after, with scientific classification.
 frozen_g14=read('frozen/g14/01_CASE_MATRIX.json')['independent_g14'];gi={c['name']:c for c in cand['g14_67']}
 adjudication=[]
 prereg={x['name']:x for x in read('01_CAUSATION_PREREGISTRATION.json')['reds']}
 for x in frozen_g14:
  adj=dict(name=x['name'],family=x['family'],baseline=x['status'],candidate=gi[x['name']]['status'],expected_assertions=x['expected_assertions'],original_source_file='frozen/g14/test_g14_science.py',classification=prereg[x['name']]['classification'] if x['name'] in prereg else 'PRESERVED_CONTROL',grade='ASSERTION_EFFICACY_PROVED_AT_SOURCEFREE_SCOPE' if x['name'] in prereg else 'EXECUTED_CONTROL')
  adjudication.append(adj)
 dump(ROOT/'06_G14_SAME_ASSERTION_COMPARISON.json',dict(count=67,baseline=base['counts_g14'],candidate=cand['counts_g14'],cases=adjudication))
 # Verify every original test source in the execution copies remains exact.
 tests=[]
 for epoch in ['baseline','candidate']:
  for p in (ROOT/'runs'/epoch/'reproduction').rglob('test*.py'):
   rel=p.relative_to(ROOT/'runs'/epoch/'reproduction');src=ROOT/'frozen/g13'/rel
   assert src.exists() and src.read_bytes()==p.read_bytes(),str(rel)
   tests.append(dict(epoch=epoch,path=str(p.relative_to(ROOT)),sha256=sha(p)))
 source_graph=[]
 for p in sorted((ROOT/'candidate').rglob('*')):
  if p.is_file() and '__pycache__' not in p.parts:
   b=p.read_bytes();source_graph.append(dict(path=str(p.relative_to(ROOT)),sha256=sha(p),git_blob_sha1=blob(b)))
 obs=read('execution/prospective_observations.json')
 assert obs['network_attempts']==[] and obs['new_provider_calls']==0
 for imp in obs['imports']:
  assert sha(ROOT/imp['path'])==imp['sha256']
 dump(ROOT/'custody/source_and_import_graph.json',dict(frozen_object_count=len(frozen),verified_G13_imports=modules,original_manifest_preimage_count=len(original['original_manifest_preimages']),candidate_source_graph=source_graph,actual_prospective_imports=obs['imports'],unchanged_test_copies=tests,closure='FULL_RUNNABLE_SOURCEFREE_RESEARCH_NOT_NATIVE_V3'))
 print(json.dumps(dict(frozen_objects=len(frozen),baseline181=base['counts_181'],candidate181=cand['counts_181'],G14=cand['counts_g14'],original17_preserved=True,additional_RED=len(newreds),legacy_handler_groups_not_evaluable=len(not_evaluable)),sort_keys=True))
if __name__=='__main__':main()
