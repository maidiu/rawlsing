"""RSC0 law-derived hostile review. No candidate expected-class table imported."""
import copy, json, os, sys, types
from contextlib import contextmanager
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
import port.adapter as A
import port.pinned_producer as P
from port.provider_a import ProviderA
from port.provider_b import ProviderB
from port.world_baseline import BASELINE_WORLD, EMPIRICAL, REVERSAL_GRANT_SCOPED
from port.contracts import PortContractError
from port.world_laws import validate_knowledge_clock, context_fingerprint, validate_freshness
from rawlsing_next.tests import n10e_empirical_slice_fixture as FX

RET=Path(os.environ['RSC0_RETURN']); RT=Path(os.environ['RSC0_RUNTIME'])
CP=RT/'WORKER_RETURNS/SOROK-R3-HQ300-C0-SC0-ADAPTER-RED-REPAIR-R1'
CID='NONPARENT_APPRENTICESHIP_ENTRY'
PROVIDERS=[ProviderA,ProviderB]
TARGETS={'N10E':P._N10E.provide_empirical_possibility_slice,
         'C1':P._C1.compose_positioned_subject_possibility,
         'PE':P._PE.serve_generic_world_situated_possibility}
def record(name, **kw):
 out=RET/'repro/hostile_observations';out.mkdir(exist_ok=True)
 (out/(name+'.json')).write_text(json.dumps(kw,indent=2,default=str)+'\n')
@contextmanager
def independent_trace():
 """Code-object identity trace, independent of candidate's sys.setprofile."""
 counts={k:0 for k in TARGETS};returns=[];codes={f.__code__:k for k,f in TARGETS.items()}
 prev=sys.gettrace()
 def trace(frame,event,arg):
  key=codes.get(frame.f_code)
  if key and event=='call': counts[key]+=1
  if key and event=='return': returns.append(dict(module=key,return_type=type(arg).__name__,state=getattr(arg,'provider_state',getattr(arg,'result_state',None))))
  return trace
 sys.settrace(trace)
 try: yield counts,returns
 finally: sys.settrace(prev)

@pytest.mark.parametrize('provider',PROVIDERS)
def test_actual_code_object_calls_and_consumed_support(provider):
 with independent_trace() as (calls,returns): b=A.TwoContractAdapter(provider()).run()
 record('calls_'+provider.__name__,actual_calls=calls,returns=returns,lane=b['empirical_lane'],consumed=b['consumer_effects'][CID]['output']['empirical_access_support'])
 assert calls=={'N10E':1,'C1':2,'PE':1}
 s=b['possibility_receipt']['support'];c=b['consumer_effects'][CID]['output']['empirical_access_support']
 assert (s['target_yes'],s['target_no'],s['denominator'])==(54,6,60)
 assert c['base_ratio']==s['base_ratio']=='54/60' and c['minority_ratio']=='6/60'
 assert b['empirical_lane']['evidence_digest']

@pytest.mark.parametrize('provider',PROVIDERS)
@pytest.mark.parametrize('mode',['absent','revoked'])
def test_world_read_denied_before_producer_or_consumer(provider,mode,monkeypatch):
 w=copy.deepcopy(BASELINE_WORLD);w['permission_ceiling']['use_atoms'].remove('WORLD_READ')
 if mode=='revoked':w['permission_ceiling']['revoked_atoms']=['WORLD_READ']
 p=provider(world=w);reads=[];original=p.read_values
 def read(*a,**kw): reads.append(True);return original(*a,**kw)
 monkeypatch.setattr(p,'read_values',read)
 with independent_trace() as (calls,_), pytest.raises(PortContractError) as e:A.TwoContractAdapter(p).run()
 record('world_deny_'+provider.__name__+'_'+mode,error=e.value.code,calls=calls,value_reads=len(reads))
 assert e.value.code=='DENIED_USE' and not any(calls.values()) and not reads

