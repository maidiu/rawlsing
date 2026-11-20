# SOROK REMONTATHON R12 — independent R11 review defect repair

**Execution date:** 2026-11-20. **Sourcefree research implementation; no HQ accession.**

## Frozen live parents and non-overwritten owners

- R11 author candidate: PR #1190 `39f6972089858ee968e73b2e731005c71a8055dd` — parent of this R12 repair. R11 contains combined R10 #1187 and bounded SORACLE R10 trial-before-motive functions.
- Original continuing REMONT roster/source: draft PR #1171 `c0b7cd0589a7aa0ca5bd9f53c42f07ab03933ef7` at reconciliation. This includes current 71 P records and actual sourcefree P070/P071 repairs; its independently authored 53 first-fault sourcefree review is preserved, without elevating to native G5.
- Independent reviewer packet: `SOROK_REMONT_R11_INDEPENDENT_RECEIVING_20261120.zip` SHA256 `b4bdab661667214c30c568941b94d858da16804747e073eb23c5f7eace5847d4` (different author agent), `REVISE_EXACT_DEFECT`, testing frozen R11. It identified 5 failed adversarial subcases, two passing positives, and stale 69-vs-71 ledger custody. The new repair is not independently accepted by its author or by this author.
- User's separate local-machine Python 3.11.3 execution at the original frozen R11 was 232/232 normal and optimized, pytest 232 plus 10 subtests, valid 9-event SQLite ledger and cross-process cold read. **Those are R11 results only and are not misattributed to R12.**

## Actual first causes and bounded corrections

**R11-DEF-01 / P070 original storage source custody:** Ported the existing REMONT `storage.py::ResearchLedger.verify_chain` source semantics into the R11 joined owner: require exactly one matching world row; require canonical raw JSON bytes for the world and every actor; reject extra-world rosters, noncanonical whitespace and changed actor data. Exact originally approved code semantics retained; R11 retains all trial and R4–R6 mechanisms. Original P070 remains author-tested and separately awaits independent reviewer other than its original author.

**R11-DEF-01 / P071 embodied perception:** `constitution.actor_access` now uses `organism.eligible(body, 'WAIT')` to validate all finite bounded body fields *before* considering sensor thresholds. NaN cannot grant perceptual access. Original P071 still awaits independent reviewer distinct from original repair author.

**R11-DEF-02 / same-event `ADD_PROJECT` bypass:** `development.admit(..., issued_trial=...)` now prohibits ANY unqualified `ADD_PROJECT` candidate in the selected current trial event. It already blocked same-event `TAKE_UP_POSSIBLE_END`; the prior narrower guard was insufficient because a model could rename the same end and provide a new durable motive. This conservative boundary does **not** prohibit acquired projects during separately experienced nontrial events or prospectively chosen trials themselves, and is not a general psychological maturation law. Other `TRACE`/memory admissions remain staged and atomic; failed trial does not partially mutate world/actor.

**R11-DEF-03 / 69→71 queue reconciliation:** At GitHub publication, inherit the *original current* `REMONT/SOROK/OPEN_DEFECTS.md`, `.json` and existing `REVIEWS/INDEPENDENT_R9_53_20261120/` exact blobs from original #1171; preserve every P001–071 identity and its own per-record grade. Amend only additive R12 repair-status metadata and corresponding Markdown explanatory section on the isolated R12 branch; do not mark P070/P071 independently accepted, do not erase six E holds or change 8 open/8 partial statuses. The canonical protected PROGRAMMA and paired CURRENT_PROGRESS remain untouched.

## Actual execution

