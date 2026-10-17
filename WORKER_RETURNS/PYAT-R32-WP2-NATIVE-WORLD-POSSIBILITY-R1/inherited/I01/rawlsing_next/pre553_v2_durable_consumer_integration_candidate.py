"""Source-free V2 expectation -> B01E durable receipts -> Field Forge candidate.

This adapter consumes caller-frozen documentary expectations and exact owner
objects. It confers no external custody, source-use or REAL_EXECUTION grant.
The durable adapter retains unknown-outcome holds; consumers only see committed
COMPLETED receipts. Owner modules are called without modification.
"""
from __future__ import annotations

from dataclasses import dataclass, replace
import hashlib
import json
from typing import Any, Callable, Mapping

from rawlsing_next import pre553_original_workload_v2_verifier_candidate as V
from rawlsing_next import pre553_governed_batch_checkpoint_integration_candidate as G
from rawlsing_next.field_forge_conditional_support import (
    produce_exact_conditional_support_profile,
    replay_exact_conditional_support_profile,
)
from rawlsing_next.pre553_empirical_objects import ExactRef, canonicalize
from rawlsing_next.pre553_empirical_objects import exact_ref

CONSUMER = 'FIELD_FORGE_CONDITIONAL_SUPPORT'


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(',', ':'))


@dataclass(frozen=True)
class FrozenExpected:
    """Immutable documentary input, separately supplied before owner execution.

    Integrity is checkable; independent authorship and external custody are
    expressly not authenticated by this object or its digest.
    """
    payload_json: str
    payload_sha256: str

    @classmethod
    def from_documentary_payload(cls, payload: Mapping[str, Any]) -> FrozenExpected:
        if payload.get('expected_derived_from') != 'EXTERNAL_FROZEN':
            raise ValueError('EXPECTED_SET_OUTPUT_DERIVED_OR_UNDECLARED')
        V.freeze_payload(payload)
        raw = _canonical(payload)
        return cls(raw, hashlib.sha256(raw.encode()).hexdigest())

    def checked(self) -> dict:
        if hashlib.sha256(self.payload_json.encode()).hexdigest() != self.payload_sha256:
            raise ValueError('FROZEN_EXPECTATION_DIGEST_MISMATCH')
        payload = json.loads(self.payload_json)
        if payload.get('expected_derived_from') != 'EXTERNAL_FROZEN':
            raise ValueError('EXPECTED_SET_OUTPUT_DERIVED_OR_UNDECLARED')
        frozen = V.freeze_payload(payload)
        if any(r['raw'].get('multiplicity', 1) != 1 for r in frozen['records'] if r['runnable']):
            raise ValueError('FIELD_FORGE_SINGLE_RESULT_REQUIRED')
        for record in frozen['records']:
            if record['runnable'] and record['raw']['required_consumer'] == CONSUMER:
                if record['raw'].get('measure_kind', 'RAW') != 'RAW':
                    raise ValueError('FIELD_FORGE_RAW_MEASURE_REQUIRED')
                if record['raw']['semantic_op_class'] not in ('PAIR_RESPONSE_COTRAVEL', 'BOUNDED_DISCOVERY'):
                    raise ValueError('FIELD_FORGE_OPERATION_UNSUPPORTED')
        return frozen