@pytest.mark.parametrize('provider',PROVIDERS)
@pytest.mark.parametrize('mode',['absent','revoked'])
def test_possibility_query_permission_cannot_be_fabricated(provider,mode):
 w=copy.deepcopy(BASELINE_WORLD);w['permission_ceiling']['use_atoms'].remove('POSSIBILITY_QUERY')
 if mode=='revoked':w['permission_ceiling']['revoked_atoms']=['POSSIBILITY_QUERY']
 with independent_trace() as (calls,_):
  try:b=A.TwoContractAdapter(provider(world=w)).run()
  except PortContractError as e:
   record('query_deny_'+provider.__name__+'_'+mode,error=e.code,calls=calls);assert e.code=='DENIED_USE';return
 record('query_deny_'+provider.__name__+'_'+mode,issuer_and_use=b['world_receipt']['issuer_and_use'],calls=calls,consumer_output=b['consumer_effects'][CID]['output'])
 pytest.fail('POSSIBILITY_QUERY_NOT_AUTHORIZED_BUT_EFFECTIVE_AND_CONSUMED')

@pytest.mark.parametrize('provider',PROVIDERS)
def test_original_2009_2010_lookahead_rejected(provider):
 w=copy.deepcopy(BASELINE_WORLD);w['time_axes']['as_of']='2009'
 with pytest.raises(PortContractError) as e:A.TwoContractAdapter(provider(world=w)).run()
 assert e.value.code=='NO_CURRENT_OR_NOT_KNOWN_ASOF'

@pytest.mark.parametrize('forgery',[
 {'bound_authority_ref':'foreign:any-nonempty-string'},
 {'bound_authority_ref':'fx:issuer:fixture_only','source_ref':'foreign:source','known_at':'2025'},
 {'bound_authority_ref':{'kind':'TEST_ONLY','id':'forged','hash':'0'*64},'known_at':'2026','scope':'foreign:scope'},
])
def test_prior_knowledge_requires_actual_scope_and_chronology(forgery):
 w=copy.deepcopy(BASELINE_WORLD);w['time_axes']['as_of']='2009';w['prior_knowledge_declaration']=forgery
 try:result=validate_knowledge_clock(w)
 except PortContractError as e:assert e.code=='NO_CURRENT_OR_NOT_KNOWN_ASOF';return
 record('prior_forgery_'+str(len(forgery)),declaration=forgery,result=result)
 pytest.fail('PRIOR_KNOWLEDGE_ACCEPTS_NONEMPTY_REF_WITHOUT_DEREFERENCE_OR_DATE')

@pytest.mark.parametrize('provider',PROVIDERS)
def test_declared_prior_knowledge_is_not_silently_dropped(provider):
 w=copy.deepcopy(BASELINE_WORLD);w['time_axes']['as_of']='2009'
 # Fixture-bound candidate declaration; no real authority issuance is asserted.
 d={'bound_authority_ref':w['authority_ref'],'source_ref':w['source_ref'],'source_release_ref':w['source_release_ref'],'scope':w['permission_ceiling']['scope_binding'],'known_at':'2008'}
 w['prior_knowledge_declaration']=d
 assert validate_knowledge_clock(w)['state']=='KNOWLEDGE_ORDERING_OK'
 selected=provider(world=w).resolve_world_selection({'scope':w['permission_ceiling']['scope_binding']})
 record('prior_dropped_'+provider.__name__,submitted=d,selected=selected['world'].get('prior_knowledge_declaration'))
 assert selected['world'].get('prior_knowledge_declaration')==d,'PROVIDER_DROPS_THE_ONLY_PRIOR_KNOWLEDGE_EXCEPTION_CARRIER'

@pytest.mark.parametrize('provider',PROVIDERS)
def test_reverse_fixture_matches_real_reverse_owner_geometry(provider):
 b=A.TwoContractAdapter(provider()).run();p=provider()
 reverse=p.request_role_reversal(b['world_receipt'],b['possibility_receipt'],copy.deepcopy(REVERSAL_GRANT_SCOPED))
 case=FX.build_provider_case('reverse')
 result=P._N10E.provide_empirical_possibility_slice(repository=case['source']['repo'],empirical_query=case['empirical_query'],predicate=case['predicate'],authority_registry=case['registry'],release_refs=case['release_refs'],consumer_query=case['consumer_query'],model_rule=case['model_rule'],condition_binding_witness=case['condition_binding_witness'])
 geometry=result.generated_evidence_or_null.geometry
 record('reverse_real_'+provider.__name__,grant_result=reverse,geometry=geometry)
 assert reverse['reverse_slice']['numerator']==54 and reverse['reverse_slice']['denominator']==geometry['denominator']['raw_denominator_support']==62

