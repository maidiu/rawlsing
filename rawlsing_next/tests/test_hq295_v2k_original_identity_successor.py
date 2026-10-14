"""Actual source-free C11 scope variants, using pinned existing owner factories.

These fixtures construct synthetic scope inputs, never issue original authority.
No monkeypatching of owner code and no protected production edits.
"""
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace
import json
import pytest
from rawlsing_next.pre553_empirical_objects import CanonicalSemanticObject, ExactRef, exact_ref
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding
from rawlsing_next.pre553_source_backed_c11_facade import raw_physical_value_witness
from rawlsing_next.pre553_route_b_production import execute_route_b_production
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K
from rawlsing_next.tests.test_pre553_empirical_query import _ref
from rawlsing_next.tests.test_pre553_route_b_production import _fixture as physical_fixture
from rawlsing_next.tests.test_pre553_empirical_query import _branch_predicate, _predicate, _response_leaf, _query
from rawlsing_next.tests.test_pre553_discovery_exact import _grammar, _atom, _qt, _rule, _discovery_authority


def sourcefree_original_inputs(namespace, form='F1'):
    fx = physical_fixture()
    old = fx['projection']
    old_u = old.universes[0]
    universe = type(old_u)(typed_state=old_u.typed_state,
        authority_snapshot_refs=old_u.authority_snapshot_refs, dependency_refs=old_u.dependency_refs,
        producer_replay_locator_or_reference_root=old_u.producer_replay_locator_or_reference_root,
        **{**dict(old_u.semantic_fields), 'respondent_namespace': namespace, 'instrument_release': old_u.instrument_release + '/' + form})
    objects = {old_u.ref: universe}
    refs = {old_u.ref: universe.ref}
    respondents = tuple(replace(r, empirical_universe_ref=universe.ref) for r in old.respondents)
    refs.update({a.ref: b.ref for a, b in zip(old.respondents, respondents)})

    def rebind(value):
        if isinstance(value, ExactRef):
            return refs.get(value, value)
        if isinstance(value, CanonicalSemanticObject):
            if value.ref in objects:
                return objects[value.ref]
            return type(value)(typed_state=value.typed_state,
                authority_snapshot_refs=value.authority_snapshot_refs,
                dependency_refs=rebind(value.dependency_refs),
                producer_replay_locator_or_reference_root=rebind(value.producer_replay_locator_or_reference_root),
                **rebind(dict(value.semantic_fields)))
        if isinstance(value, Mapping):
            if set(value) == {'kind', 'object_id', 'content_hash'}:
                ref = ExactRef(**value)
                return refs.get(ref, ref).as_dict()
            return {k: rebind(v) for k, v in value.items()}
        if isinstance(value, tuple):
            return tuple(rebind(v) for v in value)
        if isinstance(value, list):
            return [rebind(v) for v in value]
        if is_dataclass(value):
            return replace(value, **{f.name: rebind(getattr(value, f.name)) for f in fields(value) if f.init})
        return value

    projection = rebind(old)
    assert projection.universes[0].respondent_namespace == namespace
    assert {r.empirical_universe_ref for r in projection.respondents} == {universe.ref}
    stub = dict(universe=universe, respondents={r.respondent_key: r for r in projection.respondents},
                qrefs=fx['qrefs'], risk_refs={'R': fx['risk']}, source_auth=projection.authority_snapshots[0])
    qauth, dauth = fx['qauth'], fx['dauth']
    all_p = _branch_predicate(stub, qauth, tag='a04b-actual-all')
    x1 = _predicate(stub, qauth, _response_leaf(stub, qauth, 'X', 1), tag='a04b-actual-x1')
    query = _query(stub, qauth, all_p, ('X', 'Y'), measure='RAW', tag='a04b-actual-xy')
    grammar = _grammar(operation=dauth.governed_operations[0],
        atoms=[_atom('ALL', all_p, 'BRANCH'), _atom('X1', x1, 'RESPONSE')],
        templates=[_qt('XY', query)], rules=[_rule('a04b-actual-rule', 'PAIR_RESPONSE_COTRAVEL',
        'SINGLE_ATOM', atom_ids=('X1',), baseline_atom_id='ALL', query_template_id='XY',
        validation={'kind': 'DISTRIBUTION_DIFFERS_FROM_BASELINE'})])
    discovery = _discovery_authority(stub, grammar, dauth, tag='a04b-actual-discovery')
    catalog = RuntimeObjectCatalog(authorities=(*projection.authority_snapshots, qauth, dauth),
        predicates=(all_p, x1), queries=(query,), discovery_authorities=(discovery,))
    rows = []
    for kind in ('PAIR', 'DISCOVERY'):
        row = dict(source='A04B-ACTUAL-SCOPE-SOURCEFREE', wave='W1', item='X', form=form, slot=kind,
            semantic_op_class='PAIR_RESPONSE_COTRAVEL' if kind == 'PAIR' else 'BOUNDED_DISCOVERY',
            semantic_roles=['CONDITIONER', 'TARGET'] if kind == 'PAIR' else ['BASE'], target='XY',
            condition_order=['X', 'Y'] if kind == 'PAIR' else [], measure_kind='RAW',
            source_identity=fx['stream'].source_sha256,
            authority_ref=(qauth if kind == 'PAIR' else dauth).authority_ref.key,
            risk_identity=fx['risk'].key, topology_identity='SCALAR_2X2_JOINT',
            required_consumer=P.CONSUMER, state='RUNNABLE')
        if kind == 'PAIR':
            row.update(query_ref=query.ref.as_dict(), predicate_ref=all_p.ref.as_dict())
        else:
            row.update(discovery_authority_ref=discovery.ref.as_dict())
        rows.append(row)
    inventory = []
    row_respondents = {b.row_ordinal: b.respondent_ref for b in projection.row_bindings}
    rules = {r.slot.name: r for r in projection.response_slots}
    for cell in fx['stream'].cell_iter_factory():
        if cell.variable_name not in rules:
            continue
        for occurrence in rules[cell.variable_name].values[0].occurrences:
            inventory.append(dict(respondent_ref=row_respondents[cell.row_ordinal].as_dict(),
                item_ref=fx['qrefs'][cell.variable_name].as_dict(),
                raw_response_value=raw_physical_value_witness(cell.raw_value),
                configuration=dict(occurrence.multiplicity_order_rank_fields), response_state='SUBSTANTIVE_RESPONSE'))
    expected = P.FrozenExpected.from_documentary_payload(dict(schema=P.V.ACCEPTED_EXPECTED_SCHEMA,
        expected_derived_from='EXTERNAL_FROZEN', declarations=rows, source_inventory=inventory))
    reverse_query = _query(stub, qauth, all_p, ('Y', 'X'), measure='RAW', tag='v2k-B-yx')
    catalog = RuntimeObjectCatalog(authorities=catalog.authorities, predicates=catalog.predicates,
        queries=(query, reverse_query), discovery_authorities=(discovery,))
    b_row = dict(rows[0], item='Y', slot='B', target='YX', condition_order=['Y', 'X'],
        query_ref=reverse_query.ref.as_dict())
    rows.insert(1, b_row)
    held = dict(rows[0], item='O', slot='ORDERED', semantic_op_class='NONSCALAR_TOPOLOGY_PRESERVATION',
        semantic_roles=['BASE'], target='O', condition_order=[], topology_identity='ORDERED_SEQUENCE',
        state='HELD', hold_reason='ORDERED_OWNER_NOT_ISSUED')
    held.pop('query_ref'); held.pop('predicate_ref')
    rows.append(held)
    expected = P.FrozenExpected.from_documentary_payload(dict(schema=P.V.ACCEPTED_EXPECTED_SCHEMA,
        expected_derived_from='EXTERNAL_FROZEN', declarations=rows, source_inventory=inventory))
    declarations = [C.V2ExpectedWorkDeclaration(**{k: ExactRef(**v) if k in
        ('query_ref', 'predicate_ref', 'discovery_authority_ref') else tuple(v) if k in
        ('semantic_roles', 'condition_order') else v for k, v in row.items()}) for row in rows]
    bindings = C.v2_bind_semantic_to_dispatch(declarations=declarations,
        projection_fields={f.name: getattr(projection, f.name) for f in fields(projection)}, runtime_catalog=catalog)
    return dict(fx=fx, projection=projection, universe=universe, catalog=catalog,
        all_p=all_p, query=query, reverse_query=reverse_query, discovery=discovery,
        expected=expected, declarations=declarations, bindings=bindings)


