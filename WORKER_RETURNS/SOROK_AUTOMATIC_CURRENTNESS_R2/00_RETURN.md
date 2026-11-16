# SOROK automatic currentness R2 — corrected author return

**Engineering:** `AUTHOR_CANDIDATE_FOR_FOCUSED_INDEPENDENT_RERECEIVING`
**Scientific:** `HELD` | **Authority:** `HOLD_SOURCE_AUTHORITY`
**Issue:** SOROK automatic PROGRAMMA currentness (R2 correction after #1102/fc496)
**Author session:** `ses_e21a481bfffefyvpxaeFaAOFvQ` (same implementer)
**Job:** `sorok-programma-automatic-currentness-repair-20261115-r2` (active PID `69246`)
**Base rejected source:** `ac09ac7f26fa2db8950f563e8f1decb0c32f5af5` / #1101
**Branch:** `codex/sorok-automatic-currentness-repair-20261115-r2`
**Exact source commit / artifact SHA:** reported in `WORKER_RETURN.json` and the final HQ notification.
**Terminal:** one frozen corrected candidate for the same nonauthor; no automatic R3.

## Received independent RED (unchanged)

Reviewer `ses_e2186e745ffecK1Ilg4cw26pVu` returned `REVISE_EXACT_DEFECT` at
`fc49662603c3dd8148c847cd6f35f2172184fd5a` (#1102). The complete receiving,
VERDICT, handoff, receipt, gap probe and report were read and preserved under
`reviewer_original/`. The reviewer’s old probe and original RED report are kept
byte-identically; only its own scratch path was adapted for re-execution. The
reviewer files were not modified.

## Five corrections actually implemented

1. **Live GitHub currentness.** The runtime now fetches authenticated live
   GitHub refs/SHAs through the existing git credential helper and live PR
   status/updated/SHA through the available GitHub API in memory. A local
   baseline is only an expected-ref set, never a fresh source stamp. Actual
   observation at `2026-11-16T05:15:16Z` (expires `05:30:16Z`, evidence
   `b022f8ae…`) fetched 16 live refs, repo/commit reads `200`, and PR status
   `200` for #1062/#1066/#1089/#1091/#1095. It detected the real PR #1095
   status/updated advance (`GITHUB_PR_STATUS_ADVANCED pr:1095`) and kept the
   local baseline tamper/advance/delete cases visible. Issue/comment reads return
   HTTP `403` with the existing connector scope, so
   `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:939/#1008/#1010` remain
   explicit source-authority holds; the local snapshot is not used to clear
   them.
2. **Mechanism review intake.** `MECHANISM_ID` is handled before the ordinary
   27-task lookup. A non-replay mechanism review is intakable only through a
   real supervised controller REVIEWER run with matching role/task/session/
   source, completion/job/grant/argv/worktree/recipient binding, immutable
   review artifact and reviewed `VERDICT.json`; a caller-only JSON/trust string
   refuses `REVIEW_SUPERVISED_RUN_REQUIRED`. The original ac09 `REVISE_EXACT_DEFECT`
   review is recorded separately as a posthoc real controller-run history, not
   as acceptance of the corrected source and not as automatic intake.
3. **Review authenticity.** Caller-declared `REAL_LOCAL_NONAUTHOR_REVIEW`
   strings, arbitrary distinct sessions and source-doc git pins are no longer
   sufficient. Non-replay review requires the supervised run/role/scope/source
   binding above plus a reviewed verdict artifact; a receipt that points only at
   source code is refused.
4. **Control authentication.** USER_STOP, USER_RESUME, REVOCATION and
   SOURCE_AUTHORITY_HOLD require a competent local operator/source-authority
   authorization file bound in the runtime config, exact kind/scope/evidence
   digest and expiry; arbitrary public CLI event JSON refuses
   `OPERATOR_AUTHORIZATION_UNAVAILABLE`. Resume requires the exact superseded
   stop and later order. Controller job roles do not mint source/science/actor
   grants; #939 STOP remains preserved and never dispatches.
5. **Resolution authentication.** Arbitrary `--evidence`/`--owner` text cannot
   clear a reconciliation item. Resolution requires a fresh live observation
   digest matching the exact item, or a competent operator/source-authority
   authorization tied to the exact unresolved source/digest/checkpoint. Legacy
   arbitrary resolutions are re-opened as `LEGACY_UNVERIFIED_RESOLUTION` history
   and are not silently mapped to READY.

## Real worker transition (this continuation, not a fixture)

HQ prebound this actual OpenCode job to the installed controller hook, runtime
config and `sorok_currentness` role `IMPLEMENTER`, task
`AUTOMATIC_CURRENTNESS_R1`, expected session and return path
`WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/WORKER_RETURN.json`. The real
controller run is under
`/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-programma-automatic-currentness-repair-20261115-r2`
with real job/binding/launch/process receipts. `WORKER_RETURN.json` is committed
with the exact implementation commit, code blobs, role/session and return path
hashes. The already-loaded R1 observer calls the compatible
`intake-completion` command; on process exit the corrected runtime must record
this completion as `mechanism_worker_return.execution_state =
RETURNED_REVIEW_PENDING`, never as acceptance or infrastructure-only. HQ must
observe the notification and run the cold readout commands in `G5_HANDOFF.md`.
The old R1 author/reviewer completions are retained as provenance, not as the
current worker.

## Dependency and 21-node reevaluation

The runtime keeps the original 27 B01–G04 task edges/classes and now also loads
the frozen 21 G/M/T decision nodes. It separately types settled law, executive
choices, open scientific mechanisms and source-authority holds. Scoped accepted
B05/C04/C05 remains `SCOPED_RECEIVED_UNMERGED`/`PENDING_PROTECTED_CI_AND_ADOPTION`;
full original task claims and native science remain `NOT_ESTABLISHED`. The
readout includes exact unmet full-claim decision IDs (e.g. B05 `A02,A03,A08`)
without manufacturing READY. Unknown semantic/gate inputs remain explicit HOLDs.
The dated atlas
`67698cfd32f838b7a5fdc381b0168d9225f5352f:SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/32_OPERATIONAL_GMT_WORK_DEPENDENCY_AND_RECEIVING_20261115_R1.md`
is cited as candidate documentary evidence, not protected law. OATH R2 at
`1341c81dfe0e99da030e7dca356f55789a10c6f8`/PR #1098 remains draft, not
protected operating law.

## Current visible gap (not hidden)

The R1 pair’s old “no unresolved” checkpoint is rejected as current truth. The
corrected reconcile is generation `48`, checkpoint `20b7a8e3…`, with four
visible items:

- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:939`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1008`
- `GITHUB_STATUS_UPDATED_SOURCE_UNAVAILABLE issue:1010`
- `GITHUB_PR_STATUS_ADVANCED pr:1095` (real live updated-at advance)

These remain `RECONCILIATION_REQUIRED`; none is mapped to READY. The old R1
failed infrastructure attempts and legacy arbitrary resolutions are resolved by
an explicit local HQ operator authorization with exact completion/source
digests, not arbitrary text; their history remains visible in
`reconciliation_resolved`.

## Preserved boundaries

- Frozen #1095 verifier/workflow/two sources and its reviewed static projection
  are untouched; no #1095 G5 rerun.
- Seven protected P3/P4/P5/P6/MI/MII/MIII foundations; B05 #1089, C04 #1062, C05
  #1091 scoped review pins; #1066 CG-A and G03-I0 scoped; #939 STOP; Browser
  #1008/#1010 terminal scoped/held and #1012 not launched.
- Required CI remains `PENDING_PROTECTED_CI_AND_ADOPTION`/`UNAVAILABLE_BILLING`;
  no hosted-CI PASS and no protected merge.
- Native science, actor/human authority and protected adoption remain HELD.
- Four #1095 minor documentary notes are retained as nonblocking history.

## Local executable checks (macOS, existing Python; not GitHub Actions)

- Frozen #1095 verifier: `--self-test --status`, plain and `--no-git --status`
  all exit `0`.
- `py_compile CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py` and its
  `--self-test` exit `0`.
- `verify_canonical_programma_r1.py` exit `0`.
- `verify_pyat_product_priority_visibility_r1.py` plain and `--self-test` exit
  `0`.
- MCR changed-commission selector: zero changed `WORKER_COMMISSIONS/` launch
  files; source-check not applicable.
- Runtime tests: 17 passed. New correctness probe: PASS. Reviewer’s unchanged
  old gap probe: raw outcomes show fake task review refused, mechanism review
  `REVIEW_SUPERVISED_RUN_REQUIRED`, arbitrary STOP/RESUME refused, arbitrary
  resolve refused, and live-source tokens present; its hardcoded historical
  `REVISE_EXACT_DEFECT` verdict is retained, not called green.

## Exact evidence

`EVIDENCE.json`, `evidence/`, `reviewer_original/`, `probes/`, `fixtures/`,
`WORKER_RETURN.json`, and the raw logs listed in `EVIDENCE.json`.

## Holds / STOP

Remaining: live issue/comment status connector scope, real PR #1095 status-change
reconciliation, actual independent review of this corrected source through a
supervised REVIEWER run, protected CI/adoption, and native/science/actor/human
authority. Author cannot self-review. STOP at this frozen corrected candidate;
no automatic R3, no fleet/Browser/PYAT/SEAM operation, no protected merge.
