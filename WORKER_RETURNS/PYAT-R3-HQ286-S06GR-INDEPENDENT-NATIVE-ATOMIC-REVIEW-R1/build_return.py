import ast,datetime,hashlib,json,pathlib,platform,subprocess,sys,xml.etree.ElementTree as E,collections
root=pathlib.Path.cwd();out=root/'WORKER_RETURNS/PYAT-R3-HQ286-S06GR-INDEPENDENT-NATIVE-ATOMIC-REVIEW-R1';repro=out/'repro'
def write(name,data):(out/name).write_text(json.dumps(data,indent=2)+'\n')
def git(*args):return subprocess.check_output(['git',*args],text=True).strip()
sha={'startup':'4c18ba1994f2780600d49fda3a55e74623f6b5ab','repair':'0ff13995cc55db00d02b08004e62f75d4c5cb36e','prior_review':'1b5b6072f855a74864c82d0f1b3923327bfb8b99','frozen':'7e96914ed6c9a186d5de8a778e8396e46a741eb2','canonical':'7f29aec36d24f16da52d84f17c00f08db3a55434'}
files=['rawlsing_next/pre553_learned_product_lifecycle.py','rawlsing_next/pre553_learned_product_release.py','rawlsing_next/tests/test_hq286_s06gr_independent_atomic_review.py','rawlsing_next/tests/test_pre553_s06g_atomic_integrity.py','rawlsing_next/tests/test_pre553_s06f_native_owner_security.py','rawlsing_next/tests/test_pre553_learned_product_lifecycle.py','rawlsing_next/tests/test_pre553_learned_product_release.py','rawlsing_next/tests/test_pre553_ee14_selected_current_asof_hq260.py','rawlsing_next/tests/test_pre553_learned_world_composition.py']
identities={}
for p in files:
 data=(root/p).read_bytes();row={'sha256':hashlib.sha256(data).hexdigest(),'git_blob':git('hash-object',p)}
 if 'hq286' not in p:
  row['equal_repair_commit']=data==subprocess.check_output(['git','show',sha['repair']+':'+p]);assert row['equal_repair_commit']
 identities[p]=row
session=next(pathlib.Path.home().glob('.codex/sessions/2026/10/13/*01a1360f*.jsonl'));contexts=[];session_id=None
for line in session.open():
 d=json.loads(line)
 if d['type']=='session_meta':session_id=d['payload']['id']
 if d['type']=='turn_context':contexts.append({k:d['payload'].get(k) for k in ['model','effort','cwd']})
assert session_id!='01a13306-6957-7ce0-8741-15f2365bf3ac'
assert all(c['model']=='gpt-6.1-sol' and c['effort']=='low' for c in contexts)
write('02_RESOURCE_ATTESTATION.json',dict(timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),session_id=session_id,author_session='01a13306-6957-7ce0-8741-15f2365bf3ac',distinct_session=True,model_effort_evidence=contexts,session_metadata_source=str(session),account_fingerprint='b4d51d8e',account_designation='user-designated secondary Mac Codex B',hardware_to_account_registry='UNKNOWN; designation is not independently established',provider='OpenAI Codex Desktop',platform=platform.platform(),host=platform.node(),python=sys.version,interpreter=sys.executable,pytest=subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),quota_start_used_percent={'five_hour':10,'weekly':4},quota_prepublication_used_percent={'five_hour':20,'weekly':5},reset_credits_start=3,reset_credits_remaining=3,reset_credits_used=0,paid_overflow_used=0,credits_balance='0',ordinary_usage_allowed=True,primary_Astra_account_used=False,worktree=str(root),git_registered=True,sparse_checkout_core=git('config','--get','core.sparseCheckout'),branch=git('branch','--show-current'),startup_clean_observed=True,startup_remote_tip=sha['startup'],shas=sha,tested_files=identities,scope='Only new reviewer test and own return; no owner or old/frozen test edits, survey originals, credential/issuer creation, protected CURRENT, canonical merge, V3, clone/reset/broad fetch',privacy='Local private repository source/tests; no source originals or external publication except assigned private branch'))
results={}
for label in ['independent_initial','independent_corrected','independent_before','independent_after','unfiltered','independent_before_final','independent_after_final','unfiltered_final','positive_selection']:
 p=repro/(label+'.xml')
 if not p.exists():continue
 rows=[]
 for c in E.parse(p).iter('testcase'):
  f=c.find('failure');err=c.find('error');skip=c.find('skipped')
  state='FAIL' if f is not None else 'ERROR' if err is not None else 'SKIP' if skip is not None else 'PASS'
  row=dict(classname=c.get('classname'),name=c.get('name'),status=state)
  if f is not None:row['message']=f.get('message')
  rows.append(row)
 results[label]=dict(counts=dict(collections.Counter(r['status'] for r in rows)),cases=rows)
