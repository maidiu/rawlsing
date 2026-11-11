# Parity and derived/canonical separation

## Exact small parity (64 rows, one repetition)

Same sourcefree profile, current normal streaming path vs frozen 46b vs protected 4f3413; full actual I03/I05 consumer fingerprints:

| Profile | Actual events | Fingerprint (all three sources) |
|---|---:|---|
| narrow | 128 | `97c93ac12e60729b2b0238fb58b60dbfb654fc9eb99d7e3160bb20a46d132504` |
| repeat | 384 | `adca12059db1c84a99873067d7b2d90e4adbc60c6dc106c2df9407fbb5691cbe` |
| wide | 384 | `4acb0294123fcae22470e0994ade1b0b91dc0bd589190082c9605be1d2bd34d1` |

All three profiles have identical event counts, typed states and full consumer fingerprints across sources. These are actual current consumers; no candidate statistical oracle was hand-built.

## Current 64-row full matrix

For each profile:

```text
cold:          derived miss/write; canonical persist
warm:          derived cache hit; canonical reopen hit (separate)
               normal-consumer fingerprint == canonical-reopen fingerprint
delete/rebuild: derived miss/write and canonical rebuild
```

Verified actual cache facts:

- derived file name: `c11-events-*.parquet`
- derived envelope schema: `PRE553_I02_EVENT_ACCELERATOR@2`
- canonical files: 13 per release under `canonical-carrier/releases/...`
- no canonical file is counted as derived cache hit
- warm derived hit retains the exact file envelope/mtime; warm canonical hit is recorded independently
- corrupt derived file test: safe miss/rewrite, exact release retained, not a false hit

Output `final_matrix_eligible=false`; acceptance `NON_FINAL_DIAGNOSTIC__DO_NOT_REPORT_AS_FULL_MATRIX_PASS` at 64 rows/1 repetition.

## Not run

No 100000/3-repetition matrix was launched in this repair. The prior 100k narrow numbers remain preintegration diagnostics; the final matrix requires independent same-method economic check and final HQ-pinned source SHA.
