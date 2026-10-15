"""RC0-owned assertions: no imported candidate expected-class table."""
import copy,json,os
from pathlib import Path
import pytest
from jsonschema import Draft202012Validator
from port.adapter import TwoContractAdapter,provider_equivalence_report
from port.contracts import PortContractError
from port.provider_a import ProviderA
from port.provider_b import ProviderB
from port.world_baseline import BASELINE_WORLD,REVERSAL_GRANT_SCOPED
from port.world_laws import context_fingerprint,validate_freshness
RET=Path(os.environ['RC0_RETURN']);CP=RET/'runtime_root/WORKER_RETURNS/SOROK-R3-HQ298-SC0-VALUE-BEARING-PORT-R1'


def record(case,**values):
    (RET/'repro/observations').mkdir(exist_ok=True)
    (RET/'repro/observations'/f'{case}.json').write_text(json.dumps(dict(case=case,**values),indent=2)+'\n')


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
def test_actual_value_intervention_changes_both_consumers_and_only_affected_route(provider):
    before=TwoContractAdapter(provider()).run()
    world=copy.deepcopy(BASELINE_WORLD);world['routes']['fx:r:public']['values']['min_age']=18
    after=TwoContractAdapter(provider(world=world)).run()
    for cid in ['CONCEPTION_SCENARIO_PROPOSAL_INPUT_ONLY','NONPARENT_APPRENTICESHIP_ENTRY']:
        a=after['consumer_effects'][cid];b=before['consumer_effects'][cid]
        if cid.startswith('CONCEPTION'):
            assert a['output']['eligible_scenario_constraints'][0]['route_values']['min_age']==18
            assert a['output']['eligible_scenario_constraints'][1]==b['output']['eligible_scenario_constraints'][1]
        else:
            assert a['output']['apprenticeship_access_routes'][0]['entry_values']['min_age']==18
            assert a['output']['apprenticeship_access_routes'][1]==b['output']['apprenticeship_access_routes'][1]
        assert a['values_read']['values']['fx:r:public']['values']['min_age']==18
        assert a['consumer_digest']!=b['consumer_digest']
        assert a['person_generation']=='NONE'
    assert after['possibility_receipt']['support']==before['possibility_receipt']['support']
    record('values_'+provider.__name__,before=before,after=after,conclusion='TRUE_WORLD_VALUES_READ_BOTH_CONSUMERS; EMPIRICAL_SUPPORT_INVARIANT')


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
def test_adapter_denied_world_read_must_not_emit_consumer_values(provider):
    world=copy.deepcopy(BASELINE_WORLD);world['permission_ceiling']['revoked_atoms']=['WORLD_READ'];world['permission_ceiling']['use_atoms']=['POSSIBILITY_QUERY']
    p=provider(world=world)
    try:result=TwoContractAdapter(p).run()
    except PortContractError as e:
        record('denied_'+provider.__name__,diagnostic=e.code,consumer_output_returned=False)
        assert e.code=='DENIED_USE'
    else:
        record('denied_'+provider.__name__,consumer_output_returned=True,world_permission=result['world_receipt']['world']['permission_ceiling'],consumer_effects=result['consumer_effects'])
        pytest.fail('RC0_DENIED_PROVIDER_EMITTED_WORLD_VALUES_AND_CONSUMER_EFFECTS')


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
def test_foreign_demand_cannot_be_labelled_complete(provider):
    demand={'scope':'rc0:unavailable:foreign-world-scope'}
    try:result=TwoContractAdapter(provider()).run(demand)
    except PortContractError as e:record('demand_'+provider.__name__,refused=e.code)
    else:
        record('demand_'+provider.__name__,request=demand,selection_state=result['world_receipt']['selection_state'],served_world=result['world_receipt']['world']['semantic_world_id'])
        assert result['world_receipt']['selection_state']!='COMPLETE','RC0_FOREIGN_DEMAND_FALSE_COMPLETE'


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
def test_knowledge_asof_cannot_consume_future_publication(provider):
    # The original preserved fixture itself has published=2010 and as_of=2009.
    try:result=TwoContractAdapter(provider()).run()
    except PortContractError as e:
        record('clocks_'+provider.__name__,refused=e.code)
        assert e.code=='NO_CURRENT_OR_NOT_KNOWN_ASOF'
    else:
        clock=result['world_receipt']['world']['time_axes']
        record('clocks_'+provider.__name__,clocks=clock,read_values=result['consumer_effects']['NONPARENT_APPRENTICESHIP_ENTRY']['values_read'])
        assert int(clock['published'])<=int(clock['as_of']),'RC0_KNOWLEDGE_ASOF_LOOKAHEAD_ACCEPTED'


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
@pytest.mark.parametrize('field',['issuer','scope','target'])
def test_matching_issuer_string_cannot_authorize_foreign_scope_or_target(provider,field):
    p=provider();bundle=TwoContractAdapter(p).run();grant=copy.deepcopy(REVERSAL_GRANT_SCOPED)
    if field=='target':grant['binds']['target']='rc0:foreign-target';grant['binds']['reverse_target']='rc0:foreign-target'
    else:grant[field]='rc0:foreign-'+field
    try:result=p.request_role_reversal(bundle['world_receipt'],bundle['possibility_receipt'],grant)
    except PortContractError as e:
        record('reverse_'+provider.__name__+'_'+field,refused=e.code)
        assert e.code=='HELD_AUTHORITY'
    else:
        record('reverse_'+provider.__name__+'_'+field,grant=grant,result=result)
        pytest.fail('RC0_FOREIGN_REVERSAL_BINDING_PERMITTED_'+field)


