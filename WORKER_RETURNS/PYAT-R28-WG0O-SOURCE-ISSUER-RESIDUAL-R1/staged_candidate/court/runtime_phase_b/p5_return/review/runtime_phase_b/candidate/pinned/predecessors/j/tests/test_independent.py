"""Independent expectation-first court. Failures are retained acceptance failures."""
from common import *
import copy,pytest
from collections import Counter
from rawlsing_next.pre553_empirical_query import execute_empirical_query
from rawlsing_next.pre553_batch_runner import BatchUnitSpec,BatchExecutionRunner,ExecutorBinding

OP='OP-WG0P-ORD-01-MARGINAL'
@pytest.fixture(scope='module')
def baseline():
 p=plan();r,rs,e=execute(p);return p,r,rs,e

def test_exact_frozen_25_operations(baseline):
 expected=sorted(O['operations'],key=lambda x:x['op_id'])
 p=baseline[0]
 assert list(p.frontier_receipts)==expected
 b=builder();b.freeze()
 actual=[dict(op_id=o.op_id,op_class=o.op_class,target=o.target,conditioners=list(o.conditioners),item_ids=list(o.item_ids),disposition=o.disposition.value,disposition_reason=o.disposition_reason) for o in b.enumerate()]
 assert sorted(actual,key=lambda x:x['op_id'])==expected

def test_actual_owners_and_source_record_numerics():
 d=json.loads((R/'observations/baseline.json').read_text())
 assert d['one_repository'] and len(d['releases'])==3
 for path,pin in O['pinned_owner_blobs'].items():
  assert next(i for i in d['imports'] if i['module']==path[:-3].replace('/','.'))['git_blob_sha1']==pin
 assert Counter(c['function'] for c in d['owner_calls'])=={'ingest_c11_source_release':3,'_commit_validated':3,'execute_empirical_query':3,'run':1}
 # Counts reconstructed from the actual sealed C11 event and routing records.
 totals={}
 for release in d['releases']:
  assert release['class']=='C11LogicalRelease'
  ev=[r['payload']['semantic_fields'] for r in release['records'] if r['type']=='RespondentEvent']
  counts=Counter(x['raw_response_value'] for x in ev if x['native_question_ref']['object_id'].endswith('Q-ORD-A'))
  totals[release['tag']]=dict(counts)
 assert totals['REL-A-W1']=={'0':1,'1':2,'2':2,'3':1}
 assert totals['REL-A-W2']=={'1':2,'2':1,'3':1}
 assert d['summary']['populated_data_execution_claim'] is False
 assert all(r['state']=='COMPLETED' for r in d['receipts'])
 assert {r['result_refs'][0]['content_hash'] for r in d['receipts']}=={q['facts'][0]['ref']['content_hash'] for q in d['owner_query_returns']}

def test_independent_mr_profiles_and_indicator_totals(baseline):
 e=baseline[3]['OP-WG0P-HH-MR-02-MARGINAL'][0]
 profiles={tuple(c['cell']):c['n'] for c in e['cells'] if c['n']}
 assert profiles=={('yes','yes','no','no','no'):1,('no','yes','yes','no','no'):1,('yes','no','yes','yes','no'):1,('no','no','no','no','yes'):1}
 totals={name:sum(n for profile,n in profiles.items() if profile[ix]=='yes') for ix,name in enumerate(('food','rent','health','education','none'))}
 assert totals==O['expected_native']['MR_indicator_totals'] and e['denominator']==4

def test_native_options_must_affect_computation_or_hold(baseline):
 items=w.independent_oracle_items();items[0]=replace(items[0],options=('changed','meaning'))
 p=plan(items);_,rs,e=execute(p)
 assert OP not in e or values(e)[OP]!=values(baseline[3])[OP], 'Changed options rotate identity but unchanged 0/1/2/3/9 cells still COMPUTED'

@pytest.mark.parametrize('field,value',[('wave','W99'),('unit','household'),('source_id','FOREIGN'),('form_id','Q-FOREIGN'),('response_kind','MULTIPLE_RESPONSE')])
def test_native_metadata_must_bind_release_or_hold(field,value,baseline):
 items=w.independent_oracle_items();items[0]=replace(items[0],**{field:value})
 p=plan(items);_,rs,e=execute(p)
 assert OP not in e or values(e)[OP]!=values(baseline[3])[OP], f'{field} mutation silently computes original hardcoded source'

