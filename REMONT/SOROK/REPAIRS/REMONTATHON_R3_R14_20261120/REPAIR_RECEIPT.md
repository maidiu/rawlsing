# SOROK REMONTATHON R14 — tested first-owner repair receipt

**Base:** draft #1210 `3b9b58b75bdceec901c3ba7aaa18738ea4989923` (R13 255-sourcefree test cut). No protected code changed.

## First faults independently reproducible from source

**P012 — two-stage fixed point drops motif-activated downstream machinery.** Previous `constitution.compose` first reached closure of direct cue/form links, computed an inhibitory veto, and made a *single* direct pass over relational motif candidates. Once a motif recruited an acquired form, that form's own `RECRUITS`/`SUPPORTS` edges and further qualified motifs were not traversed. Likewise a motif-recruited form with an acquired `INHIBITS` edge could leave its target falsely directly active, potentially unlocking behavior. Four new tests reproduce these failures. Repair: bounded relational-plus-positive closure, conservative potential-reachability veto, recomputed actual closure, and preserved motif receipt for newly recruited qualified forms. Does not create absent forms, alter world authority, or bypass bodily/location constraints.

**P004 — contradictory purpose selection pollutes activity history.** `activity.record_activity_afterlife` previously extracted `project:` references from `basis` and wrote per-project histories even when a separately supplied actor-policy purpose selection explicitly said **no** projects had been chosen, or named a different selection. A public injected action could therefore be misrepresented as actor-selected purposeful conduct by the direct owner function. Three new negatives reproduce this. Repair: exact match between issued selected project IDs and basis project tags (and consistent single/multiple/no-purpose selection grade); reject malformed or contradictory receipts prior to any history append. Preserve legitimate multi-project selections and separately disclosed legacy `purpose_selection=None` helper calls.

## RED–GREEN
- Frozen **unmodified R13 source** + new R14 test files: **10 tests / 7 FAIL / 3 PASS** (`R14_RED_ON_FROZEN_R13.txt`).
- R14 executable changes: `um_sorok_organism/constitution.py`, `um_sorok_organism/activity.py`; new tests `tests/test_remontathon_r14_recruitment.py`, `tests/test_remontathon_r14_activity.py`.
- Full suite author executed **265/265 normal PASS, 265/265 optimized PASS, pytest 265 pass + 14 subtests**; new 10/10 PASS; demo EXIT 0 with a valid chain and cold reopen.
- All 45 Python files byte-identified in `R14_SOURCE_SHA256.json`; fresh extraction test receipt to accompany package.

## Limits and custody
- P004 and P012 are **still PARTIAL**, not closed. P004 still needs development of historically generated actual motive/object relations, P012 still uses conservative over-inhibition and provisional motif science rather than a complete contradiction calculus.
- P019 and P022 explicitly handed off to SORACLE; no code included or status changed. P013/014/015/016/020/023 etc are untouched.
- All prior 73 original P identities and six E holds conserved; latest original REMONT `remont_r12_r2_trial_reorganization_repair` receipt should be inherited separately with clear provenance and *no duplicate P072 credit*.
- Author-tested **SOURCEFREE**, independent R14 review and Python 3.11 R14 run outstanding, no G5, protected PRE-MAIN, native P2–P6, SOROK PROGRAMMA / CURRENT_PROGRESS receiving or whole-person scientific accreditation.