def test_direct_receipts_satisfy_original_frozen_envelope_schema():
    schema=json.loads((CP/'oracles/01_VERSIONED_GENERIC_TWO_CONTRACT_ENVELOPE.json').read_text());Draft202012Validator.check_schema(schema)
    validator=Draft202012Validator(schema);bundle=TwoContractAdapter(ProviderA()).run();all_errors={}
    for key in ['world_receipt','possibility_receipt']:
        errors=list(validator.iter_errors(bundle[key]))
        all_errors[key]=[dict(path=list(e.absolute_path),message=e.message,context=[x.message for x in e.context]) for e in errors]
    record('schema',errors=all_errors)
    assert not any(all_errors.values()),'RC0_ORIGINAL_SC0_SCHEMA_NOT_IMPLEMENTED_BY_RAW_RECEIPTS'


def test_full_original_negative_state_distinctions_survive():
    source=json.loads((CP/'oracles/03_K10_STRUCTURAL_INFO_LOSS_ORACLES.json').read_text())['baseline']['status_rows']
    result=TwoContractAdapter(ProviderA()).run();actual=result['world_receipt']['world']['negative_states']
    expected={r['scope']:r['state'] for r in source};observed={r['scope']:r['state'] for r in actual}
    record('negative_states',expected=expected,actual=observed,missing={k:v for k,v in expected.items() if observed.get(k)!=v})
    assert expected==observed,'RC0_ORIGINAL_NEGATIVE_SCOPES_OR_CODES_LOST'


def test_h1_f1_f2_h3_and_both_h2_successors_preserve_explicit_deferral():
    p=ProviderA();a=TwoContractAdapter(p).run();w=a['world_receipt']['world']
    assert w['nary']['cardinality']==3 and len(w['nary']['participants'])==3
    assert w['f2']['f1_refs']==w['f1_refs'] and w['f2']['history_requirement_ref']==w['f2_requirement_ref']
    assert w['f2']['selection']=='DEFERRED_UNBOUND' and w['f2']['not_satisfaction'] is True
    assert w['generated_binding_echo']['upstream_authorship'] is False
    old=copy.deepcopy(a);p.refresh_binding_generation();b=TwoContractAdapter(p).run();p.refresh_publication_generation();c=TwoContractAdapter(p).run()
    assert [b['world_receipt']['binding_generation'],b['world_receipt']['publication_generation']]==[1,0]
    assert [c['world_receipt']['binding_generation'],c['world_receipt']['publication_generation']]==[1,1]
    assert a==old and len({x['world_receipt']['selection_digest'] for x in (a,b,c)})==3
    record('h1_h2_h3',before=a,binding=b,publication=c,actor_satisfaction='NOT_COMPUTED; EXPLICIT_DEFERRED_UNBOUND')


def test_changed_binding_guard_is_real_but_adapter_recomputes_new_selection():
    p=ProviderA();a=TwoContractAdapter(p).run();prior=context_fingerprint(a['world_receipt'])
    p._store['stage_two']['generated_binding_echo']['caller_fact']='RC0_CHANGED'
    current=p.resolve_world_selection({})
    with pytest.raises(PortContractError) as e:validate_freshness(current,prior_fingerprint=prior)
    assert e.value.code=='REJECT_STALE_BINDING_CONTEXT'
    b=TwoContractAdapter(p).run()
    assert b['world_receipt']['selection_digest']!=a['world_receipt']['selection_digest']
    record('refresh_guard',explicit_guard=e.value.code,new_selection_digest_changed=True,explicit_generation_unchanged=b['world_receipt']['binding_generation']==a['world_receipt']['binding_generation'],interpretation='NO_STALE_DIGEST_REUSE_DEMONSTRATED; AUTOMATIC_H2_GUARD_NOT_IN_ADAPTER')


def test_baseline_providers_equal_without_using_candidate_comparison_function():
    a=TwoContractAdapter(ProviderA()).run();b=TwoContractAdapter(ProviderB()).run()
    wa=copy.deepcopy(a['world_receipt']);wb=copy.deepcopy(b['world_receipt']);wa.pop('provider');wb.pop('provider')
    assert wa==wb
    for cid in a['consumer_effects']:
        ca=copy.deepcopy(a['consumer_effects'][cid]);cb=copy.deepcopy(b['consumer_effects'][cid]);ca['values_read'].pop('provider_id');cb['values_read'].pop('provider_id');assert ca==cb
    record('independent_provider_equality',whole_world_receipt_equal_except_provider=True,both_consumer_effects_equal=True,normalization='physical provider lineage plus provider_id only')
