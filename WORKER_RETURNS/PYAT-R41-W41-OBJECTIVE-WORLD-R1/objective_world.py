"""W41 readonly objective worlds over unchanged exact native owners.

Retained GT2 context, modeled E04 institutional worlds, source-indexed N9C
fixtures and F6P experiments retain separate authority scopes. No issued
multifield transport, empirical-world probability or measured trend is implied.
"""
from copy import deepcopy
from dataclasses import replace
from functools import lru_cache
from pathlib import Path
from tempfile import TemporaryDirectory
import w41_bootstrap as boot
from rawlsing_next.pre553_empirical_objects import canonicalize, semantic_hash
from rawlsing_next import m4_v557_v558_publication_repository as m4
from rawlsing_next import field_forge_conditional_support as ff
from rawlsing_next import gt12_c_to_d_relation_bridge as ff_admission
from rawlsing_next import gt12_d_to_m4_typed_bridge as ff_world
from rawlsing_next.pre553_repo_native_current_payload import load_current_gt2_query_fact_from_committed_transport
from rawlsing_next.gt12_e2b_publication_governance_binding import load_current_gt12_e2b_publication_governance_binding
from rawlsing_next import pre553_hq297_n9c_two_field_reader as n9c
from world_join import SelectedWorld
from product.nonparent import consume
from product.scenario import evaluate
import two_epoch_world as t35
from f6p_partial_bound_evidence_consumer import consume_f6m_evidence
import f6p_fixtures as f6
import ee1_temporal_owner as ee1
import ee1_fixtures as periods

SCHEMA='W41_READONLY_SOURCE_QUALIFIED_WORLD@1'
def view_hash(value):
    # Receipt identity only. Native producer semantic hashes remain untouched;
    # N9C retains its declared rounded percentage as a JSON number.
    import json,hashlib
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

CLOCKS={
 'HISTORICAL':t35.clock('HISTORICAL','2026-06-01','2026-04-15'),
 'AS_OF':t35.clock('AS_OF','2027-09-01','2027-05-01'),
 'TEST_CURRENT':t35.E2,
}
# Independent family controls extend the accepted institutional rules through
# their native publication API. They issue no empirical structural semantics.
FAMILIES=('base','two_epoch','formal','civil_sanction','civil_closed','exit_only','fee_only')
EXTRA={
 'civil_sanction':('civil_sanction',True),
 'civil_closed':('civil_open',False),
 'exit_only':('exit_cost',8),
 'fee_only':('training_fee',6),
}

@lru_cache(maxsize=1)
def retained_inputs():
    # Fixed native loader verifies all exact preimages. No caller paths or raw reads.
    return load_current_gt2_query_fact_from_committed_transport()

