# Live Itinerary

**Status:** WAVE_0_READY_FOR_LAUNCH  
**Canonical base:** `main`  
**Coordinator:** Vozhd Dva

## Immediate sequence

### 1. Launch bounded Wave 0

The worker packets are frozen under `rabochii/WAVE_0/` and should now be launched concurrently from the Wave-0 integration base.

- **R0-01:** V553/V554 boundary + `POSTG5-004` repair.
- **R0-02:** V555 mediation semantics.
- **R0-03:** V556 pressure-flow / Enneagram-like attractor semantics.
- **R0-04:** V557/V558 runtime boundary + V3/V2 consumer requirements.
- **R0-05:** vertical fixture / continuity-test harness.

Launch instructions and exact cell paths: `rabochii/WAVE_0/LAUNCH_INDEX.md`.

### 2. Maintain intake while workers run

Vozhd Dva owns `integration/WAVE_0_INTAKE_LEDGER.md`.

As each draft PR appears:
- record PR/head SHA and worker terminal state;
- read `RESULT.json` and `RESULT.md`;
- inspect the actual patch;
- identify cross-hooks affecting other active workers;
- propagate only necessary changed assumptions, not whole-worker reports.

Do not allow one worker's proposal to become shared law before review/adjudication.

### 3. Review each return

Use `reviews/WAVE_0_REVIEW_PROTOCOL.md` and create one review file per worker under `reviews/WAVE_0/`.

Priority review order if returns arrive together:
1. R0-01 isolated entry repair, because it fixes the canonical V552J→V553 seam;
2. R0-05 test infrastructure, because it can sharpen evaluation of the semantic reports;
3. R0-02/R0-03/R0-04 as a coupled semantic set, because their proposed contracts constrain one another.

### 4. Vozhd Dva Wave-0 synthesis

After all five are reviewed:
- adjudicate V555/V556/V558 object-grain and responsibility collisions;
- update `CAPABILITY_MATRIX.md` only with accepted requirements;
- convert findings into a finite implementation register;
- define Wave-1 worker lanes and non-overlapping write domains;
- bind Wave-1 acceptance to the vertical harness.

Architecture discovery stops here unless implementation exposes a concrete unanticipated dependency.

### 5. Execute Wave 1 semantic deepening

Expected parallel lanes, subject to Wave-0 findings:
- V553/V554 implementation;
- V555 implementation;
- V556 implementation;
- V557/V558 implementation;
- vertical test/harness tightening.

Workers may revise upstream representations when a downstream contract proves starvation, but cross-stage interface changes remain Vozhd-adjudicated.

### 6. Horizontal qualification

Once representative vertical slices work:
- qualify across representative multi-wave/source families;
- repair common-model failures;
- run broad corpus qualification;
- do not create source-family-specific downstream ontologies merely to force pass status.

### 7. Rebuild runtime

- V3 causal/temporal state/event/pressure-flow/attractor engine against the accepted V558 contract.
- Parent/partner/household/child genealogy orchestration.
- V2 phenomenology/conversation boundary against V3 state/history.

### 8. App/demo completion

Optimize for a polished demonstrable vertical path suitable for portfolio/resume presentation. Defer nonessential breadth.

## Current blockers / known risks

- `POSTG5-004` V552J→V553 obsolete consumer contract — assigned R0-01.
- Current downstream thin-build standard does not prove downstream semantic continuity — R0-05 begins executable replacement coverage.
- V555/V556 are scaffold-grade and must be deepened without crossing into actor-specific generated-person jurisdiction.
- R0-02/R0-03/R0-04 may propose incompatible seam contracts; this is expected and is resolved by Vozhd Dva, not by workers editing each other's domains.
- Process-sprawl risk remains active: no new control artifact unless it directly enables delegation, review, synchronization, or acceptance.

## Decision log

- 2026-08-17: current `main` established as implementation authority/frontier.
- 2026-08-17: rejected serial independent stage completion; adopted bounded verticalization.
- 2026-08-17: Enneagram-like attractor formation affirmed as intended design component; V556 supplies structural prerequisites/topology and V3 realizes actor-specific formation.
- 2026-08-17: established Vozhd Dva control room with isolated prongs, Rabochii cells, integration state, reviews, and restart state.
- 2026-08-17: made worker-context selection a Vozhd Dva responsibility; each assignment carries upstream law and downstream obligations.
- 2026-08-17: Wave 0 frozen as five concurrent bounded assignments with standard GitHub return/report protocol.

## Next Vozhd Dva action

Pin the Wave-0 integration branch from the finalized `main` control-room snapshot, then launch R0-01 through R0-05 concurrently.
