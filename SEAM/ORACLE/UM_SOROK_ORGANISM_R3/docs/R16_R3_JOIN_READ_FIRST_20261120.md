# November 21 — second executed RED and builder R3/Nadia repair

**Previous immutable executed cut:** `018d3025f0829d7b24d5ad108abf0764d3830b39`, verified locally on Python 3.11.3, [review #7058200406](https://github.com/maidiu/rawlsing/pull/1234#issuecomment-7058200406), [local evidence ledger](https://github.com/maidiu/rawlsing/blob/984d1978374767de48377f3c74deb7d73f69f393/REMONT/SOROK/REVIEWS/LOCAL_MACHINE_R12_R16_20261120/LOCAL_MACHINE_VERIFICATION_LEDGER.md). Compilation passed; 549 full `unittest` ran 5 FAIL + 22 ERROR (same normal and `-O`), pytest 27 failed/522 passed/37 subtests, and Nadia longitudinal demo stopped at `CURRENT_TRIAL_NOT_MATURE_MOTIVE`. Focused normal 137: 3 FAIL/8 ERROR; optimized 50: 2 ERROR. Original older `dbfb35c` RED remains preserved separately. R17 typed P018 repaired source and ninth test blobs were independently matched; this evidence **does not** grant a passing joined organism.

## Builder correction of the first actual source contradictions

1. **Offline heuristic violated the admissible genetic development boundary.** In `semantics.py::HeuristicSemanticProvider.propose('development')` the fallback attempted `TAKE_UP_POSSIBLE_END` on a currently actor-issued prospect trial, while `development.admit` correctly rejects same-event acquisition as `CURRENT_TRIAL_NOT_MATURE_MOTIVE`. The heuristic now reads the **already actor-issued `selected_purpose_analytic_only.status`**, marking a current `ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE`. It continues admitting a *real trial history* through the original issued-ticket recorder but does **not** propose simultaneous motive take-up. A different subsequent nontrial encounter **may** still propose uptake only if actually qualified; the existing typed development owner has final authority. Malicious/custom LLM proposals remain refused by the non-bypassable admission guard. Paired tests added to the existing joined court to assert no same-event mature project **and** preserve possibility of different-event formation.
2. **R11 test did not own its runtime fixture.** The R3 interface legitimately accepts a `practical_option_id` alone but must reject an unissued ID in `runtime._actor_plan`. The inherited R11 test now creates/initializes/closes its own temporary SQLite runtime and checks no ledger append on unissued input. No test is disabled, and no forged option admitted.
3. **Invalid sourcefree parent test packets:** R14 co-regulation, R8 lived genesis runtime, and R15 plural care each supplied `answers={}`, contrary to original `parents.construct_parent::PSEUDO_RESPONDENT_REQUIRED`. The *test fixtures only* now provide explicitly nonempirical placeholder answers and a sourcefree grade, conserving the prohibition on unqualified parent construction in the actual owner. Whether the richer constructor changes downstream test expectations must be established by retest.
4. **R6 public/private contract:** `snapshot()` materializes a model read, not the actor's complete private `activity_history`. The older R6 tests falsely accessed private episode history from this public-facing read, causing four reported `KeyError: activity_history` cases and a false-negative test for unselected projects. Tests now inspect the original private `ledger.actor('mother')[1]` owner while leaving public `snapshot()` restricted. Existing R6-integrated private-ledger tests provide the precedent.
5. **R9 P017 bounded sign duration:** `world.add_cue` already implements positive bounded persistence and rejects malformed `lasting_ticks`; joined `runtime.cue` failed to expose that parameter and raised `TypeError`. The runtime now passes `lasting_ticks=0` by default and any explicit input through to the **same existing typed world ingress**, preserving the event's signed-access window and early rejection/no-append. No duplicate clock or cue store was invented.
6. **New joined first-consumer tests:** `tests/test_r3_r18_joined_faults.py` now has **22** authored test methods (previously 20), including two explicit heuristic prospective-trial/nontrial distinctions. No new standalone test suite or parallel development owner was created.

**Grades, scope and unresolved work:** All successor repairs in this block are **`COMMITTED_UNTESTED`**; the authoritative second-run `018d3025` remains executed RED. Original remaining failures were grouped R6 4E+2F, R6-integrated 1F, R14 co-regulation 3E, R8 lived-genesis runtime 3E, R15 plural care 3E, joined demo 2E, R11 2E+1F, R9 P017 2E, Nadia backlog 1E, social-vocal 1E, whole-organism 1E+2F; every unaddressed group remains a first-fault question, **not** deemed fixed by this source edit. No source-level green or cold SQLite success is inferred.

**Next exact-head machine loop:** Re-run on a fresh detached worktree at the new SORACLE SHA: `compileall`; targeted `tests.test_r3_r18_joined_faults tests.test_r11_soracle_integrated tests.test_remontathon_r9_p017 tests.test_co_regulation_r14 tests.test_lived_genesis_runtime_r8 tests.test_plural_care_paths_r15 tests.test_intent_and_emergent_ends_r6 tests.test_intent_and_emergent_ends_r6_integrated tests.test_joined_longitudinal_demo` in normal and `-O`; full `unittest discover` both modes; pytest; direct 14 days/12 beats Nadia two-history CLI and *two cold SQLite reopens* if reached. Preserve per-command exit code, failed test names with **full tracebacks**, exact producer→first consumer, positive/negative, progress in world/actor history, and distinct historical executed SHAs. Only then repair remaining failures; do not silently move REMONT #1171's frozen old queue source pin. No protected PROGRAMMA/CURRENT_PROGRESS, native/science/actor rights, or independent receiving, `HQ_CURRENTNESS_HOLD` on operational claims.

---

# SORACLE builder repair after executed #1234 RED — November 21, 2026

**EVIDENCE CLASS: `EXECUTED_AT_SHA` RED for the immutable original `dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b`; `COMMITTED_UNTESTED` for the successor source commits below.** Do not transfer the earlier RED to the new HEAD as a new execution result; equally, do not claim that the old RED has disappeared.

**Independent local-machine return:** [#1234 exact RED](https://github.com/maidiu/rawlsing/pull/1234#issuecomment-7058012755), Python 3.11.3. The original joined candidate compiled, but normal and optimized unittest discover each reported 524 tests, 27 failures and 51 errors. Pytest failed collection with two unqualified imports. R17/P018 source raised untyped `KeyError: 'world'`; actor-issued R13 trial returned `NO_ACTION_OR_PRACTICAL_OPTION`; both 14-day Nadia counterfactual branches hit `TRIAL_MATERIAL_OBJECT_NOT_UNIQUELY_BINDABLE`; older R6/R8/R11/R12/R14/R4 tests exposed dropped source contracts. This is actual source integration RED, not GitHub Actions' earlier zero-step runner failure.

## Builder-owned direct source corrections, after original RED

The following changes were committed to **existing** SORACLE owners and inherited tests. Their presence is verified by GitHub branch commits but their complete Python integration has **not yet run**:

1. **P018 typed historical source preflight:** `storage.py` is exactly the newer REMONT R17 blob `75087ed57c3a39d82b9ded5ebf8123f949e54c21` from [R17 #1230](https://github.com/maidiu/rawlsing/pull/1230) `bd023cccea8912913ace132600c69a97b0eb6a44`, not older R18 blob `a89be36d3fe74b46f94a572be4db77941d7d9083`. Retains R17 independent source and chain preflight, now with typed malformed envelope failure. This is *source inheritance*, not proof of joined runtime parity. The original R17 ninth bad-envelope regression test was also imported unchanged: joined `tests/test_r17_source_preflight.py` now matches R17 source blob `b25f93b2fd81fa814bfeee9be843d7279cf0b31b` (9 existing cases, historical 8 retained).
2. **R13/R11 live trial-ID action selection:** `semantics.py::ValidatingSemanticService` now accepts exactly a typed `possible_end_trial_id` without a redundant `action`. The existing `runtime._actor_plan` still independently resolves the ID against the actor's own presently issued trial options, rejects unknown/ambiguous identity, mixed practical option, mismatch action and forbidden project attribution.
3. **One material thing, several psychological representations:** `runtime._bind_actor_trial_particular_object` binds one exact visible `source_material_object_ref` when R3 carries both ordinary/object-neutral and culturally learned practical alternatives for the *same* objective thing. This preserves physical identity and does not convert heard cultural meaning into a conscious end. Reject two unresolved neutral candidates, foreign objects, and mismatched project/operation. Four added joined negative/positive tests make the distinction executable.
4. **R8 P066/P067/P071 source guard conservation:** `world.py::add_cue` inherits R18 typed/no-mutation modality/tags/finite threshold guards. `constitution.py::actor_access` inherits finite embodied sensor preflight and malformed historical cue fail-closed filters **without** replacing newer R3 co-present Others, cultural objects, institutional opportunities, posted notices or situated action options.
5. **R8 P064/P065/P068 compressed life and project context:** `development.py::recurring_provisional_growth` now uses R18's actor-ID-qualified, typed, all-or-nothing sourcefree period receipt and refuses no-effect scope change. `ADD_PROJECT` and `REORGANIZE_PROJECT` only accept actual boolean `contextual_only`; no string-as-bool dormant-state fabrication. All other newer R3 developmental operations remain in place.
6. **R14/R18 selected-purpose history:** `activity.py` retains R18 existence/means validation for *all* selected projects and R3 actual projectless exploratory purpose; it restores the previously issued `ACTIVITY_PURPOSE_BASIS_CONTRADICTION` diagnostic for forged/mismatched selected-purpose envelopes.
7. **R4 fictional relational actor construction:** `semantics.py::HeuristicSemanticProvider.adult_constructor` reuses the prior R18 seed-index correspondence for explicitly fictional `relational_motifs`. Only explicitly fictional acquired forms are eligible source indices; source indices and relation-effect references are validated before becoming operative. `parents.construct_parent` remains the actual typed validating owner; no respondent unconscious-truth inference is made.
8. **Test sources:** R6 parent `answers={}` fixture was invalid under the current original pseudo-respondent qualifier and now uses an explicitly artificial one-question placeholder (following the already repaired companion). R9 pytest imports are package-qualified. One original R11 test incorrectly rejected *all* practical option IDs after R3 implemented that contract; it now positively tests the typed interface and negatively tests a forged option through the actual world runtime without event mutation.
9. **New joined first faults:** `tests/test_r3_r18_joined_faults.py` has 20 test methods, four new ones for the R13 semantic and R3 exact material object distinction. Original inherited R4/R6/R8/R11/R12/R14/R17/R18 tests are not muted or removed as a tactic to obtain an artificial green.

**Preserve negative evidence:** the red source `dbfb35c18ed0ec061050acdd1a1e5000e0bacc6b` and [REMONT review](https://github.com/maidiu/rawlsing/pull/1234#issuecomment-7058012755) are immutable historical receipts. The REMONT [local queue](https://github.com/maidiu/rawlsing/pull/1171) now intentionally defers that historical #1234 SHA in default runs. **Do not silently overwrite its pin or mark new source green.** The next run must freeze the new SORACLE builder code SHA and attach a **separate exact-SHA command/execution receipt**. If an independent REMONT later receives that candidate, it must independently challenge all repaired positive and negative contracts.

## Next exact-head builder execution, no protected promotion

Use a fresh detached worktree at this PR's next final source commit (not the frozen old `dbfb35c`), Python 3.11:

```bash
cd SEAM/ORACLE/UM_SOROK_ORGANISM_R3
python3.11 -m compileall -q um_sorok_organism
python3.11 -m unittest -v tests.test_r3_r18_joined_faults tests.test_r3_r16_joined_first_consumer tests.test_r17_source_preflight tests.test_remontathon_r18_p004_selected_means tests.test_remontathon_r13 tests.test_remontathon_r8 tests.test_remontathon_r14_activity tests.test_relational_metabolism_r4 tests.test_relational_metabolism_r4_integrated tests.test_r11_soracle_integrated tests.test_r12_independent_review_repairs tests.test_intent_and_emergent_ends_r6 tests.test_joined_longitudinal_demo
python3.11 -O -m unittest -v tests.test_r3_r18_joined_faults tests.test_remontathon_r8 tests.test_remontathon_r13 tests.test_joined_longitudinal_demo
python3.11 -m unittest discover -s tests -v
python3.11 -O -m unittest discover -s tests -v
python3.11 -m pytest -q
python3.11 -m um_sorok_organism.joined_longitudinal_demo --days 14 --beats 12
```

Preserve command exit codes, raw stderr/tracebacks, first causal RED, complete failure distribution, real Nadia world/actor history and cold SQLite verification if reachable. Only *then* repair remaining first faults in the same original owners. The working source candidate remains a non-accredited fictional research approximation; no whole-survey PYAT person, empirical psyche calibration, native actor/human rights or protected receiving is issued. **`HQ_CURRENTNESS_HOLD`** on protected SOROK paired PROGRAMMA/CURRENT_PROGRESS writer authority; this dossier and PR comment are isolated candidate currentness, not replacements for the protected pair.

---

# SORACLE builder continuation — R3 × REMONT R18, source-line corrections

**2026-11-21 · COMMITTED_UNTESTED on this joined source; no claim of completed integration.** The original joined read-first record below remains historical, not a report that its listed tests have since passed.

## Exact source corrections after original joined R18 merge

The builder inspected the R3/R18 *actual* `development.admit` first-consumer boundary and recovered two regressions against inherited REMONT R11–R13: the joined gate refused `REORGANIZE_PROJECT` and `TAKE_UP_POSSIBLE_END` on a current trial but omitted the synonymous `ADD_PROJECT` laundering path; the `RECORD_POSSIBLE_END_TRIAL` developmental operator could also be submitted without the frozen issuer ticket. A separate `runtime.cue` ingress still used `tags or [kind]`, so explicit empty or falsey tags were silently promoted to analyst kind tags, violating R13 P073.

Corrections are **committed** to these existing owners, without creating another mental store, world owner, or generic REMONT assignment:

1. `development.py::admit`: validate typed candidate list; require exactly one matching issued trial for a model-supplied trial history, or insert precisely one R3 historical record from the actual issuer when the runtime or direct caller supplies none. Reject unissued, repeated, or per-event multi-end trials. Restore R13 P072 denial of same-event `ADD_PROJECT` while retaining both `REORGANIZE_PROJECT` and `TAKE_UP_POSSIBLE_END` denial. Preserve older R13 `end` and current R3 `possible_end`+functional-bridge trial identities, and source-specific diagnostic ordering, without adopting a duplicate `record_possible_end_trial` implementation.
2. `runtime.py::cue`: distinguish omitted `None` tags (documented kind default) from explicit `[]` (actually empty). Refuse `False`, empty string, tuple, number, dict or mixed-list values as `INVALID_CUE_TAGS`, before committing any new world cue.
3. `tests/test_r3_r18_joined_faults.py`: six additional authored causal tests of atomic same-event project laundering, valid source-qualified projectless trial, single-record runtime path, forged/unissued ticket and trial, nontrial later new-project compatibility, and typed cue ingress. There are now 16 authored tests in that existing joined court, plus the inherited REMONT courts and the longitudinal Nadia demo.

**Source conservation actually inspected at this cut:** the joined `storage.py` blob is **exactly** R18's P018-preflight blob `a89be36d3fe74b46f94a572be4db77941d7d9083`; the joined cultural mediation `46597b97bff10433797c546d63ae02d030296044` and social vocal development `bf50a8edcde90503c5168bce290c1f74b6c89a7c` are exactly SORACLE R3's. The join-specific `activity.py` continues to preserve both the R18 P004 all-selected-means guard and R3 projectless trial status. This is **source parity for named blobs**, not a universal behavior/no-drop certificate.

## Execution and acceptance

GitHub Actions still does **not** establish Python execution on the joined source: runs `44863752702`, `44863752661`, and `44863752628` at the pre-documentary source code cut `ad6311189fc4459e054c0873433d800807fdd66f` completed with failure and no exposed step details. Earlier jobs had zero reported steps, and logs were inaccessible. Treat as **RUNNER/PRESTEP EVIDENCE HELD**, not Python source RED or green. No full repository checkout is available to the current connector-only builder environment; the GitHub connector permits source commits but cannot directly execute its checked-out Python tree.

A **narrow isolated author smoke** was executed with Python 3.13.5 on a manually transcribed excerpt of the admission guard and deliberately stubbed `_admit_in_place`, nine unit tests in normal mode and nine in optimized `-O`, all passing. It exercises gate logic only and **IS NOT `EXECUTED_AT_SHA` for the original repository, full world/SQLite, or the 16 authored integration tests**. It does not authorize a software-pass headline.

The next builder-owned executable boundary remains an actual exact-HEAD complete checkout, then `python -m compileall -q um_sorok_organism`, the combined R3/R18/R13-positive/negative tests, `python -m unittest discover -s tests -v`, `python -O -m unittest discover -s tests -v`, source-integrity falsifiers and the two-household Nadia longitudinal CLI with cold SQLite. SORACLE—not a generic REMONT assignment—owns ordinary initial RED repairs. A separately reproducible consequential P/T/E first fault can subsequently be submitted to independent REMONT with source and observed/expected.

**Protected PRE-MAIN, canonical PROGRAMMA and paired SOROK CURRENT_PROGRESS are unchanged.** No writer lease, independent reviewer receiving, original PYAT source/science, native CAN/ADP, actor rights, or human authorization was established: `HQ_CURRENTNESS_HOLD` for operational SOROK/PYAT HQ status. SR-P019/P022 and other original REMONT identities retain their competent ledger status; no automatic closures are asserted.

---

# SORACLE R3 × REMONT R18 — builder-owned joined organism continuation

**AUTHOR RECONCILIATION: THIS VERSION SUPERSEDES THE R16-ONLY CODE STATE DESCRIBED BELOW.** The earlier R16 evidence is retained as historical source ancestry, not as a statement of this branch's current code or test grade.

## What changed since the earlier R16×R3 two-parent source join

- **REMONT R17 source:** `6f2e98433822a4fb1246ff72c388b2e901c6ab7f` (#1230) repaired P018 by running full chain/history preflight under the original source/transaction lock before source read, late seal, or normal commit. Its exact later R18 `storage.py` blob is imported.
- **REMONT R18 source:** `a4a495bbb456bd211b4fbdbd29478c0f0052603f` (#1241), inheriting R17, repaired P004 truthful actor-policy selected-project history before any project/actor mutation. It was author-executed as 296 normal, 296 optimized, pytest 296+32 subtests **ONLY at its own R18 source HEAD**.
- **SORACLE integration author:** A true two-parent follow-up merge from the earlier R16×R3 joined code and immutable R18 source conserves R17/R18 Git ancestry and their source/negative tests. The current `activity.py` preserves newer R3 actor-purpose receipts and R18's validate-all-selected-projects-before-mutation rule. It also preflights duplicate event IDs across *all* selected projects to avoid partially appended historical activity.
- **P012 R15 repair reconstituted:** The previous R3-only motif/positive closure retained conservative potential-source veto and hence **had regressed** REMONT R15's acyclic stratified-inhibitor semantics. It now incorporates R15's fixed-point verification for acyclic inhibition chains **without retiring** R3's historically admitted REINFORCES/ACTIVATES/SUPPRESSES forms and deeper acquired motif recruitment. Cycles and support-dependency remain conservative. Do not call this parity proven before original tests execute.
- **Further SORACLE source integration repair:** R3 exploratory end trials emit `ACTOR_POLICY_PROVISIONAL_END_TRIAL_NOT_DURABLE_MOTIVE`. R16 joined `activity.py` rejected that genuine projectless status; the author adapted the existing activity owner to preserve an attempt with no forged durable purpose. No REMONT commission.
- **Builder regressions:** `tests/test_r3_r18_joined_faults.py` includes stratified inhibition/cycles, missing/incompatible/mixed projects, all-or-nothing history, projectless trial and corrupted-source preflight. `tests/test_r17_source_preflight.py` and `tests/test_remontathon_r18_p004_selected_means.py` retain the original negative courts from their own source.
- **Longitudinal first consumer:** `um_sorok_organism/joined_longitudinal_demo.py` uses two separate real SQLite worlds with otherwise matched fictional parents. Father makes the same real artifact in both; only one father publicly speaks about it. Subsequent Nadia behavior is selected by her own actor policy, not a player-scripted INSPECT. A source-qualified cultural reference must appear in the spoken-history child and not in the unspoken-history child. Then existing compressed world time, independently actor-selected beats, and cold SQLite reopen must conserve the distinct histories. This is sourcefree developmental causality, *not* a scientifically calibrated child or an adult destination.
- **New executable court:** `tests/test_joined_longitudinal_demo.py` additionally requires matched material first consumers, distinct acquisition, source/reopen, reproducibility and bounded scheduling.

**Running status as of this documentary update:** `COMMITTED_UNTESTED`. Neither this newer joint R3×R18 source nor its longitudinal demonstration has an original Python execution receipt. GitHub Actions on predecessor #1234 recorded failures with zero steps; do NOT convert them into Python RED/PASS. No local runner with a complete exact checkout has been established in this author environment. The separate R18 296 executed author cases are original-R18-only evidence, not joined-world evidence. Do not dispatch a generic REMONT request for this unfinished builder validation. SORACLE keeps first execution and normal fixes.

**Source-author owner boundaries:** The old general REMONT intake is withdrawn in [PR #1234's correction](https://github.com/maidiu/rawlsing/pull/1234#issuecomment-7056666318) under the adopted first-fault discipline. REMONT may later receive an actual pinned P/T/E first fault or independent court on an executable candidate, but does not own routine SORACLE build completion. PYAT empirically qualified original parents, P009 privacy, P018 external source issuer, original psychogenesis/LLM science, SOROK native actor owner and protected paired CURRENT_PROGRESS remain held.

**Run from `SEAM/ORACLE/UM_SOROK_ORGANISM_R3` at the exact final HEAD:**

```sh
python -m compileall -q um_sorok_organism
python -m unittest -v tests.test_r3_r18_joined_faults
python -O -m unittest -v tests.test_r3_r18_joined_faults
python -m unittest -v tests.test_r17_source_preflight tests.test_remontathon_r18_p004_selected_means
python -m unittest -v tests.test_joined_longitudinal_demo
python -O -m unittest -v tests.test_joined_longitudinal_demo
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python -m um_sorok_organism.joined_longitudinal_demo --days 14 --beats 12
```

Any first RED on the joined exact cut belongs to SORACLE's builder integration and ordinary repair, with genuine independently found first faults treated under REMONT's stricter intake charter.

---

# SORACLE R3 × REMONT R16 — historical first join (superseded code cut)

**Date:** 2026-11-20 (Eastern). **Purpose:** preserve SORACLE's current developmental organism while explicitly inheriting REMONT's real engineering corrections, NOT restart independent archaeology. The local/remote executable readback remains a requirement, not assumed evidence.

## Exact immutable entrances

- SORACLE R3 source branch / PR #1228: `f3e6a793b87605b67668c02b40543a9ca3982e51`. Distinct earlier R2/R1/R19/R20 historical and psychiatric-development line retained by first merge parent.
- REMONT R16 source branch / PR #1222: `7a8a18c153ee5a36e1c52eca15f4e5e8862296be`, inheriting R15 #1220 / R14 and preceding REMONT repairs. Retained as **second actual Git merge parent**; no R16 source history dropped.
- Verified common Git merge base before join: `5bdaaeb8a6e4fd99d76402a9c85bd1fd0f0e4400`. Different code owners diverged. New merge preserves **SORACLE's expanded psychological modules**, not a destructive wholesale replacement with the earlier R16 world.

## File-level reconciliation

The GitHub diff from the common ancestor showed 136 paths changed on each side and **14 overlapping paths**, all under `SEAM/ORACLE/UM_SOROK_ORGANISM_R3/`. Non-overlapping R16 source/test/proof artifacts have been grafted into the R3 tree (entire `REMONT/SOROK` tree plus R16-only `SEAM/ORACLE/.../` files). This includes all R16 historical test/results custody as preexisting source-specific receipts, not a new test run. For the 14 overlaps, retain SORACLE R3's developed module bodies and use source-aware explicit correction, not blind conflict resolution. THIS IS A STAGED CANDIDATE: remaining R16/P012 equivalences must be reconciled in executable tests, not declared merely from the two-parent ancestry.

Changes deliberately ported to R3's core owners:

1. `storage.py`: take the full compatible R16 ledger source blob (its public `ResearchLedger` API matches R3), preserving native SQLite atomic transactions, original R15 P018 auxiliary source seals/ownership, typed exact canonical actor/world snapshot failures, and the separate verification methods. This is a **sourcefree local integrity** improvement, never native issuer rights.
2. `constitution.py`: preserve R3's newer pre-cue pressure, developmental motif closure and relational architecture, but sort its final qualified active-form set before materializing forms. This is the necessary R16 deterministic recruitment fix, adapted to R3's different closure rather than replacing it with the older R16 algorithm.
3. `development.py`: preserve every R3 onward acquired genetic end, relational, caregiving, cultural and vocal developmental operator. Add an optional, issuer-bound current-trial gate to `admit`, refusing *any* same-event `TAKE_UP_POSSIBLE_END` and `REORGANIZE_PROJECT` when an actual actor-issued exploratory trial is active, irrespective of a different end ID. No current-trial event can be promoted into a durable end or altered project. R3's existing `RECORD_POSSIBLE_END_TRIAL` is NOT replaced or duplicated.
4. `runtime.py`: supply the actually selected `actor_attempt.practical_selection.possible_end_trial` from the pre-event actor to the atomic developmental owner. Never infer a trial from post-event narrative or a researcher's requested operation. Observers and independent nontrial actions carry `None`.

## Frozen tests and new joined first consumer

- R16: original 280 tests at the R16 author's Python 3.13.5 exact source head are **historical evidence**, not a result of this joint tree. Import its whole sourcefree test suite and R16 four targeted tests.
- SORACLE R3: Nadia-first new R3 tests previously authored but **never executed** on their then-head; preserve these and the earlier R2, R1, R20 other life tests.
- NEW `tests/test_r3_r16_joined_first_consumer.py`: full runtime parent making artifact → actual public speech → Nadia independent self-selected inspection → acquired cultural practical orientation → R16 exact ledger verification → cold reopen source-anchored child history. Also verifies current-trial inability to mint another end or reorganize projects.
- Both normal and optimized Python, pytest, independent reviewer, two-seed reproducibility and actual negative-source/P012 source-seal attacks must be run at the final joined SHA. Do not convert authored tests or earlier side-branch results into a green join.

From the source root `SEAM/ORACLE/UM_SOROK_ORGANISM_R3`:
```sh
python -m compileall -q um_sorok_organism
python -m unittest -v tests.test_r3_r16_joined_first_consumer
python -m unittest -v tests.test_r16_r12_local_machine_reconcile
python -m unittest -v tests.test_cultural_mediation_r3
python -m unittest -v tests.test_social_vocal_development_r3
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python -m pytest -q
python -m um_sorok_organism demo --db /tmp/soracle_remont_r16_r3_join.sqlite3
```

## Real remaining integration gaps

**Overlap code not yet proven behaviorally equivalent**: `activity.py`, `parents.py`, `plans.py`, `prospective_horizon.py`, `psychodynamics.py`, `relational_metabolism.py`, `semantics.py`, `types.py`, `world.py`, and changed older test bodies. The R16 source ancestry is conserved, but those R16 old code versions did **not** overwrite R3's richer current ones. Their relevant R14/R15 expectations must pass the imported negative tests; if not, repair the affected latest owner, never replay an obsolete snapshot. R15's conservative P012 inhibitor conflict and R3's motif recruitment have different implementations; a pass/fail head-to-head is mandatory.

**Provenance warning:** R16 `SOURCE_SHA256` historical source hashes refer to the ORIGINAL R16 standalone cut, not the new combined files. They are preserved as immutable reference evidence; new source digests need independent generation once a real executable runner is available.

**Authenticity/epistemic distinction:** no PYAT original-survey binding, whole survey blind parent science or native source authorization was obtained by this merge. No real LLM sampled model was run. No native privacy/actor consent/right owner is superseded by R15 sourcefree source seals. No scientific proof of human psychology or full nonlinear life.

**HQ_CURRENTNESS_HOLD:** This candidate does not have a verified incumbent SOROK HQ protected writer lease or native receiving decision. The protected PROGRAMMA SOROK front door and paired `SOROK_PRODUCT_CONTROL_ROOM/CURRENT_PROGRESS.md` / `.json` are intentionally untouched. Competent HQ/REMONT receiving must incorporate the exact final join SHA, command exits, independent reviewer and limitations into the EXISTING paired progress, and then decide protected PRE-MAIN receiving. Never invent that outcome.

**Next construction, after execution/repair:** one genuinely *longitudinal* Nadia-life scenario with actual world and independent Others, counterfactual differences in acquired ends/cultural practices/relationships, repeated cold reopening and no scripted adult destination. Protect user's Nadia-first priority from another detour into detached labor/institutional submodules.

**Disposition:** `PROVISIONAL_EXPLICIT_TWO_PARENT_CODE_JOIN__PYTHON_EXECUTION_HELD__P012_RECONCILIATION_HELD__HQ_CURRENTNESS_HOLD`.