def retained_context():
    """Actual FF -> admission -> V554 -> M4 resolution, then lawful dereference.

    No operative M5 CURRENT authority is issued for the retained GT2 field;
    selected modeled rules independently exercise native M5 RSC reads.
    """
    query,fact=retained_inputs()
    relation=ff.produce_exact_conditional_support_profile(
        joint_fact=fact,joint_query=query,conditioner_ref=query.target_refs[0],
        target_ref=query.target_refs[1],
        producer_permission_ceiling=('STRUCTURAL_MEDIATION_INPUT',),
        relation_permission_ceiling=('STRUCTURAL_MEDIATION_INPUT',))
    admitted=ff_admission.admit_gt12_c_relation(relation).admission
    binding=load_current_gt12_e2b_publication_governance_binding()
    _,v554=ff_world.evaluate_typed_d_to_e_at_v554(admitted,
        governed_use_id=binding.governed_use_id,v554_rule_ref=binding.v554_rule_ref,
        publication_authority=binding.publication_authority)
    terminal=ff_world.publish_and_resolve_relation_v554_at_current_m4(admitted,v554,
        v557_allowed_uses=('CONTEXT',),requested_resolution_uses=('CONTEXT',),
        v557_authority_ref=binding.v557_authority_ref,
        v557_decision_state='ALLOW_CONTEXT_ONLY')
    # Consumer independently selects the resolved native object, reads F1
    # lineage, and dereferences that exact relation. No report-file value copy.
    entries=terminal.resolution.resolved_entries
    if len(entries)!=1:raise ValueError('EXACT_GT2_CONTEXT_REQUIRED')
    ref=entries[0].producer_object_ref
    obj=next(e.obj for e in terminal.repository.entries if e.obj.ref==ref)
    payload=canonicalize(obj.payload)
    if payload != canonicalize(v554.f1):raise ValueError('RESOLVED_F1_PAYLOAD_MISMATCH')
    if canonicalize(v554.f1['originating_field_forge_relation_exact_refs']) != [relation.ref.as_dict()]:
        raise ValueError('FF_RELATION_LINEAGE_MISMATCH')
    profile=canonicalize(relation.as_dict())
    return dict(state='RETAINED_CONTEXT_VALUES_READ',grade='EXACT_RETAINED_SOURCE_LOCAL_CONTEXT',
        source='Afrobarometer R5',native_unit='same respondent in 19210 common exposure risk set',
        measure='RAW_COUNTS_NOT_POPULATION_PROBABILITY',uncertainty='UNQUANTIFIED',
        permission='CONTEXT_ONLY',relation=profile,producer_fact_ref=fact.ref.as_dict(),
        producer_query_ref=query.ref.as_dict(),v554_F1=canonicalize(v554.f1),
        published_B1=None,resolved_producer_ref=ref.as_dict(),values_read=payload,
        resolution_ref=terminal.resolution.receipt.ref.as_dict(),
        operative_currentness='HOLD_NO_CURRENT_WORLD_M5_ISSUANCE',
        strong_field_mechanism='BLOCKED_EXPLICIT_AUTHORITY',
        route_probability=None)

def context_read_or_refusal():
    try:return retained_context()
    except ValueError as exc:
        return dict(state='RETAINED_CONTEXT_REFUSED',reason=str(exc),route_probability=None)

def position_context():
    """Reconstruct J04's exact qualified proving fact, not a new respondent read."""
    from rawlsing_next.tests.test_prev3_objective_position_v557_v558_publication import _input
    from rawlsing_next.prev3_objective_position_materializer import materialize_objective_position
    from rawlsing_next import prev3_objective_position_v557_v558_publication as owner
    fact=materialize_objective_position(_input())
    carrier=owner.publish_objective_position_fact(fact)
    query=owner.make_bound_objective_position_context_query(carrier,requested_source_domain_use=owner.SOURCE_DOMAIN_USE)
    result=owner.resolve_bound_objective_position_context(carrier,query)
    return dict(state='EXACT_J04_RECONSTRUCTION_CONTEXT_READ',
        grade='RETAINED_J04_PROVING_FACT_RECONSTRUCTION_NOT_SOURCE_REEXECUTION',
        fact_ref=fact.fact_ref.as_dict(),values_read=canonicalize(fact.canonical_material),
        resolution_ref=result.receipt.ref.as_dict(),
        source_domain_use=owner.SOURCE_DOMAIN_USE,scope='Afro R5 BEN0002 Q73A native0vs1',
        present_day_persistence=False,route_probability=None)

def independent_fields(*,as_of='2027-09-01',revoked=None,rows=None):
    """Native N9C dereference, without person/household/subscription conversion."""
    rows=deepcopy(rows if rows is not None else boot.bootstrap.fixture_rows())
    for row in rows:
        if row['role']==revoked:row['status']='REVOKED_TEST_ONLY'
    registry=n9c.TestOnlyRegistry(rows)
    refs=registry.refs_by_role()
    relation=dict(kind='TEST_ONLY_NONPOOLED_COPRESENCE',fixture_only=True,
                  issued_EE13=False,ordered_refs=[refs[n9c.GSS],refs[n9c.NCA]],population_join=False)
    return n9c.read_historical_test_only(registry,selected_refs=refs,relation=relation,
        as_of=as_of,clock_mode='HISTORICAL_PUBLICATION_AWARE',partial_allowed=True)

