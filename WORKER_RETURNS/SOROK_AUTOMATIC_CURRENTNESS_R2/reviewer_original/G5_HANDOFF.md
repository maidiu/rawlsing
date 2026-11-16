# SOROK automatic currentness R1 — G5 handoff (not accepted)

**Verdict:** `REVISE_EXACT_DEFECT`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu`
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Candidate source:** `ac09ac7f26fa2db8950f563e8f1decb0c32f5af5`
**Main implementation:** `53dd139a7179180d2b3d52dc53a9f581f15467ba`
**Base / frozen #1095:** `75581fa9e2c8576d1ca9a7a9a18759ea840d82e8`
**Runtime blob:** `6164e595efcd176bb2ec9b75aa99074472a4c9b4`
**Test blob:** `6cf53b66cf6eff3f4ced4a24f79e163ec50fd347`
**Evidence commit:** this frozen review commit (the receipt `review_commit`
points here; final receipt is committed separately)
**Receipt path:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R1_G5/REVIEW_RECEIPT.json`
**Grade:** `SOURCEFREE_S2_ONLY`
**Full original claim:** `NOT_ESTABLISHED`
**Protected CI:** `UNAVAILABLE_BILLING`
**Adoption:** `PENDING_PROTECTED_CI_AND_ADOPTION`

## Exact mission gaps

1. **Mechanism review cannot be intaken.**
   `intake-review` with `task_id = AUTOMATIC_CURRENTNESS_R1` exits `1` with
   `SOROK_CURRENTNESS_RUNTIME_RED: TASK_UNKNOWN: AUTOMATIC_CURRENTNESS_R1`.
   `apply_event` calls `_task_by_id` at
   `operational_currentness_runtime_r1.py:771` before the mechanism branch at
   `:775`. The required actual independent-review event and post-review restart
   are not executable. The sandbox mechanism state remains
   `PENDING_EXTERNAL_NONAUTHOR_REVIEW`.
2. **No live GitHub reconciliation.** The runtime reads only a local baseline
   file (`_baseline_rows`, `:1176`), derives observations, and `startup
   --reconcile` stamps `as_of = now_utc()` (`:1289-1305`). There is no network or
   GitHub client primitive. A baseline with mtime `2020-01-01` read as
   `2026-11-16T04:31:56Z`; changing a local PR head was accepted with no live
   observation and zero unresolved items; an unchanged stale baseline also gives
   no item. Missing file is detected, but freshness/advance/unavailability is
   not. This fails the user’s required GitHub-since-checkpoint check.
3. **Review/control authentication trusts caller fields.** A fabricated C05
   review receipt with arbitrary distinct session strings,
   `source_trust=REAL_LOCAL_NONAUTHOR_REVIEW`, and a commit containing the source
   docs was accepted (exit 0; C05 review trust set). No supervised review job,
   controller completion, role, or operator intake exists. `_validate_review_receipt`
   checks only caller fields/git document pins.
4. **Arbitrary STOP→RESUME/control intake.** `USER_STOP` and `USER_RESUME` events
   with `source.trust=ARBITRARY_LOCAL_TEST_STRING` were accepted. STOP count went
   `1 → 0`; B02 changed from `STOPPED_BY_USER` to
   `CANDIDATE_RETURNED_RECEIVING_NOT_RUN`. No operator/role/evidence is required.
5. **Arbitrary reconciliation resolution.** A persisted
   `AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE` item was cleared with
   `resolve-reconciliation --evidence "arbitrary unverified local text"
   --owner fake-operator`; exit 0; item count `1 → 0`; fake resolution persisted.

## Exact correction targets

- Fix mechanism review dispatch ordering and bind the mechanism receipt to a real
  supervised nonauthor review job/immutable review evidence and competent HQ
  intake role. Do not accept caller session/trust strings.
- Add an authenticated live GitHub fetch or a wired, expiring external connector
  feed with ref/status/source SHA, fetch time, expiry and missing/change/
  unavailable detection. Never stamp `as_of` from a local baseline file. Clear an
  item only after a fresh source observation or a competent source HOLD.
- Require competent operator/HQ role/scope/evidence for USER_STOP, USER_RESUME,
  REVOCATION and SOURCE_AUTHORITY_HOLD; reject arbitrary local event JSON.
- Require authenticated evidence for reconciliation resolution; reject arbitrary
  local text.
- If no authenticated GitHub connector is authorized, return exact
  `HOLD_SOURCE_AUTHORITY` for that connector; do not substitute a snapshot.

## What was not done

The author’s 17 tests, full atomic crash matrix, canonical validator and
end-to-end success demo were **not** independently run because the live-GitHub
and actual review-transition requirements fail first. The author’s 17-pass claim
is author evidence only and does not cover these gaps. No full original
mechanism is accepted.

## Historical boundaries

The sandbox readout preserves seven protected P3/P4/P5/P6/MI/MII/MIII merge
SHAs; #939 `USER_STOP_AFTER_ORIGINAL_ASSIGNMENTS` and
`persistent_dispatch=false`; Browser #1008/#1010 typed ownership and #1012 not
launched; B05/C04/C05 scoped review pins; #1066 CG-A typed
`RECEIVED_SCOPED_UNMERGED_PR1066` outside the 27 DAG; required CI remains
`PENDING_PROTECTED_CI_AND_ADOPTION`/`UNAVAILABLE_BILLING`. Historical #1089/
#1091/#1062 intakes are explicit replays, not new reviews. #1095’s G5 was not
rerun; its verifier/workflow/two frozen task sources remain pinned.

## HQ post-review route

After correcting the five gaps, run one focused rereceiving of the exact fixed
source. The reviewer receipt at this path must be intakable by the corrected
runtime; only then may HQ run `intake-review`, fresh-process `startup`/`status`,
and bank the scoped result. Do not claim protected adoption, hosted-CI PASS,
native/science/actor/human authority, or auto-dispatch. STOP.
