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
