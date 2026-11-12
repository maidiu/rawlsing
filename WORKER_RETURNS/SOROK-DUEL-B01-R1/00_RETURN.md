# SOROK B01 Agent A return

**Task:** B01 `Select existing material writer and bounded household state ABI` (CG-B).
**Grade:** `SOURCEFREE_S2_ONLY`; no native/science/actor/human/rights/merge authority.
**Code:** `05a9b988ae039d44c55e636e1c610c01d89b4c1d` on `codex/sorok-duel-b01-a-20261112-r1`.
**Full handoff:** `AGENT_A_HANDOFF.md`.
**Machine delta:** `PROGRAMMA_DELTA.json`, `impact.json`.

## FINDING

The actual S47/P2 checkpoint writer can carry one bounded `p6_household` material fact through cold reopen, and P6 can read it as a source-qualified household with place/owner/resources. A PsycheStore `MEDIATOR` with `payload.room="kitchen"` and a CG-A-style test-local `later_decision` are ignored; when the world household is severed, the world readers refuse even though the PsycheStore decision still says `ENTER_KITCHEN`.

## ACTION

Added the bounded P2 material-fact envelope/writer (`p2_owner.py`) and the P6 household reader plus frozen parent-choice input ABI (`house.py`). `establish(session)` admits the fixture on the ordinary `new` path. No new owner, scheduler, person-world ledger, parent action or native claim.

## EVIDENCE

- B01 tests: 4 passed in 32.93s (`evidence/b01_household.log`).
- Full P6 `test_house.py`: 8 passed in 151.38s (`evidence/p6_test_house_regression.log`).
- P2 owner + actor scene + selected P3 owner reopen/config: 9 passed in 46.39s (`evidence/adjacent_regression.log`).
- Pre-existing P6 chronology proof failure reproduced identically at baseline `6a5c12f` and on this branch; disclosed, not repaired (`evidence/preexisting_p6_chronology_failure.log`).

## LIMITS

Parent first consumer is `NONE_VERIFIED` until C. No B02–B05 material surface. No crash-atomic multi-writer commit. `p2_owner.py` byte change breaks cold reopen of pre-B01 P3 state roots through the existing code pin; no migration invented. The two ChatGPT Library architecture records remain NOT_INSPECTED locally. Cost UNKNOWN.