@pytest.mark.parametrize('field,value',[('conditioners',('WG0P-ORD-05',)),('op_class','CONDITIONAL'),('disposition_reason','UNPROVED')])
def test_same_operation_id_changed_semantics_rejected(field,value):
 ops=builder().enumerate();o=next(o for o in ops if o.op_id==OP)
 with pytest.raises((ValueError,KeyError,RuntimeError)):
  plan(ops=[o,replace(o,**{field:value})])

@pytest.mark.parametrize('status',['HELD','INADMISSIBLE'])
def test_missing_nonproduced_operation_rejected(status):
 ops=builder().enumerate();removed=next(o for o in ops if o.disposition.value==status)
 with pytest.raises((ValueError,KeyError,RuntimeError)):
  p=plan(ops=[o for o in ops if o.op_id!=removed.op_id]);execute(p)

def test_same_key_altered_target_must_not_execute_original_source():
 ops=builder().enumerate();ops=[replace(o,target='WG0P-ORD-05',item_ids=('WG0P-ORD-05',)) if o.op_id==OP else o for o in ops]
 with pytest.raises((ValueError,KeyError,RuntimeError)):
  p=plan(ops=ops);r,rs,e=execute(p)
  if OP not in e: raise ValueError('typed non-execution')

def test_unknown_operation_has_no_fallback(baseline):
 p=baseline[0];u=p.manifest.units[0]
 with pytest.raises(KeyError): w.make_executor(p)(replace(u,job_ref=w._ref('EmpiricalQuerySpec@1.0.0','UNKNOWN')))

@pytest.mark.parametrize('grant',['UNKNOWN','WITHDRAWN','','forged-license'])
def test_unknown_withdrawn_grants_hold(grant):
 items=w.independent_oracle_items();items[0]=replace(items[0],grant=grant)
 p=plan(items);_,_,e=execute(p)
 assert OP not in e and next(r for r in p.frontier_receipts if r['op_id']==OP)['disposition']=='HELD'

def test_late_revocation_blocks_current_read():
 p=plan();_,rs,e=execute(p);p.source_issuer_grant['grant']='WITHDRAWN'
 with pytest.raises((PermissionError,ValueError,KeyError)):
  after=w.consumer_effects(p,rs)
  if OP not in after: raise PermissionError('typed revocation')

def test_fact_payload_is_bound_at_read():
 p=plan();_,rs,e=execute(p)
 entry=e[OP][0];entry['denominator']=999;entry['cells'][0]['n']=999
 with pytest.raises((ValueError,KeyError,RuntimeError)):
  after=w.consumer_effects(p,rs)
  assert after[OP][0]['denominator']!=999, 'Same exact result ref reads caller-mutated 999 support'

def test_wrong_release_bound_to_unit_is_rejected():
 p=plan();p.op_specs[OP].release_tag='REL-A-W2';p.op_specs[OP].risk_name='R_ORD2';p.op_specs[OP].member_ids=('R11','R12','R13','R14')
 r,rs,e=execute(p)
 assert OP not in e, 'COMPLETED unit pinned A-W1 computed A-W2 denominator 4'

def test_inconsistent_mr_native_sets_rejected(monkeypatch):
 c=copy.deepcopy(w.COHORTS['REL-A-W1']);c['native_option_sets']['H1']=('none',)
 monkeypatch.setitem(w.COHORTS,'REL-A-W1',c)
 with pytest.raises((ValueError,KeyError,RuntimeError)): execute(plan())

@pytest.mark.parametrize('value',[None,'-1','foreign'])
def test_invalid_native_response_rejected(value,monkeypatch):
 c=copy.deepcopy(w.COHORTS['REL-A-W1']);c['rows'][0]['responses']['Q-ORD-A']=value
 monkeypatch.setitem(w.COHORTS,'REL-A-W1',c)
 with pytest.raises((ValueError,KeyError,RuntimeError)): plan()

def test_missing_special_9_not_substantive(monkeypatch):
 c=copy.deepcopy(w.COHORTS['REL-A-W1']);c['rows'][0]['responses']['Q-ORD-A']='9'
 monkeypatch.setitem(w.COHORTS,'REL-A-W1',c)
 p=plan();_,_,e=execute(p)
 assert next(c for c in e[OP][0]['cells'] if c['cell']=='9')['n']==0, 'Declared missing 9 ingested and counted SUBSTANTIVE_RESPONSE'

