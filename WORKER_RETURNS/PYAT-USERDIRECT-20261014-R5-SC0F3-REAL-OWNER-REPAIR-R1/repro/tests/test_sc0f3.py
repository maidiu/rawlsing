"""Executable candidate predicates. Original suites stay separately unchanged."""
import copy
import datetime
import inspect
from fractions import Fraction
import pytest
from sc0f3.adapter import TwoContractAdapter,provider_equivalence_report
from sc0f3.providers import ProviderA,ProviderB
from sc0f3.fixture_owner import fixture_world,reversal_fixture_permit
from sc0f3.common import Hold,digest
from sc0f3.receipts import verify,refkey,schema
from jsonschema import Draft202012Validator


@pytest.fixture(scope='module')
def baseline():return TwoContractAdapter(ProviderA()).run()


def test_real_owners_completed_with_actual_args_results_and_values(baseline):
    n=baseline['native_computation']
    names=[x['function'] for x in n['calls']]
    for name in ('provide_empirical_possibility_slice','compose_positioned_subject_possibility','evaluate_positioned_subject_possibility'):
        assert names.count(name)>0
    for c in n['calls']:
        assert c['args_digest']==digest(c['args']) and c['result_digest']==digest(c['result'])
        assert c['args_digest']!=c['result_digest']
        assert c['module_file'].endswith('.py') and len(c['git_blob_sha1'])==40
    assert n['values_read'] and all(x['value_digest']==digest(x['value']) for x in n['values_read'])
    assert n['support']==dict(cells={'yes':54,'no':6},denominator=60)


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
def test_full_oneof_schema_and_all_refs_resolve(provider):
    b=TwoContractAdapter(provider()).run()
    for name in ('world_receipt','possibility_receipt'):
        Draft202012Validator(schema()).validate(b[name])
    assert verify(b)
    assert b['possibility_receipt']['world_snapshot_ref']==b['world_receipt']['snapshot_ref']


def test_50_10_native_numeric_propagation_both_consumers_and_cell_carriers(baseline):
    after=TwoContractAdapter(ProviderA(variant='50_10')).run()
    native=after['native_computation']
    assert native['support']==dict(cells={'yes':50,'no':10},denominator=60)
    geometry=native['geometry']
    assert {c['cell']:Fraction(*c['raw_probability_exact_fraction']['$exact_fraction']) for c in geometry['cells']}=={'yes':Fraction(5,6),'no':Fraction(1,6)}
    for cid,effect in after['consumer_effects'].items():
        s=effect['output']['empirical_support']
        assert (s['target_yes'],s['target_no'],s['denominator'])==(50,10,60)
        assert effect['consumer_digest']!=baseline['consumer_effects'][cid]['consumer_digest']
        assert effect['values_read']==baseline['consumer_effects'][cid]['values_read']
        assert after['carriers'][refkey(effect['empirical_read_ref'])]==geometry
    option_cells=[after['carriers'][refkey(c['value_ref'])] for c in after['possibility_receipt']['options']]
    assert {c['cell']:c['raw_numerator_support'] for c in option_cells}=={'yes':50,'no':10}
    worldcarrier=next(p for p in after['world_receipt']['payloads'] if p['object_ref']['id']=='complete-world')
    assert after['carriers'][refkey(worldcarrier['payload_ref'])]['support']['target_yes']==54


def test_no_register_or_mutable_issuer_store_and_forgery_stays_held():
    import sc0f3.adapter as a
    assert not hasattr(a,'register_issuer_warrant') and not hasattr(a,'ISSUER_REGISTRY')
    good=reversal_fixture_permit();bad=copy.deepcopy(good);bad['grant_id']='ATTACKER'
    for supplied in (None,bad,{'issuer':'TEST_ONLY:SC0F3_OWNER'},{}):
        with pytest.raises(Hold,match='HELD_AUTHORITY'):
            TwoContractAdapter(ProviderA()).request_role_reversal(supplied)
    # Caller mutation of a returned record does not change the owner fixture.
    good['denominator']=999
    assert reversal_fixture_permit()['denominator']==62


@pytest.mark.parametrize('field,value',[
 ('issuer','FORGED'),('world_source','OTHER'),('world_release','OTHER'),
 ('target','ANSWER'),('risk','FOREIGN'),('denominator',60),('operation','WORLD_READ'),
 ('expires','2999-01-01'),('not_before','2000-01-01'),('revoked_at','2999-01-01'),('knowledge_as_of','2012')])
def test_closed_warrant_exact_scope_cannot_be_altered(field,value):
    permit=reversal_fixture_permit();permit[field]=value
    with pytest.raises(Hold,match='HELD_AUTHORITY'):
        TwoContractAdapter(ProviderA()).request_role_reversal(permit)


