# Wave 0 Intake / Synchronization Ledger

**Owner:** Vozhd Dva  
**Purpose:** track worker returns, accepted findings, cross-hooks, collisions, and merge order without letting worker-local conclusions silently become system law.

## Worker intake table

| Worker | Branch | Draft PR | Worker status | Vozhd review | Merge state | Blocking cross-hook |
|---|---|---:|---|---|---|---|
| R0-01 | `agent/vozhd-dva-r0-01-v553-v554` | — | NOT_LAUNCHED | — | — | — |
| R0-02 | `agent/vozhd-dva-r0-02-v555` | — | NOT_LAUNCHED | — | — | — |
| R0-03 | `agent/vozhd-dva-r0-03-v556-attractor` | — | NOT_LAUNCHED | — | — | — |
| R0-04 | `agent/vozhd-dva-r0-04-runtime-contract` | — | NOT_LAUNCHED | — | — | — |
| R0-05 | `agent/vozhd-dva-r0-05-vertical-harness` | — | NOT_LAUNCHED | — | — | — |

## Known entry dependencies

### INT-W0-001 — POSTG5-004

- **Producer:** canonical V552J
- **Consumer:** V553
- **Owner:** R0-01
- **Law:** repair obsolete V553 consumer expectation on V553 side; do not recreate legacy V552J packet.
- **Status:** READY_FOR_R0-01

### INT-W0-002 — V555/V556 shared seam

- **R0-02 owes R0-03:** minimum mediation information needed for structural pressure-flow.
- **R0-03 owes R0-02/Vozhd:** explicit V556 consumer requirements, not code changes to V555.
- **Status:** PARALLEL_RECON_ALLOWED; Vozhd adjudicates conflicting proposed grains.

### INT-W0-003 — V556/V558/V3 seam

- **R0-03 owes R0-04:** structural pressure-flow and attractor information that must survive V557/V558.
- **R0-04 owes R0-03/Vozhd:** minimum V3 consumer requirements that constrain V556/V557/V558 representations.
- **Status:** PARALLEL_RECON_ALLOWED; no shared production edits in Wave 0.

### INT-W0-004 — Harness obligations

- **R0-05 consumes:** current contracts plus frozen five-slice target.
- **R0-05 may expose:** missing producer/consumer obligations for R0-01 through R0-04.
- **Law:** test failures/current gaps are evidence, not permission for R0-05 to repair production stages.
- **Status:** PARALLEL_RECON_ALLOWED.

## Accepted cross-stage findings

None yet. Add only after Vozhd Dva review.

Required fields for each accepted finding:

- finding ID;
- originating worker;
- affected producer/consumer;
- Vozhd ruling;
- required owner;
- blocking/nonblocking;
- implementation wave target;
- affected capability/vertical slice;
- whether another active worker must be informed or relaunched.

## Interface collisions

None yet. A collision exists when two workers propose incompatible object grains, responsibilities, meanings, or information-loss rules at the same seam. Vozhd Dva must resolve it before either proposal becomes authoritative.

## Merge policy

- R0-05 test-only infrastructure may be merged early if scope-clean and independent.
- R0-01 isolated `POSTG5-004` repair may be merged after focused review if it does not prejudge broader V553/V554 semantics.
- R0-02/R0-03/R0-04 reconnaissance PRs primarily contribute reports/findings; any diagnostic-only additions are reviewed independently.
- Proposed cross-stage contracts become authoritative only in the post-return Vozhd synthesis, not merely through worker merge order.

## Wave-0 synthesis exit

Wave 0 exits only when Vozhd Dva has:

1. reviewed all five worker returns;
2. adjudicated interface collisions;
3. updated `CAPABILITY_MATRIX.md` with accepted requirements;
4. produced a finite Wave-1 implementation register;
5. assigned non-overlapping Wave-1 write domains;
6. updated `state/CURRENT_STATE.md` and `LIVE_ITINERARY.md`.
