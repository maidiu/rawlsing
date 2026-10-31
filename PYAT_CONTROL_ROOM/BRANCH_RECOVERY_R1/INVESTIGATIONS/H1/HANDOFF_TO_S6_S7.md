# H1 handoff to S6 #533 and S7 #538

## Exact H1 package

- Branch: `review/pyat-845-s1-s5-independent-hostile-court-20261030-r1`
- Startup: `750548ddbb9b4392a16ce93097b856f349e16182`
- Actual current PRE-MAIN checked: `5fc1d43e3d5412194d1f1eaa30ff448f84635e99`
- Original S1–S5: `c85db397…`, `ab303ee4…`, `65b83dee…`, `8f4ad92a…`, `1aa04078…`
- Corrected S1–S5: `6a658ad3…`, `3042fca8…`, `ebdb51a5…`, `d93e8c24…`, `32dac59b…`
- Shared evidence law: `f50651a2bb0758e9fe6d6a2852441dcc782344be`
- H1 challenge rows: **2,146** (2,138 function claims, 5 court receipts, 2 custody-schema rows, 1 current-receiver partial receipt)
- H1 branch/function custody: **845 branches**, **3,135 function rows** across five shards; original/corrected counts preserved.

The exact H1 branch SHA is reported externally after push. Do not substitute it from the branch name.

## H1 verdict matrix for S6

| Input | H1 verdict | S6 instruction |
|---|---|---|
| S1 150 `CURRENT_PRODUCTION_ACCEPTED_AT_NAMED_SCOPE` | `ENGINEERING_REVISE__ROW_SCOPE_CURRENT_ACCEPTANCE_UNPROVEN` | Do not treat as row-level current production acceptance. H1's 105 current module tests are partial coverage only. 27 rows are outside those modules and require row-level tests. |
| S4 325 `RENAMED_EQUIVALENT_PROVEN` | `ENGINEERING_RED__RENAMED_EQUIVALENCE_UNPROVEN__E1_ONLY` | Downgrade to `RENAMED_BODY_EXACT__BEHAVIOR_UNPROVEN`; 325/325 have E1 only, empty first consumer, no positive/fault-negative tests, zero receipts; 323/325 original paths are WORKER_RETURNS test/corpus. |
| S3 seam court | `ENGINEERING_ACCEPT_NEGATIVE__REPRODUCED_26_PASS_1_FAIL` | Preserve the exact seam failure. Do not combine with unrelated test rows. |
| S3 PE strict | `ENGINEERING_ACCEPT_NEGATIVE__REPRODUCED_4_PASS_9_FAIL` | Preserve the nine strict failures and the reverse-scoped issuer forgery failure. |
| S3 V2K | `ENGINEERING_ACCEPT_NEGATIVE__REPRODUCED_COLLECTION_ERROR_EXIT_2` | Restore the missing exact dependency before any replay; do not count collection as pass. |
| S3 selected-world / E03 | `ENGINEERING_ACCEPT_SCOPED__24_PASS` / `18_PASS` | Keep at sourcefree declared scope; no whole N9/N10W, native or GT2 promotion. |
| S3 398 / S4 897 custody | `CUSTODY_ACCEPT_WITH_SCHEMA_GAP__0_ATTRIBUTE_MISMATCH` | S3/S4 lack `original_row_sha256`; direct attribute comparison matched 398/398 and 897/897. Add the hash field in the next schema revision. |
| S5 119 READY | `ENGINEERING_RED__READY_WITHOUT_CURRENT_TESTS` | Do not grandfather; current ABI/first consumer/fault-negative execution is absent. |
| Original SUPERSEDED (89 total) | 88 `REVISE__SUPERIORITY_UNPROVEN`, 1 preserved specific defect | Do not promote any as superior without current behavior + positive/fault-negative receipt. |
| Original HELD (555 total) | 546 operation-specific `REVISE`, 9 preserved specific defects | Replace blanket holds with exact operation/issuer; allow lawful sourcefree tests. |
| Original adaptation/uniqueness (713 total) | `HOLD__UNIQUE_VALUE_AND_CURRENT_TESTS_UNPROVEN` | HYPOTHESIZED_VALUE only; no READY or unique capability claim. |
| Original INVALID/TRASH (187 total) | 16 preserved specific defects; 171 flat trash downgraded to evidence-only/insufficient | Preserve the 28 total specific defective blocks (16 original trash labels + 9 S4 held + 3 S3 adaptation); do not broaden to unrelated helpers. |

## S6 #533 cross-shard join requirements

1. Unify function families across S1–S5 using exact path/blob/AST/behavior evidence; do not count inherited branch copies as unique functions.
2. Include the R61/P41 and cross-shard precedent cases: original C3 six-blob vs PR526 decoder snapshot and R9 broker; E03 byte-identity with P41 vendor but larger P41 service not integrated; R61-R09 child-authored forged capture RED; F7/P07 alias and unauthenticated receipt/unsafe C. H1 does not adjudicate these; it preserves them.
3. Treat S1/S4 corrected labels as **evidence inputs**, not S6 conclusions. In particular, S1's 150 current-production labels and S4's 325 renamed-equivalence labels are downgraded by H1.
4. Preserve the 28 specific defective blocks and the S3 seam/PE/V2K negative receipts; do not let a shard-level aggregate erase them.
5. Recheck current PRE-MAIN after S6 starts. If `rawlsing_next` moved, rerun the current-presence comparisons and the relevant sourcefree receivers.

## S7 #538 acceptance gates

- No `READY`, `SUPERSEDED_BETTER`, `INDEPENDENTLY_REBUILT_EQUIVALENT` or `TRASH` may be accepted without the exact positive/negative/current-receiver evidence required by `f50651a2…`.
- Source-native read, scientific rule issue, model use, world structural admission, N11/N12 and Sorok actor remain separate ungranted authorities; no S6/S7 action may self-issue them.
- The final product must retain all 845 branches and 3,135 original function claims, with contradictions preserved and no silent loss.
- Any current production acceptance must include current integration and executed current-receiver tests at the exact SHA; historical reviewer acceptance is not current adoption.

No merge, no PRE-MAIN mutation, no source/actor issuance, no self-adoption.
