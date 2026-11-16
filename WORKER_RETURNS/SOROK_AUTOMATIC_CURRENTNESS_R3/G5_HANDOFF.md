# SOROK automatic currentness R3 — focused G5 handoff

**Candidate:** R3 material-event authority correction on
`codex/sorok-automatic-currentness-material-auth-20261116-r3`.
**Exact source/artifact commits:** `WORKER_RETURN.json` and the HQ notification.
**Base:** `d2883f60b1f8b0d83221051844eca7e11b72dc01` (actual R2 lifecycle).
**Rejected R2 source:** `ea5e48cf3240e72e39cd19be3120ad727902eee2`.
**R2 review:** `53fad99fd8da86e4ab1cd12fdcfcd93fc8b2942f`, evidence
`f8006235266aa618963b186e5c357bf92be830b3`, `REVISE_EXACT_DEFECT`.
**Required reviewer:** same independent nonauthor
`ses_e2186e745ffecK1Ilg4cw26pVu`, or another genuinely distinct nonauthor in a
separate checkout. The author cannot self-review.

## Exact local review commands

Use the authorized Python and a separate scratch/worktree:

```text
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
CFG=/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json
```

Pin source and frozen assets:

```text
git rev-parse HEAD
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
git hash-object WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R3/tests/test_material_auth_boundary.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_task_packets_20261112.json
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_gmt_overlay_20261112.json
```

Frozen #1095 blobs must remain `d971b6ea…`, `f76c0d90…`, `17cfae53…`,
`474befcb…`.

Run the mechanism and R3 tests:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py \
  WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R3/tests/test_material_auth_boundary.py
```

Expected: `27 passed` (17 original + 10 R3).

Run the reviewer RED probe unchanged in its own scratch copy and preserve the
raw output. On the rejected source `ea5e48` it must show the four material gaps;
on this corrected source it must show `7 fixed, 0 gaps, PASS`.

```text
"$PY" WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R3/probes/material_auth_probe.py
"$PY" WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R3/probes/fake_reviewer_run_probe.py
```

Expected: material `PASS`; fake reviewer `PASS` with
`UNTRUSTED_CONTROLLER_RUN`. The probe writes its own report under its adapted
evidence directory; preserve the raw stdout/exit/time, do not edit the product.

Run the original local workflow equivalents (macOS, not GitHub Actions):

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py --self-test --status
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py --no-git --status
"$PY" -m py_compile CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py
"$PY" CROSS_HQ_CONTROL_ROOM/verify_copy_paste_commission_r1.py --self-test
"$PY" CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
"$PY" CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_pyat_product_priority_visibility_r1.py
"$PY" CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_pyat_product_priority_visibility_r1.py --self-test
```

Expected exit `0`; changed `WORKER_COMMISSIONS` remains zero. These are local
checks, not hosted-CI PASS or protected adoption.

## Actual review run

The review must be a real supervised `REVIEWER` run using the latest correctly
installed controller launcher. The binding `sorok_currentness` object is:

```json
{
  "runtime_script": "/Users/matthewsmith/.codex/worktrees/sorok1037-b-receipt-g5/Rawlsing/SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py",
  "config_path": "/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json",
  "python": "/private/tmp/rawlsing-oct28-p1r1/venv/bin/python",
  "return_filename": "WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/REVIEW_RECEIPT.json",
  "task_id": "AUTOMATIC_CURRENTNESS_R1",
  "role": "REVIEWER",
  "expected_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
  "expected_source_commit": "<R3 source commit from WORKER_RETURN.json>",
  "scope": "FOCUSED_SOURCE_CORRECTION_RECEIVING_ONLY"
}
```

HQ must launch it with the patched controller so `launch.py` attests the live
job/process tree, or explicitly enroll that already-running real job with the
HQ operator authorization. A self-consistent directory, copied run, fake PID,
tampered registry or unenrolled reviewer run is refused.

Reviewer receipt requirements:

- Commit the review evidence first; `review_commit` contains `VERDICT.json` and
  your `REVIEW_RECEIPT.json`.
- `task_id: AUTOMATIC_CURRENTNESS_R1`
- `implementation_commit`: R3 source commit
- `implementation_code_sha`: R3 runtime git blob
- `author_session: ses_e21a481bfffefyvpxaeFaAOFvQ`
- `reviewer_session`: your distinct session
- `review_commit`: frozen evidence commit
- `verdict`: `ACCEPT_SCOPED_SOURCEFREE`, `REVISE_EXACT_DEFECT` or
  `HOLD_SOURCE_AUTHORITY`
- `scope`: exact focused material-auth scope
- `full_original_claim: NOT_ESTABLISHED`
- `protected_ci: UNAVAILABLE_BILLING`
- `adoption: PENDING_PROTECTED_CI_AND_ADOPTION`
- `source_documents`: runtime/test at `review_commit`, plus `VERDICT.json`;
  the receipt verdict must exactly equal the verdict artifact. Prefixes are
  refused.

The real controller completion automatically calls
`intake-completion --run-dir <real run>`. The hook records the R3 worker return
first (`RETURNED_REVIEW_PENDING`), then the actual reviewer run records the
review verdict. Zero exit is not acceptance.

## HQ cold restart

After the real R3 worker exit and after any real reviewer run:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" startup
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
```

Verify the new generation/checkpoint, R3 `mechanism_worker_return`, the actual
review verdict, 27 task readiness, 21 decision-node holds and the visible
GitHub source holds. `status` returns `2` while reconciliation items remain.
No protected adoption, CI PASS, native science, actor/human authority or full
original claim is inferred.

## Nonclaims

No native science, actor/human authority, protected merge, hosted-CI PASS, new
ledger/world store/scheduler/fleet, account/provider change or Browser/PYAT/SEAM
operation. No #1095 G5 rerun. No automatic R3 or protected merge follows from
this handoff.
