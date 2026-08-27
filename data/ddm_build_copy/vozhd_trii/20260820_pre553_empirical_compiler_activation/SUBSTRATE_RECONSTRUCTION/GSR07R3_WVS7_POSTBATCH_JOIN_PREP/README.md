# G-SR07-R3 WVS7 post-batch join / relaunch harness prep

Status: `PREPARED__NO_W1_W6_BATCH_FACTS_CONSUMED__HQ_FINAL_RETURN_INPUT_REQUIRED`

This directory is **Lane 12 only**. It implements the deterministic machinery authorized by HQ26 after reading the Trii front door/Route-A anti-drift law, accepted Lane A/B/C law, and Authorities 83/84. It never fetches W1-W6 branches and contains no documentary country findings from those workers.

## Join entry point

```bash
python3 wvs7_postbatch_join.py HQ_JOIN_REQUEST.json --output WVS7_POSTBATCH_JOIN_REPORT.json
```

Use `--report-only` only when HQ intentionally wants a deterministic blocked report that surfaces unresolved contradictions/UNKNOWNs before substantive adjudication. Normal mode exits fail-closed unless relaunch preflight is `PASS`.

## Exact HQ inputs after all six final returns exist

1. Six **final** W1-W6 commit SHAs and exact terminal tokens.
2. SHA-256 for every Authority-83 required batch file: `RESULT.md`, `RESULT.json`, `COUNTRY_DOCUMENT_AUTHORITY.csv`, `COUNTRY_UNIVERSE_RECOVERY.csv`, `ROUTING_DOCUMENTARY_RECOVERY.csv`, `DOCUMENT_IDENTITY_AND_PROVENANCE.csv`, `UNRESOLVED_GAPS.csv`, `CHANGED_FILES.txt`.
3. A lossless normalized country bundle for each exact Authority-83 country/year. Every normalized record carries `source_locator` back to the final batch file/row; no semantic inference is permitted in normalization.
4. Explicit HQ D03 adjudication package for the frozen person-position targets, with accepted authority ref + content SHA-256.
5. Exact D11 `EmpiricalUniverse` binding for all 66 Lane-C source-present country/year identities, including Australia, with accepted authority ref + content SHA-256.
6. Exact D12 replay-binding manifest(s) whose country coverage union is the same 66-country source-present universe, including source snapshot, row-ordinal binding and manifest SHA-256.
7. HQ adjudication receipts for every surfaced documentary/dedup contradiction.
8. HQ disposition receipts for every mechanically derived UNKNOWN: `BLOCKING`, `NONBLOCKING_EXCLUDED`, or `RESOLVED_WITH_ACCEPTED_AUTHORITY`. The harness rejects dispositions for unknown IDs not backed by final batch unresolved evidence.

## Mechanical gates

- exact six-batch presence;
- exact Authority-83 batch/country membership and 65-country recovery union;
- duplicate/missing country rejection;
- exact required batch-file manifest + SHA-256 shape;
- documentary identity/provenance validation and deterministic dedupe;
- conflicting document identities are surfaced as contradictions, never resolved silently;
- D01-D02/D04-D10 must have an explicit record per country (`NOT_APPLICABLE_TO_CLAIM` is a record, not absence);
- routing records may reference only the frozen Lane-B rule family IDs authorized for that gap;
- D03/D11/D12 are separate HQ surfaces, not worker facts;
- the recovery union is exactly the 65 Authority-83 batch countries and the separately frozen source-present universe is exactly 66 including Australia;
- D11 and D12 each cover that exact 66-country source-present universe;
- unresolved evidence must appear in the UNKNOWN ledger, and every UNKNOWN must be traceable to an unresolved evidence record;
- final package is canonical-JSON content addressed by SHA-256.

## What remains substantive HQ adjudication

Mechanical joining cannot decide: conflicting source-owner documents; D03 person-position presence/binding authority; which exact accepted `EmpiricalUniverse` ref closes each D11 country; exact D12 scoped-respondent/source-snapshot/row-ordinal replay authority; whether a residual UNKNOWN is lawfully nonblocking/excluded or remains a certification blocker; or whether documentary closure is substantively sufficient to authorize G-SR07 relaunch. Those require HQ authority, not code inference.

## Synthetic tests

`test_wvs7_postbatch_join.py` creates only in-memory `NON_AUTHORITATIVE_SYNTHETIC_ONLY` returns. No W1-W6 branch or output is read.
