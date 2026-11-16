# SOROK automatic currentness R2 — focused independent receiving

**Engineering:** `REVISE_EXACT_DEFECT`
**Scientific:** `HELD`
**Authority:** `HOLD_SOURCE_AUTHORITY`
**Full original claim:** `NOT_ESTABLISHED`
**Accept scoped:** `false`

**Reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` (distinct nonauthor)
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ`
**Corrected implementation:** `ea5e48cf3240e72e39cd19be3120ad727902eee2`
**Worker artifact commit:** `20ae27f802a863370d215d9f4b7ed44e76c54da3`
**Final author report:** `d71d52a5cf0c604a0738c0928bcf2b7e7ea8eb12`
**Runtime blob:** `d06cd8a9a736fac728ea6b5ea2c098aa4986cfa0`
**Test blob:** `202e81d85d78e4d158a43bfcfa55a818149bf8fd`
**Predecessor RED:** `fc49662603c3dd8148c847cd6f35f2172184fd5a` / #1102
**Review job:** `sorok-programma-automatic-currentness-r2-receiving-20261116-r1`
**Review run:** `/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-programma-automatic-currentness-r2-receiving-20261116-r1`
**Receipt bound path:** `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R2_G5/REVIEW_RECEIPT.json`

This is one focused receiving of the corrected source, not a #1095 G5 rerun and
not a review-of-review. The R1 adverse verdict is preserved; this verdict is
tied only to `ea5` and the exact source pins above. Product was read-only. All
mutations were in reviewer-owned sandbox pairs/configs under the R2 lease.
The author live pair/config was read for custody only and was never edited or
used as a mutation target.

## 1. The five R1 reds are materially repaired

1. **Stale local baseline no longer becomes live freshness.** The corrected
   runtime performs authenticated live `git ls-remote` plus GitHub API reads
   through the existing credential helper. Actual sandbox observation:
   `AUTHENTICATED_LIVE_GITHUB`, 16 refs, repo read `200`, PR reads
   `1062/1066/1089/1091/1095 = 200`, issue reads `939/1008/1010 = 403`,
   coverage `REF_SHA_ONLY`. The local baseline mtime was 2020; the live
   observation carried its own `fetched_at_utc`, `expires_at_utc` and
   `evidence_digest`. Changing a local baseline head produced
   `LOCAL_GITHUB_BASELINE_BRANCH_UNAVAILABLE pr:1062`, not a fresh checkpoint.
   The four current items stayed visible:
   `issue:939`, `issue:1008`, `issue:1010` and
   `GITHUB_PR_STATUS_ADVANCED pr:1095`.
2. **Mechanism review is no longer `TASK_UNKNOWN`.** A caller-only mechanism
   receipt now refuses `REVIEW_SUPERVISED_RUN_REQUIRED`. The old R1
   `TASK_UNKNOWN` ordering defect is gone.
3. **Fabricated ordinary task review is refused.** The unchanged R1 probe's
   fake C05 receipt exits `1` with `REVIEW_SUPERVISED_RUN_REQUIRED`; the C05
   task is not promoted.
4. **Arbitrary STOP/RESUME is refused.** The unchanged R1 probe's fabricated
   `USER_STOP`/`USER_RESUME` events produce no stops and no B02 transition.
   An authorized positive stop/superseding resume was independently exercised
   and did transition B02/B04/B05 and restore them.
5. **Arbitrary resolution is refused.** The unchanged R1 probe leaves the
   reconciliation item in place; CLI resolution without authentication exits
   `RESOLUTION_AUTHENTICATION_REQUIRED`. A fresh live observation digest did
   resolve the exact `pr:1095` item in a separate sandbox.

The unchanged R1 probe was copied byte-identically (`sha256
7f55b507381fc7e907a0cbb755b65006b44356885a18195ba2ab69a4a2ccaa85`) and
only its own scratch/tmp/evidence paths were adapted. Its raw exit is `0`
because the historical probe hardcodes `REVISE_EXACT_DEFECT`; its raw
outcomes are the evidence, not a green product claim.

## 2. Remaining material-event authority REDs

The five primary R1 reds are repaired, but the required “all material event
kinds” boundary is not:

- `REJECTION` is still an unauthenticated public `intake-event`. A fabricated
  event changed B01 to `REJECTED` (exit `0`), while B01 remained
  `READY_FOR_SCOPED_ENGINEERING`. This is a blind public rejection transition.
- `PROTECTED_INTEGRATION` is still an unauthenticated public event. A
  fabricated B05 event with `ci_state=PASS` and merge SHA `ffff…` was accepted
  (exit `0`) and set `protected_integration=PROTECTED_SOURCEFREE`,
  `protected_ci=PASS`, `protected_merge_sha=ffff…`. No protected CI or merger
  authority was checked.
- `GITHUB_OBSERVATION` is still accepted from public `intake-event` without
  authenticating its source or digest. A fabricated observation with
  `source_identity=FAKE_SOURCE`, future expiry and `evidence_digest=evil` was
  stored as `authenticated_checkpoint.live_github` (exit `0`).
- A self-consistent fabricated controller run and a fabricated
  `WORKER_RETURN.json` were accepted by `intake-completion` (exit `0`); the
  runtime recorded `mechanism_worker_return` for `ses_FAKE_WORKER_NO_PROCESS`,
  even though PID `99999` was not a real process. `validate_controller_run`
  checks JSON self-consistency, hashes and a worktree, but not a trusted
  controller root or the actual launched process.