def freeze_original_before_production(inputs):
    """Separately authored synthetic original roster, never reconstructed from results."""
    projection = inputs['projection']; universe = inputs['universe']
    records = []
    for declaration in inputs['declarations']:
        order = declaration.condition_order if declaration.query_ref else ('X', 'Y')
        if not declaration.is_runnable and declaration.item in inputs['fx']['qrefs']:
            order = (declaration.item,)
        if not order:
            order = ('X', 'Y')
        original = K.OriginalIdentity(
            source_release_ref=ExactRef('SOURCE_ARTIFACT', projection.source_artifact_id, projection.expected_source_sha256),
            empirical_universe_ref=universe.ref,
            native_item_refs=tuple(inputs['fx']['qrefs'][item] for item in order),
            respondent_namespace=universe.respondent_namespace, respondent_unit='SYNTHETIC_SELECTED_ADULT',
            form=declaration.form, language='SOURCEFREE-LANGUAGE-A', instrument_release=universe.instrument_release,
            administered_occurrence='SOURCEFREE-INSTRUMENT-BATTERY-1',
            option_scope=('AB','BA') if declaration.item=='O' else ('0','1'),
            routing_refs=tuple(r.ref for r in projection.routing if exact_ref(r.question_or_target_ref) in
                {inputs['fx']['qrefs'][item] for item in order}),
            original_item_scope_ref=_ref('SOURCEFREE_ORIGINAL_ITEM_SCOPE','v2k-items-'+declaration.item))
        records.append(K.OriginalExpectedWork(original, declaration,
            _ref('SOURCEFREE_OPERATION_SCOPE','v2k-operation-'+declaration.slot),
            _ref('SOURCEFREE_ORIGINAL_U','v2k-independent-U'),
            _ref('SOURCEFREE_PROSPECTIVE_E','v2k-independent-E'),
            _ref('SOURCEFREE_CUSTODY_WITNESS','v2k-custodian-not-authenticated')))
    return tuple(records), K.FrozenOriginalExpected.from_records(records, input_origin=K.ORIGIN)


