# Sorok Interval Producer R1 — Exact executable source archive

TEST_ONLY SOURCEFREE. No product runtime, production authority or native CAN011 learning rule.

Run: `python -m pytest -q test_sorok_interval_witness_lab.py test_sorok_interval_participation_producer_r1.py`
Observed: **56 passed in 0.06s**

## `sorok_interval_witness_lab.py`

SHA-256: `ff4dc3c5dab0f4953921b981dfbb012d86aff35cf0e81b570f8d92cff53d83d8`

```python
"""Source-free SDTF P3/OBL062 scientific *interface* discriminator.

This is an illustrative diagnostic, NOT native Rawlsing, not a scientific
learning rule, and not a validated model of children.
"""
from dataclasses import dataclass
from typing import Tuple
from hashlib import sha256
import json

TEST_OWNER = 'TEST_ONLY_HOUSEHOLD_ACTIVITY_OWNER@1'
TEST_RULE = 'TEST_ONLY_CARE_REORIENTATION_FORMATION@1'


def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), default=str).encode()).hexdigest()


@dataclass(frozen=True)
class Witness:
    witness_id: str
    actor_id: str
    owner: str
    kind: str  # ACTUAL_RECURRENT_PARTICIPATION vs OBLIGATION_ONLY vs SCHEDULE_ONLY
    coverage: Tuple[Tuple[int, int], ...]
    valid_until: int
    status: str = 'ACTIVE'  # ACTIVE | TERMINATED | SUPERSEDED
    polarity: str = 'POSITIVE'  # NEGATIVE only via explicit competent negative witness
    rule_id: str = 'TEST_ONLY_ACTIVITY_RULE@1'
    scope_id: str = 'HOUSEHOLD_SIBLING_CARE'


@dataclass(frozen=True)
class Episode:
    episode_id: str
    kind: str
    actor_access: bool = True


EPISODES = (
    Episode('E1_CARE_AFTERNOON', 'ACTUAL_CARE_PERFORMANCE'),
    Episode('E2_SCHOOL_CONFLICT', 'CAREGIVING_SCHOOL_CONFLICT'),
    Episode('E3_NEGOTIATION_WORDS', 'NEGOTIATION_SIGN_ENCOUNTER'),
    Episode('E4_NEGOTIATION_TRY', 'ATTEMPTED_NEGOTIATION'),
)


@dataclass(frozen=True)
class Interval:
    actor_id: str
    start_month: int
    end_month: int
    episodes: Tuple[Episode, ...]
    witness: Witness | None
    uptake_refs: Tuple[str, ...] = ('U2_CONFLICT_EXPERIENCED', 'U4_PRACTICAL_NEGOTIATION_ATTEMPT')


def interval_qualification(interval: Interval) -> dict:
    """Exact witness coverage rather than inferred event counts or duration multiplier."""
    w = interval.witness
    if w is None:
        return {'status': 'UNKNOWN', 'reason': 'NO_RECURRENCE_WITNESS', 'segments': ()}
    if w.owner != TEST_OWNER or w.actor_id != interval.actor_id:
        return {'status': 'REFUSED', 'reason': 'OWNER_OR_ACTOR_MISMATCH', 'segments': ()}
    if w.scope_id != 'HOUSEHOLD_SIBLING_CARE' or w.rule_id != 'TEST_ONLY_ACTIVITY_RULE@1':
        return {'status': 'REFUSED', 'reason': 'RULE_OR_SCOPE_MISMATCH', 'segments': ()}
    if w.status != 'ACTIVE' or w.valid_until < interval.end_month:
        return {'status': 'UNKNOWN', 'reason': 'NONCURRENT_OR_SUPERSEDED_WITNESS', 'segments': ()}
    if w.polarity == 'NEGATIVE':
        return {'status': 'EXPLICIT_NEGATIVE', 'reason': 'COMPETENT_NEGATIVE_WITNESS', 'segments': ()}
    if w.polarity != 'POSITIVE':
        return {'status': 'REFUSED', 'reason': 'INVALID_WITNESS_POLARITY', 'segments': ()}
    if w.kind != 'ACTUAL_RECURRENT_PARTICIPATION':
        return {'status': 'NOT_PROVEN_REALIZED', 'reason': 'OBLIGATION_OR_SCHEDULE_NOT_PARTICIPATION', 'segments': ()}
    if not w.coverage or any(e <= s for s,e in w.coverage):
        return {'status': 'REFUSED', 'reason': 'INVALID_COVERAGE', 'segments': ()}
    clipped = sorted((max(s, interval.start_month), min(e, interval.end_month)) for s,e in w.coverage)
    clipped = [(s,e) for s,e in clipped if e > s]
    if not clipped:
        return {'status': 'UNKNOWN', 'reason': 'NO_OVERLAPPING_COVERAGE', 'segments': ()}
    cursor = interval.start_month
    for s,e in clipped:
        if s > cursor:
            return {'status': 'PARTIAL', 'reason': 'GAP_IN_POSITIVE_PARTICIPATION_COVERAGE', 'segments': tuple(clipped)}
        cursor = max(cursor, e)
    if cursor < interval.end_month:
        return {'status': 'PARTIAL', 'reason': 'UNCOVERED_END_OF_INTERVAL', 'segments': tuple(clipped)}
    return {'status': 'QUALIFIED', 'reason': 'COVERED_RECURRENT_PARTICIPATION', 'segments': tuple(clipped)}


def formation_candidate(interval: Interval) -> dict:
    """Candidate diagnostic only; NEVER commits a CAN011 record."""
    q = interval_qualification(interval)
    ids = {e.episode_id for e in interval.episodes if e.actor_access}
    exact_event_basis = {'E2_SCHOOL_CONFLICT', 'E4_NEGOTIATION_TRY'} <= ids
    actor_basis = {'U2_CONFLICT_EXPERIENCED', 'U4_PRACTICAL_NEGOTIATION_ATTEMPT'} <= set(interval.uptake_refs)
    eligible = q['status'] == 'QUALIFIED' and exact_event_basis and actor_basis
    return {
        'test_rule': TEST_RULE,
        'candidate': 'SCOPED_INTERPRETIVE_ORIENTING' if eligible else None,
        'verdict': 'TEST_ONLY_FORMATION_CANDIDATE' if eligible else 'NO_DURABLE_UPDATE_AUTHORIZED',
        'recurrence_status': q['status'],
        'recurrence_reason': q['reason'],
        'source_witness_id': interval.witness.witness_id if interval.witness else None,
        'consumed_event_ids': tuple(sorted({'E2_SCHOOL_CONFLICT','E4_NEGOTIATION_TRY'} & ids)),
        'target_scope': 'NADIA_HOUSEHOLD_CARE_NEGOTIABILITY',
        'persistent_v3_mutation': False,
        'receipt_hash': digest({
            'witness': interval.witness, 'episodes': interval.episodes,
            'uptake': interval.uptake_refs, 'qualification': q,
            'eligible': eligible, 'rule': TEST_RULE
        }),
    }


def scenario(recurring=True) -> Interval:
    return Interval('NADIA', 96, 120, EPISODES,
        Witness('W_REAL_CARE_96_120', 'NADIA', TEST_OWNER,
            'ACTUAL_RECURRENT_PARTICIPATION', ((96,120),), 120) if recurring else None)


def counterfactual_report():
    a, b = scenario(True), scenario(False)
    assert a.episodes == b.episodes
    return {
        'same_episode_ids': [e.episode_id for e in EPISODES],
        'same_episode_count': len(EPISODES),
        'A_recurrence': formation_candidate(a),
        'B_isolated': formation_candidate(b),
        'naive_event_count_baseline': {'A': len(a.episodes), 'B': len(b.episodes), 'discriminates': False},
        'scientific_grade': 'TEST_ONLY_MECHANISM_DISCRIMINATOR_NOT_REAL_HUMAN_CALIBRATION',
    }


if __name__ == '__main__':
    print(json.dumps(counterfactual_report(), indent=2))
```

