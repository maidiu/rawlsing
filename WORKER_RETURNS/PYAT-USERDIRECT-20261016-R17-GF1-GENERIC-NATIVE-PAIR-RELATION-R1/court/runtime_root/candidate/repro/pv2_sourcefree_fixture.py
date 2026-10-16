"""R10 PV2 sourcefree original-scope fixture.

Two synthetic namespaces x four original-scope slots, built on the pinned
existing owner factories.  Every original identity label is set to the value
the independently precommitted register declares, so a coherent relabel is
detectable.  Nothing here issues original authority.
"""
from __future__ import annotations

import json
from collections.abc import Mapping
from dataclasses import fields, is_dataclass, replace

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

import pv2_original_scope_register as PV2

NAMESPACES = tuple(o.respondent_namespace for o in
                   PV2.author_sourcefree_original_scope_register().obligations
                   if o.slot == 'PAIR')


def _rebind_all(old, universe, respondents):
    old_u = old.universes[0]
    objects = {old_u.ref: universe}
    refs = {old_u.ref: universe.ref}
    refs.update({a.ref: b.ref for a, b in zip(old.respondents, respondents)})

    def rebind(value):
        if isinstance(value, ExactRef):
            return refs.get(value, value)
        if isinstance(value, CanonicalSemanticObject):
            if value.ref in objects:
                return objects[value.ref]
            return type(value)(
                typed_state=value.typed_state,
                authority_snapshot_refs=value.authority_snapshot_refs,
                dependency_refs=rebind(value.dependency_refs),
                producer_replay_locator_or_reference_root=rebind(
                    value.producer_replay_locator_or_reference_root),
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
            return replace(value, **{
                f.name: rebind(getattr(value, f.name)) for f in fields(value) if f.init})
        return value

    return rebind(old)


def sourcefree_original_inputs(namespace: str, form: str = 'F1') -> dict:
    fx = physical_fixture()
    old = fx['projection']
    old_u = old.universes[0]
    universe = type(old_u)(
        typed_state=old_u.typed_state,
        authority_snapshot_refs=old_u.authority_snapshot_refs,
        dependency_refs=old_u.dependency_refs,
        producer_replay_locator_or_reference_root=old_u.producer_replay_locator_or_reference_root,
        **{**dict(old_u.semantic_fields), 'respondent_namespace': namespace,
           'instrument_release': f'INST-{namespace}/{form}'})
    respondents = tuple(replace(r, empirical_universe_ref=universe.ref) for r in old.respondents)
    projection = _rebind_all(old, universe, respondents)
    assert projection.universes[0].respondent_namespace == namespace
    stub = dict(universe=universe,
                respondents={r.respondent_key: r for r in projection.respondents},
                qrefs=fx['qrefs'], risk_refs={'R': fx['risk']},
                source_auth=projection.authority_snapshots[0])
    qauth, dauth = fx['qauth'], fx['dauth']
    all_p = _branch_predicate(stub, qauth, tag='pv2-actual-all')
    x1 = _predicate(stub, qauth, _response_leaf(stub, qauth, 'X', 1), tag='pv2-actual-x1')
    query = _query(stub, qauth, all_p, ('X', 'Y'), measure='RAW', tag='pv2-actual-xy')
    reverse_query = _query(stub, qauth, all_p, ('Y', 'X'), measure='RAW', tag='pv2-actual-yx')
    grammar = _grammar(
        operation=dauth.governed_operations[0],
        atoms=[_atom('ALL', all_p, 'BRANCH'), _atom('X1', x1, 'RESPONSE')],
        templates=[_qt('XY', query), _qt('YX', reverse_query)],
        rules=[_rule('pv2-actual-rule', 'PAIR_RESPONSE_COTRAVEL', 'SINGLE_ATOM',
                     atom_ids=('X1',), baseline_atom_id='ALL', query_template_id='XY',
                     validation={'kind': 'DISTRIBUTION_DIFFERS_FROM_BASELINE'})])
    discovery = _discovery_authority(stub, grammar, dauth, tag='pv2-actual-discovery')
    catalog = RuntimeObjectCatalog(
        authorities=(*projection.authority_snapshots, qauth, dauth),
        predicates=(all_p, x1), queries=(query, reverse_query),
        discovery_authorities=(discovery,))
    rows = []
    for kind in ('PAIR', 'DISCOVERY'):
        row = dict(source='PV2-ACTUAL-SCOPE-SOURCEFREE', wave='W1', item='X', form=form,
                   slot=kind,
                   semantic_op_class='PAIR_RESPONSE_COTRAVEL' if kind == 'PAIR' else 'BOUNDED_DISCOVERY',
                   semantic_roles=['CONDITIONER', 'TARGET'] if kind == 'PAIR' else ['BASE'],
                   target='XY', condition_order=['X', 'Y'] if kind == 'PAIR' else [],
                   measure_kind='RAW', source_identity=fx['stream'].source_sha256,
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
            inventory.append(dict(
                respondent_ref=row_respondents[cell.row_ordinal].as_dict(),
                item_ref=fx['qrefs'][cell.variable_name].as_dict(),
                raw_response_value=raw_physical_value_witness(cell.raw_value),
                configuration=dict(occurrence.multiplicity_order_rank_fields),
                response_state='SUBSTANTIVE_RESPONSE'))
    expected = P.FrozenExpected.from_documentary_payload(dict(
        schema=P.V.ACCEPTED_EXPECTED_SCHEMA, expected_derived_from='EXTERNAL_FROZEN',
        declarations=rows, source_inventory=inventory))
    reverse_query = reverse_query
    catalog = RuntimeObjectCatalog(
        authorities=catalog.authorities, predicates=catalog.predicates,
        queries=(query, reverse_query), discovery_authorities=catalog.discovery_authorities)
    b_row = dict(rows[0], item='Y', slot='B', target='YX', condition_order=['Y', 'X'],
                 query_ref=reverse_query.ref.as_dict())
    rows.insert(1, b_row)
    held = dict(rows[0], item='O', slot='ORDERED',
                semantic_op_class='NONSCALAR_TOPOLOGY_PRESERVATION',
                semantic_roles=['BASE'], target='O', condition_order=[],
                topology_identity='ORDERED_SEQUENCE', state='HELD',
                hold_reason='ORDERED_OWNER_NOT_ISSUED')
    held.pop('query_ref')
    held.pop('predicate_ref')
    rows.append(held)
    expected = P.FrozenExpected.from_documentary_payload(dict(
        schema=P.V.ACCEPTED_EXPECTED_SCHEMA, expected_derived_from='EXTERNAL_FROZEN',
        declarations=rows, source_inventory=inventory))
    declarations = [C.V2ExpectedWorkDeclaration(**{
        k: (ExactRef(**v) if k in ('query_ref', 'predicate_ref', 'discovery_authority_ref') and v
            else tuple(v) if k in ('semantic_roles', 'condition_order') else v)
        for k, v in row.items()}) for row in rows]
    bindings = C.v2_bind_semantic_to_dispatch(
        declarations=declarations,
        projection_fields={f.name: getattr(projection, f.name) for f in fields(projection)},
        runtime_catalog=catalog)
    return dict(fx=fx, projection=projection, universe=universe, catalog=catalog,
                all_p=all_p, query=query, reverse_query=reverse_query, discovery=discovery,
                expected=expected, declarations=declarations, bindings=bindings,
                respondent_refs={r.respondent_key: r.ref for r in projection.respondents},
                item_refs=dict(fx['qrefs']))


def freeze_original_before_production(inputs: dict, register: PV2.PrecommittedOriginalRegister):
    """Author original identities against the precommitted register's labels."""
    projection, universe = inputs['projection'], inputs['universe']
    records = []
    for declaration in inputs['declarations']:
        obligation = register.obligation_for(universe.respondent_namespace, declaration.slot)
        order = tuple(declaration.condition_order) if declaration.query_ref else ('X', 'Y')
        if not declaration.is_runnable and declaration.item in inputs['fx']['qrefs']:
            order = (declaration.item,)
        if not order:
            order = ('X', 'Y')
        original = K.OriginalIdentity(
            source_release_ref=ExactRef(
                'SOURCE_ARTIFACT', projection.source_artifact_id,
                projection.expected_source_sha256),
            empirical_universe_ref=universe.ref,
            native_item_refs=tuple(inputs['fx']['qrefs'][item] for item in order),
            respondent_namespace=universe.respondent_namespace,
            respondent_unit=obligation.respondent_unit,
            form=declaration.form, language=obligation.language,
            instrument_release=universe.instrument_release,
            administered_occurrence=obligation.administered_occurrence,
            option_scope=obligation.option_scope,
            routing_refs=tuple(r.ref for r in projection.routing
                               if exact_ref(r.question_or_target_ref) in
                               {inputs['fx']['qrefs'][item] for item in order}),
            original_item_scope_ref=_ref(
                'PV2_ORIGINAL_ITEM_SCOPE', f'pv2-items-{declaration.slot}'))
        records.append(K.OriginalExpectedWork(
            original, declaration,
            obligation.original_operation_scope_ref,
            obligation.original_U_ref, obligation.independent_E_ref,
            obligation.independent_custody_ref))
    return tuple(records)


def prepare_owner_scope(root, inputs: dict, records: tuple, namespace: str):
    """Only called AFTER the original successor expectation was frozen."""
    production = execute_route_b_production(
        source=inputs['fx']['stream'], projection=inputs['projection'],
        runtime_catalog=inputs['catalog'],
        i03_requests=[dict(query_ref=q.ref, predicate_ref=inputs['all_p'].ref)
                      for q in (inputs['query'], inputs['reverse_query'])],
        discovery_authority_ref=inputs['discovery'].ref)
    executor = production.repository_binding.executor
    facts = {f.ref.key: f for outcome in production.i03_results for f in outcome.facts}
    discoveries = {r.ref.key: production.i05_result for r in production.i05_result.receipts}
    calls = []

    def execute(unit):
        calls.append(unit.unit_ref.key)
        if unit.job_kind == 'DISCOVERY':
            outcome = executor.execute_i05(discovery_authority_ref=unit.job_ref)
            discoveries.update({r.ref.key: outcome for r in outcome.receipts})
            refs = tuple(r.ref for r in outcome.receipts)
        else:
            outcome = executor.execute_i03(query_ref=unit.job_ref,
                                           predicate_ref=inputs['all_p'].ref)
            facts.update({f.ref.key: f for f in outcome.facts})
            refs = tuple(f.ref for f in outcome.facts)
        return ExecutionOutcome(result_refs=refs,
                                provenance_refs=(unit.job_ref, *unit.semantic_input_refs))

    manifest = BatchManifest(tuple(
        BatchUnitSpec(job_kind='QUERY' if b.dispatch_predicate_ref else 'DISCOVERY',
                      job_ref=b.dispatch_job_ref,
                      release_refs=(production.c11_release.release_ref,),
                      semantic_input_refs=tuple(
                          r for r in (b.dispatch_predicate_ref, b.dispatch_authority_ref) if r))
        for b in inputs['bindings']))
    session = G.open_session(
        manifest=manifest, repository=executor.repository, root=root,
        source_sha256=inputs['fx']['stream'].source_sha256,
        executors={'QUERY': ExecutorBinding(inputs['fx']['qauth'].ref, execute),
                   'DISCOVERY': ExecutorBinding(inputs['fx']['dauth'].ref, execute)})
    kwargs = dict(expected=inputs['expected'], session=session,
                  runtime_catalog=inputs['catalog'],
                  resolve_fact=lambda r: facts[r.key],
                  resolve_discovery=lambda r: discoveries[r.key],
                  producer_permission_ceiling=('SOURCE_FREE_DEV',))
    return (K.OwnerScopePlan(tuple(r.key for r in records if r.legacy.is_runnable), kwargs),
            calls, dict(source_sha256=inputs['fx']['stream'].source_sha256,
                        respondent_namespace=namespace,
                        respondent_refs=dict(inputs['respondent_refs'])))


def pv2_sourcefree_fixture(root):
    """Freeze the complete original scope across ALL namespaces before any owner."""
    register = PV2.author_sourcefree_original_scope_register()
    inputs = [sourcefree_original_inputs(ns) for ns in NAMESPACES]
    per_scope = [freeze_original_before_production(data, register) for data in inputs]
    records = tuple(r for group in per_scope for r in group)
    expected = K.FrozenOriginalExpected.from_records(records, input_origin=K.ORIGIN)
    prepared = [prepare_owner_scope(root / str(i), data, group, ns)
                for i, (data, group, ns) in enumerate(zip(inputs, per_scope, NAMESPACES))]
    return dict(register=register, records=records, expected=expected,
                plans=tuple(p for p, _calls, _meta in prepared),
                calls=[calls for _p, calls, _meta in prepared],
                meta=[dict(respondent_namespace=m['respondent_namespace'],
                           respondent_refs=m['respondent_refs'])
                      for _p, _calls, m in prepared],
                inputs=inputs)
