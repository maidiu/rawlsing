"""Independent TEST_ONLY court. Never imports HQ295 fixture/oracle builders."""
from collections import Counter
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace
from pathlib import Path
import hashlib
import json
import os
import pytest
from rawlsing_next import pre553_original_identity_v2k_successor_candidate as K
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.pre553_empirical_objects import ExactRef, CanonicalSemanticObject, exact_ref
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, ExecutorBinding, ExecutionOutcome
from rawlsing_next.pre553_route_b_production import execute_route_b_production
from rawlsing_next.pre553_source_backed_c11_facade import raw_physical_value_witness
from rawlsing_next.tests.test_pre553_route_b_production import _fixture
from rawlsing_next.tests.test_pre553_empirical_query import _ref, _branch_predicate, _predicate, _response_leaf, _query
from rawlsing_next.tests.test_pre553_discovery_exact import _grammar, _atom, _qt, _rule, _discovery_authority

RETURN = Path(os.environ['PV_RETURN'])
ORACLE = json.loads((RETURN/'01_FROZEN_ORIGINAL_IDENTITY_ORACLES.json').read_text())
assert hashlib.sha256((RETURN/'01_FROZEN_ORIGINAL_IDENTITY_ORACLES.json').read_bytes()).hexdigest() == '1d551e0776e01e32a9c180f55ed2913a527f9e91a6c76278c8e923497304c5eb'


def audit(name, **values):
    with (RETURN/'repro/independent_observations.jsonl').open('a') as f:
        f.write(json.dumps(dict(case=name, **values), sort_keys=True)+'\n')


