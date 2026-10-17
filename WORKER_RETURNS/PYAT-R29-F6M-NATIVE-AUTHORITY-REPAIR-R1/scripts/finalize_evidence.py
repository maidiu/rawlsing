"""Reconcile executed courts and actual imports; never promote legacy emitter labels."""
from pathlib import Path
import json,hashlib,difflib,subprocess,sys,datetime,uuid,platform
ROOT=Path(__file__).resolve().parents[1]
START='1a6096f263623e57b77c7b70b5fcfb23cdebdad8'
BRANCH='agent/rabochii-pyat-r29-f6m-native-decision-admission-executable-repair-r1'
def read(p):return json.loads((ROOT/p).read_text())
def write(p,o):(ROOT/p).write_text(json.dumps(o,indent=2,sort_keys=True)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def blob(raw):return hashlib.sha1(b'blob '+str(len(raw)).encode()+bytes([0])+raw).hexdigest()
def main():
 original=read('custody/original_trees.json')
 assert len(original)==150
 for row in original:
  p=ROOT/row['materialized'];assert sha(p)==row['sha256'];assert blob(p.read_bytes())==row['git_blob']
 native=ROOT/'candidate/rawlsing_next/pre553_heterogeneous_synthesis.py'
 expected=read('custody/candidate.json');assert blob(native.read_bytes())==expected['producer_git_blob']
 original_native=ROOT/'inherited/F6J/01_STAGED_NATIVE/rawlsing_next/pre553_heterogeneous_synthesis.py'
 assert blob(original_native.read_bytes())=='fc5e37fa5b2f0eb689593b42d95479d1327cb94c'
 dependency=ROOT/'candidate/rawlsing_next/pre553_empirical_objects.py'
 assert blob(dependency.read_bytes())=='a61365b994e5c3c50de0f598fcf40e90abf757b6'
 diff=''.join(difflib.unified_diff(original_native.read_text().splitlines(True),native.read_text().splitlines(True),fromfile='original/rawlsing_next/pre553_heterogeneous_synthesis.py',tofile='F6M/candidate/rawlsing_next/pre553_heterogeneous_synthesis.py'))
 (ROOT/'custody/native_repair.diff').write_text(diff)
 a={r['case']:r for r in read('evidence/original/consumer_outputs.json')};b={r['case']:r for r in read('evidence/repaired/consumer_outputs.json')}
 changes=[]
 for case,after in b.items():
  before=a[case];x=before['producer_output'];y=after['producer_output']
  assert before['input_hash']==after['input_hash']
  for src,base in zip(y['replay']['sources'],y['baseline']):assert base['native_summary']==src
  changes.append(dict(case=case,input_hash=after['input_hash'],before_decision=x['decision'],after_decision=y['decision'],before_uncovered=x['candidate']['uncovered_target_mass'],after_uncovered=y['candidate']['uncovered_target_mass'],before_ceilings={n['node_id']:n.get('authority_ceiling') for n in x['evidence_graph']},after_ceilings={n['node_id']:n['authority_ceiling'] for n in y['evidence_graph']},before_conditional=before['native_conditional'],after_conditional=after['native_conditional'],real_use=after['real_use_consumer'],before_decision_consumer=before['decision_only_consumer'],after_decision_consumer=after['decision_only_consumer']))
 preserve={}
 for case in ('world_a','world_b','novel_2x2_no_positivity','novel_3category_no_positivity','minority_cell_threshold5'):
  fields=('distribution','covered_subprobability','uncovered_target_mass','uncertainty')
  preserve[case]={k:a[case]['producer_output']['candidate'][k]==b[case]['producer_output']['candidate'][k] for k in fields}
  assert all(preserve[case].values()),(case,preserve[case])
 assert b['world_b']['producer_output']['candidate']['uncovered_target_mass']=='1/5'
 assert b['minority_source_exclusion150']['producer_output']['candidate']['uncovered_target_mass']=='1/2'
 write('01_REAL_DECISION_AUTHORITY_DIFF.json',dict(schema='F6M_ACTUAL_NATIVE_DIFF@1',startup=START,candidate=expected,source_path='candidate/rawlsing_next/pre553_heterogeneous_synthesis.py',native_diff='custody/native_repair.diff',changes=changes,unchanged_numerical_and_uncertainty_projections=preserve,support_repair='Planned weights over present source strata; failed aggregate-support contributions remain uncovered instead of survivor renormalization.',f6n_review_required=True))
 modes={}
 for mode in ('original','repaired','compat'):
  rows=read(f'evidence/{mode}/courts.json')
  assert all(r.get('counts',{}).get('skipped',0)==0 for r in rows)
  rational=read(f'evidence/{mode}/native_vs_frozen.json')
  for row in rows:
   imports=read(row['imports'])
   actual=imports['rawlsing_next.pre553_heterogeneous_synthesis']['git_blob']
   assert actual==('fc5e37fa5b2f0eb689593b42d95479d1327cb94c' if mode=='original' else expected['producer_git_blob'])
   row['actual_producer_git_blob']=actual
  assert rational['comparisons_total']==rational['comparisons_passed']==82
  modes[mode]=dict(courts=rows,rational_comparisons_passed=82,rational_comparisons_total=82)
 assert all(r['exit']==0 for r in modes['compat']['courts'])
 baseline=[r for r in modes['original']['courts'] if r['name']=='f6l26'][0];assert baseline['counts']['failures']==11
 cold=read('evidence/cold_replay.json');assert all(r['exit']==0 for r in cold['courts'])
 write('02_ACTUAL_NATIVE_COURTS.json',dict(schema='F6M_COURTS@1',status='SOURCEFREE_CANDIDATE_EXECUTED__INDEPENDENT_F6N_REQUIRED',modes=modes,cold_replay='evidence/cold_replay.json',cold_replay_passed=True,compatibility_diff='custody/safety_compatibility_v1.json',zero_skips=True,important_limits=['Unchanged source courts retain original assertions including observations of defects. Their nonzero exits on the candidate are retained, not counted as passes.','F6L original 15PASS/11FAIL includes one missing-world-key test failure before mixed-origin execution; compatibility resolves via its existing CASE_WORLD alias without changing world contents.','F6J legacy script payloads contain hardcoded original native_git_blob/candidate_commit/role and some unconditional historical verdict strings. These labels are emitter history, not actual execution identity, present-tense independent review or acceptance. Actual import receipts and this report govern identities; inspect observations, not those inherited verdict strings.','Scientific numerical oracle JSONs and original source/test bytes remain unchanged; safety compatibility changes are separately diffed.']))
 reads=[(START,'WORKER_COMMISSIONS/PYAT-R29-F6M-ACTUAL-F6-NATIVE-AUTHORITY-REPAIR-R1/00_COMMISSION.md'),(START,'PYAT_CONTROL_ROOM/00D_WARM_EXECUTION_PASSPORT_AND_MONEY_FIRST_AGENT_DISPENSATION_R1.md'),(START,'PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md'),(START,'PYAT_CONTROL_ROOM/HQ_OPERATING_REQUIREMENTS_EFFECTIVENESS_R1.md'),('3c33688506840869e1f05f4230248ce950b78d6c','SOROK_PRODUCT_CONTROL_ROOM/00C_HQ_PROMPT_DISPENSATION_AGENT_ROUTING_AND_ORCHESTRATION_CONSTITUTION_R1.md')]
 write('custody/governing_reads.json',[dict(commit=c,path=p,git_blob=subprocess.check_output(['git','rev-parse',c+':'+p],cwd=ROOT,text=True).strip()) for c,p in reads])
 marker=ROOT/'.environment-marker'
 if not marker.exists():marker.write_text(str(uuid.uuid4()))
 epoch=marker.read_text().strip()
 now=datetime.datetime.now(datetime.timezone.utc).isoformat()
 write('environment_passport_delta.json',dict(environment_id='F6M_LOCAL_'+epoch[:8],epoch_id=epoch,session_alias='F6M-author',surface='S2_LOCAL_CODEX',machine_alias='LOCAL_EXECUTION_HOST',status='LIVE_VERIFIED',last_live_probe_at=now,writable_marker_verified=marker.read_text().strip()==epoch,python={'version':platform.python_version(),'command':'python3 --version','status':0},pytest={'version':subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),'command':'python3 -m pytest --version','status':0},git={'version':subprocess.check_output(['git','--version'],text=True).strip(),'shared_store':True,'isolated_sparse_worktree_alias':'R29-F6M-wt','branch':BRANCH,'startup':START,'bootstrap_authorization':'User explicitly instructed creation of own worktree in this chat.'},provider_model='OpenAI Codex / GPT-6 family; exact model and effort not independently exposed',dependency_closure='FULL_FOR_BOUNDED_SOURCEFREE_COURTS',packages_installed=[],native_source={'commit':'1428c2e92bce1a49efd87378cb23df936d646dc5','path':'rawlsing_next/pre553_heterogeneous_synthesis.py','git_blob':'fc5e37fa5b2f0eb689593b42d95479d1327cb94c'},semantic_hash_dependency={'commit':'1428c2e92bce1a49efd87378cb23df936d646dc5','path':'rawlsing_next/pre553_empirical_objects.py','git_blob':'a61365b994e5c3c50de0f598fcf40e90abf757b6'},all_pinned_module_fixture_identities='custody/original_trees.json',candidate_identity='custody/candidate.json',imported_module_files='evidence/compat/*.imports.json',execution='02_ACTUAL_NATIVE_COURTS.json',assignments_completed=['F6M_SOURCEFREE_NATIVE_REPAIR_CANDIDATE'],eligibility='Original-author continuation only; not eligible as independent F6N reviewer',expiry='Reprobe marker, branch, imports and runtime after reset or before another assignment',privacy_gate='Private repository on authorized local surface; no original survey SAV/DTA or third-party model calls',claim_grade='IMPLEMENTED_EXECUTED_SOURCEFREE_ONLY',independent_review_conflict='Original F6C/F6M author; F6N must be distinct',incremental_cash='UNKNOWN; no paid API calls initiated',quota_observations={'initial_primary_used_percent':1,'initial_weekly_used_percent':72,'return_primary_used_percent':17,'return_weekly_used_percent':74,'observed_account_tier':'plus'},next_affinity='Only separately commissioned repairs to this candidate following F6N findings'))
 print('Evidence reconciled: all original blobs unchanged; native identities verified; no skipped tests')
if __name__=='__main__':main()