## `test_sorok_interval_witness_lab.py`

SHA-256: `04a5c9d36affa0f0154467a38aaa4b8e0702ba6d386c71e97d357af7b33f627b`

```python
from dataclasses import replace
from sorok_interval_witness_lab import (
    Interval, Episode, Witness, EPISODES, TEST_OWNER, formation_candidate,
    interval_qualification, scenario, counterfactual_report,
)


def witness(**kw):
    return replace(scenario().witness, **kw)


def test_same_four_events_but_different_regime():
    a,b=scenario(True), scenario(False)
    assert a.episodes == b.episodes
    assert formation_candidate(a)['candidate'] is not None
    assert formation_candidate(b)['candidate'] is None


def test_no_owner_psyche_writes():
    assert formation_candidate(scenario())['persistent_v3_mutation'] is False


def test_schedule_not_participation():
    x=replace(scenario(), witness=witness(kind='SCHEDULE_ONLY'))
    assert interval_qualification(x)['status']=='NOT_PROVEN_REALIZED'
    assert formation_candidate(x)['candidate'] is None


def test_obligation_not_participation():
    x=replace(scenario(), witness=witness(kind='OBLIGATION_ONLY'))
    assert formation_candidate(x)['candidate'] is None


def test_no_implicit_negative_from_missing():
    assert interval_qualification(scenario(False))['status']=='UNKNOWN'


def test_negative_requires_explicit_witness():
    x=replace(scenario(), witness=witness(polarity='NEGATIVE'))
    assert interval_qualification(x)['status']=='EXPLICIT_NEGATIVE'


def test_invalid_owner_refused():
    x=replace(scenario(), witness=witness(owner='UNLICENSED_LLM'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_wrong_actor_refused():
    x=replace(scenario(), witness=witness(actor_id='MOTHER'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_expired_witness_unknown_not_negative():
    x=replace(scenario(), witness=witness(valid_until=110))
    assert interval_qualification(x)['status']=='UNKNOWN'


def test_superseded_witness_unknown():
    x=replace(scenario(), witness=witness(status='SUPERSEDED'))
    assert interval_qualification(x)['status']=='UNKNOWN'


def test_gap_in_coverage_is_partial():
    x=replace(scenario(), witness=witness(coverage=((96,106),(110,120))))
    assert interval_qualification(x)['status']=='PARTIAL'


def test_partial_first_year_not_entire_two_years():
    x=replace(scenario(), witness=witness(coverage=((96,108),)))
    assert interval_qualification(x)['status']=='PARTIAL'


def test_overlapping_contiguous_segments_qualify():
    x=replace(scenario(), witness=witness(coverage=((96,110),(108,120))))
    assert interval_qualification(x)['status']=='QUALIFIED'


def test_missing_actor_uptake_no_formation():
    x=replace(scenario(), uptake_refs=())
    assert formation_candidate(x)['candidate'] is None


def test_unreceived_event_no_formation():
    eps=tuple(replace(e,actor_access=False) if e.episode_id=='E2_SCHOOL_CONFLICT' else e for e in EPISODES)
    x=replace(scenario(), episodes=eps)
    assert formation_candidate(x)['candidate'] is None


def test_no_conflict_episode_no_formation():
    x=replace(scenario(),episodes=tuple(e for e in EPISODES if e.episode_id!='E2_SCHOOL_CONFLICT'))
    assert formation_candidate(x)['candidate'] is None


def test_no_count_multiplier_or_event_count_condition():
    r=counterfactual_report()
    assert r['same_episode_count']==4
    assert not r['naive_event_count_baseline']['discriminates']
    assert r['A_recurrence']['verdict']!=r['B_isolated']['verdict']


def test_replay_exact_receipt():
    assert formation_candidate(scenario())==formation_candidate(scenario())


def test_context_change_affects_receipt_not_prior_events():
    x=scenario(); y=replace(x,witness=witness(coverage=((96,110),)))
    assert x.episodes==y.episodes
    assert formation_candidate(x)['receipt_hash']!=formation_candidate(y)['receipt_hash']


def test_no_double_counting():
    r=formation_candidate(scenario())
    assert r['consumed_event_ids']==('E2_SCHOOL_CONFLICT','E4_NEGOTIATION_TRY')
    assert r['source_witness_id']=='W_REAL_CARE_96_120'


def test_current_wrong_scope_fails():
    x=replace(scenario(),witness=witness(scope_id='EMPLOYER'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_no_events_not_fabricated_by_recurrence():
    x=replace(scenario(),episodes=())
    assert interval_qualification(x)['status']=='QUALIFIED'
    assert formation_candidate(x)['candidate'] is None


def test_absent_test_rule_prevents_retroactive_formation():
    x=replace(scenario(),witness=witness(rule_id='UNREGISTERED'))
    assert interval_qualification(x)['status']=='REFUSED'


def test_representative_prose_no_mutation():
    x=replace(scenario(),episodes=(Episode('E1_CARE_AFTERNOON','EPIC_LIFECHANGING_CARE'),)+EPISODES[1:])
    assert formation_candidate(x)['candidate'] is not None
    assert formation_candidate(x)['persistent_v3_mutation'] is False
```

