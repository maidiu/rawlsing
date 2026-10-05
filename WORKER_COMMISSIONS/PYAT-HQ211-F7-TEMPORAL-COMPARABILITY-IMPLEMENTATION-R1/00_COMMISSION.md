# PYAT HQ211 — F7 TEMPORAL COMPARABILITY SOURCE-FREE IMPLEMENTATION — R1

**STATUS:** BOUND_QUEUED — DO NOT LAUNCH UNTIL AN HQ IMPLEMENTER SLOT FREES  
**AGENT:** Space Bunny source-free implementation worker  
**MODEL / INTELLIGENCE:** **Space Bunny High**  
**BRANCH:** `agent/rabochii-pyat-hq211-f7-implementation-r1`  
**EXACT STARTUP BASE:** `b722f2e7373ad833d5f63833b1d6fe426d3dc55d`  
**ACCEPTED CONTRACT:** `agent/rabochii-pyat-hq210-f7-contract-repair-r1 @ c57a96897788108db7b194e4e51691d1ca8ab729`  
**HOSTILE REVIEW PREDECESSOR:** `f1a0dbbc8491e0d23df9005abd55b83e0261424e`  
**CHECKOUT:** SPARSE_REQUIRED  
**SOURCE ACCESS:** FORBIDDEN  
**F8 CONSUMPTION:** FORBIDDEN  
**SELF-ADOPTION:** FORBIDDEN

This commission is already bound but is **QUEUE-ONLY** while HQ211 has two active implementation slots. Launch it immediately when HQ frees one implementer slot. Do not treat branch existence as authorization to exceed concurrency.

Read and obey `PYAT_CONTROL_ROOM/SHARED_STORE_SPARSE_WORKTREE_EXECUTION_LAW_R1.md`.

## Mission

Implement the HQ211-accepted F7 temporal-comparability contract exactly as repaired at:
`c57a96897788108db7b194e4e51691d1ca8ab729`

No architecture redesign. No new temporal ontology beyond that contract.

## Exact allowed production surface

A lawful implementation may add only:

1. `TEMPORAL_COMPARABILITY` to `AUTHORITY_KINDS`;
2. exactly one matching `AUTHORITY_KIND_CEILINGS` entry;
3. one bounded temporal-comparison module and its focused court;
4. exact use of existing authority resolution;
5. cross-universe consumption of an independently resolved positive `SOURCE_EQUIVALENCE` through the existing source-relation path.

The receipt remains a module-local closed content-addressed result:
- NOT a `PUBLIC_OBJECT_FAMILIES` member;
- `relation_state` is NOT `CanonicalSemanticObject.typed_state`;
- no `STATE_FAMILIES` widening.

## Mandatory contract law

### Order
Authorized bases:
- `CALENDAR_TOTAL_ORDER`
- `FAMILY_LOCAL_ORDINAL`
- `PARTIAL_ORDER_NO_DIRECTION`

Typed no-basis refusal:
- `ORDER_UNKNOWN_NONCOMPARABLE`

That refusal MUST carry no basis ref and uniquely maps to:
`TEMPORAL_ORDER_UNAUTHORIZED / NO_PERMITTED_ORDER_BASIS_APPLIES`.

### Direction
`TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED` requires all:
- pair COMPARABLE;
- `ORDERED_RELATION_AUTHORIZED`;
- direction-permitting authorized basis;
- claimable exact direction;
- exact delta present;
- all required authorities positive.

### NO_AUTHORIZED_CHANGE
Exact signed delta == canonical zero ONLY.
No deadband, tolerance, inherited V553 threshold, or epsilon.

