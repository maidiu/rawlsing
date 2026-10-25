"""SOURCEFREE scientific seam: epoch-grain actor/world participation -> non-event V3 input.

All source and behavior rules are explicitly synthetic. This does NOT implement
Sorok production C12, ADP-021 cadence, SDTF D1' native issuance, OBL062 closure,
or CAN-011 native developmental updates. No LLM calls.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from hashlib import sha256
from typing import Tuple
import json
from sorok_interval_witness_lab import Witness, Interval, EPISODES, TEST_OWNER, TEST_RULE, formation_candidate, interval_qualification

PRODUCER = 'TEST_ONLY_INTERVAL_ACTIVITY_REALIZER@1'
V3_PORT = 'TEST_ONLY_NON_EVENT_V3_CONDITIONING_PORT@1'
WORLD_OWNER = 'TEST_ONLY_SHARED_HOUSEHOLD_WORLD@1'


def fingerprint(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), default=str).encode()).hexdigest()


@dataclass(frozen=True)
class WorldRegime:
    actor_id: str
    household_id: str
    scope_id: str
    start: int
    end: int
    assigned: bool
    schedule_ref: str
    source_rule_ref: str = 'TEST_ONLY_CARE_REGIME_SOURCE@1'


@dataclass(frozen=True)
class EpochOutcome:
    actor_id: str
    household_id: str
    scope_id: str
    start: int
    end: int
    actor_conduct: str  # ACTED / RESISTED_BUT_ACTED / REFUSED / UNKNOWN
    world_performance: str  # CONFIRMED / NOT_PERFORMED / UNKNOWN
    actor_act_receipt: str  # actual macro actor participation evidence, not intent or plan
    world_receipt: str  # independently issued world aggregate realization
    source_owner: str = WORLD_OWNER
    source_valid_to: int = 120
    superseded: bool = False


@dataclass(frozen=True)
class EpochQualification:
    start: int
    end: int
    status: str
    reason: str
    input_hash: str


def qualify_epoch(regime: WorldRegime, epoch: EpochOutcome) -> EpochQualification:
    key = fingerprint({'regime': asdict(regime), 'epoch': asdict(epoch), 'rule': PRODUCER})
    def result(status, reason):
        return EpochQualification(epoch.start, epoch.end, status, reason, key)
    if regime.start >= regime.end or epoch.start >= epoch.end:
        return result('REFUSED', 'INVALID_TIME_INTERVAL')
    if (epoch.actor_id, epoch.household_id, epoch.scope_id) != (regime.actor_id, regime.household_id, regime.scope_id):
        return result('REFUSED', 'ACTOR_HOUSEHOLD_SCOPE_MISMATCH')
    if epoch.start < regime.start or epoch.end > regime.end:
        return result('REFUSED', 'OUTSIDE_SOURCE_REGIME')
    if not regime.source_rule_ref or not regime.schedule_ref:
        return result('REFUSED', 'MISSING_SOURCE_RULE_OR_SCHEDULE_REF')
    if epoch.source_owner != WORLD_OWNER:
        return result('REFUSED', 'INVALID_WORLD_SOURCE_OWNER')
    if epoch.superseded or epoch.source_valid_to < epoch.end:
        return result('UNKNOWN', 'EXPIRED_OR_SUPERSEDED_WORLD_RECEIPT')
    if not epoch.actor_act_receipt or not epoch.world_receipt:
        return result('UNKNOWN', 'ACTOR_OR_WORLD_REALIZATION_WITNESS_MISSING')
    if epoch.actor_conduct in ('ACTED', 'RESISTED_BUT_ACTED') and epoch.world_performance == 'CONFIRMED':
        return result('REALIZED', 'MACRO_ACTOR_ACTIVITY_AND_WORLD_PERFORMANCE_BOTH_WITNESSED')
    if epoch.actor_conduct == 'REFUSED' and epoch.world_performance == 'NOT_PERFORMED':
        return result('NEGATIVE_EXPLICIT', 'SOURCE_OWNED_REFUSAL_AND_NONPERFORMANCE')
    if epoch.actor_conduct == 'REFUSED' and epoch.world_performance == 'CONFIRMED':
        return result('REFUSED', 'INCOMPATIBLE_ACTOR_AND_WORLD_RECEIPTS')
    if epoch.world_performance == 'NOT_PERFORMED':
        return result('NEGATIVE_EXPLICIT', 'SOURCE_OWNED_NONPERFORMANCE')
    return result('UNKNOWN', 'INSUFFICIENT_REALIZATION_EVIDENCE')


def realize_interval(regime: WorldRegime, epochs: Tuple[EpochOutcome, ...]):
    """Generate a positive world state from macro epoch acts and independent world receipts.

    These are MODELLED owner-generated aggregate receipts at coarse temporal grain,
    NOT observed real people, inferred daily repeated episodes, or mere scheduling.
    """
    results = tuple(qualify_epoch(regime, e) for e in epochs)
    realized = sorted((q.start, q.end) for q in results if q.status == 'REALIZED')
    invalid = tuple(q for q in results if q.status == 'REFUSED')
    if invalid:
        status = 'REFUSED'
    elif not realized:
        status = 'NO_PROVEN_PARTICIPATION'
    else:
        status = 'PARTIAL_OR_FULL_POSITIVE_PARTICIPATION'
    evidence = tuple(sorted((q.input_hash for q in results)))
    return {'status': status,
            'source': PRODUCER,
            'actor_id': regime.actor_id,
            'household_id': regime.household_id,
            'scope_id': regime.scope_id,
            'coverage': tuple(realized),
            'epochs': tuple(asdict(q) for q in results),
            'input_epoch_ids': evidence,
            'source_regime_hash': fingerprint(regime),
            'receipt_hash': fingerprint({'regime': asdict(regime), 'epoch_qualifications': tuple(asdict(q) for q in results), 'rule': PRODUCER}),
            'direct_psi_change': False,
            'individual_daily_events_invented': 0}


def non_event_v3_conditioning(regime: WorldRegime, produced: dict, actor_id: str, time: int) -> dict:
    """Explicit non-event objective input; not a CAN008 response or CAN011 state writer."""
    epochs = tuple(produced.get('epochs', ()))
    expected_hash = fingerprint({'regime': asdict(regime), 'epoch_qualifications': epochs, 'rule': PRODUCER})
    derived_segments = tuple(sorted((q['start'], q['end']) for q in epochs if q['status'] == 'REALIZED'))
    integrity = (produced.get('receipt_hash') == expected_hash
                 and produced.get('source_regime_hash') == fingerprint(regime)
                 and produced.get('source') == PRODUCER
                 and tuple(produced.get('coverage', ())) == derived_segments)
    eligible = (integrity and produced['status'] != 'REFUSED' and
                produced['actor_id'] == actor_id == regime.actor_id and
                produced['household_id'] == regime.household_id and
                produced['scope_id'] == regime.scope_id and
                regime.start <= time <= regime.end)
    status = 'REFUSED' if not eligible else ('CONDITION_AVAILABLE' if produced['coverage'] else 'NO_POSITIVE_PARTICIPATION')
    data = {'port': V3_PORT, 'status': status,
            'actor_id': actor_id, 'context_scope_ref': regime.scope_id,
            'time': time, 'interval_world_receipt': produced['receipt_hash'],
            'condition_segments': produced['coverage'] if eligible else (),
            'actor_experience_or_belief_inferred': False,
            'actor_access_asserted': False,
            'v3_response_emitted': False,
            'can011_persistence_emitted': False,
            'opaque_owner_rule_ref_required_for_future_effect': True}
    data['conditioning_receipt_hash'] = fingerprint(data)
    return data


def _witness(regime: WorldRegime, conditioning: dict):
    return Witness(witness_id=conditioning['conditioning_receipt_hash'],
                   actor_id=regime.actor_id, owner=TEST_OWNER,
                   kind='ACTUAL_RECURRENT_PARTICIPATION',
                   coverage=tuple(conditioning['condition_segments']),
                   valid_until=regime.end,
                   rule_id='TEST_ONLY_ACTIVITY_RULE@1', scope_id=regime.scope_id)


def diagnostic_candidate(regime, outcomes, uptake=('U2_CONFLICT_EXPERIENCED', 'U4_PRACTICAL_NEGOTIATION_ATTEMPT')):
    prod = realize_interval(regime, tuple(outcomes))
    cond = non_event_v3_conditioning(regime, prod, regime.actor_id, regime.end)
    w = _witness(regime, cond) if cond['status'] == 'CONDITION_AVAILABLE' else None
    interval = Interval(regime.actor_id, regime.start, regime.end, EPISODES, w, tuple(uptake))
    candidate = formation_candidate(interval)
    return {'regime': fingerprint(regime), 'world_production': prod, 'conditioning': cond,
            'interval_qualification': interval_qualification(interval),
            'test_only_formation_candidate': candidate,
            'mutated_v3': False}


def example_inputs():
    regime = WorldRegime('NADIA', 'HH1', 'HOUSEHOLD_SIBLING_CARE', 96, 120, True, 'SCHEDULE8_10')
    a = EpochOutcome('NADIA', 'HH1', regime.scope_id, 96, 108, 'RESISTED_BUT_ACTED', 'CONFIRMED',
                     'ACTOR_AGGREGATE_EPOCH_1', 'WORLD_ACTIVITY_EPOCH_1')
    b = EpochOutcome('NADIA', 'HH1', regime.scope_id, 108, 120, 'ACTED', 'CONFIRMED',
                     'ACTOR_AGGREGATE_EPOCH_2', 'WORLD_ACTIVITY_EPOCH_2')
    return regime, (a,b)


if __name__ == '__main__':
    regime, epochs = example_inputs()
    print(json.dumps(diagnostic_candidate(regime, epochs), indent=2))