def inputs(namespace):
    # Reuse only unchanged low-level owner's typed physical scaffolding.
    # Independent cells, operations, expected roster, and arithmetic come from ORACLE.
    fx = _fixture(); old = fx['projection']; u = old.universes[0]
    universe = type(u)(typed_state=u.typed_state, authority_snapshot_refs=u.authority_snapshot_refs,
        dependency_refs=u.dependency_refs, producer_replay_locator_or_reference_root=u.producer_replay_locator_or_reference_root,
        **{**dict(u.semantic_fields), 'respondent_namespace':namespace})
    refs = {u.ref:universe.ref}
    respondents = tuple(replace(r,empirical_universe_ref=universe.ref) for r in old.respondents)
    refs.update({a.ref:b.ref for a,b in zip(old.respondents,respondents)})
    def rebind(v):
        if isinstance(v,ExactRef): return refs.get(v,v)
        if isinstance(v,CanonicalSemanticObject):
            if v.ref == u.ref: return universe
            return type(v)(typed_state=v.typed_state, authority_snapshot_refs=v.authority_snapshot_refs,
                dependency_refs=rebind(v.dependency_refs), producer_replay_locator_or_reference_root=rebind(v.producer_replay_locator_or_reference_root),
                **rebind(dict(v.semantic_fields)))
        if isinstance(v,Mapping):
            if set(v)=={'kind','object_id','content_hash'}: return rebind(ExactRef(**v)).as_dict()
            return {k:rebind(x) for k,x in v.items()}
        if isinstance(v,tuple): return tuple(rebind(x) for x in v)
        if isinstance(v,list): return [rebind(x) for x in v]
        if is_dataclass(v): return replace(v,**{f.name:rebind(getattr(v,f.name)) for f in fields(v) if f.init})
        return v
    projection = rebind(old)
    # The physical scaffolding has the same routing, but our response table is asymmetric.
    cells = tuple(replace(c,raw_value=ORACLE['rows'][c.row_ordinal-1][c.variable_name])
        if c.variable_name in ('X','Y') else c for c in fx['stream'].cell_iter_factory())
    source_hash = hashlib.sha256(json.dumps([(c.row_ordinal,c.variable_name,c.raw_value) for c in cells],sort_keys=True).encode()).hexdigest()
    stream = replace(fx['stream'], source_sha256=source_hash,cell_iter_factory=lambda:iter(cells))
    projection = replace(projection,expected_source_sha256=source_hash,
        source_snapshot_retention_ref=replace(projection.source_snapshot_retention_ref,content_hash=source_hash))
    stub = dict(universe=universe, respondents={r.respondent_key:r for r in respondents},qrefs=fx['qrefs'],risk_refs={'R':fx['risk']},source_auth=projection.authority_snapshots[0])
    qa,da = fx['qauth'],fx['dauth']
    all_p = _branch_predicate(stub,qa,tag='pv-independent-all')
    y1 = _predicate(stub,qa,_response_leaf(stub,qa,'Y',1),tag='pv-independent-y1')
    queries = {slot:_query(stub,qa,all_p,tuple(order),measure='RAW',tag='pv-independent-'+slot)
        for slot,order in [('PAIR',['X','Y']),('B',['Y','X'])]}
    grammar = _grammar(operation=da.governed_operations[0],atoms=[_atom('ALL',all_p,'BRANCH'),_atom('Y1',y1,'RESPONSE')],
        templates=[_qt('XY',queries['PAIR'])],rules=[_rule('pv-rule','PAIR_RESPONSE_COTRAVEL','SINGLE_ATOM',
        atom_ids=('Y1',),baseline_atom_id='ALL',query_template_id='XY',validation={'kind':'DISTRIBUTION_DIFFERS_FROM_BASELINE'})])
    discovery = _discovery_authority(stub,grammar,da,tag='pv-independent-J')
    catalog = RuntimeObjectCatalog(authorities=(*projection.authority_snapshots,qa,da),predicates=(all_p,y1),queries=tuple(queries.values()),discovery_authorities=(discovery,))
    rows=[]; records=[]
    for op in ORACLE['operations']:
        slot=op['slot']; order=op['order']; held=op['state']=='HELD'; is_j=slot=='DISCOVERY'
        row=dict(source='PV-INDEPENDENT-SYNTHETIC',wave='W1',item=order[0],form=ORACLE['form'],slot=slot,
            semantic_op_class='NONSCALAR_TOPOLOGY_PRESERVATION' if held else 'BOUNDED_DISCOVERY' if is_j else 'PAIR_RESPONSE_COTRAVEL',
            semantic_roles=tuple(op['roles']),target=''.join(order),condition_order=() if held or is_j else tuple(order),measure_kind='RAW',
            source_identity=source_hash,authority_ref=(da if is_j else qa).authority_ref.key,risk_identity=fx['risk'].key,
            topology_identity='ORDERED_SEQUENCE' if held else 'SCALAR_2X2_JOINT',required_consumer=P.CONSUMER,state=op['state'])
        if held: row['hold_reason']=op['hold_reason']
        elif is_j: row['discovery_authority_ref']=discovery.ref
        else: row.update(query_ref=queries[slot].ref,predicate_ref=all_p.ref)
        decl=C.V2ExpectedWorkDeclaration(**row); rows.append({k:v for k,v in K.legacy_preimage(decl).items() if v is not None})
        identity=K.OriginalIdentity(ExactRef('SOURCE_ARTIFACT',projection.source_artifact_id,source_hash),universe.ref,
            tuple(fx['qrefs'][q] for q in order),namespace,'TEST_ONLY_ADULT','F1','PV-LANGUAGE','INST-m01',
            'PV-FIRST-ADMINISTRATION',('AB','BA') if held else ('0','1'),
            tuple(r.ref for r in projection.routing if exact_ref(r.question_or_target_ref) in {fx['qrefs'][q] for q in order}),
            _ref('TEST_ONLY_ORIGINAL_SCOPE',namespace+'-'+slot))
        records.append(K.OriginalExpectedWork(identity,decl,_ref('TEST_ONLY_OPERATION',slot),
            _ref('TEST_ONLY_U','pv-independent-U'),_ref('TEST_ONLY_E','pv-independent-E'),_ref('TEST_ONLY_CUSTODIAN','pv-independent-custody')))
    rowrefs={b.row_ordinal:b.respondent_ref for b in projection.row_bindings}
    rules={r.slot.name:r for r in projection.response_slots}
    inventory=[dict(respondent_ref=rowrefs[c.row_ordinal].as_dict(),item_ref=fx['qrefs'][c.variable_name].as_dict(),
        raw_response_value=raw_physical_value_witness(c.raw_value),configuration=dict(occ.multiplicity_order_rank_fields),response_state='SUBSTANTIVE_RESPONSE')
        for c in cells if c.variable_name in rules for occ in rules[c.variable_name].values[0].occurrences]
    expected=P.FrozenExpected.from_documentary_payload(dict(schema=P.V.ACCEPTED_EXPECTED_SCHEMA,expected_derived_from='EXTERNAL_FROZEN',declarations=rows,source_inventory=inventory))
    return dict(fx=fx,stream=stream,projection=projection,catalog=catalog,queries=queries,discovery=discovery,predicate=all_p,records=tuple(records),expected=expected)


