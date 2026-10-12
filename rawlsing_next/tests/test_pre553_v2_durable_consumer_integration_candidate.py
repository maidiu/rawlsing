"""P01 source-free integrated courts; no external source/custody grant."""
from copy import deepcopy
from dataclasses import replace
import json

import pytest
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next import pre553_original_workload_contract_v2_candidate as C
from rawlsing_next.pre553_batch_runner import BatchManifest, BatchUnitSpec, ExecutionOutcome, ExecutorBinding
from rawlsing_next.pre553_route_b_production import execute_route_b_production
from rawlsing_next.pre553_empirical_objects import ExactRef
from rawlsing_next.tests.test_pre553_original_workload_contract_v2_candidate import _v2_scope


def _fixture(root):
    s = _v2_scope('p01')
    from rawlsing_next.tests.test_pre553_discovery_exact import _grammar, _atom, _qt, _rule, _discovery_authority
    from rawlsing_next.pre553_carrier_execution import RuntimeObjectCatalog
    grammar = _grammar(operation=s['dauth'].governed_operations[0],
        atoms=[_atom('ALL', s['all_p'], 'BRANCH'), _atom('X1', s['fx']['x1'], 'RESPONSE')],
        templates=[_qt('XY', s['queries']['xy'])], rules=[_rule('p01-joint-rule',
        'PAIR_RESPONSE_COTRAVEL', 'SINGLE_ATOM', atom_ids=('X1',), baseline_atom_id='ALL',
        query_template_id='XY', validation={'kind': 'DISTRIBUTION_DIFFERS_FROM_BASELINE'})])
    stub = {'universe': s['projection'].universes[0], 'risk_refs': {'R': s['fx']['risk']}}
    discovery = _discovery_authority(stub, grammar, s['dauth'], tag='p01-joint')
    s['discovery_ref'] = discovery.ref
    old = s['catalog']
    s['catalog'] = RuntimeObjectCatalog(authorities=old.authorities, predicates=old.predicates,
        queries=old.queries, discovery_authorities=(discovery,))
    # Authored from original documentary item/operation inputs BEFORE production.
    # No observed facts, output keys or consumer material contribute to E.
    rows = []
    for item, slot, order in [('X', 'xy', ['X', 'Y']), ('Y', 'yx', ['Y', 'X'])]:
        rows.append(dict(source='P01-SYNTHETIC', wave='W1', item=item, form='F1', slot=slot,
            semantic_op_class='PAIR_RESPONSE_COTRAVEL', semantic_roles=['CONDITIONER', 'TARGET'],
            target='JOINT-'+slot, condition_order=order, measure_kind='RAW',
            source_identity=s['source_sha'], authority_ref=s['qauth'].authority_ref.key,
            risk_identity='COMMON-ELIGIBLE-RISK', topology_identity='SCALAR_2X2_JOINT',
            required_consumer=P.CONSUMER, state='RUNNABLE', hold_reason=None, multiplicity=1,
            query_ref=s['queries'][slot].ref.as_dict(), predicate_ref=s['all_p'].ref.as_dict()))
    rows.append(dict(source='P01-SYNTHETIC', wave='W1', item='D', form='F1', slot='discovery',
        semantic_op_class='BOUNDED_DISCOVERY', semantic_roles=['BASE'], target='JOINT-DISCOVERY',
        condition_order=[], measure_kind='RAW', source_identity=s['source_sha'],
        authority_ref=s['dauth'].authority_ref.key, risk_identity='COMMON-ELIGIBLE-RISK',
        topology_identity='SCALAR_2X2_JOINT', required_consumer=P.CONSUMER,
        state='RUNNABLE', hold_reason=None, multiplicity=1, discovery_authority_ref=discovery.ref.as_dict()))
    for item, state, reason in [('O', 'HELD', 'ORDERED_SEQUENCE_NOT_AUTHORIZED'),
                                ('R', 'HELD', 'REPEATED_EVENT_NOT_AUTHORIZED'),
                                ('V', 'DENIED', 'SOURCE_GAP'),
                                ('U', 'SOURCE_NONAPPLICABLE', 'NO_TARGET_IN_SLICE')]:
        rows.append(dict(source='P01-SYNTHETIC', wave='W1', item=item, form='F1', slot='S1',
            semantic_op_class='NONSCALAR_TOPOLOGY_PRESERVATION' if item in ('O','R') else 'UNARY_DISTRIBUTION',
            semantic_roles=['BASE'], target=item, condition_order=[], measure_kind='RAW',
            source_identity=s['source_sha'], authority_ref=s['qauth'].authority_ref.key,
            risk_identity='ORIGINAL-DOCUMENTARY', topology_identity='NATIVE-CONFIGURATION',
            required_consumer=P.CONSUMER, state=state, hold_reason=reason))
    from rawlsing_next.pre553_source_backed_c11_facade import raw_physical_value_witness
    source_inventory = []
    # Independently frozen respondent/item/value/configuration multiset from
    # ORIGINAL synthetic cells and input projection rules, never C11 output.
    respondent_by_row = {binding.row_ordinal: binding.respondent_ref for binding in s['projection'].row_bindings}
    rules_by_name = {rule.slot.name: rule for rule in s['projection'].response_slots}
    for cell in s['stream'].cell_iter_factory():
        if cell.variable_name not in rules_by_name:
            continue
        rule = rules_by_name[cell.variable_name]
        for occurrence in rule.values[0].occurrences:
            source_inventory.append(dict(respondent_ref=respondent_by_row[cell.row_ordinal].as_dict(),
                item_ref=s['fx']['qrefs'][cell.variable_name].as_dict(),
                raw_response_value=raw_physical_value_witness(cell.raw_value),
                configuration=dict(occurrence.multiplicity_order_rank_fields), response_state='SUBSTANTIVE_RESPONSE'))
    frozen = P.FrozenExpected.from_documentary_payload(dict(schema=P.V.ACCEPTED_EXPECTED_SCHEMA,
        expected_derived_from='EXTERNAL_FROZEN', declarations=rows, source_inventory=source_inventory))
    declarations = []
    for row in rows:
        d = dict(row)
        for field in ('query_ref', 'predicate_ref', 'discovery_authority_ref'):
            if field in d:
                d[field] = ExactRef(**d[field])
        declarations.append(C.V2ExpectedWorkDeclaration(**d))
    bindings = C.v2_bind_semantic_to_dispatch(declarations=declarations,
        projection_fields=s['projection_fields'], runtime_catalog=s['catalog'])
    prod = execute_route_b_production(source=s['stream'], projection=s['projection'],
        runtime_catalog=s['catalog'], i03_requests=[dict(query_ref=d.query_ref,
        predicate_ref=d.predicate_ref) for d in declarations if d.query_ref is not None],
        discovery_authority_ref=s['discovery_ref'])
    executor = prod.repository_binding.executor
    facts = {f.ref.key: f for outcome in prod.i03_results for f in outcome.facts}
    discoveries = {r.ref.key: prod.i05_result for r in prod.i05_result.receipts}
    calls = []
    def execute(unit):
        calls.append(unit.unit_ref.key)
        if unit.job_kind == 'DISCOVERY':
            outcome = executor.execute_i05(discovery_authority_ref=unit.job_ref)
            discoveries.update({r.ref.key: outcome for r in outcome.receipts})
            return ExecutionOutcome(result_refs=tuple(r.ref for r in outcome.receipts),
                                    provenance_refs=(unit.job_ref, *unit.semantic_input_refs))
        outcome = executor.execute_i03(query_ref=unit.job_ref, predicate_ref=s['all_p'].ref)
        facts.update({f.ref.key: f for f in outcome.facts})
        return ExecutionOutcome(result_refs=tuple(f.ref for f in outcome.facts),
                                provenance_refs=(unit.job_ref, *unit.semantic_input_refs))
    manifest = BatchManifest(tuple(BatchUnitSpec(job_kind='QUERY' if b.dispatch_class == 'I03_UNARY_OR_JOINT_QUERY' else 'DISCOVERY', job_ref=b.dispatch_job_ref,
        release_refs=(prod.c11_release.release_ref,),
        semantic_input_refs=tuple(r for r in (b.dispatch_predicate_ref, b.dispatch_authority_ref) if r is not None)) for b in bindings))
    session = G.open_session(manifest=manifest, repository=executor.repository,
        executors={'QUERY': ExecutorBinding(s['qauth'].ref, execute), 'DISCOVERY': ExecutorBinding(s['dauth'].ref, execute)}, root=root,
        source_sha256=s['source_sha'])
    return dict(expected=frozen, session=session, runtime_catalog=s['catalog'],
                resolve_fact=lambda ref: facts[ref.key], resolve_discovery=lambda ref: discoveries[ref.key], producer_permission_ceiling=('SOURCE_FREE_DEV',)), calls


