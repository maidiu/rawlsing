# SOROK automatic currentness R2 — focused G5 handoff

**Candidate:** corrected source on
`codex/sorok-automatic-currentness-repair-20261115-r2`; exact source commit and
artifact commit are in `WORKER_RETURN.json` and the HQ notification.
**Rejected predecessor:** `ac09ac7f26fa2db8950f563e8f1decb0c32f5af5` / #1101.
**Independent RED:** `fc49662603c3dd8148c847cd6f35f2172184fd5a` / #1102,
`REVISE_EXACT_DEFECT`, preserved under `reviewer_original/`.
**Required reviewer:** same independent nonauthor
`ses_e2186e745ffecK1Ilg4cw26pVu` or another genuinely distinct nonauthor in a
separate checkout. Author cannot self-review.

## Exact review commands

Use the authorized Python and your own scratch:

```text
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
CFG=/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json
```

1. Pin source and frozen assets:

```text
git rev-parse HEAD
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_task_packets_20261112.json
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_gmt_overlay_20261112.json
```

Frozen #1095 blobs must remain `d971b6ea…`, `f76c0d90…`, `17cfae53…`,
`474befcb…`.

2. Run the mechanism tests and correctness probe:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
"$PY" WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/probes/r2_correctness_probe.py
```

Expected: `17 passed`; correctness probe `PASS`.

3. Run the reviewer’s unchanged negative oracle separately and preserve its raw
exit/output; do not call it green if it expects the old bug:

```text
"$PY" WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R2/probes/currentness_gap_probe.py
```

Expected raw outcomes now include: fake task review refused, mechanism review
`REVIEW_SUPERVISED_RUN_REQUIRED`, arbitrary STOP/RESUME refused, arbitrary
resolve refused, live-source tokens present. Its hardcoded historical
`REVISE_EXACT_DEFECT` verdict is not a new product verdict.

4. Run the local equivalents of the authorized checks (macOS, not Ubuntu/Actions):

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

Expected exit `0` for each. This is local compatibility, not hosted-CI PASS.

5. Inspect the live GitHub source and the current visible holds:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
```

Expected: a live observation with `source_trust=AUTHENTICATED_LIVE_GITHUB`,
`fetched_at_utc`/`expires_at_utc`/`evidence_digest`, PR status `200` where
available, and explicit issue/comment `HTTP 403` holds. The local baseline
mtime is never used as source truth. Current visible items include the real
`GITHUB_PR_STATUS_ADVANCED pr:1095` and the three issue status holds. Status
returns `2` while those holds remain.

## The actual corrected-source review must be a real supervised run

Do not intaken an arbitrary caller JSON as a review. Bind the same installed
controller hook to a distinct REVIEWER run with this `sorok_currentness` shape:

```json
{
  "runtime_script": "/absolute/.../SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py",
  "config_path": "/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json",
  "python": "/private/tmp/rawlsing-oct28-p1r1/venv/bin/python",
  "return_filename": "WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R2_G5/REVIEW_RECEIPT.json",
  "task_id": "AUTOMATIC_CURRENTNESS_R1",
  "role": "REVIEWER",
  "expected_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
  "expected_source_commit": "<corrected source commit from WORKER_RETURN.json>",
  "scope": "FOCUSED_SOURCE_CORRECTION_RECEIVING_ONLY"
}
```

The real controller completion will make the installed hook call
`intake-completion --run-dir <real run>`. The runtime infers role `REVIEWER`,
requires the real job/binding/launch/process/completion and return artifact,
verifies the reviewer session/source/role/task and the immutable
`VERDICT.json`, and sets `mechanism_review` to the scoped verdict. A reviewer
receipt that points only at source code or uses caller-only trust/session
strings refuses.

Reviewer receipt requirements:

- Commit the review evidence first (an evidence commit containing `VERDICT.json`
  and your `REVIEW_RECEIPT.json`; no self-reference).
- `task_id: AUTOMATIC_CURRENTNESS_R1`
- `implementation_commit`: corrected source commit
- `implementation_code_sha`: corrected runtime git blob
- `author_session: ses_e21a481bfffefyvpxaeFaAOFvQ`
- `reviewer_session`: your distinct session
- `review_commit`: the frozen evidence commit
- `verdict`: `ACCEPT_SCOPED_SOURCEFREE`, `REVISE_EXACT_DEFECT` or
  `HOLD_SOURCE_AUTHORITY`
- `scope`: exact corrected-mechanism scope
- `full_original_claim: NOT_ESTABLISHED`
- `protected_ci: UNAVAILABLE_BILLING`
- `adoption: PENDING_PROTECTED_CI_AND_ADOPTION`
- `source_documents`: runtime/test paths at `review_commit` plus
  `VERDICT.json`; the verdict must match the receipt.

The old ac09 `REVISE_EXACT_DEFECT` review is already recorded separately as a
posthoc real controller-run history under `mechanism_review_original`; it is
not acceptance of this corrected source.

## HQ post-review restart

After the real reviewer exits and the hook records intake:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" startup
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
```

A fresh process must show the new generation/checkpoint, the corrected-source
verdict in `mechanism_review`, the real implementer return in
`mechanism_worker_return` (`RETURNED_REVIEW_PENDING` before review), the 27 task
readiness and 21 decision-node holds, and any remaining live-source HOLDs. No
protected adoption, CI PASS or auto-dispatch is inferred.

## Nonclaims

No native science, actor/human authority, protected merge, hosted-CI PASS, new
ledger/world store/scheduler/fleet, account/provider change or Browser/PYAT/SEAM
operation.
