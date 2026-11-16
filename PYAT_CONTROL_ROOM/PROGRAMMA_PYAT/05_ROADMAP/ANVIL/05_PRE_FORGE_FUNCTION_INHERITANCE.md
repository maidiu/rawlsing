# 05 — Pre-FORGE DDM inheritance: what function must survive, what must not

**Status:** source-led reconstruction/conservation obligation, not a scientific acceptance or automatic programming backlog. This document summarizes [DDM VOSKRES #1059](https://github.com/maidiu/rawlsing/issues/1059), [VOSKRES documentary return](https://github.com/maidiu/rawlsing/blob/819dc54c69633dd75b6d13ac0ee8c3bbfd624853/WORKER_RETURNS/DDM_VOSKRES1059_HQ_R1/00_RECONCILED_RETURN.md) and [ZL-15 / #1097 full ledger](09_1097_VERBATIM_HISTORICAL_LEDGERS.md). Original source inspection, actual old execution, modern tested implementation and qualified first consumer are **different evidence grades**.

## 1. What “conservation” really means

Not retaining Python modules or matching historical number of files. A genuinely conserved analytical function preserves: **input source and scientific identity → eligible/asked/observed denominators → transformation/estimator with its meaning → output and typed negatives → provenance/parent path → actual first downstream consumer → ability to compute it economically.**

A correct new estimator need **not** reproduce a historically defective numerical answer. A reused source table is not a restored branch algorithm. A statement that modern I03 *could express* a calculation is not proof that I05/FF/N9 actually runs it and consumes its result.

## 2. Four different kinds of old DDM preparation/reuse

| Mechanism | Reused object / scope | Served products | Distinct limitations |
|---|---|---|---|
| **V550 country/question prefetch** | Source-specific country-wide selected question rows and harmonization reused across per-question calculations | country/pooled distributions, indicators, entropy, branch candidates, other V550 outputs | Fallback to per-question source SQL; no universal all-source speed or logs proving old runtime superiority |
| **V549 respondent×variable pivot and branch masks** | Respondent-wide frame and memoized parent→child masks across recursive branches | branch/co-signature, same-person conditional associations and minority selection | Blank demographic predictor inputs could make masks degenerate; V549b did not necessarily reuse V549 cache |
| **V550J source/wave/country prepared joint substrate** | Same-person inputs shared across distinct pattern/association family computations | ordered co-travel, pattern prevalence, outside-variable association with distinct respondent bases | Stale cache signature and first-row respondent-variable collapse are documented conditional defects; no assumption exact modern equivalent |
| **F26 query-response signature cache** | Query signature/results/checkpointed response, distinct from country prefetch | avoiding repeated *exactly compatible* work across calculations | Need source/rule/version/authority invalidation and first-reader proof; do not relabel V550 prefetch as F26 |

Checkpointing/resume has yet another responsibility: do not recompute completed verified question products after a restart, but **existence of a matching checkpoint name/hash is not itself proof every output body was revalidated**. VOSKRES corrected an earlier unsupported allegation that V550 lacked any guard.

## 3. Historically necessary substantive products

| Original stratum | Valuable function(s) | Scientific correction / unresolved first-reader obligation |
|---|---|---|
| V547 | position-aware distributions, mutual information and predictor/gain selection | Exact eligible population, genuine MI estimand, position role science, selected recipient |
| V548 | indicator ranking, primary/secondary, four-way majority/minority and conform/deviate branch selection | “missing” is not observed absent; correct all-row vs indicator-observed denominator; selected branch stops and bounded recursion |
| V549 | recursive branch/co-signature/association and respondent mask reuse | Proper populated predictors, parent membership and ancestry; do not equate a source-only mask with a qualified result |
| V549b | literal answer anchor, co-attitude/presence, true/false comparator and top-N | A missing answer is not observed false; precise threshold/state and correct overlap; top-N must account for omitted tail |
| V550 | per-country and pooled distributions, indicator entropy/MI/NMI, primary/secondary, output/checkpoint families, early cloud diagnostics | Old MI may mix denominators/weight regimes; V550 cloud table is not a full same-person ordered joint |
| V550J | true same-person ordered k-way patterns, component occurrences, branch-family substrate and pattern↔outside-variable association | Distinct **pattern-member**, **answered-variable**, **overlap**, **eligible-baseline** denominators; old “mutual_information” sometimes prevalence-scaled log ratio, not full MI |
| F03/F08/QRA/QUC | applied source-wave-item semantic role, six-coordinate directional vs nondirectional rules; no-match guard; specificity and conflict refusal | Must select exact rule, preserve role/review/use separation, clear or retain coordinates according to authorized semantics; not just a label |
| V551 | source-qualified candidate selection, adjudicated signed response geometry, neutral vs nonneutral, certified relation atoms, coverage | Eleven gates/science and source rules distinct; no treating neutral zero as absent or coverage as approval |
| V552 | signed component/pressure/entropy/rollup and structural handoff | score may be allowed while coverage is BLOCKED; observed output does not automatically cause structural power/hegemony claim |
| V551J | ordered component alignment, exact role/scale matching, independent certification vs review packet | A match is not automatically a certified structural spine; evidence must include no-match/review |
| V552J | join qualified J components and V552 pressure at exact source/run/country scope | Distinguish exact two-producer joins, alternative compatibility diagnostics and unmatched/held outcomes |
| V553 | sparse keyed temporal index and selected multiwave harmonization | Two authorized time anchors; no invented missing-year interpolation; temporal scope and measured changes vs structural clock |
| V554–V557 | seed-affordance/readiness/handoff and material possibility candidate | Readiness or metadata not an actor; strict keyed index/selected first reader remains required |
| V558 | audit/gate of subsequent use | Preparedness is not N11 formal adjudication or N12 independent actor grant |
| F6M/F6P | separate-survey nonpooling, partial identification, numerical upper/lower bounds, uncovered mass | No same-person merge without respondent linkage; report interval/bounds and unknown population mass |
| I07/R08/N10W and Long Memory | relation guard, signed provenance and time, actual selected first reader, atomic lifecycle | A guard receipt is not numeric science; stale/current/as-of wrong-world ref must refuse; source-derived product can be retracted |
| SOROK downstream | person-world uptake, subsequent two events, developing activity, consent/actor choices | Survey correlation is not biographical destiny; separately owned actor and material-position science |

## 4. Explicit historical mistakes that must NOT migrate

- **V548:** source-level “missing” versus observed zero/absence comparator may be collapsed; unequal all-rows/indicator-observed denominators can manufacture apparent entropy/gain.
- **V549:** blank demographic predictors can make all-false/degenerate branch masks, yet a source script can still produce plausible output. Do not pretend *all* old trees failed without executed inventory.
- **V550/V550J:** “mutual_information” labels may not implement full mutual information; some metrics conflate weighted/unweighted or overlap bases. Verify actual formula rather than variable name.
- **V550J:** stale cache signatures and first encountered respondent-variable collapse risk wrong same-person patterns.
- **V551:** signed neutral and nonneutral values need distinct rule application; review/permission/coverage distinct from whether score is produced.
- **V552:** score ALLOW and coverage BLOCKED can coexist. A single “success” boolean destroys meaning.
- **V552J/V553:** missing selected counterpart, temporal key or source comparability cannot be filled by inference; sparse time cannot become fictitious dense chronology.
- **V548 branch complexity corrections from VOSKRES:** primary-versus-secondary loop is at most k−1 candidates after one primary is selected (not universally O(k²) all-pairs); `max_depth=3` is a configurable default, not universal cap; a purity label is not proof the procedure stops when pure.
- **Historical function may not have a substantive consumer:** V552 records a conditional determinicity input in one inspected path but does not actually use it there; name a first reader before treating preserved transport as working science.

## 5. New computational requirements implied by those functions

Stage 4 needs more than cached scalar I03 queries. It needs **source/country/wave prefilter reuse; respondent-wide joint access; exact eligible/answered/overlap sets; recursive parent/child masks; conditional distribution and entropy/gain *inputs*; proper weighted arithmetic; ordered occurrence vectors; signed/role-qualified evidence; explicit multi-source nonpooling; temporal/as-of slices; checkpoint/cold-recovery of derived products; provenance and claim-grade preservation**.

The engine may store these as reusable derived structures; they are *not* a new canonical source corpus. Their **scientific use** is governed by separately qualified source rules/estimands/consumer owners, not guaranteed because computational machinery exists.

## 6. The present modern fate is not fully reconciled

- Current sourcefree I03/I05 supports exact probability/condition/joint semantics and bounded discovery. Its existence is positive capital.
- Certain retrospective ZL-15 “missing” notes were compared with an older protected cut, **not** the current `b830458c` or new `cea2d4d` candidate. Recheck exact current first consumer before asserting “missing.”
- The full #1097 ledger has 52 historical-to-modern function contracts, 24 integrated paths, **21 prospective nonadopted candidates**. They are not automatically 97 separate implementation assignments. See [verbatim snapshot](09_1097_VERBATIM_HISTORICAL_LEDGERS.md).
- VOSKRES was an **S0–S1 documentary pilot**, not a historical runtime comparison. It explicitly classified modern/historical shared-causal performance regression as **RELATED_UNPROVED**, not PROVED, absent matched workloads.
- Capability recovery must follow the **operation + scientific meaning + consumer + performance** chain, rather than porting old version names V550–V558 wholesale or regressing to historical mistakes.

## 7. Preservation against incomplete priority

The user's September-era demand covered **all** pre-553 functionality up through V558/PRE-V3, not merely GT1/GT2 F1/F2. Subsequent chosen sprint order starts with a generic economical source→C11→full joined empirical→FF/person pilot, not all35 source ingestion. That sequencing does **not** revoke eventual original35, F5–F8, multi-source/time, material-position/contradiction or actor-world obligations.

A canonical C11 can be fully persisted yet discard source role, original questionnaire semantics, occurrence identity, population survey design or wave relation required later. If these are not recoverable upstream, Stage 4 cannot recreate them. **Reverse-read the full inherited functions against the source projection before calling the 13-family interface future-complete.**