### Deterministic relation-state precedence
Highest first:
1. TEMPORAL_INSUFFICIENT_AUTHORITY
2. TEMPORAL_IDENTITY_UNRESOLVED
3. TEMPORAL_INSUFFICIENT_ANCHORS
4. TEMPORAL_CROSS_UNIVERSE_EQUIVALENCE_ABSENT
5. TEMPORAL_MAPPING_MATERIAL_ABSENT
6. TEMPORAL_ESTIMAND_MISMATCH
7. TEMPORAL_MEASURE_MISMATCH
8. TEMPORAL_NONCOMPARABLE
9. TEMPORAL_ORDER_UNAUTHORIZED
10. TEMPORAL_INTERVAL_OVERLAP_NO_DIRECTION
11. TEMPORAL_COMPARABLE_NO_DIRECTION
12. TEMPORAL_DIRECTIONAL_CLAIM_AUTHORIZED

All detected failures remain in provenance/results; precedence chooses one public terminal state.

`relation_state_reason` is exactly one scalar reason under state-local precedence.

Existing `AUTHORITY_STATE` failures map to `TEMPORAL_INSUFFICIENT_AUTHORITY` while preserving the exact authority state in provenance.

### Prior F7 states
- AUTHORITY_MISSING / CONFLICT / OUT_OF_SCOPE -> TEMPORAL_INSUFFICIENT_AUTHORITY
- INTERPOLATION_NOT_AUTHORIZED -> TEMPORAL_NONCOMPARABLE
- PROBE_ONLY -> NO TEMPORAL_RELATION_RECEIPT
- RESPONSE_SURFACE_MISMATCH -> TEMPORAL_NONCOMPARABLE

## Cross-universe law

Two independent positive paths:
1. source-relation owner resolves `SOURCE_EQUIVALENCE`;
2. temporal owner resolves `TEMPORAL_COMPARABILITY` and consumes that exact equivalence ref.

Neither may mint or imply the other.

## Explicit non-surfaces

No:
- F8 conditioning/source selection/geometry/distribution transform;
- cause/event/mediation/mechanism;
- continuity/interpolation/midpoint;
- rate/trend/trajectory/acceleration;
- >=3-anchor law;
- rupture producer/threshold/cause;
- source-equivalence creation, linkage, overlap, pooling, estimand composition;
- currentness;
- scalar temporal pressure;
- `EmpiricalFact` time-field change;
- universal grain enum;
- actor/person inference.

Keep literal `TEMPORAL_NONCOMPARABLE` in `FORBIDDEN_BACKFILL_TARGET_STATES`.
A receipt is never a backfill target; a temporally noncomparable pair cannot be backfilled into positivity.

## Qualification

Create a court that independently proves:
- kind/ceiling pairing;
- all 12 states reachable where appropriate and deterministic;
- multi-failure precedence;
- scalar reason determinism;
- positive-state reason nonempty;
- invalid cross-field tuples refuse;
- exact-zero semantics;
- partial-order direction refusal;
- no-basis unique path;
- authority-state mapping;
- probe-only no-receipt path;
- cross-universe two-path positive and refusal;
- backfill noncollapse;
- no F8 import/consumption;
- replay identity stability.

Run focused court plus current authority/source-relation regression courts and report exact failure-ID set deltas.

## Required return

Write only under:
`WORKER_RETURNS/PYAT-HQ211-F7-TEMPORAL-COMPARABILITY-IMPLEMENTATION-R1/`

Required:
- `00_RETURN.md`
- `01_IMPLEMENTATION_AND_OWNER_RECEIPT.json`
- `02_STATE_AND_PRECEDENCE_RECEIPT.json`
- `03_NONCOLLAPSE_AND_POWER_CEILING.json`
- `04_COURT_AND_REGRESSION_RESULTS.json`
- `05_FINAL_DISPOSITION.json`

Allowed:
- `F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_COMPLETE__READY_FOR_HOSTILE_REVIEW`
- `F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_PARTIAL__NAMED_DEFECT`
- `F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_REVEALS_AUTHORITY_CONFLICT`

Terminal:
`HQ211_F7_TEMPORAL_COMPARABILITY_IMPLEMENTATION_RETURNED__HOSTILE_REVIEW_REQUIRED`