def prepare(root,data,records):
    production=execute_route_b_production(source=data['stream'],projection=data['projection'],runtime_catalog=data['catalog'],
        i03_requests=[dict(query_ref=q.ref,predicate_ref=data['predicate'].ref) for q in data['queries'].values()],discovery_authority_ref=data['discovery'].ref)
    executor=production.repository_binding.executor
    facts={f.ref.key:f for result in production.i03_results for f in result.facts}
    discoveries={r.ref.key:production.i05_result for r in production.i05_result.receipts}; calls=[]
    def execute(unit):
        calls.append(unit.unit_ref.key)
        if unit.job_kind=='DISCOVERY':
            result=executor.execute_i05(discovery_authority_ref=unit.job_ref)
            discoveries.update({r.ref.key:result for r in result.receipts});refs=tuple(r.ref for r in result.receipts)
        else:
            result=executor.execute_i03(query_ref=unit.job_ref,predicate_ref=data['predicate'].ref)
            facts.update({f.ref.key:f for f in result.facts});refs=tuple(f.ref for f in result.facts)
        return ExecutionOutcome(result_refs=refs,provenance_refs=(unit.job_ref,*unit.semantic_input_refs))
    units=tuple(BatchUnitSpec(job_kind='DISCOVERY' if w.legacy.discovery_authority_ref else 'QUERY',
        job_ref=w.legacy.discovery_authority_ref or w.legacy.query_ref,release_refs=(production.c11_release.release_ref,),
        semantic_input_refs=tuple(r for r in (w.legacy.predicate_ref,(data['fx']['dauth'] if w.legacy.discovery_authority_ref else data['fx']['qauth']).ref) if r))
        for w in records if w.legacy.is_runnable)
    session=G.open_session(manifest=BatchManifest(units),repository=executor.repository,root=root,source_sha256=data['stream'].source_sha256,
        executors={'QUERY':ExecutorBinding(data['fx']['qauth'].ref,execute),'DISCOVERY':ExecutorBinding(data['fx']['dauth'].ref,execute)})
    kwargs=dict(expected=data['expected'],session=session,runtime_catalog=data['catalog'],resolve_fact=lambda r:facts[r.key],
        resolve_discovery=lambda r:discoveries[r.key],producer_permission_ceiling=('SOURCE_FREE_DEV',))
    return K.OwnerScopePlan(tuple(w.key for w in records if w.legacy.is_runnable),kwargs),calls


def independent_preimage(w):
    """Reviewer spells the identity schema; no candidate serializer/hash used."""
    o,d=w.original,w.legacy
    ref=lambda r:dict(kind=r.kind,object_id=r.object_id,content_hash=r.content_hash)
    original={name:getattr(o,name) for name in ('respondent_namespace','respondent_unit','form','language','instrument_release','administered_occurrence')}
    original.update(source_release_ref=ref(o.source_release_ref),empirical_universe_ref=ref(o.empirical_universe_ref),
        native_item_refs=[ref(r) for r in o.native_item_refs],option_scope=list(o.option_scope),
        routing_refs=[ref(r) for r in sorted(o.routing_refs,key=lambda r:r.key)],original_item_scope_ref=ref(o.original_item_scope_ref))
    operation={name:getattr(d,name) for name in ('source','wave','item','slot','semantic_op_class','target','measure_kind','multiplicity','authority_ref','risk_identity','topology_identity')}
    operation.update(semantic_roles=list(d.semantic_roles),condition_order=list(d.condition_order))
    operation.update({name:ref(getattr(d,name)) if getattr(d,name) is not None else None for name in ('query_ref','predicate_ref','discovery_authority_ref')})
    return dict(schema='HQ295_ORIGINAL_EXPECTED_WORK_V2K_CANDIDATE@1.0.0',kind='ORIGINAL_EXPECTED_WORK',original=original,operation=operation,
        **{name:ref(getattr(w,name)) for name in ('original_operation_scope_ref','original_U_ref','independent_E_ref','independent_custody_ref')})


