# PYAT C1-03A — NEGATIVE-STATE / ROUTE-LEGITIMACY / FINAL-CONSUMER COMPOSITION — R1

Status: ISSUED__OVERNIGHT_SOURCE_FREE_IMPLEMENTATION

**LAUNCH IN: OpenCode — Space Bunny Free**

Repository:
`maidiu/rawlsing`

Branch:
`agent/opencode-pyat-hq146-c1-03a-negative-route-consumer-r1`

Exact base:
`bc661188b51e995d9f5d74e55c4e37d2ba358a17`

This base is the HQ-adopted C1-02 source-free AT08–AT13 implementation.

Governing specifications:
- `PYAT_CONTROL_ROOM/OMEGA_VOZHD_ORCHESTRATION_R1/05_C1_EXECUTION_SPEC.md`
- `PYAT_CONTROL_ROOM/ASTRA_PYAT_INTEGRATED_DEVELOPMENT_ATLAS_R1/acceptance/AT14.md`
- `.../AT15.md`
- `.../AT16.md`
- `.../nodes/N2.md`
- `.../nodes/N3.md`

AT17 is reserved to the already-built N10E provider and is **not** part of this job.
AT18–AT19 are assigned to a separate parallel worker and are **not** part of this job.

## Mission

Implement and prove the C1-03A source-free tranche:

- **AT14 — negative-state conservation**
- **AT15 — direct-route legitimacy**
- **AT16 — final-consumer witness**

The job is not complete merely because schemas can represent these states. Drive real current owners and actual public paths.

## Existing owners to inspect and reuse

At minimum inspect before designing:
- `rawlsing_next/pre553_analytical_composition.py`
- `rawlsing_next/pre553_empirical_query.py`
- `rawlsing_next/pre553_discovery_exact.py`
- `rawlsing_next/pre553_discovery_adaptive.py`
- `rawlsing_next/pre553_recursive_handoff.py`
- `rawlsing_next/source_backed_positioned_subject_possibility.py`
- `rawlsing_next/pre553_structural_admission.py`
- relevant M1/M2 publication/adjudication owners only where a learned/adjudicated route is actually required.

Do not impose M1/M2 on competent direct empirical products merely to make the architecture uniform.

## AT14 — negative-state conservation

Prove distinct final analytical/consumer handling for the mandatory estate:

1. observed **zero** in a nonzero denominator;
2. **VALID_EMPTY**;
3. **UNDERPOWERED / insufficient support**;
4. **UNKNOWN / UNRESOLVED**;
5. **UNVISITED**;
6. **NONCOMPARABLE**;
7. **BLOCKED / unavailable because required authority is absent or denies use**;
8. **INTEGRITY_FAILURE**.

Use the competent owner for each state.

Important:
- exact discovery already has valid-empty and underpowered states;
- adaptive discovery has explicit nonexhaustive coverage and `EXPLICIT_UNKNOWN_UNVISITED`;
- do not fabricate an “unvisited” token inside a wrapper without executing the adaptive owner;
- observed numeric zero must remain different from valid-empty;
- unknown/unresolved must remain different from underpowered;
- blocked/noncomparable/integrity failure must remain distinguishable from empirical absence.

If one final consumer cannot legally consume every state directly, create or extend the smallest analytical result envelope that preserves:
- producer-native state;
- coverage state;
- reason;
- exact producer refs;
- consumer state if invocation is lawful;
- explicit “consumer not invoked” reason if invocation is unlawful.

Do not coerce every state into `UNKNOWN`, `VALID_EMPTY`, zero, or `FAIL_CLOSED`.

### Positive-only handoff hostile

Show that a positive recursive handoff is **not** the complete coverage record.

A selected handoff must remain linked to / accompanied by access to the discovery/adaptive coverage record containing:
- evaluated negatives;
- underpowered/valid-empty states;
- unvisited frontier where applicable.

Do not claim exhaustive coverage from a positive bundle alone.

## AT15 — direct-route legitimacy

Build an explicit route classification at the analytical-family grain.

Require at least:
- one competent **DIRECT_EMPIRICAL** route whose producer contract is already sufficient and is consumed without unnecessary learned adjudication;
- one **LEARNED_OR_ADJUDICATED_REQUIRED** route/case where current authority/rule is actually required.

Hostile:
- take a learned/adjudicated-required claim that fails or lacks its required rule;
- prove it cannot be relabeled as `DIRECT_PRODUCER` / direct empirical merely to reach the consumer.

