from pathlib import Path
import json,hashlib,xml.etree.ElementTree as ET,subprocess,datetime
R=Path(__file__).resolve().parents[1];root=R.parents[1]
def read(n):return json.loads((R/n).read_text())
def put(n,x):(R/n).write_text(json.dumps(x,indent=2)+'\n')
def suite(n):
 tree=ET.parse(R/f'observations/{n}.xml');cases=[]
 for c in tree.findall('.//testcase'):
  f=c.find('failure');err=c.find('error');skip=c.find('skipped')
  cases.append({'name':c.attrib['name'],'state':'FAIL' if f is not None else 'ERROR' if err is not None else 'SKIP' if skip is not None else 'PASS','message':None if f is None else f.attrib.get('message')})
 return {'cases':cases,'pass':sum(c['state']=='PASS' for c in cases),'fail':sum(c['state']=='FAIL' for c in cases),'total':len(cases),'skip':sum(c['state']=='SKIP' for c in cases),'error':sum(c['state']=='ERROR' for c in cases),'terminal':read(f'observations/{n}.terminal.json')}
b=read('observations/baseline.json');ex=read('observations/experiments.json');cold=read('observations/cold_comparison.json');a=suite('author');i=suite('independent');sel=read('source_selector.json');oracle=read('01_FROZEN_ORACLE_AND_PINNED_OWNERS.json')
assert hashlib.sha256((R/'01_FROZEN_ORACLE_AND_PINNED_OWNERS.json').read_bytes()).hexdigest()=='5144c481300e8f8c158cfe67fbcf2ee2746f66529fc5ac2757f1a65b5f330f58'
assert (a['pass'],a['fail'],i['pass'],i['fail'])==(29,0,24,20)
assert a['skip']==i['skip']==a['error']==i['error']==0
checks=[]
for r in sel['files']:
 data=(R/'runtime_root'/r['staging_path']).read_bytes();assert hashlib.sha256(data).hexdigest()==r['sha256'];assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==r['git_blob_sha1']
 checks.append(r['staging_path'])
for m in b['imports']:
 rel=str(Path(m['file']).relative_to(R/'runtime_root'));row=next(x for x in sel['files'] if x['staging_path']==rel);assert row['git_blob_sha1']==m['git_blob_sha1']
