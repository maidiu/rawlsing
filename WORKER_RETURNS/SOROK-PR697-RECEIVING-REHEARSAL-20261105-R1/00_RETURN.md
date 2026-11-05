# SOROK PR697 receiving rehearsal R1

**RESULT:** `PASS` — engineering rehearsal only.

**Grade:** `ENGINEERING_RECEIVING_REHEARSAL_NOT_INDEPENDENT_FINAL_ACCEPTANCE`.

Selective rehearsal of draft PR697 product candidate `da97d2624486b783bf5c4f465b17fdcdea3af20a`
against protected baseline `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`,
performed **only** on rehearsal branch
`codex/sorok-pr697-receiving-rehearsal-20261105-r1`.

No protected PRE-MAIN branch was changed and PR697 was not merged. No product
candidate files were added to the protected baseline. The candidate was
materialized at exact PR-head bytes only under
`.local-logs/pr697-rehearsal/candidate` for execution.

## Exact base, head and merge compatibility

| Field | Value |
|---|---|
| Protected baseline | `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| PR697 head | `da97d2624486b783bf5c4f465b17fdcdea3af20a` |
| Merge base | `8ffec40a6924848a49f95950aa9ce28c27ee3ec1` |
| `git merge-tree --write-tree` | exit `0`, tree `65d7083a774ad4d3415f38382f61871b14369947` |
| Compatibility | `COMPATIBLE` |

## Changed path allowlist

PR diff is **497 additions, 0 modifications, 0 deletions**. Every path is under
the permitted new-return/commission roots:

| Prefix | Paths |
|---|---:|
| `WORKER_COMMISSIONS/SOROK-20261105-S45-S47-CANONICAL-SOURCEFREE-PRODUCT-RECEIVING-R1/` | 1 |
| `WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/` | 458 |
| `WORKER_RETURNS/SOROK-S45-S47-PROJECTION-20261105-R1/` | 20 |
| `WORKER_RETURNS/SOROK-S45-S47-CAUSAL-HARNESS-20261105-R1/` | 18 |

**No unrelated protected file change.** Full path list:
`evidence/changed_path_allowlist.json`.

## Candidate materialization and source/import audit

- Candidate materialized from PR head by `git archive` at exact bytes.
- `497/497` candidate files match `git show <head>:<path>` byte-for-byte;
  missing `0`, mismatch `0`, extra `0`:
  `evidence/candidate_materialization.json`.
- Shipped `SOURCE_MANIFEST.json`: `424/424` files present with matching SHA-256;
  problems `[]`: `evidence/manifest.json`, `evidence/manifest_audit.json`.
- Import audit: `284` modules, `175` local shipped modules, `109` stdlib,
  **`0` external checkout/temp/Desktop modules**. Independent scan confirms no
  non-candidate, non-stdlib import rows: `evidence/import_audit_scan.json`.
- Package causal harness supplied its own package-closure audit and confirmed
  modules under the shipped package closure.

## Fresh-process user-facing CLI

Executed from the materialized candidate product with clean environment
(`PYTHONPATH` and all prior source-root variables unset, `python3 -I -B`).

First actual consuming command:

```text
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py new --state <path>
```

Then:

```text
python3 WORKER_RETURNS/SOROK-20261105-S45-S47-PRODUCT-IMPORT-CLOSURE-R1/product/run_s45_s47.py view --state <path> --text
```

Rehearsal sequence `new`, `view --text`, `say "Can I help?"`, `do-help`,
`attend`, `status`, `wait` all exited `0`. `new` produced verify-true root
`3bcb21fc22df3255269382ad249f706dd6dd5378cb886af26542991ff516a4f7`;
`say` returned `HELP_INVITE`; `do-help` returned `HELP_ACCEPT` with actor repair
performed by A; `attend` returned `NO_CHANGE` with no world event; `wait` was a
typed hold. Receipts: `evidence/cli/`.

## Causal demo and receiving-specific regressions

- `run_s45_s47.py demo --root ... --keep` in fresh process: **exit 0**, all 10
  top-level checks true, including S45, ACTUAL, SCHEDULED_ONLY, event-local C9,
  cut/restore, admission-source, cold subprocess, source manifest and import
  closure. Source audit `424/424`; import audit external modules `0`.
  Receipt: `evidence/demo.json`.
- Supplied package-closure causal harness with `--original-tests none`:
  **PASS**, 22/22 checks true, elapsed `64.797s`; package source manifest exact,
  package modules under closure, ACTUAL refused, SCHEDULED_ONLY accepted,
  sever RED, restore PASS, cold replay PASS, wrong-root refusal PASS.
  Receipt: `evidence/causal_harness.json`.
- Projection package tests: **11 passed**, 0 failed/error/skipped in `20.65s`.
  Receipt: `evidence/projection_tests.xml`, `logs/projection_tests.log`.
- Full S45/S46/S47 author suites were intentionally **NOT_RUN** to avoid
  duplicating the already-passed 21/17/17 full-55 suite. No receiving-specific
  failure was observed.

## Source exclusions and native holds

- Grade remains TEST_ONLY sourcefree product closure; `native: false` and all
  native grants false.
- No S48-S52 actual B positive, B personality/context fabrication or paid
  counterpart.
- CAN008 Rule A: not issued.
- CAN011 O05 PRACTICE / O07 NO_CHANGE: not issued.
- Independent ADP person sources: not issued.
- C8 original security and native C9/C12 authority: not issued.
- Pyat native selected world / E001-E002: not issued.
- Human S11/A5 Gate4/Gate5, human usability, external message delivery, paid
  action: not run.
- Independent exact-commit review: NOT_RUN. Final code verdict remains with the
  separate independent reviewer.

## Result and next receiving owner action

**Rehearsal PASS.** Merge-tree compatible, allowlist clean, candidate bytes
exact, manifest/import closure self-contained, user-facing CLI and causal demo
pass in fresh processes, focused receiving regressions pass.

Next receiving owner action:

1. The existing independent reviewer reviews exact PR head
   `da97d2624486b783bf5c4f465b17fdcdea3af20a` and this rehearsal evidence.
2. Only after an independent PASS verdict may the receiving lead prepare a
   selective PRE-MAIN PR. No automatic merge and no protected-branch mutation
   follows from this rehearsal.

This engineering rehearsal is **not** independent final acceptance.

## PROGRAMMA_DELTA

See `PROGRAMMA_DELTA.md` / `PROGRAMMA_DELTA.json`: rehearsal and scoped evidence
only; no PROGRAMMA canonical product, seam/gate register, native science or
receiving authority changed.


## HQ final correction-diff receiving check

Final candidate `41bf45813fd0adeffd9b54e1306c2022abe96514` remains merge-tree compatible with protected baseline `8ffec40a6924848a49f95950aa9ce28c27ee3ec1`; Git produced tree `29b9e99fea0c70722434d2dce2410e8848c1cf5e` with exit 0. HQ checked the exact diff against previously rehearsed `da97d2624486b783bf5c4f465b17fdcdea3af20a`: source manifest and product/vendor blobs are unchanged. Changes are the public new receipt, focused tests, census helper, harness option refusal and associated evidence/documentation.

Actual final CLI privacy and harness behavior were independently checked at this final SHA and ACCEPTED. The immutable review is `f2a4210dbd86ad4ecc3d4633b6cbf5ebf958cc70:WORKER_RETURNS/SOROK-S45-S47-INDEPENDENT-REVIEW-20261105-R1/`. It contains two focused CLI tests, explicit unsupported-option refusals and lawful harness PASS22/22. HQ reused this exact final-head runtime evidence and the preceding full receiving rehearsal, rather than claiming another fresh execution.

No protected write or merge occurred. Next action belongs to the competent PRE-MAIN receiving owner: verify moving base and exact PR697 head, then merge only with explicit authority. Original native, B-context, Pyat and human holds remain. The final incremental worker attempts failed on retryable provider overload before executing; these Git checks were performed by HQ.