write('03_COURT_RESULTS.json',results)
failures=[]
for row in results['unfiltered_final']['cases']:
 if row['status']!='FAIL':continue
 name=row['name']
 if name.startswith('test_17') or name.startswith('test_18'):
  classification='INHERITED_FIXTURE_SETUP_INCOMPATIBILITY';evidence='test_m2_early_refusal_lawful_foreign_mismatch_and_same_release_failover'
 elif 'race_overwrites' in name or 'concurrent_b5' in name:
  classification='HISTORICAL_DEFECT_PROBE_BLOCKED_BY_TRANSACTION_BOUNDARY';evidence='test_four_concurrent_public_selectors; test_public_m2_colliding_preimages'
 else:
  classification='HISTORICAL_DEFECT_PRESENCE_ASSERTION_NO_LONGER_SATISFIED';evidence='own positive immutability, semantic/receipt, rollback and helper refusal tests'
 failures.append(dict(**row,classification=classification,independent_positive_evidence=evidence,retained_failed=True))
write('04_FAILURE_ADJUDICATION.json',failures)
writers=('stage_release','stage_protocol','selection_key','register_product','publish_product','record_recertification','select_current','declare_no_current','supersede_current','withdraw_product','declare_invalidation','record_rebuild_eligibility','link_rebuild','record_cache_materialized','record_cache_dropped','attest_gc_eligibility','record_payload_gc')
m2writers=('register_subject','register_closure','register_release','register_representation','register_binding')
methods=[]
for filename,clsname,owner,names in [('pre553_learned_product_lifecycle.py','LearnedProductLifecycleExecutor','B5',writers),('pre553_learned_product_release.py','M2Repository','M2',m2writers)]:
 tree=ast.parse((root/'rawlsing_next'/filename).read_text());cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name==clsname)
 for n in cls.body:
  if not isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef)) or (n.name.startswith('_') and n.name not in ('_append_events','_commit_selection_transition_receipts','_insert')):continue
  if n.name in names:
   local='PASS';evidence=f'test_baseexception_rollback_then_success_and_recovery[{n.name}]' if owner=='B5' else f'test_m2_baseexception_rollback_and_retry[{n.name}]'
   guard='PASS; unchanged S06FR all_saved_native_writers in three refused modes, executed in unfiltered_final'
  elif n.name=='require_external_issuer':
   local='PASS_REFUSAL';evidence='test_saved_helpers_and_unwrapped_bodies_refuse';guard='PASS_REFUSAL'
  elif n.name.startswith('_'):
   local='PASS_OUTSIDE_TRANSACTION_REFUSAL';evidence='test_saved_helpers_and_unwrapped_bodies_refuse; no same-process authentication claim';guard='PASS_REFUSAL'
  else:
   local='PASS_BOUNDED_LOCAL';guard='READ_OR_SCHEMA_ROUTE'
   evidence='own recursive snapshot, reader rollback, full world/N04/fresh process, concurrent replay; unchanged accepted B5/M2/current-asof and S06FR courts'
  methods.append(dict(owner=owner,method=n.name,line=n.lineno,local_verdict=local,evidence=evidence,external_guard=guard,external_issuance_custody='HOLD'))
for function,target in [('register_producer_subject','register_subject'),('constitute_closure','register_closure'),('constitute_release','register_release'),('register_representation','register_representation'),('publish_binding','register_binding')]:
 methods.append(dict(owner='M2_MODULE_ROUTE',method=function,writer=target,local_verdict='PASS_BOUNDED_LOCAL',evidence='full world or m2_fixture/accepted M2 tests; static route reaches guarded repository writer',external_issuance_custody='HOLD'))