def independent_key(w):
    return hashlib.sha256(json.dumps(independent_preimage(w),sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()).hexdigest()


def external_check(works,frozen):
    assert Counter(independent_key(w) for w in works)==Counter(independent_key(w) for w in frozen),'INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'


def court(root):
    data=[inputs(ns) for ns in ORACLE['scopes']]
    records=tuple(w for d in data for w in d['records'])
    assert Counter((w.original.respondent_namespace,w.legacy.slot) for w in records)==Counter(map(tuple,ORACLE['expected_multiset']))
    assert all(independent_key(w)==w.key and independent_preimage(w)==w.identity_preimage() for w in records)
    independent = [{'key':independent_key(w),'preimage':independent_preimage(w),'state':w.legacy.state,'hold_reason':w.legacy.hold_reason} for w in records]
    (root/'reviewer_reconstructed_before_production.json').write_text(json.dumps(independent,indent=2))
    expected=K.FrozenOriginalExpected.from_records(records,input_origin=K.ORIGIN)
    # Persist exact generated preimages BEFORE invoking any candidate/owner producer.
    (root/'frozen_before_production.json').write_text(expected.payload_json)
    p=[prepare(root/str(i),d,d['records']) for i,d in enumerate(data)]
    return records,expected,tuple(x[0] for x in p),[x[1] for x in p]


def remap(plans,old,new):
    return tuple(replace(p,original_work_keys=tuple(new.key if k==old.key else k for k in p.original_work_keys)) for p in plans)


def test_independent_positive_denominators_and_replay(tmp_path):
    records,expected,plans,calls=court(tmp_path)
    report=K.run_sourcefree(expected=expected,selected_scopes=plans)
    assert report['ok'] and len(report['links'])==6 and len(report['nonrunnable'])==2
    assert [len(c) for c in calls]==[3,3]
    assert len({l['legacy_expected_work_key'] for l in report['links']})==3
    assert len({json.dumps(l['consumer_ref'],sort_keys=True) for l in report['links']})==6
    for link in report['links']:
        slot=link['original_identity']['operation']['slot']
        if slot not in ORACLE['expected_consumer_counts']: continue
        mat=link['consumer_material']
        profile={str(r['condition_state']):dict(denominator=r['condition_denominator_support'],targets={str(t['target_state']):t['joint_support_count'] for t in r['target_counts']}) for r in mat['conditional_count_profile']}
        assert profile==ORACLE['expected_consumer_counts'][slot]
        assert mat['roles']['CONDITIONER']['ref']==link['original_identity']['original']['native_item_refs'][0]
        assert mat['roles']['TARGET']['ref']==link['original_identity']['original']['native_item_refs'][1]
        assert mat['producer_fact_ref']==link['producer_result_ref']
    prior={l['original_expected_work_key']:ExactRef(**l['consumer_ref']) for l in report['links']}
    replay=K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs=prior)
    assert replay['links']==report['links'] and [len(c) for c in calls]==[3,3]
    (RETURN/'repro/independent_positive.json').write_text(json.dumps(report,indent=2))
    (RETURN/'repro/exact_frozen_before_production.json').write_text(expected.payload_json)
    (RETURN/'repro/reviewer_reconstructed_before_production.json').write_bytes((tmp_path/'reviewer_reconstructed_before_production.json').read_bytes())
    audit('positive',ok=report['ok'],durable_calls=[len(c) for c in calls],links=6,held=2,denominators='INDEPENDENT_ARITHMETIC_MATCH',replay='EXACT_ZERO_ADDITIONAL_CALLS')


