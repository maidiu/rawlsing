# Vozhd Dva Current State

**As of:** 2026-08-17  
**Canonical codebase:** `main`  
**Phase:** WAVE_0_READY_FOR_LAUNCH

## Mission now

Execute the bounded five-worker Wave 0 that will make V553→V558 downstream requirements concrete, repair the known V552J→V553 entry defect, and establish executable vertical-continuity infrastructure. Vozhd Dva will then adjudicate the five returns into a finite Wave-1 implementation register.

## Canonical assumptions

- Current repository code is the implementation frontier.
- V550–V552J are closed by default.
- `POSTG5-004` is active: repair the obsolete V552J→V553 consumer expectation on the V553 side.
- V553–V558 are not independently finishable without downstream-consumer visibility.
- Enneagram-like attractor formation is part of the intended design; V556 supplies structural pressure-flow/attractor prerequisites and topology, while V3 later realizes actor-specific developmental formation.
- V3 is the intended causal/temporal actor engine; V2 is the intended phenomenological/conversational layer and is not causal authority.
- Architecture/process work is bounded by execution value and may not become an independent infinite project.

## Wave 0 integration base

- **Integration branch:** `agent/vozhd-dva-wave0-integration`
- **Pinned base SHA:** `958983139b8f75dc5cda65d5bf71b376d17820df`
- The branch contains the finalized Wave-0 control-room packets and is the required base/PR target for R0-01 through R0-05.

## Wave 0 structure

Five worker cells are fully specified under `rabochii/WAVE_0/`:

1. **R0-01 V553/V554** — repair `POSTG5-004`; audit V552J→V553→V554 preservation/loss.
2. **R0-02 V555** — define the minimum mediation-information contract without actor-specific biography.
3. **R0-03 V556/attractor** — define pressure-flow/attractor topology and the V556/V3 jurisdiction seam.
4. **R0-04 runtime contract** — define minimum V557/V558→V3 and V3→V2 consumer requirements.
5. **R0-05 vertical harness** — build isolated deterministic five-slice continuity-test infrastructure.

Common worker protocol:
- `rabochii/WAVE_0/README.md`
- `rabochii/WAVE_0/LAUNCH_INDEX.md`
- `rabochii/WAVE_0/REPORT_FORMAT.json`

Every worker returns `RESULT.md` + `RESULT.json` inside its assigned cell on its worker branch and opens a draft PR against the Wave-0 integration branch.

## Vozhd Dva intake/review structure

- Intake/synchronization: `integration/WAVE_0_INTAKE_LEDGER.md`
- Review protocol: `reviews/WAVE_0_REVIEW_PROTOCOL.md`
- Individual Vozhd reviews will be written under `reviews/WAVE_0/`.
- Worker self-report never equals project acceptance.

## Immediate next action

Launch R0-01 through R0-05 concurrently from `agent/vozhd-dva-wave0-integration` using `rabochii/WAVE_0/LAUNCH_INDEX.md` and the exact assignment packet in each worker cell.

As returns arrive, review PR + report together, update the intake ledger, and propagate cross-hooks only to affected lanes.

## Active blockers

No control-room blocker to Wave-0 launch.

Known implementation entry defect:
- `POSTG5-004`, owned by R0-01.

## Wave-0 exit condition

Wave 0 is complete only after Vozhd Dva has reviewed all five returns, adjudicated collisions, updated `CAPABILITY_MATRIX.md`, and produced a finite Wave-1 implementation register with non-overlapping write domains and executable acceptance tests.

## Restart instruction

A future Vozhd Dva chat should read, in order:

1. `CONTROL_ROOM_MAP.md`
2. `state/CURRENT_STATE.md`
3. `LIVE_ITINERARY.md`
4. `rabochii/WAVE_0/LAUNCH_INDEX.md` if Wave 0 is still active
5. `integration/WAVE_0_INTAKE_LEDGER.md`
6. only the specific worker/review/prong files needed for the next action.

Do not reconstruct project state from chat history when the control-room state is available.