- Complete frozen R11 baseline rerun in this turn: **232/232 normal and optimized PASS** on extracted exact R11 archive before edits.
- Independent reviewer's actual 6-test file copied byte-for-byte into R12 `tests/test_independent_r11_receiving.py`. On unmodified R11 it reproduced **5 failing subcases** (noncanonical world, noncanonical actor, second world, NaN sensor, same-event forged motive), **2 positive tests passing**. Source red witness `R12_REVIEWER_RED_ON_FROZEN_R11.txt`.
- After source repair: reviewer same six tests **6 PASS / 0 FAIL**. Original P070/P071 3-test file from original #1171 retained **exact Git blob `c4dfd179ef3e0ea650bdaff6d8b8d27ea38e1e81`** and now passes on this R12 implementation.
- Five additional R12 tests: exact-current-trial motive, renamed-object current motive, batch rejection atomicity, genuine separately experienced nontrial ADD_PROJECT, real trial history without mature motive.
- Full combined suite: **246/246 PASS normal, 246/246 PASS `python -O`, pytest 246 PASS + 14 subtests**. (232 inherited + 6 reviewer tests + 3 original P070/71 tests + 5 new R12 tests.)
- Demo executed exit 0 and independently cold-opened using two separate runtime instances: **9 events, stable matching event IDs and last hash `27de011b1861f864b07f57f4c4ec1cd3eeb9a0488b126edf8032e594de9ae47d`, `PRAGMA integrity_check=ok`, `verify().valid=True`**. This is an R12 demo/hash, not R11's earlier `2921bbaa…`.
- These are Python 3.13.5 local author-side executions. **Python 3.11 of new R12 head and nonauthor re-review are still pending**; earlier user Python 3.11 R11 green is conserved separately.

## Addendum — independent hostile G5 correction (2026-11-20)

A separate hostile review at the exact R12 HEAD found one residual same-event motive route the original six reviewer tests did not cover: `REORGANIZE_PROJECT` could set a mature `motive` (and optionally `object`/`status`) on a pre-existing project during an issued current-trial event. `ADD_PROJECT` was blocked, but the broader project-mutation path was not.

**Source corrections:** `development.admit` now rejects `ADD_PROJECT` **and** `REORGANIZE_PROJECT` whenever an issued current-trial ticket is present, and rejects any `TAKE_UP_POSSIBLE_END` in that event. `storage.verify_chain` now emits typed `WORLD_SNAPSHOT_NOT_OBJECT` / `ACTOR_SNAPSHOT_NOT_OBJECT` errors for canonical non-object snapshots instead of an untyped `AttributeError`. `constitution.compose` now sorts the qualified active-form closure, removing hash-seed-dependent demo/event ordering.

**New regression tests:** `test_current_trial_cannot_reorganize_existing_project_into_motive` and `test_canonical_nonobject_world_and_actor_snapshots_are_typed_red` in `tests/test_r12_independent_review_repairs.py`. The hostile pre-fix runtime probe reproduced a committed mature motive while the end remained `POSSIBLE_NOT_ACQUIRED_MOTIVE`; post-fix it is `REFUSED:InvalidDevelopment:CURRENT_TRIAL_CANNOT_ACQUIRE_DURABLE_PROJECT`, no project mutation, no trial history.

**Execution after correction:** **248/248 PASS normal**, **248/248 PASS `python -O`**, pytest **248 passed + 16 subtests** on Python 3.11.3. Fresh demo runs now produce the same 9-event last hash `bc47d6102f9cf402193131bd196cb697aa47930e53ff53cc6329ef3efed5b363` across processes and `PYTHONHASHSEED` values; cross-process cold reopen and `PRAGMA integrity_check` remain valid.

The prior 246-test receipts above are preserved as historical cuts. The 71 queue_P records and six queue_E holds are unchanged; no status was self-promoted. R12 remains sourcefree author-tested, not independently accepted, and P070/P071 remain separately review-pending.

## Unresolved, preserved

R12 repairs only the independently identified three R11 defects. No claim of the whole organism being complete or of mature psychological truth. The original 8 open and 8 partial P identities remain not fixed/partial, and the 53 sourcefree bounded original first-fault review passes remain *scoped*. P070/P071 still require distinct independent acceptance; R12's new source cut requires its own independent review and protected authorized receiving. The R12 work does not include all of separately evolving SORACLE R11/R12. The six evidence/authority holds, G5, original PYAT parent source fidelity and scientifically calibrated live LLM remain open. Do not update protected PROGRAMMA or paired CURRENT_PROGRESS without authorized competent receiving.