def prepare_owner_scope(root, inputs, records):
    """Only called AFTER original successor expectation was frozen."""
    production = execute_route_b_production(source=inputs['fx']['stream'], projection=inputs['projection'],
        runtime_catalog=inputs['catalog'], i03_requests=[dict(query_ref=q.ref, predicate_ref=inputs['all_p'].ref)
            for q in (inputs['query'], inputs['reverse_query'])], discovery_authority_ref=inputs['discovery'].ref)
    executor = production.repository_binding.executor
    facts = {f.ref.key:f for outcome in production.i03_results for f in outcome.facts}
    discoveries = {r.ref.key:production.i05_result for r in production.i05_result.receipts}
    calls = []
    def execute(unit):
        calls.append(unit.unit_ref.key)
        if unit.job_kind == 'DISCOVERY':
            outcome=executor.execute_i05(discovery_authority_ref=unit.job_ref)
            discoveries.update({r.ref.key:outcome for r in outcome.receipts})
            refs=tuple(r.ref for r in outcome.receipts)
        else:
            outcome=executor.execute_i03(query_ref=unit.job_ref,predicate_ref=inputs['all_p'].ref)
            facts.update({f.ref.key:f for f in outcome.facts}); refs=tuple(f.ref for f in outcome.facts)
        return ExecutionOutcome(result_refs=refs,provenance_refs=(unit.job_ref,*unit.semantic_input_refs))
    manifest=BatchManifest(tuple(BatchUnitSpec(job_kind='QUERY' if b.dispatch_predicate_ref else 'DISCOVERY',
        job_ref=b.dispatch_job_ref,release_refs=(production.c11_release.release_ref,),
        semantic_input_refs=tuple(r for r in (b.dispatch_predicate_ref,b.dispatch_authority_ref) if r))
        for b in inputs['bindings']))
    session=G.open_session(manifest=manifest,repository=executor.repository,root=root,
        source_sha256=inputs['fx']['stream'].source_sha256,
        executors={'QUERY':ExecutorBinding(inputs['fx']['qauth'].ref,execute),
                   'DISCOVERY':ExecutorBinding(inputs['fx']['dauth'].ref,execute)})
    kwargs=dict(expected=inputs['expected'],session=session,runtime_catalog=inputs['catalog'],
        resolve_fact=lambda r:facts[r.key],resolve_discovery=lambda r:discoveries[r.key],
        producer_permission_ceiling=('SOURCE_FREE_DEV',))
    return K.OwnerScopePlan(tuple(r.key for r in records if r.legacy.is_runnable),kwargs),calls


