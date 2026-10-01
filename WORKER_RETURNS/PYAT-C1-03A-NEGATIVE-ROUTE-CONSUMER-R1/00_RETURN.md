# PYAT C1-03A — NEGATIVE-STATE / ROUTE-LEGITIMACY / FINAL-CONSUMER COMPOSITION — R1

Status: `PASS_C1_03A_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`

## Mission

Implement and prove AT14, AT15 and AT16 as a source-free tranche on the adopted
C1-02 base.

Branch: `agent/opencode-pyat-hq146-c1-03a-negative-route-consumer-r1`
Base: `bc661188b51e995d9f5d74e55c4e37d2ba358a17`
Commission tip: `da29402473ad671625feb49fad5142a1d689978b`

This was a real implementation tranche, not an audit. One bounded new owner was
written and every mandatory state is driven through a competent current owner.

## What was built

| File | Role |
|---|---|
| `rawlsing_next/pre553_analytical_state_and_route.py` | Bounded state-conservation + route-legitimacy envelope |
| `rawlsing_next/tests/test_pre553_analytical_state_and_route.py` | 20 courts across AT14/AT15/AT16 |
| `rawlsing_next/tests/c1_at14_at16_fixture.py` | Fixtures that drive real owners per state |

The adopted C1-02 owner `pre553_analytical_composition.py` was **not modified**,
and its 109-test court is unchanged. No AT14–AT16 gap forced a change there.

## AT14 — negative-state conservation

All eight mandatory states are reached from a competent owner and retained
pairwise-distinct. Nothing is called N/A.

| State | Competent owner | Producer-native |
|---|---|---|
| OBSERVED_ZERO | empirical query | fact `SUPPORTED` + cell `OBSERVED_ZERO_IN_SUPPORTED_RISK_SET` |
| VALID_EMPTY | empirical query | `VALID_EMPTY` (empty declared domain, positive denominator) |
| UNDERPOWERED | exact discovery | `INSUFFICIENT_SUPPORT` / `EVALUATED_UNDERPOWERED` |
| UNKNOWN/UNRESOLVED | empirical query | `UNRESOLVED` |
| UNVISITED | **adaptive discovery** | `PARTIAL_BUDGET_EXHAUSTED` + real `unvisited_unit_refs` |
| NONCOMPARABLE | empirical query | `NONCOMPARABLE` |
| BLOCKED_REQUIRED_AUTHORITY | exact discovery | owner raises on `DENY` snapshot |
| INTEGRITY_FAILURE | canonical object constructor | `Pre553IntegrityError` on tampered body with stale sealed id |

### Two findings worth calling out

**Observed zero is a cell state, not a fact state.** The owning fact stays
`SUPPORTED` and the zero lives in the complete cell projection. My first
implementation classified it from the fact state, which silently collapsed
observed zero into a plain positive — exactly the collapse the commission
forbids. Fixed with `classify_empirical_cells`, which reads the producer's own
cell projection and refuses an observed-zero cell on a non-supported fact.

**`SUPPORTED` is not part of the mandatory estate.** I initially validated
`retained_state` against the 8 mandatory negatives only, which made it impossible
to carry a competent positive result through the same envelope. Split into
`MANDATORY_AT14_STATES` (the 8) and `RETAINABLE_STATES` (8 + positive baseline).

### No state was coerced

Where the final consumer cannot losslessly represent a state, the envelope records
**explicit non-invocation with a reason** rather than fabricating a verdict.
`test_at16_negative_states_are_not_coerced_into_a_consumer_state` covers
UNRESOLVED, NONCOMPARABLE and INTEGRITY_FAILURE.

One honesty correction I made mid-build: my default disposition initially claimed
`CONSUMER_INVOKED` for observed zero with a null result — that is precisely the
fabrication AT16 forbids. The default now never claims an invocation; only the
AT16 positive-path court, which drives the real consumer, records one.