- A fully self-consistent fabricated REVIEWER run and fake `VERDICT.json` were
  accepted by `intake-review --review-run-dir` (exit `0`), moving
  `mechanism_review` to `ACCEPT_SCOPED_PENDING_HQ_ADOPTION` for the fake
  commit `2b068c60…`. This is the strongest residual breach: a local caller
  can mint the actual supervised-review transition the mission requires.

These are code/authority gaps, not source-authority data gaps. The shortest
runnable correction is to authenticate REJECTION, PROTECTED_INTEGRATION,
GITHUB_OBSERVATION, WORKER_RETURN and REVIEWER runs against a trusted
controller/role/source/process/immutable-artifact boundary, and to require
exact verdict equality rather than `startswith` (`_verify_verdict_artifact`).
No new PKI is required; a real controller root/process and competent role
binding are sufficient for this local mission.

## 3. Live source and source-authority holds

The live connector is not a static library: it really fetched live refs and
PR status. The issue/comment `403` responses are an existing credential-scope
blocker, not a fake observation. They remain explicit
`GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE` items, not READY. The real
`pr:1095` status/updated advance is also visible. Therefore:

- Currentness of refs/SHA and four watched PR statuses is demonstrated for
  this observation.
- Full issue/comment currentness is **not** certified; it is a source-authority
  hold for the connector scope.
- No GitHub Actions or hosted CI is claimed. Required CI remains
  `UNAVAILABLE_BILLING` / `PENDING_PROTECTED_CI_AND_ADOPTION`.
- No protected merge/adoption, native science, actor knowledge, or human
  authority is claimed.

## 4. Real lifecycle custody

The actual author R2 job
`sorok-programma-automatic-currentness-repair-20261115-r2` (session
`ses_e21a481bfffefyvpxaeFaAOFvQ`, PID 69246) completed and the installed hook
recorded `controller_integration.hook_state =
REAL_MECHANISM_WORKER_RETURN_INTAKEN`. The author live pair generation 49 has
`mechanism_worker_return.execution_state = RETURNED_REVIEW_PENDING`, exact
`ea5` implementation, runtime/test blobs, return SHA
`7403e06e…`, and controller run receipts. The prebound review job
`CURRENTNESS_R2_G5` is bound to this reviewer, task
`AUTOMATIC_CURRENTNESS_R1`, expected source `ea5`, and the receipt path above.
This is not a fixture. The old R1 author/reviewer runs are retained as
provenance.

## 5. Historical and dependency boundaries

PR #1098 OATH R2 (`1341c81d…`) remains a draft, and PR #1100 atlas
(`67698cfd…`) remains a documentary candidate; neither is treated as
protected law. The reviewed state preserves 27 `B01–G04` tasks, 21 G/M/T decision nodes,
144/38/83/304/100 original scope, seven protected P3/P4/P5/P6/MI/MII/MIII
foundations, B05 #1089 / C04 #1062 / C05 #1091 scoped review pins, CG-A #1066
outside the 27 DAG, G03-I0 `RECEIVED_SCOPED_UNMERGED_PR993` with full G03
held, Browser #1008/#1010 terminal and #1012 not launched, and #939
`USER_STOP_AFTER_ORIGINAL_ASSIGNMENTS` with `persistent_dispatch=false`.
B05 R3 scoped acceptance is not a full-claim or protected claim. A revocation
of B02 blocked B04/B05 transitively; an authorized stop then superseding
resume restored descendants. No auto-dispatch is inferred. No documented
revocation-restoration event was found; that remains outside the demonstrated
scope rather than being silently treated as recovery.

## 6. Local checks (macOS, existing Python; not GitHub Actions)

All commands used the reviewer venv and reviewer scratch. The 17-test file
passes only when `TMPDIR` is under the checkout so its temporary sandbox has a
git ancestry; with the default macOS TMPDIR, three tests fail
`REVIEW_COMMIT_UNAVAILABLE` because their fixture root is not a git repository.
The corrected-TMPDIR run is the meaningful local run:

- `pytest ... test_operational_currentness_runtime_r1.py`: **17 passed**,
  exit `0`, 13.61s.
- Frozen #1095 verifier `--self-test --status`, plain, and `--no-git --status`:
  exit `0` each.
- `py_compile CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py` and
  its `--self-test`: exit `0` each.
- `verify_canonical_programma_r1.py`: exit `0`.
- `verify_pyat_product_priority_visibility_r1.py` plain and `--self-test`:
  exit `0` each.
- Workflow selector: no changed `WORKER_COMMISSIONS/` launch files; MCR
  source-check not applicable.
- Author R2 correctness probe: `PASS` (8 checks), but it does not cover the
  residual material-event authority gaps above.
- Cold live startup/status/what-next: exit `2` while the four source items
  remain visible; `recommended_next` is B01 `RECEIVE` with its owner and
  prerequisites; live observation digest/time persisted across the follow-up
  status without being reset from the baseline file.

## 7. Verdict and STOP

Engineering is **REVISE_EXACT_DEFECT** because a caller can still mint
rejection, protected integration, live GitHub observation, worker return and
supervised review authority. The fixed five R1 edges are acknowledged; they
are not enough for the complete mission. Scientific authority remains HELD.
Authority remains `HOLD_SOURCE_AUTHORITY` for the live issue/comment connector
scope, with no claim of full currentness. This is a finite code correction,
not another author cycle or campaign. After correction, one focused rereceiving
of the exact fixed source is required. **STOP.**
