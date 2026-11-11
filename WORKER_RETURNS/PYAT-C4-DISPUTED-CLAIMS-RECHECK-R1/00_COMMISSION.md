# LAUNCH IN: OpenCode — Space Bunny Free
# ROLE: PYAT C4 — DISPUTED-CLAIMS INDEPENDENT RE-CHECK — R2 (CORRECTED)
# REPOSITORY: maidiu/rawlsing

Branch:
`agent/opencode-pyat-hq183-c4-disputed-claims-recheck-r1`

## Lineage — read this first

This commission supersedes R1. The branch has MOVED.

- R1 commissioned tip: `dd00896848c98de5e6ff124fd50f8508431fc0ff`
- Current branch tip: fetch it; do not assume
- The commissioned tip REMAINS AN ANCESTOR of the current tip
- NO force-push was used; the anchor is intact
- `commits-over-commissioned-tip` remains exactly computable with
  `git rev-list --count dd00896848c98de5e6ff124fd50f8508431fc0ff..HEAD`

Verify the lineage yourself before reviewing. Report the actual tip you saw.

## Packet under review

Read `PYAT_CONTROL_ROOM/SPACE_BUNNY_OPENCODE_R1/ACTIVATION_RETURNS/OPS-04/01_CORRECTED_DECISION_CLAIMS.md`.

It supersedes `00_C4_CONSOLIDATED_DECISION_CLAIMS.md` on finding **C1 only**.
C2–C5 stand. Both documents are preserved; the earlier one is history.

## Hard prohibitions

Do not execute C4. Do not access, hash, stat, inspect, decode or materialize
any raw survey source. Do not discover or fill source locators. Do not issue
or alter a warrant. Do not mutate production code. Do not adopt the freeze,
lift HQ182's hold, or self-adopt. Do not rerun the C4 review.

`python3` works on this host (3.11.3). Prefer it for JSON and Git plumbing.

## C1 — withdrawn. Try to break the withdrawal.

HQ183 claimed Sol's shadow HQ byte-identity justification was false. HQ186
**withdrew that in full**. Reproduce the comparisons:

| File | `46f3bec82` | freeze `8ff40d37d` |
|---|---|---|
| `rawlsing_next/pre553_route_b_production.py` | `2385cd32…` | `2385cd32…` |
| `rawlsing_next/pre553_carrier_execution.py` | `e7cda773…` | `e7cda773…` |
| `rawlsing_next/tests/test_pre553_route_b_production.py` | `d244eaaa…` | `d244eaaa…` |
| `rawlsing_next/tests/test_pre553_carrier_execution.py` | `bc0db646…` | `bc0db646…` |

Producer at M01 court-run head `74a067742a370d4f6296c56140c28cc8acc53e63`
= `2385cd32…`, identical to the freeze. `74a06774` changed only
`.rabochii/court_spec.json`, repointing `semantic_candidate_sha` from
`a1545aee` to `46f3bec82`, whose `tests` array is the four bounded-court files.

Confirm or refute. Specifically: does any M01 court rebind bind the 61/61 to
bytes OTHER than the freeze's? If you find one, that is a counterexample and
C1 must be reinstated.

Also judge: was HQ's error (reading the first binding `295d270c3` instead of
the final `74a06774`) a genuine miss, and is "recurring failure mode"
a fair self-characterization given HQ182's C2?

## C2 — R7 wording and reproduction

Read `01_ENVIRONMENT_LOCK.json` at `1df64cc59` in full. Confirm the exact
wording is "from this path alone", that it continues "The reproducible
content is the freeze below, not the path", and that a pinned 13-package
`reproduce_command` exists. State the residual class: environment
irreproducibility, fingerprint incompleteness, or both.

## C3 — hash census

Census every hex-valued string in that lock. Assert: 32 values of 16 hex,
all field-named `*_prefix16`; 6 of 32 hex (1 `base_interpreter_sha256_prefix32`,
5 `compiled_extensions.*.cpython-311-darwin.so` with no prefix marker); 2 of
40 hex that are complete Git SHA-1 tree identities
(`no_repo_mutation.rawlsing_next_tree_before/_after`, both `b0c1ab47…`); and
3 complete 64-hex values equal to `9cde8e5ab9abba…`. Confirm or correct.

## C4 — R9 precise gap

Compare C4B `07_UNSIGNED_SOURCE_WARRANT_TEMPLATE.json` at `c2af4f61`, the
candidate `04_SOURCE_EXECUTION_WARRANT_CANDIDATE.json` at `8ff40d37d`, and
`07_EXECUTION_ACCOUNTING_AND_FAILURE_LAW.json`. Confirm that per-source
constraints survive (artifact 07's 8 sources with `expected_full_reads`,
`expected_selected_reads`, `max_retry_budget`, `retry_law`) and that only
explicit per-source read-limit counters are absent from the warrant.

## C5 — R10 digest

Recover `T3_freeze_sha256` from C4B `04_WVS_ORACLE_CUSTODY.json`. Assert
`7dfb62362b983b92dee2774d862a46c0c0ce3ca2c3bb48850e0f400346936908`. Do not guess.

## Also check

- The HQ185 pointer repair: `LATEST.json` previously claimed HQD-185 while
  pointing at the HQ184 checkpoint with an unsealed `handoff_commit`. Confirm
  the current `LATEST.json` is internally coherent: `checkpoint_id`,
  `current_md_path`, `current_json_path`, `manifest_path`, `handoff_commit`
  and `pyat_review_adjudication_decision` must all agree, and the named
  checkpoint must exist with a MANIFEST whose blob SHAs match the actual
  blobs.
- Whether any of C2–C5 suffers the same inference-from-truncated-evidence
  failure mode as C1.

## Return

Write only `WORKER_RETURNS/PYAT-C4-DISPUTED-CLAIMS-RECHECK-R1/**`:
`00_RECHECK.md`, `01_C1_WITHDRAWAL_REVIEW.json`, `02_C2_R7_WORDING.json`,
`03_C3_HASH_CENSUS.json`, `04_C4_R9_GAP.json`, `05_C5_R10_DIGEST.json`,
`06_POINTER_AND_LINEAGE_INTEGRITY.json`, `07_FINAL_DISPOSITION.json`.

Dispositions: `ALL_UPHELD`, `UPHELD_WITH_CORRECTIONS`, `MATERIAL_CORRECTION_REQUIRED`,
`INSUFFICIENT_EVIDENCE`.

Terminal: `C4_DISPUTED_CLAIMS_RECHECK_R2_RETURNED__HQ_ADJUDICATION_REQUIRED`