The route label itself must not create authority.
The route decision must bind exact producer/result/authority identities.

If no current source-free family on this base legitimately requires a positive learned route, prove that fact and exercise the hostile using the competent current admission/authority owner. Do not invent a learned rule.

## AT16 — final-consumer witness

Prove actual producer output reaches a named current consumer through the public path.

At minimum:
- one direct empirical positive path;
- one non-positive/negative path where final consumer behavior or non-invocation is explicitly preserved.

A handmade `PossibilitySliceEvidence`, handwritten distribution, schema-only object, or direct call to a consumer primitive without the producer path does **not** satisfy AT16.

Record:
- producer ref;
- analytical/composed result ref/hash;
- consumer query/rule identity;
- generated evidence ref where applicable;
- consumer result ref/state;
- exact proof grade.

## Required hostile themes

At minimum:
- zero vs valid-empty noncollapse;
- underpowered vs unresolved noncollapse;
- unvisited preserved from adaptive owner;
- noncomparable not coerced to unresolved;
- integrity failure cannot become valid-empty;
- failed learned claim cannot be route-laundered as direct;
- handmade final slice cannot satisfy final-consumer proof;
- positive recursive handoff cannot masquerade as full coverage.

## Implementation terrain

Preferred new owner if a bounded envelope/router is needed:

`rawlsing_next/pre553_analytical_state_and_route.py`

Preferred tests:

`rawlsing_next/tests/test_pre553_analytical_state_and_route.py`

Optional fixtures/runners:

`rawlsing_next/tests/c1_at14_at16_fixture.py`
`rawlsing_next/tests/c1_at14_at16_fresh_process_runner.py`

You may modify:
- `rawlsing_next/pre553_analytical_composition.py`
- its C1 tests

**only** if an exact AT14–AT16 owner gap cannot be closed through a bounded new owner using the existing public composition result. If you touch the adopted C1-02 owner, preserve the 109-test accepted C1-02 court and explain exactly why the owner change was necessary.

Do not modify replay/invalidation owner terrain assigned to the parallel AT18–AT19 worker:
- `rawlsing_next/pre553_authority_maintenance.py`
- `rawlsing_next/pre553_replay_audit.py`

## Required return

Write only:

`WORKER_RETURNS/PYAT-C1-03A-NEGATIVE-ROUTE-CONSUMER-R1/**`

Required:
- `00_RETURN.md`
- `01_STATE_CONSERVATION_MATRIX.json`
- `02_ROUTE_LEGITIMACY_AUDIT.json`
- `03_FINAL_CONSUMER_TRACE.json`
- `04_HOSTILE_CASE_RECEIPTS.json`
- `05_EXECUTION_RECEIPT.json`
- `06_FINAL_DISPOSITION.json`

The state matrix must include every mandatory AT14 state with:
- competent producer owner;
- exact fixture/test;
- producer-native state;
- analytical retained state;
- final consumer state or explicit lawful non-invocation;
- proof grade.

## Final test obligations

Run:
- all new C1-03A tests;
- the complete accepted C1-02 six-file court;
- adaptive-discovery tests materially relied on for UNVISITED;
- any structural/admission tests materially relied on for route legitimacy.

Record exact counts and commands.

## Allowed dispositions

- `PASS_C1_03A_SOURCE_FREE_PATCH_READY__INDEPENDENT_REVIEW_REQUIRED`
- `BOUNDED_IMPLEMENTATION_OR_COMPOSITION_GAP`
- `TYPED_AUTHORITY_RESIDUAL`
- `EXISTING_OWNER_CHANGE_REQUIRED`
- `ARCHITECTURE_WARRANT`

Do not call something N/A merely to pass a mandatory AT14 state.

## Absolute prohibitions

No raw survey files.
No Candidate A/B/C.
No measured P2X.
No real-source C11.
No C4.
No AT17 implementation or N10E duplication.
No AT18/AT19 implementation.
No C1-R.
No V3 actor/person implementation.
No new real-source semantic/comparability/model authority.
No merge/self-adoption.

## Git completion

When coherent:
1. verify diff from `bc661188...` stays inside this commission;
2. commit all work;
3. push exactly this branch;
4. report final SHA, disposition, terminal, changed files and test counts.

Terminal:

`C1_03A_NEGATIVE_ROUTE_CONSUMER_RETURNED__HQ_ADJUDICATION_REQUIRED`