def f6_evidence(case,*,request_overrides=None):
    key=next(k for k in f6.OW.WORLD_BUILDERS if k.split('_')[0]==case)
    target,sources,policy=f6.OW.WORLD_BUILDERS[key]()
    try:bundle=f6.F6M.synthesize(target,sources,policy)
    except f6.F6M.SynthesisError as exc:
        return dict(case=case,state='INCOMPLETE_NATIVE_JOINT_DOMAIN',native_sources=sources,
            target=target,policy=policy,reason=str(exc),product_ref=None,evidence=None,
            world_use='TYPED_SOURCEFREE_PRODUCER_REFUSAL',display_class='TYPED_LIMITATION',
            route_probability=None,world_joint=None)
    request=f6.request(key);request.update(request_overrides or {})
    evidence=consume_f6m_evidence(bundle,request)
    # Keep the native receipt hash identified as such; the portable projection
    # replaces only the machine path, never a value, unit or permission.
    evidence['native_output_hash']=evidence.pop('output_hash')
    evidence['source_product']['module_file']='owners/f6p/native/rawlsing_next/pre553_heterogeneous_synthesis.py'
    evidence['portable_projection_hash']=semantic_hash(evidence)
    # The readonly consumer USES the evidence: point only when supported;
    # unknown mass and bounds are mandatory for partial identification.
    return dict(case=case,state=evidence['evidence_state'],
        world_use='SEPARATE_SOURCEFREE_EVIDENCE_ONLY__NO_N9_TRANSPORT_ADMISSION',
        native_sources=deepcopy(sources),target=target,policy=policy,
        evidence=evidence,product_ref=bundle['content_hash'],
        display_class=('POINT_AT_TEST_ESTIMAND' if evidence['evidence_state']=='SUPPORTED_SYNTHESIS'
                       else 'BOUNDS_AND_UNKNOWN' if evidence['evidence_state']=='PARTIAL_IDENTIFICATION'
                       else 'TYPED_LIMITATION'),
        route_probability=None,world_joint=None)

class ObjectiveWorld:
    """A read-only client combines only correctly typed scoped views.

    E04 NONPARENT_OPTIONS is called unchanged. Neither proposal nor R13 N9
    empirical purpose is rewritten. F6 evidence stays a distinct use contract.
    """
    def __init__(self,family='two_epoch',*,release='base'):
        if family not in FAMILIES:raise ValueError('UNDECLARED_RULE_FAMILY')
        self.family=family
        self.native=SelectedWorld(release=release,rules=family if family in ('base','two_epoch','formal') else 'base')
        if family in EXTRA:
            key,value=EXTRA[family];catalog=self.native.service.catalog;r=t35.RULE_REVISION
            catalog._publish(key,value,r['effective_from'],r['effective_to'],r['publication'],revision=r['revision'])
            catalog.catalog_hash=semantic_hash(dict(records=catalog.records,empirical=catalog.empirical_identity()))
        self.archive={}
    def read(self,mode='TEST_CURRENT',*,budget=5):
        if mode not in CLOCKS:raise ValueError('DECLARED_CLOCK_REQUIRED')
        clock=CLOCKS[mode]
        snapshot=self.native.snapshot(clock)
        acceptance=self.native.adapter.accept(t35.make_request(clock),snapshot)
        result=consume(self.native.service,snapshot,budget_tokens=budget)
        structural={k:self.native.service.catalog.read(snapshot,k) for k in t35.E.STRUCTURAL_KEYS}
        material=dict(schema=SCHEMA,grade='SOURCEFREE_TEST_ONLY_NATIVE_ORIGINAL_CONSUMER',
            family=self.family,clock=clock.binding(),snapshot_hash=snapshot.snapshot_hash,
            acceptance=acceptance.binding(),native_consumer=result,
            structural_values=structural,learned_binding=deepcopy(self.native.service.catalog.learned_binding),
            budget_tokens=budget,operative_N9=False,operative_CURRENT=False,
            route_probability=None,actor_executions=0)
        material['content_hash']=semantic_hash(material)
        self.archive[material['content_hash']]=deepcopy(material)
        return material
    def historical_receipt(self,h):
        if h not in self.archive:raise ValueError('EXACT_ARCHIVE_REF_REQUIRED')
        return dict(receipt=deepcopy(self.archive[h]),archival_only=True,fresh_use_authorized=False)
    def revoke(self,key):return self.native.service.catalog.revoke(key)
    def evidence_view(self,case='W2',*,mode='TEST_CURRENT',include_context=False):
        original=self.read(mode)
        fields=independent_fields(as_of=CLOCKS[mode].published_asof)
        evidence=f6_evidence(case)
        # A matching label cannot authorize an estimand/unit join. The exact
        # independently qualified view is returned beside the original client.
        view=dict(original_client=original,independent_native_fields=fields,
            multifield_evidence=evidence,matching_decision=dict(
                state='NO_AUTHORIZED_JOIN',reason='NO_MATCHED_SOURCE_ESTIMAND_OR_TRANSPORT_CONTRACT',
                empirical_source=original['learned_binding'],evidence_product=evidence['product_ref'],
                common_respondents=None,joint_probability=None),
            route_probability=None)
        if include_context:view['retained_context']=context_read_or_refusal()
        view['content_hash']=view_hash(view)
        return view