def test_actual_field_forge_consumes_saved_durable_results_and_replays(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    first = P.run_integrated(**kwargs)
    assert first['ok'], first
    assert len(calls) == 3
    assert len(first['consumer_products']) == 3
    for product in first['consumer_products']:
        assert product['result_ref'] == product['consumer_material']['producer_fact_ref']
        assert len(product['consumer_material']['conditional_count_profile']) == 2
    prior = {p['expected_work_key']: ExactRef(**p['consumer_ref']) for p in first['consumer_products']}
    replay = P.run_integrated(**kwargs, prior_consumer_refs=prior)
    assert replay['ok'], replay
    assert replay['consumer_products'] == first['consumer_products']
    assert replay['run']['executed'] == []
    assert len(calls) == 3
    (tmp_path / 'integrated_receipt.json').write_text(json.dumps(first, default=str, indent=2))


def test_missing_original_operation_refused_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    session = kwargs['session']
    kwargs['session'] = replace(session, manifest=BatchManifest(session.manifest.units[:1]))
    with pytest.raises(ValueError, match='EXPECTED_OPERATION_OMITTED'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_source_mismatch_refused_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    kwargs['session'] = replace(kwargs['session'], source_sha256='foreign')
    with pytest.raises(ValueError, match='SOURCE_IDENTITY_MISMATCH'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_output_derived_expectation_refused(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    payload = json.loads(kwargs['expected'].payload_json)
    payload['expected_derived_from'] = 'RESULT_OUTPUT'
    with pytest.raises(ValueError, match='EXPECTED_SET_OUTPUT_DERIVED'):
        P.FrozenExpected.from_documentary_payload(payload)


def test_stale_consumer_ref_refused_by_real_owner(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    first = P.run_integrated(**kwargs)
    assert first['ok'], first
    prior = {p['expected_work_key']: ExactRef(**p['consumer_ref']) for p in first['consumer_products']}
    key = next(iter(prior))
    prior[key] = ExactRef(prior[key].kind, prior[key].object_id, '0'*64)
    with pytest.raises(ValueError, match='replay mismatch'):
        P.run_integrated(**kwargs, prior_consumer_refs=prior)


def test_foreign_job_ref_and_release_ref_are_refused_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    session = kwargs['session']
    first = session.manifest.units[0]
    foreign = ExactRef(first.job_ref.kind, 'urn:p01:foreign', '1'*64)
    bad = replace(first, job_ref=foreign)
    kwargs['session'] = replace(session, manifest=BatchManifest((bad, *session.manifest.units[1:])))
    with pytest.raises(ValueError, match='FOREIGN_OR_COLLIDING'):
        P.run_integrated(**kwargs)
    foreign_release = ExactRef('C11LogicalRelease', 'urn:p01:foreign-release', '2'*64)
    bad = replace(first, release_refs=(foreign_release,))
    kwargs['session'] = replace(session, manifest=BatchManifest((bad, *session.manifest.units[1:])))
    with pytest.raises(ValueError, match='MANIFEST_RELEASE_IDENTITY_MISMATCH'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_duplicate_expected_dispatch_is_refused_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    rows = [r for r in doc['declarations'] if 'query_ref' in r]
    rows[1]['query_ref'] = rows[0]['query_ref']
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='DUPLICATE_OWNER_JOB_REF'):
        P.run_integrated(**kwargs)
    assert calls == []


@pytest.mark.parametrize('state', ['DEFERRED', 'FAILED'])
def test_deferred_and_failed_units_remain_pinned(tmp_path, state):
    from rawlsing_next.pre553_batch_runner import BatchDeferred
    kwargs, calls = _fixture(tmp_path)
    def stop(unit):
        calls.append(unit.unit_ref.key)
        if state == 'DEFERRED':
            raise BatchDeferred('P01_DEFERRED', 'source-free fixture deliberately deferred')
        raise ValueError('source-free fixture deliberately failed')
    session = kwargs['session']
    kwargs['session'] = replace(session, executors={kind: ExecutorBinding(binding.executor_ref, stop)
        for kind, binding in session.executors.items()})
    first = P.run_integrated(**kwargs)
    assert not first['ok']
    assert first['run']['pinned_deferred']
    count = len(calls)
    second = P.run_integrated(**kwargs)
    assert not second['ok']
    assert second['run']['executed'] == []
    assert len(calls) == count


def test_custodian_hash_claim_never_grants_external_authentication(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    frozen = kwargs['expected'].checked()
    doc['custodian'] = {'issuer': 'CLAIMED-EXTERNAL-OWNER', 'frozen_frontier_digest': frozen['frontier_digest'],
                        'authenticated': True, 'signature': 'invented'}
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    report = P.run_integrated(**kwargs)
    assert any(h['code'] == 'EXTERNAL_CUSTODIAN_ISSUER_HOLD' for h in report['holds'])
    assert report['custodian']['signature_trusted'] is False


def test_real_interruption_after_effect_holds_pending_head_and_never_duplicates(tmp_path):
    import subprocess, sys, signal
    script = '''
from pathlib import Path
import os, signal, sys
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
kwargs, _ = _fixture(Path(sys.argv[1]))
def interrupt(*args, **kwargs):
    os.kill(os.getpid(), signal.SIGKILL)
P.G.record_commit = interrupt
P.run_integrated(**kwargs)
'''
    child = subprocess.run([sys.executable, '-c', script, str(tmp_path)], capture_output=True, text=True, timeout=30)
    assert child.returncode == -signal.SIGKILL, child.stderr
    kwargs, calls = _fixture(tmp_path)
    before = G.recover(kwargs['session'])
    assert len(before.plan.held_units) == 1
    assert len(before.journal_entries) == 1
    report = P.run_integrated(**kwargs)
    assert not report['ok']
    assert report['run']['executed'] == []
    assert len(report['run']['blocked_behind_held']) == 2
    assert calls == []
    after = G.recover(kwargs['session'])
    assert after.journal_entries == before.journal_entries
    from rawlsing_next.pre553_batch_durable_checkpoint_candidate import plan_recovery
    checkpoint = kwargs['session'].checkpoint()
    unit_key = before.plan.held_units[0]
    forged = plan_recovery(checkpoint, idempotence_proof={unit_key: 'forged-proof'})
    assert forged.held_units == before.plan.held_units
    assert forged.rerunnable_units == ()


def test_original_respondent_item_and_configuration_are_required(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    payload = json.loads(kwargs['expected'].payload_json)
    assert len(payload['source_inventory']) == 18
    payload['source_inventory'].pop()
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(payload)
    with pytest.raises(ValueError, match='ORIGINAL_RESPONDENT_ITEM_CONFIGURATION_MISMATCH'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_minority_values_all_item_keys_and_nonscalar_configurations_survive(tmp_path):
    kwargs, _ = _fixture(tmp_path)
    report = P.run_integrated(**kwargs)
    assert report['ok']
    inventory = report['source_inventory']
    keys = {(r['respondent_ref']['content_hash'], r['item_ref']['content_hash']) for r in inventory}
    assert len(keys) == 12
    assert len(inventory) == 18
    # The original X=0 response belongs to one respondent; X=1 to two.
    x = [r for r in inventory if r['item_ref']['object_id'].endswith('m01-X')]
    assert sorted(r['raw_response_value']['$raw_physical_value']['token']['v'] for r in x) == ['0','1','1']
    o = [r for r in inventory if r['item_ref']['object_id'].endswith('m01-O')]
    assert sorted({r['configuration']['semantic_ordinal'] for r in o}) == [0,1]
    assert {r['raw_response_value']['$raw_physical_value']['token']['v'] for r in o} == {'AB','BA'}
    repeated = [r for r in inventory if r['item_ref']['object_id'].endswith('m01-R')]
    assert sorted({r['configuration']['multiplicity_index'] for r in repeated}) == [0,1]
    assert {r['raw_response_value']['$raw_physical_value']['token']['v'] for r in repeated} == {'XY','XZ'}
    assert sorted(r['state'] for r in report['produced']['held_export']) == ['DENIED','HELD','HELD','SOURCE_NONAPPLICABLE']


def test_foreign_respondent_and_incomplete_saved_input_are_refused(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    payload = json.loads(kwargs['expected'].payload_json)
    payload['source_inventory'][0]['respondent_ref']['content_hash'] = '3'*64
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(payload)
    with pytest.raises(ValueError, match='ORIGINAL_RESPONDENT_ITEM_CONFIGURATION_MISMATCH'):
        P.run_integrated(**kwargs)
    assert calls == []
    kwargs, _ = _fixture(tmp_path)
    original = kwargs['resolve_fact']
    def unrelated(ref):
        fact = original(ref)
        from rawlsing_next.pre553_empirical_objects import EmpiricalFact
        return EmpiricalFact(typed_state=fact.typed_state,
            authority_snapshot_refs=fact.authority_snapshot_refs,
            dependency_refs=fact.dependency_refs,
            producer_replay_locator_or_reference_root=fact.producer_replay_locator_or_reference_root,
            **{**dict(fact.semantic_fields), 'raw_denominator_support': 999})
    kwargs['resolve_fact'] = unrelated
    with pytest.raises(ValueError, match='SAVED_RESULT_OBJECT_IDENTITY_MISMATCH'):
        P.run_integrated(**kwargs)


def test_wrong_condition_order_is_refused_before_execution(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    row = next(r for r in doc['declarations'] if 'query_ref' in r)
    row['condition_order'].reverse()
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='CONDITION_ORDER_SUBSTITUTION'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_multiple_results_are_explicitly_unsupported(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    doc['declarations'][0]['multiplicity'] = 2
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='FIELD_FORGE_SINGLE_RESULT_REQUIRED'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_second_integrated_writer_is_refused_before_execution(tmp_path):
    import subprocess, sys
    kwargs, calls = _fixture(tmp_path)
    from rawlsing_next.pre553_batch_durable_checkpoint_candidate import ledger_lock
    script = '''
from pathlib import Path
import sys
from rawlsing_next.tests.test_pre553_v2_durable_consumer_integration_candidate import _fixture
from rawlsing_next import pre553_v2_durable_consumer_integration_candidate as P
kwargs,calls = _fixture(Path(sys.argv[1]))
P.run_integrated(**kwargs)
'''
    with ledger_lock(tmp_path / '.p01.integration.lock'):
        child = subprocess.run([sys.executable, '-c', script, str(tmp_path)], capture_output=True, text=True, timeout=30)
    assert child.returncode != 0
    assert 'CheckpointLockError' in child.stderr
    assert calls == []
    assert not kwargs['session'].store.exists()


def test_extra_manifest_predicate_cannot_substitute_frozen_query_predicate(tmp_path):
    from rawlsing_next.pre553_batch_durable_checkpoint_candidate import CheckpointIdentity
    kwargs, calls = _fixture(tmp_path)
    payload = json.loads(kwargs['expected'].payload_json)
    row = next(r for r in payload['declarations'] if 'query_ref' in r)
    original = ExactRef(**row['predicate_ref'])
    other = next(p.ref for p in kwargs['runtime_catalog'].predicates if p.ref != original)
    row['predicate_ref'] = other.as_dict()
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(payload)
    session = kwargs['session']
    units = tuple(replace(unit, semantic_input_refs=(*unit.semantic_input_refs, other))
                  if unit.job_ref == ExactRef(**row['query_ref']) else unit for unit in session.manifest.units)
    manifest = BatchManifest(units)
    kwargs['session'] = replace(session, manifest=manifest, identity=CheckpointIdentity.from_manifest(manifest))
    with pytest.raises(ValueError, match='QUERY_PREDICATE_SUBSTITUTION'):
        P.run_integrated(**kwargs)
    assert calls == []


@pytest.mark.parametrize('substitution', ['predicate', 'release'])
def test_saved_fact_must_use_frozen_predicate_and_release(tmp_path, substitution):
    from rawlsing_next.pre553_empirical_objects import EmpiricalFact
    kwargs, _ = _fixture(tmp_path)
    session = kwargs['session']
    facts = {}
    other = next(p.ref for p in kwargs['runtime_catalog'].predicates
                 if p.ref != ExactRef(**next(r for r in json.loads(kwargs['expected'].payload_json)['declarations'] if 'predicate_ref' in r)['predicate_ref']))
    original_execute = session.executors['QUERY'].execute
    def substituted(unit):
        outcome = original_execute(unit)
        original = kwargs['resolve_fact'](outcome.result_refs[0])
        fields = dict(original.semantic_fields)
        if substitution == 'predicate':
            fields['condition_predicate_ref'] = other
        else:
            provenance = [ref for ref in fields['source_empirical_provenance_refs'] if ref['kind'] != 'C11LogicalRelease']
            provenance.append(ExactRef('C11LogicalRelease', 'FOREIGN-RELEASE', '4'*64).as_dict())
            fields['source_empirical_provenance_refs'] = provenance
        fact = EmpiricalFact(typed_state=original.typed_state,
            authority_snapshot_refs=original.authority_snapshot_refs,
            dependency_refs=original.dependency_refs,
            producer_replay_locator_or_reference_root=original.producer_replay_locator_or_reference_root,
            **fields)
        facts[fact.ref.key] = fact
        return ExecutionOutcome(result_refs=(fact.ref,), provenance_refs=outcome.provenance_refs)
    kwargs['session'] = replace(session, executors={**session.executors,
        'QUERY': ExecutorBinding(session.executors['QUERY'].executor_ref, substituted)})
    resolver = kwargs['resolve_fact']
    kwargs['resolve_fact'] = lambda ref: facts[ref.key] if ref.key in facts else resolver(ref)
    with pytest.raises(ValueError, match='FACT_PREDICATE_SUBSTITUTION' if substitution == 'predicate' else 'FACT_RELEASE_SUBSTITUTION'):
        P.run_integrated(**kwargs)


@pytest.mark.parametrize('job', ['QUERY','DISCOVERY'])
def test_field_forge_measure_is_bound_for_queries_and_discovery(tmp_path, job):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    row = next(r for r in doc['declarations'] if ('discovery_authority_ref' in r) == (job == 'DISCOVERY') and r['state']=='RUNNABLE')
    row['measure_kind'] = 'GOVERNED_WEIGHTED'
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='FIELD_FORGE_RAW_MEASURE_REQUIRED'):
        P.run_integrated(**kwargs)
    assert calls == []


@pytest.mark.parametrize('job', ['QUERY','DISCOVERY'])
def test_nonexistent_frozen_authority_is_refused_before_execution(tmp_path, job):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    row = next(r for r in doc['declarations'] if ('discovery_authority_ref' in r) == (job == 'DISCOVERY') and r['state']=='RUNNABLE')
    row['authority_ref'] = 'UNRELATED-NONEXISTENT-AUTHORITY'
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='declared operation authority is not exactly present'):
        P.run_integrated(**kwargs)
    assert calls == []


def test_different_existing_authority_cannot_replace_dispatch_authority(tmp_path):
    kwargs, calls = _fixture(tmp_path)
    doc = json.loads(kwargs['expected'].payload_json)
    row = next(r for r in doc['declarations'] if 'query_ref' in r)
    row['authority_ref'] = next(a.authority_ref.key for a in kwargs['runtime_catalog'].authorities if a.authority_ref.key != row['authority_ref'])
    kwargs['expected'] = P.FrozenExpected.from_documentary_payload(doc)
    with pytest.raises(ValueError, match='DISPATCH_AUTHORITY_SUBSTITUTION'):
        P.run_integrated(**kwargs)
    assert calls == []