## `sorok_interval_participation_producer_r1.py`

SHA-256: `1ed6a3eda9762739619d7cd664dd208a4bfcfef6af90d9791a41b3cbb3d02f26`

```python
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
```

## `test_sorok_interval_participation_producer_r1.py`

SHA-256: `a049279e997395031fc87e7389f1c5a6e52da2b732cd4da39285d5df4bd853cf`

```python
from dataclasses import replace
from sorok_interval_participation_producer_r1 import (WorldRegime, EpochOutcome,
    qualify_epoch, realize_interval, non_event_v3_conditioning, diagnostic_candidate,
    example_inputs)


def base(): return example_inputs()


def test_macro_world_producer_generates_positive_condition():
    r, es=base(); x=realize_interval(r,es)
    assert x['coverage']==((96,108),(108,120))
    assert x['individual_daily_events_invented']==0


def test_exact_life_interval_is_eligible_without_new_daily_events():
    r, es=base(); x=diagnostic_candidate(r,es)
    assert x['interval_qualification']['status']=='QUALIFIED'
    assert x['test_only_formation_candidate']['candidate']=='SCOPED_INTERPRETIVE_ORIENTING'
    assert x['mutated_v3'] is False


def test_four_events_identical_with_unknown_participation():
    r, es=base(); a=diagnostic_candidate(r,es)
    b=diagnostic_candidate(r,tuple(replace(e,world_performance='UNKNOWN') for e in es))
    assert a['test_only_formation_candidate']['candidate'] is not None
    assert b['test_only_formation_candidate']['candidate'] is None
    assert a['test_only_formation_candidate']['consumed_event_ids']==b['test_only_formation_candidate']['consumed_event_ids']


def test_schedule_alone_not_activity():
    r,es=base(); assert realize_interval(r,())['coverage']==()


def test_actual_actor_act_no_world_confirmation_is_unknown():
    r, es=base(); e=replace(es[0], world_performance='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_world_claim_without_actor_act_unproven():
    r,es=base(); e=replace(es[0],actor_conduct='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_coerced_performance_not_mistaken_for_consent():
    r,es=base(); assert qualify_epoch(r,es[0]).status=='REALIZED'
    assert es[0].actor_conduct=='RESISTED_BUT_ACTED'


def test_refused_assignment_and_nonperformance_explicit_negative():
    r,es=base(); e=replace(es[0],actor_conduct='REFUSED',world_performance='NOT_PERFORMED')
    assert qualify_epoch(r,e).status=='NEGATIVE_EXPLICIT'


def test_inconsistent_actor_refusal_and_world_performance_refused():
    r,es=base(); e=replace(es[0],actor_conduct='REFUSED',world_performance='CONFIRMED')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_missing_positive_does_not_create_negative():
    r,es=base(); e=replace(es[0],world_performance='UNKNOWN')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_valid_negative_source_is_not_positive_participation():
    r,es=base(); alt=tuple(replace(e,world_performance='NOT_PERFORMED') for e in es)
    assert realize_interval(r,alt)['coverage']==()


def test_partial_coverage_keeps_gaps_not_filled():
    r,es=base(); e=replace(es[1],world_performance='UNKNOWN')
    a=diagnostic_candidate(r,(es[0],e))
    assert a['interval_qualification']['status']=='PARTIAL'
    assert a['test_only_formation_candidate']['candidate'] is None


def test_expired_source_becomes_unknown():
    r,es=base(); e=replace(es[0],source_valid_to=100)
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_superseded_source_becomes_unknown():
    r,es=base(); e=replace(es[0],superseded=True)
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_world_owner_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],source_owner='LLM')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_actor_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],actor_id='MOTHER')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_household_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],household_id='HH2')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_scope_mismatch_is_refusal():
    r,es=base(); e=replace(es[0],scope_id='COMPANY')
    assert qualify_epoch(r,e).status=='REFUSED'


def test_outside_regime_is_refusal():
    r,es=base(); e=replace(es[0],start=80)
    assert qualify_epoch(r,e).status=='REFUSED'


def test_missing_actor_world_evidence_is_unknown():
    r,es=base(); e=replace(es[0],world_receipt='')
    assert qualify_epoch(r,e).status=='UNKNOWN'


def test_schedule_source_rule_required():
    r,es=base(); assert qualify_epoch(replace(r,schedule_ref=''),es[0]).status=='REFUSED'


def test_non_event_conditioning_no_v3_psyche_mutation():
    r,es=base(); p=realize_interval(r,es); c=non_event_v3_conditioning(r,p,r.actor_id,r.end)
    assert c['status']=='CONDITION_AVAILABLE'
    assert c['can011_persistence_emitted'] is False
    assert c['v3_response_emitted'] is False
    assert c['actor_experience_or_belief_inferred'] is False


def test_ingress_actor_scope_firewall():
    r,es=base(); p=realize_interval(r,es)
    assert non_event_v3_conditioning(r,p,'OTHER',r.end)['status']=='REFUSED'


def test_ingress_clock_not_arbitrarily_outside_interval():
    r,es=base(); p=realize_interval(r,es)
    assert non_event_v3_conditioning(r,p,r.actor_id,135)['status']=='REFUSED'


def test_no_double_counting_no_new_realized_event_list():
    r,es=base(); d=diagnostic_candidate(r,es)
    assert d['world_production']['individual_daily_events_invented']==0
    assert len(d['world_production']['epochs'])==2
    assert len(d['test_only_formation_candidate']['consumed_event_ids'])==2


def test_replay_deterministic():
    r,es=base(); assert diagnostic_candidate(r,es)==diagnostic_candidate(r,es)


def test_change_witness_changes_conditioning_not_events():
    r,es=base(); a=diagnostic_candidate(r,es)
    b=diagnostic_candidate(r,(es[0],replace(es[1],world_performance='UNKNOWN')))
    assert a['conditioning']['conditioning_receipt_hash']!=b['conditioning']['conditioning_receipt_hash']
    assert a['test_only_formation_candidate']['consumed_event_ids']==b['test_only_formation_candidate']['consumed_event_ids']


def test_absence_of_regime_assignment_still_not_an_automatic_negative():
    r,es=base(); r=replace(r,assigned=False)
    # sourcefree input can establish performed activity absent duty; assignment not a formation parent by itself
    assert qualify_epoch(r,es[0]).status=='REALIZED'


def test_witness_does_not_cause_durable_effect_without_rule():
    r,es=base(); d=diagnostic_candidate(r,es)
    assert d['test_only_formation_candidate']['persistent_v3_mutation'] is False
    assert d['mutated_v3'] is False


def test_tampered_coverage_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['coverage']=((96,120),)
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'


def test_tampered_world_receipt_hash_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['receipt_hash']='TAMPERED'
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'


def test_tampered_qualifications_refused_at_ingress():
    r,es=base(); p=realize_interval(r,es); p['epochs']=()
    assert non_event_v3_conditioning(r,p,r.actor_id,r.end)['status']=='REFUSED'
```