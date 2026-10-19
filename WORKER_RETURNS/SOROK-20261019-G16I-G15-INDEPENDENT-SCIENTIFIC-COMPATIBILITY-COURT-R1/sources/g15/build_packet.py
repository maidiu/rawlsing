"""Package actual value witnesses, permission holds and exact terminal delta."""
from pathlib import Path
import datetime,hashlib,json,platform,re,subprocess,sys
from court_runner import ROOT,REPO,dump

def read(p):return json.loads((ROOT/p).read_text())

def main():
 result=read('execution/joined_positive.json')['result'];record=result['causal_replay_record']
 assert result['terminal']['status']=='COMMITTED'
 assert read('execution/joined_cold_replay.json')['complete_causal_record_equal'] is True
 assert read('execution/prospective/results.json')[0]['counts']=={'PASS':75,'RED':0,'ERROR':0,'SKIP':0}
 rows=[]
 for phase,events in [('maternal',result['anchor']['history_events']),('second_adult',result['dad_events'])]:
  sys.path.insert(0,str(ROOT/'candidate'))
  from lab_sgi1.history import replay_history
  for w in replay_history(events)['value_witnesses']:
   rows.append(dict(phase=phase,consumer_event_id=w['event_id'],consumer_kind=w['kind'],owner_id=w['owner_id'],clock=w['effective_index'],values_read=w['readset'],effect=w['effect']))
 witness=result['relation']['objective_relation']['witness']
 for a in witness['actions']:
  rows.append(dict(phase='joint_action',consumer_event_id=a['event_id'],consumer_kind=a['kind'],owner_id=a['owner_id'],clock=a['effective_index'],values_read=a['values_read']+[dict(event_id=witness['material']['event_id'],value=witness['material'])],before=a['before'],after=a['after']))
 for e in result['continuation']['continuation_events']:
  rows.append(dict(phase='adult_continuation',consumer_event_id=e['event_id'],consumer_kind=e['kind'],owner_id=e['actor'],clock=e['effective_index'],values_read=e['payload']['values_read'],before=e['payload']['before'],after=e['payload']['after']))
 later=result['continuation']['research_relation_continuation']
 for a in later['actions']:
  rows.append(dict(phase='later_contact',consumer_event_id=a['event_id'],consumer_kind=a['kind'],owner_id=a['owner_id'],clock=a['effective_index'],source_refs=a['causal_parent_event_ids'],material_read=later['material_source'],before=a['before'],after=a['after']))
 dump(ROOT/'09_DEPENDENCY_READSETS.json',dict(causal_replay_hash=result['causal_replay_hash'],selected_contract=result['scenario']['endpoint_constraints'],full_event_closure=result['dag_validation']['complete_event_closure'],source_to_actual_consumer=rows,science_grade='BOUNDED_SOURCEFREE_TRANSITION_EXPERIMENT_NOT_NATIVE_OWNER_SEMANTICS'))
 holds=[
  ('ADP007','V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE','No native actor initialization or domain-initial-fact grant; research roots are not ADP007 actors'),
  ('ADP010','V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE','No native OEE active-actor, opportunity, encounter or child-exposure grants'),
  ('ADP015','V3_ACTOR_DEVELOPMENTAL_CAUSALITY_ENGINE','No adoption of retrospective construction/selection, task relationship, household, parenthood or generation rules'),
  ('ADP019','V3 External Admission Court','Research observer is not a competent native producer/event-kind issuer'),
  ('ADP020','Competent semantic rule/stream and RNG registry owners','Algorithm reference evidence does not issue genealogy scope, semantic stream, candidate, weight or stochastic-operation grants'),
  ('CAN008_CAN011','Competent concrete actor-response and durable mediator/practice owners','No native response, practice or target-person grant'),
  ('ADP016_ADP017','Native memory/access owners','Numeric research experience/psyche is not native causal memory or actor knowledge'),
  ('BIOLOGY','Competent biological/occurrence owners','No conception, gestation, birth or biological parent generation'),
  ('CHILD_ACTOR','Competent generation and initialization owners','No focal child actor, child exposure, uptake or personality'),
  ('POPULATION','Original source/design/calibration owners','No observed population prior, likelihood, pairing model, reversed query, calibrated posterior or source sampling'),
  ('PRODUCTION_N12_WELD','Competent HQ and independent Pyat source/world/wake owners','No installation, PRE-MAIN/current mutation, adoption, N12 or physical weld')]
 grid=[
  dict(node='C4',before='G13 sourcefree causal defects independently falsified',after='One joined value-consuming historical research candidate, 67 unchanged G14 assertions and 75 prospective assertions executed; 73 inherited literal REDs remain',status='SOURCEFREE_CANDIDATE_ONLY_NOT_ADOPTED',native_delta='NONE'),
  dict(node='C9',before='No competent native person response/practice/actor positive established',after='Research source/consumer contract and same-assertion witnesses supplied; native positive still absent',status='OWNER_HELD_NOT_GRANTED',requirements=['CAN008 concrete issuer','CAN011 target grant','ADP007 active actor','ADP010/019 encounter and event witnesses','ADP015/020 exact construction/selection decisions','positive native registry']),
  dict(node='C10_C11',before='Separate transport, owner and Pyat N11/N12/weld prerequisites',after='No transport, Pyat or physical-weld authority changed',status='SEPARATE_OWNER_HELD'),
  dict(node='C12',before='No actual pipeline-produced native person',after='No actual pipeline-produced native person; no child or biological event created',status='NOT_GRANTED_NOT_PRODUCED')]
 dump(ROOT/'10_PERMISSION_HOLDS_AND_TERMINAL_DELTA.json',dict(role='G15_SOURCEFREE_IMPLEMENTATION_AUTHOR_NOT_HQ_OR_ISSUER',permissions=[dict(authority=a,competent_owner=o,status='NOT_GRANTED',reason=r) for a,o,r in holds],terminal_acceptance_grid=grid,A0_A5=dict(status='NOT_ESTABLISHED',native_person=False,live_engine=False,reentry=False,independent_native_life=False,generalization=False,alpha=False),parallel_lanes=dict(C0R3='INDEPENDENT_NOT_A_PREREQUISITE_NOT_LAUNCHED_BY_THIS_WORKER',C9PI='INDEPENDENT_NOT_A_PREREQUISITE_NOT_LAUNCHED_BY_THIS_WORKER',Pyat='EXTERNALLY_OWNED_NOT_COMMISSIONED'),child_generated_events=0,child_exposures=[],sourcefree_grade='AUTHOR_CANDIDATE_FOR_HQ_INTAKE_NOT_SELF_ADOPTED'))
 # Full literal failures retain technical/scientific caveats instead of waivers.
 flags=read('05_INHERITED_RED_FLAGS.json')
 for c in flags['cases']:
  name=c['name'];suite=c['suite']
  if suite in {'sgi1_target','g13_postrepair'}:
   cls='LEGACY_FINGERPRINT_OR_PREDICATE_CONTRACT_CHANGED__REVISE';meaning='Read case receipts; nine positive handler groups are NOT_EVALUABLE under earlier refusal outputs. No blanket scientific waiver.'
  elif 'NONFORWARD' in name or 'removed_route' in name:
   cls='OLD_POSITIONAL_FIXTURE_OR_DIAGNOSTIC_CODE_EXPECTATION';meaning='Event positions and typed refusal paths changed; the original exact assertion remains RED.'
  elif 'future_child_outcome_counterfactual' in name:
   cls='DISALLOWED_TAINTED_OUTPUT_SELECTION_POSITIVE';meaning='The marked candidate now holds before any draw; the old test expects a selected/drawn result.'
  elif 'adp020' in name or '32_byte_root' in name:
   cls='NATIVE_ENTITLEMENT_OWNER_HELD';meaning='Reference sampler mechanics do not grant ADP020 entitlement; NOT_GRANTED is explicit.'
  elif 'm0_and_m2' in name:
   cls='FINITE_HISTORY_SEARCH_DOES_NOT_FORCE_SELECTED_INSTITUTION';meaning='Actual independently selected material action need not meet the requested institutional endpoint; search denies without rewriting the person.'
  elif suite=='g12_supplemental' or 'test_f7_' in name:
   cls='SOLO_WORK_OR_PSYCHIC_LABEL_NOT_RELATIONSHIP_AUTHORITY';meaning='A supplied adult and solo commissioned work do not supply two performed joint actions, a separate witness or affectionate perception authority.'
  else:
   cls='REVISE_UNRESOLVED_LITERAL_CONTRACT';meaning='Inspect exact JUnit; this return does not waive or relabel the failed assertion.'
  c.update(classification=cls,scientific_disposition=meaning,waived=False)
 dump(ROOT/'05_INHERITED_RED_FLAGS.json',flags)
 p=ROOT/'environment_passport_delta.json';passport=read('environment_passport_delta.json')
 passport.update(status='LIVE_VERIFIED',last_live_probe_at=datetime.datetime.now(datetime.timezone.utc).isoformat(),surface='LOCAL_SHARED_STORE',machine_alias='LOCAL_RUNNER_A',git_object_store_alias='EXISTING_SHARED_RAWLSING_STORE',worktree_alias='G15_ASSIGNED',conversation_or_account_affinity='CURRENT_SESSION_ONLY',source_family='SOURCEFREE_GENEALOGY',filesystem_shell='VERIFIED',dependencies={'python':sys.version.split()[0],'pytest':subprocess.check_output([sys.executable,'-m','pytest','--version'],text=True).strip(),'git':subprocess.check_output(['git','--version'],text=True).strip(),'node':'NOT_NEEDED_NOT_PROBED','third_party_runtime_libraries':'pytest only; candidate runtime stdlib'},covered_test_suites={'baseline':'execution/baseline/results.json','candidate':'execution/candidate/results.json','prospective':'execution/prospective/results.json','faults':'execution/faults/receipts.json','historical':'execution/preservation/results.json'},materialized_source_refs='custody/source_and_import_graph.json',assignments_completed=['G15 coherent candidate, author proof and custody packet'],next_good_affinity_tags=['GENEALOGY','TEMPORAL','CAUSAL_REPLAY'],staged_state_preservation='RUNNABLE_FROZEN_PACKET_AND_IGNORED_LOCAL_RUNS',model_provider='CURRENT_USER_SELECTED_CODEX_SESSION_UNCHANGED',model_exact='NOT_INTROSPECTED',reasoning_effort='NOT_CHANGED',quota_snapshot={'source':'Codex get_usage_limits read-only tool','account_wide_not_attributed_to_this_commission':True,'primary':{'used_percent':41,'remaining_percent':59,'window_minutes':300,'resets_at_unix':1792440723},'secondary':{'used_percent':72,'remaining_percent':28,'window_minutes':10080,'resets_at_unix':1792879715},'ordinary_usage_allowed':True,'spend_control_reached':False,'credit_balance':'0','available_reset_count':3,'reset_credits_consumed':0},cash_attribution=None,new_provider_calls=0,new_provider_tokens=0,historical_tokens_not_new=12183,other_machine_account_slots='UNKNOWN')
 # Never persist account IDs, credit identifiers, personal homes or credentials.
 p.write_text(json.dumps(passport,indent=2,sort_keys=True)+'\n')
 startup='278c789d4d1cf844b7fb614ae673288ff1dc9ce2'
 paths=subprocess.check_output(['git','diff','--name-only',startup+'^',startup],cwd=REPO,text=True).splitlines()
 dump(ROOT/'custody/startup.json',dict(startup=startup,parent=subprocess.check_output(['git','rev-parse',startup+'^'],cwd=REPO,text=True).strip(),commission_only_paths=paths,remote_startup_verified='278c789d4d1cf844b7fb614ae673288ff1dc9ce2',allowed_write_terrain=str(ROOT.relative_to(REPO)),one_accountable_worker=True,no_helpers=True,no_reviewer_commissioned=True))
 # Execution metadata is portable. Frozen original preimages are never edited.
 for p in (ROOT/'execution').rglob('*'):
  if p.is_file() and p.suffix in {'.xml','.txt','.json'}:
   s=p.read_text().replace(str(REPO),'$WORKTREE')
   if p.suffix=='.xml':s=re.sub(r'hostname="[^"]*"','hostname="local-runner"',s)
   p.write_text(s)
 # Every changed path remains inside this commission. Manifest excludes itself
 # and reconstructable runs/runtime markers, avoiding a circular hash.
 paths=[]
 for p in sorted(ROOT.rglob('*')):
  if not p.is_file() or any(x in p.parts for x in ['runs','__pycache__','.pytest_cache']) or p==ROOT/'artifact_manifest.json' or p.name=='.runtime_marker':continue
  paths.append(dict(path=str(p.relative_to(ROOT)),sha256=hashlib.sha256(p.read_bytes()).hexdigest(),bytes=p.stat().st_size))
 dump(ROOT/'artifact_manifest.json',dict(schema='G15_ARTIFACT_MANIFEST_R1',files=paths,source_startup=startup,publication_sha='REPORTED_OUTSIDE_ITS_OWN_COMMIT'))
 print(json.dumps(dict(files=len(paths),candidate_causal_hash=result['causal_replay_hash'],readset_rows=len(rows),native_permissions='NOT_GRANTED')))
if __name__=='__main__':main()
