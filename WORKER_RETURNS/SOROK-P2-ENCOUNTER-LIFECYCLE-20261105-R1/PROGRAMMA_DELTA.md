# PROGRAMMA_DELTA — Sorok P2 encounter lifecycle R1

**Delta ID:** `SOROK-P2-ENCOUNTER-LIFECYCLE-20261105-R1`
**Base:** `41bf45813fd0adeffd9b54e1306c2022abe96514` (independently ACCEPTED scoped TEST_ONLY; PR697 unchanged/unmerged).
**Grade:** `TEST_ONLY_LOCAL_UI_LIFECYCLE_NOT_NATIVE`.
**Result:** focused `5 passed`; cold CLI `PORTAL -> OUTSIDE -> PORTAL`; canonical store unchanged.

## Added

- Additive `LifecycleEncounter` around the accepted `S45Projection`.
- Persistent local `PORTAL`/`OUTSIDE` mode in `<state_root>/.sorok_p2_local/encounter_lifecycle.json`, separate from canonical actor/world state and root-bound.
- Cold `EXIT`/reopen, local `RETURN`, and outside-mode `SAY`/`DO_HELP`/`ATTEND` boundary before real S45 calls.
- Additive lifecycle CLI `run_lifecycle_cli.py`.
- Focused tests/evidence for positive actions, cold exit, return, root mismatch, sidecar cut/restore and privacy.

## Semantics

- `PORTAL` actions use the existing WP19/S11 projection results.
- `PORTAL` `EXIT` uses existing `LOCAL_EXIT_ONLY`; sidecar becomes `OUTSIDE`; no world/store mutation.
- `OUTSIDE` actions are refused locally as `LOCAL_OUTSIDE_MODE_BLOCKED` with no actor response, clock change, world event or delivery.
- `OUTSIDE` local `RETURN` is `LOCAL_RETURN_ONLY`, restores `PORTAL`, and does not simulate world return, elapsed life or absence.
- `PORTAL` `RETURN` keeps the existing `RETURN_UNSUPPORTED_TYPED_HOLD`; no world-return producer is invented.
- Another root cannot inherit `OUTSIDE` (`LOCAL_LIFECYCLE_ROOT_MISMATCH`).

## Missing producers preserved

`WAIT_TIME_ADVANCE_RECEIPT`, `PORTAL_EXIT_RETURN_RECEIPT`, `USER_ABSENCE_LIFE_ADVANCE`, `MESSAGE_CHANNEL_ESTABLISHMENT_AND_DELIVERY`, `ACCESSIBILITY_PREFERENCE_ACK` remain missing. Local UI return is not a world return producer.

## Boundary

No inherited product/vendor/projection edits, protected writes, PROGRAMMA working-file changes, native rights, human validation, fabricated absence/activity/delivery, fabricated motives or B states. No self-acceptance; focused independent review is required for this new commit.
