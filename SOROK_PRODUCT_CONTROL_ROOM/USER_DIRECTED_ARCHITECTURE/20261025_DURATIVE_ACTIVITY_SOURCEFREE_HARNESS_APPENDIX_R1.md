# Sorok Durative Activity — Sourcefree Test Harness Appendix R1

**Status:** TEST_ONLY. No original source or native V3/CAN authority; no claims of scientific validity or Sorok consumer integration.

Reproduce locally: install pytest and run `python -m pytest -q test_sorok_interval_witness_lab.py`. The output observed in this court was `24 passed in 0.04s`.

## sorok_interval_witness_lab.py

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

## test_sorok_interval_witness_lab.py

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

## Exact counterfactual receipt

```json
{
  "same_episode_ids": [
    "E1_CARE_AFTERNOON",
    "E2_SCHOOL_CONFLICT",
    "E3_NEGOTIATION_WORDS",
    "E4_NEGOTIATION_TRY"
  ],
  "same_episode_count": 4,
  "A_recurrence": {
    "test_rule": "TEST_ONLY_CARE_REORIENTATION_FORMATION@1",
    "candidate": "SCOPED_INTERPRETIVE_ORIENTING",
    "verdict": "TEST_ONLY_FORMATION_CANDIDATE",
    "recurrence_status": "QUALIFIED",
    "recurrence_reason": "COVERED_RECURRENT_PARTICIPATION",
    "source_witness_id": "W_REAL_CARE_96_120",
    "consumed_event_ids": [
      "E2_SCHOOL_CONFLICT",
      "E4_NEGOTIATION_TRY"
    ],
    "target_scope": "NADIA_HOUSEHOLD_CARE_NEGOTIABILITY",
    "persistent_v3_mutation": false,
    "receipt_hash": "4d1bfb8cc77aad49e70ecc8558ecb66fa37240be3b86c8ac3c0971a43789226f"
  },
  "B_isolated": {
    "test_rule": "TEST_ONLY_CARE_REORIENTATION_FORMATION@1",
    "candidate": null,
    "verdict": "NO_DURABLE_UPDATE_AUTHORIZED",
    "recurrence_status": "UNKNOWN",
    "recurrence_reason": "NO_RECURRENCE_WITNESS",
    "source_witness_id": null,
    "consumed_event_ids": [
      "E2_SCHOOL_CONFLICT",
      "E4_NEGOTIATION_TRY"
    ],
    "target_scope": "NADIA_HOUSEHOLD_CARE_NEGOTIABILITY",
    "persistent_v3_mutation": false,
    "receipt_hash": "3d1b22259aa32e640b833e2531dbd411b09e49b087adef5d6dd25e4cddc30719"
  },
  "naive_event_count_baseline": {
    "A": 4,
    "B": 4,
    "discriminates": false
  },
  "scientific_grade": "TEST_ONLY_MECHANISM_DISCRIMINATOR_NOT_REAL_HUMAN_CALIBRATION"
}

```