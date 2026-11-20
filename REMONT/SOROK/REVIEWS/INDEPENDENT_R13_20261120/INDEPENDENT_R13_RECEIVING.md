# SOROK REMONT R13 — independent hostile receiving (sourcefree)

**Verdict: `REVISE_EXACT_DEFECT`** on PR #1210 at immutable HEAD `3b9b58b75bdceec901c3ba7aaa18738ea4989923`. This is a distinct assistant's actual source/test execution, not credential-independent GitHub/owner/G5 review or native science/actor authority.

## Recovered exact code and inherited positives

- The R13 Library executable ZIP `SOROK_REMONT_R13_255_TESTS.zip` independently SHA256 verified equal to the author's declared `753a841ba39e98d4e1db95a1add4e2685e9874b134439099afd4d1253e438473`.
- Executed from a clean ZIP extraction on Python 3.13.5: **255/255 normal unittest PASS**, **255/255 optimized `-O` PASS**, **255 pytest PASS + 14 subtests**.
- All **43/43** original Python files matched the R13 file identity manifest for byte count, SHA-256 and Git object SHA-1; the two corresponding GitHub Python directory trees (`tests/`, `um_sorok_organism/`) contained exactly the same 43 Python Git blobs.
- R13 `REORGANIZE_PROJECT` same-event guard rejects old-project motive/status/means rewrites. R13 `cue` now distinguishes omitted tags (`None`) from explicit invalid values. Both have positive independent inherited-suite support.
- All **71/71** production-defect records inherited from original REMONT #1171 exact `30f9ce0208bad066fe89231f0e25d75f56857700` compare identically as ordered structured records; R13 adds only `SR-P072` and `SR-P073`. P=73, T=0, E=6, prior scoped-review flag count=53, existing 8 open and 8 partial identities preserved.

## New first fault: same-event `TAKE_UP_POSSIBLE_END` can launder a parallel end

The guard in `um_sorok_organism/development.py::admit` refuses `ADD_PROJECT`, `REORGANIZE_PROJECT`, and `TAKE_UP_POSSIBLE_END` *only if its `possible_end_ref` equals the current issued trial's end ID*. This means the semantic provider can select a legitimate provisional trial of end A and, during that same event, promote **different ID B with identical meaning/object** using `TAKE_UP_POSSIBLE_END`. The owner appends a durable project, leaves A's trial legitimately recorded, and certifies a valid event chain. Merely checking end ID does not prevent current event motive promotion through equivalent paths.

**Actual runtime reproduction, without post-hoc actor mutation:**

1. `ConstitutiveRuntime.initialize()`, then material body/history background at 280 ticks.
2. A real injected `SING` experience creates possible end A (still `POSSIBLE_NOT_ACQUIRED_MOTIVE`).
3. A distinct later performed `SING` and model `NOTICE_POSSIBLE_END` create possible end B with exactly the same `possible_object`, but a distinct historically issued identity.
4. Actor callback selects a genuine runtime-offered `possible_end_trial_id` for A, while development callback supplies `TAKE_UP_POSSIBLE_END` for B.
5. **R13 actually commits the transition.** A retains a one-entry trial history as provisional; B is `TAKEN_UP_AS_PRACTICAL_PROJECT`, and a new durable project with B's ID appears in the same objective event. SQLite event chain verifies. The expected refusal test fails: `AssertionError: InvalidDevelopment not raised`.

A second owner-level negative (real `issued_trial` ticket, two earlier acquired possible ends) independently reproduces the same admission bypass. Three new positive controls pass: later *nontrial* end takeup remains possible; normal ticketed trial without takeup remains provisional; invalid explicit false/empty/bogus `tags` are rejected before a SQLite event.

**Fresh five-reviewer test results:** **3 PASS / 2 FAIL** under normal Python and optimized Python. Combined full suite **258 PASS / 2 FAIL out of 260**, normal and optimized. Pytest **258 passed / 2 failed + 19 subtests**. Both failures are the new alias-takeup authority breach, not inherited regressions or source mismatch.

## Narrow causal repair and eligibility

In the `issued_trial is not None` admission court, do **not** allow **any** current-event `TAKE_UP_POSSIBLE_END` to create a durable project from that episode, regardless of possible-end ID or object label, unless a separate, explicitly qualified historical takeup issuer has independently authorized that transition (none currently exists). Retain R6 `TAKE_UP_POSSIBLE_END` on **later nontrial** actor-owned experienced events; retain R13 `ADD_PROJECT`/`REORGANIZE_PROJECT` prohibitions and P070/P071/P073 guards. Run these reviewer cases normal/-O/pytest plus inherited tests and SQLite cold reopen after repair; independent receiving must use a new exact HEAD.

This review does **not** settle sourcefree realism of motive acquisition, model psychological validity, original P070/P071 original-author-independence, native CAN/ADP/P2–P6 ownership, G5, protected PRE-MAIN or canonical paired PROGRAMMA acceptance. Protected status is unchanged; authorized receiving remains separate under `HQ_CURRENTNESS_HOLD`. No author source files were changed by this review; reviewer-only test/evidence is attached.