@pytest.mark.parametrize('variant,yes,denom',[('54_6',54,62),('50_10',50,58)])
def test_authentic_test_only_reverse_executes_distinct_query_and_denominator(variant,yes,denom):
    b=TwoContractAdapter(ProviderA(variant=variant)).request_role_reversal(reversal_fixture_permit(variant))
    assert b['state']=='TEST_ONLY_NATIVE_REVERSE_QUERY_COMPUTED'
    n=b['native_computation'];assert n['support']==dict(cells={'P1':yes,'P2':8},denominator=denom)
    assert n['query']['requested_projection']['target_role']=='POSITION'
    assert any(c['function']=='provide_empirical_possibility_slice' for c in n['calls'])
    assert denom!=60 and b['computed_from_forward'] is False


@pytest.mark.parametrize('date',['2026-09-30','2026-10-25','2026-11-01'])
def test_active_reverse_notbefore_revocation_and_expiry(monkeypatch,date):
    class Date(datetime.date):
        @classmethod
        def today(cls):return cls.fromisoformat(date)
    monkeypatch.setattr(datetime,'date',Date)
    with pytest.raises(Hold,match='HELD_AUTHORITY'):
        TwoContractAdapter(ProviderA()).request_role_reversal(reversal_fixture_permit())


@pytest.mark.parametrize('provider',[ProviderA,ProviderB])
@pytest.mark.parametrize('atom',['WORLD_READ','POSSIBILITY_QUERY'])
def test_missing_or_revoked_permission_blocks_before_producer(monkeypatch,provider,atom):
    import sc0f3.producer as p
    def never(*a,**k):pytest.fail('Producer must not execute after denial')
    monkeypatch.setattr(p,'produce',never)
    for revoked in (False,True):
        w=fixture_world()
        if revoked:w['permission_ceiling']['revoked_atoms']=[atom]
        else:w['permission_ceiling']['use_atoms'].remove(atom)
        pr=provider(w)
        with pytest.raises(Hold,match='DENIED_USE'):TwoContractAdapter(pr).run()
        assert pr.read_count==0


def test_revocation_on_actual_read_prevents_return():
    class Revoking(ProviderA):
        def read_values(self,selection,keys):
            self.revoked_atoms=frozenset({'WORLD_READ'})
            return super().read_values(selection,keys)
    with pytest.raises(Hold,match='DENIED_USE'):TwoContractAdapter(Revoking()).run()


@pytest.mark.parametrize('state',[None,'PARTIAL','NO_CURRENT','DEFERRED'])
def test_selection_state_mandatory_and_active_before_producer(monkeypatch,state):
    class Partial(ProviderA):
        def resolve_world_selection(self,demand):
            s=super().resolve_world_selection(demand)
            if state is None:s.pop('selection_state')
            else:s['selection_state']=state
            return s
    import sc0f3.producer as p
    monkeypatch.setattr(p,'produce',lambda *a,**k:pytest.fail('Gate failed'))
    with pytest.raises(Hold,match='INCOMPLETE_SELECTION_NOT_POSITIVE'):TwoContractAdapter(Partial()).run()


@pytest.mark.parametrize('demand',[
 {'scope':'FOREIGN'},{'source':'FOREIGN'},{'release':'FOREIGN'},
 {'strata':['FOREIGN']},{'native_unit':'HOUSEHOLD'}, {'sampling_unit':'HOUSEHOLD'},
 {'target':'POSITION'}, {'temporal_operation':'LAG_INTERPOLATION'},
 {'demand_closure_verified':True}])
def test_demand_relative_source_stratum_target_and_no_global_scope_bypass(demand):
    with pytest.raises(Hold):TwoContractAdapter(ProviderA()).run(demand)


def test_town_scope_cannot_bypass_missing_stratum():
    w=fixture_world();w['native_strata'].pop()
    with pytest.raises(Hold,match='DEMAND_CLOSURE_INCOMPLETE'):
        TwoContractAdapter(ProviderA(w)).run({'scope':'fx:scope:town2008'})


def test_2009_2010_refuses_and_arbitrary_earlier_evidence_cannot_bypass():
    for evidence in (None,'forged',{'issued':True}):
        w=fixture_world();w['earlier_knowledge_evidence_ref']=evidence
        with pytest.raises(Hold,match='NO_CURRENT_OR_NOT_KNOWN_ASOF'):
            TwoContractAdapter(ProviderA(w)).run({'as_of':'2009'})


def test_scoped_earlier_fixture_evidence_and_content_scope_check():
    w=fixture_world();w['earlier_knowledge_evidence_ref']='TEST_ONLY:earlier-publication:2008'
    b=TwoContractAdapter(ProviderA(w)).run({'as_of':'2009'})
    assert b['world_receipt']['clock']['publication_knowledge']['knowledge_as_of']=='2009'
    w['routes']['fx:r:public']['values']['min_age']=18
    with pytest.raises(Hold,match='NO_CURRENT_OR_NOT_KNOWN_ASOF'):
        TwoContractAdapter(ProviderA(w)).run({'as_of':'2009'})


