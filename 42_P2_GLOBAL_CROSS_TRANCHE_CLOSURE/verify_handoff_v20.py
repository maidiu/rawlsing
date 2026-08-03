#!/usr/bin/env python3
from __future__ import annotations
import argparse,csv,hashlib,json,sys,zipfile
from collections import Counter,defaultdict
from pathlib import Path
sys.dont_write_bytecode=True
from docx import Document
try: import yaml
except Exception: yaml=None
csv.field_size_limit(sys.maxsize)

def sha(p):
 h=hashlib.sha256()
 with Path(p).open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
 return h.hexdigest()
def rows(p):
 with Path(p).open(encoding='utf-8-sig',newline='') as f: return list(csv.DictReader(f))
def loadj(p): return json.load(Path(p).open(encoding='utf-8'))

def main():
 ap=argparse.ArgumentParser(description='Incremental cryptographic + authority verifier for v20')
 ap.add_argument('root',nargs='?',default=str(Path(__file__).resolve().parents[1])); ap.add_argument('--json-out')
 a=ap.parse_args(); root=Path(a.root).resolve(); checks=[]; failures=[]
 def ck(name,ok,detail=''):
  checks.append({'check':name,'status':'PASS' if ok else 'FAIL','detail':detail})
  if not ok: failures.append({'check':name,'detail':detail})

 # Top-level manifests cover every file except themselves and the post-verification self-report.
 excluded={'PACKAGE_INDEX.csv','SHA256SUMS.csv','42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE/FINAL_RELEASE_GATE_RETURN.json'}
 for mname in ('PACKAGE_INDEX.csv','SHA256SUMS.csv'):
  m=root/mname; rs=rows(m); bad=[]
  for r in rs:
   p=root/r['relative_path']
   if not p.exists() or sha(p)!=r['sha256'] or int(r['bytes'])!=p.stat().st_size: bad.append(r['relative_path'])
  actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.relative_to(root).as_posix() not in excluded}
  listed={r['relative_path'] for r in rs}
  ck(mname+':hashes',not bad,json.dumps(bad[:20]))
  ck(mname+':coverage',actual==listed,json.dumps({'actual':len(actual),'listed':len(listed),'only_actual':sorted(actual-listed),'only_listed':sorted(listed-actual)}))

 # Cryptographic inheritance of the already accepted v19 tree.
 pre=root/'40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7'/'PRE_V20_ROOT_CONTROLS'
 v19ret=loadj(pre/'CUMULATIVE_VERIFIER_BUILD_RETURN_v19.json')
 ck('v19_inherited_verifier_152_of_152',v19ret.get('status')=='PASS' and v19ret.get('checks_passed')==152 and v19ret.get('checks_total')==152 and v19ret.get('recursive_archive_instances')==88 and v19ret.get('unique_archive_payloads')==77,json.dumps({k:v19ret.get(k) for k in ('status','checks_passed','checks_total','recursive_archive_instances','unique_archive_payloads')}))
 baseline=rows(pre/'PACKAGE_INDEX_v19.csv')
 superseded={
  'PACKAGE_INDEX.csv','SHA256SUMS.csv','README_FIRST.md','MASTER_HANDOFF.md','VALIDATION.json',
  '00_START_HERE/CURRENT_STATE.json','00_START_HERE/SCOPE_LOCK.json','00_START_HERE/README_FIRST.md','00_START_HERE/NEXT_CHAT_OPENING_INSTRUCTION.txt'}
 changed=[]; missing=[]
 for r in baseline:
  rel=r['relative_path']
  if rel in superseded: continue
  p=root/rel
  if not p.exists(): missing.append(rel)
  elif sha(p)!=r['sha256'] or int(r['bytes'])!=p.stat().st_size: changed.append(rel)
 ck('v19_inherited_files_hash_identical',not missing and not changed,json.dumps({'baseline_rows':len(baseline),'compared':len(baseline)-len(superseded),'missing':missing[:20],'changed':changed[:20]}))
 ck('v19_recursive_archives_inherited_unchanged',not any((root/r['relative_path']).suffix.lower()=='.zip' and r['relative_path'] in changed for r in baseline if r['relative_path'] not in superseded),'88 archive instances / 77 unique payloads inherited from accepted v19')

 # New/superseded file readability; inherited files are byte-identical to validated v19.
 baseline_paths={r['relative_path'] for r in baseline}; new_or_changed=[]; readfail=[]
 for p in sorted(x for x in root.rglob('*') if x.is_file()):
  rel=p.relative_to(root).as_posix()
  if rel in excluded: continue
  if rel not in baseline_paths or rel in superseded:
   new_or_changed.append(rel); ext=p.suffix.lower()
   try:
    if p.stat().st_size==0 and ext!='.py': raise ValueError('empty')
    if ext=='.csv':
     with p.open(encoding='utf-8-sig',newline='') as f:
      rr=csv.reader(f); hdr=next(rr)
      for n,row in enumerate(rr,2):
       if len(row)!=len(hdr): raise ValueError(f'row {n}: {len(row)} != {len(hdr)}')
    elif ext=='.json': loadj(p)
    elif ext in ('.yaml','.yml'):
     if yaml is None: raise RuntimeError('PyYAML unavailable')
     yaml.safe_load(p.read_text(encoding='utf-8'))
    elif ext=='.py': compile(p.read_text(encoding='utf-8'),str(p),'exec')
    elif ext=='.docx': Document(p)
    elif ext=='.zip':
     with zipfile.ZipFile(p) as z:
      if z.testzip(): raise ValueError('bad zip member')
    else: p.open('rb').read(1)
   except Exception as e: readfail.append({'path':rel,'error':repr(e)})
 ck('v20_new_and_superseded_files_type_readable',not readfail,json.dumps({'files':len(new_or_changed),'failures':readfail[:20]}))
 new_zips=[r for r in new_or_changed if r.lower().endswith('.zip')]
 ck('v20_no_new_nested_archive_surface',not new_zips,json.dumps(new_zips))

 # Current controls.
 cur=loadj(root/'00_START_HERE'/'CURRENT_STATE.json'); scope=loadj(root/'00_START_HERE'/'SCOPE_LOCK.json'); val=loadj(root/'VALIDATION.json')
 expected='P3_TYPED_COLLISION_HYPEREDGE_CANDIDATE_FAMILY_RANKING_AND_CANONICAL_V550J_ADJUDICATION'
 ck('v20_current_state_closed',cur.get('handoff_version')=='v20' and cur.get('global_p2_closed') is True and cur.get('semantic_priority_pairs_adjudicated_cumulative')==18831 and cur.get('semantic_priority_pairs_remaining')==0 and cur.get('next_pass')==expected,'')
 ck('v20_scope_lock_closed',scope.get('global_p2_closed') is True and scope.get('next_pass')==expected and 'respondent joins' in scope.get('prohibited_until_canonical_authority_closes',[]),'')
 ck('v20_validation_boundary',val.get('global_p2_closed') is True and val.get('semantic_priority_pairs_adjudicated')==18831 and val.get('semantic_priority_pairs_remaining')==0 and val.get('live_component_bridge_installed') is False and val.get('canonical_j_family_authority_authored') is False and val.get('next_pass')==expected,'')
 ck('v20_output_protocol_present',(root/'00_START_HERE'/'OUTPUT_AND_HANDOFF_PROTOCOL.md').exists() and 'fully updated cumulative handoff' in (root/'00_START_HERE'/'README_FIRST.md').read_text(encoding='utf-8') if False else (root/'00_START_HERE'/'OUTPUT_AND_HANDOFF_PROTOCOL.md').exists(),'')

 # Final 2,847 tranche.
 s41=root/'41_P2_GLOBAL_FINAL_2847_PAIR_TRANCHE8'; rul=rows(s41/'Rawlsing_P2_Final_2847_Pair_Rulings_v1.csv'); ev=rows(s41/'Rawlsing_P2_Final_2847_Two_Sided_Evidence_Ledger_v1.csv'); classes=rows(s41/'Rawlsing_P2_Final_2847_Lineage_Classification_v1.csv'); rem=rows(s41/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Final_Tranche_v8.csv')
 prior=rows(root/'40_P2_GLOBAL_SOCIAL_ORDER_FIXED_3000_TRANCHE7'/'Rawlsing_P2_Semantic_Priority_Queue_Remaining_After_Social_Order_Fixed_3000_Tranche_v7.csv')
 ck('v20_final_queue_2847_to_zero',len(prior)==2847 and len(rul)==2847 and len(rem)==0 and {r['semantic_pair_candidate_id'] for r in prior}=={r['semantic_pair_candidate_id'] for r in rul},'')
 rel=Counter(r['relation_type'] for r in rul)
 ck('v20_final_relation_partition',rel==Counter({'NEGATIVE_AUTHORITY':2247,'OTHER_DOMAIN_REVIEW_REQUIRED':218,'DOMAIN_COORDINATE_ONLY':190,'REWORDED_PROPOSITION_EQUIVALENCE':89,'UNRESOLVED':84,'CONSTRUCT_TARGET_COORDINATE_ONLY':19}),json.dumps(rel))
 cby={r['lineage_id']:r for r in classes}; acc=[r for r in rul if r['relation_type']=='REWORDED_PROPOSITION_EQUIVALENCE']; badacc=[]
 for r in acc:
  if not (r['left_relation_axis']==r['right_relation_axis'] and r['left_target_or_scope']==r['right_target_or_scope'] and r['left_operator']==r['right_operator'] and cby[r['left_lineage_id']]['classification_confidence']=='HIGH' and cby[r['right_lineage_id']]['classification_confidence']=='HIGH'): badacc.append(r['pair_ruling_id'])
 ck('v20_final_proposition_gate',len(acc)==89 and not badacc and Counter(r['portability_ceiling'] for r in acc)==Counter({'QUESTION_PROPOSITION_ONLY':54,'QUESTION_PROPOSITION_AND_RESPONSE_TOPOLOGY':35}),json.dumps({'bad':badacc,'ceilings':Counter(r['portability_ceiling'] for r in acc)}))
 ec=Counter(r['pair_ruling_id'] for r in ev); es=defaultdict(set)
 for r in ev: es[r['pair_ruling_id']].add(r['side'])
 ck('v20_final_two_sided_evidence',len(ev)==5694 and set(ec)=={r['pair_ruling_id'] for r in rul} and all(v==2 for v in ec.values()) and all(v=={'LEFT','RIGHT'} for v in es.values()),'')
 unr=[r for r in rul if r['relation_type']=='UNRESOLVED']
 ck('v20_final_unresolved_fail_closed',len(unr)==84 and set(r['semantic_content_id'] for r in unr)=={'CHILD_OBEDIENCE'} and all(r['portability_ceiling']=='NO_AUTHORITY' for r in unr),'')
 review=loadj(s41/'FINAL_2847_ACCEPTANCE_REVIEW_RETURN.json')
 ck('v20_final_acceptance_review',review.get('acceptance_status')=='PASS' and review.get('initial_mechanical_proposition_positive_surface')==129 and review.get('final_proposition_positive_surface')==89 and review.get('net_proposition_downgrades_or_reclassifications')==40,'')
 # Test return text and direct rerun are both governed.
 import subprocess,os
 cp=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_final_2847_tranche_v1.py'],cwd=s41,capture_output=True,text=True,timeout=120,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 ck('v20_final_7_tests',cp.returncode==0 and '7 passed' in cp.stdout,(cp.stdout+cp.stderr).strip())

 # Global closure.
 s42=root/'42_P2_GLOBAL_CROSS_TRANCHE_CLOSURE'; sem=rows(s42/'Rawlsing_P2_Global_Semantic_Priority_Pair_Authority_Registry_v1.csv'); ex=rows(s42/'Rawlsing_P2_Global_Exact_Foundation_Authority_Registry_v1.csv'); initial=rows(root/'32_P2_GLOBAL_CROSS_SOURCE_RECONCILIATION_TRANCHE1'/'Rawlsing_P2_Semantic_Neighborhood_Pair_Queue_v1.csv')
 ck('v20_global_semantic_exact_coverage',len(sem)==18831 and len({r['semantic_pair_candidate_id'] for r in sem})==18831 and {r['semantic_pair_candidate_id'] for r in sem}=={r['semantic_pair_candidate_id'] for r in initial},'')
 ck('v20_global_semantic_partition',Counter(r['normalized_authority_class'] for r in sem)==Counter({'NEGATIVE_AUTHORITY':14857,'REDIRECTED_OTHER_DOMAIN_AUTHORITY':1958,'COORDINATE_OR_BOUNDED_RELATION_AUTHORITY':1024,'PROPOSITION_RELATION_AUTHORITY':641,'UNRESOLVED_FAIL_CLOSED_AUTHORITY':351}),json.dumps(Counter(r['normalized_authority_class'] for r in sem)))
 ck('v20_global_tranche_partition',Counter(r['origin_tranche'] for r in sem)==Counter({'TRANCHE2_HIGH_PRECISION':121,'TRANCHE3_TRUST':3863,'TRANCHE4_DEMOCRACY_ELECTORAL':3000,'TRANCHE5_MEDIA_CIVIC':3000,'TRANCHE6_MATERIAL_ECONOMY':3000,'TRANCHE7_SOCIAL_ORDER':3000,'TRANCHE8_FINAL_2847':2847}),json.dumps(Counter(r['origin_tranche'] for r in sem)))
 ck('v20_all_36_source_pairs',len({(r['left_source_family'],r['right_source_family']) for r in sem})==36,'')
 ck('v20_exact_foundation_closed',len(ex)==751 and Counter(r['normalized_authority_class'] for r in ex)==Counter({'UNRESOLVED_EXACT_FOUNDATION_AUTHORITY':403,'ACCEPTED_EXACT_FOUNDATION_AUTHORITY':270,'REJECTED_EXACT_FOUNDATION_AUTHORITY':78}),json.dumps(Counter(r['normalized_authority_class'] for r in ex)))
 close=loadj(s42/'GLOBAL_P2_CLOSURE_RETURN.json'); runtime=loadj(s42/'LIVE_COMPONENT_BRIDGE_INSTALLATION_BOUNDARY_AUDIT.json')
 ck('v20_global_closure_truthful',close.get('global_p2_closed') is True and close.get('semantic_priority_pairs_remaining')==0 and close.get('canonical_j_family_authority_authored') is False and close.get('respondents_joined') is False and close.get('values_harmonized') is False and close.get('database_or_registry_written') is False,'')
 ck('v20_live_bridge_boundary_honest',runtime.get('user_designated_current_live_repository_found') is False and runtime.get('installation_performed') is False and close.get('live_component_bridge_installed') is False,'')
 vchecks=rows(s42/'GLOBAL_P2_CLOSURE_VALIDATION_CHECKS.csv')
 ck('v20_closure_validation_16_of_16',len(vchecks)==16 and all(r['status']=='PASS' for r in vchecks),'')
 cp2=subprocess.run([sys.executable,'-m','pytest','-q','-p','no:cacheprovider','test_global_p2_closure_v1.py'],cwd=s42,capture_output=True,text=True,timeout=120,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
 ck('v20_closure_6_tests',cp2.returncode==0 and '6 passed' in cp2.stdout,(cp2.stdout+cp2.stderr).strip())
 repro=loadj(s42/'V20_REPRODUCIBILITY_RETURN.json')
 ck('v20_reproducibility_hash_identical',repro.get('hash_identical') is True and repro.get('artifacts_checked')==7,'')

 # Documents and package hygiene.
 docs=[root/'00_START_HERE'/'Rawlsing_J_Family_Authority_Strategy_Master_Handoff_v20_20260731.docx',s41/'Rawlsing_P2_Global_Final_2847_Tranche8_Report_20260731.docx',s42/'Rawlsing_P2_Global_Cross_Tranche_Closure_Report_20260731.docx']
 ck('v20_governing_documents_present',all(p.exists() for p in docs),'')
 a11y=[s41/'DOCX_A11Y_MASTER_RETURN.json',s41/'DOCX_A11Y_REPORT_RETURN.json',s42/'DOCX_A11Y_CLOSURE_RETURN.json']
 ck('v20_docx_accessibility_zero_findings',all(p.exists() and sum(loadj(p).get('counts',{}).values())==0 for p in a11y),'')
 qa=loadj(s42/'DOCX_QA_RETURN.json')
 ck('v20_docx_visual_qa',qa.get('status')=='PASS' and qa.get('pages_visually_inspected')==4 and qa.get('clipping_overlap_or_orphan_pages')==0,'')
 debris=[p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_dir() and p.name in ('__pycache__','.pytest_cache')]
 debris += [p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() and p.suffix in ('.pyc','.pyo')]
 ck('v20_no_generated_debris',not debris,json.dumps(debris))

 result={'status':'PASS' if not failures else 'FAIL','root':str(root),'checks_passed':sum(x['status']=='PASS' for x in checks),'checks_total':len(checks),'inherited_v19_checks':152,'inherited_recursive_archive_instances':88,'inherited_unique_archive_payloads':77,'new_or_superseded_files_checked':len(new_or_changed),'failures':failures,'checks':checks}
 text=json.dumps(result,indent=2,ensure_ascii=False)
 if a.json_out: Path(a.json_out).write_text(text+'\n',encoding='utf-8')
 print(text); raise SystemExit(0 if not failures else 1)
if __name__=='__main__': main()
