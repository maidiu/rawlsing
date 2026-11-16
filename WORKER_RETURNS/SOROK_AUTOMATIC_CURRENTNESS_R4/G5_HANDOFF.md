# SOROK automatic currentness R4 — focused G5 handoff

**Candidate:** R4 launch-enrollment/session correction on
`codex/sorok-automatic-currentness-launch-auth-20261116-r4`.
**Exact source/artifact:** `WORKER_RETURN.json` and the HQ notification.
**Base:** `a60bffc293cf8805cd80fc2a95e4e0369be916c3` (real R3 review intake,
generation 52).
**Rejected R3 source:** `0b2664a8353f5957e1dad4bb5678be66fa9470ef`.
**R3 review:** `b83438438dcb82eec43d23f170cf5672269edf54`, evidence
`a49be6e8bf728262dad62753f3066e99351b7af9`, path
`WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R3_G5/`,
`REVISE_EXACT_DEFECT`.
**Required reviewer:** same independent nonauthor
`ses_e2186e745ffecK1Ilg4cw26pVu`, or another genuinely distinct nonauthor in a
separate checkout. The author cannot self-review.

## Exact local review commands

Use the authorized Python and your own scratch/worktree:

```text
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
CFG=/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json
```

Pin source and frozen assets:

```text
git rev-parse HEAD
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
git hash-object WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R4/tests/test_launch_auth_boundary.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_task_packets_20261112.json
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_gmt_overlay_20261112.json
```

Frozen #1095 blobs must remain `d971b6ea…`, `f76c0d90…`, `17cfae53…`,
`474befcb…`.

Run the full focused suite:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py \
  WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R3/tests/test_material_auth_boundary.py \
  WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R4/tests/test_launch_auth_boundary.py
```

Expected: `34 passed` (28 prior + 6 R4).

Run the exact hostile witness and the launcher proof variants:

```text
"$PY" -B WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R4/probes/fake_attest_witness.py
"$PY" -B WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R4/probes/launcher_proof_variants.py
"$PY" -B WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R4/probes/installed_launcher_positive.py
```

Expected: witness `PASS` (old fake attestation and fake review accepted; corrected
exact fake refused at actual-session, matching-session fake refused for missing
launcher proof, corrected fake review `UNTRUSTED_CONTROLLER_RUN`); proof variants
`PASS` (exact accepted; path/byte-copy/hash/token/session/job/source/role
tampering refused); installed launcher positive `PASS`.

Run the retained R2/R3 probes from your own scratch; do not rewrite the frozen
R3 evidence. Expected: material `7 fixed / 0 gaps / PASS`; fake reviewer
`UNTRUSTED_CONTROLLER_RUN`.

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

Expected exit `0`; changed `WORKER_COMMISSIONS` zero. These are local checks, not
hosted-CI PASS or protected adoption.

## Actual review run

The review must be a real supervised `REVIEWER` run launched by the installed,
patched controller launcher. The binding `sorok_currentness` object is:

```json
{
  "runtime_script": "/Users/matthewsmith/.codex/worktrees/sorok1037-b-receipt-g5/Rawlsing/SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py",
  "config_path": "/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json",
  "python": "/private/tmp/rawlsing-oct28-p1r1/venv/bin/python",
  "return_filename": "WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R4_G5/REVIEW_RECEIPT.json",
  "task_id": "AUTOMATIC_CURRENTNESS_R1",
  "role": "REVIEWER",
  "expected_session": "ses_e2186e745ffecK1Ilg4cw26pVu",
  "expected_source_commit": "<R4 source commit from WORKER_RETURN.json>",
  "scope": "FOCUSED_LAUNCH_AUTH_RECEIVING_ONLY"
}
```

The patched installed launcher (`cfd180ac…`) computes the exact path/hash and
HMAC launch-spec proof automatically from the fixed local key/identity files.
If that controller/key is unavailable, HQ may explicitly enroll the real
already-running review job with the signed operator authorization; never use a
caller-authored `launch.py`, byte-copy, own PID tree, or unsigned operator file.

The review receipt must have:

- `task_id: AUTOMATIC_CURRENTNESS_R1`
- `implementation_commit`: R4 source commit
- `implementation_code_sha`: R4 runtime git blob
- `author_session: ses_e21a481bfffefyvpxaeFaAOFvQ`
- `reviewer_session`: this reviewer's actual run session
- `review_commit`: frozen evidence commit containing `VERDICT.json`
- `verdict`: `ACCEPT_SCOPED_SOURCEFREE`, `REVISE_EXACT_DEFECT` or
  `HOLD_SOURCE_AUTHORITY`
- `scope`: exact focused launch-auth scope
- `full_original_claim: NOT_ESTABLISHED`
- `protected_ci: UNAVAILABLE_BILLING`
- `adoption: PENDING_PROTECTED_CI_AND_ADOPTION`
- `source_documents`: runtime/test at `review_commit`, plus `VERDICT.json`;
  the receipt verdict must exactly equal the verdict artifact.

The actual run `job.session` must equal `receipt.reviewer_session` and the
binding `expected_session`; it must differ from `receipt.author_session`. The
runtime must also match the binding role/task/expected source, the trusted
registry entry, and the exact review artifact. Expected fields alone are not
enough.

## HQ cold restart

After the real R4 worker exit and after any real reviewer run:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" startup
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
```

Verify the new generation/checkpoint, R4 `mechanism_worker_return`, the actual
review verdict, 27 task readiness, 21 decision-node holds, the legacy R3
attestation and R4 migration provenance, and the visible GitHub source holds.
`status` returns `2` while reconciliation items remain. No protected adoption,
CI PASS, native science, actor/human authority or full original claim is
inferred.

## Nonclaims

No native science, actor/human authority, protected merge, hosted-CI PASS, new
ledger/world store/scheduler/fleet, account/provider change or Browser/PYAT/SEAM
operation. No #1095 G5 rerun. No new author cycle beyond this focused correction.