@pytest.mark.parametrize('mutation,code',[
 ('AH','REJECT_SEMANTIC_LOSS'),('nary','REJECT_CARDINALITY_ROLE_TOPOLOGY_LOSS'),
 ('F2','REJECT_F2_PREREQUISITE_LOSS'),('negative','REJECT_NEGATIVE_ALGEBRA_LOSS'),
 ('minority','REJECT_SUPPORT_ERASURE'),('contradiction','REJECT_ALTERNATIVE_ERASURE'),
 ('echo','REJECT_GENERATED_FACT_PROMOTION'),('public','REJECT_PUBLIC_RULE_AND_OWNER_LOSS')])
def test_conservation_through_real_adapter(mutation,code):
    w=fixture_world()
    if mutation=='AH':w['values'].pop('fx:AH')
    elif mutation=='nary':w['nary']['participants'].pop()
    elif mutation=='F2':w['f2']['history_requirement_ref']='FOREIGN_F1'
    elif mutation=='negative':w['negative_states'].pop()
    elif mutation=='minority':w['support']['target_no']=0
    elif mutation=='contradiction':w['contradictory_alternatives'].pop()
    elif mutation=='echo':w['generated_binding_echo']['upstream_authorship']=True
    elif mutation=='public':w['public_sanctions'].pop()
    with pytest.raises(Hold,match=code):TwoContractAdapter(ProviderA(w)).run()


def test_world_value_changes_both_readers_unrelated_route_and_empirics_stable(baseline):
    w=fixture_world();w['routes']['fx:r:public']['values']['min_age']=18
    b=TwoContractAdapter(ProviderA(w)).run()
    for cid,effect in b['consumer_effects'].items():
        old=baseline['consumer_effects'][cid]
        assert effect['output']!=old['output'] and effect['consumer_digest']!=old['consumer_digest']
        assert effect['values_read']['fx:r:public']['values']['min_age']==18
        assert effect['values_read']['fx:r:mutual']==old['values_read']['fx:r:mutual']
    assert b['native_computation']==baseline['native_computation']


def test_whole_provider_equivalence_and_semantic_extension_not_whitelisted(baseline):
    b=TwoContractAdapter(ProviderB()).run()
    assert provider_equivalence_report(baseline,b)['equivalent_except_physical_lineage']
    w=fixture_world();w['future_semantic_extension']='AUTH-B'
    changed=TwoContractAdapter(ProviderB(w)).run()
    assert not provider_equivalence_report(baseline,changed)['equivalent_except_physical_lineage']


def test_h2_real_source_boundary_separate_binding_successor_prior_unchanged():
    p=ProviderA();ad=TwoContractAdapter(p);a=ad.run();saved=copy.deepcopy(a)
    p.refresh_binding_generation();b=ad.run()
    p.refresh_publication_generation();c=ad.run()
    assert a==saved
    assert a['world_receipt']['snapshot_ref']!=b['world_receipt']['snapshot_ref']!=c['world_receipt']['snapshot_ref']
    assert a['native_computation']==b['native_computation']==c['native_computation']
    complete=lambda x:next(x['carriers'][refkey(z['payload_ref'])] for z in x['world_receipt']['payloads'] if z['object_ref']['id']=='complete-world')
    assert complete(a)['source_release_ref']==complete(b)['source_release_ref']
    assert complete(c)['source_release_ref']!=complete(b)['source_release_ref']
    assert complete(c)['time_axes']['published']!=complete(b)['time_axes']['published']


@pytest.mark.parametrize('drift',['binding','publication','counter_only'])
def test_h2_unmarked_drift_active_in_entrypoint(drift):
    p=ProviderA();a=TwoContractAdapter(p);a.run();w=p._read_world()
    if drift=='binding':w['generated_binding_echo']['caller_fact']='UNMARKED'
    elif drift=='publication':w['time_axes']['published']='2010-09'
    else:p.publication_generation += 1
    p._write_world(w)
    with pytest.raises(Hold,match='REJECT_STALE_'):a.run()


@pytest.mark.parametrize('part',['output','carrier','receipt','remove_effect'])
def test_bound_receipts_values_and_complete_consumer_effects_reject_tamper(baseline,part):
    b=copy.deepcopy(baseline)
    if part=='output':next(iter(b['consumer_effects'].values()))['output']['empirical_support']['target_yes']=999
    elif part=='carrier':b['carriers'][next(iter(b['carriers']))]='TAMPER'
    elif part=='receipt':b['world_receipt']['state']['reason']='TAMPER'
    else:b['consumer_effects'].pop(next(iter(b['consumer_effects'])))
    with pytest.raises(Hold):verify(b)