def test_zero_risk_and_positive_conditional_actual_i03(baseline):
 rel=baseline[0].releases['REL-A-W1']
 pred=w._branch_predicate_for(rel,(),tag='wg0j-empty',risk_name='R_ORD')
 q=w._query_for(rel,pred,(('Q-ORD-A',('0','1','2','3','9')),),risk='R_ORD',tag='wg0j-empty')
 result=execute_empirical_query(repository=rel.repo,query=q,predicate=pred,authority_registry=w._registry_for(rel),release_refs=(rel.release_ref,))
 assert result.facts[0].typed_state=='ZERO_SUPPORT' and result.facts[0].raw_denominator_support==0
 pred=w._response_predicate_for(rel,'Q-ORD-A','1',risk_name='R_JOINT_ORD_RT',tag='wg0j-joint')
 q=w._query_for(rel,pred,(('Q-RT-C',('yes','no')),),risk='R_JOINT_ORD_RT',tag='wg0j-joint')
 result=execute_empirical_query(repository=rel.repo,query=q,predicate=pred,authority_registry=w._registry_for(rel),release_refs=(rel.release_ref,))
 assert result.facts[0].raw_denominator_support==2
 assert {c['cell']:c['raw_numerator_support'] for c in result.facts[0].target_topology['complete_cell_semantic_projection']}=={'yes':1,'no':1}

def test_absent_joint_split_ballot_holds():
 a=w.independent_oracle_items()[0];b=replace(a,item_id='SPLIT',form_id='SPLIT-FORM')
 ops=builder([a,b]).enumerate()
 assert len(ops)==4 and all(o.disposition!=w.Disposition.PRODUCED for o in ops if o.op_class=='CONDITIONAL')

def test_source_bytes_mutation_changes_source_artifact_identity(baseline,monkeypatch):
 c=copy.deepcopy(w.COHORTS['REL-A-W1']);c['rows'][0]['responses']['Q-ORD-A']='3'
 monkeypatch.setitem(w.COHORTS,'REL-A-W1',c)
 p=plan();_,_,after=execute(p)
 old=baseline[0].repository.resolve_release_exact(baseline[0].releases['REL-A-W1'].release_ref)
 new=p.repository.resolve_release_exact(p.releases['REL-A-W1'].release_ref)
 assert values(after)[OP]!=values(baseline[3])[OP]
 assert values(after)['OP-WG0P-ORD-05-MARGINAL']==values(baseline[3])['OP-WG0P-ORD-05-MARGINAL']
 assert p.releases['REL-A-W2'].release_ref==baseline[0].releases['REL-A-W2'].release_ref
 assert new.source_artifact_ref!=old.source_artifact_ref, 'Changed source bytes retain identical source artifact hash'

def test_unavailable_unit_release_ref_rejected(baseline):
 p=baseline[0];unit=replace(p.manifest.units[0],release_refs=(w._ref('C11LogicalRelease','FOREIGN'),))
 with pytest.raises(ValueError): BatchExecutionRunner(manifest=w.BatchManifest((unit,)),repository=p.repository)

@pytest.mark.parametrize('field,value',[('options',('changed',)),('missing_codes',('9','999')),('grant','WITHDRAWN'),('route_evidence','new-route'),('version','v2')])
def test_freeze_binds_native_fields(field,value):
 items=w.independent_oracle_items();before=builder(items).freeze()
 items[0]=replace(items[0],**{field:value})
 assert builder(items).freeze()!=before

def test_conflicting_carrier_and_changed_target_duplicate_refused():
 a=w.independent_oracle_items()[0];b=builder([a])
 assert b.add_item(replace(a,item_id='OTHER',unit='household'))=='CONFLICTING_NATIVE_ITEM_IDENTITY'
 o=next(o for o in builder().enumerate() if o.op_id==OP)
 with pytest.raises((ValueError,KeyError)):
  plan(ops=[o,replace(o,target='OTHER',item_ids=('OTHER',))])