### Positive handoff ≠ coverage record

`test_at14_positive_recursive_handoff_is_not_the_coverage_record` builds a real
generation-one handoff, then attempts two launderings: relabelling the positive
handoff as UNVISITED coverage with no unvisited territory, and attaching unvisited
territory to a positive state. Both fail closed in the envelope builder.

## AT15 — direct-route legitimacy

**Competent direct stays direct.** A real empirical fact is consumed on
`DIRECT_EMPIRICAL` with `authority_refs == ()`. No learned wrapper is imposed.

**A genuinely learned/adjudicated-required case exists on this base.** Structural
mediation use of a fact requires a named, hash-bound `StructuralAdmissionRule`
plus matching `STRUCTURAL_ADMISSION` authority. With `rule=None` the owner cannot
return ADMITTED — even for a SUPPORTED fact. The same fact is simultaneously
lawfully consumable on the direct route, which proves the requirement is
use-specific rather than universal. No learned rule was invented; the rule and
authority come from the owner's own public builders.

**Two laundering hostiles blocked.** A failed learned claim (UNRESOLVED fact
submitted with a real rule and ALLOW authority, failing admission) and a DENY-authority
claim both raise `RouteLegitimacyError` when relabelled `DIRECT_EMPIRICAL`.

**The route label creates no authority.** Two envelopes over the same fact
differing only in route have different identities, neither carries authority, and
neither changes the retained state.

## AT16 — final-consumer witness

**Positive path.** Real producer → C1 composition → actual
`evaluate_positioned_subject_possibility`. Recorded: producer fact ref, composed
result identity hash, consumer query ref, consumer rule hash, generated evidence
ref, consumer result state and hash. Custody is asserted by
`evidence.geometry["source_fact_ref"] == composition.producer_fact_ref`, so the
evidence provably descends from the producer.

**Negative path.** VALID_EMPTY records explicit non-invocation; the reason is
inside the envelope identity preimage, so it cannot be dropped.

**Handmade-slice hostile.** Calling the real consumer directly *does* return
EXACT_SUPPORTED — which is the point. That result carries no
`producer_fact_ref` and no `composed_result_identity_hash`, so the primitive alone
cannot satisfy AT16.

## Test obligations

| Obligation | Tests | Exit |
|---|---|---|
| C1-03A new courts | 20 | 0 |
| Accepted C1-02 six-file court | 109 | 0 |
| Adaptive discovery (relied on for UNVISITED) | 11 | 0 |
| Structural admission (relied on for route legitimacy) | 17 | 0 |
| **Total** | **157** | **0 failures** |

All eight required hostile themes are covered; see
`04_HOSTILE_CASE_RECEIPTS.json`.

## Prohibitions

No raw survey files. No Candidate A/B/C. No measured P2X. No real-source C11. No
C4. No AT17/N10E. No AT18/AT19 — `pre553_authority_maintenance.py` and
`pre553_replay_audit.py` untouched. No C1-R. No V3 actor/person. No new semantic,
comparability, model or pooling authority; M1/M2 not imposed on the competent
direct route. No merge. Not self-adopted.

## Return inventory

`00_RETURN.md`, `01_STATE_CONSERVATION_MATRIX.json`,
`02_ROUTE_LEGITIMACY_AUDIT.json`, `03_FINAL_CONSUMER_TRACE.json`,
`04_HOSTILE_CASE_RECEIPTS.json`, `05_EXECUTION_RECEIPT.json`,
`06_FINAL_DISPOSITION.json`, `FINAL_COURT.txt`.

## Non-claims

AT17 reserved to N10E. AT18–AT19 to the parallel worker. The retained C1-02
three-tree wider-regression attribution was **not** re-run, because this tranche
adds one new owner and modifies no adopted owner.

## Terminal

`C1_03A_NEGATIVE_ROUTE_CONSUMER_RETURNED__HQ_ADJUDICATION_REQUIRED`