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
