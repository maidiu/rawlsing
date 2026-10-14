"""Actual source-free C11 scope variants, using pinned existing owner factories.

These fixtures construct synthetic scope inputs, never issue original authority.
No monkeypatching of owner code and no protected production edits.
"""
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace
import json
import pytest
from rawlsing_next.pre553_empirical_objects import CanonicalSemanticObject, ExactRef
from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding
from rawlsing_next.pre553_source_backed_c11_facade import raw_physical_value_witness
from rawlsing_next.pre553_route_b_production import execute_route_b_production
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.tests.test_pre553_route_b_production import _fixture as physical_fixture
from rawlsing_next.tests.test_pre553_empirical_query import _branch_predicate, _predicate, _response_leaf, _query
from rawlsing_next.tests.test_pre553_discovery_exact import _grammar, _atom, _qt, _rule, _discovery_authority


def actual_scope_fixture(root, namespace, form='F1'):
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
    declarations = [C.V2ExpectedWorkDeclaration(**{k: ExactRef(**v) if k in
        ('query_ref', 'predicate_ref', 'discovery_authority_ref') else tuple(v) if k in
        ('semantic_roles', 'condition_order') else v for k, v in row.items()}) for row in rows]
    bindings = C.v2_bind_semantic_to_dispatch(declarations=declarations,
        projection_fields={f.name: getattr(projection, f.name) for f in fields(projection)}, runtime_catalog=catalog)
    production = execute_route_b_production(source=fx['stream'], projection=projection,
        runtime_catalog=catalog, i03_requests=[dict(query_ref=query.ref, predicate_ref=all_p.ref)],
        discovery_authority_ref=discovery.ref)
    executor = production.repository_binding.executor
    facts = {f.ref.key: f for o in production.i03_results for f in o.facts}
    discoveries = {r.ref.key: production.i05_result for r in production.i05_result.receipts}
    calls = []
    def execute(unit):
        calls.append(unit.unit_ref.key)
        if unit.job_kind == 'DISCOVERY':
            outcome = executor.execute_i05(discovery_authority_ref=unit.job_ref)
            discoveries.update({r.ref.key: outcome for r in outcome.receipts})
            result_refs = tuple(r.ref for r in outcome.receipts)
        else:
            outcome = executor.execute_i03(query_ref=unit.job_ref, predicate_ref=all_p.ref)
            facts.update({f.ref.key: f for f in outcome.facts})
            result_refs = tuple(f.ref for f in outcome.facts)
        return ExecutionOutcome(result_refs=result_refs, provenance_refs=(unit.job_ref, *unit.semantic_input_refs))
    manifest = BatchManifest(tuple(BatchUnitSpec(job_kind='QUERY' if b.dispatch_predicate_ref else 'DISCOVERY',
        job_ref=b.dispatch_job_ref, release_refs=(production.c11_release.release_ref,),
        semantic_input_refs=tuple(r for r in (b.dispatch_predicate_ref, b.dispatch_authority_ref) if r)) for b in bindings))
    session = G.open_session(manifest=manifest, repository=executor.repository, root=root,
        source_sha256=fx['stream'].source_sha256,
        executors={'QUERY': ExecutorBinding(qauth.ref, execute), 'DISCOVERY': ExecutorBinding(dauth.ref, execute)})
    return dict(expected=expected, session=session, runtime_catalog=catalog, resolve_fact=lambda r: facts[r.key],
        resolve_discovery=lambda r: discoveries[r.key], producer_permission_ceiling=('SOURCE_FREE_DEV',)), calls, universe


def test_actual_c11_namespace_changes_owner_jobs_results_and_consumers_but_not_v2_keys(tmp_path):
    reports = []
    scopes = []
    for namespace in ('A04B-ACTUAL-NAMESPACE-A', 'A04B-ACTUAL-NAMESPACE-B'):
        kwargs, calls, universe = actual_scope_fixture(tmp_path / namespace, namespace)
        report = P.run_integrated(**kwargs)
        assert report['ok'] and len(calls) == 2 and len(report['consumer_products']) == 2
        assert len(report['source_inventory']) == 18
        reports.append(report); scopes.append((kwargs, universe))
    assert scopes[0][1].ref != scopes[1][1].ref
    assert scopes[0][0]['session'].manifest.manifest_ref != scopes[1][0]['session'].manifest.manifest_ref
    a, b = reports
    assert a['consumer_products'] != b['consumer_products']
    assert {p['expected_work_key'] for p in a['consumer_products']} == {p['expected_work_key'] for p in b['consumer_products']}
    assert {json.dumps(r['respondent_ref'], sort_keys=True) for r in a['source_inventory']}.isdisjoint(
        {json.dumps(r['respondent_ref'], sort_keys=True) for r in b['source_inventory']})
    (tmp_path/'actual_namespace_reports.json').write_text(json.dumps(reports, indent=2))


def test_actual_scoped_form_successor_has_distinct_expected_identity(tmp_path):
    results = []
    for form in ('F1', 'F2'):
        kwargs, calls, _ = actual_scope_fixture(tmp_path / form, 'A04B-FORM-NAMESPACE', form)
        report = P.run_integrated(**kwargs)
        assert report['ok'] and len(calls) == 2
        results.append(report)
    assert {p['expected_work_key'] for p in results[0]['consumer_products']}.isdisjoint(
        {p['expected_work_key'] for p in results[1]['consumer_products']})


def test_actual_foreign_namespace_expected_inventory_rejected_before_durable_calls(tmp_path):
    left, calls, _ = actual_scope_fixture(tmp_path / 'left', 'A04B-LEFT')
    right, _, _ = actual_scope_fixture(tmp_path / 'right', 'A04B-RIGHT')
    # Even when the V2 keys alias, actual independently frozen respondent refs
    # do not match the other namespace's C11 release.
    doc = json.loads(left['expected'].payload_json)
    doc['source_inventory'] = json.loads(right['expected'].payload_json)['source_inventory']
    left['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='ORIGINAL_RESPONDENT_ITEM_CONFIGURATION_MISMATCH'):
        P.run_integrated(**left)
    assert calls == []