def test_positive_conditional_through_independent_qualified_manifest(baseline):
 rel=baseline[0].releases['REL-A-W1']
 pred=w._response_predicate_for(rel,'Q-ORD-A','1',risk_name='R_JOINT_ORD_RT',tag='wg0j-batch-joint')
 query=w._query_for(rel,pred,(('Q-RT-C',('yes','no')),),risk='R_JOINT_ORD_RT',tag='wg0j-batch-joint')
 unit=BatchUnitSpec(job_kind='QUERY',job_ref=query.ref,release_refs=(rel.release_ref,),semantic_input_refs=(pred.ref,query.ref))
 actual=[]
 def executor(u):
  assert u==unit
  result=execute_empirical_query(repository=rel.repo,query=query,predicate=pred,authority_registry=w._registry_for(rel),release_refs=u.release_refs)
  actual.extend(result.facts)
  return w.ExecutionOutcome(result_refs=tuple(f.ref for f in result.facts),provenance_refs=(query.ref,pred.ref))
 runner=BatchExecutionRunner(manifest=w.BatchManifest((unit,)),repository=rel.repo)
 receipts=runner.run(executors={'QUERY':ExecutorBinding(w._ref('EXECUTOR','wg0j-qualified-conditional'),executor)})
 assert receipts[0].state=='COMPLETED' and receipts[0].result_refs==(actual[0].ref,)
 assert actual[0].raw_denominator_support==2
 assert {c['cell']:c['raw_numerator_support'] for c in actual[0].target_topology['complete_cell_semantic_projection']}=={'yes':1,'no':1}
 dump('positive_conditional_batch.json',{'qualification':'SOURCEFREE_OWNER_MECHANISM_ONLY; independent manifest, not frozen25 or candidate builder product path','unit':unit.semantic_projection(),'query':query.semantic_projection(),'predicate':pred.semantic_projection(),'receipt':receipts[0].projection(),'fact':actual[0].semantic_projection(),'summary':asdict(runner.summary())})

def test_frozen_product_path_has_no_positive_conditionals(baseline):
 p=baseline[0]
 assert sum(r['op_class']=='CONDITIONAL' and r['disposition']=='PRODUCED' for r in p.frontier_receipts)==0
 assert all('GIVEN' not in u.job_ref.object_id for u in p.manifest.units)

def test_typed_owner_authority_deny_fails_closed(baseline):
 rel=baseline[0].releases['REL-A-W1']
 fields=dict(rel.qauth.semantic_fields);fields['decision_state']='DENY'
 denied=w.AuthoritySnapshot(typed_state='DENY',authority_snapshot_refs=(),dependency_refs=(),producer_replay_locator_or_reference_root=w._ref('REPLAY_ROOT','wg0j-deny'),**fields)
 bad=replace(rel,qauth=denied)
 pred=w._branch_predicate_for(bad,('R1',),tag='deny',risk_name='R_ORD')
 query=w._query_for(bad,pred,(('Q-ORD-A',('0','1','2','3','9')),),risk='R_ORD',tag='deny')
 result=execute_empirical_query(repository=bad.repo,query=query,predicate=pred,authority_registry=w._registry_for(bad),release_refs=(bad.release_ref,))
 dump('denied_authority.json',{'states':[f.typed_state for f in result.facts]})
 assert all(f.typed_state!='SUPPORTED' for f in result.facts)

def test_cold_replay_and_shard_values():
 d=json.loads((R/'observations/cold_comparison.json').read_text())
 assert d['cold_identical_receipts'] and d['cold_identical_values'] and d['cold_frontier25']
 assert d['shard_combined_unit_keys_match_full'] and d['shard_values_match_full']
 assert d['processes']['checkpoint']['exit']==23

def test_cold_resume_restores_published_fact_custody():
 d=json.loads((R/'observations/cold_comparison.json').read_text())
 assert d['resume']['summary']['coverage_state']=='FULL_MANIFEST_COVERAGE'
 assert 'consumer_error' not in d['resume'], 'Completed checkpoint skips old unit but its result payload is lost in fresh process'

def test_wave2_source_universe_has_correct_wave(baseline):
 for tag in ('REL-A-W2','REL-B-W2'):
  rel=baseline[0].releases[tag]
  universe=rel.repo.resolve_object_exact(rel.universe_ref)
  assert universe.raw_wave=='W2', 'Source universe hardcodes raw_wave W1 for W2 fixture'