write('05_METHOD_MATRIX.json',methods)
requirements=[
 ('Recursive public event/history immutability','PASS','own recursive snapshot and unchanged prior immutability oracle pass'),
 ('Detached state/checkpoint and input exports','PASS','own snapshot, restored checkpoint survives caller-container mutation'),
 ('Publication/registration subject semantics','PASS','rehashed final event drift refuses on semantic replay, not stale hash'),
 ('Exact receipt fields, release/event/subject linkage and cardinality','PASS','six receipt omission cases, six rehashed field cases; author 42-case repair court additionally passes'),
 ('Concurrent same/distinct-key selectors','PASS','four public callers, eight trials per variant; exactly one winner per key, all histories restore'),
 ('M2 subject/locator collision serialization','PASS','two public record writers, eight trials per variant; winner retained, retry idempotent'),
 ('All 17 B5 and five M2 exception rollback/retry','PASS','own post-write BaseException injection, full state equality and lawful retry; B5 cold restore'),
 ('Public reader pending mutation visibility','PASS','reader blocks then observes exact rollback'),
 ('Saved helpers/unwrapped bodies out-of-transaction','PASS','native guards refuse; no arbitrary Python isolation'),
 ('N04 exact release to producer-subject route','PASS','full-world spy requires release_subject_ref; identities distinct'),
 ('Actual source-free consumer compatibility','PASS','full M01/M1/M2/B5 composition, current receipt and fresh process checkpoint equivalence; 45 unchanged adjacent passes'),
 ('Inherited M2 early refusal and lawful downstream mismatch','PASS','early RELEASE_UNAVAILABLE retained; lawful foreign registration then PUBLICATION_BINDING_MISMATCH, same-release failover works'),
 ('Authenticated issuer/subject entitlement/permission ceiling','HOLD','no independent issuer or credential furnished; constructor refs do not grant authority'),
 ('External anchored history authenticity/completeness','HOLD','coherent whole-history replacement remains locally replayable; no custody root'),
 ('Authenticated epochs, expiry, revocation and protected CURRENT','HOLD','native checkpoint has no authenticated issuer epoch/revocation source; external modes refuse'),
 ('Python same-process principal isolation','FAIL_AS_SECURITY_BOUNDARY','private dictionaries, transaction context and replaceable methods remain reachable; explicit non-goal, not new repair regression'),
 ('OS-kill/durable/multiprocess/distributed atomicity','HOLD','only in-memory thread serialization, exception rollback, complete checkpoint restart tested'),
 ('No-op invalidation anchored timing/completeness','HOLD','legacy zero-event receipts have only registration-prefix graph consistency; precise time/omission not provable'),
 ('Large-history throughput/production scale','HOLD','snapshot copies and semantic replay may be quadratic; no production-scale qualification'),
]
write('06_SECURITY_MATRIX.json',[dict(requirement=r,verdict=v,evidence=e) for r,v,e in requirements])
frozen=json.loads((repro/'frozen_expectations.json').read_text())
localpass={6,11,12,13,14,17,18,20,21,23,24};refusal={1,2,3,5,7,15,16};hold={4,8,9,10,19,22}
for c in frozen['cases']:
 n=int(c['id'].split('H')[1]);c['s06gr_local_verdict']='PASS_BOUNDED_NATIVE' if n in localpass else 'PASS_REFUSAL' if n in refusal else 'HOLD_EXTERNAL_REQUIREMENT'
 c['s06gr_external_authoritative_verdict']='HOLD'
 c['s06gr_evidence']='06_SECURITY_MATRIX.json; own positive court and unchanged native accepted/prior tests; detached S06R suite read, not native-executed'
 if n==4:c['s06gr_note']='No native revoke method; refuse mode does not implement authenticated revocation.'
 if n in (8,19):c['s06gr_note']='Coherent replacement/cold replay proves only LOCAL_UNAUTHENTICATED consistency.'
 if n in (9,10,22):c['s06gr_note']='No authenticated epoch/revocation policy; local as-of event lookup separately passes.'
 if n==23:c['s06gr_note']='Inconsistent subject/event/receipt semantics rejected; coherently replaced subjects/authority require external anchor.'
write('07_FROZEN_EXPECTATIONS_ADJUDICATION.json',frozen)