(R/'observations/candidate_original_ledger.json').write_bytes((R/'runtime_root/candidate/01_FULL_OPPORTUNITY_AND_DISPOSITION_LEDGER.json').read_bytes())
oldnames=[c['name'] for c in a['cases'] if c['name'].startswith('test_red_')];assert len(oldnames)==15
judgments=[
('CLOSED_FIXTURE','Missing operation raises; unknown operation independent guard PASS. No 1/2 fallback.'),
('CLOSED_FIXTURE','None, negative -1, foreign values independently rejected. Other missing event accepted with typed incomplete output; inspect experiments.'),
('CLOSED_SOURCEFREE_OWNER','Three real ingest and commit calls; sealed C11LogicalRelease resolved in one repository; no candidate private injection.'),
('CLOSED_NEGATIVE_ONLY','No automatically produced same-grain pair; split-ballot held. Frozen product positive conditional still unproved.'),
('CLOSED_TOKEN_GATE_TEST_ONLY','Unknown rights tokens hold; not independent issuer/currentness proof.'),
('CLOSED_TOKEN_GATE_TEST_ONLY','Arbitrary grant token holds. Literal GRANTED_FIXTURE remains locally authored test authorization.'),
('CLOSED_HASH_ONLY','Options change freeze; actual source/query domain remains hardcoded. Wider source-native semantic closure RED.'),
('CLOSED_HASH_ONLY','Permission string changes freeze; late read does not consult current grant.'),
('CLOSED_BASELINE','Withdrawn conditioning pair retained HELD in independently exact25 oracle.'),
('CLOSED_BASELINE','Unrouteable conditioning pair retained HELD in independently exact25 oracle.'),
('CLOSED_FIXTURE','Conflicting same-form carrier explicitly refused; independent guard PASS.'),
('PARTIAL_RED','Changed item_ids/target duplicate refused, but changed conditioners/op_class/reason accepted under same ID.'),
('PARTIAL_RED','Baseline25 retained; omitted HELD or INADMISSIBLE produces24 and identical full 3-unit manifest/receipts. No independently enforced expected frontier.'),
('PARTIAL_RED','Author test checks unit identity only; actual changed options still compute identical original cells. Source row changes compute different values but retain source artifact hash.'),
('TEST_ONLY_HOLD','Plan carries local string and fixture issuer, not a separately trustworthy issued source grant; read revocation fails.')]
closure=[{'previous_test':name,'author_replay':'PASS','independent_judgment':v,'basis':reason} for name,(v,reason) in zip(oldnames,judgments)]
put('02_ACTUAL_OWNER_CALLS_AND_NEW_HOSTILES.json',{'schema':'WG0J_ACTUAL_EXECUTED_COURT@1','verdict':'RED','candidate':sel['candidate'],'oracle_sha256':'5144c481300e8f8c158cfe67fbcf2ee2746f66529fc5ac2757f1a65b5f330f58','author_suite':a,'independent_suite':i,'all15_claimed_repairs':closure,'actual_owner_calls':b['owner_calls'],'actual_imports':b['imports'],'source_integrity_post_execution':{'all29_staged_files_unchanged':len(checks)==29,'actual_NUL_git_preimages_verified':True},'actual_releases':[{'tag':r['tag'],'class':r['class'],'release_ref':r['ref'],'source_artifact_ref':r['source_artifact']} for r in b['releases']],'batch_summary':b['summary'],'numeric_evidence':'observations/independent_native_reconstruction.json','full_baseline_evidence':'observations/baseline.json','hostile_counterexamples':'observations/experiments.json','documentary_count_audit':ex['ledger'],'positive_conditional':'Independent qualified manifest ran real I03 via accepted batch; observations/positive_conditional_batch.json. This is separate mechanism, zero positive conditionals in frozen25.','cold_replay':{'identical_receipts':cold['cold_identical_receipts'],'identical_values':cold['cold_identical_values'],'frontier25':cold['cold_frontier25'],'shard_values':cold['shard_values_match_full'],'checkpoint_exit':cold['processes']['checkpoint']['exit'],'resume_summary':cold['resume']['summary'],'resume_consumer_error':cold['resume']['consumer_error']},'permission_grade':'TEST_ONLY synthetic snapshots; original source/E/C11 issuer/model-use remain HOLD','harness_corrections':'Initial independent run had reviewer record-envelope extraction error; corrected. Intermediate DENY test expected exception; accepted owner law returns typed UNAVAILABLE, now PASS. Two probe serialization errors retained separately. These are not candidate failures; final44 has no errors/skips. Candidate files never edited.'})
passport={'schema':'WG0J_REVIEWER_PASSPORT@1','at':datetime.datetime.now(datetime.timezone.utc).isoformat(),'role':'Distinct independent reviewer; no WG0P2/WG0I implementation; no source or adopter authority','assigned_branch':'agent/userdirect-pyat-20261014-r6-wg0j-independent-workload-court-r1','sealed_start':'328fd01473f50872e77d5325936713c2946609c1','sealed_start_parent':'0d551d36ff19dc9806e0ad490ff33a1e4c25e381','direct_remote':'https://github.com/maidiu/rawlsing.git','worktree':str(root),'model':'gpt-6.1-sol','effort':'medium','model_evidence':'Own latest turn_context in /Users/matthewsmith/.codex/sessions/2026/10/14/rollout-2026-10-14T10-14-07-01a13ac3-6875-7bc0-9d56-d1124400de89.jsonl; fields model/effort only inspected','quota_initial':{'ordinaryUsageAllowed':True,'primaryUsedPercent':18,'weeklyUsedPercent':39},'quota_prepublication':{'ordinaryUsageAllowed':True,'primaryUsedPercent':32,'weeklyUsedPercent':42},'reset_or_overflow_used':False,'runtime_marker':read('runtime_root/runtime_marker.json'),'versions':b['versions'],'git_version':'2.43.0','write_terrain':str(R.relative_to(root)),'source_identity':'29 exact staged Git files, 5 required accepted owner pins and transitive import closure, imported physical paths independently hashed','current_permission_projection_source':'Exact accepted empirical authority, canonical objects, query/predicate/eval source at pinned candidate tree; all actual imported hashes retained. No alternate policy/projection installed. Fixture ALLOW does not establish external trust.','canonical_or_production_owner_edits':False,'original_survey_access':False,'subagents_used':False,'sourcefree_only':True,'publication':'Final commit identity and direct remote readback reported by final response; cannot embed self-referential final SHA inside its own commit.'}
put('04_REVIEWER_PASSPORT.json',passport)
# Complete exact source dispositions remain readable without runtime staging.
put('observations/frontier_comparison.json',{'oracle':oracle['operations'],'runtime_frontier':b['frontier'],'equal':sorted(oracle['operations'],key=lambda x:x['op_id'])==b['frontier'],'expected_counts':oracle['expected_counts'],'candidate_original_count_object':ex['ledger']['declared']})
print('ADJUDICATED_29_AUTHOR_44_INDEPENDENT_15_CLOSURES_29_SOURCE_HASHES')