def temporal_methods():
    cases={'comparable_probe':periods.comparable_pair,'mixed_family':periods.mixed_family,
        'mixed_country':periods.mixed_country,'population_change':periods.population_change,
        'estimand_change':periods.estimand_change,'future_rule':periods.future_rule,
        'future_evidence':periods.future_evidence,'annual_gap':periods.annual_gap,
        'duplicate_year':periods.duplicate_year}
    results={}
    for name,maker in cases.items():
        with TemporaryDirectory(prefix='w41-temporal-') as d:
            verdict=ee1.compare_periods(maker(),periods.ASOF,d)
        # Overlay temp paths are execution-local locators, not scientific identity.
        def sanitize(value):
            if isinstance(value,dict):return {k:('EXECUTION_TIMESTAMP_NOT_SCIENTIFIC_IDENTITY' if k=='created_at' else sanitize(v)) for k,v in value.items()}
            if isinstance(value,list):return [sanitize(v) for v in value]
            if isinstance(value,str) and d in value:return value.replace(d,'SOURCEFREE_OVERLAY_ROOT')
            return value
        results[name]=sanitize(verdict)
    return dict(method='INHERITED_V553_WITH_EE1_IDENTITY_POPULATION_CLOCK_GATE',
        cases=results,measured_pairs=[],measured_delta=None,
        Ghana_measured_change=None,measured_state='HELD_UNISSUED_EE12',
        authority='SOURCEFREE_PROBE_ONLY_NOT_MEASURED_ISSUANCE')

def purpose_refusals():
    w=ObjectiveWorld();s=w.native.snapshot(t35.E1);out={}
    for name,call in {
        'CONCEPTION_SCENARIO_PROPOSALS':lambda:evaluate(w.native.service,s,t35.PROPOSALS),
        'N9_SELECTED_WORLD':lambda:w.native.adapter.serve(t35.make_request(t35.E1),w.native.adapter.accept(t35.make_request(t35.E1),s),s,consumers=[]),
    }.items():
        try:call()
        except ValueError as exc:out[name]=dict(state='HOLD',reason=str(exc))
        else:raise AssertionError('UNEXPECTED_PURPOSE_ADMISSION:'+name)
    return out

def product():
    worlds={}
    for family in FAMILIES:
        w=ObjectiveWorld(family)
        for mode in CLOCKS:
            for budget in (0,2,5,10):
                key=f'{family}/{mode}/budget{budget}'
                worlds[key]=w.read(mode,budget=budget)
    return dict(schema=SCHEMA,scope='SOURCEFREE_PRODUCT_BANK_PLUS_RETAINED_GT2_CONTEXT',
        worlds=worlds,retained_context=context_read_or_refusal(),
        position_context=position_context(),independent_fields=independent_fields(),
        multifield={f'W{i}':f6_evidence(f'W{i}') for i in range(1,9)},
        temporal=temporal_methods(),purposes=purpose_refusals(),
        operative_N9=False,transport_admitted=False,route_probability=None)

if __name__=='__main__':
    import json,sys
    Path(sys.argv[1]).write_text(json.dumps(product(),sort_keys=True,indent=2)+'\n')