def _run_integrated_locked(
    *, expected: FrozenExpected,
    session: G.GovernedBatchCheckpointSession,
    runtime_catalog: Any,
    resolve_fact: Callable[[ExactRef], Any],
    producer_permission_ceiling: tuple[str, ...],
    prior_consumer_refs: Mapping[str, ExactRef] | None = None,
    resolve_discovery: Callable[[ExactRef], Any] | None = None,
) -> dict:
    """Run the real durable owner adapter and consume exact saved result refs.

    resolve_fact must resolve the owner-produced object identified by the saved
    receipt. Field Forge independently validates semantic hashes and query,
    risk, universe, authority, replay and provenance closure. A stale consumer
    identity is refused by its actual replay API. Missing or unsupported
    consumers are explicit holds, never fabricated successful receipts.
    """
    frozen = expected.checked()  # before ANY execution in this adapter
    rows = {r['recomputed']['expected_work_key']: r for r in frozen['records']}
    by_dispatch = {}
    for key, row in rows.items():
        if not row['runnable']:
            continue
        raw = row['raw']
        ref = raw.get('query_ref', raw.get('discovery_authority_ref'))
        dispatch = _canonical(ref)
        if dispatch in by_dispatch:
            raise ValueError('DUPLICATE_OWNER_JOB_REF')
        by_dispatch[dispatch] = key
    # Full outer join before execution: missing original work cannot disappear.
    units_by_key = {}
    for unit in session.manifest.units:
        key = by_dispatch.get(_canonical(unit.job_ref.as_dict()))
        if key is None or key in units_by_key:
            raise ValueError('FOREIGN_OR_COLLIDING_MANIFEST_UNIT')
        row = rows[key]['raw']
        from rawlsing_next.pre553_original_workload_binder_candidate import _resolve_declared_authority
        snapshot = _resolve_declared_authority(runtime_catalog, row['authority_ref'], expected_work_key_value=key)
        if snapshot.ref not in unit.semantic_input_refs:
            raise ValueError('DISPATCH_AUTHORITY_SUBSTITUTION')
        if row['source_identity'] != session.source_sha256:
            raise ValueError('SOURCE_IDENTITY_MISMATCH')
        expected_kind = 'DISCOVERY' if row['semantic_op_class'] == 'BOUNDED_DISCOVERY' else 'QUERY'
        if unit.job_kind != expected_kind:
            raise ValueError('DISPATCH_KIND_SUBSTITUTION')
        if unit.job_kind == 'QUERY':
            from rawlsing_next.pre553_original_workload_contract_v2_candidate import _v2_owner_short_order
            query = runtime_catalog.resolve_query_exact(unit.job_ref)
            if snapshot.authority_ref not in query.authority_snapshot_refs:
                raise ValueError('QUERY_AUTHORITY_SUBSTITUTION')
            owner_order = _v2_owner_short_order(query)
            if len(owner_order) > 1 and tuple(row.get('condition_order', ())) != owner_order:
                raise ValueError('CONDITION_ORDER_SUBSTITUTION')
            if query.requested_output_grain.get('measure_kind') != row.get('measure_kind', 'RAW'):
                raise ValueError('MEASURE_KIND_SUBSTITUTION')
            predicate = ExactRef(**row['predicate_ref'])
            if exact_ref(query.condition_predicate_ref) != predicate:
                raise ValueError('QUERY_PREDICATE_SUBSTITUTION')
            if predicate not in unit.semantic_input_refs:
                raise ValueError('PREDICATE_SUBSTITUTION')
        if unit.job_kind == 'DISCOVERY':
            discovery_authority = runtime_catalog.resolve_discovery_authority_exact(unit.job_ref)
            if snapshot.authority_ref not in discovery_authority.authority_snapshot_refs:
                raise ValueError('DISCOVERY_AUTHORITY_SUBSTITUTION')
        units_by_key[key] = unit
    if set(units_by_key) != set(frozen['runnable_keys']):
        raise ValueError('EXPECTED_OPERATION_OMITTED')
    from rawlsing_next.pre553_batch_durable_checkpoint_candidate import CheckpointIdentity
    if CheckpointIdentity.from_manifest(session.manifest) != session.identity:
        raise ValueError('MANIFEST_RELEASE_IDENTITY_MISMATCH')
    if prior_consumer_refs is not None and set(prior_consumer_refs) - set(units_by_key):
        raise ValueError('FOREIGN_CONSUMER_KEY')

    payload = json.loads(expected.payload_json)
    original_inventory = payload.get('source_inventory')
    if not isinstance(original_inventory, list) or not original_inventory:
        raise ValueError('ORIGINAL_SOURCE_INVENTORY_REQUIRED')
    actual_inventory = []
    for ref in session.identity.release_refs:
        release = session.repository.resolve_release_exact(ref)
        if release.source_artifact_ref.content_hash != session.source_sha256:
            raise ValueError('RELEASE_SOURCE_IDENTITY_MISMATCH')
        for event in release.public_objects:
            if event.FAMILY != 'RespondentEvent@1.0.0':
                continue
            actual_inventory.append(dict(respondent_ref=exact_ref(event.scoped_respondent_ref).as_dict(),
                item_ref=exact_ref(event.native_question_ref).as_dict(),
                raw_response_value=canonicalize(event.raw_response_value),
                configuration=canonicalize(event.multiplicity_order_rank_fields), response_state=event.response_state))
    if sorted(map(_canonical, original_inventory)) != sorted(map(_canonical, actual_inventory)):
        raise ValueError('ORIGINAL_RESPONDENT_ITEM_CONFIGURATION_MISMATCH')
    # Drive one unit per call. Re-plan after every COMMIT so a new FAILED or
    # DEFERRED head remains pinned before considering the next unit.
    executed = []
    while True:
        report = G.run_to_completion(session, max_units=1)
        executed.extend(report.executed_units)
        if not report.executed_units:
            break
        if any(unit.receipt_state != 'COMPLETED' for unit in report.executed_units):
            report = G.run_to_completion(session, max_units=0)
            break
    report = replace(report, executed_units=tuple(executed))
    recovery = G.recover(session)
    receipts = {r.unit_ref.key: r for r in G.admit_saved_receipts(session)}
    produced_units, consumers, consumer_products, holds = [], [], [], []
    for key, unit in units_by_key.items():
        raw = rows[key]['raw']
        from rawlsing_next.pre553_original_workload_binder_candidate import _resolve_declared_authority
        snapshot = _resolve_declared_authority(runtime_catalog, raw['authority_ref'], expected_work_key_value=key)
        receipt = receipts.get(unit.unit_ref.key)
        if receipt is None or receipt.state != 'COMPLETED':
            holds.append({'code': 'DURABLE_RESULT_NOT_COMPLETED', 'expected_work_key': key})
            continue
        if raw['required_consumer'] != CONSUMER:
            holds.append({'code': 'CONSUMER_OWNER_CALL_UNSUPPORTED', 'expected_work_key': key,
                          'job_kind': unit.job_kind, 'consumer': raw['required_consumer']})
            continue
        discovery_receipt = None
        if unit.job_kind == 'QUERY':
            query = runtime_catalog.resolve_query_exact(unit.job_ref)
            facts = tuple(resolve_fact(ref) for ref in receipt.result_refs)
            if not facts or tuple(f.ref for f in facts) != receipt.result_refs:
                raise ValueError('SAVED_RESULT_OBJECT_IDENTITY_MISMATCH')
            for fact in facts:
                if snapshot.authority_ref not in fact.authority_snapshot_refs:
                    raise ValueError('FACT_AUTHORITY_SUBSTITUTION')
                if exact_ref(fact.condition_predicate_ref) != ExactRef(**raw['predicate_ref']):
                    raise ValueError('FACT_PREDICATE_SUBSTITUTION')
        elif unit.job_kind == 'DISCOVERY' and resolve_discovery is not None:
            if len(receipt.result_refs) != 1:
                raise ValueError('EXPECTED_DISCOVERY_MULTIPLICITY_MISMATCH')
            result = resolve_discovery(receipt.result_refs[0])
            from rawlsing_next.pre553_discovery_exact import ExactBoundedDiscoveryResult
            from rawlsing_next.pre553_empirical_objects import semantic_hash
            if not isinstance(result, ExactBoundedDiscoveryResult):
                raise ValueError('EXACT_DISCOVERY_RESULT_REQUIRED')
            for result_receipt in result.receipts:
                if semantic_hash(result_receipt.semantic_projection()) != result_receipt.content_hash:
                    raise ValueError('DISCOVERY_RECEIPT_SEMANTIC_IDENTITY_MISMATCH')
            if result.discovery_authority_ref != unit.job_ref:
                raise ValueError('DISCOVERY_AUTHORITY_SUBSTITUTION')
            matching = [r for r in result.receipts if r.ref == receipt.result_refs[0]]
            if len(matching) != 1:
                raise ValueError('SAVED_DISCOVERY_RECEIPT_IDENTITY_MISMATCH')
            discovery_receipt = matching[0]
            if snapshot.authority_ref not in discovery_receipt.authority_snapshot_refs:
                raise ValueError('DISCOVERY_RECEIPT_AUTHORITY_SUBSTITUTION')
            if discovery_receipt.typed_state != 'DISCOVERED_RESULT_SUPPORTED':
                holds.append({'code': 'DISCOVERY_RESULT_NOT_SUPPORTED', 'expected_work_key': key,
                              'typed_state': discovery_receipt.typed_state})
                continue
            winning = exact_ref(discovery_receipt.winning_predicate_ref)
            receipt_fact_refs = tuple(exact_ref(ref) for ref in discovery_receipt.empirical_fact_refs)
            facts = tuple(f for f in result.empirical_facts
                          if f.ref in receipt_fact_refs
                          and exact_ref(f.condition_predicate_ref) == winning)
            if len(facts) != 1:
                holds.append({'code': 'DISCOVERY_WINNER_NOT_SINGLE_FACT', 'expected_work_key': key})
                continue
            query = next(q for q in result.executed_queries if q.ref == exact_ref(facts[0].empirical_query_spec_ref))
        else:
            holds.append({'code': 'CONSUMER_OWNER_CALL_UNSUPPORTED', 'expected_work_key': key,
                          'job_kind': unit.job_kind, 'consumer': raw['required_consumer']})
            continue
        if len(facts) != raw.get('multiplicity', 1):
            raise ValueError('EXPECTED_MULTIPLICITY_MISMATCH')
        # Current Field Forge owner accepts one exact RAW two-target fact.
        if len(facts) != 1 or len(query.target_refs) != 2:
            holds.append({'code': 'FIELD_FORGE_REQUIRES_SINGLE_TWO_TARGET_FACT',
                          'expected_work_key': key})
            continue
        if query.requested_output_grain.get('measure_kind') != raw.get('measure_kind', 'RAW') or facts[0].measure_kind != raw.get('measure_kind', 'RAW'):
            raise ValueError('CONSUMED_MEASURE_SUBSTITUTION')
        fact_releases = {exact_ref(ref) for ref in facts[0].source_empirical_provenance_refs
                         if exact_ref(ref).kind == 'C11LogicalRelease'}
        if fact_releases != set(unit.release_refs):
            raise ValueError('FACT_RELEASE_SUBSTITUTION')
        if exact_ref(query.condition_predicate_ref) != exact_ref(facts[0].condition_predicate_ref):
            raise ValueError('QUERY_FACT_PREDICATE_MISMATCH')
        kwargs = dict(joint_fact=facts[0], joint_query=query,
                      conditioner_ref=query.target_refs[0], target_ref=query.target_refs[1],
                      producer_permission_ceiling=producer_permission_ceiling)
        profile = produce_exact_conditional_support_profile(**kwargs)
        prior = (prior_consumer_refs or {}).get(key, profile.ref)
        replayed = replay_exact_conditional_support_profile(expected_ref=prior, **kwargs)
        if replayed.ref != profile.ref or profile.producer_fact_ref != facts[0].ref:
            raise ValueError('CONSUMER_RESULT_REPLAY_MISMATCH')
        consumers.append({'expected_work_key': key, 'consumer': CONSUMER})
        consumer_products.append({'expected_work_key': key,
            'durable_unit_ref': unit.unit_ref.as_dict(),
            'result_ref': facts[0].ref.as_dict(),
            'producer_query_ref': query.ref.as_dict(),
            'producer_predicate_ref': exact_ref(facts[0].condition_predicate_ref).as_dict(),
            'producer_release_refs': [ref.as_dict() for ref in sorted(fact_releases, key=lambda ref: ref.key)],
            'durable_result_refs': [ref.as_dict() for ref in receipt.result_refs],
            'discovery_receipt_ref': discovery_receipt.ref.as_dict() if discovery_receipt else None,
            'consumer_ref': profile.ref.as_dict(),
            'consumer_material': profile.as_dict()})
        produced_units.append({'job_kind': unit.job_kind, 'job_ref': unit.job_ref.as_dict(),
            'claimed_expected_work_key': key, 'declared_source_identity': session.source_sha256,
            'declared_condition_order': raw.get('condition_order', []),
            'predicate_ref': exact_ref(facts[0].condition_predicate_ref).as_dict() if unit.job_kind == 'QUERY' else None,
            'release_refs': [r.as_dict() for r in unit.release_refs],
            'attempt_index': receipt.attempt_index, 'state': receipt.state,
            'result_typed_states': [discovery_receipt.typed_state] if discovery_receipt else [f.typed_state for f in facts],
            'denominators': [f.raw_denominator_support for f in facts],
            'reported_success': all(f.typed_state == 'SUPPORTED' for f in facts) and
                (discovery_receipt is None or discovery_receipt.typed_state == 'DISCOVERED_RESULT_SUPPORTED')})
    release_refs = session.identity.release_refs
    if len(release_refs) != 1:
        raise ValueError('SINGLE_RELEASE_REQUIRED')
    produced = {'executed_source_sha': session.source_sha256,
        'executed_release_ref': release_refs[0].as_dict(), 'units': produced_units,
        'held_export': [{'expected_work_key': key, 'item': row['raw']['item'],
                         'state': row['state']} for key, row in rows.items() if not row['runnable']],
        'consumer_receipts': consumers, 'expected_derived_from': 'EXTERNAL_FROZEN'}
    verdict = V.verify(frozen, produced)
    # The pinned verifier is preserved byte-for-byte. Close its permissive
    # unknown-state branch at this candidate's supported consumer boundary.
    for unit in produced_units:
        if unit['reported_success'] and any(
            V.classify_result(state) not in V.MEASURED_RESULT_CLASSES
            for state in unit['result_typed_states']
        ):
            verdict.fail('UNSUPPORTED_RESULT_REPORTED_AS_SUCCESS', unit['claimed_expected_work_key'])
            verdict.ok = False
    return {'ok': verdict.ok and recovery.reconciliation.ok and not holds,
        'expected_payload_sha256': expected.payload_sha256,
        'run': report.summary(), 'recovery': recovery.summary(), 'produced': produced,
        'source_inventory': actual_inventory,
        'source_inventory_sha256': hashlib.sha256(_canonical(sorted(actual_inventory, key=_canonical)).encode()).hexdigest(),
        'consumer_products': consumer_products, 'failure_codes': verdict.failure_codes(),
        'custodian': V.custodian_check(frozen, json.loads(expected.payload_json).get('custodian')),
        'holds': holds + [{'code': 'EXTERNAL_CUSTODIAN_ISSUER_HOLD'},
                          {'code': 'SOURCE_USE_AND_REAL_EXECUTION_NOT_GRANTED'}]}


def run_integrated(*, session: G.GovernedBatchCheckpointSession, **kwargs: Any) -> dict:
    """Single-writer entry point for the complete P01 checkpoint transaction.

    All P01 callers must use this entry point. Raw imported B01E calls are not
    covered by its outer lock and are not an authorized parallel writer route.
    """
    from rawlsing_next.pre553_batch_durable_checkpoint_candidate import ledger_lock
    with ledger_lock(session.store.root / '.p01.integration.lock'):
        return _run_integrated_locked(session=session, **kwargs)
