# SOROK REMONTATHON R13 — new first faults on exact R12, code repaired and tested

**Frozen executable parent:** draft PR #1199 `9db0e6f64bf568409e638ff2215af8b8a414487f` (R12, Python 3.11 independently run 246 PASS). The R13 ZIP was derived from that exact pinned source; prior repo source/test identities checked. No changes to the original R12 receiving candidate, protected PRE-MAIN, or PROGRAMMA/current-progress pair.

## Source-level first faults and repairs

**SR-P072 — provisional trial launders durable motive via existing-project reorganization**

R12 blocks `ADD_PROJECT` and direct `TAKE_UP_POSSIBLE_END` for the current actor-issued trial, but still allowed `REORGANIZE_PROJECT` in the same `development.admit` batch. A model could rename an old project's object and motive, switch its means to the exploratory action, and reactivate a dormant project. This is the same unearned current-trial-to-mature-motive shortcut under an older ID. R13 denies `REORGANIZE_PROJECT` in any current issued-trial event, before staging, independent of labels. Historical project reorganization in a distinct **nontrial** qualified event still works. It does not establish a general psychological law, only a conservative sourcefree boundary. Tests exercise direct admission, dormant reactivation, fully connected runtime and rollback, legitimate nontrial reorganization and valid tried-but-not-motive history.

**SR-P073 — explicit falsey cue tags silently substituted with kind tag**

`ConstitutiveRuntime.cue(tags or [kind])` transformed callers' explicit `False`, `''`, and `[]` into a false historical `['kind']` tag, bypassing the R8 input-typing first gate and fabricating cues for later recruitment. R13 uses `tags is None` for the documented omitted-tags default. Invalid strings/Booleans reject before the SQLite event; an explicit empty list stays empty and an omitted list preserves the original default. No change to world-level sensory `add_cue` semantics.

## Executed negative/positive evidence and exact test counts

- Nine R13 tests run against **frozen unmodified R12**: **six FAIL, three PASS**; full red transcript retained. The failures include one whole-runtime sourcefree trial forgery and two malformed external cue cases.
- After two first-owner changes, **all nine R13 cases PASS**, and joined R12+R13 suite **255/255 PASS** in normal Python and **255/255 PASS** under `python -O`.
- `python -m pytest -q`: **255 passed + 14 subtests**. Demo executes successfully.
- Full runnable ZIP includes all R12 inherited code, tests and R13 additions, normal/optimized/pytest transcripts, red log, readme and manifest. Cold extraction should be used before independent execution; published SHA recorded in git receipt.
- R12's separate local Python 3.11.3 246 PASS proof **does not apply to R13**. Python 3.11 execution, separate reviewer hostile challenges and native/protected receiving remain pending.

## Accurate scope and custody

Candidate P072/P073 are **author-side software repairs**, not independently accepted. Existing 53 bounded independent first-fault reviews, original 8 OPEN + 8 PARTIAL, P070/P071 author-repaired pending distinct independent review, and original six E holds remain conserved. R13 adds no new psychological theory, actor power, scientific claim, administrative issuer, or protected merge. The live original #1171 queue may advance independently and must be re-reconciled before qualified receiving.
