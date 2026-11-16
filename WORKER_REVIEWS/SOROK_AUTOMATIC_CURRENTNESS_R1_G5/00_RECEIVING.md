# SOROK automatic currentness R1 — independent nonauthor receiving

**Verdict:** `REVISE_EXACT_DEFECT`
**Engineering:** `REVISE_EXACT_DEFECT`
**Scientific:** `HELD`
**Authority:** `HOLD_SOURCE_AUTHORITY`

**Candidate source:** `ac09ac7f26fa2db8950f563e8f1decb0c32f5af5`
**Main implementation:** `53dd139a7179180d2b3d52dc53a9f581f15467ba`
**Base / frozen #1095 cut:** `75581fa9e2c8576d1ca9a7a9a18759ea840d82e8`
**Runtime blob:** `6164e595efcd176bb2ec9b75aa99074472a4c9b4`
**Test blob:** `6cf53b66cf6eff3f4ced4a24f79e163ec50fd347`
**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` (distinct nonauthor)
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Checkout:** `/Users/matthewsmith/.codex/worktrees/sorok1038-custody-g5/Rawlsing`
**Branch:** `codex/sorok-automatic-currentness-independent-20261115-r1`
**Sandbox:** `.local-logs/sorok-programma-automatic-currentness-independent-20261115-r1/scratch-gap-probe/repo`

The author return, implementation, tests, installed-controller patch/backups,
real-controller-run receipts and frozen #1095 assets were read. The product is
read-only; all mutations were in an own sandbox pair/config. The author live
`currentness/config.json` and its pair were not invoked/mutated. #1095's G5 was
not rerun; its verifier, workflow and two frozen task/GMT sources remain pinned
(`d971b6ea...`, `f76c0d90...`, `17cfae53...`, `474befcb...`). Installed
controller hashes are `4c5004ef...` and `503f7b41...`; originals remain in the
author backup. The author's “real” child is a finite **fixture infrastructure**
child (`ses_local_fixture_child_r1`, `LOCAL_FIXTURE_CHILD_PROCESS_NOT_NATIVE`),
not an actual worker task return; it does not satisfy the user's worker/reviewer
mission.

## 1. Mission-critical negative: no live GitHub reconciliation

The runtime's only GitHub path is a local baseline file. There is no network or
GitHub client primitive (`evidence/live_github_absence.txt`; tokens `[]`); it
reads `_baseline_rows`, derives observations, and on `startup --reconcile` emits
`GITHUB_OBSERVATION` with `as_of = now_utc()` (`operational_currentness_runtime_r1.py:1176`,
`:1289-1305`). Consequences reproduced in the sandbox:

- Baseline file mtime `2020-01-01`; readout `authenticated_github_baseline.as_of`
  `2026-11-16T04:31:56Z`; no item. The stale local file is presented as a fresh
  authenticated checkpoint.
- Change one PR head in the local baseline (original sha
  `3996034f...` → changed sha `bfa1fb72...`); `startup --reconcile` accepts it
  as authenticated, records a new checkpoint, and returns **zero** unresolved
  items. No live GitHub source was observed.
- Keep the baseline unchanged: no item, even if actual GitHub refs/status/source
  SHA advanced or are unavailable. There is no live fetch, ref/status/sourceSHA
  freshness, expiry, or external connector feed.
- Missing baseline is detected (`AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE`, exit
  2), which is only file-unavailability detection, not source freshness.

This is the exact original user requirement missing. A local snapshot file is
not authenticated fresh online reconciliation. **Correction target:** add an
authenticated live GitHub fetch (or a wired, expiring external refreshed
connector feed) with source ref/status/SHA, fetch time, expiry, deletion/change
and unavailable detection; never stamp `as_of` from the local file; require a
fresh source observation before clearing an item. If no authenticated GitHub
connector is authorized, this edge is `HOLD_SOURCE_AUTHORITY`, not a snapshot
library.

## 2. Mission-critical negative: actual review transition cannot be intaken

`intake-review` with the required mechanism receipt (`task_id =
AUTOMATIC_CURRENTNESS_R1`) returns exit `1`,
`SOROK_CURRENTNESS_RUNTIME_RED: TASK_UNKNOWN: AUTOMATIC_CURRENTNESS_R1`.
`apply_event` calls `_task_by_id(state, receipt["task_id"])` at line 771
**before** the mechanism branch at line 775; no mechanism task exists in the 27
task list. The mechanism review state remains
`PENDING_EXTERNAL_NONAUTHOR_REVIEW`, so the required distinct actual review
event and post-review restart cannot be recorded. This is a direct executable
defect against the H5 handoff and the user’s mission. **Correction target:** handle
`MECHANISM_ID` before `_task_by_id` and bind the receipt to a real supervised
review job/immutable review evidence; never accept arbitrary caller strings.

## 3. Mission-critical negative: review/control authentication is caller-trusted

- A fabricated task receipt for C05 with `runtime_blob` source docs, arbitrary
  distinct session strings, `source_trust = REAL_LOCAL_NONAUTHOR_REVIEW`, and an
  implementation commit containing the docs was accepted: exit `0`,
  `C05.review_trust = REAL_LOCAL_NONAUTHOR_REVIEW`,
  `C05.review_sha = 4b33b8be...`. No real review job, controller completion,
  role, or operator intake exists. `_validate_review_receipt` checks only
  self-declared sessions/source_trust/local git document pins, not a supervised
  review job/evidence.
- An arbitrary `USER_STOP` event and then `USER_RESUME` event with
  `source.trust = ARBITRARY_LOCAL_TEST_STRING` were both accepted. The STOP was
  cleared, B02 changed from `STOPPED_BY_USER` to
  `CANDIDATE_RETURNED_RECEIVING_NOT_RUN`. No operator/role/evidence is required.
- An unresolved `AUTHENTICATED_GITHUB_INTAKE_UNAVAILABLE` item was cleared with
  `resolve-reconciliation --evidence "arbitrary unverified local text"
  --owner fake-operator`; exit `0`, item absent, fake resolution persisted.
- This is a public CLI authority boundary, not root-level checkpoint forging.
  **Correction target:** require a real supervised review/controller job and
  immutable evidence for review verdicts; require competent operator/HQ role,
  scope and evidence for STOP/resume/control events; reject arbitrary local
  resolve text and self-declared trust flags. Do not invent external PKI; a
  competent local controller/operator binding and source checks suffice.

## 4. What was not done (early precise stop)

Because the live-GitHub requirement and actual review-transition path fail,
this receiving does **not** spend on the author's 17 tests, full atomic crash
matrix, canonical validator, or an end-to-end success demo. The author's 17
“passed” is author evidence only; it is not an independent pass and does not
cover these mission failures. The runtime's baseline/file-unavailability,
REVISE/self-review/wrong-document, mixed-pair, basic transaction and historical
replay behaviors are present in source/tests, but the failed edges above are
enough to return `REVISE_EXACT_DEFECT`. No full original mechanism is accepted.

## 5. Historical boundaries preserved

The sandbox readout retains the seven protected P3/P4/P5/P6/MI/MII/MIII
foundations with their exact merge SHAs; #939 controller STOP, Browser
#1008/#1010 typed ownership, #1012 not launched; B05/C04/C05 scoped review pins;
#1066 CG-A typed `RECEIVED_SCOPED_UNMERGED_PR1066` (outside the 27 DAG, no full
source pin in this runtime). Historical reviews are explicit replays, not new
reviews. Required hosted CI remains
`PENDING_PROTECTED_CI_AND_ADOPTION`/`UNAVAILABLE_BILLING`; no protected merge or
native/science/actor/human authority is claimed.

## 6. Correction priority and STOP

1. Make the mechanism review intakable and bind it to a real supervised
   nonauthor review job/evidence (not caller session/trust strings).
2. Add authenticated live GitHub/currentness fetch or an authorized expiring
   connector feed; no local-baseline `as_of=now`; no self-clearing.
3. Bind STOP/resume/control and reconciliation resolution to competent
   operator/HQ role/scope/evidence.
4. After correction, one bounded focused rereceiving of the exact fixed source,
   with a real review event and fresh-process restart, is required. No
   automatic author round, campaign, protected merge or B05 reopen.

**Receipt:** `REVIEW_RECEIPT.json` at the evidence commit, with the final receipt
committed separately; `review_commit` points at the frozen evidence commit, not
a self-reference. The runtime currently cannot intake it (`TASK_UNKNOWN`); HQ
must correct that before any post-review restart. STOP.