def test_explicit_actor_denial():
    with pytest.raises(Hold,match='REFUSE_UNGRANTED_ACTOR_USE'):
        TwoContractAdapter(ProviderA()).request_actor_weld()


def test_sourcefree_ceiling_original_source_is_typed_hold():
    with pytest.raises(Hold,match='DEMAND_CLOSURE_INCOMPLETE'):
        TwoContractAdapter(ProviderA()).run({'source':'ORIGINAL_SURVEY_SOURCE'})


def test_native_owner_refusal_never_falls_back(monkeypatch):
    import rawlsing_next.pre553_empirical_possibility_provider as owner
    def unavailable(**kwargs):
        raise Hold('HELD_AUTHORITY','Native owner refusal probe')
    monkeypatch.setattr(owner,'provide_empirical_possibility_slice',unavailable)
    with pytest.raises(Hold,match='Native owner refusal probe'):
        TwoContractAdapter(ProviderA()).run()


def test_actor_fields_cannot_enter_world_payload():
    w=fixture_world();w['actor_state']={'personality':'INVENTED'}
    with pytest.raises(Hold,match='REJECT_ACTOR_JURISDICTION'):
        TwoContractAdapter(ProviderA(w)).run()


def test_deleted_consumer_rehashed_container_still_refuses(baseline):
    b=copy.deepcopy(baseline);b['consumer_effects'].pop('NONPARENT_APPRENTICESHIP_ENTRY')
    b['carrier_digest']=digest({k:v for k,v in b.items() if k!='carrier_digest'})
    with pytest.raises(Hold,match='Complete two-consumer'):
        verify(b)


def test_reversal_knowledge_cut_must_match_owner_warrant():
    w=fixture_world();w['time_axes']['as_of']='2012'
    with pytest.raises(Hold,match='Knowledge-as-of'):
        TwoContractAdapter(ProviderA(w)).request_role_reversal(reversal_fixture_permit())


def test_all_twelve_native_negative_scopes_and_measures_survive(baseline):
    entry=next(z for z in baseline['world_receipt']['payloads'] if z['object_ref']['id']=='complete-world')
    w=baseline['carriers'][refkey(entry['payload_ref'])]
    assert w['negative_states']==fixture_world()['negative_states']
    assert len(w['negative_states'])==12
    statuses={s['scope']:s['state'] for s in w['negative_states']}
    actual={s['demand_key']:s['status']['code'] for s in baseline['world_receipt']['selection'] if s['demand_key'] in statuses}
    assert actual==statuses


@pytest.mark.parametrize('field',['sanction_refs','category_refs','rule_ref'])
def test_each_route_retains_public_owner_refs(field):
    w=fixture_world();w['routes']['fx:r:public'][field]=[] if field!='rule_ref' else 'FOREIGN'
    with pytest.raises(Hold,match='REJECT_PUBLIC_RULE_AND_OWNER_LOSS'):
        TwoContractAdapter(ProviderA(w)).run()


def test_route_cannot_promote_fixture_grade():
    w=fixture_world();w['routes']['fx:r:mutual']['epistemic_grade']='OBSERVED_SOURCE_FACT'
    with pytest.raises(Hold,match='REJECT_EPISTEMIC_PROMOTION'):
        TwoContractAdapter(ProviderB(w)).run()


def test_opaque_selected_values_are_typed_refusal():
    w=fixture_world();w['values']={k:'sha256:opaque' for k in w['values']}
    with pytest.raises(Hold,match='DEMAND_CLOSURE_INCOMPLETE'):
        TwoContractAdapter(ProviderA(w)).run()


@pytest.mark.parametrize('denominator',[62.0,True,'62'])
def test_warrant_denominator_requires_exact_integer_type(denominator):
    grant=reversal_fixture_permit();grant['denominator']=denominator
    with pytest.raises(Hold,match='HELD_AUTHORITY'):
        TwoContractAdapter(ProviderA()).request_role_reversal(grant)


def test_reverse_checks_selected_ceiling_before_native_computation(monkeypatch):
    class DeniedSelection(ProviderA):
        def resolve_world_selection(self,demand):
            s=super().resolve_world_selection(demand)
            s['world']['permission_ceiling']['revoked_atoms']=['POSSIBILITY_QUERY']
            return s
    import sc0f3.producer as p
    monkeypatch.setattr(p,'produce',lambda *a,**kw:pytest.fail('Native producer reached after selected denial'))
    with pytest.raises(Hold,match='DENIED_USE'):
        TwoContractAdapter(DeniedSelection()).request_role_reversal(reversal_fixture_permit())
