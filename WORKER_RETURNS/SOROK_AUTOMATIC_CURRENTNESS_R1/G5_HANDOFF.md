# SOROK automatic currentness R1 — G5 handoff

**Candidate:** the commit containing this return on
`codex/sorok-automatic-currentness-engine-20261115-r1`
**Base:** `75581fa9e2c8576d1ca9a7a9a18759ea840d82e8`
**Author:** `ses_e21a481bfffefyvpxaeFaAOFvQ` (not reviewer)
**Required reviewer:** `ses_e2186e745ffecK1Ilg4cw26pVu` or another
genuinely distinct nonauthor session in a separate checkout.
**Author cannot self-review.**

## Frozen implementation

```text
SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py
  blob 6164e595efcd176bb2ec9b75aa99074472a4c9b4
  sha256 622c4187b2332d85a221bb1e1b39db4f70e833afc5cf0d55aa2a540d654ae337
SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
  blob 38465315646d3a4deec68ddff87651ca47f5f89b
  sha256 219226fefda8fc74afe0f8e8df87e0d67ce0ad83c487dbe7afd6860e8c882f8f
```

Frozen #1095 assets must remain exact:
verifier `d971b6ea...`, workflow `f76c0d90...`, task source `17cfae53...`,
GMT source `474befcb...`.

## Exact review commands

Use your own scratch and the authorized Python. Do not edit product.

```text
PY=/private/tmp/rawlsing-oct28-p1r1/venv/bin/python
CFG=/Users/matthewsmith/.local/state/rawlsing-controller/sorok-01a161c5/sorok-automatic-currentness-20261115/currentness/config.json
```

1. Pin the candidate and frozen sources:

```text
git rev-parse HEAD
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_task_packets_20261112.json
git hash-object SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/CURRENTNESS_FROZEN_SOURCE_R1/original_gmt_overlay_20261112.json
```

2. Run the mechanism tests:

```text
"$PY" -m pytest -p no:cacheprovider -q \
  SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py
```

Expected: `15 passed`. Add your own negative witness if useful; do not rewrite
the author tests.

3. Run the canonical local validators (not a new #1095 G5):

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/verify_operational_currentness_r1.py \
  --self-test --status
"$PY" CROSS_HQ_CONTROL_ROOM/PROGRAMMA/verify_canonical_programma_r1.py
```

Expected: both exit 0. The frozen verifier's own `SOROK_CURRENTNESS_NOT_LIVE`
line is historical and must remain; it does not describe this runtime.

4. Cold readout and restart:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" startup
```

Expected: generation/checkpoint, frozen projection preserved, verified
receiving/scoped READY, HOLDs with owners, exact unmet prerequisites, scoped
review pins, `PENDING_PROTECTED_CI_AND_ADOPTION`, and
`PENDING_EXTERNAL_NONAUTHOR_REVIEW` for this mechanism. `startup` returns `0`
when no reconciliation item remains; `2` is typed reconciliation required.

5. Test your own real return intake on a sandbox pair, not the frozen pair:

```text
# copy CURRENT_PROGRESS.json/.md and CURRENTNESS_FROZEN_SOURCE_R1 to a temp root,
# write a runtime config with repo_root/pair paths/state_root for that temp root,
# run runtime init, then launch a finite local controller child with notify=False
# and a binding `sorok_currentness` object pointing at that config.
```

The author used exactly this shape; see
`evidence/COMMANDS.txt`, `evidence/child/` and `evidence/controller_runs/`.
A real child exit `0` must appear as `RETURNED_REVIEW_PENDING`, never
acceptance. The installed controller hook is optional and SOROK-only; it can be
restored with:

```text
"$PY" WORKER_RETURNS/SOROK_AUTOMATIC_CURRENTNESS_R1/controller/manage_hook.py restore
```

## Your review receipt

After reviewing, commit a receipt under `WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R1_G5/`
and provide its commit SHA and path. Use this schema exactly:

```json
{
  "schema": "SOROK_CURRENTNESS_REVIEW_RECEIPT@1",
  "task_id": "AUTOMATIC_CURRENTNESS_R1",
  "implementation_commit": "<frozen candidate 40-hex commit>",
  "implementation_code_sha": "6164e595efcd176bb2ec9b75aa99074472a4c9b4",
  "author_session": "ses_e21a481bfffefyvpxaeFaAOFvQ",
  "reviewer_session": "<your distinct nonauthor session>",
  "review_commit": "<your review commit 40-hex>",
  "review_pr": null,
  "verdict": "ACCEPT_SCOPED_SOURCEFREE | REVISE_EXACT_DEFECT | HOLD_SOURCE_AUTHORITY",
  "scope": "<exact admitted operational-currentness mechanism scope>",
  "grade": "SOURCEFREE_S2_ONLY",
  "full_original_claim": "NOT_ESTABLISHED",
  "protected_ci": "UNAVAILABLE_BILLING",
  "adoption": "PENDING_PROTECTED_CI_AND_ADOPTION",
  "source_trust": "REAL_LOCAL_NONAUTHOR_REVIEW",
  "source_documents": [
    {"path": "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py",
     "git_blob": "6164e595efcd176bb2ec9b75aa99074472a4c9b4"},
    {"path": "SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/test_operational_currentness_runtime_r1.py",
     "git_blob": "38465315646d3a4deec68ddff87651ca47f5f89b"}
  ]
}
```

`review_commit` and every `source_documents[].git_blob` are verified with git;
wrong source, self-review, scope inflation, stale commit or missing document
refuses with a typed error. `full_original_claim` must remain
`NOT_ESTABLISHED`. `protected_ci` must not claim PASS unless hosted CI actually
passed; this account currently has CI unavailable, so keep
`UNAVAILABLE_BILLING`.

## HQ post-review commands

After the reviewer commits the receipt, HQ feeds it to the same runtime:

```text
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" intake-review \
  --receipt WORKER_REVIEWS/SOROK_AUTOMATIC_CURRENTNESS_R1_G5/REVIEW_RECEIPT.json
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" startup
"$PY" SOROK_PRODUCT_CONTROL_ROOM/PROGRAMMA_SOROK/operational_currentness_runtime_r1.py \
  --config "$CFG" status
```

Expected post-review restart: `mechanism_review.state` becomes
`ACCEPTED_SCOPED_PENDING_HQ_ADOPTION` (or the exact REVISE/HOLD verdict), the
27-task readiness and holds remain separate, and no protected adoption or job
dispatch is inferred. A new generation/checkpoint must be visible in a fresh
process. This is the required end-to-end post-review cold readout.

## Nonclaims

No native science, actor knowledge, human authority, protected merge, hosted-CI
PASS, new ledger/world store/scheduler/fleet, account/provider change or
automatic job dispatch.