def successor_fixture(root):
    # Original inputs and independent candidate E are frozen across ALL scopes
    # before even the first Route B / I03 / I05 producer is invoked.
    inputs=[sourcefree_original_inputs(ns) for ns in ('V2K-NAMESPACE-A','V2K-NAMESPACE-B')]
    per_scope=[freeze_original_before_production(i)[0] for i in inputs]
    records=tuple(r for group in per_scope for r in group)
    expected=K.FrozenOriginalExpected.from_records(records,input_origin=K.ORIGIN)
    prepared=[prepare_owner_scope(root/str(i),data,group) for i,(data,group) in enumerate(zip(inputs,per_scope))]
    return records,expected,tuple(p for p,calls in prepared),[calls for p,calls in prepared]


def test_actual_two_namespace_original_successor_consumes_all_B_and_J_only(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    report=K.run_sourcefree(expected=expected,selected_scopes=plans)
    assert report['ok'] and len(report['links'])==6
    assert [len(c) for c in calls]==[3,3]
    assert len({l['original_expected_work_key'] for l in report['links']})==6
    assert len({l['legacy_expected_work_key'] for l in report['links']})==3
    assert len({json.dumps(l['consumer_ref'],sort_keys=True) for l in report['links']})==6
    assert len(report['nonrunnable'])==2
    assert all(r['legacy']['state']=='HELD' for r in report['nonrunnable'])
    assert all(r['original']['native_item_refs'][0]['object_id'].endswith('m01-O')
        and r['original']['option_scope']==['AB','BA']
        and r['legacy']['topology_identity']=='ORDERED_SEQUENCE' for r in report['nonrunnable'])
    for link in report['links']:
        assert link['producer_result_ref']==link['consumer_material']['producer_fact_ref']
    prior={l['original_expected_work_key']:ExactRef(**l['consumer_ref']) for l in report['links']}
    replay=K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs=prior)
    assert replay['ok'] and replay['links']==report['links'] and [len(c) for c in calls]==[3,3]


@pytest.mark.parametrize('omit', ['B','DISCOVERY'])
def test_independent_B_or_J_only_omission_rejected_before_any_durable_call(tmp_path,omit):
    records,expected,plans,calls=successor_fixture(tmp_path)
    omitted={r.key for r in records if r.legacy.slot==omit}
    selected=tuple(replace(p,original_work_keys=tuple(k for k in p.original_work_keys if k not in omitted)) for p in plans)
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN'):
        K.run_sourcefree(expected=expected,selected_scopes=selected)
    assert calls==[[],[]]