@pytest.mark.parametrize('slot',['B','DISCOVERY'])
def test_independent_omission(tmp_path,slot):
    records,expected,plans,calls=court(tmp_path)
    omitted={w.key for w in records if w.legacy.slot==slot}
    plans=tuple(replace(p,original_work_keys=tuple(k for k in p.original_work_keys if k not in omitted)) for p in plans)
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN'): K.run_sourcefree(expected=expected,selected_scopes=plans)
    assert calls==[[],[]]


def test_same_count_foreign_substitution(tmp_path):
    _,expected,plans,calls=court(tmp_path)
    p=replace(plans[1],original_work_keys=('f'*64,*plans[1].original_work_keys[1:]))
    with pytest.raises(K.IdentityError,match='ORIGINAL_EXPECTED_SELECTED_ANTI_JOIN'): K.run_sourcefree(expected=expected,selected_scopes=(plans[0],p))
    assert calls==[[],[]]


@pytest.mark.parametrize('field,value',[('respondent_namespace','FOREIGN'),('native_item_refs',None),('routing_refs',None)])
def test_wrong_c11_binding(tmp_path,field,value):
    records,expected,plans,calls=court(tmp_path);old=records[0]
    if field=='native_item_refs': value=tuple(reversed(old.original.native_item_refs))
    if field=='routing_refs': value=(_ref('ROUTING','foreign'),)
    new=replace(old,original=replace(old.original,**{field:value}))
    changed=tuple(new if w is old else w for w in records)
    with pytest.raises(AssertionError,match='INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'):external_check(changed,records)
    frozen=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN)
    with pytest.raises(K.IdentityError):K.run_sourcefree(expected=frozen,selected_scopes=remap(plans,old,new))
    assert calls==[[],[]]


def test_changed_preimage_and_foreign_query(tmp_path):
    records,expected,plans,calls=court(tmp_path)
    raw=json.loads(expected.payload_json);raw['records'][0]['original']['language']='FOREIGN'
    with pytest.raises(K.IdentityError,match='DIGEST_MISMATCH'): replace(expected,payload_json=json.dumps(raw)).checked()
    with pytest.raises(K.IdentityError,match='KEY_PREIMAGE_MISMATCH'): replace(expected,payload_json=json.dumps(raw),payload_sha256=K.semantic_hash(raw)).checked()
    old=records[0];new=replace(old,legacy=replace(old.legacy,query_ref=_ref('QUERY','foreign')))
    frozen=K.FrozenOriginalExpected.from_records(tuple(new if w is old else w for w in records),input_origin=K.ORIGIN)
    with pytest.raises(K.IdentityError):K.run_sourcefree(expected=frozen,selected_scopes=remap(plans,old,new))
    assert calls==[[],[]]


@pytest.mark.parametrize('field',['original_U_ref','independent_E_ref','independent_custody_ref','original_operation_scope_ref'])
def test_foreign_issuer_is_not_authenticated(tmp_path,field):
    records,expected,plans,calls=court(tmp_path);old=records[0]
    new=replace(old,**{field:_ref('FOREIGN_SELF_ISSUED',field)})
    changed=tuple(new if w is old else w for w in records)
    with pytest.raises(AssertionError,match='INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'):external_check(changed,records)
    report=K.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN),selected_scopes=remap(plans,old,new))
    assert report['ok'] and 'ORIGINAL_U_E_CUSTODY_NOT_AUTHENTICATED' in report['holds']
    audit('foreign_issuer_'+field,candidate_ok=report['ok'],external_oracle_rejected=True,holds=report['holds'])


def test_missing_all_held_rows_exposes_outer_gap(tmp_path):
    records,expected,plans,calls=court(tmp_path)
    reduced=tuple(w for w in records if w.legacy.is_runnable)
    with pytest.raises(AssertionError,match='INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'): external_check(reduced,records)
    report=K.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(reduced,input_origin=K.ORIGIN),selected_scopes=plans)
    assert report['ok'] and report['nonrunnable']==[]
    audit('missing_all_held',candidate_ok=True,external_oracle_rejected=True,held_returned=0)