@pytest.mark.parametrize('provider',PROVIDERS)
@pytest.mark.parametrize('bad',[{'reverse_numerator':999,'reverse_denominator':0},{'reverse_numerator':54,'reverse_denominator':61},{'reverse_risk_set':'foreign:unissued-risk','reverse_numerator':1,'reverse_denominator':999}])
def test_reverse_claim_not_issued_by_hashing_caller_numbers(provider,bad):
 b=A.TwoContractAdapter(provider()).run();g=copy.deepcopy(REVERSAL_GRANT_SCOPED);g['binds'].update(bad)
 try:result=provider().request_role_reversal(b['world_receipt'],b['possibility_receipt'],g)
 except PortContractError as e:assert e.code=='HELD_AUTHORITY';return
 record('reverse_forgery_'+provider.__name__+'_'+str(bad.get('reverse_denominator')),grant=g,result=result)
 pytest.fail('CALLER_AUTHORED_REVERSE_NUMBERS_LABELLED_INDEPENDENTLY_ISSUED')

@pytest.mark.parametrize('provider',PROVIDERS)
def test_testonly_operational_request_never_promotes_grade(provider):
 demand={'scope':BASELINE_WORLD['permission_ceiling']['scope_binding'],'mode':'OPERATIVE_N10W','requested_use_atoms':['WORLD_READ','POSSIBILITY_QUERY','ACTOR_GENERATION'],'model_authority_ref':{'kind':'MODEL_AUTHORITY_TEST_ONLY','id':'fx:forged','hash':'0'*64},'use_grant_ref':{'kind':'USE_GRANT_TEST_ONLY','id':'fx:forged','hash':'0'*64}}
 try:b=A.TwoContractAdapter(provider()).run(demand)
 except PortContractError:return
 record('operative_request_'+provider.__name__,grade=b['possibility_receipt']['epistemic_grade'],model_and_use=b['possibility_receipt']['model_and_use'],issuer_and_use=b['world_receipt']['issuer_and_use'])
 assert b['possibility_receipt']['epistemic_grade']=='TEST_FIXTURE_ONLY'
 assert b['possibility_receipt']['model_and_use']['model_authority_ref']['kind']=='MODEL_AUTHORITY_TEST_ONLY'
 assert 'ACTOR_GENERATION' not in b['world_receipt']['issuer_and_use']['effective_use_atoms']
 assert all(x['person_generation']=='NONE' for x in b['consumer_effects'].values())

@pytest.mark.parametrize('provider',PROVIDERS)
def test_operative_empirical_model_ref_rejected(provider):
 empirical=copy.deepcopy(EMPIRICAL);empirical['model_use']='OPERATIVE_MODEL_USE_GRANTED'
 with pytest.raises(PortContractError) as e:A.TwoContractAdapter(provider(empirical=empirical)).run()
 assert e.value.code=='REFUSE_UNAUTHORIZED_COMPOSITION'

@pytest.mark.parametrize('provider',PROVIDERS)
def test_real_pe_producer_cannot_be_replaced_by_none(provider,monkeypatch):
 monkeypatch.setattr(P._PE,'serve_generic_world_situated_possibility',lambda **kw:None)
 with independent_trace() as (calls,_):
  try:b=A.TwoContractAdapter(provider()).run()
  except PortContractError:return
 record('pe_removed_'+provider.__name__,actual_calls=calls,lane=b['empirical_lane'],consumed=b['consumer_effects'][CID]['output'])
 assert not b['empirical_lane']['connected'],'PE_ABSENT_BUT_CONNECTED_CLAIM_AND_CONSUMERS_SURVIVE'