@pytest.mark.parametrize('field,value', [('respondent_namespace','OTHER'),('respondent_unit','HOUSEHOLD'),
    ('form','F2'),('language','OTHER'),('administered_occurrence','SECOND'),('option_scope',('1','0'))])
def test_original_identity_fields_distinguish_successor_keys(field,value):
    data=sourcefree_original_inputs('V2K-SCOPE');records,_=freeze_original_before_production(data)
    work=records[0]
    identity=replace(work.original,**{field:value})
    legacy=replace(work.legacy,form=value) if field=='form' else work.legacy
    other=replace(work,original=identity,legacy=legacy)
    assert other.key!=work.key


def test_exact_query_predicate_routing_and_custody_refs_bind_successor_identity():
    data=sourcefree_original_inputs('V2K-SCOPE');work=freeze_original_before_production(data)[0][0]
    for field in ('query_ref','predicate_ref'):
        assert replace(work,legacy=replace(work.legacy,**{field:_ref('SOURCEFREE_FOREIGN_REF',field)})).key!=work.key
    assert replace(work,original=replace(work.original,routing_refs=(_ref('SOURCEFREE_ROUTE','other'),))).key!=work.key
    for field in ('original_operation_scope_ref','original_U_ref','independent_E_ref','independent_custody_ref'):
        assert replace(work,**{field:_ref('SOURCEFREE_FOREIGN_REF',field)}).key!=work.key


def test_actual_wrong_namespace_or_routing_rejected_before_first_scope_execution(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    for field,value,diagnostic in [('respondent_namespace','ALIEN','ORIGINAL_RESPONDENT_NAMESPACE_MISMATCH'),
        ('routing_refs',(_ref('SOURCEFREE_ROUTE','alien'),),'ORIGINAL_ROUTING_NOT_EXACT')]:
        altered=replace(records[-2],original=replace(records[-2].original,**{field:value}))
        changed=tuple(altered if w is records[-2] else w for w in records)
        frozen=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN)
        selected=tuple(replace(p,original_work_keys=tuple(altered.key if k==records[-2].key else k
            for k in p.original_work_keys)) for p in plans)
        with pytest.raises(K.IdentityError,match=diagnostic):
            K.run_sourcefree(expected=frozen,selected_scopes=selected)
        assert calls==[[],[]]


