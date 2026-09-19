# EE-P2X governed local execution return

Status: `BLOCKED__COMMON_COURT_AUTHORITY`

Exact terminal:

`EE_P2X_LITS_I_A_S02_C11_REACHABILITY__COMMON_COURT_AUTHORITY_FAILURE`

## Authority and runtime

Live HQ checkpoint `20260919T0111-0400` was resolved from the control branch, with immutable handoff `6986ce4187f35a9be354f6d47d6b46cc1ac83f17`, semantic PRE-MAIN `1dcd2a79dd6d4208738f655ab7fe4e71c219e354`, and decisions `HQD-2026-09-19-075` / `HQD-2026-09-19-076`. The exact P2X branch started at fan-in head `548d7ae9be4a8a624601b5d468fb2e19693ca597`.

Preflight passed on Darwin x86_64 / CPython 3.11.3 with `pyreadstat==1.3.6` and `pyarrow==25.0.1`. The exact carriers were hash-verified before source use:

- LiTS-I: `7cac43e2ca5b31cb658dc2b3a6cfbcec99363ca8c47da457df90e31b588efc09`
- WVS7: `2bd2a20fc565e7e7b4b2030fd8457db4d0d88160c5ee5186e9ea6c267209af7d`

The qualified driver, reducer, R6S backend, projection materializer, LiTS support, and WVS runtime package were not modified.

## Exact common-court blocker

The resumed driver entered the authorized first unfinished stage:

`LITS_I/A/S02_C11_REACHABILITY`

The exact backend attempted to deploy the pinned immutable R5B authority from commit `3ce639e1a8ab0ad48954c0aeff4b5c42f3d0b06f` and failed closed because this required path is unavailable at that immutable commit:

`data/ddm_build_copy/recovery_integration/semantic_relation_R1_through_Job3/R1_20260825/AS4I0_CHETIRI_ROUTE_B_PRODUCTION_DRIVER_20260827/AS2A_LITS1_SHARED_CERTIFICATION_20260827/01_LITS1_1198_SLOT_OWNERSHIP_PROJECTION_EXCLUSION_LEDGER.csv`

The commit contains the `banked_as2a` authority path instead; no path substitution, backend patch, semantic inference, or fallback was made. The driver produced the candidate-neutral `COURT_UNTIL_RESUME` failure receipt and stopped the court before any candidate measurement or WVS execution.

The driver-bound final verifier returned:

`EE_P2X_LITS_I_A_S02_C11_REACHABILITY__COMMON_COURT_AUTHORITY_FAILURE`

The synchronized ledger hash is `830df67a3f1e3eb6b3a70016bd60dce576b1f658ca1dcbff5f5090db6fea00e1`; the exact LITS-I/A supervisor token is preserved under `LOCAL_COURT/supervisor_tokens/`.

## Preserved bounded attempts

An earlier preflight-valid attempt on the same branch was separately committed as `62fac68505e2295ef16429f50dc87e25fd46688f`. It was classified as an infrastructure nonresult because the isolated environment lacked supporting `duckdb` and `pandas`; its typed receipts are preserved in `LOCAL_COURT/` and `14_LOCAL_ATTEMPT_20260919_RUNTIME_DEPENDENCY_BLOCKER.json`. Supporting packages were then co-located, and the fresh continuation reached the common authority blocker above.

## Boundaries

- No Lock1 or Lock2 mutation.
- No candidate, workload, semantic, routing, lifecycle, or harness redesign.
- No ranking, score, recommendation, selection, surrogate metric, or cross-source pooling.
- No WVS carrier execution after the common-court stop.
- No historic learned-product substitution.
- No successful `S17` terminal; driver `--verify-only` was not run because S17 was never lawfully terminal.

Required wake: repair/re-authorize the exact pinned backend authority path, then resume from `LITS_I/A/S02_C11_REACHABILITY` on this same branch.