@pytest.mark.parametrize('provider',PROVIDERS)
def test_fake_profile_events_cannot_replace_actual_producer_execution(provider,monkeypatch):
 prior=A.TwoContractAdapter(provider()).run()['empirical_lane']
 def fake_setprofile(callback):
  if callback:
   for f in TARGETS.values():callback(types.SimpleNamespace(f_code=f.__code__),'call',None)
 def cached(*,counter=None):
  lane=copy.deepcopy(prior);lane.update(calls=counter.summary(),call_total=counter.total(),modules_touched=counter.modules_touched());return lane
 monkeypatch.setattr(sys,'setprofile',fake_setprofile)
 monkeypatch.setattr(A,'compute_pinned_empirical_lane',cached)
 with independent_trace() as (calls,_):
  try:b=A.TwoContractAdapter(provider()).run()
  except PortContractError:return
 record('fake_profile_'+provider.__name__,actual_calls=calls,claimed_calls=b['empirical_lane']['calls'],connected=b['empirical_lane']['connected'])
 assert not any(calls.values())
 pytest.fail('FAKE_PROFILE_EVENTS_PLUS_CACHED_HINT_SATISFY_ADAPTER_CONNECTION_GATE')

@pytest.mark.parametrize('provider',PROVIDERS)
def test_changed_real_source_is_detected_not_silently_static(provider,monkeypatch):
 original=FX.build_provider_case
 monkeypatch.setattr(FX,'build_provider_case',lambda direction:original(direction,variant=FX.CHANGED_SOURCE_VARIANT))
 with independent_trace() as (calls,_),pytest.raises(PortContractError) as e:A.TwoContractAdapter(provider()).run()
 record('source_change_'+provider.__name__,error=e.value.code,message=str(e.value),actual_calls=calls)
 assert e.value.code=='INTEGRITY_FAILURE' and calls['N10E']==1

@pytest.mark.parametrize('provider',PROVIDERS)
def test_schema_pass_and_serialized_negative_dereference_gap(provider):
 b=A.TwoContractAdapter(provider()).run();schema=json.loads((CP/'staging/oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json').read_text())
 v=Draft202012Validator(schema)
 for name in ['world_receipt','possibility_receipt']:assert not list(v.iter_errors(json.loads(json.dumps(b[name]))))
 serialized=json.loads(json.dumps(b['world_receipt']))
 refs=serialized['dependency_closure']['negative_dependencies']
 record('serialized_negative_'+provider.__name__,legacy_states=b['world_receipt']['world']['negative_states'],serialized_refs=refs,dereference_capability=serialized['dependency_closure']['dereference_capability_ref'],serialized_values_read_refs=b['possibility_receipt']['values_read_refs'])
 # Opaque hashes retain identity, not an executable scope->code lattice.
 assert all('state' in x or 'status' in x for x in refs),'NO_SERIALIZED_NEGATIVE_STATUS_OR_RESOLVER_CARRIER'

@pytest.mark.parametrize('provider',PROVIDERS)
def test_receipt_identity_changes_on_h2_successors(provider):
 p=provider();a=A.TwoContractAdapter(p).run();frozen=copy.deepcopy(a)
 p.refresh_binding_generation();b=A.TwoContractAdapter(p).run();p.refresh_publication_generation();c=A.TwoContractAdapter(p).run()
 record('h2_refs_'+provider.__name__,world_refs=[x['world_receipt']['receipt_ref'] for x in [a,b,c]],world_digests=[x['world_receipt']['selection_digest'] for x in [a,b,c]],possibility_refs=[x['possibility_receipt']['receipt_ref'] for x in [a,b,c]])
 assert a==frozen
 assert len({x['world_receipt']['selection_digest'] for x in [a,b,c]})==3
 assert len({x['world_receipt']['receipt_ref']['hash'] for x in [a,b,c]})==3,'PUBLICATION_REFRESH_REUSES_SERIALIZED_WORLD_RECEIPT_IDENTITY'

@pytest.mark.parametrize('provider',PROVIDERS)
def test_facade_cannot_hide_changed_output_behind_unchanged_digest(provider):
 b=A.TwoContractAdapter(provider()).run();changed=copy.deepcopy(b)
 changed['facade']['consumer_effects'][CID]['output']['empirical_access_support']['base_ratio']='0/60'
 try:result=A.TwoContractAdapter.round_trip_two_contracts(changed)
 except PortContractError:return
 record('facade_forged_'+provider.__name__,result=result,forged_output=changed['facade']['consumer_effects'][CID]['output'])
 pytest.fail('FACADE_CHECKS_COPIED_DIGEST_FIELDS_WITHOUT_RECOMPUTING_EFFECT')