def test_local_selected_A_only_pass_cannot_replace_independent_original_B_and_J(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    selected_record=records[0]
    kwargs=dict(plans[0].p01_kwargs)
    doc=json.loads(kwargs['expected'].payload_json)
    doc['declarations']=[r for r in doc['declarations'] if r.get('state')!='RUNNABLE'
                         or r.get('query_ref')==selected_record.legacy.query_ref.as_dict()]
    kwargs['expected']=P.FrozenExpected.from_documentary_payload(doc)
    old=kwargs['session']
    unit=next(u for u in old.manifest.units if u.job_ref==selected_record.legacy.query_ref)
    kwargs['session']=G.open_session(manifest=BatchManifest((unit,)),repository=old.repository,
        executors=old.executors,root=tmp_path/'A-only-local',source_sha256=old.source_sha256)
    local=P.run_integrated(**kwargs)
    assert local['ok'] and len(local['consumer_products'])==1 and len(calls[0])==1
    snapshot=[len(c) for c in calls]
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN'):
        K.run_sourcefree(expected=expected,selected_scopes=(K.OwnerScopePlan((selected_record.key,),kwargs),))
    assert [len(c) for c in calls]==snapshot
    assert len(expected.checked())==8


def test_foreign_original_key_same_count_and_duplicate_are_rejected(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    first=plans[0]
    replaced=replace(first,original_work_keys=('f'*64,*first.original_work_keys[1:]))
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN'):
        K.run_sourcefree(expected=expected,selected_scopes=(replaced,plans[1]))
    duplicate=replace(first,original_work_keys=(*first.original_work_keys,first.original_work_keys[0]))
    with pytest.raises(K.IdentityError,match='DUPLICATE_ORIGINAL_SELECTED_WORK'):
        K.run_sourcefree(expected=expected,selected_scopes=(duplicate,plans[1]))
    assert calls==[[],[]]


def test_original_payload_digest_preimage_and_origin_tampering_rejected():
    data=sourcefree_original_inputs('V2K-TAMPER');records,expected=freeze_original_before_production(data)
    raw=json.loads(expected.payload_json); raw['records'][0]['original']['language']='ALIEN'
    text=json.dumps(raw)
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTATION_DIGEST_MISMATCH'):
        replace(expected,payload_json=text).checked()
    # Attacker recomputes payload integrity but leaves its supplied work-key stale.
    with pytest.raises(K.IdentityError,match='ORIGINAL_KEY_PREIMAGE_MISMATCH'):
        replace(expected,payload_json=text,payload_sha256=K.semantic_hash(raw)).checked()
    with pytest.raises(K.IdentityError,match='EXPECTED_SET_NOT_INDEPENDENT_SOURCEFREE_INPUT'):
        K.FrozenOriginalExpected.from_records(records,input_origin='RESULT_DERIVED')
    with pytest.raises(K.IdentityError,match='DUPLICATE_OR_EMPTY_ORIGINAL_EXPECTED_KEYS'):
        K.FrozenOriginalExpected.from_records((*records,records[0]),input_origin=K.ORIGIN)


def test_real_source_permission_and_foreign_replay_keys_never_granted(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    kwargs=dict(plans[1].p01_kwargs);kwargs['producer_permission_ceiling']=('REAL_EXECUTION',)
    with pytest.raises(K.IdentityError,match='SOURCEFREE_ONLY_NO_REAL_EXECUTION'):
        K.run_sourcefree(expected=expected,selected_scopes=(plans[0],replace(plans[1],p01_kwargs=kwargs)))
    with pytest.raises(K.IdentityError,match='ORIGINAL_REPLAY_CONSUMER_KEY_SET_MISMATCH'):
        K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs={})
    assert calls==[[],[]]


def test_legacy_original_direction_source_and_form_mismatch_rejected(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    w=records[0]
    with pytest.raises(K.IdentityError,match='ORIGINAL_FORM_BINDING_MISMATCH'):
        replace(w,original=replace(w.original,form='ALIEN'))
    with pytest.raises(K.IdentityError,match='ORIGINAL_SOURCE_BINDING_MISMATCH'):
        replace(w,original=replace(w.original,source_release_ref=_ref('SOURCE_ARTIFACT','ALIEN')))
    reverse=replace(w,legacy=replace(w.legacy,condition_order=('Y','X')))
    frozen=K.FrozenOriginalExpected.from_records(tuple(reverse if r is w else r for r in records),input_origin=K.ORIGIN)
    selected=tuple(replace(p,original_work_keys=tuple(reverse.key if key==w.key else key for key in p.original_work_keys)) for p in plans)
    with pytest.raises(K.IdentityError,match='P01_EXPECTED_ORIGINAL_BINDING_ANTI_JOIN'):
        K.run_sourcefree(expected=frozen,selected_scopes=selected)
    assert calls==[[],[]]


def test_source_release_item_operation_and_measure_identity_changes_keys():
    data=sourcefree_original_inputs('V2K-KEYS');work=freeze_original_before_production(data)[0][0]
    variants=[replace(work,legacy=replace(work.legacy,semantic_roles=('TARGET','CONDITIONER'))),
        replace(work,legacy=replace(work.legacy,condition_order=('Y','X'))),
        replace(work,legacy=replace(work.legacy,measure_kind='GOVERNED_WEIGHTED')),
        replace(work,legacy=replace(work.legacy,risk_identity='OTHER')),
        replace(work,original=replace(work.original,empirical_universe_ref=_ref('EmpiricalUniverse','OTHER'))),
        replace(work,original=replace(work.original,native_item_refs=tuple(reversed(work.original.native_item_refs)))),
        replace(work,original=replace(work.original,original_item_scope_ref=_ref('SOURCEFREE_ORIGINAL_ITEM_SCOPE','OTHER')))]
    assert len({w.key for w in (work,*variants)})==len(variants)+1


def test_no_false_productive_pass_for_all_held_original_expectation():
    data=sourcefree_original_inputs('V2K-HELD');held=freeze_original_before_production(data)[0][-1]
    with pytest.raises(K.IdentityError,match='NO_RUNNABLE_ORIGINAL_WORK'):
        K.FrozenOriginalExpected.from_records((held,),input_origin=K.ORIGIN)


def test_original_item_order_cannot_claim_other_actual_query(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    work=records[0]
    other=replace(work,original=replace(work.original,native_item_refs=tuple(reversed(work.original.native_item_refs))))
    changed=tuple(other if r is work else r for r in records)
    frozen=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN)
    selected=tuple(replace(p,original_work_keys=tuple(other.key if key==work.key else key for key in p.original_work_keys)) for p in plans)
    with pytest.raises(K.IdentityError,match='ORIGINAL_ORDERED_ITEM_QUERY_BINDING_MISMATCH'):
        K.run_sourcefree(expected=frozen,selected_scopes=selected)
    assert calls==[[],[]]


@pytest.mark.parametrize('mutation', ['missing_namespace','unknown_original_field','unknown_top_field'])
def test_incomplete_or_unknown_original_schema_cannot_be_laundered_by_digest(mutation):
    data=sourcefree_original_inputs('V2K-SCHEMA');_,expected=freeze_original_before_production(data)
    raw=json.loads(expected.payload_json)
    if mutation=='missing_namespace':
        raw['records'][0]['original'].pop('respondent_namespace')
    elif mutation=='unknown_original_field':
        raw['records'][0]['original']['caller_permission']='REAL_EXECUTION'
    else:
        raw['self_issued_source_permission']=True
    forged=replace(expected,payload_json=json.dumps(raw),payload_sha256=K.semantic_hash(raw))
    with pytest.raises(K.IdentityError,match='ORIGINAL_RECORD_FIELDS_MISSING_OR_UNKNOWN'):
        forged.checked()


def test_old_V2_schema_cannot_be_silently_rebranded_or_made_mutable():
    data=sourcefree_original_inputs('V2K-VERSION');work=freeze_original_before_production(data)[0][0]
    with pytest.raises(K.IdentityError,match='LEGACY_SCHEMA_MUST_REMAIN_PUBLISHED_V2'):
        replace(work,legacy=replace(work.legacy,schema_version=K.SCHEMA))
    with pytest.raises(K.IdentityError,match='IMMUTABLE_LEGACY_ROLE_AND_CONDITION_TUPLES_REQUIRED'):
        replace(work,legacy=replace(work.legacy,semantic_roles=['CONDITIONER','TARGET']))


def test_distinct_original_language_cannot_double_count_same_actual_owner_unit(tmp_path):
    records,expected,plans,calls=successor_fixture(tmp_path)
    originals=records[:4]
    translations=tuple(replace(w,original=replace(w.original,language='SOURCEFREE-LANGUAGE-B')) for w in originals)
    frozen=K.FrozenOriginalExpected.from_records((*originals,*translations),input_origin=K.ORIGIN)
    duplicate_owner_plan=replace(plans[0],original_work_keys=tuple(w.key for w in translations if w.legacy.is_runnable))
    with pytest.raises(K.IdentityError,match='ORIGINAL_MULTI_IDENTITY_TO_ONE_OWNER_UNIT_NOT_GOVERNED'):
        K.run_sourcefree(expected=frozen,selected_scopes=(plans[0],duplicate_owner_plan))
    assert calls==[[],[]]