def test_cherry_picked_A_only_exposes_outer_gap(tmp_path):
    records,expected,plans,calls=court(tmp_path);w=records[0];kw=dict(plans[0].p01_kwargs)
    doc=json.loads(kw['expected'].payload_json);doc['declarations']=[K.legacy_preimage(w.legacy)]
    kw['expected']=P.FrozenExpected.from_documentary_payload(doc);s=kw['session']
    unit=next(u for u in s.manifest.units if u.job_ref==w.legacy.query_ref)
    kw['session']=G.open_session(manifest=BatchManifest((unit,)),repository=s.repository,root=tmp_path/'picked',source_sha256=s.source_sha256,executors=s.executors)
    selected=(K.OwnerScopePlan((w.key,),kw),)
    with pytest.raises(K.IdentityError,match='ANTI_JOIN'):K.run_sourcefree(expected=expected,selected_scopes=selected)
    with pytest.raises(AssertionError,match='INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'):external_check((w,),records)
    local=K.run_sourcefree(expected=K.FrozenOriginalExpected.from_records((w,),input_origin=K.ORIGIN),selected_scopes=selected)
    assert local['ok'] and len(local['links'])==1
    audit('cherry_pick_A',candidate_local_ok=True,frozen_full_rejected=True)


@pytest.mark.parametrize('mutation',['wrong_role','wrong_direction','foreign_form','foreign_unit'])
def test_coherent_semantic_rekey(tmp_path,mutation):
    records,expected,plans,calls=court(tmp_path);old=records[0]
    if mutation=='wrong_role': new=replace(old,legacy=replace(old.legacy,semantic_roles=('TARGET','CONDITIONER')))
    elif mutation=='wrong_direction':new=replace(old,legacy=replace(old.legacy,condition_order=('Y','X')))
    elif mutation=='foreign_form':new=replace(old,original=replace(old.original,form='FOREIGN-FORM'),legacy=replace(old.legacy,form='FOREIGN-FORM'))
    else:new=replace(old,original=replace(old.original,respondent_unit='HOUSEHOLD'))
    changed=tuple(new if w is old else w for w in records)
    with pytest.raises(AssertionError,match='INDEPENDENT_ORIGINAL_MULTISET_MISMATCH'):external_check(changed,records)
    pp=list(remap(plans,old,new));kw=dict(pp[0].p01_kwargs);doc=json.loads(kw['expected'].payload_json)
    doc['declarations']=[K.legacy_preimage(new.legacy) if r['slot']=='PAIR' else r for r in doc['declarations']]
    kw['expected']=P.FrozenExpected.from_documentary_payload(doc);pp[0]=replace(pp[0],p01_kwargs=kw)
    try:
        report=K.run_sourcefree(expected=K.FrozenOriginalExpected.from_records(changed,input_origin=K.ORIGIN),selected_scopes=tuple(pp))
    except (ValueError,TypeError) as e:
        audit(mutation,candidate_rejected=True,diagnostic=str(e),calls=[len(c) for c in calls]);assert calls==[[],[]]
    else:
        assert report['ok'];audit(mutation,candidate_ok=True,external_oracle_rejected=True,holds=report['holds'])


def test_foreign_replay_ref_rejected(tmp_path):
    _,expected,plans,calls=court(tmp_path)
    report=K.run_sourcefree(expected=expected,selected_scopes=plans)
    prior={l['original_expected_work_key']:ExactRef(**l['consumer_ref']) for l in report['links']}
    prior[next(iter(prior))]=_ref('FOREIGN_CONSUMER','replay')
    with pytest.raises(ValueError):K.run_sourcefree(expected=expected,selected_scopes=plans,prior_consumer_refs=prior)
    assert [len(c) for c in calls]==[3,3]


def test_all_held_no_productive_pass():
    held=tuple(w for w in inputs(ORACLE['scopes'][0])['records'] if not w.legacy.is_runnable)
    with pytest.raises(K.IdentityError,match='NO_RUNNABLE'):K.FrozenOriginalExpected.from_records(held,input_origin=K.ORIGIN)


def test_original_namespace_and_form_key_discrimination():
    a=inputs(ORACLE['scopes'][0])['records'][0];b=inputs(ORACLE['scopes'][1])['records'][0]
    assert a.legacy.expected_work_key==b.legacy.expected_work_key and a.key!=b.key
    c=replace(a,original=replace(a.original,form='F2'),legacy=replace(a.legacy,form='F2'))
    assert c.key!=a.key
